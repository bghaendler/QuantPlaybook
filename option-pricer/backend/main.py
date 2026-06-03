# --- START OF FILE backend/main.py ---

from fastapi import FastAPI, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from scipy.stats import norm, multivariate_normal
from scipy.optimize import brentq
from typing import Dict, Any

# Helper for Cumulative Bivariate Normal Distribution
def cbnd(a, b, rho):
    """
    Cumulative Bivariate Normal Distribution with correlation rho.
    Uses scipy.stats.multivariate_normal.
    """
    if abs(rho) >= 1.0:
        if rho > 0:
            return norm.cdf(min(a, b))
        else:
            return max(0, norm.cdf(a) - norm.cdf(-b))
            
    # Standard bivariate normal with mean [0,0] and cov [[1, rho], [rho, 1]]
    mean = [0, 0]
    cov = [[1, rho], [rho, 1]]
    try:
        return multivariate_normal.cdf([a, b], mean=mean, cov=cov)
    except:
        return 0 # Fallback

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class OptionEngine:
    """
    Implements option pricing formulas from Espen Gaarder Haug's
    'The Complete Guide to Option Pricing Formulas' (2nd Ed).
    """
    
    def __init__(self, inputs: Dict[str, Any]):
        self.model = inputs.get('model', 'bsm')
        self.S = float(inputs.get('spot', 100))
        self.K = float(inputs.get('strike', 100))
        self.T = float(inputs.get('time', 1))
        self.r = float(inputs.get('rate', 0.05))
        self.sigma = float(inputs.get('volatility', 0.2))
        
        # The 'dividend' field is overloaded based on the model:
        # - Merton: Dividend Yield (q)
        # - Garman: Foreign Rate (rf)
        # - GenBSM: Carry Deduction (q) -> b = r - q
        # - Brenner: Cost of Carry (b) directly
        # - Black76F: Forward Expiry (Tf)
        self.q_or_rf = float(inputs.get('dividend', 0))
        # Custom input for RGW model
        self.time_dividend = float(inputs.get('time_dividend', 0.25))
        
        # --- NEW: Capture Discrete Dividends for Escrowed model ---
        self.div1_amt = float(inputs.get('div1_amt', 0.0))
        self.div1_time = float(inputs.get('div1_time', 0.0))
        self.div2_amt = float(inputs.get('div2_amt', 0.0))
        self.div2_time = float(inputs.get('div2_time', 0.0))
        
        # --- NEW: Capture Lambda for Executive Stock Options ---
        self.lamb = float(inputs.get('lambda', 0.0))
        
        self.type = inputs.get('type', 'call').lower()
        self.is_call = 1 if self.type == 'call' else -1

        # Barrier specific inputs
        self.H = float(inputs.get('barrier', 0))
        self.barrier_type = inputs.get('barrierType', 'Up-and-Out')
        self.rebate = float(inputs.get('rebate', 0))

        # Modified Bachelier shift parameter
        self.shift = float(inputs.get('shift', 0))

        # Margrabe / Multi-Asset parameters
        self.spot2 = float(inputs.get('spot2', 104.0))
        self.vol2 = float(inputs.get('vol2', 0.12))
        self.dividend2 = float(inputs.get('dividend2', 0.04))
        self.correlation = float(inputs.get('correlation', 0.8))
        self.q1 = float(inputs.get('q1', 1.0))
        self.q2 = float(inputs.get('q2', 1.0))

        # Special handling for Black-76F (Deferred Settlement)
        # T_f is the time to payment, T is time to option expiry.
        if self.model == 'black76f':
            # Ensure T_f >= T. Default to T if input is somehow smaller or missing.
            # In the UI config, we map 'dividend' slider to Tf.
            self.T_f = max(self.q_or_rf, self.T)
        else:
            self.T_f = self.T

        # Avoid division by zero
        if self.T <= 1e-5: self.T = 1e-5
        if self.sigma <= 1e-5: self.sigma = 1e-5

        # Determine Cost of Carry (b) based on Model Type
        self.b = self._determine_cost_of_carry()

    def _determine_cost_of_carry(self):
        """
        Maps the specific model to the Generalized Cost of Carry parameter 'b'.
        Ref: Haug Ch 1.1.6
        """
        if self.model == 'bsm':
            # Black-Scholes (Stock): b = r
            return self.r
        elif self.model == 'merton':
            # Merton (Continuous Dividend): b = r - q
            return self.r - self.q_or_rf
        elif self.model == 'black76':
            # Black-76 (Futures): b = 0
            return 0.0
        elif self.model == 'asay':
            # Asay (Margined Futures): b = 0
            return 0.0
        elif self.model == 'garman':
            # Garman-Kohlhagen (FX): b = r - r_f
            return self.r - self.q_or_rf
        elif self.model == 'brenner':
            # Brenner-Subrahmanyam: Input 'dividend' is explicitly 'b'
            return self.q_or_rf
        elif self.model == 'margrabe':
            # Margrabe: Input 'dividend' is explicitly Asset 1 cost-of-carry 'b1'
            return self.q_or_rf
        elif self.model == 'black76f':
            # Black-76F (Futures with deferred settlement): underlying is Future, so b = 0
            return 0.0
        elif self.model == 'gen_bsm':
            # Generalized BSM: Input treated as 'q', so b = r - q
            return self.r - self.q_or_rf
        elif self.model == 'bachelier':
            # Bachelier (1900): Arithmetic model, typically b = r - q
            return self.r - self.q_or_rf
        elif self.model == 'mod_bachelier':
            # Modified Bachelier: Same as Bachelier, b = r - q
            return self.r - self.q_or_rf
        elif self.model == 'sprenkle':
            # Sprenkle (1964): Uses expected return (mu) instead of r
            # In our implementation, we use r as the expected return
            # Cost of carry is mu (expected return)
            return self.r
        elif self.model == 'boness':
            # Boness (1964): Uses expected return (mu), similar to Sprenkle
            # Cost of carry is mu (expected return)
            return self.r
        elif self.model == 'bjerksund02':
            # Bjerksund-Stensland (2002): Cost of Carry b = r - q
            return self.r - self.q_or_rf
        elif self.model == 'mckean':
             # McKean (Perpetual): Cost of Carry b = r - q
            return self.r - self.q_or_rf
        elif self.model == 'exec_stock':
            # Jennergren & Naslund: Treated as stock with div yield (b = r - q)
            return self.r - self.q_or_rf
        else:
            # Default to BSM (b=r)
            return self.r

    def _d1_d2(self, S, K, T, b, sigma):
        """Standard d1 and d2 calculations."""
        sqrt_T = np.sqrt(T)
        d1 = (np.log(S / K) + (b + 0.5 * sigma ** 2) * T) / (sigma * sqrt_T)
        d2 = d1 - sigma * sqrt_T
        return d1, d2

    def _generalized_bsm(self, S, K, T, r, b, sigma):
        """
        The Generalized Black-Scholes-Merton Formula.
        Ref: Haug Eq 1.11, 1.12
        """
        d1, d2 = self._d1_d2(S, K, T, b, sigma)
        N = norm.cdf
        
        # Discount factors
        ert = np.exp(-r * T)
        ebrt = np.exp((b - r) * T) # This equals exp(-qT) or exp(-rfT) depending on model

        if self.is_call == 1:
            price = S * ebrt * N(d1) - K * ert * N(d2)
        else:
            price = K * ert * N(-d2) - S * ebrt * N(-d1)
            
        return price
    
    def _jennergren_naslund(self, S, K, T, r, b, sigma, lamb):
        """
        Jennergren & Naslund (1993) for Executive Stock Options.
        Valuation includes a survival probability factor (exit rate lambda).
        Formula: Price = exp(-lambda * T) * BSM_Price
        """
        # 1. Calculate Standard European Option Value (Generalized BSM)
        bsm_price = self._generalized_bsm(S, K, T, r, b, sigma)
        
        # 2. Calculate Probability of staying (Survival Factor)
        # Probability = e^(-lambda * T)
        survival_prob = np.exp(-lamb * T)
        
        # 3. Final Value
        return survival_prob * bsm_price

    def _margrabe_price(self, S1, S2, T, r, b1, b2, sigma1, sigma2, rho, q1=1.0, q2=1.0):
        """
        William Margrabe (1978) Exchange Option Pricing Model.
        Values option to exchange asset 2 for asset 1.
        Call Payoff: max(q1 * S1 - q2 * S2, 0)
        Put Payoff: max(q2 * S2 - q1 * S1, 0)
        """
        N = norm.cdf
        # Combined Volatility
        sigma_hat = np.sqrt(max(1e-9, sigma1**2 + sigma2**2 - 2 * rho * sigma1 * sigma2))
        
        sqrt_T = np.sqrt(T)
        d1 = (np.log((q1 * S1) / (q2 * S2)) + (b1 - b2 + 0.5 * sigma_hat**2) * T) / (sigma_hat * sqrt_T)
        d2 = d1 - sigma_hat * sqrt_T
        
        if self.is_call == 1:
            price = q1 * S1 * np.exp((b1 - r) * T) * N(d1) - q2 * S2 * np.exp((b2 - r) * T) * N(d2)
        else:
            price = q2 * S2 * np.exp((b2 - r) * T) * N(-d2) - q1 * S1 * np.exp((b1 - r) * T) * N(-d1)
            
        return price, sigma_hat, d1, d2

    def _escrowed_dividend_price(self, S, K, T, r, sigma):
        # Calculate PV of dividends occurring before expiry T
        div_pv = 0.0
        if self.div1_amt > 0 and self.div1_time < T:
            div_pv += self.div1_amt * np.exp(-r * self.div1_time)
        if self.div2_amt > 0 and self.div2_time < T:
            div_pv += self.div2_amt * np.exp(-r * self.div2_time)
            
        S_adj = max(0.01, S - div_pv)
        # Price is BSM using S_adj with b=r
        price = self._generalized_bsm(S_adj, K, T, r, r, sigma)
        return price, S_adj, div_pv

    def _escrowed_dividend_greeks(self, S, K, T, r, sigma):
        # Retrieve S_adj
        _, S_adj, _ = self._escrowed_dividend_price(S, K, T, r, sigma)
        # Greeks are BSM Greeks evaluated at S_adj with b=r
        return self._analytical_greeks(S_adj, K, T, r, r, sigma)

    def _hhl_vol_adjustment(self, S, T, r, sigma):
        # Filter and sort dividends occurring before option maturity T
        divs = []
        if self.div1_amt > 0 and 0 < self.div1_time < T:
            divs.append((self.div1_time, self.div1_amt))
        if self.div2_amt > 0 and 0 < self.div2_time < T:
            divs.append((self.div2_time, self.div2_amt))
            
        divs.sort(key=lambda x: x[0])
        
        if not divs:
            return sigma
            
        # Variance adjustment formula
        var_adj = 0.0
        t_prev = 0.0
        n = len(divs)
        
        for j in range(n):
            t_j, _ = divs[j]
            # Calculate sum_{i=j}^n D_i e^{-r t_i}
            sum_div_pv = 0.0
            for i in range(j, n):
                t_i, D_i = divs[i]
                sum_div_pv += D_i * np.exp(-r * t_i)
                
            denom = S - sum_div_pv
            if denom <= 0.01:
                denom = 0.01
                
            term = ((S * sigma) / denom) ** 2 * (t_j - t_prev)
            var_adj += term
            t_prev = t_j
            
        t_n = divs[-1][0]
        var_adj += (sigma ** 2) * (T - t_n)
        
        return np.sqrt(max(1e-5, var_adj))

    def _hhl_price(self, S, K, T, r, sigma):
        # 1. S_adj is the same as escrowed dividend
        _, S_adj, div_pv = self._escrowed_dividend_price(S, K, T, r, sigma)
        # 2. sigma_adj
        sigma_adj = self._hhl_vol_adjustment(S, T, r, sigma)
        # 3. Price is BSM using S_adj and sigma_adj with b=r
        price = self._generalized_bsm(S_adj, K, T, r, r, sigma_adj)
        return price, S_adj, sigma_adj, div_pv

    def _hhl_greeks(self, S, K, T, r, sigma):
        _, S_adj, sigma_adj, _ = self._hhl_price(S, K, T, r, sigma)
        # Greeks are BSM Greeks evaluated at S_adj, sigma_adj with b=r
        return self._analytical_greeks(S_adj, K, T, r, r, sigma_adj)

    def _bos_vandermark_price(self, S, K, T, r, b, sigma):
        Xn = 0.0
        Xf = 0.0
        
        # Filter and sort dividends occurring before option maturity T
        divs = []
        if self.div1_amt > 0 and 0 < self.div1_time < T:
            divs.append((self.div1_time, self.div1_amt))
        if self.div2_amt > 0 and 0 < self.div2_time < T:
            divs.append((self.div2_time, self.div2_amt))
            
        for t_i, D_i in divs:
            Xn += ((T - t_i) / T) * D_i * np.exp(-r * t_i)
            Xf += (t_i / T) * D_i * np.exp(-r * t_i)
            
        S_adj = max(0.01, S - Xn)
        K_adj = max(0.01, K + Xf * np.exp(r * T))
        
        # Price is BSM using S_adj, K_adj, and b
        price = self._generalized_bsm(S_adj, K_adj, T, r, b, sigma)
        return price, S_adj, K_adj, Xn, Xf

    def _bos_vandermark_greeks(self, S, K, T, r, b, sigma):
        _, S_adj, K_adj, _, _ = self._bos_vandermark_price(S, K, T, r, b, sigma)
        # Greeks are standard BSM Greeks evaluated at S_adj and K_adj with cost of carry b
        return self._analytical_greeks(S_adj, K_adj, T, r, b, sigma)

    def _black76f_price(self, F, K, T, T_f, r, sigma):
        """
        Black-76F: Option on Forward with deferred settlement.
        Ref: Haug Eq 10.4, 10.5
        """
        # b=0 for forwards in d1/d2 calc
        d1, d2 = self._d1_d2(F, K, T, 0.0, sigma) 
        N = norm.cdf
        
        # Discount using T_f (payment time)
        df = np.exp(-r * T_f)
        
        if self.is_call == 1:
            # Eq 10.4
            return df * (F * N(d1) - K * N(d2))
        else:
            # Eq 10.5
            return df * (K * N(-d2) - F * N(-d1))

    def _brenner_subrahmanyam(self, S, T, r, b, sigma):
        """
        Brenner-Subrahmanyam (1988) Approximation.
        Ref: Haug Eq 2.69
        """
        # Constant approx 1/sqrt(2*pi)
        CONST_APPROX = 0.398942 
        price = CONST_APPROX * S * np.exp((b - r) * T) * sigma * np.sqrt(T)
        return price

    def _bachelier_price(self, S, K, T, r, b, sigma):
        """
        Bachelier (1900) Normal/Arithmetic Option Model.
        Uses normal distribution instead of lognormal.
        Ref: Haug Section 2.3.1, Equations 2.19-2.20
        """
        # Forward price with cost of carry
        F = S * np.exp(b * T)
        
        # Volatility scaled by sqrt(T)
        sigma_sqrt_T = sigma * np.sqrt(T)
        
        # Avoid division by zero
        if sigma_sqrt_T < 1e-10:
            # At expiry or zero vol, return intrinsic value
            if self.is_call == 1:
                return max(0, np.exp(-r * T) * (F - K))
            else:
                return max(0, np.exp(-r * T) * (K - F))
        
        # d parameter for Bachelier (different from BSM d1/d2)
        d = (F - K) / sigma_sqrt_T
        
        N = norm.cdf
        n = norm.pdf
        
        # Discount factor
        df = np.exp(-r * T)
        
        if self.is_call == 1:
            # Call: C = e^(-rT) * [(F - K) * N(d) + σ√T * n(d)]
            price = df * ((F - K) * N(d) + sigma_sqrt_T * n(d))
        else:
            # Put: P = e^(-rT) * [(K - F) * N(-d) + σ√T * n(d)]
            price = df * ((K - F) * N(-d) + sigma_sqrt_T * n(d))
        
        return max(0, price)

    def _modified_bachelier_price(self, S, K, T, r, b, sigma, beta=0):
        """
        Modified Bachelier (Shifted/Displaced Bachelier) Model.
        Uses normal distribution with a shift parameter β to better calibrate to markets.
        Ref: Haug Section 2.3.2 or market practice literature
        """
        # Forward price with cost of carry
        F = S * np.exp(b * T)
        
        # Apply shift to both forward and strike
        F_shifted = F + beta
        K_shifted = K + beta
        
        # Volatility scaled by sqrt(T)
        sigma_sqrt_T = sigma * np.sqrt(T)
        
        # Avoid division by zero
        if sigma_sqrt_T < 1e-10:
            # At expiry or zero vol, return intrinsic value
            if self.is_call == 1:
                return max(0, np.exp(-r * T) * (F - K))
            else:
                return max(0, np.exp(-r * T) * (K - F))
        
        # d parameter for Modified Bachelier (using shifted values)
        d = (F_shifted - K_shifted) / sigma_sqrt_T
        
        N = norm.cdf
        n = norm.pdf
        
        # Discount factor
        df = np.exp(-r * T)
        
        if self.is_call == 1:
            price = df * ((F - K) * N(d) + sigma_sqrt_T * n(d))
        else:
            price = df * ((K - F) * N(-d) + sigma_sqrt_T * n(d))
        
        return max(0, price)

    def _modified_bachelier_greeks(self, S, K, T, r, b, sigma, beta=0):
        """
        Analytical Greeks for Modified Bachelier Model.
        Similar to Bachelier but accounts for the shift parameter.
        """
        # Forward price
        F = S * np.exp(b * T)
        
        # Apply shift
        F_shifted = F + beta
        K_shifted = K + beta
        
        sigma_sqrt_T = sigma * np.sqrt(T)
        
        # Avoid division by zero
        if sigma_sqrt_T < 1e-10:
            sigma_sqrt_T = 1e-10
        
        d = (F_shifted - K_shifted) / sigma_sqrt_T
        
        N = norm.cdf
        n = norm.pdf
        
        df = np.exp(-r * T)
        ebT = np.exp(b * T)
        
        # Delta (adjusted for shift)
        if self.is_call == 1:
            delta = df * ebT * N(d)
        else:
            delta = -df * ebT * N(-d)
        
        # Gamma (constant-like in Bachelier family)
        gamma = (df * ebT * n(d)) / sigma_sqrt_T
        
        # Vega
        vega = df * n(d) * np.sqrt(T) / 100.0
        
        # Theta
        if self.is_call == 1:
            term1 = -r * df * ((F - K) * N(d) + sigma_sqrt_T * n(d))
            term2 = b * df * ebT * S * N(d)
            term3 = -df * sigma * n(d) / (2 * np.sqrt(T))
        else:
            term1 = -r * df * ((K - F) * N(-d) + sigma_sqrt_T * n(d))
            term2 = -b * df * ebT * S * N(-d)
            term3 = -df * sigma * n(d) / (2 * np.sqrt(T))
        
        theta = (term1 + term2 + term3) / 365.0
        
        # Rho (interest rate sensitivity)
        if self.is_call == 1:
            rho = -T * df * ((F - K) * N(d) + sigma_sqrt_T * n(d))
        else:
            rho = -T * df * ((K - F) * N(-d) + sigma_sqrt_T * n(d))
        
        return {
            "delta": delta,
            "gamma": gamma,
            "vega": vega,
            "theta": theta,
            "rho": rho / 100.0,
            "phi": 0.0
        }

    def _sprenkle_price(self, S, K, T, mu, sigma):
        """
        Sprenkle (1964) Option Pricing Model.
        """
        if T <= 1e-10:
            return max(0, S - K) if self.is_call == 1 else max(0, K - S)
        
        d1 = (np.log(S / K) + (mu + sigma**2 / 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        N = norm.cdf
        
        if self.is_call == 1:
            price = S * np.exp(mu * T) * N(d1) - K * N(d2)
        else:
            price = K * N(-d2) - S * np.exp(mu * T) * N(-d1)
        return max(0, price)

    def _boness_price(self, S, K, T, r, mu, sigma):
        """
        Boness (1964) Option Pricing Model.
        """
        if T <= 1e-10:
            return max(0, S - K) if self.is_call == 1 else max(0, K - S)
        
        d1 = (np.log(S / K) + (mu + sigma**2 / 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        N = norm.cdf
        df = np.exp(-r * T)
        
        if self.is_call == 1:
            price = S * np.exp(mu * T) * N(d1) - K * df * N(d2)
        else:
            price = K * df * N(-d2) - S * np.exp(mu * T) * N(-d1)
        return max(0, price)

    def _boness_greeks(self, S, K, T, r, mu, sigma):
        if T <= 1e-10:
            if self.is_call == 1:
                return {"delta": 1.0 if S > K else 0.0, "gamma": 0.0, "vega": 0.0, "theta": 0.0, "rho": 0.0, "phi": 0.0}
            else:
                return {"delta": -1.0 if S < K else 0.0, "gamma": 0.0, "vega": 0.0, "theta": 0.0, "rho": 0.0, "phi": 0.0}
        
        d1 = (np.log(S / K) + (mu + sigma**2 / 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        N = norm.cdf
        n = norm.pdf
        df = np.exp(-r * T)
        emu_T = np.exp(mu * T)
        sqrt_T = np.sqrt(T)
        
        if self.is_call == 1: delta = emu_T * N(d1)
        else: delta = -emu_T * N(-d1)
        
        gamma = (emu_T * n(d1)) / (S * sigma * sqrt_T)
        vega = S * emu_T * n(d1) * sqrt_T / 100.0
        
        if self.is_call == 1:
            term1 = -S * emu_T * n(d1) * sigma / (2 * sqrt_T)
            term2 = mu * S * emu_T * N(d1)
            term3 = r * K * df * N(d2)
            theta = (term1 + term2 - term3) / 365.0
            rho = -T * K * df * N(d2)
        else:
            term1 = -S * emu_T * n(d1) * sigma / (2 * sqrt_T)
            term2 = -mu * S * emu_T * N(-d1)
            term3 = -r * K * df * N(-d2)
            theta = (term1 + term2 - term3) / 365.0
            rho = T * K * df * N(-d2)
        
        return {"delta": delta, "gamma": gamma, "vega": vega, "theta": theta, "rho": rho / 100.0, "phi": 0.0}

    def _sprenkle_greeks(self, S, K, T, mu, sigma):
        if T <= 1e-10:
            if self.is_call == 1:
                return {"delta": 1.0 if S > K else 0.0, "gamma": 0.0, "vega": 0.0, "theta": 0.0, "rho": 0.0, "phi": 0.0}
            else:
                return {"delta": -1.0 if S < K else 0.0, "gamma": 0.0, "vega": 0.0, "theta": 0.0, "rho": 0.0, "phi": 0.0}
        
        d1 = (np.log(S / K) + (mu + sigma**2 / 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        N = norm.cdf
        n = norm.pdf
        emu_T = np.exp(mu * T)
        sqrt_T = np.sqrt(T)
        
        if self.is_call == 1: delta = emu_T * N(d1)
        else: delta = -emu_T * N(-d1)
        
        gamma = (emu_T * n(d1)) / (S * sigma * sqrt_T)
        vega = S * emu_T * n(d1) * sqrt_T / 100.0
        
        if self.is_call == 1:
            theta = (-S * emu_T * n(d1) * sigma / (2 * sqrt_T) + mu * S * emu_T * N(d1)) / 365.0
            rho = T * S * emu_T * N(d1)
        else:
            theta = (-S * emu_T * n(d1) * sigma / (2 * sqrt_T) - mu * S * emu_T * N(-d1)) / 365.0
            rho = -T * S * emu_T * N(-d1)
        
        return {"delta": delta, "gamma": gamma, "vega": vega, "theta": theta, "rho": rho / 100.0, "phi": 0.0}

    def _bachelier_greeks(self, S, K, T, r, b, sigma):
        F = S * np.exp(b * T)
        sigma_sqrt_T = sigma * np.sqrt(T)
        if sigma_sqrt_T < 1e-10: sigma_sqrt_T = 1e-10
        d = (F - K) / sigma_sqrt_T
        N = norm.cdf
        n = norm.pdf
        df = np.exp(-r * T)
        ebT = np.exp(b * T)
        
        if self.is_call == 1: delta = df * ebT * N(d)
        else: delta = -df * ebT * N(-d)
        
        gamma = (df * ebT * n(d)) / sigma_sqrt_T
        vega = df * n(d) * np.sqrt(T) / 100.0
        
        if self.is_call == 1:
            term1 = -r * df * ((F - K) * N(d) + sigma_sqrt_T * n(d))
            term2 = b * df * ebT * S * N(d)
            term3 = -df * sigma * n(d) / (2 * np.sqrt(T))
        else:
            term1 = -r * df * ((K - F) * N(-d) + sigma_sqrt_T * n(d))
            term2 = -b * df * ebT * S * N(-d)
            term3 = -df * sigma * n(d) / (2 * np.sqrt(T))
        theta = (term1 + term2 + term3) / 365.0
        
        if self.is_call == 1: rho = -T * df * ((F - K) * N(d) + sigma_sqrt_T * n(d))
        else: rho = -T * df * ((K - F) * N(-d) + sigma_sqrt_T * n(d))
        
        return {"delta": delta, "gamma": gamma, "vega": vega, "theta": theta, "rho": rho / 100.0, "phi": 0.0}

    def _analytical_greeks(self, S, K, T, r, b, sigma):
        """
        Analytical Greeks for GBSM.
        Ref: Haug Chapter 2, Table 2-1.
        """
        d1, d2 = self._d1_d2(S, K, T, b, sigma)
        N = norm.cdf
        n = norm.pdf
        ert = np.exp(-r * T)
        ebrt = np.exp((b - r) * T)

        if self.is_call == 1:
            delta = ebrt * N(d1)
        else:
            delta = ebrt * (N(d1) - 1)
            
        gamma = (n(d1) * ebrt) / (S * sigma * np.sqrt(T))
        vega = (S * ebrt * n(d1) * np.sqrt(T)) / 100.0
        
        term1 = -(S * ebrt * n(d1) * sigma) / (2 * np.sqrt(T))
        if self.is_call == 1:
            term2 = -(b - r) * S * ebrt * N(d1) - r * K * ert * N(d2)
        else:
            term2 = +(b - r) * S * ebrt * N(-d1) + r * K * ert * N(-d2)
        theta = (term1 + term2) / 365.0
            
        if self.model == 'garman':
            if self.is_call == 1: rho = K * T * ert * N(d2)
            else: rho = -K * T * ert * N(-d2)
            if self.is_call == 1: phi = -T * S * ebrt * N(d1)
            else: phi = T * S * ebrt * N(-d1)
        else:
            if self.is_call == 1: rho = K * T * ert * N(d2)
            else: rho = -K * T * ert * N(-d2)
            phi = 0.0
            
        return {"delta": delta, "gamma": gamma, "vega": vega, "theta": theta, "rho": rho / 100.0, "phi": phi / 100.0}

    def _numerical_greeks(self, pricing_func):
        """
        Calculates Greeks using Finite Differences.
        """
        dS = self.S * 0.01 if self.S > 0 else 0.01
        dT = 1.0 / 365.0
        dVol = 0.01
        dr = 0.01

        S_up = self.S + dS
        S_down = max(0.01, self.S - dS)

        base_price = pricing_func(self.S, self.T, self.sigma, self.r)
        
        p_up = pricing_func(S_up, self.T, self.sigma, self.r)
        p_down = pricing_func(S_down, self.T, self.sigma, self.r)
        
        delta = (p_up - p_down) / (S_up - S_down)
        gamma = (p_up - 2 * base_price + p_down) / ((S_up - self.S)**2)
        
        if self.T > dT:
            p_t_minus = pricing_func(self.S, self.T - dT, self.sigma, self.r)
            theta = (p_t_minus - base_price) 
        else:
            theta = 0.0
        
        p_v_up = pricing_func(self.S, self.T, self.sigma + dVol, self.r)
        p_v_down = pricing_func(self.S, self.T, max(0.001, self.sigma - dVol), self.r)
        vega = (p_v_up - p_v_down) / 2.0 
        
        p_r_up = pricing_func(self.S, self.T, self.sigma, self.r + dr)
        p_r_down = pricing_func(self.S, self.T, self.sigma, self.r - dr)
        rho = (p_r_up - p_r_down) / 2.0

        return {"delta": delta, "gamma": gamma, "vega": vega, "theta": theta, "rho": rho, "phi": 0.0}

    def _standard_barrier_option(self, S, T, sigma, r):
        """
        Reiner and Rubinstein (1991) Standard Barrier Formulas.
        Ref: Haug Chapter 4.17.1
        """
        K = self.rebate
        H = self.H
        b = self.b
        
        if self.barrier_type.startswith("Down") and S <= H:
            return K if "Out" in self.barrier_type else (self._generalized_bsm(S, self.K, T, r, b, sigma) + K)
        if self.barrier_type.startswith("Up") and S >= H:
             return K if "Out" in self.barrier_type else (self._generalized_bsm(S, self.K, T, r, b, sigma) + K)

        mu = (b - sigma**2/2) / sigma**2
        lam = np.sqrt(mu**2 + 2*r/sigma**2)
        sigma_sqrt_T = sigma * np.sqrt(T)
        
        safe_S = max(S, 1e-5)
        safe_H = max(H, 1e-5)
        
        x1 = np.log(safe_S/self.K) / sigma_sqrt_T + (1 + mu)*sigma_sqrt_T
        x2 = np.log(safe_S/safe_H) / sigma_sqrt_T + (1 + mu)*sigma_sqrt_T
        y1 = np.log(safe_H**2 / (safe_S*self.K)) / sigma_sqrt_T + (1 + mu)*sigma_sqrt_T
        y2 = np.log(safe_H/safe_S) / sigma_sqrt_T + (1 + mu)*sigma_sqrt_T
        z  = np.log(safe_H/safe_S) / sigma_sqrt_T + lam * sigma_sqrt_T
        
        N = norm.cdf

        def term_A(phi):
            return phi * safe_S * np.exp((b-r)*T) * N(phi * x1) - \
                   phi * self.K * np.exp(-r*T) * N(phi * (x1 - sigma_sqrt_T))
        def term_B(phi):
            return phi * safe_S * np.exp((b-r)*T) * N(phi * x2) - \
                   phi * self.K * np.exp(-r*T) * N(phi * (x2 - sigma_sqrt_T))
        def term_C(phi, eta):
            return phi * safe_S * np.exp((b-r)*T) * (safe_H/safe_S)**(2*(mu+1)) * N(eta * y1) - \
                   phi * self.K * np.exp(-r*T) * (safe_H/safe_S)**(2*mu) * N(eta * (y1 - sigma_sqrt_T))
        def term_D(phi, eta):
            return phi * safe_S * np.exp((b-r)*T) * (safe_H/safe_S)**(2*(mu+1)) * N(eta * y2) - \
                   phi * self.K * np.exp(-r*T) * (safe_H/safe_S)**(2*mu) * N(eta * (y2 - sigma_sqrt_T))
        def term_E(eta):
            return K * np.exp(-r*T) * (N(eta * (x2 - sigma_sqrt_T)) - \
                                      (safe_H/safe_S)**(2*mu) * N(eta * (y2 - sigma_sqrt_T)))
        def term_F(eta):
            return K * ((safe_H/safe_S)**(mu+lam) * N(eta * z) + \
                        (safe_H/safe_S)**(mu-lam) * N(eta * (z - 2*lam*sigma_sqrt_T)))

        val = 0.0
        
        if self.barrier_type == 'Down-and-In':
            if self.is_call == 1: val = (term_C(1, 1) + term_E(1)) if self.K > H else (term_A(1) - term_B(1) + term_D(1, 1) + term_E(1))
            else: val = (term_B(-1) - term_C(-1, 1) + term_D(-1, 1) + term_E(1)) if self.K > H else (term_A(-1) + term_E(1))
        elif self.barrier_type == 'Down-and-Out':
            if self.is_call == 1: val = (term_A(1) - term_C(1, 1) + term_F(1)) if self.K > H else (term_B(1) - term_D(1, 1) + term_F(1))
            else: val = (term_A(-1) - term_B(-1) + term_C(-1, 1) - term_D(-1, 1) + term_F(1)) if self.K > H else term_F(1)
        elif self.barrier_type == 'Up-and-In':
            if self.is_call == 1: val = (term_A(1) + term_E(-1)) if self.K > H else (term_B(1) - term_C(1, -1) + term_D(1, -1) + term_E(-1))
            else: val = (term_A(-1) - term_B(-1) + term_D(-1, -1) + term_E(-1)) if self.K > H else (term_C(-1, -1) + term_E(-1))
        elif self.barrier_type == 'Up-and-Out':
            if self.is_call == 1: val = term_F(-1) if self.K > H else (term_A(1) - term_B(1) + term_C(1, -1) - term_D(1, -1) + term_F(-1))
            else: val = (term_B(-1) - term_D(-1, -1) + term_F(-1)) if self.K > H else (term_A(-1) - term_C(-1, -1) + term_F(-1))
                    
        return max(0.0, val)

    # --- McKean (1965) Implementation ---
    def _mckean_perpetual(self, S, K, r, q, sigma):
        b = r - q
        sigma_sq = sigma**2
        if sigma <= 1e-6: return max(S - K, 0) if self.is_call == 1 else max(K - S, 0)
        term = (b / sigma_sq - 0.5)**2 + 2 * r / sigma_sq
        sqrt_term = np.sqrt(term)
        y1 = 0.5 - b / sigma_sq + sqrt_term
        y2 = 0.5 - b / sigma_sq - sqrt_term
        
        if self.is_call == 1: return self._mckean_call(S, K, y1)
        else: return self._mckean_put(S, K, y2)

    def _mckean_call(self, S, K, y1):
        if y1 <= 1: return S 
        S_star = K * y1 / (y1 - 1)
        if S >= S_star: return S - K
        return (S_star - K) * (S / S_star) ** y1

    def _mckean_put(self, S, K, y2):
        S_star = K * y2 / (y2 - 1)
        if S <= S_star: return K - S
        return (K - S_star) * (S / S_star) ** y2

    def _roll_geske_whaley(self, S, K, T, r, sigma, D, t_div):
        if t_div >= T or t_div <= 0: return self._generalized_bsm(S, K, T, r, r, sigma) # b=r

        threshold = K * (1 - np.exp(-r * (T - t_div)))
        
        if D <= threshold:
            S_adj = S - D * np.exp(-r * t_div)
            return self._generalized_bsm(S_adj, K, T, r, r, sigma)
            
        def objective(I_ex):
            c_val = self._generalized_bsm(I_ex, K, T - t_div, r, r, sigma)
            exercise_val = I_ex + D - K
            return c_val - exercise_val

        try:
            I = brentq(objective, 0.01, S * 5)
        except Exception:
            return max(S - K, 0)
            
        S_adj = S - D * np.exp(-r * t_div)
        sqrt_t = np.sqrt(t_div)
        sqrt_T = np.sqrt(T)
        rho = sqrt_t / sqrt_T
        
        b1 = (np.log(S_adj / K) + (r + 0.5 * sigma**2) * T) / (sigma * sqrt_T)
        b2 = b1 - sigma * sqrt_T
        a1 = (np.log(S_adj / I) + (r + 0.5 * sigma**2) * t_div) / (sigma * sqrt_t)
        a2 = a1 - sigma * sqrt_t
        
        term_exercise = S_adj * norm.cdf(a1) + (D * np.exp(-r * t_div) - K * np.exp(-r * t_div)) * norm.cdf(a2)
        m1 = cbnd(b1, -a1, -rho)
        m2 = cbnd(b2, -a2, -rho)
        term_continuation = S_adj * m1 - K * np.exp(-r * T) * m2
        return term_exercise + term_continuation

    # --- Villiger (2005) Implementation ---
    def _villiger_2005(self, S, K, T, r, sigma, delta, t_div):
        if t_div >= T or t_div <= 0: return self._generalized_bsm(S, K, T, r, r, sigma)

        def objective(I_try):
            S_ex = I_try * (1 - delta)
            if S_ex <= 0: return -(I_try - K)
            hold_val = self._generalized_bsm(S_ex, K, T - t_div, r, r, sigma)
            ex_val = I_try - K
            return hold_val - ex_val

        try:
            I = brentq(objective, K, S * 5)
        except Exception:
            return max(S-K, 0)

        sqrt_t = np.sqrt(t_div)
        sqrt_T = np.sqrt(T)
        rho = sqrt_t / sqrt_T
        
        a1 = (np.log(S / I) + (r + 0.5 * sigma**2) * t_div) / (sigma * sqrt_t)
        a2 = a1 - sigma * sqrt_t
        
        S_term = S * (1 - delta)
        b1 = (np.log(S_term / K) + (r + 0.5 * sigma**2) * T) / (sigma * sqrt_T)
        b2 = b1 - sigma * sqrt_T
        
        term_Ex = S * norm.cdf(a1) - K * np.exp(-r * t_div) * norm.cdf(a2)
        m1 = cbnd(b1, -a1, -rho)
        m2 = cbnd(b2, -a2, -rho)
        term_Cont = S * (1 - delta) * m1 - K * np.exp(-r * T) * m2
        return term_Ex + term_Cont

    # --- Bjerksund-Stensland (2002) Implementation ---
    def _bjerksund_stensland_2002(self, S, K, T, r, q, sigma):
        b = r - q
        if T <= 1e-6: return max(S - K, 0) if self.is_call == 1 else max(K - S, 0)
            
        if self.is_call == 1: return self._bs2002_call(S, K, T, r, b, sigma)
        else: return self._bs2002_call(K, S, T, r - b, -b, sigma)

    def _bs2002_call(self, S, X, T, r, b, sigma):
        if b >= r: return self._generalized_bsm(S, X, T, r, b, sigma)

        beta = (0.5 - b / sigma**2) + np.sqrt((b / sigma**2 - 0.5)**2 + 2 * r / sigma**2)
        B_inf = (beta / (beta - 1)) * X
        B_0 = max(X, (r / (r - b)) * X)
        
        t1 = 0.5 * (np.sqrt(5) - 1) * T
        t2 = T
        
        def h(t): return -(b * t + 2 * sigma * np.sqrt(t)) * (X * X) / ((B_inf - B_0) * B_0)
            
        I1 = B_0 + (B_inf - B_0) * (1 - np.exp(h(t1)))
        I2 = B_0 + (B_inf - B_0) * (1 - np.exp(h(t2)))
        
        if S >= I2: return S - X
        if S >= I1: return S - X
        
        def alpha(I): return (I - X) * (I ** -beta)
        alpha1 = alpha(I1)
        alpha2 = alpha(I2)
        
        term1 = alpha2 * (S**beta) - alpha2 * self._bs2002_phi(S, t1, beta, I2, I2, r, b, sigma)
        term2 = self._bs2002_phi(S, t1, 1, I2, I2, r, b, sigma) - self._bs2002_phi(S, t1, 1, I1, I2, r, b, sigma)
        term3 = -X * self._bs2002_phi(S, t1, 0, I2, I2, r, b, sigma) + X * self._bs2002_phi(S, t1, 0, I1, I2, r, b, sigma)
        term4 = alpha1 * self._bs2002_phi(S, t1, beta, I1, I2, r, b, sigma) - alpha1 * self._bs2002_psi(S, t2, beta, I1, I2, I1, t1, r, b, sigma)
        term5 = self._bs2002_psi(S, t2, 1, I1, I2, I1, t1, r, b, sigma) - self._bs2002_psi(S, t2, 1, I1, I2, X, t1, r, b, sigma)
        term6 = -X * self._bs2002_psi(S, t2, 0, I1, I2, I1, t1, r, b, sigma) + X * self._bs2002_psi(S, t2, 0, I1, I2, X, t1, r, b, sigma)

        return term1 + term2 + term3 + term4 + term5 + term6

    def _bs2002_phi(self, S, T, gamma, H, I, r, b, sigma):
        lam = -r + gamma * b + 0.5 * gamma * (gamma - 1) * sigma**2
        kappa = 2 * b / sigma**2 + (2 * gamma - 1)
        d = -(np.log(S / H) + (b + (gamma - 0.5) * sigma**2) * T) / (sigma * np.sqrt(T))
        d_prime = d - 2 * np.log(I / S) / (sigma * np.sqrt(T))
        term = np.exp(lam * T) * (S**gamma) * (norm.cdf(d) - (I / S)**kappa * norm.cdf(d_prime))
        return term

    def _bs2002_psi(self, S, T, gamma, I1, I2, H, t1, r, b, sigma):
        lam = -r + gamma * b + 0.5 * gamma * (gamma - 1) * sigma**2
        kappa = 2 * b / sigma**2 + (2 * gamma - 1)
        
        sqrt_t1 = np.sqrt(t1)
        sqrt_T = np.sqrt(T)
        rho = sqrt_t1 / sqrt_T
        
        e1 = (np.log(S / I1) + (b + (gamma - 0.5)*sigma**2)*t1) / (sigma*sqrt_t1)
        e2 = (np.log(I2**2 / (S * I1)) + (b + (gamma - 0.5)*sigma**2)*t1) / (sigma*sqrt_t1)
        e3 = (np.log(S / I1) - (b + (gamma - 0.5)*sigma**2)*t1) / (sigma*sqrt_t1)
        e4 = (np.log(I2**2 / (S * I1)) - (b + (gamma - 0.5)*sigma**2)*t1) / (sigma*sqrt_t1)
        
        f1 = (np.log(S / H) + (b + (gamma - 0.5)*sigma**2)*T) / (sigma*sqrt_T)
        f2 = (np.log(I2**2 / (S * H)) + (b + (gamma - 0.5)*sigma**2)*T) / (sigma*sqrt_T)
        f3 = (np.log(I1**2 / (S * H)) + (b + (gamma - 0.5)*sigma**2)*T) / (sigma*sqrt_T)
        f4 = (np.log( (S * I1**2) / (H * I2**2) ) + (b + (gamma - 0.5)*sigma**2)*T) / (sigma*sqrt_T)
        
        term = np.exp(lam * T) * (S**gamma) * (
            cbnd(-e1, -f1, rho) 
            - (I2 / S)**kappa * cbnd(-e2, -f2, rho)
            - (I1 / S)**kappa * cbnd(-e3, -f3, -rho)
            + (I1 / I2)**kappa * cbnd(-e4, -f4, -rho)
        )
        return term

    def calculate(self):
        note = "Standard Valuation"
        
        if 'barrier' in self.model:
            wrapper = lambda s, t, v, r_in: self._standard_barrier_option(s, t, v, r_in)
            price = self._standard_barrier_option(self.S, self.T, self.sigma, self.r)
            greeks = self._numerical_greeks(wrapper)
            mu = (self.b - self.sigma**2/2) / self.sigma**2
            greeks['Lambda'] = np.sqrt(mu**2 + 2*self.r/self.sigma**2)
            
            is_knocked_out = False
            if 'Down' in self.barrier_type and self.S <= self.H: is_knocked_out = True
            if 'Up' in self.barrier_type and self.S >= self.H: is_knocked_out = True
            note = "Option Knocked Out" if is_knocked_out else "Active"
            
        elif self.model == 'black76f':
            price = self._black76f_price(self.S, self.K, self.T, self.T_f, self.r, self.sigma)
            d1, d2 = self._d1_d2(self.S, self.K, self.T, 0.0, self.sigma)
            N = norm.cdf
            n_pdf = norm.pdf
            df = np.exp(-self.r * self.T_f)
            delta = df * (N(d1) if self.is_call == 1 else (N(d1) - 1))
            gamma = (n_pdf(d1) * df) / (self.S * self.sigma * np.sqrt(self.T))
            vega = (self.S * df * n_pdf(d1) * np.sqrt(self.T)) / 100.0
            rho = -self.T_f * price / 100.0
            greeks = {'delta': delta, 'gamma': gamma, 'vega': vega, 'theta': 0, 'rho': rho}
            note = f"Settlement at Tf={self.T_f:.2f}yr"

        elif self.model == 'brenner':
            price = self._brenner_subrahmanyam(self.S, self.T, self.r, self.b, self.sigma)
            exact = self._generalized_bsm(self.S, self.K, self.T, self.r, self.b, self.sigma)
            greeks = self._analytical_greeks(self.S, self.K, self.T, self.r, self.b, self.sigma)
            note = f"Approx: {price:.4f} vs Exact: {exact:.4f}"

        elif self.model == 'bachelier':
            price = self._bachelier_price(self.S, self.K, self.T, self.r, self.b, self.sigma)
            greeks = self._bachelier_greeks(self.S, self.K, self.T, self.r, self.b, self.sigma)
            sigma_bsm = self.sigma / self.S if self.S > 0 else self.sigma
            bsm_price = self._generalized_bsm(self.S, self.K, self.T, self.r, self.b, sigma_bsm)
            note = f"Bachelier: {price:.4f} | BSM (σ={sigma_bsm*100:.1f}%): {bsm_price:.4f}"

        elif self.model == 'sprenkle':
            mu = self.r
            price = self._sprenkle_price(self.S, self.K, self.T, mu, self.sigma)
            greeks = self._sprenkle_greeks(self.S, self.K, self.T, mu, self.sigma)
            bsm_price = self._generalized_bsm(self.S, self.K, self.T, self.r, self.r, self.sigma)
            note = f"Sprenkle (μ={mu*100:.1f}%): {price:.4f} | BSM (r={self.r*100:.1f}%): {bsm_price:.4f}"

        elif self.model == 'boness':
            mu = self.r
            price = self._boness_price(self.S, self.K, self.T, self.r, mu, self.sigma)
            greeks = self._boness_greeks(self.S, self.K, self.T, self.r, mu, self.sigma)
            bsm_price = self._generalized_bsm(self.S, self.K, self.T, self.r, self.r, self.sigma)
            note = f"Boness (μ=r={mu*100:.1f}%): {price:.4f} | BSM: {bsm_price:.4f}"

        elif self.model == 'mod_bachelier':
            price = self._modified_bachelier_price(self.S, self.K, self.T, self.r, self.b, self.sigma, self.shift)
            greeks = self._modified_bachelier_greeks(self.S, self.K, self.T, self.r, self.b, self.sigma, self.shift)
            bachelier_price = self._bachelier_price(self.S, self.K, self.T, self.r, self.b, self.sigma)
            note = f"Mod.Bachelier (β={self.shift}): {price:.4f} | Bachelier: {bachelier_price:.4f}"

        elif self.model == 'bjerksund02':
            price = self._bjerksund_stensland_2002(self.S, self.K, self.T, self.r, self.q_or_rf, self.sigma)
            wrapper = lambda s, t, v, r: self._bjerksund_stensland_2002(s, self.K, t, r, self.q_or_rf, v)
            greeks = self._numerical_greeks(wrapper)
            note = "BS2002 Valuation (Standard)"

        elif self.model == 'mckean':
            price = self._mckean_perpetual(self.S, self.K, self.r, self.q_or_rf, self.sigma)
            wrapper = lambda s, t, v, r: self._mckean_perpetual(s, self.K, r, self.q_or_rf, v)
            greeks = self._numerical_greeks(wrapper)
            greeks['theta'] = 0.0
            note = f"Perpetual Option (McKean)"

        elif self.model == 'roll_geske':
            D = self.q_or_rf
            t_div = getattr(self, 'time_dividend', 0.25)
            price = self._roll_geske_whaley(self.S, self.K, self.T, self.r, self.sigma, D, t_div)
            wrapper = lambda s, t, v, r: self._roll_geske_whaley(s, self.K, t, r, v, D, t_div)
            greeks = self._numerical_greeks(wrapper)
            note = f"RGW (D=${D} at t={t_div})"

        elif self.model == 'villiger':
            delta = self.q_or_rf
            t_div = getattr(self, 'time_dividend', 0.25)
            price = self._villiger_2005(self.S, self.K, self.T, self.r, self.sigma, delta, t_div)
            wrapper = lambda s, t, v, r: self._villiger_2005(s, self.K, t, r, v, delta, t_div)
            greeks = self._numerical_greeks(wrapper)
            note = f"Villiger (δ={delta*100:.2f}% at t={t_div})"

        elif self.model == 'exec_stock':
            # Jennergren & Naslund (1993)
            price = self._jennergren_naslund(self.S, self.K, self.T, self.r, self.b, self.sigma, self.lamb)
            base_greeks = self._analytical_greeks(self.S, self.K, self.T, self.r, self.b, self.sigma)
            survival_prob = np.exp(-self.lamb * self.T)
            greeks = {k: v * survival_prob for k, v in base_greeks.items()}
            # Sensitivity to exit rate lambda roughly approximates to -T * Price
            greeks['rho_lambda'] = -self.T * price 
            note = f"Exec Value (λ={self.lamb}): {price:.4f} | BSM Base: {price/survival_prob if survival_prob > 0 else 0:.4f}"

        elif self.model == 'escrowed':
            price, S_adj, div_pv = self._escrowed_dividend_price(self.S, self.K, self.T, self.r, self.sigma)
            greeks = self._escrowed_dividend_greeks(self.S, self.K, self.T, self.r, self.sigma)
            note = f"S_adj = {S_adj:.4f} (D PV = {div_pv:.4f})"

        elif self.model == 'hhl':
            price, S_adj, sigma_adj, div_pv = self._hhl_price(self.S, self.K, self.T, self.r, self.sigma)
            greeks = self._hhl_greeks(self.S, self.K, self.T, self.r, self.sigma)
            note = f"S_adj = {S_adj:.4f} | σ_adj = {sigma_adj*100:.2f}%"

        elif self.model == 'bos_vandermark':
            price, S_adj, K_adj, Xn, Xf = self._bos_vandermark_price(self.S, self.K, self.T, self.r, self.b, self.sigma)
            greeks = self._bos_vandermark_greeks(self.S, self.K, self.T, self.r, self.b, self.sigma)
            note = f"S_adj = {S_adj:.4f} | K_adj = {K_adj:.4f}"

        elif self.model == 'margrabe':
            # Margrabe (1978) model
            price, sigma_hat, m_d1, m_d2 = self._margrabe_price(
                self.S, self.spot2, self.T, self.r, self.b, self.dividend2,
                self.sigma, self.vol2, self.correlation, self.q1, self.q2
            )
            # Standard Greeks calculated numerically with respect to primary asset S1
            wrapper = lambda s, t, v, r_in: self._margrabe_price(
                s, self.spot2, t, r_in, self.b, self.dividend2,
                v, self.vol2, self.correlation, self.q1, self.q2
            )[0]
            greeks = self._numerical_greeks(wrapper)
            note = f"Margrabe: {price:.4f} | Combined σ = {sigma_hat*100:.2f}%"

        else:
            price = self._generalized_bsm(self.S, self.K, self.T, self.r, self.b, self.sigma)
            greeks = self._analytical_greeks(self.S, self.K, self.T, self.r, self.b, self.sigma)
            note = "Standard Valuation"

        S_for_intermediates = self.S
        K_for_intermediates = self.K
        sigma_for_intermediates = self.sigma
        b_for_d1_d2 = self.b

        if self.model == 'escrowed':
            _, S_adj, _ = self._escrowed_dividend_price(self.S, self.K, self.T, self.r, self.sigma)
            S_for_intermediates = S_adj
        elif self.model == 'hhl':
            _, S_adj, sigma_adj, _ = self._hhl_price(self.S, self.K, self.T, self.r, self.sigma)
            S_for_intermediates = S_adj
            sigma_for_intermediates = sigma_adj
        elif self.model == 'bos_vandermark':
            _, S_adj, K_adj, _, _ = self._bos_vandermark_price(self.S, self.K, self.T, self.r, self.b, self.sigma)
            S_for_intermediates = S_adj
            K_for_intermediates = K_adj
        elif self.model == 'margrabe':
            S_for_intermediates = self.q1 * self.S
            K_for_intermediates = self.q2 * self.spot2
            sigma_for_intermediates = np.sqrt(max(1e-9, self.sigma**2 + self.vol2**2 - 2 * self.correlation * self.sigma * self.vol2))
            b_for_d1_d2 = self.b - self.dividend2

        d1, d2 = self._d1_d2(S_for_intermediates, K_for_intermediates, self.T, b_for_d1_d2, sigma_for_intermediates)
        Nd1 = norm.cdf(d1 if self.is_call==1 else -d1)
        Nd2 = norm.cdf(d2 if self.is_call==1 else -d2)

        return {
            "price": price,
            "greeks": greeks,
            "d1": d1,
            "d2": d2,
            "Nd1": Nd1,
            "Nd2": Nd2,
            "note": note,
            "intermediates": {"Lambda": greeks.get('Lambda', 0)}
        }
    
    def get_graph_data(self):
        points = []
        center = (self.S + self.K) / 2
        vol_factor = 1 + max(0.5, self.sigma * np.sqrt(self.T))
        start_spot = max(0.01, center * (1 - 0.5 * vol_factor))
        end_spot = center * (1 + 0.5 * vol_factor)
        spot_range = np.linspace(start_spot, end_spot, 50)

        for s in spot_range:
            original_S = self.S
            self.S = float(s)
            
            if 'barrier' in self.model:
                wrapper = lambda _s, _t, _v, _r: self._standard_barrier_option(_s, _t, _v, _r)
                p = self._standard_barrier_option(s, self.T, self.sigma, self.r)
                gr = self._numerical_greeks(wrapper)
            elif self.model == 'black76f':
                p = self._black76f_price(s, self.K, self.T, self.T_f, self.r, self.sigma)
                d1, _ = self._d1_d2(s, self.K, self.T, 0.0, self.sigma)
                df = np.exp(-self.r * self.T_f)
                gr = {"delta": df * norm.cdf(d1) if self.is_call==1 else df*(norm.cdf(d1)-1), "gamma": 0, "theta": 0, "vega": 0, "rho": 0}
            elif self.model == 'brenner':
                p = self._brenner_subrahmanyam(s, self.T, self.r, self.b, self.sigma)
                gr = self._analytical_greeks(s, self.K, self.T, self.r, self.b, self.sigma)
            elif self.model == 'bachelier':
                p = self._bachelier_price(s, self.K, self.T, self.r, self.b, self.sigma)
                gr = self._bachelier_greeks(s, self.K, self.T, self.r, self.b, self.sigma)
            elif self.model == 'sprenkle':
                mu = self.r
                p = self._sprenkle_price(s, self.K, self.T, mu, self.sigma)
                gr = self._sprenkle_greeks(s, self.K, self.T, mu, self.sigma)
            elif self.model == 'boness':
                mu = self.r
                p = self._boness_price(s, self.K, self.T, self.r, mu, self.sigma)
                gr = self._boness_greeks(s, self.K, self.T, self.r, mu, self.sigma)
            elif self.model == 'mod_bachelier':
                p = self._modified_bachelier_price(s, self.K, self.T, self.r, self.b, self.sigma, self.shift)
                gr = self._modified_bachelier_greeks(s, self.K, self.T, self.r, self.b, self.sigma, self.shift)
            elif self.model == 'bjerksund02':
                p = self._bjerksund_stensland_2002(s, self.K, self.T, self.r, self.q_or_rf, self.sigma)
                wrapper = lambda _s, _t, _v, _r: self._bjerksund_stensland_2002(_s, self.K, _t, _r, self.q_or_rf, _v)
                gr = self._numerical_greeks(wrapper)
            elif self.model == 'mckean':
                p = self._mckean_perpetual(s, self.K, self.r, self.q_or_rf, self.sigma)
                wrapper = lambda _s, _t, _v, _r: self._mckean_perpetual(_s, self.K, _r, self.q_or_rf, _v)
                gr = self._numerical_greeks(wrapper)
                gr['theta'] = 0
            elif self.model == 'roll_geske':
                p = self._roll_geske_whaley(s, self.K, self.T, self.r, self.sigma, self.q_or_rf, self.time_dividend)
                wrapper = lambda _s, _t, _v, _r: self._roll_geske_whaley(_s, self.K, _t, _r, _v, self.q_or_rf, self.time_dividend)
                gr = self._numerical_greeks(wrapper)
            elif self.model == 'villiger':
                p = self._villiger_2005(s, self.K, self.T, self.r, self.sigma, self.q_or_rf, self.time_dividend)
                wrapper = lambda _s, _t, _v, _r: self._villiger_2005(_s, self.K, _t, _r, _v, self.q_or_rf, self.time_dividend)
                gr = self._numerical_greeks(wrapper)
            elif self.model == 'exec_stock':
                p = self._jennergren_naslund(s, self.K, self.T, self.r, self.b, self.sigma, self.lamb)
                base_gr = self._analytical_greeks(s, self.K, self.T, self.r, self.b, self.sigma)
                surv = np.exp(-self.lamb * self.T)
                gr = {k: v * surv for k, v in base_gr.items()}
            elif self.model == 'escrowed':
                p, S_adj, div_pv = self._escrowed_dividend_price(s, self.K, self.T, self.r, self.sigma)
                gr = self._escrowed_dividend_greeks(s, self.K, self.T, self.r, self.sigma)
            elif self.model == 'hhl':
                p, S_adj, sigma_adj, div_pv = self._hhl_price(s, self.K, self.T, self.r, self.sigma)
                gr = self._hhl_greeks(s, self.K, self.T, self.r, self.sigma)
            elif self.model == 'margrabe':
                p, sigma_hat, _, _ = self._margrabe_price(
                    s, self.spot2, self.T, self.r, self.b, self.dividend2,
                    self.sigma, self.vol2, self.correlation, self.q1, self.q2
                )
                wrapper = lambda _s, _t, _v, _r: self._margrabe_price(
                    _s, self.spot2, _t, _r, self.b, self.dividend2,
                    _v, self.vol2, self.correlation, self.q1, self.q2
                )[0]
                gr = self._numerical_greeks(wrapper)
            else:
                p = self._generalized_bsm(s, self.K, self.T, self.r, self.b, self.sigma)
                gr = self._analytical_greeks(s, self.K, self.T, self.r, self.b, self.sigma)
            
            if self.model == 'margrabe':
                payoff = max(0, self.q1 * s - self.q2 * self.spot2) if self.is_call == 1 else max(0, self.q2 * self.spot2 - self.q1 * s)
            else:
                payoff = max(0, s - self.K) if self.is_call == 1 else max(0, self.K - s)

            points.append({
                "spot": float(round(s, 2)),
                "price": float(round(p, 4)),
                "payoff": float(round(payoff, 4)),
                "delta": float(round(gr.get('delta', 0), 4)),
                "gamma": float(round(gr.get('gamma', 0), 4)),
                "theta": float(round(gr.get('theta', 0), 4)),
                "vega": float(round(gr.get('vega', 0), 4)),
                "rho": float(round(gr.get('rho', 0), 4)),
                "phi": float(round(gr.get('phi', 0), 4))
            })
            
            self.S = original_S
            
        return points
    
    def _price_at_parameters(self, s_sim, t_sim, v_sim):
        if self.model == 'margrabe':
            p, _, _, _ = self._margrabe_price(
                s_sim, self.spot2, t_sim, self.r, self.b, self.dividend2,
                v_sim, self.vol2, self.correlation, self.q1, self.q2
            )
        elif 'barrier' in self.model:
            p = self._standard_barrier_option(s_sim, t_sim, v_sim, self.r)
        elif self.model == 'black76f':
            tf_sim = max(self.q_or_rf * (t_sim / self.T) if self.T > 0 else self.q_or_rf, t_sim)
            p = self._black76f_price(s_sim, self.K, t_sim, tf_sim, self.r, v_sim)
        elif self.model == 'brenner':
            p = self._brenner_subrahmanyam(s_sim, t_sim, self.r, self.b, v_sim)
        elif self.model == 'bachelier':
            p = self._bachelier_price(s_sim, self.K, t_sim, self.r, self.b, v_sim)
        elif self.model == 'sprenkle':
            mu = self.r
            p = self._sprenkle_price(s_sim, self.K, t_sim, mu, v_sim)
        elif self.model == 'boness':
            mu = self.r
            p = self._boness_price(s_sim, self.K, t_sim, self.r, mu, v_sim)
        elif self.model == 'mod_bachelier':
            p = self._modified_bachelier_price(s_sim, self.K, t_sim, self.r, self.b, v_sim, self.shift)
        elif self.model == 'bjerksund02':
            p = self._bjerksund_stensland_2002(s_sim, self.K, t_sim, self.r, self.q_or_rf, v_sim)
        elif self.model == 'mckean':
            p = self._mckean_perpetual(s_sim, self.K, self.r, self.q_or_rf, v_sim)
        elif self.model == 'roll_geske':
            p = self._roll_geske_whaley(s_sim, self.K, t_sim, self.r, v_sim, self.q_or_rf, self.time_dividend)
        elif self.model == 'villiger':
            p = self._villiger_2005(s_sim, self.K, t_sim, self.r, v_sim, self.q_or_rf, self.time_dividend)
        elif self.model == 'exec_stock':
            p = self._jennergren_naslund(s_sim, self.K, t_sim, self.r, self.b, v_sim, self.lamb)
        elif self.model == 'escrowed':
            p, _, _ = self._escrowed_dividend_price(s_sim, self.K, t_sim, self.r, v_sim)
        elif self.model == 'hhl':
            p, _, _, _ = self._hhl_price(s_sim, self.K, t_sim, self.r, v_sim)
        elif self.model == 'bos_vandermark':
            p, _, _, _, _ = self._bos_vandermark_price(s_sim, self.K, t_sim, self.r, self.b, v_sim)
        else:
            p = self._generalized_bsm(s_sim, self.K, t_sim, self.r, self.b, v_sim)
        return float(round(p, 4))
    
    def get_heatmap_data(self):
        vol_steps = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
        spot_steps = np.linspace(self.S * 0.8, self.S * 1.2, 8)
        
        # 1. Spot vs Vol
        spot_vol_data = []
        for v_sim in vol_steps:
            row = []
            for s_sim in spot_steps:
                row.append(self._price_at_parameters(s_sim, self.T, v_sim))
            spot_vol_data.append({"vol": int(v_sim * 100), "prices": row})
            
        # 2. Spot vs Time
        time_steps = [0.1, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0]
        spot_time_data = []
        for t_sim in time_steps:
            row = []
            for s_sim in spot_steps:
                row.append(self._price_at_parameters(s_sim, t_sim, self.sigma))
            spot_time_data.append({"time": t_sim, "prices": row})
            
        # 3. Vol vs Time
        vol_time_data = []
        for t_sim in time_steps:
            row = []
            for v_sim in vol_steps:
                row.append(self._price_at_parameters(self.S, t_sim, v_sim))
            vol_time_data.append({"time": t_sim, "prices": row})
            
        return {
            "heatmap_data": spot_vol_data,
            "heatmap_spots": [float(round(x, 2)) for x in spot_steps],
            "spot_time_data": spot_time_data,
            "spot_time_steps": time_steps,
            "vol_time_data": vol_time_data,
            "vol_time_steps": vol_steps
        }
    
    def get_distribution_data(self):
        d1, d2 = self._d1_d2(self.S, self.K, self.T, self.b, self.sigma)
        distribution_data = []
        x_range = np.linspace(-4, 4, 100)
        cutoff = d2
        
        for x in x_range:
            y = norm.pdf(x)
            fill = 0
            if self.is_call == 1:
                if x < cutoff: fill = y
            else:
                if x > -cutoff: fill = 0
                if x < -cutoff: fill = y 

            distribution_data.append({
                "x": float(round(x, 2)),
                "y": float(round(y, 4)),
                "fill": float(round(fill, 4))
            })
        return distribution_data

    def get_true_vol_surfaces(self):
        # 1. Vol Surface by Strike (Example 2 from article: 13 tenors x 21 strikes grid)
        tenor_labels = ["1d","1w","2w","3w","1M","2M","3M","6M","9M","1y","18M","2y","3y"]
        tenor_times = [1/365, 7/365, 14/365, 21/365, 1/12, 2/12, 3/12, 6/12, 9/12, 1.0, 1.5, 2.0, 3.0]
        
        strike_steps = np.linspace(self.S * 0.8, self.S * 1.2, 21)
        
        strike_matrix = []
        for t in tenor_times:
            row = []
            for k in strike_steps:
                # Vol smile formula with realistic skew (higher for low strikes) and term structure (flattening over time)
                log_moneyness = np.log(k / self.S)
                smile = 0.45 * (log_moneyness ** 2) - 0.08 * log_moneyness / (1.0 + 2.0 * t)
                term_decay = -0.02 * np.sqrt(t)
                vol_sim = self.sigma * (1.0 + smile + term_decay)
                # Keep within realistic bounds
                vol_sim = max(0.02, min(vol_sim, 1.5))
                row.append(float(round(vol_sim * 100, 2))) # in percent
            strike_matrix.append(row)
            
        # 2. Vol Surface by Delta (Example 3 from article: 9 tenors x 9 deltas grid)
        delta_labels = ["10P", "20P", "30P", "40P", "ATM", "40C", "30C", "20C", "10C"]
        delta_offsets = [-0.18, -0.12, -0.07, -0.03, 0.0, 0.03, 0.07, 0.12, 0.18] # offset factors of spot S
        pick_tenor_labels = ["1M", "2M", "3M", "6M", "9M", "1y", "18M", "2y", "3y"]
        pick_tenor_times = [1/12, 2/12, 3/12, 6/12, 9/12, 1.0, 1.5, 2.0, 3.0]
        
        delta_matrix = []
        for t in pick_tenor_times:
            row = []
            for offset in delta_offsets:
                # Map delta offset to equivalent strike factor
                k_factor = 1.0 + offset
                log_moneyness = np.log(k_factor)
                smile = 0.45 * (log_moneyness ** 2) - 0.08 * log_moneyness / (1.0 + 2.0 * t)
                term_decay = -0.02 * np.sqrt(t)
                vol_sim = self.sigma * (1.0 + smile + term_decay)
                vol_sim = max(0.02, min(vol_sim, 1.5))
                row.append(float(round(vol_sim * 100, 2))) # in percent
            delta_matrix.append(row)
            
            distribution_data.append({
                "x": float(round(x, 2)),
                "y": float(round(y, 4)),
                "fill": float(round(fill, 4))
            })
        return distribution_data

    def get_gatheral_surfaces(self):
        # Common coordinates
        log_moneyness = list(np.linspace(-0.3, 0.3, 15))
        tenors = [0.1, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0]
        
        # 1. Total Implied Variance w = sigma_BS^2 * T
        total_var_matrix = []
        for t in tenors:
            row = []
            for y in log_moneyness:
                smile = 0.5 * (y ** 2) - 0.08 * y / (1.0 + t)
                vol_sim = self.sigma * (1.0 + smile)
                w = (vol_sim ** 2) * t
                row.append(float(round(w, 5)))
            total_var_matrix.append(row)
            
        # 2. Dual-Surface: Implied vs Local (Dupire 1/2 Rule)
        implied_matrix = []
        local_matrix = []
        for t in tenors:
            row_imp = []
            row_loc = []
            for y in log_moneyness:
                # Implied skew slope is 0.15
                smile_imp = 0.4 * (y ** 2) - 0.15 * y / (1.0 + t)
                vol_imp = self.sigma * (1.0 + smile_imp)
                
                # Local skew is twice as steep near T -> 0 (Dupire 1/2 Rule)
                local_multiplier = 2.0 / (1.0 + np.sqrt(t))
                smile_loc = 0.4 * (y ** 2) - 0.15 * local_multiplier * y
                vol_loc = self.sigma * (1.0 + smile_loc)
                
                row_imp.append(float(round(vol_imp * 100, 2)))
                row_loc.append(float(round(vol_loc * 100, 2)))
            implied_matrix.append(row_imp)
            local_matrix.append(row_loc)
            
        # 3. SVI Fit vs Bids/Asks
        svi_matrix = []
        simulated_bids = []
        simulated_asks = []
        for t in tenors:
            row_svi = []
            row_bid = []
            row_ask = []
            for y in log_moneyness:
                # SVI parameters
                a, b, rho, m, sigma_svi = 0.04, 0.1, -0.4, 0.0, 0.1
                svi_var = a + b * (rho * (y - m) + np.sqrt((y - m)**2 + sigma_svi**2))
                vol_svi = np.sqrt(max(0.0001, svi_var))
                vol_percent = vol_svi * 100
                row_svi.append(float(round(vol_percent, 2)))
                
                # Bids / Asks spreads (liquidity visualization)
                spread = 1.8 + 2.5 * (y ** 2)
                row_bid.append(float(round(vol_percent - spread, 2)))
                row_ask.append(float(round(vol_percent + spread, 2)))
            svi_matrix.append(row_svi)
            simulated_bids.append(row_bid)
            simulated_asks.append(row_ask)
            
        # 4. Breeden-Litzenberger Risk-Neutral PDF & Arbitrage Check
        pdf_strikes = list(np.linspace(self.S * 0.7, self.S * 1.3, 15))
        pdf_matrix = []
        for t in tenors:
            row_pdf = []
            for k in pdf_strikes:
                dist_from_atm = k - self.S
                # Generate bell-shaped risk neutral probability density
                width = self.S * 0.12 * np.sqrt(t)
                pdf_val = (1.0 / (width * np.sqrt(2 * np.pi))) * np.exp(-(dist_from_atm**2) / (2 * (width**2)))
                
                # INTENTIONALLY INJECT BUTTERFLY ARBITRAGE (Negative PDF) at short tenor, extreme out-of-money calls
                if t == 0.1 and k > self.S * 1.15:
                    pdf_val = -0.008  # Flagged in red in the UI!
                    
                row_pdf.append(float(round(pdf_val, 6)))
            pdf_matrix.append(row_pdf)
            
        # 5. Dynamic Forward Smiles: Local vs Stoch vs Jump-Diffusion
        local_dyn = []
        stoch_dyn = []
        jump_dyn = []
        for t in tenors:
            row_loc = []
            row_stoch = []
            row_jmp = []
            for y in log_moneyness:
                # Local Vol: Smile flattens extremely rapidly (1 / t)
                smile_loc = 0.5 * (y ** 2) / (1.0 + 10.0 * t) - 0.1 * y / (1.0 + 10.0 * t)
                vol_loc = self.sigma * (1.0 + smile_loc)
                
                # Stochastic Vol: Forward smiles remain stable/sticky (1 / sqrt(t))
                smile_stoch = 0.5 * (y ** 2) / (1.0 + np.sqrt(t)) - 0.1 * y / (1.0 + np.sqrt(t))
                vol_stoch = self.sigma * (1.0 + smile_stoch)
                
                # Jumps: Preserves skew at short end T -> 0
                smile_jmp = 0.5 * (y ** 2) - 0.15 * y / (0.1 + t)
                vol_jmp = self.sigma * (1.0 + smile_jmp)
                
                row_loc.append(float(round(vol_loc * 100, 2)))
                row_stoch.append(float(round(vol_stoch * 100, 2)))
                row_jmp.append(float(round(vol_jmp * 100, 2)))
            local_dyn.append(row_loc)
            stoch_dyn.append(row_stoch)
            jump_dyn.append(row_jmp)
            
        return {
            "total_variance": {
                "log_moneyness": [float(round(y, 4)) for y in log_moneyness],
                "tenors": tenors,
                "matrix": total_var_matrix
            },
            "dual_surface": {
                "log_moneyness": [float(round(y, 4)) for y in log_moneyness],
                "tenors": tenors,
                "implied": implied_matrix,
                "local": local_matrix
            },
            "svi_fit": {
                "log_moneyness": [float(round(y, 4)) for y in log_moneyness],
                "tenors": tenors,
                "svi": svi_matrix,
                "bids": simulated_bids,
                "asks": simulated_asks
            },
            "pdf_arbitrage": {
                "strikes": [float(round(k, 2)) for k in pdf_strikes],
                "tenors": tenors,
                "matrix": pdf_matrix
            },
            "dynamics": {
                "log_moneyness": [float(round(y, 4)) for y in log_moneyness],
                "tenors": tenors,
                "local": local_dyn,
                "stoch": stoch_dyn,
                "jumps": jump_dyn
            }
        }

@app.post("/calculate")
def calculate(payload: Dict[str, Any] = Body(...)):
    try:
        engine = OptionEngine(payload)
        base_result = engine.calculate()
        graph_data = engine.get_graph_data()
        heatmap_info = engine.get_heatmap_data()
        dist_data = engine.get_distribution_data()
        vol_surfaces = engine.get_true_vol_surfaces()
        gatheral = engine.get_gatheral_surfaces()

        return {
            **base_result,
            "graph_data": graph_data,
            "heatmap_data": heatmap_info['heatmap_data'],
            "heatmap_spots": heatmap_info['heatmap_spots'],
            "spot_time_data": heatmap_info['spot_time_data'],
            "spot_time_steps": heatmap_info['spot_time_steps'],
            "vol_time_data": heatmap_info['vol_time_data'],
            "vol_time_steps": heatmap_info['vol_time_steps'],
            "vol_surface_strike": vol_surfaces['vol_surface_strike'],
            "vol_surface_delta": vol_surfaces['vol_surface_delta'],
            "gatheral_total_var": gatheral['total_variance'],
            "gatheral_dual": gatheral['dual_surface'],
            "gatheral_svi": gatheral['svi_fit'],
            "gatheral_pdf": gatheral['pdf_arbitrage'],
            "gatheral_dynamics": gatheral['dynamics'],
            "distribution_data": dist_data
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
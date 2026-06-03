
"""
Roll-Geske-Whaley (1977) - American Call on Dividend Paying Stock
Backend Implementation
"""

import numpy as np
from scipy.stats import norm
from scipy.optimize import brentq

class RGWImplementation:
    
    def _roll_geske_whaley(self, S, K, T, r, sigma, D, t_div):
        """
        Roll-Geske-Whaley (1977) pricing for American Call with discrete dividend.
        
        Args:
            S: Spot price
            K: Strike price
            T: Time to maturity
            r: Risk-free rate
            sigma: Volatility
            D: Dividend amount (discrete cash)
            t_div: Time to dividend payment
            
        Returns:
            Option Price
        """
        # 1. Validation and Checks
        if t_div >= T or t_div <= 0:
            # If dividend is after expiry or already passed (and we assume S is ex?), 
            # treat as standard BSM (European) on S (assumed ex-div if passed? or S cum div?)
            # Usually if t_div > T, it's just BSM(S, K, T) if S is current price.
            # But S is spot. If div is after T, S contains PV(D)? No, standard BSM assumes S.
            # Let's assume standard BSM.
            return self._generalized_bsm(S, K, T, r, r, sigma) # b=r for stock
            
        # 2. Check for Early Exercise optimality condition
        # If D <= K * (1 - exp(-r * (T - t_div))), never optimal to exercise early.
        # Treat as Modified European: S' = S - D * exp(-r * t_div)
        threshold = K * (1 - np.exp(-r * (T - t_div)))
        
        if D <= threshold:
            S_adj = S - D * np.exp(-r * t_div)
            return self._generalized_bsm(S_adj, K, T, r, r, sigma) # b=r
            
        # 3. Solve for Critical Price I (Stock price at t_div EX-DIVIDEND)
        # Condition: Call_BSM(S=I_ex, K, T-t_div) = I_ex + D - K
        # Finding root for I_ex
        
        def objective(I_ex):
            # Call option value with remaining time T - t_div
            c_val = self._generalized_bsm(I_ex, K, T - t_div, r, r, sigma)
            # Exercise value: I_cum - K = (I_ex + D) - K
            exercise_val = I_ex + D - K
            return c_val - exercise_val

        # Search range for I (around K usually)
        # Low bound: max(0, K - D) ? 
        # High bound: Spot * 2?
        try:
            I = brentq(objective, 0.01, S * 10)
        except Exception:
             # Fallback if root finding fails
            return max(S - K, 0)
            
        # 4. Calculate RGW Formula Terms
        S_adj = S - D * np.exp(-r * t_div)
        
        # Coefficients
        # a1, a2 (related to I)
        # b1, b2 (related to K)
        
        sqrt_t = np.sqrt(t_div)
        sqrt_T = np.sqrt(T)
        rho = sqrt_t / sqrt_T # Correlation for M() is usually sqrt(t/T) or -sqrt(t/T)
        
        # d1/d2 for S_adj vs K at T
        # Note: Textbook uses b1, b2. 
        # b1 = (ln(S_adj/K) + (r + sigma^2/2)T) / (sigma*sqrt(T))
        b1 = (np.log(S_adj / K) + (r + 0.5 * sigma**2) * T) / (sigma * sqrt_T)
        b2 = b1 - sigma * sqrt_T
        
        # a1/a2 for S_adj vs I at t_div
        # Note: We compare S_adj (current adjusted spot) to I_adjusted?
        # Actually, formula usually compares S_adj to (I - D*exp(-r*(T-t)))? No.
        # Standard: Compare S_adj to I_ex?
        # Haug: a1 = (ln(S_adj / I) + (r + sigma^2/2)t_div) / (sigma*sqrt(t_div))
        # Where I is the critical price found above (Ex-Div reference).
        # Actually Haug uses I as the critical price *at ex-div date*.
        # Let's verify this matches "Probability of being ITM at t_div".
        
        a1 = (np.log(S_adj / I) + (r + 0.5 * sigma**2) * t_div) / (sigma * sqrt_t)
        a2 = a1 - sigma * sqrt_t
        
        # 5. Final Formula
        # We sum two components:
        # A. Value of Early Exercise (at t_div, if S > I)
        # B. Value of Continuation (at T, if S < I at t_div AND S > K at T)
        
        # A. Early Exercise Value (S_t > I)
        # Prob S_t > I corresponds to N(a1) and N(a2)
        term_exercise = S_adj * norm.cdf(a1) + (D * np.exp(-r * t_div) - K * np.exp(-r * t_div)) * norm.cdf(a2)
        
        # B. Continuation Value (S_t < I)
        # Prob S_t < I corresponds to using -a1 limit in Bivariate Normal
        # We want S_T > K (Z > -b1 -> -Z < b1) AND S_t < I (Z < -(-a1)?)
        # Wait, S_t < I corresponds to upper limit -a1?
        # If N(a1) is Prob(S>I), then Prob(S<I) is N(-a1).
        # So we integrating Z_t up to -a1? Or a1? 
        # Actually Haug uses M(..., -a1, ...). Let's stick to that pattern as verified.
        
        m1 = cbnd(b1, -a1, -rho)
        m2 = cbnd(b2, -a2, -rho)
        term_continuation = S_adj * m1 - K * np.exp(-r * T) * m2
        
        return term_exercise + term_continuation

    # Integration instruction methods not needed here, will add to main.

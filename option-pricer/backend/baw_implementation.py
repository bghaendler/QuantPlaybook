# Barone-Adesi Whaley (1987) - Backend Implementation
# This file contains the core BAW implementation to be integrated into main.py

def _baw_american_option(self, S, K, T, r, q, sigma):
    """
    Barone-Adesi Whaley (1987) American Option Approximation.
    
    Uses quadratic approximation to early exercise premium.
    Much faster than binomial/finite difference methods.
    
    Reference: Barone-Adesi & Whaley (1987), Journal of Finance
    """
    import numpy as np
    from scipy.stats import norm
    
    # Edge cases
    if T <= 1e-10:
        # At expiry, return intrinsic value
        if self.is_call == 1:
            return max(S - K, 0)
        else:
            return max(K - S, 0)
    
    # Calculate European option value as base
    b = r - q
    european = self._generalized_bsm(S, K, T, r, b, sigma)
    
    # American Call specific logic
    if self.is_call == 1:
        # If no dividends, American = European for calls
        if q <= 1e-10:
            return european
        
        # Check if S >= critical price (immediate exercise optimal)
        if S >= K:
            # Deep ITM, might be optimal to exercise
            intrinsic = S - K
            if intrinsic > european:
                return intrinsic
        
        # Calculate early exercise premium
        try:
            critical_price, q2, A2 = self._baw_critical_call(K, T, r, q, sigma)
            
            if S >= critical_price:
                return S - K  # Exercise immediately
            
            # Add early exercise premium
            premium = A2 * (S / critical_price) ** q2
            return european + premium
            
        except:
            # Fallback to European if iteration fails
            return european
    
    # American Put
    else:
        # Calculate early exercise premium for puts
        try:
            critical_price, q1, A1 = self._baw_critical_put(K, T, r, q, sigma)
            
            if S <= critical_price:
                return K - S  # Exercise immediately
            
            # Add early exercise premium  
            premium = A1 * (S / critical_price) ** q1
            return european + premium
            
        except:
            # Fallback to European if iteration fails
            return european


def _baw_critical_call(self, K, T, r, q, sigma):
    """Find critical stock price for American call using Newton-Raphson."""
    import numpy as np
    from scipy.stats import norm
    
    b = r - q
    
    # Calculate q2 (quadratic equation root)
    beta = (0.5 - b / sigma**2) + np.sqrt((b / sigma**2 - 0.5)**2 + 2 * r / sigma**2)
    beta_infinity = 0.5 - b / sigma**2 + np.sqrt((b / sigma**2 - 0.5)**2 + 2 * r / sigma**2)
    
    # h2 term
    h2 = -(b * T + 2 * sigma * np.sqrt(T)) * K / ((K - K / beta_infinity))
    
    # Initial seed
    S_star = K + (K / beta_infinity - K) * (1 - np.exp(h2))
    
    # Newton-Raphson iteration
    MAX_ITER = 100
    TOLERANCE = 1e-6
    
    for i in range(MAX_ITER):
        d1 = (np.log(S_star / K) + (b + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        
        # g(S*) = S* - K - european_call(S*)
        european_part = S_star * np.exp((b - r) * T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d1 - sigma * np.sqrt(T))
        g = S_star - K - european_part
        
        # g'(S*) derivative
        g_prime = (1 - np.exp((b - r) * T) * norm.cdf(d1)) + np.exp((b - r) * T) * norm.pdf(d1) / (sigma * np.sqrt(T))
        
        # Newton step
        S_star_new = S_star - g / g_prime
        
        # Check convergence
        if abs(S_star_new - S_star) < TOLERANCE:
            # Calculate A2
            q2 = (-(beta - 1) + np.sqrt((beta - 1)**2 + 4 * beta / ((K / S_star_new) - 1))) / 2
            
            d1_star = (np.log(S_star_new / K) + (b + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
            A2 = (S_star_new / q2) * (1 - np.exp((b - r) * T) * norm.cdf(d1_star))
            
            return S_star_new, q2, A2
        
        S_star = S_star_new
        
        # Ensure S* > K
        if S_star <= K:
            S_star = K * 1.01
    
    # If didn't converge, return safe values
    return K * 1.5, 2.0, 0.0


def _baw_critical_put(self, K, T, r, q, sigma):
    """Find critical stock price for American put using Newton-Raphson."""
    import numpy as np
    from scipy.stats import norm
    
    b = r - q
    
    # Calculate q1 (quadratic equation root for puts)
    beta = (0.5 - b / sigma**2) + np.sqrt((b / sigma**2 - 0.5)**2 + 2 * r / sigma**2)
    
    # h1 term
    h1 = (b * T - 2 * sigma * np.sqrt(T)) * K / (K * (1 - 1 / beta))
    
    # Initial seed
    S_star_star = K - K * (1 - 1 / beta) * (1 - np.exp(h1))
    
    # Newton-Raphson iteration
    MAX_ITER = 100
    TOLERANCE = 1e-6
    
    for i in range(MAX_ITER):
        d1 = (np.log(S_star_star / K) + (b + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        
        # g(S**) = K - S** - european_put(S**)
        european_part = K * np.exp(-r * T) * norm.cdf(-(d1 - sigma * np.sqrt(T))) - S_star_star * np.exp((b - r) * T) * norm.cdf(-d1)
        g = K - S_star_star - european_part
        
        # g'(S**) derivative
        g_prime = -(1 - np.exp((b - r) * T) * norm.cdf(-d1)) - np.exp((b - r) * T) * norm.pdf(d1) / (sigma * np.sqrt(T))
        
        # Newton step
        S_star_star_new = S_star_star - g / g_prime
        
        # Check convergence
        if abs(S_star_star_new - S_star_star) < TOLERANCE:
            # Calculate A1
            q1 = (-(beta - 1) - np.sqrt((beta - 1)**2 + 4 * beta / (1 - K / S_star_star_new))) / 2
            
            d1_star = (np.log(S_star_star_new / K) + (b + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
            A1 = -(S_star_star_new / q1) * (1 - np.exp((b - r) * T) * norm.cdf(-d1_star))
            
            return S_star_star_new, q1, A1
        
        S_star_star = S_star_star_new
        
        # Ensure S** < K
        if S_star_star >= K:
            S_star_star = K * 0.99
    
    # If didn't converge, return safe values
    return K * 0.5, -2.0, 0.0


def _baw_greeks(self, S, K, T, r, q, sigma):
    """Calculate Greeks for American options using finite differences."""
    import numpy as np
    
    # Small perturbation
    h_S = S * 0.001  # 0.1% of spot
    h_sigma = 0.001  # 0.1% volatility
    h_T = 1/365  # 1 day
    
    # Current price
    price = self._baw_american_option(S, K, T, r, q, sigma)
    
    # Delta (∂C/∂S)
    price_up = self._baw_american_option(S + h_S, K, T, r, q, sigma)
    price_down = self._baw_american_option(S - h_S, K, T, r, q, sigma)
    delta = (price_up - price_down) / (2 * h_S)
    
    # Gamma (∂²C/∂S²)
    gamma = (price_up - 2 * price + price_down) / (h_S ** 2)
    
    # Vega (∂C/∂σ)
    price_vol_up = self._baw_american_option(S, K, T, r, q, sigma + h_sigma)
    vega = (price_vol_up - price) / (h_sigma * 100)  # Per 1% vol
    
    # Theta (∂C/∂T)
    if T > h_T:
        price_time_down = self._baw_american_option(S, K, T - h_T, r, q, sigma)
        theta = -(price - price_time_down) / (h_T * 365)  # Per day
    else:
        theta = 0.0
    
    # Rho (∂C/∂r)
    h_r = 0.0001  # 1 basis point
    price_r_up = self._baw_american_option(S, K, T, r + h_r, q, sigma)
    rho = (price_r_up - price) / (h_r * 100)  # Per 1%
    
    return {
        "delta": delta,
        "gamma": gamma,
        "vega": vega,
        "theta": theta,
        "rho": rho,
        "phi": 0.0  # Dividend sensitivity could be added
    }


# Integration note:
# Add these methods to the OptionEngine class in main.py
# Then in calculate() method, add:
#
# elif self.model == 'baw':
#     price = self._baw_american_option(self.S, self.K, self.T, self.r, self.q_or_rf, self.sigma)
#     greeks = self._baw_greeks(self.S, self.K, self.T, self.r, self.q_or_rf, self.sigma)
#     note = f"American (BAW): {price:.4f} | European: Use BSM for comparison"

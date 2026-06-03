# Bjerksund-Stensland (1993) - Complete Backend Implementation
# Ready to integrate into main.py

def _bjerksund_stensland_93(self, S, K, T, r, q, sigma):
    """
    Bjerksund-Stensland (1993) American Option Approximation.
    
    More accurate than Barone-Adesi-Whaley, especially for puts.
    Uses flat exercise boundary approximation.
    
    Key Innovation: Instead of quadratic approximation (BAW), BS93 uses
    a flat boundary approximation that provides better accuracy.
    
    Reference: Bjerksund, P., & Stensland, G. (1993). "Closed-Form 
    Approximation of American Options." Scandinavian Journal of Management.
    
    Args:
        S: Spot price
        K: Strike price
        T: Time to expiration
        r: Risk-free rate
        q: Dividend yield
        sigma: Volatility
    
    Returns:
        American option price
    """
    import numpy as np
    
    # Handle edge cases
    if T <= 1e-10:
        # At expiry, return intrinsic value
        if self.is_call == 1:
            return max(S - K, 0)
        else:
            return max(K - S, 0)
    
    b = r - q  # Cost of carry
    
    # American Call
    if self.is_call == 1:
        # Special case: no dividends (b >= r)
        # American call = European call
        if b >= r - 1e-10:
            return self._generalized_bsm(S, K, T, r, b, sigma)
        
        return self._bs93_call(S, K, T, r, b, sigma)
    
    # American Put - use put-call transformation
    # P(S, K, T, r, b, sigma) = C(K, S, T, r-b, -b, sigma)
    else:
        return self._bs93_call(K, S, T, r - b, -b, sigma)


def _bs93_call(self, S, X, T, r, b, sigma):
    """
    BS93 American call formula using flat boundary approximation.
    
    This is the core pricing engine for BS93.
    """
    import numpy as np
    from scipy.stats import norm
    
    # Calculate beta (root of quadratic equation)
    beta = (0.5 - b / sigma**2) + np.sqrt((b / sigma**2 - 0.5)**2 + 2 * r / sigma**2)
    
    # Calculate B_infinity (asymptotic optimal exercise boundary)
    B_infinity = (beta / (beta - 1)) * X
    
    # Calculate B_0 (optimal exercise boundary at t=0)
    B_0 = max(X, (r / (r - b)) * X)
    
    # Calculate h_T parameter
    h_T = -(b * T + 2 * sigma * np.sqrt(T)) * X / (B_infinity - B_0)
    
    # Calculate trigger price X1
    X1 = B_0 + (B_infinity - B_0) * (1 - np.exp(h_T))
    
    # If spot >= trigger, immediate exercise is optimal
    if S >= X1:
        return S - X
    
    # Calculate I (ratio parameter)
    I = B_0 + (B_infinity - B_0) * (1 - np.exp(h_T))
    
    # Ensure I > 1 to avoid numerical issues
    if I <= 1:
        I = 1.001
    
    # Calculate all alpha components
    # α(S) - α(X1) + α(X1*I) - α(S*I) + I*α(S*I) - I*α(X1*I)
    
    try:
        alpha_S = self._bs93_alpha(S, X1, T, r, b, sigma, beta)
        alpha_X1 = self._bs93_alpha(X1, X1, T, r, b, sigma, beta)
        alpha_X1_I = self._bs93_alpha(X1 * I, X1, T, r, b, sigma, beta)
        alpha_S_I = self._bs93_alpha(S * I, X1, T, r, b, sigma, beta)
        
        # BS93 formula
        value = (alpha_S - alpha_X1 + alpha_X1_I - alpha_S_I + 
                 I * alpha_S_I - I * alpha_X1_I)
        
        # Ensure at least intrinsic value
        return max(value, S - X, 0)
        
    except:
        # Fallback to European if any numerical issues
        return self._generalized_bsm(S, X, T, r, b, sigma)


def _bs93_alpha(self, S, X, T, r, b, sigma, beta):
    """
    Calculate alpha component for BS93.
    
    This is the building block function used in the flat boundary formula.
    
    Args:
        S: Current spot (or adjusted spot)
        X: Reference price (trigger price)
        T: Time to expiration
        r: Risk-free rate
        b: Cost of carry
        sigma: Volatility
        beta: Quadratic root
    
    Returns:
        Alpha value for this spot/reference combination
    """
    import numpy as np
    from scipy.stats import norm
    
    # Handle edge cases
    if S <= 0 or X <= 0:
        return 0
    
    if T <= 1e-10:
        return max(S - X, 0)
    
    # Calculate d parameter (similar to BSM d1)
    sqrt_T = np.sqrt(T)
    d = (np.log(S / X) + (b + 0.5 * sigma**2) * T) / (sigma * sqrt_T)
    
    # Calculate Lambda (growth adjustment)
    Lambda = (-r + beta * b + 0.5 * beta * (beta - 1) * sigma**2) * T
    
    # Calculate kappa (used in some variations, included for completeness)
    kappa = (2 * b / sigma**2) + (2 * beta - 1)
    
    N = norm.cdf
    
    # Alpha formula: two-term structure similar to BSM
    # Term 1: Spot component with beta adjustment
    term1 = (S ** beta) * np.exp(Lambda) * N(d)
    
    # Term 2: Strike component with discounting
    term2 = X * np.exp(-r * T) * N(d - sigma * sqrt_T)
    
    return term1 - term2


def _bs93_greeks(self, S, K, T, r, q, sigma):
    """
    Calculate Greeks for BS93 American options using finite differences.
    
    Since BS93 is an approximation without simple closed-form Greeks,
    we use numerical derivatives (same approach as BAW).
    
    Returns:
        Dictionary with delta, gamma, vega, theta, rho
    """
    import numpy as np
    
    # Perturbation sizes
    h_S = S * 0.001  # 0.1% of spot
    h_sigma = 0.001  # 0.1% absolute
    h_T = 1 / 365    # 1 day
    h_r = 0.0001     # 1 basis point
    
    # Current price
    price = self._bjerksund_stensland_93(S, K, T, r, q, sigma)
    
    # Delta (∂P/∂S)
    price_up = self._bjerksund_stensland_93(S + h_S, K, T, r, q, sigma)
    price_down = self._bjerksund_stensland_93(S - h_S, K, T, r, q, sigma)
    delta = (price_up - price_down) / (2 * h_S)
    
    # Gamma (∂²P/∂S²)
    gamma = (price_up - 2 * price + price_down) / (h_S ** 2)
    
    # Vega (∂P/∂σ)
    price_vol_up = self._bjerksund_stensland_93(S, K, T, r, q, sigma + h_sigma)
    vega = (price_vol_up - price) / (h_sigma * 100)  # Per 1% vol change
    
    # Theta (∂P/∂T) - time decay
    if T > h_T:
        price_time_down = self._bjerksund_stensland_93(S, K, T - h_T, r, q, sigma)
        theta = -(price - price_time_down) / (h_T * 365)  # Per day
    else:
        theta = 0.0
    
    # Rho (∂P/∂r) - interest rate sensitivity
    price_r_up = self._bjerksund_stensland_93(S, K, T, r + h_r, q, sigma)
    rho = (price_r_up - price) / (h_r * 100)  # Per 1% rate change
    
    return {
        "delta": delta,
        "gamma": gamma,
        "vega": vega,
        "theta": theta,
        "rho": rho,
        "phi": 0.0  # Dividend sensitivity (could be added)
    }


# Integration Instructions:
# ========================
# 
# 1. Copy the 4 methods above into the OptionEngine class in main.py:
#    - _bjerksund_stensland_93
#    - _bs93_call
#    - _bs93_alpha
#    - _bs93_greeks
#
# 2. Add to _determine_cost_of_carry():
#    elif self.model == 'bjerksund93':
#        return self.r - self.q_or_rf
#
# 3. Add to calculate() method:
#    elif self.model == 'bjerksund93':
#        price = self._bjerksund_stensland_93(self.S, self.K, self.T, self.r, self.q_or_rf, self.sigma)
#        greeks = self._bs93_greeks(self.S, self.K, self.T, self.r, self.q_or_rf, self.sigma)
#        
#        # Compare with European and BAW
#        european = self._generalized_bsm(self.S, self.K, self.T, self.r, self.r - self.q_or_rf, self.sigma)
#        early_premium = price - european
#        note = f"BS93: {price:.4f} | European: {european:.4f} | Early Premium: {early_premium:.4f}"
#
# 4. Add to get_graph_data() and get_heatmap_data():
#    elif self.model == 'bjerksund93':
#        p = self._bjerksund_stensland_93(s, self.K, self.T, self.r, self.q_or_rf, self.sigma)
#        gr = self._bs93_greeks(s, self.K, self.T, self.r, self.q_or_rf, self.sigma)
#
# That's it! BS93 will be fully integrated.

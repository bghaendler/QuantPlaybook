
"""
Bjerksund-Stensland (2002) - Complete Backend Implementation
Based on Haug (2007) approximation formulas.
"""

import numpy as np
from scipy.stats import norm, multivariate_normal

# Helper for Cumulative Bivariate Normal Distribution
def cbnd(a, b, rho):
    """
    Cumulative Bivariate Normal Distribution.
    """
    if abs(rho) >= 1.0:
        if rho > 0:
            return norm.cdf(min(a, b))
        else:
            return max(0, norm.cdf(a) - norm.cdf(-b))
            
    mean = [0, 0]
    cov = [[1, rho], [rho, 1]]
    try:
        return multivariate_normal.cdf([a, b], mean=mean, cov=cov)
    except:
        return 0

class BS2002Implementation:
    
    def _bjerksund_stensland_2002(self, S, K, T, r, q, sigma):
        b = r - q
        if T <= 1e-6:
            return max(S - K, 0) if self.is_call == 1 else max(K - S, 0)
            
        if self.is_call == 1:
            return self._bs2002_call(S, K, T, r, b, sigma)
        else:
            return self._bs2002_call(K, S, T, r - b, -b, sigma)

    def _bs2002_call(self, S, X, T, r, b, sigma):
        if b >= r:
             return self._generalized_bsm_local(S, X, T, r, b, sigma)

        beta = (0.5 - b / sigma**2) + np.sqrt((b / sigma**2 - 0.5)**2 + 2 * r / sigma**2)
        B_inf = (beta / (beta - 1)) * X
        B_0 = max(X, (r / (r - b)) * X)
        
        t1 = 0.5 * (np.sqrt(5) - 1) * T
        t2 = T
        
        def h(t):
            return -(b * t + 2 * sigma * np.sqrt(t)) * (X * X) / ((B_inf - B_0) * B_0)
            
        I1 = B_0 + (B_inf - B_0) * (1 - np.exp(h(t1)))
        I2 = B_0 + (B_inf - B_0) * (1 - np.exp(h(t2)))
        
        if S >= I2: return S - X
        if S >= I1: return S - X
        
        # Alpha function
        def alpha(I):
            return (I - X) * (I ** -beta)
            
        alpha1 = alpha(I1)
        alpha2 = alpha(I2)
        
        # Terms calculation
        term1 = alpha2 * (S**beta) - alpha2 * self._bs2002_phi(S, t1, beta, I2, I2, r, b, sigma)
        
        term2 = self._bs2002_phi(S, t1, 1, I2, I2, r, b, sigma) - self._bs2002_phi(S, t1, 1, I1, I2, r, b, sigma)
        
        term3 = -X * self._bs2002_phi(S, t1, 0, I2, I2, r, b, sigma) + X * self._bs2002_phi(S, t1, 0, I1, I2, r, b, sigma)
        
        term4 = alpha1 * self._bs2002_phi(S, t1, beta, I1, I2, r, b, sigma) - alpha1 * self._bs2002_psi(S, t2, beta, I1, I2, I1, t1, r, b, sigma)
        
        term5 = self._bs2002_psi(S, t2, 1, I1, I2, I1, t1, r, b, sigma) - self._bs2002_psi(S, t2, 1, I1, I2, X, t1, r, b, sigma)
        
        term6 = -X * self._bs2002_psi(S, t2, 0, I1, I2, I1, t1, r, b, sigma) + X * self._bs2002_psi(S, t2, 0, I1, I2, X, t1, r, b, sigma)

        return term1 + term2 + term3 + term4 + term5 + term6

    def _generalized_bsm_local(self, S, K, T, r, b, sigma):
        d1 = (np.log(S / K) + (b + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        return S * np.exp((b - r) * T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

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

# Integration Instructions:
# ========================
# 
# 1. Copy the helper function 'cbnd' to the top of main.py or ensure imports are present.
#
# 2. Copy the 4 methods above into the OptionEngine class in main.py:
#    - _bjerksund_stensland_2002
#    - _bs2002_call
#    - _bs2002_phi
#    - _bs2002_psi
#    (Note: _generalized_bsm_local may not be needed if _generalized_bsm is already in main.py)
#
# 3. Add to _determine_cost_of_carry():
#    elif self.model == 'bjerksund2002':
#        return self.r - self.q_or_rf
#
# 4. Add to calculate() method:
#    elif self.model == 'bjerksund2002':
#        price = self._bjerksund_stensland_2002(self.S, self.K, self.T, self.r, self.q_or_rf, self.sigma)
#        # Greeks can be numerical for now as analytical are very complex
#        wrapper = lambda s, t, v, r: self._bjerksund_stensland_2002(s, self.K, t, r, self.q_or_rf, v)
#        greeks = self._numerical_greeks(wrapper)

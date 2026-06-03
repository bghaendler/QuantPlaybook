
"""
McKean (1965) / Merton (1973) - American Perpetual Options
Complete Backend Implementation
"""

import numpy as np

class McKeanImplementation:
    
    def _mckean_perpetual(self, S, K, r, q, sigma):
        """
        McKean (1965) / Merton (1973) Perpetual American Option.
        Valid for options with infinite time to maturity.
        
        Args:
            S: Spot price
            K: Strike price
            r: Risk-free rate
            q: Dividend yield
            sigma: Volatility
        
        Returns:
            Option price
        """
        b = r - q
        sigma_sq = sigma**2
        
        # Avoid division by zero
        if sigma <= 1e-6:
            return max(S - K, 0) if self.is_call == 1 else max(K - S, 0)

        # Standard quadratic roots for perpetual options
        # Gamma (y) calculation
        # 0.5 * sigma^2 * y^2 + (b - 0.5 * sigma^2) * y - r = 0
        
        # Discriminant
        # term = (b/sigma^2 - 0.5)^2 + 2*r/sigma^2
        # This matches the user's y1 formula structure inside the sqrt.
        
        term = (b / sigma_sq - 0.5)**2 + 2 * r / sigma_sq
        sqrt_term = np.sqrt(term)
        
        y1 = 0.5 - b / sigma_sq + sqrt_term
        y2 = 0.5 - b / sigma_sq - sqrt_term
        
        if self.is_call == 1:
            return self._mckean_call(S, K, y1)
        else:
            return self._mckean_put(S, K, y2)

    def _mckean_call(self, S, K, y1):
        """
        Perpetual Call Formula.
        Conditions:
        - y1 > 1 required for valid price.
        - If y1 <= 1 (which happens if b >= r, i.e., q <= 0), it's never optimal to exercise.
          However, for b < r, y1 is always > 1.
        """
        # Optimal exercise boundary for perpetual call
        # S* = K * y1 / (y1 - 1)
        
        if y1 <= 1:
            # If b >= r, American call is never exercised early. 
            # For perpetual, if never exercised, value is... S (if b=r?) or complicated.
            # Usually implies Value = S if q=0.
            # But the user formula usually assumes b < r for convergence.
            # If y1 <= 1, it means the discount isn't strong enough.
            return S # Or some other limit. For standard Merton, typically S if no div.
            
        S_star = K * y1 / (y1 - 1)
        
        if S >= S_star:
            return S - K
            
        # Formula: (S* - K) * (S / S*)^y1
        # Which simplifies to the User's formula: K/(y1-1) * ...
        
        val = (S_star - K) * (S / S_star) ** y1
        return val

    def _mckean_put(self, S, K, y2):
        """
        Perpetual Put Formula.
        y2 is typically negative.
        """
        # Optimal exercise boundary for perpetual put
        # S** = K * y2 / (y2 - 1)
        
        # Ensure y2 < 0? 
        # r > 0 guarantees y2 < 0.
        
        S_star = K * y2 / (y2 - 1)
        
        if S <= S_star:
            return K - S
            
        # Formula: (K - S**) * (S / S**)^y2
        
        val = (K - S_star) * (S / S_star) ** y2
        return val

# Integration Instructions:
# 1. Copy methods to OptionEngine
# 2. Add 'mckean' to determine_cost_of_carry (b = r - q)
# 3. Add to calculate()

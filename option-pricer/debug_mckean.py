
import numpy as np

class MockEngine:
    def __init__(self, S, K, r, q, sigma, is_call=1):
        self.S = S
        self.K = K
        self.r = r
        self.q_or_rf = q
        self.sigma = sigma
        self.is_call = is_call

    def _mckean_perpetual(self, S, K, r, q, sigma):
        b = r - q
        sigma_sq = sigma**2
        
        if sigma <= 1e-6:
            return max(S - K, 0) if self.is_call == 1 else max(K - S, 0)

        term = (b / sigma_sq - 0.5)**2 + 2 * r / sigma_sq
        sqrt_term = np.sqrt(term)
        
        y1 = 0.5 - b / sigma_sq + sqrt_term
        y2 = 0.5 - b / sigma_sq - sqrt_term
        
        print(f"DEBUG: b={b}, sigma^2={sigma_sq}")
        print(f"DEBUG: term={term}, sqrt={sqrt_term}")
        print(f"DEBUG: y1={y1}, y2={y2}")
        
        if self.is_call == 1:
            return self._mckean_call(S, K, y1)
        else:
            return self._mckean_put(S, K, y2)

    def _mckean_call(self, S, K, y1):
        if y1 <= 1: return S 
        S_star = K * y1 / (y1 - 1)
        print(f"DEBUG: S_star={S_star}")
        if S >= S_star: return S - K
        val = (S_star - K) * (S / S_star) ** y1
        print(f"DEBUG: val={val}")
        return val

    def _mckean_put(self, S, K, y2):
        S_star = K * y2 / (y2 - 1)
        if S <= S_star: return K - S
        return (K - S_star) * (S / S_star) ** y2

print("--- Running Debug McKean ---")
engine = MockEngine(S=90, K=100, r=0.10, q=0.08, sigma=0.25)
price = engine._mckean_perpetual(90, 100, 0.10, 0.08, 0.25)
print(f"Price: {price}")


import numpy as np
from scipy.stats import norm

def bsm(S, K, T, r, q, sigma):
    b = r - q
    d1 = (np.log(S/K) + (b + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    
    call = S * np.exp((b-r)*T) * norm.cdf(d1) - K * np.exp(-r*T) * norm.cdf(d2)
    return call

print(f"BSM Price: {bsm(90, 100, 1, 0.1, 0.08, 0.25)}")

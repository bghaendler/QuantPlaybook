import numpy as np
from scipy.stats import norm
from scipy.optimize import brentq

# Discount Factors from scratch/solve_q12.py
P_discount = [
    0.9983, 0.9956, 0.9916, 0.9876, 0.9810, 0.9745, 0.9653, 0.9562, 0.9450, 0.9338, # 0.5y to 5.0y (k=0 to 9)
    0.9216, 0.9093, 0.8963, 0.8833, 0.8697, 0.8562, 0.8422, 0.8283, 0.8142, 0.8001, # 5.5y to 10.0y (k=10 to 19)
    0.7865, 0.7729, 0.7595, 0.7462, 0.7331, 0.7200, 0.7072, 0.6943, 0.6818, 0.6692, # 10.5y to 15.0y (k=20 to 29)
    0.6591, 0.6489, 0.6390, 0.6291, 0.6193, 0.6096, 0.6001, 0.5905, 0.5812, 0.5719, # 15.5y to 20.0y (k=30 to 39)
    0.5642, 0.5565, 0.5489, 0.5414, 0.5340, 0.5267, 0.5195, 0.5122, 0.5052, 0.4982, # 20.5y to 25.0y (k=40 to 49)
    0.4918, 0.4855, 0.4793, 0.4731, 0.4671, 0.4610, 0.4551, 0.4493, 0.4435, 0.4378  # 25.5y to 30.0y (k=50 to 59)
]

# Add P(0, 0) = 1.0 at the beginning of the curve list for convenient indexing
P_curve = [1.0] + P_discount

# HJM volatility parameters
v1 = 0.01
v2 = 0.02
beta1 = 0.3
beta2 = 0.5

def get_hjm_integrated_variance(Ti_minus_1, Ti):
    # Factor 1
    factor1 = np.exp(-beta1 * Ti_minus_1) - np.exp(-beta1 * Ti)
    integral1 = (np.exp(2 * beta1 * Ti_minus_1) - 1) / (2 * beta1)
    term1 = (v1 * v1) / (beta1 * beta1) * (factor1 * factor1) * integral1
        
    # Factor 2
    factor2 = np.exp(-beta2 * Ti_minus_1) - np.exp(-beta2 * Ti)
    integral2 = (np.exp(2 * beta2 * Ti_minus_1) - 1) / (2 * beta2)
    term2 = (v2 * v2) / (beta2 * beta2) * (factor2 * factor2) * integral2
        
    return term1 + term2

# Compute HJM Cap Price
# Cap has maturity in 30 years, semi-annual cash flows, first reset at 0.5y, pays at 1.0y.
# So there are 59 caplets.
# Caplet i (from 1 to 59):
# resets at T_{i} = i * 0.5 (starts at 0.5y)
# pays at T_{i+1} = (i+1) * 0.5 (starts at 1.0y)
# Strike is K = 2.71% = 0.0271 (ATM strike)
K = 0.0271
delta = 0.5

hjm_cap_price = 0.0
for i in range(1, 60):
    Ti_minus_1 = i * 0.5
    Ti = (i + 1) * 0.5
    P_minus_1 = P_curve[i]  # P(0, Ti_minus_1)
    P_i = P_curve[i + 1]     # P(0, Ti)
    
    variance = get_hjm_integrated_variance(Ti_minus_1, Ti)
    std_dev = np.sqrt(variance)
    
    # Pricing as bond option:
    # Caplet = P(0, Ti_minus_1) * N(-d2) - (1 + delta*K) * P(0, Ti) * N(-d1)
    d1 = (np.log(P_i / P_minus_1 * (1 + delta * K)) + 0.5 * variance) / std_dev
    d2 = d1 - std_dev
    
    caplet_price = P_minus_1 * norm.cdf(-d2) - (1 + delta * K) * P_i * norm.cdf(-d1)
    hjm_cap_price += caplet_price

print(f"Computed HJM Cap Price: {hjm_cap_price:.6f} ({hjm_cap_price * 100:.4f}%)")

# Now define Black Cap Pricing Formula
def black_caplet_price(F, K, df, T_expiry, vol):
    if T_expiry <= 0.0 or vol <= 0.0:
        return max(0.0, (F - K) * delta * df)
    d1 = (np.log(F / K) + 0.5 * vol * vol * T_expiry) / (vol * np.sqrt(T_expiry))
    d2 = d1 - vol * np.sqrt(T_expiry)
    return delta * df * (F * norm.cdf(d1) - K * norm.cdf(d2))

def black_cap_price(vol):
    price = 0.0
    for i in range(1, 60):
        Ti_minus_1 = i * 0.5
        Ti = (i + 1) * 0.5
        P_minus_1 = P_curve[i]
        P_i = P_curve[i + 1]
        
        # Simple Forward Rate
        F = (P_minus_1 / P_i - 1.0) / delta
        
        price += black_caplet_price(F, K, P_i, Ti_minus_1, vol)
    return price

# Solve for Implied Black Volatility
implied_black_vol = brentq(lambda vol: black_cap_price(vol) - hjm_cap_price, 1e-6, 2.0)
print(f"Implied Black Volatility: {implied_black_vol * 100:.6f}%")

# Now define Bachelier (Normal) Cap Pricing Formula
def bachelier_caplet_price(F, K, df, T_expiry, vol_N):
    if T_expiry <= 0.0 or vol_N <= 0.0:
        return max(0.0, (F - K) * delta * df)
    std_dev = vol_N * np.sqrt(T_expiry)
    d1 = (F - K) / std_dev
    return delta * df * ((F - K) * norm.cdf(d1) + std_dev * norm.pdf(d1))

def bachelier_cap_price(vol_N):
    price = 0.0
    for i in range(1, 60):
        Ti_minus_1 = i * 0.5
        Ti = (i + 1) * 0.5
        P_minus_1 = P_curve[i]
        P_i = P_curve[i + 1]
        
        # Simple Forward Rate
        F = (P_minus_1 / P_i - 1.0) / delta
        
        price += bachelier_caplet_price(F, K, P_i, Ti_minus_1, vol_N)
    return price

# Solve for Implied Normal Volatility
implied_normal_vol = brentq(lambda vol_N: bachelier_cap_price(vol_N) - hjm_cap_price, 1e-6, 0.5)
print(f"Implied Normal Volatility: {implied_normal_vol:.6f}")
print(f"Implied Normal Volatility in bps: {implied_normal_vol * 10000:.6f} bps")

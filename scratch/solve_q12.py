import numpy as np
from scipy.stats import norm

# Discount Factors from scratch/test_calib.py
P_discount = [
    0.9983, 0.9956, 0.9916, 0.9876, 0.9810, 0.9745, 0.9653, 0.9562, 0.9450, 0.9338, # 0.5y to 5.0y (k=0 to 9)
    0.9216, 0.9093, 0.8963, 0.8833, 0.8697, 0.8562, 0.8422, 0.8283, 0.8142, 0.8001, # 5.5y to 10.0y (k=10 to 19)
    0.7865, 0.7729, 0.7595, 0.7462, 0.7331, 0.7200, 0.7072, 0.6943, 0.6818, 0.6692, # 10.5y to 15.0y (k=20 to 29)
    0.6591, 0.6489, 0.6390, 0.6291, 0.6193, 0.6096, 0.6001, 0.5905, 0.5812, 0.5719, # 15.5y to 20.0y (k=30 to 39)
    0.5642, 0.5565, 0.5489, 0.5414, 0.5340, 0.5267, 0.5195, 0.5122, 0.5052, 0.4982, # 20.5y to 25.0y (k=40 to 49)
    0.4918, 0.4855, 0.4793, 0.4731, 0.4671, 0.4610, 0.4551, 0.4493, 0.4435, 0.4378  # 25.5y to 30.0y (k=50 to 59)
]

# HJM volatility parameters
v1 = 0.01
v2 = 0.02
beta1 = 0.3
beta2 = 0.5

# We need to compute the 30-year semi-annual ATM cap price.
# First reset date is in 6 months (0.5 years).
# Settlement dates are 1.0, 1.5, ..., 30.0 years.
# So there are 59 caplets.
# Caplet i resets at T_i = (i+1)*0.5, pays at T_{i+1} = (i+2)*0.5.
# For i=0, resets at T_0 = 0.5, pays at T_1 = 1.0.
# For i=58, resets at T_58 = 29.5, pays at T_59 = 30.0.

def get_hjm_integrated_variance(Ti_minus_1, Ti, v1, v2, beta1, beta2):
    delta = Ti - Ti_minus_1
    
    # Factor 1
    if abs(beta1) < 1e-5:
        term1 = v1 * v1 * delta * delta * Ti_minus_1
    else:
        factor = np.exp(-beta1 * Ti_minus_1) - np.exp(-beta1 * Ti)
        integral = (np.exp(2 * beta1 * Ti_minus_1) - 1) / (2 * beta1)
        term1 = (v1 * v1) / (beta1 * beta1) * (factor * factor) * integral
        
    # Factor 2
    if abs(beta2) < 1e-5:
        term2 = v2 * v2 * delta * delta * Ti_minus_1
    else:
        factor = np.exp(-beta2 * Ti_minus_1) - np.exp(-beta2 * Ti)
        integral = (np.exp(2 * beta2 * Ti_minus_1) - 1) / (2 * beta2)
        term2 = (v2 * v2) / (beta2 * beta2) * (factor * factor) * integral
        
    return term1 + term2

def calculate_hjm_model_cap_price(maturity, strike, v1, v2, beta1, beta2):
    num_caplets = maturity * 2 - 1  # For 30 years, 59 caplets.
    cap_price = 0
    for i in range(1, num_caplets + 1):
        # p_discount index:
        # P_discount[0] corresponds to 0.5y.
        # So P(0, T_i) is P_discount[i].
        # For caplet i (from 1 to 59):
        # Ti_minus_1 is i * 0.5
        # Ti is (i + 1) * 0.5
        # P_minus_1 is P(0, Ti_minus_1) = P_discount[i - 1]
        # P_i is P(0, Ti) = P_discount[i]
        
        Ti_minus_1 = i * 0.5
        Ti = (i + 1) * 0.5
        P_minus_1 = P_discount[i - 1]
        P_i = P_discount[i]
        
        variance = get_hjm_integrated_variance(Ti_minus_1, Ti, v1, v2, beta1, beta2)
        std_dev = np.sqrt(variance)
        
        if std_dev < 1e-8:
            payoff = max(0, P_minus_1 - (1 + 0.5 * strike) * P_i)
            cap_price += payoff
            continue
            
        d1 = (np.log(P_i / P_minus_1 * (1 + 0.5 * strike)) + 0.5 * variance) / std_dev
        d2 = d1 - std_dev
        
        caplet_price = P_minus_1 * norm.cdf(-d2) - (1 + 0.5 * strike) * P_i * norm.cdf(-d1)
        cap_price += caplet_price
    return cap_price

# Test K = 2.71%
price_271 = calculate_hjm_model_cap_price(30, 0.0271, v1, v2, beta1, beta2)
print(f"Price for strike 2.71%: {price_271 * 100:.6f}%")

# Test K = 2.75%
price_275 = calculate_hjm_model_cap_price(30, 0.0275, v1, v2, beta1, beta2)
print(f"Price for strike 2.75%: {price_275 * 100:.6f}%")

import numpy as np
from scipy.stats import norm

# Discount Factors P(0, T_k)
P_discount = [
    0.9983, 0.9956, 0.9916, 0.9876, 0.9810, 0.9745, 0.9653, 0.9562, 0.9450, 0.9338, # 0.5y to 5.0y (k=0 to 9)
    0.9216, 0.9093, 0.8963, 0.8833, 0.8697, 0.8562, 0.8422, 0.8283, 0.8142, 0.8001, # 5.5y to 10.0y (k=10 to 19)
    0.7865, 0.7729, 0.7595, 0.7462, 0.7331, 0.7200, 0.7072, 0.6943, 0.6818, 0.6692, # 10.5y to 15.0y (k=20 to 29)
    0.6591, 0.6489, 0.6390, 0.6291, 0.6193, 0.6096, 0.6001, 0.5905, 0.5812, 0.5719, # 15.5y to 20.0y (k=30 to 39)
    0.5642, 0.5565, 0.5489, 0.5414, 0.5340, 0.5267, 0.5195, 0.5122, 0.5052, 0.4982, # 20.5y to 25.0y (k=40 to 49)
    0.4918, 0.4855, 0.4793, 0.4731, 0.4671, 0.4610, 0.4551, 0.4493, 0.4435, 0.4378  # 25.5y to 30.0y (k=50 to 59)
]

# Cap Quotes
market_cap_quotes = [
    {"maturity": 1,  "price": 0.0012, "blackIV": 1.7052, "normalIV": 0.008681, "strike": 0.0054},
    {"maturity": 2,  "price": 0.0046, "blackIV": 1.1362, "normalIV": 0.007658, "strike": 0.0072},
    {"maturity": 3,  "price": 0.0092, "blackIV": 0.7652, "normalIV": 0.007092, "strike": 0.0097},
    {"maturity": 4,  "price": 0.0148, "blackIV": 0.5454, "normalIV": 0.006717, "strike": 0.0123},
    {"maturity": 5,  "price": 0.0210, "blackIV": 0.4136, "normalIV": 0.006386, "strike": 0.0148},
    {"maturity": 6,  "price": 0.0278, "blackIV": 0.3458, "normalIV": 0.006210, "strike": 0.0168},
    {"maturity": 7,  "price": 0.0349, "blackIV": 0.3046, "normalIV": 0.006079, "strike": 0.0186},
    {"maturity": 8,  "price": 0.0417, "blackIV": 0.2710, "normalIV": 0.005867, "strike": 0.0202},
    {"maturity": 9,  "price": 0.0490, "blackIV": 0.2502, "normalIV": 0.005749, "strike": 0.0216},
    {"maturity": 10, "price": 0.0565, "blackIV": 0.2367, "normalIV": 0.005686, "strike": 0.0228},
    {"maturity": 15, "price": 0.0904, "blackIV": 0.1987, "normalIV": 0.005346, "strike": 0.0267},
    {"maturity": 20, "price": 0.1196, "blackIV": 0.1938, "normalIV": 0.005480, "strike": 0.0277},
    {"maturity": 30, "price": 0.1686, "blackIV": 0.1931, "normalIV": 0.005679, "strike": 0.0275}
]

def calib_phi(x):
    return norm.pdf(x)

def calib_Phi(x):
    return norm.cdf(x)

def get_calibration_cap_rates(maturity):
    num_caplets = maturity * 2 - 1
    rates = []
    for i in range(1, num_caplets + 1):
        P_prev = P_discount[i - 1]
        P_curr = P_discount[i]
        fwd = (P_prev / P_curr - 1) / 0.5
        rates.append({
            "index": i,
            "T_minus_1": i * 0.5,
            "T_i": (i + 1) * 0.5,
            "P_minus_1": P_prev,
            "P_i": P_curr,
            "forwardRate": fwd
        })
    return rates

def calculate_black_cap_vega(maturity, strike, blackIV):
    periods = get_calibration_cap_rates(maturity)
    cap_vega = 0
    for p in periods:
        Ti_minus_1 = p["T_minus_1"]
        P_i = p["P_i"]
        F_i = p["forwardRate"]
        num = np.log(F_i / strike) + 0.5 * blackIV * blackIV * Ti_minus_1
        den = blackIV * np.sqrt(Ti_minus_1)
        d1 = num / den
        caplet_vega = 0.5 * P_i * F_i * np.sqrt(Ti_minus_1) * calib_phi(d1)
        cap_vega += caplet_vega
    return cap_vega

def calculate_bachelier_cap_vega(maturity, strike, normalIV):
    periods = get_calibration_cap_rates(maturity)
    cap_vega = 0
    for p in periods:
        Ti_minus_1 = p["T_minus_1"]
        P_i = p["P_i"]
        F_i = p["forwardRate"]
        D_i = (F_i - strike) / (normalIV * np.sqrt(Ti_minus_1))
        caplet_vega = 0.5 * P_i * np.sqrt(Ti_minus_1) * calib_phi(D_i)
        cap_vega += caplet_vega
    return cap_vega

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
    periods = get_calibration_cap_rates(maturity)
    cap_price = 0
    for p in periods:
        Ti_minus_1 = p["T_minus_1"]
        Ti = p["T_i"]
        P_minus_1 = p["P_minus_1"]
        P_i = p["P_i"]
        
        variance = get_hjm_integrated_variance(Ti_minus_1, Ti, v1, v2, beta1, beta2)
        std_dev = np.sqrt(variance)
        
        if std_dev < 1e-8:
            payoff = max(0, P_minus_1 - (1 + 0.5 * strike) * P_i)
            cap_price += payoff
            continue
            
        d1 = (np.log(P_i / P_minus_1 * (1 + 0.5 * strike)) + 0.5 * variance) / std_dev
        d2 = d1 - std_dev
        
        caplet_price = P_minus_1 * calib_Phi(-d2) - (1 + 0.5 * strike) * P_i * calib_Phi(-d1)
        cap_price += caplet_price
    return cap_price

# Optimal parameters
v1, v2, beta1, beta2 = 0.0149, 0.0056, 1.7381, 0.0127

print("NORMAL IV VOL ERRORS (WMSE):")
total_WSE_N = 0
for q in market_cap_quotes:
    model_price = calculate_hjm_model_cap_price(q["maturity"], q["strike"], v1, v2, beta1, beta2)
    vega_val = calculate_bachelier_cap_vega(q["maturity"], q["strike"], q["normalIV"])
    squared_error = ((model_price - q["price"]) / vega_val) ** 2
    total_WSE_N += squared_error
    print(f"Maturity: {q['maturity']}Y | Market Price: {q['price']:.4f} | Model Price: {model_price:.4f} | Vega: {vega_val:.4f} | Squared Err: {squared_error:.2e}")
print(f"Total Normal WMSE: {total_WSE_N:.6e}")
print("-" * 50)

print("BLACK IV VOL ERRORS (WMSE):")
total_WSE_B = 0
for q in market_cap_quotes:
    model_price = calculate_hjm_model_cap_price(q["maturity"], q["strike"], v1, v2, beta1, beta2)
    vega_val = calculate_black_cap_vega(q["maturity"], q["strike"], q["blackIV"])
    squared_error = ((model_price - q["price"]) / vega_val) ** 2
    total_WSE_B += squared_error
    print(f"Maturity: {q['maturity']}Y | Market Price: {q['price']:.4f} | Model Price: {model_price:.4f} | Vega: {vega_val:.4f} | Squared Err: {squared_error:.2e}")
print(f"Total Black WMSE: {total_WSE_B:.6e}")

import numpy as np
from scipy.optimize import minimize
from scipy.stats import norm

# Forward rates F(0, T, T+0.5)
F_rates = [0.06, 0.08, 0.09, 0.10, 0.10, 0.10, 0.09, 0.09]
delta = 0.5

# Reconstruct discount factors P(0, T_k)
# T_k = k * 0.5, for k = 0, 1, 2, ..., 8
P = [1.0]
for f in F_rates:
    P.append(P[-1] / (1 + delta * f))

print("Discount Factors:", [round(x, 6) for x in P])

# ATM Cap strike rates (par swap rates) for each maturity
# A cap of maturity M (years) pays at 1.0, 1.5, ..., M
# For a given maturity M, the ATM strike rate K_M is the par swap rate:
# K_M = (P(0, 0.5) - P(0, M)) / sum_{i=2}^{2M} (delta * P(0, i * 0.5))
# Wait, let's see. A cap pays at T_i for i = 1, ..., N, resetting at T_{i-1}.
# The first reset date is in 6 months, which is T_0 = 0.5.
# So the first payment is at T_1 = 1.0.
# The settlement dates are T_1 = 1.0, T_2 = 1.5, ..., T_n.
# So the swap rate K_M is:
# K_M = (P(0, 0.5) - P(0, M)) / sum_{i=2}^{2M} (delta * P(0, i * 0.5))
# Wait, does the first payment of the cap occur at 1.0?
# Yes, "first reset date in 6 months" means T_0 = 0.5 (reset), T_1 = 1.0 (payment).
# Let's calculate the ATM strike rates for maturities 1, 2, 3, 4.

def get_atm_strike(M_years):
    # Maturity in years
    # Settlement dates: T_1 = 1.0, T_2 = 1.5, ..., T_n = M_years.
    # So index of payment dates in P:
    # 0.5y is P[1], 1.0y is P[2], 1.5y is P[3], ..., M_years is P[2 * M_years]
    # The annuity factor A = sum_{i=2}^{2*M_years} 0.5 * P[i]
    # The par swap rate = (P[1] - P[2*M_years]) / A
    # Let's verify this.
    num = P[1] - P[2 * M_years]
    den = sum(0.5 * P[i] for i in range(2, 2 * M_years + 1))
    return num / den

strikes = {M: get_atm_strike(M) for M in [1, 2, 3, 4]}
print("ATM Strikes:", {k: round(v, 6) for k, v in strikes.items()})

# Cap Market prices
market_prices = {
    1: 0.0020,
    2: 0.0080,
    3: 0.0120,
    4: 0.0160
}

# Black vegas: to weight the least squares.
# Wait, the problem says "Calibrate the volatility parameters beta and v to the cap prices weighted by their corresponding Black vegas (weighted least squares)."
# Wait, does it mean we should weight by 1/vega or vega?
# "weighted by their corresponding Black vegas (weighted least squares)"
# Wait, in the lecture, the vega-weighted least squares is:
# sum ( (C_model - C_market) / vega_market )^2
# Yes! The weight is 1/vega, so the error term is (C_model - C_market) / vega.
# Let's double check if we need to compute Black vegas.
# To compute Black vega of the market caps, we first need their Black implied volatilities!
# Let's find the Black implied volatility for each market cap.
# The Black price of a caplet is:
# Cpl_i = delta * P(0, T_i) * (F_i * N(d1) - K * N(d2))
# and the cap price is the sum of caplets.
# Let's write a function to calculate Black cap price for a given volatility sigma.

def black_caplet_price(P_prev, P_curr, F, K, T_minus_1, sigma):
    if sigma <= 0:
        return max(0.0, F - K) * delta * P_curr
    d1 = (np.log(F / K) + 0.5 * sigma * sigma * T_minus_1) / (sigma * np.sqrt(T_minus_1))
    d2 = d1 - sigma * np.sqrt(T_minus_1)
    return delta * P_curr * (F * norm.cdf(d1) - K * norm.cdf(d2))

def black_cap_price(M_years, K, sigma):
    price = 0
    # caplets: resetting at T_{i-1} = i*0.5, paying at T_i = (i+1)*0.5 for i = 1 to 2*M_years - 1
    # T_0 = 0.5 (reset), T_1 = 1.0 (pay) -> i = 1
    # T_{n-1} = M - 0.5 (reset), T_n = M (pay) -> i = 2*M - 1
    for i in range(1, 2 * M_years):
        T_minus_1 = i * 0.5
        P_prev = P[i]
        P_curr = P[i+1]
        F = F_rates[i]
        price += black_caplet_price(P_prev, P_curr, F, K, T_minus_1, sigma)
    return price

# Find implied vols
def find_implied_vol(M_years, K, market_price):
    objective = lambda sig: (black_cap_price(M_years, K, sig) - market_price)**2
    res = minimize(objective, 0.2, bounds=[(0.0001, 5.0)])
    return res.x[0]

implied_vols = {M: find_implied_vol(M, strikes[M], market_prices[M]) for M in [1, 2, 3, 4]}
print("Implied Vols:", {k: round(v, 6) for k, v in implied_vols.items()})

# Black vegas of the market caps
def black_caplet_vega(P_curr, F, K, T_minus_1, sigma):
    d1 = (np.log(F / K) + 0.5 * sigma * sigma * T_minus_1) / (sigma * np.sqrt(T_minus_1))
    return delta * P_curr * F * np.sqrt(T_minus_1) * norm.pdf(d1)

def black_cap_vega(M_years, K, sigma):
    vega = 0
    for i in range(1, 2 * M_years):
        T_minus_1 = i * 0.5
        P_curr = P[i+1]
        F = F_rates[i]
        vega += black_caplet_vega(P_curr, F, K, T_minus_1, sigma)
    return vega

vegas = {M: black_cap_vega(M, strikes[M], implied_vols[M]) for M in [1, 2, 3, 4]}
print("Black Vegas:", {k: round(v, 6) for k, v in vegas.items()})

# Now 1-factor Gaussian HJM model volatility:
# sigma(t, T) = exp(-beta * (T-t)) * v
# The integrated variance for the i-th caplet resetting at T_{i-1} and paying at T_i:
# sigma_i^2 = \int_0^{T_{i-1}} (v(s, T_{i-1}) - v(s, T_i))^2 ds
# where v(s, T) = \int_s^T \sigma(s, u) du
# Wait, let's verify if v(s, T) is the volatility of the discount bond or the volatility of the forward rate.
# In a Gaussian HJM model:
# The volatility of the discount bond P(t, T) is:
# \sigma_P(t, T) = - \int_t^T \sigma_f(t, u) du
# In our HJM model, the forward rate volatility is \sigma_f(t, T) = e^{-\beta(T-t)} v.
# So:
# v_P(t, T) = - \int_t^T e^{-\beta(u-t)} v du = - \frac{v}{\beta} (1 - e^{-\beta(T-t)})
# Then the integrated variance of the ratio P(t, T_i) / P(t, T_{i-1}) is:
# \sigma_i^2 = \int_0^{T_{i-1}} \| \sigma_P(s, T_{i-1}) - \sigma_P(s, T_i) \|^2 ds
# = \int_0^{T_{i-1}} \left( \frac{v}{\beta} (1 - e^{-\beta(T_{i-1}-s)}) - \frac{v}{\beta} (1 - e^{-\beta(T_i-s)}) \right)^2 ds
# = \int_0^{T_{i-1}} \left( \frac{v}{\beta} e^{-\beta T_{i-1}} e^{\beta s} (1 - e^{-\beta (T_i - T_{i-1})}) \right)^2 ds
# Let delta = T_i - T_{i-1} = 0.5.
# = \frac{v^2}{\beta^2} (e^{-\beta T_{i-1}} - e^{-\beta T_i})^2 \int_0^{T_{i-1}} e^{2\beta s} ds
# = \frac{v^2}{\beta^2} (e^{-\beta T_{i-1}} - e^{-\beta T_i})^2 \frac{e^{2\beta T_{i-1}} - 1}{2\beta}
# This is exactly the HJM integrated variance formula! Let's write a function for this.

def hjm_integrated_variance(T_minus_1, T_i, v, beta):
    if abs(beta) < 1e-6:
        # Limit as beta -> 0:
        # (e^{-\beta T_{i-1}} - e^{-\beta T_i}) / beta -> T_i - T_{i-1} = delta
        # (e^{2\beta T_{i-1}} - 1) / (2\beta) -> T_{i-1}
        # So the whole term becomes: v^2 * delta^2 * T_{i-1}
        return v * v * delta * delta * T_minus_1
    
    factor = np.exp(-beta * T_minus_1) - np.exp(-beta * T_i)
    integral = (np.exp(2 * beta * T_minus_1) - 1) / (2 * beta)
    return (v * v) / (beta * beta) * (factor * factor) * integral

def hjm_caplet_price(P_prev, P_curr, K, T_minus_1, T_i, v, beta):
    var = hjm_integrated_variance(T_minus_1, T_i, v, beta)
    std_dev = np.sqrt(var)
    if std_dev < 1e-8:
        return max(0.0, P_prev - (1 + delta * K) * P_curr)
    
    d1 = (np.log(P_curr / P_prev * (1 + delta * K)) + 0.5 * var) / std_dev
    d2 = d1 - std_dev
    return P_prev * norm.cdf(-d2) - (1 + delta * K) * P_curr * norm.cdf(-d1)

def hjm_cap_price(M_years, K, v, beta):
    price = 0
    for i in range(1, 2 * M_years):
        T_minus_1 = i * 0.5
        T_i = (i + 1) * 0.5
        P_prev = P[i]
        P_curr = P[i+1]
        price += hjm_caplet_price(P_prev, P_curr, K, T_minus_1, T_i, v, beta)
    return price

# Now let's perform vega-weighted least squares calibration:
# Minimize sum_{M=1}^4 [ (HJM_Cap(M, K_M, v, beta) - Market_Cap(M)) / vega_M ]^2

def objective_function(x):
    v_val, beta_val = x[0], x[1]
    error = 0
    for M in [1, 2, 3, 4]:
        model_p = hjm_cap_price(M, strikes[M], v_val, beta_val)
        market_p = market_prices[M]
        vega = vegas[M]
        error += ((model_p - market_p) / vega) ** 2
    return error

# Let's perform optimization
res = minimize(objective_function, [0.01, 1.0], bounds=[(0.0001, 1.0), (0.0001, 10.0)])
print("Optimization result:", res)
v_opt, beta_opt = res.x[0], res.x[1]
print(f"Calibrated v: {v_opt:.6f} -> rounded: {v_opt:.2f}")
print(f"Calibrated beta: {beta_opt:.6f} -> rounded: {beta_opt:.2f}")

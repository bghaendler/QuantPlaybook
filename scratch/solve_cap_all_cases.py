import numpy as np
from scipy.stats import norm
from scipy.optimize import minimize_scalar

N_periods = 60
dt = 0.5
T = np.arange(1, N_periods + 1) * dt

swap_quotes = {
    1: 0.36 / 100,
    2: 0.52 / 100,
    3: 0.93 / 100,
    4: 1.21 / 100,
    5: 1.46 / 100,
    6: 1.66 / 100,
    7: 1.84 / 100,
    8: 1.99 / 100,
    9: 2.13 / 100,
    10: 2.21 / 100,
    15: 2.63 / 100,
    20: 2.73 / 100,
    30: 2.71 / 100
}

maturities = sorted(swap_quotes.keys())
N_eqs = len(maturities)
A = np.zeros((N_eqs, N_periods))
b = np.ones(N_eqs)

for idx, U in enumerate(maturities):
    S = swap_quotes[U]
    num_payments = int(2 * U)
    A[idx, :num_payments] = S * dt
    A[idx, num_payments - 1] += 1.0

C = np.tril(np.ones((N_periods, N_periods)))
W = np.diag(np.ones(N_periods) * np.sqrt(dt))

M = A @ C @ W
b_rhs = b - A @ np.ones(N_periods)

y_pseudo = np.linalg.pinv(M) @ b_rhs
p_pseudo = np.ones(N_periods) + C @ W @ y_pseudo

P_30 = p_pseudo[59]
annuity_30 = dt * np.sum(p_pseudo)
strike = (1.0 - P_30) / annuity_30
print(f"ATM strike: {strike*100:.6f}%")

v1, v2 = 0.01, 0.02
beta1, beta2 = 0.3, 0.5

def get_integrated_var(T_d, T_p):
    if T_d == 0:
        return 0.0
    var1 = (v1**2 / beta1**2) * (np.exp(-beta1 * T_d) - np.exp(-beta1 * T_p))**2 * (np.exp(2 * beta1 * T_d) - 1.0) / (2 * beta1)
    var2 = (v2**2 / beta2**2) * (np.exp(-beta2 * T_d) - np.exp(-beta2 * T_p))**2 * (np.exp(2 * beta2 * T_d) - 1.0) / (2 * beta2)
    return var1 + var2

# --- CASE 1: 59 caplets (excluding first) ---
print("\n--- CASE 1: 59 Caplets (Excluding First) ---")
cap_price_59 = 0.0
for i in range(1, 60):
    T_d = i * dt
    T_p = (i + 1) * dt
    sig2 = get_integrated_var(T_d, T_p)
    sig = np.sqrt(sig2)
    P_d = p_pseudo[i - 1]
    P_p = p_pseudo[i]
    d1 = (np.log(P_p / P_d * (1.0 + dt * strike)) + 0.5 * sig2) / sig
    d2 = d1 - sig
    cpl = P_d * norm.cdf(-d2) - (1.0 + dt * strike) * P_p * norm.cdf(-d1)
    cap_price_59 += cpl

print(f"Price: {cap_price_59 * 100:.6f}%")

def black_price_59(sig_B):
    price = 0.0
    for i in range(1, 60):
        T_d = i * dt
        T_p = (i + 1) * dt
        P_d = p_pseudo[i - 1]
        P_p = p_pseudo[i]
        F = (P_d / P_p - 1.0) / dt
        if sig_B <= 0:
            cpl = max(0.0, dt * P_p * (F - strike))
        else:
            d1 = (np.log(F / strike) + 0.5 * sig_B**2 * T_d) / (sig_B * np.sqrt(T_d))
            d2 = d1 - sig_B * np.sqrt(T_d)
            cpl = dt * P_p * (F * norm.cdf(d1) - strike * norm.cdf(d2))
        price += cpl
    return price

res_b59 = minimize_scalar(lambda s: (black_price_59(s) - cap_price_59)**2, bounds=(0.01, 2.0), method='bounded')
print(f"Black Vol: {res_b59.x * 100:.6f}%")

def bach_price_59(sig_N):
    price = 0.0
    for i in range(1, 60):
        T_d = i * dt
        T_p = (i + 1) * dt
        P_d = p_pseudo[i - 1]
        P_p = p_pseudo[i]
        F = (P_d / P_p - 1.0) / dt
        if sig_N <= 0:
            cpl = max(0.0, dt * P_p * (F - strike))
        else:
            d1 = (F - strike) / (sig_N * np.sqrt(T_d))
            cpl = dt * P_p * ((F - strike) * norm.cdf(d1) + sig_N * np.sqrt(T_d) * norm.pdf(d1))
        price += cpl
    return price

res_n59 = minimize_scalar(lambda s: (bach_price_59(s) - cap_price_59)**2, bounds=(0.0001, 0.1), method='bounded')
print(f"Normal Vol: {res_n59.x * 10000:.6f} bps")


# --- CASE 2: 60 caplets (including first) ---
print("\n--- CASE 2: 60 Caplets (Including First) ---")
cap_price_60 = 0.0
# The first caplet resets at T_d = 0.0, pays at T_p = 0.5. Its value under HJM is 0 since at t=0 there is no volatility (sig2 = 0)
# and its payoff is deterministic: max(0, F(0, 0, 0.5) - K) * dt
# F(0, 0, 0.5) = (1.0 / P(0, 0.5) - 1.0) / 0.5
# Let's see:
F_0 = (1.0 / p_pseudo[0] - 1.0) / dt
cpl0 = dt * p_pseudo[0] * max(0.0, F_0 - strike)
cap_price_60 = cpl0

for i in range(1, 60):
    T_d = i * dt
    T_p = (i + 1) * dt
    sig2 = get_integrated_var(T_d, T_p)
    sig = np.sqrt(sig2)
    P_d = p_pseudo[i - 1]
    P_p = p_pseudo[i]
    d1 = (np.log(P_p / P_d * (1.0 + dt * strike)) + 0.5 * sig2) / sig
    d2 = d1 - sig
    cpl = P_d * norm.cdf(-d2) - (1.0 + dt * strike) * P_p * norm.cdf(-d1)
    cap_price_60 += cpl

print(f"Price: {cap_price_60 * 100:.6f}%")

def black_price_60(sig_B):
    # first caplet resets at T_d = 0, so sig_B = 0 payoff is deterministic
    F_0 = (1.0 / p_pseudo[0] - 1.0) / dt
    price = dt * p_pseudo[0] * max(0.0, F_0 - strike)
    for i in range(1, 60):
        T_d = i * dt
        T_p = (i + 1) * dt
        P_d = p_pseudo[i - 1]
        P_p = p_pseudo[i]
        F = (P_d / P_p - 1.0) / dt
        if sig_B <= 0:
            cpl = max(0.0, dt * P_p * (F - strike))
        else:
            d1 = (np.log(F / strike) + 0.5 * sig_B**2 * T_d) / (sig_B * np.sqrt(T_d))
            d2 = d1 - sig_B * np.sqrt(T_d)
            cpl = dt * P_p * (F * norm.cdf(d1) - strike * norm.cdf(d2))
        price += cpl
    return price

res_b60 = minimize_scalar(lambda s: (black_price_60(s) - cap_price_60)**2, bounds=(0.01, 2.0), method='bounded')
print(f"Black Vol: {res_b60.x * 100:.6f}%")

def bach_price_60(sig_N):
    F_0 = (1.0 / p_pseudo[0] - 1.0) / dt
    price = dt * p_pseudo[0] * max(0.0, F_0 - strike)
    for i in range(1, 60):
        T_d = i * dt
        T_p = (i + 1) * dt
        P_d = p_pseudo[i - 1]
        P_p = p_pseudo[i]
        F = (P_d / P_p - 1.0) / dt
        if sig_N <= 0:
            cpl = max(0.0, dt * P_p * (F - strike))
        else:
            d1 = (F - strike) / (sig_N * np.sqrt(T_d))
            cpl = dt * P_p * ((F - strike) * norm.cdf(d1) + sig_N * np.sqrt(T_d) * norm.pdf(d1))
        price += cpl
    return price

res_n60 = minimize_scalar(lambda s: (bach_price_60(s) - cap_price_60)**2, bounds=(0.0001, 0.1), method='bounded')
print(f"Normal Vol: {res_n60.x * 10000:.6f} bps")

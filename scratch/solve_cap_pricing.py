import numpy as np
from scipy.stats import norm
from scipy.optimize import minimize_scalar

# 1. Setup the grid
# Semi-annual cash flows for 30 years -> 60 periods
N_periods = 60
dt = 0.5
T = np.arange(1, N_periods + 1) * dt

# Observed swap rates (spot starting, semi-annual fixed leg)
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

# 2. Build the linear system A * p = b for discount factors p
# p = [P(0, T_1), P(0, T_2), ..., P(0, T_60)]
# Equation for swap rate S with maturity U:
# S * dt * sum_{j=1}^{2U} P(0, T_j) + P(0, T_{2U}) = 1.0
maturities = sorted(swap_quotes.keys())
N_eqs = len(maturities)
A = np.zeros((N_eqs, N_periods))
b = np.ones(N_eqs)

for idx, U in enumerate(maturities):
    S = swap_quotes[U]
    num_payments = int(2 * U)
    A[idx, :num_payments] = S * dt
    A[idx, num_payments - 1] += 1.0

# 3. Pseudo-inverse formulation to minimize the first derivative
# P(0, T_j) = 1.0 + sum_{i=1}^j y_i * sqrt(dt)
# p = 1 + C * W * y
# M * y = b - A * 1, where M = A * C * W
C = np.tril(np.ones((N_periods, N_periods)))
W = np.diag(np.ones(N_periods) * np.sqrt(dt))

M = A @ C @ W
b_rhs = b - A @ np.ones(N_periods)

# Minimum norm solution for y
y_pseudo = np.linalg.pinv(M) @ b_rhs
p_pseudo = np.ones(N_periods) + C @ W @ y_pseudo

print("Discount Factors:")
for i in range(10):
    print(f"  T={T[i]:.1f}: {p_pseudo[i]:.6f}")
print("...")
for i in range(50, 60):
    print(f"  T={T[i]:.1f}: {p_pseudo[i]:.6f}")

# 4. Caplet Pricing under 2-factor Gaussian HJM model
# Volatility: sigma(t, T) = ( e^-beta_1(T-t) * v_1, e^-beta_2(T-t) * v_2 )
v1, v2 = 0.01, 0.02
beta1, beta2 = 0.3, 0.5

# For each caplet i = 1 to 59 (the 30-year cap has 59 caplets since first is at 0.5Y, expires in 30Y)
# The first caplet resets at T_0 = 0.5 and pays at T_1 = 1.0. Wait, first reset is in 6 months, so T_0 = 0.5, paying at T_1 = 1.0.
# Wait, a 30-year semi-annual cap with first reset in 6 months has resets at 0.5, 1.0, ..., 29.5, and payments at 1.0, 1.5, ..., 30.0.
# So there are 59 caplets: i = 1 to 59, where the i-th caplet resets at T_{i} = i * dt, and pays at T_{i+1} = (i+1) * dt.
# Wait, let's look at the index carefully:
# i = 1 (reset at T_1 = 0.5, payment at T_2 = 1.0)
# ...
# i = 59 (reset at T_59 = 29.5, payment at T_60 = 30.0)

# Let's compute integrated variance sigma_p_i^2 for each caplet i:
# The caplet resets at T_d = T_i = i * dt, and pays at T_p = T_{i+1} = (i+1) * dt.
# The integrated variance is:
# sigma_p_i^2 = Var_1(i) + Var_2(i)
# Var_k = (v_k^2 / beta_k^2) * ( e^-beta_k*T_d - e^-beta_k*T_p )^2 * ( e^(2*beta_k*T_d) - 1 ) / (2 * beta_k)
# Note that ( e^-beta_k*T_d - e^-beta_k*T_p ) = e^-beta_k*T_d * (1 - e^-beta_k*dt)
# So Var_k = (v_k^2 / beta_k^2) * (1 - e^-beta_k*dt)^2 * ( 1 - e^(-2*beta_k*T_d) ) / (2 * beta_k)

def get_integrated_var(T_d, T_p):
    var1 = (v1**2 / beta1**2) * (np.exp(-beta1 * T_d) - np.exp(-beta1 * T_p))**2 * (np.exp(2 * beta1 * T_d) - 1.0) / (2 * beta1)
    var2 = (v2**2 / beta2**2) * (np.exp(-beta2 * T_d) - np.exp(-beta2 * T_p))**2 * (np.exp(2 * beta2 * T_d) - 1.0) / (2 * beta2)
    return var1 + var2

# ATM strike is the par swap rate for the 30-year swap:
# S_30 = (P(0, T_0) - P(0, T_N)) / (dt * sum P(0, T_j))
# Since it is spot starting, P(0, T_0) = 1.0
P_30 = p_pseudo[59]
annuity_30 = dt * np.sum(p_pseudo)
strike = (1.0 - P_30) / annuity_30
print(f"Strike K (ATM): {strike * 100:.6f}%")

# Now price the caplets
cap_price = 0.0
caplet_prices = []
for i in range(1, 60):
    T_d = i * dt
    T_p = (i + 1) * dt
    sig2 = get_integrated_var(T_d, T_p)
    sig = np.sqrt(sig2)
    
    P_d = p_pseudo[i - 1] # P(0, T_d)
    P_p = p_pseudo[i]     # P(0, T_p)
    
    d1 = (np.log(P_p / P_d * (1.0 + dt * strike)) + 0.5 * sig2) / sig
    d2 = d1 - sig
    
    # Caplet value is equivalent to (1 + dt*K) put options on P(., T_p) expiring at T_d:
    # Price = P_d * Phi(-d2) - (1 + dt*strike) * P_p * Phi(-d1)
    cpl = P_d * norm.cdf(-d2) - (1.0 + dt * strike) * P_p * norm.cdf(-d1)
    cap_price += cpl
    caplet_prices.append(cpl)

print(f"Cap Price: {cap_price * 100:.6f}%")

# 5. Implied Black Volatility
# Black's formula for semi-annual caplet:
# Cpl_Black = dt * P(0, T_p) * [ F * Phi(d1) - K * Phi(d2) ]
# where F = (P(0, T_d) / P(0, T_p) - 1) / dt
# d1 = (ln(F/K) + 0.5 * sigma_B^2 * T_d) / (sigma_B * sqrt(T_d))
# d2 = d1 - sigma_B * sqrt(T_d)

def black_cap_price(sig_B):
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

res_black = minimize_scalar(lambda s: (black_cap_price(s) - cap_price)**2, bounds=(0.01, 2.0), method='bounded')
print(f"Implied Black Vol: {res_black.x * 100:.6f}%")

# 6. Implied Normal (Bachelier) Volatility
# Bachelier formula for semi-annual caplet:
# Cpl_Bach = dt * P(0, T_p) * [ (F - K) * Phi(d1) + sig_N * sqrt(T_d) * phi(d1) ]
# where d1 = (F - K) / (sig_N * sqrt(T_d))
# Note: Expressed in bps, sig_N is absolute volatility.

def bachelier_cap_price(sig_N):
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

res_normal = minimize_scalar(lambda s: (bachelier_cap_price(s) - cap_price)**2, bounds=(0.0001, 0.1), method='bounded')
print(f"Implied Normal Vol: {res_normal.x * 10000:.6f} bps")

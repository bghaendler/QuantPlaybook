import math

# Forward rates and discount factors
F = [0.06, 0.08, 0.09, 0.10, 0.10, 0.10, 0.09, 0.09]
delta = 0.25

P = [1.0]
for i in range(8):
    P.append(P[-1] / (1 + delta * F[i]))

# Swaption details: 1 x 1 swaption (expiry T_0 = 1, swap matures at T_n = 2)
# Payment times of underlying swap: 1.25, 1.50, 1.75, 2.00. (indices 5, 6, 7, 8)
# Reset times: 1.0, 1.25, 1.50, 1.75. (indices 4, 5, 6, 7)
P_expiry = P[4]  # P(0, 1.0)
P_swap_pay = P[5:9] # P(0, 1.25) to P(0, 2.00)

# Par swap rate (strike K since it is ATM):
A_0 = sum(delta * p for p in P_swap_pay)
K = (P_expiry - P[8]) / A_0
print(f"ATM Strike K = {K*100:.6f}%")
print(f"Annuity factor A(0) = {A_0}")

# Swaption Black pricing formula
def swaption_black(sig, K, T0, A):
    d1 = (math.log(S0 / K) + 0.5 * sig**2 * T0) / (sig * math.sqrt(T0))
    d2 = d1 - sig * math.sqrt(T0)
    cdf = lambda x: 0.5 * (1 + math.erf(x / math.sqrt(2)))
    return A * (S0 * cdf(d1) - K * cdf(d2))

# Since it is ATM, S0 = K
S0 = K

def swaption_black_atm(sig, T0, A):
    d1 = 0.5 * sig * math.sqrt(T0)
    d2 = -0.5 * sig * math.sqrt(T0)
    cdf = lambda x: 0.5 * (1 + math.erf(x / math.sqrt(2)))
    return A * S0 * (cdf(d1) - cdf(d2))

# Swaption Normal pricing formula
def swaption_normal_atm(sig_N, T0, A):
    pdf = lambda x: math.exp(-0.5 * x**2) / math.sqrt(2 * math.pi)
    return A * sig_N * math.sqrt(T0) * pdf(0.0)

# Implied Black Vol for 1% (0.01) price
low, high = 0.0001, 2.0
for _ in range(50):
    mid = 0.5 * (low + high)
    p = swaption_black_atm(mid, 1.0, A_0)
    if p < 0.01:
        low = mid
    else:
        high = mid
black_vol = low
print(f"Implied Black Volatility: {black_vol*100:.4f}%")

# Implied Normal Vol for 1% (0.01) price
low, high = 0.0001, 0.2
for _ in range(50):
    mid = 0.5 * (low + high)
    p = swaption_normal_atm(mid, 1.0, A_0)
    if p < 0.01:
        low = mid
    else:
        high = mid
normal_vol = low
print(f"Implied Normal Volatility: {normal_vol*10000:.4f} bps")

# Price for 50% Black Vol
p_50 = swaption_black_atm(0.50, 1.0, A_0)
print(f"Price for 50% Black Vol: {p_50*100:.4f}%")

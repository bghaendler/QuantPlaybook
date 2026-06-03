import math

# Simple forward rates
F = [0.06, 0.08, 0.09, 0.10, 0.10, 0.10, 0.09, 0.09]
delta = 0.25

# Compute discount factors
P = [1.0]
for i in range(8):
    P.append(P[-1] / (1 + delta * F[i]))

print("Discount factors P(0, T_i):", [round(p, 6) for p in P])

# We have two interpretations for the ATM Cap:
# Interpretation A: Includes first period (resets at T_0 = 0, settles at T_1 = 0.25).
# Swap is from T_0 to T_8. Par swap rate:
kappa_A = (P[0] - P[8]) / (delta * sum(P[1:9]))
print("Interpretation A - Swap rate (ATM strike):", round(kappa_A * 100, 4), "%")

# Interpretation B: Standard market practice where the first caplet (reset at T_0 = 0) is excluded.
# So the caplets are for i=2,...,8 (resets at T_1,...,T_7, settles at T_2,...,T_8).
# The underlying swap is forward-starting from T_1 to T_8. Par swap rate:
kappa_B = (P[1] - P[8]) / (delta * sum(P[2:9]))
print("Interpretation B - Forward swap rate (ATM strike):", round(kappa_B * 100, 4), "%")

# Let's write functions to price the caplets under Black and Normal models.
def black_caplet(F, K, sig, T, P_pay):
    if T == 0:
        return max(F - K, 0.0) * delta * P_pay
    d1 = (math.log(F / K) + 0.5 * sig**2 * T) / (sig * math.sqrt(T))
    d2 = d1 - sig * math.sqrt(T)
    cdf = lambda x: 0.5 * (1 + math.erf(x / math.sqrt(2)))
    return delta * P_pay * (F * cdf(d1) - K * cdf(d2))

def normal_caplet(F, K, sig, T, P_pay):
    if T == 0:
        return max(F - K, 0.0) * delta * P_pay
    d = (F - K) / (sig * math.sqrt(T))
    cdf = lambda x: 0.5 * (1 + math.erf(x / math.sqrt(2)))
    pdf = lambda x: math.exp(-0.5 * x**2) / math.sqrt(2 * math.pi)
    return delta * P_pay * ((F - K) * cdf(d) + sig * math.sqrt(T) * pdf(d))

def price_cap_black(sig, K, exclude_first=False):
    total = 0.0
    start = 1 if exclude_first else 0
    for i in range(start, 8):
        # Reset date T_i, settlement date T_{i+1}
        # T_i is i*delta
        total += black_caplet(F[i], K, sig, i * delta, P[i+1])
    return total

def price_cap_normal(sig, K, exclude_first=False):
    total = 0.0
    start = 1 if exclude_first else 0
    for i in range(start, 8):
        total += normal_caplet(F[i], K, sig, i * delta, P[i+1])
    return total

# Let's find implied volatilities for a target cap price of 1% (0.01)
# under both interpretations.
for label, K, exclude_first in [("A (include first)", kappa_A, False), ("B (exclude first)", kappa_B, True)]:
    print(f"\n--- Pricing under Interpretation {label} (K = {K*100:.4f}%) ---")
    # Implied Black Vol
    low, high = 0.0001, 2.0
    for _ in range(50):
        mid = 0.5 * (low + high)
        p = price_cap_black(mid, K, exclude_first)
        if p < 0.01:
            low = mid
        else:
            high = mid
    black_vol = low
    print(f"Implied Black Vol for 1.00% price: {black_vol*100:.4f}%")
    
    # Implied Normal Vol
    low, high = 0.0001, 0.2
    for _ in range(50):
        mid = 0.5 * (low + high)
        p = price_cap_normal(mid, K, exclude_first)
        if p < 0.01:
            low = mid
        else:
            high = mid
    normal_vol = low
    print(f"Implied Normal Vol for 1.00% price: {normal_vol*10000:.4f} bps")

    # Price for 14.1% Black Vol
    p_141 = price_cap_black(0.141, K, exclude_first)
    print(f"Price for 14.1% Black Vol: {p_141*100:.4f}%")

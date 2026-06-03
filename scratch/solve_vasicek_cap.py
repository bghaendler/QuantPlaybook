import math

# Parameters
kappa = 0.86
theta = 0.09
sig = 0.0148
r0 = 0.08
N = 120
delta = 0.25

# Vasicek ZCB price function P(0, T)
def vasicek_B(T):
    return (1 - math.exp(-kappa * T)) / kappa

def vasicek_A(T):
    B = vasicek_B(T)
    val = (theta - (sig**2) / (2 * kappa**2)) * (B - T) - (sig**2 * B**2) / (4 * kappa)
    return math.exp(val)

def get_P(T):
    return vasicek_A(T) * math.exp(-vasicek_B(T) * r0)

# Compute discount factors
P = [get_P(i * delta) for i in range(N + 1)]
print("Discount factors P(0, 1) to P(0, 30):")
print("P(0, 0.25) =", P[1])
print("P(0, 30.0) =", P[120])

# Since the ATM cap starts at i=0, we have reset/settlement dates T_i = (i+1)/4 for i=0,...,119.
# The swap payment dates are T_1 = 0.25, ..., T_120 = 30.0.
# The reset dates are T_0 = 0, ..., T_119 = 29.75.
# Wait! Let's see if the first caplet (reset at T_0 = 0) is included.
# Let's compute both:
# Interpretation A: Includes first period (starts at i=0).
# Under Interpretation A, the par swap rate is:
# swap is from T_0 = 0 to T_N = 30.0.
kappa_A = (P[0] - P[120]) / (delta * sum(P[1:121]))
print("Interpretation A (include first) - Par swap rate:", round(kappa_A * 100, 4), "%")

# Interpretation B: Excludes first period (starts at i=1, i.e., reset at T_1 = 0.25, settles at T_2 = 0.50).
# swap is forward-starting from T_1 = 0.25 to T_120 = 30.0.
kappa_B = (P[1] - P[120]) / (delta * sum(P[2:121]))
print("Interpretation B (exclude first) - Par swap rate:", round(kappa_B * 100, 4), "%")

# Let's write the put option on ZCB in Vasicek
def cdf(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))

def price_vasicek_cap(K, exclude_first=False):
    total = 0.0
    start = 1 if exclude_first else 0
    # X_strike for ZCB option is 1 / (1 + delta * K)
    X = 1.0 / (1.0 + delta * K)
    
    for i in range(start, N):
        # caplet i resets at T_r = i * delta, settles at T_p = (i+1) * delta
        Tr = i * delta
        Tp = (i + 1) * delta
        
        if Tr == 0:
            # Deterministic caplet at t=0
            # forward rate L(0, delta) = (1/delta) * (P[0]/P[1] - 1)
            # payoff is delta * max(L - K, 0) * P[1] = max(P[0] - P[1] * (1 + delta*K), 0)
            total += max(P[0] - P[1] * (1.0 + delta * K), 0.0)
            continue
            
        # ZCB Put price in Vasicek
        # Volatility of bond option sigma_p
        # sigma_p = sig * B(Tr, Tp) * sqrt((1 - e^{-2*kappa*Tr}) / (2*kappa))
        B_diff = (1.0 - math.exp(-kappa * (Tp - Tr))) / kappa
        sig_p = sig * B_diff * math.sqrt((1.0 - math.exp(-2.0 * kappa * Tr)) / (2.0 * kappa))
        
        # bond prices
        P_r = P[i]   # P(0, Tr)
        P_p = P[i+1] # P(0, Tp)
        
        d1 = (math.log(P_p / (X * P_r)) + 0.5 * sig_p**2) / sig_p
        d2 = d1 - sig_p
        
        put_val = X * P_r * cdf(-d2) - P_p * cdf(-d1)
        total += (1.0 + delta * K) * put_val
        
    return total

price_A = price_vasicek_cap(kappa_A, False)
print("Interpretation A (include first) - Cap price:", round(price_A * 100, 4), "%")

price_B = price_vasicek_cap(kappa_B, True)
print("Interpretation B (exclude first) - Cap price:", round(price_B * 100, 4), "%")


import math

# Given parameters
kappa = 0.2
sig = 0.1
r0 = 0.05
T = 1.0
target_P = 1.0 / 1.05  # since 1-year LIBOR is 5%

# Calculate h
h = math.sqrt(kappa**2 + 2 * sig**2)

# Calculate B(T)
num_B = 2 * (math.exp(h * T) - 1)
den_B = (kappa + h) * (math.exp(h * T) - 1) + 2 * h
B_T = num_B / den_B

# Calculate A(T) base (excluding the exponent 2*kappa*theta / sig**2)
num_A_base = 2 * h * math.exp((kappa + h) * T / 2.0)
den_A_base = den_B
A_base = num_A_base / den_A_base

print(f"h = {h}")
print(f"B(T) = {B_T}")
print(f"A_base = {A_base}")

# Bond price formula: P(0, T) = A(T) * exp(-B(T) * r0)
# A(T) = A_base ** (2 * kappa * theta / sig**2)
# target_P = A_base ** (2 * kappa * theta / sig**2) * exp(-B(T) * r0)
# A_base ** (2 * kappa * theta / sig**2) = target_P * exp(B(T) * r0)
# (2 * kappa * theta / sig**2) * ln(A_base) = ln(target_P) + B(T) * r0
# theta = (sig**2 / (2 * kappa * ln(A_base))) * (ln(target_P) + B(T) * r0)

ln_A_base = math.log(A_base)
rhs = math.log(target_P) + B_T * r0
theta = (sig**2 / (2 * kappa * ln_A_base)) * rhs

print(f"Optimal theta: {theta}")
print(f"Optimal theta in %: {theta * 100:.6f}%")

# Double check bond price with this theta
A_T = A_base ** (2 * kappa * theta / sig**2)
P_check = A_T * math.exp(-B_T * r0)
print(f"Check bond price: {P_check} (Target: {target_P})")
print(f"Check LIBOR: {(1/P_check - 1)*100}%")

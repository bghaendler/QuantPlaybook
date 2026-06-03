import math

# Given parameters
kappa = 0.86
sig = 0.01

# B(1, 2)
B_1_2 = (1 - math.exp(-kappa)) / kappa

# Variance of r(1)
var_r1 = sig**2 * (1 - math.exp(-2 * kappa)) / (2 * kappa)
std_r1 = math.sqrt(var_r1)

# Standard deviation of Z
std_Z = B_1_2 * std_r1

print(f"B(1, 2) = {B_1_2}")
print(f"std_r1 = {std_r1}")
print(f"std_Z = {std_Z}")
print(f"std_Z in bps = {std_Z * 10000:.6f}")

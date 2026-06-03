import numpy as np

y = 0.08
q = 1.0 / (1.0 + y)

# Price
price = q / (1.0 - q)
print(f"Price: {price:.2f}")

# Duration
duration = (1.0 + y) / y
print(f"Duration: {duration:.2f}")

# Macaulay Convexity: sum(k^2 * q^k) / price
# sum(k^2 * q^k) = q * (1 + q) / (1 - q)^3
sum_k2 = q * (1.0 + q) / (1.0 - q)**3
mac_conv = sum_k2 / price
print(f"Macaulay Convexity: {mac_conv:.2f}")

# Modified Convexity: (1 / price) * d^2 Price / dy^2
# Price = 1/y => d^2 Price / dy^2 = 2 / y^3
# Modified Convexity = (1 / (1/y)) * (2 / y^3) = 2 / y^2
mod_conv = 2.0 / (y**2)
print(f"Modified Convexity: {mod_conv:.2f}")

# Let's also check if there is another common definition:
# Convexity = sum(k * (k+1) * q^(k+2)) / price? No, that's modified convexity.
# Let's check another definition: sum(k * (k+1) * q^k) / (price * (1+y)^2)
sum_k_k_plus_1 = sum(k * (k + 1) * (q ** k) for k in range(1, 10000))
mod_conv_check = sum_k_k_plus_1 / (price * (1.0 + y)**2)
print(f"Modified Convexity (check): {mod_conv_check:.2f}")

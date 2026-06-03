# Q1 swap valuation
S1 = 0.06
S2 = 0.06
K = 0.05
N = 100.0

# Discount factors at t=3
D1 = 1.0 / (1.0 + S1)
D2 = (1.0 - S2 * D1) / (1.0 + S2)

print(f"D1 (t=4 from t=3): {D1:.6f}")
print(f"D2 (t=5 from t=3): {D2:.6f}")

# Value of receiving fixed K and paying floating
# PV of fixed leg = N * (K * D1 + K * D2)
# PV of floating leg = N * (1 - D2)
pv_fixed = N * (K * D1 + K * D2)
pv_floating = N * (1.0 - D2)
val = pv_fixed - pv_floating

print(f"PV Fixed Leg: {pv_fixed:.6f}")
print(f"PV Floating Leg: {pv_floating:.6f}")
print(f"Swap Value: {val:.6f}")
print(f"Swap Value rounded: {val:.2f}")

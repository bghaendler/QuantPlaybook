import numpy as np

kappa = 0.86
theta = 0.08
sigma = 0.01
r0 = 0.06
delta = 0.25
T0 = 1.0
T1 = 1.25

def B_vas(T):
    return (1.0 - np.exp(-kappa * T)) / kappa

def A_vas(T):
    term1 = (theta - (sigma**2) / (2.0 * kappa**2)) * (B_vas(T) - T)
    term2 = (sigma**2) * (B_vas(T)**2) / (4.0 * kappa)
    return term1 - term2

P_T0 = np.exp(A_vas(T0) - B_vas(T0) * r0)
P_T1 = np.exp(A_vas(T1) - B_vas(T1) * r0)
ratio = P_T0 / P_T1

exponent = (sigma**2) / (2.0 * kappa**3) * (1.0 - np.exp(-kappa * delta)) * (1.0 - np.exp(-kappa * T0))**2
gamma = (1.0 / delta) * ratio * (np.exp(exponent) - 1.0)
gamma_bps = gamma * 10000.0

print("B(1.0):", B_vas(T0))
print("A(1.0):", A_vas(T0))
print("P(0, 1.0):", P_T0)
print("B(1.25):", B_vas(T1))
print("A(1.25):", A_vas(T1))
print("P(0, 1.25):", P_T1)
print("Ratio P(0,1.0)/P(0,1.25):", ratio)
print("Exponent:", exponent)
print("Gamma (raw):", gamma)
print("Gamma (bps):", gamma_bps)
print("Gamma (bps) rounded to 2 decimal places: {:.2f}".format(gamma_bps))
print("Gamma (bps) rounded to 4 decimal places: {:.4f}".format(gamma_bps))

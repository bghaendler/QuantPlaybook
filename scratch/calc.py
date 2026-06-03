import numpy as np

kappa = 0.86
theta = 0.08
sigma = 0.01
r_0 = 0.06
delta = 0.25
T0 = 1.0
T1 = 1.25
t = 0.0

# Affine functions B(tau), A(tau)
def B(tau, kappa):
    return (1.0 - np.exp(-kappa * tau)) / kappa

def A(tau, kappa, theta, sigma):
    term1 = (theta - (sigma**2) / (2.0 * (kappa**2))) * (B(tau, kappa) - tau)
    term2 = (sigma**2) * (B(tau, kappa)**2) / (4.0 * kappa)
    return term1 - term2

# Direct Vasicek expectation of 1/P(T_0, T_1)
# P(T_0, T_1)^{-1} = exp(-A(delta) + B(delta) * r(T_0))
# r(T_0) | F_t ~ N(mu_r, var_r)
mu_r = r_0 * np.exp(-kappa * (T0 - t)) + theta * (1.0 - np.exp(-kappa * (T0 - t)))
var_r = ((sigma**2) / (2.0 * kappa)) * (1.0 - np.exp(-2.0 * kappa * (T0 - t)))

E_inv_P = np.exp(-A(delta, kappa, theta, sigma) + B(delta, kappa) * mu_r + 0.5 * (B(delta, kappa)**2) * var_r)

P_T0 = np.exp(A(T0 - t, kappa, theta, sigma) - B(T0 - t, kappa) * r_0)
P_T1 = np.exp(A(T1 - t, kappa, theta, sigma) - B(T1 - t, kappa) * r_0)

gamma_direct = (1.0 / delta) * (E_inv_P - P_T0 / P_T1)
gamma_direct_bps = gamma_direct * 10000.0

print(f"Direct Vasicek expectation E[1/P(T0, T1)]: {E_inv_P:.8f}")
print(f"Direct Vasicek convexity adjustment (bps): {gamma_direct_bps:.8f}")

# Let's compare this with Formula 1 (code's formula):
exponent_code = ((sigma**2) / (2.0 * (kappa**3))) * (1.0 - np.exp(-kappa * delta)) * ((1.0 - np.exp(-kappa * (T0 - t)))**2)
gamma_code = (1.0 / delta) * (P_T0 / P_T1) * (np.exp(exponent_code) - 1.0)
print(f"Formula 1 convexity adjustment (bps): {gamma_code * 10000.0:.8f}")

# Let's compare with Formula 3 (screenshot's formula):
I = (1.0/kappa)*(1.0 - np.exp(-kappa*T0)) - (np.exp(-kappa*delta)/(2.0*kappa))*(1.0 - np.exp(-2.0*kappa*T0))
exponent_3 = ((sigma**2) / (kappa**2)) * (1.0 - np.exp(-kappa*delta)) * I
gamma_3 = (1.0 / delta) * (P_T0 / P_T1) * (np.exp(exponent_3) - 1.0)
print(f"Formula 3 convexity adjustment (bps): {gamma_3 * 10000.0:.8f}")

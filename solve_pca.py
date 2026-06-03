import pandas as pd
import numpy as np

# Read data and format index
# We need to handle the date format correctly "YYYY MM" or "YYYY-MM-DD"
data = pd.read_csv('SwissGovYields.csv', index_col=0)
# Convert string index to datetime if not already
data.index = pd.to_datetime(data.index, format='%Y %m', errors='ignore')
try:
    data.index = pd.to_datetime(data.index)
except:
    pass

data = data / 100.0  # Convert percentages to decimals

# Calculate monthly changes
changes = data.diff().dropna()

# Perform PCA
cov_mat = np.cov(changes, rowvar=False) # ddof=1 is used by np.cov by default
lambdas, A = np.linalg.eig(cov_mat)

# Sort eigenvalues and eigenvectors in descending order
idx = lambdas.argsort()[::-1]
lambdas = lambdas[idx]
A = A[:, idx]

# Question a)
# Variance explained by first two principal components
var_explained = np.sum(lambdas[:2]) / np.sum(lambdas)
print(f"a) Variance explained by first two PCs: {var_explained * 100:.2f}%")

# Question b)
# July 2010 yields for maturities 2, 3, 4, 5
# Note: July 2010 is the last row in the dataset
yields_jul2010 = data.loc['2010-07'].iloc[0] if isinstance(data.loc['2010-07'], pd.DataFrame) else data.loc['2010-07']
if len(yields_jul2010.shape) > 1:
    yields_jul2010 = yields_jul2010.iloc[-1]
elif isinstance(yields_jul2010, pd.DataFrame):
    yields_jul2010 = yields_jul2010.iloc[0]

# Extract yields for 2, 3, 4, 5 years (columns 0, 1, 2, 3)
y_i = yields_jul2010.iloc[0:4].values

# Portfolio Cash Flows
T_i = np.array([2, 3, 4, 5])
CF_i = np.array([80, 70, 150, 40])

# Calculate partial derivatives
# V = sum(CF_i * exp(-y_i * T_i))
# dV/dy_i = -CF_i * T_i * exp(-y_i * T_i)
dV_dy = -CF_i * T_i * np.exp(-y_i * T_i)

# The time derivative term partial_t * dt is constant for all months
# Since we need the STANDARD DEVIATION of delta V, the constant term does not affect the standard deviation.
# We just need to compute the standard deviation of sum(dV/dy_i * delta_y_i)

# Reconstruct monthly changes using only first two principal components
mean_changes = changes.mean(axis=0).values
X_centered = changes.values - mean_changes

# Project onto principal components
Y_scores = np.dot(X_centered, A)

# Reconstruct using first 2 components
Y_reduced = Y_scores[:, :2]
A_reduced = A[:, :2]
X_reconstructed = np.dot(Y_reduced, A_reduced.T)
dy_approx = X_reconstructed + mean_changes

# Extract only the approximated changes for the 2, 3, 4, 5 year maturities
dy_approx_sub = dy_approx[:, 0:4]

# Calculate approximated dV time series
# dV approx = constant + sum(dV_dy * dy_approx_sub)
dV_approx_series = np.dot(dy_approx_sub, dV_dy)

# Calculate empirical standard deviation
# Typically empirical standard deviation uses ddof=1 (sample standard deviation)
std_dV = np.std(dV_approx_series, ddof=1)

print(f"b) Empirical standard deviation of the monthly change of portfolio value: {std_dV:.2f}")


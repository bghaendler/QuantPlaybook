import pandas as pd
import numpy as np
import json

data = pd.read_csv('../SwissGovYields.csv', index_col=0)
data = data / 100.0  # Decimals
changes = data.diff().dropna()
cov_mat = np.cov(changes, rowvar=False)
lambdas, A = np.linalg.eig(cov_mat)

# Sort descending
idx = lambdas.argsort()[::-1]
lambdas = lambdas[idx]
A = A[:, idx]

mean_changes = changes.mean(axis=0).values

# Last row (July 2010)
jul2010 = data.iloc[-1].values

cols = list(data.columns)

output = {
    "columns": cols,
    "eigenvalues": list(lambdas),
    "eigenvectors": A.tolist(),
    "mean_changes": list(mean_changes),
    "jul2010_yields": list(jul2010 * 100.0)  # back to %
}

print(json.dumps(output, indent=2))

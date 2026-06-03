
# Bjerksund-Stensland (2002) - Math Engine Breakdown

## ✅ IMPLEMENTATION COMPLETE

The Bjerksund-Stensland (2002) model is now fully implemented in the backend. This document provides the **Math Engine breakdown** to guide the user (or frontend implementation) through the complex "Two-Step Boundary" logic.

## 🎯 Math Engine - 4 Interactive Steps

### Step 1: The Setup & Beta ($\beta$)
Unlike Black-Scholes which assumes a fixed setup, BS2002 starts by solving the fundamental quadratic equation that defines the "elasticity" of the option price with respect to the boundary.

**Formula Display:**
```math
\beta = \left(\frac{1}{2} - \frac{b}{\sigma^2}\right) + \sqrt{\left(\frac{b}{\sigma^2} - \frac{1}{2}\right)^2 + \frac{2r}{\sigma^2}}
```

**Narrative:**
*   "This $\beta$ parameter is the key to the 'Early Exercise Premium'. It determines how much extra value the American feature adds compared to a European option."
*   **Comparison**: Same $\beta$ as the 1993 model, but used twice here!

### Step 2: The Two Barriers ($I_1$ and $I_2$) 🚀
The 2002 model's main innovation: **Splitting time**.

**Time Split:**
```math
t_1 = \tfrac{1}{2}(\sqrt{5}-1) T  \approx 0.618 T
```
*   **Golden Ratio!** The time split uses the golden section for optimal approximation.

**Boundaries:**
1.  **$I_1$**: The flat boundary effective from $0$ to $t_1$.
2.  **$I_2$**: The flat boundary effective from $t_1$ to $T$.

**Visual Logic:**
*   Instead of one flat line (BS93), we have a "step" function. This approximates the true curved boundary much better.
*   *If Spot > Barrier at any point, we exercise!*

### Step 3: The Building Blocks ($\phi$ and $\Psi$) 🧩
This is where the math gets heavy. The price is a sum of probability-weighted terms.

**The $\phi$ Function (Univariate):**
*   Represents the probability of staying below a barrier in a single time interval.
*   Uses standard Normal CDF $N(\cdot)$.

**The $\Psi$ Function (Bivariate) ⭐:**
*   **New in 2002!** Represents the joint probability of staying below $I_1$ in the first period AND staying below $I_2$ in the second period.
*   Uses **Cumulative Bivariate Normal Distribution** $M(\cdot)$.
*   *Correlation coefficient* $\rho = \sqrt{t_1/T}$.

### Step 4: The Valuation Formula 🧮
The final price $C$ is a sum of 6-8 terms:

```math
C = \alpha(I_2)S^\beta - \alpha(I_2)\phi(S, t_1, \dots) + \dots + \Psi(\dots)
```

**Receipt Breakdown:**
*   **Immediate Exercise Value**: $(S-X)$ (if $S \ge I$)
*   **European Value**: Base value if no early exercise.
*   **Early Exercise Premium**: The extra value captured by the $\beta$ terms and boundaries.

## 🎨 Visual Design Features for Frontend

If implementing this in the frontend Math Engine:
1.  **Step-Boundary Chart**: Plot time on X-axis, Price on Y-axis. Show $I_1$ as a flat line for first 60% of time, then $I_2$ as a flat line for the rest.
2.  **Heatmap**: Show probability density.
3.  **Golden Ratio Note**: Highlight that $t_1$ is chosen via $( \sqrt{5}-1)/2$.

## 📊 Accuracy vs Complexity Table

| Model | Setup | Boundaries | Distribution | Accuracy | Speed |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **BS 1993** | $\beta$ | 1 Flat Line | Univariate $N(\cdot)$ | Good | Very Fast |
| **BS 2002** | $\beta$ | **2 Flat Levels** | **Bivariate $M(\cdot)$** | **Excellent** | Slower |
| **Binomial** | Mesh | Steps | Discrete | Exact | Slow |

## 🌟 Why BS2002?
References typically cite BS2002 as the **"practitioner's choice"** for American options when speed is less critical than precision but full tree methods are too slow. It captures the curvature of the boundary without the computational cost of thousands of tree nodes.

## 📝 Implementation Notes
The backend implementation in `bs2002_implementation.py` handles:
*   $\rho$ calculation for bivariate normal.
*   The exact algebraic sum of the 4 $\phi$ terms and 4 $\Psi$ terms.
*   Edge cases where $b \ge r$ (European limit).

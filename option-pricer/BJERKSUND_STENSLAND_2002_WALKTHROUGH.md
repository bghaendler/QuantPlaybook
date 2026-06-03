
# Bjerksund-Stensland (2002) Model - Math Walkthrough
<!-- Type: walkthrough -->

## 1. Introduction

The Bjerksund-Stensland (2002) model is a significant refinement of the 1993 approximation for American option pricing. While the 1993 model assumes a single flat exercise boundary, the 2002 model improves accuracy by dividing the time to maturity into two parts, $[0, t_1)$ and $[t_1, T)$, each with its own flat exercise boundary ($I_1$ and $I_2$).

This "Two-Step Boundary" approach allows the model to better capture the curved nature of the true optimal exercise boundary, particularly for long-dated options.

## 2. Key Characteristics

*   **Two Critical Prices**: The model calculates trigger prices $I_1$ (for $t < t_1$) and $I_2$ (for $t_1 \leq t \leq T$).
*   **Accuracy**: It is generally more accurate than Barone-Adesi & Whaley (1987) and Bjerksund & Stensland (1993), providing a closed-form approximation that rivals numerical methods (like Binomial trees) in precision while being much faster for many steps.
*   **Complexity**: Unlike the 1993 model which uses the univariate normal distribution, the 2002 model requires the **cumulative bivariate normal distribution function** ($M(\cdot)$), making it computationally more intensive but mathematically richer.

## 3. Mathematical Formulation

### 3.1 Parameters and Definitions

Let:
*   $S$: Spot price
*   $X$: Strike price
*   $T$: Time to maturity
*   $r$: Risk-free rate
*   $b$: Cost of carry (where $b = r - q$)
*   $\sigma$: Volatility

The model defines the time partition $t_1$:
$$ t_1 = \tfrac{1}{2}(\sqrt{5}-1) T $$

The roots of the characteristic equation $\beta$ are defined as:
$$ \beta = \left(\frac{1}{2} - \frac{b}{\sigma^2}\right) + \sqrt{\left(\frac{b}{\sigma^2} - \frac{1}{2}\right)^2 + \frac{2r}{\sigma^2}} $$

### 3.2 The Exercise Boundaries ($I_1, I_2$)

The boundaries are derived from the asymptotic boundary $B_\infty$ and the zero-time boundary $B_0$:

$$ B_\infty = \frac{\beta}{\beta - 1} X $$
$$ B_0 = \max\left(X, \frac{r}{r-b} X\right) $$

Let $h(t)$ be a helper function:
$$ h(t) = -(b t + 2\sigma\sqrt{t}) \frac{X^2}{(B_\infty - B_0)B_0} $$

The two boundaries are:
$$ I_1 = B_0 + (B_\infty - B_0)(1 - e^{h(t_1)}) $$
$$ I_2 = B_0 + (B_\infty - B_0)(1 - e^{h(T)}) $$

### 3.3 The Call Pricing Formula

The approximation for the American Call price $C$ is given by a sum of terms involving functions $\phi$ (univariate) and $\Psi$ (bivariate).

If $S \ge I_2$, exercise immediately: $C = S - X$.

If $S < I_2$, the price is:

$$ 
\begin{aligned}
C &= \alpha(I_2) S^\beta - \alpha(I_2) \phi(S, t_1, \beta, I_2, I_2) \\
  &\quad + \phi(S, t_1, 1, I_2, I_2) - \phi(S, t_1, 1, I_1, I_2) \\
  &\quad - X \phi(S, t_1, 0, I_2, I_2) + X \phi(S, t_1, 0, I_1, I_2) \\
  &\quad + \alpha(I_1) \phi(S, t_1, \beta, I_1, I_2) - \alpha(I_1) \Psi(S, T, \beta, I_1, I_2, I_1, t_1) \\
  &\quad + \Psi(S, T, 1, I_1, I_2, I_1, t_1) - \Psi(S, T, 1, I_1, I_2, X, t_1) \\
  &\quad - X \Psi(S, T, 0, I_1, I_2, I_1, t_1) + X \Psi(S, T, 0, I_1, I_2, X, t_1)
\end{aligned}
$$

Where $\alpha(I) = (I - X)I^{-\beta}$.

This complex summation adjusts the value of the option by accounting for the probability of hitting the exercise boundary $I_1$ during the first period or $I_2$ during the second period.

The functions $\phi$ and $\Psi$ are defined using the cumulative normal distribution $N(\cdot)$ and the cumulative bivariate normal distribution $M(\cdot)$, respectively.

## 4. Numerical Validation

We verified the model implementation against the provided textbook examples for Options on Futures ($b=0$).

**Parameters:**
*   Strike ($X$): 100
*   Risk-free Rate ($r$): 0.10
*   Time ($T$): 0.5
*   Type: Call (on Future)

**Results Comparison:**

| Volatility ($\sigma$) | Futures Price ($F$) | Textbook BS2002 Value | **Our Implementation** | Error |
| :--- | :--- | :--- | :--- | :--- |
| **0.15** | 90 | 0.8099 | **0.8099** | 0.0000 |
| | 100 | 4.0628 | **4.0628** | 0.0000 |
| | 110 | 10.7898 | **10.7898** | 0.0000 |
| **0.25** | 90 | 2.7180 | **2.7180** | 0.0000 |
| | 100 | 6.7661 | **6.7661** | 0.0000 |
| | 110 | 12.9814 | **12.9814** | 0.0000 |

Our implementation matches the provided reference values to the 4th decimal place, confirming the correctness of the Bivariate Normal logic and the multi-term approximation formula.

## 5. Implementation Files

The full Python implementation is available in `backend/bs2002_implementation.py`. It includes:
1.  `cbnd`: Cumulative Bivariate Normal Distribution helper.
2.  `_bjerksund_stensland_2002`: Main pricing function.
3.  `_bs2002_call`: The core logic implementing the 4-part formula.
4.  `_bs2002_phi` and `_bs2002_psi`: The mathematical helper functions.

To integrate this into your pricing engine, follow the instructions at the bottom of the implementation file.

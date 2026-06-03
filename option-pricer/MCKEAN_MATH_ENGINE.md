
# American Perpetual Options (McKean/Merton) - Math Engine Breakdown

## ✅ IMPLEMENTATION COMPLETE

The American Perpetual Option model (McKean 1965, Merton 1973) is now fully implemented. This document guides the user through the infinite-horizon logic.

## 🎯 Math Engine - 3 Interactive Steps

### Step 1: The Characteristic Root ($\gamma$)
Since time $t$ is removed from the equation (due to $T \to \infty$), the partial differential equation becomes an ordinary differential equation (ODE) of the form:
$$ \tfrac{1}{2}\sigma^2 S^2 F_{SS} + b S F_S - r F = 0 $$
The solution involves finding the roots of the quadratic equation.

**Formula Display:**
```math
\gamma = \frac{1}{2} - \frac{b}{\sigma^2} \pm \sqrt{\left(\frac{b}{\sigma^2} - \frac{1}{2}\right)^2 + \frac{2r}{\sigma^2}}
```
*   **Call**: Use the positive root $\gamma_1 (> 1)$.
*   **Put**: Use the negative root $\gamma_2 (< 0)$.

### Step 2: The Optimal Barrier ($S^*$) 🚧
For a perpetual option, the optimal strategy is a single static barrier.
*   **Values**: If Spot hits this barrier, exercise immediately.

**Formula Display:**
```math
S^* = K \cdot \frac{\gamma}{\gamma - 1}
```
*   The factor $\frac{\gamma}{\gamma - 1}$ is always $> 1$ for Calls (barrier above strike) and always $< 1$ for Puts (barrier below strike).

### Step 3: Valuation Formula 🧮
The value is simply the payoff at the barrier, discounted by the "distance" to the barrier raised to the power of $\gamma$.

**Formula Display:**
```math
V = (S^* - K) \left( \frac{S}{S^*} \right)^\gamma
```

**Receipt Breakdown:**
*   **Barrier Payoff**: $(S^* - K)$
*   **Discount Factor**: $(S/S^*)^\gamma$ (This acts like a probability-weighted discount factor).

## 🎨 Visual Design Features
*   **Barriers**: Visual indicator showing if current Spot is above/below the optimal barrier.
*   **Infinity Icon**: Emphasizes that this model assumes *infinite* time.
*   **Validation**: Confirmed against the textbook example ($X=100, S=90, r=10\%, q=8\%, \sigma=25\% \to 20.6133$).

## 📊 Comparison with Finite Models

| Model | Time Horizon | Boundary | Speed |
| :--- | :--- | :--- | :--- |
| **Black-Scholes** | Finite ($T$) | N/A (European) | Fast |
| **Bjerksund 2002** | Finite ($T$) | 2 Steps | Moderate |
| **McKean** | **Infinite ($\infty$)** | **1 Static Line** | **Instant** |

## 🌟 Why McKean?
It provides a "floor" or "ceiling" value for long-dated American options. As $T \to \infty$, the BAW and BS2002 models converge to this McKean value. It's a crucial theoretical benchmark.

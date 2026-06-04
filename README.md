# QuantPlaybook 📈

An interactive, premium quantitative finance simulation platform and reference manual. **QuantPlaybook** is designed to bridge advanced theoretical stochastic calculus models with real-time numeric calculations and visual laboratories. Inspired by clean Notion-style layout aesthetics, it features a unified collapsible sidebar workspace, dark/light themes, and beautiful, interactive data models.

To make this quantitative finance training book app highly practical, we integrate the comprehensive analytical and closed-form formulas compiled in Espen Gaarder Haug’s landmark text, ***The Complete Guide to Option Pricing Formulas***. 

While the Certificate in Quantitative Finance (CQF) provides conceptual depth and Paul Wilmott offers physical intuition and modeling limitations, Haug’s work provides the exact mathematical "dictionary" of closed-form formulas, analytical approximations, and distribution functions used on trading desks.

---

# **The Comprehensive App Menu Outline**

## **Phase 0: Preparatory Primers (Pre-Program)**
*Aim: Aligning mathematics, programming, and financial knowledge to the baseline required for quant-level modeling.*

*   **0.1 Mathematics Primer:** 
    *   Calculus (Differentiation, integration, Taylor series).
    *   Linear Algebra (Matrices, vectors, eigenvalues, and eigenvectors).
    *   Differential Equations (Ordinary and partial differential equations).
*   **0.2 Python/C++ Programming Primer:** 
    *   Python core syntax, data analysis libraries (NumPy, Pandas, SciPy).
    *   Introduction to object-oriented programming (classes, inheritance, memory management in C++).
*   **0.3 Finance Primer:** 
    *   Time value of money, yield calculations, primary asset classes, and market structure.

---

## **Module 1: Building Blocks of Quantitative Finance (Beginner)**
*Aim: Standardizing the mathematical tools used to model asset prices in continuous time.*

*   **1.1 Random Behavior of Assets:**
    *   Random walks, Brownian motion, and continuous-time limits.
    *   Empirical stylised facts of asset returns (fat tails, volatility clustering).
*   **1.2 Applied Ito Calculus:**
    *   Stochastic differential equations (SDEs).
    *   Ito’s Lemma and the quadratic variation of Brownian motion.
    *   Transition density functions: Fokker-Planck (forward Kolmogorov) and backward Kolmogorov equations.
*   **1.3 Martingale Theory Foundations:**
    *   Conditional expectation, martingales, and the Radon-Nikodym derivative.
    *   Girsanov's Theorem and the change of probability measure.
*   **1.4 Wilmott’s Classic Case Study: The Mathematics of Gambling**
    *   Kelly Criterion, coin-tossing, and optimal bet sizing.

---

## **Module 2: Quantitative Risk and Return (Lower Intermediate)**
*Aim: Optimizing asset allocation, measuring volatility, and managing regulatory and portfolio risk.*

*   **2.1 Classical Portfolio Theory:**
    *   Markowitz Mean-Variance Portfolio Optimization and the Efficient Frontier.
    *   The Capital Asset Pricing Model (CAPM) and Arbitrage Pricing Theory (APT).
    *   Black-Litterman Model: Incorporating active investor views.
*   **2.2 Value at Risk (VaR) & Expected Shortfall (ES):**
    *   Parametric, historical, and Monte Carlo approaches to VaR.
    *   Coherent risk measures and Expected Shortfall.
*   **2.3 Empirical Volatility Modeling:**
    *   ARCH, GARCH, and extensions (EGARCH, GJR-GARCH).
    *   Realized and implied volatility dynamics.
*   **2.4 Risk Regulation & Operational Realities:**
    *   Basel Accord evolution (Basel I, II, III, and IV).
    *   Collateral, margins, and the role of clearinghouses (CCPs).

---

## **Module 3: Equities, Currencies, & Vanilla Option Formulas (Intermediate)**
*Aim: Mastering the exact closed-form pricing models and analytical approximations for vanilla contracts.*

*   **3.1 The Generalized Black-Scholes-Merton Model (Haug Ch. 1):**
    *   The standard Black-Scholes-Merton formula.
    *   **The Cost of Carry ($b$) Framework:** Consolidating pricing formulas for stocks ($b=r-q$), stock indexes ($b=r-q$), futures ($b=0$ via Black-76), and foreign currencies ($b=r-r_f$ via Garman-Kohlhagen) into a single generalized equation.
    *   Historical models (Bachelier normal model, Sprenkle, Boness, Samuelson).
*   **3.2 Closed-Form Options Greeks (Haug Ch. 2):**
    *   Exact analytical formulas for first-order Greeks (Delta, Gamma, Theta, Vega, Rho).
    *   Higher-order and cross-asset Greeks (Vanna, Volga, Color, Charm).
*   **3.3 Analytical Approximations for American Options (Haug Ch. 3):**
    *   Why analytical solutions fail for American early exercise.
    *   **Roll-Geske-Whaley Model:** Analytical formula for American calls on dividend-paying stocks.
    *   **Barone-Adesi and Whaley Quadratic Approximation:** Analytical approximation for American options.
    *   **Bjerksund and Stensland Model:** Highly accurate analytical approximation for American option pricing.
*   **3.4 Discrete Dividends & Volatility Solvers (Haug Ch. 9 & 12):**
    *   Adjusting pricing formulas for stocks paying discrete dividends (Escrowed dividend model, Roll-Geske-Whaley modifications).
    *   Numerical solvers for Implied Volatility: Bisection, Newton-Raphson, and the Corrado-Miller closed-form approximation.

---

## **Module 4: Numerical Methods & Data Science (Upper Intermediate)**
*Aim: Pricing options when analytical formulas do not exist, and applying modern machine learning tools to market data.*

*   **4.1 Trees and Finite Difference Methods (Haug Ch. 7 & Wilmott Vol. 3):**
    *   **Binomial & Trinomial Trees:** Cox-Ross-Rubinstein model, Leisen-Reimer, and trinomial extensions.
    *   **Finite Difference Methods:** Implicit, Explicit, and Crank-Nicolson schemes for solving the Black-Scholes PDE.
*   **4.2 Monte Carlo Simulation (Haug Ch. 8):**
    *   Generating paths under Geometric Brownian Motion.
    *   Low-discrepancy sequences (Quasi-Monte Carlo) and variance reduction (Antithetic, Control Variates).
*   **4.3 Machine Learning in Finance (CQF Module 4 & 5):**
    *   **Supervised Learning:** Lasso, Ridge, Random Forests, XGBoost, and Support Vector Machines (SVM).
    *   **Unsupervised Learning:** K-Means and Gaussian Mixture Models (GMM) for market regime detection.
    *   **Deep Learning & NLP:** LSTM networks for time-series forecasting; sentiment analysis of financial text (news, transcripts).
    *   **Reinforcement Learning:** Q-learning for automated execution and portfolio management.

---

## **Module 5: Commodities, Energy, & Interest Rate Derivatives (Advanced)**
*Aim: Expanding quantitative valuation models to physical assets, commodities, and debt instruments.*

*   **5.1 Commodity and Energy Options (Haug Ch. 10):**
    *   The Black '76 model for commodity options.
    *   **Spread Options:** Pricing spark spreads (power vs. natural gas/coal) and crack spreads (refined products vs. crude oil).
    *   **Swing Contracts:** Analytical approximations for energy contracts with flexible volume take-up.
*   **5.2 Interest Rate Derivative Formulas (Haug Ch. 11 & Wilmott Vol. 2):**
    *   Analytical formulas for interest rate Caps, Floors, and Swaptions (using the lognormal Black model).
    *   One-factor short-rate models (Vasicek, Cox-Ingersoll-Ross, Hull-White).
    *   Framework models: Heath-Jarrow-Morton (HJM) and the Libor Market Model (LMM).

---

## **Module 6: The Haug Library of Exotic Options & Credit Risk (Expert)**
*Aim: Implementing exact closed-form pricing for complex path-dependent exotics, correlation products, and credit structures.*

*   **6.1 Exotic Options on a Single Asset (Haug Ch. 4):**
    *   **Binary/Digital Options:** Asset-or-nothing and cash-or-nothing formulas.
    *   **Barrier Options:** Analytical formulas for standard down-and-out, down-and-in, up-and-out, and up-and-in options (Rubinstein-Reiner formulas).
    *   **Lookback Options:** Goldman-Soshin-Gatto formulas for floating strike lookbacks; Conze-Viswanathan formulas for fixed strike lookbacks.
    *   **Asian Options:** Exact formulas for Geometric Asians; analytical approximations for Arithmetic Asians (Levy, Turnbull-Wakeman).
    *   **Compound and Chooser Options:** Geske’s formula for options-on-options; Rubinstein’s formula for complex choosers.
*   **6.2 Exotic Options on Two Assets (Haug Ch. 5):**
    *   **Exchange Options:** Margrabe’s formula to exchange one asset for another.
    *   **Rainbow Options:** Options on the maximum or minimum of two risky assets (Stulz formulas).
    *   **Basket Options & Spread Options:** Analytical approximations for index and portfolio options (Kirk’s approximation for spread options).
*   **6.3 Black-Scholes-Merton Adjustments & Alternatives (Haug Ch. 6):**
    *   **Merton’s Jump-Diffusion Model:** Pricing options when asset prices can exhibit discontinuous jumps.
    *   **Gram-Charlier Expansion:** Adjusting the standard BSM model for non-normal skewness and kurtosis in the underlying asset returns.
*   **6.4 Credit Risk Modeling (Wilmott Vol. 2):**
    *   Merton’s structural model of default.
    *   Reduced-form intensity models.
    *   Credit derivatives (CDS pricing) and copulas for joint default correlation (CDO pricing).
*   **6.5 Statistical Distribution Helpers (Haug Ch. 13):**
    *   The mathematical approximations required to evaluate the cumulative univariate, bivariate, and trivariate normal distributions (which underpin the exotic and multi-asset option formulas above).

---

### **App Interface & Interaction Mapping (Haug Integration)**

Integrating Haug's content provides highly functional utility for your app’s user interface:

*   **The "Haug Dictionary" Look-up Tool:** A quick-reference calculator where users select any exotic option (e.g., *Down-and-Out Barrier Call*), input the variables ($S, K, \sigma, r, q, H$), and instantly view both the calculated price/Greeks and the raw mathematical formula.
*   **Formula vs. Simulation Sandbox:** An interactive module where users price a complex option (like an *Arithmetic Asian*) using Haug’s closed-form approximation, then run a Monte Carlo simulation alongside it, visually tracking how the simulated price converges toward the Haug analytical value as the number of paths increases.

---

## 🛠 System Architecture

The application is built on a modern, decoupled stack ensuring sub-millisecond numeric execution and reactive UI rendering:
- **Backend (API)**: Powered by **FastAPI** (`app/backend.py`), managing CSV data feeds (like Swiss government yields), interest rate calibration routines, and math computation models.
- **Frontend**: A highly polished, single-page application (`app/index.html` and components) utilizing:
  - **Chart.js** for real-time asset paths, term structures, and bivariate normal distribution plots.
  - **MathJax 3** for rendering complex mathematical equations ($\Phi_2$, $\Phi$, $\lambda$, etc.).
  - **Vanilla CSS** with CSS Custom Properties for smooth dark/light theme switching.

---

## 💻 How to Run Locally

### Prerequisites
- Python 3.8+
- Node.js (only if compiling option-pricer frontend dependencies, otherwise the app uses precompiled production builds in `/pricer`)

### Setup and Execution

1. **Install Python Dependencies**:
   ```bash
   pip install fastapi uvicorn pandas numpy scipy jinja2
   ```

2. **Start the Application**:
   Navigate to the project root and run the FastAPI server:
   ```bash
   python3 app/backend.py
   ```
   *Alternatively:*
   ```bash
   uvicorn app.backend:app --host 127.0.0.1 --port 8000 --reload
   ```

3. **Open in Browser**:
   Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your web browser.

---

## 📂 Project Structure

```
.
├── README.md               # Main documentation manual (this file)
├── .gitignore              # Git ignore rules for node_modules/venv
├── SwissGovYields.csv      # Swiss yield data source
├── app/
│   ├── backend.py          # FastAPI application server
│   ├── index.html          # Main application page (QuantPlaybook workspace)
│   └── templates/
│       └── sections/
│           ├── view-cqf-m6-l9.html          # Credit Default Swaps view
│           └── view-cqf-option-pricer.html  # Option Pricer mount point
└── option-pricer/          # Option Pricer subsystem code
```

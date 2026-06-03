# QuantPlaybook 📈

An interactive, premium quantitative finance simulation platform and reference manual. **QuantPlaybook** is designed to bridge advanced theoretical stochastic calculus models with real-time numeric calculations and visual laboratories. Inspired by modern Notion-style styling, it features a unified collapsible sidebar workspace, dark/light themes, and beautiful, interactive data models.

---

## 🚀 Key Modules & Interactive Labs

### 1. Fixed Income & Credit (Module 06)
#### **Lecture 09: Credit Default Swaps (CDS)**
- **Risky Discounting & Survival Math**: Explores physical/cash default settlements and calibrates credit default hazard rate curves under the assumption $S(t) = \exp(-ht)$.
- **Lab A (Survival Probability Bootstrapper)**: Calibrates constant default intensity hazard rates dynamically across customized Recovery Rates (RR) and plots the term structure of survival curves.
- **Lab B (FRTB-CVA Proxy Regressor)**: Estimates proxy credit default swap spreads for illiquid counterparties under Basel III rules based on Credit Rating (AAA to CCC), Geographical Region, and Sector attributes.
- **Lab C (Wrong-Way Risk Gaussian Copula)**: Models counterparty wrong-way risk (WWR) using a continuous bivariate Gaussian Copula integrated via Simpson's rule over 10 steps in raw JavaScript for sub-millisecond execution.

---

### 2. Interactive Option Pricer
Contains complete interactive mathematical engines for option pricing across classical and pre-BSM historical milestones:
- **Bachelier (1900)**: The birth of mathematical finance using arithmetic Brownian motion.
- **Sprenkle (1961)**: Introducing log-normal stock pricing and default/survival coefficients.
- **Boness (1964)**: Incorporating subjective interest rates and risk adjustments.
- **Samuelson (1965)**: Establishing rational option pricing based on geometric Brownian motion.
- **Black-Scholes-Merton (1973)**: The foundational pricing and hedging model.
- **McKean (1965) / Barone-Adesi & Whaley (1987)**: Analytical approximations for American options.
- **Bjerksund-Stensland (1993 / 2002)**: Highly efficient approximations for American options.

---

## 🛠 System Architecture

The application is built on a modern, decoupled stack ensuring sub-millisecond numeric execution and reactive UI rendering:
- **Backend (API)**: Powered by **FastAPI** (`app/backend.py`), managing CSV data feeds (like Swiss government yields), interest rate calibration routines, and math computation models.
- **Frontend**: A highly polished, single-page application (`app/index.html` and components) utilizing:
  - **Chart.js** for real-time asset paths, term structures, and bivariate normal distribution plots.
  - **MathJax 3** for rendering complex mathematical equations ($\Phi_2$, $\Phi$, $\lambda$, etc.).
  - **Vanilla CSS** with CSS Custom Properties for smooth dark/light theme switching.

---

## 📱 How the Sidebar Menu Works

QuantPlaybook features a sleek **Notion-style** navigation panel designed for optimal workspace area:
- **Always-Visible Top Header**: Holds your workspace switcher avatar (`BG`), workspace label (`QuantPlaybook`), the **Theme Toggle** (sun/moon), and the **Collapse Sidebar** button (`●●●`).
- **Collapsible Sidebar**: Clicking the `●●●` button triggers a smooth CSS transition that slides the sidebar left (`margin-left: -290px`), letting the workspace automatically expand to fill the full screen width.
- **Auto-Resize Canvas**: Collapsing or expanding the sidebar automatically dispatches a window `resize` event, forcing active Chart.js simulations to immediately recalculate aspect ratios without visual distortion.
- **Expand / Collapse All**: Contains dedicated controls to expand or collapse all details blocks inside the menu with asynchronous race-condition safety.

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

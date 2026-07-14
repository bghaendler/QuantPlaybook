#!/usr/bin/env python3
"""Enrich the scaffolded Legacy Lecture Series talk sections with real content.

Regenerates app/templates/sections/view-talk-<slug>.html for every legacy talk:
series overview, core mathematics (MathJax), plain-English notes, and prev/next
part navigation. Also restructures the 'Legacy Lecture Series' sidebar group
into one <details> per series with short "Part NN" labels.

Run after scaffold_talk.py --category legacy. Idempotent (regenerates files).
"""
import html as H
import json
import os
import re
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDX = os.path.join(ROOT, "app", "index.html")
SECTIONS = os.path.join(ROOT, "app", "templates", "sections")
CATALOG = os.path.join(ROOT, "scratch", "talks_catalog.json")

# ---------------------------------------------------------------- series content
S = {
    "mmnm": dict(
        nav="Math Methods & Numerical Methods",
        overview="A ground-up tour of the applied mathematics toolkit every quant leans on: "
                 "Taylor expansions, ordinary and partial differential equations, root finding, "
                 "interpolation, numerical integration and the finite-difference method — the numerical "
                 "engine behind PDE option pricing.",
        maths=[
            ("Taylor expansion", r"$$f(x+h) = f(x) + h f'(x) + \tfrac{h^2}{2} f''(x) + O(h^3)$$"),
            ("Newton–Raphson root finding", r"$$x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)}$$"),
            ("Central finite difference", r"$$\frac{\partial V}{\partial S} \approx \frac{V_{i+1} - V_{i-1}}{2\,\Delta S}, \qquad \frac{\partial^2 V}{\partial S^2} \approx \frac{V_{i+1} - 2V_i + V_{i-1}}{\Delta S^2}$$"),
            ("Simpson's rule", r"$$\int_a^b f(x)\,dx \approx \tfrac{h}{3}\left(f_0 + 4f_1 + 2f_2 + \cdots + f_n\right)$$"),
        ],
        plain="Every pricing model ends in a computation. This series builds the bridge from calculus "
              "on paper to stable numerical schemes in code: how to approximate derivatives and integrals, "
              "how fast each method converges, and where naive schemes blow up.",
    ),
    "bsmw": dict(
        nav="BSM & Numerical Methods Workshop",
        presenter="Dr. Riaz Ahmad",
        overview="A four-part workshop deriving and solving the Black-Scholes equation end-to-end: "
                 "transformation to the heat equation, similarity reduction and Greeks, matrix methods "
                 "for implicit schemes, and root-finding for American early exercise.",
        maths=[
            ("Black-Scholes PDE", r"$$\frac{\partial V}{\partial t} + \tfrac{1}{2}\sigma^2 S^2 \frac{\partial^2 V}{\partial S^2} + rS\frac{\partial V}{\partial S} - rV = 0$$"),
            ("Heat-equation transformation", r"$$V(S,t) \;\xrightarrow{\;x=\ln S,\ \tau=\frac{\sigma^2}{2}(T-t)\;}\; \frac{\partial u}{\partial \tau} = \frac{\partial^2 u}{\partial x^2}$$"),
            ("Fundamental solution", r"$$u(x,\tau) = \frac{1}{2\sqrt{\pi \tau}} \int_{-\infty}^{\infty} u_0(s)\, e^{-(x-s)^2/4\tau}\, ds$$"),
            ("Newton–Raphson for the exercise boundary", r"$$S^*_{n+1} = S^*_n - \frac{g(S^*_n)}{g'(S^*_n)}, \qquad g(S^*) = V(S^*) - (K - S^*)$$"),
        ],
        plain="Black-Scholes is 'just' the physicists' heat equation wearing a suit. Change variables and "
              "150 years of diffusion mathematics become available: closed forms for vanillas, and when the "
              "contract kills the closed form (American exercise), numerical root finding takes over.",
    ),
    "mart": dict(
        nav="Martingales",
        overview="The probabilistic backbone of arbitrage-free pricing: conditional expectation, filtrations "
                 "and information, the martingale property, stopping times and the optional stopping theorem, "
                 "and why discounted prices must be martingales under the risk-neutral measure.",
        maths=[
            ("Martingale property", r"$$\mathbb{E}[X_t \,|\, \mathcal{F}_s] = X_s, \qquad s \le t$$"),
            ("Tower property", r"$$\mathbb{E}\big[\,\mathbb{E}[X \,|\, \mathcal{F}_t]\, \big|\, \mathcal{F}_s\big] = \mathbb{E}[X \,|\, \mathcal{F}_s], \qquad s \le t$$"),
            ("Exponential martingale", r"$$M_t = \exp\!\left(\sigma W_t - \tfrac{1}{2}\sigma^2 t\right)$$"),
            ("Risk-neutral pricing", r"$$V_t = \mathbb{E}^{\mathbb{Q}}\!\left[ e^{-r(T-t)}\, V_T \,\middle|\, \mathcal{F}_t \right]$$"),
        ],
        plain="A martingale is a fair game: given everything you know today, tomorrow's expected value is "
              "today's value. No-arbitrage forces discounted asset prices to be fair games under the "
              "risk-neutral measure — that single idea generates every pricing formula in the course.",
    ),
    "pmir": dict(
        nav="Probabilistic Methods for IR",
        overview="Interest rate modelling from the probabilistic side: short-rate dynamics under the "
                 "risk-neutral measure, the bond pricing equation, the market price of risk, and the "
                 "affine models (Vasicek, CIR) with closed-form bond prices.",
        maths=[
            ("Short-rate dynamics", r"$$dr_t = \mu(r_t,t)\,dt + \sigma(r_t,t)\,dW_t$$"),
            ("Bond pricing equation", r"$$\frac{\partial Z}{\partial t} + \tfrac{1}{2}\sigma^2 \frac{\partial^2 Z}{\partial r^2} + (\mu - \lambda\sigma)\frac{\partial Z}{\partial r} - rZ = 0$$"),
            ("Vasicek / CIR", r"$$dr = \kappa(\theta - r)\,dt + \sigma\,dW \qquad\text{vs.}\qquad dr = \kappa(\theta - r)\,dt + \sigma\sqrt{r}\,dW$$"),
            ("Affine bond price", r"$$Z(t,T) = e^{A(t,T) - B(t,T)\, r_t}$$"),
        ],
        plain="Bonds are bets on the path of the overnight rate. Model that single rate as a mean-reverting "
              "random process and the entire yield curve, with its humps and inversions, drops out of one "
              "expectation. The affine family is loved because that expectation has a closed form.",
    ),
    "rba": dict(
        nav="Random Behaviour of Assets",
        overview="The empirical starting point of quantitative finance: examining real return data, the "
                 "random walk model, and the scaling behaviour that leads to Brownian motion as the "
                 "continuous-time limit.",
        maths=[
            ("Simple return", r"$$R_i = \frac{S_{i+1} - S_i}{S_i} \approx \mu\,\delta t + \sigma\,\phi\sqrt{\delta t},\quad \phi \sim N(0,1)$$"),
            ("Scaling signature", r"$$\mathbb{E}[R] \sim \delta t, \qquad \operatorname{sd}(R) \sim \sqrt{\delta t}$$"),
            ("Continuous-time limit", r"$$dS = \mu S\,dt + \sigma S\,dW_t$$"),
        ],
        plain="Measure returns over shorter and shorter windows and a fingerprint emerges: the drift shrinks "
              "linearly, the noise shrinks like a square root. The square root wins at small timescales — "
              "which is why randomness, not the trend, dominates day-to-day prices.",
    ),
    "mrc": dict(
        nav="Model Risk & Calibration",
        overview="A fifteen-part deep dive into fitting models to markets and the danger of trusting the fit: "
                 "calibration as an inverse problem, ill-posedness and regularization, local volatility via "
                 "Dupire, parameter instability, and quantifying model risk as valuation uncertainty.",
        maths=[
            ("Calibration objective", r"$$\min_{\theta} \sum_{i} w_i \left( V^{\text{model}}_i(\theta) - V^{\text{mkt}}_i \right)^2$$"),
            ("Dupire local volatility", r"$$\sigma_{\text{loc}}^2(K,T) = \frac{\dfrac{\partial C}{\partial T} + rK\dfrac{\partial C}{\partial K}}{\tfrac{1}{2}K^2 \dfrac{\partial^2 C}{\partial K^2}}$$"),
            ("Tikhonov regularization", r"$$\min_{\theta}\; \|V(\theta) - V^{\text{mkt}}\|^2 + \alpha\,\|\theta - \theta_0\|^2$$"),
            ("Model risk band", r"$$\text{MR} = \max_{m \in \mathcal{M}} V_m - \min_{m \in \mathcal{M}} V_m \quad\text{over models calibrated to the same data}$$"),
        ],
        plain="Calibration runs a model backwards: instead of parameters in, prices out, it demands the "
              "parameters that reproduce today's market. Backwards problems are treacherous — many parameter "
              "sets fit equally well, tiny data noise swings the answer, and two perfectly calibrated models "
              "can disagree violently on the exotic you actually care about. That disagreement is model risk.",
    ),
    "lwv": dict(
        nav="Libor World Valuation",
        overview="The post-2008, post-LIBOR valuation framework in nine parts: multi-curve discounting, OIS "
                 "as the discount curve, tenor basis, risk-free reference rates (SOFR, €STR, SONIA), "
                 "compounded-in-arrears coupons and the fallback machinery of the LIBOR transition.",
        maths=[
            ("OIS discounting", r"$$V_t = \mathbb{E}^{\mathbb{Q}}\!\left[ e^{-\int_t^T r^{\text{OIS}}_s\, ds}\, V_T \right]$$"),
            ("Forward rate under the T-forward measure", r"$$F(t;T_1,T_2) = \mathbb{E}^{T_2}\!\left[ L(T_1;T_1,T_2)\,\middle|\,\mathcal{F}_t \right]$$"),
            ("Compounded RFR coupon", r"$$R = \frac{1}{\delta}\left( \prod_{i} \left(1 + \delta_i\, r_i\right) - 1 \right)$$"),
        ],
        plain="Before 2008 one curve did everything; the crisis broke that symmetry. Cash flows are now "
              "projected off one curve and discounted off another (OIS), each LIBOR tenor grew its own basis, "
              "and the transition to overnight risk-free rates rebuilt the plumbing of every swap on earth.",
    ),
    "bgm": dict(
        nav="BGM / Libor Market Model",
        overview="The Brace-Gatarek-Musiela (Libor Market Model): modelling the observable forward Libor "
                 "rates directly, lognormal dynamics consistent with Black's caplet formula, measure changes "
                 "between forward measures, and the drift corrections needed for joint simulation.",
        maths=[
            ("Forward Libor under its own measure", r"$$dF_k(t) = \sigma_k(t)\, F_k(t)\, dW^{k+1}_t \qquad \text{(driftless martingale)}$$"),
            ("Drift under the spot measure", r"$$dF_k = \sigma_k F_k \left( \sum_{j=\beta(t)}^{k} \frac{\delta_j F_j\, \rho_{jk}\, \sigma_j}{1 + \delta_j F_j} \right) dt + \sigma_k F_k\, dW_t$$"),
            ("Black caplet price", r"$$\text{Cpl} = \delta\, Z(0,T_{k+1}) \left[ F_k \Phi(d_1) - K \Phi(d_2) \right]$$"),
        ],
        plain="Short-rate models drive the curve from an invisible variable; BGM models what the market "
              "actually quotes — the strip of forward rates. Each forward is a fair game under its own "
              "numeraire; the price of simulating them together is a drift correction linking every rate "
              "to its neighbours.",
    ),
    "strm": dict(
        nav="Structural Models",
        overview="Credit risk from the balance sheet up: Merton's insight that equity is a call option on "
                 "the firm's assets, distance to default, first-passage extensions (Black-Cox), and what "
                 "structural models say about credit spreads.",
        maths=[
            ("Equity as a call on firm assets", r"$$E_0 = A_0 \Phi(d_1) - D e^{-rT} \Phi(d_2)$$"),
            ("Distance to default", r"$$DD = \frac{\ln(A_0/D) + (\mu - \tfrac{1}{2}\sigma_A^2)T}{\sigma_A \sqrt{T}}$$"),
            ("Credit spread", r"$$s(T) = -\frac{1}{T}\ln\frac{P(0,T)}{D\,Z(0,T)} \;>\; 0$$"),
        ],
        plain="A leveraged firm's shareholders hold a call option: if assets end above the debt, they keep "
              "the difference; if not, they walk away. Default is the option expiring worthless — so option "
              "pricing machinery prices default risk, mapping balance-sheet volatility into credit spreads.",
    ),
    "acm": dict(
        nav="Credit Modelling (Albanese)",
        presenter="Claudio Albanese (2007)",
        overview="A four-lecture 2007 series on credit modelling: default intensities and survival "
                 "probabilities, rating transition dynamics, CDS pricing, and the correlation modelling "
                 "that underpins portfolio credit derivatives.",
        maths=[
            ("Survival probability", r"$$\mathbb{Q}(\tau > t) = \exp\!\left(-\int_0^t \lambda_s\, ds\right)$$"),
            ("CDS par spread", r"$$s = \frac{(1-R)\int_0^T Z(0,t)\, dPD(t)}{\sum_i \delta_i\, Z(0,t_i)\, \mathbb{Q}(\tau > t_i)}$$"),
            ("Rating transition generator", r"$$P(t) = e^{\Lambda t}, \qquad \Lambda = \text{generator matrix of rating migrations}$$"),
        ],
        plain="Reduced-form credit treats default like a lightbulb failing: it can pop at any instant with "
              "intensity λ. Survival curves, CDS spreads and rating migrations all become statements about "
              "that hazard rate — calibrated from market spreads rather than balance sheets.",
    ),
    "fim": dict(
        nav="Fixed Income Modelling",
        overview="Four lectures on modern fixed income modelling built around stochastic monetary policy "
                 "models — central bank target rates that move in discrete steps — and their application to "
                 "callable CMS spread range accruals and other complex structured notes.",
        maths=[
            ("Policy-rate jump dynamics", r"$$r_t = r_0 + \sum_{i: t_i \le t} J_i, \qquad J_i \in \{-0.25\%, 0, +0.25\%\}$$"),
            ("CMS spread range accrual coupon", r"$$C = Q \cdot \frac{\#\{ \text{days}: L \le \text{CMS}_{10} - \text{CMS}_2 \le U \}}{N}$$"),
            ("Convexity adjustment (CMS)", r"$$\mathbb{E}^{T}[S_T] \approx S_0 + \text{conv. adj.} \propto S_0\,\sigma_S^2\, T$$"),
        ],
        plain="Central banks don't diffuse — they jump in 25bp steps at scheduled meetings. Modelling the "
              "policy rate as a jump process fits reality better than a diffusion, and matters enormously "
              "for exotic notes whose coupons switch on and off as rates drift through a range.",
    ),
    "mcam": dict(
        nav="MC & American Options",
        overview="Monte Carlo meets early exercise: why naive simulation cannot price American options, and "
                 "the Longstaff-Schwartz least-squares regression method for estimating continuation values "
                 "and exercise boundaries from simulated paths.",
        maths=[
            ("Optimal stopping value", r"$$V_0 = \sup_{\tau \le T}\; \mathbb{E}^{\mathbb{Q}}\!\left[ e^{-r\tau}\, \Pi(S_\tau) \right]$$"),
            ("LSM continuation value", r"$$\hat{C}(S) = \sum_{j=1}^{M} \beta_j\, \phi_j(S) \quad\text{(regression on basis functions)}$$"),
            ("Exercise rule", r"$$\text{exercise at } t_i \iff \Pi(S_{t_i}) > \hat{C}(S_{t_i})$$"),
        ],
        plain="An American option is a chain of should-I-stay-or-should-I-go decisions. Simulation runs "
              "forward but the decision needs the future — Longstaff-Schwartz squares the circle by "
              "regressing realized payoffs on today's state, giving a cheap estimate of what waiting is worth.",
    ),
    "nf": dict(
        nav="Northfield Risk Series",
        presenter="Dan diBartolomeo",
        overview="A ten-part practitioner series on risk models in asset management: factor risk models, "
                 "conditional/regime risk estimation, interest-rate and credit risk, hedge funds and illiquid "
                 "assets, higher moments, and the decomposition and reporting of portfolio risk.",
        maths=[
            ("Linear factor model", r"$$R = B f + \varepsilon$$"),
            ("Portfolio variance", r"$$\sigma_p^2 = w^\top \!\left( B \Sigma_f B^\top + D \right) w$$"),
            ("Cornish-Fisher (higher moments)", r"$$z_{CF} = z + \tfrac{1}{6}(z^2 - 1)\,S + \tfrac{1}{24}(z^3 - 3z)\,K - \tfrac{1}{36}(2z^3 - 5z)\,S^2$$"),
        ],
        plain="You cannot estimate a 500×500 covariance matrix from a year of data — factor models compress "
              "the problem to a handful of drivers plus stock-specific noise. The series shows how that one "
              "idea powers everything from index tracking to hedge fund risk and tail-risk reporting.",
    ),
}

# ------------------------------------------------------------- stand-alone talks
STANDALONE = {
    "talk-stochastic-calculus-for-quant-finance": dict(
        maths=[
            ("Brownian motion properties", r"$$W_0 = 0, \quad W_t - W_s \sim N(0,\, t-s), \quad \text{independent increments}$$"),
            ("Quadratic variation", r"$$(dW_t)^2 = dt$$"),
            ("Itô's Lemma", r"$$dF = \left( \frac{\partial F}{\partial t} + \tfrac{1}{2}\sigma^2 S^2 \frac{\partial^2 F}{\partial S^2} + \mu S \frac{\partial F}{\partial S} \right) dt + \sigma S \frac{\partial F}{\partial S}\, dW$$"),
        ],
        plain="Brownian paths are so rough that ordinary calculus fails on them — the square of a small "
              "step is not negligible. Itô's correction term captures exactly that, and it is where the "
              "half-sigma-squared in every pricing formula comes from.",
    ),
    "talk-markov-chain-monte-carlo-methods-a-beginners": dict(
        maths=[
            ("Target via detailed balance", r"$$\pi(x)\, P(x \to y) = \pi(y)\, P(y \to x)$$"),
            ("Metropolis-Hastings acceptance", r"$$\alpha = \min\!\left(1,\; \frac{\pi(y)\, q(x|y)}{\pi(x)\, q(y|x)}\right)$$"),
        ],
        plain="When you cannot sample a distribution directly, build a random walk whose long-run habitat "
              "is that distribution. Metropolis-Hastings accepts or rejects proposed moves so the walk "
              "spends time in proportion to probability — Bayesian calibration runs on this engine.",
    ),
    "talk-copula-and-implementing-cdo-pricing": dict(
        maths=[
            ("Sklar's theorem", r"$$F(x_1,\dots,x_n) = C\!\left(F_1(x_1),\dots,F_n(x_n)\right)$$"),
            ("Gaussian copula default times", r"$$\tau_i = F_i^{-1}\!\left(\Phi(X_i)\right), \qquad X_i = \rho\, M + \sqrt{1-\rho^2}\, Z_i$$"),
            ("Tranche loss", r"$$L_{[a,b]} = \frac{\min(L,b) - \min(L,a)}{b - a}$$"),
        ],
        plain="A copula splits a joint distribution into individual behaviours plus a pure dependence "
              "structure. CDO pricing hangs entirely on that dependence: correlation decides whether "
              "defaults arrive alone (hurting equity tranches) or together (reaching the senior ones).",
    ),
    "talk-ica-and-hedge-fund-returns-part-01": dict(
        maths=[
            ("ICA mixing model", r"$$x = A s, \qquad s = \text{statistically independent sources}$$"),
            ("Non-Gaussianity objective", r"$$\max_{w}\; \left| \operatorname{kurt}(w^\top x) \right| \quad\text{(or negentropy)}$$"),
        ],
        plain="PCA finds uncorrelated combinations; ICA demands full statistical independence, exploiting "
              "the non-Gaussian, fat-tailed nature of returns. Applied to hedge funds it tries to unmix "
              "reported returns into the true underlying strategies.",
    ),
    "talk-cqf-alumni-hb-finite-difference-model-part": dict(
        maths=[
            ("Explicit scheme", r"$$V_i^{m} = V_i^{m+1} + \Delta t \left( \tfrac{1}{2}\sigma^2 S_i^2 \Delta_{SS} + r S_i \Delta_S - r \right) V^{m+1}$$"),
            ("Stability constraint", r"$$\Delta t \le \frac{\Delta S^2}{\sigma^2 S_{\max}^2}$$"),
        ],
        plain="A finite-difference pricer walks the option value backwards from expiry across a grid of "
              "prices and dates. Explicit schemes are simple but only stable for small time steps; the "
              "walkthrough builds one from scratch.",
    ),
    "talk-principles-and-tools-of-quantitative-finance": dict(
        maths=[
            ("The three pillars", r"$$\text{no-arbitrage} \;+\; \text{replication} \;+\; \text{risk-neutral expectation}$$"),
        ],
        plain="A panoramic introduction to how quants think: hedging arguments remove risk, no-arbitrage "
              "fixes prices, and expectations under an adjusted probability measure compute them.",
    ),
    "talk-quants-toolbox": dict(
        maths=[
            ("The workflow", r"$$\text{model} \to \text{calibrate} \to \text{price} \to \text{hedge} \to \text{monitor}$$"),
        ],
        plain="A guided tour of the day-to-day toolkit — stochastic calculus, PDEs, statistics, numerical "
              "methods and code — and how the pieces fit together on a working desk.",
    ),
    "talk-manging-smile-risk-fixed-income-derivatives": dict(
        maths=[
            ("SABR dynamics", r"$$dF = \alpha F^{\beta} dW_1, \quad d\alpha = \nu \alpha\, dW_2, \quad dW_1 dW_2 = \rho\, dt$$"),
            ("Hagan implied vol (ATM)", r"$$\sigma_{\text{ATM}} \approx \frac{\alpha}{F^{1-\beta}} \left[ 1 + \left( \frac{(1-\beta)^2 \alpha^2}{24 F^{2-2\beta}} + \frac{\rho \beta \nu \alpha}{4 F^{1-\beta}} + \frac{2 - 3\rho^2}{24}\nu^2 \right) T \right]$$"),
        ],
        plain="The volatility smile is not decoration — it moves, and hedges must respect how it moves. "
              "SABR won the fixed-income desk because its parameters map cleanly onto level, skew and "
              "curvature of the smile and imply sane dynamics for all three.",
    ),
    "talk-real-options": dict(
        maths=[
            ("Investment as a perpetual call", r"$$V(P) = A P^{\beta_1}, \qquad \text{invest when } P \ge P^* = \frac{\beta_1}{\beta_1 - 1}\, I$$"),
        ],
        plain="A factory you may build, a mine you may expand, a project you may abandon — all options on "
              "real assets. Option thinking explains why firms rationally wait far past the NPV break-even "
              "before committing capital.",
    ),
    "talk-high-frequency-trading": dict(
        maths=[
            ("Mid-price and microprice", r"$$m = \frac{P^{bid} + P^{ask}}{2}, \qquad m^{micro} = \frac{Q^{ask} P^{bid} + Q^{bid} P^{ask}}{Q^{bid} + Q^{ask}}$$"),
            ("Inventory-adjusted quoting (Avellaneda-Stoikov)", r"$$\delta^{\pm} = \frac{\gamma \sigma^2 (T-t)}{2} \pm \frac{1}{\gamma} \ln\!\left(1 + \frac{\gamma}{\kappa}\right)$$"),
        ],
        plain="At millisecond scale the order book is the market: queues, cancellations and adverse "
              "selection replace drift and volatility. Market making becomes an inventory-control problem "
              "— earn the spread while never holding a position the flow is about to run over.",
    ),
    "talk-high-frequency-data-analysis": dict(
        maths=[
            ("Realized variance", r"$$RV = \sum_{i} r_i^2 \;\xrightarrow{\;\delta t \to 0\;}\; \int_0^T \sigma_s^2\, ds \;+\; \text{microstructure noise bias}$$"),
            ("Signature plot", r"$$RV(\delta t) \text{ vs } \delta t \quad\text{reveals the noise/efficiency trade-off}$$"),
        ],
        plain="Tick data promises infinite precision and delivers infinite headaches: bid-ask bounce, "
              "irregular timestamps and noise that grows as you sample faster. Realized-volatility "
              "estimators thread the needle between statistical efficiency and microstructure bias.",
    ),
    "talk-recent-developments-in-credit-risk": dict(
        maths=[
            ("Portfolio loss (one-factor)", r"$$\mathbb{Q}(L > x) \approx \Phi\!\left( \frac{\sqrt{1-\rho}\,\Phi^{-1}(x) - \Phi^{-1}(PD)}{\sqrt{\rho}} \right)$$"),
        ],
        plain="A survey of where credit modelling moved after the crisis: counterparty risk and CVA, "
              "wrong-way risk, central clearing, and the shift from pricing exotic correlation products "
              "to managing the credit risk embedded in every derivative book.",
    ),
    "talk-recent-developments-in-deep-learning-in": dict(
        maths=[
            ("Universal approximation", r"$$f(x) \approx \sum_{i} c_i\, \sigma(w_i^\top x + b_i)$$"),
            ("Deep hedging objective", r"$$\min_{\theta}\; \rho\!\left( \Pi_T - \sum_t \delta_\theta(S_t)\, \Delta S_t \right)$$"),
        ],
        plain="Neural networks enter the pricing stack twice: as fast surrogates for slow models "
              "(calibration in milliseconds) and as direct policy learners (deep hedging), where the "
              "network learns to hedge under frictions no closed form can handle.",
    ),
}

# ---------------------------------------------------------------- template
PAGE = """<div id="view-{slug}" style="display: none; font-family: var(--font-family-sans);">
    <header style="margin-bottom: 2rem;">
        <p style="color: var(--accent); font-weight: 700; font-size: 0.8rem; text-transform: uppercase; margin: 0;">CQF Talks &bull; Legacy Lecture Series{crumb}</p>
        <h1 style="margin: 0; font-size: 2rem; font-weight: 800; border-bottom: none; padding-bottom: 0;">{title}</h1>
        <p style="color: var(--text-muted); margin-top: 0.5rem;">{subtitle}</p>
    </header>

    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 2rem; align-items: stretch; margin-bottom: 2rem;">
        <div class="card" style="margin-bottom: 0; padding: 1.5rem;">
            <h3 style="margin-top: 0;">{left_heading}</h3>
            <p style="line-height: 1.7; margin-bottom: 0;">{overview}</p>
        </div>
        <div class="card" style="margin-bottom: 0; background: #fffbeb; border-left: 4px solid #f59e0b; border-radius: 8px; padding: 1.5rem;">
            <h3 style="margin-top: 0; color: #b45309; font-family: 'Inter', sans-serif; font-weight: 700;">Plain English Notes</h3>
            <p style="font-family: 'Inter', sans-serif; line-height: 1.7; color: #451a03; margin-bottom: 0;"><strong>The Big Picture:</strong> {plain}</p>
        </div>
    </div>

    <div class="card" style="margin-bottom: 2rem;">
        <h3 style="margin-top: 0;">Core Mathematics</h3>
        {maths_rows}
    </div>

    {navrow}

    <div class="card" style="border-left: 4px solid var(--accent); background: var(--bg-subtle);">
        <h3 style="margin-top:0;">Per-Lecture Notes Coming Soon</h3>
        <p style="margin-bottom:0; color: var(--text-secondary);">The cards above cover the {scope}. Detailed notes, derivations and interactive demos for this specific video will be added here.</p>
    </div>
</div>
"""

MATH_ROW = """<div style="padding: 0.75rem 0; border-bottom: 1px solid var(--card-border);">
            <div style="font-weight: 600; font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 0.25rem;">{label}</div>
            <div style="overflow-x: auto;">{formula}</div>
        </div>"""

NAV_BTN = ('<a href="#{slug}" onclick="showSection(\'{slug}\')" style="text-decoration: none; color: var(--accent); '
           'border: 1px solid var(--card-border); border-radius: 8px; padding: 0.5rem 1rem; font-size: 0.85rem; '
           'font-weight: 600; background: var(--metric-bg);">{label}</a>')


def build_page(slug, title, subtitle, crumb, left_heading, overview, plain, maths, navrow, scope):
    rows = "\n        ".join(
        MATH_ROW.format(label=H.escape(lbl), formula=f) for lbl, f in maths
    )
    return PAGE.format(slug=slug, title=H.escape(title), subtitle=H.escape(subtitle),
                       crumb=crumb, left_heading=left_heading, overview=H.escape(overview),
                       plain=H.escape(plain), maths_rows=rows, navrow=navrow, scope=scope)


def main():
    catalog = json.load(open(CATALOG, encoding="utf-8"))
    legacy = [t for t in catalog if t["cat"] == "legacy"]

    series = defaultdict(list)   # abbr -> [talks in order]
    standalone = []
    for t in legacy:
        m = re.match(r"talk-([a-z]+)-p(\d+)$", t["slug"])
        if m and m.group(1) in S:
            series[m.group(1)].append(t)
        else:
            standalone.append(t)

    n_pages = 0
    # ---- series pages
    for abbr, talks in series.items():
        talks.sort(key=lambda t: t["slug"])
        info = S[abbr]
        total = len(talks)
        for i, t in enumerate(talks):
            part_label = t["title"].split(": ", 1)[1] if ": " in t["title"] else t["title"]
            series_name = t["title"].split(": ", 1)[0]
            btns = []
            if i > 0:
                btns.append(NAV_BTN.format(slug=talks[i-1]["slug"], label="&larr; Previous part"))
            btns.append(NAV_BTN.format(slug="talks-portal", label="All talks"))
            if i < total - 1:
                btns.append(NAV_BTN.format(slug=talks[i+1]["slug"], label="Next part &rarr;"))
            navrow = ('<div style="display: flex; gap: 0.75rem; flex-wrap: wrap; margin-bottom: 2rem;">'
                      + "".join(btns) + "</div>")
            subtitle = info.get("presenter", "")
            subtitle = (subtitle + " — " if subtitle else "") + f"{part_label} of {total} in this series"
            page = build_page(
                slug=t["slug"], title=series_name, subtitle=subtitle,
                crumb=" &bull; " + H.escape(info["nav"]) + f" &bull; {part_label}",
                left_heading="Series Overview", overview=info["overview"], plain=info["plain"],
                maths=info["maths"], navrow=navrow, scope="series as a whole",
            )
            open(os.path.join(SECTIONS, f"view-{t['slug']}.html"), "w", encoding="utf-8").write(page)
            n_pages += 1

    # ---- stand-alone pages
    for t in standalone:
        extra = STANDALONE.get(t["slug"])
        if not extra:
            print("  (no content defined, leaving scaffold):", t["slug"])
            continue
        navrow = ('<div style="display: flex; gap: 0.75rem; flex-wrap: wrap; margin-bottom: 2rem;">'
                  + NAV_BTN.format(slug="talks-portal", label="All talks") + "</div>")
        page = build_page(
            slug=t["slug"], title=t["title"],
            subtitle=(t.get("presenter") or "Stand-alone legacy lecture"),
            crumb="", left_heading="What This Lecture Covers",
            overview=extra.get("overview", extra["plain"]), plain=extra["plain"],
            maths=extra["maths"], navrow=navrow, scope="lecture's core ideas",
        )
        open(os.path.join(SECTIONS, f"view-{t['slug']}.html"), "w", encoding="utf-8").write(page)
        n_pages += 1

    # ---- sidebar: nest legacy nav by series
    idx = open(IDX, encoding="utf-8").read()
    m = re.search(
        r'(<summary class="nav-section-title">Legacy Lecture Series</summary>\s*<div class="nav-group">)(.*?)(<!-- TALKS_NAV:legacy -->)',
        idx, re.S)
    assert m, "legacy nav group not found"

    order = ["mmnm", "bsmw", "mart", "pmir", "rba", "mrc", "lwv", "bgm", "strm", "acm", "fim", "mcam", "nf"]
    parts_nav = []
    for abbr in order:
        if abbr not in series:
            continue
        info = S[abbr]
        links = "\n".join(
            f'            <a class="nav-item" href="#{t["slug"]}" onclick="showSection(\'{t["slug"]}\')">'
            f'{H.escape(t["title"].split(": ", 1)[1] if ": " in t["title"] else t["title"])}</a>'
            for t in series[abbr]
        )
        parts_nav.append(
            '        <details class="nav-level-2">\n'
            f'        <summary class="nav-section-title">{H.escape(info["nav"])}</summary>\n'
            '        <div class="nav-group">\n'
            f"{links}\n"
            "        </div>\n"
            "        </details>"
        )
    solo_links = "\n".join(
        f'        <a class="nav-item" href="#{t["slug"]}" onclick="showSection(\'{t["slug"]}\')">{H.escape(t["title"])}</a>'
        for t in standalone
    )
    new_inner = "\n" + "\n".join(parts_nav) + "\n" + solo_links + "\n        "
    idx = idx[: m.start(2)] + new_inner + idx[m.end(2):]
    open(IDX, "w", encoding="utf-8").write(idx)

    print(f"enriched {n_pages} pages; legacy nav nested into {len(parts_nav)} series + {len(standalone)} stand-alone")


if __name__ == "__main__":
    main()

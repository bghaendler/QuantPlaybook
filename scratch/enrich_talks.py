#!/usr/bin/env python3
"""Generic CQF Talks enrichment engine.

Regenerates view-talk-<slug>.html for every slug present in CONTENT with real
notes: overview, core mathematics (MathJax), plain-English intuition, and a
link back to the Talks Portal. Add entries per category and re-run (idempotent).

Usage: python3 scratch/enrich_talks.py [category-key ...]   (default: all keys present)
"""
import html as H
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECTIONS = os.path.join(ROOT, "app", "templates", "sections")
CATALOG = os.path.join(ROOT, "scratch", "talks_catalog.json")

CAT_LABELS = {
    "legacy": "Legacy Lecture Series", "volatility": "Volatility & Smile",
    "options": "Options & BSM", "rates": "Rates & Fixed Income",
    "credit": "Credit, XVA & Structured", "portfolio": "Portfolio & Allocation",
    "kelly": "Kelly & Ziemba", "ml-ai": "Machine Learning & AI",
    "nlp": "NLP, Sentiment & Alt Data", "quantum": "Quantum Computing",
    "crypto": "Crypto & DeFi", "commodities": "Commodities & Energy",
    "microstructure": "Microstructure & Algo Trading", "risk": "Risk Management & Regulation",
    "esg": "ESG & Climate", "dev": "Numerical Methods, HPC & Dev",
    "careers": "Careers & Industry", "history": "History & Philosophy",
}

# ============================================================================
# CONTENT — keyed by slug. Fields: overview, plain, maths=[(label, latex)...]
# ============================================================================
CONTENT = {

# ---------------------------------------------------------------- volatility
"talk-rough-volatility-an-overview": dict(
    overview="Why volatility is 'rough': empirical log-volatility increments scale like fractional "
             "Brownian motion with Hurst exponent H ≈ 0.1, far below the H = 1/2 of standard models. "
             "Covers the RFSV model, its microstructural foundation, and the term structure of the "
             "ATM implied-volatility skew.",
    maths=[
        ("Fractional Brownian motion scaling", r"$$\mathbb{E}\left[ \left| \log\sigma_{t+\Delta} - \log\sigma_t \right|^2 \right] \;\propto\; \Delta^{2H}, \qquad H \approx 0.1$$"),
        ("RFSV volatility dynamics", r"$$\sigma_t = \sigma\, \exp\!\left( \nu\, W^H_t \right), \qquad W^H = \text{fBM with Hurst } H$$"),
        ("ATM skew term structure", r"$$\psi(\tau) := \left| \frac{\partial \sigma_{BS}}{\partial k} \right|_{k=0} \;\sim\; \tau^{\,H - 1/2}$$"),
    ],
    plain="Volatility wiggles far more violently at short timescales than diffusion models allow. "
          "Making it 'rough' — fractal, with memory — reproduces two stubborn facts at once: the "
          "statistics of realized volatility and the explosive short-dated skew in option markets.",
),
"talk-rough-volatility-with-python": dict(
    overview="Jim Gatheral's hands-on companion to rough volatility: estimating the Hurst exponent "
             "from realized variance data, forecasting variance under RFSV, and pricing claims with "
             "the rough Bergomi (rBergomi) model in Python.",
    maths=[
        ("rBergomi variance process", r"$$v_t = \xi_0(t)\, \mathcal{E}\!\left( \eta \sqrt{2H} \int_0^t (t-s)^{H-1/2}\, dW_s \right)$$"),
        ("Variance forecast (RFSV)", r"$$\mathbb{E}[v_{t+\Delta} \,|\, \mathcal{F}_t] = \exp\!\left( \mathbb{E}[\log v_{t+\Delta} | \mathcal{F}_t] + 2\nu^2 c\, \Delta^{2H} \right)$$"),
    ],
    plain="The notebook version of the rough revolution: measure roughness yourself from public data, "
          "then watch a two-parameter model fit whole volatility surfaces that took older models "
          "a dozen parameters to approximate.",
),
"talk-the-sabr-short-maturity-expansion-is": dict(
    overview="A careful look at the mathematical status of the celebrated Hagan SABR smile formula: "
             "the short-maturity expansion is asymptotic rather than convergent, with practical "
             "consequences for when and how far the formula can be trusted.",
    maths=[
        ("SABR dynamics", r"$$dF = \alpha F^{\beta}\, dW_1, \qquad d\alpha = \nu\, \alpha\, dW_2, \qquad dW_1\, dW_2 = \rho\, dt$$"),
        ("Asymptotic (not convergent) series", r"$$\sigma_{BS}(K,T) \sim \sigma_0(K)\left( 1 + \sigma_1(K)\, T + \sigma_2(K)\, T^2 + \cdots \right), \quad T \to 0$$"),
    ],
    plain="Asymptotic series are excellent servants and terrible masters: the first terms are superbly "
          "accurate for short maturities, but adding more terms eventually makes things worse, and at "
          "long maturities or extreme strikes the formula quietly leaves its domain of validity.",
),
"talk-cross-currency-options-and-the-correlated": dict(
    overview="If EURUSD and USDJPY each follow SABR dynamics, what does that imply for EURJPY? Under "
             "mild correlation assumptions the cross rate admits a consistent SABR-type smile, giving "
             "a no-arbitrage way to mark illiquid cross smiles from liquid ones.",
    maths=[
        ("Cross-rate identity", r"$$S^{EURJPY}_t = S^{EURUSD}_t \cdot S^{USDJPY}_t$$"),
        ("Cross volatility (lognormal core)", r"$$\sigma_X^2 = \sigma_1^2 + \sigma_2^2 + 2\rho\, \sigma_1 \sigma_2$$"),
    ],
    plain="Currency triangles must close: the euro-yen smile cannot be marked independently of the "
          "dollar legs without creating arbitrage. The talk turns that constraint into a constructive "
          "recipe for the cross smile.",
),
"talk-computing-skew-stickiness": dict(
    overview="Gatheral on the skew-stickiness ratio (SSR): how much the ATM implied volatility moves "
             "when spot moves, relative to the skew. Introduces the 'diamond' functional calculus and "
             "the Bergomi-Guillon expansion, and compares model SSR to empirical estimates.",
    maths=[
        ("Skew-stickiness ratio", r"$$\text{SSR} = \frac{1}{\psi(\tau)} \frac{d\, \sigma_{ATM}}{d \ln S}$$"),
        ("Short-maturity limits", r"$$\text{SSR} \xrightarrow{\tau \to 0} 2 \quad \text{(stochastic vol)}, \qquad \text{SSR} = 1 \;\text{(sticky-strike)}$$"),
    ],
    plain="When the market drops, does the smile slide with spot, stay pinned to strikes, or something "
          "in between? The SSR is that 'something in between' made precise — and models disagree with "
          "the data about it, which matters for every delta hedge on the desk.",
),
"talk-some-things-i-have-learned-about-volatility": dict(
    overview="Wilmott's keynote distillation of decades around volatility: why volatility matters, how "
             "to measure it honestly, how hedged option positions actually make money, and what a "
             "'good' volatility model would even look like.",
    maths=[
        ("Hedged P&L driver", r"$$d\Pi \;=\; \tfrac{1}{2}\left( \sigma_{\text{real}}^2 - \sigma_{\text{impl}}^2 \right) S^2 \Gamma\, dt$$"),
        ("Which delta? Actual vs implied vol", r"$$\Delta_{\sigma_{\text{impl}}} \;\text{(smooth P\&L)} \quad\text{vs}\quad \Delta_{\sigma_{\text{real}}} \;\text{(bigger, noisier P\&L)}$$"),
    ],
    plain="Buy options when realized volatility will beat the implied you paid; then your profit "
          "arrives through gamma, day by day. Which volatility you plug into your delta changes the "
          "journey (smooth vs wild P&L) more than the destination.",
),
"talk-some-more-things-i-have-learned-about": dict(
    overview="The sequel keynote: volatility sensitivity and vega-gamma trade-offs, pricing under "
             "uncertain volatility, and what dynamic hedging does and does not remove.",
    maths=[
        ("Uncertain volatility bounds", r"$$\sigma \in [\sigma^-, \sigma^+] \;\Rightarrow\; V^{\pm} \text{ solve BSB: } V_t + \tfrac{1}{2}\hat{\sigma}(\Gamma)^2 S^2 V_{SS} + rSV_S - rV = 0$$"),
        ("Worst-case vol selection", r"$$\hat{\sigma}(\Gamma) = \sigma^+ \,\mathbb{1}_{\Gamma < 0} + \sigma^- \,\mathbb{1}_{\Gamma > 0} \quad \text{(short side)}$$"),
    ],
    plain="If you only know volatility lives in a band, you can still price: assume the worst volatility "
          "wherever your gamma hurts you. The result is a bid-ask spread produced by mathematics rather "
          "than by markets.",
),
"talk-volatility-and-risk-with-dr-paul-wilmott": dict(
    overview="A conversation between Paul Wilmott and Dan Tudball on volatility models in the age of "
             "machine learning: what classical models still explain, where data-driven methods genuinely "
             "help, and whether human understanding can be replaced.",
    maths=[
        ("The spectrum under discussion", r"$$\text{GARCH} \;\to\; \text{stochastic vol} \;\to\; \text{local vol} \;\to\; \text{ML forecasts}$$"),
    ],
    plain="A models-versus-machines conversation: ML can beat classical volatility forecasts on data it "
          "has seen, but a desk still needs to know why a hedge failed — and 'the network said so' has "
          "never calmed a risk committee.",
),
"talk-time-changes-fourier-transforms-and-the": dict(
    overview="A model built on time-changed Lévy processes attacking the 'joint calibration problem': "
             "fitting the S&P 500 smile, the VIX smile and VIX futures simultaneously, priced "
             "efficiently by Fourier transform methods.",
    maths=[
        ("Time-changed Lévy process", r"$$S_t = S_0\, \frac{e^{X_{\tau_t}}}{\mathbb{E}[e^{X_{\tau_t}}]}, \qquad \tau_t = \int_0^t v_s\, ds$$"),
        ("Carr-Madan Fourier pricing", r"$$C(K) = \frac{e^{-\alpha k}}{\pi} \int_0^{\infty} e^{-iuk}\, \frac{\phi_T(u - (\alpha+1)i)}{\alpha^2 + \alpha - u^2 + i(2\alpha+1)u}\, du$$"),
    ],
    plain="The S&P options market and the VIX options market are two windows onto the same volatility — "
          "yet most models can't face both at once. Changing the speed of time with a stochastic clock "
          "gives enough flexibility to satisfy them jointly.",
),
"talk-the-term-structure-of-implied-correlations": dict(
    overview="A joint model for the S&P 500 and VIX designed to extract a forward-looking, "
             "market-implied term structure of the correlation between equity returns and volatility "
             "changes — the quantity behind the skew.",
    maths=[
        ("Implied equity-vol correlation", r"$$\rho_{S,\sigma}(T) = \frac{\operatorname{Cov}(r_{S}, \Delta \text{VIX})}{\operatorname{sd}(r_S)\, \operatorname{sd}(\Delta \text{VIX})} \quad\text{implied from joint option prices}$$"),
    ],
    plain="Realized correlation between the index and its volatility is history; option markets contain "
          "the market's forecast of it. Extracting that forecast maturity-by-maturity turns the skew "
          "into a readable term structure of fear.",
),
"talk-spx-vix-and-scale-invariant-lsv": dict(
    overview="Adil Reghai applies the Buckingham Pi theorem to link time-series and derivatives "
             "modelling: scale-invariant local-stochastic volatility for the S&P 500 and VIX, enabling "
             "consistent derivative pricing and trading strategies.",
    maths=[
        ("Scale invariance", r"$$V(\lambda S, \lambda K) = \lambda\, V(S, K) \;\Rightarrow\; \sigma(S,t) = \sigma(S/S_0)$$"),
        ("LSV dynamics", r"$$dS = \sigma_{loc}(S,t)\, \sqrt{v_t}\, S\, dW, \qquad dv = \kappa(\theta - v)\,dt + \xi\sqrt{v}\, dZ$$"),
    ],
    plain="Dimensional analysis — the physicist's trick of cancelling units — prunes the space of "
          "reasonable volatility models dramatically. What survives connects the historical behaviour "
          "of the index to the surface you should price derivatives on.",
),
"talk-modeling-volatility-risk-premia": dict(
    overview="Artur Sepp combines the risk-neutral (Q) and statistical (P) measures to model the "
             "volatility risk premium and turn it into systematic trading strategies, with applications "
             "to equity index and Bitcoin options.",
    maths=[
        ("Volatility risk premium", r"$$\text{VRP} = \sigma_{\text{impl}}^2 - \mathbb{E}^{\mathbb{P}}[\sigma_{\text{real}}^2] \;>\; 0 \text{ on average}$$"),
        ("Delta-hedged straddle P&L", r"$$\text{P\&L} \approx \int_0^T \tfrac{1}{2} S_t^2 \Gamma_t \left( \sigma_{\text{real}}^2 - \sigma_{\text{impl}}^2 \right) dt$$"),
    ],
    plain="Options are insurance, and insurance sells above actuarial value. Systematically selling "
          "that overpricing — while surviving the occasional hurricane — is the volatility risk "
          "premium business, and it works in crypto too.",
),
"talk-modeling-the-dynamics-of-the-entire-implied": dict(
    overview="Instead of forecasting single vols, evolve the parameters of a stochastic-volatility "
             "model with an explicit smile formula using deep learning — producing arbitrage-aware, "
             "multi-step-ahead forecasts of the entire implied volatility surface.",
    maths=[
        ("Surface parameterization", r"$$\sigma_{BS}(k,\tau) = f\!\left(k, \tau;\ \theta_t\right), \qquad \theta_{t+1} = \text{NN}(\theta_t, \text{features}_t)$$"),
    ],
    plain="A volatility surface is thousands of numbers that move together; a good parametric model "
          "compresses it to a handful. Forecast the handful with a neural network and you forecast the "
          "whole surface without ever emitting an arbitrageable shape.",
),
"talk-reconciling-p-and-q-calibration-the-discrete": dict(
    overview="The discrete-time 4-factor path-dependent volatility model (Guyon-style): volatility as "
             "a deterministic function of weighted past returns and squared returns, jointly fitting "
             "the statistical dynamics of the index (P) and the SPX/VIX option surfaces (Q).",
    maths=[
        ("Path-dependent volatility", r"$$\sigma_t = \beta_0 + \beta_1 R_{1,t} + \beta_2 \sqrt{R_{2,t}}$$"),
        ("Trend and activity features", r"$$R_{1,t} = \sum_{j} K_1(t - t_j)\, r_{t_j}, \qquad R_{2,t} = \sum_{j} K_2(t - t_j)\, r_{t_j}^2$$"),
    ],
    plain="Markets remember: volatility today is a function of the recent path — downtrends raise it, "
          "calm raises it slowly back down. Writing volatility as an explicit function of that path "
          "fits history and option markets with the same small set of parameters, something 'pure' "
          "stochastic-vol models struggle to do.",
),
"talk-mixed-local-volatility-models-for-fx": dict(
    overview="Uwe Wystup on Mixed Local Volatility for FX: blending local-volatility dynamics with a "
             "mixing weight toward stochastic behaviour, so first-generation exotics (barriers, "
             "touches) price between the LV and SV extremes where the market actually trades.",
    maths=[
        ("MLV as a mixture", r"$$\sigma^2_{\text{MLV}}(S,t) = m\, \sigma^2_{\text{SV-like}} + (1-m)\, \sigma^2_{\text{LV}}, \qquad m \in [0,1]$$"),
    ],
    plain="Pure local vol underprices touch options, pure stochastic vol overprices them; the market "
          "sits stubbornly in between. A single mixing dial calibrated to touches lets one model span "
          "the whole product range without exotic-by-exotic fudges.",
),
"talk-qi-2021-apac-practical-demonstration-of-slv": dict(
    overview="Live comparison of local volatility, stochastic volatility, SLV and MLV models on FX "
             "vanillas and first-generation exotics, including how the mixing fraction is calibrated "
             "in practice.",
    maths=[
        ("SLV dynamics", r"$$dS = \mu S\, dt + L(S,t)\, \sqrt{v_t}\, S\, dW, \qquad L \text{ calibrated so vanillas reprice}$$"),
    ],
    plain="Same vanilla surface, four different models, four different barrier prices — a live "
          "demonstration that calibration to vanillas leaves exotic prices badly underdetermined, and "
          "how desks pin them down with market data on touches.",
),
"talk-a-new-interest-rate-smile-model": dict(
    overview="Dong Qu presents an interest-rate smile model permitting Dupire-type local-volatility "
             "stripping in the rates world — bringing the equity local-vol toolkit to caps, floors and "
             "swaptions.",
    maths=[
        ("Dupire-type stripping for rates", r"$$\sigma_{loc}^2(K,T) = \frac{\partial_T C + \text{drift terms}}{\tfrac{1}{2} K^2\, \partial_{KK} C}$$"),
    ],
    plain="Equity quants have long enjoyed a unique local-vol surface recovered directly from option "
          "prices; rates quants had no clean equivalent. This model restores that luxury, giving an "
          "IR smile that reprices the market by construction.",
),
"talk-libor-smile-model-with-local-volatility": dict(
    overview="The simplest interest-rate smile model: LIBOR local volatility. Construction, smile "
             "calibration examples and pricing with the smile for caps and swaptions.",
    maths=[
        ("Local-vol forward Libor", r"$$dF_k(t) = \sigma_{loc}(F_k, t)\, F_k(t)\, dW^{k+1}_t$$"),
    ],
    plain="Before reaching for heavy artillery (SABR, LMM with stochastic vol), a deterministic "
          "volatility function of the rate level already captures most of the observed smile — and "
          "keeps calibration transparent.",
),
"talk-the-different-truths-of-ir-volatility": dict(
    overview="The 'SME rates vol status quo': normal (Bachelier) versus lognormal (Black) quoting, "
             "negative rates, shifted models, and why Black's formula refuses to die despite decades "
             "of predicted obsolescence.",
    maths=[
        ("Black vs Bachelier caplet vol", r"$$\sigma_N \;\approx\; \sigma_{LN} \cdot F \quad\text{(ATM, small vols)}$$"),
        ("Shifted lognormal for negative rates", r"$$d(F + s) = \sigma\, (F + s)\, dW, \qquad s > |F_{\min}|$$"),
    ],
    plain="When EUR rates went negative, lognormal vol quotes became mathematically impossible — the "
          "market shrugged, added a shift, and kept quoting. The talk maps which 'truth' (normal, "
          "lognormal, shifted) each corner of the rates market lives in and why.",
),
"talk-tensoring-volatility-calibration-the-power": dict(
    overview="Chebyshev tensors as an alternative to deep neural networks for accelerating model "
             "calibration: spectral accuracy, tensor-train compression to beat the curse of "
             "dimensionality, and guaranteed error bounds.",
    maths=[
        ("Chebyshev interpolation error", r"$$\|f - p_n\|_\infty \le C\, \rho^{-n} \quad \text{(exponential for analytic } f\text{)}$$"),
        ("Tensor-train decomposition", r"$$T(i_1,\dots,i_d) \approx G_1(i_1)\, G_2(i_2) \cdots G_d(i_d)$$"),
    ],
    plain="Neural networks are not the only way to make a slow pricer fast. Chebyshev interpolation "
          "offers the same speedups with mathematical error guarantees — you know exactly how wrong "
          "the approximation can be, which auditors and regulators tend to appreciate.",
),
"talk-a-singular-variance-gamma-expansion": dict(
    overview="Peter Jaeckel's analytical trick: approximating Black implied volatility under the "
             "Variance Gamma model via singular expansions of the gamma density, yielding fast and "
             "accurate smile formulas.",
    maths=[
        ("Variance Gamma process", r"$$X_t = \theta\, G_t + \sigma\, W_{G_t}, \qquad G_t \sim \Gamma(t/\nu, \nu)$$"),
    ],
    plain="The Variance Gamma model prices with an integral that resists closed forms; a singular "
          "expansion tames it into formulas fast enough for calibration loops, without losing the "
          "fat tails that made the model attractive.",
),
"talk-post-modern-volatility-when-abstraction": dict(
    overview="Panel discussion on 'post-modern' volatility: VIX products, volatility as a traded asset "
             "class in its own right, and what happens when the abstraction (implied volatility) "
             "starts driving the reality (the underlying market).",
    maths=[],
    plain="Volatility began as a parameter, became a product (VIX futures, ETNs), and by February 2018 "
          "('Volmageddon') the products were moving the market they were supposed to measure. The "
          "panel debates who is wagging whom.",
),
"talk-panel-discussion-the-origins-of-financial": dict(
    overview="Where does volatility come from? A panel spanning market microstructure, leverage and "
             "feedback effects, news versus endogenous dynamics, and what drives extreme changes in "
             "market volatility.",
    maths=[],
    plain="Prices move far more than fundamentals arrive — the excess is generated inside the market "
          "itself: leverage unwinding, hedging feedback, crowd dynamics. The panel maps the internal "
          "combustion engine of volatility.",
),
"talk-data-science-methods-for-volatility-objects": dict(
    overview="Treating whole volatility surfaces as data objects: functional data analysis, PCA on "
             "surfaces, and machine-learning methods for the joint dynamics of smile level, skew and "
             "term structure.",
    maths=[
        ("Surface PCA", r"$$\sigma_t(k, \tau) = \bar{\sigma}(k,\tau) + \sum_{i} s_{i,t}\, \phi_i(k, \tau)$$"),
    ],
    plain="A surface per day is a curve-valued time series. Functional PCA discovers that three shapes "
          "— level, skew, term structure — explain nearly all of it, turning surface dynamics into a "
          "tractable three-factor problem.",
),
"talk-volatility-trading-in-the-oil-market": dict(
    overview="One of the world's largest derivative markets, quantitatively under-documented: the "
             "structure of the oil options market, WTI volatility dynamics, and the behaviour of oil "
             "volatility strategies.",
    maths=[
        ("Samuelson effect", r"$$\sigma(T_{\text{contract}}) \uparrow \;\text{as expiry approaches} \quad\text{(futures vol term structure)}$$"),
    ],
    plain="Oil volatility lives by its own rules: inventory announcements, OPEC meetings and the "
          "physical delivery cycle imprint a seasonality and term structure that equity-trained "
          "intuition misreads.",
),
"talk-jump-risk-premia-in-the-presence-of": dict(
    overview="An option pricing model with clustered jumps: a bivariate Hawkes process with exponential "
             "memory drives self-exciting jump arrival, separating the premium for jump risk from the "
             "premium for jump clustering.",
    maths=[
        ("Hawkes intensity", r"$$\lambda_t = \lambda_\infty + \sum_{t_i < t} \alpha\, e^{-\beta (t - t_i)}$$"),
        ("Branching ratio", r"$$n = \alpha / \beta \;<\; 1 \quad\text{(fraction of endogenous events)}$$"),
    ],
    plain="Crashes come in bunches: one jump raises the odds of the next. Options must therefore price "
          "not just the jump, but the aftershock sequence — and the market demonstrably charges for "
          "both.",
),
"talk-why-do-stock-prices-jump-so-often": dict(
    overview="Joining a price-jump database with financial news reveals two dynamical classes of "
             "extreme moves — news-driven and self-excited — with roughly 95% of intraday jumps being "
             "endogenous rather than news-related.",
    maths=[
        ("Jump detection", r"$$|r_t| > c\, \hat{\sigma}_t \quad\text{with}\quad \hat{\sigma}_t = \text{local (intraday) volatility estimate}$$"),
    ],
    plain="Check the newswire after a violent price move and 19 times out of 20 you find nothing. "
          "Markets mostly startle themselves — liquidity evaporation and feedback, not information, "
          "cause most jumps. That inverts the standard efficient-market story of what prices react to.",
),
"talk-fast-times-slow-times-and-timescale": dict(
    overview="Quantitative strategies assume stationarity; reality delivers parameter drift. This talk "
             "develops timescale separation for financial time series — which components of the data "
             "are fast noise, which are slow drift, and what that means for strategy decay.",
    maths=[
        ("Timescale decomposition", r"$$X_t = \underbrace{\theta_t}_{\text{slow drift}} + \underbrace{\varepsilon_t}_{\text{fast noise}}, \qquad \tau_{\theta} \gg \tau_{\varepsilon}$$"),
    ],
    plain="Every backtest assumes the game tomorrow is the game yesterday. Separating fast fluctuations "
          "from slow regime drift tells you how long 'tomorrow' lasts — and therefore how brilliant a "
          "strategy can afford to be before drift quietly kills it.",
),
}

# ---------------------------------------------------------------- template
PAGE = """<div id="view-{slug}" style="display: none; font-family: var(--font-family-sans);">
    <header style="margin-bottom: 2rem;">
        <p style="color: var(--accent); font-weight: 700; font-size: 0.8rem; text-transform: uppercase; margin: 0;">CQF Talks &bull; {cat_label}</p>
        <h1 style="margin: 0; font-size: 2rem; font-weight: 800; border-bottom: none; padding-bottom: 0;">{title}</h1>
        <p style="color: var(--text-muted); margin-top: 0.5rem;">{subtitle}</p>
    </header>

    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 2rem; align-items: stretch; margin-bottom: 2rem;">
        <div class="card" style="margin-bottom: 0; padding: 1.5rem;">
            <h3 style="margin-top: 0;">What This Talk Covers</h3>
            <p style="line-height: 1.7; margin-bottom: 0;">{overview}</p>
        </div>
        <div class="card" style="margin-bottom: 0; background: #fffbeb; border-left: 4px solid #f59e0b; border-radius: 8px; padding: 1.5rem;">
            <h3 style="margin-top: 0; color: #b45309; font-family: 'Inter', sans-serif; font-weight: 700;">Plain English Notes</h3>
            <p style="font-family: 'Inter', sans-serif; line-height: 1.7; color: #451a03; margin-bottom: 0;"><strong>The Big Picture:</strong> {plain}</p>
        </div>
    </div>

{maths_card}
    <div style="display: flex; gap: 0.75rem; flex-wrap: wrap; margin-bottom: 2rem;">
        <a href="#talks-portal" onclick="showSection('talks-portal')" style="text-decoration: none; color: var(--accent); border: 1px solid var(--card-border); border-radius: 8px; padding: 0.5rem 1rem; font-size: 0.85rem; font-weight: 600; background: var(--metric-bg);">All talks</a>
    </div>

    <div class="card" style="border-left: 4px solid var(--accent); background: var(--bg-subtle);">
        <h3 style="margin-top:0;">Detailed Notes Coming Soon</h3>
        <p style="margin-bottom:0; color: var(--text-secondary);">Derivations, worked examples and interactive demos for this talk will be added here.</p>
    </div>
</div>
"""

MATHS_CARD = """    <div class="card" style="margin-bottom: 2rem;">
        <h3 style="margin-top: 0;">Core Mathematics</h3>
        {rows}
    </div>
"""

MATH_ROW = """<div style="padding: 0.75rem 0; border-bottom: 1px solid var(--card-border);">
            <div style="font-weight: 600; font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 0.25rem;">{label}</div>
            <div style="overflow-x: auto;">{formula}</div>
        </div>"""


def load_external_content():
    """Merge CONTENT dicts from scratch/talk_content_*.py data files."""
    import glob
    merged = {}
    for path in sorted(glob.glob(os.path.join(ROOT, "scratch", "talk_content_*.py"))):
        ns = {}
        exec(compile(open(path, encoding="utf-8").read(), path, "exec"), ns)
        merged.update(ns.get("CONTENT", {}))
    return merged


def main():
    cats = set(sys.argv[1:])
    CONTENT.update(load_external_content())
    catalog = {t["slug"]: t for t in json.load(open(CATALOG, encoding="utf-8"))}
    n = 0
    for slug, c in CONTENT.items():
        t = catalog.get(slug)
        if not t:
            print("  !! not in catalog:", slug)
            continue
        if cats and t["cat"] not in cats:
            continue
        maths_card = ""
        if c.get("maths"):
            rows = "\n        ".join(MATH_ROW.format(label=H.escape(l), formula=f) for l, f in c["maths"])
            maths_card = MATHS_CARD.format(rows=rows)
        page = PAGE.format(
            slug=slug, cat_label=H.escape(CAT_LABELS[t["cat"]]), title=H.escape(t["title"]),
            subtitle=H.escape(t.get("presenter") or CAT_LABELS[t["cat"]] + " — CQF Talks"),
            overview=H.escape(c["overview"]), plain=H.escape(c["plain"]), maths_card=maths_card,
        )
        open(os.path.join(SECTIONS, f"view-{slug}.html"), "w", encoding="utf-8").write(page)
        n += 1
    print(f"enriched {n} talk pages")


if __name__ == "__main__":
    main()

# Content for §6 Portfolio & Allocation talks — consumed by enrich_talks.py
# NOTE: talk-hrp and talk-max-diversification absent (pre-existing hand-built pages).
CONTENT = {

"talk-the-development-and-evolution-of-mean": dict(
    overview="Thirty years after the Markowitz and Ziemba applications: the development of "
             "mean-variance efficient portfolios in the US and Japan, with earnings, cash-flow and "
             "forecast-based models still producing significant excess returns.",
    maths=[
        ("Mean-variance program", r"$$\min_w\; w^\top \Sigma w \quad \text{s.t.}\quad w^\top \mu \ge \mu_0,\; w^\top \mathbf{1} = 1$$"),
    ],
    plain="The oldest quantitative idea in finance, tracked over three decades and two markets: "
          "carefully estimated inputs plus disciplined optimization kept beating naive alternatives "
          "— the craft is in the inputs, not the optimizer.",
),
"talk-quantitative-finance-corporate-finance-and": dict(
    overview="Guerard traces quantitative finance's history from Markowitz, Mossin and Sharpe through "
             "Elton-Gruber, Brealey and Ziemba: how portfolio construction and corporate finance "
             "co-evolved, then and now.",
    maths=[
        ("CAPM lineage", r"$$\mathbb{E}[R_i] - r = \beta_i \left( \mathbb{E}[R_m] - r \right)$$"),
    ],
    plain="A guided genealogy of the field: which ideas survived (diversification, factor pricing), "
          "which mutated (efficiency), and how the same names keep reappearing across portfolio "
          "theory and corporate finance.",
),
"talk-some-financial-anomalies-have-survived-the": dict(
    overview="Markowitz and Guerard in conversation: financial anomalies — value, momentum, earnings "
             "forecasts — whose statistical significance has persisted for over 30 years despite "
             "publication and arbitrage.",
    maths=[
        ("Anomaly persistence test", r"$$\alpha_{\text{post-publication}} \ne 0 \;\text{at same significance as in-sample}$$"),
    ],
    plain="Most published anomalies die on contact with real money; a stubborn few refuse. Hearing "
          "Markowitz himself weigh which are real — months before his passing — makes this as much "
          "history as finance.",
),
"talk-when-the-optimal-portfolio-selection-may-not": dict(
    overview="Have financial anomalies diminished in the US and abroad? Evidence on anomaly decay, "
             "and when the cost and effort of full optimal portfolio selection stops paying for "
             "itself relative to simple rules.",
    maths=[
        ("Optimization value test", r"$$\text{IR}_{\text{optimized}} - \text{IR}_{\text{heuristic}} \;\text{vs}\; \text{costs} + \text{estimation error}$$"),
    ],
    plain="Optimization earns its complexity only when signals are strong and estimates stable. As "
          "anomalies fade, the gap between the optimizer and a sensible equal-weight shrinks toward "
          "— and sometimes below — its costs.",
),
"talk-hierarchical-minimum-variance-portfolios": dict(
    overview="Peter Cotton's 'Schur complementary' allocation: a method bridging minimum-variance "
             "portfolios and hierarchical (cluster-based) allocation schemes, with strong performance "
             "in live portfolio competitions.",
    maths=[
        ("Schur-complement blend", r"$$\Sigma = \begin{pmatrix} A & B \\ B^\top & D \end{pmatrix}, \qquad \text{allocate via } A - \gamma\, B D^{-1} B^\top$$"),
    ],
    plain="Minimum variance trusts the covariance matrix completely; hierarchical methods barely "
          "trust it at all. A dial built from the Schur complement interpolates between them — and "
          "the sweet spot beats both parents.",
),
"talk-tell-me-what-exactly-is-diversification-and": dict(
    overview="What exactly is diversification? The standard quantitative definitions prove inadequate "
             "under scrutiny; the talk builds better formalizations and evaluation criteria for "
             "genuinely diversified portfolios.",
    maths=[
        ("Diversification ratio", r"$$DR(w) = \frac{w^\top \sigma}{\sqrt{w^\top \Sigma w}} \;\ge 1$$"),
        ("Effective number of bets", r"$$N_{\text{eff}} = e^{-\sum_i p_i \ln p_i}, \qquad p_i = \text{risk contribution shares}$$"),
    ],
    plain="Everyone recommends diversification; almost nobody can define it. Counting holdings fails "
          "(they correlate), variance reduction fails (hides tail dependence) — the talk hunts for a "
          "definition that survives its own counterexamples.",
),
"talk-managing-diversification": dict(
    overview="Managing diversification as an explicit objective: risk-contribution budgeting, "
             "correlation regimes, and keeping a portfolio diversified through time rather than at a "
             "single optimization date.",
    maths=[
        ("Risk contribution", r"$$RC_i = w_i \frac{(\Sigma w)_i}{\sqrt{w^\top \Sigma w}}, \qquad \sum_i RC_i = \sigma_p$$"),
    ],
    plain="Diversification is a perishable good: correlations drift toward one exactly in crises. "
          "Managing it means monitoring risk contributions continuously, not admiring the pie chart "
          "from last quarter's rebalance.",
),
"talk-adaptive-diversification": dict(
    overview="Philip Maymin on enhancing compound returns via higher alpha, lower volatility or "
             "positive skewness: alpha is fickle, but dynamic risk management — adaptive "
             "diversification — can be robust.",
    maths=[
        ("Compound growth decomposition", r"$$g \approx \mu - \tfrac{1}{2}\sigma^2 + \text{skew effects} \quad\text{— cut } \sigma \text{ when trend breaks}$$"),
    ],
    plain="You can't reliably raise the numerator (alpha), but you can manage the denominator: "
          "scaling exposure with market regime turns ordinary returns into better compounding by "
          "dodging part of the variance drag.",
),
"talk-fat-tailed-diversification-entropies-tail": dict(
    overview="Jan Rosenzweig uses higher moments and mutual information to find independent, "
             "'tail-orthogonal' components: diversification measured where it matters — in the "
             "tails, not the covariance matrix.",
    maths=[
        ("Tail covariance / co-kurtosis", r"$$\kappa_{ij} = \mathbb{E}\!\left[ z_i^2 z_j^2 \right] - 1 \qquad \text{beyond } \rho_{ij}$$"),
    ],
    plain="Two assets can be uncorrelated on average and lockstep in crashes. Building portfolios "
          "orthogonal in the tails — via entropy and information measures — buys the diversification "
          "you actually need on the day you need it.",
),
"talk-tails-black-swans-and-optimal-portfolios": dict(
    overview="Why are Modern Portfolio Theory's optimal portfolios not diversified? Is that a "
             "feature? Do simple rules of thumb beat MPT, which ones, and why do they even work "
             "under fat tails?",
    maths=[
        ("Estimation-error maximization", r"$$w^* = \Sigma^{-1}\mu \;\text{amplifies errors: } \operatorname{Var}(w^*) \propto \Sigma^{-1} \operatorname{Var}(\hat\mu)\, \Sigma^{-1}$$"),
    ],
    plain="The optimizer is an error amplifier: it bets biggest exactly where estimates are most "
          "wrong. Rules of thumb like equal weight are 'suboptimal' under assumptions that are "
          "false and superior under conditions that are real.",
),
"talk-the-markets-are-not-normal": dict(
    overview="Graham Giller on the profound portfolio consequences of non-normal returns: why "
             "mean-variance optimization underperforms simple heuristics that respect fat tails, "
             "and what to use instead.",
    maths=[
        ("Generalized error distribution", r"$$f(x) \propto \exp\!\left( -\left| \frac{x}{\alpha} \right|^{\beta} \right), \qquad \beta < 2 \text{ empirically}$$"),
    ],
    plain="Every input to Markowitz assumes a distribution the data reject. Giller's message from "
          "decades of desk econometrics: model the returns you have, not the returns that make the "
          "algebra pretty — sizing and allocation change materially.",
),
"talk-statistical-consequences-of-fat-tails": dict(
    overview="Around Taleb's technical volume: pre-asymptotics, why the law of large numbers works "
             "too slowly under fat tails, estimator fragility, and what remains estimable in the "
             "real-world epistemology of risk.",
    maths=[
        ("Slow LLN under fat tails", r"$$n_{\text{needed}}(\alpha) \;\text{explodes as tail index } \alpha \downarrow 2 \quad\text{(mean barely exists)}$$"),
    ],
    plain="With thin tails, 30 observations tell you the mean; with fat tails, 30,000 may not. Most "
          "of finance quietly assumes the first regime while living in the second — this is the "
          "catalogue of what breaks.",
),
"talk-black-litterman-beyond-black-litterman-views": dict(
    overview="Beyond Black-Litterman: the COP (Copula Opinion Pooling) approach to views on generic "
             "markets — a five-step implementation recipe extending view-blending past Gaussian "
             "assumptions, with a worked portfolio example.",
    maths=[
        ("BL posterior (the baseline)", r"$$\mu_{BL} = \left[ (\tau\Sigma)^{-1} + P^\top \Omega^{-1} P \right]^{-1}\left[ (\tau\Sigma)^{-1}\Pi + P^\top \Omega^{-1} Q \right]$$"),
    ],
    plain="Black-Litterman lets you whisper opinions into an equilibrium portfolio, but only Gaussian "
          "opinions about means. Copula pooling accepts views about tails, ranges and asymmetries — "
          "opinions traders actually hold.",
),
"talk-building-a-tool-for-strategic-asset": dict(
    overview="Helvetia's build of 'Sally', a bespoke Black-Litterman implementation for strategic "
             "asset allocation at a Swiss insurer: model tailoring, governance and the realities of "
             "in-housing quant tooling.",
    maths=[
        ("Insurer's constrained SAA", r"$$\max_w\; \text{BL utility} \quad \text{s.t.}\quad \text{SST capital}, \text{liquidity}, \text{ALM limits}$$"),
    ],
    plain="A textbook model meets Solvency capital charges, accounting constraints and a board: the "
          "talk is a candid diary of turning Black-Litterman into a tool an insurance investment "
          "committee actually uses.",
),
"talk-quantitative-asset-allocation-at-a-swiss": dict(
    overview="Three years of running quantitative asset allocation at Helvetia: what worked, what "
             "needed rework, and lessons from operating a Black-Litterman-based SAA process through "
             "live markets.",
    maths=[],
    plain="The rare sequel talk: the same tool three years later, with the scars. Model governance, "
          "view discipline, and the discovery that the process around the model matters more than "
          "the model.",
),
"talk-industry-talk-optimization-of-strategic-and": dict(
    overview="Optimization of strategic and tactical asset allocation for multi-asset portfolios "
             "when expected returns and covariances resist estimation: robust formulations for the "
             "practically-minded allocator.",
    maths=[
        ("Robust allocation", r"$$\max_w \min_{\mu \in U(\hat\mu)}\; w^\top \mu - \tfrac{\gamma}{2} w^\top \Sigma w$$"),
    ],
    plain="Every allocation is a bet on estimates you don't trust. Robust optimization makes the "
          "distrust explicit: optimize against the worst case inside your uncertainty set, and the "
          "portfolio stops lurching with every re-estimate.",
),
"talk-rosaa-robust-optimization-of-strategic-and": dict(
    overview="ROSAA: robust optimization of strategic and active asset allocation for modern "
             "multi-asset portfolios — handling estimation uncertainty and illiquid private assets "
             "alongside public assets and hedge funds.",
    maths=[
        ("Smoothed illiquid returns", r"$$r^{\text{obs}}_t = (1-\theta)\, r^{\text{true}}_t + \theta\, r^{\text{obs}}_{t-1} \;\Rightarrow\; \text{de-smooth before allocating}$$"),
    ],
    plain="Private assets report gentle, smoothed returns that seduce optimizers into overallocation. "
          "ROSAA unsmooths them, prices the illiquidity, and keeps the allocation honest about risks "
          "the quarterly marks hide.",
),
"talk-stationary-portfolio-optimisation-for": dict(
    overview="Stationary portfolio optimization extended to maximize the probability of achieving "
             "target returns — the natural objective for sovereign wealth funds and pension plans "
             "with explicit goals.",
    maths=[
        ("Goal-probability objective", r"$$\max_w\; \mathbb{P}\!\left( W_T \ge W_{\text{target}} \right) \quad\text{vs classic } \max \mathbb{E}[U]$$"),
    ],
    plain="A pension fund doesn't want maximal expected utility; it wants to hit its number. "
          "Optimizing the probability of reaching the target produces different — often more "
          "aggressive-then-defensive — glide paths than mean-variance ever suggests.",
),
"talk-canonical-portfolios-optimal-asset-and": dict(
    overview="Canonical portfolios: a framework for the joint optimal combination of assets and "
             "signals, building on Brandt & Santa-Clara's parametric approach via canonical "
             "correlation structure.",
    maths=[
        ("Signal-asset combination", r"$$w_t = \theta\, z_t, \qquad \max_\theta\; \mathbb{E}\left[ U\!\left( (\theta z_t)^\top r_{t+1} \right) \right]$$"),
    ],
    plain="Two entangled questions — which assets, weighted by which signals — collapse into one "
          "clean optimization over a policy matrix. Canonical analysis then reveals how many "
          "genuinely independent signal-asset combinations your data supports.",
),
"talk-parametric-portfolio-policies": dict(
    overview="Parametric portfolio policies: modelling weights directly as functions of asset "
             "characteristics, sidestepping return-distribution estimation entirely.",
    maths=[
        ("Characteristic-based weights", r"$$w_{i,t} = \bar{w}_{i,t} + \frac{1}{N_t}\, \theta^\top x_{i,t}, \qquad \max_\theta \mathbb{E}\left[ U(r_p) \right]$$"),
    ],
    plain="Skip forecasting returns and covariances; optimize the three numbers that map "
          "characteristics (value, momentum, size) into over- and under-weights. Radical parsimony, "
          "surprisingly hard to beat out of sample.",
),
"talk-portfolio-maximum-entropy-and-sampling-error": dict(
    overview="Maximum-entropy portfolio construction with explicit sampling-error control: "
             "regularizing allocation by information-theoretic criteria rather than ad hoc "
             "constraints.",
    maths=[
        ("Entropy-regularized weights", r"$$\max_w\; \mu^\top w - \tfrac{\gamma}{2} w^\top \Sigma w + \lambda\, H(w)$$"),
    ],
    plain="When data can't distinguish between many near-optimal portfolios, pick the least opinionated "
          "one — maximum entropy is Occam's razor for allocation, and it doubles as a defence against "
          "estimation noise.",
),
"talk-portfolio-management-for-people": dict(
    overview="Portfolio risk is an insufficient measure for wealth management: incorporating the "
             "person — human capital, life circumstances, goals and behavioural constraints — into "
             "portfolio design.",
    maths=[
        ("Total-wealth view", r"$$W_{\text{total}} = W_{\text{financial}} + PV(\text{human capital}) \quad\text{allocate on the total}$$"),
    ],
    plain="A tenured professor and a startup founder with identical portfolios hold wildly different "
          "risks, because their paychecks are different assets. Wealth management that ignores the "
          "human column of the balance sheet manages the wrong portfolio.",
),
"talk-conditional-maximum-loss-a-new-dynamic-risk": dict(
    overview="Conditional Maximum Loss (CML): a dynamic risk measure designed for fully general "
             "Monte Carlo simulation paths and their probabilities, with portfolio optimization "
             "applications.",
    maths=[
        ("CML definition (schematic)", r"$$\text{CML}_\alpha = \mathbb{E}\!\left[ \max_{t \le T} L_t \,\middle|\, \text{worst } \alpha \text{ fraction of paths} \right]$$"),
    ],
    plain="VaR asks about one date; investors bleed along paths. Conditioning on the worst paths and "
          "measuring their maximum drawdown captures the experience of living through a bad scenario "
          "— and optimizing against it changes the portfolio.",
),
"talk-covariance-complexity-and-rates-of-return-on": dict(
    overview="Covariance structure as shared information: how the complexity of the covariance matrix "
             "determines what can be borrowed across assets when estimating each one's expected "
             "return.",
    maths=[
        ("Shrinkage via structure", r"$$\hat\mu_i = \bar\mu + \text{loading}_i \times \text{common component} \quad\text{— James-Stein logic through } \Sigma$$"),
    ],
    plain="Assets that co-move share information: the covariance matrix tells you how much of one "
          "asset's history is testimony about another's mean. Exploiting that pooling beats "
          "estimating each return in isolation.",
),
"talk-can-you-count-on-your-correlation-matrix": dict(
    overview="Can you count on your correlation matrix? Estimation noise, non-positive-definiteness, "
             "regime instability and cleaning methods (shrinkage, RMT filtering) for the most "
             "abused object in finance.",
    maths=[
        ("Marchenko-Pastur noise band", r"$$\lambda_{\pm} = \sigma^2 \left( 1 \pm \sqrt{N/T} \right)^2 \quad\text{eigenvalues inside are noise}$$"),
    ],
    plain="With 500 assets and two years of data, most of your correlation matrix is statistical "
          "static. Random matrix theory tells you exactly which eigenvalues carry signal — filter "
          "the rest or the optimizer will trade pure noise.",
),
"talk-excess-out-of-sample-risk-and-fleeting-modes": dict(
    overview="Using Random Matrix Theory to reveal 'fleeting modes': directions of risk that appear "
             "out-of-sample but were invisible in-sample, explaining the systematic underestimation "
             "of realized portfolio risk.",
    maths=[
        ("In/out-of-sample overlap", r"$$\text{risk ratio} = \frac{w^\top \Sigma_{\text{out}}\, w}{w^\top \Sigma_{\text{in}}\, w} > 1 \;\text{systematically}$$"),
    ],
    plain="Optimized portfolios always look riskier live than in the backtest — partly because "
          "correlation structure rotates. The 'fleeting modes' formalism measures how fast risk "
          "directions decay, and thus how much extra risk to budget for.",
),
"talk-tests-of-asset-pricing-models-with-a-large": dict(
    overview="Extending the Gibbons-Ross-Shanken test to settings where the number of assets exceeds "
             "the sample size: statistical and economic tests of factor pricing models in high "
             "dimension.",
    maths=[
        ("GRS statistic (classic)", r"$$\text{GRS} = \frac{T - N - K}{N} \cdot \frac{\hat\alpha^\top \hat\Sigma^{-1} \hat\alpha}{1 + \hat\mu_f^\top \hat\Omega^{-1} \hat\mu_f} \sim F_{N, T-N-K}$$"),
    ],
    plain="The classic test of 'do these factors price everything' breaks when you have more assets "
          "than months. High-dimensional statistics repairs it — and several celebrated factor models "
          "fail the repaired exam.",
),
"talk-standardized-conditional-expectation-sce-an": dict(
    overview="Standardized Conditional Expectation (SCE) applied to the CAPM: a conditional "
             "reformulation of beta and expected-return relationships with empirical implementation.",
    maths=[
        ("Conditional beta", r"$$\beta_t = \frac{\operatorname{Cov}(R_i, R_m \,|\, \mathcal{F}_t)}{\operatorname{Var}(R_m \,|\, \mathcal{F}_t)} \quad\text{— time-varying by construction}$$"),
    ],
    plain="Unconditional CAPM tests average over booms and busts where betas differ; conditioning "
          "restores the information. SCE standardizes that conditioning so the model can be tested "
          "— and used — regime by regime.",
),
"talk-new-financial-decision-theory-objectives": dict(
    overview="OU processes with tempered fractional Lévy drivers reduce to (d+1)-dimensional "
             "Markovian systems; new decision-theory objectives are then formulated for stock "
             "trading in this high-dimensional Markovian model.",
    maths=[
        ("Markovian embedding", r"$$X_t = \text{OU with TFLP drift} \;\Rightarrow\; (X, Z_1, \dots, Z_d) \text{ Markov}$$"),
    ],
    plain="Long-memory processes are un-Markovian nightmares for optimization — unless the memory "
          "has special structure that unfolds into a few extra state variables. Then dynamic "
          "programming returns, and with it optimal trading rules.",
),
"talk-towards-a-paradigm-of-structural-factor": dict(
    overview="Against the proliferation of empirical factor methods that transfer poorly across "
             "asset classes: a structural paradigm for factor investing grounded in economic "
             "mechanism rather than backtest archaeology.",
    maths=[
        ("Structural vs statistical factors", r"$$R = B_{\text{econ}}\, f_{\text{econ}} + \varepsilon \quad\text{vs}\quad R = \text{whatever fits}$$"),
    ],
    plain="The factor zoo grew by data mining; few exhibits survive transport to new asset classes. "
          "Structural factors — built from how returns are economically generated — travel, because "
          "the mechanism travels.",
),
"talk-advances-in-factor-investing": dict(
    overview="BlackRock's view of factor investing: defining factors, the reasons risk premia exist, "
             "translating factors across asset classes, and factor timing via diversification and "
             "multiple weak signals.",
    maths=[
        ("Factor timing composite", r"$$w_f \propto \text{valuation}_f + \text{momentum}_f + \text{dispersion}_f + \text{regime}_f$$"),
    ],
    plain="Factors earn premia for reasons — risk, structure or behaviour — and the reason predicts "
          "the durability. Timing them individually is nearly hopeless; nudging with several weak, "
          "diversified signals is merely hard.",
),
"talk-factor-investing-and-the-road-to-diversified": dict(
    overview="Panel: factor investing and the road to 'diversified serfdom' — crowding, the "
             "commodification of quant strategies, and whether systematic risk premia survive their "
             "own popularity.",
    maths=[],
    plain="When everyone owns the same 'smart' portfolio, its risks synchronize and its premia "
          "compress: diversification for each, fragility for all. The panel argues where factor "
          "investing's genuine value survives the crowd.",
),
"talk-why-active-managers-should-not-try-to": dict(
    overview="Why maximizing the Information Ratio and using tracking error as the risk measure "
             "misleads active managers: with bi-modal active-return distributions, conventional "
             "active risk metrics reward the wrong behaviour.",
    maths=[
        ("The conventional objective", r"$$\text{IR} = \frac{\mathbb{E}[R_p - R_b]}{\operatorname{sd}(R_p - R_b)} \quad\text{— pathological under bi-modal } R_p - R_b$$"),
    ],
    plain="Tracking error punishes deviation symmetrically: beating the benchmark hugely counts as "
          "'risk'. For genuinely active portfolios with two-humped outcomes, IR-maximization "
          "systematically prefers mediocrity — the metric, not the manager, is broken.",
),
"talk-worrying-about-alpha-adam-rej-overfitting": dict(
    overview="Adam Rej on the two decays of systematic strategies in production: in-sample "
             "overfitting (the backtest lied) and arbitrage/crowding (the truth stopped being true), "
             "with diagnostics and defences for each.",
    maths=[
        ("Live-vs-backtest haircut", r"$$\text{IR}_{\text{live}} \approx \kappa \cdot \text{IR}_{\text{backtest}}, \qquad \kappa \ll 1 \text{ and estimable}$$"),
    ],
    plain="Strategies die twice: once retroactively (it never worked; you tortured the data) and "
          "once truly (it worked; the crowd arrived). Distinguishing the autopsy matters because "
          "the defences — statistical discipline vs capacity management — are different.",
),
"talk-when-love-is-blind-making-sense-of-in-sample": dict(
    overview="Rej's deep dive on in-sample overfitting: why and how it occurs in backtest-based "
             "strategy development, and quantitative frameworks for estimating how much in-sample "
             "Sharpe is illusion.",
    maths=[
        ("Expected max-Sharpe inflation", r"$$\mathbb{E}\left[ \max_{k \le K} \widehat{SR}_k \right] \approx \sigma_{SR} \sqrt{2 \ln K} \quad\text{under zero true skill}$$"),
    ],
    plain="Test enough variants and the best backtest looks brilliant by pure chance — the formula "
          "above prices that mirage. Subtract it from your best in-sample Sharpe and meet your "
          "strategy's honest expected future.",
),
"talk-how-to-identify-and-mitigate-overfitting": dict(
    overview="SigTech and Cuemacro on practical overfitting hygiene: identification symptoms, "
             "out-of-sample discipline, parameter-sensitivity analysis and process design that "
             "mitigates backtest self-deception.",
    maths=[
        ("Deflated Sharpe ratio", r"$$DSR = \Phi\!\left( \frac{\widehat{SR} - SR_0(K)}{\hat\sigma_{SR}} \right)$$"),
    ],
    plain="Overfitting is rarely fraud and usually enthusiasm: every 'improvement' silently burns "
          "out-of-sample evidence. The mitigation is procedural — pre-registration, untouched "
          "holdouts, sensitivity maps — not statistical heroics after the fact.",
),
"talk-false-confidence-in-systematic-trading": dict(
    overview="In systematic trading, speed sells — and much of it is illusion: short lookback "
             "windows adapt 'fast' but mostly chase noise, a statistical mirage this talk "
             "dismantles.",
    maths=[
        ("Estimator variance vs window", r"$$\operatorname{Var}(\hat\mu_L) \propto \frac{\sigma^2}{L} \quad\text{— halve the window, double the noise}$$"),
    ],
    plain="A 20-day signal isn't nimbler than a 200-day one; it's twenty times noisier. What looks "
          "like rapid adaptation is the estimator vibrating — and every vibration is a trade with "
          "costs attached.",
),
"talk-achieving-reliable-return-projections-in": dict(
    overview="SigTech and Quantpedia on backtesting and simulating strategies under highly uncertain "
             "markets: the challenges of reliable return projections and the practices that keep "
             "them honest.",
    maths=[
        ("Projection with regime uncertainty", r"$$\mathbb{E}[R] = \sum_k \pi_k\, \mu_k, \qquad \pi_k \text{ itself uncertain}$$"),
    ],
    plain="A backtest is one draw from history; a projection pretends the draw repeats. Stress the "
          "assumptions — regimes, costs, capacity — and report ranges instead of points, or the "
          "projection is marketing wearing mathematics.",
),
"talk-what-signals-worked-and-what-did-not-1980": dict(
    overview="Three decades of prediction signals reviewed across asset classes with equity focus: "
             "what worked 1980-2009, what did not, and the survivorship-aware accounting of both.",
    maths=[
        ("The scorecard form", r"$$\text{IC}_t = \operatorname{corr}\!\left( \text{signal}_{t-1}, R_t \right) \quad\text{tracked across eras}$$"),
    ],
    plain="A brutal ledger of quant signals through four market regimes: value's long reign and "
          "collapses, momentum's crashes, earnings signals' slow bleed. The pattern — every signal's "
          "obituary was written at least once — argues for diversification of beliefs.",
),
"talk-update-on-us-stock-market-calendar-anomalies": dict(
    overview="Ziemba's calendar-anomaly canon — turn-of-month, January, holiday effects — updated "
             "through 2019 and into the COVID-19 era: which seasonals survived, which faded.",
    maths=[
        ("Turn-of-month effect", r"$$\mathbb{E}[R \,|\, \text{days } -1..+4] \gg \mathbb{E}[R \,|\, \text{other days}]$$"),
    ],
    plain="Payroll flows, rebalancing schedules and human holidays imprint a calendar on returns. "
          "The update finds several classics alive (turn-of-month) even through a pandemic — flows "
          "don't read the anomalies literature.",
),
"talk-the-predictability-of-stock-prices-and-stock": dict(
    overview="Is predictability there and how to find it: the DJIA and S&P 500 examined for return "
             "predictability with valuation and technical conditioning variables.",
    maths=[
        ("Predictive regression", r"$$R_{t+1} = \alpha + \beta\, x_t + \varepsilon_{t+1}, \qquad \text{Stambaugh bias in } \hat\beta$$"),
    ],
    plain="Index returns are slightly predictable at long horizons — valuation ratios whisper about "
          "the next decade, not the next week. The econometrics is treacherous (persistent "
          "regressors flatter you), which is why the whisper took decades to authenticate.",
),
"talk-a-model-for-passive-that-breaks-the-market": dict(
    overview="A plausible model of the US equity market's dollar size incorporating passive share: "
             "as indexing grows, price elasticity falls and flows move prices more — 'passive breaks "
             "the market' quantified.",
    maths=[
        ("Inelastic markets multiplier", r"$$\Delta P \approx M \cdot \frac{\text{flow}}{\text{market cap}}, \qquad M \sim 3\text{-}8 \text{ and rising with passive share}$$"),
    ],
    plain="Passive funds don't ask prices, they take them — so a dollar into indexes moves valuations "
          "several dollars. As passive share compounds, markets get simpler to push and harder to "
          "anchor: the model traces where that road leads.",
),
"talk-algorithms-for-tracking-the-s-and-p-500": dict(
    overview="Index tracking as an optimization benchmark: good old-fashioned heuristics versus "
             "machine learning for sparse replication of the S&P 500 — which actually works better, "
             "measured properly.",
    maths=[
        ("Sparse tracking problem", r"$$\min_w\; \left\| R_{\text{idx}} - R w \right\|^2 \quad \text{s.t.}\quad \|w\|_0 \le k$$"),
    ],
    plain="Replicating 500 stocks with 40 is a combinatorial puzzle where fancy learners meet humble "
          "heuristics on equal terms — and the verdict is uncomfortable for fashion: tuned classics "
          "hold their ground.",
),
"talk-simply-quant-investing-pim-van-vliet": dict(
    overview="Pim van Vliet's evidence-based case for simplicity: three rules — low volatility, "
             "value, momentum — generating high long-term returns with lower downside risk, and the "
             "low-vol anomaly at the centre.",
    maths=[
        ("The low-volatility anomaly", r"$$\mathbb{E}[R_{\text{low-vol}}] \;\gtrsim\; \mathbb{E}[R_{\text{high-vol}}] \quad\text{— CAPM inverted in the data}$$"),
    ],
    plain="The market pays boring stocks nearly as much as exciting ones while scaring you far less "
          "— a century-old free lunch protected by career risk: managers can't hug benchmarks with "
          "them. Three simple rules harvest it.",
),
"talk-crowd-sourced-alpha-the-search-for-the-holy": dict(
    overview="Crowd-sourced alpha: why it is so hard to find, what to demand from active management, "
             "the market-to-peers comparison, and the strategic intent behind crowdsourcing "
             "platforms.",
    maths=[
        ("Crowd aggregation hope", r"$$\alpha_{\text{crowd}} = \frac{1}{N}\sum_i \alpha_i, \qquad \operatorname{Var} \downarrow \text{ iff errors independent — they aren't}$$"),
    ],
    plain="Crowdsourcing works when errors are independent; quant crowds share data, tools and "
          "tutorials, so their errors correlate. The gold survives, but panning it from correlated "
          "silt is the platform's real problem.",
),
"talk-equity-portfolio-risk-management": dict(
    overview="Practitioner equity risk management: stock risk models, generic versus practical risk "
             "modelling examples, and decomposing portfolio return and risk for actual decision "
             "support.",
    maths=[
        ("Active risk decomposition", r"$$\sigma^2_{\text{active}} = w_a^\top \left( B \Sigma_f B^\top + D \right) w_a$$"),
    ],
    plain="Risk models exist to answer manager questions — where am I betting, what happens if value "
          "crashes, which position is the outlier — not to admire eigenvalues. The talk keeps the "
          "machinery pointed at decisions.",
),
"talk-enhancing-performance-of-mid-to-low": dict(
    overview="Enhancing performance of mid-to-low frequency trade portfolios: execution, netting, "
             "signal blending and turnover control where holding periods stretch from days to "
             "months.",
    maths=[
        ("Turnover-penalized objective", r"$$\max_w\; \mu^\top w - \tfrac{\gamma}{2} w^\top \Sigma w - c\, \|w - w_{\text{prev}}\|_1$$"),
    ],
    plain="At lower frequencies alpha per trade is thin, so implementation is the edge: netting "
          "signals before trading, penalizing turnover inside the optimizer, and treating "
          "transaction costs as first-class citizens.",
),
"talk-is-it-possible-to-make-investors-happy": dict(
    overview="Investors as bosses: career advice meets behavioural finance in a simple model of "
             "happiness — what managers can and cannot do to satisfy clients whose satisfaction "
             "follows prospect theory.",
    maths=[
        ("Prospect-theory happiness", r"$$v(x) = \begin{cases} x^{\alpha} & x \ge 0 \\ -\lambda\, (-x)^{\alpha} & x < 0 \end{cases}, \qquad \lambda \approx 2.25$$"),
    ],
    plain="Clients feel losses twice as hard as gains and anchor on recent peaks — so mathematically "
          "'optimal' portfolios can guarantee misery. Designing for the happiness function, not just "
          "the wealth process, is part of the job.",
),
"talk-the-pain-and-pleasure-of-investing": dict(
    overview="The asymmetrical experience of making and losing money, quantified with stochastic "
             "calculus: pain-adjusted performance measures and their portfolio applications.",
    maths=[
        ("Pain-adjusted value", r"$$\text{PAV} = \mathbb{E}\!\left[ \int_0^T u(dW_t)\, dt \right], \qquad u \text{ loss-averse}$$"),
    ],
    plain="A year that ends flat after a 20% drawdown hurts more than one that was flat throughout "
          "— experience has a path integral. Pricing the journey, not just the destination, "
          "reorders which strategies investors should actually hold.",
),
"talk-the-knowing-doing-gap-in-behavioral-finance": dict(
    overview="The knowing-doing gap: investors and advisors know the behavioural findings yet fail "
             "to act on them — why knowledge doesn't transfer to behaviour and which mechanisms "
             "close the gap.",
    maths=[],
    plain="Everyone knows not to sell at the bottom; the bottom disagrees. Closing the gap takes "
          "pre-commitment devices and process design, because information alone has never beaten "
          "adrenaline.",
),
"talk-classifying-alternative-investments-using": dict(
    overview="Self-organizing maps applied to alternative investments: unsupervised classification of "
             "hedge funds and alternatives by return behaviour rather than declared style.",
    maths=[
        ("SOM update rule", r"$$m_j \leftarrow m_j + \eta\, h_{jc}\, (x - m_j)$$"),
    ],
    plain="Fund labels lie; return patterns don't. A self-organizing map arranges funds on a grid "
          "where neighbours behave alike, revealing style drift and closet replication that the "
          "marketing deck omits.",
),
"talk-a-machine-learning-tool-for-visual-risk": dict(
    overview="Claus Huber's SOM-based visual risk analysis for manager selection: mapping long-"
             "volatility strategies for tail-risk hedging, making high-dimensional due diligence "
             "visually navigable.",
    maths=[
        ("Distance on the map", r"$$d(f_i, f_j) = \| \text{SOM}(f_i) - \text{SOM}(f_j) \| \quad\text{— behavioural, not stated, similarity}$$"),
    ],
    plain="Choosing a tail-hedge manager means comparing dozens of funds across dozens of metrics; "
          "a trained map collapses that into a picture where the eye does the clustering — and "
          "outliers announce themselves.",
),
"talk-polymodel-analysis-of-hedge-funds-selection": dict(
    overview="Polymodels for hedge funds: profiling each fund by a battery of nonlinear single-factor "
             "responses to its environment, then selecting and combining funds on those profiles.",
    maths=[
        ("Nonlinear factor battery", r"$$R_{\text{fund}} = \phi_j(X_j) + \varepsilon_j \quad \forall j \;\Rightarrow\; \text{profile} = \{\phi_j\}$$"),
    ],
    plain="One regression per factor, hundreds of factors: the collection of curves is the fund's "
          "fingerprint — how it behaves when oil spikes, credit cracks or vol jumps. Portfolios "
          "built from complementary fingerprints diversify where linear factor models can't see.",
),
"talk-a-picture-worth-a-thousand-words-fine-art": dict(
    overview="Art as an investment: return and risk of fine art, market structure, high-profile "
             "transactions since the late 1980s, and the regulatory and tax dimensions of the asset "
             "class.",
    maths=[
        ("Repeat-sales return index", r"$$\ln P_{i,t_2} - \ln P_{i,t_1} = \sum_{t} \delta_t\, D_{i,t} + \varepsilon$$"),
    ],
    plain="Art returns exist but arrive wrapped in illiquidity, 25% transaction costs and provenance "
          "risk — and the index you read is built from the winners that resold. Beautiful on the "
          "wall, awkward in the portfolio.",
),
}

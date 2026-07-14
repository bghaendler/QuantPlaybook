# Content for §3 Options & BSM talks — consumed by enrich_talks.py
CONTENT = {

"talk-why-you-should-not-go-drinking-with-pure": dict(
    overview="Wilmott recaps the many ways of deriving Black-Scholes — hedging, replication, "
             "risk-neutral expectation, CAPM, transforms — and what each derivation reveals and, more "
             "importantly, quietly hides about the model's assumptions.",
    maths=[
        ("The hedging derivation", r"$$\Pi = V - \Delta S, \qquad d\Pi = r\Pi\, dt \;\Rightarrow\; \text{BS PDE}$$"),
        ("The expectation derivation", r"$$V = e^{-rT}\, \mathbb{E}^{\mathbb{Q}}\!\left[ \Pi(S_T) \right]$$"),
    ],
    plain="Each derivation of Black-Scholes is a different alibi for the same suspect: one needs "
          "continuous hedging, another needs complete markets, another needs Gaussian returns. Knowing "
          "which assumption each proof leans on tells you exactly how the model fails in practice.",
),
"talk-some-derivations-of-the-black-scholes": dict(
    overview="A systematic tour of Black-Scholes derivations — delta hedging, martingale pricing, "
             "utility limits, binomial limits — with the pros, cons and hidden assumptions of each "
             "route to the same PDE.",
    maths=[
        ("The destination", r"$$\frac{\partial V}{\partial t} + \tfrac{1}{2}\sigma^2 S^2 \frac{\partial^2 V}{\partial S^2} + rS\frac{\partial V}{\partial S} - rV = 0$$"),
        ("Binomial limit route", r"$$u = e^{\sigma\sqrt{\delta t}}, \quad d = e^{-\sigma\sqrt{\delta t}}, \quad n \to \infty$$"),
    ],
    plain="Ten roads to one equation — and the road you take determines which generalizations you can "
          "see. The hedging road generalizes to transaction costs; the expectation road to jumps; "
          "picking your derivation is picking your research programme.",
),
"talk-reflections-on-the-black-scholes-model-and": dict(
    overview="Fifty years after publication: reflections on the Black-Scholes technology, the growth "
             "of listed option markets, their informational efficiency, and the use of options in "
             "dynamic risk management strategies.",
    maths=[
        ("The formula at 50", r"$$C = S\,\Phi(d_1) - K e^{-rT}\, \Phi(d_2)$$"),
    ],
    plain="Few equations created an industry; this one did. The retrospective covers what the model "
          "got right (a common language for risk transfer) and how markets evolved around — and "
          "beyond — its assumptions.",
),
"talk-from-theory-to-practice-the-evolution-of": dict(
    overview="Tracing quantitative finance through Fischer Black's contributions: the 1973 option "
             "model, Black-76 for futures, the Black-Derman-Toy rate model, and Black-Litterman "
             "portfolio construction.",
    maths=[
        ("Black-76", r"$$C = e^{-rT}\left[ F\,\Phi(d_1) - K\,\Phi(d_2) \right]$$"),
        ("Black-Litterman posterior", r"$$\mu_{BL} = \left[ (\tau\Sigma)^{-1} + P^\top \Omega^{-1} P \right]^{-1} \left[ (\tau\Sigma)^{-1}\Pi + P^\top \Omega^{-1} Q \right]$$"),
    ],
    plain="Black's fingerprints are on options, rates and portfolios alike. The common thread is "
          "equilibrium thinking: start from what the market as a whole must believe, then deviate "
          "only where you have a reason.",
),
"talk-time-and-black-scholes-merton": dict(
    overview="On the model's 50th birthday: an argument that time in Black-Scholes-Merton must be "
             "completely reinterpreted — trading time, business time and calendar time are different "
             "clocks, with different consequences for volatility.",
    maths=[
        ("Time-scaled volatility", r"$$\sigma^2_{\text{eff}}\, T_{\text{calendar}} \;=\; \int_0^{T} \sigma^2(u)\, d\tau(u), \qquad \tau = \text{business/trading clock}$$"),
    ],
    plain="An option doesn't age by the calendar — it ages by how much trading happens. Weekends, "
          "holidays and quiet sessions stretch and squeeze the clock that volatility actually runs on.",
),
"talk-thought-and-black-scholes-merton-concept-and": dict(
    overview="A philosophical examination of BSM through Kant's distinction between concept and "
             "intuition: what probability theory can conceptualize versus what the financial market "
             "actually presents to experience.",
    maths=[],
    plain="A rare genuinely philosophical talk: probability theory builds concepts (measures, "
          "expectations), but markets deliver singular events that may not be instances of any "
          "concept. Where the two part ways is where models quietly stop referring to reality.",
),
"talk-a-truthful-generalization-of-black-scholes": dict(
    overview="The claim: regime-switching is the only 'truthful' generalization of Black-Scholes-Merton "
             "— the minimal extension that acknowledges the market can recalibrate, without pretending "
             "to know the future dynamics.",
    maths=[
        ("Regime-switching dynamics", r"$$dS = \mu_{Z_t} S\, dt + \sigma_{Z_t} S\, dW, \qquad Z_t \in \{1,\dots,m\} \text{ Markov}$$"),
    ],
    plain="Every model gets recalibrated tomorrow, contradicting its own assumptions today. "
          "Regime-switching bakes that recalibration into the model itself: the parameters are "
          "allowed to jump because in reality they always do.",
),
"talk-renewing-black-scholes-interpreting-renewal": dict(
    overview="Enhancing BSM with renewal waiting times: replacing the Poisson clock between price "
             "moves with general waiting-time distributions, and what the resulting semi-Markov "
             "dynamics mean for option prices.",
    maths=[
        ("Renewal process", r"$$N_t = \max\{n : T_1 + \cdots + T_n \le t\}, \qquad T_i \sim F \text{ i.i.d.}$$"),
    ],
    plain="Markets pause: quiet stretches between bursts of activity are not Poisson. Letting the "
          "waiting times have memory produces heavy tails and volatility clustering from first "
          "principles — the empirical facts BSM lacks.",
),
"talk-imaginary-oscillations-quantum-uncertainty": dict(
    overview="No equation has been more influential in finance than Black-Scholes; this talk re-reads "
             "it through quantum mechanics, where the same PDE with imaginary time is Schrödinger's "
             "equation, and asks what the analogy buys.",
    maths=[
        ("Wick rotation", r"$$\text{BS/heat equation} \;\xleftrightarrow{\; t \to i\tau \;}\; i\hbar\, \partial_t \psi = -\tfrac{\hbar^2}{2m}\, \partial_{xx} \psi$$"),
    ],
    plain="Diffusion and quantum evolution are the same mathematics separated by an imaginary number. "
          "The quantum reading treats price uncertainty as intrinsic superposition rather than "
          "ignorance — a different philosophy generating testably different dynamics.",
),
"talk-why-the-black-scholes-model-is-good-and-the": dict(
    overview="Gątarek's provocation: Black-Scholes is good and the Gaussian copula is not — because "
             "one is a hedging technology whose errors self-correct through recalibration, while the "
             "other is a static correlation assumption with no feedback mechanism.",
    maths=[
        ("Gaussian copula default correlation", r"$$C(u_1,\dots,u_n) = \Phi_\Sigma\!\left( \Phi^{-1}(u_1), \dots, \Phi^{-1}(u_n) \right)$$"),
    ],
    plain="BS is wrong but self-correcting: the desk re-hedges daily and recalibrates hourly. The "
          "copula was wrong and static: correlation was marked once and left to detonate in 2008. "
          "The difference isn't accuracy — it's the feedback loop.",
),
"talk-the-non-greek-non-foundation-of-derivative": dict(
    overview="A contrarian examination of derivative pricing's foundations: whether the Greeks-based "
             "hedging story really grounds the discipline, and what pricing looks like when the "
             "foundation is the market itself rather than the model.",
    maths=[],
    plain="The official story says prices come from models and hedging. The heretical reading: prices "
          "come from markets, models are interpolation devices, and the Greeks are bookkeeping for a "
          "practice that would survive without them.",
),
"talk-neither-god-nor-machine-mans-model": dict(
    overview="Between the fantasy of a perfect ('God's') model and blind data-driven ('machine') "
             "pricing lies Man's model: a search for the truthful middle ground in derivative pricing, "
             "honest about recalibration and regime change.",
    maths=[],
    plain="A perfect model would never need recalibrating; a pure machine can't say why it prices. "
          "The working quant lives between the two — with models simple enough to understand and "
          "humble enough to update.",
),
"talk-american-option-pricing-in-a-tick": dict(
    overview="The Andersen-Lake-Offengenden method: staggeringly fast and accurate American option "
             "pricing under Black-Scholes via fixed-point iteration for the exercise boundary and "
             "spectral collocation — microsecond pricing, calibration in a click.",
    maths=[
        ("Early exercise premium", r"$$P_{Am} = P_{Eu} + \int_0^T r K e^{-r u}\, \Phi(-d_2(S, B_u, u))\, du - \int_0^T q S e^{-qu}\, \Phi(-d_1)\, du$$"),
        ("Boundary fixed point", r"$$B_t = K\, \frac{N(t, B)}{D(t, B)} \quad \text{iterated to convergence}$$"),
    ],
    plain="American options were priced on trees for forty years — slow, jagged convergence. Recast "
          "the exercise boundary as a fixed-point problem, solve it with spectral accuracy, and a "
          "whole option chain prices faster than the market data feed updates.",
),
"talk-valuing-exotic-options-and-estimating-model": dict(
    overview="John Hull's volatility feature approach (VFA): feed the points of the implied volatility "
             "surface into a neural network as features to value exotics, and use the dispersion "
             "across retrainings to estimate model risk.",
    maths=[
        ("VFA mapping", r"$$V_{\text{exotic}} = \text{NN}\!\left( \{\sigma_{BS}(K_i, T_j)\},\ \text{contract terms} \right)$$"),
    ],
    plain="Rather than choosing one stochastic model and inheriting its prejudices, let the network "
          "read the whole surface directly. Different runs disagree slightly — and that disagreement "
          "is itself a usable estimate of model risk.",
),
"talk-pricing-of-digital-option-by-monte-carlo": dict(
    overview="Valuing digital options by discretizing the asset SDE and simulating — where the "
             "discontinuous payoff makes naive Monte Carlo converge badly — and an adaptive scheme "
             "that concentrates effort near the strike.",
    maths=[
        ("Digital payoff", r"$$\Pi = \mathbb{1}_{S_T > K}, \qquad V = e^{-rT}\, \mathbb{Q}(S_T > K) = e^{-rT}\Phi(d_2)$$"),
        ("Euler-Maruyama step", r"$$S_{t+\delta} = S_t\left( 1 + r\,\delta + \sigma \sqrt{\delta}\, Z \right)$$"),
    ],
    plain="A cliff-edge payoff punishes simulation: paths near the strike carry all the sensitivity. "
          "Adaptive schemes shrink the time step exactly where the path flirts with the barrier, "
          "buying accuracy where it matters.",
),
"talk-the-unreasonable-effectiveness-of-randomized": dict(
    overview="Monte Carlo, quasi-Monte Carlo and randomized QMC compared for option pricing and risk "
             "under the time-homogeneous hyperbolic local volatility model — with RQMC delivering "
             "near-N^{-3/2} convergence and honest error bars.",
    maths=[
        ("Convergence rates", r"$$\text{MC}: N^{-1/2} \qquad \text{QMC}: N^{-1}(\log N)^d \qquad \text{RQMC}: \approx N^{-3/2}$$"),
    ],
    plain="Deterministic low-discrepancy points beat random ones, but lose the error estimate. "
          "Randomize the scramble and you get both: faster convergence and a statistically valid "
          "confidence interval. Free lunch, mostly.",
),
"talk-the-importance-of-being-scrambled": dict(
    overview="Supercharged quasi-Monte Carlo: how scrambling (Owen-style) low-discrepancy sequences "
             "restores unbiasedness and error estimation while often improving convergence beyond "
             "plain Sobol sequences.",
    maths=[
        ("Owen-scrambled estimate", r"$$\hat{V} = \frac{1}{R} \sum_{r=1}^{R} \frac{1}{N} \sum_{i=1}^{N} f\!\left( \pi_r(x_i) \right), \qquad \operatorname{Var} \to \text{estimable}$$"),
    ],
    plain="Sobol points are too orderly to admit error bars; a careful random shuffle keeps their "
          "even coverage while making every run an independent draw. Practically: replace your "
          "random number generator, keep your code, halve your variance.",
),
"talk-finance-in-focus-application-of-quasi-monte": dict(
    overview="Applying quasi-Monte Carlo across finance: pricing, sensitivities and global sensitivity "
             "analysis (Sobol indices), with effective-dimension reduction explaining why QMC works so "
             "well on payoffs that are nominally high-dimensional.",
    maths=[
        ("Sobol sensitivity index", r"$$S_i = \frac{\operatorname{Var}\!\left( \mathbb{E}[f | x_i] \right)}{\operatorname{Var}(f)}$$"),
    ],
    plain="A 30-year monthly simulation is 360-dimensional on paper but low-dimensional in effect — a "
          "few principal directions carry the value. QMC exploits exactly that, and Sobol indices "
          "tell you which inputs matter enough to model well.",
),
"talk-singular-perturbation-problems-arising-in": dict(
    overview="Fluid-dynamics asymptotics imported into option pricing: singular perturbation and "
             "boundary-layer analysis for PDEs with small parameters — fast mean-reverting volatility, "
             "small transaction costs, short maturities.",
    maths=[
        ("Boundary layer expansion", r"$$V = V_0 + \varepsilon^{1/2}\, V_1 + \varepsilon\, V_2 + \cdots, \qquad \varepsilon = \text{fast timescale}$$"),
    ],
    plain="Near expiry or near a barrier the solution develops thin layers where everything happens "
          "at once — precisely where grids fail. Matched asymptotics, built for aircraft wings, "
          "resolve those layers with formulas instead of mesh points.",
),
"talk-can-you-feel-the-heat-inverse-problems-in": dict(
    overview="Inverse problems in engineering and finance: recovering causes (volatility surfaces, "
             "model parameters) from effects (prices), the theory of ill-posedness, and why "
             "regularization is not optional.",
    maths=[
        ("Ill-posed calibration", r"$$A\theta = V^{\text{mkt}}, \qquad \text{small } \delta V \Rightarrow \text{large } \delta\theta$$"),
        ("Tikhonov cure", r"$$\theta_\alpha = \arg\min \|A\theta - V\|^2 + \alpha \|L\theta\|^2$$"),
    ],
    plain="Feeling the heat at the wall and inferring the fire inside is mathematically treacherous — "
          "many fires produce the same wall temperature. Calibration is the same problem wearing "
          "finance clothes, and the same medicine (regularization) applies.",
),
"talk-option-writing-beyond-theta": dict(
    overview="A practitioner's framework for option writing: what and why, the Greeks that matter to "
             "a seller, whether theta alone is an edge, adding a forecasting element, and strategy "
             "optimization.",
    maths=[
        ("Writer's P&L decomposition", r"$$\text{P\&L} \approx \Theta\, dt + \tfrac{1}{2}\Gamma\, (dS)^2 + \text{Vega}\, d\sigma$$"),
    ],
    plain="Collecting theta is not an edge — it's compensation for gamma risk. The edge, if any, "
          "comes from selling when implied exceeds your honest forecast of realized, and sizing so "
          "one bad week doesn't return five good years.",
),
"talk-optimal-portfolio-construction-and-risk": dict(
    overview="Building optimal option portfolios from forecasts of distinct risk factors, and the "
             "empirical relationships between the equity, volatility and skew risk premia.",
    maths=[
        ("Factor-based option portfolio", r"$$\max_w\; w^\top \mu_{\text{premia}} - \tfrac{\gamma}{2} w^\top \Sigma w, \qquad \mu = (\text{ERP}, \text{VRP}, \text{SRP})$$"),
    ],
    plain="An options book is exposure to three rents: the equity premium, the variance premium and "
          "the skew premium. Treating them as an allocation problem — rather than trade-by-trade "
          "punts — is what separates a volatility business from a volatility bet.",
),
"talk-the-new-world-of-options-trading-valuation": dict(
    overview="Misha Fomytskyi (Vola Dynamics) on modern options desk workflows: detecting and fixing "
             "bad marks, building arbitrage-free volatility curves through chaotic markets (GME, "
             "0DTE), and robust risk management with real-world examples.",
    maths=[
        ("No-arbitrage surface constraints", r"$$\partial_K C \le 0, \qquad \partial_{KK} C \ge 0, \qquad \partial_T (\text{total variance}) \ge 0$$"),
    ],
    plain="Real quote screens are full of junk: crossed markets, stale prints, meme-stock chaos. An "
          "industrial-strength fitter turns that mess into smooth arbitrage-free curves fast enough "
          "to re-mark thousands of names continuously.",
),
"talk-robust-options-valuation-and-risk-management": dict(
    overview="An overview of a modern options valuation framework: the practical headaches of discount "
             "rates, borrow costs, dividends and time conventions, and how the Vola Dynamics analytics "
             "library addresses them.",
    maths=[
        ("Forward with borrow and dividends", r"$$F_T = (S_0 - PV_{\text{div}})\, e^{(r - b)T}$$"),
    ],
    plain="Most valuation errors on a desk aren't exotic-model failures — they're wrong dividends, "
          "wrong borrow, wrong day counts. The unglamorous inputs deserve the engineering attention "
          "this talk gives them.",
),
"talk-tools-for-options-trading-in-the-new-world-a": dict(
    overview="A short report from the cutting edge of options trading tooling: what changed in market "
             "structure and what the modern toolchain looks like.",
    maths=[],
    plain="A brief tour piece: faster markets, shorter-dated options, and the tooling arms race that "
          "followed. Companion to the full-length Vola Dynamics talks.",
),
"talk-the-hidden-cost-in-costless-put-spread": dict(
    overview="'Costless' put-spread collars carry a hidden cost: rebalance timing luck (RTL) — the "
             "dispersion of outcomes driven purely by which day of the cycle the hedge resets, and "
             "how to neutralize it by tranching.",
    maths=[
        ("Timing-luck dispersion", r"$$\sigma_{RTL}^2 \approx \frac{\sigma_{\text{strategy}}^2 - \sigma_{\text{tranched}}^2}{1}, \qquad \text{tranching: } \tfrac{1}{n}\sum_i \text{offset}_i$$"),
    ],
    plain="Two identical collar strategies, one resetting in March and one in April, can differ by "
          "whole percentage points a year out of sheer luck. Splitting the hedge into staggered "
          "tranches diversifies the calendar itself.",
),
"talk-the-short-lira-put-option-investment": dict(
    overview="Uwe Wystup's case study: short EUR/TRY put (lira call) 'yield enhancement' positions "
             "that harvested carry until volatility spiked, positions were force-closed, and losses "
             "became disastrous — anatomy of a blowup.",
    maths=[
        ("Short option exposure", r"$$\text{P\&L} = \text{premium} - \max(K - S_T, 0) \quad \text{unbounded on the left for FX}$$"),
    ],
    plain="Selling insurance on a fragile currency looks like income until the earthquake. The case "
          "study traces every step — the seductive carry, the margin call spiral, the forced unwind "
          "at the worst price — as a template for recognizing the trade in other costumes.",
),
"talk-fx-options-wrong-from-the-start": dict(
    overview="FX options are among the most liquid derivatives on earth, yet systematic valuation "
             "biases have persisted historically. The talk documents them and asks why arbitrage "
             "hasn't removed them.",
    maths=[
        ("The persistent finding", r"$$\sigma_{\text{impl}} \;\gtrsim\; \sigma_{\text{real}} \quad \text{systematically, especially for short-dated OTM}$$"),
    ],
    plain="A market can be huge, liquid and still mispriced for decades if the mispricing pays off "
          "slowly and blows up rarely. FX options are the standing counterexample to 'liquidity "
          "implies efficiency'.",
),
"talk-anomalies-and-opportunities-in-the-fx-option": dict(
    overview="Jessica James reviews the FX option market from its origins to today: where standard "
             "valuation has been wrong, which anomalies persist, and where the durable opportunities "
             "lie for systematic sellers and buyers.",
    maths=[
        ("Carry-to-vol connection", r"$$\text{forward premium} = r_d - r_f \quad\text{vs}\quad \text{realized drift} \Rightarrow \text{FX carry anomaly}$$"),
    ],
    plain="The history of FX options is a history of quoted prices disagreeing with statistics — "
          "and of the disagreement persisting because the natural buyers (hedgers) are not "
          "price-sensitive. Anomalies backed by structural flows die slowly.",
),
"talk-recent-trends-in-products-and-models-for-fx": dict(
    overview="Uwe Wystup on the FX derivatives market's evolution: dual currency investments, target "
             "forwards (TARFs) and other yield-enhancement structures reaching private banking, and "
             "the models needed to price and risk-manage them.",
    maths=[
        ("Target forward knockout", r"$$\text{TARF: accumulate } \sum_i \max(K - S_{t_i}, 0) \text{ until } \sum \ge \text{target} \Rightarrow \text{terminate}$$"),
    ],
    plain="Yield enhancement migrates down-market in every cycle: structures born on hedge fund desks "
          "end up in private-bank portfolios. Knowing the product zoo — and where each one hides its "
          "short option — is consumer protection for the buy side.",
),
"talk-a-market-design-to-trade-bundles-of": dict(
    overview="Market design meets derivatives: an exchange mechanism for trading bundles of securities "
             "directly, and its implications for the minimal exercise of American options.",
    maths=[
        ("Bundle auction allocation", r"$$\max \sum_j v_j\, x_j \quad \text{s.t.} \quad \sum_j A_{ij} x_j \le q_i$$"),
    ],
    plain="Exchanges match one instrument at a time, forcing traders to leg into packages with "
          "execution risk. A bundle market matches whole portfolios atomically — and changes when "
          "exercising an American option early is ever rational.",
),
"talk-jensen-probably-the-best-inequality-in-the": dict(
    overview="A love letter to Jensen's inequality: convexity as the mathematical source of option "
             "value, volatility drag, convexity adjustments and half the phenomena in quantitative "
             "finance.",
    maths=[
        ("Jensen's inequality", r"$$\mathbb{E}[f(X)] \;\ge\; f(\mathbb{E}[X]) \quad \text{for convex } f$$"),
        ("Its children", r"$$\text{option value} > \text{intrinsic}, \qquad \mathbb{E}[e^X] > e^{\mathbb{E}[X]}, \qquad \text{CMS convexity adj.}$$"),
    ],
    plain="Why does an option on the average beat the average of options? Why does volatility eat "
          "compound returns? Why do CMS swaps need adjusting? One inequality answers all of it: "
          "curvature plus randomness creates (or destroys) value.",
),
"talk-continuity-and-risk-randomness-path": dict(
    overview="An argument that randomness plus path continuity is a strange, almost contradictory "
             "request: examining what continuous-path models smuggle into risk management and what "
             "genuinely discontinuous markets do to hedging arguments.",
    maths=[
        ("The tension", r"$$\text{continuous paths} \Rightarrow \text{perfect hedging possible}; \qquad \text{jumps} \Rightarrow \text{incomplete markets}$$"),
    ],
    plain="Continuity is what lets delta hedging work perfectly in theory — and continuity is exactly "
          "what fails at every earnings release, devaluation and flash crash. The convenient "
          "assumption and the dangerous one are the same assumption.",
),
"talk-acceptability-applications-acceptability-and": dict(
    overview="Acceptability indices and choice theory: describing actions desirable to many agents at "
             "once (acceptability) versus optimal for a single agent (choice), with applications to "
             "pricing, hedging and performance measurement.",
    maths=[
        ("Acceptability via test measures", r"$$X \text{ acceptable at level } \gamma \iff \mathbb{E}^{\mathbb{Q}}[X] \ge 0 \;\; \forall\, \mathbb{Q} \in \mathcal{M}_\gamma$$"),
    ],
    plain="A trade one investor likes is a choice; a trade a whole family of stress-tested observers "
          "signs off on is acceptable. Grading trades by how demanding an audience they satisfy "
          "generalizes both arbitrage and Sharpe ratios.",
),
}

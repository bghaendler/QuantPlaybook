# Content for §5 Credit, XVA & Structured talks — consumed by enrich_talks.py
CONTENT = {

"talk-the-pricing-of-cdos-using-levy-copulas": dict(
    overview="A generic Lévy copula CDO pricing model incorporating skewness, kurtosis and jumps: a "
             "semi-dynamic generalization of the Gaussian setting that achieves better tranche fits by "
             "replacing the Normal with a shifted Gamma distribution.",
    maths=[
        ("One-factor Lévy setting", r"$$A_i = \sqrt{\rho}\, M + \sqrt{1-\rho}\, X_i, \qquad M, X_i \sim \text{shifted Gamma}$$"),
        ("Tranche expected loss", r"$$\mathbb{E}\!\left[ L_{[a,b]} \right] = \frac{\mathbb{E}[\min(L,b)] - \mathbb{E}[\min(L,a)]}{b-a}$$"),
    ],
    plain="The Gaussian copula couldn't fit the correlation smile because Gaussian factors have no "
          "skew and no jumps — the two things default clustering is made of. Swap in a Gamma-based "
          "Lévy factor and the same one-factor architecture suddenly fits all tranches at once.",
),
"talk-cdos-correlation-products-and-dangers": dict(
    overview="CDOs and correlation products from mechanics to menace: tranching, base correlation, "
             "correlation sensitivity of different tranches, and the dangers that materialized "
             "spectacularly in 2008.",
    maths=[
        ("Tranche correlation exposure", r"$$\frac{\partial\, \text{Equity}}{\partial \rho} < 0, \qquad \frac{\partial\, \text{Senior}}{\partial \rho} > 0$$"),
    ],
    plain="Equity tranche holders love dispersion (a few defaults, contained); senior holders die of "
          "correlation (everyone defaults together). The crisis was, in one sentence, the market "
          "discovering that mortgage correlation was close to one.",
),
"talk-the-credit-crunch-past-present-and-future": dict(
    overview="The 2007-08 credit crunch dissected: the securitization chain, funding runs, the role "
             "of models and ratings, and what the crisis implies for the future of credit markets and "
             "regulation.",
    maths=[
        ("The leverage spiral", r"$$\text{losses} \to \text{margin calls} \to \text{fire sales} \to \text{mark-downs} \to \text{losses}$$"),
    ],
    plain="A century of banking crises compressed into eighteen months: illiquid assets funded "
          "overnight, models that assumed housing never falls nationally, and a run not on banks "
          "but on the shadow system between them.",
),
"talk-contingent-capital-and-coco-bonds": dict(
    overview="Contingent convertibles from the ground up: the life of a CoCo, trigger types "
             "(mechanical vs discretionary), conversion mechanics, issuers and investors, the "
             "quantitative anatomy and the risk management of these instruments.",
    maths=[
        ("Equity-derivative CoCo valuation", r"$$V_{CoCo} = \text{bond} - \text{knock-in on trigger} + \text{conversion equity claim}$$"),
    ],
    plain="A CoCo is a bond that becomes equity exactly when you least want equity — when the bank is "
          "in trouble. Investors are paid handsomely to stand under that piano; the quant work is "
          "measuring the rope.",
),
"talk-cocos-the-new-kid-around-the-block": dict(
    overview="Wim Schoutens introduces contingent capital: what CoCos are, good boy or bad boy, the "
             "pros and cons for banks and the financial system, and first-generation pricing "
             "approaches.",
    maths=[
        ("Credit-derivative style pricing", r"$$s_{CoCo} \approx (1 - R_{\text{conv}})\, \lambda_{\text{trigger}} \quad\text{— trigger intensity replaces default intensity}$$"),
    ],
    plain="Regulators wanted banks that recapitalize themselves in a storm without taxpayer money; "
          "CoCos are that wish written as a security. Whether they stabilize or amplify a panic "
          "depends on details this talk lays bare.",
),
"talk-ito33-on-convertible-bonds-and-banking-cocos": dict(
    overview="ITO33's presentation of its services on convertible bonds and banking regulatory "
             "capital securities: two decades of convertible-bond analytics applied to the CoCo "
             "market.",
    maths=[
        ("Convertible decomposition (heuristic)", r"$$CB \approx \text{straight bond} + \text{equity call} - \text{issuer call} + \text{credit linkage}$$"),
    ],
    plain="Convertibles are the original hybrid — debt with an equity engine — and the software that "
          "prices them well must couple credit, equity and volatility in one PDE rather than bolt "
          "them together.",
),
"talk-volatility-inputs-for-convertible-bond": dict(
    overview="Convertible bond pricing with jump-to-default: the effect of credit spread, using "
             "volatility as an input versus implying it from CB market prices, and the exercise "
             "policies embedded in convertibles.",
    maths=[
        ("Jump-to-default equity dynamics", r"$$\frac{dS}{S} = (r + \lambda)\, dt + \sigma\, dW - dN_t, \qquad S \to 0 \text{ on default}$$"),
    ],
    plain="A convertible's equity option rides on a stock that can vanish. The jump-to-default "
          "coupling means credit spread and equity volatility are not separate inputs but two "
          "faces of the same calibration.",
),
"talk-convertible-bond-coding-workshop-paul": dict(
    overview="Wilmott codes a convertible bond pricer live: the explicit finite-difference method in "
             "Excel/VBA, handling conversion, call and put features on a grid — a complete build "
             "from equation to working spreadsheet.",
    maths=[
        ("CB free-boundary conditions", r"$$V \ge \kappa S \;\text{(conversion)}, \qquad V \le \max(C_{\text{call}}, \kappa S), \qquad V \ge P_{\text{put}}$$"),
    ],
    plain="Watching a model get coded teaches what papers hide: boundary conditions, grid choices, "
          "stability limits. By the end there's a working convertible pricer and — more valuable — "
          "the habit of testing every line against intuition.",
),
"talk-joint-calibration-the-case-of-bank": dict(
    overview="Jointly calibrating all securities of one issuer — equity, CDS, senior debt, AT1 CoCos "
             "— with one parsimonious model: seldom achieved, seldom even discussed, yet a "
             "prerequisite for honest capital-structure risk management.",
    maths=[
        ("One issuer, one model", r"$$\{S, \text{CDS}(T), \text{bonds}, \text{AT1}\} \;=\; f(\text{firm value}, \lambda, \sigma; \theta) \quad \text{single } \theta$$"),
    ],
    plain="Banks' securities are priced by different desks with different models that quietly "
          "contradict each other. Calibrating the whole capital structure at once exposes which "
          "instrument is rich, which is cheap — and when the equity and credit markets disagree "
          "about survival itself.",
),
"talk-mva-margin-valuation-adjustment": dict(
    overview="Andrew Green introduces MVA: the funding cost of posting initial margin over the life "
             "of a cleared or bilateral trade, its computation via simulated ISDA SIMM/CCP margin, "
             "and its role in the XVA family.",
    maths=[
        ("MVA definition", r"$$\text{MVA} = \int_0^T f_s\, \mathbb{E}^{\mathbb{Q}}\!\left[ \text{IM}_s \right] e^{-\int_0^s r_u du}\, ds$$"),
    ],
    plain="Initial margin is cash locked in a box for the trade's lifetime; someone funds that box. "
          "MVA prices the box-funding into the trade — and since margin models are risk-sensitive, "
          "computing it means simulating a risk model inside a pricing model.",
),
"talk-revisiting-fva-shareholder-and-bondholder": dict(
    overview="Green revisits FVA through shareholder versus bondholder value: why funding costs create "
             "a wealth transfer between them, the resulting FVA accounting debates, and model "
             "implications.",
    maths=[
        ("FVA (symmetric form)", r"$$\text{FVA} = \int_0^T s^{\text{fund}}_u\, \mathbb{E}^{\mathbb{Q}}\!\left[ (V_u - C_u) \right] e^{-ru}\, du$$"),
    ],
    plain="When a bank funds an uncollateralized trade at its own spread, who pays — the client, the "
          "shareholders or the bondholders? FVA is the accounting shadow of that question, and the "
          "answer changes what 'fair value' means.",
),
"talk-capital-valuation-adjustments-kva": dict(
    overview="Should derivative values be adjusted for the cost of regulatory capital? KVA: measuring "
             "lifetime capital consumption of a trade, the hurdle rate on that capital, and the "
             "circumstances where the adjustment bites.",
    maths=[
        ("KVA definition", r"$$\text{KVA} = \int_0^T \gamma_h\, \mathbb{E}^{\mathbb{Q}}\!\left[ K_u \right] e^{-\int_0^u r ds}\, du, \qquad \gamma_h = \text{capital hurdle}$$"),
    ],
    plain="A trade that ties up regulatory capital for ten years must out-earn the shareholders' "
          "required return on that capital, or it destroys value even if 'profitable'. KVA moves "
          "that constraint from annual budgeting into the price itself.",
),
"talk-derivatives-funding-netting-and-accounting": dict(
    overview="Mats Kjaer's rigorous treatment of derivatives funding: netting sets, funding strategies "
             "and the consistency between XVA models and accounting statements — a balance-sheet view "
             "of derivative pricing.",
    maths=[
        ("Balance-sheet consistent value", r"$$V = V_{\text{risk-free}} - \text{CVA} + \text{DVA} - \text{FVA} \quad\text{tied to ledger entries}$$"),
    ],
    plain="XVA formulas float free until they must reconcile with the bank's actual books. Deriving "
          "them from the balance sheet — cash accounts, funding legs, netting sets — settles debates "
          "that stipulated formulas cannot.",
),
"talk-risk-aware-otc-pricing-using-xva-getting": dict(
    overview="Getting ready for the 'new normal' of OTC derivatives: an integrated tour of CVA, DVA, "
             "FVA, ColVA, KVA and MVA — risk-aware pricing where the trade's lifetime costs enter at "
             "inception.",
    maths=[
        ("The XVA stack", r"$$V = V_{\text{clean}} - \text{CVA} + \text{DVA} - \text{FVA} - \text{MVA} - \text{KVA}$$"),
    ],
    plain="A derivative's price used to be its expected payoff; now it is that minus the lifetime "
          "cost of counterparty risk, funding, margin and capital. The clean price is the beginning "
          "of the negotiation, not the end.",
),
"talk-deploying-an-ai-based-xva-platform-into": dict(
    overview="Riskfuel's Ryan Ferguson and Scotiabank's Andrew Green on lessons from deploying "
             "AI-accelerated valuation models into a production XVA platform: training, validation, "
             "governance and the million-fold speedups achieved.",
    maths=[
        ("Neural surrogate", r"$$V_{\text{NN}}(x) \approx V_{\text{model}}(x), \qquad \text{speedup} \sim 10^6, \quad \|V_{\text{NN}} - V\| < \text{tol on domain}$$"),
    ],
    plain="XVA needs millions of valuations per night; traditional pricers can't keep up. Train a "
          "network to imitate the pricer and the bottleneck disappears — the hard part is proving "
          "to model validation that the imitation never wanders off script.",
),
"talk-loan-pricing-arbitrage-free-models-with": dict(
    overview="Ho and Lee on arbitrage-free loan pricing with credit risk: a framework consistent with "
             "financial accounting in income simulations, with neural networks handling the "
             "data-intensive behavioural components.",
    maths=[
        ("Loan value with credit and behaviour", r"$$V = \mathbb{E}\!\left[ \sum_i CF_i\, e^{-\int r + \lambda\, ds} \right], \qquad CF_i = f(\text{prepay}, \text{draw}, \text{default})$$"),
    ],
    plain="Loans are derivatives on customer behaviour — prepayment, drawdown, default — priced "
          "against accounting income rather than market quotes. Arbitrage-free discipline plus ML "
          "behaviour models bridges the trading book and the banking book.",
),
"talk-fourier-based-methods-for-the-management-of": dict(
    overview="Laura Ballotta's framework for complex life-insurance contracts as portfolios of "
             "embedded options activated by triggering events, valued and risk-managed with "
             "Fourier-transform methods.",
    maths=[
        ("Fourier valuation kernel", r"$$V = \frac{e^{-rT}}{2\pi} \int_{\mathbb{R}} \hat{\Pi}(u)\, \phi_{X_T}(-u)\, du$$"),
    ],
    plain="A with-profits policy or variable annuity is a bundle of exotic options in actuarial "
          "clothing. Characteristic-function methods price the whole bundle under realistic "
          "(jumpy, skewed) dynamics fast enough for hedging, not just reporting.",
),
"talk-multivariate-additive-subordination-with": dict(
    overview="A multivariate additive-subordination model: time-changing Lévy processes with additive "
             "clocks to capture implied volatility surfaces and time-varying correlation between "
             "assets, for pricing, scenario analysis and risk management.",
    maths=[
        ("Additive subordination", r"$$Y_i(t) = X_i\big(T_i(t)\big), \qquad T_i = \text{additive (time-inhomogeneous) clock, partly common}$$"),
    ],
    plain="Assets share busy days: a common stochastic clock creates correlation that strengthens in "
          "turmoil, exactly as markets do. Making the clock additive (not stationary) lets the model "
          "also match how surfaces vary across maturities.",
),
"talk-the-p2p-pandemic-swap-decentralized-pandemic": dict(
    overview="Daniel Linders proposes the P2P pandemic swap: pandemic-linked securities providing "
             "risk management through solidarity between countries and risk transfer to financial "
             "markets, in the spirit of cat bonds.",
    maths=[
        ("Parametric trigger payout", r"$$\text{payout}_i = f\!\left( I_i(t) \right) \;\text{vs pooled premium} \quad I = \text{infection/severity index}$$"),
    ],
    plain="Pandemics hit countries asynchronously, which is exactly what makes them insurable "
          "peer-to-peer: today's spared fund today's stricken, with capital markets absorbing the "
          "tail where everyone is hit at once.",
),
"talk-risk-sharing-pension-plans": dict(
    overview="Mary Hardy adapts theoretical pension-design results to a practical target-benefit "
             "plan with structured, transparent intergenerational risk sharing between cohorts of "
             "members.",
    maths=[
        ("Target benefit adjustment", r"$$B_{t+1} = B_t \cdot g\!\left( FR_t \right), \qquad g \text{ smooths funding shocks across cohorts}$$"),
    ],
    plain="Pure DB dumps risk on sponsors; pure DC dumps it on whoever retires in a crash. "
          "Target-benefit designs spread shocks across generations by rule rather than by "
          "renegotiation — fairer, and actuarially calmer.",
),
"talk-more-wealth-in-retirement-asset-location": dict(
    overview="Optimal asset location across taxable, tax-deferred and tax-exempt (Roth) accounts: "
             "which assets belong in which wrapper, and how much retirement wealth good location "
             "adds over good allocation alone.",
    maths=[
        ("Location principle", r"$$\text{high-tax assets} \to \text{sheltered accounts}, \qquad \Delta W \approx 0.1\text{-}0.5\%/\text{yr}$$"),
    ],
    plain="Allocation decides what you hold; location decides where. Putting bonds where interest is "
          "sheltered and equities where gains are favoured is a free lunch worth tens of basis "
          "points a year — compounding to real money over a career.",
),
"talk-potential-impacts-of-the-covid-19-pandemic": dict(
    overview="A quantitative study of COVID-era market movements' impact on private wealth "
             "management, at both the product level (structured products, guarantees) and the "
             "portfolio level.",
    maths=[
        ("Barrier breach cascade", r"$$S \downarrow 30\% \Rightarrow \text{autocall/barrier products knock in} \Rightarrow \text{client losses realize}$$"),
    ],
    plain="March 2020 stress-tested every yield-enhancement product sold to private banking clients "
          "in the preceding decade. The study measures what broke, what held, and what the episode "
          "teaches about product suitability.",
),
}

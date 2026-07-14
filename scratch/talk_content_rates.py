# Content for §4 Rates & Fixed Income talks — consumed by enrich_talks.py
CONTENT = {

"talk-what-short-rate-model-should-i-use": dict(
    overview="Thirty years of short-rate modelling assessed: Vasicek, CIR, Ho-Lee, Hull-White, "
             "Black-Karasinski and beyond — the strengths, weaknesses and use-cases of each, and how "
             "to choose for a given pricing or risk task.",
    maths=[
        ("The family tree", r"$$dr = \kappa(\theta_t - r)\,dt + \sigma r^{\gamma}\, dW, \qquad \gamma = 0 \text{ (HW)},\ \tfrac{1}{2} \text{ (CIR)},\ 1 \text{ (BK, lognormal)}$$"),
        ("Hull-White fit to the curve", r"$$\theta_t = \partial_T f(0,t) + \kappa f(0,t) + \frac{\sigma^2}{2\kappa}\left(1 - e^{-2\kappa t}\right)$$"),
    ],
    plain="No short-rate model wins everywhere: Hull-White fits the curve and gives closed forms but "
          "allows negative rates; lognormal models fix that and lose tractability. The right question "
          "is never 'which is true' but 'which failure mode can this desk live with'.",
),
"talk-libor-dont-fallback-step-forward": dict(
    overview="Marc Henrard on the discontinuation of LIBOR: the fallback protocols, their valuation "
             "consequences, and his argument for stepping forward to cleanly-defined new products "
             "rather than falling back onto adjusted legacy terms.",
    maths=[
        ("ISDA fallback rate", r"$$R_{\text{fallback}} = \text{compounded RFR in arrears} + \text{fixed spread (5y median)}$$"),
    ],
    plain="Trillions of contracts referenced a number that stopped existing. The fallback bolts a "
          "backward-looking compounded rate plus a frozen spread onto forward-looking contracts — "
          "workable, but with value transfers and risk quirks this talk itemizes.",
),
"talk-swap-rate-fallback-unreasonable": dict(
    overview="The swap-rate (ICE Swap Rate) fallback analyzed: canceling effects that make crude "
             "approximations unreasonably effective, the residual exotic features, and a proposed "
             "adjusted mechanism that simplifies risk management of the legacy book.",
    maths=[
        ("Fallback swap rate approximation", r"$$S_{\text{fallback}} \approx \frac{(1 + \delta S_{\text{RFR}})^{n} \text{ adjustments}}{\text{annuity ratio}} \;\approx\; S_{\text{RFR}} + \text{spread terms}$$"),
    ],
    plain="When the reference swap rate died, its fallback formula turned every legacy swaption into "
          "a small exotic. The talk shows why the errors of the simple approximation largely cancel "
          "— and how a modest redesign would remove the exotic residue entirely.",
),
"talk-swap-rate-a-la-stock-bermudan-swaptions-made": dict(
    overview="Gątarek's reduction: Markovian projection plus judicious parameter freezing collapses a "
             "full volatility interest-rate model into a minimal form where the swap rate evolves like "
             "a dividend-paying stock — making Bermudan swaptions easy.",
    maths=[
        ("Markovian projection", r"$$dS_t = \sigma(t, S_t)\, dW_t, \qquad \sigma^2(t,x) = \mathbb{E}\!\left[ \Sigma_t^2 \,\middle|\, S_t = x \right]$$"),
    ],
    plain="A Bermudan swaption in a full LMM is a high-dimensional monster. Project the swap rate "
          "onto a one-factor process that matches its marginals and the monster becomes an American "
          "option on a 'stock' — solvable on a lattice in milliseconds.",
),
"talk-ois-and-its-impact-on-modelling-calibration": dict(
    overview="The move to OIS discounting after the crisis: what it changed in curve construction, "
             "model calibration and the funding of OTC derivatives, and why collateral agreements "
             "dictate the discount curve.",
    maths=[
        ("Collateralized derivative value", r"$$V_t = \mathbb{E}^{\mathbb{Q}}\!\left[ e^{-\int_t^T c_s\, ds}\, V_T \right], \qquad c = \text{collateral (OIS) rate}$$"),
    ],
    plain="Who funds a trade decides its discount rate. Collateralized trades earn the OIS rate on "
          "posted cash, so OIS — not LIBOR — is their time value of money. That one observation "
          "rebuilt every swap curve on the street.",
),
"talk-bond-futures-delivery-option-with-term": dict(
    overview="Henrard on bond futures: a 'vanilla' product hiding a complex delivery option — cheapest "
             "-to-deliver switching — whose pricing requires a full term-structure model to capture "
             "correlation between deliverable bonds.",
    maths=[
        ("Futures invoice relation", r"$$\text{Invoice} = F \times CF_i + \text{accrued}, \qquad \text{CTD} = \arg\min_i \left( P_i - F\, CF_i \right)$$"),
    ],
    plain="A bond future is an option in disguise: the short chooses which bond to deliver, and that "
          "choice flips as yields move through conversion-factor break-evens. Pricing the switch "
          "needs the whole curve to move realistically, not just one bond.",
),
"talk-revisiting-elastic-string-models-of-forward": dict(
    overview="Twenty-five years after the original papers: the forward curve as an elastic string "
             "along which shocks propagate, revisited against modern data on the correlation of "
             "returns across maturities.",
    maths=[
        ("String/random-field dynamics", r"$$df(t,T) = \alpha(t,T)\,dt + \sigma(t,T)\, dW(t,T), \qquad \operatorname{corr}\big(dW(t,T_1), dW(t,T_2)\big) = c(|T_1 - T_2|)$$"),
    ],
    plain="HJM shakes the whole curve with a handful of factors; a string model lets every maturity "
          "have its own noise, tied to neighbours by elasticity. The data — a stubbornly local "
          "correlation structure — keeps voting for the string.",
),
"talk-the-market-price-of-risk-fear-and-greed-in": dict(
    overview="Wilmott's 2007 lecture on stochastic spot-rate models: interest rate risk, the market "
             "price of risk λ, and how fear and greed enter fixed-income pricing through the risk "
             "adjustment in the bond equation.",
    maths=[
        ("Market price of risk", r"$$\mu_V - r V = \lambda\, \sigma_V \quad\text{for every rate-dependent asset}$$"),
    ],
    plain="Bonds can't be hedged with the rate itself (you can't hold 'the short rate'), so risk "
          "preferences survive into prices through λ — the price of a unit of interest-rate fear. "
          "Estimating it is half econometrics, half psychology.",
),
"talk-beyond-convexity": dict(
    overview="Jessica James on super-long bonds in the near-zero yield era: century tenors where the "
             "standard duration-plus-convexity expansion fails and higher-order terms are required to "
             "describe returns.",
    maths=[
        ("Price expansion", r"$$\frac{\Delta P}{P} = -D\,\Delta y + \tfrac{1}{2} C\, \Delta y^2 + \tfrac{1}{6} T_3\, \Delta y^3 + \cdots$$"),
    ],
    plain="For a 100-year bond at 0.5% yield, the 'small' third-order term is not small: duration and "
          "convexity alone misstate returns badly. Ultra-long, ultra-low bonds live in the part of "
          "the Taylor series everyone else truncates.",
),
"talk-beyond-convexity-ii": dict(
    overview="The sequel: empirical behaviour of very long dated bonds when yields were near zero, "
             "the extra mathematical terms needed beyond duration and convexity, and practical "
             "consequences for portfolio hedging.",
    maths=[
        ("Higher-order sensitivity", r"$$T_3 = \frac{1}{P}\frac{\partial^3 P}{\partial y^3} \;\sim\; T^3 \quad\text{— cubic in tenor}$$"),
    ],
    plain="Part two brings the data: realized returns of Austria's 100-year bond and friends, showing "
          "the cubic term earning (and losing) real money that a duration-convexity book cannot even "
          "see.",
),
"talk-the-impact-of-carry-and-roll-down-on-macro": dict(
    overview="Decomposing macro fixed-income returns into carry (yield accrual) and roll-down (riding "
             "the curve), and quantifying how much of long-run bond strategy performance these "
             "'static' components explain.",
    maths=[
        ("Return decomposition", r"$$R \approx \underbrace{y\,\Delta t}_{\text{carry}} + \underbrace{-D\,(y_{T-\Delta t} - y_T)}_{\text{roll-down}} + \underbrace{-D\,\Delta y}_{\text{curve moves}}$$"),
    ],
    plain="A bond earns three ways: coupon time, sliding down a steep curve, and luck on rate moves. "
          "The first two are visible today — and historically they explain an embarrassing share of "
          "what gets marketed as macro skill.",
),
"talk-the-rise-of-carry": dict(
    overview="Coldiron, Lee and Lee on carry as the organizing principle of modern markets: how carry "
             "trades drive liquidity, credit creation and the pattern of market returns — and why "
             "carry regimes end in synchronized unwinds.",
    maths=[
        ("The carry trade archetype", r"$$\text{P\&L} = (y_{\text{high}} - y_{\text{low}})\,\Delta t - \text{drawdown risk} \quad\text{(short volatility in disguise)}$$"),
    ],
    plain="Selling insurance, funding EM bonds with yen, harvesting VIX roll-down — all one trade: "
          "steady income for occasional catastrophe. The book's thesis: this trade has become the "
          "market's backbone, so its unwinds are now systemic events, not sideshows.",
),
"talk-a-systematic-fixed-income-process-delivering": dict(
    overview="Designing next-generation systematic fixed income: factor definitions that survive "
             "bond-market microstructure (liquidity, issuance patterns), and a process delivering "
             "both scalable index-plus and bespoke portfolio solutions.",
    maths=[
        ("Bond factor score", r"$$s_i = w_V\, \text{value}_i + w_M\, \text{momentum}_i + w_C\, \text{carry}_i + w_Q\, \text{quality}_i$$"),
    ],
    plain="Equity factor investing translated to bonds — where trading costs are brutal and half the "
          "universe barely trades. The craft is in implementation: turnover control, liquidity "
          "screens and issuer-level aggregation rather than raw signal chasing.",
),
"talk-market-impact-and-optimal-execution-in-fixed": dict(
    overview="Execution-cost modelling in fixed income: why equity-style impact models fail for bonds, "
             "the data challenges (RFQ markets, sparse prints), and machine-learning approaches to "
             "impact and optimal execution.",
    maths=[
        ("Square-root impact baseline", r"$$\Delta P \approx Y\, \sigma \sqrt{\frac{Q}{V}} \quad\text{— and where it breaks in RFQ markets}$$"),
    ],
    plain="In equities you watch a tape; in bonds you ask five dealers and reveal your hand by "
          "asking. Impact modelling becomes a game-theory-plus-ML problem: what did the asking cost, "
          "and whom should you have asked?",
),
"talk-qi-machine-learning-methods-for-market": dict(
    overview="Edith Mandel on ML for market-making and execution in fixed income: order-flow "
             "modelling, quote optimization and execution scheduling in dealer markets, from the "
             "Quant Insights ML conference.",
    maths=[
        ("Quote optimization objective", r"$$\max_{\delta^{bid}, \delta^{ask}} \; \mathbb{E}\left[ \text{spread capture} \right] - \gamma\, \operatorname{Var}\left[ \text{inventory P\&L} \right]$$"),
    ],
    plain="A corporate-bond market maker sees a fraction of the market a fraction of the time. ML "
          "earns its keep by imputing the missing picture — fair value between trades — so quotes "
          "can be tight without being picked off.",
),
"talk-enhanced-prediction-of-sovereign-bond": dict(
    overview="Forecasting sovereign bond spreads with macroeconomic news sentiment: constructing "
             "sentiment indices from news flow and demonstrating incremental predictive power over "
             "standard macro variables.",
    maths=[
        ("Spread regression with sentiment", r"$$\Delta s_{i,t+1} = \alpha + \beta^\top X_{i,t} + \gamma\, \text{Sent}_{i,t} + \varepsilon, \qquad \gamma \ne 0$$"),
    ],
    plain="Bond spreads react to the story as well as the statistics: news tone about a country moves "
          "its borrowing cost before the hard data confirms. Quantified sentiment is the early, noisy "
          "echo of next quarter's fundamentals.",
),
"talk-repo-rates-and-short-selling-restrictions": dict(
    overview="The repo market as the plumbing of short selling: special repo rates, the cost of "
             "shorting bonds, and how short-selling restrictions propagate into derivatives pricing "
             "and basis trades.",
    maths=[
        ("Specialness in the forward", r"$$F = S\, e^{(r_{\text{repo}} - y)T} \qquad r_{\text{special}} < r_{GC} \Rightarrow \text{shorting costs carry}$$"),
    ],
    plain="To short a bond you must borrow it, and the borrowing fee (repo specialness) is a shadow "
          "price on negative opinions. When a bond goes 'special', every arbitrage relationship "
          "involving it quietly shifts.",
),
"talk-quantifying-fissures-in-the-us-high-yield": dict(
    overview="A model connecting central-bank balance-sheet size to risky asset performance, applied "
             "to detecting stress fissures in the US high-yield market before they widen into "
             "spread blowouts.",
    maths=[
        ("Liquidity-driven spread model", r"$$s_{HY,t} = f\!\left( \Delta \text{CB balance sheet}_t,\ \text{defaults}_t,\ \text{flows}_t \right)$$"),
    ],
    plain="High yield floats on central-bank liquidity: when the balance sheet tide goes out, the "
          "weakest credits crack first. Watching the tide, not the swimmers, gives the earlier "
          "signal.",
),
"talk-long-term-market-model": dict(
    overview="Modelling interest rates over multi-decade horizons: combining term-structure dynamics "
             "with macroeconomic anchoring so that simulated curves remain plausible for pension and "
             "insurance applications.",
    maths=[
        ("Long-horizon anchoring", r"$$r_t \to \theta_{\infty} \;\text{(macro anchor)}, \qquad \text{sim horizon} \gg \text{calibration window}$$"),
    ],
    plain="A trading model needs to be right for a month; an ALM model must be sane for fifty years. "
          "That flips the design priorities: economic plausibility and mean levels dominate, smile "
          "fitting recedes.",
),
"talk-modelling-banking-book-portfolios": dict(
    overview="Forecasting balance and income for banking-book portfolios: behavioural modelling of "
             "deposits, prepayment of mortgages, and product-specific considerations for interest-rate "
             "risk in the banking book (IRRBB).",
    maths=[
        ("Non-maturity deposit modelling", r"$$\text{core deposits} = \text{stable fraction} \times \text{balance}, \qquad \text{repricing beta } \beta < 1$$"),
    ],
    plain="A checking account has no maturity, yet behaves like a long-dated bond because customers "
          "are sticky and rates pass through slowly. Modelling that behaviour — not any contract — "
          "is what banking-book risk management actually is.",
),
"talk-balance-sheet-risk-and-return-analysis": dict(
    overview="Applying Markowitz's risk-return framework to whole depository institutions: systematic "
             "balance-sheet optimization for banks that habitually take risk but rarely analyze it "
             "portfolio-style.",
    maths=[
        ("Balance-sheet frontier", r"$$\max_w\; \text{NII}(w) - \tfrac{\gamma}{2}\, w^\top \Sigma w \quad \text{s.t. regulatory and liquidity constraints}$$"),
    ],
    plain="A bank is a leveraged fixed-income portfolio with a marketing department. Treating the "
          "balance sheet as a portfolio-selection problem exposes concentrations and mispriced "
          "risks that product-by-product management never sees.",
),
"talk-case-study-bank-of-americas-credit-card": dict(
    overview="Case study: Bank of America's credit-card receivables — their impact on net interest "
             "income, impairment dynamics, and the interest-rate hedging and funding of a revolving "
             "consumer-credit book.",
    maths=[
        ("Receivables economics", r"$$\text{NII} = \text{APR} \times B - \text{funding} - \text{expected charge-offs}$$"),
    ],
    plain="A credit-card book is a floating-rate asset with embedded behavioural options: customers "
          "revolve, transact, default and attrite. The case study walks through how a real bank "
          "measures and hedges that bundle.",
),
"talk-bank-of-america-credit-card-receivables": dict(
    overview="Juan Ramirez on the accounting and hedging implications of poor prepayment modelling in "
             "credit-card receivables: how behavioural model error propagates into hedge accounting "
             "and earnings volatility.",
    maths=[
        ("Prepayment-sensitive duration", r"$$D_{\text{eff}} = D(\text{CPR}), \qquad \delta \text{CPR} \Rightarrow \text{hedge mismatch} \Rightarrow \text{P\&L noise}$$"),
    ],
    plain="Get customer prepayment behaviour wrong and your 'perfect' interest-rate hedge hedges a "
          "portfolio that doesn't exist — the error resurfaces as unexplained earnings volatility "
          "with accounting consequences.",
),
"talk-asset-liability-models-that-are-useful-in": dict(
    overview="A tutorial on asset-liability models for pension funds and insurers that are actually "
             "useful in practice: scenario generation, liability-driven objectives, and the gap "
             "between textbook ALM and board-room decisions.",
    maths=[
        ("Funding ratio dynamics", r"$$FR_t = \frac{A_t}{L_t}, \qquad \text{objective: } \mathbb{P}(FR_T < 1) \le \varepsilon$$"),
    ],
    plain="Pension ALM is a race between two portfolios — assets you choose and liabilities you owe "
          "— driven by the same rates. Useful models keep the liability side honest and express "
          "risk as probability of failing people, not variance of returns.",
),
}

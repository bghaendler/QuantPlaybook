# Content for §13 Microstructure & Algo Trading and §14 Risk Management talks
# NOTE: talk-trend-following absent (pre-existing hand-built page).
CONTENT = {

# ------------------------------------------------------------- microstructure
"talk-the-science-and-practice-of-trend-following": dict(
    overview="Artur Sepp describes three trend-following system approaches and represents their "
             "expected returns through the stochastic-process features of financial returns — "
             "autocorrelation, vol clustering, tails.",
    maths=[
        ("Trend P&L driver", r"$$\mathbb{E}[\text{P\&L}] \propto \sum_{k} \rho_k \quad\text{— cumulative return autocorrelation}$$"),
        ("Convexity signature", r"$$\text{trend returns} \sim \text{long straddle on the market's drift}$$"),
    ],
    plain="Trend following is long convexity in disguise: it loses small and often in chop, wins "
          "large in sustained moves. Its profitability is a measurable statement about return "
          "autocorrelation — not a mystery, a moment condition.",
),
"talk-option-orderbooks-from-ai-agents-to-self": dict(
    overview="Modelling limit order books for options: recent approaches spanning single-symbol LoBs "
             "to chains of option books on one underlying, including AI-agent-based and "
             "self-similarity perspectives.",
    maths=[
        ("Coupled option books", r"$$\text{LoB}_{K_1,T_1} \leftrightarrow \text{LoB}_{K_2,T_2} \quad\text{via shared underlying and market makers}$$"),
    ],
    plain="An option chain is hundreds of order books handcuffed together by no-arbitrage — quote "
          "one, constrain them all. Modelling them jointly, with learning agents as market makers, "
          "reproduces microstructure that isolated models miss.",
),
"talk-do-spikes-make-it-harder-to-find-profitable": dict(
    overview="Stephen Weston's novel spike model embedded in an agent-based limit-order-book "
             "framework: whether price spikes destroy or merely obscure profitable patterns in LoB "
             "data.",
    maths=[
        ("Spike-augmented dynamics", r"$$dP = \text{LoB flow} + J\, dN_t, \qquad N = \text{spike arrivals}$$"),
    ],
    plain="Spikes are pattern-killers for naive models: they dominate the loss function and drown "
          "the signal. Modelling them explicitly as their own process lets the subtler order-book "
          "patterns re-emerge, tradable again.",
),
"talk-are-spikes-and-shocks-making-value-and-risk": dict(
    overview="Weston on recent price spikes across markets: whether spikes and shocks are making "
             "value and risk genuinely less predictable, and what that means for models built on "
             "smoother eras.",
    maths=[
        ("Regime comparison", r"$$\frac{\#\{\text{moves} > 5\sigma\}_{\text{recent}}}{\#\{\text{moves} > 5\sigma\}_{\text{past}}} \gg 1$$"),
    ],
    plain="Five-sigma days arrive more often than they used to — electronic liquidity vanishes "
          "faster than human liquidity did. Models calibrated to the smooth past systematically "
          "understate both tails and the speed at which they open.",
),
"talk-guidelines-for-building-a-realistic": dict(
    overview="A bottom-up approach to market simulation for backtesting algorithmic trading with "
             "market impact: agent-based simulator design guidelines that make strategy tests "
             "honest.",
    maths=[
        ("Impact-aware backtest", r"$$\text{fill price} = P_{\text{mid}} + \text{spread}/2 + I(Q, \text{depth}) \quad\text{— never the printed price}$$"),
    ],
    plain="A backtest that fills you at the printed price is fiction: your order would have moved "
          "that price. Simulating the book's reaction — agents, queues, impact — is the difference "
          "between testing a strategy and flattering it.",
),
"talk-a-market-impact-model-that-works": dict(
    overview="Market impact of large trades — the least researched input to optimal rebalancing — "
             "modelled rationally: functional forms, empirical calibration and integration into "
             "portfolio optimization.",
    maths=[
        ("Square-root law", r"$$I = Y\, \sigma\, \sqrt{\frac{Q}{V}} \quad\text{— remarkably universal across markets}$$"),
    ],
    plain="Impact follows a square root of trade size with eerie universality — stocks, futures, "
          "even bitcoin. One robust law, properly calibrated, converts 'can we trade this idea at "
          "size' from folklore into arithmetic.",
),
"talk-modelling-intraday-risk-and-flow-co-movement": dict(
    overview="Intraday risk and order-flow co-movement modelled jointly to improve trading "
             "performance: intraday covariance dynamics and cross-asset flow spillovers.",
    maths=[
        ("Intraday covariance profile", r"$$\Sigma(t_{\text{day}}) = \text{U-shaped in volume and vol} \quad\text{— risk is time-of-day dependent}$$"),
    ],
    plain="Ten a.m. and three-thirty p.m. are different markets: risk, liquidity and flow "
          "correlations all follow the intraday clock. Execution that respects the clock beats "
          "execution that treats the day as homogeneous.",
),
"talk-doing-more-with-tick-data-a-machine-learning": dict(
    overview="Signal research on tick data: huge datasets, flawed history, trade-flow imbalance "
             "features, execution-cost modelling and accurate timestamping — an ML approach to "
             "intraday signals.",
    maths=[
        ("Order flow imbalance", r"$$\text{OFI}_t = \sum_{\tau \in t} \left( \Delta B_\tau - \Delta A_\tau \right) \quad\text{— strongest short-horizon predictor}$$"),
    ],
    plain="At tick scale the best predictor of the next move is pressure in the book, not price "
          "history. The craft is industrial: cleaning corrupt ticks, aligning clocks and keeping "
          "the model honest about the costs of acting on microseconds.",
),
"talk-price-destabilizing-speculation-the-role-of": dict(
    overview="Suman Banerjee shows that under quantity competition with few strategic sellers, a "
             "large speculator with storage access can destabilize prices and profit — strategic "
             "limit orders as a manipulation channel.",
    maths=[
        ("Manipulation profitability", r"$$\pi_{\text{spec}} = \text{buy low (induced)} \to \text{store} \to \text{sell high (induced)} > 0$$"),
    ],
    plain="Textbooks say speculators stabilize prices by buying low and selling high; with market "
          "power and a warehouse, the arrow reverses — they can manufacture the very swings they "
          "profit from. Regulation's interest follows directly.",
),
"talk-market-maker-positioning-and-the-recent": dict(
    overview="Hari Krishnan on the February-March 2020 meltdown: how options market-maker (dealer) "
             "positioning — short gamma dynamics — amplified the violence of the equity crash.",
    maths=[
        ("Dealer hedging feedback", r"$$\text{dealers short } \Gamma \Rightarrow \text{sell into declines}: \; \Delta_{\text{hedge}} \propto \Gamma \cdot \Delta S$$"),
    ],
    plain="When dealers are short gamma, their hedging chases the market — selling falls, buying "
          "rallies — turning them into amplifiers. Reading dealer positioning tells you when the "
          "market's shock absorbers have become shock generators.",
),
"talk-cost-effective-composite-forex-and-us": dict(
    overview="Building composite FX and US equity feeds by combining OTC feeds 'in the best possible "
             "way' mathematically: outlier-robust aggregation for cost-effective reference pricing.",
    maths=[
        ("Robust composite mid", r"$$P_{\text{comp}} = \text{median}_i\!\left( P^{\text{mid}}_i \right) \;\text{with staleness and outlier filters}$$"),
    ],
    plain="Ten cheap noisy feeds, properly cleaned and medianed, rival one expensive golden feed. "
          "The mathematics of robust aggregation is the difference between a bargain and garbage.",
),
"talk-risk-budgeting-and-machine-learning-for-fx": dict(
    overview="PARIS, a benchmark FX three-factor model: carry, value and momentum style factors, "
             "their time-series and cross-sectional contributions across currencies, with risk "
             "budgeting and ML enhancements.",
    maths=[
        ("FX factor decomposition", r"$$R_{\text{ccy}} = \beta_C\, F_{\text{carry}} + \beta_V\, F_{\text{value}} + \beta_M\, F_{\text{mom}} + \alpha$$"),
    ],
    plain="Three styles explain most systematic currency returns; the residual is where managers "
          "claim skill. A public benchmark model makes that claim testable — and risk budgeting "
          "keeps the three engines from all stalling at once.",
),
"talk-agent-based-models-in-finance-foundations": dict(
    overview="An introduction to agent-based modelling in finance: stochastic simulation of "
             "heterogeneous interacting investors that reproduces real-world trading patterns no "
             "representative-agent model can.",
    maths=[
        ("Heterogeneous agent dynamics", r"$$P_{t+1} = f\!\left( \sum_i d_i(P_t, \text{state}_i) \right), \qquad d_i = \text{agent demand rules}$$"),
    ],
    plain="Fat tails, volatility clustering and bubbles emerge spontaneously when you simulate "
          "chartists, fundamentalists and noise traders jostling — the 'anomalies' are what "
          "interaction looks like. No shocks from outside required.",
),
"talk-agents-provocateurs-quant-finances-next": dict(
    overview="Panel: the case that quant finance's next evolution must incorporate agent-based "
             "modelling — for stress testing, market impact and understanding endogenous risk.",
    maths=[],
    plain="Equilibrium models assume the crowd away; 2008, 2010 and 2020 were the crowd. The panel "
          "debates whether ABMs are ready to be regulatory and desk tools rather than academic "
          "curiosities.",
),
"talk-anticipating-the-anticipations-of-others": dict(
    overview="Grant Fuller on Keynes's beauty contest operationalized: how investor anticipations "
             "shape expectations, allocations and thereby price formation, volatility and "
             "liquidity.",
    maths=[
        ("Beauty-contest levels", r"$$p^* = \tfrac{2}{3}\,\mathbb{E}\!\left[ \bar{p} \right] \text{ iterated: level-}k \text{ reasoning}$$"),
    ],
    plain="Markets price not what investors believe, but what they believe others believe — "
          "iterated. AI systems that model that anticipation layer read positioning and flows as "
          "expressions of crowd expectation, not information.",
),
"talk-practical-implications-of-the-anticipations": dict(
    overview="Fuller's companion talk: practical implications, positive and negative, of "
             "anticipating the anticipations of others — from signal construction to crowding "
             "detection.",
    maths=[],
    plain="If you can measure what the crowd expects, you can fade its disappointments and ride "
          "its surprises — but the same measurement tells you when your own trade is the crowded "
          "one. The mirror points both ways.",
),
"talk-vicarious-risk-estimating-the-risk": dict(
    overview="Vicarious risk: estimating the risk identified by others — using AI over institutional "
             "positioning and behaviour to infer what risks the market's participants collectively "
             "perceive.",
    maths=[
        ("Implied concern index", r"$$\text{Risk}_{\text{vicarious}} = g\!\left( \Delta \text{positioning}, \text{hedging flows}, \text{attention} \right)$$"),
    ],
    plain="You can't read minds, but you can read portfolios: when institutions quietly de-risk a "
          "sector, their actions publish their private worries. Aggregating those actions yields a "
          "risk sensor built from other people's homework.",
),
"talk-how-epidemiology-and-the-science-of-networks": dict(
    overview="Modern epidemiology's toolkit — contagion models, network structure, superspreaders — "
             "applied to investor behaviour: parallels between disease spread and the propagation "
             "of sentiment and crises.",
    maths=[
        ("SIR contagion", r"$$\frac{dI}{dt} = \beta\, S I - \gamma\, I, \qquad R_0 = \beta/\gamma$$"),
    ],
    plain="Panic spreads like a pathogen: through contact networks, with superspreaders (media, "
          "big funds) and immunity (burned investors). Epidemic mathematics gives finance a "
          "vocabulary for crises that spread rather than strike.",
),
"talk-a-newbs-beginnings-in-algorithmic-investing": dict(
    overview="A newcomer's honest journey into algorithmic investing, alongside evidence from Credit "
             "Suisse's Gender 3000 on diversity and company performance.",
    maths=[],
    plain="A beginner's diary with data: the first strategies, the first overfits, the humbling "
          "gap between backtest and reality — plus the corporate-diversity evidence that framed "
          "the talk's investing angle.",
),

# ------------------------------------------------------------------------ risk
"talk-omnipresent-model-risk": dict(
    overview="Model risk demonstrated at scale: various models calibrated to identical data yield "
             "significantly different results — in finance and beyond — with consequences for "
             "governance.",
    maths=[
        ("Calibration non-uniqueness", r"$$\{m_i\}: \; \text{fit}(m_i) \approx \text{fit}(m_j) \;\;\text{but}\;\; V_{m_i}(\text{exotic}) \ne V_{m_j}(\text{exotic})$$"),
    ],
    plain="Perfect calibration is not identification: many models wear the same vanilla surface "
          "and disagree violently off it. Model risk is that disagreement, and it is everywhere "
          "you cannot triangulate with market prices.",
),
"talk-a-framework-based-approach-to-model-risk": dict(
    overview="A framework-driven approach to model risk management: quantifying model risk, stress "
             "and scenario testing of models themselves, and organizing MRM beyond checklists.",
    maths=[
        ("Model risk capital-style measure", r"$$\text{MR} = \rho\!\left( \{V_m\}_{m \in \mathcal{M}_{\text{plausible}}} \right) \quad \rho = \text{range or quantile}$$"),
    ],
    plain="Mature model risk management treats the model inventory like a portfolio: measure each "
          "model's uncertainty, stress its assumptions, and hold reserves against the ones whose "
          "errors would hurt most.",
),
"talk-model-risk-quantification-in-banking": dict(
    overview="Tiziano Bellini on model risk quantification in banking: with models driving decisions "
             "from provisioning to capital, the challenges and practical solutions for measuring "
             "their aggregate risk.",
    maths=[
        ("Aggregate model risk", r"$$\text{MR}_{\text{bank}} = f\!\left( \text{sensitivity} \times \text{materiality} \times \text{model quality} \right) \text{ summed over inventory}$$"),
    ],
    plain="A bank runs on hundreds of models whose errors correlate — the credit model and the "
          "capital model share assumptions. Quantifying that stacked exposure is the frontier of "
          "model risk, past validation-one-model-at-a-time.",
),
"talk-fintech-model-risk-and-all-that": dict(
    overview="Tanveer Bhatti on model risk inside a FinTech: where MRM becomes allied with software "
             "engineering rather than traditional bank validation — continuous deployment meets "
             "model governance.",
    maths=[],
    plain="In a FinTech the model ships weekly and the validator is a CI pipeline. Governance "
          "must move at engineering speed — automated testing, monitoring and rollback as the new "
          "validation report.",
),
"talk-tail-risk-and-portfolio-management": dict(
    overview="Tail risks in portfolio management strategies: why they matter, the hidden tails "
             "inside common strategies, and measuring tail risk to generate alpha during crises.",
    maths=[
        ("Expected shortfall", r"$$\text{ES}_\alpha = \mathbb{E}\!\left[ L \,\middle|\, L > \text{VaR}_\alpha \right]$$"),
    ],
    plain="Most 'alpha' strategies are short tails somewhere — the income is rent for standing "
          "under pianos. Measuring where the pianos hang, and being long a few, converts crisis "
          "from threat into harvest.",
),
"talk-shielding-portfolios-from-extremes-tail-risk": dict(
    overview="Tail-risk strategies for a turbulent era: with geopolitical shocks, inflation "
             "uncertainty and rising cross-asset correlations, traditional diversification is "
             "insufficient against extreme drawdowns.",
    maths=[
        ("Crisis correlation convergence", r"$$\rho_{ij} \to 1 \text{ as } |R_m| \to \text{extreme} \quad\text{— diversification's failure mode}$$"),
    ],
    plain="Diversification is a fair-weather friend: correlations converge exactly when you need "
          "them low. Explicit tail hedges — options, trend, convexity — cost carry in calm and "
          "pay when the averaging stops working.",
),
"talk-the-second-leg-down-strategies-for-surviving": dict(
    overview="Hari Krishnan's playbook from a simple observation: nobody hedges in calm markets, "
             "then protection is bid after the first sell-off — strategies for the cheaper hedge "
             "into the second leg down.",
    maths=[
        ("Post-shock hedge selection", r"$$\text{after leg 1: } \sigma_{\text{impl}} \uparrow\uparrow \Rightarrow \text{buy convexity via spreads, VIX structures, trend}$$"),
    ],
    plain="After the first crash leg, puts are expensive but the danger isn't over. The craft is "
          "buying convexity sideways — put spreads, vol futures curve trades, trend overlays — "
          "protection for the second leg without paying panic prices.",
),
"talk-market-tremors-hidden-risks-in-modern": dict(
    overview="Krishnan's 'Market Tremors': a non-technical tour of zombified markets — dominant "
             "agents (central banks, passive, dealers) whose mechanical behaviour stores hidden "
             "instability.",
    maths=[
        ("Dominant-agent amplification", r"$$\text{price move} = \text{shock} \times \left( 1 + \text{forced flows of dominant agents} \right)$$"),
    ],
    plain="When a handful of mechanical actors dominate flows, markets look calm while loading "
          "springs: the tremors metaphor is literal — small quakes reveal fault lines before the "
          "big one. The book maps today's faults.",
),
"talk-systemic-risk-and-market-fear-measurement": dict(
    overview="Measuring systemic risk and market fear: indicator construction from options, "
             "correlations and funding markets, and their behaviour around crises.",
    maths=[
        ("Absorption ratio", r"$$AR = \frac{\sum_{k=1}^{K} \lambda_k}{\sum_{k=1}^{N} \lambda_k} \quad\text{— high absorption} = \text{fragile, unified market}$$"),
    ],
    plain="When one factor starts explaining everything, the market has become a single trade — "
          "and single trades unwind together. Fear gauges built on that concentration warn before "
          "volatility itself does.",
),
"talk-estimating-and-forecasting-risk-measures-in": dict(
    overview="Fabrizio Lillo on risk measures in dynamical environments: estimation and forecasting "
             "of VaR/ES when volatility, correlation and liquidity are themselves stochastic "
             "processes.",
    maths=[
        ("Dynamic quantile forecast", r"$$\text{VaR}_{t+1} = \hat{q}_\alpha\!\left( r_{t+1} \,\middle|\, \mathcal{F}_t \right) \quad\text{via GARCH/EVT/quantile methods}$$"),
    ],
    plain="A risk number is a forecast, not a measurement — and forecasting quantiles of a "
          "shape-shifting distribution is genuinely hard. The talk benchmarks which methods track "
          "regime change fast enough to be useful.",
),
"talk-correlation-stress-testing-of-stock-and": dict(
    overview="Natalie Packham's general approach to stressing correlations in stock and credit "
             "portfolios: Bayesian variable selection builds a sparse factor structure linking "
             "names to country and industry factors.",
    maths=[
        ("Sparse factor stress", r"$$\Sigma(\theta) = B(\theta)\, \Sigma_f\, B(\theta)^\top + D, \qquad \text{stress } \theta \text{ coherently}$$"),
    ],
    plain="You cannot stress a correlation matrix cell-by-cell — it stops being a correlation "
          "matrix. Stressing the sparse factor skeleton underneath moves all correlations "
          "coherently, producing stress scenarios that are severe and possible.",
),
"talk-liquidity-risk-the-calm-before-the-storm": dict(
    overview="Gudni Adalsteinsson on why liquidity risk remains latent in calm markets, how it "
             "materializes, and how financial organizations should prepare for the unexpected.",
    maths=[
        ("Liquidity coverage logic", r"$$\text{LCR} = \frac{\text{HQLA}}{\text{30-day stressed outflows}} \ge 100\%$$"),
    ],
    plain="Liquidity is the risk that disappears when measured and reappears when needed: funding "
          "that rolls daily until the day it doesn't. Preparation is structural — term funding, "
          "buffers, tested contingency lines — because the storm gives no notice.",
),
"talk-capital-modeling-in-operational-risk": dict(
    overview="Ruben Cohen defines operational risk and its capital modelling: regulatory "
             "classification, loss-distribution approaches, and the roles of supervisors and local "
             "regulators.",
    maths=[
        ("Loss distribution approach", r"$$L = \sum_{i=1}^{N} X_i, \qquad N \sim \text{frequency}, \; X \sim \text{severity}; \quad \text{capital} = q_{99.9}(L)$$"),
    ],
    plain="Op risk capital asks a brutal question: the 1-in-1000-year rogue trader or cyber loss. "
          "Frequency-severity models give an answer; whether tail severity is estimable from any "
          "internal dataset remains the honest doubt.",
),
"talk-navigating-sector-investing-risks": dict(
    overview="Samit Ahlawat on sector investing: risks and returns across market environments, and "
             "formulating portfolio strategies from how sectors respond to regimes.",
    maths=[
        ("Sector regime sensitivity", r"$$R_{\text{sector}} = \alpha_s + \beta_s^{\text{regime}}\, F_{\text{regime}} + \varepsilon$$"),
    ],
    plain="Sectors are regime bets in drag: energy is inflation, utilities are duration, banks are "
          "the curve. Naming the bet behind each sector keeps a 'diversified' sector portfolio "
          "from being one macro trade in eleven costumes.",
),
"talk-quantifying-geopolitical-risk-data-punditry": dict(
    overview="GeoQuant's systematic measurement of geopolitical risk: political science plus data "
             "science versus traditional punditry, integrated into asset and risk management "
             "decisions.",
    maths=[
        ("Geo-risk factor test", r"$$R_t = \alpha + \beta\, \Delta \text{GeoRisk}_t + \varepsilon_t, \qquad \beta \ne 0 \text{ for FX/EM assets}$$"),
    ],
    plain="Pundits give vibes; measured political risk gives time series that can be backtested, "
          "hedged and priced. The demonstration: systematic geo-risk indices moving EM currencies "
          "and equities with tradable lead times.",
),
"talk-u-s-trump-2-0-accelerating-em-ification": dict(
    overview="Mark Rosenberg's GeoQuant analysis of Trump 2.0: accelerating 'EM-ification' of US "
             "institutions driving systemic risks to Treasuries, amid high uncertainty around "
             "regulatory reforms.",
    maths=[
        ("Institutional risk premium", r"$$y_{UST} = y_{\text{macro}} + \pi_{\text{institutional}} \quad\text{— the new term in the old equation}$$"),
    ],
    plain="Emerging markets pay a premium for institutional unpredictability; the provocation is "
          "that US assets have started pricing the same term. Measured political risk turns that "
          "claim from polemic into a testable time series.",
),
"talk-financial-crises-contagion-and-complexity": dict(
    overview="An overview of financial crises, manias, panics and crashes: economics, technology and "
             "innovation as crisis fuel, and where the next one may come from — the interconnected "
             "world's challenge.",
    maths=[
        ("Minsky dynamics (schematic)", r"$$\text{stability} \to \text{leverage} \to \text{fragility} \to \text{crisis} \to \text{repeat}$$"),
    ],
    plain="Crises follow a script older than any market: stability breeds the leverage that ends "
          "it. Each era adds its own accelerant — this survey's question is which of today's "
          "innovations is playing that role.",
),
"talk-financial-network-models-with-python": dict(
    overview="Miguel Vaz on the financial system's interconnectedness: network models in Python for "
             "interbank exposures, contagion simulation and systemic importance measures.",
    maths=[
        ("Contagion iteration", r"$$\text{default}_i \Rightarrow L_{ji} \text{ hits } j\text{'s capital} \Rightarrow \text{possibly default}_j \; \dots$$"),
    ],
    plain="The banking system is a web of IOUs: one failure transmits along exposure edges. "
          "Network analysis identifies the nodes whose failure cascades — systemic importance as "
          "a graph property, computable in a notebook.",
),
"talk-causal-asset-and-factor-network-inference": dict(
    overview="Gueorgui Konstantinov's framework integrating assets and factors in one network with "
             "causal treatment-effect analysis: potential outcomes from 'treating' nodes, capturing "
             "interconnectedness.",
    maths=[
        ("Network treatment effect", r"$$\text{ATE} = \mathbb{E}\!\left[ Y(\text{do}(X_v = x)) \right] - \mathbb{E}[Y] \quad\text{on the asset-factor graph}$$"),
    ],
    plain="Correlation networks show who moves together; causal networks ask what happens if you "
          "push a node. For allocators that difference is everything — contagion channels versus "
          "coincidences.",
),
"talk-breaking-the-waves-financial-storms": dict(
    overview="A history of securities regulation, policy and practice through financial storms: "
             "derivatives innovation, capital management, the Amaranth collapse, what happened to "
             "the quants, and the journey ahead.",
    maths=[],
    plain="Regulation is crisis archaeology: each rule marks a previous disaster. Walking the "
          "strata — from early securities acts through Amaranth and 2008 — explains both today's "
          "rulebook and the gaps the next storm will find.",
),
"talk-the-monetary-system-a-new-approach-to": dict(
    overview="Jean-François Serval's lecture on the monetary system: a new approach to analyzing and "
             "regulating money in a world where most 'money' is private credit and shadow "
             "instruments.",
    maths=[
        ("Broad money composition", r"$$M_{\text{effective}} = M_{\text{central bank}} + \text{bank credit} + \text{shadow claims}$$"),
    ],
    plain="Most money is not printed but promised — deposits, repos, fund shares all function as "
          "money until doubted. Regulating the system requires an accounting of those promises, "
          "which is precisely what standard aggregates miss.",
),
"talk-cooperation-and-competition-modern-economic": dict(
    overview="Modern economic history through cooperation and competition: classical economics, "
             "Marxism and neoclassical thought, 20th-century theory, and the post-war international "
             "political economy of trade.",
    maths=[
        ("Comparative advantage", r"$$\text{trade gains exist if } \frac{a_1}{a_2} \ne \frac{b_1}{b_2} \quad\text{(relative productivities differ)}$$"),
    ],
    plain="A grand tour from Smith to Bretton Woods and beyond: how each era's theory justified "
          "its trade order, and why cooperation and competition between nations cycle like the "
          "markets they govern.",
),
"talk-the-great-reset": dict(
    overview="A macro-financial big-picture talk: debt loads, monetary experimentation and the "
             "scenarios — inflationary, deflationary, distributive — by which the system resets.",
    maths=[
        ("Debt sustainability", r"$$\frac{d}{dt}\!\left( \frac{D}{Y} \right) = (r - g)\,\frac{D}{Y} - \text{primary balance}$$"),
    ],
    plain="When r exceeds g with debt this high, arithmetic forces a choice: inflate, default, "
          "repress or grow. 'Reset' talks are about which combination — and who pays — not "
          "whether.",
),
"talk-the-doomsday-debt-machine": dict(
    overview="The global debt machine examined: how leverage accumulates across sovereigns, "
             "corporates and households, the feedback loops that sustain it, and the endgames.",
    maths=[
        ("The spiral condition", r"$$r > g \;\Rightarrow\; \text{debt service compounds faster than income}$$"),
    ],
    plain="Debt that funds consumption rather than productive assets must be rolled forever — a "
          "machine that runs smoothly until rates rise or growth stalls. The talk inventories the "
          "machine's pressure points.",
),
"talk-the-risky-horror-show": dict(
    overview="A tour through risk management's chamber of horrors: blowups, measurement failures "
             "and the recurring human patterns behind quantitative disasters.",
    maths=[
        ("The recurring epitaph", r"$$\text{VaR fine} + \text{tails ignored} + \text{leverage} = \text{the usual obituary}$$"),
    ],
    plain="Every risk disaster autopsy finds the same organs: a measure that behaved, tails it "
          "didn't see, and incentives to look away. The horror show is educational precisely "
          "because the script never changes.",
),
"talk-why-most-published-findings-in-finance-are": dict(
    overview="Finance's replication crisis, after Ioannidis: multiple testing across thousands of "
             "factor studies, publication bias, and the statistical reforms (higher t-hurdles, "
             "pre-registration) the field needs.",
    maths=[
        ("Multiple-testing hurdle", r"$$t_{\text{required}} \approx 3.0+ \;\text{(not } 1.96\text{)} \quad\text{after accounting for the factor zoo}$$"),
    ],
    plain="Test 300 factors and a dozen clear t=2 by chance; journals publish the dozen. Half the "
          "factor zoo fails replication — the honest response is raising the evidence bar, not "
          "mourning the anomalies that were never there.",
),
}

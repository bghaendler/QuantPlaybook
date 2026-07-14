# Content for §10 Quantum, §11 Crypto, §12 Commodities, §15 ESG talks
# NOTE: talk-quantum-ml, talk-quantum-economics, talk-quantum-pricing, talk-crypto-lob
# absent (pre-existing hand-built pages).
CONTENT = {

# ------------------------------------------------------------------- quantum
"talk-what-is-quantum-computing": dict(
    overview="Alonso Peña's introductory overview: qubits, superposition, entanglement and quantum "
             "gates, and the areas of finance beginning to apply the technology.",
    maths=[
        ("Qubit state", r"$$|\psi\rangle = \alpha\,|0\rangle + \beta\,|1\rangle, \qquad |\alpha|^2 + |\beta|^2 = 1$$"),
    ],
    plain="A classical bit is a coin lying flat; a qubit is a coin spinning — heads and tails at "
          "once until observed. Computing with spinning coins lets some problems be explored in "
          "superposition, which is the entire promise and the entire catch.",
),
"talk-financial-applications-of-quantum-computing": dict(
    overview="Why quantum computing matters for finance: the basic concepts, candidate applications "
             "— Monte Carlo speedup, optimization, machine learning — and the steps institutions can "
             "take to become quantum-ready.",
    maths=[
        ("Amplitude estimation speedup", r"$$\varepsilon \sim N^{-1} \;\text{(quantum)} \quad\text{vs}\quad \varepsilon \sim N^{-1/2} \;\text{(classical MC)}$$"),
    ],
    plain="The headline promise is quadratic: risk numbers that need a million classical scenarios "
          "might need a thousand quantum queries. Hardware isn't there yet — the talk maps the "
          "distance between promise and machine.",
),
"talk-harnessing-the-power-of-quantum-computing-in": dict(
    overview="Finance as one of the first sectors with identified quantum use cases: portfolio "
             "optimization, derivative pricing and risk analysis pilots, and how to structure a "
             "quantum programme today.",
    maths=[
        ("QUBO formulation", r"$$\min_{x \in \{0,1\}^n}\; x^\top Q x \quad\text{— portfolio selection in annealer form}$$"),
    ],
    plain="Banks aren't waiting for perfect hardware; they're reformulating problems (portfolio "
          "choice as QUBO, pricing as amplitude estimation) so that when machines mature, the "
          "problems are already dressed for them.",
),
"talk-advances-in-quantum-computing": dict(
    overview="The state of the art: quantum hardware development across modalities, new quantum "
             "algorithms, and the evolving evidence on quantum advantage.",
    maths=[
        ("The scaling battle", r"$$\text{logical qubits} = \frac{\text{physical qubits}}{\text{error-correction overhead}} \quad\text{(currently } \sim 10^3\text{:1)}$$"),
    ],
    plain="Progress is real but the bottleneck is unforgiving: quantum states decay, and correcting "
          "the decay eats a thousand physical qubits per useful one. The talk tracks who is closing "
          "that ratio and how fast.",
),
"talk-advances-in-quantum-machine-learning": dict(
    overview="QML as the likeliest first source of quantum utility: algorithms with inherent noise "
             "resistance, quantum kernels and variational circuits, and the honest state of the "
             "evidence.",
    maths=[
        ("Variational quantum circuit", r"$$f(x;\theta) = \langle 0 |\, U^\dagger(x,\theta)\, M\, U(x,\theta)\, | 0 \rangle$$"),
    ],
    plain="Noisy machines can't run long algorithms — but ML tolerates noise by design, making it "
          "the natural first passenger. Whether quantum features genuinely beat classical ones "
          "remains the field's central open bet.",
),
"talk-advances-in-quantum-optimization-solvers-for": dict(
    overview="Davide Venturelli on quantum optimization for near-term hardware and beyond: QAOA, "
             "annealing, embedding real problems onto imperfect devices, and benchmark results.",
    maths=[
        ("QAOA ansatz", r"$$|\gamma, \beta\rangle = \prod_{k=1}^{p} e^{-i\beta_k H_M} e^{-i\gamma_k H_C}\, |+\rangle^{\otimes n}$$"),
    ],
    plain="Optimization is quantum computing's most crowded battlefield because business value is "
          "immediate. Current devices tie, not beat, classical heuristics — the interesting curve "
          "is how the tie moves with every hardware generation.",
),
"talk-quantum-machine-learning": dict(
    overview="Alexei Kondratyev on applied quantum computing research whose main focus is an "
             "experimental demonstration of quantum advantage: QML architectures, hardware "
             "experiments and the finance problems closest to benefiting.",
    maths=[
        ("Quantum advantage target", r"$$T_{\text{quantum}}(n) \ll T_{\text{classical}}(n) \quad\text{demonstrated on hardware, not paper}$$"),
    ],
    plain="The field's honest scoreboard-keeper: not whether quantum ML works in theory but "
          "whether any experiment on real hardware has beaten the best classical baseline yet — "
          "and what the nearest credible finance win looks like.",
),
"talk-quantum-complementarity-and-potential-for": dict(
    overview="Quantum and classical ML rest on different mathematical paradigms and provably predict "
             "different pattern classes efficiently: complementarity, not supremacy, as the realistic "
             "goal.",
    maths=[
        ("Quantum kernel", r"$$k(x, x') = \left| \langle \phi(x) | \phi(x') \rangle \right|^2 \quad\text{— inner products in Hilbert space}$$"),
    ],
    plain="Some patterns are easy for quantum models and hard classically — and vice versa. The "
          "mature strategy is a portfolio of models: let each paradigm classify the data it sees "
          "naturally.",
),
"talk-complementarity-of-quantum-and-classical-ml": dict(
    overview="A first end-to-end Quantum Support Vector Machine application in the financial payment "
             "industry: fraud classification, where quantum kernels complement classical features.",
    maths=[
        ("QSVM decision function", r"$$f(x) = \operatorname{sign}\!\left( \sum_i \alpha_i y_i\, k_Q(x_i, x) + b \right)$$"),
    ],
    plain="Fraud detection on real payment data, run on real quantum hardware: modest data sizes, "
          "genuine pipeline, and evidence that quantum kernels see some fraud patterns classical "
          "kernels blur.",
),
"talk-predicting-recessions-using-quantum-machine": dict(
    overview="David Garvin compares classical recession-prediction models to versions using quantum "
             "feature maps generated on quantum computers: methodology, results and caveats.",
    maths=[
        ("Quantum feature map", r"$$x \mapsto |\phi(x)\rangle = U_{\Phi}(x)\, |0\rangle^{\otimes n}$$"),
    ],
    plain="Recession prediction is small-data, nonlinear and noisy — the regime where exotic feature "
          "maps might matter. The experiment: same scarce macro data, classical vs quantum features, "
          "and a scoreboard.",
),
"talk-probability-distribution-classification": dict(
    overview="Olexiy Kondratiev on a statistical problem with quantum flavour: testing whether "
             "financial datasets come from the same probability distribution, comparing classical "
             "and quantum approaches.",
    maths=[
        ("Two-sample question", r"$$H_0: F_X = F_Y \quad\text{— tested via classical statistics vs quantum state discrimination}$$"),
    ],
    plain="'Are these two markets playing the same game?' is a distribution-comparison problem. "
          "Encoding distributions as quantum states turns it into state discrimination — a task "
          "quantum information theory understands deeply.",
),
"talk-quantum-monte-carlo": dict(
    overview="Rafał Pracht on quantum-accelerated Monte Carlo for derivative pricing: amplitude "
             "estimation mechanics, circuit construction for payoffs, and overcoming classical "
             "memory limits.",
    maths=[
        ("Amplitude estimation", r"$$\text{estimate } a = \langle \psi | P | \psi \rangle \text{ with } O(1/\varepsilon) \text{ queries vs } O(1/\varepsilon^2)$$"),
    ],
    plain="Quantum Monte Carlo doesn't sample paths — it interferes them, extracting the expectation "
          "with quadratically fewer oracle calls. Building the payoff oracle is the engineering "
          "mountain this talk climbs in public.",
),
"talk-quantum-inspired-tensor-networks-in": dict(
    overview="Quantum-inspired tensor networks — no quantum computer required — for high-dimensional "
             "quantitative finance: compressing pricing and risk problems that defeat dense grids.",
    maths=[
        ("Matrix product state", r"$$\Psi(i_1,\dots,i_d) = A_1^{i_1} A_2^{i_2} \cdots A_d^{i_d} \quad\text{— exponential object, polynomial storage}$$"),
    ],
    plain="The mathematics built to describe entangled quantum systems turns out to compress "
          "high-dimensional financial functions beautifully — a quantum dividend that pays today, "
          "on classical hardware.",
),
"talk-quantum-technologies-a-global-understanding": dict(
    overview="The quantum ecosystem mapped: hardware and software players, national programmes, the "
             "funding landscape, and near-term opportunities across industries with finance in "
             "focus.",
    maths=[],
    plain="Beyond the physics: who is funding what, which countries treat quantum as strategic "
          "infrastructure, and where a financial institution's early bets buy option value rather "
          "than hype.",
),
"talk-qi-quantum-solutions-for-finance": dict(
    overview="Araceli Venegas-Gomez surveys quantum solutions for finance from the ML-in-quant-"
             "finance conference: use cases, vendor landscape and adoption timelines.",
    maths=[],
    plain="A field guide for deciding when to care: which financial problems map naturally to "
          "quantum machines, which vendors are real, and what 'quantum-ready' concretely means for "
          "a quant team's roadmap.",
),
"talk-the-algorithms-bottleneck": dict(
    overview="Horizon Quantum Computing's founder on the real constraint: not qubits but algorithms "
             "and software — compiling from classical descriptions to quantum speedups "
             "automatically.",
    maths=[
        ("The gap", r"$$\#\{\text{useful quantum algorithms}\} \lll \#\{\text{problems people want solved}\}$$"),
    ],
    plain="Hardware progress is loud; the quiet crisis is that humanity knows only a handful of "
          "quantum algorithms. Tooling that squeezes speedups out of ordinary code — without "
          "quantum PhDs — is the bottleneck-breaker this company bets on.",
),
"talk-confessions-of-a-quantum-tourist-in-finance": dict(
    overview="A bank insider's honest account of leading quantum-computing projects — FX arbitrage "
             "detection among them — and the practical hurdles (privacy, data movement, integration) "
             "between pilot and production.",
    maths=[
        ("FX arbitrage as a cycle problem", r"$$\prod_{(i,j) \in \text{cycle}} S_{ij} > 1 \quad\text{— negative-cycle detection, QUBO-encoded}$$"),
    ],
    plain="Pilots discover the unglamorous truths: your data can't leave the building, the quantum "
          "cloud is outside the building, and the classical baseline is better than the vendor "
          "deck admitted. Tourism, honestly reported.",
),
"talk-how-quantum-should-change-the-way-we-think": dict(
    overview="Beyond speedups: how quantum concepts — superposition, measurement, incompatible "
             "observables — should change how finance conceptualizes uncertainty, prices and "
             "decisions.",
    maths=[
        ("Non-commuting observables", r"$$[A, B] \ne 0 \;\Rightarrow\; \text{no joint distribution — order of questions matters}$$"),
    ],
    plain="Quantum theory is at bottom a calculus of incompatible questions — and markets are full "
          "of them (ask price then depth, or depth then price?). The claim: the formalism fits "
          "finance even where the hardware is irrelevant.",
),
"talk-quantum-judder-for-financial-engineers": dict(
    overview="Quant finance's classical worldview — equilibrium plus random news — confronted with "
             "'quantum judder': discreteness and measurement effects at market microscale that the "
             "continuous picture smooths away.",
    maths=[
        ("Discreteness at the bottom", r"$$\text{ticks, lots, discrete fills} \;\ne\; \text{continuous } dW \text{ at small scales}$$"),
    ],
    plain="Zoom in far enough and markets stop being smooth: quotes jump between discrete levels "
          "and observation moves the observed. The analogy to quantum granularity is playful but "
          "the modelling consequences are serious.",
),
"talk-quantum-economics-and-finance-the-quantum": dict(
    overview="David Orrell prices a financial option with a quantum walk: replacing the classical "
             "random walk with quantum cognition's interference-capable walk, and comparing the "
             "resulting behaviour.",
    maths=[
        ("Quantum walk variance", r"$$\sigma_{\text{QW}}(t) \propto t \quad\text{vs}\quad \sigma_{\text{RW}}(t) \propto \sqrt{t}$$"),
    ],
    plain="A quantum walker spreads ballistically — its distribution piles up at the edges instead "
          "of the middle. Option prices built on that walk inherit fat extremes natively, no jump "
          "processes bolted on.",
),
"talk-quantum-economics-and-finance-the-quantum-2": dict(
    overview="The quantum coin trick: Orrell's hands-on introduction to quantum economics via the "
             "mathematics of quantum coins and simple circuits, from his applied-mathematics "
             "introduction to the field.",
    maths=[
        ("Hadamard coin", r"$$H = \tfrac{1}{\sqrt{2}}\begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix}, \qquad H|0\rangle = \tfrac{|0\rangle + |1\rangle}{\sqrt{2}}$$"),
    ],
    plain="Flip a quantum coin twice and it always lands heads — interference erases the tails "
          "paths. From that party trick the talk builds toward money, decisions and markets as "
          "interference-bearing systems.",
),
"talk-green-inflation-money-printing-and-quantum": dict(
    overview="A macro triptych: how the green transition's capital demands may drive 'green "
             "inflation' amid money printing and populism — with quantum computing as the wildcard "
             "technology thread.",
    maths=[
        ("Energy-money linkage", r"$$\pi_{\text{green}} \sim f\!\left( \text{capex}_{\text{transition}},\ \Delta M,\ \text{EROI} \right)$$"),
    ],
    plain="Replacing an energy system costs energy and capital before it yields any; financed by "
          "printing, that gap becomes inflation with a green label. A provocation about the "
          "transition's macro bill.",
),

# -------------------------------------------------------------------- crypto
"talk-the-bitcoin-innovation": dict(
    overview="Antonio Roldao on Bitcoin's innovation stack: the history and concerns, plus the "
             "technology, analytics, statistics and services that grew around the protocol.",
    maths=[
        ("Proof-of-work condition", r"$$\text{SHA256}\big(\text{SHA256}(\text{header})\big) < \text{target}$$"),
    ],
    plain="Bitcoin's trick is making history expensive to rewrite: each block buries the past under "
          "provable work. Everything else — wallets, exchanges, analytics — is infrastructure built "
          "on that one economic invariant.",
),
"talk-blockchain-and-bitcoin-a-mathematical": dict(
    overview="Julien Riposo's mathematical introduction: mining and proof-of-work, P2P network "
             "structure, halving schedules, blockchain stability and robustness, and information "
             "diffusion modelled with differential equations.",
    maths=[
        ("Supply schedule", r"$$S_\infty = \sum_{k=0}^{\infty} 210000 \cdot \frac{50}{2^k} = 21\text{M}$$"),
        ("Information diffusion", r"$$\frac{dI}{dt} = \beta\, I\,(N - I) \quad\text{— logistic spread across the network}$$"),
    ],
    plain="Under the ideology is clean mathematics: a geometric supply series, a race between "
          "block propagation and mining, and stability conditions that say when the longest chain "
          "is safe from rewriting.",
),
"talk-bitcoin-and-blockchain-opening-the-blackbox": dict(
    overview="Yves Hilpisch opens the black box with Python: hashing, blocks, transactions and a "
             "toy blockchain implemented live, turning crypto concepts into runnable code.",
    maths=[
        ("Hash chaining", r"$$h_n = H(h_{n-1} \,\|\, \text{data}_n) \quad\text{— tamper any block, break every successor}$$"),
    ],
    plain="Fifty lines of Python demystify the whole thing: a blockchain is a linked list with "
          "attitude. Building one yourself replaces mystique with an accurate sense of what is and "
          "isn't hard.",
),
"talk-blockchains-decentralized-financial-market": dict(
    overview="Recent developments in the cryptocurrency ecosystem: stablecoins and their "
             "classification, decentralized financial market infrastructure, and potential "
             "applications.",
    maths=[
        ("Stablecoin peg mechanics", r"$$P_{\text{coin}} \approx 1 \text{ via } \{\text{full reserve},\ \text{overcollateralized},\ \text{algorithmic}\}$$"),
    ],
    plain="Stablecoins are the bridge between crypto rails and real money — and their peg "
          "mechanisms range from boring (dollars in a bank) to reflexive (algorithmic seigniorage) "
          "with failure modes to match.",
),
"talk-decentralized-finance-central-bank-digital": dict(
    overview="DeFi, central bank digital currencies and automated market makers: the emerging "
             "architecture of currency markets, and what 'forex of the future' might look like.",
    maths=[
        ("Constant-product AMM", r"$$x \cdot y = k, \qquad P = \frac{y}{x}, \qquad \text{slippage} \propto \frac{\Delta x}{x}$$"),
    ],
    plain="An AMM replaces the order book with a formula: prices come from a curve, liquidity "
          "providers are the passive counterparty, and arbitrageurs keep the curve honest. Central "
          "banks are studying the same plumbing for sovereign money.",
),
"talk-industry-talk-forecast-bitcoin-price-using-a": dict(
    overview="Daniele Bernardi's quantitative Bitcoin forecasting: stock-to-flow, adoption-rate and "
             "hash-rate remuneration models, with (heroic) price projections to 2028.",
    maths=[
        ("Stock-to-flow model", r"$$\ln P = a + b \ln \frac{\text{stock}}{\text{flow}} \quad\text{— scarcity as the driver}$$"),
    ],
    plain="Three lenses — scarcity, adoption curves, miner economics — all pointed bullish when "
          "delivered. The methodological value survives the specific numbers: how one builds (and "
          "should stress) valuation models for an asset with no cash flows.",
),
"talk-cryptocurrency-exchange-microstructure-and": dict(
    overview="Aaron Brown's comprehensive analysis of major crypto exchange trading from a quant-"
             "strategy standpoint: microstructure quirks, data reliability and what systematic "
             "traders actually face.",
    maths=[
        ("Cross-exchange basis", r"$$b_{ij} = \frac{P_i - P_j}{P_j} \quad\text{— persistent, and expensive to arbitrage}$$"),
    ],
    plain="Crypto microstructure is equities' wild-west cousin: fragmented venues, wash trading, "
          "questionable prints. The alpha is real and so is the operational risk — the analysis "
          "weighs both with desk-level honesty.",
),
"talk-high-frequency-price-leadership-of-bitcoin": dict(
    overview="Two published studies: the time-lag between large moves on leading crypto derivatives "
             "exchanges and spot venues (price leadership), and construction of a Bitcoin VIX.",
    maths=[
        ("Lead-lag estimation", r"$$\hat\tau = \arg\max_\tau\; \operatorname{corr}\!\left( r^{\text{fut}}_t,\ r^{\text{spot}}_{t+\tau} \right)$$"),
    ],
    plain="Price discovery happens where the leverage is: derivatives exchanges move first and spot "
          "follows milliseconds to seconds later — a measurable lag that is both a research finding "
          "and a trading signal.",
),
"talk-portfolio-construction-for-sector-indices-of": dict(
    overview="Designing diversified crypto sector exposure: weighting methodology choices, handling "
             "dreadful data quality, and bootstrap simulation of sector-index risk-return profiles.",
    maths=[
        ("Capped weighting", r"$$w_i = \min\!\left( \frac{\text{mcap}_i}{\sum \text{mcap}}, \; c \right) \text{ renormalized — BTC/ETH dominance control}$$"),
    ],
    plain="Naive market-cap weighting makes every crypto index a Bitcoin tracker with decoration. "
          "Caps, sector definitions and bootstrap stress tests turn a chaotic asset zoo into "
          "something an allocator can size.",
),
"talk-is-crypto-the-next-frontier-of-opportunities": dict(
    overview="Panel: is crypto the next frontier for quants? Market maturity, data and "
             "infrastructure, strategy capacity and career considerations, debated.",
    maths=[],
    plain="The case for: inefficiencies everywhere, 24/7 data, no incumbent advantage. The case "
          "against: capacity, custody, regulation and the possibility the whole edge is beta in "
          "costume. The panel keeps score.",
),
"talk-rarity-metrics-for-profile-pictures-nfts": dict(
    overview="As Web3 expands into metaverses, PFP NFTs became digital identity assets: rarity "
             "metrics for scoring them, and how rarity relates to price formation.",
    maths=[
        ("Rarity score", r"$$R(\text{NFT}) = \sum_{\text{traits}} \frac{1}{f_{\text{trait}}} \quad f = \text{trait frequency in collection}$$"),
    ],
    plain="NFT collections are lotteries over trait combinations; rarity scores are the actuarial "
          "tables. Whether scarcity of a hat pixel deserves a premium is the market's question — "
          "measuring it consistently is the quant's.",
),
"talk-the-rise-and-rise-of-upi": dict(
    overview="India's Unified Payments Interface: the architecture and staggering growth of the "
             "world's most successful instant-payment system, and its lessons for digital money "
             "everywhere.",
    maths=[
        ("Network effect growth", r"$$V \propto n^2 \quad\text{— users} \times \text{merchants compounding}$$"),
    ],
    plain="While the West debated CBDCs, India shipped: interoperable, instant, effectively free "
          "payments at billions-per-month scale. UPI is the existence proof in every digital-money "
          "argument.",
),

# --------------------------------------------------------------- commodities
"talk-commodities-modelling": dict(
    overview="William Smith's fundamentals: what commodities are, energy modelling, storage and "
             "seasonality, and commodity correlation structure.",
    maths=[
        ("Storage cost-of-carry", r"$$F = S\, e^{(r + u - y)T}, \qquad y = \text{convenience yield}$$"),
    ],
    plain="Commodities are consumed, stored and delivered — so their forward curves encode "
          "warehouses and pipelines, not just interest rates. Convenience yield is the price of "
          "having the barrel now.",
),
"talk-principles-of-commodity-option-pricing-a": dict(
    overview="A mathematical introduction to commodity models and products: from Black-76 through "
             "mean-reverting and two-factor models to the option structures particular to "
             "commodity markets.",
    maths=[
        ("Schwartz mean-reverting spot", r"$$d\ln S = \kappa(\mu - \ln S)\,dt + \sigma\, dW$$"),
    ],
    plain="Commodity prices are tethered: high prices summon supply, low prices destroy it. Mean "
          "reversion changes everything downstream — long-dated options are cheaper, and the "
          "volatility term structure slopes down instead of flat.",
),
"talk-using-the-signature-method-to-classify": dict(
    overview="Can commodities be distinguished purely from their price paths? Path signatures as "
             "features for classifying markets and selecting commodity options strategies.",
    maths=[
        ("Path signature terms", r"$$S(X) = \left( 1,\ \int dX,\ \int\!\!\int dX \otimes dX,\ \dots \right)$$"),
    ],
    plain="A path's signature is its complete geometric fingerprint — order of moves included. "
          "Feeding signatures to a classifier answers 'does gold trade like oil?' from shape "
          "alone, then picks the option structure suiting each shape.",
),
"talk-path-signatures-for-data-pooling-and": dict(
    overview="Advanced models need data commodities markets don't have; pooling similar datasets via "
             "path-signature similarity enhances training, tackles complexity and stabilizes "
             "commodity strategy models.",
    maths=[
        ("Signature kernel pooling", r"$$k(X, Y) = \langle S(X), S(Y) \rangle \quad\text{— pool markets with high } k$$"),
    ],
    plain="Ten years of cocoa data is too little for deep models — but cocoa plus its "
          "signature-similar cousins is a respectable corpus. Signatures decide who counts as a "
          "cousin, mathematically rather than anecdotally.",
),
"talk-graph-based-learning-for-commodity-futures": dict(
    overview="Commodity futures with graph neural networks over temporal knowledge graphs: encoding "
             "the macro, geopolitical and physical-flow web that drives these notoriously "
             "hard-to-model markets.",
    maths=[
        ("GNN message passing", r"$$h_v^{(k+1)} = \phi\!\left( h_v^{(k)}, \bigoplus_{u \in N(v)} \psi(h_u^{(k)}, e_{uv}) \right)$$"),
    ],
    plain="Wheat depends on weather, freight, politics and substitutes — a graph, not a time "
          "series. Letting the model see the graph, with time-stamped edges, imports exactly the "
          "structure commodity fundamentals always had.",
),
"talk-covid-19-and-crude-oil-prices": dict(
    overview="How geopolitics plus COVID demand collapse produced negative WTI futures in April "
             "2020 — unprecedented since the 1983 contract launch — and what it taught about "
             "physical delivery and storage.",
    maths=[
        ("Negative price logic", r"$$P = -\text{(storage scarcity cost)} \quad\text{when tanks are full and delivery is compulsory}$$"),
    ],
    plain="Oil went to minus $37 because a futures contract is a promise to receive barrels, and "
          "nobody had anywhere to put them. The episode is the definitive lesson that financial "
          "prices have physical boundary conditions.",
),
"talk-energy-options-volatility-and-energy": dict(
    overview="Panel on real options in the energy transition: battery storage and critical new "
             "technologies valued as options on volatility, and what the transition does to energy "
             "optionality.",
    maths=[
        ("Storage as a spread option", r"$$V_{\text{battery}} = \mathbb{E}\left[ \sum_t \max\!\left( P^{\text{peak}}_t - P^{\text{off}}_t - c, 0 \right) \right]$$"),
    ],
    plain="A battery is a call on price spreads between hours; its value rises with volatility that "
          "renewables themselves create. The transition thus feeds the economics of its own "
          "enabling technology — a rare virtuous loop.",
),
"talk-supply-chain-climate-exposure": dict(
    overview="Investors want climate-risk exposure data and get poor coverage; this work measures "
             "climate exposure through supply chains, propagating risk from suppliers to the firms "
             "that depend on them.",
    maths=[
        ("Propagated exposure", r"$$E_i = e_i + \sum_j w_{ij}\, E_j \quad\text{— exposure through the supplier graph}$$"),
    ],
    plain="A company with green operations and a flood-prone supplier is not green when it rains. "
          "Tracing exposure through the supply graph reveals climate risk where disclosure "
          "documents show none.",
),

# ----------------------------------------------------------------------- esg
"talk-managing-climate-risk": dict(
    overview="Climate as systemic versus specific risk: distinguishing economy-wide from localized "
             "climate impacts, and the risk-management toolkit for a decade the speaker argues is "
             "decisive.",
    maths=[
        ("Expected climate loss", r"$$\mathbb{E}[L] = \sum_s \pi_s \cdot D_s(\text{warming}_s) \quad\text{— scenario-weighted damages}$$"),
    ],
    plain="Diversification cannot hedge a risk the whole economy shares. Climate risk management "
          "is therefore scenario planning, not portfolio optimization — and the scenarios are "
          "narrowing as the decade advances.",
),
"talk-climate-risk-and-opportunity": dict(
    overview="Climate change framed as a major risk-management failure with a crucial decade ahead: "
             "physical and transition risks, and the investment opportunities in fixing both.",
    maths=[
        ("Transition vs physical risk", r"$$R_{\text{total}} = R_{\text{physical}}(\Delta T) + R_{\text{transition}}(\text{policy path})$$"),
    ],
    plain="The paradox: acting hard creates transition risk, not acting creates physical risk — the "
          "portfolio question is which risk you're being paid to hold. Opportunity lives where "
          "mitigation capital must flow regardless.",
),
"talk-climate-financial-risk-portfolios-and-stress": dict(
    overview="How investors should use ESG in portfolio formation: optimality criteria compared, "
             "with statistical and fundamental analysis of climate hedge portfolios and stress "
             "tests.",
    maths=[
        ("Climate-hedged optimization", r"$$\max_w\; \mu^\top w - \tfrac{\gamma}{2} w^\top \Sigma w \quad \text{s.t.}\quad \beta_{\text{climate}}(w) \le b$$"),
    ],
    plain="A climate hedge portfolio overweights what gains and shorts what suffers as climate news "
          "arrives — buildable today with mimicking-portfolio techniques, testable against "
          "climate-news indices, and stress-tested here.",
),
"talk-ai-and-esg-investing": dict(
    overview="Grant Fuller on SRI/ESG investing as a discipline: incorporating ESG criteria for "
             "long-term risk management and returns, with AI handling the unstructured data burden.",
    maths=[
        ("ESG signal extraction", r"$$\text{ESG}_i = f_{\text{NLP}}\!\left( \text{disclosures}_i, \text{news}_i, \text{alt data}_i \right)$$"),
    ],
    plain="ESG's data problem — self-reported, unaudited, inconsistent — is exactly the kind of "
          "mess NLP eats: read everything, cross-check claims against news, and score companies on "
          "behaviour rather than brochures.",
),
"talk-esg-and-shareholder-value": dict(
    overview="ESG's uneasy marriage of financial and social returns: greenwashing scrutiny, the "
             "woke/anti-woke debate, and the evidence on when ESG creates versus costs shareholder "
             "value.",
    maths=[
        ("The materiality split", r"$$\alpha_{\text{ESG}} > 0 \text{ for material issues}, \quad \approx 0 \text{ (or } < 0\text{) otherwise}$$"),
    ],
    plain="ESG helps returns when the E, S or G issue is material to the business (safety at a "
          "miner, governance anywhere) and is decoration otherwise. The debate rages because both "
          "sides quote the half of the evidence that suits them.",
),
"talk-esg-emergence-of-the-sustainability-linked": dict(
    overview="Diana Ouamar on sustainability-linked bonds: structures whose coupons step on missed "
             "KPIs — friend or foe to sustainability, given the incentive design questions.",
    maths=[
        ("SLB coupon step", r"$$c_t = c_0 + \Delta \cdot \mathbb{1}\{\text{KPI missed}\} \quad\text{— typically } \Delta = 25\text{bp}$$"),
    ],
    plain="An SLB fines the issuer for missing green targets — but if the fine is cheaper than "
          "compliance, it's a licence, not an incentive. Whether these bonds fund transition or "
          "greenwash depends on numbers this talk interrogates.",
),
"talk-your-attention-please-weaponising-the-esg": dict(
    overview="How ESG thematics amplify attention asymmetries in markets: consequences for issuers, "
             "portfolio and risk managers, activists on both sides, short-sellers and regulators.",
    maths=[],
    plain="ESG narratives concentrate attention, and concentrated attention moves prices "
          "independent of fundamentals — a weapon available to activists, shorts and issuers "
          "alike. The talk maps who wields it and who absorbs it.",
),
"talk-symbols-vs-solutions-quant-as-a-driver-for": dict(
    overview="ESG as political symbol versus quant as value driver: refocusing on technology that "
             "identifies and rewards innovation and stewardship through capital deployment.",
    maths=[],
    plain="When ESG became a culture-war symbol it stopped informing prices; the constructive "
          "residue is quantitative: measure what companies actually do, reward it with capital, "
          "and skip the symbolism.",
),
}

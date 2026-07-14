# Content for §16 Dev, §17 Careers, §18 History talks — consumed by enrich_talks.py
# NOTE: talk-quant-interview, talk-day-portfolio-manager, talk-day-quant-trader,
# talk-day-quant-auditor absent (pre-existing hand-built pages).
CONTENT = {

# ------------------------------------------------------------------------ dev
"talk-fast-greeks-through-adjoint-algorithmic": dict(
    overview="Speeding up Greeks by orders of magnitude with adjoint algorithmic differentiation: "
             "mathematical and structural insight, with case studies demonstrating the end-to-end "
             "process.",
    maths=[
        ("The adjoint miracle", r"$$\text{cost}\!\left( \nabla f \right) \le c \cdot \text{cost}(f), \qquad c \approx 4 \;\text{— independent of } \dim$$"),
    ],
    plain="Bumping 500 inputs costs 500 pricings; running the computation backwards once yields "
          "all 500 sensitivities for the price of a handful. Adjoint AD is the closest thing "
          "computational finance has to a magic trick.",
),
"talk-adjoint-parameter-calibration-in": dict(
    overview="Uwe Naumann on adjoint AD for calibration: efficiently and accurately computing "
             "sensitivities of numerical simulations, with applications to parameter calibration "
             "problems.",
    maths=[
        ("Gradient-based calibration", r"$$\theta_{k+1} = \theta_k - \eta\, \nabla_\theta \| V(\theta) - V^{\text{mkt}} \|^2 \quad \nabla \text{ via adjoints}$$"),
    ],
    plain="Calibration is optimization, optimization wants gradients, and finite differences make "
          "them slow and noisy. Adjoints deliver machine-precision gradients at fixed cost — "
          "calibrations converge in fewer, better steps.",
),
"talk-aad-applications-as-a-game-changer-for": dict(
    overview="AAD as a game changer: fundamentals of the technology plus direct applications (Greeks, "
             "XVA) and indirect ones (training AI models is backpropagation, i.e. the same adjoint "
             "idea).",
    maths=[
        ("Chain rule, reversed", r"$$\bar{x}_i = \sum_j \bar{y}_j\, \frac{\partial y_j}{\partial x_i} \quad\text{— accumulated backwards through the graph}$$"),
    ],
    plain="Backpropagation and adjoint Greeks are one algorithm wearing two costumes. Understanding "
          "it once buys you fast risk, fast calibration and a deeper grasp of how every neural "
          "network learns.",
),
"talk-parallel-computing-and-gpus": dict(
    overview="Parallel computing and GPUs for quantitative finance: architectures, when Monte Carlo "
             "and PDE workloads parallelize well, and the practicalities of GPU acceleration.",
    maths=[
        ("Amdahl's law", r"$$S = \frac{1}{(1-p) + p/N} \quad\text{— the serial fraction rules the ceiling}$$"),
    ],
    plain="Monte Carlo is embarrassingly parallel — a GPU eats it. The catch is Amdahl: the 5% of "
          "your pipeline that stays serial caps the speedup, so profiling beats hardware shopping.",
),
"talk-faster-intelligence-hardware-and-software": dict(
    overview="What's possible with modern hardware plus the software tricks — quantization, "
             "precision management, sparsity, compiler optimizations — that make models radically "
             "faster.",
    maths=[
        ("Precision-speed trade", r"$$\text{FP32} \to \text{FP16/INT8}: \; 2\text{-}4\times \text{ throughput}, \; \text{accuracy} \approx \text{unchanged if calibrated}$$"),
    ],
    plain="Most model 'speed limits' are software choices: half the bits, structured sparsity and "
          "a good compiler routinely buy 10x. Intuition for these dials is now core quant "
          "infrastructure literacy.",
),
"talk-quant-development": dict(
    overview="The craft of quant development: architecture for pricing libraries, testing numerical "
             "code, performance engineering and the collaboration between quants and developers.",
    maths=[],
    plain="Production quant code outlives its authors and its models: the discipline — clean "
          "interfaces, regression tests against known values, reproducible builds — is what lets "
          "a pricing library survive a decade of hands.",
),
"talk-agile-development": dict(
    overview="Agile development for quants: what actually happens on desks, formalized — iterative "
             "delivery, feedback loops and the best practices agile adds to quant workflows.",
    maths=[],
    plain="Desk quants were agile before the manifesto: ship small, get trader feedback, iterate "
          "daily. The formal method adds the missing parts — tests, retrospectives, sustainable "
          "pace — without the ceremony that kills speed.",
),
"talk-introduction-to-tdd-for-quantitative": dict(
    overview="Test-driven development for quantitative developers: writing tests first for numerical "
             "code, regression-testing models against analytic limits, and TDD's fit with research "
             "code.",
    maths=[
        ("The numerical test oracle", r"$$\left| V_{\text{numeric}} - V_{\text{closed-form}} \right| < \varepsilon \quad\text{on every commit}$$"),
    ],
    plain="Numerical code fails silently — a sign error prices happily, just wrongly. Tests pinned "
          "to analytic limits, put-call parity and known solutions catch tomorrow's refactoring "
          "mistake today, automatically.",
),
"talk-taming-the-lint-monster-accu": dict(
    overview="ACCU talk on static analysis at scale: taming warning floods from linters and "
             "analyzers in large C++ codebases, and making the signal survive the noise.",
    maths=[],
    plain="Turn on all warnings in a legacy codebase and drown in ten thousand; turn them off and "
          "ship bugs. The craft is ratcheting: freeze the baseline, forbid new warnings, and "
          "shrink the monster one merge at a time.",
),
"talk-accu-mocking-in-c": dict(
    overview="ACCU: mocking in C++ with MockItNow — testing code you can't refactor to interfaces, "
             "including mocking free functions when the source can't change.",
    maths=[],
    plain="Legacy quant libraries resist testing because everything calls everything concretely. "
          "Link-time and instrumentation tricks let you fake the market-data call without "
          "rewriting the library first — tests before refactoring, not after.",
),
"talk-accu-enterprise-web-application-development": dict(
    overview="ACCU: enterprise web development in Java with AJAX and ORMs — data access layers, "
             "integration testing, and a GWT presentation layer, as done in enterprise finance.",
    maths=[],
    plain="A period piece with durable lessons: layered architecture, ORM discipline and testable "
          "data access outlive any particular framework fashion — including the ones in this "
          "talk's title.",
),
"talk-accu": dict(
    overview="ACCU — Anticipating Surprises: how to find problems in software before they find you, "
             "and how to persuade people you have avoided them.",
    maths=[],
    plain="Half of engineering is finding failure modes early; the other half is making the "
          "avoided disaster visible to people who only see that nothing happened. Both halves are "
          "skills, and this talk teaches the second one too.",
),
"talk-building-an-enterprise-computation-strategy": dict(
    overview="The ultimate enterprise computation platform: values, types of enterprise software, "
             "and what organization-wide computation should look like, illustrated with Wolfram "
             "technology.",
    maths=[],
    plain="Every firm runs on scattered spreadsheets and scripts that are secretly critical "
          "infrastructure. A computation strategy makes them citizens: versioned, discoverable, "
          "auditable and composable across the organization.",
),
"talk-running-quantitative-analytics-with-google": dict(
    overview="Quantitative analytics on Google Dataflow: the evolution of streaming engines and "
             "running risk and analytics pipelines on managed cloud dataflow infrastructure.",
    maths=[],
    plain="Risk batches that ran overnight can stream continuously: the same aggregation, "
          "expressed as a dataflow graph, scales elastically and recovers from failure by design. "
          "The mental shift is from jobs to flows.",
),
"talk-from-open-source-to-industry-standard": dict(
    overview="The Open Source Risk Engine's journey to industry standard: trade coverage across "
             "asset classes, pricing, XVA, market risk and capital analytics — key challenges and "
             "milestones.",
    maths=[],
    plain="An open-source risk engine survives on trust: transparent methodology beats black-box "
          "vendors precisely where regulators and auditors ask 'show me'. ORE's decade proves "
          "open quant infrastructure can win.",
),
"talk-applying-the-open-source-risk-engine-for": dict(
    overview="Roland Lichters applies ORE hands-on: setting up portfolios, running pricing and risk "
             "analyses, and extending the engine for practical use.",
    maths=[],
    plain="The companion workshop: from XML trade files to XVA numbers with an open toolchain — "
          "the fastest route to a working, auditable risk stack for a small desk or a classroom.",
),
"talk-technical-news-from-the-python-financial": dict(
    overview="The Python/PyData ecosystem's rapid growth: recent valuable additions for financial "
             "analytics and what they change in daily quant work.",
    maths=[],
    plain="The Python data stack compounds like an index fund: every year the same analysis needs "
          "fewer lines and runs faster. Staying current is free alpha for research productivity.",
),
"talk-optimizing-pandas-for-performance": dict(
    overview="Jeff Reback (pandas core) on optimizing pandas: vectorization, dtypes, memory layout, "
             "and the do's and don'ts when writing performant data code.",
    maths=[],
    plain="Pandas is fast when you speak its language (columns, vectors, categoricals) and "
          "glacial when you fight it (row loops, object dtypes). A core developer's tour of "
          "which is which, with receipts.",
),
"talk-using-financial-data-from-quandl-with-python": dict(
    overview="Quandl's financial data via Python: the API, dataset discovery and building clean "
             "research datasets from a unified source.",
    maths=[],
    plain="Data acquisition is research's unglamorous half. A unified API for thousands of "
          "datasets turns 'where do I even get that series' from an afternoon into a line of "
          "code.",
),
"talk-how-to-build-a-hedge-fund-with-python": dict(
    overview="Adam Sherman on building a hedge fund's technology on Python: research, execution, "
             "risk and operations on an open-source stack.",
    maths=[],
    plain="A fund's entire stack — signals to settlement — can stand on Python and open source. "
          "The talk is an architecture walkthrough with the honest costs: glue code, data "
          "hygiene and the places you still buy rather than build.",
),
"talk-how-to-build-a-cta-with-pythalesians": dict(
    overview="Saeed Amen builds a CTA with his open-source PyThalesians library: trend signals, "
             "backtesting and analysis of a systematic futures strategy in Python.",
    maths=[
        ("Starter trend rule", r"$$w_t = \operatorname{sign}\!\left( \text{SMA}_{\text{fast}} - \text{SMA}_{\text{slow}} \right) \cdot \frac{\text{vol target}}{\hat\sigma_t}$$"),
    ],
    plain="A minimal CTA is a weekend project: moving-average signals, vol targeting and honest "
          "cost assumptions. The library does the plumbing; the talk shows how quickly ideas "
          "become testable curves.",
),
"talk-julia-a-new-approach-for-quantitative": dict(
    overview="Avik Sengupta on Julia: an open-source language for scientific computing that is "
             "productive, fast and mathematically expressive — solving the two-language problem.",
    maths=[
        ("The two-language problem", r"$$\text{prototype (Python)} + \text{production (C++)} \;\to\; \text{one language (Julia)}$$"),
    ],
    plain="Quants prototype in a slow language and rewrite in a fast one, paying twice and "
          "diverging forever. Julia's bet: one language fast enough to ship and pleasant enough "
          "to research in.",
),
"talk-julia-in-finance": dict(
    overview="Industry practitioners demonstrate Julia in financial services: production use cases "
             "where mathematical computing speed became a competitive advantage.",
    maths=[],
    plain="The sequel with production scars: risk engines and pricing libraries running Julia in "
          "anger, with the benchmarks — and migration lessons — from firms that jumped.",
),
"talk-software-issues-in-wavelet-analysis-of": dict(
    overview="Software issues in wavelet analysis of financial data: implementation pitfalls — "
             "boundary effects, alignment, leakage — that silently corrupt wavelet-based studies.",
    maths=[
        ("Discrete wavelet transform", r"$$W_{j,k} = \sum_t x_t\, \psi_{j,k}(t) \quad\text{— boundary handling changes the answer}$$"),
    ],
    plain="Wavelets promise time-frequency insight and deliver artifacts if the implementation is "
          "careless: edge effects masquerade as market events. The talk is a debugging checklist "
          "for anyone decomposing returns.",
),
"talk-principal-component-analysis-for-financial": dict(
    overview="PCA for financial time series from principles to practice: applications to curves and "
             "portfolios, through independent component analysis, with Python illustrations.",
    maths=[
        ("Eigen-decomposition", r"$$\Sigma = Q \Lambda Q^\top, \qquad \text{PC}_k = Q_{\cdot k}^\top x$$"),
    ],
    plain="PCA is finance's favourite compression: curves become level-slope-curvature, equity "
          "panels become market-plus-styles. The lecture builds it from scratch and shows where "
          "its linear worldview misleads.",
),
"talk-latest-innovations-in-financial-time-series": dict(
    overview="Rebecca Killick on changepoints, structural breaks and segmentation in financial time "
             "series, paired with recent advances in mathematical optimization from NAG.",
    maths=[
        ("Changepoint objective", r"$$\min_{\tau_1 < \dots < \tau_m} \sum_{i} C\!\left( x_{\tau_{i-1}:\tau_i} \right) + \beta m$$"),
    ],
    plain="Markets change regimes; most models pretend otherwise. Modern changepoint detection "
          "finds the break dates with statistical guarantees — so parameters can be estimated "
          "within regimes instead of blurred across them.",
),
"talk-fun-with-name-value-pairs-derek-yates-2": dict(
    overview="Derek Yates has fun with small data: two case studies on name-value pairs showing how "
             "much insight modest, well-structured datasets can yield.",
    maths=[],
    plain="A counterweight to big-data maximalism: two tiny case studies where careful thought "
          "about humble key-value data beats brute force — a reminder that insight scales with "
          "questions, not rows.",
),
"talk-data-science-is-more-than-just-statistics": dict(
    overview="Data science reframed as 'computation with data': the full workflow — acquisition, "
             "modelling, deployment, communication — beyond the statistical core.",
    maths=[],
    plain="Statistics is the engine but not the vehicle: real data science is plumbing, domain "
          "judgment and delivering answers people can act on. The talk maps the whole vehicle.",
),
"talk-data-science-and-symbolic-data": dict(
    overview="Symbolic computation meets data science: representing knowledge and data symbolically "
             "so that models, units and meaning travel with the numbers.",
    maths=[],
    plain="Numbers with meanings attached — units, entities, assumptions — resist an entire class "
          "of silent errors. Symbolic data science makes the computer carry the context humans "
          "forget.",
),
"talk-data-science-and-ml-applied-to-business": dict(
    overview="Data science and ML for business analytics: financial and retail market use cases "
             "showing the path from raw data to deployed decision support.",
    maths=[],
    plain="Case-study driven: churn, credit, demand — the same modelling patterns recur across "
          "industries, and the deployment last mile decides whether any of it matters.",
),
"talk-breaking-the-boundaries-of-traditional-data": dict(
    overview="Jon McLoone: data science as 'computation with data' rather than statistics — "
             "automation, symbolic methods and broader computation expanding what the discipline "
             "covers.",
    maths=[],
    plain="When every step — cleaning, modelling, reporting — is computable, the boundary between "
          "analyst and developer dissolves. The talk argues the future belongs to computational "
          "generalists.",
),
"talk-computation-meets-data-science": dict(
    overview="Promoting an analytics-driven decision culture: how organizations get better, more "
             "insightful answers when computation permeates decision-making.",
    maths=[],
    plain="Tools don't change outcomes until culture does: the talk is about making 'show me the "
          "computation' the default response to any claim in a meeting.",
),
"talk-smart-cities-and-data-overload-insight-from": dict(
    overview="Smart cities and the Internet of Things: extracting insight from sensor floods — "
             "lessons transferable to any domain drowning in high-frequency telemetry.",
    maths=[],
    plain="A city's sensor feed looks remarkably like tick data: too much, too fast, mostly "
          "boring. The filtering and anomaly-detection patterns transfer both directions between "
          "urban telemetry and markets.",
),
"talk-finance-focus-deep-space-analytics": dict(
    overview="'Deep Space Analytics': a finance-focus session on pushing analytics into unexplored "
             "data territory — methods for finding structure where standard tools see noise.",
    maths=[],
    plain="Most alpha hides where standard tooling stops looking. The session is a tour of "
          "less-travelled analytical techniques and the mindset of exploring data frontiers "
          "systematically.",
),
"talk-applied-finance": dict(
    overview="Applied Finance — The Third Culture: bridging the gap between traditional data science "
             "cultures and applied finance, from an ODSC Europe keynote.",
    maths=[],
    plain="Data scientists distrust financial theory; quants distrust black boxes. The 'third "
          "culture' claims both: theory-informed features, evidence-disciplined models, and "
          "respect for how markets punish overconfidence.",
),

# -------------------------------------------------------------------- careers
"talk-quantitative-finance-skills-of-the-future": dict(
    overview="Expert panel on what quant professionals need now and next: the evolving skill mix "
             "across mathematics, programming, ML and communication.",
    maths=[],
    plain="The consensus stack keeps shifting toward breadth: solid probability, fluent Python, "
          "ML literacy and — increasingly decisive — the ability to explain models to people who "
          "will never read them.",
),
"talk-navigating-the-quant-future-upcoming-trends": dict(
    overview="Panel on upcoming trends and essential skills: what professionals need to succeed in "
             "quant finance now and what they might need as the field evolves.",
    maths=[],
    plain="A market scan for careers: which specialties are commoditizing (vanilla pricing), "
          "which are scarce (ML with market sense, XVA, systematic credit) and how to position "
          "before the crowd notices.",
),
"talk-quantitative-finance-careers-india-2": dict(
    overview="Quant careers in India: pathways, essential skills, recruitment trends specific to "
             "the Indian market, and how structured credentials position candidates.",
    maths=[],
    plain="India's quant market is scaling fast on the back of GCCs, prop shops and fintech: the "
          "talk maps who hires, what they test and how the recruiting funnel differs from London "
          "or New York.",
),
"talk-how-to-build-a-standout-quant-resume-best": dict(
    overview="Quant resume best practices: with specialized skills in demand, candidates are "
             "forgiven many mistakes — but the standout resume avoids them anyway.",
    maths=[],
    plain="A quant resume is a claims document: every line should be a verifiable, quantified "
          "statement a technical interviewer can probe. Adjectives are noise; numbers and "
          "artifacts are signal.",
),
"talk-crafting-a-high-impact-quant-finance-resume": dict(
    overview="Brian Cullinan's insights on impactful resumes: common mistakes, engaging structure, "
             "and standing out during the quant recruitment process.",
    maths=[],
    plain="Recruiters read in ten-second passes: front-load the strongest quantified achievement, "
          "cut everything that doesn't survive the 'so what' test, and make the technical stack "
          "scannable at a glance.",
),
"talk-careers-in-quant-finance-and-resume-building": dict(
    overview="Sonia Arora explores career pathways in quantitative finance and the skills needed in "
             "today's competitive market, with resume-building guidance.",
    maths=[],
    plain="A map of the quant career lattice — sell side, buy side, risk, fintech — with honest "
          "notes on mobility between them and how to write the document that opens each door.",
),
"talk-careers-talk-a-day-in-the-life-of-a": dict(
    overview="A portfolio manager's typical day: tasks, challenges, and collaboration with research "
             "and risk teams — the texture of the role behind the title.",
    maths=[],
    plain="The PM's day is allocation of attention: markets at dawn, positioning reviews, research "
          "debates, risk conversations — decisions per day, not lines of code. Knowing the rhythm "
          "tells you if you'd love it.",
),
"talk-careers-talk-with-chloe-vuong-quant": dict(
    overview="Chloe Vuong's journey as a quantitative developer: roles across quant risk, "
             "derivative pricing and quant trading, and the key skills each demanded.",
    maths=[],
    plain="Quant development is the field's connective tissue — the same C++/Python craft opens "
          "risk, pricing and trading doors. One career's path through all three, with the "
          "transferable skills named.",
),
"talk-communication-best-practices-in-quantitative": dict(
    overview="Ed Ma (Bloomberg) on communication in quant finance: presenting technical work to "
             "product, business and leadership audiences with impact.",
    maths=[],
    plain="A model that can't be explained doesn't get deployed: the communication stack — "
          "audience calibration, narrative before detail, visuals over notation — is a production "
          "dependency, not a soft skill.",
),
"talk-communicating-for-impact-in-quant-finance": dict(
    overview="Equipping quants for high-stakes communication: structure, clarity and persuasion "
             "when presenting models and results under pressure.",
    maths=[],
    plain="The risk committee gives you five minutes and one chance: lead with the conclusion, "
          "quantify the uncertainty, anticipate the killer question. Rehearsed clarity is career "
          "leverage.",
),
"talk-how-the-fundamental-analysts-work-in-banks": dict(
    overview="How fundamental analysts actually work in banks: the research process, models, "
             "company access and how their output feeds trading and sales.",
    maths=[],
    plain="Useful reconnaissance for quants: knowing how the fundamental side builds conviction — "
          "channel checks, management meetings, earnings models — reveals both what their "
          "numbers mean and where systematic methods complement them.",
),
"talk-the-power-of-data-and-quantitative": dict(
    overview="Pamela Saliba on quantitative techniques for fundamental portfolio managers: "
             "leveraging data analysis in stock selection and risk management within a "
             "discretionary process.",
    maths=[],
    plain="Quantamental in practice: screens narrow the universe, factor lenses expose unintended "
          "bets, and the human keeps the thesis. The blend beats either purity — when the "
          "boundaries are honest.",
),
"talk-hedge-fund-2-0-the-era-of-the-cyborg": dict(
    overview="Bryan Wisk on the hedge fund industry's evolution: the cyborg era where human "
             "judgment and machine systematicity merge, and what it means for fund structure.",
    maths=[],
    plain="Neither the discretionary hero nor the pure machine won: the surviving model is the "
          "cyborg — human theses executed and risk-managed by systematic infrastructure. The "
          "talk traces the industry's convergence there.",
),
"talk-panel-discussion-saints-and-sinners": dict(
    overview="Panel: how quant finance professionals respond to a new reality and keep delivering "
             "high performance — ethics, incentives and conduct in the profession.",
    maths=[],
    plain="The profession's conscience on stage: where quants have been sinners (complexity as "
          "camouflage, models as marketing) and what sainthood realistically looks like inside "
          "commercial pressure.",
),
"talk-panel-discussion-will-a-new-paradigm-in": dict(
    overview="Panel with Thomas Ho, Sang Bin Lee and David Liu: will a new financial modelling "
             "paradigm rise out of East Asian capital markets?",
    maths=[],
    plain="Markets with different structures — policy banks, retail dominance, distinct "
          "derivatives cultures — may demand different models, not imported ones. The panel "
          "weighs whether the next modelling paradigm speaks Mandarin or Korean first.",
),

# -------------------------------------------------------------------- history
"talk-what-i-dont-like-about-quant-finance": dict(
    overview="Wilmott rails against risk neutrality as a 'cult': false assumptions, limited "
             "modelling frameworks, and his advocacy for more creative, robust and realistic "
             "approaches.",
    maths=[
        ("The heresy stated", r"$$\text{risk-neutral } \mathbb{Q} \ne \text{real world } \mathbb{P} \quad\text{— and hedging is never continuous}$$"),
    ],
    plain="Risk-neutral pricing rests on perfect continuous hedging that no desk performs; treat "
          "it as gospel and you mistake elegance for truth. The rant's serious core: model the "
          "market you trade, not the one that makes the maths pretty.",
),
"talk-the-money-formula": dict(
    overview="Wilmott explores the deadly elegance of finance's hidden powerhouse — the themes of "
             "'The Money Formula': dodgy finance, pseudo-science, and how mathematicians took over "
             "the markets.",
    maths=[],
    plain="Mathematics gave finance power tools and finance used some to cut corners: the book's "
          "tour of quant triumphs and disasters asks where rigor ends and ritual begins — and "
          "who pays when ritual wins.",
),
"talk-my-life-as-a-mathematician": dict(
    overview="Asked constantly 'how can I have a career like yours?', Wilmott answers 'You can't!' "
             "— the events and personality traits behind an unrepeatable path through quant "
             "finance.",
    maths=[],
    plain="An anti-career-guide: luck, contrarianism and the willingness to be the Marmite of "
          "quants. The transferable part isn't the path but the posture — independence of mind "
          "over credential accumulation.",
),
"talk-odsc-keynote-a-new-kind-of-dinosaur": dict(
    overview="Wilmott at ODSC on the past and future: old and new theories and models in quant "
             "finance, and whether classical quants are dinosaurs — or a new kind of one.",
    maths=[],
    plain="Data science arrived declaring quant theory extinct; markets keep punishing the "
          "theory-free. The keynote's synthesis: the surviving species combines old structural "
          "understanding with new statistical machinery.",
),
"talk-wilmott-magazine-at-20": dict(
    overview="Wilmott and Tudball reflect on twenty years of Wilmott magazine: the research, "
             "models, products and community that shaped two decades of quantitative finance.",
    maths=[],
    plain="Twenty years of the field's house journal is twenty years of its intellectual weather: "
          "what got published, what got argued and how the community's center of gravity moved "
          "from derivatives to data.",
),
"talk-how-i-successfully-forecast-the-results-of": dict(
    overview="Wilmott's two-part account of forecasting the 2015 UK general election: methodology, "
             "polling adjustments and why his approach beat the pollsters.",
    maths=[
        ("Bias-corrected polling", r"$$\hat{p} = p_{\text{poll}} + \text{systematic corrections (shy voters, turnout, herding)}$$"),
    ],
    plain="Polls in 2015 all missed the same way — herding and uncorrected bias. Treating "
          "pollsters as correlated noisy instruments, not oracles, produced a forecast that "
          "embarrassed the industry. Quant thinking, exported.",
),
"talk-20-years-of-cqf-and-the-evolution-of": dict(
    overview="Wilmott, Gug and Tudball's panel on the CQF's 20th anniversary: pioneering online "
             "quant education, evolving with the field, and adapting to innovations like AI.",
    maths=[],
    plain="The program's history mirrors the profession's: derivatives-heavy at birth, "
          "risk-focused after 2008, ML-infused now. The panel reads the curriculum as a proxy "
          "for what the market values in a quant.",
),
"talk-a-stylized-history-of-quantitative-finance": dict(
    overview="Emanuel Derman's seventy-year arc: models quantifying derivatives, diffusion, risk, "
             "volatility, diversification, hedging and no-arbitrage — how each idea linked risk "
             "to return.",
    maths=[
        ("The through-line", r"$$\text{Bachelier} \to \text{Markowitz} \to \text{CAPM} \to \text{BSM} \to \text{smiles} \to \text{today}$$"),
    ],
    plain="Derman compresses a century into one idea evolving: how to price risk. Each "
          "generation's model kept the skeleton and replaced an assumption — a history that "
          "doubles as a map of which assumption falls next.",
),
"talk-how-jim-simons-and-a-group-of-unlikely": dict(
    overview="Gregory Zuckerman tells the Renaissance story: how Simons and unlikely "
             "mathematicians solved the market, launched the quantitative revolution, and built "
             "the Medallion track record.",
    maths=[
        ("The compounding legend", r"$$\sim 66\%\ \text{gross p.a. (Medallion, decades)} \quad\text{— capacity-capped by design}$$"),
    ],
    plain="The best investment record ever belongs to people who ignored finance theory and "
          "treated markets as a signal-processing problem. The story's lessons: data obsession, "
          "collaboration structure and ruthless capacity discipline.",
),
"talk-don-quixote-on-wall-street": dict(
    overview="Finance read through literature: Borges' Pierre Menard and market models illuminate "
             "originality, replication and the impossibility of predicting financial futures.",
    maths=[],
    plain="Menard rewrote Don Quixote word-for-word and made it new; a backtest replays history "
          "and calls it foresight. The literary lens exposes what quantitative replication can "
          "and cannot claim about originality and prediction.",
),
"talk-the-blank-swan": dict(
    overview="Elie Ayache's philosophical provocation: after black swans, the blank swan — the "
             "market as the medium of contingency where writing prices precedes probability "
             "itself.",
    maths=[],
    plain="Ayache inverts the standard picture: models don't generate prices, the traded price is "
          "primary and models are commentary after the fact. Dense philosophy, but it sharpens "
          "every question about what calibration means.",
),
"talk-the-unbearable-lightness-of-benchmarks-and": dict(
    overview="Around 'The Financial Metaverse': derivatives as digital twins of their underlyings, "
             "and why the lightness of benchmarks matters for modelling synthetic assets.",
    maths=[
        ("Benchmark as an index map", r"$$\text{derivative} = f(\text{benchmark fixing}) \quad\text{— fragile when the fixing is thin}$$"),
    ],
    plain="Trillions settle on benchmarks produced by thin panels and thinner markets — LIBOR's "
          "ghost warns what happens when the twin outweighs the original. The metaverse framing: "
          "synthetic assets increasingly reference other synthetics.",
),
"talk-a-rationally-ig-nobel-view-of-finance": dict(
    overview="Judging from finance Nobels, excess volatility is irrational exuberance and vol-of-"
             "vol is disconnected from fundamentals — an irreverent, Ig-Nobel-spirited counter-"
             "reading.",
    maths=[
        ("Excess volatility puzzle", r"$$\operatorname{Var}(P) \gg \operatorname{Var}\!\left( PV(\text{dividends}) \right) \quad\text{(Shiller)}$$"),
    ],
    plain="Prize-winning theories explain markets that don't quite exist; the Ig-Nobel view "
          "celebrates the anomalies instead. Satirical in tone, serious in content: the puzzles "
          "are the field's real curriculum.",
),
"talk-gods-money-the-key-to-unlimited-clean-energy": dict(
    overview="Espen Gaarder Haug on alternative monetary systems: linking money to energy, and "
             "accessing the vast energy potential in matter — the age of abundance thesis.",
    maths=[
        ("The ultimate reserve", r"$$E = mc^2 \quad\text{— matter as the deepest energy (and value?) store}$$"),
    ],
    plain="If money is a claim on energy, then monetary systems should be judged by their energy "
          "backing — a heterodox lens connecting physics, currency debasement and the clean-"
          "energy endgame. Speculative by design, stimulating throughout.",
),
"talk-worrying-about-alpha-companion-talk-see-6": dict(
    overview="Companion delivery of Adam Rej's 'Worrying about Alpha': in-sample overfitting and "
             "arbitrage-driven decay of systematic strategies in production (see the Portfolio & "
             "Allocation section for the merged main entry).",
    maths=[
        ("The two decay channels", r"$$\text{IR}_{\text{live}} = \text{IR}_{\text{true}} \times (1 - \text{crowding}) \quad\text{vs}\quad \text{IR}_{\text{true}} = 0 \text{ all along}$$"),
    ],
    plain="The same diagnosis from a second angle: strategies fail either because the backtest "
          "hallucinated or because success invited the crowd. Both talks together form the "
          "field's best short course on strategy mortality.",
),
}

# Content for §8 Machine Learning & AI talks — consumed by enrich_talks.py
# NOTE: talk-llm-quant, talk-ai-safety, talk-ai-risk-management absent (pre-existing pages).
CONTENT = {

"talk-zero-to-ai-series-jon-mcloone-introduction": dict(
    overview="Jon McLoone's eight-part Zero to AI series: Wolfram Language syntax, machine learning "
             "paradigms, prediction and sequence prediction, unbalanced data, feature extraction and "
             "dimension reduction, neural networks, and deployment of the data science workflow.",
    maths=[
        ("The supervised learning core", r"$$\hat{f} = \arg\min_{f \in \mathcal{F}} \; \frac{1}{n}\sum_i L\!\left(y_i, f(x_i)\right) + \Omega(f)$$"),
    ],
    plain="An honest from-scratch on-ramp: what machine learning is (function fitting with "
          "discipline), when each paradigm applies, and how a complete workflow — data to deployed "
          "model — looks when the tooling gets out of the way.",
),
"talk-wolfram-managing-risk-in-ai-series-parts-01": dict(
    overview="The six-part Managing Risk in AI series: what modern AI can and cannot do, when ML is "
             "appropriate, sources of bias, validation, measuring performance, explainability limits, "
             "when predictions justify decisions, and the ethics of human-machine decision-making.",
    maths=[
        ("Decision-grade prediction", r"$$\text{act} \iff \mathbb{E}[\text{benefit} \,|\, \hat{y}] > \text{cost}, \quad \text{with calibrated } \hat{y}$$"),
    ],
    plain="AI risk management in six lessons: most failures come not from bad models but from "
          "using adequate models on questions they shouldn't decide. Bias enters through data, "
          "leaves through validation, and accountability stays human throughout.",
),
"talk-from-zero-to-ai-in-45-minutes": dict(
    overview="The compressed version: machine learning from zero to working examples in 45 minutes "
             "— paradigms, a build, and honest limits.",
    maths=[],
    plain="A whirlwind proof that the core of ML fits in a lunch break: define the task, fit, "
          "validate, deploy. The speed is the message — the barrier to entry is lower than the "
          "mystique suggests.",
),
"talk-you-can-ai-like-an-expert": dict(
    overview="Making AI just another tool for everyday data science: the steps that let anyone with "
             "basic coding achieve significant results with modern automated ML.",
    maths=[],
    plain="Expert-level AI results increasingly come from expert-level problem framing, not "
          "hand-tuned networks: automated tooling handles the optimization while you supply the "
          "domain sense. Democratization, demonstrated live.",
),
"talk-reinforcement-learning-classical-techniques": dict(
    overview="Reinforcement learning explained through classical techniques: the terminology "
             "(states, actions, rewards, policies), core algorithms, worked examples and a guide to "
             "good resources.",
    maths=[
        ("Bellman equation", r"$$Q(s,a) = r(s,a) + \gamma\, \mathbb{E}_{s'}\!\left[ \max_{a'} Q(s', a') \right]$$"),
    ],
    plain="RL is dynamic programming that learns the dynamics by trial: act, observe, update value "
          "estimates, repeat. Everything else — deep RL included — is machinery for making that "
          "loop work when states are too many to enumerate.",
),
"talk-qi-applications-of-reinforcement-learning-in": dict(
    overview="John Hull on RL applied to hedging: learning hedge policies under transaction costs "
             "where classical delta hedging is suboptimal, from the Quant Insights ML conference.",
    maths=[
        ("Hedging as RL objective", r"$$\min_\pi\; \mathbb{E}\!\left[ C_T \right] + \lambda\, \operatorname{sd}(C_T), \qquad C_T = \text{hedging cost under policy } \pi$$"),
    ],
    plain="With trading costs, the optimal hedge is not the delta — it hedges less, later, and "
          "asymmetrically. RL discovers that policy from simulation without anyone deriving it, "
          "and beats delta hedging exactly where theory says it should.",
),
"talk-qi-results-on-pricing-american-options-with": dict(
    overview="Daniel Bloch's results on pricing American options with reinforcement learning: "
             "optimal stopping as an RL problem, benchmarked against classical methods.",
    maths=[
        ("Stopping as control", r"$$V(s) = \max\!\left( \Pi(s),\; \mathbb{E}[V(s')] \right) \quad\text{— exercise vs continue, learned}$$"),
    ],
    plain="Early exercise is the original sequential decision problem, so RL is a natural fit: "
          "learn the continuation value by interacting with simulated paths. The interesting "
          "part is where it matches Longstaff-Schwartz and where it finds more.",
),
"talk-reinforcement-learning-interpretability": dict(
    overview="Interpreting RL-based trading strategies: methods to understand what a learned "
             "policy responds to, and to audit RL traders before capital touches them.",
    maths=[
        ("Policy attribution", r"$$\frac{\partial \pi(a|s)}{\partial s_i} \quad\text{— which state features drive the action}$$"),
    ],
    plain="An RL trader that can't explain itself is unmanageable risk: interpretability tools — "
          "feature attribution, policy distillation, counterfactual probing — turn the black box "
          "into something a risk committee can interrogate.",
),
"talk-reinforcement-learning-and-hidden-markov": dict(
    overview="Samit Ahlawat's two methodologies for smart trading strategies: hidden Markov model "
             "regime detection and reinforcement learning, both addressing the myopia of static "
             "rule-based trading.",
    maths=[
        ("HMM regime filter", r"$$\mathbb{P}(z_t \,|\, x_{1:t}) \propto \mathbb{P}(x_t | z_t) \sum_{z_{t-1}} \mathbb{P}(z_t | z_{t-1})\, \mathbb{P}(z_{t-1} | x_{1:t-1})$$"),
    ],
    plain="Static rules can't tell a trending market from a mean-reverting one; an HMM infers the "
          "hidden regime and RL learns what to do in each. Together they give rules a memory and "
          "a context.",
),
"talk-deep-reinforcement-learning-for-asset": dict(
    overview="Deep RL for US equity asset allocation: solving the dynamic portfolio problem "
             "almost model-free by maximizing a reward over state and action spaces.",
    maths=[
        ("Portfolio RL formulation", r"$$\max_\pi\; \mathbb{E}\left[ \sum_t \gamma^t\, r(w_t, R_{t+1}) \right], \qquad r = \text{utility of wealth change}$$"),
    ],
    plain="Classic dynamic allocation needs a model of returns; deep RL skips it and learns "
          "allocation from data directly. The price: sample hunger and fragility to regime change "
          "— both quantified in the results.",
),
"talk-financial-reasoning-agents-in-context": dict(
    overview="LLMs meeting reinforcement learning for financial agents: in-context RL and test-time "
             "compute, where reasoning depth trades off against real-time decision latency.",
    maths=[
        ("Test-time compute trade-off", r"$$\text{quality}(\hat{a}) \uparrow \text{ with thinking tokens}, \quad \text{latency budget fixed by markets}$$"),
    ],
    plain="New-generation agents can 'think longer' on demand — but markets bill by the "
          "millisecond. The frontier question: which financial decisions merit slow reasoning, "
          "and which must stay reflexes.",
),
"talk-deep-learning-techniques-in-derivatives": dict(
    overview="Credit Suisse quants on deep learning in derivatives pricing: architectures, training "
             "regimes and deployment of neural approximators inside an equity derivatives "
             "business.",
    maths=[
        ("Pricing surrogate", r"$$\text{NN}_\theta(S, K, T, \sigma, \dots) \approx V, \qquad \sup_{\text{domain}} |NN - V| < \text{tol}$$"),
    ],
    plain="A bank-grade account of the surrogate-pricing workflow: sample the slow model offline, "
          "train, bound the error, and serve microsecond prices — with the validation story that "
          "makes it deployable.",
),
"talk-deep-learning-for-derivatives-pricing-from": dict(
    overview="Tim Wood's foundation-to-practice tour: deep learning fundamentals, then efficient "
             "pricing applications on NVIDIA accelerated computing, through increasingly demanding "
             "examples.",
    maths=[
        ("Universal approximation", r"$$\forall \varepsilon > 0\; \exists \text{NN}: \|f - \text{NN}\|_\infty < \varepsilon \;\text{on compacts}$$"),
    ],
    plain="From perceptron to exotic pricer in one arc, with the GPU as co-star: the demos "
          "escalate until a full pricing model trains and serves at speeds that change what's "
          "operationally possible.",
),
"talk-the-application-of-deep-learning-to-high": dict(
    overview="Deep learning for high-dimensional models in finance: PDEs and expectations in "
             "dimensions where grids die, solved with neural parameterizations.",
    maths=[
        ("Deep BSDE method", r"$$V(0, x) \approx \theta_0, \quad \text{NN learns } \nabla V \text{ along simulated paths}$$"),
    ],
    plain="A 100-asset option has no grid — but a neural network can represent the value function "
          "and learn it along Monte Carlo paths. Deep solvers turned 'impossible dimension' into "
          "'expensive but doable'.",
),
"talk-on-accuracy-guarantees-for-machine-learning": dict(
    overview="Riskfuel on accuracy guarantees for ML pricing surrogates: achieving million-fold "
             "speedups without compromising accuracy, and the validation evidence behind the "
             "claim.",
    maths=[
        ("Domain-bounded guarantee", r"$$\max_{x \in \mathcal{D}} \left| \text{NN}(x) - V(x) \right| < \varepsilon \quad\text{— certified by dense sampling}$$"),
    ],
    plain="'Fast but is it right?' is the only question that matters for surrogates. The answer "
          "is engineering: define the domain, sample it brutally, measure worst-case error and "
          "refuse extrapolation. Guarantees by construction, not hope.",
),
"talk-building-neural-networks-that-calibrate-to": dict(
    overview="Thijs van den Berg's parametric neural architecture for real-time calibration: "
             "networks that are superior in both model performance and calibration speed.",
    maths=[
        ("Inverse-map learning", r"$$\text{NN}: \text{market quotes} \mapsto \theta^* \quad\text{— calibration as a learned function}$$"),
    ],
    plain="Instead of optimizing parameters per calibration, learn the whole quotes-to-parameters "
          "map once: calibration becomes a forward pass. Every recalibration after that is "
          "effectively free.",
),
"talk-neural-parametric-models-novel-modelling": dict(
    overview="A generic ML method to extract parametric models and calibration algorithms directly "
             "from data: neural parametric models bridging flexibility and interpretability.",
    maths=[
        ("Structured decomposition", r"$$f(x; \theta) = \text{interpretable form}, \qquad \theta = \text{NN}(\text{data})$$"),
    ],
    plain="Pure networks are flexible and opaque; classic parametrics are readable and rigid. "
          "Letting a network choose the parameters of an interpretable form captures both — the "
          "model stays explainable while the fitting gets superhuman.",
),
"talk-alternatives-to-deep-neural-networks-for": dict(
    overview="Neo-classical alternatives to DNNs for financial function approximation: with limited "
             "data and explainability requirements, splines, kernels and Chebyshev methods often "
             "win.",
    maths=[
        ("The comparison axis", r"$$\text{data-hungry, opaque DNN} \quad\text{vs}\quad \text{sample-efficient, certified classical approximators}$$"),
    ],
    plain="Finance rarely has ImageNet-scale data, and regulators dislike shrugs. On smooth "
          "pricing functions with modest data, spectral and kernel methods match networks with "
          "error bounds attached — fashion isn't a reason.",
),
"talk-non-adversarial-training-of-neural-sdes-with": dict(
    overview="Training neural SDE market generators without adversarial instability: signature "
             "kernel scores as the objective for simulating realistic market behaviour.",
    maths=[
        ("Signature kernel score", r"$$\mathcal{L} = \text{MMD}_{k_{\text{sig}}}\!\left( \text{real paths}, \text{generated paths} \right)$$"),
    ],
    plain="GAN training fights itself; scoring generated paths against real ones with a signature "
          "kernel gives a stable, proper objective. Neural SDEs then learn market dynamics — "
          "tails, clustering — without the adversarial drama.",
),
"talk-generative-models-and-predictive-machines": dict(
    overview="Kernel-based (RKHS) generative and predictive methods with uncertainty "
             "quantification for financial applications: theory and performance.",
    maths=[
        ("Kernel ridge prediction", r"$$\hat{f}(x) = k(x, X)\,(K + \lambda I)^{-1} y, \qquad \text{posterior variance for free}$$"),
    ],
    plain="Kernel methods are the adults in the room: closed-form training, built-in uncertainty, "
          "proofs. For mid-sized financial problems they match networks while telling you how "
          "confident to be — which is half the job in finance.",
),
"talk-financial-applications-with-kernels": dict(
    overview="Kernel (RKHS) algorithms across quant finance: pricing, risk computation, trend "
             "detection and portfolio optimization with excellent performance.",
    maths=[
        ("The kernel trick", r"$$k(x, x') = \langle \phi(x), \phi(x') \rangle \quad\text{— nonlinearity without explicit features}$$"),
    ],
    plain="One mathematical move — inner products in feature space — powers a whole toolkit: "
          "nonlinear regression, generation, optimization. This talk is the applied catalogue "
          "for finance, benchmarks included.",
),
"talk-mixture-models-for-genai": dict(
    overview="Mixture models as GenAI for markets: generating reliable synthetic market data with "
             "classical mixture machinery — transparent, calibratable and tail-aware.",
    maths=[
        ("Gaussian mixture density", r"$$p(x) = \sum_k \pi_k\, \mathcal{N}(x; \mu_k, \Sigma_k) \quad\text{— regimes as components}$$"),
    ],
    plain="Before reaching for diffusion models, mixtures already generate: components map to "
          "regimes, tails are explicit, and every parameter is auditable. Synthetic market data "
          "with a paper trail.",
),
"talk-panel-data-driven-market-generators-and": dict(
    overview="Panel on data-driven market generators and their model governance: sequential-data "
             "ML as market simulator, and the validation questions it raises.",
    maths=[],
    plain="Synthetic markets promise unlimited stress scenarios and privacy-safe data sharing — "
          "if you can validate a generator whose job is producing things that never happened. "
          "The governance debate is the interesting part.",
),
"talk-qi-decoding-the-auto-encoder": dict(
    overview="Jesper Andreasen decodes the autoencoder: what the architecture actually does, "
             "demystified for quants, with pricing and curve applications.",
    maths=[
        ("Autoencoder objective", r"$$\min_{\theta}\; \| x - D_\theta(E_\theta(x)) \|^2, \qquad \dim(\text{code}) \ll \dim(x)$$"),
    ],
    plain="An autoencoder is nonlinear PCA with attitude: squeeze data through a bottleneck and "
          "the code that survives is the structure. Kwant-legend commentary on when that beats "
          "plain PCA and when it's just harder to explain.",
),
"talk-ai-and-machine-learning-in-quant-finance": dict(
    overview="Autoencoders describing yield curve shapes with 2-3 factors: demonstrated across "
             "10 currencies and 12 years of cross-sectional data.",
    maths=[
        ("Curve compression", r"$$y(\tau) \approx D\!\left( z_1, z_2, z_3 \right), \qquad z = E(y) \text{ — nonlinear level/slope/curvature}$$"),
    ],
    plain="PCA's level-slope-curvature is linear; autoencoders find the curved version and fit "
          "ten currencies with the same tiny code. Fewer factors, better reconstruction — and a "
          "new question: what are these factors economically?",
),
"talk-risk-factor-aggregation-and-stress-testing": dict(
    overview="Natalie Packham on PCA and autoencoders for aggregating risk factors in stress "
             "testing: scenario construction applied to DAX and S&P portfolios.",
    maths=[
        ("Stress in factor space", r"$$x_{\text{stress}} = \bar{x} + \sum_{k} s_k\, \phi_k \quad\text{— shock the factors, map back coherently}$$"),
    ],
    plain="Stressing hundreds of risk factors independently produces impossible scenarios; "
          "stressing their learned low-dimensional drivers produces severe-but-plausible ones. "
          "Autoencoders extend the trick where linear factors fall short.",
),
"talk-risk-factor-detection-with-methods-from": dict(
    overview="Explainable ML for risk factor detection: post-crisis regulatory attention meets "
             "SHAP-style attribution to find which factors genuinely drive portfolio risk.",
    maths=[
        ("Shapley attribution", r"$$\phi_i = \sum_{S \subseteq N \setminus i} \frac{|S|!\,(n-|S|-1)!}{n!} \left[ v(S \cup i) - v(S) \right]$$"),
    ],
    plain="ML finds risk drivers linear models miss, but risk management can't act on 'the "
          "network says so'. Shapley values split the prediction among factors fairly — "
          "game theory as the translator between model and committee.",
),
"talk-developments-and-applications-in-explainable": dict(
    overview="Panel of portfolio-management practitioners on explainable ML: experiences and best "
             "practices as ML transitions from cutting edge to standard toolkit.",
    maths=[],
    plain="Practitioners compare notes on the explainability tax: which methods clients accept, "
          "which attributions actually inform decisions, and where 'explainable' has become "
          "compliance theatre versus genuine understanding.",
),
"talk-the-psychology-of-llms": dict(
    overview="LLMs in classic behavioural psychology experiments: AI reproduces human cognitive "
             "biases and human-like errors of logic and recall — with consequences for financial "
             "use.",
    maths=[
        ("Bias inheritance", r"$$\text{human text} \to \text{training data} \to \text{human-like biases in the model}$$"),
    ],
    plain="Train on human writing, inherit human folly: LLMs anchor, frame and overconfide like "
          "their teachers. Deploying them in finance means behavioural-bias risk management for "
          "software — a genuinely new category.",
),
"talk-how-to-choose-a-threshold-for-an-evaluation": dict(
    overview="Choosing thresholds for LLM evaluation metrics: making 'good enough for production' "
             "a statistically grounded decision for reliability monitoring.",
    maths=[
        ("Threshold as hypothesis test", r"$$\text{deploy} \iff \mathbb{P}(\text{metric} \ge \tau \,|\, \text{data}) \ge 1 - \alpha$$"),
    ],
    plain="Every LLM guardrail hides an arbitrary number; this work replaces folklore thresholds "
          "with calibrated ones — error rates you chose deliberately rather than inherited from "
          "a demo notebook.",
),
"talk-beyond-agent-washing-from-idea-to": dict(
    overview="Against 'agent-washing': most so-called agentic AI in finance is API wrappers "
             "without autonomy — what real agentic infrastructure requires, from idea to "
             "production.",
    maths=[],
    plain="Calling a chatbot with function calls an 'autonomous agent' is this cycle's "
          "vaporware. Real agency needs state, goals, verification and accountability — an "
          "infrastructure checklist this talk supplies for separating shipping from showing.",
),
"talk-ai-powered-traders-ready-or-not": dict(
    overview="Pradeep's update on the trader of tomorrow: NLP, HPC and AI advances, synthetic "
             "data, and computing technology shifts reshaping trading desks.",
    maths=[],
    plain="A progress report from the front: which AI capabilities crossed from demo to desk "
          "this year — and the readiness question pointed at both the technology and the "
          "traders it augments.",
),
"talk-ai-liars-poker": dict(
    overview="Aaron Brown pits AI against Liar's Poker: respectable play but not yet superhuman, "
             "and the parallels between the game's deception dynamics and trading.",
    maths=[
        ("Bluffing equilibrium", r"$$\text{optimal play mixes truth and bluff: } \pi^*(\text{bid} \,|\, \text{hand}) \text{ randomized}$$"),
    ],
    plain="Liar's Poker is trading distilled: incomplete information, deception and reading "
          "opponents. AI handles the probabilities and struggles with the theatre — a scoreboard "
          "for how much of trading is still human game.",
),
"talk-ai-ml-in-systematic-investing-and-trading": dict(
    overview="AI/ML's transformation of systematic investing: recent advances across the strategy "
             "development pipeline and the challenges ahead.",
    maths=[],
    plain="A field survey with a practitioner's skepticism: where ML genuinely upgraded the "
          "pipeline (features, execution, risk) versus where classical statistics still rules "
          "(portfolio construction, small-sample inference).",
),
"talk-the-application-of-ai-to-quantitative": dict(
    overview="AI applied to quantitative systematic strategies: concrete opportunities, concrete "
             "risks, and the discipline separating one from the other.",
    maths=[],
    plain="The double ledger: alpha from new data and nonlinearity on one side; overfitting, "
          "crowding and regime fragility on the other. Process — not enthusiasm — determines "
          "which column dominates.",
),
"talk-cqf-institute-machine-learning-in-systematic": dict(
    overview="ML in systematic futures allocation: seven years of research corpus and gradual "
             "practitioner adoption, applied to CTA-style portfolios.",
    maths=[
        ("ML-enhanced trend allocation", r"$$w_i \propto \text{ML}\!\left( \text{trend, carry, vol features}_i \right) / \hat\sigma_i$$"),
    ],
    plain="Futures allocation is a natural ML testbed — liquid, long histories, defined universe. "
          "The talk reports what seven years of literature says actually improves a CTA: modest, "
          "real gains in signal blending and risk timing.",
),
"talk-machine-learning-for-tactical-asset": dict(
    overview="ML for tactical asset allocation: regime features and cross-asset signals for "
             "shifting weights at monthly-to-quarterly horizons.",
    maths=[
        ("TAA classifier", r"$$\mathbb{P}(\text{risk-on}_{t+1}) = f_{\text{ML}}\!\left( \text{macro, momentum, vol}_t \right)$$"),
    ],
    plain="TAA has few independent decisions per decade — brutal for data-hungry methods. The "
          "honest recipe: heavy regularization, economically-motivated features and expectations "
          "calibrated to the sample size.",
),
"talk-machine-learning-for-financial-markets": dict(
    overview="A practitioner overview of ML for financial markets: the method landscape mapped to "
             "market problems, with adoption guidance.",
    maths=[],
    plain="A matching exercise: trees for tabular alpha, sequence models for flow, kernels for "
          "small data — and the market problems where classical econometrics remains the "
          "undefeated champion.",
),
"talk-machine-learning-for-factor-based": dict(
    overview="ML for factor-based commodity investing: transplanting the equity ML playbook to "
             "commodities, where fundamentals, seasonality and roll dynamics change the game.",
    maths=[
        ("Commodity factor set", r"$$R_i = f\!\left( \text{basis}_i, \text{momentum}_i, \text{inventory}_i, \text{seasonality}_i \right)$$"),
    ],
    plain="Commodity 'value' is the futures basis and 'quality' is inventory cover: the factors "
          "translate but their clothes don't. ML earns its keep combining them nonlinearly — "
          "curve shape times stocks times season.",
),
"talk-using-machine-learning-algorithms-to": dict(
    overview="ML estimating the functional form of optimal trading strategies: a stochastic-"
             "programming framework where the learned policy replaces closed-form rules.",
    maths=[
        ("Learned policy form", r"$$a_t = f_{\text{ML}}(\text{alpha}_t, \text{inventory}_t, \text{cost state}_t) \approx \text{unknown optimal } f^*$$"),
    ],
    plain="Optimal execution with alpha has no closed form once costs get realistic; let a "
          "learner approximate the policy directly from the stochastic program. The output "
          "resembles known solutions where they exist — and extends beyond them.",
),
"talk-how-machine-learning-can-help-stock-pickers": dict(
    overview="ML as augmentation for fundamental stock pickers: screening, idea triage and risk "
             "flags that raise a discretionary process's hit rate.",
    maths=[],
    plain="The machine reads ten thousand filings so the analyst reads ten good ones: ML as "
          "attention allocation for stock pickers, keeping human judgment where it earns its "
          "fees and automation where it doesn't.",
),
"talk-how-ai-is-used-to-generate-alpha-in-the": dict(
    overview="Renee Yao's journey from Citadel and Millennium to founding Neo Ivy Capital: "
             "building an AI-native hedge fund and how its alpha generation differs.",
    maths=[],
    plain="A founder's account of leaving the pod world to build AI-first: what breaks when you "
          "replace analyst pipelines with learned systems, and what the incumbents can't easily "
          "copy.",
),
"talk-how-ai-is-used-to-generate-alpha-in": dict(
    overview="Neo Ivy's approach since 2014: AI strategies leveraging leading indicators and "
             "intertwined systems, versus traditional machine learning's lagging features.",
    maths=[
        ("Leading vs lagging features", r"$$x_{\text{lead}} \to R_{t+1} \quad\text{vs}\quad x_{\text{lag}} \to R_{t+1} \text{ (already priced)}$$"),
    ],
    plain="The differentiation claim: most quant ML learns from what markets already digested; "
          "systems built on leading indicators — flows before prices, activity before earnings "
          "— trade tomorrow's information today.",
),
"talk-using-ai-to-integrate-behavioral-insights": dict(
    overview="AI integrating behavioural insights into investment strategies: detecting and "
             "exploiting the systematic mistakes of other market participants.",
    maths=[
        ("Behavioural alpha template", r"$$\alpha \propto \text{overreaction}_{\text{detected}} - \text{underreaction}_{\text{detected}}$$"),
    ],
    plain="Behavioural finance names the biases; AI finds them at scale in real time — panic "
          "selling signatures, anchored analysts, herding funds. The strategy is being the "
          "counterparty to measurable human error.",
),
"talk-the-use-of-big-data-and-artificial": dict(
    overview="Big data and AI as alpha generators: the data-driven investment stack from "
             "alternative sources through signals to portfolios.",
    maths=[],
    plain="The industrialization of edge: alpha increasingly comes from data logistics — "
          "acquiring, cleaning and joining sources faster than rivals — with the model itself "
          "as the least differentiated layer.",
),
"talk-fundamentals-for-finding-alpha-signals-with": dict(
    overview="Alpha signals from AI plus influencer analysis plus big data: the fundamentals of "
             "constructing and validating such signals.",
    maths=[
        ("Signal validation gauntlet", r"$$\text{IC} > 0 \;\text{out-of-sample},\; \text{decay profiled},\; \text{capacity estimated}$$"),
    ],
    plain="Exotic data doesn't exempt a signal from the boring tests: out-of-sample IC, decay "
          "curves, capacity. Influencer feeds and web exhaust enter the same gauntlet as price "
          "momentum — most don't survive it.",
),
"talk-putting-big-data-advanced-analytics-and": dict(
    overview="Big data, advanced analytics and breakthrough strategies put to work in financial "
             "markets: an implementation-focused walkthrough.",
    maths=[],
    plain="From proof-of-concept to production: the unglamorous 80% — data engineering, "
          "monitoring, failure handling — that turns an analytics demo into something that "
          "trades money unattended.",
),
"talk-quantamental-factor-investing-using": dict(
    overview="Quantamental factor investing with alternative data and ML: blending fundamental "
             "insight with systematic factor construction.",
    maths=[
        ("Quantamental blend", r"$$\text{score}_i = \lambda\, \text{factor}_i + (1-\lambda)\, \text{analyst view}_i$$"),
    ],
    plain="Alt data lets factors read what analysts read — supply chains, hiring, satellite "
          "imagery — while ML fuses it with classic signals. The quantamental promise: "
          "fundamental insight at systematic breadth.",
),
"talk-drawdown-mitigation-via-identification-and": dict(
    overview="Data-driven drawdown mitigation in equity index investing: identifying and "
             "predicting risk-off periods with ML to cut exposure before the damage.",
    maths=[
        ("Drawdown regime classifier", r"$$\mathbb{P}(\text{drawdown regime}) = f\!\left( \text{vol structure, breadth, credit, flows} \right)$$"),
    ],
    plain="Crashes cluster in identifiable conditions — stressed credit, narrow breadth, "
          "inverted vol curves. A classifier trained on those fingerprints won't call tops, but "
          "cutting exposure when it fires historically dodged the worst months.",
),
"talk-predicting-financial-crises-with-machine": dict(
    overview="Anticipating banking crises with ML: a data-driven early-warning approach for "
             "global financial stability.",
    maths=[
        ("Early-warning objective", r"$$\max\; \text{AUC subject to lead time} \ge k \text{ quarters}$$"),
    ],
    plain="Credit booms, asset bubbles and external imbalances precede banking crises with "
          "enough regularity for ML to score them. The hard trade-off is timing: early enough "
          "to act, specific enough to believe.",
),
"talk-practical-aspects-of-applying-deep-learning": dict(
    overview="Deep learning for market making in practice: latency budgets, feature staleness, "
             "and model management where microseconds and adverse selection rule.",
    maths=[
        ("The market maker's constraint", r"$$\text{inference time} + \text{feature latency} \ll \text{quote update interval}$$"),
    ],
    plain="A brilliant model that answers late is a liability in market making: the talk is "
          "about engineering deep learning to fit inside the latency and adverse-selection "
          "budget — distillation, caching, and knowing when simpler wins.",
),
"talk-hedging-in-the-age-of-statistical-learning": dict(
    overview="Proxy GMM Hedge: a data-driven, model-free approach to hedging introduced as an "
             "alternative to model-based Greeks.",
    maths=[
        ("Statistical hedge ratio", r"$$h^* = \arg\min_h\; \widehat{\operatorname{Var}}\!\left( \Delta V - h\, \Delta S \right) \quad\text{— estimated, not derived}$$"),
    ],
    plain="Why trust a model's delta when you can measure the hedge that historically minimized "
          "variance? Statistical hedging skips the model middleman — at the cost of needing "
          "history to resemble the future.",
),
"talk-what-we-learned-from-kaggle-two-sigma-news": dict(
    overview="Lessons from the Kaggle Two Sigma news competition: what thousands of teams "
             "discovered about predicting returns from news data — and about competitions.",
    maths=[
        ("The leaderboard lesson", r"$$\text{public LB rank} \not\Rightarrow \text{private LB rank} \quad\text{— overfitting at competition scale}$$"),
    ],
    plain="Crowdsourcing produced clever features and a masterclass in overfitting: public "
          "leaderboard heroes collapsed on private data. The meta-lesson for quant hiring and "
          "research process design outlasted the signals.",
),
"talk-qi-zero-knowledge-machine-learning": dict(
    overview="Aaron Brown on zero-knowledge machine learning: proving properties of models and "
             "data without revealing either — cryptography meeting quant finance.",
    maths=[
        ("ZK guarantee (schematic)", r"$$\text{prove } f(x) = y \;\text{without revealing } f \text{ or } x$$"),
    ],
    plain="Imagine proving to a regulator that your model passed every test without showing the "
          "model, or renting a strategy's signals without exposing it. Zero-knowledge proofs "
          "make both cryptographically possible — the applications write themselves.",
),
"talk-qi-beating-the-markets-with-hpc-ai": dict(
    overview="Prabhu Ramamoorthy on HPC+AI for alpha and excess returns: accelerated computing "
             "across the financial services stack.",
    maths=[],
    plain="Compute as competitive weapon: when backtests run 100x faster, research iterates "
          "100x more — the alpha is partly in the silicon. A tour of the accelerated stack from "
          "data loading to training to inference.",
),
"talk-genetic-algorithms-and-evolutionary": dict(
    overview="Genetic algorithms and evolutionary computation: nature-inspired solving of hard "
             "financial problems in finite time, with an accessible theoretical foundation.",
    maths=[
        ("Evolution loop", r"$$\text{select} \to \text{crossover} \to \text{mutate} \to \text{evaluate} \to \text{repeat}$$"),
    ],
    plain="When the objective is jagged and gradient-free — trading rule discovery, discrete "
          "portfolio problems — breeding solutions works where calculus can't. The catch is the "
          "same as ever: evolved rules overfit unless the fitness test is honest.",
),
"talk-panel-how-can-we-be-more-ambitious-with-ai": dict(
    overview="Panel: how can finance be more ambitious with AI? Beyond incremental ML adoption "
             "toward transformative uses.",
    maths=[],
    plain="A decade of ML in finance produced mostly incrementalism — better versions of "
          "existing signals. The panel asks what the genuinely ambitious version looks like, "
          "and what institutional courage it demands.",
),
"talk-industry-talk-the-future-of-quants": dict(
    overview="With so much AI hype: the truth about the future and how it affects the quant "
             "profession — and how individuals can prepare.",
    maths=[],
    plain="Neither doom nor hype: AI automates the routinizable parts of quant work and raises "
          "the premium on judgment, problem framing and communication. The preparation list is "
          "concrete and mostly about becoming harder to automate.",
),
"talk-industry-talk-automating-procurement": dict(
    overview="Automating procurement negotiations with AI: agents making supply chains agile — a "
             "case study of applied negotiation AI.",
    maths=[],
    plain="Negotiation bots handling supplier terms at scale: thousands of small negotiations no "
          "human team could staff, each yielding a few percent. Outside finance's core but a "
          "preview of agentic AI doing real economic work.",
),
"talk-mumbai-society-meeting-artificial": dict(
    overview="Shivaram KR in Mumbai on AI in trading: why it's there, and building robust "
             "trading strategies with machine learning and deep learning.",
    maths=[],
    plain="A ground-level workshop: the full strategy pipeline with ML at each stage, and the "
          "robustness checklist — costs, regime tests, capacity — that separates trading systems "
          "from curve-fit souvenirs.",
),
"talk-analytics-and-ai-impact-implementation-and": dict(
    overview="Tony Boobier on analytics and AI in the workplace: implementation realities and the "
             "future of professional work as automation advances.",
    maths=[],
    plain="The organizational half of the AI story: adoption fails on change management more "
          "than on models. What roles transform, what skills appreciate, and how professionals "
          "ride the wave rather than compete with it.",
),
"talk-ai-and-machine-learning-for-risk-management": dict(
    overview="Current AI/ML techniques in risk management: credit risk modelling's growing ML "
             "adoption and applications across the risk stack.",
    maths=[
        ("ML credit scoring", r"$$\mathbb{P}(\text{default}) = f_{\text{GBM/NN}}(x) \quad\text{with explainability constraints}$$"),
    ],
    plain="Risk was ML's quiet early adopter — credit scoring is decades old. The new wave "
          "extends it across market, liquidity and op risk, with regulators insisting the "
          "models explain themselves at supervisory depth.",
),
}

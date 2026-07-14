# Content for §9 NLP, Sentiment & Alt Data talks — consumed by enrich_talks.py
# NOTE: talk-nlp-sdg and talk-sentiment-portfolios absent (pre-existing pages).
CONTENT = {

"talk-sentiment-classification-and-opinion-mining": dict(
    overview="The six-session sentiment classification and opinion mining series (Pullman, "
             "Gonzalez, Kolychyna & Souza, Messina): extracting opinion from news wires and "
             "microblogs, from linguistic foundations to trading-ready sentiment scores.",
    maths=[
        ("Sentiment classification core", r"$$\hat{s} = \arg\max_{s}\; \mathbb{P}(s \,|\, \text{text}) \quad s \in \{-, 0, +\}$$"),
    ],
    plain="Turning language into a tradable number is a pipeline of choices — tokenization, "
          "entity linking, negation handling, aggregation — and each session of this series owns "
          "one stage. The output: sentiment time series with known error bars.",
),
"talk-text-analytics-for-sentiment-extraction-in": dict(
    overview="Text analytics for sentiment extraction in finance, part I: information extraction "
             "and text analytics foundations — entities, events and relations from financial "
             "text.",
    maths=[
        ("TF-IDF weighting", r"$$w_{t,d} = tf_{t,d} \cdot \log\frac{N}{df_t}$$"),
    ],
    plain="Before sentiment comes structure: who did what to whom, in which document, about "
          "which company. Information extraction is the unglamorous 80% of financial NLP and "
          "this session builds it properly.",
),
"talk-text-analytics-for-sentiment-extraction-in-2": dict(
    overview="Part II: techniques of classification and predictive analytics — supervised "
             "sentiment models, feature engineering for text, and validating predictive power on "
             "financial outcomes.",
    maths=[
        ("Text-to-return validation", r"$$R_{t+1} = \alpha + \beta\, \text{Sent}_t + \varepsilon, \qquad \text{test } \beta \ne 0 \text{ out-of-sample}$$"),
    ],
    plain="A sentiment score is only as good as its predictive audit: this session covers the "
          "classifiers and — more importantly — the honest testing that separates signal from "
          "narrative decoration.",
),
"talk-text-analytics-for-sentiment-extraction-in-3": dict(
    overview="Part III: implementation with R and applications analytics — hands-on sentiment "
             "extraction workflows and applied case studies.",
    maths=[],
    plain="The workbench session: real code, real corpora, and the practical details (encoding "
          "messes, stopword choices, aggregation windows) that tutorials omit and practitioners "
          "collide with immediately.",
),
"talk-text-mining-and-deep-learning-for-sentiment": dict(
    overview="Deep learning applied to text mining for sentiment: from bag-of-words to neural "
             "representations for financial sentiment analysis.",
    maths=[
        ("Embedding representation", r"$$\text{word} \mapsto v \in \mathbb{R}^d, \qquad \text{similar meaning} \Rightarrow \text{nearby vectors}$$"),
    ],
    plain="Neural text models read context — 'crude fell' versus 'volatility fell' — where "
          "keyword counting can't. The upgrade from dictionaries to embeddings roughly doubled "
          "what sentiment signals could see.",
),
"talk-deep-learning-for-sentiment-analysis": dict(
    overview="Deep learning architectures for sentiment analysis: CNNs, RNNs and attention for "
             "classifying financial text tone at scale.",
    maths=[
        ("Attention weighting", r"$$\alpha_i = \frac{e^{q^\top k_i}}{\sum_j e^{q^\top k_j}} \quad\text{— the model learns which words matter}$$"),
    ],
    plain="Attention mechanisms let sentiment models show their work: which words drove the "
          "score. In finance that interpretability is not cosmetic — it's how you debug a signal "
          "before it trades.",
),
"talk-sentiment-analysis-in-microblogs": dict(
    overview="Sentiment analysis in microblogs: the special challenges of short, noisy, "
             "sarcasm-rich social text and methods that survive them.",
    maths=[
        ("Aggregated microblog signal", r"$$S_t = \frac{\sum_i w_i\, s_{i,t}}{\sum_i w_i}, \qquad w = \text{author credibility weights}$$"),
    ],
    plain="Tweets are the hardest text in finance: 20 words, irony, bots and cascades. Weighting "
          "by author track record and detecting coordinated posting matter more than classifier "
          "sophistication.",
),
"talk-keynote-sentiment-analysis-for-fun-and": dict(
    overview="Keynote: sentiment analysis for fun and profit — the field surveyed from research "
             "curiosity to production trading input.",
    maths=[],
    plain="A keynote-level map of financial sentiment: what a decade of research established "
          "(short-horizon predictability, event asymmetries), what remains contested, and where "
          "profits actually materialized.",
),
"talk-keynote-modeling-news-impact-asymmetries": dict(
    overview="Keynote on news impact asymmetries: negative news moves markets differently than "
             "positive — modelling the asymmetry for prediction and risk.",
    maths=[
        ("Asymmetric impact", r"$$|\Delta P \,|\, \text{bad news}| > |\Delta P \,|\, \text{good news}| \quad\text{at matched surprise size}$$"),
    ],
    plain="Markets take bad news harder, faster and with longer volatility echoes than good news "
          "of equal size. Any sentiment strategy that ignores the asymmetry is averaging away "
          "its own best signal.",
),
"talk-keynote-text-mining-and-networks-for": dict(
    overview="Keynote: text mining and network methods combined for systemic risk measurement — "
             "who is mentioned with whom, and what co-mention networks reveal about contagion.",
    maths=[
        ("Co-mention network risk", r"$$A_{ij} = \#\{\text{documents mentioning } i \text{ and } j\} \;\to\; \text{centrality} = \text{systemic exposure}$$"),
    ],
    plain="When news repeatedly names two banks in the same breath, markets treat their fates as "
          "linked — and the network of such co-mentions maps perceived contagion channels before "
          "balance-sheet data can.",
),
"talk-econometrics-with-text-data": dict(
    overview="The econometrics of text: transforming qualitative sentiment into quantitative "
             "variables with valid inference — measurement error, generated regressors and "
             "identification with text data.",
    maths=[
        ("Generated-regressor correction", r"$$\hat{\text{Sent}} = \text{Sent} + \eta \;\Rightarrow\; \text{s.e.}(\hat\beta) \text{ must reflect } \eta$$"),
    ],
    plain="A sentiment index is an estimate pretending to be data: regressions using it inherit "
          "its noise. Text econometrics supplies the corrections that keep t-statistics honest "
          "when the regressor came from a language model.",
),
"talk-natural-language-processing-in-trading": dict(
    overview="James Isilay on NLP in trading: bringing information extraction down to "
             "milliseconds, and the technology stack that makes news-driven execution possible.",
    maths=[
        ("The latency race", r"$$t_{\text{parse}} + t_{\text{signal}} + t_{\text{order}} < t_{\text{competitors}} \quad\text{— milliseconds decide}$$"),
    ],
    plain="A headline's value has a half-life of milliseconds: the engineering — co-located "
          "parsers, pre-compiled entity maps, template detection — is the strategy. The NLP is "
          "table stakes; the pipeline is the edge.",
),
"talk-senrisk-sentiment-of-news-and-market": dict(
    overview="SENRISK: news sentiment plus market analysis of sovereign and corporate bonds for "
             "credit risk assessment — sentiment as an early-warning credit input.",
    maths=[
        ("Sentiment-augmented credit score", r"$$\mathbb{P}(\text{downgrade}) = f\!\left( \text{financials}, \text{spreads}, \text{news sentiment} \right)$$"),
    ],
    plain="Credit deterioration leaks into news months before ratings move: supplier disputes, "
          "management exits, covenant chatter. A sentiment layer over bond analysis reads those "
          "leaks systematically.",
),
"talk-correlation-influence-networks-for-sentiment": dict(
    overview="Correlation influence networks for sentiment in European sovereign bonds: how "
             "sentiment propagates between sovereigns and what the network implies for spreads.",
    maths=[
        ("Sentiment spillover", r"$$\text{Sent}_{i,t} = \sum_j \phi_{ij}\, \text{Sent}_{j,t-1} + \varepsilon \quad\text{— the influence matrix } \Phi$$"),
    ],
    plain="Eurozone sentiment is contagious by construction: bad news about one periphery "
          "sovereign re-prices the others. Estimating the influence network shows which "
          "country's news is systemically loudest.",
),
"talk-daily-trade-signals-using-sentiment-analysis": dict(
    overview="Daily trade signals from sentiment with stochastic dominance for downside risk "
             "control: combining tone signals with distribution-aware position rules.",
    maths=[
        ("Second-order stochastic dominance", r"$$\int_{-\infty}^{x} F_A(u)\, du \le \int_{-\infty}^{x} F_B(u)\, du \;\; \forall x \;\Rightarrow\; A \succeq_{SSD} B$$"),
    ],
    plain="Sentiment picks the trade; stochastic dominance vets the distribution — only positions "
          "whose whole return profile beats the alternative survive. Signal enthusiasm, "
          "distributional discipline.",
),
"talk-news-sentiment-and-multi-asset-investing": dict(
    overview="News sentiment applied across asset classes: equity, rates, FX and commodity "
             "sentiment signals in one multi-asset framework.",
    maths=[
        ("Cross-asset sentiment matrix", r"$$S \in \mathbb{R}^{\text{assets} \times \text{topics}} \quad\text{— the same news read per asset class}$$"),
    ],
    plain="The same headline means different trades in different markets: a hawkish surprise is "
          "short duration, long dollar, mixed for equities. Multi-asset sentiment is about the "
          "mapping, not the tone score.",
),
"talk-incorporating-news-analytics-into": dict(
    overview="Incorporating news analytics into quantitative investment and trading strategies: "
             "integration patterns from signal construction to portfolio overlay.",
    maths=[
        ("Overlay integration", r"$$w = w_{\text{base}} \cdot \left( 1 + \kappa\, \text{Sent} \right) \quad\text{— tilt, don't replace}$$"),
    ],
    plain="News signals rarely stand alone; they earn their place tilting existing strategies — "
          "scaling momentum by news confirmation, gating entries on event risk. Integration "
          "design decides whether the data pays.",
),
"talk-the-power-of-news-and-blog-data-integrated": dict(
    overview="News and blog data integrated into automated strategies: source breadth versus "
             "reliability, and the automation pipeline from feed to fills.",
    maths=[],
    plain="Blogs and niche press front-run the wires on specialist stories — at the cost of "
          "credibility filtering. The pipeline that weighs source trust against speed is where "
          "this signal lives or dies.",
),
"talk-exploiting-alternative-data-in-the": dict(
    overview="Peter Hafez's overview of RavenPack's big-data analytics: product evolution and his "
             "latest work on news impact asymmetries in the investment process.",
    maths=[
        ("Event-study alpha", r"$$CAR(\tau) = \sum_{t=0}^{\tau} \left( R_t - \mathbb{E}[R_t] \right) \;\text{post news event}$$"),
    ],
    plain="A vendor's-eye view of a decade of news analytics: which event types move prices, for "
          "how long, and the asymmetries (negative news again) that survive transaction costs.",
),
"talk-alternative-data-for-investors": dict(
    overview="Saeed Amen defines alternative data and its usage challenges: sourcing, evaluation, "
             "legal questions, and the build-vs-buy economics for investors.",
    maths=[
        ("Data ROI test", r"$$\text{value} = \Delta \text{IR} \times \text{capacity} - \text{cost}_{\text{data+engineering}} > 0$$"),
    ],
    plain="Most alternative datasets fail the arithmetic: evaluation time, engineering cost and "
          "short histories eat the alpha. The skill is rapid triage — killing datasets in days, "
          "not quarters.",
),
"talk-extracting-embedded-alpha-in-social-and-news": dict(
    overview="Statistical arbitrage techniques applied to social and news data: extracting the "
             "embedded alpha with cross-sectional and event-driven methods.",
    maths=[
        ("Sentiment stat-arb", r"$$\text{long top decile Sent}, \; \text{short bottom decile}, \; \text{neutralize factors}$$"),
    ],
    plain="Treat sentiment like any cross-sectional signal: rank, hedge the factor exposures, "
          "and harvest the residual. The stat-arb machinery is standard — the data's short "
          "half-life is what changes the execution.",
),
"talk-how-ultra-low-latency-social-media-trading": dict(
    overview="Ultra-low latency social media signals disrupting traditional strategies: the "
             "infrastructure and the events where social beats the newswire.",
    maths=[],
    plain="For certain events — disasters, executive statements, product failures — social media "
          "leads official news by minutes. Harvesting that lead is an infrastructure race with "
          "a bot-filtering problem attached.",
),
"talk-social-media-news-media-and-the-stock-market": dict(
    overview="Social media versus news media effects on stocks: which channel moves prices, "
             "when, and how the two interact.",
    maths=[
        ("Channel attribution", r"$$R_t = \beta_1\, \text{Social}_t + \beta_2\, \text{News}_t + \beta_3\, (\text{Social} \times \text{News})_t + \varepsilon$$"),
    ],
    plain="Social buzz without news coverage fades; news without social amplification "
          "under-reacts. The interaction term is the story: attention cascades need both "
          "channels, and returns follow the cascade.",
),
"talk-social-listening-and-financial-crowd": dict(
    overview="Social listening and financial crowd intelligence: mining collective investor "
             "opinion from social platforms as a market signal (both catalog sessions merged).",
    maths=[
        ("Crowd signal quality", r"$$\text{value} \propto \text{diversity} \times \text{independence} \quad\text{— both decay in cascades}$$"),
    ],
    plain="Crowds are wise until they synchronize: social listening extracts genuine dispersed "
          "information while herding detection flags when the crowd has become one loud, wrong "
          "voice — a distinction worth basis points.",
),
"talk-revolutionizing-financial-information": dict(
    overview="Crowdsourcing plus AI revolutionizing financial information: estimates and research "
             "from distributed contributors, machine-validated.",
    maths=[
        ("Crowd estimate aggregation", r"$$\hat{y} = \sum_i w_i\, y_i, \qquad w_i \propto \text{contributor track record}$$"),
    ],
    plain="Crowdsourced earnings estimates beat sell-side consensus by weighting contributors on "
          "accuracy history — the wisdom of tracked crowds. AI does the tracking, weighting and "
          "anomaly policing.",
),
"talk-using-unstructured-information-for-improving": dict(
    overview="Sameena Shah on unstructured information improving oil futures predictability: "
             "news, reports and event data as inputs to energy price models.",
    maths=[
        ("Augmented forecast", r"$$\Delta P_{\text{oil}} = f\!\left( \text{inventories}, \text{macro}, \text{event/news features} \right)$$"),
    ],
    plain="Oil trades on geopolitics that structured data captures late: pipeline incidents, "
          "OPEC rhetoric, sanctions chatter. Parsing the unstructured stream adds the "
          "hours-ahead information the inventory reports lack.",
),
"talk-japanese-news-analyser-for-investors": dict(
    overview="A Japanese news analyser for investors: NLP for Japanese financial text and the "
             "market inefficiencies language barriers preserve.",
    maths=[],
    plain="Language walls protect alpha: Tokyo-listed news in Japanese digests slowly into "
          "global prices. A native-language analyser harvests the lag — an edge that exists "
          "precisely because most quants can't read it.",
),
"talk-going-native-with-japanese-news-analysis": dict(
    overview="Going native with Japanese news analysis: why translation pipelines lose the "
             "signal and native-language NLP retains it.",
    maths=[],
    plain="Translate-then-analyse mangles honorifics, hedged statements and cultural context "
          "that carry the actual sentiment in Japanese business language. Native models keep "
          "the nuance — and the nuance is the signal.",
),
"talk-knowledge-graphs-and-nlp-for-asset": dict(
    overview="Knowledge graphs plus NLP for asset management: entities, relationships and events "
             "in one queryable structure powering research and risk.",
    maths=[
        ("Graph-augmented signal", r"$$\text{exposure}(i) = \sum_{\text{paths } i \to \text{event}} \text{decay}(\text{path}) \quad\text{— risk via relationships}$$"),
    ],
    plain="A knowledge graph answers questions text search can't: 'which holdings depend on "
          "suppliers exposed to this earthquake?' Relationships, not documents, are the asset "
          "manager's real data structure.",
),
"talk-how-ai-ml-and-text-analysis-of-alternative": dict(
    overview="AI, ML and text analysis of alternative data across financial and retail markets: "
             "cross-industry use cases and impact.",
    maths=[],
    plain="The same text stack serves hedge funds and retailers: entity extraction, sentiment, "
          "demand signals. Seeing the retail applications sharpens intuition for which "
          "financial ones are real.",
),
"talk-how-to-solve-the-esg-data-challenge-using": dict(
    overview="Peter Hafez on the ESG data challenge: NLP over textual content for scalable, "
             "behaviour-based ESG scoring and sentiment tracking for investor edge.",
    maths=[
        ("Behaviour-based ESG score", r"$$\text{ESG}_i = g\!\left( \text{news events}_i \right) \quad\text{vs self-reported disclosures}$$"),
    ],
    plain="Company-reported ESG is marketing; news-derived ESG is behaviour. NLP over incident "
          "coverage — spills, strikes, fines — scores what firms do rather than what they "
          "publish, and the divergence itself is a signal.",
),
}

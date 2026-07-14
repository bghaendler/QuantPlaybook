# Content for §7 Kelly & Ziemba talks — consumed by enrich_talks.py
# NOTE: talk-kelly-ziemba intentionally absent (pre-existing hand-built page).
CONTENT = {

"talk-the-kelly-strategy-for-investing-risk-and": dict(
    overview="The Kelly strategy for investing examined through its risk and its reward: growth "
             "optimality, the violence of full-Kelly drawdowns, and the fractional compromises "
             "practitioners actually run.",
    maths=[
        ("Kelly fraction (binary bet)", r"$$f^* = \frac{p\,b - q}{b} \qquad (p+q=1,\ b = \text{odds})$$"),
        ("Growth-optimal property", r"$$f^* = \arg\max_f\; \mathbb{E}\left[ \ln\!\left(1 + f\,X\right) \right]$$"),
    ],
    plain="Kelly maximizes the growth rate of wealth — and en route to riches it will happily halve "
          "your bankroll repeatedly. The reward is asymptotic domination; the risk is a ride most "
          "humans and all clients abandon at the bottom.",
),
"talk-your-opinion-your-kelly-strategy": dict(
    overview="Kelly betting with subjective views: how the strategy transforms your probability "
             "opinions into position sizes, and what happens to growth and drawdown when the "
             "opinions are miscalibrated.",
    maths=[
        ("Continuous Kelly weight", r"$$f^* = \frac{\mu - r}{\sigma^2} \quad\text{— your } \mu \text{, your position}$$"),
        ("Overbetting penalty", r"$$g(cf^*) = \left( c - \tfrac{c^2}{2} \right) \frac{(\mu-r)^2}{\sigma^2} \;\Rightarrow\; c=2 \text{ gives zero growth}$$"),
    ],
    plain="Kelly is an opinion amplifier: a small edge estimate becomes a large position. Overestimate "
          "your edge by 2x and growth drops to zero; by more and Kelly ruins you faster than caution "
          "ever would. The formula is fine — the inputs are the danger.",
),
"talk-fat-tailed-kelly": dict(
    overview="Kelly sizing when returns have fat tails: how heavy-tailed distributions shrink the "
             "optimal fraction relative to Gaussian mean-variance intuition, and robust versions of "
             "the criterion.",
    maths=[
        ("General Kelly condition", r"$$\mathbb{E}\!\left[ \frac{X}{1 + f^* X} \right] = 0 \quad\text{— tails enter through the full distribution}$$"),
    ],
    plain="Under Gaussian assumptions Kelly looks brave; under real fat-tailed returns the same "
          "formula, honestly computed, says bet much less — the rare catastrophic outcome dominates "
          "the log expectation. Fat tails don't break Kelly; they discipline it.",
),
"talk-a-response-to-professor-paul-a-samuelsons": dict(
    overview="Ziemba responds to Samuelson's famous objections to Kelly investing: what the criticism "
             "actually establishes, examples of successful Kelly application, and the honest list of "
             "advantages and disadvantages of log-optimal betting.",
    maths=[
        ("Samuelson's point", r"$$\max \mathbb{E}[\ln W] \;\ne\; \max \mathbb{E}[U(W)] \text{ for } U \ne \ln$$"),
        ("Ziemba's reply in one line", r"$$\text{long horizon} + \text{growth objective} \Rightarrow \ln \text{ is the right } U$$"),
    ],
    plain="Samuelson proved Kelly isn't optimal for every utility — true and beside the point, says "
          "Ziemba: for investors whose goal is long-run wealth growth with controlled ruin, log "
          "utility is not an assumption but a theorem. Buffett, Soros and Keynes bet that way.",
),
"talk-professional-syndicate-racetrack-betting": dict(
    overview="Inside professional racetrack syndicates: the Dr. Z place-and-show system, inefficiencies "
             "in parimutuel pools, and Kelly bet sizing as the approximation to an infinite sequence "
             "of favourable bets.",
    maths=[
        ("Expected value in the place pool", r"$$EV_i = \frac{\text{payout}_i \times p_i^{\text{true}}}{1} > 1 \quad\text{where win odds imply } p^{\text{true}}$$"),
    ],
    plain="The win pool prices horses well; the place and show pools lag it. Betting the discrepancy "
          "with Kelly sizing built real fortunes — the cleanest laboratory demonstration that the "
          "criterion works when edges are genuine and repeated.",
),
"talk-optimal-growth-investment-and-wealth": dict(
    overview="Optimal growth investment connected to wealth benchmarking: growth-optimal strategies "
             "relative to benchmarks and targets, and the trade-off frontier between growth and "
             "security.",
    maths=[
        ("Growth-security trade-off", r"$$\max_f\; g(f) \quad \text{s.t.} \quad \mathbb{P}\!\left( W_t < b\, W_0 \right) \le \alpha$$"),
    ],
    plain="Full Kelly answers 'how fast can I grow'; investors also ask 'how sure am I to stay above "
          "my benchmark'. Trading a little growth for a lot of security defines a frontier — "
          "fractional Kelly walks along it.",
),
"talk-average-and-great-investors-how-do-they-do": dict(
    overview="Ziemba's tour of investment camps: how various investors view markets, incentives and "
             "risk-taking in hedge funds, what separates great investors from average ones, and "
             "Fortune's Formula in practice.",
    maths=[
        ("The great-investor signature", r"$$\text{few large bets when } \frac{p b - q}{b} \gg 0, \quad \text{small or none otherwise}$$"),
    ],
    plain="Great investors bet like Kelly gamblers: rarely, big and only with the odds. Average "
          "investors bet constantly and size by convention. The performance gap is mostly the sizing "
          "discipline, not the forecasts.",
),
"talk-update-on-financial-markets-and-strategies": dict(
    overview="Ziemba's markets update: the Yale endowment model and non-exchange-traded equity, "
             "Yale vs Harvard vs the S&P 500 over the cycle, the flash crash, Kelly betting at PIMCO, "
             "and choosing hedge fund managers.",
    maths=[
        ("Endowment model tilt", r"$$w_{\text{illiquid}} \uparrow \;\Rightarrow\; \text{return premium} + \text{smoothed marks} - \text{liquidity risk}$$"),
    ],
    plain="A grab-bag masterclass: why endowments beat public portfolios (and when they don't), what "
          "the flash crash revealed about market structure, and Kelly thinking applied inside the "
          "world's biggest bond manager.",
),
"talk-political-investing": dict(
    overview="Where politics and economics mesh into favourable investment opportunities: Fed "
             "movements, election cycles, party effects on markets, and other politically-driven "
             "calendar anomalies Ziemba has traded.",
    maths=[
        ("Presidential cycle effect", r"$$\mathbb{E}[R \,|\, \text{year 3}] > \mathbb{E}[R \,|\, \text{years 1,2,4}] \quad\text{(historically)}$$"),
    ],
    plain="Governments juice economies on political schedules, and markets echo it: the third year "
          "of presidential terms, pre-election stimulus, party-dependent sector effects. Political "
          "calendars are anomaly calendars.",
),
"talk-the-euro-currency-black-swan-bad-scenario": dict(
    overview="How traders lose money in derivatives — the general anatomy of blowups — applied to a "
             "euro-currency black-swan scenario: what the bad path looks like and the strategies that "
             "avoid being on it.",
    maths=[
        ("The blowup template", r"$$\text{short tail options} + \text{leverage} + \text{one shock} = \text{ruin} \quad\text{despite } \mathbb{E}[\text{P\&L}] > 0$$"),
    ],
    plain="Almost every derivatives disaster is the same trade: positive expected value, negative "
          "skew, too much size. The euro scenario is a case study in recognizing that shape before "
          "the tail arrives.",
),
"talk-navigating-stock-market-crashes-in-the": dict(
    overview="Ziemba on crash prediction and crash navigation in the Brexit/Trump era: bubble "
             "identification measures, dealing with crash consequences, and how it all feeds his "
             "trading.",
    maths=[
        ("BSEYD signal", r"$$\text{BSEYD} = y_{10Y} - \frac{E}{P} \;>\; \text{threshold} \Rightarrow \text{crash danger zone}$$"),
    ],
    plain="When bond yields tower over the stock market's earnings yield, equities are living on "
          "borrowed time — the signal that called 1987 and Japan 1990 gets re-run on the "
          "Brexit-Trump years.",
),
"talk-prediction-of-stock-market-crashes-entry": dict(
    overview="What is a bubble, how to identify one, and whether the major decline can be predicted: "
             "crash measures, entry and exit from bubble markets, and hedge fund disasters and their "
             "prevention.",
    maths=[
        ("Crash danger condition", r"$$\text{signal}_t > \mu_{\text{signal}} + k\,\sigma_{\text{signal}} \;\Rightarrow\; \text{exit/hedge}$$"),
    ],
    plain="You cannot time the top, but you can measure when conditions historically preceded "
          "crashes and stand aside. Missing the last month of a bubble costs little; missing the "
          "crash saves everything.",
),
"talk-can-we-predict-stock-market-crashes-using": dict(
    overview="The bond-stock earnings yield difference (BSEYD) model tested as a crash predictor: "
             "studies across markets and decades, the crashes it called, and its false-alarm "
             "behaviour.",
    maths=[
        ("BSEYD definition", r"$$\text{BSEYD}_t = y_{10Y,t} - \frac{E_t}{P_t}$$"),
    ],
    plain="One subtraction — long bond yield minus earnings yield — has flagged an outsized share "
          "of major crashes worldwide before they happened. Not a timing machine, but as a "
          "seatbelt light it has few rivals for its simplicity.",
),
"talk-historical-perspectives-on-the-bond-stock": dict(
    overview="The BSEYD model in historical perspective across world markets: moving-average and "
             "signal-chart variants, fat-tailed versions, the relation to the Fed model, and "
             "whether BSEYD beats high-P/E rules at crash prediction.",
    maths=[
        ("Fed model cousin", r"$$\frac{E}{P} \;\text{vs}\; y_{10Y} \quad\text{— BSEYD is its difference form with thresholds}$$"),
    ],
    plain="Around the world and across a century, the pattern repeats: when bonds out-yield stocks' "
          "earnings by enough, subsequent equity returns are poor. The talk stress-tests the rule "
          "against its critics and its rivals.",
),
"talk-market-lessons-from-the-work-of-william-t": dict(
    overview="Rachel Ziemba draws lessons from her father's work and their collaboration: capital "
             "markets, crash models and risk management insights relevant to investing in today's "
             "volatile, policy-driven markets.",
    maths=[],
    plain="A retrospective through a macro strategist's eyes: which of Bill Ziemba's tools — Kelly "
          "sizing, bubble measures, anomaly calendars — transfer intact to a world of QE, "
          "geopolitics and instant liquidity vacuums.",
),
"talk-predicting-stock-market-drawdowns-using": dict(
    overview="A systemic risk indicator from polymodel estimation: measuring the strength of links "
             "between the stock market and its economic environment, where weakening linkage "
             "precedes drawdowns.",
    maths=[
        ("Polymodel battery", r"$$Y = \phi_j(X_j) + \varepsilon_j \;\; \forall j, \qquad \text{indicator} = f\!\left( \{R^2_j\}_j \right)$$"),
    ],
    plain="Instead of one multivariate model, fit hundreds of tiny one-factor models — a polymodel — "
          "and watch their collective explanatory power. When the market decouples from its "
          "environment, it is levitating; levitation ends badly.",
),
"talk-optimal-portfolios-under-the-threat-of-a": dict(
    overview="Wilmott on crash-resistant portfolio construction: Crash Metrics and worst-case "
             "optimization — building portfolios optimal under the threat of a crash of uncertain "
             "size and timing.",
    maths=[
        ("Worst-case crash objective", r"$$\max_w \; \min_{\text{crash} \in \mathcal{C}} \; U\!\left( W(w, \text{crash}) \right)$$"),
    ],
    plain="Instead of assigning probabilities to crashes (unknowable), assume the worst crash within "
          "a plausible family happens at the worst time — then optimize. The resulting portfolios "
          "give up little upside for crash immunity that probabilistic models can't promise.",
),
}

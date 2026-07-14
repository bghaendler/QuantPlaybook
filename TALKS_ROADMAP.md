# CQF Talks — Implementation Roadmap

Goal: implement the CQF Talks video library (~567 videos) as interactive QuantPlaybook sections,
following the established app pattern:

1. One template per talk: `app/templates/sections/view-talk-<slug>.html`
   (summary, key concepts, math derivations side-by-side with Plain English Notes,
   interactive Chart.js demos where the topic allows).
2. Wire into `app/index.html`: `{% include %}`, `_sectionMap` entry (`math: true`), sidebar nav link
   under a new **Talks** portal grouped by the categories below.
3. Series with parts (e.g. "Model Risk and Calibration Part 01–15") become one section per part,
   under a collapsible `<details>` group, mirroring the Masterclass pattern (`view-arm-p01` etc.).

Legend: `[ ]` not started · `[~]` scaffolded (outline only) · `[x]` fully implemented.
Duplicated catalog entries (same talk listed twice) are merged and noted.

---

## 0. Infrastructure (prerequisite)

- [x] "Talks" portal hub section (`view-talks-portal`) with category cards + search/filter
- [x] Sidebar: `TALKS` nav group with per-category `<details>` sub-groups
- [x] Scaffold generator script (`scratch/scaffold_talk.py`) + catalog builder (`scratch/build_talks_catalog.py`) + enrichment engine (`scratch/enrich_talks.py` with `talk_content_*.py` data files)
- [~] Knowledge-graph integration: "CQF Talks" category added to graph legend; talk nodes/links still to be curated

## 1. Legacy lecture series (structured multi-part courses)

### 1.1 Mathematical Methods & Introduction to Numerical Methods (12 parts)
- [~] Part 01 · [~] Part 02 · [~] Part 03 · [~] Part 04 · [~] Part 05 · [~] Part 06
- [~] Part 07 · [~] Part 08 · [~] Part 09 · [~] Part 10 · [~] Part 11 · [~] Part 12

### 1.2 Black Scholes, Mathematical Methods & Intro to Numerical Methods — Dr. Riaz Ahmad (4 parts)
- [~] Part 01 (deriving/solving BS via heat equation) · [~] Part 02 (similarity reduction, Greeks, FDM intro)
- [~] Part 03 (LU decomposition, relaxation) · [~] Part 04 (bisection, Newton-Raphson, early exercise)

### 1.3 Martingales (4 parts)
- [~] Part 01 · [~] Part 02 · [~] Part 03 · [~] Part 04

### 1.4 Probabilistic Methods for Interest Rates (4 parts)
- [~] Part 01 · [~] Part 02 · [~] Part 03 · [~] Part 04

### 1.5 Random Behaviour of Assets (2 parts)
- [~] Part 01 · [~] Part 02

### 1.6 Model Risk and Calibration (15 parts)
- [~] Part 01 · [~] Part 02 · [~] Part 03 · [~] Part 04 · [~] Part 05
- [~] Part 06 · [~] Part 07 · [~] Part 08 · [~] Part 09 · [~] Part 10
- [~] Part 11 · [~] Part 12 · [~] Part 13 · [~] Part 14 · [~] Part 15

### 1.7 Valuation framework for interest rate derivatives in today's Libor world (9 parts)
- [~] Part 01 · [~] Part 02 · [~] Part 03 · [~] Part 04 · [~] Part 05
- [~] Part 06 · [~] Part 07 · [~] Part 08 · [~] Part 09

### 1.8 Brace, Gatarek and Musiela (BGM/LMM) Model (4 parts)
- [~] Part 01 · [~] Part 02 · [~] Part 03 · [~] Part 04

### 1.9 Structural Models (credit) (4 parts)
- [~] Part 01 · [~] Part 02 · [~] Part 03 · [~] Part 04

### 1.10 Credit Modelling Lectures — Claudio Albanese, 2007 (4 lectures)
- [~] Lecture 1 · [~] Lecture 2 · [~] Lecture 3 · [~] Lecture 4

### 1.11 Fixed Income Modelling Lectures (stochastic monetary policy, callable CMS spread range accruals) (4 lectures)
- [~] Lecture 1 · [~] Lecture 2 · [~] Lecture 3 · [~] Lecture 4

### 1.12 Monte Carlo Simulation and Early Exercise of American Options (2 parts)
- [~] Part 01 · [~] Part 02

### 1.13 Northfield risk series — Dan diBartolomeo (10 parts)
- [~] 01 Investment Risk for Asset Management Pt 1 · [~] 02 Investment Risk for Asset Management Pt 2
- [~] 03 Factor Risk Models · [~] 04 Conditional Risk Estimation · [~] 05 Interest Rate Risk
- [~] 06 Credit Risk · [~] 07 Hedge Fund Risk · [~] 08 Portfolio Risk Inclusive of Illiquid Assets
- [~] 09 Incorporation of Higher Moments / Tail Risk · [~] 10 Decomposition and Reporting of Risk

### 1.14 Stand-alone legacy lectures
- [~] Stochastic Calculus for Quant Finance — Dr. Riaz Ahmad
- [~] Markov Chain Monte Carlo Methods: A Beginner's Guide
- [~] Copula and Implementing CDO Pricing
- [~] ICA and Hedge Fund Returns Part 01
- [~] CQF Alumni HB Finite Difference Model Part 04
- [~] Principles and Tools of Quantitative Finance
- [~] Quants Toolbox
- [~] Manging Smile Risk (fixed income derivatives extra lecture)
- [~] Real Options
- [~] High Frequency Trading
- [~] High Frequency Data Analysis
- [~] Recent Developments in Credit Risk
- [~] Recent Developments in Deep Learning in Finance

## 2. Volatility & smile modeling

- [~] Rough Volatility: An Overview
- [~] Rough Volatility with Python — Jim Gatheral
- [~] The SABR Short-Maturity Expansion is Asymptotic
- [~] Cross-Currency Options and the Correlated SABR Model
- [~] Computing Skew-Stickiness — Jim Gatheral
- [~] Some Things I Have Learned About Volatility Over the Years — Paul Wilmott
- [~] Some More Things I have Learned About Volatility Over the Years — Paul Wilmott
- [~] Volatility and Risk with Dr. Paul Wilmott
- [~] Time Changes, Fourier Transforms and the Joint Calibration to the S&P500/VIX Smiles
- [~] The Term Structure of Implied Correlations Between S&P and VIX Markets
- [~] SPX VIX and Scale Invariant LSV — Adil Reghai
- [~] Modeling Volatility Risk-Premia — Artur Sepp
- [~] Modeling the Dynamics of the Entire Implied Volatility Surface with Deep Learning
- [~] Reconciling P- and Q-Calibration: The Discrete-Time 4-Factor Path-Dependent Volatility Model
- [~] Mixed Local Volatility Models for FX Derivatives — Uwe Wystup
- [~] QI 2021 APAC: Practical Demonstration of SLV, MLV and Other Models in FX Derivatives Markets
- [~] A New Interest Rate Smile Model — Dong Qu
- [~] LIBOR Smile Model with Local Volatility — Dong Qu
- [~] The Different Truths of IR Volatility Modeling: About Normality and Black's Immortality
- [~] Tensoring Volatility Calibration: The Power of Chebyshev
- [~] A Singular Variance Gamma Expansion — Peter Jaeckel
- [~] Post-Modern Volatility: When Abstraction Becomes Reality (panel)
- [~] Panel Discussion: The Origins of Financial Market Volatility
- [~] Data Science Methods for Volatility Objects
- [~] Volatility Trading in the Oil Market
- [~] Jump Risk Premia in the Presence of Clustered Jumps (Hawkes processes)
- [~] Why do Stock Prices Jump so Often?
- [~] Fast Times, Slow Times and Timescale Separation in Financial Timeseries Data

## 3. Options pricing, exotics & Black-Scholes at 50

- [~] Why You Should Not Go Drinking with Pure Mathematicians (BS derivations) — Paul Wilmott
- [~] Some Derivations of the Black-Scholes Equation and What They Tell Us
- [~] Reflections on the Black Scholes Model and its Applications
- [~] From Theory to Practice: The Evolution of Quantitative Finance through Fischer Black's Contributions
- [~] Time and Black-Scholes-Merton
- [~] Thought and Black-Scholes-Merton: Concept and intuition in probability theory vs. the financial market
- [~] A Truthful Generalization of Black Scholes-Merton (regime switching)
- [~] Renewing Black-Scholes: Interpreting Renewal Waiting Times
- [~] Imaginary Oscillations: Quantum Uncertainty and the Black-Scholes Formula
- [~] Why the Black-Scholes Model is Good and the Gaussian Copula is Not — Dariusz Gątarek
- [~] The "Non-Greek" Non-Foundation of Derivative Pricing
- [~] Neither God nor Machine: Man's Model
- [~] American Option Pricing in a Tick, Calibration in a Click (Andersen-Lake-Offengenden)
- [~] Valuing Exotic Options and Estimating Model Risk — John Hull (volatility feature approach)
- [~] Pricing of Digital Option by Monte Carlo Method with Adaptive Scheme
- [~] The Unreasonable Effectiveness of Randomized Quasi-Monte Carlo
- [~] The Importance Of Being Scrambled: Supercharged Quasi Monte Carlo
- [~] Finance in Focus — Application of Quasi Monte Carlo Methods in Finance and Sensitivity Analysis
- [~] Singular Perturbation Problems Arising in Mathematical Finance: Fluid Dynamics Concepts in Option Pricing
- [~] Can you feel the heat? Inverse Problems in Finance
- [~] Option Writing Beyond Theta — Shubham Agarwal
- [~] Optimal Portfolio Construction and Risk Premia in Options Markets
- [~] The New World of Options Trading: Valuation, Risk and Robust Workflows — Misha Fomytskyi
- [~] Robust Options Valuation and Risk Management Workflows with Vola Dynamics Analytics
- [~] Tools for Options Trading in the New World: A Report from the Cutting Edge
- [~] The Hidden Cost in Costless Put-Spread Collars: Rebalance Timing Luck
- [~] The Short Lira Put Option Investment — Uwe Wystup
- [~] FX Options — Wrong from the Start
- [~] Anomalies and Opportunities in the FX Option Market — Jessica James
- [~] Recent Trends in Products and Models for FX Derivatives — Uwe Wystup
- [~] A Market Design to Trade Bundles of Securities and Minimal Exercise of American Options
- [~] Jensen (probably the best inequality in the world)
- [~] Continuity and Risk (randomness + path continuity)
- [~] Acceptability Applications (acceptability & choice theory)

## 4. Interest rates & fixed income

- [~] What Short Rate Model Should I Use?
- [~] LIBOR Don't Fallback, Step Forward — Marc Henrard
- [~] Swap Rate Fallback: Unreasonable Effectiveness of Approximations and Alternatives
- [~] Swap Rate a la Stock: Bermudan Swaptions Made Easy — Dariusz Gątarek
- [~] OIS and its Impact on Modelling, Calibration and Funding of OTC Derivatives
- [~] Bond futures: Delivery Option with Term Structure Modelling — Marc Henrard
- [~] Revisiting Elastic String Models of Forward Interest Rates
- [~] The Market Price of Risk: Fear and Greed in the Fixed Income Markets — Paul Wilmott (2007)
- [~] Beyond Convexity — Jessica James
- [~] Beyond Convexity II — Jessica James
- [~] The Impact of Carry and Roll-Down on Macro Returns
- [~] The Rise of Carry — Coldiron, Lee & Lee
- [~] A Systematic Fixed Income Process Delivering Scalable and Bespoke Portfolio Solutions
- [~] Market Impact and Optimal Execution in Fixed Income: A Machine Learning Approach
- [~] QI: Machine learning methods for market-making & execution in Fixed Income — Edith Mandel
- [~] Enhanced Prediction of Sovereign Bond Spreads Through Macroeconomic News Sentiment
- [~] Repo Rates and Short Selling Restrictions
- [~] Quantifying Fissures in the US High Yield Market
- [~] Long Term Market Model
- [~] Modelling Banking Book Portfolios
- [~] Balance Sheet Risk and Return Analysis
- [~] Case Study: Bank of America's Credit Card Receivables
- [~] Bank of America Credit Card Receivables: Accounting and Hedging Implications of Poor Prepayment Modeling — Juan Ramirez
- [~] Asset Liability Models that are Useful in Practice

## 5. Credit risk, XVA & structured products

- [~] The Pricing of CDO's using Levy Copulas
- [~] CDOs, Correlation Products and Dangers Therein
- [~] The Credit Crunch: Past, Present and Future
- [~] Contingent Capital and CoCo Bonds
- [~] CoCos: The New Kid around the Block
- [~] ITO33 on Convertible Bonds and Banking Cocos
- [~] Volatility Inputs for Convertible Bond Pricing with Jump to Default
- [~] Convertible Bond Coding Workshop — Paul Wilmott (explicit FD in Excel/VBA)
- [~] Joint Calibration: The Case of Bank Regulatory Capital Securities
- [~] MVA: Margin Valuation Adjustment — Andrew Green
- [~] Revisiting FVA: Shareholder and Bondholder Perspectives — Andrew Green
- [~] Capital Valuation Adjustments (KVA)
- [~] Derivatives Funding, Netting and Accounting — Mats Kjaer
- [~] Risk-Aware OTC Pricing (using XVA): Getting Ready for the New Normal
- [~] Deploying an AI-based XVA Platform into Production — Riskfuel & Scotiabank
- [~] Loan Pricing: Arbitrage Free Models with Credit and Neural Network
- [~] Fourier-Based Methods for the Management of Complex Insurance Products — Laura Ballotta
- [~] Multivariate Additive Subordination with Applications in Finance — Laura Ballotta
- [~] The P2P Pandemic Swap: Decentralized Pandemic-linked Securities
- [~] Risk Sharing Pension Plans — Mary Hardy
- [~] More Wealth in Retirement (asset location across account types)
- [~] Potential Impacts of the COVID-19 Pandemic on Private Wealth Advisory

## 6. Portfolio theory & asset allocation

- [~] The Development and Evolution of Mean-Variance Efficient Portfolios in the US and Japan — John Guerard (2 versions in catalog, merge)
- [~] Quantitative Finance: Corporate Finance and Investments, Then and Now — John Guerard
- [~] Some Financial Anomalies have Survived the Past 30 Years — Markowitz & Guerard (2 versions in catalog, merge)
- [~] When the Optimal Portfolio Selection May Not be Worth the Cost or Effort
- [~] Overcoming Markowitz's Instability with the help of the Hierarchical Risk Parity (HRP)
- [~] Hierarchical Minimum Variance Portfolios — Peter Cotton
- [~] A Novel Way to Diversify Portfolio Weights (Robust Maximum Diversification)
- [~] Tell me, what exactly is diversification and how do we evaluate it?
- [~] Managing Diversification
- [~] Adaptive Diversification — Philip Maymin
- [~] Fat Tailed Diversification: Entropies, Tail Covariances et al — Jan Rosenzweig
- [~] Tails, Black Swans and Optimal Portfolios
- [~] The Markets are Not Normal — Graham Giller
- [~] Statistical Consequences of Fat Tails
- [~] Black-Litterman: Beyond Black-Litterman Views on Generic Markets (COP)
- [~] Building a Tool for Strategic Asset Allocation at a Swiss Insurance Company
- [~] Quantitative Asset Allocation at a Swiss Insurer: Insights from Three Years
- [~] Industry Talk: Optimization of Strategic and Tactical Asset Allocation for Multi-Asset Portfolios
- [~] ROSAA: Robust Optimization of Strategic and Active Asset Allocation
- [~] Stationary Portfolio Optimisation for Probability-Based Goals
- [~] Canonical Portfolios: Optimal Asset and Signal Combinations
- [~] Parametric Portfolio Policies
- [~] Portfolio Maximum Entropy and Sampling Error Control
- [~] Portfolio Management for People
- [~] Conditional Maximum Loss: A New Dynamic Risk Measure for Portfolio Optimization
- [~] Covariance Complexity and Rates of Return on Assets
- [~] Can you Count on your Correlation Matrix?
- [~] Excess Out-of-Sample Risk and Fleeting Modes (Random Matrix Theory)
- [~] Tests of Asset Pricing Models with A Large Number of Assets
- [~] Standardized Conditional Expectation (SCE): An application in CAPM
- [~] New Financial Decision Theory Objectives Applied to Stock Trading in a High Dimensional Markovian Model
- [~] Towards a Paradigm of Structural Factor Investing
- [~] Advances in Factor Investing
- [~] Factor Investing and the Road to Diversified Serfdom (panel)
- [~] Why Active Managers Should not Try to Maximize IR or Use Tracking Error as a Risk Measure
- [~] Worrying About Alpha — Adam Rej (overfitting & alpha decay; 2 versions in catalog, merge)
- [~] When Love is Blind: Making Sense of in-Sample Overfitting when Backtesting Strategies You Adore — Adam Rej
- [~] How to Identify and Mitigate Overfitting
- [~] False Confidence in Systematic Trading
- [~] Achieving Reliable Return Projections in Uncertain Times
- [~] What Signals Worked and What Did Not 1980-2009
- [~] Update on US Stock Market Calendar Anomalies in the COVID-19 Era
- [~] The Predictability of Stock Prices and Stock Returns
- [~] A Model for Passive That Breaks the Market
- [~] Algorithms for Tracking the S&P 500: Heuristics or Machine Learning?
- [~] Simply Quant Investing — Pim van Vliet
- [~] Crowd-sourced Alpha: The Search for the Holy Grail of Investing
- [~] Equity Portfolio Risk Management
- [~] Enhancing Performance of Mid to Low Frequency Trade Portfolios
- [~] Is It Possible To Make Investors Happy?
- [~] The Pain and Pleasure of Investing
- [~] The Knowing Doing Gap in Behavioral Finance
- [~] Classifying Alternative Investments Using Self-Organizing Maps
- [~] A Machine-Learning Tool for Visual Risk Analysis and Manager Selection
- [~] Polymodel Analysis of Hedge Funds, Selection and Portfolio Construction
- [~] A Picture Worth a Thousand Words: Fine Art and Investment

## 7. Kelly criterion, Ziemba lectures & crash prediction

- [~] The Kelly Capital Growth Investment Criterion — William Ziemba
- [~] The Kelly Strategy for Investing: Risk and Reward
- [~] Your opinion, Your Kelly strategy
- [~] Fat Tailed Kelly
- [~] A Response to Professor Paul A. Samuelson's Objections to Kelly Capital Growth Investing — Ziemba
- [~] Professional Syndicate Racetrack Betting using the Kelly Capital Growth Criterion — Ziemba
- [~] Optimal Growth Investment and Wealth Benchmarking
- [~] Average and Great Investors: How do they do it and how do we evaluate them? — Ziemba
- [~] Update on Financial Markets and Strategies — Ziemba (Yale model, flash crash, PIMCO)
- [~] Political Investing — Ziemba
- [~] The Euro Currency Black Swan Bad Scenario — Ziemba
- [~] Navigating Stock Market Crashes in the Brexit Trump Era — Ziemba
- [~] Prediction of Stock Market Crashes, Entry Exits from Bubbles, Hedge Fund Disasters — Ziemba
- [~] Can we predict stock market crashes using the bond-stock earnings yield difference model? — Ziemba
- [~] Historical Perspectives on the Bond-Stock Yield Model for Crash Prediction Around the World
- [~] Market Lessons from the Work of William T Ziemba — Rachel Ziemba
- [~] Predicting Stock Market Drawdowns using Polymodels
- [~] Optimal Portfolios Under the Threat of a Crash — Paul Wilmott

## 8. Machine learning & AI in finance

- [~] Zero to AI Series — Jon McLoone (Introduction + Parts 01–07, 8 sections)
- [~] Wolfram Managing Risk in AI Series (Parts 01–06, 6 sections)
- [~] From Zero to AI in 45 Minutes
- [~] You Can AI Like an Expert
- [~] Reinforcement Learning (classical techniques overview)
- [~] QI: Applications of Reinforcement Learning in Hedging — John Hull
- [~] QI: Results on pricing American Options with Reinforcement Learning — Daniel Bloch
- [~] Reinforcement Learning Interpretability: Applications to Algorithmic Trading
- [~] Reinforcement Learning and Hidden Markov Model Based Smart Trading Strategies
- [~] Deep Reinforcement Learning for Asset Allocation in US Equities
- [~] Financial Reasoning Agents: In-Context Reinforcement Learning and Test-Time Compute
- [~] Deep Learning Techniques in Derivatives Pricing — Credit Suisse
- [~] Deep Learning for Derivatives Pricing from Theory to Practice (2 versions in catalog, merge)
- [~] The Application of Deep Learning to High Dimensional Models in Finance
- [~] On Accuracy Guarantees for Machine Learning in Derivatives Pricing — Riskfuel
- [~] Building Neural Networks that Calibrate to Data in Real-Time
- [~] Neural Parametric Models: Novel Modelling Methods in Finance
- [~] Alternatives to Deep Neural Networks for Function Approximations in Finance
- [~] Non-Adversarial Training of Neural SDEs with Signature Kernel Scores
- [~] Generative Models and Predictive Machines with Uncertainty Quantification (kernels/RKHS)
- [~] Financial Applications with Kernels
- [~] Mixture Models for GenAI
- [~] Panel: Data Driven Market Generators and their Model Governance
- [~] QI: Decoding the Auto Encoder — Jesper Andreasen
- [~] AI and Machine Learning in Quant Finance — Decoding the Autoencoder (yield curves)
- [~] Risk Factor Aggregation and Stress Testing (PCA & autoencoders) — Natalie Packham
- [~] Risk Factor Detection with Methods from Explainable ML
- [~] Developments and Applications in (explainable) ML in Portfolio Management (panel)
- [~] The Psychology of LLMs
- [~] QI: Customizing Large Language Models for Quant Finance Applications — Alexander Sokol
- [~] How to Choose a Threshold for an Evaluation Metric for Large Language Models
- [~] A Behavioral Economics Approach To AI Safety — Steve Phelps
- [~] Beyond Agent-Washing: From Idea to Infrastructure (agentic AI)
- [~] AI Powered Traders: Ready or Not?
- [~] AI Liar's Poker — Aaron Brown
- [~] AI/ML in Systematic Investing and Trading: Recent Advances and Challenges Ahead
- [~] The Application of AI to Quantitative Systematic Strategies, Opportunities and Risks
- [~] CQF Institute — Machine Learning in Systematic Futures Allocation
- [~] Machine Learning for Tactical Asset Allocation Decisions
- [~] Machine Learning for Financial Markets
- [~] Machine Learning for Factor-based Commodities Investing
- [~] Using Machine Learning Algorithms to Estimate the Functional Form of Optimal Trading Strategies
- [~] How Machine Learning Can Help Stock Pickers
- [~] How AI Is Used to Generate Alpha in the Stock Market — Renee Yao
- [~] How AI is Used to Generate Alpha in Investing — Renee Yao
- [~] Using AI to Integrate Behavioral Insights into Investment Strategies
- [~] The Use of Big Data and Artificial Intelligence as an Alpha Generator
- [~] Fundamentals for finding Alpha Signals with AI + Influencer Analysis + Big Data
- [~] Putting Big Data, Advanced Analytics and Break-Through Trading Strategies To Work
- [~] Quantamental Factor Investing using Alternative Data and Machine Learning
- [~] Drawdown Mitigation via Identification and Prediction Using Machine Learning
- [~] Predicting Financial Crises with Machine Learning: A Data-Driven Approach
- [~] Practical Aspects of Applying Deep Learning for Market Making
- [~] Hedging in the Age of Statistical Learning (Proxy GMM Hedge)
- [~] What we learned from Kaggle Two Sigma News Competition
- [~] QI: Zero-Knowledge Machine Learning — Aaron Brown
- [~] QI: Beating the Markets with HPC+AI — Prabhu Ramamoorthy
- [~] Genetic Algorithms and Evolutionary Computation
- [~] Panel: How Can We Be More Ambitious with AI in Finance?
- [~] Industry Talk: The Future of Quants — An AI Perspective
- [~] Industry Talk: Automating Procurement Negotiations with AI
- [~] Mumbai Society Meeting: Artificial Intelligence in Trading
- [~] Analytics and AI Impact: Implementation and the Future of Work
- [~] AI and Machine Learning for Risk Management
- [~] A Revolution in Risk Management (LLMs & embeddings) — Rick Bookstaber

## 9. NLP, sentiment & alternative data

- [~] Sentiment Classification & Opinion Mining Using News Wires & Micro Blogs (6 sessions: Pullman Pt1–2, Gonzalez, Kolychyna/Souza Pt1–2, Messina)
- [~] Text Analytics for Sentiment Extraction in Finance: Information Extraction and Text Analytics
- [~] Text Analytics for Sentiment Extraction in Finance: Techniques of Classification and Predictive Analytics
- [~] Text Analytics for Sentiment Extraction in Finance: Use of R and Applications Analytics
- [~] Text Mining and Deep Learning for Sentiment Analysis
- [~] Deep Learning for Sentiment Analysis
- [~] Sentiment Analysis in Microblogs
- [~] Keynote: Sentiment Analysis for Fun and Profit
- [~] Keynote: Modeling News Impact Asymmetries
- [~] Keynote: Text Mining and Networks for Systemic Risk Measurement
- [~] Econometrics with text data
- [~] Natural Language Processing in Trading — James Isilay
- [~] SENRISK — Sentiment of News and Market Analysis of Sovereign and Corporate Bonds
- [~] Correlation Influence Networks for Sentiment Analysis in European Sovereign Bonds
- [~] Daily Trade Signals Using Sentiment Analysis and Stochastic Dominance for Downside Risk Control
- [~] Beating Markowitz with Sentiment and Downside Risk Control
- [~] News Sentiment and Multi-asset Investing
- [~] Incorporating News Analytics into Quantitative Investment and Trading Strategies
- [~] The Power of News & Blog Data Integrated into Automated Strategies
- [~] Exploiting Alternative Data in the Investment Process — Peter Hafez
- [~] Alternative Data for Investors — Saeed Amen
- [~] Extracting Embedded Alpha in Social & News Data Using Statistical Arbitrage Techniques
- [~] How Ultra-Low Latency Social Media Trading Signals are Disrupting Traditional Trading Strategies
- [~] Social Media, News Media and the Stock Market
- [~] Social Listening and Financial Crowd Intelligence (2 versions in catalog, merge)
- [~] Revolutionizing Financial Information through Crowdsourcing and Artificial Intelligence
- [~] Using Unstructured Information for Improving Predictability of Oil Futures — Sameena Shah
- [~] Japanese News Analyser for Investors
- [~] Going Native with Japanese News Analysis
- [~] Knowledge Graphs and NLP for Asset Management
- [~] How AI, ML & Text Analysis of Alternative Data is Impacting Financial and Retail Markets
- [~] How to Solve the ESG Data Challenge Using NLP to Access Textual Content
- [~] Natural Language Processing for Sustainable Development Goals

## 10. Quantum computing & quantum finance

- [~] What is Quantum Computing — Alonso Peña
- [~] Financial Applications of Quantum Computing (2 versions in catalog, merge)
- [~] Harnessing the Power of Quantum Computing in the Financial Industry
- [~] Advances in Quantum Computing
- [~] Advances in Quantum Machine Learning
- [~] Advances in Quantum Optimization Solvers for Near-term Hardware and Beyond
- [~] Quantum Machine Learning — Alexei Kondratyev
- [~] Quantum Complementarity and Potential for Advantage in Machine Learning
- [~] Complementarity of Quantum and Classical ML: Financial Fraud Detection (QSVM)
- [~] How can Current Quantum Computing Help with ML Tasks?
- [~] Predicting Recessions using Quantum Machine Learning Techniques
- [~] Probability Distribution Classification Problem (quantum vs classical)
- [~] Quantum Monte Carlo — Rafał Pracht
- [~] Quantum-Inspired Tensor Networks in Quantitative Finance
- [~] Quantum Technologies: A Global Understanding of the Opportunities Landscape
- [~] QI: Quantum solutions for finance — Araceli Venegas-Gomez
- [~] The Algorithms Bottleneck — Horizon Quantum Computing
- [~] Confessions of a Quantum Tourist in Finance
- [~] How Quantum Should Change the Way We Think About Finance
- [~] Quantum Judder for Financial Engineers
- [~] Quantum Economics and Finance: The Quantum Option — David Orrell
- [~] Quantum Economics and Finance: The Quantum Coin Trick — David Orrell
- [~] Let's Do Quantum Economics!
- [~] A Quantum Finance Approach to Option Pricing (quantum walk)
- [~] Green Inflation, Money Printing, and Quantum Computers

## 11. Crypto, DeFi & digital assets

- [~] The Bitcoin Innovation — Antonio Roldao
- [~] Blockchain and Bitcoin: A Mathematical Introduction to Bitcoin — Julien Riposo
- [~] Bitcoin and Blockchain, Opening the Blackbox with Python — Yves Hilpisch
- [~] Blockchains, Decentralized Financial Market Infrastructure and Decentralized Finance
- [~] Decentralized Finance, Central Bank Digital Coins, Automated Market Makers and Forex of the Future
- [~] Industry Talk — Forecast Bitcoin Price Using a Quantitative Approach — Daniele Bernardi
- [~] Cryptocurrency Exchange Microstructure and Quant Trading — Aaron Brown
- [~] High Frequency Price Leadership of Bitcoin Futures and the Bitcoin VIX
- [~] Limit Order Book Flows and Price Formation in Crypto Markets
- [~] Portfolio Construction for Sector Indices of Crypto Assets
- [~] Is Crypto The Next Frontier Of Opportunities For Quants? (panel)
- [~] Rarity Metrics for Profile Pictures (NFTs)
- [~] The Rise and Rise of UPI

## 12. Commodities & energy

- [~] Commodities Modelling — William Smith
- [~] Principles of Commodity Option Pricing: A Mathematical Introduction
- [~] Using the Signature Method to Classify Commodities and Select Commodity Options Strategies
- [~] Path Signatures for Data Pooling and Commodities Strategies
- [~] Graph-Based Learning for Commodity Futures: Temporal Knowledge Graph Triples with GNNs
- [~] COVID 19 and Crude Oil Prices
- [~] Energy Options, Volatility, and Energy Transition (panel)
- [~] Supply Chain Climate Exposure

## 13. Market microstructure & algorithmic trading

- [~] The Science and Practice of Trend-following Systems — Artur Sepp
- [~] De-constructing a Trend Following Trading System
- [~] Option Orderbooks: from AI Agents to Self Similarity
- [~] Do Spikes Make it Harder to Find Profitable Patterns in Limit Order Books — Stephen Weston
- [~] Are Spikes and Shocks Making Value and Risk Less Predictable — Stephen Weston
- [~] Guidelines for Building a Realistic Algorithmic Trading Market Simulator (market impact)
- [~] A Market Impact Model that Works
- [~] Modelling Intraday Risk and Flow Co-movement to Improve Trading Performance
- [~] Doing More with Tick Data: A Machine Learning Approach to Intraday Signal Development
- [~] Price Destabilizing Speculation: The Role of Strategic Limit Orders
- [~] Market Maker Positioning and the Recent Market Meltdown — Hari Krishnan
- [~] Cost-Effective Composite Forex and US Equities Feeds
- [~] Risk Budgeting and Machine Learning for FX Factor Models (PARIS)
- [~] Agent Based Models in Finance: Foundations, Explanatory Power and Application
- [~] Agents Provocateurs: Quant Finance's Next Evolution Must Incorporate Agent Based Modeling (panel)
- [~] Anticipating the Anticipations of Others — Grant Fuller
- [~] Practical Implications of the Anticipations of Others — Grant Fuller
- [~] Vicarious Risk — Estimating the Risk Identified by Others — Grant Fuller
- [~] How Epidemiology and the Science of Networks Help Understand Investor Behaviour
- [~] A Newbs Beginnings in Algorithmic Investing

## 14. Risk management & regulation

- [~] Omnipresent Model Risk
- [~] A Framework Based Approach to Model Risk
- [~] Model Risk Quantification in Banking: Challenges and Practical Solutions — Tiziano Bellini
- [~] FinTech Model Risk and All that — Tanveer Bhatti
- [~] Tail Risk & Portfolio Management Strategies
- [~] Shielding Portfolios from Extremes: Tail Risk Strategies for a Turbulent Era
- [~] The Second Leg Down: Strategies for Surviving a Market Sell Off — Hari Krishnan
- [~] Market Tremors: Hidden Risks in Modern "Zombified" Markets — Hari Krishnan
- [~] Systemic Risk and Market Fear Measurement
- [~] Estimating and Forecasting Risk Measures in Dynamical Environments
- [~] Correlation Stress Testing of Stock and Credit Portfolios — Natalie Packham
- [~] Liquidity Risk — The Calm Before the Storm
- [~] Capital Modeling in Operational Risk
- [~] Navigating Sector Investing Risks — Samit Ahlawat
- [~] Quantifying Geopolitical Risk: Data > Punditry — Mark Rosenberg
- [~] U.S./Trump 2.0: Accelerating "EM-ification" Drives Systemic Risks to U.S. Treasuries
- [~] Financial Crises, Contagion, and Complexity: The Challenges of an Interconnected World
- [~] Financial Network Models with Python — Miguel Vaz
- [~] Causal Asset and Factor Network Inference under Treatment Effects
- [~] Breaking the Waves: Financial Storms, Securities Regulation and the Journey Ahead
- [~] The Monetary System: A New Approach to Analysis and Regulation
- [~] Cooperation and Competition: Modern Economic History and International Trade
- [~] The Great Reset
- [~] The Doomsday Debt Machine
- [~] The Risky Horror Show
- [~] Why Most Published Findings in Finance are False (replication crisis)

## 15. ESG & climate

- [~] Managing Climate Risk
- [~] Climate Risk and Opportunity
- [~] Climate Financial Risk: Portfolios And Stress Tests
- [~] AI and ESG Investing — Grant Fuller
- [~] ESG and Shareholder Value
- [~] ESG: Emergence of the Sustainability Linked Bond — Diana Ouamar
- [~] 'Your Attention Please!' — Weaponising the ESG Narrative
- [~] Symbols vs Solutions: Quant as a Driver for Value Creation

## 16. Numerical methods, HPC & quant development

- [~] Fast Greeks through Adjoint Algorithmic Differentiation
- [~] Adjoint Parameter Calibration in Computational Finance — Uwe Naumann
- [~] AAD Applications as a Game Changer for Finance
- [~] Parallel Computing and GPUs
- [~] Faster Intelligence (hardware & software optimization)
- [~] Quant Development
- [~] Agile Development
- [~] Introduction to TDD for Quantitative Developers
- [~] Taming the Lint Monster (ACCU)
- [~] ACCU Mocking in C++
- [~] ACCU: Enterprise Web Application Development in Java with AJAX and ORMs
- [~] ACCU — Anticipating Surprises
- [~] Building an Enterprise Computation Strategy
- [~] Running Quantitative Analytics with Google Dataflow
- [~] From Open Source to Industry Standard — Open Source Risk Engine
- [~] Applying the Open-Source Risk Engine for pricing and risk analysis — Roland Lichters
- [~] Technical News from the Python Financial Analytics Front
- [~] Optimizing Pandas for Performance — Jeff Reback
- [~] Using Financial Data from Quandl with Python
- [~] How to Build a Hedge Fund with Python — Adam Sherman
- [~] How to Build a CTA with PyThalesians — Saeed Amen
- [~] Julia: A New Approach for Quantitative Finance — Avik Sengupta
- [~] Julia in Finance
- [~] Software Issues in Wavelet Analysis of Financial Data
- [~] Principal Component Analysis for Financial Time Series
- [~] Latest Innovations in Financial Time Series & Mathematical Optimization
- [~] Fun with Name-Value Pairs — Derek Yates (2 versions in catalog, merge)
- [~] Data Science is More than Just Statistics
- [~] Data Science and Symbolic Data
- [~] Data Science and ML Applied to Business Analytics: Financial and Retail Markets Use Cases
- [~] Breaking the Boundaries of Traditional Data Science — Jon McLoone
- [~] Computation Meets Data Science
- [~] Smart Cities and Data Overload — Insight from the Internet of Things
- [~] Finance Focus: "Deep Space Analytics"
- [~] Applied Finance — The Third Culture

## 17. Careers & industry insight

- [~] Quantitative Finance: Skills of the Future (panel)
- [~] Navigating the Quant Future: Upcoming Trends and Essential Skills (panel)
- [~] Quantitative Finance Careers India (2 versions in catalog, merge)
- [~] How to Build a Standout Quant Resume: Best Practices
- [~] Crafting a High-Impact Quant Finance Resume — Brian Cullinan
- [~] Careers in Quant Finance and Resume Building — Sonia Arora
- [~] Careers Talk: Master the Quant Finance Interview — Katherina Duong-Bernet
- [~] Careers Talk: A Day in the Life of a Portfolio Manager
- [~] A Day in the Life of a Quantitative Portfolio Manager — Michael Althof
- [~] A Day of a Quant Trader — Vitor Angrisani
- [~] A Day in the Life of a Quant Auditor
- [~] Careers Talk with Chloe Vuong (quant developer)
- [~] Communication Best Practices in Quantitative Finance — Ed Ma
- [~] Communicating for Impact in Quant Finance
- [~] How the Fundamental Analysts work in Banks
- [~] The Power of Data and Quantitative Approaches in Discretionary Investing — Pamela Saliba
- [~] Hedge Fund 2.0: The Era of the Cyborg
- [~] Panel Discussion: Saints and Sinners
- [~] Panel Discussion: Will a New Paradigm in Financial Modelling Rise Out of East Asian Capital Markets

## 18. History, philosophy & Wilmott lectures

- [~] What I Don't Like About Quant Finance — Paul Wilmott
- [~] The Money Formula — Paul Wilmott
- [~] My Life as a Mathematician — Paul Wilmott
- [~] ODSC Keynote: A New Kind of Dinosaur — Paul Wilmott
- [~] Wilmott Magazine at 20 — Wilmott & Tudball
- [~] How I Successfully Forecast the Results of the General Election 2015 (Parts 01–02) — Paul Wilmott
- [~] 20 Years of CQF and the Evolution of Quantitative Finance (panel)
- [~] A Stylized History of Quantitative Finance — Emanuel Derman
- [~] How Jim Simons and a Group of Unlikely Mathematicians Solved the Market — Gregory Zuckerman
- [~] Don Quixote on Wall Street
- [~] The Blank Swan
- [~] The Unbearable Lightness of Benchmarks and Why It Matters for Modelling
- [~] A Rationally Ig Nobel View of Finance
- [~] God's Money: The Key to Unlimited Clean Energy — Espen Gaarder Haug
- [~] Worrying about Alpha (companion talk; see §6 for merged entry)

---

### Progress summary

All 540 catalogued talks are wired into the app (template + include + `_sectionMap` + sidebar nav)
and carry enriched notes: overview, core mathematics (MathJax), Plain English intuition and
portal/part navigation. Status `[~]` = notes page live; `[x]` = deepened with per-video detail
and interactive demos (the remaining work).

| Category | Sections | Notes pages live |
|---|---|---|
| 1. Legacy lecture series | 91 | 91 (series-level notes + prev/next nav) |
| 2. Volatility & smile | 28 | 28 |
| 3. Options & BSM | 34 | 34 |
| 4. Rates & fixed income | 24 | 24 |
| 5. Credit, XVA & structured | 22 | 22 |
| 6. Portfolio & allocation | 56 | 56 |
| 7. Kelly & Ziemba | 18 | 18 |
| 8. ML & AI | 65 | 65 |
| 9. NLP & sentiment | 33 | 33 |
| 10. Quantum | 25 | 25 |
| 11. Crypto & DeFi | 13 | 13 |
| 12. Commodities & energy | 8 | 8 |
| 13. Microstructure & algo | 20 | 20 |
| 14. Risk & regulation | 26 | 26 |
| 15. ESG & climate | 8 | 8 |
| 16. Numerical, HPC & dev | 35 | 35 |
| 17. Careers & industry | 19 | 19 |
| 18. History & philosophy | 15 | 15 |
| **Total** | **540** | **540** |

Regenerate any category's pages: `python3 scratch/enrich_talks.py <category-key>` after editing
its `scratch/talk_content_*.py` data file. Rebuild the catalog/portal after roadmap edits:
`python3 scratch/build_talks_catalog.py`.

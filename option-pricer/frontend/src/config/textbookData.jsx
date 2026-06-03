import React from 'react';
import { InlineMath } from 'react-katex';

export const TEXTBOOK_DATA = {
  // --- 1. General & Derivatives ---
  bsm: {
    source: "Haug, Chapter 1 (Section 1.1.1)",
    concept: [
      <span key="1">The <strong>Black-Scholes (1973)</strong> formula values European options on non-dividend paying stocks. It assumes geometric Brownian motion and risk-neutral valuation.</span>,
      <span key="2">It remains the most famous formula in finance, serving as the benchmark for all other pricing models.</span>
    ],
    formulas: [
      { label: "Call", math: "c = S N(d_1) - X e^{-r T} N(d_2)" },
      { label: "Put", math: "p = X e^{-r T} N(-d_2) - S N(-d_1)" }
    ],
    where: [
      "d_1 = \\frac{\\ln(S/X) + (r + \\sigma^2/2)T}{\\sigma\\sqrt{T}}",
      "d_2 = d_1 - \\sigma\\sqrt{T}"
    ],
    notation: [
      { symbol: "S", def: "Stock Price" },
      { symbol: "X", def: "Strike Price" },
      { symbol: "r", def: "Risk-free Rate" },
      { symbol: "\\sigma", def: "Volatility" }
    ],
    contextText: "Standard European option with no dividends.",
    contextMath: "b = r",
    examplePage: "42",
    example: {
      inputs: [
        { label: "Spot", sym: "S", val: "60" },
        { label: "Strike", sym: "X", val: "65" },
        { label: "Time", sym: "T", val: "0.25" },
        { label: "Rate", sym: "r", val: "8%" },
        { label: "Vol", sym: "\\sigma", val: "30%" }
      ],
      calcs: [
        { sym: "d_1", val: "-0.3253" },
        { sym: "N(d_1)", val: "0.3725" }
      ],
      result: "2.1334 (Call)"
    }
  },
  merton: {
    source: "Haug, Chapter 1 (Section 1.1.2)",
    concept: [
      <span key="1">Merton (1973) extended BSM to allow for a <strong>continuous dividend yield</strong> (<InlineMath math="q" />).</span>,
      <span key="2">Commonly used for stock indices and stocks paying continuous dividends.</span>
    ],
    formulas: [
      { label: "Call", math: "c = S e^{-q T} N(d_1) - X e^{-r T} N(d_2)" },
      { label: "Put", math: "p = X e^{-r T} N(-d_2) - S e^{-q T} N(-d_1)" }
    ],
    where: [
      "d_1 = \\frac{\\ln(S/X) + (r - q + \\sigma^2/2)T}{\\sigma\\sqrt{T}}"
    ],
    notation: [
      { symbol: "q", def: "Continuous Dividend Yield" }
    ],
    contextText: "Cost of carry reflects the opportunity cost of holding the stock vs the dividend income.",
    contextMath: "b = r - q",
    examplePage: "43",
    example: {
      inputs: [
        { label: "Spot", sym: "S", val: "100" },
        { label: "Strike", sym: "X", val: "95" },
        { label: "Time", sym: "T", val: "0.5" },
        { label: "Rate", sym: "r", val: "10%" },
        { label: "Div", sym: "q", val: "5%" },
        { label: "Vol", sym: "\\sigma", val: "20%" }
      ],
      calcs: [
        { sym: "d_1", val: "0.6102" }
      ],
      result: "2.4648 (Put)"
    }
  },
  black76: {
    source: "Haug, Chapter 1 (Section 1.1.3)",
    concept: [
      <span key="1">Fischer Black (1976) derived the formula for <strong>futures options</strong>.</span>,
      <span key="2">Since futures require no initial investment (ignoring margin), the cost of carry is zero.</span>
    ],
    formulas: [
      { label: "Call", math: "c = e^{-r T} [F N(d_1) - X N(d_2)]" }
    ],
    where: [
      "d_1 = \\frac{\\ln(F/X) + (\\sigma^2/2)T}{\\sigma\\sqrt{T}}"
    ],
    notation: [
      { symbol: "F", def: "Futures Price" }
    ],
    contextText: "Cost of carry is zero for futures.",
    contextMath: "b = 0",
    examplePage: "44",
    example: {
      inputs: [
        { label: "Futures", sym: "F", val: "19" },
        { label: "Strike", sym: "X", val: "19" },
        { label: "Time", sym: "T", val: "0.75" },
        { label: "Rate", sym: "r", val: "10%" },
        { label: "Vol", sym: "\\sigma", val: "28%" }
      ],
      calcs: [
        { sym: "d_1", val: "0.1212" }
      ],
      result: "1.7011 (Call)"
    }
  },
  asay: {
    source: "Haug, Chapter 1 (Section 1.1.4)",
    concept: [
      <span key="1">Asay (1982) modified Black-76 for <strong>margined futures options</strong>.</span>,
      <span key="2">If the option premium is margined daily, the discounting term drops out entirely.</span>
    ],
    formulas: [
      { label: "Call", math: "c = F N(d_1) - X N(d_2)" }
    ],
    where: [
      "d_1 = \\frac{\\ln(F/X) + (\\sigma^2/2)T}{\\sigma\\sqrt{T}}"
    ],
    notation: [
      { symbol: "F", def: "Futures Price" }
    ],
    contextText: "No discounting due to daily margin settlement.",
    contextMath: "b = 0, r = 0",
    examplePage: "45",
    example: {
      inputs: [
        { label: "Futures", sym: "F", val: "4200" },
        { label: "Strike", sym: "X", val: "3800" },
        { label: "Time", sym: "T", val: "0.75" },
        { label: "Vol", sym: "\\sigma", val: "15%" }
      ],
      calcs: [
        { sym: "d_1", val: "0.8354" }
      ],
      result: "65.6185 (Put)"
    }
  },
  garman: {
    source: "Haug, Chapter 1 (Section 1.1.5)",
    concept: [
      <span key="1">The Garman-Kohlhagen model values <strong>currency options</strong> (FX).</span>,
      <span key="2">The foreign interest rate acts like a continuous dividend yield.</span>
    ],
    formulas: [
      { label: "Call", math: "c = S e^{-r_f T} N(d_1) - X e^{-r_d T} N(d_2)" }
    ],
    where: [
      "d_1 = \\frac{\\ln(S/X) + (r_d - r_f + \\sigma^2/2)T}{\\sigma\\sqrt{T}}"
    ],
    notation: [
      { symbol: "r_d", def: "Domestic Rate" },
      { symbol: "r_f", def: "Foreign Rate" }
    ],
    contextText: "Cost of carry is the interest rate differential.",
    contextMath: "b = r_d - r_f",
    examplePage: "46",
    example: {
      inputs: [
        { label: "Spot", sym: "S", val: "1.56" },
        { label: "Strike", sym: "X", val: "1.60" },
        { label: "Dom", sym: "r_d", val: "6%" },
        { label: "For", sym: "r_f", val: "8%" },
        { label: "Vol", sym: "\\sigma", val: "12%" }
      ],
      calcs: [
        { sym: "d_1", val: "-0.3738" }
      ],
      result: "0.0291 (Call)"
    }
  },
  gen_bsm: {
    source: "Haug, Chapter 1 (Section 1.1.6)",
    concept: [
      <span key="1">The <strong>Generalized Black-Scholes-Merton</strong> formula unifies all standard models using a cost-of-carry parameter <InlineMath math="b" />.</span>
    ],
    formulas: [
      { label: "Call", math: "c = S e^{(b-r)T} N(d_1) - X e^{-r T} N(d_2)" }
    ],
    where: [
      "d_1 = \\frac{\\ln(S/X) + (b + \\sigma^2/2)T}{\\sigma\\sqrt{T}}"
    ],
    notation: [
      { symbol: "b", def: "Cost of Carry" }
    ],
    contextText: "b=r (Stock), b=r-q (Merton), b=0 (Futures), b=r-rf (FX).",
    contextMath: "b = \\text{varies}",
    examplePage: "47",
    example: {
      inputs: [
        { label: "Spot", sym: "S", val: "75" },
        { label: "Strike", sym: "X", val: "70" },
        { label: "Rate", sym: "r", val: "10%" },
        { label: "Carry", sym: "b", val: "5%" },
        { label: "Vol", sym: "\\sigma", val: "35%" }
      ],
      calcs: [
        { sym: "d_1", val: "0.4868" }
      ],
      result: "4.0870 (Put)"
    }
  },
  brenner: {
    source: "Haug, Chapter 2 (Section 2.10.1)",
    concept: [
      <span key="1">Brenner and Subrahmanyam (1988) provided a simple "back-of-the-envelope" formula for <strong>At-the-Money Forward (ATMF)</strong> options.</span>
    ],
    formulas: [
      { label: "Approx", math: "c \\approx 0.4 S e^{(b-r)T} \\sigma \\sqrt{T}" }
    ],
    notation: [
      { symbol: "0.4", def: "Approx for 1/√(2π)" }
    ],
    contextText: "Valid when X = F = S*e^(bT).",
    examplePage: "84",
    example: {
      inputs: [
        { label: "Spot", sym: "S", val: "70" },
        { label: "Strike", sym: "X", val: "70" },
        { label: "Vol", sym: "\\sigma", val: "28%" }
      ],
      calcs: [],
      result: "3.87 (Approx)"
    }
  },
  black76f: {
    source: "Haug, Chapter 10 (Section 10.2.1)",
    concept: [
      <span key="1"><strong>Black-76F</strong> calculates options on forward contracts where the forward contract expires <em>after</em> the option expires (Deferred Settlement).</span>
    ],
    formulas: [
      { label: "Call", math: "c = e^{-r T_f} [F N(d_1) - X N(d_2)]" }
    ],
    where: [
      "T = \\text{Option Expiry}",
      "T_f = \\text{Forward Settlement}"
    ],
    notation: [
      { symbol: "T_f", def: "Settlement Time" }
    ],
    contextText: "Discounting occurs from Tf, volatility scales with T.",
    examplePage: "401",
    example: {
      inputs: [
        { label: "Fwd", sym: "F", val: "19" },
        { label: "Time", sym: "T", val: "0.75" },
        { label: "Settle", sym: "T_f", val: "1.0" }
      ],
      calcs: [],
      result: "1.6591 (Call)"
    }
  },

  // --- 2. Pre-Black-Scholes ---
  bachelier: {
    source: "Haug, Chapter 2 (Section 2.3.1)",
    concept: [
      <span key="1">Louis Bachelier (1900) introduced the first option model using <strong>Normal Distribution</strong> and arithmetic returns.</span>,
      <span key="2">Allows negative prices; uses absolute volatility.</span>
    ],
    formulas: [
      { label: "Call", math: "c = e^{-rT} [(F - X) N(d) + \\sigma\\sqrt{T} n(d)]" }
    ],
    where: [
      "d = \\frac{F - X}{\\sigma\\sqrt{T}}"
    ],
    notation: [
      { symbol: "\\sigma", def: "Absolute Volatility" }
    ],
    contextText: "Foundation of finance. b = r-q used for Forward.",
    examplePage: "82",
    example: {
      inputs: [
        { label: "Spot", sym: "S", val: "100" },
        { label: "Vol", sym: "\\sigma", val: "20" }
      ],
      calcs: [
        { sym: "F", val: "105.13" }
      ],
      result: "10.33 (Call)"
    }
  },
  mod_bachelier: {
    source: "Market Practice",
    concept: [
      <span key="1">Modified Bachelier adds a <strong>shift parameter β</strong> to displace the normal distribution.</span>
    ],
    formulas: [
      { label: "Call", math: "c = e^{-rT} [(F - X) N(d_\\beta) + \\sigma\\sqrt{T} n(d_\\beta)]" }
    ],
    where: [
      "d_\\beta = \\frac{F-X}{\\sigma\\sqrt{T}} \\text{ (Shift cancels in dist)}"
    ],
    notation: [
      { symbol: "\\beta", def: "Shift Parameter" }
    ],
    contextText: "Allows calibration to volatility smile.",
    examplePage: "N/A",
    example: {
      inputs: [
        { label: "Spot", sym: "S", val: "100" },
        { label: "Shift", sym: "\\beta", val: "10" }
      ],
      calcs: [],
      result: "Same as Bachelier if ATM"
    }
  },
  sprenkle: {
    source: "Sprenkle (1964)",
    concept: [
      <span key="1">First to use <strong>Lognormal Distribution</strong>. Used expected return <InlineMath math="\mu" /> but failed to discount the strike price.</span>
    ],
    formulas: [
      { label: "Call", math: "c = S e^{\\mu T} N(d_1) - X N(d_2)" }
    ],
    where: [
      "\\text{No } e^{-rT} \\text{ on Strike term!}"
    ],
    notation: [
      { symbol: "\\mu", def: "Expected Return" }
    ],
    contextText: "Precursor to BSM.",
    examplePage: "Yale Economic Essays",
    example: {
      inputs: [
        { label: "Spot", sym: "S", val: "100" },
        { label: "Rate", sym: "\\mu", val: "10%" }
      ],
      calcs: [],
      result: "Higher than BSM"
    }
  },
  boness: {
    source: "Boness (1964)",
    concept: [
      <span key="1">Improved Sprenkle by <strong>discounting the strike</strong> price. Closest model to BSM before 1973.</span>
    ],
    formulas: [
      { label: "Call", math: "c = S e^{\\mu T} N(d_1) - X e^{-rT} N(d_2)" }
    ],
    notation: [
      { symbol: "\\mu", def: "Expected Return" }
    ],
    contextText: "Only missing risk-neutral argument (using r instead of μ for spot growth).",
    examplePage: "J. Political Economy",
    example: {
      inputs: [
        { label: "Spot", sym: "S", val: "100" }
      ],
      calcs: [],
      result: "Depends on μ vs r"
    }
  },
  samuelson: {
    source: "Samuelson (1965)",
    concept: [
      <span key="1">Independent discovery of lognormal pricing. Similar to Sprenkle (no strike discount).</span>
    ],
    formulas: [
      { label: "Call", math: "c = S e^{\\mu T} N(d_1) - X N(d_2)" }
    ],
    contextText: "Published alongside Sprenkle and Boness.",
    examplePage: "Industrial Management",
    example: {
      inputs: [],
      calcs: [],
      result: "Similar to Sprenkle"
    }
  },

  // --- 3. American Options ---
  baw: {
    source: "Barone-Adesi Whaley (1987)",
    concept: [
      <span key="1">Analytical approximation for American options using a <strong>quadratic estimation</strong> of the early exercise premium.</span>
    ],
    formulas: [
      { label: "Call", math: "C_{Amer} = C_{Eur} + A_2 (S/S^*)^{q_2}" }
    ],
    where: [
      "S^* = \\text{Critical Stock Price}"
    ],
    notation: [
      { symbol: "S^*", def: "Exercise Boundary" }
    ],
    contextText: "Much faster than binomial trees. Accurate for standard maturities.",
    examplePage: "100",
    example: {
      inputs: [
        { label: "Spot", sym: "S", val: "100" },
        { label: "Time", sym: "T", val: "0.25" }
      ],
      calcs: [],
      result: "Includes Premium"
    }
  },
  bjerksund93: {
    source: "Bjerksund & Stensland (1993)",
    concept: [
      <span key="1">Uses a <strong>flat boundary approximation</strong> to the American exercise boundary.</span>,
      <span key="2">More accurate than BAW, especially for long-dated options and high dividends.</span>
    ],
    formulas: [
      { label: "Value", math: "\\alpha(S) - \\alpha(X) + \\dots" }
    ],
    contextText: "Closed-form approximation avoiding numerical iteration.",
    examplePage: "101",
    example: {
      inputs: [
        { label: "Spot", sym: "S", val: "40" },
        { label: "Strike", sym: "X", val: "40" },
        { label: "Div", sym: "q", val: "0.04" }
      ],
      calcs: [],
      result: "Good accuracy"
    }
  },
  bjerksund02: {
    source: "Bjerksund & Stensland (2002)",
    concept: [
      <span key="1">Divides time into two steps with two flat boundaries. Uses <strong>Bivariate Normal</strong> distribution.</span>
    ],
    formulas: [
      { label: "Value", math: "C = \\Psi(S, T, \\dots) + \\dots" }
    ],
    contextText: "Generally the most accurate analytical approximation for American options.",
    examplePage: "105",
    example: {
      inputs: [],
      calcs: [],
      result: "Very High Accuracy"
    }
  },
  mckean: {
    source: "McKean (1965) / Merton (1973)",
    concept: [
      <span key="1">Pricing for <strong>Perpetual American Options</strong> (Infinite time).</span>,
      <span key="2">Value depends purely on the asset price relative to an optimal barrier.</span>
    ],
    formulas: [
      { label: "Call", math: "c = (S^* - X) (S/S^*)^{\\gamma}" }
    ],
    where: [
      "\\gamma = \\text{Elasticity Root}"
    ],
    notation: [
      { symbol: "S^*", def: "Optimal Barrier" }
    ],
    contextText: "Time derivative is zero.",
    examplePage: "110",
    example: {
      inputs: [
        { label: "Spot", sym: "S", val: "90" },
        { label: "Strike", sym: "X", val: "100" }
      ],
      calcs: [],
      result: "20.61"
    }
  },
  roll_geske: {
    source: "Roll-Geske-Whaley",
    concept: [
      <span key="1">Models American Calls with <strong>discrete dividends</strong>.</span>,
      <span key="2">Checks if early exercise is optimal just before the ex-dividend date.</span>
    ],
    formulas: [
      { label: "Call", math: "C = \\text{BlackScholes} + \\text{EarlyExProb}" }
    ],
    notation: [
      { symbol: "D", def: "Discrete Dividend" }
    ],
    contextText: "Compound option approach.",
    examplePage: "376",
    example: {
      inputs: [
        { label: "Div", sym: "D", val: "4.0" },
        { label: "Time", sym: "t", val: "0.25" }
      ],
      calcs: [],
      result: "4.38"
    }
  },
  villiger: {
    source: "Villiger (2005)",
    concept: [
      <span key="1">Values American options with <strong>discrete dividend YIELD</strong>.</span>,
      <span key="2">Avoids negative price issues of fixed cash dividends.</span>
    ],
    formulas: [
      { label: "Call", math: "C = S N(a_1) - X e^{-rt} N(a_2) + \\text{Cont}" }
    ],
    contextText: "Uses Bivariate Normal.",
    examplePage: "392",
    example: {
      inputs: [
        { label: "Yield", sym: "\\delta", val: "5%" }
      ],
      calcs: [],
      result: "3.7178"
    }
  },

  // --- 4. Exotic: Path-Independent ---
  exec_stock: {
    source: "Haug, Chapter 4 (Section 4.2)",
    concept: [
      <span key="1">The <strong>Jennergren and Näslund (1993)</strong> model values executive stock options that are forfeited if the employee leaves the company.</span>,
      <span key="2">It introduces an <strong>exit rate (<InlineMath math="\lambda" />)</strong>. The option value is simply the Black-Scholes value multiplied by the probability that the executive remains until expiration.</span>
    ],
    formulas: [
      { label: "Executive Call", math: "c = e^{-\\lambda T} \\times C_{BSM}" }
    ],
    where: [
      "C_{BSM} = \\text{Generalized Black-Scholes Price}",
      "\\lambda = \\text{Exit rate (jump rate) per year}",
      "e^{-\\lambda T} = \\text{Probability of staying}"
    ],
    notation: [
      { symbol: "\\lambda", def: "Exit / Forfeiture Rate" },
      { symbol: "T", def: "Time to Vesting/Expiry" }
    ],
    contextText: "Used for Employee Stock Options (ESOs) where vesting is contingent on continued employment. The exit rate acts as a continuous discount factor.",
    examplePage: "114",
    example: {
      inputs: [
        { label: "Spot", sym: "S", val: "60" },
        { label: "Strike", sym: "X", val: "64" },
        { label: "Time", sym: "T", val: "2.0" },
        { label: "Rate", sym: "r", val: "7%" },
        { label: "Div", sym: "q", val: "3%" },
        { label: "Vol", sym: "\\sigma", val: "38%" },
        { label: "Exit", sym: "\\lambda", val: "15%" }
      ],
      calcs: [
        { sym: "b", val: "0.04" },
        { sym: "d_1", val: "0.2975" },
        { sym: "N(d_1)", val: "0.6169" },
        { sym: "e^{-\\lambda T}", val: "0.7408" }
      ],
      result: "9.1244"
    }
  },
  var_purchase: {
    source: "Handley (1992)",
    concept: [
      <span key="1">Handley generalized the pricing of options where the number of shares purchased can vary (Power Options).</span>,
      <span key="2">With standard parameters (n=1), it is identical to Black-Scholes-Merton.</span>
    ],
    formulas: [
      { label: "General Form", math: "V = S^n e^{((n-1)(r + \\frac{n\\sigma^2}{2}) - q)T} N(d_1) - K e^{-rT} N(d_2)" }
    ],
    where: [
      "n = \\text{Power parameter}",
      "d_1, d_2 \\text{ adjusted for } n"
    ],
    notation: [
      { symbol: "n", def: "Leverage/Power" }
    ],
    contextText: "Reduces to BSM when n=1.",
    examplePage: "N/A",
    example: {
      inputs: [
        { label: "Spot", sym: "S", val: "100" },
        { label: "Vol", sym: "\\sigma", val: "20%" }
      ],
      calcs: [],
      result: "10.4506 (n=1)"
    }
  },

  // --- 5. Exotic: Path-Dependent (Barriers) ---
  barrier_std: {
    source: "Haug, Chapter 4 (Section 4.17.1)",
    concept: [
      <span key="1">Standard Barrier Options are knocked in or out if the asset price hits a barrier <InlineMath math="H" />.</span>,
      <span key="2">Pricing uses the <strong>Reflection Principle</strong> to adjust probability density for barrier hits.</span>
    ],
    formulas: [
      { label: "Value", math: "V = A - B + C - D + E + F" }
    ],
    where: [
      "\\lambda = \\frac{r - q + \\sigma^2/2}{\\sigma^2}",
      "y = \\frac{\\ln(H^2/SX)}{\\sigma\\sqrt{T}} + \\lambda\\sigma\\sqrt{T}"
    ],
    notation: [
      { symbol: "H", def: "Barrier Level" },
      { symbol: "K", def: "Rebate (if any)" }
    ],
    contextText: "Terms A-F correspond to vanilla and reflection components.",
    examplePage: "154",
    example: {
      inputs: [
        { label: "Spot", sym: "S", val: "100" },
        { label: "Barrier", sym: "H", val: "95" },
        { label: "Type", sym: "", val: "Down-and-Out" }
      ],
      calcs: [],
      result: "9.02 (Call)"
    }
  },
  escrowed: {
    source: "Haug, Chapter 9 (Section 9.1.1)",
    concept: [
      <span key="1">The <strong>Escrowed Dividend Model</strong> prices European options on stocks with discrete cash dividends by adjusting the spot stock price used in the BSM formula.</span>,
      <span key="2">It subtracts the present value of all cash dividends expected to be paid before the option's expiration from the current spot price.</span>
    ],
    formulas: [
      { label: "Adjusted Spot", math: "S_{adj} = S - \\sum_{i=1}^{n} D_i e^{-r t_i}" },
      { label: "Call Price", math: "c \\approx S_{adj} N(d_1) - X e^{-r T} N(d_2)" }
    ],
    where: [
      "d_1 = \\frac{\\ln(S_{adj}/X) + (r + \\sigma^2/2)T}{\\sigma\\sqrt{T}}",
      "d_2 = d_1 - \\sigma\\sqrt{T}",
      "t_i = \\text{Time to each dividend payment } (t_i < T)"
    ],
    notation: [
      { symbol: "S_{adj}", def: "Adjusted Spot Price" },
      { symbol: "D_i", def: "Dividend Amount at time t_i" }
    ],
    contextText: "The standard BSM parameters are evaluated at the adjusted stock price S_adj with b = r.",
    examplePage: "348",
    example: {
      inputs: [
        { label: "Spot", sym: "S", val: "100" },
        { label: "Strike", sym: "X", val: "90" },
        { label: "Time", sym: "T", val: "0.75" },
        { label: "Rate", sym: "r", val: "10%" },
        { label: "Vol", sym: "\\sigma", val: "25%" },
        { label: "Div 1", sym: "D_1", val: "$2.00 at t_1=0.25" },
        { label: "Div 2", sym: "D_2", val: "$2.00 at t_2=0.50" }
      ],
      calcs: [
        { sym: "S_{adj}", val: "96.1469" },
        { sym: "d_1", val: "0.7598" },
        { sym: "N(d_1)", val: "0.7763" }
      ],
      result: "15.6465 (Call)"
    }
  },
  hhl: {
    source: "Haug, Chapter 9 (Section 9.1.1)",
    concept: [
      <span key="1">The <strong>Haug-Haug Volatility Adjustment</strong> improves option pricing accuracy by replacing the constant BSM volatility with an adjusted volatility <InlineMath math="\\sigma_{adj}" />.</span>,
      <span key="2">Designed to work alongside the escrowed dividend adjustment, it compensates for the underestimation of absolute price volatility.</span>
    ],
    formulas: [
      { label: "Variance Adj", math: "\\sigma_{adj}^2 \\approx \\sum_{j=1}^{n} \\left(\\frac{S\\sigma}{S-\\sum_{i=j}^{n} D_i e^{-rt_i}}\\right)^{2} (t_j - t_{j-1}) + \\sigma^2(T - t_n)" }
    ],
    where: [
      "S_{adj} = S - \\sum D_i e^{-r t_i}",
      "\\sigma_{adj} = \\text{Adjusted Volatility used in BSM formula}"
    ],
    notation: [
      { symbol: "\\sigma_{adj}", def: "Adjusted Volatility" },
      { symbol: "t_j", def: "Dividend payout times" }
    ],
    contextText: "Provides higher pricing accuracy compared to standard escrowed model by correcting volatility biases.",
    examplePage: "348",
    example: {
      inputs: [
        { label: "Spot", sym: "S", val: "100" },
        { label: "Strike", sym: "X", val: "90" },
        { label: "Rate", sym: "r", val: "10%" },
        { label: "Vol", sym: "\\sigma", val: "25%" },
        { label: "Div 1", sym: "D_1", val: "$2.00 at t_1=0.25" },
        { label: "Div 2", sym: "D_2", val: "$2.00 at t_2=0.50" }
      ],
      calcs: [
        { sym: "S_{adj}", val: "96.1469" },
        { sym: "\\sigma_{adj}", val: "26.02%" }
      ],
      result: "15.7001 (Call)"
    }
  },
  bos_vandermark: {
    source: "Haug, Chapter 9 (Section 9.1.5)",
    concept: [
      <span key="1">The <strong>Bos-Vandermark</strong> method is an alternative way to implement the escrowed dividend model by adjusting both the stock price and the strike price in the Black-Scholes-Merton (BSM) formula.</span>,
      <span key="2">It is a fast and efficient closed-form approximation designed strictly for European options.</span>
    ],
    formulas: [
      { label: "Option Price", math: "c \\approx c_{BSM}(S - X_n, X + X_f e^{r T}, T, r, b, \\sigma)" }
    ],
    where: [
      "X_n = \\sum_{i=1}^{n} \\frac{T-t_i}{T} D_i e^{-rt_i}",
      "X_f = \\sum_{i=1}^{n} \\frac{t_i}{T} D_i e^{-rt_i}"
    ],
    notation: [
      { symbol: "X_n", def: "Deduction from spot price" },
      { symbol: "X_f", def: "Addition to strike price (compounded)" }
    ],
    contextText: "Generally performs better than simpler volatility adjustments for discrete cash dividends.",
    examplePage: "351",
    example: {
      inputs: [
        { label: "Spot", sym: "S", val: "100" },
        { label: "Strike", sym: "X", val: "100" },
        { label: "Vol", sym: "\\sigma", val: "25%" },
        { label: "Rate", sym: "r", val: "6%" },
        { label: "Time", sym: "T", val: "1 Year" },
        { label: "Dividend", sym: "D", val: "$4.00 at t=0.50" }
      ],
      calcs: [
        { sym: "X_n", val: "1.9409" },
        { sym: "X_f", val: "1.9409" }
      ],
      result: "10.6596 (Call)"
    }
  }
};
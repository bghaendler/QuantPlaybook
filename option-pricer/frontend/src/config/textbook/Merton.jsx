import React from 'react';
import { InlineMath } from 'react-katex';

export const MERTON_DATA = {
  source: "Haug, Chapter 1 (Section 1.1.2)",
  concept: [
    <span key="1">Merton (1973) extended the Black-Scholes model to allow for a <strong>continuous dividend yield</strong> (<InlineMath math="q" />).</span>,
    <span key="2">This model is widely used for pricing options on Stock Indexes which pay dividends continuously.</span>
  ],
  formulas: [
    { label: "Call", math: "c = S e^{-q T} N(d_1) - X e^{-r T} N(d_2)" },
    { label: "Put", math: "p = X e^{-r T} N(-d_2) - S e^{-q T} N(-d_1)" }
  ],
  where: [
    "d_1 = \\frac{\\ln(S/X) + (r - q + \\sigma^2/2)T}{\\sigma\\sqrt{T}}",
    "d_2 = d_1 - \\sigma\\sqrt{T}"
  ],
  notation: [
    { symbol: "q", def: "Continuous dividend yield" }
  ],
  contextText: "In the Generalized BSM framework, the cost-of-carry (b) is the risk-free rate minus the dividend yield.",
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
      { sym: "d_1", val: "0.6102" },
      { sym: "d_2", val: "0.4688" }
    ],
    result: "2.4648 (Put)"
  }
};
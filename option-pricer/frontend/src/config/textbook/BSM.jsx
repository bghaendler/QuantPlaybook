import React from 'react';
import { InlineMath } from 'react-katex';

export const BSM_DATA = {
  source: "Haug, Chapter 1 (Section 1.1.1)",
  concept: [
    <span key="1">The <strong>Black-Scholes (1973)</strong> formula is used to value European options on a stock that does not pay dividends before the option's expiration.</span>,
    <span key="2">It assumes the underlying asset follows a geometric Brownian motion. The key insight was constructing a risk-free hedge portfolio to derive a partial differential equation (PDE).</span>
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
    { symbol: "r", def: "Risk-free interest rate" },
    { symbol: "\\sigma", def: "Volatility" }
  ],
  contextText: "In the Generalized BSM framework (Section 1.1.6), this is the specific case where the cost-of-carry (b) equals the risk-free rate (r).",
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
      { sym: "d_2", val: "-0.4753" },
      { sym: "N(d_1)", val: "0.3725" }
    ],
    result: "2.1334 (Call)"
  }
};
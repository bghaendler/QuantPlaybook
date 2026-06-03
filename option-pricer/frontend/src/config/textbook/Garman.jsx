import React from 'react';
import { InlineMath } from 'react-katex';

export const GARMAN_DATA = {
  source: "Haug, Chapter 1 (Section 1.1.5)",
  concept: [
    <span key="1">The Garman-Kohlhagen model is used to value <strong>European currency options</strong>.</span>,
    <span key="2">It is mathematically equivalent to the Merton model, where the foreign risk-free rate (<InlineMath math="r_f" />) plays the role of the continuous dividend yield.</span>
  ],
  formulas: [
    { label: "Call", math: "c = S e^{-r_f T} N(d_1) - X e^{-r T} N(d_2)" },
    { label: "Put", math: "p = X e^{-r T} N(-d_2) - S e^{-r_f T} N(-d_1)" }
  ],
  where: [
    "d_1 = \\frac{\\ln(S/X) + (r - r_f + \\sigma^2/2)T}{\\sigma\\sqrt{T}}",
    "d_2 = d_1 - \\sigma\\sqrt{T}"
  ],
  notation: [
    { symbol: "S", def: "Spot Exchange Rate" },
    { symbol: "X", def: "Strike Price" },
    { symbol: "r", def: "Domestic Rate" },
    { symbol: "r_f", def: "Foreign Rate" }
  ],
  contextText: "In the Generalized BSM framework, the cost-of-carry (b) is the interest rate differential.",
  contextMath: "b = r - r_f",
  examplePage: "46",
  example: {
    inputs: [
      { label: "Spot", sym: "S", val: "1.56" },
      { label: "Strike", sym: "X", val: "1.60" },
      { label: "Time", sym: "T", val: "0.5" },
      { label: "Dom Rate", sym: "r", val: "6%" },
      { label: "For Rate", sym: "r_f", val: "8%" },
      { label: "Vol", sym: "\\sigma", val: "12%" }
    ],
    calcs: [
      { sym: "d_1", val: "-0.3738" },
      { sym: "d_2", val: "-0.4587" }
    ],
    result: "0.0291 (Call)"
  },
  greeks: [
    {
      name: "Delta (Δ)",
      concept: "Sensitivity to spot exchange rate.",
      math: "\\Delta_{call} = e^{-r_f T} N(d_1)"
    },
    {
      name: "Rho (ρ)",
      concept: "Sensitivity to domestic interest rate.",
      math: "\\rho_{call} = T X e^{-r T} N(d_2)"
    },
    {
      name: "Phi (Φ)",
      concept: "Sensitivity to foreign interest rate (Rho-2).",
      math: "\\Phi_{call} = -T S e^{-r_f T} N(d_1)"
    }
  ]
};
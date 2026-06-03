import React from 'react';
import { InlineMath } from 'react-katex';

export const GEN_BSM_DATA = {
  source: "Haug, Chapter 1 (Section 1.1.6)",
  concept: [
    <span key="1">The <strong>Generalized Black-Scholes-Merton</strong> formula unifies all the standard models by introducing a <strong>cost-of-carry parameter (<InlineMath math="b" />)</strong>.</span>,
    <span key="2">By adjusting <InlineMath math="b" />, one can price options on stocks, stocks with dividends, futures, and currencies using a single equation.</span>
  ],
  formulas: [
    { label: "Call", math: "c = S e^{(b-r)T} N(d_1) - X e^{-r T} N(d_2)" },
    { label: "Put", math: "p = X e^{-r T} N(-d_2) - S e^{(b-r)T} N(-d_1)" }
  ],
  where: [
    "d_1 = \\frac{\\ln(S/X) + (b + \\sigma^2/2)T}{\\sigma\\sqrt{T}}",
    "d_2 = d_1 - \\sigma\\sqrt{T}"
  ],
  notation: [
    { symbol: "b", def: "Cost of Carry" }
  ],
  contextText: "Mapping 'b' to specific models:",
  contextMath: "\\begin{aligned} b &= r & \\text{(Black-Scholes)} \\\\ b &= r-q & \\text{(Merton)} \\\\ b &= 0 & \\text{(Black-76)} \\\\ b &= r-r_f & \\text{(Garman-Kohlhagen)} \\end{aligned}",
  examplePage: "47",
  example: {
    inputs: [
      { label: "Spot", sym: "S", val: "75" },
      { label: "Strike", sym: "X", val: "70" },
      { label: "Time", sym: "T", val: "0.5" },
      { label: "Rate", sym: "r", val: "10%" },
      { label: "Carry", sym: "b", val: "5%" },
      { label: "Vol", sym: "\\sigma", val: "35%" }
    ],
    calcs: [
      { sym: "d_1", val: "0.4868" }, // recalculated approx
      { sym: "N(d_1)", val: "0.6868" }
    ],
    result: "4.0870 (Put)"
  }
};
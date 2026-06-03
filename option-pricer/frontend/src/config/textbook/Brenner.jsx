import React from 'react';
import { InlineMath } from 'react-katex';

export const BRENNER_DATA = {
  source: "Haug, Chapter 2 (Section 2.10.1)",
  concept: [
    <span key="1">Brenner and Subrahmanyam (1988) provided a simple "back-of-the-envelope" formula to approximate the value of <strong>At-the-Money Forward (ATMF)</strong> options.</span>,
    <span key="2">An option is ATMF when the strike price equals the forward price: <InlineMath math="X = F = S e^{bT}" />. Under these conditions, <InlineMath math="d_1 \approx \frac{\sigma\sqrt{T}}{2}" /> and <InlineMath math="N(d_1) \approx 0.5" />.</span>
  ],
  formulas: [
    { label: "Call & Put", math: "c \\approx p \\approx 0.4 \\cdot S \\cdot e^{(b-r)T} \\cdot \\sigma \\sqrt{T}" }
  ],
  where: [
    "\\text{Condition: } X = S e^{bT} \\text{ (Strike = Forward Price)}",
    "0.4 \\approx \\frac{1}{\\sqrt{2\\pi}} \\text{ (Standard Normal Density at 0)}"
  ],
  notation: [
    { symbol: "S", def: "Spot Price" },
    { symbol: "\\sigma", def: "Volatility" },
    { symbol: "b", def: "Cost of Carry" }
  ],
  contextText: "This approximation is extremely fast and useful for traders to check valuations quickly without a computer.",
  contextMath: "N(d_1) - N(d_2) \\approx \\frac{1}{\\sqrt{2\\pi}} \\sigma\\sqrt{T}",
  examplePage: "84",
  example: {
    inputs: [
      { label: "Futures", sym: "F", val: "70" },
      { label: "Strike", sym: "X", val: "70" },
      { label: "Time", sym: "T", val: "0.25" },
      { label: "Rate", sym: "r", val: "5%" },
      { label: "Carry", sym: "b", val: "0%" },
      { label: "Vol", sym: "\\sigma", val: "28%" }
    ],
    calcs: [
      { sym: "S_{equiv}", val: "70" }, // Since b=0, F=S
      { sym: "\\sigma\\sqrt{T}", val: "0.14" }
    ],
    result: "3.8713 (Approx)"
  }
};
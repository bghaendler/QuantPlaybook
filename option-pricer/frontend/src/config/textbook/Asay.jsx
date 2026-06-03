import React from 'react';
import { InlineMath } from 'react-katex';

export const ASAY_DATA = {
  source: "Haug, Chapter 1 (Section 1.1.4)",
  concept: [
    <span key="1">Asay (1982) modified the Black-76 model for options on futures where the <strong>premium is fully margined</strong>.</span>,
    <span key="2">The option premium is paid into a margin account which accrues interest. This removes the discounting factor from the equation entirely.</span>
  ],
  formulas: [
    { label: "Call", math: "c = F N(d_1) - X N(d_2)" },
    { label: "Put", math: "p = X N(-d_2) - F N(-d_1)" }
  ],
  where: [
    "d_1 = \\frac{\\ln(F/X) + (\\sigma^2/2)T}{\\sigma\\sqrt{T}}",
    "d_2 = d_1 - \\sigma\\sqrt{T}"
  ],
  notation: [
    { symbol: "F", def: "Futures Price" }
  ],
  contextText: "In the Generalized BSM framework, this corresponds to cost-of-carry b = 0 and risk-free rate r = 0 for the valuation formula.",
  contextMath: "b = 0, \\quad r = 0",
  examplePage: "45",
  example: {
    inputs: [
      { label: "Futures", sym: "F", val: "4200" },
      { label: "Strike", sym: "X", val: "3800" },
      { label: "Time", sym: "T", val: "0.75" },
      { label: "Vol", sym: "\\sigma", val: "15%" }
    ],
    calcs: [
      { sym: "d_1", val: "0.8354" },
      { sym: "d_2", val: "0.7055" }
    ],
    result: "65.6185 (Put)"
  }
};
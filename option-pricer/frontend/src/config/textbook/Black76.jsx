// --- START OF FILE src/config/textbook/Black76.jsx ---

import React from 'react';
import { InlineMath } from 'react-katex';

export const BLACK76_DATA = {
  source: "Haug, Chapter 1 (Section 1.1.3)",
  concept: [
    <span key="1">Fischer Black (1976) derived the formula for valuing European options on <strong>futures contracts</strong>.</span>,
    <span key="2">Since entering a futures contract requires no initial investment (ignoring margin), the cost of carry is zero.</span>
  ],
  formulas: [
    { label: "Call", math: "c = e^{-r T} [F N(d_1) - X N(d_2)]" },
    { label: "Put", math: "p = e^{-r T} [X N(-d_2) - F N(-d_1)]" }
  ],
  where: [
    "d_1 = \\frac{\\ln(F/X) + (\\sigma^2/2)T}{\\sigma\\sqrt{T}}",
    "d_2 = d_1 - \\sigma\\sqrt{T}"
  ],
  notation: [
    { symbol: "F", def: "Futures Price" }
  ],
  contextText: "In the Generalized BSM framework, for futures, the cost-of-carry (b) is zero.",
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
      { sym: "d_1", val: "0.1212" },
      { sym: "d_2", val: "-0.1212" }
    ],
    result: "1.7011 (Call)"
  }
};
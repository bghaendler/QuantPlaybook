// --- START OF FILE src/config/textbook/Black76F.jsx ---

import React from 'react';
import { InlineMath } from 'react-katex';

export const BLACK76F_DATA = {
  source: "Haug, Chapter 10 (Section 10.2.1)",
  concept: [
    <span key="1"><strong>Black-76F</strong> calculates options on forward contracts where the forward contract expires <em>after</em> the option expires.</span>,
    <span key="2">If you exercise the option at time <InlineMath math="T" />, you receive a forward contract expiring at <InlineMath math="T_f" />. The intrinsic value is locked in at <InlineMath math="T" />, but cash is not received until <InlineMath math="T_f" />.</span>
  ],
  formulas: [
    { label: "Call", math: "c = e^{-r T_f} [F N(d_1) - X N(d_2)]" },
    { label: "Put", math: "p = e^{-r T_f} [X N(-d_2) - F N(-d_1)]" }
  ],
  where: [
    "d_1 = \\frac{\\ln(F/X) + (\\sigma^2/2)T}{\\sigma\\sqrt{T}}",
    "d_2 = d_1 - \\sigma\\sqrt{T}",
    "T = \\text{Time to Option Expiry}",
    "T_f = \\text{Time to Forward/Payment Expiry}"
  ],
  notation: [
    { symbol: "T_f", def: "Forward Settlement Time" },
    { symbol: "F", def: "Forward Price" }
  ],
  contextText: "Note that the discounting uses the Forward Expiry (T_f), while volatility scaling uses Option Expiry (T).",
  examplePage: "401",
  example: {
    inputs: [
      { label: "Forward", sym: "F", val: "19" },
      { label: "Strike", sym: "X", val: "19" },
      { label: "Opt Time", sym: "T", val: "0.75" },
      { label: "Fwd Time", sym: "T_f", val: "1.0" },
      { label: "Rate", sym: "r", val: "10%" },
      { label: "Vol", sym: "\\sigma", val: "28%" }
    ],
    calcs: [
      { sym: "d_1", val: "0.1212" }
    ],
    result: "1.6591 (Call)"
  }
};
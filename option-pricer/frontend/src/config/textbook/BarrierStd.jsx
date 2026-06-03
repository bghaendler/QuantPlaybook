import React from 'react';
import { InlineMath } from 'react-katex';

export const BARRIER_STD_DATA = {
  source: "Haug, Chapter 4 (Section 4.17.1)",
  concept: [
    <span key="1"><strong>Standard Barrier Options</strong> are path-dependent. They are knocked in or out if the asset price <InlineMath math="S" /> hits a barrier <InlineMath math="H" /> during the option's lifetime.</span>,
    <span key="2">Pricing relies on the <strong>Reflection Principle</strong>, adjusting the probability density for paths that touch the barrier.</span>
  ],
  formulas: [
    { label: "Generic Value", math: "V = A - B + C - D + E + F" },
    { label: "Rebate", math: "K \\text{ (paid at hit or expiry)}" }
  ],
  where: [
    "\\lambda = \\frac{r - q + \\sigma^2/2}{\\sigma^2}",
    "y = \\frac{\\ln(H^2/SX)}{\\sigma\\sqrt{T}} + \\lambda\\sigma\\sqrt{T}",
    "x_1 = \\frac{\\ln(S/X)}{\\sigma\\sqrt{T}} + \\lambda\\sigma\\sqrt{T}",
    "\\text{Terms A-F are combinations of BSM values & reflection terms}"
  ],
  notation: [
    { symbol: "H", def: "Barrier Level" },
    { symbol: "K", def: "Rebate (if any)" },
    { symbol: "\\eta, \\phi", def: "Binary switches for In/Out/Up/Down" }
  ],
  contextText: "Example: Down-and-out Call (Knock-out). If Asset > Barrier, pays vanilla call. If Asset touches Barrier, option dies (pays rebate).",
  contextMath: "C_{do} = c_{vanilla} - c_{di} \\quad \\text{(In-Out Parity)}",
  examplePage: "154",
  example: {
    inputs: [
      { label: "Spot", sym: "S", val: "100" },
      { label: "Strike", sym: "X", val: "90" },
      { label: "Barrier", sym: "H", val: "95" },
      { label: "Time", sym: "T", val: "0.5" },
      { label: "Vol", sym: "\\sigma", val: "25%" },
      { label: "Rebate", sym: "K", val: "3" } 
    ],
    calcs: [
      { sym: "c_{do}", val: "9.0246" },
      { sym: "p_{do}", val: "2.2798" }
    ],
    result: "Values for Down-and-Out (Table 4-13)"
  }
};
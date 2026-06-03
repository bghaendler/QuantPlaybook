// --- START OF FILE src/models/BrennerWalkthrough.jsx ---

import React, { useState } from 'react';
import { BlockMath, InlineMath } from 'react-katex';
import { ChevronDown, ChevronUp, AlertTriangle, Calculator, EqualNot } from 'lucide-react';
import 'katex/dist/katex.min.css';

import ModelExplanation from '../ModelExplanation';
import { TEXTBOOK_DATA } from '../config/textbookData'; 

// --- COLOR PALETTE FOR MATH ---
const COLORS = {
  S: "#3b82f6",     // Blue-500
  K: "#ec4899",     // Pink-500
  T: "#f59e0b",     // Amber-500
  r: "#10b981",     // Emerald-500
  b: "#d946ef",     // Fuchsia-500 (Cost of Carry)
  sigma: "#8b5cf6", // Violet-500
};

const BrennerWalkthrough = ({ inputs, results, showNumbers }) => {
  const [expanded, setExpanded] = useState({ 1: true, 2: true });

  const toggleStep = (step) => {
    setExpanded((prev) => ({ ...prev, [step]: !prev[step] }));
  };

  const fmt = (num, digits = 4) => {
    if (num === undefined || num === null || isNaN(num)) return "-";
    return parseFloat(num.toFixed(digits));
  };

  // Inputs
  const S = inputs.spot || 100;
  const K = inputs.strike || 100;
  const T = inputs.time || 1;
  const r = inputs.rate || 0.05;
  const b = inputs.dividend || 0; // In this model context, this is 'b'
  const v = inputs.volatility || 0.2;

  // Check ATMF condition
  const forwardPrice = S * Math.exp(b * T);
  const isATMF = Math.abs(forwardPrice - K) < (S * 0.01); // 1% tolerance

  // Calculate Approx locally to show the math terms
  const sqrtT = Math.sqrt(T);
  const discount = Math.exp((b-r)*T);
  
  // --- DYNAMIC LATEX GENERATOR ---
  const V = (symbol, value, colorKey) => {
    const color = COLORS[colorKey];
    if (showNumbers) {
       return `\\textcolor{${color}}{${fmt(value, 3)}}`;
    }
    return `\\textcolor{${color}}{${symbol}}`;
  };

  // Condition Formula: X = S * e^{bT}
  const condition_lhs = V('X', K, 'K');
  const condition_rhs = `${V('S', S, 'S')} e^{${V('b', b, 'b')}${V('T', T, 'T')}}`;

  // Approx Formula: c approx 0.4 * S * e^{(b-r)T} * sigma * sqrt(T)
  const approx_eq = `0.4 \\cdot ${V('S', S, 'S')} \\cdot e^{(${V('b', b, 'b')} - ${V('r', r, 'r')})${V('T', T, 'T')}} \\cdot ${V('\\sigma', v, 'sigma')} \\sqrt{${V('T', T, 'T')}}`;

  return (
    <div className="math-steps">
      
      {/* --- STEP 1: ATMF CHECK --- */}
      <div className={`step-card ${expanded[1] ? 'open' : ''}`}>
        <div className="step-trigger" onClick={() => toggleStep(1)}>
          <div className="step-info">
            <span className="step-circle">1</span>
            <span className="step-title-text">ATMF Condition</span>
          </div>
          <div className="step-summary-right">
             {isATMF ? (
                 <span className="text-green-600 font-bold text-xs">Valid (Approx)</span>
             ) : (
                 <span className="text-orange-500 font-bold text-xs">Deviation</span>
             )}
            {expanded[1] ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
          </div>
        </div>

        {expanded[1] && (
          <div className="step-content">
            <div className="mb-4 text-center">
                <span className="text-xs text-muted font-bold uppercase tracking-wider">Check: Strike = Forward Price?</span>
                <div className="latex-box mt-2 transition-all duration-300">
                    <BlockMath math={`${condition_lhs} \\stackrel{?}{\\approx} ${condition_rhs}`} />
                </div>
            </div>

            {!isATMF && (
                <div className="p-3 mb-3 bg-orange-50 border border-orange-200 rounded text-sm text-orange-800 flex gap-2">
                    <AlertTriangle size={18} className="shrink-0" />
                    <div>
                        The Strike (<InlineMath math={V('X', K, 'K')} />) deviates from the Forward Price. 
                        This approximation assumes <InlineMath math="X = F" />, so the error term increases as they diverge.
                    </div>
                </div>
            )}
            <div className="breakdown-grid">
                <div className="breakdown-item border-l-4" style={{borderLeftColor: COLORS.S}}>
                    <span className="label">Spot (S)</span>
                    <span className="value" style={{color: COLORS.S}}>{S}</span>
                </div>
                <div className="breakdown-item border-l-4" style={{borderLeftColor: COLORS.b}}>
                    <span className="label">Forward (F)</span>
                    <span className="value" style={{color: COLORS.b}}>{fmt(forwardPrice, 2)}</span>
                </div>
                <div className="breakdown-item border-l-4" style={{borderLeftColor: COLORS.K}}>
                    <span className="label">Strike (X)</span>
                    <span className="value" style={{color: COLORS.K}}>{K}</span>
                </div>
            </div>
          </div>
        )}
      </div>

      {/* --- STEP 2: THE APPROXIMATION --- */}
      <div className={`step-card ${expanded[2] ? 'open' : ''}`}>
        <div className="step-trigger" onClick={() => toggleStep(2)}>
          <div className="step-info">
            <span className="step-circle">2</span>
            <span className="step-title-text">Linear Approx</span>
          </div>
          <div className="step-summary-right">
            <span className="mono-val text-lg font-bold text-primary">${fmt(results.price, 4)}</span>
            {expanded[2] ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
          </div>
        </div>

        {expanded[2] && (
          <div className="step-content">
            <div className="latex-box mb-4 transition-all duration-300">
               <BlockMath math={`c \\approx ${approx_eq}`} />
            </div>

            <div className="valuation-receipt">
                <div className="receipt-row">
                    <span className="r-title">Constant <InlineMath math="(1/\sqrt{2\pi})" /></span>
                    <span className="receipt-value">0.3989</span>
                </div>
                <div className="receipt-row">
                    <span className="r-title" style={{color: COLORS.S}}>Asset Term</span>
                    <span className="receipt-value" style={{color: COLORS.S}}>{fmt(S * discount)}</span>
                </div>
                <div className="receipt-row">
                    <span className="r-title" style={{color: COLORS.sigma}}>Vol Term <InlineMath math="\sigma\sqrt{T}" /></span>
                    <span className="receipt-value" style={{color: COLORS.sigma}}>{fmt(v * sqrtT)}</span>
                </div>
                <div className="receipt-total-line"></div>
                <div className="receipt-row total">
                    <span className="r-title">Approx Value</span>
                    <span className="receipt-value">${fmt(results.price, 4)}</span>
                </div>
            </div>
            
            <div className="mt-4 text-xs text-center text-muted">
                <em>Note: The backend calculates the exact BSM price for the chart, but uses this formula for the display value here.</em><br/>
                {results.note}
            </div>
          </div>
        )}
      </div>

      {/* --- STEP 3: TEXTBOOK EXPLANATION --- */}
      <ModelExplanation data={TEXTBOOK_DATA.brenner} />

    </div>
  );
};

export default BrennerWalkthrough;
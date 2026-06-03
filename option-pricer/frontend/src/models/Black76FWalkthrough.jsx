// --- START OF FILE src/models/Black76FWalkthrough.jsx ---

import React, { useState } from 'react';
import { BlockMath, InlineMath } from 'react-katex';
import { ChevronDown, ChevronUp, Clock, AlertTriangle, Minus } from 'lucide-react';
import { AreaChart, Area, ResponsiveContainer, ReferenceLine } from 'recharts';
import 'katex/dist/katex.min.css';

// Import Explanation and Data
import ModelExplanation from '../ModelExplanation';
import { TEXTBOOK_DATA } from '../config/textbookData';

// --- COLOR PALETTE FOR MATH ---
const COLORS = {
  F: "#3b82f6",     // Blue-500 (Forward Price acts as Spot)
  K: "#ec4899",     // Pink-500
  T: "#f59e0b",     // Amber-500 (Option Expiry)
  Tf: "#06b6d4",    // Cyan-500 (Forward/Settlement Expiry)
  r: "#10b981",     // Emerald-500
  sigma: "#8b5cf6", // Violet-500
};

const Black76FWalkthrough = ({ inputs, results, showNumbers }) => {
  const [expanded, setExpanded] = useState({ 1: true, 2: false, 3: true });

  const toggleStep = (step) => {
    setExpanded((prev) => ({ ...prev, [step]: !prev[step] }));
  };

  const fmt = (num, digits = 4) => {
    if (num === undefined || num === null || isNaN(num)) return "-";
    return parseFloat(num.toFixed(digits));
  };

  const F = inputs.spot;
  const K = inputs.strike;
  const T = inputs.time; // Option Expiry
  // In Black76F model config, 'dividend' field is repurposed as Tf (Forward Expiry)
  const Tf = inputs.dividend || T; 
  const r = inputs.rate;
  const v = inputs.volatility;
  const isCall = inputs.type === 'call';

  // Results from backend
  const { d1, Nd1, Nd2, price } = results;

  const discountFactorFwd = Math.exp(-r * Tf);

  // --- DYNAMIC LATEX GENERATOR ---
  const V = (symbol, value, colorKey) => {
    const color = COLORS[colorKey];
    if (showNumbers) {
       return `\\textcolor{${color}}{${fmt(value, 3)}}`;
    }
    return `\\textcolor{${color}}{${symbol}}`;
  };

  // Dynamic Formulas
  // d1 uses Option Time (T)
  const d1_num = `\\ln(${V('F', F, 'F')} / ${V('X', K, 'K')}) + (${V('\\sigma', v, 'sigma')}^2/2)${V('T', T, 'T')}`;
  const d1_den = `${V('\\sigma', v, 'sigma')}\\sqrt{${V('T', T, 'T')}}`;
  
  // Price uses Settlement Time (Tf) for discounting
  // c = e^{-r Tf} [F N(d1) - X N(d2)]
  const call_eq = `e^{-${V('r', r, 'r')}${V('T_f', Tf, 'Tf')}} [${V('F', F, 'F')} N(d_1) - ${V('X', K, 'K')} N(d_2)]`;
  const put_eq = `e^{-${V('r', r, 'r')}${V('T_f', Tf, 'Tf')}} [${V('X', K, 'K')} N(-d_2) - ${V('F', F, 'F')} N(-d_1)]`;

  return (
    <div className="math-steps">
      
      {/* --- STEP 1: TIME LAG CHECK --- */}
      <div className={`step-card ${expanded[1] ? 'open' : ''}`}>
        <div className="step-trigger" onClick={() => toggleStep(1)}>
          <div className="step-info">
            <span className="step-circle">1</span>
            <span className="step-title-text">Delivery Time Lag</span>
          </div>
          <div className="step-summary-right">
             <span className="text-xs text-muted font-mono">T={T}, Tf={Tf}</span>
            {expanded[1] ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
          </div>
        </div>

        {expanded[1] && (
          <div className="step-content">
            {Tf < T ? (
                <div className="p-3 mb-3 bg-red-50 border border-red-200 rounded text-sm text-red-800 flex gap-2">
                    <AlertTriangle size={18} className="shrink-0" />
                    <div>Error: Forward expiry (Tf) cannot be before Option expiry (T).</div>
                </div>
            ) : (
                <div className="p-3 mb-3 bg-blue-50 border border-blue-100 rounded text-sm text-blue-800 flex items-start gap-2">
                    <Clock size={16} className="mt-0.5 shrink-0" />
                    <div>
                        <strong>Deferred Settlement:</strong> The option expires at <InlineMath math={`T=${T}`} />, locking in the intrinsic value. However, the cash is not received until the forward contract expires at <InlineMath math={`T_f=${Tf}`} />.
                    </div>
                </div>
            )}
            
            <div className="latex-box transition-all duration-300">
               <BlockMath math={`\\text{Discount Factor} = e^{-${V('r', r, 'r')} ${V('T_f', Tf, 'Tf')}}`} />
            </div>
            <div className="text-center text-sm text-muted">
                <InlineMath math={`e^{-${r} \\cdot ${Tf}} = ${fmt(discountFactorFwd, 4)}`} />
            </div>
          </div>
        )}
      </div>

      {/* --- STEP 2: VALUATION --- */}
      <div className={`step-card ${expanded[3] ? 'open' : ''}`}>
        <div className="step-trigger" onClick={() => toggleStep(3)}>
          <div className="step-info">
            <span className="step-circle">2</span>
            <span className="step-title-text">Valuation</span>
          </div>
          <div className="step-summary-right">
            <span className="text-primary font-bold text-lg">${fmt(price, 4)}</span>
            {expanded[3] ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
          </div>
        </div>

        {expanded[3] && (
          <div className="step-content">
            <div className="latex-box small-latex mb-3 transition-all duration-300">
              <BlockMath math={isCall ? `c = ${call_eq}` : `p = ${put_eq}`} />
            </div>

            <div className="valuation-receipt">
              <div className="receipt-row positive">
                <div className="receipt-label">
                  <span className="r-title" style={{color: COLORS.F}}>{isCall ? "Forward Value" : "Strike Inflow"}</span>
                </div>
                <div className="receipt-value" style={{color: COLORS.F}}>
                   {isCall ? fmt(F * Nd1, 4) : fmt(K * (1 - Nd2), 4)}
                </div>
              </div>

              <div className="receipt-divider"><Minus size={14} /></div>

              <div className="receipt-row negative">
                <div className="receipt-label">
                  <span className="r-title" style={{color: COLORS.K}}>{isCall ? "Strike Cost" : "Forward Outflow"}</span>
                </div>
                <div className="receipt-value" style={{color: COLORS.K}}>
                    {isCall ? fmt(K * Nd2, 4) : fmt(F * (1 - Nd1), 4)}
                </div>
              </div>
              
              <div className="receipt-row">
                 <div className="receipt-label">
                     <span className="r-title font-normal text-muted">Undiscounted Payoff</span>
                 </div>
                 <div className="receipt-value text-muted">
                     {fmt(isCall ? (F*Nd1 - K*Nd2) : (K*(1-Nd2) - F*(1-Nd1)), 4)}
                 </div>
              </div>

              <div className="receipt-total-line"></div>

              <div className="receipt-row total">
                <div className="receipt-label">
                    Fair Price <br/>
                    <span className="text-xs font-normal text-muted">
                        (Discounted by <InlineMath math={`e^{-r T_f}`} />)
                    </span>
                </div>
                <div className="receipt-value">${fmt(price, 4)}</div>
              </div>
            </div>
          </div>
        )}
      </div>

      <ModelExplanation data={TEXTBOOK_DATA.black76f} />

    </div>
  );
};

export default Black76FWalkthrough;
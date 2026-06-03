// --- START OF FILE src/models/BosVandermarkWalkthrough.jsx ---

import React, { useState } from 'react';
import { BlockMath, InlineMath } from 'react-katex';
import ModelExplanation from '../ModelExplanation';
import { ChevronDown, ChevronUp, Minus, Plus } from 'lucide-react';
import 'katex/dist/katex.min.css';
import { TEXTBOOK_DATA } from '../config/textbookData';

const COLORS = {
  S: "#3b82f6",     // Blue-500
  K: "#ec4899",     // Pink-500
  T: "#f59e0b",     // Amber-500
  r: "#10b981",     // Emerald-500
  sigma: "#8b5cf6", // Violet-500
  div: "#06b6d4",   // Cyan-500
};

const BosVandermarkWalkthrough = ({ inputs, results, showNumbers }) => {
  const [expanded, setExpanded] = useState({ 1: true, 2: true, 3: true });

  const toggleStep = (step) => setExpanded(prev => ({ ...prev, [step]: !prev[step] }));

  const S = inputs.spot || 100;
  const K = inputs.strike || 100;
  const T = inputs.time || 1.0;
  const r = inputs.rate || 0.06;
  const sigma = inputs.volatility || 0.25;
  
  const div1_amt = inputs.div1_amt !== undefined ? inputs.div1_amt : 4.0;
  const div1_time = inputs.div1_time !== undefined ? inputs.div1_time : 0.50;
  const div2_amt = inputs.div2_amt !== undefined ? inputs.div2_amt : 0.0;
  const div2_time = inputs.div2_time !== undefined ? inputs.div2_time : 0.0;

  const price = results?.price || 0;
  const d1 = results?.d1 || 0;
  const d2 = results?.d2 || 0;
  const Nd1 = results?.Nd1 || 0;
  const Nd2 = results?.Nd2 || 0;
  const isCall = inputs.type === 'call';

  const fmt = (num, digits = 4) => {
    if (num === undefined || num === null || isNaN(num)) return "-";
    return parseFloat(num.toFixed(digits));
  };

  // Dynamic parameters calculation
  const getBVParams = () => {
    let Xn = 0;
    let Xf = 0;
    const divs = [];
    if (div1_amt > 0 && div1_time < T) divs.push({ t: div1_time, amt: div1_amt });
    if (div2_amt > 0 && div2_time < T) divs.push({ t: div2_time, amt: div2_amt });
    
    for (let i = 0; i < divs.length; i++) {
      const t_i = divs[i].t;
      const D_i = divs[i].amt;
      Xn += ((T - t_i) / T) * D_i * Math.exp(-r * t_i);
      Xf += (t_i / T) * D_i * Math.exp(-r * t_i);
    }
    const S_adj = Math.max(0.01, S - Xn);
    const K_adj = Math.max(0.01, K + Xf * Math.exp(r * T));
    return { Xn, Xf, S_adj, K_adj };
  };

  const { Xn, Xf, S_adj, K_adj } = getBVParams();

  // Dynamic LaTeX formatting helper
  const V = (symbol, value, colorKey) => {
    const color = COLORS[colorKey];
    if (showNumbers) {
       return `\\textcolor{${color}}{${fmt(value, 3)}}`;
    }
    return `\\textcolor{${color}}{${symbol}}`;
  };

  return (
    <div className="math-steps">

      {/* --- STEP 1: ADJUSTMENT FACTORS --- */}
      <div className={`step-card ${expanded[1] ? 'open' : ''}`}>
        <div className="step-trigger" onClick={() => toggleStep(1)}>
          <div className="step-info">
            <span className="step-circle">1</span>
            <span className="step-title-text">Calculate Adjustment Factors</span>
          </div>
          <div className="step-summary-right">
            <span className="text-xs text-muted font-mono">Xn = {fmt(Xn, 3)} | Xf = {fmt(Xf, 3)}</span>
            {expanded[1] ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
          </div>
        </div>
        {expanded[1] && (
          <div className="step-content">
            <p className="step-desc text-xs text-muted mb-3">
              We calculate the discrete dividend adjustment factors <InlineMath math="X_n" /> and <InlineMath math="X_f" /> representing temporal allocations to spot and strike respectively.
            </p>
            <div className="latex-box transition-all duration-300 grid grid-rows-2 gap-2 text-sm p-3">
               <BlockMath math={`X_n = \\sum \\frac{${V('T', T, 'T')} - t_i}{${V('T', T, 'T')}} D_i e^{-${V('r', r, 'r')} t_i}`} />
               <BlockMath math={`X_f = \\sum \\frac{t_i}{${V('T', T, 'T')}} D_i e^{-${V('r', r, 'r')} t_i}`} />
            </div>
            <div className="grid grid-cols-2 gap-3 mt-2">
              <div className="bg-slate-50 p-2.5 rounded border border-slate-200 text-center text-sm">
                 <div><InlineMath math={`X_n = ${fmt(Xn, 4)}`} /></div>
              </div>
              <div className="bg-slate-50 p-2.5 rounded border border-slate-200 text-center text-sm">
                 <div><InlineMath math={`X_f = ${fmt(Xf, 4)}`} /></div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* --- STEP 2: SPOT & STRIKE ADJUSTMENTS --- */}
      <div className={`step-card ${expanded[2] ? 'open' : ''}`}>
        <div className="step-trigger" onClick={() => toggleStep(2)}>
          <div className="step-info">
            <span className="step-circle">2</span>
            <span className="step-title-text">Adjust Spot & Strike Inputs</span>
          </div>
          <div className="step-summary-right">
            <span className="text-xs text-muted font-mono">S_adj = {fmt(S_adj, 2)} | K_adj = {fmt(K_adj, 2)}</span>
            {expanded[2] ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
          </div>
        </div>
        {expanded[2] && (
          <div className="step-content">
            <p className="step-desc text-xs text-muted mb-3">
              We apply the adjusted spot price <InlineMath math="S_{adj} = S - X_n" /> and compound the strike adjustment factor to expiration: <InlineMath math="K_{adj} = K + X_f e^{r T}" />.
            </p>
            <div className="grid grid-cols-2 gap-3 mt-2">
              <div className="bg-slate-50 p-2.5 rounded border border-slate-200 text-center text-sm">
                 <div className="text-xs text-muted font-semibold">Adjusted Spot</div>
                 <div className="text-sm font-bold text-slate-800 mt-1">
                    <InlineMath math={`S - X_n = ${fmt(S_adj, 4)}`} />
                 </div>
              </div>
              <div className="bg-slate-50 p-2.5 rounded border border-slate-200 text-center text-sm">
                 <div className="text-xs text-muted font-semibold">Adjusted Strike</div>
                 <div className="text-sm font-bold text-slate-800 mt-1">
                    <InlineMath math={`K + X_f e^{r T} = ${fmt(K_adj, 4)}`} />
                 </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* --- STEP 3: OPTION VALUE --- */}
      <div className={`step-card ${expanded[3] ? 'open' : ''}`}>
        <div className="step-trigger" onClick={() => toggleStep(3)}>
          <div className="step-info">
            <span className="step-circle">3</span>
            <span className="step-title-text">Final Option Price</span>
          </div>
          <div className="step-summary-right">
            <span className="text-primary font-bold text-lg mr-2">${fmt(price, 4)}</span>
            {expanded[3] ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
          </div>
        </div>
        {expanded[3] && (
          <div className="step-content">
            <div className="latex-box small-latex mb-3 transition-all duration-300">
               <BlockMath math={isCall ? 
                 `c \\approx c_{BSM}(${V('S_{adj}', S_adj, 'S')}, ${V('K_{adj}', K_adj, 'K')}, T, r, b, \\sigma)` : 
                 `p \\approx p_{BSM}(${V('S_{adj}', S_adj, 'S')}, ${V('K_{adj}', K_adj, 'K')}, T, r, b, \\sigma)`
               } />
            </div>

            <div className="valuation-receipt">
              <div className="receipt-row positive">
                <div className="receipt-label">
                  <span className="r-title" style={{color: COLORS.S}}>{isCall ? "Adjusted Spot Inflow" : "Adjusted Strike Inflow"}</span>
                </div>
                <div className="receipt-value" style={{color: COLORS.S}}>
                   {isCall ? fmt(S_adj * Nd1, 4) : fmt(K_adj * Math.exp(-r * T) * (1 - Nd2), 4)}
                </div>
              </div>

              <div className="receipt-divider"><Minus size={14} /></div>

              <div className="receipt-row negative">
                <div className="receipt-label">
                  <span className="r-title" style={{color: COLORS.K}}>{isCall ? "Adjusted Strike Outflow" : "Adjusted Spot Outflow"}</span>
                </div>
                <div className="receipt-value" style={{color: COLORS.K}}>
                    {isCall ? fmt(K_adj * Math.exp(-r * T) * Nd2, 4) : fmt(S_adj * (1 - Nd1), 4)}
                </div>
              </div>

              <div className="receipt-total-line"></div>

              <div className="receipt-row total">
                <div className="receipt-label font-bold">
                    BV Option Value <br/>
                </div>
                <div className="receipt-value font-bold">${fmt(price, 4)}</div>
              </div>
            </div>
          </div>
        )}
      </div>

      <ModelExplanation data={TEXTBOOK_DATA.bos_vandermark} />
    </div>
  );
};

export default BosVandermarkWalkthrough;

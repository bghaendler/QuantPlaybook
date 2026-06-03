// --- START OF FILE src/models/HHLWalkthrough.jsx ---

import React, { useState } from 'react';
import { BlockMath, InlineMath } from 'react-katex';
import ModelExplanation from '../ModelExplanation';
import { ChevronDown, ChevronUp, Clock, AlertTriangle, Minus } from 'lucide-react';
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

const HHLWalkthrough = ({ inputs, results, showNumbers }) => {
  const [expanded, setExpanded] = useState({ 1: true, 2: true, 3: true, 4: true });

  const toggleStep = (step) => setExpanded(prev => ({ ...prev, [step]: !prev[step] }));

  const S = inputs.spot || 100;
  const K = inputs.strike || 90;
  const T = inputs.time || 0.75;
  const r = inputs.rate || 0.10;
  const sigma = inputs.volatility || 0.25;
  
  const div1_amt = inputs.div1_amt !== undefined ? inputs.div1_amt : 2.0;
  const div1_time = inputs.div1_time !== undefined ? inputs.div1_time : 0.25;
  const div2_amt = inputs.div2_amt !== undefined ? inputs.div2_amt : 2.0;
  const div2_time = inputs.div2_time !== undefined ? inputs.div2_time : 0.50;

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

  const pv1 = div1_time < T ? div1_amt * Math.exp(-r * div1_time) : 0;
  const pv2 = div2_time < T ? div2_amt * Math.exp(-r * div2_time) : 0;
  const div_pv = pv1 + pv2;
  const S_adj = Math.max(0.01, S - div_pv);

  // Dynamic Vol Adjustment Calculation in JS
  const getHHLVol = () => {
    const divs = [];
    if (div1_amt > 0 && div1_time < T) divs.push({ t: div1_time, amt: div1_amt });
    if (div2_amt > 0 && div2_time < T) divs.push({ t: div2_time, amt: div2_amt });
    divs.sort((a, b) => a.t - b.t);
    
    if (divs.length === 0) return sigma;
    
    let var_adj = 0;
    let t_prev = 0;
    for (let j = 0; j < divs.length; j++) {
      const t_j = divs[j].t;
      let sum_pv = 0;
      for (let i = j; i < divs.length; i++) {
        sum_pv += divs[i].amt * Math.exp(-r * divs[i].t);
      }
      const denom = Math.max(0.01, S - sum_pv);
      const term = Math.pow((S * sigma) / denom, 2) * (t_j - t_prev);
      var_adj += term;
      t_prev = t_j;
    }
    
    const t_n = divs[divs.length - 1].t;
    var_adj += Math.pow(sigma, 2) * (T - t_n);
    return Math.sqrt(Math.max(1e-5, var_adj));
  };
  
  const sigma_adj = getHHLVol();

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

      {/* --- STEP 1: ESCROWED ADJUSTMENT --- */}
      <div className={`step-card ${expanded[1] ? 'open' : ''}`}>
        <div className="step-trigger" onClick={() => toggleStep(1)}>
          <div className="step-info">
            <span className="step-circle">1</span>
            <span className="step-title-text">Escrowed Spot Adjustment</span>
          </div>
          <div className="step-summary-right">
            <span className="text-xs text-muted font-mono">S_adj = {fmt(S_adj, 2)}</span>
            {expanded[1] ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
          </div>
        </div>
        {expanded[1] && (
          <div className="step-content">
            <p className="step-desc text-xs text-muted mb-3">
              First, the observed stock price is replaced with the adjusted price by subtracting the present value of expected cash dividends.
            </p>
            <div className="latex-box transition-all duration-300">
               <BlockMath math={`S_{adj} = ${V('S', S, 'S')} - \\sum D_i e^{-${V('r', r, 'r')} t_i}`} />
            </div>
            <div className="bg-slate-50 p-3 rounded text-sm text-center border border-slate-200 mt-2">
              <InlineMath math={`S_{adj} = ${S} - [${fmt(pv1, 4)} + ${fmt(pv2, 4)}] = ${fmt(S_adj, 4)}`} />
            </div>
          </div>
        )}
      </div>

      {/* --- STEP 2: VOLATILITY ADJUSTMENT --- */}
      <div className={`step-card ${expanded[2] ? 'open' : ''}`}>
        <div className="step-trigger" onClick={() => toggleStep(2)}>
          <div className="step-info">
            <span className="step-circle">2</span>
            <span className="step-title-text">Haug-Haug Volatility Adjustment</span>
          </div>
          <div className="step-summary-right">
            <span className="text-xs text-muted font-mono">σ_adj = {fmt(sigma_adj * 100, 2)}%</span>
            {expanded[2] ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
          </div>
        </div>
        {expanded[2] && (
          <div className="step-content">
            <p className="step-desc text-xs text-muted mb-3">
              We adjust the volatility input using the weighted sum of volatilities over different dividend periods to compensate for the underestimation of absolute variance.
            </p>
            <div className="latex-box transition-all duration-300 mb-3">
               <BlockMath math={`\\sigma_{adj}^2 \\approx \\sum_{j=1}^{n} \\left(\\frac{${V('S', S, 'S')} ${V('\\sigma', sigma, 'sigma')}}{${V('S', S, 'S')}-\\sum_{i=j}^{n} D_i e^{-${V('r', r, 'r')} t_i}}\\right)^{2} (t_j - t_{j-1}) + ${V('\\sigma', sigma, 'sigma')}^2(T - t_n)`} />
            </div>
            <div className="bg-slate-50 p-3 rounded text-sm text-center border border-slate-200">
               <InlineMath math={`\\sigma_{adj} = \\sqrt{${fmt(sigma_adj * sigma_adj, 6)}} = ${fmt(sigma_adj * 100, 2)}\\%`} />
            </div>
          </div>
        )}
      </div>

      {/* --- STEP 3: BSM INTERMEDIATE INPUTS --- */}
      <div className={`step-card ${expanded[3] ? 'open' : ''}`}>
        <div className="step-trigger" onClick={() => toggleStep(3)}>
          <div className="step-info">
            <span className="step-circle">3</span>
            <span className="step-title-text">BSM Intermediate Inputs</span>
          </div>
          <div className="step-summary-right">
            <span className="text-xs text-muted font-mono">d1 = {fmt(d1, 2)}</span>
            {expanded[3] ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
          </div>
        </div>
        {expanded[3] && (
          <div className="step-content">
            <p className="step-desc text-xs text-muted mb-3">
              Calculate the standard BSM d1 and d2 parameters using both the adjusted spot price <InlineMath math="S_{adj}" /> and adjusted volatility <InlineMath math="\sigma_{adj}" />.
            </p>
            <div className="latex-box transition-all duration-300 mb-3">
               <BlockMath math={`d_1 = \\frac{\\ln(${V('S_{adj}', S_adj, 'S')}/${V('K', K, 'K')}) + (${V('r', r, 'r')} + ${V('\\sigma_{adj}', sigma_adj, 'sigma')}^2/2)${V('T', T, 'T')}}{${V('\\sigma_{adj}', sigma_adj, 'sigma')}\\sqrt{${V('T', T, 'T')}}}`} />
            </div>
            <div className="grid grid-cols-2 gap-3 mt-2">
              <div className="bg-slate-50 p-2.5 rounded border border-slate-200 text-center">
                <div className="text-xs font-semibold text-slate-500">d1</div>
                <div className="text-sm font-mono font-bold text-slate-800">{fmt(d1, 4)}</div>
                <div className="text-xs text-slate-400 mt-0.5">N(d1) = {fmt(Nd1, 4)}</div>
              </div>
              <div className="bg-slate-50 p-2.5 rounded border border-slate-200 text-center">
                <div className="text-xs font-semibold text-slate-500">d2</div>
                <div className="text-sm font-mono font-bold text-slate-800">{fmt(d2, 4)}</div>
                <div className="text-xs text-slate-400 mt-0.5">N(d2) = {fmt(Nd2, 4)}</div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* --- STEP 4: OPTION VALUE --- */}
      <div className={`step-card ${expanded[4] ? 'open' : ''}`}>
        <div className="step-trigger" onClick={() => toggleStep(4)}>
          <div className="step-info">
            <span className="step-circle">4</span>
            <span className="step-title-text">Final Option Price</span>
          </div>
          <div className="step-summary-right">
            <span className="text-primary font-bold text-lg mr-2">${fmt(price, 4)}</span>
            {expanded[4] ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
          </div>
        </div>
        {expanded[4] && (
          <div className="step-content">
            <div className="latex-box small-latex mb-3 transition-all duration-300">
               <BlockMath math={isCall ? 
                 `c \\approx ${V('S_{adj}', S_adj, 'S')} N(d_1) - ${V('K', K, 'K')} e^{-${V('r', r, 'r')}${V('T', T, 'T')}} N(d_2)` : 
                 `p \\approx ${V('K', K, 'K')} e^{-${V('r', r, 'r')}${V('T', T, 'T')}} N(-d_2) - ${V('S_{adj}', S_adj, 'S')} N(-d_1)`
               } />
            </div>

            <div className="valuation-receipt">
              <div className="receipt-row positive">
                <div className="receipt-label">
                  <span className="r-title" style={{color: COLORS.S}}>{isCall ? "Adjusted Asset Value" : "Strike Inflow"}</span>
                </div>
                <div className="receipt-value" style={{color: COLORS.S}}>
                   {isCall ? fmt(S_adj * Nd1, 4) : fmt(K * Math.exp(-r * T) * (1 - Nd2), 4)}
                </div>
              </div>

              <div className="receipt-divider"><Minus size={14} /></div>

              <div className="receipt-row negative">
                <div className="receipt-label">
                  <span className="r-title" style={{color: COLORS.K}}>{isCall ? "Strike Cost" : "Adjusted Asset Outflow"}</span>
                </div>
                <div className="receipt-value" style={{color: COLORS.K}}>
                    {isCall ? fmt(K * Math.exp(-r * T) * Nd2, 4) : fmt(S_adj * (1 - Nd1), 4)}
                </div>
              </div>

              <div className="receipt-total-line"></div>

              <div className="receipt-row total">
                <div className="receipt-label font-bold">
                    HHL Call Value <br/>
                </div>
                <div className="receipt-value font-bold">${fmt(price, 4)}</div>
              </div>
            </div>
          </div>
        )}
      </div>

      <ModelExplanation data={TEXTBOOK_DATA.hhl} />
    </div>
  );
};

export default HHLWalkthrough;

// --- START OF FILE src/models/GarmanWalkthrough.jsx ---

import React, { useState, useMemo } from 'react';
import { BlockMath, InlineMath } from 'react-katex';
import { ChevronDown, ChevronUp, Globe, ArrowLeftRight, Minus } from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, ResponsiveContainer, ReferenceLine, Tooltip as RechartsTooltip } from 'recharts';
import 'katex/dist/katex.min.css';

import ModelExplanation from '../ModelExplanation'; 
import { TEXTBOOK_DATA } from '../config/textbookData'; 

// --- COLOR PALETTE FOR MATH ---
const COLORS = {
  S: "#3b82f6",     // Blue-500
  K: "#ec4899",     // Pink-500
  T: "#f59e0b",     // Amber-500
  rd: "#10b981",    // Emerald-500
  rf: "#06b6d4",    // Cyan-500
  sigma: "#8b5cf6", // Violet-500
};

const GarmanWalkthrough = ({ inputs, results, showNumbers }) => {
  const [expanded, setExpanded] = useState({ 1: true, 2: true, 3: true });

  const toggleStep = (step) => {
    setExpanded((prev) => ({ ...prev, [step]: !prev[step] }));
  };

  const fmt = (num, digits = 4) => {
    if (num === undefined || num === null || isNaN(num)) return "-";
    return parseFloat(num.toFixed(digits));
  };

  // Inputs
  const S = inputs.spot || 1.3000; 
  const K = inputs.strike || 1.3000;
  const T = inputs.time || 1;
  const v = inputs.volatility || 0.1;
  const r_dom = inputs.rate || 0.05;      
  const r_for = inputs.dividend || 0.0;   
  const isCall = inputs.type === 'call';

  // Results
  const { d1, Nd1, Nd2, price } = results;

  // Local Calcs
  const ln_SK = Math.log(S / K);
  const vol_term = v * Math.sqrt(T);
  const df_for = Math.exp(-r_for * T);
  const df_dom = Math.exp(-r_dom * T);

  // --- CHART LOGIC: FX DISTRIBUTION ---
  // Centers on Forward Exchange Rate: F = S * e^{(rd - rf)T}
  const distributionData = useMemo(() => {
    const points = [];
    const steps = 60;
    
    // Forward Rate
    const fwd = S * Math.exp((r_dom - r_for) * T);
    
    // Standard Deviation of Rate at T
    const stdDevPrice = fwd * v * Math.sqrt(T);
    
    // Determine Graph Range
    let minX = Math.min(K, fwd) - 3 * stdDevPrice;
    let maxX = Math.max(K, fwd) + 3 * stdDevPrice;
    if (minX <= 0) minX = 0.01;
    
    const range = maxX - minX;
    const stepSize = range / steps;

    // LogNormal PDF Parameters
    const mu_ln = Math.log(S) + (r_dom - r_for - 0.5 * v * v) * T;
    const sigma_ln = v * Math.sqrt(T);

    for (let i = 0; i <= steps; i++) {
        const x = minX + i * stepSize;
        
        // LogNormal PDF
        const term1 = 1 / (x * sigma_ln * Math.sqrt(2 * Math.PI));
        const term2 = Math.exp(-Math.pow(Math.log(x) - mu_ln, 2) / (2 * sigma_ln * sigma_ln));
        const density = term1 * term2;

        // Shading Logic
        let fillValue = 0;
        if (isCall && x >= K) fillValue = density;
        if (!isCall && x <= K) fillValue = density;

        points.push({
            price: x,
            density: density,
            fill: fillValue
        });
    }
    return { data: points, fwd };
  }, [S, K, T, r_dom, r_for, v, isCall]);


  // --- DYNAMIC LATEX GENERATOR ---
  const V = (symbol, value, colorKey) => {
    const color = COLORS[colorKey];
    if (showNumbers) {
       return `\\textcolor{${color}}{${fmt(value, 4)}}`; // 4 digits for FX usually
    }
    return `\\textcolor{${color}}{${symbol}}`;
  };

  // Dynamic Formulas
  const d1_num = `\\ln(${V('S', S, 'S')} / ${V('K', K, 'K')}) + (${V('r_d', r_dom, 'rd')} - ${V('r_f', r_for, 'rf')} + ${V('\\sigma', v, 'sigma')}^2/2)${V('T', T, 'T')}`;
  const d1_den = `${V('\\sigma', v, 'sigma')}\\sqrt{${V('T', T, 'T')}}`;
  
  // c = S e^{-rf T} N(d1) - K e^{-rd T} N(d2)
  const call_eq = `${V('S', S, 'S')} e^{-${V('r_f', r_for, 'rf')}${V('T', T, 'T')}} N(d_1) - ${V('K', K, 'K')} e^{-${V('r_d', r_dom, 'rd')}${V('T', T, 'T')}} N(d_2)`;
  // p = K e^{-rd T} N(-d2) - S e^{-rf T} N(-d1)
  const put_eq = `${V('K', K, 'K')} e^{-${V('r_d', r_dom, 'rd')}${V('T', T, 'T')}} N(-d_2) - ${V('S', S, 'S')} e^{-${V('r_f', r_for, 'rf')}${V('T', T, 'T')}} N(-d_1)`;

  return (
    <div className="math-steps">
      
      {/* --- STEP 1: RATE DIFFERENTIAL --- */}
      <div className={`step-card ${expanded[1] ? 'open' : ''}`}>
        <div className="step-trigger" onClick={() => toggleStep(1)}>
          <div className="step-info">
            <span className="step-circle">1</span>
            <span className="step-title-text">Rate Differential (d₁)</span>
          </div>
          <div className="step-summary-right">
            <span className="mono-val">d₁ = {fmt(d1)}</span>
            {expanded[1] ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
          </div>
        </div>
        {expanded[1] && (
          <div className="step-content">
            <div className="p-3 mb-3 bg-indigo-50 border border-indigo-100 rounded text-sm text-indigo-900 flex items-start gap-2">
              <Globe size={16} className="mt-0.5 shrink-0" />
              <div>
                <strong>FX Logic:</strong> The drift is driven by the interest rate differential <InlineMath math="(r_d - r_f)" />.
              </div>
            </div>
            
            <div className="latex-box transition-all duration-300">
              <BlockMath math={`d_1 = \\frac{${d1_num}}{${d1_den}}`} />
            </div>

            <div className="breakdown-grid">
              <div className="breakdown-item border-l-4" style={{borderLeftColor: COLORS.S}}>
                <span className="label">Moneyness</span>
                <span className="value" style={{color: COLORS.S}}>{fmt(ln_SK)}</span>
              </div>
              <div className="breakdown-item border-l-4" style={{borderLeftColor: COLORS.rd}}>
                <span className="label">Net Rate <InlineMath math="r_d - r_f" /></span>
                <span className="value" style={{color: COLORS.rd}}>{fmt(r_dom - r_for, 3)}</span>
              </div>
              <div className="breakdown-item border-l-4" style={{borderLeftColor: COLORS.sigma}}>
                <span className="label">Vol Term</span>
                <span className="value" style={{color: COLORS.sigma}}>{fmt(vol_term)}</span>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* --- STEP 2: PROBABILITIES (VISUALIZED) --- */}
      <div className={`step-card ${expanded[2] ? 'open' : ''}`}>
        <div className="step-trigger" onClick={() => toggleStep(2)}>
          <div className="step-info">
            <span className="step-circle">2</span>
            <span className="step-title-text">Probability of Profit</span>
          </div>
          <div className="step-summary-right">
            <span className="mono-val">Prob = {fmt(Nd2 * 100, 1)}%</span>
            {expanded[2] ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
          </div>
        </div>

        {expanded[2] && (
          <div className="step-content">
            <p className="step-desc text-xs text-muted mb-4">
              The distribution below shows the <strong>Projected Exchange Rate</strong> range. 
              The Forward Rate (dashed blue) is determined by the rate differential <InlineMath math="r_d - r_f" />.
            </p>

            <div style={{ height: '160px', width: '100%', marginBottom: '10px' }}>
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={distributionData.data}>
                  <defs>
                    <linearGradient id="fxFill" x1="0" y1="0" x2="1" y2="0">
                      <stop offset="0%" stopColor="#6366f1" stopOpacity={isCall ? 0 : 0.4} />
                      <stop offset="100%" stopColor="#6366f1" stopOpacity={isCall ? 0.4 : 0} />
                    </linearGradient>
                  </defs>
                  <XAxis 
                    dataKey="price" 
                    type="number" 
                    domain={['auto', 'auto']} 
                    tickFormatter={(v) => v.toFixed(2)} 
                    tick={{fontSize: 10}}
                    interval="preserveStartEnd"
                  />
                  <YAxis hide />
                  <RechartsTooltip 
                    formatter={(val) => val.toFixed(5)}
                    labelFormatter={(label) => `Rate: ${parseFloat(label).toFixed(4)}`}
                  />
                  <Area 
                    type="monotone" 
                    dataKey="density" 
                    stroke="#94a3b8" 
                    fill="none" 
                    strokeWidth={1.5}
                    isAnimationActive={false} 
                  />
                  <Area 
                    type="monotone" 
                    dataKey="fill" 
                    stroke="none" 
                    fill="#6366f1" 
                    fillOpacity={0.3} 
                    isAnimationActive={false}
                  />
                  <ReferenceLine x={K} stroke="#ec4899" strokeWidth={2} label={{ value: 'Strike', fill: '#ec4899', fontSize: 10, position: 'top' }} />
                  <ReferenceLine x={distributionData.fwd} stroke="#3b82f6" strokeDasharray="3 3" label={{ value: 'Fwd', fill: '#3b82f6', fontSize: 10, position: 'top' }} />
                </AreaChart>
              </ResponsiveContainer>
            </div>

            <div className="probability-table">
              {/* N(d1) */}
              <div className="prob-row">
                <div className="prob-label">
                  <div className="flex items-center gap-2">
                    <InlineMath math={`N(${isCall ? '' : '-'}d_1)`} />
                    <span className="text-xs font-bold bg-green-100 text-green-800 px-1 rounded">Delta</span>
                  </div>
                  <span className="prob-desc mt-1">Foreign Delta</span>
                </div>
                <div className="text-right">
                    <div className="prob-val text-green-600">{fmt(Nd1, 4)}</div>
                    <div className="text-[10px] text-muted leading-tight max-w-[150px]">
                        Hedge ratio for the Foreign Currency.
                    </div>
                </div>
              </div>

              {/* N(d2) */}
              <div className="prob-row">
                <div className="prob-label">
                  <div className="flex items-center gap-2">
                    <InlineMath math={`N(${isCall ? '' : '-'}d_2)`} />
                    <span className="text-xs font-bold bg-blue-100 text-blue-800 px-1 rounded">Prob. ITM</span>
                  </div>
                  <span className="prob-desc mt-1">Probability of Profit</span>
                </div>
                <div className="text-right">
                    <div className="prob-val text-blue-600">{fmt(Nd2, 4)}</div>
                    <div className="text-[10px] text-muted leading-tight max-w-[150px]">
                        Likelihood option expires In-The-Money.
                    </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* --- STEP 3: VALUATION --- */}
      <div className={`step-card ${expanded[3] ? 'open' : ''}`}>
        <div className="step-trigger" onClick={() => toggleStep(3)}>
          <div className="step-info">
            <span className="step-circle">3</span>
            <span className="step-title-text">Valuation</span>
          </div>
          <div className="step-summary-right">
            <span className="text-primary font-bold text-lg">{fmt(price, 4)}</span>
            {expanded[3] ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
          </div>
        </div>

        {expanded[3] && (
          <div className="step-content">
            <div className="latex-box small-latex mb-3">
              <BlockMath math={isCall ? `c = ${call_eq}` : `p = ${put_eq}`} />
            </div>

            <div className="valuation-receipt">
              <div className="flex justify-center mb-2">
                 <div className="inline-flex items-center gap-1 bg-gray-100 text-gray-500 px-2 py-1 rounded text-xs font-semibold uppercase tracking-wider">
                    <ArrowLeftRight size={12} />
                    Dual Discounting
                 </div>
              </div>
              
              <div className="receipt-row positive">
                <div className="receipt-label">
                  <span className="r-title" style={{color: COLORS.S}}>{isCall ? "Foreign Inflow" : "Domestic Inflow"}</span>
                  <span className="r-sub">
                    {isCall ? <span>Discounts at <InlineMath math="r_f" /></span> : <span>Discounts at <InlineMath math="r_d" /></span>}
                  </span>
                </div>
                <div className="receipt-value" style={{color: COLORS.S}}>
                   {isCall ? fmt(S * df_for * Nd1, 4) : fmt(K * df_dom * Nd2, 4)}
                </div>
              </div>
              <div className="receipt-divider"><Minus size={14} /></div>
              <div className="receipt-row negative">
                <div className="receipt-label">
                  <span className="r-title" style={{color: COLORS.K}}>{isCall ? "Domestic Cost" : "Foreign Outflow"}</span>
                  <span className="r-sub">
                     {isCall ? <span>Discounts at <InlineMath math="r_d" /></span> : <span>Discounts at <InlineMath math="r_f" /></span>}
                  </span>
                </div>
                <div className="receipt-value" style={{color: COLORS.K}}>
                    {isCall ? fmt(K * df_dom * Nd2, 4) : fmt(S * df_for * Nd1, 4)}
                </div>
              </div>
              <div className="receipt-total-line"></div>
              <div className="receipt-row total">
                <div className="receipt-label">Option Value</div>
                <div className="receipt-value">{fmt(price, 4)}</div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* --- STEP 4: TEXTBOOK EXPLANATION --- */}
      <ModelExplanation data={TEXTBOOK_DATA.garman} />

    </div>
  );
};

export default GarmanWalkthrough;
// --- START OF FILE src/models/Black76Walkthrough.jsx ---

import React, { useState, useMemo } from 'react';
import { BlockMath, InlineMath } from 'react-katex';
import { ArrowRight, ChevronDown, ChevronUp, Minus, Clock } from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, ResponsiveContainer, ReferenceLine, Tooltip as RechartsTooltip } from 'recharts';
import 'katex/dist/katex.min.css';

// Import Explanation and Data
import ModelExplanation from '../ModelExplanation'; 
import { TEXTBOOK_DATA } from '../config/textbookData'; 

// --- COLOR PALETTE FOR MATH ---
const COLORS = {
  F: "#3b82f6",     // Blue-500 (Futures Price)
  K: "#ec4899",     // Pink-500
  T: "#f59e0b",     // Amber-500
  r: "#10b981",     // Emerald-500
  sigma: "#8b5cf6", // Violet-500
};

const Black76Walkthrough = ({ inputs, results, showNumbers }) => {
  const [expanded, setExpanded] = useState({ 1: true, 2: true, 3: true });

  const toggleStep = (step) => {
    setExpanded((prev) => ({ ...prev, [step]: !prev[step] }));
  };

  const fmt = (num, digits = 4) => {
    if (num === undefined || num === null || isNaN(num)) return "-";
    return parseFloat(num.toFixed(digits));
  };

  // Inputs - For Black-76, "Spot" is actually the Futures Price (F)
  const F = inputs.spot || 100; 
  const K = inputs.strike || 100;
  const T = inputs.time || 1;
  const r = inputs.rate || 0.05;
  const v = inputs.volatility || 0.2;
  const isCall = inputs.type === 'call';

  // Results
  const { d1, Nd1, Nd2, price } = results;

  // Local Calcs
  const ln_FK = Math.log(F / K);
  // Black-76 Drift is (sigma^2)/2 because cost of carry is 0
  const drift = (v * v / 2) * T;
  const vol_term = v * Math.sqrt(T);

  // --- CHART LOGIC: FUTURES DISTRIBUTION ---
  // In Black-76, F is a martingale, so E[F_T] = F
  const distributionData = useMemo(() => {
    const points = [];
    const steps = 60;
    
    // The expected futures price at expiry is just the current F
    const fwd = F;
    
    // Standard Deviation
    const stdDevPrice = F * v * Math.sqrt(T);
    
    // Determine Graph Range
    let minX = Math.min(K, fwd) - 3 * stdDevPrice;
    let maxX = Math.max(K, fwd) + 3 * stdDevPrice;
    if (minX <= 0) minX = 0.1;
    
    const range = maxX - minX;
    const stepSize = range / steps;

    // LogNormal PDF Parameters for Black-76
    // mu = ln(F) - 0.5 * sigma^2 * T
    const mu_ln = Math.log(F) - 0.5 * v * v * T;
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
  }, [F, K, T, v, isCall]);


  // --- DYNAMIC LATEX GENERATOR ---
  const V = (symbol, value, colorKey) => {
    const color = COLORS[colorKey];
    if (showNumbers) {
       return `\\textcolor{${color}}{${fmt(value, 3)}}`;
    }
    return `\\textcolor{${color}}{${symbol}}`;
  };

  // Dynamic Formulas
  // d1 = (ln(F/K) + (sigma^2/2)T) / (sigma * sqrt(T))
  const d1_num = `\\ln(${V('F', F, 'F')} / ${V('K', K, 'K')}) + (${V('\\sigma', v, 'sigma')}^2/2)${V('T', T, 'T')}`;
  const d1_den = `${V('\\sigma', v, 'sigma')}\\sqrt{${V('T', T, 'T')}}`;
  
  // c = e^{-rT} [F N(d1) - K N(d2)]
  const call_eq = `e^{-${V('r', r, 'r')}${V('T', T, 'T')}} [${V('F', F, 'F')} N(d_1) - ${V('K', K, 'K')} N(d_2)]`;
  const put_eq = `e^{-${V('r', r, 'r')}${V('T', T, 'T')}} [${V('K', K, 'K')} N(-d_2) - ${V('F', F, 'F')} N(-d_1)]`;


  return (
    <div className="math-steps">
      
      {/* --- STEP 1: STANDARDIZE --- */}
      <div className={`step-card ${expanded[1] ? 'open' : ''}`}>
        <div className="step-trigger" onClick={() => toggleStep(1)}>
          <div className="step-info">
            <span className="step-circle">1</span>
            <span className="step-title-text">Futures Drift (d₁)</span>
          </div>
          <div className="step-summary-right">
            <span className="mono-val">d₁ = {fmt(d1)}</span>
            {expanded[1] ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
          </div>
        </div>

        {expanded[1] && (
          <div className="step-content">
             <div className="p-3 mb-3 bg-gray-50 border border-gray-200 rounded text-sm text-gray-700">
                <strong>Note:</strong> For Futures options, the drift is determined solely by volatility. The risk-free rate only affects the final discounting.
            </div>

            <div className="latex-box transition-all duration-300">
              <BlockMath math={`d_1 = \\frac{${d1_num}}{${d1_den}}`} />
            </div>

            <div className="breakdown-grid">
              <div className="breakdown-item border-l-4" style={{borderLeftColor: COLORS.F}}>
                <span className="label">Log Ratio <InlineMath math="\ln(F/K)" /></span>
                <span className="value" style={{color: COLORS.F}}>{fmt(ln_FK)}</span>
              </div>
              <div className="breakdown-item border-l-4" style={{borderLeftColor: COLORS.sigma}}>
                <span className="label">Convexity <InlineMath math="\sigma^2/2" /></span>
                <span className="value" style={{color: COLORS.sigma}}>{fmt(drift)}</span>
              </div>
              <div className="breakdown-item border-l-4" style={{borderLeftColor: COLORS.sigma}}>
                <span className="label">Vol Term</span>
                <span className="value" style={{color: COLORS.sigma}}>{fmt(vol_term)}</span>
              </div>
            </div>

            <div className="calculation-flow">
              <span className="calc-math">
                ({fmt(ln_FK)} + {fmt(drift)}) ÷ {fmt(vol_term)}
              </span>
              <ArrowRight size={14} className="mx-2 text-muted" />
              <span className="mono-val text-primary font-bold">{fmt(d1)}</span>
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
              The distribution below shows the range of possible <strong>Futures Prices</strong> at expiration. 
              Since futures are risk-neutral, the curve is centered on the current Futures Price ({fmt(F)}).
            </p>

            <div style={{ height: '160px', width: '100%', marginBottom: '10px' }}>
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={distributionData.data}>
                  <defs>
                    <linearGradient id="b76Fill" x1="0" y1="0" x2="1" y2="0">
                      <stop offset="0%" stopColor="#3b82f6" stopOpacity={isCall ? 0 : 0.4} />
                      <stop offset="100%" stopColor="#3b82f6" stopOpacity={isCall ? 0.4 : 0} />
                    </linearGradient>
                  </defs>
                  <XAxis 
                    dataKey="price" 
                    type="number" 
                    domain={['auto', 'auto']} 
                    tickFormatter={(v) => v.toFixed(0)} 
                    tick={{fontSize: 10}}
                    interval="preserveStartEnd"
                  />
                  <YAxis hide />
                  <RechartsTooltip 
                    formatter={(val) => val.toFixed(5)}
                    labelFormatter={(label) => `Price: $${parseFloat(label).toFixed(2)}`}
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
                    fill="#3b82f6" 
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
                  <span className="prob-desc mt-1">Futures Hedge Ratio</span>
                </div>
                <div className="text-right">
                    <div className="prob-val text-green-600">{fmt(Nd1, 4)}</div>
                    <div className="text-[10px] text-muted leading-tight max-w-[150px]">
                        Sensitivity to Futures Price.
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
            <span className="text-primary font-bold text-lg">${fmt(price, 2)}</span>
            {expanded[3] ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
          </div>
        </div>

        {expanded[3] && (
          <div className="step-content">
            <div className="latex-box small-latex mb-3">
              <BlockMath math={isCall ? `C = ${call_eq}` : `P = ${put_eq}`} />
            </div>

            <div className="valuation-receipt">
              <div className="flex justify-center mb-4">
                 <div className="inline-flex items-center gap-1 bg-gray-100 text-gray-600 px-2 py-1 rounded text-xs font-semibold uppercase tracking-wider">
                    <Clock size={12} />
                    Discounted at end (Late Settlement)
                 </div>
              </div>

              {/* Positive Flow */}
              <div className="receipt-row positive">
                <div className="receipt-label">
                  <span className="r-title" style={{color: COLORS.F}}>{isCall ? "Futures Value" : "Strike Inflow"}</span>
                  <span className="r-sub">Weighted by Prob</span>
                </div>
                <div className="receipt-value" style={{color: COLORS.F}}>
                   {isCall ? fmt(F * Nd1, 2) : fmt(K * (1 - Nd2), 2)}
                </div>
              </div>

              <div className="receipt-divider"><Minus size={14} /></div>

              {/* Negative Flow */}
              <div className="receipt-row negative">
                <div className="receipt-label">
                  <span className="r-title" style={{color: COLORS.K}}>{isCall ? "Strike Cost" : "Futures Outflow"}</span>
                  <span className="r-sub">Weighted by Prob</span>
                </div>
                <div className="receipt-value" style={{color: COLORS.K}}>
                    {isCall ? fmt(K * Nd2, 2) : fmt(F * (1 - Nd1), 2)}
                </div>
              </div>
              
              <div className="receipt-row">
                 <div className="receipt-label">
                     <span className="r-title">Undiscounted Value</span>
                 </div>
                 <div className="receipt-value text-muted">
                     {fmt(isCall ? (F*Nd1 - K*Nd2) : (K*(1-Nd2) - F*(1-Nd1)), 2)}
                 </div>
              </div>

              <div className="receipt-total-line"></div>

              <div className="receipt-row total">
                <div className="receipt-label">
                    Discounted Price <br/>
                    <span className="text-xs font-normal text-muted">
                        <InlineMath math={`\\times e^{-${fmt(r,2)}\\cdot${T}}`} />
                    </span>
                </div>
                <div className="receipt-value">${fmt(price, 2)}</div>
              </div>
            </div>
          </div>
        )}
      </div>
      
      {/* --- STEP 4: TEXTBOOK EXPLANATION --- */}
      <ModelExplanation data={TEXTBOOK_DATA.black76} />

    </div>
  );
};

export default Black76Walkthrough;
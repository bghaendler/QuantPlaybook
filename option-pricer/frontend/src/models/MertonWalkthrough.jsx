// --- START OF FILE src/models/MertonWalkthrough.jsx ---

import React, { useState, useMemo } from 'react';
import { BlockMath, InlineMath } from 'react-katex';
import { ArrowRight, ChevronDown, ChevronUp, Minus, Lightbulb } from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, ResponsiveContainer, ReferenceLine, Tooltip as RechartsTooltip } from 'recharts';
import 'katex/dist/katex.min.css';

// 1. Import the Explanation Component and Data
import ModelExplanation from '../ModelExplanation';
import { TEXTBOOK_DATA } from '../config/textbookData';

// --- COLOR PALETTE FOR MATH ---
const COLORS = {
  S: "#3b82f6",     // Blue-500
  K: "#ec4899",     // Pink-500
  T: "#f59e0b",     // Amber-500
  r: "#10b981",     // Emerald-500
  q: "#06b6d4",     // Cyan-500 (Dividend Yield)
  sigma: "#8b5cf6", // Violet-500
};

const MertonWalkthrough = ({ inputs, results, showNumbers, highlightedVar, onHighlight, activeView }) => {
  const [expanded, setExpanded] = useState({ 1: true, 2: true, 3: true });

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
  const v = inputs.volatility || 0.2;
  const q = inputs.dividend || 0; // The Star of Merton '73
  const isCall = inputs.type === 'call';

  // Results
  const { d1, Nd1, Nd2, price } = results;

  // Local Calcs
  const ln_SK = Math.log(S / K);
  // Note: Merton Drift = r - q + v^2/2
  const drift = (r - q + (v * v) / 2) * T;
  const vol_term = v * Math.sqrt(T);
  const df_q = Math.exp(-q * T); // Dividend Discount Factor
  const df_r = Math.exp(-r * T); // Risk-Free Discount Factor

  // --- CHART LOGIC: PRICE DISTRIBUTION ---
  // Calculates Log-Normal distribution centered on Forward Price (S * e^{(r-q)T})
  const distributionData = useMemo(() => {
    const points = [];
    const steps = 60;

    // Forward Price taking Dividend (q) into account
    // High dividends reduce the forward price
    const fwd = S * Math.exp((r - q) * T);

    // Standard Deviation of Price at T
    const stdDevPrice = fwd * v * Math.sqrt(T);

    // Determine Graph Range
    let minX = Math.min(K, fwd) - 3 * stdDevPrice;
    let maxX = Math.max(K, fwd) + 3 * stdDevPrice;
    if (minX <= 0) minX = 0.1;

    const range = maxX - minX;
    const stepSize = range / steps;

    // LogNormal PDF Parameters
    const mu_ln = Math.log(S) + (r - q - 0.5 * v * v) * T;
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
  }, [S, K, T, r, q, v, isCall]);


  // --- DYNAMIC LATEX GENERATOR ---
  const V = (symbol, value, colorKey) => {
    const color = COLORS[colorKey];

    // Map highlightedVar to colorKey
    const varMap = {
      'spot': 'S',
      'strike': 'K',
      'time': 'T',
      'rate': 'r',
      'volatility': 'sigma',
      'dividend': 'q'
    };

    const isHighlighted = highlightedVar && varMap[highlightedVar] === colorKey;

    const content = showNumbers ? fmt(value, 3) : symbol;
    const coloredContent = `\\textcolor{${color}}{${content}}`;

    if (isHighlighted) {
      return `\\mathbf{${coloredContent}}`;
    }
    return coloredContent;
  };

  // Dynamic Formulas
  const d1_num = `\\ln(${V('S', S, 'S')} / ${V('K', K, 'K')}) + (${V('r', r, 'r')} - ${V('q', q, 'q')} + ${V('\\sigma', v, 'sigma')}^2/2)${V('T', T, 'T')}`;
  const d1_den = `${V('\\sigma', v, 'sigma')}\\sqrt{${V('T', T, 'T')}}`;

  const call_eq = `${V('S', S, 'S')} e^{-${V('q', q, 'q')}${V('T', T, 'T')}} N(d_1) - ${V('K', K, 'K')} e^{-${V('r', r, 'r')}${V('T', T, 'T')}} N(d_2)`;
  const put_eq = `${V('K', K, 'K')} e^{-${V('r', r, 'r')}${V('T', T, 'T')}} N(-d_2) - ${V('S', S, 'S')} e^{-${V('q', q, 'q')}${V('T', T, 'T')}} N(-d_1)`;


  return (
    <div className="math-steps">

      {activeView === 'calc' && (
        <>
          {/* --- STEP 1: COST OF CARRY ADJUSTMENT --- */}
          <div className={`step-card ${expanded[1] ? 'open' : ''}`}>
            <div className="step-trigger" onClick={() => toggleStep(1)}>
              <div className="step-info">
                <span className="step-circle">1</span>
                <span className="step-title-text">Cost of Carry (d₁)</span>
              </div>
              <div className="step-summary-right">
                <span className="mono-val">d₁ = {fmt(d1)}</span>
                {expanded[1] ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
              </div>
            </div>

            {expanded[1] && (
              <div className="step-content">
                <div className="p-3 mb-3 bg-indigo-50 border border-indigo-100 rounded-lg text-sm text-indigo-900 flex items-start gap-3 shadow-sm">
                  <div className="bg-indigo-100 p-1.5 rounded-full shrink-0 mt-0.5">
                    <Lightbulb size={14} className="text-indigo-600" />
                  </div>
                  <div className="leading-relaxed">
                    <strong className="block mb-1 text-indigo-700">Merton's Innovation</strong>
                    The drift term includes <InlineMath math="-q" />, accounting for the <strong>continuous dividend yield</strong> paying out from the asset, which reduces its future expected spot price.
                  </div>
                </div>

                <div className="latex-box transition-all duration-300">
                  <BlockMath math={`d_1 = \\frac{${d1_num}}{${d1_den}}`} />
                </div>

                <div className="breakdown-grid">
                  <div className="breakdown-item border-l-4" style={{ borderLeftColor: COLORS.S }}>
                    <span className="label">Moneyness</span>
                    <span className="value" style={{ color: COLORS.S }}>{fmt(ln_SK)}</span>
                  </div>
                  <div
                    className="breakdown-item border-l-4 hover:bg-slate-50 cursor-pointer transition-colors"
                    style={{ borderLeftColor: COLORS.q }}
                    onMouseEnter={() => onHighlight && onHighlight('dividend')}
                    onMouseLeave={() => onHighlight && onHighlight(null)}
                  >
                    <span className="label">Adj. Drift (r - q)</span>
                    <span className="value" style={{ color: COLORS.q }}>{fmt(r - q, 3)}</span>
                  </div>
                  <div
                    className="breakdown-item border-l-4 hover:bg-slate-50 cursor-pointer transition-colors"
                    style={{ borderLeftColor: COLORS.sigma }}
                    onMouseEnter={() => onHighlight && onHighlight('volatility')}
                    onMouseLeave={() => onHighlight && onHighlight(null)}
                  >
                    <span className="label">Vol Term</span>
                    <span className="value" style={{ color: COLORS.sigma }}>{fmt(vol_term)}</span>
                  </div>
                </div>

                <div className="calculation-flow">
                  <span className="calc-math">
                    <InlineMath math={`q=${fmt(q, 3)}`} /> reduces drift → lower d₁ → lower Call Price
                  </span>
                </div>
              </div>
            )}
          </div>

          {/* --- STEP 2: PROBABILITIES (LOG-NORMAL) --- */}
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
                  The distribution below shows the <strong>Projected Price Range</strong> taking dividends into account.
                  The dividend yield (<InlineMath math="q" />) drags the Forward Price (dashed blue line) lower, affecting the probability of finishing In-The-Money.
                </p>

                <div style={{ height: '160px', width: '100%', marginBottom: '10px' }}>
                  <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={distributionData.data}>
                      <defs>
                        <linearGradient id="mertonFill" x1="0" y1="0" x2="1" y2="0">
                          <stop offset="0%" stopColor="#3B82F6" stopOpacity={isCall ? 0 : 0.4} />
                          <stop offset="100%" stopColor="#3B82F6" stopOpacity={isCall ? 0.4 : 0} />
                        </linearGradient>
                      </defs>
                      <XAxis
                        dataKey="price"
                        type="number"
                        domain={['auto', 'auto']}
                        tickFormatter={(v) => v.toFixed(0)}
                        tick={{ fontSize: 10 }}
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
                        fill="#3B82F6"
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
                      <span className="prob-desc mt-1">The Hedge Ratio</span>
                    </div>
                    <div className="text-right">
                      <div className="prob-val text-green-600">{fmt(Nd1, 4)}</div>
                      <div className="text-[10px] text-muted leading-tight max-w-[150px]">
                        Sensitivity to Spot Price.
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
                  {/* Positive Flow */}
                  <div className="receipt-row positive">
                    <div className="receipt-label">
                      <span className="r-title" style={{ color: COLORS.S }}>{isCall ? "Asset Inflow" : "Strike Inflow"}</span>
                      <span className="r-sub">
                        {isCall ? <span>Discounted by yield <InlineMath math={`e^{-${fmt(q, 2)}T}`} /></span> : "Risk-free discounted"}
                      </span>
                    </div>
                    <div className="receipt-value" style={{ color: COLORS.S }}>
                      {isCall ? fmt(S * df_q * Nd1, 2) : fmt(K * df_r * (1 - Nd2), 2)}
                    </div>
                  </div>

                  <div className="receipt-divider"><Minus size={14} /></div>

                  {/* Negative Flow */}
                  <div className="receipt-row negative">
                    <div className="receipt-label">
                      <span className="r-title" style={{ color: COLORS.K }}>{isCall ? "Strike Cost" : "Asset Outflow"}</span>
                      <span className="r-sub">
                        {isCall ? "Risk-free discounted" : <span>Discounted by yield <InlineMath math={`e^{-${fmt(q, 2)}T}`} /></span>}
                      </span>
                    </div>
                    <div className="receipt-value" style={{ color: COLORS.K }}>
                      {isCall ? fmt(K * df_r * Nd2, 2) : fmt(S * df_q * (1 - Nd1), 2)}
                    </div>
                  </div>

                  <div className="receipt-total-line"></div>

                  <div className="receipt-row total">
                    <div className="receipt-label">Fair Price</div>
                    <div className="receipt-value">${fmt(price, 2)}</div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </>
      )}

      {/* --- STEP 4: TEXTBOOK EXPLANATION --- */}
      {activeView === 'doc' && (
        <ModelExplanation data={TEXTBOOK_DATA.merton} />
      )}

    </div>
  );
};

export default MertonWalkthrough;
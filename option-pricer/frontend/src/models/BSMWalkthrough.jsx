// --- START OF FILE src/models/BSMWalkthrough.jsx ---

import React, { useState, useMemo } from 'react';
import { BlockMath, InlineMath } from 'react-katex';
import { ArrowRight, ChevronDown, ChevronUp, Minus, HelpCircle } from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, ResponsiveContainer, ReferenceLine, Tooltip as RechartsTooltip } from 'recharts';
import 'katex/dist/katex.min.css';
import ModelExplanation from '../ModelExplanation';
import { TEXTBOOK_DATA } from '../config/textbookData';

// --- COLOR PALETTE FOR MATH ---
const COLORS = {
  S: "#3b82f6",     // Blue-500
  K: "#ec4899",     // Pink-500
  T: "#f59e0b",     // Amber-500
  r: "#10b981",     // Emerald-500
  sigma: "#8b5cf6", // Violet-500
  q: "#06b6d4",     // Cyan-500
};

const BSMWalkthrough = ({ inputs, results, showNumbers, highlightedVar, onHighlight, activeView }) => {
  const [expanded, setExpanded] = useState({ 1: true, 2: true, 3: true });

  const toggleStep = (step) => {
    setExpanded((prev) => ({ ...prev, [step]: !prev[step] }));
  };

  const fmt = (num, digits = 4) => {
    if (num === undefined || num === null || isNaN(num)) return "-";
    return parseFloat(num.toFixed(digits));
  };

  // Extract Inputs
  const S = inputs.spot || 100;
  const K = inputs.strike || 100;
  const T = inputs.time || 1;
  const r = inputs.rate || 0.05;
  const v = inputs.volatility || 0.2;
  const q = inputs.dividend || 0;
  const isCall = inputs.type === 'call';

  // Extract Results
  const { d1, Nd1, Nd2, price } = results;

  // Local Calcs
  const ln_SK = Math.log(S / K);
  const drift = (r - q + (v * v) / 2) * T;
  const vol_term = v * Math.sqrt(T);
  const df_q = Math.exp(-q * T);
  const df_r = Math.exp(-r * T);

  // --- CHART LOGIC: PRICE DISTRIBUTION ---
  // We generate a LogNormal distribution centered around the Forward Price
  const distributionData = useMemo(() => {
    const points = [];
    const steps = 60;

    // Forward Price (Expected Value of S_T in risk-neutral world)
    const fwd = S * Math.exp((r - q) * T);

    // Standard Deviation of Price at T (approximate for graph range)
    // We assume roughly log-normal spread
    const stdDevPrice = fwd * v * Math.sqrt(T);

    // Determine Graph Range
    // Ensure Strike is visible, but center on Forward
    let minX = Math.min(K, fwd) - 3 * stdDevPrice;
    let maxX = Math.max(K, fwd) + 3 * stdDevPrice;

    // Clamp minX to > 0
    if (minX <= 0) minX = 0.1;

    const range = maxX - minX;
    const stepSize = range / steps;

    // LogNormal PDF Parameters
    // mu_ln = ln(S) + (r - q - v^2/2)T
    const mu_ln = Math.log(S) + (r - q - 0.5 * v * v) * T;
    const sigma_ln = v * Math.sqrt(T);

    for (let i = 0; i <= steps; i++) {
      const x = minX + i * stepSize;

      // LogNormal PDF formula
      // f(x) = (1 / (x * sigma * sqrt(2*pi))) * exp( - (ln x - mu)^2 / (2sigma^2) )
      const term1 = 1 / (x * sigma_ln * Math.sqrt(2 * Math.PI));
      const term2 = Math.exp(-Math.pow(Math.log(x) - mu_ln, 2) / (2 * sigma_ln * sigma_ln));
      const density = term1 * term2;

      // Shading Logic
      // For Call: Shade if Price > Strike
      // For Put: Shade if Price < Strike
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

    // Add a thin space in KaTeX to prevent browser font clipping on the last digit
    const content = showNumbers ? `${fmt(value, 3)}\\,` : symbol;
    const coloredContent = `\\textcolor{${color}}{${content}}`;

    if (isHighlighted) {
      return `\\mathbf{${coloredContent}}`;
    }
    return coloredContent;
  };

  const d1_numerator = `\\ln(${V('S', S, 'S')} / ${V('K', K, 'K')}) + (${V('r', r, 'r')} - ${V('q', q, 'q')} + ${V('\\sigma', v, 'sigma')}^2/2)${V('T', T, 'T')}`;
  const d1_denominator = `${V('\\sigma', v, 'sigma')}\\sqrt{${V('T', T, 'T')}}`;

  const call_formula = `${V('S', S, 'S')} e^{-${V('q', q, 'q')}${V('T', T, 'T')}} N(d_1) - ${V('K', K, 'K')} e^{-${V('r', r, 'r')}${V('T', T, 'T')}} N(d_2)`;
  const put_formula = `${V('K', K, 'K')} e^{-${V('r', r, 'r')}${V('T', T, 'T')}} N(-d_2) - ${V('S', S, 'S')} e^{-${V('q', q, 'q')}${V('T', T, 'T')}} N(-d_1)`;

  return (
    <div className="math-steps">

      {activeView === 'calc' && (
        <>
          {/* --- STEP 1: STANDARDIZE --- */}
          <div className={`step-card ${expanded[1] ? 'open' : ''}`}>
            <div className="step-trigger" onClick={() => toggleStep(1)}>
              <div className="step-info">
                <span className="step-circle">1</span>
                <span className="step-title-text">Standardize Inputs (d₁)</span>
              </div>
              <div className="step-summary-right">
                <span className="mono-val">d₁ = {fmt(d1)}</span>
                {expanded[1] ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
              </div>
            </div>

            {expanded[1] && (
              <div className="step-content">
                <div className="latex-box transition-all duration-300">
                  <BlockMath math={`d_1 = \\frac{${d1_numerator}}{${d1_denominator}}`} />
                </div>

                <div className="breakdown-grid">
                  <div
                    className="breakdown-item border-l-4 hover:bg-slate-50 cursor-pointer transition-colors"
                    style={{ borderLeftColor: COLORS.S }}
                    onMouseEnter={() => onHighlight && onHighlight('spot')}
                    onMouseLeave={() => onHighlight && onHighlight(null)}
                  >
                    <span className="label">Moneyness <InlineMath math="\ln(S/K)" /></span>
                    <span className="value" style={{ color: COLORS.S }}>{fmt(ln_SK)}</span>
                  </div>
                  <div
                    className="breakdown-item border-l-4 hover:bg-slate-50 cursor-pointer transition-colors"
                    style={{ borderLeftColor: COLORS.r }}
                    onMouseEnter={() => onHighlight && onHighlight('rate')}
                    onMouseLeave={() => onHighlight && onHighlight(null)}
                  >
                    <span className="label">Drift Term</span>
                    <span className="value" style={{ color: COLORS.r }}>{fmt(drift)}</span>
                  </div>
                  <div
                    className="breakdown-item border-l-4 hover:bg-slate-50 cursor-pointer transition-colors"
                    style={{ borderLeftColor: COLORS.sigma }}
                    onMouseEnter={() => onHighlight && onHighlight('volatility')}
                    onMouseLeave={() => onHighlight && onHighlight(null)}
                  >
                    <span className="label">Volatility Term</span>
                    <span className="value" style={{ color: COLORS.sigma }}>{fmt(vol_term)}</span>
                  </div>
                </div>

                <div className="calculation-flow">
                  <span className="calc-math">
                    ({fmt(ln_SK)} + {fmt(drift)}) ÷ {fmt(vol_term)}
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
                  The distribution below shows the <strong>Projected Price Range</strong> at expiration based on Volatility.
                  The shaded area represents the probability of the option finishing <strong>In-The-Money</strong>.
                </p>

                <div style={{ height: '160px', width: '100%', marginBottom: '10px' }}>
                  <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={distributionData.data} margin={{ top: 10, right: 12, left: 12, bottom: 18 }}>
                      <defs>
                        <linearGradient id="probFill" x1="0" y1="0" x2="1" y2="0">
                          <stop offset="0%" stopColor="#4F46E5" stopOpacity={isCall ? 0 : 0.4} />
                          <stop offset="100%" stopColor="#4F46E5" stopOpacity={isCall ? 0.4 : 0} />
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
                      {/* Hide Y Axis, it's PDF density, abstract to user */}
                      <YAxis hide />

                      <RechartsTooltip
                        formatter={(val) => val.toFixed(5)}
                        labelFormatter={(label) => `Price: $${parseFloat(label).toFixed(2)}`}
                      />

                      {/* The Curve */}
                      <Area
                        type="monotone"
                        dataKey="density"
                        stroke="#94a3b8"
                        fill="none"
                        strokeWidth={1.5}
                        isAnimationActive={false}
                      />

                      {/* The Shaded ITM Area */}
                      <Area
                        type="monotone"
                        dataKey="fill"
                        stroke="none"
                        fill="#4F46E5"
                        fillOpacity={0.3}
                        isAnimationActive={false}
                      />

                      {/* Strike Line */}
                      <ReferenceLine x={K} stroke="#ec4899" strokeWidth={2} label={{ value: 'Strike', fill: '#ec4899', fontSize: 10, position: 'top' }} />

                      {/* Forward Price Line */}
                      <ReferenceLine x={distributionData.fwd} stroke="#3b82f6" strokeDasharray="3 3" label={{ value: 'Fwd', fill: '#3b82f6', fontSize: 10, position: 'top' }} />

                    </AreaChart>
                  </ResponsiveContainer>
                </div>

                <div className="probability-table">
                  {/* N(d1) - Delta */}
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
                        Amount of asset to buy/sell to replicate the option.
                      </div>
                    </div>
                  </div>

                  {/* N(d2) - Probability */}
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
                  <BlockMath math={isCall ? `C = ${call_formula}` : `P = ${put_formula}`} />
                </div>

                <div className="valuation-receipt">
                  {/* Positive Flow */}
                  <div className="receipt-row positive">
                    <div className="receipt-label">
                      <span className="r-title" style={{ color: COLORS.S }}>Asset Term</span>
                      <span className="r-sub">Adjusted for Prob & Disc</span>
                    </div>
                    <div className="receipt-value" style={{ color: COLORS.S }}>
                      {isCall ? fmt(S * df_q * Nd1, 2) : fmt(K * df_r * (1 - Nd2), 2)}
                    </div>
                  </div>

                  <div className="receipt-divider">
                    <Minus size={14} />
                  </div>

                  {/* Negative Flow */}
                  <div className="receipt-row negative">
                    <div className="receipt-label">
                      <span className="r-title" style={{ color: COLORS.K }}>Strike Term</span>
                      <span className="r-sub">Adjusted for Prob & Disc</span>
                    </div>
                    <div className="receipt-value" style={{ color: COLORS.K }}>
                      {isCall ? fmt(K * df_r * Nd2, 2) : fmt(S * df_q * (1 - Nd1), 2)}
                    </div>
                  </div>

                  {/* Total */}
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

      {activeView === 'doc' && (
        <ModelExplanation data={TEXTBOOK_DATA.bsm} />
      )}
    </div>
  );
};

export default BSMWalkthrough;
import React, { useState } from 'react';
import { BlockMath, InlineMath } from 'react-katex';
import { ArrowRight, ChevronDown, ChevronUp, Minus } from 'lucide-react';
import { AreaChart, Area, ResponsiveContainer, ReferenceLine } from 'recharts';
import 'katex/dist/katex.min.css';

const BSMWalkthrough = ({ inputs, results }) => {
  const [expanded, setExpanded] = useState({ 1: true, 2: false, 3: true });

  const toggleStep = (step) => {
    setExpanded((prev) => ({ ...prev, [step]: !prev[step] }));
  };

  const fmt = (num, digits = 4) => {
    if (num === undefined || num === null || isNaN(num)) return "-";
    return num.toFixed(digits);
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

  // Local Calcs for visualization only
  const ln_SK = Math.log(S / K);
  const drift = (r - q + (v * v) / 2) * T;
  const vol_term = v * Math.sqrt(T);
  const df_q = Math.exp(-q * T);
  const df_r = Math.exp(-r * T);

  // Determine terms based on Call/Put
  const term_asset = isCall ? S * df_q * Nd1 : S * df_q * (1 - Nd1);
  const term_strike = isCall ? K * df_r * Nd2 : K * df_r * (1 - Nd2);

  // For the receipt visualization
  const inflow = isCall ? term_asset : term_strike;
  const outflow = isCall ? term_strike : term_asset;

  return (
    <div className="math-steps">
      
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
            <div className="latex-box">
              <BlockMath math={`d_1 = \\frac{\\ln(S/K) + (r - q + \\sigma^2/2)T}{\\sigma\\sqrt{T}}`} />
            </div>

            <div className="breakdown-grid">
              <div className="breakdown-item">
                <span className="label">Moneyness <InlineMath math="\ln(S/K)" /></span>
                <span className="value">{fmt(ln_SK)}</span>
              </div>
              <div className="breakdown-item">
                <span className="label">Drift Term</span>
                <span className="value">{fmt(drift)}</span>
              </div>
              <div className="breakdown-item">
                <span className="label">Volatility Term</span>
                <span className="value">{fmt(vol_term)}</span>
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

      {/* --- STEP 2: PROBABILITIES --- */}
      <div className={`step-card ${expanded[2] ? 'open' : ''}`}>
        <div className="step-trigger" onClick={() => toggleStep(2)}>
          <div className="step-info">
            <span className="step-circle">2</span>
            <span className="step-title-text">Probabilities</span>
          </div>
          <div className="step-summary-right">
            <span className="mono-val">N(d₂) = {fmt(Nd2)}</span>
            {expanded[2] ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
          </div>
        </div>

        {expanded[2] && (
          <div className="step-content">
            <p className="step-desc">
              The probability of the option finishing In-The-Money (risk-adjusted).
            </p>

            {results.distribution_data && (
              <div style={{ height: '100px', width: '100%', marginBottom: '10px' }}>
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={results.distribution_data}>
                    <defs>
                      <linearGradient id="colorFill" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#4F46E5" stopOpacity={0.3} />
                        <stop offset="95%" stopColor="#4F46E5" stopOpacity={0} />
                      </linearGradient>
                    </defs>
                    <Area type="monotone" dataKey="fill" stroke="none" fill="url(#colorFill)" />
                    <Area type="monotone" dataKey="y" stroke="#94a3b8" fill="none" strokeWidth={1} />
                    <ReferenceLine x={isCall ? results.d2 : -results.d2} stroke="#EF4444" strokeDasharray="2 2" />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
            )}

            <div className="probability-table">
              <div className="prob-row">
                <div className="prob-label">
                  <InlineMath math={`N(${isCall ? '' : '-'}d_1)`} />
                  <span className="prob-desc">Asset Factor</span>
                </div>
                <div className="prob-val text-green-600">{fmt(Nd1)}</div>
              </div>
              <div className="prob-row">
                <div className="prob-label">
                  <InlineMath math={`N(${isCall ? '' : '-'}d_2)`} />
                  <span className="prob-desc">Prob. Exercise</span>
                </div>
                <div className="prob-val text-blue-600">{fmt(Nd2)}</div>
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
              {isCall ? (
                <BlockMath math={`C = Se^{-qT}N(d_1) - Ke^{-rT}N(d_2)`} />
              ) : (
                <BlockMath math={`P = Ke^{-rT}N(-d_2) - Se^{-qT}N(-d_1)`} />
              )}
            </div>

            <div className="valuation-receipt">
              {/* Positive Flow */}
              <div className="receipt-row positive">
                <div className="receipt-label">
                  <span className="r-title">{isCall ? "Asset Value" : "Strike Inflow"}</span>
                  <span className="r-sub">Adjusted for Prob & Disc</span>
                </div>
                <div className="receipt-value">
                   {isCall ? fmt(S * df_q * Nd1, 2) : fmt(K * df_r * (1 - Nd2), 2)}
                </div>
              </div>

              {/* Subtraction Symbol */}
              <div className="receipt-divider">
                <Minus size={14} />
              </div>

              {/* Negative Flow */}
              <div className="receipt-row negative">
                <div className="receipt-label">
                  <span className="r-title">{isCall ? "Strike Cost" : "Asset Outflow"}</span>
                  <span className="r-sub">Adjusted for Prob & Disc</span>
                </div>
                <div className="receipt-value">
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
    </div>
  );
};

export default BSMWalkthrough;
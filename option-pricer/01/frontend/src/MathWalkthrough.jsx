import React, { useState } from 'react';
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts';
import { BookOpen, TrendingUp, Activity, Clock, Calculator, Sigma, ArrowRight, ChevronDown, ChevronUp, Minus, Equal } from 'lucide-react';
import 'katex/dist/katex.min.css';
import { InlineMath, BlockMath } from 'react-katex';

const MathWalkthrough = ({ inputs, results, mode }) => {
  // State to track which steps are expanded
  const [expanded, setExpanded] = useState({ 1: false, 2: false, 3: true });

  const toggleStep = (step) => {
    setExpanded(prev => ({ ...prev, [step]: !prev[step] }));
  };

  if (!results || results.d1 === undefined || results.greeks === undefined) return null;

  const isCall = inputs.type === 'call';
  const q = mode === 'bs' ? 0 : inputs.dividend;
  const { spot, strike, time, rate, volatility } = inputs;

  // --- Intermediate Calculations ---
  const ln_SK = Math.log(spot / strike).toFixed(4);
  const drift = (rate - q + (0.5 * Math.pow(volatility, 2))).toFixed(4);
  const vol_time = (volatility * Math.sqrt(time)).toFixed(4);
  
  // Discounting logic
  const df_q = Math.exp(-q * time); 
  const df_r = Math.exp(-rate * time); 
  
  // The two main terms of the equation
  const rawAsset = spot * results.Nd1; // S * N(d1)
  const discountedAsset = (rawAsset * df_q).toFixed(2); // discounted
  
  const rawStrike = strike * results.Nd2; // K * N(d2)
  const discountedStrike = (rawStrike * df_r).toFixed(2); // discounted

  return (
    <div className="math-container">
      <div className="math-header">
        <h2><BookOpen size={20} className="text-indigo-600"/> The Math Engine</h2>
        <p>Step-by-step derivation of the {isCall ? "Call" : "Put"} Price.</p>
      </div>

      {/* --- STEP 1: STANDARDIZATION --- */}
      <div className={`step-card ${expanded[1] ? 'open' : ''}`}>
        <div className="step-trigger" onClick={() => toggleStep(1)}>
          <div className="step-info">
            <span className="step-circle">1</span>
            <span className="step-title-text">Standardize Inputs</span>
          </div>
          <div className="step-summary-right">
             <span className="mono-val">d₁ = {results.d1}</span>
             {expanded[1] ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
          </div>
        </div>

        {expanded[1] && (
          <div className="step-content">
            <p className="step-desc">
              We normalize the price and time into standard deviations. <InlineMath math="d_1" /> represents the "moneyness" adjusted for volatility.
            </p>
            
            <div className="latex-box">
              <BlockMath math={`d_1 = \\frac{\\ln(S/K) + (r - q + \\sigma^2/2)T}{\\sigma\\sqrt{T}}`} />
            </div>

            <div className="breakdown-grid">
              <div className="breakdown-item">
                <span className="label">Log Ratio <InlineMath math="\ln(S/K)" /></span>
                <span className="value">{ln_SK}</span>
              </div>
              <div className="breakdown-item">
                <span className="label">Drift Term</span>
                <span className="value">{drift}</span>
              </div>
              <div className="breakdown-item">
                <span className="label">Volatility Term</span>
                <span className="value">{vol_time}</span>
              </div>
            </div>

            <div className="calculation-flow">
               <span className="calc-math">
                 ({ln_SK} + {drift} · {time}) ÷ {vol_time}
               </span>
               <ArrowRight size={16} className="mx-2 text-gray-400" />
               <span className="mono-val text-indigo-600">{results.d1}</span>
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
             <span className="mono-val">N(d₂) = {results.Nd2}</span>
             {expanded[2] ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
          </div>
        </div>

        {expanded[2] && (
          <div className="step-content">
            <p className="step-desc">
              We map the standard deviations to a normal distribution to find the probability of the option finishing In-The-Money.
            </p>

            <div className="distribution-chart" style={{ height: '120px', width: '100%' }}>
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={results.distribution_data}>
                  <defs>
                    <linearGradient id="colorFill" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#4F46E5" stopOpacity={0.3}/>
                      <stop offset="95%" stopColor="#4F46E5" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <XAxis dataKey="x" type="number" domain={[-4, 4]} hide />
                  <YAxis hide />
                  <Tooltip labelFormatter={(v) => `Std Dev: ${v}`} formatter={(v) => v.toFixed(4)} />
                  <Area type="monotone" dataKey="y" stroke="#94a3b8" fill="none" strokeWidth={1} />
                  <Area type="monotone" dataKey="fill" stroke="none" fill="url(#colorFill)" />
                  <ReferenceLine x={isCall ? results.d2 : -results.d2} stroke="#EF4444" strokeDasharray="2 2" label={{ value: 'd2', fill: 'red', fontSize: 10 }}/>
                </AreaChart>
              </ResponsiveContainer>
            </div>
            
            <div className="probability-table">
              <div className="prob-row">
                  <div className="prob-label">
                      <InlineMath math={`N(${isCall ? '' : '-'}d_1)`} />
                      <span className="prob-desc">Asset Delta</span>
                  </div>
                  <div className="prob-val text-green-600">{results.Nd1}</div>
              </div>
              <div className="prob-row">
                  <div className="prob-label">
                      <InlineMath math={`N(${isCall ? '' : '-'}d_2)`} />
                      <span className="prob-desc">Prob. Exercise</span>
                  </div>
                  <div className="prob-val text-blue-600">{results.Nd2}</div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* --- STEP 3: VALUATION (Redesigned) --- */}
      <div className={`step-card ${expanded[3] ? 'open' : ''}`}>
        <div className="step-trigger" onClick={() => toggleStep(3)}>
          <div className="step-info">
            <span className="step-circle">3</span>
            <span className="step-title-text">Valuation</span>
          </div>
          <div className="step-summary-right">
             <span className="text-primary font-bold">${results.price}</span>
             {expanded[3] ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
          </div>
        </div>

        {expanded[3] && (
          <div className="step-content">
            <p className="step-desc">The fair value is the <strong>Expected Asset Value</strong> minus the <strong>Expected Strike Cost</strong>, discounted to today.</p>
            
            <div className="latex-box small-latex">
              {isCall ? (
                <BlockMath math={`C = Se^{-qT}N(d_1) - Ke^{-rT}N(d_2)`} />
              ) : (
                <BlockMath math={`P = Ke^{-rT}N(-d_2) - Se^{-qT}N(-d_1)`} />
              )}
            </div>

            <div className="valuation-receipt">
                {/* LINE 1: POSITIVE FLOW */}
                <div className="receipt-row positive">
                    <div className="receipt-label">
                        <span className="r-title">{isCall ? "Asset Value" : "Strike Value"}</span>
                        <span className="r-sub">
                            {isCall ? `${spot} × ${results.Nd1}` : `${strike} × ${results.Nd2}`}
                        </span>
                    </div>
                    <div className="receipt-value">
                        {isCall ? (spot * results.Nd1).toFixed(2) : (strike * results.Nd2).toFixed(2)}
                    </div>
                </div>

                {/* LINE 2: DISCOUNTING */}
                <div className="receipt-row discount">
                    <div className="receipt-label">
                        <span className="r-sub">Discount Factor (e<sup>{isCall ? '-qT' : '-rT'}</sup>)</span>
                    </div>
                    <div className="receipt-value text-muted">
                         × {isCall ? df_q.toFixed(4) : df_r.toFixed(4)}
                    </div>
                </div>

                <div className="divider"><Minus size={16} className="mx-auto text-gray-300"/></div>

                {/* LINE 3: NEGATIVE FLOW */}
                <div className="receipt-row negative">
                    <div className="receipt-label">
                        <span className="r-title">{isCall ? "Strike Cost" : "Asset Cost"}</span>
                        <span className="r-sub">
                            (Discounted)
                        </span>
                    </div>
                    <div className="receipt-value">
                        - {isCall ? discountedStrike : discountedAsset}
                    </div>
                </div>

                <div className="divider double"></div>

                {/* LINE 4: TOTAL */}
                <div className="receipt-row total">
                    <div className="receipt-label">Fair Price</div>
                    <div className="receipt-value">${results.price}</div>
                </div>
            </div>

          </div>
        )}
      </div>
      
      {/* --- GREEKS (Redesigned) --- */}
      <div className="math-header" style={{marginTop: '24px'}}>
        <h2>Risk Sensitivities</h2>
      </div>

      <div className="greek-grid-modern">
        <div className="greek-card-modern">
            <div className="gc-top">
                <span className="gc-label">Delta</span>
                <TrendingUp size={14} className="text-green-500"/>
            </div>
            <div className="gc-val">{results.greeks.delta}</div>
            <div className="gc-desc">Hedge Ratio ($/$)</div>
        </div>
        <div className="greek-card-modern">
            <div className="gc-top">
                <span className="gc-label">Gamma</span>
                <Activity size={14} className="text-purple-500"/>
            </div>
            <div className="gc-val">{results.greeks.gamma}</div>
            <div className="gc-desc">Convexity (Speed)</div>
        </div>
        <div className="greek-card-modern">
            <div className="gc-top">
                <span className="gc-label">Theta</span>
                <Clock size={14} className="text-orange-500"/>
            </div>
            <div className="gc-val">{results.greeks.theta}</div>
            <div className="gc-desc">Time Decay (Daily)</div>
        </div>
        <div className="greek-card-modern">
            <div className="gc-top">
                <span className="gc-label">Vega</span>
                <Sigma size={14} className="text-red-500"/>
            </div>
            <div className="gc-val">{results.greeks.vega}</div>
            <div className="gc-desc">Vol Sensitivity</div>
        </div>
      </div>

    </div>
  );
};

export default MathWalkthrough;
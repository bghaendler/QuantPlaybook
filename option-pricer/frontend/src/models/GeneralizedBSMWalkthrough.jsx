// --- START OF FILE src/models/GeneralizedBSMWalkthrough.jsx ---

import React, { useState } from 'react';
import { BlockMath, InlineMath } from 'react-katex';
import { ArrowRight, ChevronDown, ChevronUp, Layers, TableProperties, Minus } from 'lucide-react';
import { AreaChart, Area, ResponsiveContainer, ReferenceLine } from 'recharts';
import 'katex/dist/katex.min.css';

import ModelExplanation from '../ModelExplanation';
import { TEXTBOOK_DATA } from '../config/textbookData';

// --- COLOR PALETTE FOR MATH ---
const COLORS = {
  S: "#3b82f6",     // Blue-500
  K: "#ec4899",     // Pink-500
  T: "#f59e0b",     // Amber-500
  r: "#10b981",     // Emerald-500
  b: "#d946ef",     // Fuchsia-500 (The Unifying Parameter)
  sigma: "#8b5cf6", // Violet-500
};

const GeneralizedBSMWalkthrough = ({ inputs, results, showNumbers }) => {
  const [expanded, setExpanded] = useState({ 1: true, 2: false, 3: true, 4: true });

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
  const v = inputs.volatility || 0.2;
  const r = inputs.rate || 0.05;
  const q = inputs.dividend || 0; // Represents the "deduction" from r to get b
  
  const isCall = inputs.type === 'call';

  // The Magic Parameter: Cost of Carry (b)
  const b = r - q;

  // Results
  const { d1, Nd1, Nd2, price } = results;

  // Local Calcs
  const ln_SK = Math.log(S / K);
  const drift = (b + (v * v) / 2) * T;
  const vol_term = v * Math.sqrt(T);
  
  // Discount Factors expressed in terms of b
  const df_asset = Math.exp((b - r) * T);
  const df_cash = Math.exp(-r * T);

  // --- DYNAMIC LATEX GENERATOR ---
  const V = (symbol, value, colorKey) => {
    const color = COLORS[colorKey];
    if (showNumbers) {
       return `\\textcolor{${color}}{${fmt(value, 3)}}`;
    }
    return `\\textcolor{${color}}{${symbol}}`;
  };

  // Dynamic Formulas
  // d1 = (ln(S/K) + (b + sigma^2/2)T) / (sigma * sqrt(T))
  const d1_num = `\\ln(${V('S', S, 'S')} / ${V('K', K, 'K')}) + (${V('b', b, 'b')} + ${V('\\sigma', v, 'sigma')}^2/2)${V('T', T, 'T')}`;
  const d1_den = `${V('\\sigma', v, 'sigma')}\\sqrt{${V('T', T, 'T')}}`;
  
  // c = S e^{(b-r)T} N(d1) - K e^{-rT} N(d2)
  const call_eq = `${V('S', S, 'S')} e^{(${V('b', b, 'b')}-${V('r', r, 'r')})${V('T', T, 'T')}} N(d_1) - ${V('K', K, 'K')} e^{-${V('r', r, 'r')}${V('T', T, 'T')}} N(d_2)`;
  // p = K e^{-rT} N(-d2) - S e^{(b-r)T} N(-d1)
  const put_eq = `${V('K', K, 'K')} e^{-${V('r', r, 'r')}${V('T', T, 'T')}} N(-d_2) - ${V('S', S, 'S')} e^{(${V('b', b, 'b')}-${V('r', r, 'r')})${V('T', T, 'T')}} N(-d_1)`;

  return (
    <div className="math-steps">
      
      {/* --- STEP 1: COST OF CARRY (b) --- */}
      <div className={`step-card ${expanded[1] ? 'open' : ''}`}>
        <div className="step-trigger" onClick={() => toggleStep(1)}>
          <div className="step-info">
            <span className="step-circle">1</span>
            <span className="step-title-text">Cost of Carry (b)</span>
          </div>
          <div className="step-summary-right">
            <span className="mono-val">b = {fmt(b, 3)}</span>
            {expanded[1] ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
          </div>
        </div>

        {expanded[1] && (
          <div className="step-content">
            <div className="p-3 mb-3 bg-fuchsia-50 border border-fuchsia-100 rounded text-sm text-fuchsia-900">
              <div className="flex items-start gap-2 mb-2">
                <Layers size={16} className="mt-0.5 shrink-0" />
                <strong>The Unifying Parameter:</strong>
              </div>
              <p>
                The Generalized BSM model defines the cost of carry rate as <InlineMath math="b = r - q" />.
                By changing <InlineMath math="b" />, this single formula generates all other models.
              </p>
            </div>

            <div className="overflow-x-auto mb-3 border rounded-lg">
                <table className="w-full text-xs text-left">
                    <thead className="bg-gray-100 font-semibold text-gray-600 border-b">
                        <tr>
                            <th className="p-2">Model</th>
                            <th className="p-2">Asset Type</th>
                            <th className="p-2">Cost of Carry (b)</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y text-gray-700">
                        <tr className={q === 0 ? "bg-fuchsia-100 font-medium" : ""}>
                            <td className="p-2">Black-Scholes</td>
                            <td className="p-2">Non-div Stock</td>
                            <td className="p-2"><InlineMath math="b = r" /></td>
                        </tr>
                        <tr className={q > 0 && q !== r ? "bg-fuchsia-100 font-medium" : ""}>
                            <td className="p-2">Merton</td>
                            <td className="p-2">Dividend Stock</td>
                            <td className="p-2"><InlineMath math="b = r - q" /></td>
                        </tr>
                        <tr className={Math.abs(b) < 0.001 ? "bg-fuchsia-100 font-medium" : ""}>
                            <td className="p-2">Black-76</td>
                            <td className="p-2">Futures</td>
                            <td className="p-2"><InlineMath math="b = 0" /></td>
                        </tr>
                        <tr>
                            <td className="p-2">Garman-Kohlhagen</td>
                            <td className="p-2">Currency</td>
                            <td className="p-2"><InlineMath math="b = r - r_f" /></td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <div className="calculation-flow justify-center">
               <span className="text-gray-500 mr-2">Calculation:</span>
               <InlineMath math={`b = r - q = ${r} - ${q} = `} />
               <span className="mono-val font-bold ml-2 text-fuchsia-600">{fmt(b, 4)}</span>
            </div>
          </div>
        )}
      </div>

      {/* --- STEP 2: GENERALIZED D1 --- */}
      <div className={`step-card ${expanded[2] ? 'open' : ''}`}>
        <div className="step-trigger" onClick={() => toggleStep(2)}>
          <div className="step-info">
            <span className="step-circle">2</span>
            <span className="step-title-text">Standardize Inputs (d₁)</span>
          </div>
          <div className="step-summary-right">
            <span className="mono-val">d₁ = {fmt(d1)}</span>
            {expanded[2] ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
          </div>
        </div>

        {expanded[2] && (
          <div className="step-content">
            <div className="latex-box transition-all duration-300">
              <BlockMath math={`d_1 = \\frac{${d1_num}}{${d1_den}}`} />
            </div>

            <div className="breakdown-grid">
              <div className="breakdown-item border-l-4" style={{borderLeftColor: COLORS.S}}>
                <span className="label">Moneyness</span>
                <span className="value" style={{color: COLORS.S}}>{fmt(ln_SK)}</span>
              </div>
              <div className="breakdown-item border-l-4" style={{borderLeftColor: COLORS.b}}>
                <span className="label">Carry Drift (b)</span>
                <span className="value" style={{color: COLORS.b}}>{fmt(b, 3)}</span>
              </div>
              <div className="breakdown-item border-l-4" style={{borderLeftColor: COLORS.sigma}}>
                <span className="label">Vol Term</span>
                <span className="value" style={{color: COLORS.sigma}}>{fmt(vol_term)}</span>
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
            <span className="text-primary font-bold text-lg">${fmt(price, 4)}</span>
            {expanded[3] ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
          </div>
        </div>

        {expanded[3] && (
          <div className="step-content">
            <div className="latex-box small-latex mb-3">
              <BlockMath math={isCall ? `c = ${call_eq}` : `p = ${put_eq}`} />
            </div>

            <div className="valuation-receipt">
              {/* Positive Flow */}
              <div className="receipt-row positive">
                <div className="receipt-label">
                  <span className="r-title" style={{color: COLORS.S}}>{isCall ? "Asset Inflow" : "Strike Inflow"}</span>
                  <span className="r-sub">
                    {isCall ? <span>Discounts at <InlineMath math="b-r" /></span> : <span>Discounts at <InlineMath math="r" /></span>}
                  </span>
                </div>
                <div className="receipt-value" style={{color: COLORS.S}}>
                   {isCall ? fmt(S * df_asset * Nd1, 4) : fmt(K * df_cash * (1 - Nd2), 4)}
                </div>
              </div>

              <div className="receipt-divider"><Minus size={14} /></div>

              {/* Negative Flow */}
              <div className="receipt-row negative">
                <div className="receipt-label">
                  <span className="r-title" style={{color: COLORS.K}}>{isCall ? "Strike Cost" : "Asset Outflow"}</span>
                  <span className="r-sub">
                     {isCall ? <span>Discounts at <InlineMath math="r" /></span> : <span>Discounts at <InlineMath math="b-r" /></span>}
                  </span>
                </div>
                <div className="receipt-value" style={{color: COLORS.K}}>
                    {isCall ? fmt(K * df_cash * Nd2, 4) : fmt(S * df_asset * (1 - Nd1), 4)}
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

      {/* Textbook Explanation */}
      <ModelExplanation data={TEXTBOOK_DATA.gen_bsm} />

    </div>
  );
};

export default GeneralizedBSMWalkthrough;
import React, { useState } from 'react';
import { BlockMath, InlineMath } from 'react-katex';
import { ChevronDown, ChevronUp, UserMinus, Briefcase, TrendingDown } from 'lucide-react';
import 'katex/dist/katex.min.css';
import ModelExplanation from '../ModelExplanation';
import { TEXTBOOK_DATA } from '../config/textbookData';

// --- COLOR PALETTE ---
const COLORS = {
    S: "#3b82f6",     // Blue
    K: "#ec4899",     // Pink
    lambda: "#ef4444", // Red (Exit Rate)
    prob: "#10b981",   // Emerald (Survival Prob)
    bsm: "#64748b",    // Slate (Base Value)
    exec: "#8b5cf6",   // Violet (Final Value)
};

const ExecutiveStockOptionWalkthrough = ({ inputs, results, showNumbers }) => {
    const [expanded, setExpanded] = useState({ 1: true, 2: true, 3: true });

    const toggleStep = (step) => setExpanded(prev => ({ ...prev, [step]: !prev[step] }));

    const fmt = (num, digits = 4) => {
        if (num === undefined || num === null || isNaN(num)) return "-";
        return parseFloat(num.toFixed(digits));
    };

    // Inputs
    const S = inputs.spot || 60;
    const K = inputs.strike || 64;
    const T = inputs.time || 2;
    const r = inputs.rate || 0.07;
    const q = inputs.dividend || 0.03;
    const v = inputs.volatility || 0.38;
    const lamb = inputs.lambda || 0.15; // Exit rate

    const price = results?.price || 0;

    // Derived values
    const b = r - q;
    const survival_prob = Math.exp(-lamb * T);

    // Reverse engineer BSM price from final price (or calculate locally)
    const bsm_price = price / survival_prob;
    const lost_value = bsm_price - price;

    // --- DYNAMIC LATEX GENERATOR ---
    const V = (symbol, value, colorKey) => {
        const color = COLORS[colorKey] || "#374151";
        if (showNumbers) return `\\textcolor{${color}}{${fmt(value, 4)}}`;
        return `\\textcolor{${color}}{${symbol}}`;
    };

    return (
        <div className="math-steps">
            {/* INFO BANNER */}
            <div className="info-banner mb-4 p-3 bg-indigo-50 border border-indigo-200 rounded-lg">
                <div className="flex items-start gap-2">
                    <Briefcase size={18} className="text-indigo-600 mt-0.5 flex-shrink-0" />
                    <div className="text-xs text-indigo-900">
                        <strong>Jennergren & Näslund (1993):</strong> Executive stock options are forfeited if the employee leaves.
                        This model discounts the standard Black-Scholes value by the probability of the executive remaining at the firm.
                    </div>
                </div>
            </div>

            {/* --- STEP 1: SURVIVAL PROBABILITY --- */}
            <div className={`step-card ${expanded[1] ? 'open' : ''}`}>
                <div className="step-trigger" onClick={() => toggleStep(1)}>
                    <div className="step-info">
                        <span className="step-circle">1</span>
                        <span className="step-title-text">Probability of Vesting</span>
                    </div>
                    <div className="step-summary-right">
                        <span className="mono-val" style={{ color: COLORS.prob }}>{fmt(survival_prob * 100, 1)}%</span>
                        {expanded[1] ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                    </div>
                </div>
                {expanded[1] && (
                    <div className="step-content">
                        <p className="step-desc text-xs text-muted mb-3">
                            Calculate the probability that the executive stays with the company for the full duration <InlineMath math="T" />, given an exit rate <InlineMath math="\lambda" />.
                        </p>
                        <div className="latex-box transition-all duration-300 mb-3">
                            <BlockMath math={`P_{stay} = e^{-\\lambda T} = e^{-${fmt(lamb, 2)} \\times ${fmt(T, 1)}} = ${fmt(survival_prob, 4)}`} />
                        </div>
                        <div className="flex items-center gap-2 p-2 bg-red-50 text-red-800 rounded text-xs border border-red-100">
                            <UserMinus size={14} />
                            <span>Risk of Forfeiture: <strong>{fmt((1 - survival_prob) * 100, 1)}%</strong> chance option is lost.</span>
                        </div>
                    </div>
                )}
            </div>

            {/* --- STEP 2: STANDARD BSM VALUE --- */}
            <div className={`step-card ${expanded[2] ? 'open' : ''}`}>
                <div className="step-trigger" onClick={() => toggleStep(2)}>
                    <div className="step-info">
                        <span className="step-circle">2</span>
                        <span className="step-title-text">Standard Black-Scholes Value</span>
                    </div>
                    <div className="step-summary-right">
                        <span className="mono-val" style={{ color: COLORS.bsm }}>${fmt(bsm_price, 2)}</span>
                        {expanded[2] ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                    </div>
                </div>
                {expanded[2] && (
                    <div className="step-content">
                        <p className="step-desc text-xs text-muted mb-3">
                            Value of the option assuming it is fully transferable and never forfeited (standard European Call).
                        </p>
                        <div className="latex-box small-latex mb-3">
                            <BlockMath math={`C_{BSM} = S e^{(b-r)T} N(d_1) - K e^{-rT} N(d_2)`} />
                        </div>
                        <div className="text-center">
                            <span className="text-sm font-mono font-bold text-slate-600">${fmt(bsm_price, 4)}</span>
                        </div>
                    </div>
                )}
            </div>

            {/* --- STEP 3: FINAL VALUATION --- */}
            <div className={`step-card ${expanded[3] ? 'open' : ''}`}>
                <div className="step-trigger" onClick={() => toggleStep(3)}>
                    <div className="step-info">
                        <span className="step-circle">3</span>
                        <span className="step-title-text">Executive Option Value</span>
                    </div>
                    <div className="step-summary-right">
                        <span className="text-primary font-bold text-lg">${fmt(price, 2)}</span>
                        {expanded[3] ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                    </div>
                </div>
                {expanded[3] && (
                    <div className="step-content">
                        <p className="step-desc text-xs text-muted mb-3">
                            Apply the survival factor to the standard BSM price.
                        </p>
                        <div className="latex-box transition-all duration-300 mb-3">
                            <BlockMath math={`C_{exec} = C_{BSM} \\times e^{-\\lambda T}`} />
                        </div>

                        <div className="valuation-receipt">
                            <div className="receipt-row">
                                <div className="receipt-label">Standard BSM Value</div>
                                <div className="receipt-value text-slate-500">${fmt(bsm_price, 4)}</div>
                            </div>
                            <div className="receipt-row">
                                <div className="receipt-label">x Survival Probability</div>
                                <div className="receipt-value text-emerald-600">{fmt(survival_prob, 4)}</div>
                            </div>
                            <div className="receipt-total-line"></div>
                            <div className="receipt-row total">
                                <div className="receipt-label">Executive Value</div>
                                <div className="receipt-value text-violet-600">${fmt(price, 4)}</div>
                            </div>
                        </div>

                        <div className="mt-3 p-2 bg-slate-100 rounded text-xs text-slate-600 flex justify-between items-center">
                            <span>Value Haircut due to Exit Risk:</span>
                            <span className="font-bold text-red-500">-${fmt(lost_value, 2)} ({fmt((1 - survival_prob) * 100, 1)}%)</span>
                        </div>
                    </div>
                )}
            </div>

            <ModelExplanation data={TEXTBOOK_DATA.exec_stock} />
        </div>
    );
};

export default ExecutiveStockOptionWalkthrough;
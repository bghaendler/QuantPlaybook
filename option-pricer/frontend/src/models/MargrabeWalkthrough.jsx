import React, { useState } from 'react';
import { BlockMath, InlineMath } from 'react-katex';
import { ChevronDown, ChevronUp } from 'lucide-react';
import 'katex/dist/katex.min.css';
import ModelExplanation from '../ModelExplanation';

const COLORS = {
    S1: "#3b82f6",     // Blue-500
    S2: "#ec4899",     // Pink-500
    T: "#f59e0b",     // Amber-500
    sigma_hat: "#8b5cf6", // Violet-500
    r: "#10b981",     // Emerald-500
};

const MargrabeWalkthrough = ({ inputs, results, showNumbers }) => {
    const [expanded, setExpanded] = useState({ 1: true, 2: true, 3: true });

    const toggleStep = (step) => setExpanded(prev => ({ ...prev, [step]: !prev[step] }));

    const fmt = (num, digits = 4) => {
        if (num === undefined || num === null || isNaN(num)) return "-";
        return parseFloat(num.toFixed(digits));
    };

    // Inputs
    const S1 = inputs.spot || 101;
    const v1 = inputs.volatility || 0.18;
    const b1 = inputs.dividend || 0.02; // Asset 1 Carry
    const S2 = inputs.spot2 || 104;
    const v2 = inputs.vol2 || 0.12;
    const b2 = inputs.dividend2 || 0.04; // Asset 2 Carry
    const q1 = inputs.q1 || 1.0;
    const q2 = inputs.q2 || 1.0;
    const rho = inputs.correlation || 0.8;
    const r = inputs.rate || 0.10;
    const T = inputs.time || 0.5;
    const isCall = inputs.type === 'call';

    // Results
    const price = results?.price || 0;
    const d1 = results?.d1 || 0;
    const d2 = results?.d2 || 0;

    // Derived values for display
    const sigma_hat = Math.sqrt(v1 * v1 + v2 * v2 - 2 * rho * v1 * v2);

    const V = (symbol, value, colorKey) => {
        const color = COLORS[colorKey];
        if (showNumbers) {
            return `\\textcolor{${color}}{${fmt(value, 3)}}`;
        }
        return `\\textcolor{${color}}{${symbol}}`;
    };

    const sigma_formula = `\\sqrt{${V('\\sigma_1', v1, 'S1')}^2 + ${V('\\sigma_2', v2, 'S2')}^2 - 2${V('\\rho', rho, 'sigma_hat')}${V('\\sigma_1', v1, 'S1')}${V('\\sigma_2', v2, 'S2')}}`;
    const d1_formula = `\\frac{\\ln((${V('Q_1', q1, 'S1')}${V('S_1', S1, 'S1')})/(${V('Q_2', q2, 'S2')}${V('S_2', S2, 'S2')})) + (${V('b_1', b1, 'S1')} - ${V('b_2', b2, 'S2')} + ${V('\\hat{\\sigma}', sigma_hat, 'sigma_hat')}^2/2)${V('T', T, 'T')}}{${V('\\hat{\\sigma}', sigma_hat, 'sigma_hat')}\\sqrt{${V('T', T, 'T')}}}`;

    return (
        <div className="math-steps">
            {/* INFO BANNER */}
            <div className="info-banner mb-4 p-3 bg-blue-50 border border-blue-200 rounded-lg text-slate-800">
                <div className="flex items-start gap-2">
                    <div className="text-xs">
                        <strong>Margrabe Model (1978):</strong> European-style option to exchange one risky asset for another.
                        Payoff is defined as: <InlineMath math="\max(Q_1 S_1 - Q_2 S_2, 0)" /> (for Call) or <InlineMath math="\max(Q_2 S_2 - Q_1 S_1, 0)" /> (for Put).
                    </div>
                </div>
            </div>

            {/* --- STEP 1: COMBINED VOLATILITY --- */}
            <div className={`step-card ${expanded[1] ? 'open' : ''}`}>
                <div className="step-trigger" onClick={() => toggleStep(1)}>
                    <div className="step-info">
                        <span className="step-circle">1</span>
                        <span className="step-title-text text-slate-750 font-semibold">Combined Volatility (σ̂)</span>
                    </div>
                    <div className="step-summary-right">
                        <span className="mono-val font-semibold">σ̂ = {fmt(sigma_hat)}</span>
                        {expanded[1] ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                    </div>
                </div>
                {expanded[1] && (
                    <div className="step-content">
                        <div className="latex-box transition-all duration-300 mb-3 bg-white p-3 rounded shadow-sm border border-slate-100">
                            <BlockMath math={`\\hat{\\sigma} = ${sigma_formula} = ${fmt(sigma_hat, 4)}`} />
                        </div>
                    </div>
                )}
            </div>

            {/* --- STEP 2: STANDARDIZE INPUTS --- */}
            <div className={`step-card ${expanded[2] ? 'open' : ''}`}>
                <div className="step-trigger" onClick={() => toggleStep(2)}>
                    <div className="step-info">
                        <span className="step-circle">2</span>
                        <span className="step-title-text text-slate-750 font-semibold">Standardize Inputs (d₁, d₂)</span>
                    </div>
                    <div className="step-summary-right">
                        <span className="mono-val font-semibold">d₁ = {fmt(d1)}</span>
                        {expanded[2] ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                    </div>
                </div>
                {expanded[2] && (
                    <div className="step-content">
                        <div className="latex-box transition-all duration-300 mb-3 bg-white p-3 rounded shadow-sm border border-slate-100">
                            <BlockMath math={`d_1 = ${d1_formula} = ${fmt(d1, 4)}`} />
                        </div>
                        <div className="latex-box transition-all duration-300 mb-3 bg-white p-3 rounded shadow-sm border border-slate-100">
                            <BlockMath math={`d_2 = d_1 - ${V('\\hat{\\sigma}', sigma_hat, 'sigma_hat')}\\sqrt{${V('T', T, 'T')}} = ${fmt(d2, 4)}`} />
                        </div>
                    </div>
                )}
            </div>

            {/* --- STEP 3: VALUATION --- */}
            <div className={`step-card ${expanded[3] ? 'open' : ''}`}>
                <div className="step-trigger" onClick={() => toggleStep(3)}>
                    <div className="step-info">
                        <span className="step-circle">3</span>
                        <span className="step-title-text text-slate-750 font-semibold">Valuation Formula</span>
                    </div>
                    <div className="step-summary-right flex items-center gap-2">
                        <span className="text-indigo-600 font-bold text-lg">{fmt(price, 4)}</span>
                        {expanded[3] ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                    </div>
                </div>
                {expanded[3] && (
                    <div className="step-content">
                        <div className="latex-box small-latex mb-3 bg-white p-3 rounded shadow-sm border border-slate-100">
                            {isCall ? (
                                <BlockMath math={`c_{Exchange} = Q_1 S_1 e^{(b_1-r)T} N(d_1) - Q_2 S_2 e^{(b_2-r)T} N(d_2)`} />
                            ) : (
                                <BlockMath math={`p_{Exchange} = Q_2 S_2 e^{(b_2-r)T} N(-d_2) - Q_1 S_1 e^{(b_1-r)T} N(-d_1)`} />
                            )}
                        </div>
                        <div className="valuation-receipt">
                            <div className="receipt-row total">
                                <div className="receipt-label text-slate-600 font-medium">Calculated Option Value</div>
                                <div className="receipt-value text-indigo-600 font-bold">{fmt(price, 6)}</div>
                            </div>
                        </div>
                    </div>
                )}
            </div>

            {/* --- EXPLANATION DATA --- */}
            <ModelExplanation data={{
                source: "William Margrabe (1978)",
                concept: [
                    "Valuates European options to exchange asset 2 for asset 1.",
                    "Payoff equates to the differential price at option expiration.",
                    "Highly applicable in firm takeovers, delivery choices embedded in futures, and currency switches."
                ],
                formulas: [
                    { label: "Call Price", math: "c = Q_1 S_1 e^{(b_1-r)T} N(d_1) - Q_2 S_2 e^{(b_2-r)T} N(d_2)" },
                    { label: "Put Price", math: "p = Q_2 S_2 e^{(b_2-r)T} N(-d_2) - Q_1 S_1 e^{(b_1-r)T} N(-d_1)" }
                ],
                where: [
                    "d_1 = \\frac{\\ln(Q_1 S_1 / (Q_2 S_2)) + (b_1 - b_2 + \\hat{\\sigma}^2/2)T}{\\hat{\\sigma}\\sqrt{T}}",
                    "\\hat{\\sigma} = \\sqrt{\\sigma_1^2 + \\sigma_2^2 - 2\\rho\\sigma_1\\sigma_2}"
                ],
                notation: [
                    { symbol: "S_1, S_2", def: "Spot prices of Asset 1 and Asset 2" },
                    { symbol: "\\sigma_1, \\sigma_2", def: "Asset Volatilities" },
                    { symbol: "b_1, b_2", def: "Cost of carry rates" },
                    { symbol: "\\rho", def: "Correlation between assets" }
                ],
                contextText: "Designed for exchange privileges and options involving multiple risky underlying assets.",
                examplePage: "Margrabe 1978",
                example: {
                    inputs: [
                        { label: "Asset 1 Spot", sym: "S1", val: "101" },
                        { label: "Asset 2 Spot", sym: "S2", val: "104" },
                        { label: "Correlation", sym: "\\rho", val: "0.8" },
                        { label: "Time", sym: "T", val: "0.5" }
                    ],
                    calcs: [
                        { sym: "\\hat{\\sigma}", val: "0.1106" },
                        { sym: "d_1", val: "-0.4629" },
                        { sym: "d_2", val: "-0.5411" }
                    ],
                    result: "1.5260"
                }
            }} />
        </div>
    );
};

export default MargrabeWalkthrough;

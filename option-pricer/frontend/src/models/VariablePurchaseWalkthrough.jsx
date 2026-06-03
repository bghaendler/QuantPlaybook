import React, { useState } from 'react';
import { BlockMath, InlineMath } from 'react-katex';
import { ChevronDown, ChevronUp } from 'lucide-react';
import 'katex/dist/katex.min.css';
import ModelExplanation from '../ModelExplanation';

// --- COLOR PALETTE ---
const COLORS = {
    S: "#3b82f6",     // Blue-500
    K: "#ec4899",     // Pink-500
    T: "#f59e0b",     // Amber-500
    r: "#10b981",     // Emerald-500
    sigma: "#8b5cf6", // Violet-500
};

const VariablePurchaseWalkthrough = ({ inputs, results, showNumbers }) => {
    const [expanded, setExpanded] = useState({ 1: true, 2: true, 3: true });

    const toggleStep = (step) => setExpanded(prev => ({ ...prev, [step]: !prev[step] }));

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
    const q = inputs.dividend || 0;
    const isCall = inputs.type === 'call';

    // Results
    const price = results?.price || 0;

    // Derived values for display
    const b = r - q; // Cost of carry
    const d1 = (Math.log(S / K) + (b + 0.5 * v * v) * T) / (v * Math.sqrt(T));
    const d2 = d1 - v * Math.sqrt(T);

    // --- DYNAMIC LATEX GENERATOR ---
    const V = (symbol, value, colorKey) => {
        const color = COLORS[colorKey];
        if (showNumbers) {
            return `\\textcolor{${color}}{${fmt(value, 3)}}`;
        }
        return `\\textcolor{${color}}{${symbol}}`;
    };

    const d1_formula = `\\frac{\\ln(${V('S', S, 'S')}/${V('K', K, 'K')}) + (${V('r', r, 'r')} - ${V('q', q, 'r')} + ${V('\\sigma', v, 'sigma')}^2/2)${V('T', T, 'T')}}{${V('\\sigma', v, 'sigma')}\\sqrt{${V('T', T, 'T')}}}`;

    return (
        <div className="math-steps">

            {/* INFO BANNER */}
            <div className="info-banner mb-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
                <div className="flex items-start gap-2">
                    <div className="text-xs text-blue-900">
                        <strong>Variable Purchase (Handley 1992):</strong> A generalized framework for path-independent options.
                        For standard inputs, it reduces to the Black-Scholes-Merton formula shown below.
                    </div>
                </div>
            </div>

            {/* --- STEP 1: STANDARDIZATION --- */}
            <div className={`step-card ${expanded[1] ? 'open' : ''}`}>
                <div className="step-trigger" onClick={() => toggleStep(1)}>
                    <div className="step-info">
                        <span className="step-circle">1</span>
                        <span className="step-title-text">Standardize Inputs ($d_1$)</span>
                    </div>
                    <div className="step-summary-right">
                        <span className="mono-val">d₁ = {fmt(d1)}</span>
                        {expanded[1] ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                    </div>
                </div>
                {expanded[1] && (
                    <div className="step-content">
                        <div className="latex-box transition-all duration-300 mb-3">
                            <BlockMath math={`d_1 = ${d1_formula} = ${fmt(d1, 4)}`} />
                        </div>
                        <div className="latex-box transition-all duration-300 mb-3">
                            <BlockMath math={`d_2 = d_1 - ${V('\\sigma', v, 'sigma')}\\sqrt{${V('T', T, 'T')}} = ${fmt(d2, 4)}`} />
                        </div>
                    </div>
                )}
            </div>

            {/* --- STEP 2: VALUATION --- */}
            <div className={`step-card ${expanded[2] ? 'open' : ''}`}>
                <div className="step-trigger" onClick={() => toggleStep(2)}>
                    <div className="step-info">
                        <span className="step-circle">2</span>
                        <span className="step-title-text">Valuation Formula</span>
                    </div>
                    <div className="step-summary-right">
                        <span className="text-primary font-bold text-lg">${fmt(price, 2)}</span>
                        {expanded[2] ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                    </div>
                </div>
                {expanded[2] && (
                    <div className="step-content">
                        <div className="latex-box small-latex mb-3">
                            {isCall ? (
                                <BlockMath math={`c = Se^{-qT}N(d_1) - Ke^{-rT}N(d_2)`} />
                            ) : (
                                <BlockMath math={`p = Ke^{-rT}N(-d_2) - Se^{-qT}N(-d_1)`} />
                            )}
                        </div>
                        <div className="valuation-receipt">
                            <div className="receipt-row total">
                                <div className="receipt-label">Calculated Price</div>
                                <div className="receipt-value">${fmt(price, 4)}</div>
                            </div>
                        </div>
                    </div>
                )}
            </div>

            {/* --- EXPLANATION DATA --- */}
            <ModelExplanation data={{
                source: "Handley (1992)",
                concept: [
                    "Handley generalized the pricing of options where the number of shares purchased can vary.",
                    "The model is a general case that encompasses standard European options, power options, and others.",
                    "With standard parameters (n=1), it is identical to Black-Scholes-Merton."
                ],
                formulas: [
                    { label: "General Form", math: "V = S^n e^{((n-1)(r + \\frac{n\\sigma^2}{2}) - q)T} N(d_1) - K e^{-rT} N(d_2)" },
                    { label: "Standard Case (n=1)", math: "V = S e^{-qT} N(d_1) - K e^{-rT} N(d_2)" }
                ],
                where: [
                    "n = \\text{Power parameter (set to 1 for standard options)}",
                    "b = r - q \\text{ (Cost of Carry)}"
                ],
                notation: [
                    { symbol: "S", def: "Spot Price" },
                    { symbol: "K", def: "Strike Price" },
                    { symbol: "n", def: "Quantity/Power Parameter" }
                ],
                contextText: "Used for 'Variable Purchase' contracts where the payoff depends on a power of the asset price.",
                examplePage: "Handley Paper",
                example: {
                    inputs: [
                        { label: "Spot", sym: "S", val: "100" },
                        { label: "Strike", sym: "K", val: "100" },
                        { label: "Time", sym: "T", val: "1.0" },
                        { label: "Rate", sym: "r", val: "5%" },
                        { label: "Vol", sym: "\\sigma", val: "20%" }
                    ],
                    calcs: [
                        { sym: "d_1", val: "0.35" },
                        { sym: "N(d_1)", val: "0.6368" }
                    ],
                    result: "10.4506"
                }
            }} />
        </div>
    );
};

export default VariablePurchaseWalkthrough;
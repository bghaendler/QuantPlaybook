
import React, { useState } from 'react';
import { BlockMath } from 'react-katex';
import { ArrowRight, ChevronDown, ChevronUp, Infinity, Calculator, TrendingUp, Award } from 'lucide-react';
import 'katex/dist/katex.min.css';
import ModelExplanation from '../ModelExplanation';

// --- COLOR PALETTE ---
const COLORS = {
    S: "#3b82f6",     // Blue
    K: "#ec4899",     // Pink
    y: "#8b5cf6",     // Violet (Gamma/Power)
    S_star: "#10b981", // Emerald (Optimal Boundary)
    val: "#f59e0b",   // Amber (Value)
};

const McKeanWalkthrough = ({ inputs, results, showNumbers, highlightedVar, onHighlight }) => {
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
    const r = inputs.rate || 0.05;
    const q = inputs.dividend || 0.03;
    const v = inputs.volatility || 0.30;
    const type = inputs.type || 'call';
    const isCall = type === 'call';

    const b = r - q;
    const sigma2 = v * v;

    // Step 1: Calculate Gamma (y1 or y2)
    // Formula: (b/sigma^2 - 0.5)^2 + 2r/sigma^2
    const term = Math.pow(b / sigma2 - 0.5, 2) + 2 * r / sigma2;
    const sqrt_term = Math.sqrt(term);

    // y1 for call, y2 for put
    const y1 = 0.5 - b / sigma2 + sqrt_term;
    const y2 = 0.5 - b / sigma2 - sqrt_term;

    const y = isCall ? y1 : y2;
    const yLabel = isCall ? "y_1" : "y_2";

    // Step 2: Optimal Exercise Boundary S*
    // Call: K * y1 / (y1 - 1)
    // Put: K * y2 / (y2 - 1) (valid since y2 < 0 generally)

    let S_star = 0;
    let isValid = true;

    if (isCall) {
        if (y1 <= 1) isValid = false;
        else S_star = K * y1 / (y1 - 1);
    } else {
        S_star = K * y2 / (y2 - 1);
    }

    // Step 3: Valuation
    let price = results.price;
    // Local check
    // Formula: (S* - K) * (S/S*)^y
    if (isValid) {
        if (isCall) {
            if (S >= S_star) price = S - K;
            // else price determined by backend
        } else {
            if (S <= S_star) price = K - S;
        }
    }

    // --- DYNAMIC LATEX GENERATOR ---
    const V = (symbol, value, colorKey) => {
        const color = COLORS[colorKey] || "#374151";
        const varMap = {
            'spot': 'S', 'strike': 'K', 'rate': 'r', 'volatility': 'sigma', 'dividend': 'q'
        };
        const isHighlighted = highlightedVar && varMap[highlightedVar] === colorKey;
        const content = showNumbers ? fmt(value, 3) : symbol;
        const coloredContent = `\\textcolor{${color}}{${content}}`;
        return isHighlighted ? `\\mathbf{${coloredContent}}` : coloredContent;
    };

    return (
        <div className="math-steps">
            {/* INFO BANNER */}
            <div className="info-banner mb-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
                <div className="flex items-start gap-2">
                    <Infinity size={18} className="text-blue-600 mt-0.5 flex-shrink-0" />
                    <div className="text-xs text-blue-900">
                        <strong>Perpetual Option:</strong> An American option with no expiration date ($T = \infty$).
                        The value depends purely on the asset price relative to an optimal exercise barrier $S^*$.
                    </div>
                </div>
            </div>

            {!isValid && (
                <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-xs text-red-900">
                    ⚠️ <strong>Never Optimal to Exercise:</strong> Since cost-of-carry $b \ge r$, the optimal strategy is to hold the call forever. Value = Spot?
                </div>
            )}

            {/* --- STEP 1: GAMMA FACTOR --- */}
            <div className={`step-card ${expanded[1] ? 'open' : ''}`}>
                <div className="step-trigger" onClick={() => toggleStep(1)}>
                    <div className="step-info">
                        <span className="step-circle">1</span>
                        <span className="step-title-text">Calculate Characteristic Root ({yLabel})</span>
                    </div>
                    <div className="step-summary-right">
                        <span className="mono-val" style={{ color: COLORS.y }}>{yLabel} = {fmt(y, 3)}</span>
                        {expanded[1] ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                    </div>
                </div>
                {expanded[1] && (
                    <div className="step-content">
                        <p className="step-desc text-xs text-muted mb-4">
                            First, we solve the fundamental quadratic equation derived from the differential equation when time is removed. This gives us the elasticity factor.
                        </p>
                        <div className="latex-box transition-all duration-300 mb-3">
                            <BlockMath math={`${yLabel} = \\frac{1}{2} - \\frac{b}{\\sigma^2} \\pm \\sqrt{\\left(\\frac{b}{\\sigma^2} - \\frac{1}{2}\\right)^2 + \\frac{2r}{\\sigma^2}} = ${fmt(y, 4)}`} />
                        </div>
                    </div>
                )}
            </div>

            {/* --- STEP 2: OPTIMAL EXERCISE BOUNDARY --- */}
            <div className={`step-card ${expanded[2] ? 'open' : ''}`}>
                <div className="step-trigger" onClick={() => toggleStep(2)}>
                    <div className="step-info">
                        <span className="step-circle">2</span>
                        <span className="step-title-text">Optimal Exercise Price ($S^*$)</span>
                    </div>
                    <div className="step-summary-right">
                        <span className="mono-val" style={{ color: COLORS.S_star }}>S* = {fmt(S_star, 2)}</span>
                        {expanded[2] ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                    </div>
                </div>
                {expanded[2] && (
                    <div className="step-content">
                        <p className="step-desc text-xs text-muted mb-4">
                            Since time is infinite, the optimal strategy is simply a <strong>barrier</strong>. If the price ever hits this level, you exercise immediately.
                        </p>
                        <div className="latex-box transition-all duration-300 mb-3">
                            <BlockMath math={`S^* = ${V('K', K, 'K')} \\cdot \\frac{${V(yLabel, y, 'y')}}{${V(yLabel, y, 'y')} - 1} = ${fmt(S_star, 2)}`} />
                        </div>
                        <div className="mt-2 text-xs text-center text-slate-500">
                            {isCall ?
                                (S >= S_star ? "🚀 Current Spot is ABOVE barrier! Exercise Now." : "Current Spot is below barrier. Wait.") :
                                (S <= S_star ? "🚀 Current Spot is BELOW barrier! Exercise Now." : "Current Spot is above barrier. Wait.")
                            }
                        </div>
                    </div>
                )}
            </div>

            {/* --- STEP 3: VALUATION --- */}
            <div className={`step-card ${expanded[3] ? 'open' : ''}`}>
                <div className="step-trigger" onClick={() => toggleStep(3)}>
                    <div className="step-info">
                        <span className="step-circle">3</span>
                        <span className="step-title-text">Perpetual Value</span>
                    </div>
                    <div className="step-summary-right">
                        <span className="text-primary font-bold text-lg">${fmt(price, 2)}</span>
                        {expanded[3] ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                    </div>
                </div>
                {expanded[3] && (
                    <div className="step-content">
                        <p className="step-desc text-xs text-muted mb-4">
                            The value is the payoff at the barrier, discounted by the probability (power law) of reaching that barrier from the current spot.
                        </p>
                        <div className="latex-box small-latex mb-3">
                            <BlockMath math={`V = (S^* - K) \\left(\\frac{S}{S^*}\\right)^{${yLabel}}`} />
                        </div>

                        <div className="valuation-receipt">
                            <div className="receipt-row">
                                <span className="receipt-label">Payoff at S*</span>
                                <span className="receipt-value">${fmt(Math.abs(S_star - K), 2)}</span>
                            </div>
                            <div className="receipt-row">
                                <span className="receipt-label">Distance Factor (S/S*)^{yLabel}</span>
                                <span className="receipt-value">{fmt(Math.pow(S / S_star, y), 4)}</span>
                            </div>
                            <div className="receipt-total-line"></div>
                            <div className="receipt-row total">
                                <div className="receipt-label">Option Value</div>
                                <div className="receipt-value">${fmt(price, 2)}</div>
                            </div>
                        </div>
                    </div>
                )}
            </div>

            <ModelExplanation data={{
                source: "Haug, Chapter 3.5, Pages 109-110",
                concept: [
                    "This model provides a closed-form solution for pricing American options with no expiration date (infinite time to maturity).",
                    "Because the option reigns in perpetuity, the value does not depend on time (t). This simplifies the partial differential equation into an ordinary differential equation, allowing for exact solutions."
                ],
                formulas: [
                    { label: "Perpetual Call (c)", math: "c = \\frac{X}{y_1 - 1} \\left( \\frac{y_1 - 1}{y_1} \\frac{S}{X} \\right)^{y_1}" },
                    { label: "Perpetual Put (p)", math: "p = \\frac{X}{1 - y_2} \\left( \\frac{y_2 - 1}{y_2} \\frac{X}{S} \\right)^{y_2}" }
                ],
                where: [
                    "y_1 = \\frac{1}{2} - \\frac{b}{\\sigma^2} + \\sqrt{(\\frac{b}{\\sigma^2} - \\frac{1}{2})^2 + \\frac{2r}{\\sigma^2}}",
                    "y_2 = \\frac{1}{2} - \\frac{b}{\\sigma^2} - \\sqrt{(\\frac{b}{\\sigma^2} - \\frac{1}{2})^2 + \\frac{2r}{\\sigma^2}}"
                ],
                notation: [
                    { symbol: "S", def: "Asset Price" },
                    { symbol: "X", def: "Strike Price" },
                    { symbol: "r", def: "Risk-free Rate" },
                    { symbol: "b", def: "Cost of Carry (r-q)" },
                    { symbol: "y_1, y_2", def: "Characteristic Roots (Elasticity)" }
                ],
                contextText: "By setting the time derivative to zero (∂C/∂t = 0), the Black-Scholes PDE simplifies.",
                contextMath: "\\frac{1}{2}\\sigma^2 S^2 F_{SS} + b S F_S - r F = 0",
                examplePage: "110",
                example: {
                    inputs: [
                        { label: "Strike", sym: "X", val: "100" },
                        { label: "Asset", sym: "S", val: "90" },
                        { label: "Rate", sym: "r", val: "0.10" },
                        { label: "Div Yield", sym: "q", val: "0.08" },
                        { label: "Vol", sym: "\\sigma", val: "0.25" }
                    ],
                    calcs: [
                        { sym: "b", val: "0.02" },
                        { sym: "y_1", val: "1.9779" }
                    ],
                    result: "20.6133"
                }
            }} />
        </div>
    );
};

export default McKeanWalkthrough;

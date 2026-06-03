
import React, { useState } from 'react';
import { BlockMath, InlineMath } from 'react-katex';
import ModelExplanation from '../ModelExplanation';
import { ChevronDown, ChevronUp } from 'lucide-react';

const RollGeskeWhaleyWalkthrough = ({ inputs, results, showNumbers, highlightedVar, onHighlight }) => {
    const [expanded, setExpanded] = useState({ 1: true, 2: true, 3: true });

    const toggleStep = (step) => setExpanded(prev => ({ ...prev, [step]: !prev[step] }));

    const S = inputs.spot || 0;
    const K = inputs.strike || 0;
    const T = inputs.time || 0;
    const r = inputs.rate || 0;
    const sigma = inputs.volatility || 0;
    const D = inputs.dividend || 0; // Discrete Amount
    const t_div = inputs.time_dividend || 0;

    const price = results?.price || 0;

    // Helper to format numbers
    const fmt = (num, digits = 4) => num ? num.toFixed(digits) : '0';

    // RGW Logic Helpers for display
    const S_adj = S - D * Math.exp(-r * t_div);
    const threshold = K * (1 - Math.exp(-r * (T - t_div)));
    const check_passed = D > threshold;

    // Attempt to reconstruct intermediate values
    // Since we don't return all intermediates from backend, we might recalculate them or just show final/concepts
    // We can recalculate approximations for the UI

    // Critical Price I - we don't have it from backend unless we add it to response. 
    // We can just explain the concept.

    return (
        <div className="math-steps">

            {/* --- STEP 1: CHECK OPTIMALITY --- */}
            <div className={`step-card ${expanded[1] ? 'open' : ''}`}>
                <div className="step-trigger" onClick={() => toggleStep(1)}>
                    <div className="step-info">
                        <span className="step-circle">1</span>
                        <span className="step-title-text">Discrete Dividend Check</span>
                    </div>
                </div>
                {expanded[1] && (
                    <div className="step-content">
                        <p className="step-desc text-xs text-muted mb-3">
                            Check if the dividend is large enough to warrant early exercise consideration specifically before the ex-dividend date.
                        </p>

                        <div className="latex-box transition-all duration-300 mb-3">
                            <BlockMath math={`D > K(1 - e^{-r(T - t_{div})})`} />
                        </div>

                        <div className="bg-slate-50 p-3 rounded text-sm font-mono text-center">
                            {D} {check_passed ? '>' : '<='} {fmt(threshold)}
                        </div>

                        <div className={`mt-2 text-xs font-bold text-center ${check_passed ? 'text-success' : 'text-danger'}`}>
                            {check_passed
                                ? "Possibility of early exercise exists. Proceeding to RGW Formula."
                                : "Dividend too small. Standard European BSM optimal."}
                        </div>
                    </div>
                )}
            </div>

            {/* --- STEP 2: CRITICAL PRICE --- */}
            <div className={`step-card ${expanded[2] ? 'open' : ''}`}>
                <div className="step-trigger" onClick={() => toggleStep(2)}>
                    <div className="step-info">
                        <span className="step-circle">2</span>
                        <span className="step-title-text">Critical Price ($I$)</span>
                    </div>
                </div>
                {expanded[2] && (
                    <div className="step-content">
                        <p className="step-desc text-xs text-muted mb-3">
                            We assume there is a critical stock price <InlineMath math="I" /> (ex-dividend). If the spot price just before the dividend is above <InlineMath math="I + D" />, we exercise.
                        </p>
                        <div className="latex-box small-latex mb-3">
                            <BlockMath math={`C_{BSM}(I, K, T-t) = I + D - K`} />
                        </div>
                        <p className="text-xs text-muted">
                            The model solves numerically for $I$ where the value of holding the option equals the exercise value.
                        </p>
                    </div>
                )}
            </div>

            {/* --- STEP 3: VALUATION --- */}
            <div className={`step-card ${expanded[3] ? 'open' : ''}`}>
                <div className="step-trigger" onClick={() => toggleStep(3)}>
                    <div className="step-info">
                        <span className="step-circle">3</span>
                        <span className="step-title-text">RGW Formula</span>
                    </div>
                    <div className="step-summary-right">
                        <span className="text-primary font-bold text-lg">${fmt(price, 2)}</span>
                        {expanded[3] ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                    </div>
                </div>
                {expanded[3] && (
                    <div className="step-content">
                        <div className="latex-box small-latex mb-3">
                            <BlockMath math={`C = \\underbrace{S_{adj} N(a_1) + (D-K)e^{-rt} N(a_2)}_{\\text{Exercise Value}} + \\underbrace{\\text{Continuation Value}}_{(S < I)}`} />
                        </div>
                        <div className="valuation-receipt">
                            <div className="receipt-row total">
                                <span className="receipt-label">Calculated Price</span>
                                <span className="receipt-value">${fmt(price, 4)}</span>
                            </div>
                        </div>
                    </div>
                )}
            </div>

            <ModelExplanation data={{
                source: "Roll (1977), Geske (1979), Whaley (1981)",
                concept: [
                    "This model treats the American call as a compound option.",
                    "It considers two decision points: (1) Maturity T, and (2) Just before the dividend T_div.",
                    "If the dividend is large enough, optimal exercise might occur at T_div."
                ],
                formulas: [
                    { label: "RGW Call", math: "C = \\text{Exercise Part} + \\text{Continuation Part}" },
                    { label: "Condition", math: "S(t_{div}) > I" }
                ],
                where: [
                    "S_{adj} = S - D e^{-r t_{div}}",
                    "I = \\text{Critical Ex-Dividend Price}",
                    "\\rho = \\sqrt{t_{div}/T}"
                ],
                notation: [
                    { symbol: "D", def: "Discrete Dividend Amount" },
                    { symbol: "t_{div}", def: "Time to Dividend" },
                    { symbol: "I", def: "Critical Price" }
                ],
                contextText: "Standard Black-Scholes fails for large discrete dividends because it assumes continuous yield or no early exercise.",
                examplePage: "376",
                example: {
                    inputs: [
                        { label: "Spot", sym: "S", val: "80" },
                        { label: "Strike", sym: "K", val: "82" },
                        { label: "Dividend", sym: "D", val: "4" },
                        { label: "Time", sym: "t_div", val: "0.25" }
                    ],
                    calcs: [
                        { sym: "I", val: "80.11" },
                        { sym: "b_1", val: "-0.23" }
                    ],
                    result: "4.3860"
                }
            }} />
        </div>
    );
};

export default RollGeskeWhaleyWalkthrough;

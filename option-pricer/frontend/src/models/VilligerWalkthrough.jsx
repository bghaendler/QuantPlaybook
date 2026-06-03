import React, { useState } from 'react';
import { BlockMath, InlineMath } from 'react-katex';
import ModelExplanation from '../ModelExplanation';
import { ChevronDown, ChevronUp } from 'lucide-react';

const VilligerWalkthrough = ({ inputs, results, showNumbers }) => {
    const [expanded, setExpanded] = useState({ 1: true, 2: true });

    const toggleStep = (step) => setExpanded(prev => ({ ...prev, [step]: !prev[step] }));

    const S = inputs.spot || 0;
    const K = inputs.strike || 0;
    const T = inputs.time || 0;
    const r = inputs.rate || 0;
    // For Villiger, dividend is passed as 'dividend' but represents yield %
    const delta = inputs.dividend || 0;
    const t_div = inputs.time_dividend || 0;

    const price = results?.price || 0;
    const fmt = (num, digits = 4) => num ? num.toFixed(digits) : '0';

    return (
        <div className="math-steps">

            {/* --- STEP 1: CONCEPT --- */}
            <div className={`step-card ${expanded[1] ? 'open' : ''}`}>
                <div className="step-trigger" onClick={() => toggleStep(1)}>
                    <div className="step-info">
                        <span className="step-circle">1</span>
                        <span className="step-title-text">Discrete vs Continuous Yield</span>
                    </div>
                    <div className="step-summary-right">
                        {expanded[1] ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                    </div>
                </div>
                {expanded[1] && (
                    <div className="step-content">
                        <p className="step-desc text-xs text-muted mb-3">
                            Unlike Merton (continuous yield), Villiger assumes a single discrete drop of <InlineMath math="\delta \%" /> at time <InlineMath math="t" />. This prevents negative stock prices.
                        </p>
                        <div className="bg-slate-50 p-3 rounded text-sm text-center border border-slate-200">
                            Ex-Dividend Price = <InlineMath math={`S(1 - \\delta) = ${fmt(S * (1 - delta), 2)}`} />
                        </div>
                    </div>
                )}
            </div>

            {/* --- STEP 2: FORMULA --- */}
            <div className={`step-card ${expanded[2] ? 'open' : ''}`}>
                <div className="step-trigger" onClick={() => toggleStep(2)}>
                    <div className="step-info">
                        <span className="step-circle">2</span>
                        <span className="step-title-text">Villiger Formula</span>
                    </div>
                    <div className="step-summary-right">
                        <span className="text-primary font-bold text-lg mr-2">${fmt(price, 4)}</span>
                        {expanded[2] ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                    </div>
                </div>
                {expanded[2] && (
                    <div className="step-content">
                        <div className="latex-box small-latex mb-3">
                            <BlockMath math={`C = S N(a_1) - Ke^{-rt} N(a_2) + \\text{Term}_{Cont}`} />
                        </div>
                        <p className="step-desc text-xs text-muted mb-3">
                            The first part captures the value if exercised early (to capture dividend). The second part uses bivariate normal distributions for the continuation value.
                        </p>
                    </div>
                )}
            </div>

            <ModelExplanation data={{
                source: "Villiger (2005)",
                concept: [
                    "Closed-form analytical solution for American calls with discrete DIVIDEND YIELD.",
                    "Avoids arbitrage issues of fixed-cash dividend models (like RGW) where S - D can be negative."
                ],
                formulas: [
                    { label: "Villiger Call", math: "C = \\text{Ex}(S_t > I) + \\text{Cont}(S_t < I)" }
                ],
                where: [
                    "\\delta = \\text{Dividend Yield}",
                    "I = \\text{Critical Price solving } C_{BSM}(I(1-\\delta)) = I - K"
                ],
                notation: [
                    { symbol: "\\delta", def: "Dividend Yield (Percentage)" },
                    { symbol: "t", def: "Time to Dividend" }
                ],
                contextText: "A robust alternative to Roll-Geske-Whaley when dividends are proportional to stock price.",
                examplePage: "392",
                example: {
                    inputs: [
                        { label: "Spot", sym: "S", val: "100" },
                        { label: "Strike", sym: "K", val: "102" },
                        { label: "Yield", sym: "\\delta", val: "0.05" },
                        { label: "Time", sym: "T", val: "0.5" },
                        { label: "Div Time", sym: "t", val: "0.25" }
                    ],
                    calcs: [
                        { sym: "I", val: "105.23" }
                    ],
                    result: "3.7178"
                }
            }} />
        </div>
    );
};

export default VilligerWalkthrough;
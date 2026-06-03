
import React, { useState } from 'react';
import { BlockMath } from 'react-katex';
import { ChevronDown, ChevronUp, Layers, TrendingUp, Award, Clock } from 'lucide-react';
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
    alpha: "#7c3aed",    // Violet-600 (Alpha components)
    boundary: "#059669", // Emerald-600
    bivariate: "#dc2626", // Red-600 (New complexity)
    time_split: "#ea580c", // Orange-600 (t1 split)
};

const Bs2002Walkthrough = ({ inputs, results, showNumbers, highlightedVar, onHighlight }) => {
    const [expanded, setExpanded] = useState({ 1: true, 2: true, 3: true, 4: true });

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
    const q = inputs.dividend || 0.03;
    const v = inputs.volatility || 0.30;
    // const isCall = inputs.type === 'call';

    const { price, note } = results;

    // Local Calculations for Walkthrough Display
    const b = r - q;

    // 1. Beta
    const beta = (0.5 - b / (v * v)) + Math.sqrt(Math.pow(b / (v * v) - 0.5, 2) + 2 * r / (v * v));

    // 2. Time Split (Golden Ratio)
    const t1 = 0.5 * (Math.sqrt(5) - 1) * T;

    // 3. Boundaries
    const B_inf = (beta / (beta - 1)) * K;
    const B_0 = Math.max(K, (r / (r - b)) * K);

    const h = (t) => -(b * t + 2 * v * Math.sqrt(t)) * (K * K) / ((B_inf - B_0) * B_0);

    const I1 = B_0 + (B_inf - B_0) * (1 - Math.exp(h(t1)));
    const I2 = B_0 + (B_inf - B_0) * (1 - Math.exp(h(T)));

    // --- DYNAMIC LATEX GENERATOR ---
    const V = (symbol, value, colorKey) => {
        const color = COLORS[colorKey];
        const varMap = {
            'spot': 'S', 'strike': 'K', 'time': 'T', 'rate': 'r', 'volatility': 'sigma', 'dividend': 'q'
        };
        const isHighlighted = highlightedVar && varMap[highlightedVar] === colorKey;
        const content = showNumbers ? fmt(value, 3) : symbol;
        const coloredContent = `\\textcolor{${color}}{${content}}`;
        return isHighlighted ? `\\mathbf{${coloredContent}}` : coloredContent;
    };

    return (
        <div className="math-steps">

            {/* INFO BANNER */}
            <div className="info-banner mb-4 p-3 bg-indigo-50 border border-indigo-200 rounded-lg">
                <div className="flex items-start gap-2">
                    <Award size={18} className="text-indigo-600 mt-0.5 flex-shrink-0" />
                    <div className="text-xs text-indigo-900">
                        <strong>Bjerksund-Stensland (2002)</strong> refines the 1993 model by conducting a <strong>Two-Step Boundary Approximation</strong>.
                        It divides time into two intervals for significantly higher accuracy, specifically correcting for the 1993 model's single flat boundary limitations.
                    </div>
                </div>
            </div>

            {/* IMPROVEMENT BANNER */}
            <div className="info-banner mb-4 p-3 bg-red-50 border border-red-200 rounded-lg">
                <div className="flex items-start gap-2">
                    <TrendingUp size={18} className="text-red-600 mt-0.5 flex-shrink-0" />
                    <div className="text-xs text-red-900">
                        <strong>New Complexity:</strong> Uses the <strong>Cumulative Bivariate Normal Distribution</strong> $\Psi(\cdot)$ to handle the joint probability of not hitting either of the two boundaries.
                    </div>
                </div>
            </div>

            {/* --- STEP 1: TIME SPLIT & BETA --- */}
            <div className={`step-card ${expanded[1] ? 'open' : ''}`}>
                <div className="step-trigger" onClick={() => toggleStep(1)}>
                    <div className="step-info">
                        <span className="step-circle">1</span>
                        <span className="step-title-text">Setup: The Golden Ratio Time Split</span>
                    </div>
                    <div className="step-summary-right">
                        <span className="mono-val" style={{ color: COLORS.time_split }}>t₁ = {fmt(t1, 3)}</span>
                        {expanded[1] ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                    </div>
                </div>

                {expanded[1] && (
                    <div className="step-content">
                        <p className="step-desc text-xs text-muted mb-4">
                            Unlike BS93 (one period), BS2002 splits the time to maturity $T$ into two parts using the <strong>Golden Ratio</strong> $\phi \approx 0.618$ for optimal approximation.
                        </p>

                        <div className="latex-box transition-all duration-300 mb-3">
                            <BlockMath math={`t_1 = \\tfrac{1}{2}(\\sqrt{5}-1) ${V('T', T, 'T')} = ${fmt(t1, 4)}`} />
                        </div>

                        <div className="latex-box transition-all duration-300 mb-3">
                            <BlockMath math={`\\beta = \\left(\\tfrac{1}{2} - \\tfrac{${V('b', b, 'q')}}{${V('\\sigma', v, 'sigma')}^2}\\right) + \\sqrt{(\\dots)^2 + \\frac{2${V('r', r, 'r')}}{${V('\\sigma', v, 'sigma')}^2}} = ${fmt(beta, 4)}`} />
                        </div>

                        <div className="mt-3 p-2 bg-orange-50 rounded text-xs text-orange-900 flex items-start gap-2">
                            <Clock size={14} className="mt-0.5" />
                            <div>
                                <strong>Why Splitting Time?</strong> Dividing the lifetime of the option allows the model to respond to the curved exercise boundary with <strong>two different flat levels</strong> instead of just one.
                            </div>
                        </div>
                    </div>
                )}
            </div>

            {/* --- STEP 2: TWO BOUNDARIES --- */}
            <div className={`step-card ${expanded[2] ? 'open' : ''}`}>
                <div className="step-trigger" onClick={() => toggleStep(2)}>
                    <div className="step-info">
                        <span className="step-circle">2</span>
                        <span className="step-title-text">Two-Step Boundaries (I₁ & I₂)</span>
                    </div>
                    <div className="step-summary-right">
                        <span className="mono-val" style={{ color: COLORS.boundary }}>I₁={fmt(I1, 1)}, I₂={fmt(I2, 1)}</span>
                        {expanded[2] ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                    </div>
                </div>

                {expanded[2] && (
                    <div className="step-content">
                        <div className="grid grid-cols-2 gap-3 mb-3">
                            <div className="p-3 bg-emerald-50 rounded border border-emerald-200">
                                <div className="text-xs font-semibold text-emerald-900 mb-1">Interval [0, {fmt(t1, 2)})</div>
                                <div className="text-lg font-bold text-emerald-700">Boundary I₁ = {fmt(I1, 2)}</div>
                                <div className="text-[10px] text-emerald-800 mt-1">
                                    Effectively a lower trigger price for early life.
                                </div>
                            </div>
                            <div className="p-3 bg-emerald-50 rounded border border-emerald-200">
                                <div className="text-xs font-semibold text-emerald-900 mb-1">Interval [{fmt(t1, 2)}, {fmt(T, 2)}]</div>
                                <div className="text-lg font-bold text-emerald-700">Boundary I₂ = {fmt(I2, 2)}</div>
                                <div className="text-[10px] text-emerald-800 mt-1">
                                    Higher trigger price near expiration.
                                </div>
                            </div>
                        </div>

                        <div className="latex-box small-latex mb-3">
                            <BlockMath math={`I_1 = B_0 + (B_\\infty - B_0)(1 - e^{h(t_1)})`} />
                            <BlockMath math={`I_2 = B_0 + (B_\\infty - B_0)(1 - e^{h(T)})`} />
                        </div>

                        <div className="mt-3 p-2 bg-blue-50 rounded text-xs text-blue-900">
                            <strong>Visual Concept:</strong> Imagine a step-function. The critical price needed to exercise starts at $I_1$ and then jumps to $I_2$ at time $t_1$. This approximates the "curve" of the real boundary much better than a single flat line.
                        </div>
                    </div>
                )}
            </div>

            {/* --- STEP 3: PROBABILITY FUNCTIONS --- */}
            <div className={`step-card ${expanded[3] ? 'open' : ''}`}>
                <div className="step-trigger" onClick={() => toggleStep(3)}>
                    <div className="step-info">
                        <span className="step-circle">3</span>
                        <span className="step-title-text">Bivariate Probability (Ψ)</span>
                    </div>
                    <div className="step-summary-right">
                        <span className="text-xs text-red-600 font-bold">New Function</span>
                        {expanded[3] ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                    </div>
                </div>

                {expanded[3] && (
                    <div className="step-content">
                        <p className="step-desc text-xs text-muted mb-4">
                            BS2002 introduces $\Psi$ to calculate the joint probability of the asset price staying below $I_1$ in period 1 <strong>AND</strong> below $I_2$ in period 2.
                        </p>

                        <div className="p-3 bg-red-50 rounded border border-red-200 mb-3">
                            <div className="latex-box small-latex">
                                <BlockMath math={`\\Psi(S, T, \\dots) = M(d_1, d_2, \\rho)`} />
                            </div>
                            <div className="text-center text-xs text-red-800 mt-2 font-mono">
                                where ρ = √(t₁/T) ≈ {fmt(Math.sqrt(t1 / T), 3)}
                            </div>
                        </div>

                        <div className="grid grid-cols-2 gap-2 text-xs text-slate-600">
                            <div>
                                <strong>Φ (Phi):</strong> Univariate Normal (Probability of 1 event)
                            </div>
                            <div>
                                <strong>Ψ (Psi):</strong> Bivariate Normal (Probability of 2 simultaneous events)
                            </div>
                        </div>
                    </div>
                )}
            </div>

            {/* --- STEP 4: FINAL VALUATION --- */}
            <div className={`step-card ${expanded[4] ? 'open' : ''}`}>
                <div className="step-trigger" onClick={() => toggleStep(4)}>
                    <div className="step-info">
                        <span className="step-circle">4</span>
                        <span className="step-title-text">Final Valuation</span>
                    </div>
                    <div className="step-summary-right">
                        <span className="text-primary font-bold text-lg">${fmt(price, 2)}</span>
                        {expanded[4] ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                    </div>
                </div>

                {expanded[4] && (
                    <div className="step-content">
                        <div className="latex-box small-latex mb-3">
                            <BlockMath math={`C = \\alpha(I_2)S^\\beta - \\alpha(I_2)\\phi(\\dots) + \\Psi(\\dots) - \\Psi(\\dots)`} />
                        </div>

                        <div className="valuation-receipt mb-3">
                            <div className="receipt-row total">
                                <div className="receipt-label">BS2002 Price</div>
                                <div className="receipt-value">${fmt(price, 2)}</div>
                            </div>
                        </div>

                        {note && (
                            <div className="mt-3 p-2 bg-blue-50 rounded text-xs">
                                <div className="font-semibold text-blue-900 mb-1">Model Note:</div>
                                <div className="text-blue-800">{note}</div>
                            </div>
                        )}

                        <div className="p-3 bg-violet-50 rounded border border-violet-200 text-xs mt-3">
                            <div className="font-semibold text-violet-900 mb-1">Summary:</div>
                            This "Two-Step" approach provides excellent accuracy (matching Binomial trees) while being much faster to compute, making it the preferred analytical approximation for American options.
                        </div>
                    </div>
                )}
            </div>

            {inputs && <ModelExplanation data={TEXTBOOK_DATA.bjerksund93} />}
        </div>
    );
};

export default Bs2002Walkthrough;

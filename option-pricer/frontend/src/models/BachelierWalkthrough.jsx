// --- START OF FILE src/models/BachelierWalkthrough.jsx ---

import React, { useState, useMemo } from 'react';
import { BlockMath, InlineMath } from 'react-katex';
import { ArrowRight, ChevronDown, ChevronUp, Minus, HelpCircle } from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, ResponsiveContainer, ReferenceLine, Tooltip as RechartsTooltip } from 'recharts';
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
};

const BachelierWalkthrough = ({ inputs, results, showNumbers }) => {
    const [expanded, setExpanded] = useState({ 1: true, 2: true, 3: true });

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
    const v = inputs.volatility || 0.2;
    const q = inputs.dividend || 0;
    const isCall = inputs.type === 'call';

    // Extract Results from Backend
    const { price, note } = results;
    const greeks = results.greeks || {};

    // Local Calculations for Bachelier
    const b = r - q; // Cost of carry
    const F = S * Math.exp(b * T); // Forward price
    const sigma_sqrt_T = v * Math.sqrt(T);
    const d = (F - K) / sigma_sqrt_T; // Bachelier d parameter

    // Normal distribution functions (approximation)
    const norm_cdf = (x) => {
        const t = 1 / (1 + 0.2316419 * Math.abs(x));
        const d = 0.3989423 * Math.exp(-x * x / 2);
        const prob = d * t * (0.3193815 + t * (-0.3565638 + t * (1.781478 + t * (-1.821256 + t * 1.330274))));
        return x > 0 ? 1 - prob : prob;
    };

    const norm_pdf = (x) => {
        return (1 / Math.sqrt(2 * Math.PI)) * Math.exp(-0.5 * x * x);
    };

    const N_d = norm_cdf(d);
    const N_minus_d = norm_cdf(-d);
    const n_d = norm_pdf(d);
    const df = Math.exp(-r * T);

    // --- CHART LOGIC: NORMAL PRICE DISTRIBUTION (Not LogNormal!) ---
    const distributionData = useMemo(() => {
        const points = [];
        const steps = 60;

        // For Bachelier, we use NORMAL distribution centered on Forward
        const fwd = F;

        // Standard Deviation is simply sigma * sqrt(T)
        const stdDev = sigma_sqrt_T;

        // Determine Graph Range (±3 standard deviations)
        let minX = fwd - 3 * stdDev;
        let maxX = fwd + 3 * stdDev;

        // Ensure Strike is visible
        if (K < minX) minX = K - stdDev;
        if (K > maxX) maxX = K + stdDev;

        const range = maxX - minX;
        const stepSize = range / steps;

        for (let i = 0; i <= steps; i++) {
            const x = minX + i * stepSize;

            // NORMAL PDF formula (not lognormal!)
            // f(x) = (1 / (σ√(2π))) * exp(-(x-μ)² / (2σ²))
            const density = (1 / (stdDev * Math.sqrt(2 * Math.PI))) *
                Math.exp(-Math.pow(x - fwd, 2) / (2 * stdDev * stdDev));

            // Shading Logic
            let fillValue = 0;
            if (isCall && x >= K) fillValue = density;
            if (!isCall && x <= K) fillValue = density;

            points.push({
                price: x,
                density: density,
                fill: fillValue
            });
        }

        return { data: points, fwd };
    }, [S, K, T, r, q, v, isCall, F, sigma_sqrt_T]);

    // --- DYNAMIC LATEX GENERATOR ---
    const V = (symbol, value, colorKey) => {
        const color = COLORS[colorKey];
        if (showNumbers) {
            return `\\textcolor{${color}}{${fmt(value, 3)}}`;
        }
        return `\\textcolor{${color}}{${symbol}}`;
    };

    const d_formula = `\\frac{${V('F', F, 'S')} - ${V('K', K, 'K')}}{${V('\\sigma', v, 'sigma')}\\sqrt{${V('T', T, 'T')}}}`;

    const call_formula = `e^{-${V('r', r, 'r')}${V('T', T, 'T')}} \\left[(${V('F', F, 'S')} - ${V('K', K, 'K')}) N(d) + ${V('\\sigma', v, 'sigma')}\\sqrt{${V('T', T, 'T')}} n(d)\\right]`;
    const put_formula = `e^{-${V('r', r, 'r')}${V('T', T, 'T')}} \\left[(${V('K', K, 'K')} - ${V('F', F, 'S')}) N(-d) + ${V('\\sigma', v, 'sigma')}\\sqrt{${V('T', T, 'T')}} n(d)\\right]`;

    return (
        <div className="math-steps">

            {/* INFO BANNER */}
            <div className="info-banner mb-4 p-3 bg-amber-50 border border-amber-200 rounded-lg">
                <div className="flex items-start gap-2">
                    <HelpCircle size={18} className="text-amber-600 mt-0.5 flex-shrink-0" />
                    <div className="text-xs text-amber-900">
                        <strong>Bachelier (1900)</strong> uses <strong>Normal Distribution</strong> (not Lognormal).
                        This allows <strong>negative prices</strong>, making it ideal for <strong>interest rates</strong> and <strong>commodity spreads</strong>.
                        The volatility is in <strong>absolute price units</strong>, not percentage.
                    </div>
                </div>
            </div>

            {/* --- STEP 1: FORWARD PRICE & d PARAMETER --- */}
            <div className={`step-card ${expanded[1] ? 'open' : ''}`}>
                <div className="step-trigger" onClick={() => toggleStep(1)}>
                    <div className="step-info">
                        <span className="step-circle">1</span>
                        <span className="step-title-text">Calculate Forward & d Parameter</span>
                    </div>
                    <div className="step-summary-right">
                        <span className="mono-val">d = {fmt(d)}</span>
                        {expanded[1] ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                    </div>
                </div>

                {expanded[1] && (
                    <div className="step-content">
                        <div className="latex-box transition-all duration-300 mb-3">
                            <BlockMath math={`F = ${V('S', S, 'S')} e^{(${V('r', r, 'r')} - ${V('q', q, 'q')})${V('T', T, 'T')}} = ${fmt(F, 2)}`} />
                        </div>

                        <div className="latex-box transition-all duration-300">
                            <BlockMath math={`d = ${d_formula} = ${fmt(d, 4)}`} />
                        </div>

                        <div className="breakdown-grid">
                            <div className="breakdown-item border-l-4" style={{ borderLeftColor: COLORS.S }}>
                                <span className="label">Forward Price (F)</span>
                                <span className="value" style={{ color: COLORS.S }}>{fmt(F, 2)}</span>
                            </div>
                            <div className="breakdown-item border-l-4" style={{ borderLeftColor: COLORS.K }}>
                                <span className="label">Distance (F - K)</span>
                                <span className="value" style={{ color: COLORS.K }}>{fmt(F - K, 2)}</span>
                            </div>
                            <div className="breakdown-item border-l-4" style={{ borderLeftColor: COLORS.sigma }}>
                                <span className="label">Volatility Term σ√T</span>
                                <span className="value" style={{ color: COLORS.sigma }}>{fmt(sigma_sqrt_T, 3)}</span>
                            </div>
                        </div>

                        <div className="mt-3 p-2 bg-blue-50 rounded text-xs text-blue-900">
                            <strong>Note:</strong> Unlike BSM's ln(S/K), Bachelier uses the <strong>arithmetic difference</strong> (F - K).
                            This is why negative prices are possible.
                        </div>
                    </div>
                )}
            </div>

            {/* --- STEP 2: NORMAL DISTRIBUTION PROBABILITIES --- */}
            <div className={`step-card ${expanded[2] ? 'open' : ''}`}>
                <div className="step-trigger" onClick={() => toggleStep(2)}>
                    <div className="step-info">
                        <span className="step-circle">2</span>
                        <span className="step-title-text">Normal Distribution (No Skew)</span>
                    </div>
                    <div className="step-summary-right">
                        <span className="mono-val">N(d) = {fmt(N_d, 4)}</span>
                        {expanded[2] ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                    </div>
                </div>

                {expanded[2] && (
                    <div className="step-content">
                        <p className="step-desc text-xs text-muted mb-4">
                            The <strong>Normal Distribution</strong> is symmetric (unlike lognormal).
                            The shaded area shows the ITM probability based on absolute price movements.
                        </p>

                        <div style={{ height: '160px', width: '100%', marginBottom: '10px' }}>
                            <ResponsiveContainer width="100%" height="100%">
                                <AreaChart data={distributionData.data}>
                                    <defs>
                                        <linearGradient id="bachelierFill" x1="0" y1="0" x2="1" y2="0">
                                            <stop offset="0%" stopColor="#8b5cf6" stopOpacity={isCall ? 0 : 0.4} />
                                            <stop offset="100%" stopColor="#8b5cf6" stopOpacity={isCall ? 0.4 : 0} />
                                        </linearGradient>
                                    </defs>
                                    <XAxis
                                        dataKey="price"
                                        type="number"
                                        domain={['auto', 'auto']}
                                        tickFormatter={(v) => v.toFixed(1)}
                                        tick={{ fontSize: 10 }}
                                        interval="preserveStartEnd"
                                    />
                                    <YAxis hide />

                                    <RechartsTooltip
                                        formatter={(val) => val.toFixed(5)}
                                        labelFormatter={(label) => `Price: ${parseFloat(label).toFixed(2)}`}
                                    />

                                    {/* The Normal Curve */}
                                    <Area
                                        type="monotone"
                                        dataKey="density"
                                        stroke="#8b5cf6"
                                        fill="none"
                                        strokeWidth={2}
                                        isAnimationActive={false}
                                    />

                                    {/* The Shaded ITM Area */}
                                    <Area
                                        type="monotone"
                                        dataKey="fill"
                                        stroke="none"
                                        fill="#8b5cf6"
                                        fillOpacity={0.3}
                                        isAnimationActive={false}
                                    />

                                    {/* Strike Line */}
                                    <ReferenceLine x={K} stroke="#ec4899" strokeWidth={2} label={{ value: 'Strike', fill: '#ec4899', fontSize: 10, position: 'top' }} />

                                    {/* Forward Price Line */}
                                    <ReferenceLine x={distributionData.fwd} stroke="#3b82f6" strokeDasharray="3 3" label={{ value: 'Forward', fill: '#3b82f6', fontSize: 10, position: 'top' }} />

                                </AreaChart>
                            </ResponsiveContainer>
                        </div>

                        <div className="probability-table">
                            {/* N(d) */}
                            <div className="prob-row">
                                <div className="prob-label">
                                    <div className="flex items-center gap-2">
                                        <InlineMath math={`N(${isCall ? '' : '-'}d)`} />
                                        <span className="text-xs font-bold bg-violet-100 text-violet-800 px-1 rounded">Probability</span>
                                    </div>
                                    <span className="prob-desc mt-1">Probability ITM</span>
                                </div>
                                <div className="text-right">
                                    <div className="prob-val text-violet-600">{fmt(isCall ? N_d : N_minus_d, 4)}</div>
                                    <div className="text-[10px] text-muted leading-tight max-w-[150px]">
                                        {fmt((isCall ? N_d : N_minus_d) * 100, 2)}% chance of profit at expiry.
                                    </div>
                                </div>
                            </div>

                            {/* n(d) */}
                            <div className="prob-row">
                                <div className="prob-label">
                                    <div className="flex items-center gap-2">
                                        <InlineMath math={`n(d)`} />
                                        <span className="text-xs font-bold bg-indigo-100 text-indigo-800 px-1 rounded">Density</span>
                                    </div>
                                    <span className="prob-desc mt-1">Normal PDF Value</span>
                                </div>
                                <div className="text-right">
                                    <div className="prob-val text-indigo-600">{fmt(n_d, 4)}</div>
                                    <div className="text-[10px] text-muted leading-tight max-w-[150px]">
                                        Used for Vega and Gamma calculations.
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div className="mt-3 p-2 bg-purple-50 rounded text-xs text-purple-900">
                            <strong>Symmetric:</strong> Normal distribution is symmetric, unlike the right-skewed lognormal used in BSM.
                        </div>
                    </div>
                )}
            </div>

            {/* --- STEP 3: VALUATION --- */}
            <div className={`step-card ${expanded[3] ? 'open' : ''}`}>
                <div className="step-trigger" onClick={() => toggleStep(3)}>
                    <div className="step-info">
                        <span className="step-circle">3</span>
                        <span className="step-title-text">Bachelier Valuation</span>
                    </div>
                    <div className="step-summary-right">
                        <span className="text-primary font-bold text-lg">${fmt(price, 2)}</span>
                        {expanded[3] ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                    </div>
                </div>

                {expanded[3] && (
                    <div className="step-content">
                        <div className="latex-box small-latex mb-3">
                            <BlockMath math={isCall ? `C = ${call_formula}` : `P = ${put_formula}`} />
                        </div>

                        <div className="valuation-receipt">
                            {/* Distance Term */}
                            <div className="receipt-row positive">
                                <div className="receipt-label">
                                    <span className="r-title" style={{ color: COLORS.S }}>Distance Term</span>
                                    <span className="r-sub">(F - K) × N(d) × e^(-rT)</span>
                                </div>
                                <div className="receipt-value" style={{ color: COLORS.S }}>
                                    {fmt(df * (F - K) * (isCall ? N_d : N_minus_d), 3)}
                                </div>
                            </div>

                            <div className="receipt-divider">
                                <span className="text-xs text-muted">+</span>
                            </div>

                            {/* Volatility Term */}
                            <div className="receipt-row positive">
                                <div className="receipt-label">
                                    <span className="r-title" style={{ color: COLORS.sigma }}>Volatility Term</span>
                                    <span className="r-sub">σ√T × n(d) × e^(-rT)</span>
                                </div>
                                <div className="receipt-value" style={{ color: COLORS.sigma }}>
                                    {fmt(df * sigma_sqrt_T * n_d, 3)}
                                </div>
                            </div>

                            {/* Total */}
                            <div className="receipt-total-line"></div>
                            <div className="receipt-row total">
                                <div className="receipt-label">Bachelier Price</div>
                                <div className="receipt-value">${fmt(price, 2)}</div>
                            </div>
                        </div>

                        {note && (
                            <div className="mt-3 p-2 bg-green-50 rounded text-xs">
                                <div className="font-semibold text-green-900 mb-1">Comparison:</div>
                                <div className="text-green-800">{note}</div>
                            </div>
                        )}

                        <div className="mt-3 p-2 bg-amber-50 rounded text-xs text-amber-900">
                            <strong>Key Difference from BSM:</strong> Bachelier has <strong>two terms</strong> instead of a difference.
                            The (F-K) term represents intrinsic value adjusted by probability,
                            and the σ√T×n(d) term represents time value from volatility.
                        </div>
                    </div>
                )}
            </div>

            <ModelExplanation data={TEXTBOOK_DATA.bachelier} />
        </div>
    );
};

export default BachelierWalkthrough;

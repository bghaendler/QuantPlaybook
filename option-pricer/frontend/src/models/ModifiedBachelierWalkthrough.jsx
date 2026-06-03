// --- START OF FILE src/models/ModifiedBachelierWalkthrough.jsx ---

import React, { useState, useMemo } from 'react';
import { BlockMath, InlineMath } from 'react-katex';
import { ArrowRight, ChevronDown, ChevronUp, Minus, HelpCircle, Shuffle } from 'lucide-react';
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
    beta: "#f43f5e",  // Rose-500 (for shift)
};

const ModifiedBachelierWalkthrough = ({ inputs, results, showNumbers }) => {
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
    const v = inputs.volatility || 20;
    const q = inputs.dividend || 0;
    const beta = inputs.shift || 0;  // Shift parameter!
    const isCall = inputs.type === 'call';

    // Extract Results from Backend
    const { price, note } = results;
    const greeks = results.greeks || {};

    // Local Calculations for Modified Bachelier
    const b = r - q; // Cost of carry
    const F = S * Math.exp(b * T); // Forward price

    // Apply shift
    const F_shifted = F + beta;
    const K_shifted = K + beta;

    const sigma_sqrt_T = v * Math.sqrt(T);
    const d = (F_shifted - K_shifted) / sigma_sqrt_T; // Modified d parameter

    // Normal distribution functions
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

    // --- CHART LOGIC: SHOW SHIFTED DISTRIBUTION ---
    const distributionData = useMemo(() => {
        const points = [];
        const steps = 60;

        // Center on shifted forward
        const fwd_center = F_shifted;
        const stdDev = sigma_sqrt_T;

        let minX = fwd_center - 3 * stdDev;
        let maxX = fwd_center + 3 * stdDev;

        // Ensure both K and K_shifted are visible
        if (K < minX) minX = K - stdDev;
        if (K > maxX) maxX = K + stdDev;
        if (K_shifted < minX) minX = K_shifted - stdDev;
        if (K_shifted > maxX) maxX = K_shifted + stdDev;

        const range = maxX - minX;
        const stepSize = range / steps;

        for (let i = 0; i <= steps; i++) {
            const x = minX + i * stepSize;

            // SHIFTED Normal PDF
            const density = (1 / (stdDev * Math.sqrt(2 * Math.PI))) *
                Math.exp(-Math.pow(x - fwd_center, 2) / (2 * stdDev * stdDev));

            // Shading based on shifted strike
            let fillValue = 0;
            if (isCall && x >= K_shifted) fillValue = density;
            if (!isCall && x <= K_shifted) fillValue = density;

            points.push({
                price: x,
                density: density,
                fill: fillValue
            });
        }

        return { data: points, fwd: F, fwd_shifted: F_shifted };
    }, [S, K, T, r, q, v, beta, isCall, F, F_shifted, K_shifted, sigma_sqrt_T]);

    // --- DYNAMIC LATEX GENERATOR ---
    const V = (symbol, value, colorKey) => {
        const color = COLORS[colorKey];
        if (showNumbers) {
            return `\\textcolor{${color}}{${fmt(value, 3)}}`;
        }
        return `\\textcolor{${color}}{${symbol}}`;
    };

    const d_formula = `\\frac{(${V('F', F, 'S')} + ${V('\\beta', beta, 'beta')}) - (${V('K', K, 'K')} + ${V('\\beta', beta, 'beta')})}{${V('\\sigma', v, 'sigma')}\\sqrt{${V('T', T, 'T')}}}`;

    const call_formula = `e^{-${V('r', r, 'r')}${V('T', T, 'T')}} \\left[(${V('F', F, 'S')} - ${V('K', K, 'K')}) N(d_\\beta) + ${V('\\sigma', v, 'sigma')}\\sqrt{${V('T', T, 'T')}} n(d_\\beta)\\right]`;
    const put_formula = `e^{-${V('r', r, 'r')}${V('T', T, 'T')}} \\left[(${V('K', K, 'K')} - ${V('F', F, 'S')}) N(-d_\\beta) + ${V('\\sigma', v, 'sigma')}\\sqrt{${V('T', T, 'T')}} n(d_\\beta)\\right]`;

    return (
        <div className="math-steps">

            {/* INFO BANNER */}
            <div className="info-banner mb-4 p-3 bg-rose-50 border border-rose-200 rounded-lg">
                <div className="flex items-start gap-2">
                    <Shuffle size={18} className="text-rose-600 mt-0.5 flex-shrink-0" />
                    <div className="text-xs text-rose-900">
                        <strong>Modified Bachelier (Shifted)</strong> extends Bachelier by adding a <strong>shift parameter β={beta}</strong>.
                        This displaces the normal distribution, allowing better calibration to market prices. When <strong>β=0</strong>, it reduces to standard Bachelier.
                    </div>
                </div>
            </div>

            {/* --- STEP 1: THE SHIFT EFFECT --- */}
            <div className={`step-card ${expanded[1] ? 'open' : ''}`}>
                <div className="step-trigger" onClick={() => toggleStep(1)}>
                    <div className="step-info">
                        <span className="step-circle">1</span>
                        <span className="step-title-text">Apply Shift Parameter (β={fmt(beta, 1)})</span>
                    </div>
                    <div className="step-summary-right">
                        <span className="mono-val">d_β = {fmt(d)}</span>
                        {expanded[1] ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                    </div>
                </div>

                {expanded[1] && (
                    <div className="step-content">
                        <div className="latex-box transition-all duration-300 mb-3">
                            <BlockMath math={`F = ${V('S', S, 'S')} e^{(${V('r', r, 'r')} - ${V('q', q, 'q')})${V('T', T, 'T')}} = ${fmt(F, 2)}`} />
                        </div>

                        <div className="bg-rose-50 border border-rose-200 rounded p-3 my-3">
                            <div className="text-sm font-semibold text-rose-900 mb-2">Shifted Values:</div>
                            <div className="grid grid-cols-2 gap-3 text-xs">
                                <div>
                                    <div className="text-rose-700 font-mono">F' = F + β</div>
                                    <div className="text-rose-900">{fmt(F, 2)} + {fmt(beta, 1)} = <strong>{fmt(F_shifted, 2)}</strong></div>
                                </div>
                                <div>
                                    <div className="text-rose-700 font-mono">K' = K + β</div>
                                    <div className="text-rose-900">{fmt(K, 2)} + {fmt(beta, 1)} = <strong>{fmt(K_shifted, 2)}</strong></div>
                                </div>
                            </div>
                        </div>

                        <div className="latex-box transition-all duration-300">
                            <BlockMath math={`d_\\beta = ${d_formula} = ${fmt(d, 4)}`} />
                        </div>

                        <div className="breakdown-grid">
                            <div className="breakdown-item border-l-4" style={{ borderLeftColor: COLORS.beta }}>
                                <span className="label">Shift (β)</span>
                                <span className="value" style={{ color: COLORS.beta }}>{fmt(beta, 2)}</span>
                            </div>
                            <div className="breakdown-item border-l-4" style={{ borderLeftColor: COLORS.S }}>
                                <span className="label">Shifted Forward (F')</span>
                                <span className="value" style={{ color: COLORS.S }}>{fmt(F_shifted, 2)}</span>
                            </div>
                            <div className="breakdown-item border-l-4" style={{ borderLeftColor: COLORS.K }}>
                                <span className="label">Shifted Strike (K')</span>
                                <span className="value" style={{ color: COLORS.K }}>{fmt(K_shifted, 2)}</span>
                            </div>
                        </div>

                        <div className="mt-3 p-2 bg-blue-50 rounded text-xs text-blue-900">
                            <strong>Key Insight:</strong> Notice that F' - K' = (F+β) - (K+β) = F - K = {fmt(F - K, 2)}.
                            The shift <strong>cancels out</strong> in the distance term but <strong>affects the probabilities</strong> N(d_β) and n(d_β).
                        </div>
                    </div>
                )}
            </div>

            {/* --- STEP 2: SHIFTED DISTRIBUTION --- */}
            <div className={`step-card ${expanded[2] ? 'open' : ''}`}>
                <div className="step-trigger" onClick={() => toggleStep(2)}>
                    <div className="step-info">
                        <span className="step-circle">2</span>
                        <span className="step-title-text">Shifted Normal Distribution</span>
                    </div>
                    <div className="step-summary-right">
                        <span className="mono-val">N(d_β) = {fmt(N_d, 4)}</span>
                        {expanded[2] ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                    </div>
                </div>

                {expanded[2] && (
                    <div className="step-content">
                        <p className="step-desc text-xs text-muted mb-4">
                            The shift <strong>β={fmt(beta, 1)}</strong> moves the entire distribution {beta > 0 ? 'rightward' : beta < 0 ? 'leftward' : 'not at all'}.
                            This changes which regions have higher probability density.
                        </p>

                        <div style={{ height: '160px', width: '100%', marginBottom: '10px' }}>
                            <ResponsiveContainer width="100%" height="100%">
                                <AreaChart data={distributionData.data}>
                                    <defs>
                                        <linearGradient id="modBachelierFill" x1="0" y1="0" x2="1" y2="0">
                                            <stop offset="0%" stopColor="#f43f5e" stopOpacity={isCall ? 0 : 0.4} />
                                            <stop offset="100%" stopColor="#f43f5e" stopOpacity={isCall ? 0.4 : 0} />
                                        </linearGradient>
                                    </defs>
                                    <XAxis
                                        dataKey="price"
                                        type="number"
                                        domain={['auto', 'auto']}
                                        tickFormatter={(v) => v.toFixed(0)}
                                        tick={{ fontSize: 10 }}
                                        interval="preserveStartEnd"
                                    />
                                    <YAxis hide />

                                    <RechartsTooltip
                                        formatter={(val) => val.toFixed(5)}
                                        labelFormatter={(label) => `Price: ${parseFloat(label).toFixed(2)}`}
                                    />

                                    {/* The Shifted Normal Curve */}
                                    <Area
                                        type="monotone"
                                        dataKey="density"
                                        stroke="#f43f5e"
                                        fill="none"
                                        strokeWidth={2}
                                        isAnimationActive={false}
                                    />

                                    {/* The Shaded ITM Area */}
                                    <Area
                                        type="monotone"
                                        dataKey="fill"
                                        stroke="none"
                                        fill="#f43f5e"
                                        fillOpacity={0.3}
                                        isAnimationActive={false}
                                    />

                                    {/* Original Strike Line */}
                                    <ReferenceLine x={K} stroke="#94a3b8" strokeWidth={1} strokeDasharray="3 3" label={{ value: 'K', fill: '#94a3b8', fontSize: 9, position: 'top' }} />

                                    {/* Shifted Strike Line */}
                                    <ReferenceLine x={K_shifted} stroke="#ec4899" strokeWidth={2} label={{ value: "K'", fill: '#ec4899', fontSize: 10, position: 'top' }} />

                                    {/* Shifted Forward Line */}
                                    <ReferenceLine x={distributionData.fwd_shifted} stroke="#f43f5e" strokeDasharray="3 3" label={{ value: "F'", fill: '#f43f5e', fontSize: 10, position: 'top' }} />

                                </AreaChart>
                            </ResponsiveContainer>
                        </div>

                        <div className="probability-table">
                            <div className="prob-row">
                                <div className="prob-label">
                                    <div className="flex items-center gap-2">
                                        <InlineMath math={`N(${isCall ? '' : '-'}d_\\beta)`} />
                                        <span className="text-xs font-bold bg-rose-100 text-rose-800 px-1 rounded">Probability</span>
                                    </div>
                                    <span className="prob-desc mt-1">ITM Probability (shifted)</span>
                                </div>
                                <div className="text-right">
                                    <div className="prob-val text-rose-600">{fmt(isCall ? N_d : N_minus_d, 4)}</div>
                                    <div className="text-[10px] text-muted leading-tight max-w-[150px]">
                                        {fmt((isCall ? N_d : N_minus_d) * 100, 2)}% chance given shifted distribution.
                                    </div>
                                </div>
                            </div>

                            <div className="prob-row">
                                <div className="prob-label">
                                    <div className="flex items-center gap-2">
                                        <InlineMath math={`n(d_\\beta)`} />
                                        <span className="text-xs font-bold bg-amber-100 text-amber-800 px-1 rounded">Density</span>
                                    </div>
                                    <span className="prob-desc mt-1">Normal PDF at d_β</span>
                                </div>
                                <div className="text-right">
                                    <div className="prob-val text-amber-600">{fmt(n_d, 4)}</div>
                                    <div className="text-[10px] text-muted leading-tight max-w-[150px]">
                                        Probability density for volatility term.
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div className="mt-3 p-2 bg-purple-50 rounded text-xs text-purple-900">
                            <strong>Effect of β:</strong> {beta > 0 ?
                                `Positive β shifts distribution right, potentially increasing call value for OTM strikes.` :
                                beta < 0 ?
                                    `Negative β shifts distribution left, potentially increasing put value for OTM strikes.` :
                                    `β=0 gives standard Bachelier with no shift - identical probabilities to classic model.`}
                        </div>
                    </div>
                )}
            </div>

            {/* --- STEP 3: VALUATION --- */}
            <div className={`step-card ${expanded[3] ? 'open' : ''}`}>
                <div className="step-trigger" onClick={() => toggleStep(3)}>
                    <div className="step-info">
                        <span className="step-circle">3</span>
                        <span className="step-title-text">Modified Bachelier Valuation</span>
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
                            {/* Distance Term (shift cancels out!) */}
                            <div className="receipt-row positive">
                                <div className="receipt-label">
                                    <span className="r-title" style={{ color: COLORS.S }}>Distance Term</span>
                                    <span className="r-sub">(F - K) × N(d_β) × e^(-rT)</span>
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
                                    <span className="r-sub">σ√T × n(d_β) × e^(-rT)</span>
                                </div>
                                <div className="receipt-value" style={{ color: COLORS.sigma }}>
                                    {fmt(df * sigma_sqrt_T * n_d, 3)}
                                </div>
                            </div>

                            {/* Total */}
                            <div className="receipt-total-line"></div>
                            <div className="receipt-row total">
                                <div className="receipt-label">Modified Bachelier Price</div>
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
                            <strong>Distance Invariance:</strong> Notice (F - K) appears, not (F' - K'). The shift β modifies the
                            <strong> probabilities</strong> N(d_β) and n(d_β), but the intrinsic distance remains F - K = {fmt(F - K, 2)}.
                        </div>
                    </div>
                )}
            </div>

            {/* --- STEP 4: CALIBRATION INSIGHT --- */}
            <div className={`step-card ${expanded[4] ? 'open' : ''}`}>
                <div className="step-trigger" onClick={() => toggleStep(4)}>
                    <div className="step-info">
                        <span className="step-circle">4</span>
                        <span className="step-title-text">Why Use a Shift?</span>
                    </div>
                    <div className="step-summary-right">
                        <span className="text-xs text-muted">Market Calibration</span>
                        {expanded[4] ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                    </div>
                </div>

                {expanded[4] && (
                    <div className="step-content">
                        <div className="grid grid-cols-2 gap-3 text-xs">
                            <div className="p-3 bg-blue-50 rounded border border-blue-200">
                                <div className="font-semibold text-blue-900 mb-2">β = 0 (Standard Bachelier)</div>
                                <div className="text-blue-800">
                                    • Simple, fast computation<br />
                                    • Symmetric distribution<br />
                                    • May not match market prices<br />
                                    • Good for quick estimates
                                </div>
                            </div>

                            <div className="p-3 bg-rose-50 rounded border border-rose-200">
                                <div className="font-semibold text-rose-900 mb-2">β ≠ 0 (Modified)</div>
                                <div className="text-rose-800">
                                    • Better market calibration<br />
                                    • Flexible probability adjustment<br />
                                    • Matches volatility smile<br />
                                    • One extra parameter to fit
                                </div>
                            </div>
                        </div>

                        <div className="mt-3 p-3 bg-purple-50 rounded border border-purple-200 text-xs">
                            <div className="font-semibold text-purple-900 mb-2">📊 Typical Use Cases:</div>
                            <ul className="text-purple-800 space-y-1 ml-4">
                                <li><strong>Interest Rate Options:</strong> Adjust β to match caps/floors prices</li>
                                <li><strong>Volatility Smile:</strong> Better fit than pure Bachelier, simpler than SABR</li>
                                <li><strong>OTM Options:</strong> Shift can increase/decrease tail probabilities</li>
                                <li><strong>Model Interpolation:</strong> Smoothly transition between pricing regimes</li>
                            </ul>
                        </div>

                        <div className="mt-3 p-2 bg-green-50 rounded text-xs text-green-900">
                            <strong>🎯 Calibration Tip:</strong> Start with β=0 (Bachelier). If market prices are higher/lower than model,
                            adjust β accordingly. Positive β typically increases OTM call values, negative β increases OTM put values.
                        </div>
                    </div>
                )}
            </div>

            <ModelExplanation data={TEXTBOOK_DATA.mod_bachelier} />
        </div>
    );
};

export default ModifiedBachelierWalkthrough;

// --- START OF FILE src/models/SamuelsonWalkthrough.jsx ---

import React, { useState, useMemo } from 'react';
import { BlockMath, InlineMath } from 'react-katex';
import { ArrowRight, ChevronDown, ChevronUp, BookOpen, Award, TrendingUp, Users } from 'lucide-react';
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
    mu: "#0891b2",    // Cyan-600 (for Samuelson's expected return)
    sigma: "#8b5cf6", // Violet-500
    samuelson: "#0891b2", // Cyan-600 (Samuelson's signature color)
};

const SamuelsonWalkthrough = ({ inputs, results, showNumbers }) => {
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
    const mu = inputs.rate || 0.10;  // Expected return (Samuelson's μ)
    const v = inputs.volatility || 0.30;
    const isCall = inputs.type === 'call';

    // Extract Results from Backend
    const { price, note } = results;
    const greeks = results.greeks || {};

    // Local Calculations for Samuelson (similar to Sprenkle/Boness)
    const ln_SK = Math.log(S / K);
    const drift = (mu + v * v / 2) * T;
    const vol_term = v * Math.sqrt(T);

    const d1 = (ln_SK + drift) / vol_term;
    const d2 = d1 - vol_term;

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

    const N_d1 = norm_cdf(d1);
    const N_d2 = norm_cdf(d2);
    const N_minus_d1 = norm_cdf(-d1);
    const N_minus_d2 = norm_cdf(-d2);
    const n_d1 = norm_pdf(d1);

    const emu_T = Math.exp(mu * T);
    const r = mu; // For Samuelson, r is interpreted as expected return

    // --- CHART LOGIC: LOGNORMAL DISTRIBUTION ---
    const distributionData = useMemo(() => {
        const points = [];
        const steps = 60;

        const expected = S * emu_T;
        const mu_ln = Math.log(S) + (mu - 0.5 * v * v) * T;
        const sigma_ln = v * Math.sqrt(T);

        let minX = Math.max(0.1, expected - 3 * expected * v * Math.sqrt(T));
        let maxX = expected + 3 * expected * v * Math.sqrt(T);

        if (K < minX) minX = K * 0.7;
        if (K > maxX) maxX = K * 1.3;

        const range = maxX - minX;
        const stepSize = range / steps;

        for (let i = 0; i <= steps; i++) {
            const x = minX + i * stepSize;
            if (x <= 0) continue;

            const term1 = 1 / (x * sigma_ln * Math.sqrt(2 * Math.PI));
            const term2 = Math.exp(-Math.pow(Math.log(x) - mu_ln, 2) / (2 * sigma_ln * sigma_ln));
            const density = term1 * term2;

            let fillValue = 0;
            if (isCall && x >= K) fillValue = density;
            if (!isCall && x <= K) fillValue = density;

            points.push({
                price: x,
                density: density,
                fill: fillValue
            });
        }

        return { data: points, expected };
    }, [S, K, T, mu, v, isCall, emu_T]);

    // --- DYNAMIC LATEX GENERATOR ---
    const V = (symbol, value, colorKey) => {
        const color = COLORS[colorKey];
        if (showNumbers) {
            return `\\textcolor{${color}}{${fmt(value, 3)}}`;
        }
        return `\\textcolor{${color}}{${symbol}}`;
    };

    const d1_formula = `\\frac{\\ln(${V('S', S, 'S')}/${V('K', K, 'K')}) + (${V('\\mu', mu, 'mu')} + ${V('\\sigma', v, 'sigma')}^2/2)${V('T', T, 'T')}}{${V('\\sigma', v, 'sigma')}\\sqrt{${V('T', T, 'T')}}}`;

    const call_formula = `${V('S', S, 'S')} e^{${V('\\mu', mu, 'mu')}${V('T', T, 'T')}} N(d_1) - ${V('K', K, 'K')} N(d_2)`;
    const put_formula = `${V('K', K, 'K')} N(-d_2) - ${V('S', S, 'S')} e^{${V('\\mu', mu, 'mu')}${V('T', T, 'T')}} N(-d_1)`;

    return (
        <div className="math-steps">

            {/* INFO BANNER */}
            <div className="info-banner mb-4 p-3 bg-cyan-50 border border-cyan-200 rounded-lg">
                <div className="flex items-start gap-2">
                    <Award size={18} className="text-cyan-600 mt-0.5 flex-shrink-0" />
                    <div className="text-xs text-cyan-900">
                        <strong>Samuelson (1965)</strong> - Another independent discovery of lognormal option pricing!
                        Published alongside Sprenkle & Boness, contributed to the intellectual foundation that led to BSM (1973).
                    </div>
                </div>
            </div>

            {/* HISTORICAL BANNER */}
            <div className="info-banner mb-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
                <div className="flex items-start gap-2">
                    <Users size={18} className="text-blue-600 mt-0.5 flex-shrink-0" />
                    <div className="text-xs text-blue-900">
                        <strong>1964-1965:</strong> Three economists (Sprenkle, Boness, Samuelson) independently reached similar conclusions!
                        All used <strong>lognormal distributions</strong> and <strong>expected returns</strong>, setting the stage for BSM's breakthrough.
                    </div>
                </div>
            </div>

            {/* --- STEP 1: LOGNORMAL PARAMETERS --- */}
            <div className={`step-card ${expanded[1] ? 'open' : ''}`}>
                <div className="step-trigger" onClick={() => toggleStep(1)}>
                    <div className="step-info">
                        <span className="step-circle">1</span>
                        <span className="step-title-text">Calculate d₁ and d₂ (Lognormal)</span>
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
                            <BlockMath math={`d_2 = d_1 - ${V('\\sigma', v, 'sigma')}\\sqrt{${V('T', T, 'T')}} = ${fmt(d1, 4)} - ${fmt(vol_term, 4)} = ${fmt(d2, 4)}`} />
                        </div>

                        <div className="breakdown-grid">
                            <div className="breakdown-item border-l-4" style={{ borderLeftColor: COLORS.S }}>
                                <span className="label">Moneyness ln(S/K)</span>
                                <span className="value" style={{ color: COLORS.S }}>{fmt(ln_SK)}</span>
                            </div>
                            <div className="breakdown-item border-l-4" style={{ borderLeftColor: COLORS.mu }}>
                                <span className="label">Drift Term (μ + σ²/2)T</span>
                                <span className="value" style={{ color: COLORS.mu }}>{fmt(drift)}</span>
                            </div>
                            <div className="breakdown-item border-l-4" style={{ borderLeftColor: COLORS.sigma }}>
                                <span className="label">Volatility Term σ√T</span>
                                <span className="value" style={{ color: COLORS.sigma }}>{fmt(vol_term)}</span>
                            </div>
                        </div>

                        <div className="mt-3 p-2 bg-cyan-50 rounded text-xs text-cyan-900">
                            <strong>Samuelson's Insight:</strong> Like Sprenkle and Boness, Samuelson recognized that stock prices follow a
                            <strong> lognormal distribution</strong>, using expected return μ in the drift term. This was a major advance over Bachelier!
                        </div>
                    </div>
                )}
            </div>

            {/* --- STEP 2: LOGNORMAL DISTRIBUTION --- */}
            <div className={`step-card ${expanded[2] ? 'open' : ''}`}>
                <div className="step-trigger" onClick={() => toggleStep(2)}>
                    <div className="step-info">
                        <span className="step-circle">2</span>
                        <span className="step-title-text">Lognormal Distribution</span>
                    </div>
                    <div className="step-summary-right">
                        <span className="mono-val">E[S] = {fmt(distributionData.expected, 0)}</span>
                        {expanded[2] ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                    </div>
                </div>

                {expanded[2] && (
                    <div className="step-content">
                        <p className="step-desc text-xs text-muted mb-4">
                            Samuelson's model uses the <strong>lognormal distribution</strong>, ensuring stock prices remain positive.
                            Expected value grows by <strong>e^(μT) = {fmt(emu_T, 4)}</strong>.
                        </p>

                        <div style={{ height: '160px', width: '100%', marginBottom: '10px' }}>
                            <ResponsiveContainer width="100%" height="100%">
                                <AreaChart data={distributionData.data}>
                                    <defs>
                                        <linearGradient id="samuelsonFill" x1="0" y1="0" x2="1" y2="0">
                                            <stop offset="0%" stopColor="#0891b2" stopOpacity={isCall ? 0 : 0.4} />
                                            <stop offset="100%" stopColor="#0891b2" stopOpacity={isCall ? 0.4 : 0} />
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
                                        labelFormatter={(label) => `Price: $${parseFloat(label).toFixed(2)}`}
                                    />

                                    <Area
                                        type="monotone"
                                        dataKey="density"
                                        stroke="#0891b2"
                                        fill="none"
                                        strokeWidth={2}
                                        isAnimationActive={false}
                                    />

                                    <Area
                                        type="monotone"
                                        dataKey="fill"
                                        stroke="none"
                                        fill="#0891b2"
                                        fillOpacity={0.3}
                                        isAnimationActive={false}
                                    />

                                    <ReferenceLine x={K} stroke="#ec4899" strokeWidth={2} label={{ value: 'Strike', fill: '#ec4899', fontSize: 10, position: 'top' }} />
                                    <ReferenceLine x={distributionData.expected} stroke="#0891b2" strokeDasharray="3 3" label={{ value: `E[S]=${fmt(distributionData.expected, 0)}`, fill: '#0891b2', fontSize: 9, position: 'top' }} />
                                </AreaChart>
                            </ResponsiveContainer>
                        </div>

                        <div className="probability-table">
                            <div className="prob-row">
                                <div className="prob-label">
                                    <div className="flex items-center gap-2">
                                        <InlineMath math={`N(${isCall ? '' : '-'}d_1)`} />
                                        <span className="text-xs font-bold bg-cyan-100 text-cyan-800 px-1 rounded">Spot Weight</span>
                                    </div>
                                    <span className="prob-desc mt-1">Probability weighting for growing spot</span>
                                </div>
                                <div className="text-right">
                                    <div className="prob-val text-cyan-600">{fmt(isCall ? N_d1 : N_minus_d1, 4)}</div>
                                </div>
                            </div>

                            <div className="prob-row">
                                <div className="prob-label">
                                    <div className="flex items-center gap-2">
                                        <InlineMath math={`N(${isCall ? '' : '-'}d_2)`} />
                                        <span className="text-xs font-bold bg-pink-100 text-pink-800 px-1 rounded">Strike Weight</span>
                                    </div>
                                    <span className="prob-desc mt-1">Applied to undiscounted strike</span>
                                </div>
                                <div className="text-right">
                                    <div className="prob-val text-pink-600">{fmt(isCall ? N_d2 : N_minus_d2, 4)}</div>
                                </div>
                            </div>
                        </div>

                        <div className="mt-3 p-2 bg-blue-50 rounded text-xs text-blue-900">
                            <strong>Right-Skewed:</strong> The lognormal distribution has a <strong>positive skew</strong>, meaning there's more
                            upside potential than downside risk. This matches real stock price behavior!
                        </div>
                    </div>
                )}
            </div>

            {/* --- STEP 3: SAMUELSON VALUATION --- */}
            <div className={`step-card ${expanded[3] ? 'open' : ''}`}>
                <div className="step-trigger" onClick={() => toggleStep(3)}>
                    <div className="step-info">
                        <span className="step-circle">3</span>
                        <span className="step-title-text">Samuelson Valuation</span>
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
                            {/* Spot Term */}
                            <div className="receipt-row positive">
                                <div className="receipt-label">
                                    <span className="r-title" style={{ color: COLORS.samuelson }}>Spot Term (with μ growth)</span>
                                    <span className="r-sub">S × e^(μT) × N(d₁)</span>
                                </div>
                                <div className="receipt-value" style={{ color: COLORS.samuelson }}>
                                    {fmt(S * emu_T * (isCall ? N_d1 : (1 - N_minus_d1)), 3)}
                                </div>
                            </div>

                            <div className="receipt-divider">
                                <span className="text-xs">−</span>
                            </div>

                            {/* Strike Term (NO DISCOUNTING) */}
                            <div className="receipt-row negative">
                                <div className="receipt-label">
                                    <span className="r-title" style={{ color: COLORS.K }}>Strike Term (no discount)</span>
                                    <span className="r-sub">K × N(d₂)</span>
                                </div>
                                <div className="receipt-value" style={{ color: COLORS.K }}>
                                    {fmt(K * (isCall ? N_d2 : N_minus_d2), 3)}
                                </div>
                            </div>

                            {/* Total */}
                            <div className="receipt-total-line"></div>
                            <div className="receipt-row total">
                                <div className="receipt-label">Samuelson Price</div>
                                <div className="receipt-value">${fmt(price, 2)}</div>
                            </div>
                        </div>

                        {note && (
                            <div className="mt-3 p-2 bg-blue-50 rounded text-xs">
                                <div className="font-semibold text-blue-900 mb-1">Comparison:</div>
                                <div className="text-blue-800">{note}</div>
                            </div>
                        )}

                        <div className="mt-3 p-2 bg-amber-50 border border-amber-200 rounded text-xs text-amber-900">
                            <strong>⚠️ Samuelson's Formula:</strong> Like Sprenkle, Samuelson used μ (expected return) and <strong>did not discount the strike</strong>.
                            The strike K appears without e^(-rT), which was later corrected by Boness and BSM!
                        </div>
                    </div>
                )}
            </div>

            {/* --- STEP 4: CONVERGENCE TO BSM --- */}
            <div className={`step-card ${expanded[4] ? 'open' : ''}`}>
                <div className="step-trigger" onClick={() => toggleStep(4)}>
                    <div className="step-info">
                        <span className="step-circle">4</span>
                        <span className="step-title-text">The Path to Black-Scholes</span>
                    </div>
                    <div className="step-summary-right">
                        <span className="text-xs text-muted">1965 → 1973</span>
                        {expanded[4] ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                    </div>
                </div>

                {expanded[4] && (
                    <div className="step-content">
                        <div className="p-3 bg-purple-50 rounded border border-purple-200 mb-3">
                            <div className="text-xs font-semibold text-purple-900 mb-2">📚 The 1964-1965 Breakthrough:</div>
                            <div className="text-purple-800 text-[11px]">
                                Three economists independently discovered lognormal option pricing:
                                <ul className="ml-4 mt-2 space-y-1">
                                    <li><strong>Sprenkle (1964)</strong>: Lognormal + μ, no strike discount</li>
                                    <li><strong>Boness (1964)</strong>: Lognormal + μ, WITH strike discount ✅</li>
                                    <li><strong>Samuelson (1965)</strong>: Lognormal + μ, no strike discount</li>
                                </ul>
                                <div className="mt-2">
                                    All three were <strong>so close</strong> to the complete answer!
                                </div>
                            </div>
                        </div>

                        {/* Comparison Table */}
                        <div className="p-3 bg-green-50 rounded border border-green-200 mb-3">
                            <div className="text-xs font-semibold text-green-900 mb-2">📊 Feature Comparison:</div>
                            <table className="w-full text-[10px] text-green-800">
                                <tr className="border-b border-green-300">
                                    <th className="text-left py-1">Model</th>
                                    <th className="text-left py-1">Distribution</th>
                                    <th className="text-left py-1">Drift</th>
                                    <th className="text-left py-1">Strike Discount</th>
                                </tr>
                                <tr className="border-b border-green-100">
                                    <td className="py-1">Sprenkle (1964)</td>
                                    <td>Lognormal ✅</td>
                                    <td>μ</td>
                                    <td>❌ No</td>
                                </tr>
                                <tr className="border-b border-green-100">
                                    <td className="py-1">Boness (1964)</td>
                                    <td>Lognormal ✅</td>
                                    <td>μ</td>
                                    <td>✅ Yes</td>
                                </tr>
                                <tr className="border-b border-green-100">
                                    <td className="py-1 font-bold">Samuelson (1965)</td>
                                    <td className="font-bold">Lognormal ✅</td>
                                    <td className="font-bold">μ</td>
                                    <td className="font-bold">❌ No</td>
                                </tr>
                                <tr>
                                    <td className="py-1 text-green-900">BSM (1973)</td>
                                    <td className="text-green-900">Lognormal ✅</td>
                                    <td className="text-green-900 font-bold">r ✅</td>
                                    <td className="text-green-900">✅ Yes</td>
                                </tr>
                            </table>
                        </div>

                        {/* Timeline */}
                        <div className="p-3 bg-amber-50 rounded border border-amber-200 mb-3">
                            <div className="text-xs font-semibold text-amber-900 mb-2">🕐 Timeline to BSM:</div>
                            <div className="space-y-2 text-[11px] text-amber-800">
                                <div className="flex items-start gap-2">
                                    <div className="font-mono font-bold min-w-[60px]">1900:</div>
                                    <div>Bachelier - Normal distribution (first model!)</div>
                                </div>
                                <div className="flex items-start gap-2">
                                    <div className="font-mono font-bold min-w-[60px]">1964:</div>
                                    <div>Sprenkle & Boness - Lognormal breakthrough</div>
                                </div>
                                <div className="flex items-start gap-2">
                                    <div className="font-mono font-bold min-w-[60px] text-cyan-700">1965:</div>
                                    <div className="font-bold text-cyan-700">Samuelson - Independent lognormal model</div>
                                </div>
                                <div className="flex items-start gap-2">
                                    <div className="font-mono font-bold min-w-[60px] text-green-700">1973:</div>
                                    <div className="font-bold text-green-700">Black-Scholes-Merton - Risk-neutral pricing! 🏆</div>
                                </div>
                            </div>
                        </div>

                        <div className="p-2 bg-blue-50 rounded text-xs text-blue-900">
                            <strong>🎓 BSM's Final Insight:</strong> Black, Scholes, and Merton realized that you should use the
                            <strong> risk-free rate r</strong> (not expected return μ) in a <strong>risk-neutral world</strong>.
                            This made pricing preference-free and led to the Nobel Prize! 🏆
                        </div>
                    </div>
                )}
            </div>

            <ModelExplanation data={TEXTBOOK_DATA.samuelson} />
        </div>
    );
};

export default SamuelsonWalkthrough;

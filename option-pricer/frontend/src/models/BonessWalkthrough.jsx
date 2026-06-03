// --- START OF FILE src/models/BonessWalkthrough.jsx ---

import React, { useState, useMemo } from 'react';
import { BlockMath, InlineMath } from 'react-katex';
import { ArrowRight, ChevronDown, ChevronUp, Minus, Check, TrendingUp, DollarSign } from 'lucide-react';
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
    mu: "#059669",    // Emerald-600 (for expected return)
    sigma: "#8b5cf6", // Violet-500
    discount: "#dc2626", // Red-600 (for discounting)
};

const BonessWalkthrough = ({ inputs, results, showNumbers }) => {
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
    const mu = inputs.rate || 0.10;  // Expected return (same as r in our implementation)
    const r = mu;  // In Boness, we use same value for both
    const v = inputs.volatility || 0.30;
    const isCall = inputs.type === 'call';

    // Extract Results from Backend
    const { price, note } = results;
    const greeks = results.greeks || {};

    // Local Calculations for Boness
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
    const df = Math.exp(-r * T);  // Discount factor!

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

    const call_formula = `${V('S', S, 'S')} e^{${V('\\mu', mu, 'mu')}${V('T', T, 'T')}} N(d_1) - ${V('K', K, 'K')} \\textcolor{${COLORS.discount}}{e^{-${V('r', r, 'r')}${V('T', T, 'T')}}} N(d_2)`;
    const put_formula = `${V('K', K, 'K')} \\textcolor{${COLORS.discount}}{e^{-${V('r', r, 'r')}${V('T', T, 'T')}}} N(-d_2) - ${V('S', S, 'S')} e^{${V('\\mu', mu, 'mu')}${V('T', T, 'T')}} N(-d_1)`;

    return (
        <div className="math-steps">

            {/* INFO BANNER */}
            <div className="info-banner mb-4 p-3 bg-green-50 border border-green-200 rounded-lg">
                <div className="flex items-start gap-2">
                    <Check size={18} className="text-green-600 mt-0.5 flex-shrink-0" />
                    <div className="text-xs text-green-900">
                        <strong>Boness (1964)</strong> improved on Sprenkle by adding <strong>proper strike discounting</strong>!
                        Uses lognormal distribution with <strong>μ</strong> (expected return) in drift AND <strong>e^(-rT)</strong> on strike.
                        This is the <strong>closest model to BSM</strong> before 1973!
                    </div>
                </div>
            </div>

            {/* IMPROVEMENT BANNER */}
            <div className="info-banner mb-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
                <div className="flex items-start gap-2">
                    <TrendingUp size={18} className="text-blue-600 mt-0.5 flex-shrink-0" />
                    <div className="text-xs text-blue-900">
                        <strong>Key Innovation:</strong> Boness recognized that the strike should be discounted to present value using <strong>e^(-rT)</strong>.
                        Only remaining difference from BSM: uses <strong>μ</strong> (subjective expected return) instead of <strong>r</strong> (objective risk-free rate) in the drift.
                    </div>
                </div>
            </div>

            {/* --- STEP 1: LOGNORMAL PARAMETERS (d1, d2) --- */}
            <div className={`step-card ${expanded[1] ? 'open' : ''}`}>
                <div className="step-trigger" onClick={() => toggleStep(1)}>
                    <div className="step-info">
                        <span className="step-circle">1</span>
                        <span className="step-title-text">Calculate d₁ and d₂ (Same as Sprenkle)</span>
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

                        <div className="mt-3 p-2 bg-purple-50 rounded text-xs text-purple-900">
                            <strong>Same as Sprenkle!</strong> Boness uses identical d₁ and d₂ formulas with μ in the drift.
                            The improvement comes in <strong>Step 3</strong> where the strike gets discounted!
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
                            Boness uses <strong>lognormal distribution</strong> (same as Sprenkle and BSM).
                            Expected value grows by <strong>e^(μT) = {fmt(emu_T, 4)}</strong> using expected return μ={fmt(mu * 100, 1)}%.
                        </p>

                        <div style={{ height: '160px', width: '100%', marginBottom: '10px' }}>
                            <ResponsiveContainer width="100%" height="100%">
                                <AreaChart data={distributionData.data}>
                                    <defs>
                                        <linearGradient id="bonessFill" x1="0" y1="0" x2="1" y2="0">
                                            <stop offset="0%" stopColor="#10b981" stopOpacity={isCall ? 0 : 0.4} />
                                            <stop offset="100%" stopColor="#10b981" stopOpacity={isCall ? 0.4 : 0} />
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
                                        stroke="#10b981"
                                        fill="none"
                                        strokeWidth={2}
                                        isAnimationActive={false}
                                    />

                                    <Area
                                        type="monotone"
                                        dataKey="fill"
                                        stroke="none"
                                        fill="#10b981"
                                        fillOpacity={0.3}
                                        isAnimationActive={false}
                                    />

                                    <ReferenceLine x={K} stroke="#ec4899" strokeWidth={2} label={{ value: 'Strike', fill: '#ec4899', fontSize: 10, position: 'top' }} />
                                    <ReferenceLine x={distributionData.expected} stroke="#059669" strokeDasharray="3 3" label={{ value: `E[S]=${fmt(distributionData.expected, 0)}`, fill: '#059669', fontSize: 9, position: 'top' }} />
                                </AreaChart>
                            </ResponsiveContainer>
                        </div>

                        <div className="probability-table">
                            <div className="prob-row">
                                <div className="prob-label">
                                    <div className="flex items-center gap-2">
                                        <InlineMath math={`N(${isCall ? '' : '-'}d_1)`} />
                                        <span className="text-xs font-bold bg-emerald-100 text-emerald-800 px-1 rounded">Spot Weight</span>
                                    </div>
                                    <span className="prob-desc mt-1">Applied to growing spot</span>
                                </div>
                                <div className="text-right">
                                    <div className="prob-val text-emerald-600">{fmt(isCall ? N_d1 : N_minus_d1, 4)}</div>
                                </div>
                            </div>

                            <div className="prob-row">
                                <div className="prob-label">
                                    <div className="flex items-center gap-2">
                                        <InlineMath math={`N(${isCall ? '' : '-'}d_2)`} />
                                        <span className="text-xs font-bold bg-red-100 text-red-800 px-1 rounded">Strike Weight</span>
                                    </div>
                                    <span className="prob-desc mt-1">Applied to DISCOUNTED strike</span>
                                </div>
                                <div className="text-right">
                                    <div className="prob-val text-red-600">{fmt(isCall ? N_d2 : N_minus_d2, 4)}</div>
                                    <div className="text-[10px] text-muted">
                                        Boness improvement: K gets e^(-rT)!
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                )}
            </div>

            {/* --- STEP 3: BONESS VALUATION (WITH DISCOUNTING!) --- */}
            <div className={`step-card ${expanded[3] ? 'open' : ''}`}>
                <div className="step-trigger" onClick={() => toggleStep(3)}>
                    <div className="step-info">
                        <span className="step-circle">3</span>
                        <span className="step-title-text">Boness Valuation (WITH Discounting!)</span>
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
                                    <span className="r-title" style={{ color: COLORS.S }}>Spot Term (with μ growth)</span>
                                    <span className="r-sub">S × e^(μT) × N(d₁)</span>
                                </div>
                                <div className="receipt-value" style={{ color: COLORS.S }}>
                                    {fmt(S * emu_T * (isCall ? N_d1 : (1 - N_minus_d1)), 3)}
                                </div>
                            </div>

                            <div className="receipt-divider">
                                <Minus size={14} />
                            </div>

                            {/* Strike Term (WITH DISCOUNTING!) */}
                            <div className="receipt-row negative">
                                <div className="receipt-label">
                                    <span className="r-title" style={{ color: COLORS.discount }}>Strike Term (WITH e^(-rT)!) ✅</span>
                                    <span className="r-sub">K × e^(-rT) × N(d₂)</span>
                                </div>
                                <div className="receipt-value" style={{ color: COLORS.discount }}>
                                    {fmt(K * df * (isCall ? N_d2 : N_minus_d2), 3)}
                                </div>
                            </div>

                            {/* Breakdown of discounting */}
                            <div className="mt-3 p-3 bg-green-50 border border-green-200 rounded">
                                <div className="text-xs font-semibold text-green-900 mb-2">Discount Factor Breakdown:</div>
                                <div className="grid grid-cols-3 gap-2 text-[11px]">
                                    <div>
                                        <div className="text-green-700">Strike K</div>
                                        <div className="font-mono text-green-900">{fmt(K, 2)}</div>
                                    </div>
                                    <div>
                                        <div className="text-green-700">× e^(-rT)</div>
                                        <div className="font-mono text-green-900">{fmt(df, 4)}</div>
                                    </div>
                                    <div>
                                        <div className="text-green-700">= Present Value</div>
                                        <div className="font-mono font-bold text-green-900">{fmt(K * df, 2)}</div>
                                    </div>
                                </div>
                            </div>

                            {/* Total */}
                            <div className="receipt-total-line"></div>
                            <div className="receipt-row total">
                                <div className="receipt-label">Boness Price</div>
                                <div className="receipt-value">${fmt(price, 2)}</div>
                            </div>
                        </div>

                        {note && (
                            <div className="mt-3 p-2 bg-blue-50 rounded text-xs">
                                <div className="font-semibold text-blue-900 mb-1">Comparison:</div>
                                <div className="text-blue-800">{note}</div>
                            </div>
                        )}

                        <div className="mt-3 p-2 bg-green-50 border border-green-200 rounded text-xs text-green-900">
                            <strong>✅ Boness's Improvement:</strong> The strike K is multiplied by <strong>e^(-{fmt(r, 2)}×{fmt(T, 1)}) = {fmt(df, 4)}</strong>,
                            properly discounting it to present value. This fixes Sprint's fatal flaw!
                        </div>
                    </div>
                )}
            </div>

            {/* --- STEP 4: SO CLOSE TO BSM! --- */}
            <div className={`step-card ${expanded[4] ? 'open' : ''}`}>
                <div className="step-trigger" onClick={() => toggleStep(4)}>
                    <div className="step-info">
                        <span className="step-circle">4</span>
                        <span className="step-title-text">How Close to BSM?</span>
                    </div>
                    <div className="step-summary-right">
                        <span className="text-xs text-muted">90% there!</span>
                        {expanded[4] ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                    </div>
                </div>

                {expanded[4] && (
                    <div className="step-content">
                        <div className="grid grid-cols-2 gap-3 text-xs mb-3">
                            <div className="p-3 bg-green-50 rounded border border-green-200">
                                <div className="font-semibold text-green-900 mb-2">✅ What Boness Has (like BSM):</div>
                                <div className="text-green-800 space-y-1">
                                    • <strong>Lognormal distribution</strong><br />
                                    • <strong>Strike discounting</strong> e^(-rT)<br />
                                    • Separate μ and r<br />
                                    • Probability weighting<br />
                                    • Two-term formula
                                </div>
                            </div>

                            <div className="p-3 bg-amber-50 rounded border border-amber-200">
                                <div className="font-semibold text-amber-900 mb-2">⚠️ Only Difference from BSM:</div>
                                <div className="text-amber-800 space-y-1">
                                    • Uses <strong>μ</strong> (expected return)<br />
                                    • Spot grows by <strong>e^(μT)</strong><br />
                                    • Not risk-neutral<br />
                                    • Preference-dependent<br />
                                    • No arbitrage proof
                                </div>
                            </div>
                        </div>

                        <div className="p-3 bg-purple-50 rounded border border-purple-200 text-xs mb-3">
                            <div className="font-semibold text-purple-900 mb-2">📐 Formula Comparison:</div>
                            <div className="text-purple-800 space-y-2">
                                <div className="font-mono text-[10px] bg-white p-2 rounded">
                                    <div className="font-bold">Boness (1964):</div>
                                    C = S·e^(μT)·N(d₁) - K·e^(-rT)·N(d₂)
                                </div>
                                <div className="font-mono text-[10px] bg-white p-2 rounded">
                                    <div className="font-bold">BSM (1973):</div>
                                    C = S·N(d₁') - K·e^(-rT)·N(d₂')
                                </div>
                                <div className="text-[11px] mt-2">
                                    <strong>Key:</strong> BSM removed e^(μT) growth and adjusted d₁', d₂' to use r instead of μ in drift!
                                </div>
                            </div>
                        </div>

                        <div className="p-3 bg-blue-50 rounded border border-blue-200 text-xs mb-3">
                            <div className="font-semibold text-blue-900 mb-2">📊 Numerical Example (Current Inputs):</div>
                            <div className="text-blue-800">
                                <table className="w-full text-[10px]">
                                    <tr className="border-b border-blue-200">
                                        <th className="text-left py-1">Model</th>
                                        <th className="text-left py-1">Spot Growth</th>
                                        <th className="text-left py-1">Strike Discount</th>
                                        <th className="text-right py-1">Price</th>
                                    </tr>
                                    <tr className="border-b border-blue-100">
                                        <td className="py-1">Sprenkle</td>
                                        <td>S × {fmt(emu_T, 3)}</td>
                                        <td>❌ None</td>
                                        <td className="text-right font-mono">Lower</td>
                                    </tr>
                                    <tr className="border-b border-blue-100">
                                        <td className="py-1 font-bold">Boness</td>
                                        <td className="font-bold">S × {fmt(emu_T, 3)}</td>
                                        <td className="font-bold">✅ {fmt(df, 3)}</td>
                                        <td className="text-right font-mono font-bold">${fmt(price, 2)}</td>
                                    </tr>
                                    <tr>
                                        <td className="py-1">BSM</td>
                                        <td>S (no growth)</td>
                                        <td>✅ {fmt(df, 3)}</td>
                                        <td className="text-right font-mono">Compare in note</td>
                                    </tr>
                                </table>
                            </div>
                        </div>

                        <div className="p-3 bg-red-50 rounded border border-red-200 text-xs">
                            <div className="font-semibold text-red-900 mb-2">🎯 Why BSM Was Still Needed:</div>
                            <div className="text-red-800">
                                Boness was <strong>so close</strong>, but the final leap required:
                                <ul className="ml-4 mt-1 space-y-1">
                                    <li>• <strong>Risk-neutral valuation</strong> - price in a world where μ = r</li>
                                    <li>• <strong>Replicating portfolio</strong> - show how to hedge</li>
                                    <li>• <strong>No-arbitrage</strong> - rigorous mathematical proof</li>
                                    <li>• <strong>Preference-free</strong> - independent of investor opinions</li>
                                </ul>
                                <div className="mt-2 font-semibold">
                                    That's why Black, Scholes, and Merton won the Nobel Prize! 🏆
                                </div>
                            </div>
                        </div>
                    </div>
                )}
            </div>

            <ModelExplanation data={TEXTBOOK_DATA.boness} />
        </div>
    );
};

export default BonessWalkthrough;

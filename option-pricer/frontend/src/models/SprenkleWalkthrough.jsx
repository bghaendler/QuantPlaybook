// --- START OF FILE src/models/SprenkleWalkthrough.jsx ---

import React, { useState, useMemo } from 'react';
import { BlockMath, InlineMath } from 'react-katex';
import { ArrowRight, ChevronDown, ChevronUp, Minus, HelpCircle, TrendingUp, AlertTriangle } from 'lucide-react';
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
    q: "#06b6d4",     // Cyan-500
};

const SprenkleWalkthrough = ({ inputs, results, showNumbers }) => {
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
    const mu = inputs.rate || 0.10;  // Expected return, not r!
    const v = inputs.volatility || 0.30;
    const isCall = inputs.type === 'call';

    // Extract Results from Backend
    const { price, note } = results;
    const greeks = results.greeks || {};

    // Local Calculations for Sprenkle
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

    // --- CHART LOGIC: LOGNORMAL DISTRIBUTION ---
    const distributionData = useMemo(() => {
        const points = [];
        const steps = 60;

        // Expected value with mu growth
        const expected = S * emu_T;

        // Lognormal parameters
        const mu_ln = Math.log(S) + (mu - 0.5 * v * v) * T;
        const sigma_ln = v * Math.sqrt(T);

        // Determine range
        let minX = Math.max(0.1, expected - 3 * expected * v * Math.sqrt(T));
        let maxX = expected + 3 * expected * v * Math.sqrt(T);

        if (K < minX) minX = K * 0.7;
        if (K > maxX) maxX = K * 1.3;

        const range = maxX - minX;
        const stepSize = range / steps;

        for (let i = 0; i <= steps; i++) {
            const x = minX + i * stepSize;

            if (x <= 0) continue;

            // Lognormal PDF
            const term1 = 1 / (x * sigma_ln * Math.sqrt(2 * Math.PI));
            const term2 = Math.exp(-Math.pow(Math.log(x) - mu_ln, 2) / (2 * sigma_ln * sigma_ln));
            const density = term1 * term2;

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
            <div className="info-banner mb-4 p-3 bg-emerald-50 border border-emerald-200 rounded-lg">
                <div className="flex items-start gap-2">
                    <TrendingUp size={18} className="text-emerald-600 mt-0.5 flex-shrink-0" />
                    <div className="text-xs text-emerald-900">
                        <strong>Sprenkle (1964)</strong> was the first model to use <strong>lognormal distribution</strong> for options!
                        It uses <strong>expected return μ</strong> instead of risk-free rate r, and <strong>does not discount the strike</strong>.
                        This made it more optimistic than BSM but less rigorous (no risk-neutral valuation).
                    </div>
                </div>
            </div>

            {/* WARNING BANNER */}
            <div className="info-banner mb-4 p-3 bg-orange-50 border border-orange-200 rounded-lg">
                <div className="flex items-start gap-2">
                    <AlertTriangle size={18} className="text-orange-600 mt-0.5 flex-shrink-0" />
                    <div className="text-xs text-orange-900">
                        <strong>Key Difference:</strong> In Sprenkle, the "rate" parameter represents <strong>expected return μ={fmt(mu * 100, 1)}%</strong>,
                        NOT risk-free rate. The strike K appears without e^(-rT) discounting, making options more valuable than BSM.
                    </div>
                </div>
            </div>

            {/* --- STEP 1: LOGNORMAL PARAMETERS (d1, d2) --- */}
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

                        <div className="mt-3 p-2 bg-blue-50 rounded text-xs text-blue-900">
                            <strong>Lognormal!</strong> Unlike Bachelier's normal distribution, Sprenkle uses <strong>lognormal</strong>
                            (same as BSM). But notice the drift uses <strong>μ</strong> (expected return, {fmt(mu * 100, 1)}%)
                            instead of <strong>r</strong> (risk-free rate).
                        </div>

                        <div className="calculation-flow mt-3">
                            <span className="calc-math">
                                ({fmt(ln_SK)} + {fmt(drift)}) ÷ {fmt(vol_term)}
                            </span>
                            <ArrowRight size={14} className="mx-2 text-muted" />
                            <span className="mono-val text-primary font-bold">{fmt(d1)}</span>
                        </div>
                    </div>
                )}
            </div>

            {/* --- STEP 2: LOGNORMAL DISTRIBUTION & PROBABILITIES --- */}
            <div className={`step-card ${expanded[2] ? 'open' : ''}`}>
                <div className="step-trigger" onClick={() => toggleStep(2)}>
                    <div className="step-info">
                        <span className="step-circle">2</span>
                        <span className="step-title-text">Lognormal Distribution & Probabilities</span>
                    </div>
                    <div className="step-summary-right">
                        <span className="mono-val">N(d₂) = {fmt(isCall ? N_d2 : N_minus_d2, 4)}</span>
                        {expanded[2] ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                    </div>
                </div>

                {expanded[2] && (
                    <div className="step-content">
                        <p className="step-desc text-xs text-muted mb-4">
                            Sprenkle uses <strong>lognormal distribution</strong> (stock price can't go negative, has right skew).
                            The expected value grows by <strong>e^(μT) = {fmt(emu_T, 4)}</strong> due to expected return μ={fmt(mu * 100, 1)}%.
                        </p>

                        <div style={{ height: '160px', width: '100%', marginBottom: '10px' }}>
                            <ResponsiveContainer width="100%" height="100%">
                                <AreaChart data={distributionData.data}>
                                    <defs>
                                        <linearGradient id="sprenkleFill" x1="0" y1="0" x2="1" y2="0">
                                            <stop offset="0%" stopColor="#059669" stopOpacity={isCall ? 0 : 0.4} />
                                            <stop offset="100%" stopColor="#059669" stopOpacity={isCall ? 0.4 : 0} />
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

                                    {/* The Lognormal Curve */}
                                    <Area
                                        type="monotone"
                                        dataKey="density"
                                        stroke="#059669"
                                        fill="none"
                                        strokeWidth={2}
                                        isAnimationActive={false}
                                    />

                                    {/* The Shaded ITM Area */}
                                    <Area
                                        type="monotone"
                                        dataKey="fill"
                                        stroke="none"
                                        fill="#059669"
                                        fillOpacity={0.3}
                                        isAnimationActive={false}
                                    />

                                    {/* Strike Line */}
                                    <ReferenceLine x={K} stroke="#ec4899" strokeWidth={2} label={{ value: 'Strike', fill: '#ec4899', fontSize: 10, position: 'top' }} />

                                    {/* Expected Value */}
                                    <ReferenceLine x={distributionData.expected} stroke="#059669" strokeDasharray="3 3" label={{ value: `E[S]=${fmt(distributionData.expected, 0)}`, fill: '#059669', fontSize: 9, position: 'top' }} />

                                </AreaChart>
                            </ResponsiveContainer>
                        </div>

                        <div className="probability-table">
                            {/* N(d1) */}
                            <div className="prob-row">
                                <div className="prob-label">
                                    <div className="flex items-center gap-2">
                                        <InlineMath math={`N(${isCall ? '' : '-'}d_1)`} />
                                        <span className="text-xs font-bold bg-emerald-100 text-emerald-800 px-1 rounded">Spot Growth</span>
                                    </div>
                                    <span className="prob-desc mt-1">Probability-weighted spot term</span>
                                </div>
                                <div className="text-right">
                                    <div className="prob-val text-emerald-600">{fmt(isCall ? N_d1 : N_minus_d1, 4)}</div>
                                    <div className="text-[10px] text-muted leading-tight max-w-[150px]">
                                        Weighted by lognormal distribution at d₁.
                                    </div>
                                </div>
                            </div>

                            {/* N(d2) */}
                            <div className="prob-row">
                                <div className="prob-label">
                                    <div className="flex items-center gap-2">
                                        <InlineMath math={`N(${isCall ? '' : '-'}d_2)`} />
                                        <span className="text-xs font-bold bg-blue-100 text-blue-800 px-1 rounded">Strike Term</span>
                                    </div>
                                    <span className="prob-desc mt-1">Probability-weighted strike</span>
                                </div>
                                <div className="text-right">
                                    <div className="prob-val text-blue-600">{fmt(isCall ? N_d2 : N_minus_d2, 4)}</div>
                                    <div className="text-[10px] text-muted leading-tight max-w-[150px]">
                                        Applied to K (no discounting in Sprenkle!).
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div className="mt-3 p-2 bg-purple-50 rounded text-xs text-purple-900">
                            <strong>Right-Skewed:</strong> Lognormal distribution has a longer right tail (large gains more likely than large losses).
                            This is more realistic for stock prices than Bachelier's symmetric normal distribution.
                        </div>
                    </div>
                )}
            </div>

            {/* --- STEP 3: SPRENKLE VALUATION (NO STRIKE DISCOUNTING!) --- */}
            <div className={`step-card ${expanded[3] ? 'open' : ''}`}>
                <div className="step-trigger" onClick={() => toggleStep(3)}>
                    <div className="step-info">
                        <span className="step-circle">3</span>
                        <span className="step-title-text">Sprenkle Valuation (No Discounting!)</span>
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
                            {/* Spot Term with μ growth */}
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

                            {/* Strike Term (NO DISCOUNTING!) */}
                            <div className="receipt-row negative">
                                <div className="receipt-label">
                                    <span className="r-title" style={{ color: COLORS.K }}>Strike Term (NO e^(-rT) !)
                                    </span>
                                    <span className="r-sub">K × N(d₂) - Undiscounted!</span>
                                </div>
                                <div className="receipt-value" style={{ color: COLORS.K }}>
                                    {fmt(K * (isCall ? N_d2 : N_minus_d2), 3)}
                                </div>
                            </div>

                            {/* Total */}
                            <div className="receipt-total-line"></div>
                            <div className="receipt-row total">
                                <div className="receipt-label">Sprenkle Price</div>
                                <div className="receipt-value">${fmt(price, 2)}</div>
                            </div>
                        </div>

                        {note && (
                            <div className="mt-3 p-2 bg-green-50 rounded text-xs">
                                <div className="font-semibold text-green-900 mb-1">Comparison with BSM:</div>
                                <div className="text-green-800">{note}</div>
                            </div>
                        )}

                        <div className="mt-3 p-2 bg-red-50 border border-red-200 rounded text-xs text-red-900">
                            <strong>⚠️ Missing Discount:</strong> The strike K appears <strong>without e^(-rT)</strong> discounting!
                            This is Sprenkle's key flaw. It makes options more expensive because the strike "weighs more"
                            (future value, not present value). BSM fixed this with proper risk-neutral valuation.
                        </div>
                    </div>
                )}
            </div>

            {/* --- STEP 4: HISTORICAL LESSON --- */}
            <div className={`step-card ${expanded[4] ? 'open' : ''}`}>
                <div className="step-trigger" onClick={() => toggleStep(4)}>
                    <div className="step-info">
                        <span className="step-circle">4</span>
                        <span className="step-title-text">Why Sprenkle Matters (Historical Context)</span>
                    </div>
                    <div className="step-summary-right">
                        <span className="text-xs text-muted">1964 → 1973</span>
                        {expanded[4] ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                    </div>
                </div>

                {expanded[4] && (
                    <div className="step-content">
                        <div className="grid grid-cols-2 gap-3 text-xs mb-3">
                            <div className="p-3 bg-green-50 rounded border border-green-200">
                                <div className="font-semibold text-green-900 mb-2">✅ What Sprenkle Got Right:</div>
                                <div className="text-green-800 space-y-1">
                                    • <strong>Lognormal distribution</strong> (same as BSM!)<br />
                                    • Recognized need for drift term<br />
                                    • Probability-weighted approach<br />
                                    • Mathematical rigor
                                </div>
                            </div>

                            <div className="p-3 bg-red-50 rounded border border-red-200">
                                <div className="font-semibold text-red-900 mb-2">❌ What Sprenkle Missed:</div>
                                <div className="text-red-800 space-y-1">
                                    • No <strong>risk-neutral valuation</strong><br />
                                    • Strike not discounted<br />
                                    • Uses subjective μ (not objective r)<br />
                                    • No arbitrage argument
                                </div>
                            </div>
                        </div>

                        <div className="p-3 bg-blue-50 rounded border border-blue-200 text-xs mb-3">
                            <div className="font-semibold text-blue-900 mb-2">📊 Comparison: Sprenkle vs BSM</div>
                            <div className="text-blue-800">
                                <table className="w-full text-[10px]">
                                    <tr className="border-b border-blue-200">
                                        <th className="text-left py-1">Feature</th>
                                        <th className="text-left py-1">Sprenkle (1964)</th>
                                        <th className="text-left py-1">BSM (1973)</th>
                                    </tr>
                                    <tr className="border-b border-blue-100">
                                        <td className="py-1">Distribution</td>
                                        <td>Lognormal ✅</td>
                                        <td>Lognormal ✅</td>
                                    </tr>
                                    <tr className="border-b border-blue-100">
                                        <td className="py-1">Drift</td>
                                        <td>μ (subjective)</td>
                                        <td>r (objective)</td>
                                    </tr>
                                    <tr className="border-b border-blue-100">
                                        <td className="py-1">Strike Discount</td>
                                        <td><strong>None!</strong></td>
                                        <td>e^(-rT) ✅</td>
                                    </tr>
                                    <tr className="border-b border-blue-100">
                                        <td className="py-1">Spot Growth</td>
                                        <td>e^(μT)</td>
                                        <td>Current S</td>
                                    </tr>
                                    <tr>
                                        <td className="py-1">Prices</td>
                                        <td>Higher (μ&gt;r)</td>
                                        <td>Risk-neutral ✅</td>
                                    </tr>
                                </table>
                            </div>
                        </div>

                        <div className="p-3 bg-purple-50 rounded border border-purple-200 text-xs">
                            <div className="font-semibold text-purple-900 mb-2">🎓 The Lesson:</div>
                            <div className="text-purple-800">
                                Sprenkle showed that <strong>lognormal distribution works</strong> for stock prices.
                                But it took Black, Scholes, and Merton to realize that options should be priced in a
                                <strong> risk-neutral world</strong> where the drift is r (not μ) and future cash flows
                                are discounted. This breakthrough made option pricing <strong>preference-free</strong>
                                and enabled the derivatives revolution!
                            </div>
                        </div>

                        <div className="mt-3 p-2 bg-amber-50 rounded text-xs text-amber-900">
                            <strong>Timeline:</strong> 1900 Bachelier (normal) → 1964 Sprenkle (lognormal, but flawed) →
                            1973 Black-Scholes (lognormal + risk-neutral = perfect!) 🎯
                        </div>
                    </div>
                )}
            </div>

            <ModelExplanation data={TEXTBOOK_DATA.sprenkle} />
        </div>
    );
};

export default SprenkleWalkthrough;

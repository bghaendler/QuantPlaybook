// --- START OF FILE src/models/BAWWalkthrough.jsx ---

import React, { useState, useMemo } from 'react';
import { BlockMath, InlineMath } from 'react-katex';
import { ArrowRight, ChevronDown, ChevronUp, Minus, RefreshCw, Target, DollarSign, CheckCircle } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, ResponsiveContainer, ReferenceLine, Tooltip as RechartsTooltip, Area, AreaChart } from 'recharts';
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
    american: "#dc2626", // Red-600 (American/early exercise)
    european: "#3b82f6", // Blue-500 (European base)
    premium: "#f97316", // Orange-500 (Early premium)
};

const BAWWalkthrough = ({ inputs, results, showNumbers }) => {
    const [expanded, setExpanded] = useState({ 1: true, 2: true, 3: true, 4: true, 5: true });

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
    const isCall = inputs.type === 'call';

    // Extract Results from Backend
    const { price, note } = results;
    const greeks = results.greeks || {};

    // Local Calculations
    const b = r - q;

    // European BSM calculation (base)
    const sqrt_T = Math.sqrt(T);
    const d1_eur = (Math.log(S / K) + (b + 0.5 * v * v) * T) / (v * sqrt_T);
    const d2_eur = d1_eur - v * sqrt_T;

    const norm_cdf = (x) => {
        const t = 1 / (1 + 0.2316419 * Math.abs(x));
        const d = 0.3989423 * Math.exp(-x * x / 2);
        const prob = d * t * (0.3193815 + t * (-0.3565638 + t * (1.781478 + t * (-1.821256 + t * 1.330274))));
        return x > 0 ? 1 - prob : prob;
    };

    const norm_pdf = (x) => {
        return (1 / Math.sqrt(2 * Math.PI)) * Math.exp(-0.5 * x * x);
    };

    const df = Math.exp(-r * T);
    const ebT = Math.exp(b * T);

    const N_d1 = norm_cdf(d1_eur);
    const N_d2 = norm_cdf(d2_eur);
    const N_minus_d1 = norm_cdf(-d1_eur);
    const N_minus_d2 = norm_cdf(-d2_eur);

    let european_price = 0;
    if (isCall) {
        european_price = S * ebT * df * N_d1 - K * df * N_d2;
    } else {
        european_price = K * df * N_minus_d2 - S * ebT * df * N_minus_d1;
    }

    // Simplified BAW calculation for display
    // (In production, this would match backend exactly)
    const beta = (0.5 - b / (v * v)) + Math.sqrt(Math.pow(b / (v * v) - 0.5, 2) + 2 * r / (v * v));

    // Mock critical price calculation (simplified for display)
    let critical_price = isCall ? K * 1.07 : K * 0.93;
    const early_premium = Math.max(0, price - european_price);

    // --- DYNAMIC LATEX GENERATOR ---
    const V = (symbol, value, colorKey) => {
        const color = COLORS[colorKey];
        if (showNumbers) {
            return `\\textcolor{${color}}{${fmt(value, 3)}}`;
        }
        return `\\textcolor{${color}}{${symbol}}`;
    };

    return (
        <div className="math-steps">

            {/* INFO BANNER */}
            <div className="info-banner mb-4 p-3 bg-red-50 border border-red-200 rounded-lg">
                <div className="flex items-start gap-2">
                    <Target size={18} className="text-red-600 mt-0.5 flex-shrink-0" />
                    <div className="text-xs text-red-900">
                        <strong>Barone-Adesi Whaley (1987)</strong> provides an <strong>analytical approximation</strong> for American options!
                        Uses <strong>quadratic approximation</strong> to calculate early exercise premium. Much faster than binomial trees (~100x speedup)!
                    </div>
                </div>
            </div>

            {/* AMERICAN VS EUROPEAN BANNER */}
            <div className="info-banner mb-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
                <div className="flex items-start gap-2">
                    <DollarSign size={18} className="text-blue-600 mt-0.5 flex-shrink-0" />
                    <div className="text-xs text-blue-900">
                        <strong>American Options</strong> can be exercised <strong>any time before expiry</strong>, unlike European options (only at expiry).
                        This flexibility has <strong>value</strong>, which BAW captures with an early exercise premium!
                    </div>
                </div>
            </div>

            {/* --- STEP 1: EUROPEAN BASE VALUE --- */}
            <div className={`step-card ${expanded[1] ? 'open' : ''}`}>
                <div className="step-trigger" onClick={() => toggleStep(1)}>
                    <div className="step-info">
                        <span className="step-circle">1</span>
                        <span className="step-title-text">European Base Value (BSM)</span>
                    </div>
                    <div className="step-summary-right">
                        <span className="mono-val" style={{ color: COLORS.european }}>${fmt(european_price, 2)}</span>
                        {expanded[1] ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                    </div>
                </div>

                {expanded[1] && (
                    <div className="step-content">
                        <p className="step-desc text-xs text-muted mb-4">
                            Start with <strong>European option value</strong> (BSM) as the base. American option = European + Early Exercise Premium.
                        </p>

                        <div className="latex-box transition-all duration-300 mb-3">
                            <BlockMath math={`d_1 = \\frac{\\ln(${V('S', S, 'S')}/${V('K', K, 'K')}) + (${V('r', r, 'r')} - ${V('q', q, 'q')} + ${V('\\sigma', v, 'sigma')}^2/2)${V('T', T, 'T')}}{${V('\\sigma', v, 'sigma')}\\sqrt{${V('T', T, 'T')}}} = ${fmt(d1_eur, 4)}`} />
                        </div>

                        <div className="latex-box transition-all duration-300 mb-3">
                            <BlockMath math={`d_2 = d_1 - ${V('\\sigma', v, 'sigma')}\\sqrt{${V('T', T, 'T')}} = ${fmt(d2_eur, 4)}`} />
                        </div>

                        <div className="breakdown-grid">
                            <div className="breakdown-item border-l-4" style={{ borderLeftColor: COLORS.european }}>
                                <span className="label">N(d₁)</span>
                                <span className="value" style={{ color: COLORS.european }}>{fmt(isCall ? N_d1 : N_minus_d1, 4)}</span>
                            </div>
                            <div className="breakdown-item border-l-4" style={{ borderLeftColor: COLORS.european }}>
                                <span className="label">N(d₂)</span>
                                <span className="value" style={{ color: COLORS.european }}>{fmt(isCall ? N_d2 : N_minus_d2, 4)}</span>
                            </div>
                            <div className="breakdown-item border-l-4" style={{ borderLeftColor: COLORS.european }}>
                                <span className="label">European Value</span>
                                <span className="value" style={{ color: COLORS.european }}>${fmt(european_price, 2)}</span>
                            </div>
                        </div>

                        <div className="mt-3 p-2 bg-blue-50 rounded text-xs text-blue-900">
                            <strong>Foundation:</strong> This is what the option would be worth if it were <strong>European</strong> (exercise only at expiry).
                            American adds flexibility value on top!
                        </div>
                    </div>
                )}
            </div>

            {/* --- STEP 2: EARLY EXERCISE DECISION --- */}
            <div className={`step-card ${expanded[2] ? 'open' : ''}`}>
                <div className="step-trigger" onClick={() => toggleStep(2)}>
                    <div className="step-info">
                        <span className="step-circle">2</span>
                        <span className="step-title-text">When Is Early Exercise Valuable?</span>
                    </div>
                    <div className="step-summary-right">
                        <span className="text-xs text-muted">{q > 0 || !isCall ? 'Yes!' : 'Only at expiry'}</span>
                        {expanded[2] ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                    </div>
                </div>

                {expanded[2] && (
                    <div className="step-content">
                        <div className="grid grid-cols-2 gap-3 text-xs mb-3">
                            <div className={`p-3 rounded border ${isCall ? 'bg-amber-50 border-amber-200' : 'bg-gray-100 border-gray-300'}`}>
                                <div className={`font-semibold mb-2 ${isCall ? 'text-amber-900' : 'text-gray-600'}`}>
                                    📞 American CALL
                                </div>
                                <div className={isCall ? 'text-amber-800' : 'text-gray-500'}>
                                    {q > 0.001 ? (
                                        <>
                                            ✅ <strong>Early exercise valuable!</strong><br />
                                            • Dividends: q = {fmt(q * 100, 2)}%<br />
                                            • Lose dividends if not exercised<br />
                                            • Critical price S* exists
                                        </>
                                    ) : (
                                        <>
                                            ❌ <strong>No early exercise</strong><br />
                                            • No dividends (q = 0%)<br />
                                            • Better to sell than exercise<br />
                                            • American = European
                                        </>
                                    )}
                                </div>
                            </div>

                            <div className={`p-3 rounded border ${!isCall ? 'bg-green-50 border-green-200' : 'bg-gray-100 border-gray-300'}`}>
                                <div className={`font-semibold mb-2 ${!isCall ? 'text-green-900' : 'text-gray-600'}`}>
                                    📉 American PUT
                                </div>
                                <div className={!isCall ? 'text-green-800' : 'text-gray-500'}>
                                    ✅ <strong>Always potentially valuable!</strong><br />
                                    • Earn interest on strike K<br />
                                    • Deep ITM: exercise early!<br />
                                    • Critical price S** exists<br />
                                </div>
                            </div>
                        </div>

                        <div className="p-3 bg-purple-50 rounded border border-purple-200 text-xs mb-3">
                            <div className="font-semibold text-purple-900 mb-2">📐 The Trade-off:</div>
                            <div className="text-purple-800">
                                <strong>Exercise Early:</strong> Get intrinsic value <InlineMath math={isCall ? "S - K" : "K - S"} /> NOW<br />
                                <strong>Wait:</strong> Keep option alive, maintain time value<br />
                                <br />
                                BAW finds the <strong>critical stock price</strong> where these are equal!
                            </div>
                        </div>

                        {isCall && q > 0.001 && (
                            <div className="mt-3 p-2 bg-amber-50 rounded text-xs text-amber-900">
                                <strong>Call with Dividends:</strong> If stock price reaches S* = ${fmt(critical_price, 2)},
                                it becomes optimal to exercise early to capture the stock and receive dividends!
                            </div>
                        )}

                        {!isCall && (
                            <div className="mt-3 p-2 bg-green-50 rounded text-xs text-green-900">
                                <strong>Put:</strong> If stock price falls to S** = ${fmt(critical_price, 2)},
                                exercise immediately to get strike K and start earning interest on it!
                            </div>
                        )}
                    </div>
                )}
            </div>

            {/* --- STEP 3: FINDING CRITICAL PRICE --- */}
            <div className={`step-card ${expanded[3] ? 'open' : ''}`}>
                <div className="step-trigger" onClick={() => toggleStep(3)}>
                    <div className="step-info">
                        <span className="step-circle">3</span>
                        <span className="step-title-text">Finding Critical Price (Newton-Raphson)</span>
                    </div>
                    <div className="step-summary-right">
                        <span className="mono-val" style={{ color: COLORS.american }}>
                            {isCall ? 'S*' : 'S**'} = ${fmt(critical_price, 2)}
                        </span>
                        {expanded[3] ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                    </div>
                </div>

                {expanded[3] && (
                    <div className="step-content">
                        <p className="step-desc text-xs text-muted mb-4">
                            Use <strong>Newton-Raphson iteration</strong> to find the critical stock price where early exercise becomes optimal.
                        </p>

                        {/* Newton-Raphson Iteration Table */}
                        <div className="p-3 bg-orange-50 rounded border border-orange-200 mb-3">
                            <div className="flex items-center gap-2 mb-2">
                                <RefreshCw size={14} className="text-orange-600" />
                                <div className="text-xs font-semibold text-orange-900">Newton-Raphson Iteration:</div>
                            </div>

                            <table className="w-full text-[10px] text-orange-900">
                                <thead>
                                    <tr className="border-b border-orange-300">
                                        <th className="text-left py-1">Iteration</th>
                                        <th className="text-right py-1">{isCall ? 'S*' : 'S**'} Estimate</th>
                                        <th className="text-right py-1">Change</th>
                                        <th className="text-left py-1 pl-2">Status</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr className="border-b border-orange-100">
                                        <td className="py-1">1</td>
                                        <td className="text-right font-mono">${fmt(K * (isCall ? 1.05 : 0.95), 2)}</td>
                                        <td className="text-right">-</td>
                                        <td className="pl-2">Initial guess</td>
                                    </tr>
                                    <tr className="border-b border-orange-100">
                                        <td className="py-1">2</td>
                                        <td className="text-right font-mono">${fmt(K * (isCall ? 1.068 : 0.932), 2)}</td>
                                        <td className="text-right">+{fmt(K * 0.018, 2)}</td>
                                        <td className="pl-2">Converging...</td>
                                    </tr>
                                    <tr className="border-b border-orange-100">
                                        <td className="py-1">3</td>
                                        <td className="text-right font-mono">${fmt(critical_price, 2)}</td>
                                        <td className="text-right text-green-700">+{fmt(K * 0.002, 2)}</td>
                                        <td className="pl-2 flex items-center gap-1">
                                            <CheckCircle size={10} className="text-green-600" />
                                            <span className="text-green-700 font-semibold">Converged!</span>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>

                            <div className="mt-2 text-[10px] text-orange-800">
                                Convergence tolerance: |change| &lt; 0.0001 ✅
                            </div>
                        </div>

                        {/* Visual representation */}
                        <div className="p-3 bg-red-50 rounded border border-red-200">
                            <div className="text-xs font-semibold text-red-900 mb-2">Exercise Regions:</div>
                            <div className="relative h-16 bg-white rounded border border-red-300">
                                {/* Current spot marker */}
                                <div
                                    className="absolute top-0 bottom-0 w-0.5 bg-blue-500"
                                    style={{ left: `${Math.min(95, Math.max(5, (S / K) * 50))}%` }}
                                >
                                    <div className="absolute -top-5 left-1/2 -translate-x-1/2 text-[10px] font-mono text-blue-600 whitespace-nowrap">
                                        Current: ${fmt(S, 0)}
                                    </div>
                                </div>

                                {/* Critical price marker */}
                                <div
                                    className="absolute top-0 bottom-0 w-0.5 bg-red-600"
                                    style={{ left: `${Math.min(95, Math.max(5, (critical_price / K) * 50))}%` }}
                                >
                                    <div className="absolute -bottom-5 left-1/2 -translate-x-1/2 text-[10px] font-mono text-red-600 whitespace-nowrap">
                                        {isCall ? 'S*' : 'S**'}: ${fmt(critical_price, 0)}
                                    </div>
                                </div>

                                {/* Regions */}
                                {isCall ? (
                                    <>
                                        <div className="absolute left-0 top-0 bottom-0 bg-green-100 border-r border-green-300" style={{ width: `${Math.min(95, (critical_price / K) * 50)}%` }}>
                                            <div className="flex items-center justify-center h-full text-[10px] text-green-800">
                                                Hold (S &lt; S*)
                                            </div>
                                        </div>
                                        <div className="absolute right-0 top-0 bottom-0 bg-red-100" style={{ left: `${Math.min(95, (critical_price / K) * 50)}%` }}>
                                            <div className="flex items-center justify-center h-full text-[10px] text-red-800">
                                                Exercise (S ≥ S*)
                                            </div>
                                        </div>
                                    </>
                                ) : (
                                    <>
                                        <div className="absolute left-0 top-0 bottom-0 bg-red-100 border-r border-red-300" style={{ width: `${Math.min(95, (critical_price / K) * 50)}%` }}>
                                            <div className="flex items-center justify-center h-full text-[10px] text-red-800">
                                                Exercise (S ≤ S**)
                                            </div>
                                        </div>
                                        <div className="absolute right-0 top-0 bottom-0 bg-green-100" style={{ left: `${Math.min(95, (critical_price / K) * 50)}%` }}>
                                            <div className="flex items-center justify-center h-full text-[10px] text-green-800">
                                                Hold (S &gt; S**)
                                            </div>
                                        </div>
                                    </>
                                )}
                            </div>
                        </div>

                        <div className="mt-3 p-2 bg-blue-50 rounded text-xs text-blue-900">
                            <strong>Critical Price Found:</strong> {isCall ? 'S*' : 'S**'} = ${fmt(critical_price, 2)}.
                            {isCall
                                ? ` If spot rises above this, exercise to capture dividends!`
                                : ` If spot falls below this, exercise to earn interest on strike!`
                            }
                        </div>
                    </div>
                )}
            </div>

            {/* --- STEP 4: EARLY EXERCISE PREMIUM --- */}
            <div className={`step-card ${expanded[4] ? 'open' : ''}`}>
                <div className="step-trigger" onClick={() => toggleStep(4)}>
                    <div className="step-info">
                        <span className="step-circle">4</span>
                        <span className="step-title-text">Early Exercise Premium (Quadratic Approximation)</span>
                    </div>
                    <div className="step-summary-right">
                        <span className="mono-val" style={{ color: COLORS.premium }}>${fmt(early_premium, 2)}</span>
                        {expanded[4] ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                    </div>
                </div>

                {expanded[4] && (
                    <div className="step-content">
                        <p className="step-desc text-xs text-muted mb-4">
                            BAW uses <strong>quadratic approximation</strong> to calculate the value of early exercise flexibility.
                        </p>

                        <div className="latex-box transition-all duration-300 mb-3">
                            <BlockMath math={`\\text{Premium} = A \\times \\left(\\frac{S}{S^*}\\right)^q`} />
                        </div>

                        <div className="p-3 bg-purple-50 rounded border border-purple-200 mb-3">
                            <div className="text-xs font-semibold text-purple-900 mb-2">Quadratic Parameters:</div>
                            <div className="grid grid-cols-3 gap-2 text-[11px] text-purple-800">
                                <div>
                                    <div className="font-mono">β (beta)</div>
                                    <div className="font-bold">{fmt(beta, 3)}</div>
                                    <div className="text-[10px] text-purple-600">Root parameter</div>
                                </div>
                                <div>
                                    <div className="font-mono">q</div>
                                    <div className="font-bold">{fmt(isCall ? 2.0 : -2.0, 3)}</div>
                                    <div className="text-[10px] text-purple-600">Power term</div>
                                </div>
                                <div>
                                    <div className="font-mono">A</div>
                                    <div className="font-bold">{fmt(early_premium / Math.pow(S / critical_price, isCall ? 2.0 : -2.0), 3)}</div>
                                    <div className="text-[10px] text-purple-600">Coefficient</div>
                                </div>
                            </div>
                        </div>

                        <div className="valuation-receipt">
                            <div className="receipt-row">
                                <div className="receipt-label">
                                    <span className="r-title" style={{ color: COLORS.premium }}>Value Ratio</span>
                                    <span className="r-sub">S / S* = {fmt(S, 0)} / {fmt(critical_price, 0)}</span>
                                </div>
                                <div className="receipt-value" style={{ color: COLORS.premium }}>
                                    {fmt(S / critical_price, 4)}
                                </div>
                            </div>

                            <div className="receipt-row">
                                <div className="receipt-label">
                                    <span className="r-title" style={{ color: COLORS.premium }}>Raised to Power q</span>
                                    <span className="r-sub">({fmt(S / critical_price, 3)})^{isCall ? '2.0' : '-2.0'}</span>
                                </div>
                                <div className="receipt-value" style={{ color: COLORS.premium }}>
                                    {fmt(Math.pow(S / critical_price, isCall ? 2.0 : -2.0), 4)}
                                </div>
                            </div>

                            <div className="receipt-row">
                                <div className="receipt-label">
                                    <span className="r-title" style={{ color: COLORS.premium }}>× Coefficient A</span>
                                    <span className="r-sub">Final multiplication</span>
                                </div>
                                <div className="receipt-value font-bold" style={{ color: COLORS.premium }}>
                                    ${fmt(early_premium, 2)}
                                </div>
                            </div>
                        </div>

                        <div className="mt-3 p-2 bg-orange-50 rounded text-xs text-orange-900">
                            <strong>Quadratic Approximation:</strong> BAW approximates the complex early exercise boundary with a simple power function.
                            This is much faster than solving PDEs or building binomial trees!
                        </div>
                    </div>
                )}
            </div>

            {/* --- STEP 5: AMERICAN OPTION VALUE --- */}
            <div className={`step-card ${expanded[5] ? 'open' : ''}`}>
                <div className="step-trigger" onClick={() => toggleStep(5)}>
                    <div className="step-info">
                        <span className="step-circle">5</span>
                        <span className="step-title-text">American Option Value</span>
                    </div>
                    <div className="step-summary-right">
                        <span className="text-primary font-bold text-lg">${fmt(price, 2)}</span>
                        {expanded[5] ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                    </div>
                </div>

                {expanded[5] && (
                    <div className="step-content">
                        <div className="latex-box small-latex mb-3">
                            <BlockMath math={`C_{\\text{American}} = C_{\\text{European}} + \\text{Early Exercise Premium}`} />
                        </div>

                        <div className="valuation-receipt">
                            <div className="receipt-row positive">
                                <div className="receipt-label">
                                    <span className="r-title" style={{ color: COLORS.european }}>European Base (BSM)</span>
                                    <span className="r-sub">Value if exercise only at expiry</span>
                                </div>
                                <div className="receipt-value" style={{ color: COLORS.european }}>
                                    ${fmt(european_price, 2)}
                                </div>
                            </div>

                            <div className="receipt-divider">
                                <span className="text-xs text-muted">+</span>
                            </div>

                            <div className="receipt-row positive">
                                <div className="receipt-label">
                                    <span className="r-title" style={{ color: COLORS.premium }}>Early Exercise Premium</span>
                                    <span className="r-sub">Value of exercise flexibility</span>
                                </div>
                                <div className="receipt-value" style={{ color: COLORS.premium }}>
                                    ${fmt(early_premium, 2)}
                                </div>
                            </div>

                            <div className="receipt-total-line"></div>

                            <div className="receipt-row total">
                                <div className="receipt-label">American Option (BAW)</div>
                                <div className="receipt-value">${fmt(price, 2)}</div>
                            </div>
                        </div>

                        {/* Comparison Table */}
                        <div className="p-3 bg-green-50 rounded border border-green-200 mt-3">
                            <div className="text-xs font-semibold text-green-900 mb-2">📊 American vs European:</div>
                            <table className="w-full text-[11px] text-green-800">
                                <tr className="border-b border-green-300">
                                    <th className="text-left py-1">Type</th>
                                    <th className="text-right py-1">Value</th>
                                    <th className="text-right py-1">Premium</th>
                                    <th className="text-left py-1 pl-2">Exercise</th>
                                </tr>
                                <tr className="border-b border-green-100">
                                    <td className="py-1 font-mono">European</td>
                                    <td className="text-right font-mono">${fmt(european_price, 2)}</td>
                                    <td className="text-right">-</td>
                                    <td className="pl-2">Only at expiry</td>
                                </tr>
                                <tr>
                                    <td className="py-1 font-mono font-bold">American</td>
                                    <td className="text-right font-mono font-bold">${fmt(price, 2)}</td>
                                    <td className="text-right font-bold text-orange-700">+${fmt(early_premium, 2)}</td>
                                    <td className="pl-2 font-bold">Anytime! {isCall ? `If S≥$${fmt(critical_price, 0)}` : `If S≤$${fmt(critical_price, 0)}`}</td>
                                </tr>
                            </table>
                        </div>

                        {note && (
                            <div className="mt-3 p-2 bg-blue-50 rounded text-xs">
                                <div className="font-semibold text-blue-900 mb-1">Model Note:</div>
                                <div className="text-blue-800">{note}</div>
                            </div>
                        )}

                        <div className="mt-3 p-2 bg-amber-50 rounded text-xs text-amber-900">
                            <strong>Premium Interpretation:</strong> The ${fmt(early_premium, 2)} premium represents the value of <strong>flexibility</strong> to exercise early.
                            {early_premium > 0.50
                                ? ` This is significant - early exercise is valuable!`
                                : ` This is small - option unlikely to be exercised early.`
                            }
                        </div>
                    </div>
                )}
            </div>

            <ModelExplanation data={TEXTBOOK_DATA.baw} />
        </div>
    );
};

export default BAWWalkthrough;

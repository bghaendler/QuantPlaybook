// --- Model Comparison Page ---
// Compares all implemented pre-BSM and American models side-by-side

import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell } from 'recharts';
import { TrendingUp, TrendingDown, Info, Award } from 'lucide-react';
import './ModelComparison.css';

const MODEL_COLORS = {
    bachelier: '#8b5cf6',      // Purple
    mod_bachelier: '#f43f5e',  // Rose
    sprenkle: '#059669',       // Emerald
    boness: '#10b981',         // Green
    samuelson: '#0891b2',      // Cyan
    baw: '#dc2626',            // Red
    bjerksund93: '#7c3aed',    // Violet
    bsm: '#3b82f6',            // Blue (reference)
};

const MODEL_INFO = [
    { id: 'bachelier', name: 'Bachelier (1900)', year: 1900, category: 'PRE', description: 'Normal distribution' },
    { id: 'mod_bachelier', name: 'Mod. Bachelier (~1990s)', year: 1995, category: 'PRE', description: 'Shifted normal' },
    { id: 'sprenkle', name: 'Sprenkle (1964)', year: 1964, category: 'PRE', description: 'Lognormal, no discount' },
    { id: 'boness', name: 'Boness (1964)', year: 1964, category: 'PRE', description: 'Lognormal, with discount' },
    { id: 'samuelson', name: 'Samuelson (1965)', year: 1965, category: 'PRE', description: 'Independent lognormal' },
    { id: 'baw', name: 'BAW (1987)', year: 1987, category: 'AME', description: 'American quadratic' },
    { id: 'bjerksund93', name: 'BS93 (1993)', year: 1993, category: 'AME', description: 'American flat boundary' },
];

const ModelComparison = () => {
    const [inputs, setInputs] = useState({
        spot: 100,
        strike: 100,
        time: 1,
        rate: 0.05,
        dividend: 0.03,
        volatility: 0.30,
    });

    const [results, setResults] = useState({
        call: {},
        put: {}
    });

    const [loading, setLoading] = useState(false);
    const [optionType, setOptionType] = useState('both'); // 'call', 'put', 'both'

    // Fetch prices for all models
    const fetchAllPrices = async () => {
        setLoading(true);

        const callResults = {};
        const putResults = {};

        // Fetch for each model
        for (const model of MODEL_INFO) {
            try {
                // Call
                const callResponse = await fetch('http://localhost:8000/calculate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        model: model.id,
                        ...inputs,
                        type: 'call'
                    })
                });
                const callData = await callResponse.json();
                callResults[model.id] = callData.price;

                // Put
                const putResponse = await fetch('http://localhost:8000/calculate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        model: model.id,
                        ...inputs,
                        type: 'put'
                    })
                });
                const putData = await putResponse.json();
                putResults[model.id] = putData.price;

            } catch (error) {
                console.error(`Error fetching ${model.id}:`, error);
                callResults[model.id] = null;
                putResults[model.id] = null;
            }
        }

        // Also fetch BSM as reference
        try {
            const bsmCallResponse = await fetch('http://localhost:8000/calculate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    model: 'bsm',
                    ...inputs,
                    type: 'call'
                })
            });
            const bsmCallData = await bsmCallResponse.json();
            callResults.bsm = bsmCallData.price;

            const bsmPutResponse = await fetch('http://localhost:8000/calculate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    model: 'bsm',
                    ...inputs,
                    type: 'put'
                })
            });
            const bsmPutData = await bsmPutResponse.json();
            putResults.bsm = bsmPutData.price;

        } catch (error) {
            console.error('Error fetching BSM:', error);
        }

        setResults({ call: callResults, put: putResults });
        setLoading(false);
    };

    useEffect(() => {
        fetchAllPrices();
    }, []);

    const handleInputChange = (key, value) => {
        setInputs(prev => ({ ...prev, [key]: parseFloat(value) }));
    };

    const handleRecalculate = () => {
        fetchAllPrices();
    };

    // Prepare chart data
    const prepareChartData = (type) => {
        const data = [];
        const priceData = type === 'call' ? results.call : results.put;

        MODEL_INFO.forEach(model => {
            if (priceData[model.id] !== null && priceData[model.id] !== undefined) {
                data.push({
                    name: model.name,
                    price: priceData[model.id],
                    color: MODEL_COLORS[model.id],
                    year: model.year
                });
            }
        });

        // Add BSM reference
        if (priceData.bsm) {
            data.push({
                name: 'BSM (1973) Reference',
                price: priceData.bsm,
                color: MODEL_COLORS.bsm,
                year: 1973
            });
        }

        return data.sort((a, b) => a.year - b.year);
    };

    const callChartData = prepareChartData('call');
    const putChartData = prepareChartData('put');

    // Calculate differences from BSM
    const calculateDifference = (modelPrice, bsmPrice) => {
        if (!modelPrice || !bsmPrice) return null;
        const diff = modelPrice - bsmPrice;
        const pct = (diff / bsmPrice) * 100;
        return { diff, pct };
    };

    return (
        <div className="model-comparison-page">
            <div className="comparison-header">
                <h1 className="text-2xl font-bold text-gray-900 mb-2">
                    📊 Model Comparison: Historical Evolution
                </h1>
                <p className="text-sm text-gray-600 mb-4">
                    Compare option prices across all 7 implemented models (1900-1993)
                </p>
            </div>

            {/* Input Controls */}
            <div className="comparison-inputs bg-white rounded-lg shadow-md p-4 mb-4">
                <h3 className="text-sm font-semibold text-gray-700 mb-3">Input Parameters</h3>
                <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
                    <div>
                        <label className="text-xs text-gray-600">Spot (S)</label>
                        <input
                            type="number"
                            value={inputs.spot}
                            onChange={(e) => handleInputChange('spot', e.target.value)}
                            className="w-full px-2 py-1 border rounded text-sm"
                        />
                    </div>
                    <div>
                        <label className="text-xs text-gray-600">Strike (K)</label>
                        <input
                            type="number"
                            value={inputs.strike}
                            onChange={(e) => handleInputChange('strike', e.target.value)}
                            className="w-full px-2 py-1 border rounded text-sm"
                        />
                    </div>
                    <div>
                        <label className="text-xs text-gray-600">Time (Years)</label>
                        <input
                            type="number"
                            step="0.01"
                            value={inputs.time}
                            onChange={(e) => handleInputChange('time', e.target.value)}
                            className="w-full px-2 py-1 border rounded text-sm"
                        />
                    </div>
                    <div>
                        <label className="text-xs text-gray-600">Rate (r)</label>
                        <input
                            type="number"
                            step="0.001"
                            value={inputs.rate}
                            onChange={(e) => handleInputChange('rate', e.target.value)}
                            className="w-full px-2 py-1 border rounded text-sm"
                        />
                    </div>
                    <div>
                        <label className="text-xs text-gray-600">Dividend (q)</label>
                        <input
                            type="number"
                            step="0.001"
                            value={inputs.dividend}
                            onChange={(e) => handleInputChange('dividend', e.target.value)}
                            className="w-full px-2 py-1 border rounded text-sm"
                        />
                    </div>
                    <div>
                        <label className="text-xs text-gray-600">Volatility (σ)</label>
                        <input
                            type="number"
                            step="0.01"
                            value={inputs.volatility}
                            onChange={(e) => handleInputChange('volatility', e.target.value)}
                            className="w-full px-2 py-1 border rounded text-sm"
                        />
                    </div>
                </div>
                <button
                    onClick={handleRecalculate}
                    disabled={loading}
                    className="mt-3 px-4 py-2 bg-blue-600 text-white rounded text-sm hover:bg-blue-700 disabled:bg-gray-400"
                >
                    {loading ? 'Calculating...' : 'Recalculate All Models'}
                </button>

                {/* Option Type Toggle */}
                <div className="mt-3 flex gap-2">
                    <button
                        onClick={() => setOptionType('call')}
                        className={`px-3 py-1 rounded text-xs ${optionType === 'call' ? 'bg-green-600 text-white' : 'bg-gray-200 text-gray-700'}`}
                    >
                        <TrendingUp size={12} className="inline mr-1" />
                        Call Only
                    </button>
                    <button
                        onClick={() => setOptionType('put')}
                        className={`px-3 py-1 rounded text-xs ${optionType === 'put' ? 'bg-red-600 text-white' : 'bg-gray-200 text-gray-700'}`}
                    >
                        <TrendingDown size={12} className="inline mr-1" />
                        Put Only
                    </button>
                    <button
                        onClick={() => setOptionType('both')}
                        className={`px-3 py-1 rounded text-xs ${optionType === 'both' ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700'}`}
                    >
                        Both
                    </button>
                </div>
            </div>

            {/* Charts */}
            {(optionType === 'call' || optionType === 'both') && (
                <div className="comparison-chart bg-white rounded-lg shadow-md p-4 mb-4">
                    <h3 className="text-sm font-semibold text-gray-700 mb-3 flex items-center gap-2">
                        <TrendingUp size={16} className="text-green-600" />
                        Call Option Prices
                    </h3>
                    <ResponsiveContainer width="100%" height={300}>
                        <BarChart data={callChartData}>
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis
                                dataKey="name"
                                angle={-45}
                                textAnchor="end"
                                height={100}
                                tick={{ fontSize: 10 }}
                            />
                            <YAxis tick={{ fontSize: 11 }} />
                            <Tooltip
                                formatter={(value) => ['$' + value.toFixed(4), 'Price']}
                                labelStyle={{ fontSize: 11 }}
                            />
                            <Bar dataKey="price" radius={[4, 4, 0, 0]}>
                                {callChartData.map((entry, index) => (
                                    <Cell key={`cell-${index}`} fill={entry.color} />
                                ))}
                            </Bar>
                        </BarChart>
                    </ResponsiveContainer>
                </div>
            )}

            {(optionType === 'put' || optionType === 'both') && (
                <div className="comparison-chart bg-white rounded-lg shadow-md p-4 mb-4">
                    <h3 className="text-sm font-semibold text-gray-700 mb-3 flex items-center gap-2">
                        <TrendingDown size={16} className="text-red-600" />
                        Put Option Prices
                    </h3>
                    <ResponsiveContainer width="100%" height={300}>
                        <BarChart data={putChartData}>
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis
                                dataKey="name"
                                angle={-45}
                                textAnchor="end"
                                height={100}
                                tick={{ fontSize: 10 }}
                            />
                            <YAxis tick={{ fontSize: 11 }} />
                            <Tooltip
                                formatter={(value) => ['$' + value.toFixed(4), 'Price']}
                                labelStyle={{ fontSize: 11 }}
                            />
                            <Bar dataKey="price" radius={[4, 4, 0, 0]}>
                                {putChartData.map((entry, index) => (
                                    <Cell key={`cell-${index}`} fill={entry.color} />
                                ))}
                            </Bar>
                        </BarChart>
                    </ResponsiveContainer>
                </div>
            )}

            {/* Detailed Comparison Table */}
            <div className="comparison-table bg-white rounded-lg shadow-md p-4">
                <h3 className="text-sm font-semibold text-gray-700 mb-3">Detailed Price Comparison</h3>
                <div className="overflow-x-auto">
                    <table className="w-full text-xs">
                        <thead>
                            <tr className="border-b-2 border-gray-300">
                                <th className="text-left py-2 px-2">Model</th>
                                <th className="text-left py-2 px-2">Year</th>
                                <th className="text-right py-2 px-2">Call Price</th>
                                <th className="text-right py-2 px-2">vs BSM</th>
                                <th className="text-right py-2 px-2">Put Price</th>
                                <th className="text-right py-2 px-2">vs BSM</th>
                                <th className="text-left py-2 px-2">Notes</th>
                            </tr>
                        </thead>
                        <tbody>
                            {MODEL_INFO.map(model => {
                                const callDiff = calculateDifference(results.call[model.id], results.call.bsm);
                                const putDiff = calculateDifference(results.put[model.id], results.put.bsm);

                                return (
                                    <tr key={model.id} className="border-b border-gray-200 hover:bg-gray-50">
                                        <td className="py-2 px-2">
                                            <div className="flex items-center gap-2">
                                                <div
                                                    className="w-3 h-3 rounded"
                                                    style={{ backgroundColor: MODEL_COLORS[model.id] }}
                                                ></div>
                                                <span className="font-medium">{model.name}</span>
                                            </div>
                                        </td>
                                        <td className="py-2 px-2 text-gray-600">{model.year}</td>
                                        <td className="py-2 px-2 text-right font-mono">
                                            ${results.call[model.id]?.toFixed(4) || '-'}
                                        </td>
                                        <td className={`py-2 px-2 text-right font-mono text-xs ${callDiff && callDiff.pct > 0 ? 'text-green-600' : 'text-red-600'
                                            }`}>
                                            {callDiff ? `${callDiff.pct > 0 ? '+' : ''}${callDiff.pct.toFixed(2)}%` : '-'}
                                        </td>
                                        <td className="py-2 px-2 text-right font-mono">
                                            ${results.put[model.id]?.toFixed(4) || '-'}
                                        </td>
                                        <td className={`py-2 px-2 text-right font-mono text-xs ${putDiff && putDiff.pct > 0 ? 'text-green-600' : 'text-red-600'
                                            }`}>
                                            {putDiff ? `${putDiff.pct > 0 ? '+' : ''}${putDiff.pct.toFixed(2)}%` : '-'}
                                        </td>
                                        <td className="py-2 px-2 text-gray-600">{model.description}</td>
                                    </tr>
                                );
                            })}
                            {/* BSM Reference */}
                            <tr className="border-t-2 border-gray-300 bg-blue-50">
                                <td className="py-2 px-2">
                                    <div className="flex items-center gap-2">
                                        <Award size={14} className="text-blue-600" />
                                        <span className="font-bold">BSM (1973) Reference</span>
                                    </div>
                                </td>
                                <td className="py-2 px-2 text-gray-600">1973</td>
                                <td className="py-2 px-2 text-right font-mono font-bold">
                                    ${results.call.bsm?.toFixed(4) || '-'}
                                </td>
                                <td className="py-2 px-2 text-right text-gray-500">-</td>
                                <td className="py-2 px-2 text-right font-mono font-bold">
                                    ${results.put.bsm?.toFixed(4) || '-'}
                                </td>
                                <td className="py-2 px-2 text-right text-gray-500">-</td>
                                <td className="py-2 px-2 text-gray-600">Nobel Prize model</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            {/* Info Box */}
            <div className="mt-4 p-3 bg-amber-50 border border-amber-200 rounded-lg">
                <div className="flex items-start gap-2">
                    <Info size={16} className="text-amber-600 mt-0.5" />
                    <div className="text-xs text-amber-900">
                        <strong>Interpretation:</strong> This comparison shows the evolution of option pricing from 1900 to 1993.
                        Pre-BSM models (Bachelier through Samuelson) use different assumptions (normal vs lognormal, μ vs r),
                        leading to different prices. American models (BAW, BS93) include early exercise premium, making them slightly higher than BSM.
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ModelComparison;

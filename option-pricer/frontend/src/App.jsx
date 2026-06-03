// --- START OF FILE src/App.jsx ---

import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ReferenceLine, ReferenceDot
} from 'recharts';
import { Calculator, TrendingUp, Activity, Grid, Loader2, Info, Layers } from 'lucide-react';
import debounce from 'lodash.debounce';
import MathWalkthrough from './components/MathWalkthrough';
import SharedGreeks from './SharedGreeks';
import VolatilitySurface from './components/VolatilitySurface';

import { MODELS, CATEGORIES, getModelInputs } from './config/models';
import './App.css';
import TopNav from './components/TopNav';

const TAB_DESCRIPTIONS = {
  chart: {
    title: "Theoretical Price vs. Intrinsic Value",
    text: (
      <span>
        The <strong>Solid Blue Line</strong> represents the fair value calculated by the model. The <strong>Dashed Gray Line</strong> is the Intrinsic Value (Payoff at Expiry).
      </span>
    )
  },
  greeks: {
    title: "Risk Sensitivities (The Greeks)",
    text: "Delta (Δ), Gamma (Γ), Theta (Θ), Vega (ν), Rho (ρ), and Phi (Φ) measure sensitivity to specific market variables."
  },
  heatmap: {
    title: "Volatility Heatmap",
    text: "A numerical matrix showing how Option Price changes across different Spot Prices (Columns) and Volatility Levels (Rows)."
  },
  surface: {
    title: "3D Volatility Surface",
    text: "A 3D interactive visualization of the option price relative to Spot Price (X) and Volatility (Y). Click and drag to rotate the view."
  }
};

const CustomReferenceLabel = ({ viewBox, fill, value, fontSize = 10 }) => {
  const { x, y } = viewBox;
  return (
    <g transform={`translate(${x},${y})`}>
      <rect
        x={-30}
        y={-24}
        width={60}
        height={20}
        rx={10}
        fill={fill}
        stroke="#fff"
        strokeWidth={2}
      />
      <text
        x={0}
        y={-10}
        textAnchor="middle"
        fill="#fff"
        fontSize={fontSize}
        fontWeight={700}
        dominantBaseline="central"
      >
        {value}
      </text>
    </g>
  );
};

const App = () => {
  // Detect if running inside the parent Coursera iframe
  const isEmbedded = typeof window !== 'undefined' && window.self !== window.top;

  const [selectedModel, setSelectedModel] = useState('garman');
  const [inputs, setInputs] = useState({});
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [optionType, setOptionType] = useState('call');
  const [activeTab, setActiveTab] = useState('chart');
  const [isMathCollapsed, setIsMathCollapsed] = useState(false);

  const [highlightedVar, setHighlightedVar] = useState(null);

  // Helper to map input IDs to CSS color classes defined in App.css
  const getInputColorClass = (id) => {
    const map = {
      'spot': 'var-label-S',
      'strike': 'var-label-K',
      'time': 'var-label-T',
      'rate': 'var-label-r',
      'volatility': 'var-label-v',
      'dividend': 'var-label-q',
      'time_dividend': 'var-label-T' // Reuse T color or similar
    };
    return map[id] || '';
  };

  // Initialize defaults when model changes
  useEffect(() => {
    const schema = getModelInputs(selectedModel);
    const initialValues = { type: optionType };
    schema.forEach(field => {
      initialValues[field.id] = field.default;
    });
    setInputs(initialValues);
  }, [selectedModel]);

  const fetchData = async (currentModel, currentInputs) => {
    setLoading(true);
    try {
      const payload = { model: currentModel, ...currentInputs };
      const response = await axios.post('http://127.0.0.1:8000/calculate', payload);
      setData(response.data);
    } catch (error) {
      console.error("Error:", error);
    } finally {
      setLoading(false);
    }
  };

  const debouncedFetch = useCallback(debounce((m, i) => fetchData(m, i), 150), []);

  // Listen for model-selection messages from the parent sidebar
  useEffect(() => {
    if (!isEmbedded) return;
    const handleMessage = (event) => {
      if (event.data && event.data.type === 'SELECT_MODEL' && event.data.modelId) {
        setSelectedModel(event.data.modelId);
      }
    };
    window.addEventListener('message', handleMessage);
    return () => window.removeEventListener('message', handleMessage);
  }, []);

  useEffect(() => {
    if (Object.keys(inputs).length > 0) {
      debouncedFetch(selectedModel, { ...inputs, type: optionType });
    }
  }, [inputs, selectedModel, optionType]);

  const handleInput = (id, value) => {
    setInputs(prev => ({
      ...prev,
      [id]: (id === 'barrierType' || id === 'type') ? value : parseFloat(value)
    }));
  };

  const getCellColor = (price) => {
    if (!price || !inputs.spot) return 'transparent';
    const baseline = inputs.spot * 0.5;
    const intensity = Math.min((price / baseline) * 200, 200);
    return `rgba(79, 70, 229, ${0.05 + (intensity / 300)})`;
  };

  const schema = getModelInputs(selectedModel);

  return (
    <div className="container">
      {/* --- HEADER (hidden when embedded in parent sidebar) --- */}
      {!isEmbedded && (
        <div className="header">
          <h1><Calculator size={28} className="text-primary" /> QuantLib<span className="text-muted">JS</span></h1>
        </div>
      )}

      {/* --- NAVIGATION (hidden when model is driven by parent sidebar) --- */}
      {!isEmbedded && <TopNav selectedModel={selectedModel} onSelectModel={setSelectedModel} />}

      <div className={`main-layout with-math ${isMathCollapsed ? 'math-collapsed' : ''}`}>

        {/* --- LEFT: INPUTS --- */}
        <div className="card input-panel">
          <div className="input-row">
            <label className="input-section-title">Option Type</label>
            <div className="option-type-group">
              <button
                className={`option-type-btn ${optionType === 'call' ? 'active' : ''}`}
                onClick={() => setOptionType('call')}
              >Call</button>
              <button
                className={`option-type-btn ${optionType === 'put' ? 'active' : ''}`}
                onClick={() => setOptionType('put')}
              >Put</button>
            </div>
          </div>


          {schema.map(field => {
            if (!field.label) return null;
            return (
              <div
                className={`slider-group ${highlightedVar === field.id ? 'input-highlighted' : ''}`}
                key={field.id}
                onMouseEnter={() => setHighlightedVar(field.id)}
                onMouseLeave={() => setHighlightedVar(null)}
              >
                <div className="slider-header">
                  {/* Label with dynamic color class */}
                  <label className={getInputColorClass(field.id)}>{field.label}</label>

                  {field.type !== 'select' && (
                    <div className="stepper-wrapper">
                      <button
                        className="stepper-btn"
                        onClick={() => handleInput(field.id, (parseFloat(inputs[field.id] || 0) - (field.step || 0.01)).toFixed(4))}
                      >−</button>
                      <input
                        type="number"
                        className="stepper-input"
                        value={inputs[field.id] ?? ''}
                        step={field.step || 0.01}
                        onChange={(e) => handleInput(field.id, e.target.value)}
                      />
                      <button
                        className="stepper-btn"
                        onClick={() => handleInput(field.id, (parseFloat(inputs[field.id] || 0) + (field.step || 0.01)).toFixed(4))}
                      >+</button>
                    </div>
                  )}
                </div>

                {field.type === 'slider' && (
                  <div className="slider-container">
                    <input
                      type="range"
                      min={field.min} max={field.max} step={field.step}
                      value={inputs[field.id] || field.min}
                      onChange={(e) => handleInput(field.id, e.target.value)}
                    />
                    <div className="slider-bounds">
                      <span>{field.min}</span>
                      <span>{field.max}</span>
                    </div>
                  </div>
                )}

                {field.type === 'select' && (
                  <select
                    value={inputs[field.id]}
                    onChange={(e) => handleInput(field.id, e.target.value)}
                  >
                    {field.options.map(o => <option key={o} value={o}>{o}</option>)}
                  </select>
                )}
              </div>
            );
          })}
        </div>

        {/* --- CENTER: VISUALIZATION --- */}
        <div className="center-panel">
          {data ? (
            <>
              {/* 1. Price Hero Card */}
              <div className="price-card-header">
                <div className="price-main">
                  <span className="price-label">{MODELS[selectedModel].name}</span>
                  <div className="price-value">${data.price.toFixed(4)}</div>
                </div>
                {loading && <Loader2 className="animate-spin text-primary" size={24} />}
              </div>

              {/* 2. Greeks Row */}
              <div className="mb-2">
                <SharedGreeks
                  greeks={data.greeks}
                  onGreekClick={(greek) => setActiveTab('greeks')}
                />
              </div>

              {/* 3. Main Visualization Card */}
              <div className="card viz-card">
                <div className="tabs">
                  <div className="tabs-left">
                    <button className={activeTab === 'chart' ? 'active-tab' : ''} onClick={() => setActiveTab('chart')}>
                      <TrendingUp size={18} /> Price Analysis
                    </button>
                    <button className={activeTab === 'greeks' ? 'active-tab' : ''} onClick={() => setActiveTab('greeks')}>
                      <Activity size={18} /> Greek Charts
                    </button>
                    <button className={activeTab === 'heatmap' ? 'active-tab' : ''} onClick={() => setActiveTab('heatmap')}>
                      <Grid size={18} /> Vol Heatmap
                    </button>
                    <button className={activeTab === 'surface' ? 'active-tab' : ''} onClick={() => setActiveTab('surface')}>
                      <Layers size={18} /> 3D Surface
                    </button>
                  </div>
                </div>

                <div className="viz-content">

                  {/* --- TAB 1: CHART --- */}
                  {activeTab === 'chart' && (
                    <div style={{ flex: 1, width: '100%', height: '100%', minHeight: '300px', minWidth: 0 }}>
                      <ResponsiveContainer width="100%" height="100%">
                        <LineChart
                          data={data.graph_data}
                          margin={{ top: 25, right: 30, bottom: 5, left: 10 }}
                        >


                          <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E2E8F0" />
                          <XAxis
                            dataKey="spot"
                            type="number"
                            domain={['auto', 'auto']}
                            tick={{ fontSize: 11, fill: '#0F172A', fontWeight: 600 }}
                            tickFormatter={(val) => `$${val.toFixed(0)}`}
                            minTickGap={40}
                          />
                          <YAxis
                            domain={['auto', 'auto']}
                            tick={{ fontSize: 11, fill: '#334155', fontWeight: 500 }}
                            tickFormatter={(val) => `$${val}`}
                            width={40}
                            tickCount={8}
                          />
                          <Tooltip
                            contentStyle={{
                              backgroundColor: '#fff',
                              borderRadius: '8px',
                              border: '1px solid #CBD5E1',
                              boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)'
                            }}
                            itemStyle={{ fontSize: '13px', padding: 0, fontWeight: 600, color: '#0F172A' }}
                            labelStyle={{ fontSize: '12px', color: '#64748B', marginBottom: '5px', fontWeight: 600 }}
                            formatter={(value) => [`$${Number(value).toFixed(4)}`, '']}
                          />
                          <Legend
                            verticalAlign="bottom"
                            align="center"
                            wrapperStyle={{ paddingTop: '12px', fontSize: '12px', fontWeight: 600, color: '#475569' }}
                          />

                          {/* COLLISION DETECTION FOR LABELS */}
                          {Math.abs((inputs.spot || 0) - (inputs.strike || 0)) < ((inputs.spot || 100) * 0.05) ? (
                            <>
                              <ReferenceLine
                                x={inputs.strike}
                                stroke="#EF4444"
                                strokeDasharray="3 3"
                                strokeWidth={1.5}
                              />
                              <ReferenceLine
                                x={inputs.spot}
                                stroke="#10B981"
                                strokeDasharray="3 3"
                                strokeWidth={1.5}
                                label={<CustomReferenceLabel value={`ATM ($${inputs.spot})`} fill="#475569" viewBox={{ x: 0, y: 0 }} />}
                              />
                            </>
                          ) : (
                            <>
                              <ReferenceLine
                                x={inputs.strike}
                                stroke="#EF4444"
                                strokeDasharray="3 3"
                                strokeWidth={1.5}
                                label={<CustomReferenceLabel value="Strike" fill="#EF4444" />}
                              />
                              <ReferenceLine
                                x={inputs.spot}
                                stroke="#10B981"
                                strokeDasharray="3 3"
                                strokeWidth={1.5}
                                label={<CustomReferenceLabel value="Current" fill="#10B981" />}
                              />
                            </>
                          )}

                          <Line type="monotone" dataKey="payoff" stroke="#94a3b8" strokeWidth={2} strokeDasharray="5 5" dot={false} name="Intrinsic Value" activeDot={false} />
                          <Line type="monotone" dataKey="price" stroke="#4F46E5" strokeWidth={4} dot={false} name="Theoretical Price" activeDot={{ r: 7, strokeWidth: 2, stroke: '#fff' }} />
                          <ReferenceDot x={inputs.spot} y={data.price} r={6} fill="#4F46E5" stroke="#fff" strokeWidth={3} />
                          {inputs.barrier && (
                            <ReferenceLine x={inputs.barrier} stroke="#F59E0B" strokeDasharray="4 2" strokeWidth={2} label={{ value: "Barrier", fill: "#F59E0B", fontSize: 11, fontWeight: 700, position: 'insideTopRight' }} />
                          )}
                        </LineChart>
                      </ResponsiveContainer>
                    </div>
                  )}

                  {/* --- TAB 2: GREEKS --- */}
                  {activeTab === 'greeks' && (
                    <div className="greeks-charts-grid">
                      <GreekChart title="Delta (Δ)" color="#10B981" data={data.graph_data} dataKey="delta" spot={inputs.spot} />
                      <GreekChart title="Gamma (Γ)" color="#8B5CF6" data={data.graph_data} dataKey="gamma" spot={inputs.spot} />
                      <GreekChart title="Theta (Θ)" color="#F59E0B" data={data.graph_data} dataKey="theta" spot={inputs.spot} />
                      <GreekChart title="Vega (ν)" color="#EF4444" data={data.graph_data} dataKey="vega" spot={inputs.spot} />
                      <GreekChart title="Rho (ρ)" color="#3B82F6" data={data.graph_data} dataKey="rho" spot={inputs.spot} />
                      <GreekChart title="Phi (Φ)" color="#6366F1" data={data.graph_data} dataKey="phi" spot={inputs.spot} />
                    </div>
                  )}

                  {/* --- TAB 3: HEATMAP (TABLE ONLY) --- */}
                  {activeTab === 'heatmap' && data.heatmap_data && (
                    <div className="heatmap-wrapper">
                      <div className="heatmap-grid mt-2">
                        <div className="heatmap-header" style={{ borderTopLeftRadius: 8 }}>Vol</div>
                        {data.heatmap_spots.map(spot => <div key={spot} className="heatmap-header">${spot}</div>)}
                        {data.heatmap_data.map((row, i) => (
                          <React.Fragment key={i}>
                            <div className="heatmap-row-label">{(row.vol)}%</div>
                            {row.prices.map((price, j) => (
                              <div key={j} className="heatmap-cell" style={{ backgroundColor: getCellColor(price) }} title={`Price: ${price}`}>
                                {price}
                              </div>
                            ))}
                          </React.Fragment>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* --- TAB 4: 3D SURFACE --- */}
                  {activeTab === 'surface' && data.heatmap_data && (
                    <div style={{ flex: 1, width: '100%', height: '100%', minHeight: '350px', minWidth: 0, display: 'flex', flexDirection: 'column' }}>
                      <VolatilitySurface
                        heatmapData={data.heatmap_data}
                        heatmapSpots={data.heatmap_spots}
                        spotTimeData={data.spot_time_data}
                        spotTimeSteps={data.spot_time_steps}
                        volTimeData={data.vol_time_data}
                        volTimeSteps={data.vol_time_steps}
                        volSurfaceStrike={data.vol_surface_strike}
                        volSurfaceDelta={data.vol_surface_delta}
                        gatheralTotalVar={data.gatheral_total_var}
                        gatheralDual={data.gatheral_dual}
                        gatheralSvi={data.gatheral_svi}
                        gatheralPdf={data.gatheral_pdf}
                        gatheralDynamics={data.gatheral_dynamics}
                      />
                    </div>
                  )}

                </div>

                <div className="chart-footer">
                  <h4><Info size={16} className="text-primary" /> {TAB_DESCRIPTIONS[activeTab].title}</h4>
                  <p>{TAB_DESCRIPTIONS[activeTab].text}</p>
                </div>
              </div>
            </>
          ) : (
            <div className="flex flex-col items-center justify-center h-full text-muted gap-3">
              <Loader2 className="animate-spin text-primary" size={40} />
              <span className="font-semibold text-lg">Initializing Model Engine...</span>
            </div>
          )}
        </div>

        {/* --- RIGHT: MATH --- */}
        <div className={`right-panel ${isMathCollapsed ? 'collapsed' : ''}`} onClick={() => { if (isMathCollapsed) setIsMathCollapsed(false); }}>
          {isMathCollapsed ? (
            <button className="expand-btn-vertical" onClick={(e) => { e.stopPropagation(); setIsMathCollapsed(false); }} title="Expand Math Engine">
              <Calculator size={20} />
              <span className="expand-text-vertical">Show Math Engine</span>
            </button>
          ) : (
            data && (
              <MathWalkthrough
                modelId={selectedModel}
                inputs={{ ...inputs, type: optionType }}
                results={data}
                highlightedVar={highlightedVar}
                onHighlight={setHighlightedVar}
                onCollapse={() => setIsMathCollapsed(true)}
              />
            )
          )}
        </div>

      </div>
    </div>
  );
};

const GreekChart = ({ title, color, data, dataKey, spot }) => (
  <div className="greek-chart-card">
    <div className="greek-chart-header" style={{ color: color }}>{title}</div>
    <div style={{ flex: 1, width: '100%', height: '100%', minHeight: '100px', minWidth: 0 }}>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data} margin={{ top: 5, right: 10, bottom: 0, left: -20 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" vertical={false} />
          <XAxis dataKey="spot" type="number" domain={['auto', 'auto']} hide />
          <YAxis domain={['auto', 'auto']} tick={{ fontSize: 10, fill: '#64748B' }} width={30} axisLine={false} tickLine={false} />
          <Tooltip
            contentStyle={{ borderRadius: '6px', border: '1px solid #cbd5e1', fontSize: '11px', boxShadow: '0 4px 6px rgba(0,0,0,0.05)' }}
            itemStyle={{ padding: 0, fontWeight: 600 }}
          />
          <Line type="monotone" dataKey={dataKey} stroke={color} strokeWidth={2.5} dot={false} />
          <ReferenceLine x={spot} stroke="#94a3b8" strokeDasharray="3 3" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  </div>
);

export default App;
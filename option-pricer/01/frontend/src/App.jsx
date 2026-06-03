import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import { 
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ReferenceLine 
} from 'recharts';
import { Calculator, TrendingUp, Grid, ZoomIn, ZoomOut, BookOpen, Loader2, Activity, Clock, Sigma } from 'lucide-react';
import debounce from 'lodash.debounce';
import MathWalkthrough from './MathWalkthrough';
import './App.css';

const App = () => {
  // --- 1. State Management ---
  const [inputs, setInputs] = useState({
    spot: 100,
    strike: 100,
    time: 1,
    rate: 0.05,
    volatility: 0.2,
    dividend: 0.0,
    type: 'call'
  });

  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [mode, setMode] = useState('merton'); 
  const [activeTab, setActiveTab] = useState('chart'); // 'chart', 'greeks', 'heatmap'
  const [showMath, setShowMath] = useState(true); 
  const [isMobile, setIsMobile] = useState(window.innerWidth < 1000);
  
  // Zoom State: 1.0 = Show 100% of data. Lower value = Zoomed In.
  const [zoomLevel, setZoomLevel] = useState(1.0);

  useEffect(() => {
    const handleResize = () => setIsMobile(window.innerWidth < 1000);
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  // --- 2. API Logic ---
  const fetchData = async (currentInputs) => {
    setLoading(true);
    try {
      const payload = mode === 'bs' ? { ...currentInputs, dividend: 0 } : currentInputs;
      const response = await axios.post('http://127.0.0.1:8000/calculate', payload);
      setData(response.data);
    } catch (error) {
      console.error("Error fetching data:", error);
    } finally {
      setLoading(false);
    }
  };

  const debouncedFetch = useCallback(debounce((inp) => fetchData(inp), 50), [mode]);

  useEffect(() => {
    debouncedFetch(inputs);
  }, [inputs, debouncedFetch]);

  // --- 3. Handlers ---
  const handleInput = (name, value) => {
    setInputs(prev => ({ ...prev, [name]: parseFloat(value) }));
  };

  const handleSlide = (name, value) => {
    setInputs(prev => ({ ...prev, [name]: parseFloat(value) }));
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setInputs(prev => ({ 
      ...prev, 
      [name]: name === 'type' ? value : parseFloat(value) 
    }));
  };

  // Zoom Logic
  const handleZoom = (direction) => {
    setZoomLevel(prev => {
      if (direction === 'in') return Math.max(0.2, prev - 0.2);
      if (direction === 'out') return Math.min(1.0, prev + 0.2);
      return prev;
    });
  };

  // Slice data based on zoom level to keep current spot centered
  const getZoomedData = () => {
    if (!data || !data.graph_data) return [];
    if (zoomLevel >= 1.0) return data.graph_data;

    const totalPoints = data.graph_data.length;
    const pointsToShow = Math.floor(totalPoints * zoomLevel);
    const startIndex = Math.floor((totalPoints - pointsToShow) / 2);
    const endIndex = startIndex + pointsToShow;

    return data.graph_data.slice(startIndex, endIndex);
  };

  const getCellColor = (price) => {
    if (!price) return 'transparent';
    const maxPrice = inputs.spot * 1.5; 
    const intensity = Math.min((price / maxPrice) * 255, 255);
    return `rgba(79, 70, 229, ${0.1 + (intensity/350)})`;
  };

  return (
    <div className="container">
      <div className="header">
        <h1><Calculator size={24} className="text-indigo-600" /> OptionValuation<span style={{color: 'var(--text-muted)', fontWeight: 400}}>Pro</span></h1>
        <div className="mode-toggle">
          <button className={mode === 'bs' ? 'active' : ''} onClick={() => setMode('bs')}>Black-Scholes</button>
          <button className={mode === 'merton' ? 'active' : ''} onClick={() => setMode('merton')}>Merton</button>
        </div>
      </div>

      <div className={`main-layout ${showMath && !isMobile ? 'with-math' : ''}`}>
        
        {/* LEFT: INPUTS */}
        <div className="card input-panel">
          <div className="input-row">
             <select name="type" value={inputs.type} onChange={handleChange}>
               <option value="call">Call Option</option>
               <option value="put">Put Option</option>
             </select>
          </div>

          <div className="input-section-title">Contract Details</div>
          {[
            { label: 'Spot Price', key: 'spot', min: 1, max: 500, step: 1 },
            { label: 'Strike Price', key: 'strike', min: 1, max: 500, step: 1 },
            { label: 'Time (Years)', key: 'time', min: 0.01, max: 5, step: 0.1 },
          ].map(field => (
            <div className="slider-group" key={field.key}>
              <div className="slider-header">
                <label>{field.label}</label>
                <div className="input-wrapper">
                  <input type="number" value={inputs[field.key]} onChange={(e) => handleInput(field.key, e.target.value)} />
                </div>
              </div>
              <input type="range" min={field.min} max={field.max} step={field.step} value={inputs[field.key]} onChange={(e) => handleSlide(field.key, e.target.value)} />
            </div>
          ))}

          <div className="input-section-title">Market Conditions</div>
          {[
            { label: 'Volatility', key: 'volatility', min: 0.01, max: 1.5, step: 0.01 },
            { label: 'Risk-Free Rate', key: 'rate', min: 0, max: 0.2, step: 0.005 },
          ].map(field => (
            <div className="slider-group" key={field.key}>
              <div className="slider-header">
                <label>{field.label}</label>
                <div className="input-wrapper">
                  <input type="number" value={inputs[field.key]} step={field.step} onChange={(e) => handleInput(field.key, e.target.value)} />
                </div>
              </div>
              <input type="range" min={field.min} max={field.max} step={field.step} value={inputs[field.key]} onChange={(e) => handleSlide(field.key, e.target.value)} />
            </div>
          ))}

          {mode === 'merton' && (
             <div className="slider-group">
               <div className="slider-header">
                <label>Dividend Yield</label>
                <div className="input-wrapper">
                  <input type="number" value={inputs.dividend} step="0.01" onChange={(e) => handleInput('dividend', e.target.value)} />
                </div>
              </div>
               <input type="range" min="0" max="0.2" step="0.005" value={inputs.dividend} onChange={(e) => handleSlide('dividend', e.target.value)} />
             </div>
          )}
        </div>

        {/* CENTER: CHARTS */}
        <div className="center-panel">
          {data ? (
            <>
              <div className="kpi-row">
                <div className="kpi-item main-price">
                   <span>Theoretical Price</span>
                   <div className="flex items-center justify-center gap-2">
                      {loading && <Loader2 className="animate-spin" size={14} />}
                      <h2 style={{fontSize: '1.6rem'}}>${data.price.toFixed(2)}</h2>
                   </div>
                </div>
                <div className="kpi-item"><span>Delta</span> <div className="kpi-value">{data.greeks.delta}</div></div>
                <div className="kpi-item"><span>Gamma</span> <div className="kpi-value">{data.greeks.gamma}</div></div>
                <div className="kpi-item"><span>Theta</span> <div className="kpi-value">{data.greeks.theta}</div></div>
                <div className="kpi-item"><span>Vega</span> <div className="kpi-value">{data.greeks.vega}</div></div>
              </div>

              <div className="card viz-card">
                <div className="tabs">
                  <div className="tabs-left">
                    <button className={activeTab === 'chart' ? 'active-tab' : ''} onClick={() => setActiveTab('chart')}>
                        <TrendingUp size={16} /> Price
                    </button>
                    <button className={activeTab === 'greeks' ? 'active-tab' : ''} onClick={() => setActiveTab('greeks')}>
                        <Activity size={16} /> Greeks
                    </button>
                    <button className={activeTab === 'heatmap' ? 'active-tab' : ''} onClick={() => setActiveTab('heatmap')}>
                        <Grid size={16} /> Heatmap
                    </button>
                  </div>

                  {/* RIGHT CONTROLS: Zoom & Math Toggle */}
                  <div className="controls-right">
                    {(activeTab === 'chart' || activeTab === 'greeks') && (
                      <div className="zoom-controls">
                        <button onClick={() => handleZoom('out')} disabled={zoomLevel >= 1} title="Zoom Out">
                            <ZoomOut size={16}/>
                        </button>
                        <span className="zoom-label">{(100/zoomLevel).toFixed(0)}%</span>
                        <button onClick={() => handleZoom('in')} disabled={zoomLevel <= 0.2} title="Zoom In">
                            <ZoomIn size={16}/>
                        </button>
                      </div>
                    )}
                    
                    {!isMobile && (
                      <button className={`math-toggle ${showMath ? 'active-math' : ''}`} onClick={() => setShowMath(!showMath)}>
                        <BookOpen size={16} /> {showMath ? "Hide Details" : "Show Details"}
                      </button>
                    )}
                  </div>
                </div>

                <div className="viz-content">
                  {activeTab === 'chart' && (
                    <ResponsiveContainer width="100%" height="100%">
                      <LineChart data={getZoomedData()} margin={{ top: 10, right: 30, bottom: 0, left: 0 }}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" vertical={false} />
                        <XAxis 
                          dataKey="spot" 
                          type="number"
                          domain={['auto', 'auto']} 
                          axisLine={false}
                          tickLine={false}
                          tick={{ fill: '#64748B', fontSize: 12 }}
                          dy={10}
                          allowDataOverflow={true}
                        />
                        <YAxis 
                          domain={['auto', 'auto']} 
                          axisLine={false}
                          tickLine={false}
                          tick={{ fill: '#64748B', fontSize: 12 }}
                        />
                        <Tooltip contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 20px rgba(0,0,0,0.1)' }} />
                        <Legend verticalAlign="top" height={30} iconSize={10} wrapperStyle={{ fontSize: '12px'}} />
                        <Line type="monotone" dataKey="price" stroke="var(--primary)" strokeWidth={3} dot={false} isAnimationActive={!loading} name="Option Price" />
                        <Line type="monotone" dataKey="payoff" stroke="#CBD5E1" strokeWidth={2} strokeDasharray="4 4" dot={false} isAnimationActive={!loading} name="Intrinsic Value" />
                        <ReferenceLine x={inputs.spot} stroke="#EF4444" strokeDasharray="3 3" label={{ value: "Spot", fontSize: 10, fill: "#EF4444", position: "insideTop" }} />
                      </LineChart>
                    </ResponsiveContainer>
                  )}

                  {activeTab === 'greeks' && (
                    <div className="greeks-charts-grid">
                      <GreekChart 
                        title="Delta (Δ)" color="#10B981" data={getZoomedData()} dataKey="delta" 
                        spot={inputs.spot} loading={loading}
                      />
                      <GreekChart 
                        title="Gamma (Γ)" color="#8B5CF6" data={getZoomedData()} dataKey="gamma" 
                        spot={inputs.spot} loading={loading}
                      />
                      <GreekChart 
                        title="Theta (Θ)" color="#F59E0B" data={getZoomedData()} dataKey="theta" 
                        spot={inputs.spot} loading={loading}
                      />
                      <GreekChart 
                        title="Vega (ν)" color="#EF4444" data={getZoomedData()} dataKey="vega" 
                        spot={inputs.spot} loading={loading}
                      />
                    </div>
                  )}

                  {activeTab === 'heatmap' && (
                    <div className="heatmap-wrapper">
                      <div className="heatmap-grid">
                         <div className="heatmap-header" style={{borderTopLeftRadius: 8}}>Vol</div>
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
                </div>
              </div>
            </>
          ) : (
            <div className="flex h-full items-center justify-center text-muted">
               <Loader2 className="animate-spin mr-2" /> Initializing...
            </div>
          )}
        </div>

        {/* RIGHT: MATH */}
        {(showMath || isMobile) && data && (
          <div className="right-panel">
            <MathWalkthrough inputs={inputs} results={data} mode={mode} />
          </div>
        )}
      </div>
    </div>
  );
};

// Small helper component for the Greeks charts
const GreekChart = ({ title, color, data, dataKey, spot, loading }) => (
  <div className="greek-chart-card">
    <div className="greek-chart-header" style={{ color: color }}>
      {title}
    </div>
    <div style={{ width: '100%', height: '100%' }}>
      <ResponsiveContainer>
        <LineChart data={data} margin={{ top: 5, right: 10, bottom: 0, left: -20 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" vertical={false} />
          <XAxis dataKey="spot" type="number" domain={['auto', 'auto']} hide />
          <YAxis domain={['auto', 'auto']} tick={{ fontSize: 10 }} width={30} axisLine={false} tickLine={false} />
          <Tooltip contentStyle={{ fontSize: '11px', borderRadius: '4px', padding: '5px' }} />
          <Line 
            type="monotone" 
            dataKey={dataKey} 
            stroke={color} 
            strokeWidth={2} 
            dot={false} 
            isAnimationActive={!loading}
          />
          <ReferenceLine x={spot} stroke="#94a3b8" strokeDasharray="3 3" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  </div>
);

export default App;
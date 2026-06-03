// --- START OF FILE src/components/VolatilitySurface.jsx ---

import React, { useState } from 'react';
import Plotly from 'plotly.js-dist-min';
import createPlotlyComponent from 'react-plotly.js/factory';

const Plot = (createPlotlyComponent.default || createPlotlyComponent)(Plotly);

const VolatilitySurface = ({ 
  heatmapData, 
  heatmapSpots,
  spotTimeData,
  spotTimeSteps,
  volTimeData,
  volTimeSteps,
  volSurfaceStrike,
  volSurfaceDelta,
  gatheralTotalVar,
  gatheralDual,
  gatheralSvi,
  gatheralPdf,
  gatheralDynamics
}) => {
  if (!heatmapData || !heatmapSpots) return null;

  // Track the active projection view state
  const [dimMode, setDimMode] = useState('smile_delta');

  // Track dynamic smile paradigm state for Gatheral dynamics view
  const [dynModel, setDynModel] = useState('local');

  // Crisp Light Mode colors (fits white cards flawlessly)
  const gridColor = '#CBD5E1'; // Light grey modern grid lines
  const axisBgColor = '#F8FAFC';
  const textColor = '#0F172A'; // High-contrast dark slate text
  const surfaceGridColor = 'rgba(15, 23, 42, 0.45)';

  // Build the traces array dynamically
  let x, y, z, hoverTemplate;
  let traces = [];
  let xAxisTitle = 'Spot ($)';
  let yAxisTitle = 'Volatility (%)';
  let zAxisTitle = 'Option Price ($)';
  let xAxisFormat = '.2f';
  let yAxisFormat = '.0%';
  let zAxisFormat = '.4f';
  let layoutTitle = 'Option Price Surface';

  if (dimMode === 'smile_delta' && volSurfaceDelta) {
    xAxisTitle = 'Delta';
    yAxisTitle = 'Tenor / Maturity';
    zAxisTitle = 'Implied Vol (%)';
    layoutTitle = 'Implied Volatility Surface (Delta)';
    xAxisFormat = ''; 
    yAxisFormat = ''; 
    zAxisFormat = '.1f';
    traces = [{
      x: volSurfaceDelta.deltas,
      y: volSurfaceDelta.tenors,
      z: volSurfaceDelta.matrix,
      type: 'surface',
      showscale: false, 
      colorscale: 'Jet',
      hovertemplate: '<b>Delta:</b> %{x}<br><b>Tenor:</b> %{y}<br><b>Implied Vol:</b> %{z:.2f}%<extra></extra>',
      contours: {
        x: { show: true, color: surfaceGridColor, width: 1, usecolormap: false },
        y: { show: true, color: surfaceGridColor, width: 1, usecolormap: false },
        z: { show: false }
      }
    }];
  } else if (dimMode === 'smile_strike' && volSurfaceStrike) {
    xAxisTitle = 'Strike ($)';
    yAxisTitle = 'Tenor / Maturity';
    zAxisTitle = 'Implied Vol (%)';
    layoutTitle = 'Implied Volatility Surface (Strike)';
    xAxisFormat = '.2f';
    yAxisFormat = ''; 
    zAxisFormat = '.1f';
    traces = [{
      x: volSurfaceStrike.strikes,
      y: volSurfaceStrike.tenors,
      z: volSurfaceStrike.matrix,
      type: 'surface',
      showscale: false, 
      colorscale: 'Jet',
      hovertemplate: '<b>Strike:</b> $%{x:.2f}<br><b>Tenor:</b> %{y}<br><b>Implied Vol:</b> %{z:.2f}%<extra></extra>',
      contours: {
        x: { show: true, color: surfaceGridColor, width: 1, usecolormap: false },
        y: { show: true, color: surfaceGridColor, width: 1, usecolormap: false },
        z: { show: false }
      }
    }];
  } else if (dimMode === 'gatheral_total_var' && gatheralTotalVar) {
    xAxisTitle = 'Log-Moneyness (y)';
    yAxisTitle = 'Time to Expiry (T)';
    zAxisTitle = 'Total Variance (w)';
    layoutTitle = 'Total Implied Variance Surface (w = σ²T)';
    xAxisFormat = '.2f';
    yAxisFormat = '.2f';
    zAxisFormat = '.5f';
    traces = [{
      x: gatheralTotalVar.log_moneyness,
      y: gatheralTotalVar.tenors,
      z: gatheralTotalVar.matrix,
      type: 'surface',
      showscale: false,
      colorscale: 'Jet',
      hovertemplate: '<b>Moneyness (y):</b> %{x:.2f}<br><b>Expiry (T):</b> %{y:.2f} Yrs<br><b>Total Var (w):</b> %{z:.5f}<extra></extra>',
      contours: {
        x: { show: true, color: surfaceGridColor, width: 1, usecolormap: false },
        y: { show: true, color: surfaceGridColor, width: 1, usecolormap: false },
        z: { show: false }
      }
    }];
  } else if (dimMode === 'gatheral_dual' && gatheralDual) {
    xAxisTitle = 'Log-Moneyness (y)';
    yAxisTitle = 'Time to Expiry (T)';
    zAxisTitle = 'Volatility (%)';
    layoutTitle = 'Dual-Surface: Implied vs. Dupire Local Volatility';
    xAxisFormat = '.2f';
    yAxisFormat = '.2f';
    zAxisFormat = '.1f';
    
    // Implied Volatility Surface (Jet)
    traces.push({
      x: gatheralDual.log_moneyness,
      y: gatheralDual.tenors,
      z: gatheralDual.implied,
      type: 'surface',
      showscale: false,
      colorscale: 'Jet',
      name: 'Implied Vol',
      opacity: 0.9,
      hovertemplate: '<b>[Implied]</b><br>Moneyness: %{x:.2f}<br>Expiry: %{y:.2f}<br>IV: %{z:.1f}%<extra></extra>',
      contours: {
        x: { show: true, color: 'rgba(0,0,0,0.5)', width: 1, usecolormap: false },
        y: { show: true, color: 'rgba(0,0,0,0.5)', width: 1, usecolormap: false }
      }
    });
    // Local Volatility Surface (Hot - showing twice as steep near T->0 via 1/2 Rule)
    traces.push({
      x: gatheralDual.log_moneyness,
      y: gatheralDual.tenors,
      z: gatheralDual.local,
      type: 'surface',
      showscale: false,
      colorscale: 'Hot',
      name: 'Local Vol (Dupire)',
      opacity: 0.6,
      hovertemplate: '<b>[Local (Dupire)]</b><br>Moneyness: %{x:.2f}<br>Expiry: %{y:.2f}<br>LV: %{z:.1f}%<extra></extra>',
      contours: {
        x: { show: true, color: 'rgba(255,255,255,0.4)', width: 1, usecolormap: false },
        y: { show: true, color: 'rgba(255,255,255,0.4)', width: 1, usecolormap: false }
      }
    });
  } else if (dimMode === 'gatheral_svi' && gatheralSvi) {
    xAxisTitle = 'Log-Moneyness (y)';
    yAxisTitle = 'Time to Expiry (T)';
    zAxisTitle = 'Volatility (%)';
    layoutTitle = 'SVI Fit Calibration vs. Option Bids/Asks Spreads';
    xAxisFormat = '.2f';
    yAxisFormat = '.2f';
    zAxisFormat = '.1f';
    
    // Continuous SVI Fitted Surface
    traces.push({
      x: gatheralSvi.log_moneyness,
      y: gatheralSvi.tenors,
      z: gatheralSvi.svi,
      type: 'surface',
      showscale: false,
      colorscale: 'Viridis',
      opacity: 0.8,
      name: 'SVI Fit',
      hovertemplate: '<b>SVI Fit Vol:</b> %{z:.1f}%<extra></extra>',
      contours: {
        x: { show: true, color: 'rgba(255,255,255,0.3)', width: 1 },
        y: { show: true, color: 'rgba(255,255,255,0.3)', width: 1 }
      }
    });
    
    // Overlay 3D scatter points representing raw Bid quotes
    const bidsX = [];
    const bidsY = [];
    const bidsZ = [];
    const asksX = [];
    const asksY = [];
    const asksZ = [];
    
    gatheralSvi.tenors.forEach((t, i) => {
      gatheralSvi.log_moneyness.forEach((y, j) => {
        // Sample every second point to avoid overcrowding
        if ((i + j) % 2 === 0) {
          bidsX.push(y); bidsY.push(t); bidsZ.push(gatheralSvi.bids[i][j]);
          asksX.push(y); asksY.push(t); asksZ.push(gatheralSvi.asks[i][j]);
        }
      });
    });

    traces.push({
      x: bidsX, y: bidsY, z: bidsZ,
      type: 'scatter3d',
      mode: 'markers',
      name: 'Bids',
      marker: { size: 2.5, color: '#3B82F6', opacity: 0.9 },
      hovertemplate: '<b>Market Bid:</b> %{z:.1f}%<extra></extra>'
    });
    
    traces.push({
      x: asksX, y: asksY, z: asksZ,
      type: 'scatter3d',
      mode: 'markers',
      name: 'Asks',
      marker: { size: 2.5, color: '#EF4444', opacity: 0.9 },
      hovertemplate: '<b>Market Ask:</b> %{z:.1f}%<extra></extra>'
    });
  } else if (dimMode === 'gatheral_pdf' && gatheralPdf) {
    xAxisTitle = 'Strike ($)';
    yAxisTitle = 'Time to Expiry (T)';
    zAxisTitle = 'PDF Density ϕ(K)';
    layoutTitle = 'Breeden-Litzenberger Risk-Neutral PDF (Arbitrage Check)';
    xAxisFormat = '.1f';
    yAxisFormat = '.2f';
    zAxisFormat = '.5f';
    
    // Custom colorscale highlighting the butterfly arbitrage violation (negative PDF) in bright red
    const pdfMatrix = gatheralPdf.matrix;
    const surfaceColor = pdfMatrix.map(row => row.map(val => val < 0 ? 1.0 : 0.0));
    
    traces = [{
      x: gatheralPdf.strikes,
      y: gatheralPdf.tenors,
      z: pdfMatrix,
      surfacecolor: surfaceColor,
      type: 'surface',
      showscale: false,
      colorscale: [[0.0, '#3B82F6'], [1.0, '#EF4444']], // Blue = Valid, Red = Vertical Arbitrage!
      hovertemplate: '<b>Strike:</b> $%{x:.1f}<br><b>Density:</b> %{z:.5f}<extra></extra>',
      contours: {
        x: { show: true, color: 'rgba(255,255,255,0.4)', width: 1 },
        y: { show: true, color: 'rgba(255,255,255,0.4)', width: 1 }
      }
    }];
  } else if (dimMode === 'gatheral_dynamics' && gatheralDynamics) {
    xAxisTitle = 'Log-Moneyness (y)';
    yAxisTitle = 'Time to Expiry (T)';
    zAxisTitle = 'Volatility (%)';
    xAxisFormat = '.2f';
    yAxisFormat = '.2f';
    zAxisFormat = '.1f';
    
    let dynZ = gatheralDynamics.local;
    if (dynModel === 'stoch') {
      dynZ = gatheralDynamics.stoch;
      layoutTitle = 'Stochastic Volatility Dynamics (Sticky Smile)';
    } else if (dynModel === 'jumps') {
      dynZ = gatheralDynamics.jumps;
      layoutTitle = 'Jump-Diffusion Dynamics (Steep Short-Term Skew)';
    } else {
      layoutTitle = 'Local Volatility Dynamics (Fast Smile Flattening)';
    }
    
    traces = [{
      x: gatheralDynamics.log_moneyness,
      y: gatheralDynamics.tenors,
      z: dynZ,
      type: 'surface',
      showscale: false,
      colorscale: 'Jet',
      hovertemplate: '<b>Moneyness:</b> %{x:.2f}<br><b>Vol:</b> %{z:.1f}%<extra></extra>',
      contours: {
        x: { show: true, color: surfaceGridColor, width: 1 },
        y: { show: true, color: surfaceGridColor, width: 1 }
      }
    }];
  } else if (dimMode === 'spot_time' && spotTimeData && spotTimeSteps) {
    x = heatmapSpots;
    y = spotTimeSteps; 
    z = spotTimeData.map(row => row.prices);
    xAxisTitle = 'Spot ($)';
    yAxisTitle = 'Time (Years)';
    zAxisTitle = 'Option Price ($)';
    layoutTitle = 'Option Price vs. Spot & Maturity';
    xAxisFormat = '.2f';
    yAxisFormat = '.2f';
    zAxisFormat = '.4f';
    traces = [{
      x: x, y: y, z: z,
      type: 'surface',
      showscale: false, colorscale: 'Jet', hovertemplate: hoverTemplate,
      contours: { x: { show: true, color: surfaceGridColor }, y: { show: true, color: surfaceGridColor } }
    }];
  } else if (dimMode === 'vol_time' && volTimeData && volTimeSteps) {
    x = volTimeSteps; 
    y = volTimeData.map(row => row.time); 
    z = volTimeData.map(row => row.prices);
    xAxisTitle = 'Volatility (%)';
    yAxisTitle = 'Time (Years)';
    zAxisTitle = 'Option Price ($)';
    layoutTitle = 'Option Price vs. Volatility & Maturity';
    xAxisFormat = '.0%';
    yAxisFormat = '.2f';
    zAxisFormat = '.4f';
    traces = [{
      x: x, y: y, z: z,
      type: 'surface',
      showscale: false, colorscale: 'Jet', hovertemplate: hoverTemplate,
      contours: { x: { show: true, color: surfaceGridColor }, y: { show: true, color: surfaceGridColor } }
    }];
  } else {
    // Default: Spot vs Volatility Option Price
    x = heatmapSpots;
    y = heatmapData.map(row => row.vol / 100);
    z = heatmapData.map(row => row.prices);
    xAxisTitle = 'Spot ($)';
    yAxisTitle = 'Volatility (%)';
    zAxisTitle = 'Option Price ($)';
    layoutTitle = 'Option Price vs. Spot & Volatility';
    xAxisFormat = '.2f';
    yAxisFormat = '.0%';
    zAxisFormat = '.4f';
    traces = [{
      x: x, y: y, z: z,
      type: 'surface',
      showscale: false, colorscale: 'Jet', hovertemplate: hoverTemplate,
      contours: { x: { show: true, color: surfaceGridColor }, y: { show: true, color: surfaceGridColor } }
    }];
  }

  return (
    <div style={{ width: '100%', height: '100%', display: 'flex', flexDirection: 'column', position: 'relative', flex: 1 }}>
      
      {/* Control bar above the 3D surface plot */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px', padding: '0 4px', flexShrink: 0, gap: '12px', flexWrap: 'wrap' }}>
        <h3 style={{ margin: 0, fontSize: '0.85rem', fontWeight: 700, color: '#0F172A' }}>{layoutTitle}</h3>
        <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
          
          {/* Dynamic Paradigm Toggles for the Dynamics View */}
          {dimMode === 'gatheral_dynamics' && (
            <div style={{ display: 'flex', gap: '4px', backgroundColor: '#F1F5F9', padding: '2px', borderRadius: '6px', marginRight: '4px' }}>
              <button 
                onClick={() => setDynModel('local')}
                style={{
                  padding: '4px 8px', fontSize: '0.7rem', fontWeight: 600, border: 'none', cursor: 'pointer',
                  borderRadius: '4px', backgroundColor: dynModel === 'local' ? '#FFFFFF' : 'transparent',
                  color: dynModel === 'local' ? '#1E293B' : '#64748B', boxShadow: dynModel === 'local' ? '0 1px 3px rgba(0,0,0,0.1)' : 'none'
                }}
              >Local Vol</button>
              <button 
                onClick={() => setDynModel('stoch')}
                style={{
                  padding: '4px 8px', fontSize: '0.7rem', fontWeight: 600, border: 'none', cursor: 'pointer',
                  borderRadius: '4px', backgroundColor: dynModel === 'stoch' ? '#FFFFFF' : 'transparent',
                  color: dynModel === 'stoch' ? '#1E293B' : '#64748B', boxShadow: dynModel === 'stoch' ? '0 1px 3px rgba(0,0,0,0.1)' : 'none'
                }}
              >Stochastic</button>
              <button 
                onClick={() => setDynModel('jumps')}
                style={{
                  padding: '4px 8px', fontSize: '0.7rem', fontWeight: 600, border: 'none', cursor: 'pointer',
                  borderRadius: '4px', backgroundColor: dynModel === 'jumps' ? '#FFFFFF' : 'transparent',
                  color: dynModel === 'jumps' ? '#1E293B' : '#64748B', boxShadow: dynModel === 'jumps' ? '0 1px 3px rgba(0,0,0,0.1)' : 'none'
                }}
              >Jumps (SVJ)</button>
            </div>
          )}

          {/* Primary View Selector Dropdown */}
          <select 
            value={dimMode} 
            onChange={(e) => setDimMode(e.target.value)}
            style={{
              padding: '6px 12px',
              borderRadius: '8px',
              border: '1px solid #CBD5E1',
              backgroundColor: '#FFFFFF',
              color: '#334155',
              fontSize: '0.8rem',
              fontWeight: 600,
              cursor: 'pointer',
              outline: 'none',
              transition: 'border-color 0.2s',
            }}
          >
            {/* Gatheral Advanced Volatility Surface Models */}
            <optgroup label="Jim Gatheral's Volatility Surface Guide">
              <option value="smile_delta">1. Vol Surface (by Delta) [Implied Vol %]</option>
              <option value="smile_strike">2. Vol Surface (by Strike) [Implied Vol %]</option>
              <option value="gatheral_total_var">3. Total Implied Variance (w = σ²T) [Log-Moneyness]</option>
              <option value="gatheral_dual">4. Implied vs Dupire Local Vol (1/2 Rule)</option>
              <option value="gatheral_svi">5. SVI Calibration Fit vs. Market Bids/Asks</option>
              <option value="gatheral_pdf">6. Arbitrage Diagnostics ( Breeden-Litzenberger PDF)</option>
              <option value="gatheral_dynamics">7. Dynamic Smile Evolution (Sticky vs. Flattening)</option>
            </optgroup>
            
            {/* Standard parameter grids */}
            <optgroup label="Standard Parameter Grids [Option Price]">
              <option value="spot_vol">Option Price vs Spot & Volatility</option>
              <option value="spot_time">Option Price vs Spot & Maturity</option>
              <option value="vol_time">Option Price vs Volatility & Maturity</option>
            </optgroup>
          </select>
        </div>
      </div>

      {/* Visual warning overlay for Arbitrage Diagnostics */}
      {dimMode === 'gatheral_pdf' && (
        <div style={{
          backgroundColor: 'rgba(239, 68, 68, 0.08)',
          border: '1px solid rgba(239, 68, 68, 0.2)',
          borderRadius: '8px',
          padding: '8px 12px',
          fontSize: '0.75rem',
          color: '#B91C1C',
          fontWeight: 600,
          marginBottom: '8px',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          flexShrink: 0
        }}>
          <span>⚠️ Butterfly (Vertical) Arbitrage detected at short expiry (T = 0.1) in extreme OTM strikes! Risk-neutral PDF dips negative.</span>
          <span style={{
            backgroundColor: '#EF4444',
            color: '#FFFFFF',
            padding: '2px 6px',
            borderRadius: '4px',
            fontSize: '0.65rem',
            fontWeight: 800
          }}>PDF &lt; 0 (RED REGION)</span>
        </div>
      )}

      {/* Visual note overlay for Dupire 1/2 Rule */}
      {dimMode === 'gatheral_dual' && (
        <div style={{
          backgroundColor: 'rgba(79, 70, 229, 0.06)',
          border: '1px solid rgba(79, 70, 229, 0.15)',
          borderRadius: '8px',
          padding: '8px 12px',
          fontSize: '0.75rem',
          color: '#4338CA',
          fontWeight: 600,
          marginBottom: '8px',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          flexShrink: 0
        }}>
          <span>📈 Gatheral 1/2 Rule: The Local Volatility smile skew (Red surface) is twice as steep as the Implied Volatility skew (Blue surface) near T → 0.</span>
          <span style={{ fontSize: '0.7rem', opacity: 0.85 }}>σ_L² ≈ 2 × σ_implied² (Skew Slope)</span>
        </div>
      )}

      <Plot
        data={traces}
        layout={{
          uirevision: 'constant', // PRESERVES 3D ROTATION & POSITION ON SLIDER HOVER / DATA RE-RENDERS
          autosize: true,
          margin: { l: 15, r: 15, b: 15, t: 15, pad: 0 }, 
          font: { family: 'Inter, sans-serif' },
          scene: {
            xaxis: { 
                title: {
                  text: xAxisTitle,
                  font: { size: 12.5, color: textColor, family: 'Inter, sans-serif', weight: 800 }
                },
                tickfont: { size: 11, color: textColor, family: 'Inter, sans-serif', weight: 700 },
                tickformat: xAxisFormat,
                gridcolor: gridColor,
                backgroundcolor: axisBgColor,
                showbackground: true
            },
            yaxis: { 
                title: {
                  text: yAxisTitle,
                  font: { size: 12.5, color: textColor, family: 'Inter, sans-serif', weight: 800 }
                },
                tickfont: { size: 11, color: textColor, family: 'Inter, sans-serif', weight: 700 },
                tickformat: yAxisFormat,
                gridcolor: gridColor,
                backgroundcolor: axisBgColor,
                showbackground: true
            },
            zaxis: { 
                title: {
                  text: zAxisTitle,
                  font: { size: 12.5, color: textColor, family: 'Inter, sans-serif', weight: 800 }
                },
                tickfont: { size: 11, color: textColor, family: 'Inter, sans-serif', weight: 700 },
                tickformat: zAxisFormat,
                gridcolor: gridColor,
                backgroundcolor: axisBgColor,
                showbackground: true
            },
            // Closer camera coordinates to zoom in perfectly without cropping
            camera: {
              eye: { x: 1.1, y: 1.1, z: 0.8 } 
            },
            // Balanced aspectratio to prevent vertical squishing
            aspectratio: { x: 1.1, y: 1.1, z: 0.85 }
          },
          paper_bgcolor: 'rgba(0,0,0,0)',
          plot_bgcolor: 'rgba(0,0,0,0)',
          legend: {
            x: 0.85,
            y: 0.95,
            font: { size: 9, color: textColor },
            bgcolor: 'rgba(255,255,255,0.7)',
            bordercolor: '#CBD5E1',
            borderwidth: 1
          }
        }}
        useResizeHandler={true}
        style={{ width: '100%', height: '100%', flex: 1 }}
        config={{ displayModeBar: true, displaylogo: false, responsive: true }} 
      />
    </div>
  );
};

export default VolatilitySurface;
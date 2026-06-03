import React, { useState } from 'react';
import { BlockMath, InlineMath } from 'react-katex';
import { ChevronDown, ChevronUp, AlertTriangle, CheckCircle } from 'lucide-react';
import 'katex/dist/katex.min.css';

const BarrierWalkthrough = ({ inputs, results }) => {
  const [expanded, setExpanded] = useState({ 1: true, 2: false, 3: true });

  const toggleStep = (step) => {
    setExpanded((prev) => ({ ...prev, [step]: !prev[step] }));
  };

  const fmt = (num, digits = 4) => {
    if (num === undefined || num === null || isNaN(num)) return "-";
    return num.toFixed(digits);
  };

  // Inputs
  const S = inputs.spot || 100;
  const H = inputs.barrier || 120;
  const barrierType = inputs.barrierType || 'Up-and-Out';
  
  // Backend "intermediates" (Lambda, Barrier)
  const lambda = results.intermediates?.Lambda || 0;
  
  // Is it knocked out?
  const isKnockedOut = results.note === "Option Knocked Out";
  
  const adjustmentFactor = Math.pow(H / S, 2 * lambda);
  
  // Determine text for the logic
  const isOut = barrierType.includes('Out');
  const isUp = barrierType.includes('Up');

  return (
    <div className="math-steps">
      
      {/* --- STEP 1: BARRIER CHECK --- */}
      <div className={`step-card ${expanded[1] ? 'open' : ''}`}>
        <div className="step-trigger" onClick={() => toggleStep(1)}>
          <div className="step-info">
            <span className="step-circle">1</span>
            <span className="step-title-text">Barrier Condition</span>
          </div>
          <div className="step-summary-right">
             {isKnockedOut ? (
                <span className="text-red-500 font-bold flex items-center gap-1">
                    <AlertTriangle size={14} /> KNOCKED OUT
                </span>
             ) : (
                <span className="text-green-600 font-bold flex items-center gap-1">
                    <CheckCircle size={14} /> ACTIVE
                </span>
             )}
             {expanded[1] ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
          </div>
        </div>

        {expanded[1] && (
          <div className="step-content">
            <div className="breakdown-grid" style={{ gridTemplateColumns: '1fr 1fr' }}>
              <div className="breakdown-item">
                <span className="label">Spot Price (S)</span>
                <span className="value text-lg">${S}</span>
              </div>
              <div className="breakdown-item">
                <span className="label">Barrier Level (H)</span>
                <span className="value text-lg">${H}</span>
              </div>
            </div>

            <div className="p-3 bg-gray-50 rounded border border-gray-200 text-sm mt-3">
                <div className="flex justify-between items-center mb-1">
                    <span className="font-semibold text-muted">Condition:</span>
                    <span className="font-mono">{barrierType}</span>
                </div>
                <div className="text-center py-2 font-mono text-gray-700 bg-white rounded border border-dashed border-gray-300">
                    {isUp ? (
                        <span>Trigger if <InlineMath math={`S \\ge H`} /></span>
                    ) : (
                        <span>Trigger if <InlineMath math={`S \\le H`} /></span>
                    )}
                </div>
            </div>
          </div>
        )}
      </div>

      {/* --- STEP 2: REFLECTION FACTOR --- */}
      {!isKnockedOut && (
      <div className={`step-card ${expanded[2] ? 'open' : ''}`}>
        <div className="step-trigger" onClick={() => toggleStep(2)}>
          <div className="step-info">
            <span className="step-circle">2</span>
            <span className="step-title-text">Reflection Adjustment</span>
          </div>
          <div className="step-summary-right">
             <span className="mono-val">λ = {fmt(lambda, 2)}</span>
             {expanded[2] ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
          </div>
        </div>

        {expanded[2] && (
          <div className="step-content">
            <div className="latex-box">
              <BlockMath math={`\\lambda = \\frac{r - q + \\sigma^2/2}{\\sigma^2}`} />
            </div>
            
            <div className="breakdown-grid" style={{gridTemplateColumns: '1fr 1fr'}}>
                <div className="breakdown-item">
                    <span className="label">Curvature (Lambda)</span>
                    <span className="value">{fmt(lambda, 2)}</span>
                </div>
                <div className="breakdown-item">
                    <span className="label">Adjust Factor <InlineMath math="(H/S)^{2\lambda}" /></span>
                    <span className="value">{fmt(adjustmentFactor, 4)}</span>
                </div>
            </div>
          </div>
        )}
      </div>
      )}

      {/* --- STEP 3: VALUATION --- */}
      <div className={`step-card ${expanded[3] ? 'open' : ''}`}>
        <div className="step-trigger" onClick={() => toggleStep(3)}>
          <div className="step-info">
            <span className="step-circle">3</span>
            <span className="step-title-text">Valuation</span>
          </div>
          <div className="step-summary-right">
             <span className="text-primary font-bold text-lg">${fmt(results.price, 2)}</span>
             {expanded[3] ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
          </div>
        </div>

        {expanded[3] && (
          <div className="step-content">
            {isKnockedOut ? (
                <div className="text-center text-muted p-4">Option is worthless.</div>
            ) : (
                <div className="latex-box small-latex mb-3">
                  {isOut ? (
                    <BlockMath math={`V = V_{vanilla} - (H/S)^{2\\lambda} \\cdot V_{vanilla}`} />
                  ) : (
                    <BlockMath math={`V = (H/S)^{2\\lambda} \\cdot V_{vanilla}`} />
                  )}
                </div>
            )}
          </div>
        )}
      </div>

    </div>
  );
};

export default BarrierWalkthrough;
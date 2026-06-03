// --- START OF FILE src/ModelExplanation.jsx ---

import React, { useState } from 'react';
import { BlockMath, InlineMath } from 'react-katex';
import { BookOpen, ChevronDown, ChevronUp, Calculator, Variable, Binary, TrendingUp } from 'lucide-react';
import 'katex/dist/katex.min.css';

const ModelExplanation = ({ data }) => {
  const [isOpen, setIsOpen] = useState(false);

  if (!data) return null;

  return (
    <div className={`step-card ${isOpen ? 'open' : ''} mt-4`}>
      {/* Header / Trigger */}
      <div 
        className="step-trigger bg-slate-50 border-b border-slate-100" 
        onClick={() => setIsOpen(!isOpen)}
      >
        <div className="step-info">
          <BookOpen size={18} className="text-indigo-600" />
          <div className="flex flex-col">
            <span className="step-title-text text-slate-700">Textbook Reference</span>
            <span className="text-xs text-muted">Based on {data.source}</span>
          </div>
        </div>
        <div className="step-summary-right">
          {isOpen ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
        </div>
      </div>

      {/* Content */}
      {isOpen && (
        <div className="step-content bg-white p-0">
          
          {/* 1. Core Concept */}
          <div className="p-4 border-b border-slate-100">
            <h4 className="text-sm font-bold text-slate-800 flex items-center gap-2 mb-2">
              <Binary size={14} className="text-blue-500"/> 1. The Core Concept
            </h4>
            <div className="text-sm text-slate-600 space-y-2 leading-relaxed">
              {data.concept.map((paragraph, idx) => (
                <p key={idx}>{paragraph}</p>
              ))}
            </div>
          </div>

          {/* 2. Formulas */}
          <div className="p-4 border-b border-slate-100 bg-slate-50/50">
            <h4 className="text-sm font-bold text-slate-800 flex items-center gap-2 mb-3">
              <Variable size={14} className="text-purple-500"/> 2. The Formulas
            </h4>
            
            {data.formulas.map((item, idx) => (
              <div key={idx} className="mb-4 last:mb-0">
                <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">{item.label}:</span>
                <div className="latex-box bg-white border border-slate-200 mt-1">
                  <BlockMath math={item.math} />
                </div>
              </div>
            ))}

            {data.where && (
              <div className="mt-4">
                <span className="text-xs font-semibold text-slate-500">Where:</span>
                <div className="latex-box bg-white border border-slate-200 mt-1">
                   {data.where.map((eq, i) => <BlockMath key={i} math={eq} />)}
                </div>
              </div>
            )}
          </div>

          {/* 3. Notation */}
          <div className="p-4 border-b border-slate-100">
             <h4 className="text-sm font-bold text-slate-800 mb-2">3. Notation Definitions</h4>
             <ul className="grid grid-cols-1 gap-2 text-sm">
                {data.notation.map((n, i) => (
                    <li key={i} className="flex items-baseline gap-2">
                        <span className="font-mono font-bold text-slate-700 w-8 text-right"><InlineMath math={n.symbol} /></span>
                        <span className="text-slate-400">:</span>
                        <span className="text-slate-600">{n.def}</span>
                    </li>
                ))}
             </ul>
          </div>

          {/* 4. Generalized Context */}
          <div className="p-4 border-b border-slate-100 bg-yellow-50/30">
             <h4 className="text-sm font-bold text-slate-800 mb-2">4. Generalized BSM Context</h4>
             <p className="text-sm text-slate-600 mb-2">{data.contextText}</p>
             <div className="text-center">
                 <InlineMath math={data.contextMath} />
             </div>
          </div>

          {/* 5. Numerical Example */}
          <div className="p-4 border-b border-slate-100 bg-slate-50">
            <h4 className="text-sm font-bold text-slate-800 flex items-center gap-2 mb-3">
              <Calculator size={14} className="text-green-600"/> 5. Numerical Example (Page {data.examplePage})
            </h4>
            <div className="grid grid-cols-2 gap-4 text-sm">
                <div className="bg-white p-3 rounded border border-slate-200">
                    <h5 className="font-semibold text-slate-500 text-xs uppercase mb-2">Inputs</h5>
                    <ul className="space-y-1">
                        {data.example.inputs.map((inp, i) => (
                            <li key={i} className="flex justify-between">
                                <span>{inp.label} <InlineMath math={inp.sym} />:</span>
                                <span className="font-mono font-bold">{inp.val}</span>
                            </li>
                        ))}
                    </ul>
                </div>
                <div className="bg-white p-3 rounded border border-slate-200">
                    <h5 className="font-semibold text-slate-500 text-xs uppercase mb-2">Calculations</h5>
                    <ul className="space-y-1">
                         {data.example.calcs.map((calc, i) => (
                            <li key={i} className="flex justify-between">
                                <span><InlineMath math={calc.sym} /> =</span>
                                <span className="font-mono">{calc.val}</span>
                            </li>
                        ))}
                    </ul>
                    <div className="mt-3 pt-2 border-t border-dashed border-slate-300 flex justify-between items-center">
                        <span className="font-bold text-indigo-700">Result (c):</span>
                        <span className="font-mono font-bold text-lg text-indigo-700">{data.example.result}</span>
                    </div>
                </div>
            </div>
          </div>

          {/* 6. The Greeks (NEW SECTION) */}
          {data.greeks && (
            <div className="p-4 bg-orange-50/30">
                <h4 className="text-sm font-bold text-slate-800 flex items-center gap-2 mb-3">
                    <TrendingUp size={14} className="text-orange-600"/> 6. The Greeks (Chapter 2)
                </h4>
                <div className="space-y-4">
                    {data.greeks.map((greek, i) => (
                        <div key={i} className="bg-white border border-slate-200 rounded p-3">
                            <div className="flex justify-between items-baseline mb-1">
                                <span className="font-bold text-slate-700">{greek.name}</span>
                                <span className="text-xs text-slate-400">{greek.reference}</span>
                            </div>
                            <p className="text-xs text-slate-600 mb-2">{greek.concept}</p>
                            <div className="latex-box bg-slate-50 border border-slate-100 mb-2">
                                <BlockMath math={greek.math} />
                            </div>
                            {greek.note && (
                                <div className="text-xs text-slate-500 italic border-l-2 border-orange-300 pl-2">
                                    Note: {greek.note}
                                </div>
                            )}
                        </div>
                    ))}
                </div>
            </div>
          )}

        </div>
      )}
    </div>
  );
};

export default ModelExplanation;
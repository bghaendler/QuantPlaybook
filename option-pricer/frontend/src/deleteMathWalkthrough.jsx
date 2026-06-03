// --- START OF FILE src/MathWalkthrough.jsx ---

import React from 'react';
import { BookOpen } from 'lucide-react';
import SharedGreeks from './SharedGreeks'; // Import from src/
import BSMWalkthrough from './models/BSMWalkthrough';
import BarrierWalkthrough from './models/BarrierWalkthrough';
import MertonWalkthrough from './models/MertonWalkthrough';
import AsayWalkthrough from './models/AsayWalkthrough';
import GarmanWalkthrough from './models/GarmanWalkthrough';
import GeneralizedBSMWalkthrough from './models/GeneralizedBSMWalkthrough';

const MathWalkthrough = ({ modelId, inputs, results }) => {
  
  const renderModelSpecificContent = () => {
    switch (modelId) {
      case 'bsm':
      case 'black76': 
        return <BSMWalkthrough inputs={inputs} results={results} />;
      
      case 'gen_bsm':
        return <GeneralizedBSMWalkthrough inputs={inputs} results={results} />;

      case 'garman':
        return <GarmanWalkthrough inputs={inputs} results={results} />;

      case 'merton':
        return <MertonWalkthrough inputs={inputs} results={results} />;

      case 'asay':
        return <AsayWalkthrough inputs={inputs} results={results} />;
      
      case 'barrier_std':
      case 'double_barrier':
      case 'partial_barrier':
      case 'look_barrier':
      case 'soft_barrier':
      case 'discrete_barrier':
      case 'binary_barrier':
        return <BarrierWalkthrough inputs={inputs} results={results} />;

      default:
        return (
          <div className="p-4 bg-gray-50 rounded text-sm text-center text-muted border border-dashed border-gray-200">
            Detailed math breakdown for <strong>{modelId.toUpperCase()}</strong> is currently being implemented. 
          </div>
        );
    }
  };

  return (
    <div className="math-container">
      <div className="math-header border-b pb-2 mb-4">
        <h2 className="text-lg font-bold flex items-center gap-2">
          <BookOpen size={18} className="text-indigo-600" /> The Math Engine
        </h2>
        <p className="text-xs text-muted">Step-by-step derivation</p>
      </div>

      {/* MOVED TO TOP */}
      <SharedGreeks greeks={results.greeks} />

      <div className="mt-6">
        {renderModelSpecificContent()}
      </div>
    </div>
  );
};

export default MathWalkthrough;
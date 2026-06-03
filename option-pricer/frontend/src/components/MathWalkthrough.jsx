import React, { useState } from 'react';
import { BookOpen, Hash, Variable, ChevronRight, Calculator } from 'lucide-react';

// --- Import All Walkthrough Components ---
import BSMWalkthrough from '../models/BSMWalkthrough';
import BarrierWalkthrough from '../models/BarrierWalkthrough';
import MertonWalkthrough from '../models/MertonWalkthrough';
import AsayWalkthrough from '../models/AsayWalkthrough';
import GarmanWalkthrough from '../models/GarmanWalkthrough';
import GeneralizedBSMWalkthrough from '../models/GeneralizedBSMWalkthrough';
import Black76Walkthrough from '../models/Black76Walkthrough';
import BrennerWalkthrough from '../models/BrennerWalkthrough';
import Black76FWalkthrough from '../models/Black76FWalkthrough';
import BachelierWalkthrough from '../models/BachelierWalkthrough';
import ModifiedBachelierWalkthrough from '../models/ModifiedBachelierWalkthrough';
import SprenkleWalkthrough from '../models/SprenkleWalkthrough';
import BonessWalkthrough from '../models/BonessWalkthrough';
import BAWWalkthrough from '../models/BAWWalkthrough';
import BS93Walkthrough from '../models/BS93Walkthrough';
import Bs2002Walkthrough from '../models/Bs2002Walkthrough';
import McKeanWalkthrough from '../models/McKeanWalkthrough';
import RollGeskeWhaleyWalkthrough from '../models/RollGeskeWhaleyWalkthrough';
import VilligerWalkthrough from '../models/VilligerWalkthrough';
import SamuelsonWalkthrough from '../models/SamuelsonWalkthrough';
import VariablePurchaseWalkthrough from '../models/VariablePurchaseWalkthrough';
import ExecutiveStockOptionWalkthrough from '../models/ExecutiveStockOptionWalkthrough';
import EscrowedWalkthrough from '../models/EscrowedWalkthrough';
import HHLWalkthrough from '../models/HHLWalkthrough';
import BosVandermarkWalkthrough from '../models/BosVandermarkWalkthrough';
import MargrabeWalkthrough from '../models/MargrabeWalkthrough';

const MathWalkthrough = ({ modelId, inputs, results, highlightedVar, onHighlight, onCollapse }) => {
  const [showNumbers, setShowNumbers] = useState(true);
  const [activeView, setActiveView] = useState('calc');

  const renderModelSpecificContent = () => {
    // Pass activeView down to render calculation vs documentation
    const props = { inputs, results, showNumbers, highlightedVar, onHighlight, activeView };

    switch (modelId) {
      // --- 1. General & Derivatives ---
      case 'bsm': return <BSMWalkthrough {...props} />;
      case 'black76': return <Black76Walkthrough {...props} />;
      case 'black76f': return <Black76FWalkthrough {...props} />;
      case 'gen_bsm': return <GeneralizedBSMWalkthrough {...props} />;
      case 'garman': return <GarmanWalkthrough {...props} />;
      case 'merton': return <MertonWalkthrough {...props} />;
      case 'asay': return <AsayWalkthrough {...props} />;
      case 'brenner': return <BrennerWalkthrough {...props} />;

      // --- 2. Pre-Black-Scholes ---
      case 'bachelier': return <BachelierWalkthrough {...props} />;
      case 'mod_bachelier': return <ModifiedBachelierWalkthrough {...props} />;
      case 'sprenkle': return <SprenkleWalkthrough {...props} />;
      case 'boness': return <BonessWalkthrough {...props} />;
      case 'samuelson': return <SamuelsonWalkthrough {...props} />;

      // --- 3. American Options ---
      case 'baw': return <BAWWalkthrough {...props} />;
      case 'bjerksund93': return <BS93Walkthrough {...props} />;
      case 'bjerksund02': return <Bs2002Walkthrough {...props} />;
      case 'mckean': return <McKeanWalkthrough {...props} />;
      case 'roll_geske': return <RollGeskeWhaleyWalkthrough {...props} />;
      case 'villiger': return <VilligerWalkthrough {...props} />;

      // --- 4. Exotic: Path-Independent ---
      case 'var_purchase': return <VariablePurchaseWalkthrough {...props} />;
      case 'exec_stock': return <ExecutiveStockOptionWalkthrough {...props} />;

      // --- 10. Discrete Dividends ---
      case 'escrowed': return <EscrowedWalkthrough {...props} />;
      case 'hhl': return <HHLWalkthrough {...props} />;
      case 'bos_vandermark': return <BosVandermarkWalkthrough {...props} />;
      case 'margrabe': return <MargrabeWalkthrough {...props} />;

      // --- 5. Exotic: Path-Dependent (Barriers) ---
      case 'barrier_std':
      case 'double_barrier':
      case 'partial_barrier':
      case 'look_barrier':
      case 'soft_barrier':
      case 'discrete_barrier':
      case 'binary_barrier':
        return <BarrierWalkthrough {...props} />;

      default:
        return (
          <div className="p-6 bg-slate-50 rounded-lg text-sm text-center text-slate-500 border-2 border-dashed border-slate-200 mt-4">
            <p className="mb-2 font-semibold text-slate-700">Detailed math breakdown for <strong>{modelId ? modelId.toUpperCase() : "THIS MODEL"}</strong> is currently being implemented.</p>
            <p>The calculation engine is active, but the educational walkthrough is under construction.</p>
          </div>
        );
    }
  };

  return (
    <div className="math-container">
      <div className="math-header border-b border-slate-100 pb-2 mb-4 flex items-center justify-between">
        
        {/* Left side: Clean title */}
        <h2 className="text-sm font-bold text-slate-800 m-0 flex items-center gap-2">
          <BookOpen size={16} className="text-indigo-600" />
          The Math Engine
        </h2>

        {/* Right side: 3 sleek minimalistic icon buttons */}
        <div className="math-header-actions">
          {/* 1. Numbers / Symbols Toggle */}
          <button
            onClick={() => setShowNumbers(!showNumbers)}
            className="math-header-icon-btn"
            title={showNumbers ? "Switch to Algebraic Symbols" : "Switch to Calculated Numbers"}
          >
            {showNumbers ? (
              <Hash size={14} className="text-blue-500" />
            ) : (
              <Variable size={14} className="text-purple-500" />
            )}
          </button>

          {/* 2. Calc / Doc Toggle */}
          <button
            onClick={() => setActiveView(activeView === 'calc' ? 'doc' : 'calc')}
            className="math-header-icon-btn"
            title={activeView === 'calc' ? "Switch to Written Documentation" : "Switch to Live Calculation Breakdown"}
          >
            {activeView === 'calc' ? (
              <Calculator size={14} className="text-emerald-500" />
            ) : (
              <BookOpen size={14} className="text-indigo-500" />
            )}
          </button>

          {/* 3. Collapse Panel */}
          {onCollapse && (
            <button
              onClick={onCollapse}
              className="math-header-icon-btn math-header-collapse-btn"
              title="Collapse Math Engine"
            >
              <ChevronRight size={14} />
            </button>
          )}
        </div>
      </div>

      <div className="mt-2">
        {renderModelSpecificContent()}
      </div>
    </div>
  );
};

export default MathWalkthrough;
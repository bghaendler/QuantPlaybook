import React from 'react';
import { TrendingUp, Activity, Clock, Percent, Globe, Gauge, ChevronRight } from 'lucide-react';

const GreekCard = ({ label, value, description, Icon, theme, onClick }) => {
  // Format value safely
  const displayVal = (value === undefined || value === null || isNaN(value))
    ? "-"
    : value.toFixed(4);

  return (
    <div
      className={`greek-card-modern theme-${theme} ${onClick ? 'clickable' : ''}`}
      onClick={onClick}
    >
      {onClick && (
        <div className="card-chevron">
          <ChevronRight size={16} />
        </div>
      )}

      <div className="card-top">
        <div className="label-group">
          <span className="card-label">{label}</span>
        </div>
        <div className="icon-box">
          <Icon size={18} strokeWidth={2.5} />
        </div>
      </div>

      <div className="card-value">
        {displayVal}
      </div>

      <div className="card-desc">
        {description}
      </div>
    </div>
  );
};

const SharedGreeks = ({ greeks, onGreekClick }) => {
  return (
    <div className="greek-section">
      <div className="section-header">
        <h2 className="section-title">
          <Activity size={16} />
          Risk Sensitivities
        </h2>
        <div className="header-line"></div>
      </div>

      <div className="greek-grid-modern">
        <GreekCard
          label="Delta (Δ)"
          value={greeks?.delta}
          description="Spot Price Sensitivity"
          Icon={TrendingUp}
          theme="emerald"
          onClick={onGreekClick ? () => onGreekClick('delta') : undefined}
        />
        <GreekCard
          label="Gamma (Γ)"
          value={greeks?.gamma}
          description="Convexity Rate"
          Icon={Activity}
          theme="violet"
          onClick={onGreekClick ? () => onGreekClick('gamma') : undefined}
        />
        <GreekCard
          label="Theta (Θ)"
          value={greeks?.theta}
          description="Time Decay / Day"
          Icon={Clock}
          theme="amber"
          onClick={onGreekClick ? () => onGreekClick('theta') : undefined}
        />
        <GreekCard
          label="Vega (ν)"
          value={greeks?.vega}
          description="Volatility Exposure"
          Icon={Gauge}
          theme="red"
          onClick={onGreekClick ? () => onGreekClick('vega') : undefined}
        />
        <GreekCard
          label="Rho (ρ)"
          value={greeks?.rho}
          description="Domestic Rate Risk"
          Icon={Percent}
          theme="blue"
          onClick={onGreekClick ? () => onGreekClick('rho') : undefined}
        />
        <GreekCard
          label="Phi (Φ)"
          value={greeks?.phi}
          description="Foreign Rate Risk"
          Icon={Globe}
          theme="indigo"
          onClick={onGreekClick ? () => onGreekClick('phi') : undefined}
        />
      </div>
    </div>
  );
};

export default SharedGreeks;
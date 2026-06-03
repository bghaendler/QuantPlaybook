// --- START OF FILE src/config/models.js ---

export const CATEGORIES = {
  GEN: "1. General BSM & Derivatives",
  PRE: "2. Pre-Black-Scholes Models",
  AME: "3. American Options",
  EX_PI: "4. Exotic: Path-Independent",
  EX_PD: "5. Exotic: Path-Dependent",
  MULTI: "6. Exotic: Multi-Asset",
  ASIAN: "7. Asian (Average Rate)",
  VOL: "8. Volatility & Variance",
  RATES: "9. Interest Rate & Bond",
  DIV: "10. Discrete Dividends"
};

// --- TEXTBOOK SPECIFIC INPUTS (Haug, 2nd Ed) ---

// 1. Black-Scholes (1973) - Stock Option
// Matches Haug p.42 Example: S=60, X=65, T=0.25, r=8%, v=30%
const INPUTS_BSM_HAUG = [
  { id: 'spot', label: 'Spot Price (S)', type: 'slider', min: 10, max: 150, step: 1, default: 60 },
  { id: 'strike', label: 'Strike Price (K)', type: 'slider', min: 10, max: 150, step: 1, default: 65 },
  { id: 'time', label: 'Time (Years)', type: 'slider', min: 0.01, max: 2, step: 0.01, default: 0.25 },
  { id: 'rate', label: 'Risk-Free Rate (r)', type: 'slider', min: 0, max: 0.2, step: 0.001, default: 0.08 },
  { id: 'volatility', label: 'Volatility (σ)', type: 'slider', min: 0.01, max: 1.0, step: 0.01, default: 0.30 },
  { id: 'dividend', label: 'Dividend (q)', type: 'number', default: 0.0 } // Hidden/Zero for standard BS
];

// 2. Merton (1973) - Continuous Dividend
// Matches Haug p.43 Example: S=100, X=95, T=0.5, r=10%, q=5%, v=20%
const INPUTS_MERTON_HAUG = [
  { id: 'spot', label: 'Spot Price (S)', type: 'slider', min: 50, max: 200, step: 1, default: 100 },
  { id: 'strike', label: 'Strike Price (K)', type: 'slider', min: 50, max: 200, step: 1, default: 95 },
  { id: 'time', label: 'Time (Years)', type: 'slider', min: 0.01, max: 2, step: 0.01, default: 0.5 },
  { id: 'rate', label: 'Risk-Free Rate (r)', type: 'slider', min: 0, max: 0.2, step: 0.001, default: 0.10 },
  { id: 'dividend', label: 'Dividend Yield (q)', type: 'slider', min: 0, max: 0.2, step: 0.001, default: 0.05 },
  { id: 'volatility', label: 'Volatility (σ)', type: 'slider', min: 0.01, max: 1.0, step: 0.01, default: 0.20 }
];

// 3. Black-76 (Futures)
// Matches Haug p.44 Example: F=19, X=19, T=0.75, r=10%, v=28%
const INPUTS_BLACK76_HAUG = [
  { id: 'spot', label: 'Futures Price (F)', type: 'slider', min: 10, max: 50, step: 0.5, default: 19 },
  { id: 'strike', label: 'Strike Price (K)', type: 'slider', min: 10, max: 50, step: 0.5, default: 19 },
  { id: 'time', label: 'Time (Years)', type: 'slider', min: 0.01, max: 2, step: 0.01, default: 0.75 },
  { id: 'rate', label: 'Risk-Free Rate (r)', type: 'slider', min: 0, max: 0.2, step: 0.001, default: 0.10 },
  { id: 'volatility', label: 'Volatility (σ)', type: 'slider', min: 0.01, max: 1.0, step: 0.01, default: 0.28 },
  { id: 'dividend', label: 'Cost of Carry (b)', type: 'number', default: 0.0 }
];

// 4. Asay (1982) - Margined Futures
// Matches Haug p.45 Example: F=4200, X=3800, T=0.75, v=15%
const INPUTS_ASAY_HAUG = [
  { id: 'spot', label: 'Futures Price (F)', type: 'slider', min: 2000, max: 6000, step: 50, default: 4200 },
  { id: 'strike', label: 'Strike Price (K)', type: 'slider', min: 2000, max: 6000, step: 50, default: 3800 },
  { id: 'time', label: 'Time (Years)', type: 'slider', min: 0.01, max: 2, step: 0.01, default: 0.75 },
  { id: 'rate', label: 'Risk-Free Rate (r)', type: 'number', default: 0.0 },
  { id: 'volatility', label: 'Volatility (σ)', type: 'slider', min: 0.01, max: 1.0, step: 0.01, default: 0.15 },
  { id: 'dividend', label: 'Cost of Carry (b)', type: 'number', default: 0.0 }
];

// 5. Garman-Kohlhagen (1983) - FX
// Matches Haug p.46 Example: S=1.56, K=1.60, T=0.5, r=6%, rf=8%, v=12%
const INPUTS_GARMAN_HAUG = [
  { id: 'spot', label: 'Exchange Rate (S)', type: 'slider', min: 1.0, max: 2.0, step: 0.01, default: 1.56 },
  { id: 'strike', label: 'Strike Price (K)', type: 'slider', min: 1.0, max: 2.0, step: 0.01, default: 1.60 },
  { id: 'time', label: 'Time (Years)', type: 'slider', min: 0.01, max: 2, step: 0.01, default: 0.5 },
  { id: 'rate', label: 'Domestic Rate (r)', type: 'slider', min: 0, max: 0.2, step: 0.001, default: 0.06 },
  { id: 'dividend', label: 'Foreign Rate (rf)', type: 'slider', min: 0, max: 0.2, step: 0.001, default: 0.08 },
  { id: 'volatility', label: 'Volatility (σ)', type: 'slider', min: 0.01, max: 1.0, step: 0.01, default: 0.12 }
];

// 6. Generalized BSM - Cost of Carry
const INPUTS_GEN_BSM = [
  { id: 'spot', label: 'Spot Price (S)', type: 'slider', min: 50, max: 150, step: 1, default: 75 },
  { id: 'strike', label: 'Strike Price (K)', type: 'slider', min: 50, max: 150, step: 1, default: 70 },
  { id: 'time', label: 'Time (Years)', type: 'slider', min: 0.01, max: 2, step: 0.01, default: 0.5 },
  { id: 'rate', label: 'Risk-Free Rate (r)', type: 'slider', min: 0, max: 0.2, step: 0.001, default: 0.10 },
  { id: 'dividend', label: 'Carry Deduction (q)', type: 'slider', min: -0.1, max: 0.2, step: 0.001, default: 0.05 }, // b = r - q
  { id: 'volatility', label: 'Volatility', type: 'slider', min: 0.01, max: 1.0, step: 0.01, default: 0.35 }
];

const INPUTS_BLACK76F_HAUG = [
  { id: 'spot', label: 'Forward Price (F)', type: 'slider', min: 10, max: 50, step: 0.5, default: 19 },
  { id: 'strike', label: 'Strike Price (K)', type: 'slider', min: 10, max: 50, step: 0.5, default: 19 },
  { id: 'time', label: 'Option Time (T)', type: 'slider', min: 0.01, max: 2, step: 0.01, default: 0.75 },
  // We repurpose 'spot2' or add a specific field. Let's use 'time_forward' concept mapped to a generic field or handled in UI.
  // For simplicity in this architecture, we'll map 'dividend' to 'Time to Forward (Tf)' via label, 
  // but physically it's the 'dividend' field in the payload.
  { id: 'dividend', label: 'Forward Expiry (Tf)', type: 'slider', min: 0.01, max: 3, step: 0.01, default: 1.0 },
  { id: 'rate', label: 'Risk-Free Rate (r)', type: 'slider', min: 0, max: 0.2, step: 0.001, default: 0.10 },
  { id: 'volatility', label: 'Volatility (σ)', type: 'slider', min: 0.01, max: 1.0, step: 0.01, default: 0.28 }
];

// --- GENERIC SCHEMAS (For models not yet customized) ---

const INPUTS_GENERIC = [
  { id: 'spot', label: 'Spot Price', type: 'slider', min: 1, max: 500, step: 1, default: 100 },
  { id: 'strike', label: 'Strike Price', type: 'slider', min: 1, max: 500, step: 1, default: 100 },
  { id: 'time', label: 'Time (Years)', type: 'slider', min: 0.01, max: 5, step: 0.01, default: 1 },
  { id: 'rate', label: 'Risk-Free Rate', type: 'slider', min: 0, max: 0.2, step: 0.001, default: 0.05 },
  { id: 'volatility', label: 'Volatility', type: 'slider', min: 0.01, max: 2.0, step: 0.01, default: 0.2 },
  { id: 'dividend', label: 'Dividend/Yield', type: 'slider', min: 0, max: 0.2, step: 0.001, default: 0.0 }
];

// Matches Haug p.84 Example: F=70, X=70, T=0.25, r=5%, b=0, v=28%
const INPUTS_BRENNER_HAUG = [
  { id: 'spot', label: 'Spot/Futures (S)', type: 'slider', min: 10, max: 200, step: 1, default: 70 },
  { id: 'strike', label: 'Strike (X)', type: 'slider', min: 10, max: 200, step: 1, default: 70 },
  { id: 'time', label: 'Time (Years)', type: 'slider', min: 0.01, max: 1, step: 0.01, default: 0.25 },
  { id: 'rate', label: 'Rate (r)', type: 'slider', min: 0, max: 0.2, step: 0.001, default: 0.05 },
  { id: 'dividend', label: 'Cost of Carry (b)', type: 'slider', min: -0.1, max: 0.1, step: 0.001, default: 0.0 },
  { id: 'volatility', label: 'Volatility', type: 'slider', min: 0.01, max: 1.0, step: 0.01, default: 0.28 }
];

// Bachelier (1900) - Normal/Arithmetic Model
// Matches Haug p.82-83: Uses absolute volatility (price units, not %)
const INPUTS_BACHELIER_HAUG = [
  { id: 'spot', label: 'Spot Price (S)', type: 'slider', min: 50, max: 150, step: 1, default: 100 },
  { id: 'strike', label: 'Strike Price (K)', type: 'slider', min: 50, max: 150, step: 1, default: 100 },
  { id: 'time', label: 'Time (Years)', type: 'slider', min: 0.01, max: 2, step: 0.01, default: 1 },
  { id: 'rate', label: 'Risk-Free Rate (r)', type: 'slider', min: 0, max: 0.2, step: 0.001, default: 0.05 },
  { id: 'dividend', label: 'Dividend Yield (q)', type: 'slider', min: 0, max: 0.2, step: 0.001, default: 0.0 },
  { id: 'volatility', label: 'Volatility (σ) [Price Units]', type: 'slider', min: 0.1, max: 50, step: 0.1, default: 20 },
  {
    id: 'info',
    type: 'info',
    text: '⚠️ Volatility is in absolute price units, not %. For S=100, σ=20% BSM ≈ σ=20 Bachelier'
  }
];


const INPUTS_BARRIER = [
  { ref: 'bsm' },
  { id: 'barrier', label: 'Barrier Level', type: 'slider', min: 50, max: 200, step: 1, default: 120 },
  { id: 'barrierType', label: 'Barrier Type', type: 'select', options: ['Up-and-Out', 'Up-and-In', 'Down-and-Out', 'Down-and-In'], default: 'Up-and-Out' },
  { id: 'rebate', label: 'Rebate', type: 'number', min: 0, max: 50, default: 0 }
];

const INPUTS_MULTI = [
  { ref: 'bsm' },
  { id: 'spot2', label: 'Asset 2 Spot', type: 'slider', min: 1, max: 500, default: 100 },
  { id: 'vol2', label: 'Asset 2 Vol', type: 'slider', min: 0.01, max: 2.0, default: 0.2 },
  { id: 'correlation', label: 'Correlation (ρ)', type: 'slider', min: -1, max: 1, step: 0.01, default: 0.5 }
];

const INPUTS_MARGRABE = [
  { id: 'spot', label: 'Asset 1 Spot (S1)', type: 'slider', min: 10, max: 250, step: 1, default: 101 },
  { id: 'volatility', label: 'Asset 1 Vol (σ1)', type: 'slider', min: 0.01, max: 1.0, step: 0.01, default: 0.18 },
  { id: 'dividend', label: 'Asset 1 Cost of Carry (b1)', type: 'slider', min: -0.1, max: 0.2, step: 0.001, default: 0.02 },
  { id: 'spot2', label: 'Asset 2 Spot (S2)', type: 'slider', min: 10, max: 250, step: 1, default: 104 },
  { id: 'vol2', label: 'Asset 2 Vol (σ2)', type: 'slider', min: 0.01, max: 1.0, step: 0.01, default: 0.12 },
  { id: 'dividend2', label: 'Asset 2 Cost of Carry (b2)', type: 'slider', min: -0.1, max: 0.2, step: 0.001, default: 0.04 },
  { id: 'q1', label: 'Asset 1 Qty (Q1)', type: 'slider', min: 0.1, max: 10, step: 0.1, default: 1.0 },
  { id: 'q2', label: 'Asset 2 Qty (Q2)', type: 'slider', min: 0.1, max: 10, step: 0.1, default: 1.0 },
  { id: 'correlation', label: 'Correlation (ρ)', type: 'slider', min: -0.99, max: 0.99, step: 0.01, default: 0.8 },
  { id: 'rate', label: 'Risk-Free Rate (r)', type: 'slider', min: 0, max: 0.2, step: 0.001, default: 0.10 },
  { id: 'time', label: 'Time (T) [Years]', type: 'slider', min: 0.01, max: 5.0, step: 0.01, default: 0.5 }
];

const INPUTS_STOCH_VOL = [
  { ref: 'bsm' },
  { id: 'kappa', label: 'Mean Reversion (κ)', type: 'number', default: 2.0 },
  { id: 'theta', label: 'Long Run Var (θ)', type: 'number', default: 0.04 },
  { id: 'xi', label: 'Vol of Vol (ξ)', type: 'number', default: 0.1 },
  { id: 'rho', label: 'Correlation (ρ)', type: 'slider', min: -1, max: 1, step: 0.1, default: -0.7 }
];

const INPUTS_ASIAN = [
  { ref: 'bsm' },
  { id: 'averageType', label: 'Avg Type', type: 'select', options: ['Arithmetic', 'Geometric'], default: 'Arithmetic' },
  { id: 'runningAvg', label: 'Running Avg', type: 'number', default: 100 }
];

// --- MODEL DEFINITIONS ---

export const MODELS = {
  // --- 1. General BSM & Derivatives ---
  bsm: { id: 'bsm', name: 'Black-Scholes (1973)', category: 'GEN', inputs: INPUTS_BSM_HAUG },
  merton: { id: 'merton', name: 'Merton (1973)', category: 'GEN', inputs: INPUTS_MERTON_HAUG },
  black76: { id: 'black76', name: 'Black-76 (Futures)', category: 'GEN', inputs: INPUTS_BLACK76_HAUG },
  asay: { id: 'asay', name: 'Asay (Margined Futures)', category: 'GEN', inputs: INPUTS_ASAY_HAUG },
  garman: { id: 'garman', name: 'Garman-Kohlhagen (FX)', category: 'GEN', inputs: INPUTS_GARMAN_HAUG },
  gen_bsm: { id: 'gen_bsm', name: 'Generalized BSM (Cost of Carry)', category: 'GEN', inputs: INPUTS_GEN_BSM },

  brenner: { id: 'brenner', name: 'Brenner-Subrahmanyam (1988)', category: 'GEN', inputs: INPUTS_BRENNER_HAUG },
  black76f: { id: 'black76f', name: 'Black-76F (Deferred Settlement)', category: 'GEN', inputs: INPUTS_BLACK76F_HAUG },


  // --- 2. Pre-Black-Scholes ---
  bachelier: { id: 'bachelier', name: 'Bachelier (1900) Arithmetic', category: 'PRE', inputs: INPUTS_BACHELIER_HAUG },
  mod_bachelier: {
    id: 'mod_bachelier',
    name: 'Modified Bachelier (Shifted)',
    category: 'PRE',
    inputs: [
      ...INPUTS_BACHELIER_HAUG,
      {
        id: 'shift',
        label: 'Shift Parameter (β)',
        type: 'slider',
        min: -50,
        max: 50,
        step: 0.5,
        default: 0
      },
      {
        id: 'info',
        type: 'info',
        text: 'β shifts the distribution. β=0 gives standard Bachelier. Use β to better calibrate to market prices.'
      }
    ]
  },
  sprenkle: {
    id: 'sprenkle',
    name: 'Sprenkle (1964)',
    category: 'PRE',
    inputs: [
      { id: 'spot', label: 'Spot Price (S)', type: 'slider', min: 50, max: 150, step: 1, default: 100 },
      { id: 'strike', label: 'Strike Price (K)', type: 'slider', min: 50, max: 150, step: 1, default: 100 },
      { id: 'time', label: 'Time (Years)', type: 'slider', min: 0.01, max: 2, step: 0.01, default: 1 },
      { id: 'rate', label: 'Expected Return (μ)', type: 'slider', min: 0, max: 0.3, step: 0.001, default: 0.10 },
      { id: 'volatility', label: 'Volatility (σ)', type: 'slider', min: 0.01, max: 1.0, step: 0.01, default: 0.30 },
      { id: 'dividend', label: '(unused)', type: 'number', default: 0.0 },
      {
        id: 'info',
        type: 'info',
        text: '⚠️ Sprenkle uses Expected Return (μ) instead of risk-free rate. No discounting on strike!'
      }
    ]
  },
  boness: {
    id: 'boness',
    name: 'Boness (1964)',
    category: 'PRE',
    inputs: [
      { id: 'spot', label: 'Spot Price (S)', type: 'slider', min: 50, max: 150, step: 1, default: 100 },
      { id: 'strike', label: 'Strike Price (K)', type: 'slider', min: 50, max: 150, step: 1, default: 100 },
      { id: 'time', label: 'Time (Years)', type: 'slider', min: 0.01, max: 2, step: 0.01, default: 1 },
      { id: 'rate', label: 'Expected Return (μ=r)', type: 'slider', min: 0, max: 0.3, step: 0.001, default: 0.10 },
      { id: 'volatility', label: 'Volatility (σ)', type: 'slider', min: 0.01, max: 1.0, step: 0.01, default: 0.30 },
      { id: 'dividend', label: '(unused)', type: 'number', default: 0.0 },
      {
        id: 'info',
        type: 'info',
        text: '✅ Boness improves on Sprenkle by discounting the strike! Uses μ in drift but discounts by r.'
      }
    ]
  },
  samuelson: { id: 'samuelson', name: 'Samuelson (1965)', category: 'PRE', inputs: INPUTS_GENERIC },

  // --- 3. American Options ---
  baw: {
    id: 'baw',
    name: 'Barone-Adesi Whaley (1987)',
    category: 'AME',
    inputs: [
      { id: 'spot', label: 'Spot Price (S)', type: 'slider', min: 50, max: 150, step: 1, default: 100 },
      { id: 'strike', label: 'Strike Price (K)', type: 'slider', min: 50, max: 150, step: 1, default: 100 },
      { id: 'time', label: 'Time (Years)', type: 'slider', min: 0.01, max: 2, step: 0.01, default: 1 },
      { id: 'rate', label: 'Risk-Free Rate (r)', type: 'slider', min: 0, max: 0.2, step: 0.001, default: 0.05 },
      { id: 'dividend', label: 'Dividend Yield (q)', type: 'slider', min: 0, max: 0.2, step: 0.001, default: 0.03 },
      { id: 'volatility', label: 'Volatility (σ)', type: 'slider', min: 0.01, max: 1.0, step: 0.01, default: 0.30 },
      {
        id: 'info',
        type: 'info',
        text: '🎯 BAW uses quadratic approximation for American options. Much faster than binomial trees! Early exercise considered automatically.'
      }
    ]
  },
  bjerksund93: {
    id: 'bjerksund93',
    name: 'Bjerksund-Stensland (1993)',
    category: 'AME',
    inputs: [
      { id: 'spot', label: 'Spot Price (S)', type: 'slider', min: 50, max: 150, step: 1, default: 100 },
      { id: 'strike', label: 'Strike Price (K)', type: 'slider', min: 50, max: 150, step: 1, default: 100 },
      { id: 'time', label: 'Time (Years)', type: 'slider', min: 0.01, max: 2, step: 0.01, default: 1 },
      { id: 'rate', label: 'Risk-Free Rate (r)', type: 'slider', min: 0, max: 0.2, step: 0.001, default: 0.05 },
      { id: 'dividend', label: 'Dividend Yield (q)', type: 'slider', min: 0, max: 0.2, step: 0.001, default: 0.03 },
      { id: 'volatility', label: 'Volatility (σ)', type: 'slider', min: 0.01, max: 1.0, step: 0.01, default: 0.30 },
      {
        id: 'info',
        type: 'info',
        text: '📊 BS93 improves on BAW with flat boundary approximation. 6x more accurate, especially for American puts!'
      }
    ]
  },
  bjerksund02: { id: 'bjerksund02', name: 'Bjerksund-Stensland (2002)', category: 'AME', inputs: INPUTS_GENERIC },
  mckean: {
    id: 'mckean',
    name: 'McKean/Merton (Perpetual)',
    category: 'AME',
    inputs: [
      { id: 'spot', label: 'Spot Price (S)', type: 'slider', min: 50, max: 150, step: 1, default: 100 },
      { id: 'strike', label: 'Strike Price (K)', type: 'slider', min: 50, max: 150, step: 1, default: 100 },
      // Time is irrelevant for perpetual but might be needed for graph/heatmap ranges, or kept as dummy.
      // Haug example uses standard params minus T.
      // Let's keep T but note it's unused for pricing.
      { id: 'time', label: 'Time (Unused)', type: 'slider', min: 0.1, max: 10, default: 1, disabled: true },
      { id: 'rate', label: 'Risk-Free Rate (r)', type: 'slider', min: 0, max: 0.2, step: 0.001, default: 0.10 },
      { id: 'dividend', label: 'Dividend Yield (q)', type: 'slider', min: 0, max: 0.2, step: 0.001, default: 0.08 },
      { id: 'volatility', label: 'Volatility (σ)', type: 'slider', min: 0.01, max: 1.0, step: 0.01, default: 0.25 },
      {
        id: 'info',
        type: 'info',
        text: '♾️ Perpetual Option: Time is infinite. The value depends only on Spot vs Optimal Barrier.'
      }
    ]
  },
  roll_geske: {
    id: 'roll_geske',
    name: 'Roll-Geske-Whaley (1977)',
    category: 'AME',
    inputs: [
      { id: 'spot', label: 'Spot Price (S)', type: 'slider', min: 50, max: 150, step: 1, default: 80 },
      { id: 'strike', label: 'Strike Price (K)', type: 'slider', min: 50, max: 150, step: 1, default: 82 },
      { id: 'time', label: 'Time (Years)', type: 'slider', min: 0.01, max: 2, step: 0.01, default: 0.3333 },
      { id: 'rate', label: 'Risk-Free Rate (r)', type: 'slider', min: 0, max: 0.2, step: 0.001, default: 0.06 },
      // Custom RGW Inputs
      { id: 'dividend', label: 'Dividend Amt (D)', type: 'number', default: 4.0 },
      { id: 'time_dividend', label: 'Time to Div (t)', type: 'slider', min: 0.01, max: 2, step: 0.01, default: 0.25 },

      { id: 'volatility', label: 'Volatility (σ)', type: 'slider', min: 0.01, max: 1.0, step: 0.01, default: 0.30 },
      {
        id: 'info',
        type: 'info',
        text: '💰 Discrete Dividend Model: Evaluates option as a compound option, considering early exercise just before the ex-dividend date.'
      }
    ]
  },
  villiger: {
    id: 'villiger',
    name: 'Villiger (2005)',
    category: 'AME',
    inputs: [
      { id: 'spot', label: 'Spot Price (S)', type: 'slider', min: 50, max: 150, step: 1, default: 100 },
      { id: 'strike', label: 'Strike Price (K)', type: 'slider', min: 50, max: 150, step: 1, default: 102 },
      { id: 'time', label: 'Time (Years)', type: 'slider', min: 0.01, max: 2, step: 0.01, default: 0.5 },
      { id: 'rate', label: 'Risk-Free Rate (r)', type: 'slider', min: 0, max: 0.2, step: 0.001, default: 0.10 },
      // Custom Villiger Inputs
      { id: 'dividend', label: 'Div Yield % (δ)', type: 'slider', min: 0, max: 0.2, step: 0.001, default: 0.05 },
      { id: 'time_dividend', label: 'Time to Div (t)', type: 'slider', min: 0.01, max: 2, step: 0.01, default: 0.25 },

      { id: 'volatility', label: 'Volatility (σ)', type: 'slider', min: 0.01, max: 1.0, step: 0.01, default: 0.15 },
      {
        id: 'info',
        type: 'info',
        text: '📈 Discrete Dividend Yield: Models a dividend paid as a PERCENTAGE of the stock price, avoiding RGW arbitrage issues.'
      }
    ]
  },

  // --- 4. Exotic: Path-Independent ---
  var_purchase: { id: 'var_purchase', name: 'Variable Purchase (Handley)', category: 'EX_PI', inputs: INPUTS_GENERIC },

  // Replace the existing exec_stock entry
  exec_stock: {
    id: 'exec_stock',
    name: 'Executive Stock Options (Jennergren)',
    category: 'EX_PI',
    inputs: [
      { id: 'spot', label: 'Spot Price (S)', type: 'slider', min: 10, max: 200, step: 1, default: 60 },
      { id: 'strike', label: 'Strike Price (K)', type: 'slider', min: 10, max: 200, step: 1, default: 64 },
      { id: 'time', label: 'Time (Years)', type: 'slider', min: 0.1, max: 10, step: 0.1, default: 2 },
      { id: 'rate', label: 'Risk-Free Rate (r)', type: 'slider', min: 0, max: 0.2, step: 0.001, default: 0.07 },
      { id: 'dividend', label: 'Dividend Yield (q)', type: 'slider', min: 0, max: 0.2, step: 0.001, default: 0.03 },
      { id: 'volatility', label: 'Volatility (σ)', type: 'slider', min: 0.01, max: 1.0, step: 0.01, default: 0.38 },
      // Custom input for this model
      { id: 'lambda', label: 'Exit Rate (λ)', type: 'slider', min: 0, max: 0.5, step: 0.01, default: 0.15 },
      {
        id: 'info',
        type: 'info',
        text: '📉 This model discounts the option value by the probability (e^-λT) that the employee leaves the company before expiration.'
      }
    ]
  },
  fwd_start: { id: 'fwd_start', name: 'Forward Start (Rubinstein)', category: 'EX_PI', inputs: INPUTS_GENERIC },
  ratchet: { id: 'ratchet', name: 'Ratchet (Cliquet)', category: 'EX_PI', inputs: INPUTS_GENERIC },
  time_switch: { id: 'time_switch', name: 'Time-Switch (Pechtl)', category: 'EX_PI', inputs: INPUTS_GENERIC },
  simple_chooser: { id: 'simple_chooser', name: 'Simple Chooser', category: 'EX_PI', inputs: INPUTS_GENERIC },
  complex_chooser: { id: 'complex_chooser', name: 'Complex Chooser', category: 'EX_PI', inputs: INPUTS_GENERIC },
  compound: { id: 'compound', name: 'Compound Options (Geske)', category: 'EX_PI', inputs: INPUTS_GENERIC },
  extendible: { id: 'extendible', name: 'Extendible Options', category: 'EX_PI', inputs: INPUTS_GENERIC },
  binary: { id: 'binary', name: 'Binary/Digital Options', category: 'EX_PI', inputs: INPUTS_GENERIC },
  gap: { id: 'gap', name: 'Gap Options', category: 'EX_PI', inputs: INPUTS_GENERIC },
  supershare: { id: 'supershare', name: 'Supershare (Hakansson)', category: 'EX_PI', inputs: INPUTS_GENERIC },

  // --- 5. Exotic: Path-Dependent (Barriers) ---
  // Standard Barrier uses Haug's specific barrier defaults (p.154)
  barrier_std: {
    id: 'barrier_std',
    name: 'Standard Barrier (Merton)',
    category: 'EX_PD',
    inputs: [
      { id: 'spot', label: 'Spot Price', type: 'slider', min: 50, max: 150, step: 1, default: 100 },
      { id: 'strike', label: 'Strike Price', type: 'slider', min: 50, max: 150, step: 1, default: 90 },
      { id: 'barrier', label: 'Barrier (H)', type: 'slider', min: 50, max: 150, step: 1, default: 95 },
      { id: 'time', label: 'Time (Years)', type: 'slider', min: 0.01, max: 2, step: 0.01, default: 0.5 },
      { id: 'rate', label: 'Rate (r)', type: 'slider', min: 0, max: 0.2, step: 0.001, default: 0.08 },
      { id: 'dividend', label: 'Cost of Carry Adj (b)', type: 'slider', min: -0.1, max: 0.2, step: 0.001, default: 0.04 }, // b=0.04
      { id: 'volatility', label: 'Volatility', type: 'slider', min: 0.01, max: 1.0, step: 0.01, default: 0.25 },
      { id: 'barrierType', label: 'Barrier Type', type: 'select', options: ['Up-and-Out', 'Up-and-In', 'Down-and-Out', 'Down-and-In'], default: 'Down-and-Out' },
      { id: 'rebate', label: 'Rebate', type: 'number', min: 0, max: 50, default: 3 }
    ]
  },
  double_barrier: { id: 'double_barrier', name: 'Double Barrier (Ikeda)', category: 'EX_PD', inputs: INPUTS_BARRIER },
  partial_barrier: { id: 'partial_barrier', name: 'Partial-Time Barrier', category: 'EX_PD', inputs: INPUTS_BARRIER },
  look_barrier: { id: 'look_barrier', name: 'Look-Barrier (Bermin)', category: 'EX_PD', inputs: INPUTS_BARRIER },
  soft_barrier: { id: 'soft_barrier', name: 'Soft-Barrier (Hart)', category: 'EX_PD', inputs: INPUTS_BARRIER },
  discrete_barrier: { id: 'discrete_barrier', name: 'Discrete Barrier (BGK)', category: 'EX_PD', inputs: INPUTS_BARRIER },
  binary_barrier: { id: 'binary_barrier', name: 'Binary Barrier', category: 'EX_PD', inputs: INPUTS_BARRIER },
  lookback_float: { id: 'lookback_float', name: 'Lookback Floating Strike', category: 'EX_PD', inputs: INPUTS_GENERIC },
  lookback_fixed: { id: 'lookback_fixed', name: 'Lookback Fixed Strike', category: 'EX_PD', inputs: INPUTS_GENERIC },
  extreme_spread: { id: 'extreme_spread', name: 'Extreme Spread', category: 'EX_PD', inputs: INPUTS_GENERIC },

  // --- 6. Multi-Asset ---
  margrabe: { id: 'margrabe', name: 'Exchange (Margrabe)', category: 'MULTI', inputs: INPUTS_MARGRABE },
  ame_exchange: { id: 'ame_exchange', name: 'American Exchange', category: 'MULTI', inputs: INPUTS_MULTI },
  rainbow: { id: 'rainbow', name: 'Rainbow (Min/Max)', category: 'MULTI', inputs: INPUTS_MULTI },
  spread: { id: 'spread', name: 'Spread (Kirk)', category: 'MULTI', inputs: INPUTS_MULTI },
  product: { id: 'product', name: 'Product/Quotient', category: 'MULTI', inputs: INPUTS_MULTI },
  dual_strike: { id: 'dual_strike', name: 'Dual-Strike', category: 'MULTI', inputs: INPUTS_MULTI },
  two_asset_barrier: { id: 'two_asset_barrier', name: 'Two-Asset Barrier', category: 'MULTI', inputs: [...INPUTS_MULTI, ...INPUTS_BARRIER] },
  quantos: { id: 'quantos', name: 'Quantos / FX-Linked', category: 'MULTI', inputs: INPUTS_MULTI },

  // --- 7. Asian ---
  asian_geo: { id: 'asian_geo', name: 'Geometric Average', category: 'ASIAN', inputs: INPUTS_ASIAN },
  asian_turnbull: { id: 'asian_turnbull', name: 'Turnbull & Wakeman', category: 'ASIAN', inputs: INPUTS_ASIAN },
  asian_levy: { id: 'asian_levy', name: 'Levy Approximation', category: 'ASIAN', inputs: INPUTS_ASIAN },
  asian_curran: { id: 'asian_curran', name: 'Curran Geometric', category: 'ASIAN', inputs: INPUTS_ASIAN },

  // --- 8. Volatility ---
  cev: { id: 'cev', name: 'CEV Model', category: 'VOL', inputs: INPUTS_GENERIC },
  jump_diffusion: { id: 'jump_diffusion', name: 'Merton Jump-Diffusion', category: 'VOL', inputs: INPUTS_GENERIC },
  gram_charlier: { id: 'gram_charlier', name: 'Jarrow-Rudd (Skew/Kurt)', category: 'VOL', inputs: INPUTS_GENERIC },
  corrado_su: { id: 'corrado_su', name: 'Corrado-Su', category: 'VOL', inputs: INPUTS_GENERIC },
  heston: { id: 'heston', name: 'Heston Stochastic Vol', category: 'VOL', inputs: INPUTS_STOCH_VOL },
  sabr: { id: 'sabr', name: 'SABR Model', category: 'VOL', inputs: INPUTS_STOCH_VOL },
  var_swap: { id: 'var_swap', name: 'Variance Swap', category: 'VOL', inputs: INPUTS_GENERIC },

  // --- 9. Interest Rates ---
  vasicek: { id: 'vasicek', name: 'Vasicek Model', category: 'RATES', inputs: INPUTS_GENERIC },
  ho_lee: { id: 'ho_lee', name: 'Ho & Lee', category: 'RATES', inputs: INPUTS_GENERIC },
  hull_white: { id: 'hull_white', name: 'Hull-White', category: 'RATES', inputs: INPUTS_GENERIC },
  bdt: { id: 'bdt', name: 'Black-Derman-Toy', category: 'RATES', inputs: INPUTS_GENERIC },
  jamshidian: { id: 'jamshidian', name: 'Jamshidian Bond Option', category: 'RATES', inputs: INPUTS_GENERIC },

  // --- 10. Discrete Dividends ---
  escrowed: {
    id: 'escrowed',
    name: 'Escrowed Dividend',
    category: 'DIV',
    inputs: [
      { id: 'spot', label: 'Spot Price (S)', type: 'slider', min: 50, max: 150, step: 1, default: 100 },
      { id: 'strike', label: 'Strike Price (K)', type: 'slider', min: 50, max: 150, step: 1, default: 90 },
      { id: 'time', label: 'Time (Years)', type: 'slider', min: 0.01, max: 2, step: 0.01, default: 0.75 },
      { id: 'rate', label: 'Risk-Free Rate (r)', type: 'slider', min: 0, max: 0.2, step: 0.001, default: 0.10 },
      { id: 'volatility', label: 'Volatility (σ)', type: 'slider', min: 0.01, max: 1.0, step: 0.01, default: 0.25 },
      { id: 'div1_amt', label: 'Div 1 Amount ($)', type: 'slider', min: 0, max: 10, step: 0.1, default: 2.0 },
      { id: 'div1_time', label: 'Div 1 Time (t1)', type: 'slider', min: 0, max: 2, step: 0.05, default: 0.25 },
      { id: 'div2_amt', label: 'Div 2 Amount ($)', type: 'slider', min: 0, max: 10, step: 0.1, default: 2.0 },
      { id: 'div2_time', label: 'Div 2 Time (t2)', type: 'slider', min: 0, max: 2, step: 0.05, default: 0.50 },
      { id: 'dividend', label: '(unused)', type: 'number', default: 0.0 },
      {
        id: 'info',
        type: 'info',
        text: '💡 Escrowed Dividend Model: Adjusts spot price by subtracting the present value of all expected dividends before option expiration: S_adj = S - Σ D_i e^(-r t_i). BSM formulas are then evaluated using S_adj.'
      }
    ]
  },
  hhl: {
    id: 'hhl',
    name: 'Haug-Haug Volatility Adj (HHL)',
    category: 'DIV',
    inputs: [
      { id: 'spot', label: 'Spot Price (S)', type: 'slider', min: 50, max: 150, step: 1, default: 100 },
      { id: 'strike', label: 'Strike Price (K)', type: 'slider', min: 50, max: 150, step: 1, default: 90 },
      { id: 'time', label: 'Time (Years)', type: 'slider', min: 0.01, max: 2, step: 0.01, default: 0.75 },
      { id: 'rate', label: 'Risk-Free Rate (r)', type: 'slider', min: 0, max: 0.2, step: 0.001, default: 0.10 },
      { id: 'volatility', label: 'Volatility (σ)', type: 'slider', min: 0.01, max: 1.0, step: 0.01, default: 0.25 },
      { id: 'div1_amt', label: 'Div 1 Amount ($)', type: 'slider', min: 0, max: 10, step: 0.1, default: 2.0 },
      { id: 'div1_time', label: 'Div 1 Time (t1)', type: 'slider', min: 0, max: 2, step: 0.05, default: 0.25 },
      { id: 'div2_amt', label: 'Div 2 Amount ($)', type: 'slider', min: 0, max: 10, step: 0.1, default: 2.0 },
      { id: 'div2_time', label: 'Div 2 Time (t2)', type: 'slider', min: 0, max: 2, step: 0.05, default: 0.50 },
      { id: 'dividend', label: '(unused)', type: 'number', default: 0.0 },
      {
        id: 'info',
        type: 'info',
        text: '💡 Haug-Haug Volatility Adjustment: Designed to work with the escrowed dividend model. It replaces the observed stock price with S_adj and adjusts volatility to σ_adj to account for the underestimation of absolute price volatility.'
      }
    ]
  },
  bos_vandermark: {
    id: 'bos_vandermark',
    name: 'Bos-Vandermark (BV)',
    category: 'DIV',
    inputs: [
      { id: 'spot', label: 'Spot Price (S)', type: 'slider', min: 50, max: 150, step: 1, default: 100 },
      { id: 'strike', label: 'Strike Price (K)', type: 'slider', min: 50, max: 150, step: 1, default: 100 },
      { id: 'time', label: 'Time (Years)', type: 'slider', min: 0.01, max: 2, step: 0.01, default: 1.0 },
      { id: 'rate', label: 'Risk-Free Rate (r)', type: 'slider', min: 0, max: 0.2, step: 0.001, default: 0.06 },
      { id: 'volatility', label: 'Volatility (σ)', type: 'slider', min: 0.01, max: 1.0, step: 0.01, default: 0.25 },
      { id: 'div1_amt', label: 'Div 1 Amount ($)', type: 'slider', min: 0, max: 10, step: 0.1, default: 4.0 },
      { id: 'div1_time', label: 'Div 1 Time (t1)', type: 'slider', min: 0, max: 2, step: 0.05, default: 0.50 },
      { id: 'div2_amt', label: 'Div 2 Amount ($)', type: 'slider', min: 0, max: 10, step: 0.1, default: 0.0 },
      { id: 'div2_time', label: 'Div 2 Time (t2)', type: 'slider', min: 0, max: 2, step: 0.05, default: 0.0 },
      { id: 'dividend', label: '(unused)', type: 'number', default: 0.0 },
      {
        id: 'info',
        type: 'info',
        text: '💡 Bos-Vandermark Method: Adjusts both the spot price S and the strike price K used in the standard BSM model. Excellent for fast approximations of European options with cash dividends.'
      }
    ]
  },
};

// --- Helper: Inheritance Resolver ---
export const getModelInputs = (modelId) => {
  // Default to BSM if modelId not found
  const model = MODELS[modelId] || MODELS['bsm'];

  // Flatten inherits (ref)
  return model.inputs.flatMap(input => {
    if (input.ref === 'bsm') return INPUTS_GENERIC;
    if (input.ref === 'barrier') return INPUTS_BARRIER;
    return input;
  });
};
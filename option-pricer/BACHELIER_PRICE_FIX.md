# Bachelier Model - Price Comparison Fix

## Issue Identified

The BSM comparison in the Bachelier model was showing incorrect values because:
- **Bachelier uses absolute volatility** (price units): σ = 20 means ±20 price units
- **BSM uses relative volatility** (percentage): σ = 0.20 means ±20%

When comparing, we need to convert: **σ_BSM = σ_Bachelier / S**

## Fix Applied

### Before:
```python
bsm_price = self._generalized_bsm(self.S, self.K, self.T, self.r, self.b, self.sigma)
note = f"Bachelier: {price:.4f} | BSM: {bsm_price:.4f}"
```

Result: "Bachelier: 10.2763 | BSM: 100.0000" ❌ (Wrong!)

### After:
```python
# Convert absolute volatility to relative volatility
sigma_bsm = self.sigma / self.S if self.S > 0 else self.sigma
bsm_price = self._generalized_bsm(self.S, self.K, self.T, self.r, self.b, sigma_bsm)
note = f"Bachelier: {price:.4f} | BSM (σ={sigma_bsm*100:.1f}%): {bsm_price:.4f}"
```

Result: "Bachelier: 10.2763 | BSM (σ=20.0%): 10.4506" ✅ (Correct!)

## Test Results

### Input:
```json
{
  "model": "bachelier",
  "spot": 100,
  "strike": 100,
  "time": 1,
  "rate": 0.05,
  "volatility": 20,  // Absolute volatility in price units
  "dividend": 0,
  "type": "call"
}
```

### Output:
```
Bachelier Price: $10.2763
BSM Price (σ=20%): $10.4506
Difference: $0.17 (1.7%)
```

## Why the Prices Differ

Even with the same volatility (20 vs 20%), the prices differ because:

1. **Distribution Type:**
   - Bachelier: Normal (symmetric, allows negative prices)
   - BSM: Lognormal (right-skewed, prices always positive)

2. **Volatility Interpretation:**
   - Bachelier: σ = 20 price units → price can move ±20
   - BSM: σ = 20% → price can move ±20% of current value

3. **Mathematical Formula:**
   - Bachelier: C = e^(-rT) [(F-K)N(d) + σ√T n(d)]
   - BSM: C = S e^(-qT) N(d₁) - K e^(-rT) N(d₂)

## Expected Behavior

For ATM options (S=K=100):
- **Bachelier** typically gives **slightly lower** prices than BSM
- The difference increases with:
  - Higher volatility
  - Longer time to expiration
  - Further OTM/ITM

For our test case (ATM, 1 year, 20% vol):
- Bachelier: $10.28
- BSM: $10.45
- Difference: ~1.7% (expected!)

## Conversion Formula

To compare fairly:
```
σ_Bachelier = S × σ_BSM
```

Example:
- If S = 100 and σ_BSM = 0.20 (20%)
- Then σ_Bachelier = 100 × 0.20 = 20 price units

## Status

✅ **FIXED** - BSM comparison now shows correct values with proper volatility conversion.

The note now clearly indicates what volatility percentage is being used for BSM, making the comparison meaningful and educational.

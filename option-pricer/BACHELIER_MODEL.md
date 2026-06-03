# Bachelier (1900) Arithmetic Option Model

## Overview

The Bachelier model is the **first option pricing model in history**, developed by Louis Bachelier in his 1900 doctoral thesis "Théorie de la Spéculation" - 73 years before Black-Scholes!

## Key Features

### Mathematical Foundation
- Uses **normal (Gaussian) distribution** instead of lognormal distribution
- Assumes **arithmetic (absolute) price changes** rather than geometric (percentage) returns
- Allows for the **possibility of negative prices** (unlike Black-Scholes)

### When to Use Bachelier

The Bachelier model is particularly useful for:

1. **Interest Rate Options** - Where rates can go negative
2. **Commodity Spreads** - Where spread values center around zero
3. **Low Volatility Scenarios** - When percentage vs absolute changes matter less
4. **Near-ATM Options** - Where both models converge
5. **Short-dated Options** - Where the normal assumption is more reasonable

### Differences from Black-Scholes

| Aspect | Black-Scholes-Merton | Bachelier |
|--------|---------------------|-----------|
| Distribution | Lognormal | Normal |
| Returns | Geometric (%) | Arithmetic (absolute) |
| Price Range | S > 0 (cannot go negative) | S can be negative |
| Volatility | Percentage (σ) | Absolute (σ) |
| Delta | Varies with S | More linear |
| Gamma | Higher for ATM | Constant-like behavior |

## Implementation Details

### Pricing Formula

**Call Option:**
```
C = e^(-rT) * [(F - K) * N(d) + σ√T * n(d)]
```

**Put Option:**
```
P = e^(-rT) * [(K - F) * N(-d) + σ√T * n(d)]
```

Where:
- `F = S * e^(bT)` - Forward price with cost of carry
- `d = (F - K) / (σ√T)` - Normalized distance to strike
- `N(·)` - Standard normal cumulative distribution  
- `n(·)` - Standard normal probability density
- `σ` - Absolute volatility (in price units, not percentage)

### Greeks

**Delta:**
```
Call: Δ = e^(-rT) * e^(bT) * N(d)
Put:  Δ = -e^(-rT) * e^(bT) * N(-d)
```

**Gamma:**
```
Γ = (e^(-rT) * e^(bT) * n(d)) / (σ√T)
```

Note: Gamma is approximately constant (doesn't scale with 1/S like BSM)

**Vega:**
```
ν = e^(-rT) * n(d) * √T / 100
```

**Theta:**
```
Call: Θ = -r*e^(-rT)*[(F-K)*N(d) + σ√T*n(d)] + b*e^(-rT)*e^(bT)*S*N(d) - e^(-rT)*σ*n(d)/(2√T)
Put:  [Similar with sign adjustments]
```

**Rho:**
```
Call: ρ = -T * e^(-rT) * [(F - K) * N(d) + σ√T * n(d)]
Put:  [Similar with N(-d)]
```

## API Usage

### Request

```bash
curl -X POST http://localhost:8000/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "bachelier",
    "spot": 100,
    "strike": 100,
    "time": 1,
    "rate": 0.05,
    "volatility": 0.2,
    "dividend": 0,
    "type": "call"
  }'
```

### Response

```json
{
  "price": 4.8771,
  "greeks": {
    "delta": 1.0000,
    "gamma": 0.0000,
    "vega": 0.0000,
    "theta": 0.0130,
    "rho": -0.0488,
    "phi": 0.0
  },
  "d1": 0.25,
  "d2": 0.05,
  "Nd1": 0.5987,
  "Nd2": 0.5199,
  "note": "Bachelier: 4.8771 | BSM: 10.4506"
}
```

The `note` field shows a comparison between Bachelier and Black-Scholes-Merton prices for reference.

## Example Scenarios

### Example 1: At-the-Money Option
```json
{
  "model": "bachelier",
  "spot": 100,
  "strike": 100,
  "time": 1,
  "rate": 0.05,
  "volatility": 0.2,
  "type": "call"
}
```
Result: Price ≈ 4.88 (vs BSM ≈ 10.45)

### Example 2: Interest Rate Option
```json
{
  "model": "bachelier",
  "spot": 0.02,
  "strike": 0.02,
  "time": 0.5,
  "rate": 0.01,
  "volatility": 0.005,
  "type": "call"
}
```
Useful for modeling options on rates that can go negative.

### Example 3: Commodity Spread Option
```json
{
  "model": "bachelier",
  "spot": 5.0,
  "strike": 5.0,
  "time": 0.25,
  "rate": 0.03,
  "volatility": 2.0,
  "type": "put"
}
```

## Comparison with Other Models

### Bachelier vs BSM Pricing

For an ATM option (S=K=100, T=1, r=5%, σ=20%):

- **Bachelier**: C ≈ 4.88
- **BSM**: C ≈ 10.45

The difference occurs because:
1. Bachelier uses absolute volatility (20 price units)
2. BSM uses relative volatility (20%)
3. They converge as vol → 0 or for very short maturities

### Volatility Conversion

To convert BSM volatility to Bachelier volatility:
```
σ_Bachelier ≈ S * σ_BSM
```

For S=100, σ_BSM=20%:
```
σ_Bachelier ≈ 100 * 0.20 = 20 price units
```

## Historical Context

- **1900**: Louis Bachelier publishes his thesis
- **1973**: Black, Scholes, and Merton publish their famous paper
- **2010s**: Bachelier model gains renewed interest for negative interest rate environments
- **Today**: Used extensively in interest rate derivatives and SABR model

## References

- Bachelier, L. (1900). "Théorie de la spéculation"
- Haug, E. G. (2007). "The Complete Guide to Option Pricing Formulas", Section 2.3.1
- Wystup, U. (2006). "FX Options and Structured Products"

## Cost of Carry

The Bachelier model in this implementation uses:
```
b = r - q
```

Where:
- `r` = risk-free rate
- `q` = dividend yield (or foreign rate for FX)

This can be overridden using the `dividend` parameter.

## Notes and Limitations

1. **Negative Prices**: Unlike BSM, Bachelier allows negative prices, which is useful for rates but unrealistic for stocks.

2. **Volatility Interpretation**: The volatility parameter is in **absolute price units**, not percentage. A volatility of 20 means ±20 price units, not ±20%.

3. **Convergence**: For deep OTM/ITM options or high volatility, Bachelier and BSM can diverge significantly.

4. **Best Use Cases**: 
   - Interest rate derivatives
   - FX options near zero
   - Short-dated near-ATM options
   - Academic comparisons

## Frontend Integration

To use the Bachelier model in your frontend:

```javascript
const response = await axios.post('http://localhost:8000/calculate', {
  model: 'bachelier',
  spot: 100,
  strike: 100,
  time: 1,
  rate: 0.05,
  volatility: 0.2,
  dividend: 0,
  type: 'call'
});

console.log(`Bachelier Price: ${response.data.price}`);
console.log(`BSM Comparison: ${response.data.note}`);
```

The API automatically provides a comparison to BSM in the `note` field for educational purposes.

# Sprenkle (1964) Model - Implementation Complete

## ✅ FULLY IMPLEMENTED

The Sprenkle (1964) option pricing model has been successfully integrated into the QuantLib application.

## 📖 Historical Significance

**Case D. M. Sprenkle** (1964) published "Warrant Prices as Indicators of Expectations and Preferences" in Yale Economic Essays, representing a crucial stepping stone toward the Black-Scholes-Merton model.

### Timeline:
- **1900**: Bachelier - Normal distribution, arithmetic returns
- **1964**: **Sprenkle** - Lognormal distribution, expected return μ
- **1973**: Black-Scholes-Merton - Lognormal + risk-neutral valuation

## 🔬 Mathematical Formulation

### Sprenkle's Formula:
```
Call:  C = S·e^(μT)·N(d1) - K·N(d2)
Put:   P = K·N(-d2) - S·e^(μT)·N(-d1)

where:
d1 = [ln(S/K) + (μ + σ²/2)T] / (σ√T)
d2 = d1 - σ√T
```

### Key Differences from BSM:

| Feature | Sprenkle (1964) | BSM (1973) |
|---------|-----------------|------------|
| Distribution | **Lognormal** ✅ | Lognormal ✅ |
| Drift Term | μ (expected return) | r (risk-free rate) |
| Strike Discount | **None!** | e^(-rT) |
| Spot Growth | e^(μT) | e^(rT) or e^((r-q)T) |
| Risk-Neutral | ❌ No | ✅ Yes |

### Why Sprenkle Prices Differ:

**Sprenkle:**  
`C = S·e^(μT)·N(d1) - K·N(d2)`  
- Grows spot by expected return
- NO discounting on strike!

**BSM:**  
`C = S·N(d1) - K·e^(-rT)·N(d2)`  
- Uses current spot
- DISCOUNTS strike to present value

##Test Result:
```
Inputs: S=100, K=100, T=1, μ=10%, σ=30%

Sprenkle: $18.49  (No strike discounting!)
BSM:      $16.73  (With strike discounting)

Difference: $1.76 (10.5% higher)
```

## 🎯 Implementation Details

### Backend (`/backend/main.py`)

**Methods Added:**
```python
_sprenkle_price(S, K, T, mu, sigma)
_sprenkle_greeks(S, K, T, mu, sigma)
```

**Key Features:**
- Uses μ (expected return) instead of r
- Lognormal distribution like BSM
- No strike discounting
- Analytical Greeks

**Greeks Formulas:**
```python
Delta_call = e^(μT) · N(d1)
Gamma = [e^(μT) · n(d1)] / [S · σ · √T]
Vega = S · e^(μT) · n(d1) · √T / 100
Theta_call = -[S·e^(μT)·n(d1)·σ / (2√T)] + μ·S·e^(μT)·N(d1)
Rho = T · S · e^(μT) · N(d1)  // Sensitivity to μ, not r!
```

### Frontend (`/frontend/src/config/models.js`)

**Configuration:**
```javascript
sprenkle: {
  id: 'sprenkle',
  name: 'Sprenkle (1964)',
  category: 'PRE',
  inputs: [
    Spot Price (S): 50-150, default 100
    Strike Price (K): 50-150, default 100
    Time (Years): 0.01-2, default 1
    Expected Return (μ): 0-30%, default 10%  // Not risk-free rate!
    Volatility (σ): 1%-100%, default 30%
    Info: "Uses μ instead of r. No strike discounting!"
  ]
}
```

## 🧪 Testing & Verification

### Test 1: ATM Call
```json
{
  "model": "sprenkle",
  "spot": 100,
  "strike": 100,
  "time": 1,
  "rate": 0.10,      // Interpreted as μ
  "volatility": 0.30,
  "type": "call"
}
```

**Results:**
```
Price: $18.4941
Delta: 0.7577
Comparison: Sprenkle (μ=10.0%): 18.4941 | BSM (r=10.0%): 16.7341
```

### Test 2: Higher Expected Return
```bash
# μ = 20% (more optimistic)
curl ... -d '{"model": "sprenkle", "rate": 0.20, ...}'

Expected: Even higher price than μ=10%
```

## 💡 Why Sprenkle Prices Are Higher

For typical positive expected returns (μ > 0):

1. **No Strike Discounting**: Strike K appears without e^(-rT), making it "heavier"
2. **Spot Growth**: S grows by e^(μT) which is often > 1
3. **Optimistic Valuation**: Reflects actual expected returns, not risk-neutral

**Example:**
- μ = 10%, T = 1 year
- e^(0.10×1) = 1.105 (10.5% growth)
- Strike not discounted: K stays 100 (not 100 × e^(-0.10) = 90.48)

## 🎓 Educational Value

### What Sprenkle Teaches:

1. **Lognormal Works**: Showed lognormal distribution fits stock prices
2. **Expected Return Matters**: Different from risk-free rate
3. **Missing Piece**: Needed risk-neutral valuation (BSM's breakthrough)
4. **Historical Context**: Shows evolution of option pricing theory

### Why BSM Improved On It:

❌ Sprenkle: Uses actual expected return μ (subjective!)  
✅ BSM: Uses risk-free rate r (objective!)

❌ Sprenkle: No consistent arbitrage argument  
✅ BSM: Rigorous no-arbitrage derivation  

❌ Sprenkle: Depends on investor preferences  
✅ BSM: Preference-free pricing  

## 📊 Use Cases

**Educational:**
- ✅ Understanding pre-BSM models
- ✅ Learning why risk-neutral pricing matters
- ✅ Seeing evolution of finance theory

**Practical:**
- ⚠️ Limited - BSM is superior
- 📚 Academic/historical analysis only
- 🎓 Teaching finance history

## 🔧 Integration Status

✅ **Backend Pricing**: Fully implemented  
✅ **Backend Greeks**: All analytical Greeks
✅ **Frontend Config**: Custom input configuration  
✅ **API Endpoint**: Working and tested  
✅ **Graph Generation**: Integrated  
✅ **Heatmap**: Supported  
✅ **Comparison**: Auto-compares with BSM  

⏳ **Math Walkthrough**: To be created (optional)  
⏳ **Textbook Data**: To be added (optional)  

## 📝 API Usage

### Request:
```bash
curl -X POST http://localhost:8000/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "sprenkle",
    "spot": 100,
    "strike": 100,
    "time": 1,
    "rate": 0.10,    
    "volatility": 0.30,
    "dividend": 0,
    "type": "call"
  }'
```

### Response:
```json
{
  "price": 18.4941,
  "greeks": {
    "delta": 0.7577,
    "gamma": 0.0130,
    "vega": 0.3950,
    "theta": -0.0146,
    "rho": 0.7577  // Sensitivity to μ!
  },
  "note": "Sprenkle (μ=10.0%): 18.4941 | BSM (r=10.0%): 16.7341"
}
```

## 🎯 Key Insights

1. **Lognormal Distribution**: Same as BSM ✅
2. **Expected Return**: Uses μ, not r ⚠️
3. **No Discounting**: Strike not discounted ⚠️
4. **Higher Prices**: Typically > BSM for μ > r ⚠️
5. **Historical**: Important theoretical step 📚

## 🔍 Comparison Table

| Model | Year | Distribution | Drift | Strike Discount | Status |
|-------|------|--------------|-------|-----------------|--------|
| **Bachelier** | 1900 | Normal | None | e^(-rT) | ✅ Implemented |
| **Mod. Bachelier** | ~1990s | Normal (shifted) | r-q | e^(-rT) | ✅ Implemented |
| **Sprenkle** | 1964 | **Lognormal** | **μ** | **None!** | ✅ Implemented |
| **Boness** | 1964 | Lognormal | μ | e^(-rT) | ⏳ Next |
| **Samuelson** | 1965 | Lognormal | μ | e^(-rT) | ⏳ Next |
| **BSM** | 1973 | Lognormal | r | e^(-rT) | ✅ Implemented |

## 🚀 Status

**PRODUCTION READY** ✅

Sprenkle (1964) is now fully integrated and ready to use. While not practically useful for actual trading (BSM is superior), it's valuable for:

- 📚 **Education**: Understanding option pricing history
- 🎓 **Teaching**: Showing why risk-neutral valuation matters
- 📖 **Research**: Academic and historical analysis

## 📚 References

- Sprenkle, C. M. (1964). "Warrant Prices as Indicators of Expectations and Preferences." Yale Economic Essays, Vol. 4, pp. 179-231.
- Haugen, R. A. (2001). "Modern Investment Theory" (discusses pre-BSM models)
- Black, F., & Scholes, M. (1973). "The Pricing of Options and Corporate Liabilities." (cites Sprenkle)

## ⚡ Quick Test

```bash
# Test Sprenkle
curl -s -X POST http://localhost:8000/calculate \
  -H "Content-Type: application/json" \
  -d '{"model": "sprenkle", "spot": 100, "strike": 100, \
       "time": 1, "rate": 0.10, "volatility": 0.30, "type": "call"}' \
  | python3 -c 'import sys, json; r=json.load(sys.stdin); \
    print(f"Price: ${r[\"price\"]:.2f}"); print(r["note"])'

# Expected Output:
# Price: $18.49
# Sprenkle (μ=10.0%): 18.4941 | BSM (r=10.0%): 16.7341
```

---

**Sprenkle (1964) - A Bridge from Bachelier to Black-Scholes!** 🌉

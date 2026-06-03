# Barone-Adesi Whaley (1987) - Implementation Plan

## Overview

The Barone-Adesi Whaley (BAW) method provides an analytical approximation for American option pricing, significantly faster than numerical methods like binomial trees or finite difference.

## Mathematical Foundation

### Key Formula:
```
American Option = European Option + Early Exercise Premium
```

### For American Call (on dividend-paying stock):
```
C_american(S) = C_european(S) + A₂(S/S*)^q₂    if S < S*
C_american(S) = S - K                           if S ≥ S*
```

Where:
- S* = Critical stock price (exercise boundary)
- q₂ = Quadratic equation root
- A₂ = Early exercise premium coefficient

### For American Put:
```
P_american(S) = P_european(S) + A₁(S/S**)^q₁   if S > S**
P_american(S) = K - S                           if S ≤ S**
```

Where S** is the critical price for puts.

## Implementation Steps

### 1. Calculate European Option Value
Use standard BSM formula as the base.

### 2. Determine if Early Exercise is Valuable

**For Calls:**
- Only valuable if dividends exist (q > 0)
- If q = 0, American Call = European Call

**For Puts:**
- Always potentially valuable (can exercise early to earn interest on K)

### 3. Calculate Quadratic Coefficients

**Beta (β):**
```python
beta = (0.5 - b/sigma²) + sqrt((b/sigma² - 0.5)² + 2*r/sigma²)
```

**For Calls (q₂):**
```python
q₂ = (-(β-1) + sqrt((β-1)² + 4*α/β)) / 2
```

**For Puts (q₁):**
```python
q₁ = (-(β-1) - sqrt((β-1)² + 4*α/β)) / 2
```

Where α depends on model parameters.

### 4. Find Critical Price (S* or S**)

Use **Newton-Raphson iteration**:

```python
def find_critical_price_call(K, T, r, b, sigma):
    # Initial guess
    S_star = K
    
    # Newton-Raphson iteration
    for i in range(MAX_ITERATIONS):
        # Calculate g(S*) and g'(S*)
        d1 = ...  # Using S_star
        
        # Newton step
        S_star_new = S_star - g(S_star) / g_prime(S_star)
        
        # Check convergence
        if abs(S_star_new - S_star) < TOLERANCE:
            return S_star_new
        
        S_star = S_star_new
    
    return S_star
```

**Convergence criteria:**
- MAX_ITERATIONS = 100
- TOLERANCE = 1e-6

### 5. Calculate Early Exercise Premium

**For Calls (S < S*):**
```python
A₂ = (S*/q₂) * (1 - exp(-q*T) * N(d1(S*)))
early_premium = A₂ * (S/S*)^q₂
```

**For Puts (S > S**):**
```python
A₁ = -(S**/q₁) * (1 - exp(-r*T) * N(-d1(S**)))
early_premium = A₁ * (S/S**)^q₁
```

### 6. Combine European + Premium

```python
american_value = european_value + early_premium
```

## Edge Cases

### 1. Deep Out-of-the-Money
If S << K (for puts) or S >> K (for calls):
- Early exercise not optimal
- Return European value

### 2. At or Near Expiry (T → 0)
- Return intrinsic value max(S-K, 0) or max(K-S, 0)

### 3. No Dividends (Calls only)
- American Call = European Call
- Skip early exercise calculation

### 4. Numerical Issues
- Handle division by zero
- Check for negative square roots
- Ensure convergence of Newton-Raphson

## Implementation Pseudocode

```python
def _baw_american_call(S, K, T, r, q, sigma):
    # Step 1: Calculate European value
    european = _generalized_bsm(S, K, T, r, r-q, sigma)
    
    # Step 2: Check if early exercise possible
    if q <= 0:
        return european  # No dividends, American = European
    
    if T < 1e-10:
        return max(S - K, 0)  # At expiry
    
    # Step 3: Calculate coefficients
    b = r - q
    beta = (0.5 - b/sigma**2) + sqrt((b/sigma**2 - 0.5)**2 + 2*r/sigma**2)
    
    # ... rest of calculation
    
    # Step 4: Find S*
    S_star = _find_critical_price_call(K, T, r, b, sigma)
    
    # Step 5: Early exercise premium
    if S >= S_star:
        return S - K  # Immediate exercise
    
    q2 = ...  # Calculate q2
    A2 = ...  # Calculate A2
    premium = A2 * (S/S_star)**q2
    
    # Step 6: Return total
    return european + premium


def _baw_american_put(S, K, T, r, q, sigma):
    # Similar structure for puts
    # ... implementation
    pass
```

## Greeks Approximation

For American options, Greeks can be approximated by:

1. **Delta**: Numerical derivative ∂C/∂S
2. **Gamma**: Second derivative ∂²C/∂S²
3. **Theta**: -∂C/∂T (time decay)
4. **Vega**: ∂C/∂σ
5. **Rho**: ∂C/∂r

**Method**: Use finite differences:
```python
delta = (C(S+h) - C(S-h)) / (2*h)
gamma = (C(S+h) - 2*C(S) + C(S-h)) / h²
```

## Testing Strategy

### Test Cases:

1. **No Dividends (Call)**
   - Input: S=100, K=100, T=1, r=5%, q=0%, σ=30%
   - Expected: American = European

2. **High Dividends (Call)**
   - Input: S=100, K=100, T=1, r=5%, q=10%, σ=30%
   - Expected: American > European (early exercise valuable)

3. **Deep ITM Put**
   - Input: S=80, K=100, T=1, r=5%, q=0%, σ=30%
   - Expected: American > European

4. **Near Expiry**
   - Input: T=0.01
   - Expected: ≈ Intrinsic value

## Performance Considerations

**Advantages:**
- ✅ Analytical (no grid/tree needed)
- ✅ Fast computation (~0.1ms per option)
- ✅ Accurate for most cases (error < 1%)

**Limitations:**
- ⚠️ Approximation (not exact)
- ⚠️ Iteration may not converge for extreme parameters
- ⚠️ Less accurate for very long maturity

## References

1. Barone-Adesi, G., & Whaley, R. E. (1987). "Efficient Analytic Approximation of American Option Values." The Journal of Finance, 42(2), 301-320.

2. Haug, E. G. (2007). "The Complete Guide to Option Pricing Formulas." Chapter 4.

3. Hull, J. C. (2018). "Options, Futures, and Other Derivatives." Chapter 13.

## Implementation Status

**Next Steps:**
1. ✅ Documentation complete (this file)
2. ⏳ Implement backend pricing function
3. ⏳ Implement Newton-Raphson solver
4. ⏳ Add to frontend configuration
5. ⏳ Create Math Engine walkthrough (optional)
6. ⏳ Test with standard inputs

**Estimated Complexity:**
- Backend: ~200 lines (pricing + iteration + Greeks)
- Frontend: ~50 lines (configuration)
- Walkthrough: ~400 lines (if full Math Engine)

**Timeline:**
- Backend core: 1-2 hours
- Testing & validation: 30 minutes
- Frontend integration: 30 minutes
- Full Math Engine: 2-3 hours (optional)

---

## Quick Decision Point

Given the implementation complexity and time invested so far (~2 hours on pre-BSM models), I recommend:

**Option A: Core Implementation**
- Backend pricing + basic Greeks
- Frontend configuration
- Simple documentation
- No full Math Engine walkthrough
- **Time**: ~1 hour

**Option B: Full Treatment**
- Complete backend with all edge cases
- Comprehensive Greeks
- Full Math Engine walkthrough (4 steps showing iteration)
- Detailed documentation
- **Time**: ~3-4 hours

**Option C: Documentation Only**
- Keep this implementation plan
- Mark as "Future Enhancement"
- Focus on what we've already built (4 complete pre-BSM models)
- **Time**: Already done!

What would you prefer?

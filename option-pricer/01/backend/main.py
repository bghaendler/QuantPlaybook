from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
from scipy.stats import norm

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class OptionParams(BaseModel):
    spot: float
    strike: float
    time: float
    rate: float
    volatility: float
    dividend: float
    type: str



# Add this import at the top if not present
# from scipy.stats import norm

@app.post("/calculate")
def calculate_option(params: OptionParams):
    S = params.spot
    K = params.strike
    T = params.time
    r = params.rate
    sigma = params.volatility
    q = params.dividend
    
    if T <= 0 or sigma <= 0:
        return {"error": "Time and Volatility must be > 0"}

    # -- Helper functions for re-use inside loop --
    def get_d1_d2(s_val):
        d1 = (np.log(s_val / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        return d1, d2

    # --- 1. Main Point Calculation (Current State) ---
    d1, d2 = get_d1_d2(S)
    N = norm.cdf
    n = norm.pdf
    eqT = np.exp(-q * T)
    erT = np.exp(-r * T)

    if params.type == 'call':
        price = S * eqT * N(d1) - K * erT * N(d2)
        delta = eqT * N(d1)
        theta = (- (S * sigma * eqT * n(d1)) / (2 * np.sqrt(T)) 
                 - r * K * erT * N(d2) 
                 + q * S * eqT * N(d1)) / 365.0
        rho = K * T * erT * N(d2) / 100.0
        prob_exercise = N(d2)
    else:
        price = K * erT * N(-d2) - S * eqT * N(-d1)
        delta = -eqT * N(-d1)
        theta = (- (S * sigma * eqT * n(d1)) / (2 * np.sqrt(T)) 
                 + r * K * erT * N(-d2) 
                 - q * S * eqT * N(-d1)) / 365.0
        rho = -K * T * erT * N(-d2) / 100.0
        prob_exercise = N(-d2)

    gamma = (eqT * n(d1)) / (S * sigma * np.sqrt(T))
    vega = (S * eqT * n(d1) * np.sqrt(T)) / 100.0 

    # --- 2. Graph Data (Price & Greeks vs Spot) ---
    graph_data = []
    # Generate range ±50% of spot
    spot_range = np.linspace(max(0.5 * S, 1), 1.5 * S, 40)

    for s_sim in spot_range:
        d1_s, d2_s = get_d1_d2(s_sim)
        
        # Common Greek terms
        gamma_sim = (eqT * n(d1_s)) / (s_sim * sigma * np.sqrt(T))
        vega_sim = (s_sim * eqT * n(d1_s) * np.sqrt(T)) / 100.0

        if params.type == 'call':
            price_sim = s_sim * eqT * N(d1_s) - K * erT * N(d2_s)
            delta_sim = eqT * N(d1_s)
            theta_sim = (- (s_sim * sigma * eqT * n(d1_s)) / (2 * np.sqrt(T)) 
                         - r * K * erT * N(d2_s) 
                         + q * s_sim * eqT * N(d1_s)) / 365.0
            payoff = max(0, s_sim - K)
        else:
            price_sim = K * erT * N(-d2_s) - s_sim * eqT * N(-d1_s)
            delta_sim = -eqT * N(-d1_s)
            theta_sim = (- (s_sim * sigma * eqT * n(d1_s)) / (2 * np.sqrt(T)) 
                         + r * K * erT * N(-d2_s) 
                         - q * s_sim * eqT * N(-d1_s)) / 365.0
            payoff = max(0, K - s_sim)
            
        graph_data.append({
            "spot": round(s_sim, 2),
            "price": round(price_sim, 2),
            "payoff": round(payoff, 2),
            "delta": round(delta_sim, 4),
            "gamma": round(gamma_sim, 4),
            "theta": round(theta_sim, 4),
            "vega": round(vega_sim, 4)
        })

    # --- 3. Heatmap Data ---
    heatmap_data = []
    vol_steps = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
    spot_steps = np.linspace(S * 0.8, S * 1.2, 8)
    for v_sim in vol_steps:
        row = []
        for s_sim in spot_steps:
            d1_h = (np.log(s_sim / K) + (r - q + 0.5 * v_sim ** 2) * T) / (v_sim * np.sqrt(T))
            d2_h = d1_h - v_sim * np.sqrt(T)
            if params.type == 'call':
                p_h = s_sim * np.exp(-q * T) * N(d1_h) - K * np.exp(-r * T) * N(d2_h)
            else:
                p_h = K * np.exp(-r * T) * N(-d2_h) - s_sim * np.exp(-q * T) * N(-d1_h)
            row.append(round(p_h, 2))
        heatmap_data.append({"vol": round(v_sim*100), "prices": row})

    # --- 4. Distribution Data ---
    distribution_data = []
    x_range = np.linspace(-4, 4, 100)
    cutoff = d2 if params.type == 'call' else -d2
    for x in x_range:
        y = norm.pdf(x)
        is_shaded = x <= cutoff
        distribution_data.append({
            "x": round(x, 2),
            "y": round(y, 4),
            "fill": round(y, 4) if is_shaded else 0
        })

    return {
        "price": round(price, 4),
        "d1": round(d1, 4),
        "d2": round(d2, 4),
        "Nd1": round(N(d1), 4) if params.type == 'call' else round(N(-d1), 4),
        "Nd2": round(N(d2), 4) if params.type == 'call' else round(N(-d2), 4),
        "prob_exercise": round(prob_exercise * 100, 2),
        "greeks": {
            "delta": round(delta, 4),
            "gamma": round(gamma, 4),
            "theta": round(theta, 4),
            "vega": round(vega, 4),
            "rho": round(rho, 4)
        },
        "graph_data": graph_data,
        "heatmap_data": heatmap_data,
        "heatmap_spots": [round(x, 2) for x in spot_steps],
        "distribution_data": distribution_data
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
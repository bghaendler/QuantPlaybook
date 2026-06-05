import datetime
import math
import numpy as np
import pandas as pd
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from scipy.stats import norm, multivariate_normal
from scipy.optimize import brentq
from fastapi import Body, HTTPException
from typing import Dict, Any
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from option_engine import OptionEngine










app = FastAPI()
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pricer_dir = os.path.join(base_dir, "option-pricer", "frontend", "dist")
if os.path.exists(pricer_dir):
    app.mount("/pricer", StaticFiles(directory=pricer_dir), name="pricer")
else:
    print(f"Warning: Option pricer directory {pricer_dir} not found. Skipping mount.")
templates = Jinja2Templates(directory=os.path.dirname(__file__))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def dt(d1, d2):
    return (d2 - d1).days / 360.0

@app.get("/api/data")
def get_data():
    # --- 1. Curve Construction (Bootstrap & Pseudoinverse) ---
    spot = datetime.date(2012, 10, 3)
    dates = [
        datetime.date(2012, 10, 4), datetime.date(2012, 11, 5), datetime.date(2013, 1, 3), datetime.date(2013, 3, 20),
        datetime.date(2013, 4, 3), datetime.date(2013, 6, 19), datetime.date(2013, 9, 18), datetime.date(2013, 10, 3),
        datetime.date(2013, 12, 18), datetime.date(2014, 3, 19), datetime.date(2014, 10, 3), datetime.date(2015, 10, 5),
        datetime.date(2016, 10, 3), datetime.date(2017, 10, 3), datetime.date(2018, 10, 3), datetime.date(2019, 10, 3),
        datetime.date(2020, 10, 3), datetime.date(2021, 10, 3), datetime.date(2022, 10, 3), datetime.date(2023, 10, 3),
        datetime.date(2024, 10, 3), datetime.date(2025, 10, 3), datetime.date(2026, 10, 3), datetime.date(2027, 10, 4),
        datetime.date(2028, 10, 4), datetime.date(2029, 10, 4), datetime.date(2030, 10, 4), datetime.date(2031, 10, 4),
        datetime.date(2032, 10, 4), datetime.date(2033, 10, 4), datetime.date(2034, 10, 4), datetime.date(2035, 10, 4),
        datetime.date(2036, 10, 4), datetime.date(2037, 10, 4), datetime.date(2038, 10, 4), datetime.date(2039, 10, 4),
        datetime.date(2040, 10, 4), datetime.date(2041, 10, 4), datetime.date(2042, 10, 3)
    ]
    date_idx = {d: i for i, d in enumerate(dates)}
    M = np.zeros((17, 39))
    b = np.zeros(17)
    row = 0
    L_data = [(datetime.date(2012, 10, 4), 0.095), (datetime.date(2012, 11, 5), 0.116),
              (datetime.date(2013, 1, 3), 0.223), (datetime.date(2013, 4, 3), 0.438)]
    for d, r in L_data:
        if r > 0:
            M[row, date_idx[d]] = 1.0 + (r / 100.0) * dt(spot, d)
            b[row] = 1.0
            row += 1
    f_dates = [(dates[3], dates[5], 99.786), (dates[5], dates[6], 99.752), 
               (dates[6], dates[8], 99.723), (dates[8], dates[9], 99.669)]
    for d_s, d_e, q in f_dates:
        r = (100.0 - q) / 100.0
        M[row, date_idx[d_s]] = 1.0
        M[row, date_idx[d_e]] = -(1.0 + r * dt(d_s, d_e))
        row += 1
    s_quotes = {2:0.475, 3:0.586, 4:0.752, 5:0.942, 7:1.324, 10:1.739, 15:2.165, 20:2.280, 30:2.332}
    swap_dates = [d for d in dates if d.month == 10 and d.year >= 2013]
    for idx, (year, r) in enumerate(s_quotes.items()):
        r /= 100.0
        end_date = swap_dates[year - 1]
        prev_d = spot
        for d in swap_dates:
            if d <= end_date:
                M[row, date_idx[d]] += r * dt(prev_d, d)
                prev_d = d
        M[row, date_idx[end_date]] += 1.0
        b[row] = 1.0
        row += 1

    C_matrix = np.tril(np.ones((39, 39)))
    dts = np.array([dt(spot if i==0 else dates[i-1], dates[i]) for i in range(39)])
    W = np.diag(np.sqrt(dts))
    MCW = M @ C_matrix @ W
    y_pseudo = np.linalg.pinv(MCW) @ (b - M @ np.ones(39))
    P_pseudo = np.ones(39) + C_matrix @ W @ y_pseudo
    d29, d30 = datetime.date(2041, 10, 4), datetime.date(2042, 10, 3)
    p29, p30 = P_pseudo[date_idx[d29]], P_pseudo[date_idx[d30]]
    fwd_pseudo = (p29 / p30 - 1) / dt(d29, d30)

    P_boot = {spot: 1.0}
    for d, r in L_data:
        P_boot[d] = 1.0 / (1.0 + (r/100.0) * dt(spot, d))
    t1 = dt(spot, datetime.date(2013, 1, 3))
    t2 = dt(spot, datetime.date(2013, 4, 3))
    tm = dt(spot, datetime.date(2013, 3, 20))
    logP1 = math.log(P_boot[datetime.date(2013, 1, 3)])
    logP2 = math.log(P_boot[datetime.date(2013, 4, 3)])
    P_boot[datetime.date(2013, 3, 20)] = math.exp(logP1 + (logP2 - logP1) * (tm - t1) / (t2 - t1))
    for d1, d2, q in f_dates:
        r = (100.0 - q) / 100.0
        P_boot[d2] = P_boot[d1] / (1.0 + r * dt(d1, d2))
    t1 = dt(spot, datetime.date(2013, 9, 18))
    t2 = dt(spot, datetime.date(2013, 12, 18))
    tm = dt(spot, datetime.date(2013, 10, 3))
    logP1 = math.log(P_boot[datetime.date(2013, 9, 18)])
    logP2 = math.log(P_boot[datetime.date(2013, 12, 18)])
    P_boot[datetime.date(2013, 10, 3)] = math.exp(logP1 + (logP2 - logP1) * (tm - t1) / (t2 - t1))
    swap_rates = {}
    for y_val in range(2, 31):
        if y_val in s_quotes:
            swap_rates[y_val] = s_quotes[y_val]
        else:
            y1_val = max([k for k in s_quotes.keys() if k < y_val])
            y2_val = min([k for k in s_quotes.keys() if k > y_val])
            swap_rates[y_val] = s_quotes[y1_val] + (s_quotes[y2_val] - s_quotes[y1_val]) * (y_val - y1_val) / (y2_val - y1_val)
    for y_val in range(2, 31):
        d_mat = swap_dates[y_val-1]
        S = swap_rates[y_val] / 100.0
        sum_PV = 0
        prev_d = spot
        for i in range(y_val-1):
            d_i = swap_dates[i]
            sum_PV += dt(prev_d, d_i) * P_boot[d_i]
            prev_d = d_i
        dt_n = dt(prev_d, d_mat)
        P_boot[d_mat] = (1.0 - S * sum_PV) / (1.0 + S * dt_n)
    fwd_boot = (P_boot[d29] / P_boot[d30] - 1) / dt(d29, d30)

    # --- 2. PCA Part ---
    try:
        csv_path = os.path.join(base_dir, 'SwissGovYields.csv')
        data = pd.read_csv(csv_path, index_col=0)
        data.index = pd.to_datetime(data.index, format='%Y %m', errors='ignore')
        try:
            data.index = pd.to_datetime(data.index)
        except:
            pass
        data = data / 100.0
        changes = data.diff().dropna()
        cov_mat = np.cov(changes, rowvar=False)
        lambdas, A = np.linalg.eig(cov_mat)
        idx = lambdas.argsort()[::-1]
        lambdas = lambdas[idx]
        A = A[:, idx]
        var_explained = np.sum(lambdas[:2]) / np.sum(lambdas)
        if '2010-07' in data.index:
            yields_jul2010 = data.loc['2010-07']
        else:
            yields_jul2010 = data.iloc[-1]
        if isinstance(yields_jul2010, pd.DataFrame):
            yields_jul2010 = yields_jul2010.iloc[0]
        y_i = yields_jul2010.iloc[0:4].values
        T_i = np.array([2, 3, 4, 5])
        CF_i = np.array([80, 70, 150, 40])
        dV_dy = -CF_i * T_i * np.exp(-y_i * T_i)
        mean_changes = changes.mean(axis=0).values
        X_centered = changes.values - mean_changes
        Y_scores = np.dot(X_centered, A)
        Y_reduced = Y_scores[:, :2]
        A_reduced = A[:, :2]
        X_reconstructed = np.dot(Y_reduced, A_reduced.T)
        dy_approx = X_reconstructed + mean_changes
        dy_approx_sub = dy_approx[:, 0:4]
        dV_approx_series = np.dot(dy_approx_sub, dV_dy)
        std_dV = np.std(dV_approx_series, ddof=1)
        pca_success = True
    except Exception as e:
        pca_success = False
        var_explained = 0
        std_dV = 0
        lambdas = []

    # --- 3. Splines / Lorimier Method ---
    T_lorimier = np.array([2, 3, 4, 5, 7, 10, 20, 30])
    y_lorimier = np.array([-0.79, -0.73, -0.65, -0.55, -0.33, -0.04, 0.54, 0.73])
    alpha_lor = 0.1
    N_lor = len(T_lorimier)

    def get_H(ti, tj):
        t_min = min(ti, tj)
        t_max = max(ti, tj)
        return ti * tj + 0.5 * (t_min**2) * t_max - (1/6) * (t_min**3)

    M_lor = np.zeros((N_lor + 1, N_lor + 1))
    b_lor = np.zeros(N_lor + 1)
    M_lor[0, 1:] = T_lorimier
    for i in range(N_lor):
        M_lor[i+1, 0] = T_lorimier[i]
        for j in range(N_lor):
            delta = 1.0 if i == j else 0.0
            M_lor[i+1, j+1] = get_H(T_lorimier[i], T_lorimier[j]) + (delta / alpha_lor)
        b_lor[i+1] = y_lorimier[i] * T_lorimier[i]

    betas = np.linalg.solve(M_lor, b_lor)
    beta_0 = betas[0]
    beta_vec = betas[1:]

    T_target = 6
    sum_beta_H = 0
    for i in range(N_lor):
        sum_beta_H += beta_vec[i] * get_H(T_target, T_lorimier[i])
    yield_6 = beta_0 + (1 / T_target) * sum_beta_H

    # Evaluate the spline curve from 1 to 30 years for visualization
    T_smooth = np.linspace(1, 30, 60)
    y_smooth = []
    for t_val in T_smooth:
        s_val = 0
        for i in range(N_lor):
            s_val += beta_vec[i] * get_H(t_val, T_lorimier[i])
        y_smooth.append(beta_0 + (1/t_val)*s_val)

    # Compile Results
    return {
        "dates": [d.strftime("%Y-%m-%d") for d in dates],
        "p_pseudo": P_pseudo.tolist(),
        "p_boot": [P_boot[d] for d in dates],
        "fwd_pseudo": round(fwd_pseudo * 100, 2),
        "fwd_boot": round(fwd_boot * 100, 2),
        "pca_success": pca_success,
        "var_explained": round(var_explained * 100, 2) if pca_success else 0,
        "std_dV": round(std_dV, 2) if pca_success else 0,
        "pca_lambdas": lambdas.tolist() if pca_success else [],
        "lorimier": {
            "yield_6": round(yield_6, 4),
            "input_T": T_lorimier.tolist(),
            "input_y": y_lorimier.tolist(),
            "smooth_T": T_smooth.tolist(),
            "smooth_y": y_smooth
        }
    }

@app.post("/calculate")
def calculate(payload: Dict[str, Any] = Body(...)):
    try:
        engine = OptionEngine(payload)
        base_result = engine.calculate()
        graph_data = engine.get_graph_data()
        heatmap_info = engine.get_heatmap_data()
        dist_data = engine.get_distribution_data()
        vol_surfaces = engine.get_true_vol_surfaces()
        gatheral = engine.get_gatheral_surfaces()

        return {
            **base_result,
            "graph_data": graph_data,
            "heatmap_data": heatmap_info['heatmap_data'],
            "heatmap_spots": heatmap_info['heatmap_spots'],
            "spot_time_data": heatmap_info.get('spot_time_data'),
            "spot_time_steps": heatmap_info.get('spot_time_steps'),
            "vol_time_data": heatmap_info.get('vol_time_data'),
            "vol_time_steps": heatmap_info.get('vol_time_steps'),
            "vol_surface_strike": vol_surfaces['vol_surface_strike'],
            "vol_surface_delta": vol_surfaces['vol_surface_delta'],
            "gatheral_total_var": gatheral['total_variance'],
            "gatheral_dual": gatheral['dual_surface'],
            "gatheral_svi": gatheral['svi_fit'],
            "gatheral_pdf": gatheral['pdf_arbitrage'],
            "gatheral_dynamics": gatheral['dynamics'],
            "distribution_data": dist_data
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# Trigger reload for Options Applications subpage update
@app.get("/")
def read_root(request: Request):
    import inspect
    sig = inspect.signature(templates.TemplateResponse)
    if "request" in sig.parameters:
        return templates.TemplateResponse(request, "index.html", {"request": request})
    else:
        return templates.TemplateResponse("index.html", {"request": request})


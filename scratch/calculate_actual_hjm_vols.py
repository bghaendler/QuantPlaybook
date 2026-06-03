import numpy as np
from scipy.stats import norm
from scipy.optimize import minimize_scalar
import datetime

spot = datetime.date(2012, 10, 3)

def dt(d1, d2):
    return (d2 - d1).days / 360.0

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

# Now let's calculate the cap price of 18.39% and see what vols correspond to it!
# Wait! Let's first build a grid of 59 semi-annual periods.
# Let's see: spot is 2012-10-03.
# The payment dates are every 6 months for 30 years -> 60 periods.
# T_i = spot + i * 6 months.
# Let's define the dates:
p_dates = []
curr = spot
for i in range(60):
    m_new = curr.month + 6
    y_new = curr.year
    if m_new > 12:
        m_new -= 12
        y_new += 1
    # Adjust for month end if necessary
    day_new = min(curr.day, 28 if m_new == 2 else 30)
    curr = datetime.date(y_new, m_new, day_new)
    p_dates.append(curr)

# Let's interpolate the discount curve P_pseudo to get discount factors for p_dates!
# For any date d_target, we find its relative time in years and linearly interpolate log(P)
t_pseudo = np.array([dt(spot, d) for d in dates])
logP_pseudo = np.log(P_pseudo)

# We also prepended spot (t=0, logP=0)
t_grid = np.concatenate(([0.0], t_pseudo))
logP_grid = np.concatenate(([0.0], logP_pseudo))

def get_P(d_target):
    t_target = dt(spot, d_target)
    logP = np.interp(t_target, t_grid, logP_grid)
    return np.exp(logP)

p_factors = [get_P(d) for d in p_dates]

# Let's price the HJM cap under this curve and check the price!
v1, v2 = 0.01, 0.02
beta1, beta2 = 0.3, 0.5

# ATM strike
P_30 = p_factors[59]
p_dates_extended = [spot] + p_dates
deltas_p = np.array([dt(p_dates_extended[i-1], p_dates_extended[i]) for i in range(1, len(p_dates_extended))])
annuity_30 = np.sum(deltas_p * p_factors)
strike = (1.0 - P_30) / annuity_30
print(f"ATM strike K: {strike*100:.6f}%")

target_price = 18.39 / 100

# Let's find implied Black vol that yields 18.39%
def black_cap_price(sig_B):
    price = 0.0
    for i in range(1, 60):
        T_d = dt(spot, p_dates[i-1])
        T_p = dt(spot, p_dates[i])
        delta = deltas_p[i]
        P_d = p_factors[i-1]
        P_p = p_factors[i]
        F = (P_d / P_p - 1.0) / delta
        
        if sig_B <= 0:
            cpl = max(0.0, delta * P_p * (F - strike))
        else:
            d1 = (np.log(F / strike) + 0.5 * sig_B**2 * T_d) / (sig_B * np.sqrt(T_d))
            d2 = d1 - sig_B * np.sqrt(T_d)
            cpl = delta * P_p * (F * norm.cdf(d1) - strike * norm.cdf(d2))
        price += cpl
    return price

res_black = minimize_scalar(lambda s: (black_cap_price(s) - target_price)**2, bounds=(0.01, 2.0), method='bounded')
print(f"Implied Black Vol for 18.39%: {res_black.x * 100:.6f}%")

# Let's find implied Normal vol that yields 18.39%
def bachelier_cap_price(sig_N):
    price = 0.0
    for i in range(1, 60):
        T_d = dt(spot, p_dates[i-1])
        T_p = dt(spot, p_dates[i])
        delta = deltas_p[i]
        P_d = p_factors[i-1]
        P_p = p_factors[i]
        F = (P_d / P_p - 1.0) / delta
        
        if sig_N <= 0:
            cpl = max(0.0, delta * P_p * (F - strike))
        else:
            d1 = (F - strike) / (sig_N * np.sqrt(T_d))
            cpl = delta * P_p * ((F - strike) * norm.cdf(d1) + sig_N * np.sqrt(T_d) * norm.pdf(d1))
        price += cpl
    return price

res_normal = minimize_scalar(lambda s: (bachelier_cap_price(s) - target_price)**2, bounds=(0.0001, 0.1), method='bounded')
print(f"Implied Normal Vol for 18.39%: {res_normal.x * 10000:.6f} bps")

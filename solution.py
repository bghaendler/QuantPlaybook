import datetime
import numpy as np

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

# 1. LIBOR
for d, r in zip(dates[:5], [0.095, 0.116, 0.223, 0.0, 0.438]):
    if r > 0:
        M[row, date_idx[d]] = 1.0 + (r / 100.0) * dt(spot, d)
        b[row] = 1.0
        row += 1

# 2. Futures
f_dates = [(dates[3], dates[5], 99.786), (dates[5], dates[6], 99.752), 
           (dates[6], dates[8], 99.723), (dates[8], dates[9], 99.669)]
for d_s, d_e, q in f_dates:
    r = (100.0 - q) / 100.0
    M[row, date_idx[d_s]] = 1.0
    M[row, date_idx[d_e]] = -(1.0 + r * dt(d_s, d_e))
    row += 1 # b is 0.0

# 3. Swaps
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

# ==========================================
# b) Pseudoinverse Method
# ==========================================
# Minimize the weighted L2 norm of the first derivative of the curve
C_matrix = np.tril(np.ones((39, 39)))
dts = np.array([dt(spot if i==0 else dates[i-1], dates[i]) for i in range(39)])
W = np.diag(np.sqrt(dts))

MCW = M @ C_matrix @ W
y = np.linalg.pinv(MCW) @ (b - M @ np.ones(39))
P_pseudo = np.ones(39) + C_matrix @ W @ y

d29, d30 = datetime.date(2041, 10, 4), datetime.date(2042, 10, 3)
p29, p30 = P_pseudo[date_idx[d29]], P_pseudo[date_idx[d30]]
fwd_pseudo = (p29 / p30 - 1) / dt(d29, d30)

print(f"b) Pseudoinverse Method Forward Rate: {fwd_pseudo * 100:.2f}% (Expected: 2.53%)")

# ==========================================
# a) Bootstrap Method (Interpolating par swap rates)
# ==========================================
P = {spot: 1.0}
# LIBOR
L_data = [(datetime.date(2012, 10, 4), 0.095), (datetime.date(2012, 11, 5), 0.116),
          (datetime.date(2013, 1, 3), 0.223), (datetime.date(2013, 4, 3), 0.438)]
for d, r in L_data:
    P[d] = 1.0 / (1.0 + (r/100.0) * dt(spot, d))

# Interpolate 2013-3-20 linearly by discount factor or log-discount (we use log-discount)
import math
t1 = dt(spot, datetime.date(2013, 1, 3))
t2 = dt(spot, datetime.date(2013, 4, 3))
tm = dt(spot, datetime.date(2013, 3, 20))
logP1 = math.log(P[datetime.date(2013, 1, 3)])
logP2 = math.log(P[datetime.date(2013, 4, 3)])
P[datetime.date(2013, 3, 20)] = math.exp(logP1 + (logP2 - logP1) * (tm - t1) / (t2 - t1))

# Futures
for d1, d2, q in f_dates:
    r = (100.0 - q) / 100.0
    P[d2] = P[d1] / (1.0 + r * dt(d1, d2))

# Interpolate 1Y Swap node (2013-10-3)
t1 = dt(spot, datetime.date(2013, 9, 18))
t2 = dt(spot, datetime.date(2013, 12, 18))
tm = dt(spot, datetime.date(2013, 10, 3))
logP1 = math.log(P[datetime.date(2013, 9, 18)])
logP2 = math.log(P[datetime.date(2013, 12, 18)])
P[datetime.date(2013, 10, 3)] = math.exp(logP1 + (logP2 - logP1) * (tm - t1) / (t2 - t1))

# Swaps (interpolate missing par swap rates)
swap_rates = {}
for y in range(2, 31):
    if y in s_quotes:
        swap_rates[y] = s_quotes[y]
    else:
        y1 = max([y_ for y_ in s_quotes.keys() if y_ < y])
        y2 = min([y_ for y_ in s_quotes.keys() if y_ > y])
        swap_rates[y] = s_quotes[y1] + (s_quotes[y2] - s_quotes[y1]) * (y - y1) / (y2 - y1)

# Bootstrap remaining dates
for y in range(2, 31):
    d_mat = swap_dates[y-1]
    S = swap_rates[y] / 100.0
    sum_PV = 0
    prev_d = spot
    for i in range(y-1):
        d_i = swap_dates[i]
        sum_PV += dt(prev_d, d_i) * P[d_i]
        prev_d = d_i
    dt_n = dt(prev_d, d_mat)
    P[d_mat] = (1.0 - S * sum_PV) / (1.0 + S * dt_n)

fwd_boot = (P[d29] / P[d30] - 1) / dt(d29, d30)
print(f"a) Bootstrap Method Forward Rate: {fwd_boot * 100:.2f}% (Expected: 2.55%)")

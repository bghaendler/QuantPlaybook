import numpy as np
from datetime import datetime

today = datetime(1996, 9, 4)

cf_dates_str = [
    "9/26/1996", "10/13/1996", "11/6/1996", "11/15/1996", "12/7/1996",
    "1/19/1997", "2/27/1997", "3/3/1997", "3/8/1997", "3/26/1997",
    "4/13/1997", "5/6/1997", "6/7/1997", "7/19/1997", "8/27/1997",
    "9/3/1997", "9/8/1997", "9/26/1997", "10/13/1997", "11/6/1997",
    "12/7/1997", "1/19/1998", "2/27/1998", "3/3/1998", "3/8/1998",
    "3/26/1998", "4/13/1998", "5/6/1998", "6/7/1998", "8/27/1998",
    "9/3/1998", "9/8/1998", "9/26/1998", "10/13/1998", "11/6/1998",
    "12/7/1998", "2/27/1999", "3/3/1999", "3/8/1999", "3/26/1999",
    "4/13/1999", "5/6/1999", "6/7/1999", "8/27/1999", "9/3/1999",
    "9/8/1999", "10/13/1999", "11/6/1999", "12/7/1999", "2/27/2000",
    "3/3/2000", "3/8/2000", "4/13/2000", "5/6/2000", "6/7/2000",
    "8/27/2000", "9/8/2000", "10/13/2000", "11/6/2000", "12/7/2000",
    "2/27/2001", "3/8/2001", "4/13/2001", "5/6/2001", "6/7/2001",
    "8/27/2001", "9/8/2001", "10/13/2001", "11/6/2001", "12/7/2001",
    "2/27/2002", "3/8/2002", "4/13/2002", "6/7/2002", "8/27/2002",
    "9/8/2002", "10/13/2002", "12/7/2002", "3/8/2003", "4/13/2003",
    "6/7/2003", "9/8/2003", "10/13/2003", "12/7/2003", "3/8/2004",
    "4/13/2004", "6/7/2004", "9/8/2004", "10/13/2004", "12/7/2004",
    "3/8/2005", "4/13/2005", "6/7/2005", "9/8/2005", "10/13/2005",
    "12/7/2005", "3/8/2006", "4/13/2006", "9/8/2006", "10/13/2006",
    "4/13/2007", "10/13/2007", "4/13/2008", "10/13/2008"
]

dates = [datetime.strptime(x, "%m/%d/%Y") for x in cf_dates_str]
N = len(dates)

bonds = {
    'Bond 1': {'coupon': 10.0, 'next_coupon': "11/15/1996", 'maturity': "11/15/1996", 'price': 103.82},
    'Bond 2': {'coupon': 9.75, 'next_coupon': "1/19/1997", 'maturity': "1/19/1998", 'price': 106.04},
    'Bond 3': {'coupon': 12.25, 'next_coupon': "9/26/1996", 'maturity': "3/26/1999", 'price': 118.44},
    'Bond 4': {'coupon': 9.0, 'next_coupon': "3/3/1997", 'maturity': "3/3/2000", 'price': 106.28},
    'Bond 5': {'coupon': 7.0, 'next_coupon': "11/6/1996", 'maturity': "11/6/2001", 'price': 101.15},
    'Bond 6': {'coupon': 9.75, 'next_coupon': "2/27/1997", 'maturity': "8/27/2002", 'price': 111.06},
    'Bond 7': {'coupon': 8.5, 'next_coupon': "12/7/1996", 'maturity': "12/7/2005", 'price': 106.24},
    'Bond 8': {'coupon': 7.75, 'next_coupon': "3/8/1997", 'maturity': "9/8/2006", 'price': 98.49},
    'Bond 9': {'coupon': 9.0, 'next_coupon': "10/13/1996", 'maturity': "10/13/2008", 'price': 110.87}
}

portfolio_dates_str = ["8/27/2002", "12/7/2005", "9/8/2006", "10/13/2008"]
portfolio_cash_flows = [80, 100, 60, 250]
portfolio_dates = [datetime.strptime(x, "%m/%d/%Y") for x in portfolio_dates_str]

def days_30_360(d1, d2):
    y1, m1, day1 = d1.year, d1.month, d1.day
    y2, m2, day2 = d2.year, d2.month, d2.day
    if day1 == 31: day1 = 30
    if day2 == 31 and day1 >= 30: day2 = 30
    return 360 * (y2 - y1) + 30 * (m2 - m1) + (day2 - day1)

C = np.zeros((9, N))
p = np.zeros(9)
bond_names = sorted(list(bonds.keys()))

for idx, name in enumerate(bond_names):
    b = bonds[name]
    coupon = b['coupon']
    next_c = datetime.strptime(b['next_coupon'], "%m/%d/%Y")
    mat_c = datetime.strptime(b['maturity'], "%m/%d/%Y")
    p[idx] = b['price']
    
    c_dates = []
    curr = mat_c
    while curr >= next_c:
        c_dates.append(curr)
        m_new = curr.month - 6
        y_new = curr.year
        if m_new <= 0:
            m_new += 12
            y_new -= 1
        curr = datetime(y_new, m_new, min(curr.day, 28 if m_new == 2 else 30))
        
    c_dates = sorted(c_dates)
    
    for c_date in c_dates:
        col_idx = dates.index(c_date)
        amt = coupon / 2.0
        if c_date == mat_c:
            amt += 100.0
        C[idx, col_idx] = amt

today_extended = [today] + dates
deltas = np.array([days_30_360(today_extended[i-1], today_extended[i])/360.0 for i in range(1, len(today_extended))])

W = np.diag(1.0 / np.sqrt(deltas))
M = np.diag([1] * N)
for i in range(N-1):
    M[i+1, i] = -1

Mm1 = np.linalg.inv(M)
Wm1 = np.linalg.inv(W)

A = C @ Mm1 @ Wm1
# A_m is A.T @ inv(A @ A.T)
A_m = A.T @ np.linalg.inv(A @ A.T)

# The portfolio value is V = cf^T * d
# d = Mm1 @ (Wm1 @ delta_star + vec)
#   = Mm1 @ Wm1 @ A_m @ (p - C @ ones) + Mm1 @ vec
# Thus: V = cf^T @ d = cf^T @ Mm1 @ Wm1 @ A_m @ p + constant
# The derivative of V with respect to the price vector p is:
# dV_dp = cf^T @ Mm1 @ Wm1 @ A_m
# Wait, let's identify the indices of portfolio dates:
cf_vector = np.zeros(N)
for p_date, cf in zip(portfolio_dates, portfolio_cash_flows):
    col_idx = dates.index(p_date)
    cf_vector[col_idx] = cf

dV_dp = cf_vector @ Mm1 @ Wm1 @ A_m
print("Partial derivatives dV / dp_i:")
for i, name in enumerate(bond_names):
    print(f"  {name}: {dV_dp[i]:.6f}")

# The hedge ratio is h_1 = - dV / dp_1
h1 = - dV_dp[bond_names.index('Bond 1')]
print(f"Hedge units (h_1) for Bond 1: {h1:.6f}")

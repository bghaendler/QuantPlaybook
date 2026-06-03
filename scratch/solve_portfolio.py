import datetime
import numpy as np

# Spot date
spot = datetime.date(1996, 9, 4)

def parse_date(date_str):
    parts = date_str.split('/')
    m = int(parts[0])
    d = int(parts[1])
    y = int(parts[2])
    if y < 50:
        year = 2000 + y
    else:
        year = 1900 + y
    return datetime.date(year, m, d)

# Cash flow dates
cf_dates_str = [
    "9/26/96", "10/13/96", "11/6/96", "11/15/96", "12/7/96", "1/19/97", "2/27/97", "3/3/97", "3/8/97", "3/26/97",
    "4/13/97", "5/6/97", "6/7/97", "7/19/97", "8/27/97", "9/3/97", "9/8/97", "9/26/97", "10/13/97", "11/6/97",
    "12/7/97", "1/19/98", "2/27/98", "3/3/98", "3/8/98", "3/26/98", "4/13/98", "5/6/98", "6/7/98", "8/27/98",
    "9/3/98", "9/8/98", "9/26/98", "10/13/98", "11/6/98", "12/7/98", "2/27/99", "3/3/99", "3/8/99", "3/26/99",
    "4/13/99", "5/6/99", "6/7/99", "8/27/99", "9/3/99", "9/8/99", "10/13/99", "11/6/99", "12/7/99", "2/27/00",
    "3/3/00", "3/8/00", "4/13/00", "5/6/00", "6/7/00", "8/27/00", "9/8/00", "10/13/00", "11/6/00", "12/7/00",
    "2/27/01", "3/8/01", "4/13/01", "5/6/01", "6/7/01", "8/27/01", "9/8/01", "10/13/01", "11/6/01", "12/7/01",
    "2/27/02", "3/8/02", "4/13/02", "6/7/02", "8/27/02", "9/8/02", "10/13/02", "12/7/02", "3/8/03", "4/13/03",
    "6/7/03", "9/8/03", "10/13/03", "12/7/03", "3/8/04", "4/13/04", "6/7/04", "9/8/04", "10/13/04", "12/7/04",
    "3/8/05", "4/13/05", "6/7/05", "9/8/05", "10/13/05", "12/7/05", "3/8/06", "4/13/06", "9/8/06", "10/13/06",
    "4/13/07", "10/13/07", "4/13/08", "10/13/08"
]

cf_dates = [parse_date(d) for d in cf_dates_str]
cf_dates.sort()
N = len(cf_dates)
date_to_idx = {d: i for i, d in enumerate(cf_dates)}

# Bond specifications
bonds = [
    {"coupon": 10.00, "next": "11/15/96", "mat": "11/15/96", "price": 103.82, "semi": False},
    {"coupon": 9.75,  "next": "1/19/97",  "mat": "1/19/98",  "price": 106.04, "semi": False},
    {"coupon": 12.25, "next": "9/26/96",  "mat": "3/26/99",  "price": 118.44, "semi": True},
    {"coupon": 9.00,  "next": "3/3/97",   "mat": "3/3/00",   "price": 106.28, "semi": False},
    {"coupon": 7.00,  "next": "11/6/96",  "mat": "11/6/01",  "price": 101.15, "semi": False},
    {"coupon": 9.75,  "next": "2/27/97",  "mat": "8/27/02",  "price": 111.06, "semi": True},
    {"coupon": 8.50,  "next": "12/7/96",  "mat": "12/7/05",  "price": 106.24, "semi": False},
    {"coupon": 7.75,  "next": "3/8/97",   "mat": "9/8/06",   "price": 98.49,  "semi": True},
    {"coupon": 9.00,  "next": "10/13/96", "mat": "10/13/08", "price": 110.87, "semi": True}
]

def days_30_360(d1, d2):
    y1, m1, day1 = d1.year, d1.month, d1.day
    y2, m2, day2 = d2.year, d2.month, d2.day
    
    # 30/360 US rules
    if day1 == 31:
        day1 = 30
    if day2 == 31 and day1 >= 30:
        day2 = 30
        
    return 360 * (y2 - y1) + 30 * (m2 - m1) + (day2 - day1)

def run_pseudoinverse(daycount_method):
    C = np.zeros((9, N))
    p = np.zeros(9)
    
    for b_idx, bond in enumerate(bonds):
        coupon_rate = bond["coupon"] / 100.0
        p[b_idx] = bond["price"]
        
        next_cp = parse_date(bond["next"])
        mat_date = parse_date(bond["mat"])
        
        # Generate all cash flow dates for this bond
        b_dates = []
        curr_date = next_cp
        
        if bond["semi"]:
            coupon_payment = coupon_rate / 2.0 * 100.0
            while curr_date <= mat_date:
                b_dates.append(curr_date)
                m = curr_date.month + 6
                y = curr_date.year
                if m > 12:
                    m -= 12
                    y += 1
                try:
                    curr_date = datetime.date(y, m, curr_date.day)
                except ValueError:
                    curr_date = datetime.date(y, m, curr_date.day - 1)
        else:
            coupon_payment = coupon_rate * 100.0
            while curr_date <= mat_date:
                b_dates.append(curr_date)
                curr_date = datetime.date(curr_date.year + 1, curr_date.month, curr_date.day)
                
        for d in b_dates:
            closest_d = min(cf_dates, key=lambda x: abs((x - d).days))
            idx = date_to_idx[closest_d]
            if closest_d == mat_date:
                C[b_idx, idx] = coupon_payment + 100.0
            else:
                C[b_idx, idx] = coupon_payment

    if daycount_method == '30/360':
        T = np.array([days_30_360(spot, d) / 360.0 for d in cf_dates])
    else:
        T = np.array([(d - spot).days / 365.0 for d in cf_dates])
        
    delta_T = np.zeros(N)
    delta_T[0] = T[0]
    for i in range(1, N):
        delta_T[i] = T[i] - T[i-1]
        
    W = np.diag(np.sqrt(delta_T))
    W_inv = np.diag(1.0 / np.sqrt(delta_T))
    
    M = np.zeros((N, N))
    for i in range(N):
        M[i, i] = 1.0
        if i > 0:
            M[i, i-1] = -1.0
            
    M_inv = np.linalg.inv(M)
    M_inv_W_inv = M_inv @ W_inv
    A_matrix = C @ M_inv_W_inv
    
    e1 = np.zeros(N)
    e1[0] = 1.0
    
    p_minus_Ce1 = p - C @ M_inv @ e1
    AA_T_inv = np.linalg.inv(A_matrix @ A_matrix.T)
    Delta_star = A_matrix.T @ AA_T_inv @ p_minus_Ce1
    
    d_vec = M_inv @ (W_inv @ Delta_star + e1)
    
    # Portfolio cash flows:
    # 27/08/02 (80), 07/12/05 (100), 08/09/06 (60), 13/10/08 (250)
    p_dates = ["8/27/02", "12/7/05", "9/8/06", "10/13/08"]
    p_cfs = [80.0, 100.0, 60.0, 250.0]
    
    # Portfolio cash flow vector c_port of length N
    c_port = np.zeros(N)
    for date_str, cf in zip(p_dates, p_cfs):
        d_obj = parse_date(date_str)
        idx = date_to_idx[d_obj]
        c_port[idx] = cf
        
    # V = c_port^T @ d
    # dV/dp = (AA^T)^-1 @ A @ W_inv @ M_inv^T @ c_port
    # Let's compute this derivative vector of length 9
    dV_dp = np.linalg.inv(A_matrix @ A_matrix.T) @ A_matrix @ W_inv @ M_inv.T @ c_port
    
    V = 0.0
    print(f"\n--- Method: {daycount_method} ---")
    for date_str, cf in zip(p_dates, p_cfs):
        d_obj = parse_date(date_str)
        idx = date_to_idx[d_obj]
        df = d_vec[idx]
        print(f"Date: {date_str}, T: {T[idx]:.4f}, DF: {df:.6f}, CF: {cf}, PV: {cf * df:.4f}")
        V += cf * df
        
    print(f"Total Portfolio Value V: {V:.6f}")
    print("Derivative dV/dp for each bond:")
    for i in range(9):
        print(f"Bond {i+1}: {dV_dp[i]:.6f}")
    return V

run_pseudoinverse('365')
run_pseudoinverse('30/360')

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

# Unique sorted list of cash flow dates (N = 104)
N = len(cf_dates)
print(f"Number of cash flow dates N = {N}")

# Let's map each date to its index
date_to_idx = {d: i for i, d in enumerate(cf_dates)}

# Bond specifications
bonds = [
    # (Annual Coupon, Next Coupon, Maturity, Price, IsSemi)
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

# Construct cash flow matrix C of size 9 x N
C = np.zeros((9, N))
p = np.zeros(9)

for b_idx, bond in enumerate(bonds):
    coupon_rate = bond["coupon"] / 100.0
    price_val = bond["price"]
    p[b_idx] = price_val
    
    next_cp = parse_date(bond["next"])
    mat_date = parse_date(bond["mat"])
    
    # Generate all cash flow dates for this bond
    b_dates = []
    curr_date = next_cp
    
    if bond["semi"]:
        # Semi-annual coupon payments
        coupon_payment = coupon_rate / 2.0 * 100.0
        while curr_date <= mat_date:
            b_dates.append(curr_date)
            # increment by 6 months approximately, or we can match the unique cash flow dates list!
            # Let's increment curr_date by 6 months:
            m = curr_date.month + 6
            y = curr_date.year
            if m > 12:
                m -= 12
                y += 1
            # Handle month end issues
            try:
                curr_date = datetime.date(y, m, curr_date.day)
            except ValueError:
                curr_date = datetime.date(y, m, curr_date.day - 1)
    else:
        # Annual coupon payments
        coupon_payment = coupon_rate * 100.0
        while curr_date <= mat_date:
            b_dates.append(curr_date)
            curr_date = datetime.date(curr_date.year + 1, curr_date.month, curr_date.day)
            
    # For each cash flow date, place it in the C matrix
    for d in b_dates:
        # Find closest date in cf_dates list
        closest_d = min(cf_dates, key=lambda x: abs((x - d).days))
        idx = date_to_idx[closest_d]
        if closest_d == mat_date:
            C[b_idx, idx] = coupon_payment + 100.0
        else:
            C[b_idx, idx] = coupon_payment

print("Cash flow matrix shape:", C.shape)

# Time fractions for cf_dates from spot in years
T = np.array([(d - spot).days / 365.0 for d in cf_dates])
delta_T = np.zeros(N)
delta_T[0] = T[0]
for i in range(1, N):
    delta_T[i] = T[i] - T[i-1]

# Diagonal weight matrix W
W = np.diag(np.sqrt(delta_T))
W_inv = np.diag(1.0 / np.sqrt(delta_T))

# M matrix (lower triangular difference matrix)
M = np.zeros((N, N))
for i in range(N):
    M[i, i] = 1.0
    if i > 0:
        M[i, i-1] = -1.0

M_inv = np.linalg.inv(M)

# A = C @ M_inv @ W_inv
M_inv_W_inv = M_inv @ W_inv
A_matrix = C @ M_inv_W_inv

# e1 = (1, 0, ..., 0)^T of length N
e1 = np.zeros(N)
e1[0] = 1.0

# Delta* = A^T @ (A @ A^T)^{-1} @ (p - C @ M_inv @ e1)
p_minus_Ce1 = p - C @ M_inv @ e1
AA_T_inv = np.linalg.inv(A_matrix @ A_matrix.T)
Delta_star = A_matrix.T @ AA_T_inv @ p_minus_Ce1

# d = M_inv @ (W_inv @ Delta_star + e1)
d = M_inv @ (W_inv @ Delta_star + e1)

print("Discount factors P(0, T_j) for first few:")
for i in range(10):
    print(f"T = {T[i]:.4f} ({cf_dates_str[i]}): {d[i]:.6f}")

# Verification of pricing
p_model = C @ d
print("Model prices vs Market prices:")
for i in range(9):
    print(f"Bond {i+1}: Model={p_model[i]:.4f}, Market={p[i]:.4f}")

# Let's check Question 4: "What is the discount factor for the cash flow date of Bond 1?"
# Bond 1 cash flow date is 11/15/96
idx_bond1 = date_to_idx[parse_date("11/15/96")]
print(f"Q4: Discount factor for 11/15/96 is {d[idx_bond1]:.6f}")

# Derivative of portfolio value V with respect to price of Bond 1
C_port = C.sum(axis=0)
dV_dp = C_port @ M_inv_W_inv @ A_matrix.T @ AA_T_inv
print("Derivative dV/dp for each bond:")
for i in range(9):
    print(f"Bond {i+1}: {dV_dp[i]:.6f}")

import numpy as np
from scipy.stats import norm

# Q3
log3 = np.log(3)
val = log3 - 1.5
prob3 = norm.cdf(-val)
print("Q3:", round(prob3 * 100, 2))

# Q4: W1(t), W2(t) independent. Prob(W1(1)>1 and W2(1)>1)?
# P(W1>1) * P(W2>1) = (1 - norm.cdf(1))^2
p4 = (1 - norm.cdf(1))**2
print("Q4:", round(p4 * 100, 2))

# Q5: P(1 < W(1) < W(3) - 1)
# W(3) - W(1) > 1 and W(1) > 1
# They are independent. P(W(3)-W(1) > 1) = P(N(0,2) > 1) = P(Z > 1/sqrt(2))
p5_1 = 1 - norm.cdf(1)
p5_2 = 1 - norm.cdf(1 / np.sqrt(2))
p5 = p5_1 * p5_2
print("Q5:", round(p5 * 100, 2))

# Q6: Conditional on W(1)>0, prob W(2)<0?
# P(W(2)<0 | W(1)>0) = P(W(2)<0 and W(1)>0) / P(W(1)>0)
# P(W(1)>0) = 0.5
# W(2) = W(1) + (W(2)-W(1)). Let X = W(1), Y = W(2)-W(1). Both are N(0,1) iid.
# P(X+Y < 0 and X > 0) = P(Y < -X, X > 0).
# Since X, Y are independent standard normal, this is the region in the 4th quadrant below the line y = -x.
# The angle is 45 degrees out of 360, so probability is 1/8.
# P = (1/8) / (1/2) = 1/4 = 0.25 = 25.00%
print("Q6:", 25.00)

with open("/Users/borjagarcia/Coursera/scratch/extracted_qs.txt", "r") as f:
    text = f.read()

keywords = ["Bond 1", "portfolio", "C_port", "A^T", "AA^T"]

print("Searching extracted_qs.txt for portfolio details...")
import re
matches = list(re.finditer(r'(Bond 1|portfolio|C_port|AA\^T|A\^T)', text))
print(f"Found {len(matches)} matches.")

for idx, m in enumerate(matches):
    start = max(0, m.start() - 100)
    end = min(len(text), m.end() + 800)
    segment = text[start:end]
    if any(k in segment for k in ["C_port", "p_1", "maturity", "coupon", "9/4/96"]):
        print("="*80)
        print(f"Match {idx} at position {m.start()}:")
        print(segment)
        print("="*80)
        break

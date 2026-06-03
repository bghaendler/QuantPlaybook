import os

scratch_dir = "/Users/borjagarcia/Coursera/scratch"
print("Searching scratch files for content...")

for fname in sorted(os.listdir(scratch_dir)):
    if not fname.endswith(".py") and not fname.endswith(".txt"):
        continue
    fpath = os.path.join(scratch_dir, fname)
    try:
        with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        
        # Check if the content has "Coupon Bonds" or "floating rate note" or similar
        # but let's exclude swaptions or calibration unless they also have coupon bonds
        if "coupon bond" in content.lower() and "maturity" in content.lower() and ("swap" in content.lower() or "reset" in content.lower()):
            print(f"File: {fname} contains 'coupon bond', 'maturity', and ('swap' or 'reset')")
            # print first 500 chars
            print(content[:500])
            print("="*40)
    except Exception as e:
        print(f"Error reading {fname}: {e}")

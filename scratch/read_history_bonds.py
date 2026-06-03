with open("/Users/borjagarcia/Coursera/scratch/history_bonds.txt", "r") as f:
    lines = f.readlines()

print(f"Total lines in history_bonds.txt: {len(lines)}")
for i, l in enumerate(lines):
    if any(q in l for q in ["Question 4", "Question 5", "Question 6", "Q4", "Q5", "Q6"]):
        print(f"Line {i}: {l.strip()}")
        # print some context lines around it
        start = max(0, i - 2)
        end = min(len(lines), i + 8)
        print("--- CONTEXT ---")
        for j in range(start, end):
            print(f"  {j}: {lines[j].strip()}")
        print("-" * 40)

import re

file_path = "/Users/borjagarcia/Coursera/scratch/extracted_qs.txt"

with open(file_path, "r") as f:
    text = f.read()

# Let's search for "Question 4" and "Question 5" or similar headings in the text.
# We'll print matches that look like a final quiz definition.
print("--- Searching for Question 4 & 5 in extracted_qs.txt ---")
matches = re.finditer(r'(Question 4|Question 5|UK government bonds|portfolio cash flows|perfectly hedge|Bond 1)', text, re.IGNORECASE)
printed_segments = []
for m in matches:
    start = max(0, m.start() - 150)
    end = min(len(text), m.end() + 1000)
    segment = text[start:end]
    # Check if this segment contains coupon rates, portfolio cash flows, or values to make sure it's the actual quiz question
    if any(kw in segment for kw in ["p_1", "p_9", "maturity", "coupon", "d = M", "How many units"]):
        # Avoid printing duplicate regions
        if not any(abs(start - ps) < 500 for ps in printed_segments):
            print("="*60)
            print(segment)
            printed_segments.append(start)

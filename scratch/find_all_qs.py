import json
import re

transcript_path = "/Users/borjagarcia/.gemini/antigravity/brain/d9dbeba6-8a73-4599-b8c9-d0ebb942bc4b/.system_generated/logs/transcript.jsonl"

print("Searching transcript for quiz details...")
with open(transcript_path, "r") as f:
    for line in f:
        try:
            step = json.loads(line)
            content = step.get('content', '')
            if not content:
                continue
            
            # Check for mention of Q4, Q5, or UK government bonds in MODEL responses
            if step.get('source') == 'MODEL' and any(kw in content for kw in ["Question 4", "Question 5", "Bond 1", "perpetual bond"]):
                print("="*80)
                print(f"STEP {step.get('step_index')}:")
                # Find occurrences and print some surrounding lines
                for match in re.finditer(r'(Question \d|Bond 1|perpetual|CIR|Vasicek|UK government|Q1|Q2|Q3|Q4|Q5|Q6|Q7|Q8|Q9|Q10|Q11|Q12)', content):
                    start = max(0, match.start() - 200)
                    end = min(len(content), match.end() + 600)
                    print(f"--- MATCH AT {match.start()}: ---")
                    print(content[start:end])
                    print("-"*40)
        except Exception as e:
            pass

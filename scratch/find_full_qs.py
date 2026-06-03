import json
import re

transcript_path = "/Users/borjagarcia/.gemini/antigravity/brain/d9dbeba6-8a73-4599-b8c9-d0ebb942bc4b/.system_generated/logs/transcript.jsonl"

print("Searching transcript for the text of Questions 1 to 12...")
keywords = ["Suppose at t = 0 two", "perpetual bond", "duration of the perpetual bond", "UK government bond", "perfectly hedge", "CIR model for the short rate", "Z = \log", "forward rates:", "implied Black volatility", "implied normal volatility", "ATM cap with maturity in 30 years"]

with open(transcript_path, "r") as f:
    for line_num, line in enumerate(f, 1):
        try:
            step = json.loads(line)
            content = step.get('content', '')
            idx = step.get('step_index')
            if not content:
                continue
            
            # check if any keyword is in content
            found = [kw for kw in keywords if kw.lower() in content.lower()]
            if found:
                print("="*80)
                print(f"Line {line_num}, Step {idx} (Source={step.get('source')}, Type={step.get('type')}) matches: {found}")
                # Print around the first match
                first_match = found[0]
                pos = content.lower().find(first_match.lower())
                start = max(0, pos - 100)
                end = min(len(content), pos + 1000)
                print(content[start:end])
                print("-"*80)
        except Exception as e:
            pass

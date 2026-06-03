import json

transcript_path = "/Users/borjagarcia/.gemini/antigravity/brain/d9dbeba6-8a73-4599-b8c9-d0ebb942bc4b/.system_generated/logs/transcript.jsonl"

with open(transcript_path, "r") as f:
    for line in f:
        try:
            step = json.loads(line)
            content = step.get('content', '')
            idx = step.get('step_index')
            if not content:
                continue
            
            # Look for step indices before 2085 that contain UK government or perpetual or swaption
            if idx < 2085:
                if any(kw in content for kw in ["Question 4", "Question 5", "UK government", "Bond 1"]):
                    print("="*80)
                    print(f"STEP {idx} (Source={step.get('source')}):")
                    # If the content is too long, we will search for where the keywords are and print that region
                    for kw in ["Question 4", "Question 5", "Bond 1", "perfectly hedge"]:
                        pos = content.find(kw)
                        if pos != -1:
                            start = max(0, pos - 100)
                            end = min(len(content), pos + 1200)
                            print(f"--- MATCH FOR '{kw}' at {pos} ---")
                            print(content[start:end])
                            print("-"*40)
        except Exception as e:
            pass

import json

transcript_path = "/Users/borjagarcia/.gemini/antigravity/brain/d9dbeba6-8a73-4599-b8c9-d0ebb942bc4b/.system_generated/logs/transcript.jsonl"

print("Searching transcript for 83.33 or swaps quiz...")
with open(transcript_path, "r") as f:
    for line in f:
        try:
            step = json.loads(line)
            content = step.get('content', '')
            if not content:
                continue
            
            # Check for any step containing "83.33%" or "Coupon Bonds" and "Quiz"
            if "83.33%" in content or ("coupon bonds" in content.lower() and "swap" in content.lower() and "quiz" in content.lower()):
                # Exclude step 3031 and step 2606 which are very long transcripts we already know
                if step.get('step_index') not in [3031, 2606]:
                    print("="*80)
                    print(f"STEP {step.get('step_index')} (Source={step.get('source')}):")
                    # print some surrounding text around "83.33%" or "coupon bonds"
                    pos = content.find("83.33%")
                    if pos == -1:
                        pos = content.lower().find("coupon bonds")
                    start = max(0, pos - 100)
                    end = min(len(content), pos + 1000)
                    print(content[start:end])
                    print("-"*40)
        except Exception as e:
            pass

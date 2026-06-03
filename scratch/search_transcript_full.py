import json
import re

transcript_path = "/Users/borjagarcia/.gemini/antigravity/brain/d9dbeba6-8a73-4599-b8c9-d0ebb942bc4b/.system_generated/logs/transcript.jsonl"

print("Searching full transcript for Coupon Bonds and IR Swaps quiz details...")
with open(transcript_path, "r") as f:
    for line_num, line in enumerate(f, 1):
        try:
            step = json.loads(line)
            content = step.get('content', '')
            if not content:
                continue
            
            # Check for mention of Coupon Bonds or Swaps quiz
            if "quiz" in content.lower() and "coupon" in content.lower():
                # Let's see if we can find questions or options
                print("="*80)
                print(f"Line {line_num}, Step {step.get('step_index')} (Source={step.get('source')}, Type={step.get('type')}):")
                print(content[:800])
                print("-" * 50)
        except Exception as e:
            pass

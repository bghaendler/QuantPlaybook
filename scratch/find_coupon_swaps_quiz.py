import json
import re

transcript_path = "/Users/borjagarcia/.gemini/antigravity/brain/d9dbeba6-8a73-4599-b8c9-d0ebb942bc4b/.system_generated/logs/transcript.jsonl"

print("Searching transcript for Coupon Bonds & Swap quiz questions...")
found_steps = []
with open(transcript_path, "r") as f:
    for line in f:
        try:
            step = json.loads(line)
            content = step.get('content', '')
            if not content:
                continue
            
            # Look for step indices where we see the Coupon Bonds quiz questions
            # Let's search for "Coupon Bonds and Interest Rate Swaps" and "Practice Assignment"
            if "coupon bonds" in content.lower() and "practice" in content.lower() and "assignment" in content.lower():
                found_steps.append((step.get('step_index'), step.get('source'), content[:200]))
        except Exception as e:
            pass

print(f"Found matches in {len(found_steps)} steps:")
for idx, src, excerpt in found_steps[:20]:
    print(f"Step {idx} ({src}): {excerpt}...")

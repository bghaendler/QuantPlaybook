import json

transcript_path = "/Users/borjagarcia/.gemini/antigravity/brain/d9dbeba6-8a73-4599-b8c9-d0ebb942bc4b/.system_generated/logs/transcript.jsonl"

print("Searching transcript for swaps-related quiz text...")
with open(transcript_path, "r") as f:
    for line in f:
        try:
            step = json.loads(line)
            content = step.get('content', '')
            if not content:
                continue
            
            # Check for words associated with the coupon swaps quiz
            # For example, "coupon bond" or "swap rate" in user requests or model outputs
            if "coupon bond" in content.lower() and ("quiz" in content.lower() or "question" in content.lower()):
                # Exclude video transcripts which are long by checking if it contains too many INAUDIBLEs
                if content.count("INAUDIBLE") < 2:
                    print("="*80)
                    print(f"STEP {step.get('step_index')} (Source={step.get('source')}):")
                    print(content[:1500])
                    print("-"*40)
        except Exception as e:
            pass

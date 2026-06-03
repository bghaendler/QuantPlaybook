import json

transcript_path = "/Users/borjagarcia/.gemini/antigravity/brain/d9dbeba6-8a73-4599-b8c9-d0ebb942bc4b/.system_generated/logs/transcript.jsonl"

print("Searching transcript for portfolio cash flows...")
with open(transcript_path, "r") as f:
    for line_num, line in enumerate(f, 1):
        try:
            step = json.loads(line)
            content = step.get('content', '')
            if not content:
                continue
            
            if "portfolio" in content.lower() and ("cash flow" in content.lower() or "c_port" in content.lower() or "bond 1" in content.lower()):
                if "103.82" in content or "9/4/96" in content:
                    print("="*80)
                    print(f"Line {line_num}, Step {step.get('step_index')} (Source={step.get('source')}):")
                    # print matching paragraphs
                    for p in content.split("\n\n"):
                        if "portfolio" in p.lower() or "c_port" in p.lower():
                            print(p[:1500])
                            print("-" * 50)
        except:
            pass

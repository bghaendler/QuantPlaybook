import json

transcript_path = "/Users/borjagarcia/.gemini/antigravity/brain/d9dbeba6-8a73-4599-b8c9-d0ebb942bc4b/.system_generated/logs/transcript.jsonl"

print("Searching transcript for 'Question 4' in historical steps...")
with open(transcript_path, "r") as f:
    for line_num, line in enumerate(f, 1):
        try:
            step = json.loads(line)
            content = step.get('content', '')
            idx = step.get('step_index')
            if not content:
                continue
            
            # If "Question 4" is in content and step_index < 2085, let's inspect it!
            if idx < 2085 and "question 4" in content.lower():
                print("="*80)
                print(f"Line {line_num}, STEP {idx} (Source={step.get('source')}, Type={step.get('type')}):")
                print("CONTENT LENGTH:", len(content))
                # Let's print the entire content or a large chunk of it
                print(content[:3000])
                print("="*80)
        except Exception as e:
            pass

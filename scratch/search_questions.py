import json

with open("/Users/borjagarcia/.gemini/antigravity/brain/d9dbeba6-8a73-4599-b8c9-d0ebb942bc4b/.system_generated/logs/transcript.jsonl", "r") as f:
    for line in f:
        try:
            step = json.loads(line)
            content = step.get('content', '')
            if content and any(q in content for q in ["Question 4", "Question 5", "UK government", "Bond 1"]):
                print(f"Index {step.get('step_index')}:")
                print(content[:500])
        except:
            pass

import json

with open("/Users/borjagarcia/.gemini/antigravity/brain/d9dbeba6-8a73-4599-b8c9-d0ebb942bc4b/.system_generated/logs/transcript.jsonl", "r") as f:
    for line in f:
        try:
            step = json.loads(line)
            content = step.get('content', '')
            if content and ("UK" in content or "perpetual" in content or "government" in content):
                print(f"Index {step.get('step_index')}:")
                # print any lines matching these keywords
                for l in content.split('\n'):
                    if any(w in l for w in ["UK", "perpetual", "government", "Bond"]):
                        print(l[:200])
        except:
            pass

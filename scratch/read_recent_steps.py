import json

with open("/Users/borjagarcia/.gemini/antigravity/brain/d9dbeba6-8a73-4599-b8c9-d0ebb942bc4b/.system_generated/logs/transcript.jsonl", "r") as f:
    lines = f.readlines()

print(f"Total lines in transcript: {len(lines)}")
# Look at the last 15 lines of transcript.jsonl
for i in range(max(0, len(lines)-15), len(lines)):
    try:
        step = json.loads(lines[i])
        print(f"Step {step.get('step_index')}: Source={step.get('source')}, Type={step.get('type')}")
        if step.get('source') == 'USER_EXPLICIT':
            print("Content:", step.get('content'))
        elif step.get('type') == 'PLANNER_RESPONSE':
            # print first 500 chars of content
            print("Model Content:", step.get('content')[:1000])
    except Exception as e:
        print(f"Error reading line {i}: {e}")

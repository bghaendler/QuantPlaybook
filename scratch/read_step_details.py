import json

with open("/Users/borjagarcia/.gemini/antigravity/brain/d9dbeba6-8a73-4599-b8c9-d0ebb942bc4b/.system_generated/logs/transcript.jsonl", "r") as f:
    for line in f:
        try:
            step = json.loads(line)
            idx = step.get('step_index')
            if idx is not None and idx >= 2085:
                print("="*60)
                print(f"STEP {idx}: Source={step.get('source')}, Type={step.get('type')}")
                if 'content' in step and step['content']:
                    print("Content length:", len(step['content']))
                    print("Content sample:", step['content'][:1500])
                if 'tool_calls' in step and step['tool_calls']:
                    print("Tool Calls:", json.dumps(step['tool_calls'], indent=2))
        except Exception as e:
            pass

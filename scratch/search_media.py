import json
import re

with open("/Users/borjagarcia/.gemini/antigravity/brain/d9dbeba6-8a73-4599-b8c9-d0ebb942bc4b/.system_generated/logs/transcript.jsonl", "r") as f:
    for line in f:
        try:
            step = json.loads(line)
            content = step.get('content', '')
            if content and "media__" in content:
                print(f"Index {step.get('step_index')}:")
                # find all matches of media__....png
                matches = re.findall(r'media__[0-9_]+.png', content)
                print("Matches:", matches)
                # print any context around it
                lines_with_media = [l for l in content.split('\n') if "media__" in l]
                print("Lines:", lines_with_media)
        except:
            pass

import json

transcript_path = "/Users/borjagarcia/.gemini/antigravity/brain/d9dbeba6-8a73-4599-b8c9-d0ebb942bc4b/.system_generated/logs/transcript.jsonl"
output_path = "/Users/borjagarcia/Coursera/scratch/history_bonds.txt"

keywords = ["UK", "Bond 1", "portfolio", "duration", "perpetual"]

with open(transcript_path, "r") as f, open(output_path, "w") as out:
    for line in f:
        try:
            step = json.loads(line)
            content = step.get('content', '')
            if not content:
                continue
            
            # If any keyword is in content, let's see if this is an input or planner response that has details
            if any(kw.lower() in content.lower() for kw in keywords):
                # Write a snippet or the full content if it is a user input or a major model output
                out.write("="*80 + "\n")
                out.write(f"STEP {step.get('step_index')} (Source={step.get('source')}, Type={step.get('type')}):\n")
                # To avoid writing huge dumps, let's write the matching lines or sections
                for line_in_content in content.split("\n"):
                    if any(kw.lower() in line_in_content.lower() for kw in keywords):
                        out.write(line_in_content[:150] + "\n")
                out.write("\n")
        except:
            pass

print("Finished writing historical search to scratch/history_bonds.txt")

import json

transcript_path = "/Users/borjagarcia/.gemini/antigravity/brain/d9dbeba6-8a73-4599-b8c9-d0ebb942bc4b/.system_generated/logs/transcript.jsonl"
output_path = "/Users/borjagarcia/Coursera/scratch/extracted_qs.txt"

with open(transcript_path, "r") as f, open(output_path, "w") as out:
    for line in f:
        try:
            step = json.loads(line)
            content = step.get('content', '')
            idx = step.get('step_index')
            if not content:
                continue
            
            # Check for keyword matches in model responses or user requests
            if any(kw in content for kw in ["UK government bond", "Bond 1", "perfectly hedge", "Question 4", "Question 5"]):
                out.write("="*80 + "\n")
                out.write(f"STEP {idx} (Source={step.get('source')}, Type={step.get('type')}):\n")
                # Write matching blocks
                out.write(content)
                out.write("\n\n")
        except Exception as e:
            pass

print("Finished writing all matches to scratch/extracted_qs.txt")

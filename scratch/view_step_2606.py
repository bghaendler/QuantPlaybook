import json

transcript_path = "/Users/borjagarcia/.gemini/antigravity/brain/d9dbeba6-8a73-4599-b8c9-d0ebb942bc4b/.system_generated/logs/transcript.jsonl"

with open(transcript_path, "r") as f:
    for line in f:
        try:
            step = json.loads(line)
            if step.get('step_index') == 2606:
                content = step.get('content', '')
                print(f"STEP 2606 CONTENT LENGTH: {len(content)}")
                # Print the content from around "Coupon Bonds"
                pos = content.lower().find("coupon bonds and interest rate swaps")
                while pos != -1:
                    print("="*60)
                    print(content[pos:pos+3000])
                    pos = content.lower().find("coupon bonds and interest rate swaps", pos + 1)
        except Exception as e:
            pass

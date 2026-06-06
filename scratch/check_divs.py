import os
import re

sections_dir = "/Users/borjagarcia/Coursera/app/templates/sections"
files = sorted(os.listdir(sections_dir))

for f in files:
    if not f.endswith(".html"):
        continue
    path = os.path.join(sections_dir, f)
    with open(path, "r", encoding="utf-8") as file:
        content = file.read()
        
    # Strip comments
    content_clean = re.sub(r"<!--.*?-->", "", content, flags=re.DOTALL)
    
    div_opens = len(re.findall(r"<div\b", content_clean))
    div_closes = len(re.findall(r"</div\b", content_clean))
    
    if div_opens != div_closes:
        print(f"Mismatched DIVs in {f}: Opens={div_opens}, Closes={div_closes} (Diff={div_opens - div_closes})")

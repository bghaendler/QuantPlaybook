import os
import re

sections_dir = "/Users/borjagarcia/Coursera/app/templates/sections"
pattern = re.compile(r'\*\*(.*?)\*\*')

fixed_count = 0
file_count = 0

for filename in os.listdir(sections_dir):
    if filename.endswith(".html"):
        file_path = os.path.join(sections_dir, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        new_content, count = pattern.subn(r'<strong>\1</strong>', content)
        if count > 0:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Fixed {count} occurrences in {filename}")
            fixed_count += count
            file_count += 1

print(f"Done! Fixed {fixed_count} occurrences across {file_count} files.")

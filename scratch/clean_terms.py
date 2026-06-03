import os
import re

sections_dir = "/Users/borjagarcia/Coursera/app/templates/sections"
index_file = "/Users/borjagarcia/Coursera/app/index.html"

def clean_html(html_content):
    output = []
    i = 0
    n = len(html_content)
    while i < n:
        if html_content[i:i+7].lower() == '<script':
            end_idx = html_content.find('</script>', i)
            if end_idx == -1:
                output.append(html_content[i:])
                break
            output.append(html_content[i:end_idx+9])
            i = end_idx + 9
        elif html_content[i:i+6].lower() == '<style':
            end_idx = html_content.find('</style>', i)
            if end_idx == -1:
                output.append(html_content[i:])
                break
            output.append(html_content[i:end_idx+8])
            i = end_idx + 8
        elif html_content[i] == '<':
            end_idx = html_content.find('>', i)
            if end_idx == -1:
                output.append(html_content[i:])
                break
            output.append(html_content[i:end_idx+1])
            i = end_idx + 1
        else:
            end_idx = html_content.find('<', i)
            if end_idx == -1:
                text = html_content[i:]
                i = n
            else:
                text = html_content[i:end_idx]
                i = end_idx
            
            # Replacements in user-facing text nodes
            # 1. CQF / cqf -> QuantPlaybook
            text = re.sub(r'\bCQF\b', 'QuantPlaybook', text)
            
            # 2. Lecture / lecture -> Session
            text = re.sub(r'\bLectures\b', 'Sessions', text)
            text = re.sub(r'\blectures\b', 'sessions', text)
            text = re.sub(r'\bLecture\b', 'Session', text)
            text = re.sub(r'\blecture\b', 'session', text)
            
            # 3. Video / video -> Part
            text = re.sub(r'\bVideos\b', 'Parts', text)
            text = re.sub(r'\bvideos\b', 'parts', text)
            text = re.sub(r'\bVideo\b', 'Part', text)
            text = re.sub(r'\bvideo\b', 'part', text)
            
            output.append(text)
            
    return "".join(output)

# Process templates
files_processed = 0
for filename in os.listdir(sections_dir):
    if filename.endswith(".html"):
        file_path = os.path.join(sections_dir, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        new_content = clean_html(content)
        if new_content != content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            files_processed += 1

# Process index.html
with open(index_file, "r", encoding="utf-8") as f:
    content = f.read()

new_content = clean_html(content)
if new_content != content:
    with open(index_file, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Cleaned index.html")

print(f"Done! Cleaned {files_processed} templates and index.html.")

import re
from bs4 import BeautifulSoup

file_path = "/Users/borjagarcia/Coursera/app/index.html"

with open(file_path, "r", encoding="utf-8") as f:
    html_content = f.read()

# Using BeautifulSoup to cleanly modify HTML tags
soup = BeautifulSoup(html_content, "html.parser")

# 1. Remove all SVG icons inside the sidebar
sidebar = soup.find(class_="sidebar")
if sidebar:
    for svg in sidebar.find_all("svg"):
        # We can keep switcher SVGs (btn-course-epfl, btn-course-cqf, and theme toggle button)
        # which are inside sidebar-col-1. We only decompose SVGs inside sidebar-col-2.
        col2 = sidebar.find(class_="sidebar-col-2")
        if col2:
            for col2_svg in col2.find_all("svg"):
                col2_svg.decompose()

# 2. Clean up "Module XX:" and "Module X:" prefixes
for summary in soup.find_all("summary", class_="nav-section-title"):
    text = summary.get_text()
    # Match "Module 1:", "Module 01:", etc. with optional spaces
    match = re.match(r"^Module\s+\d+:\s*(.*)$", text, re.IGNORECASE)
    if match:
        clean_text = match.group(1).strip()
        summary.string = clean_text

# Write modified HTML back
with open(file_path, "w", encoding="utf-8") as f:
    f.write(str(soup))

print("Successfully cleaned menu icons and Module prefixes!")

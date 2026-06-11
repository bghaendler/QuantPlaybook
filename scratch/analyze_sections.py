import re

with open("app/index.html", "r") as f:
    content = f.read()

# 1. Find all href links in the sidebar
sidebar_match = re.search(r'<aside class="sidebar">.*?</aside>', content, re.DOTALL)
sidebar_content = sidebar_match.group(0) if sidebar_match else content

hrefs = set(re.findall(r'href="#([^"]+)"', sidebar_content))
onclicks = set(re.findall(r"showSection\('([^']+)'\)", sidebar_content))
select_models = set(re.findall(r"selectModel\('([^']+)'\)", sidebar_content))

print("=== Sidebar Analysis ===")
print(f"Total unique href anchors in sidebar: {len(hrefs)}")
print(f"Total unique showSection calls in sidebar: {len(onclicks)}")
print(f"Total unique selectModel calls in sidebar: {len(select_models)}")

# 2. Find all keys in _sectionMap
map_match = re.search(r'const _sectionMap = \{(.*?)\};', content, re.DOTALL)
section_map_keys = []
map_lines = []
if map_match:
    map_lines = map_match.group(1).split('\n')
    for line in map_lines:
        line_match = re.search(r"^\s*'([^']+)':", line)
        if line_match:
            section_map_keys.append(line_match.group(1))

print(f"\n=== Section Map Analysis ===")
print(f"Total keys in _sectionMap: {len(section_map_keys)}")

# 3. Find all included files
includes = re.findall(r'{%\s*include\s*"templates/sections/([^"]+)"\s*%}', content)
print(f"\n=== Include Files Analysis ===")
print("Total {% include %} sections in main content: " + str(len(includes)))

print("\n--- Disconnected Sections (In _sectionMap but NOT in sidebar) ---")
disconnected_from_sidebar = [k for k in section_map_keys if k not in onclicks and k != 'pending' and k not in hrefs]
for k in sorted(disconnected_from_sidebar):
    print(f"  - {k}")

print("\n--- Placeholder Sections (Routed to 'pending') ---")
# Count how many links have href="#pending" or call showSection('pending')
pending_links_count = len(re.findall(r'showSection\(\'pending\'\)', sidebar_content))
print(f"There are {pending_links_count} links pointing to the 'pending' placeholder section.")

print("\n--- Included Templates not in _sectionMap ---")
# Let's map section elements to includes
el_to_key = {}
for line in map_lines:
    line_match = re.search(r"^\s*'([^']+)':\s*\{\s*el:\s*'([^']+)'", line)
    if line_match:
        el_to_key[line_match.group(2)] = line_match.group(1)

unmapped_includes = []
for inc in includes:
    base = inc.replace("view-", "").replace(".html", "").replace("dashboard", "dashboard")
    el_name_1 = inc.replace(".html", "")
    el_name_2 = el_name_1.replace("view-", "")
    found = False
    for line in map_lines:
        if el_name_1 in line or el_name_2 in line:
            found = True
            break
    if not found:
        unmapped_includes.append(inc)

print(f"Total unmapped includes: {len(unmapped_includes)}")
for inc in sorted(unmapped_includes):
    print(f"  - {inc}")

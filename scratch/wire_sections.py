"""Idempotently wire newly created section templates into app/index.html.

For each entry in MANIFEST (ordered like the pending anchors in index.html):
  - if templates/sections/view-<key>.html exists:
      * rewrite the next pending sidebar anchor to point at <key>
      * ensure an {% include %} line exists
      * ensure a _sectionMap entry exists
Safe to run repeatedly as batches of templates are added.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pending_manifest import MANIFEST

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(ROOT, "app", "index.html")
SECTIONS_DIR = os.path.join(ROOT, "app", "templates", "sections")

with open(INDEX, "r", encoding="utf-8") as f:
    html = f.read()

PENDING_ANCHOR = 'href="#pending" onclick="showSection(\'pending\')"'

# --- 1. Rewire sidebar anchors -------------------------------------------
# Walk pending anchors in file order; the i-th pending anchor corresponds to
# the i-th *unwired* manifest entry. Entries already wired (key found as
# showSection('<key>')) are skipped in the pending queue.
unwired = [k for k, _ in MANIFEST if f"showSection('{k}')" not in html]
wired_now, skipped = [], []

for key in unwired:
    tpl = os.path.join(SECTIONS_DIR, f"view-{key}.html")
    idx = html.find(PENDING_ANCHOR)
    if idx == -1:
        print(f"WARN: no pending anchor left for {key}")
        break
    if not os.path.exists(tpl):
        # Template not created yet: leave this anchor as pending, but we must
        # not consume it for a later key. Stop wiring here to preserve order.
        skipped.append(key)
        break
    replacement = f'href="#{key}" onclick="showSection(\'{key}\')"'
    html = html[:idx] + replacement + html[idx + len(PENDING_ANCHOR):]
    wired_now.append(key)

# --- 2. Ensure {% include %} lines ----------------------------------------
INCLUDE_SENTINEL = '            {% include "templates/sections/view-cqf-fp-tvm-discounting.html" %}\n'
include_lines = []
for key, _ in MANIFEST:
    tpl = os.path.join(SECTIONS_DIR, f"view-{key}.html")
    inc = f'            {{% include "templates/sections/view-{key}.html" %}}\n'
    if os.path.exists(tpl) and inc not in html:
        include_lines.append(inc)
if include_lines:
    assert INCLUDE_SENTINEL in html
    html = html.replace(INCLUDE_SENTINEL, INCLUDE_SENTINEL + "".join(include_lines), 1)

# --- 3. Ensure _sectionMap entries -----------------------------------------
MAP_SENTINEL = "            'cqf-mp-probability':      { el: 'view-cqf-mp-probability', math: true }"
map_lines = []
for key, _ in MANIFEST:
    tpl = os.path.join(SECTIONS_DIR, f"view-{key}.html")
    entry = f"            '{key}': {{ el: 'view-{key}', math: true }}"
    if os.path.exists(tpl) and f"'{key}':" not in html:
        map_lines.append(entry)
if map_lines:
    assert MAP_SENTINEL in html
    html = html.replace(MAP_SENTINEL, MAP_SENTINEL + ",\n" + ",\n".join(map_lines), 1)

with open(INDEX, "w", encoding="utf-8") as f:
    f.write(html)

remaining = html.count(PENDING_ANCHOR)
print(f"wired now: {len(wired_now)} ({', '.join(wired_now[:8])}{'...' if len(wired_now) > 8 else ''})")
print(f"includes added: {len(include_lines)}, map entries added: {len(map_lines)}")
print(f"pending anchors remaining: {remaining}")
if skipped:
    print(f"stopped at first missing template: {skipped[0]}")

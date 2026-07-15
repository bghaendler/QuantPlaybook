#!/usr/bin/env python3
"""Audit every sidebar topic's completeness and inject the result into the
Content Status dashboard (view-content-status.html).

Classification (per section):
  Not Started - stub markers ("Coming Soon" etc.) or near-empty content
  Complete    - substantial content + Plain English Notes + an interactive demo
  Medium      - everything in between

Run after any content change: python3 scratch/audit_content_status.py
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDX = os.path.join(ROOT, "app", "index.html")
SECTIONS = os.path.join(ROOT, "app", "templates", "sections")
DASHBOARD = os.path.join(SECTIONS, "view-content-status.html")

# Meta-navigation utility links that also live inside a domain's sidebar
# block (e.g. the "Talks Portal" entry point at the top of TALKS) - not
# gradable content topics, so excluded from the audit.
UTILITY_KEYS = {"talks-portal", "thematic-portal", "content-status", "module2"}

DOMAIN_IDS = {
    "section-academic": "Core Curriculum",
    "section-mathematical-methods": "Mathematical Methods",
    "section-masterclass": "Masterclasses",
    "section-interactive-desk": "Trading & Risk Desks",
    "section-talks": "Talks",
}

STUB_PATTERNS = [
    "content pending", "not been mathematically implemented",
    "under construction", "to be implemented", "work in progress",
]
# The exact outline-only stub heading (12 legacy CMM pages: topic list + Plain
# English card + "coming soon" trailer, no real derivations). Deliberately an
# exact tag match, not a substring like "coming soon" - every enriched talk
# page also carries an honest "more detail coming" trailer note, so a loose
# phrase match would misclassify hundreds of genuinely-populated pages.
STUB_HEADING = re.compile(r"<h3>Core Topics</h3>")

DEMO_PATTERNS = [
    r'type="range"', r"<canvas", r"<select\b", r"addEventListener\(",
    r"new Chart\(", r"Plotly\.newPlot", r"d3\.select", r"<input\b",
    # onclick= counts as a demo signal only when it drives computation, not
    # when it's a bare in-app navigation link (every "All talks"/prev-next
    # button on every talk page calls onclick="showSection(...)").
    r'onclick="(?!showSection\()',
]


def strip_tags(html):
    html = re.sub(r"<script\b.*?</script>", " ", html, flags=re.S)
    html = re.sub(r"<style\b.*?</style>", " ", html, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"&[a-zA-Z#0-9]+;", " ", text)
    return re.sub(r"\s+", " ", text).strip()


# Pages that mount substantial content the static classifier can't see (e.g.
# an <iframe> into the separately-built React option pricer, with 26 model
# walkthroughs, KaTeX and Plotly). Manually verified complete.
EXTERNALLY_MOUNTED = {"view-cqf-option-pricer"}


def classify(raw, el=None):
    if el in EXTERNALLY_MOUNTED:
        return "complete", 0, True, True, True

    low = raw.lower()
    is_stub = any(p in low for p in STUB_PATTERNS) or bool(STUB_HEADING.search(raw))
    text = strip_tags(raw)
    word_count = len(text.split())
    has_plain_english = "plain english" in low
    has_math = bool(re.search(r"\$[^$\n]{3,}\$|\\\(|\\\[|\$\$", raw))
    has_demo = any(re.search(p, raw) for p in DEMO_PATTERNS)

    if is_stub or word_count < 40:
        return "not-started", word_count, has_plain_english, has_math, has_demo
    if has_plain_english and has_demo and word_count >= 150:
        return "complete", word_count, has_plain_english, has_math, has_demo
    return "medium", word_count, has_plain_english, has_math, has_demo


def reasons_for(status, word_count, has_pe, has_math, has_demo):
    if status == "complete":
        return []
    missing = []
    if word_count < 150:
        missing.append("short content")
    if not has_pe:
        missing.append("no Plain English Notes")
    if not has_demo:
        missing.append("no interactive demo")
    if not has_math:
        missing.append("no formulas")
    return missing


def parse_sidebar():
    html = open(IDX, encoding="utf-8").read()
    start = html.index("EXPLORE\n     ====")
    end = html.index("</aside>")
    region = html[start:end]

    section_map = dict(re.findall(
        r"'([a-z0-9-]+)':\s*\{\s*el:\s*'([a-z0-9-]+)'", html))

    domain_stack = []
    group_stack = []
    entries = []

    token_re = re.compile(
        r'<details class="nav-level-1 unified-section" id="([^"]+)"[^>]*>'
        r'|<details class="nav-level-2"[^>]*>'
        r'|<details[^>]*>'
        r'|</details>'
        r'|<summary[^>]*>(.*?)</summary>'
        r'|<a class="nav-item[^"]*" href="#([^"]+)"[^>]*>(.*?)</a>',
        re.S,
    )

    # track nesting with a generic stack of (kind, label)
    stack = []
    pending_domain_id = None
    for m in token_re.finditer(region):
        tok = m.group(0)
        if tok.startswith('<details class="nav-level-1'):
            stack.append({"kind": "domain", "id": m.group(1), "label": None})
        elif tok.startswith("<details"):
            stack.append({"kind": "group", "id": None, "label": None})
        elif tok.startswith("</details>"):
            if stack:
                stack.pop()
        elif tok.startswith("<summary"):
            label = re.sub(r"<[^>]+>", "", m.group(2)).strip()
            label = label.replace("&amp;", "&")
            if stack:
                stack[-1]["label"] = label
        else:
            href = m.group(3)
            link_label = re.sub(r"<[^>]+>", "", m.group(4)).strip()
            link_label = re.sub(r"\s+", " ", link_label).replace("&amp;", "&")
            domain_frame = next((f for f in stack if f["kind"] == "domain"), None)
            if not domain_frame:
                continue
            domain_name = DOMAIN_IDS.get(domain_frame["id"])
            if not domain_name:
                continue  # EXPLORE etc. excluded - navigation/utility, not topics
            group_labels = [f["label"] for f in stack if f["kind"] == "group" and f["label"]]
            group = " › ".join(group_labels) if group_labels else ""
            entries.append({
                "key": href, "title": link_label, "domain": domain_name, "group": group,
            })
    return entries, section_map


def main():
    entries, section_map = parse_sidebar()
    rows = []
    missing_files = []
    seen = set()
    for e in entries:
        if e["key"] in UTILITY_KEYS:
            continue
        dedupe_key = (e["key"], e["title"])
        if dedupe_key in seen:
            continue
        seen.add(dedupe_key)
        el = section_map.get(e["key"])
        if not el:
            continue
        path = os.path.join(SECTIONS, f"{el}.html")
        if not os.path.exists(path):
            missing_files.append(e["key"])
            continue
        raw = open(path, encoding="utf-8").read()
        status, wc, has_pe, has_math, has_demo = classify(raw, el=el)
        reasons = reasons_for(status, wc, has_pe, has_math, has_demo)
        rows.append({
            "key": e["key"], "title": e["title"], "domain": e["domain"],
            "group": e["group"], "status": status, "words": wc, "reasons": reasons,
        })

    counts = {"complete": 0, "medium": 0, "not-started": 0}
    for r in rows:
        counts[r["status"]] += 1

    domains = sorted({r["domain"] for r in rows})

    data_js = (
        "// CS_DATA_START — generated by scratch/audit_content_status.py; do not edit by hand\n"
        "var CS_DOMAINS = " + json.dumps(domains, ensure_ascii=False) + ";\n"
        "var CS_ROWS = " + json.dumps(rows, ensure_ascii=False, separators=(",", ":")) + ";\n"
        "// CS_DATA_END"
    )

    dashboard_html = open(DASHBOARD, encoding="utf-8").read()
    new_html = re.sub(r"// CS_DATA_START.*?// CS_DATA_END", data_js, dashboard_html, flags=re.S)
    if new_html == dashboard_html and "CS_DATA_START" not in dashboard_html:
        raise SystemExit("markers not found in view-content-status.html")
    open(DASHBOARD, "w", encoding="utf-8").write(new_html)

    print(f"{len(rows)} topics audited across {len(domains)} domains")
    print(f"  Complete:    {counts['complete']:4d}  ({counts['complete']/len(rows)*100:.1f}%)")
    print(f"  Medium:      {counts['medium']:4d}  ({counts['medium']/len(rows)*100:.1f}%)")
    print(f"  Not Started: {counts['not-started']:4d}  ({counts['not-started']/len(rows)*100:.1f}%)")
    if missing_files:
        print(f"  WARNING: {len(missing_files)} nav keys had no matching template: {missing_files[:10]}")
    for d in domains:
        dr = [r for r in rows if r["domain"] == d]
        c = sum(1 for r in dr if r["status"] == "complete")
        m = sum(1 for r in dr if r["status"] == "medium")
        n = sum(1 for r in dr if r["status"] == "not-started")
        print(f"    {d:24s} total={len(dr):4d}  complete={c:4d}  medium={m:4d}  not-started={n:4d}")


if __name__ == "__main__":
    main()

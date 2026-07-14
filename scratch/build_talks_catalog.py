#!/usr/bin/env python3
"""Build the CQF Talks catalog from TALKS_ROADMAP.md.

Outputs:
  - scratch/talks_catalog.json                      (canonical catalog)
  - injects TK_CATS/TK data into
    app/templates/sections/view-talks-portal.html   (between TK_DATA_* markers)

Run from anywhere:  python3 scratch/build_talks_catalog.py
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROADMAP = os.path.join(ROOT, "TALKS_ROADMAP.md")
PORTAL = os.path.join(ROOT, "app", "templates", "sections", "view-talks-portal.html")
CATALOG = os.path.join(ROOT, "scratch", "talks_catalog.json")

# Roadmap "## N." heading -> (category key, portal label)
CATEGORIES = {
    1: ("legacy", "Legacy Lecture Series"),
    2: ("volatility", "Volatility & Smile"),
    3: ("options", "Options & BSM"),
    4: ("rates", "Rates & Fixed Income"),
    5: ("credit", "Credit, XVA & Structured"),
    6: ("portfolio", "Portfolio & Allocation"),
    7: ("kelly", "Kelly & Ziemba"),
    8: ("ml-ai", "Machine Learning & AI"),
    9: ("nlp", "NLP, Sentiment & Alt Data"),
    10: ("quantum", "Quantum Computing"),
    11: ("crypto", "Crypto & DeFi"),
    12: ("commodities", "Commodities & Energy"),
    13: ("microstructure", "Microstructure & Algo Trading"),
    14: ("risk", "Risk Management & Regulation"),
    15: ("esg", "ESG & Climate"),
    16: ("dev", "Numerical Methods, HPC & Dev"),
    17: ("careers", "Careers & Industry"),
    18: ("history", "History & Philosophy"),
}

# §1 series subsection number -> slug abbreviation
SERIES_ABBR = {
    "1.1": "mmnm", "1.2": "bsmw", "1.3": "mart", "1.4": "pmir", "1.5": "rba",
    "1.6": "mrc", "1.7": "lwv", "1.8": "bgm", "1.9": "strm", "1.10": "acm",
    "1.11": "fim", "1.12": "mcam", "1.13": "nf",
}

# Talks already implemented before this catalog existed (title substring -> slug)
ALIASES = {
    "a revolution in risk management": "talk-ai-risk-management",
    "behavioral economics approach to ai safety": "talk-ai-safety",
    "natural language processing for sustainable development": "talk-nlp-sdg",
    "customizing large language models": "talk-llm-quant",
    "beating markowitz with sentiment": "talk-sentiment-portfolios",
    "de-constructing a trend following": "talk-trend-following",
    "limit order book flows and price formation in crypto": "talk-crypto-lob",
    "the kelly capital growth investment criterion": "talk-kelly-ziemba",
    "overcoming markowitz's instability": "talk-hrp",
    "a novel way to diversify portfolio weights": "talk-max-diversification",
    "a quantum finance approach to option pricing": "talk-quantum-pricing",
    "how can current quantum computing help with ml": "talk-quantum-ml",
    "let's do quantum economics": "talk-quantum-economics",
    "a day in the life of a quantitative portfolio manager": "talk-day-portfolio-manager",
    "a day of a quant trader": "talk-day-quant-trader",
    "a day in the life of a quant auditor": "talk-day-quant-auditor",
    "master the quant finance interview": "talk-quant-interview",
}


def slugify(title, used, prefix="talk-"):
    s = title.lower()
    s = s.replace("&", " and ")
    s = re.sub(r"[’']", "", s)
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    words = s.split("-")
    out = []
    for w in words:
        if len("-".join(out + [w])) > 44:
            break
        out.append(w)
    s = prefix + "-".join(out)
    base, i = s, 2
    while s in used:
        s = f"{base}-{i}"
        i += 1
    used.add(s)
    return s


def extract_presenter(title):
    """'Title — Name Surname' -> (title, presenter) when the tail looks like a name."""
    if " — " not in title:
        return title, ""
    head, tail = title.rsplit(" — ", 1)
    words = tail.replace(".", "").split()
    namey = 1 <= len(words) <= 5 and all(w[0].isupper() for w in words if w[0].isalpha())
    if namey and not any(ch.isdigit() for ch in tail) and "(" not in tail:
        return head.strip(), tail.strip()
    return title, ""


def parse():
    talks, used = [], set()
    cat_key, series_name, series_no = None, None, None

    with open(ROADMAP, encoding="utf-8") as fh:
        lines = fh.readlines()

    def add(title, series=None):
        title = title.strip().rstrip("·").strip()
        if not title:
            return
        clean, presenter = extract_presenter(title)
        low = clean.lower()
        slug = None
        for frag, alias in ALIASES.items():
            if frag in low:
                slug = alias
                break
        if slug is None:
            if series and series_no in SERIES_ABBR:
                m = re.search(r"(\d+)", title)
                part = m.group(1).zfill(2) if m else "00"
                slug = f"talk-{SERIES_ABBR[series_no]}-p{part}"
                if slug in used:
                    slug = slugify(clean, used)
                else:
                    used.add(slug)
            else:
                slug = slugify(clean, used)
        else:
            used.add(slug)
        full = f"{series}: {clean}" if series else clean
        talks.append({"slug": slug, "title": full, "cat": cat_key, "presenter": presenter})

    for line in lines:
        line = line.rstrip()
        m = re.match(r"^## (\d+)\.", line)
        if m:
            n = int(m.group(1))
            cat_key = CATEGORIES.get(n, (None,))[0]
            series_name, series_no = None, None
            continue
        m = re.match(r"^### (\d+\.\d+) (.+)$", line)
        if m and cat_key == "legacy":
            series_no = m.group(1)
            name = re.sub(r"\s*\((?:\d+ (?:parts|lectures|sections)[^)]*)\)\s*$", "", m.group(2))
            name = re.sub(r"\s*—\s*[^—]*$", "", name) if "— Dr" in name or "— Dan" in name or "— Claudio" in name else name
            series_name = name.strip()
            if "stand-alone" in series_name.lower():
                series_name, series_no = None, None
            continue
        if cat_key is None or not line.startswith("- ["):
            continue
        body = re.sub(r"^- \[[ x~]\]\s*", "", line)
        if " · " in body or "· [" in body:
            chunks = re.split(r"\s*·\s*", body)
            for ch in chunks:
                ch = re.sub(r"^\[[ x~]\]\s*", "", ch).strip()
                if ch:
                    add(ch, series=series_name)
        else:
            add(body, series=series_name if series_name else None)
    return talks


def inject_portal(talks):
    cats_js = {k: v for k, v in (CATEGORIES[n] for n in sorted(CATEGORIES))}
    rows = [[t["slug"], t["title"], t["cat"], t["presenter"]] for t in talks]
    data = (
        "// TK_DATA_START — generated by scratch/build_talks_catalog.py; do not edit by hand\n"
        + "var TK_CATS = " + json.dumps(cats_js, ensure_ascii=False) + ";\n"
        + "var TK = " + json.dumps(rows, ensure_ascii=False, separators=(",", ":")) + ";\n"
        + "// TK_DATA_END"
    )
    with open(PORTAL, encoding="utf-8") as fh:
        html = fh.read()
    new = re.sub(r"// TK_DATA_START.*?// TK_DATA_END", data, html, flags=re.S)
    if new == html and "TK_DATA_START" not in html:
        sys.exit("Portal markers not found in view-talks-portal.html")
    with open(PORTAL, "w", encoding="utf-8") as fh:
        fh.write(new)


def main():
    talks = parse()
    dupes = [s for s in {t["slug"] for t in talks} if sum(1 for t in talks if t["slug"] == s) > 1]
    if dupes:
        sys.exit(f"Duplicate slugs: {dupes}")
    with open(CATALOG, "w", encoding="utf-8") as fh:
        json.dump(talks, fh, indent=1, ensure_ascii=False)
    inject_portal(talks)
    from collections import Counter
    counts = Counter(t["cat"] for t in talks)
    print(f"{len(talks)} talks -> {CATALOG}")
    for n in sorted(CATEGORIES):
        k, label = CATEGORIES[n]
        print(f"  {label:35s} {counts.get(k, 0)}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Scaffold CQF Talk sections into the app.

For each talk in scratch/talks_catalog.json this generates:
  1. app/templates/sections/view-<slug>.html   (outline template, ready to deepen)
  2. an {% include %} at the TALKS_INCLUDES marker in app/index.html
  3. a _sectionMap entry at the TALKS_SECTIONMAP marker
  4. a sidebar nav link at the matching TALKS_NAV:<category> marker

Idempotent: talks already wired are skipped.

Usage:
  python3 scratch/scaffold_talk.py talk-mrc-p01 talk-mrc-p02   # specific slugs
  python3 scratch/scaffold_talk.py --category volatility        # whole category
  python3 scratch/scaffold_talk.py --category legacy --limit 5
  python3 scratch/scaffold_talk.py --all
Run scratch/build_talks_catalog.py first if TALKS_ROADMAP.md changed.
"""
import argparse
import html as htmlmod
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDX = os.path.join(ROOT, "app", "index.html")
SECTIONS = os.path.join(ROOT, "app", "templates", "sections")
CATALOG = os.path.join(ROOT, "scratch", "talks_catalog.json")

CAT_LABELS = {
    "legacy": "Legacy Lecture Series", "volatility": "Volatility & Smile",
    "options": "Options & BSM", "rates": "Rates & Fixed Income",
    "credit": "Credit, XVA & Structured", "portfolio": "Portfolio & Allocation",
    "kelly": "Kelly & Ziemba", "ml-ai": "Machine Learning & AI",
    "nlp": "NLP, Sentiment & Alt Data", "quantum": "Quantum Computing",
    "crypto": "Crypto & DeFi", "commodities": "Commodities & Energy",
    "microstructure": "Microstructure & Algo Trading", "risk": "Risk Management & Regulation",
    "esg": "ESG & Climate", "dev": "Numerical Methods, HPC & Dev",
    "careers": "Careers & Industry", "history": "History & Philosophy",
}

TEMPLATE = """<div id="view-{slug_view}" style="display: none; font-family: var(--font-family-sans);">
    <header style="margin-bottom: 2rem;">
        <p style="color: var(--accent); font-weight: 700; font-size: 0.8rem; text-transform: uppercase; margin: 0;">CQF Talks &bull; {cat_label}</p>
        <h1 style="margin: 0; font-size: 2rem; font-weight: 800; border-bottom: none; padding-bottom: 0;">{title}</h1>
        <p style="color: var(--text-muted); margin-top: 0.5rem;">{subtitle}</p>
    </header>

    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 2rem; align-items: stretch; margin-bottom: 2rem;">
        <div class="card" style="margin-bottom: 0; padding: 1.5rem;">
            <h3>Key Ideas</h3>
            <ul style="line-height: 1.8;">
                <li>Core themes covered in this talk (to be filled in).</li>
                <li>Definitions, models and formulas introduced.</li>
                <li>Practical takeaways for the working quant.</li>
            </ul>
        </div>
        <div class="card" style="margin-bottom: 0; background: #fffbeb; border-left: 4px solid #f59e0b; border-radius: 8px; padding: 1.5rem;">
            <h3 style="margin-top: 0; color: #b45309; font-family: 'Inter', sans-serif; font-weight: 700;">Plain English Notes</h3>
            <p style="font-family: 'Inter', sans-serif; line-height: 1.6; color: #451a03; margin-bottom: 0;"><strong>The Big Picture:</strong> One-paragraph intuition for what this talk teaches and why it matters (to be filled in).</p>
        </div>
    </div>

    <div class="card" style="border-left: 4px solid var(--accent); background: var(--bg-subtle);">
        <h3 style="margin-top:0;">Detailed Notes Coming Soon</h3>
        <p style="margin-bottom:0; color: var(--text-secondary);">This talk section has been scaffolded from <code>TALKS_ROADMAP.md</code>. Derivations, worked examples and interactive demos will be added here.</p>
    </div>
</div>
"""


def wire(talks, idx_html):
    made, skipped = [], []
    for t in talks:
        slug, title, cat = t["slug"], t["title"], t["cat"]
        map_line = f"'{slug}':"
        if map_line in idx_html:
            skipped.append(slug)
            continue
        cat_marker = f"<!-- TALKS_NAV:{cat} -->"
        if cat_marker not in idx_html:
            sys.exit(f"nav marker missing for category '{cat}'")

        # 1. template file
        path = os.path.join(SECTIONS, f"view-{slug}.html")
        if not os.path.exists(path):
            esc = htmlmod.escape(title)
            subtitle = htmlmod.escape(t.get("presenter") or "CQF Talks lecture notes")
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(TEMPLATE.format(slug_view=slug, cat_label=htmlmod.escape(CAT_LABELS[cat]),
                                         title=esc, subtitle=subtitle))

        # 2. include
        inc_marker = "<!-- TALKS_INCLUDES (scaffold_talk.py inserts talk templates here) -->"
        inc = f'{{% include "templates/sections/view-{slug}.html" %}}\n            {inc_marker}'
        idx_html = idx_html.replace(inc_marker, inc, 1)

        # 3. sectionMap
        map_marker = "// TALKS_SECTIONMAP (scaffold_talk.py inserts talk entries here)"
        entry = f"'{slug}': {{ el: 'view-{slug}', math: true }},\n            {map_marker}"
        idx_html = idx_html.replace(map_marker, entry, 1)

        # 4. nav link (short label: strip series prefix duplication for readability)
        label = htmlmod.escape(title)
        nav = (f'<a class="nav-item" href="#{slug}" onclick="showSection(\'{slug}\')">{label}</a>'
               f"\n        {cat_marker}")
        idx_html = idx_html.replace(cat_marker, nav, 1)
        made.append(slug)
    return idx_html, made, skipped


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slugs", nargs="*")
    ap.add_argument("--category", choices=sorted(CAT_LABELS))
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--limit", type=int)
    args = ap.parse_args()

    catalog = json.load(open(CATALOG, encoding="utf-8"))
    by_slug = {t["slug"]: t for t in catalog}

    if args.all:
        picked = catalog
    elif args.category:
        picked = [t for t in catalog if t["cat"] == args.category]
    elif args.slugs:
        unknown = [s for s in args.slugs if s not in by_slug]
        if unknown:
            sys.exit(f"not in catalog: {unknown}")
        picked = [by_slug[s] for s in args.slugs]
    else:
        ap.error("give slugs, --category, or --all")
    if args.limit:
        picked = picked[: args.limit]

    idx_html = open(IDX, encoding="utf-8").read()
    idx_html, made, skipped = wire(picked, idx_html)
    if made:
        open(IDX, "w", encoding="utf-8").write(idx_html)
    print(f"scaffolded {len(made)}, skipped (already wired) {len(skipped)}")
    for s in made:
        print("  +", s)


if __name__ == "__main__":
    main()

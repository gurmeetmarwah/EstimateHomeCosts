#!/usr/bin/env python3
"""Inject methodology trust callout into root calculator pages (once)."""
from __future__ import annotations

import re
from pathlib import Path

from trust_content import trust_callout_html

ROOT = Path(__file__).resolve().parents[1]
MARKER = 'class="trust-methodology-section"'
CALCULATOR_DIRS = (
    "roof-cost-calculator",
    "hvac-cost-calculator",
    "flooring-cost-calculator",
    "fence-cost-calculator",
    "solar-panel-cost-calculator",
)


def inject(html: str) -> str:
    if MARKER in html:
        return html
    block = trust_callout_html() + "\n\n"
    # Insert before FAQ section when present
    faq_match = re.search(r'\n(\s*)<section id="faq"', html)
    if faq_match:
        idx = faq_match.start()
        return html[:idx] + "\n" + block + html[idx:]
    # Fallback: before related section
    rel_match = re.search(r'\n(\s*)<section id="related"', html)
    if rel_match:
        idx = rel_match.start()
        return html[:idx] + "\n" + block + html[idx:]
    return html.replace("  </main>", block + "  </main>", 1)


def main() -> None:
    for name in CALCULATOR_DIRS:
        path = ROOT / name / "index.html"
        if not path.is_file():
            print(f"Skip missing: {path}")
            continue
        original = path.read_text(encoding="utf-8")
        updated = inject(original)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            print(f"Updated {path.relative_to(ROOT)}")
        else:
            print(f"No change: {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

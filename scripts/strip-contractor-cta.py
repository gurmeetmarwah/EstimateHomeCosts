#!/usr/bin/env python3
"""Remove contractor quote-comparison CTAs, lead forms, and sticky quote bars from HTML pages."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TEXT_REPLACEMENTS = [
    (
        "Use our calculators for a localized range, then compare contractor bids.",
        "Use our calculators for a localized range when planning your project budget.",
    ),
    (
        "Ranges validated against contractor bids (±10–15% typical variance)",
        "Ranges validated against industry benchmarks (±10–15% typical variance)",
    ),
    (
        "before requesting contractor bids",
        "before finalizing your project budget",
    ),
    (
        ' or <a href="#contractor-cta">get a free inspection quote</a> from a local roofer.',
        ".",
    ),
]

LINK_REMOVALS = [
    r'\s*<a href="#contractor-cta" class="btn btn-header">Get Free Quotes</a>\n',
    r'\s*<li><a href="#contractor-cta" class="btn btn-primary">Get Free Quotes</a></li>\n',
    r'\s*<a href="#contractor-cta" class="btn btn-secondary btn-lg">Compare[^<]*</a>\n',
    r'\s*<a href="#contractor-cta" class="btn btn-primary btn-block">Compare[^<]*</a>\n',
]


def strip_html(html: str) -> str:
    html = re.sub(
        r'\n?\s*<!--\s*\d*\.?\s*(Lead CTA|Contractor CTA)[^>]*-->\s*\n'
        r'\s*<section id="contractor-cta"[\s\S]*?</section>\s*\n',
        "\n",
        html,
        flags=re.IGNORECASE,
    )
    html = re.sub(
        r'\n?\s*<section id="contractor-cta"[\s\S]*?</section>\s*\n',
        "\n",
        html,
    )
    html = re.sub(
        r'\n?\s*<aside class="sticky-cta"[\s\S]*?</aside>\s*\n',
        "\n",
        html,
    )
    for pattern in LINK_REMOVALS:
        html = re.sub(pattern, "\n", html)
    for old, new in TEXT_REPLACEMENTS:
        html = html.replace(old, new)
    html = re.sub(
        r'>Get Free Quotes<',
        ">Calculate Your Cost<",
        html,
    )
    return html


def main() -> None:
    changed = 0
    for path in sorted(ROOT.rglob("*.html")):
        if "node_modules" in path.parts:
            continue
        original = path.read_text(encoding="utf-8")
        updated = strip_html(original)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            changed += 1
            print(f"Updated {path.relative_to(ROOT)}")
    print(f"Done — {changed} file(s) updated.")


if __name__ == "__main__":
    main()

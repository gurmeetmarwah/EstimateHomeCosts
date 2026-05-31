#!/usr/bin/env python3
"""Generate methodology and data-sources trust pages."""
from __future__ import annotations

from pathlib import Path

from trust_content import render_data_sources_page, render_methodology_page

ROOT = Path(__file__).resolve().parents[1]

PAGES = {
    "methodology/index.html": render_methodology_page,
    "data-sources/index.html": render_data_sources_page,
}


def main() -> None:
    for rel, builder in PAGES.items():
        out = ROOT / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(builder(), encoding="utf-8")
        print(f"Wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

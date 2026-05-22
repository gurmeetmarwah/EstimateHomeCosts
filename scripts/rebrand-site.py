#!/usr/bin/env python3
"""Replace Home Metric branding with Estimate Home Costs across the repo."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REPLACEMENTS = [
    ("Home <strong>Metric</strong>", "Estimate <strong>Home Costs</strong>"),
    ("Home Metric", "Estimate Home Costs"),
]

EXTENSIONS = {".html", ".md", ".py", ".js", ".css", ".xml", ".txt"}


def rebrand_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text
    for old, new in REPLACEMENTS:
        text = text.replace(old, new)
    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    changed = 0
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix not in EXTENSIONS:
            continue
        if "node_modules" in path.parts or path.name == "rebrand-site.py":
            continue
        if rebrand_file(path):
            changed += 1
            print(path.relative_to(ROOT))
    print(f"\nUpdated {changed} files.")


if __name__ == "__main__":
    main()

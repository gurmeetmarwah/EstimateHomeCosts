#!/usr/bin/env python3
"""Replace homemetric.com with estimatehomecosts.com across the repo."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OLD = "https://estimatehomecosts.com"
NEW = "https://estimatehomecosts.com"
EXTENSIONS = {".html", ".md", ".py", ".js", ".css", ".xml", ".txt"}


def main() -> None:
    changed = 0
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix not in EXTENSIONS:
            continue
        if "node_modules" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        if OLD not in text:
            continue
        path.write_text(text.replace(OLD, NEW), encoding="utf-8")
        changed += 1
    print(f"Updated {changed} files: {OLD} → {NEW}")


if __name__ == "__main__":
    main()

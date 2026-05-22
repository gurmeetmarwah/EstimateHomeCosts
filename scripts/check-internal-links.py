#!/usr/bin/env python3
"""Report internal hrefs that do not resolve to an index.html in the repo."""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import urlparse, unquote

ROOT = Path(__file__).resolve().parents[1]
STATE_SLUGS = {"texas", "florida", "arizona", "north-carolina", "california"}
HREF_RE = re.compile(r'href="(/[^"#?]*)"', re.I)


def path_to_file(url_path: str) -> Path | None:
    path = unquote(url_path.split("?")[0].split("#")[0])
    if not path.startswith("/"):
        return None
    rel = path.strip("/")
    if not rel:
        return ROOT / "index.html"
    candidate = ROOT / rel / "index.html"
    if candidate.is_file():
        return candidate
    if (ROOT / rel).is_file():
        return ROOT / rel
    return None


def main() -> int:
    broken: list[tuple[str, str, str]] = []
    for html in sorted(ROOT.rglob("*.html")):
        if "node_modules" in html.parts:
            continue
        text = html.read_text(encoding="utf-8", errors="replace")
        for m in HREF_RE.finditer(text):
            href = m.group(1)
            if href.startswith(("/css/", "/js/", "/api/", "/privacy", "/terms")):
                continue
            if href.startswith("/#") or href in ("/",):
                continue
            parts = [p for p in href.split("/") if p]
            if parts and parts[0] not in STATE_SLUGS and parts[0] in (
                "compare",
                "search",
                "locations",
            ):
                continue
            if not path_to_file(href):
                broken.append((str(html.relative_to(ROOT)), href, ""))

    by_href: dict[str, list[str]] = {}
    for src, href, _ in broken:
        by_href.setdefault(href, []).append(src)

    if not by_href:
        print("OK: no broken internal page links found.")
        return 0

    print(f"BROKEN: {len(by_href)} unique hrefs ({len(broken)} occurrences)\n")
    for href in sorted(by_href):
        print(href)
        for src in sorted(set(by_href[href]))[:8]:
            print(f"  - {src}")
        if len(by_href[href]) > 8:
            print(f"  ... +{len(by_href[href]) - 8} more")
        print()
    return 1


if __name__ == "__main__":
    sys.exit(main())

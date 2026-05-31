#!/usr/bin/env python3
"""Generate sitemap.xml from all index.html pages in the site."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from brand import SITE_ORIGIN
from geo_paths import POPULAR_CITY_HUB_SLUGS

STATE_SLUGS = frozenset(POPULAR_CITY_HUB_SLUGS.keys())
CITY_HUBS = {state: hubs for state, hubs in POPULAR_CITY_HUB_SLUGS.items()}

ROOT_CALCULATORS = frozenset({
    "roof-cost-calculator",
    "hvac-cost-calculator",
    "flooring-cost-calculator",
    "fence-cost-calculator",
    "solar-panel-cost-calculator",
})

SKIP_DIRS = frozenset({"node_modules", ".git", "scripts", "css", "js"})


def discover_paths() -> list[str]:
    paths: list[str] = []
    for index in sorted(ROOT.rglob("index.html")):
        if any(part in SKIP_DIRS for part in index.parts):
            continue
        rel = index.parent.relative_to(ROOT)
        if rel == Path("."):
            paths.append("")
        else:
            paths.append(rel.as_posix())
    return paths


def priority_for(path: str) -> float:
    if not path:
        return 1.0

    parts = path.split("/")
    depth = len(parts)
    head = parts[0]

    if path in ("methodology", "data-sources"):
        return 0.88

    if head == "compare":
        return 0.9

    if head == "cost":
        return 0.95

    if depth == 1 and parts[0] in ROOT_CALCULATORS:
        return 0.98

    if depth == 2 and parts[0] in ROOT_CALCULATORS:
        return 0.94

    if depth == 1 and parts[0].endswith("-materials"):
        return 0.92

    if depth == 2 and parts[0].endswith("-materials"):
        return 0.92

    if depth == 1 and head in STATE_SLUGS:
        return 0.96

    if depth == 2 and head in STATE_SLUGS:
        state, second = parts[0], parts[1]
        if second in CITY_HUBS.get(state, frozenset()):
            return 0.95
        return 0.85

    if depth >= 3 and head in STATE_SLUGS:
        state, city = parts[0], parts[1]
        if city in CITY_HUBS.get(state, frozenset()):
            return 0.8 if depth == 3 else 0.78

    return 0.75


def changefreq_for(path: str) -> str:
    if path in ("methodology", "data-sources"):
        return "monthly"
    return "weekly"


def url_entry(path: str) -> str:
    loc = SITE_ORIGIN + ("/" if not path else f"/{path}/")
    pri = priority_for(path)
    freq = changefreq_for(path)
    return f"""  <url>
    <loc>{loc}</loc>
    <changefreq>{freq}</changefreq>
    <priority>{pri:.2f}</priority>
  </url>"""


def render(paths: list[str]) -> str:
    # Sort: higher priority first, then alphabetical
    ordered = sorted(paths, key=lambda p: (-priority_for(p), p))
    entries = "\n".join(url_entry(p) for p in ordered)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{entries}
</urlset>
"""


def main() -> None:
    paths = discover_paths()
    out = ROOT / "sitemap.xml"
    out.write_text(render(paths), encoding="utf-8")
    print(f"Wrote {out.relative_to(ROOT)} with {len(paths)} URLs")


if __name__ == "__main__":
    main()

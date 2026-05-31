#!/usr/bin/env python3
"""Validate city/state page figures match cost_engine calculator output."""

from __future__ import annotations

import re
import sys
from pathlib import Path

from cities_config import POPULAR_CITIES
from cost_engine import city_snapshots, example_mid, fmt_money
from pricing_cities import CITIES, STATE_DEFAULT_CITY

ROOT = Path(__file__).resolve().parents[1]


def check_city_hub(city_key: str, html_path: Path) -> list[str]:
    errors: list[str] = []
    if not html_path.exists():
        return [f"missing hub page: {html_path}"]
    text = html_path.read_text(encoding="utf-8")

    for snap in city_snapshots(city_key):
        if snap["range"] not in text:
            errors.append(f"{html_path.name}: snapshot range {snap['range']!r} ({snap['title']}) not found")

    if "DFW metro" in text:
        errors.append(f"{html_path.name}: contains stale DFW metro permit text")

    if re.search(r"\$5,000–\$80,000", text):
        errors.append(f"{html_path.name}: contains generic national FAQ renovation range")

    return errors


def check_state_hub(state_slug: str, html_path: Path) -> list[str]:
    errors: list[str] = []
    if not html_path.exists():
        return [f"missing state page: {html_path}"]
    text = html_path.read_text(encoding="utf-8")
    key = STATE_DEFAULT_CITY.get(state_slug, "national")

    for snap in city_snapshots(key):
        if snap["range"] not in text:
            errors.append(f"{state_slug}: snapshot range {snap['range']!r} ({snap['title']}) not found")

    return errors


def main() -> int:
    errors: list[str] = []

    for city in POPULAR_CITIES:
        path = ROOT / city["state_slug"] / city["slug"] / "index.html"
        errors.extend(check_city_hub(city["city_key"], path))

    for state_slug in STATE_DEFAULT_CITY:
        path = ROOT / state_slug / "index.html"
        errors.extend(check_state_hub(state_slug, path))

    missing_js = [k for k in CITIES if k != "national" and k not in {
        c["city_key"] for c in POPULAR_CITIES
    } and k not in STATE_DEFAULT_CITY.values()]

    print(f"Validated {len(POPULAR_CITIES)} city hubs and {len(STATE_DEFAULT_CITY)} state hubs.")
    if errors:
        print(f"\n{len(errors)} issue(s):")
        for e in errors:
            print(f"  - {e}")
        return 1

    print("All page figures match cost_engine output.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

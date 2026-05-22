#!/usr/bin/env python3
"""Mirror calculator/guide pages under /{state}/ with Texas context via city-path.js."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from cities_config import SCOPED_PATHS
from geo_paths import state_prefix_path
from states_config import POPULAR_STATE_SLUGS

INJECT = '  <script src="/js/city-path.js"></script>\n'


def rewrite_html_for_state(html: str, state_slug: str) -> str:
    def href_repl(m: re.Match[str]) -> str:
        path = m.group(1)
        return f'href="{state_prefix_path(path, state_slug)}"'

    html = re.sub(r'href="(/[^"#]*)"', href_repl, html)

    def canonical_repl(m: re.Match[str]) -> str:
        path = m.group(2)
        new = state_prefix_path(path, state_slug)
        return f'{m.group(1)}{new}"'

    html = re.sub(
        r'(href="https://estimatehomecosts\.com)(/[^"]*)"',
        canonical_repl,
        html,
    )
    return html


def mirror_page(state_slug: str, rel: str) -> None:
    src = ROOT / rel / "index.html"
    if not src.is_file():
        print(f"Skip missing: {src}")
        return
    dest = ROOT / state_slug / rel / "index.html"
    html = src.read_text(encoding="utf-8")
    html = rewrite_html_for_state(html, state_slug)
    if "city-path.js" not in html:
        if "calculator-cities.js" in html:
            html = html.replace(
                '<script src="/js/calculator-cities.js" defer></script>',
                '<script src="/js/calculator-cities.js" defer></script>\n' + INJECT.strip(),
                1,
            )
        else:
            html = re.sub(
                r'(<script src="/js/main\.js")',
                INJECT + r"\1",
                html,
                count=1,
            )
        if "city-path.js" not in html:
            html = html.replace("</body>", INJECT + "</body>")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(html, encoding="utf-8")
    print(f"Wrote {dest.relative_to(ROOT)}")


def main() -> None:
    for slug in POPULAR_STATE_SLUGS:
        print(f"--- {slug} (state-scoped) ---")
        for rel in SCOPED_PATHS:
            mirror_page(slug, rel)


if __name__ == "__main__":
    main()

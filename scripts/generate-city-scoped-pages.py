#!/usr/bin/env python3
"""Mirror calculator/guide pages under /{state}/{city}/ with city-path.js."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from cities_config import POPULAR_CITIES, SCOPED_PATHS
from geo_paths import city_prefix_path

INJECT = '  <script src="/js/city-path.js"></script>\n'


def rewrite_html_for_city(html: str, state_slug: str, city_slug: str) -> str:
    def href_repl(m: re.Match[str]) -> str:
        path = m.group(1)
        return f'href="{city_prefix_path(path, state_slug, city_slug)}"'

    html = re.sub(r'href="(/[^"#?]*)"', href_repl, html)

    def canonical_repl(m: re.Match[str]) -> str:
        path = m.group(2)
        new = city_prefix_path(path, state_slug, city_slug)
        return f'{m.group(1)}{new}"'

    html = re.sub(
        r'(href="https://estimatehomecosts\.com)(/[^"]*)"',
        canonical_repl,
        html,
    )
    return html


def mirror_page(state_slug: str, city_slug: str, rel: str) -> None:
    src = ROOT / rel / "index.html"
    if not src.is_file():
        print(f"Skip missing: {src}")
        return
    dest = ROOT / state_slug / city_slug / rel / "index.html"
    html = src.read_text(encoding="utf-8")
    html = rewrite_html_for_city(html, state_slug, city_slug)
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
    for city in POPULAR_CITIES:
        print(f"--- {city['state_slug']}/{city['slug']} ({city['city_key']}) ---")
        for rel in SCOPED_PATHS:
            mirror_page(city["state_slug"], city["slug"], rel)


if __name__ == "__main__":
    main()

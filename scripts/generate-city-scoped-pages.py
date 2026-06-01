#!/usr/bin/env python3
"""Mirror calculator/guide pages under /{state}/{city}/ with city-path.js."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from cities_config import POPULAR_CITIES, SCOPED_PATHS
from geo_paths import city_prefix_path
from local_seo_content import compact_local_block_html, get_city_local_seo

GEO_SCRIPTS = (
    '  <script src="/js/calculator-cities.js"></script>\n'
    '  <script src="/js/city-path.js"></script>\n'
)

LOCAL_CONTEXT_MARKER = 'class="local-seo-compact"'


def ensure_geo_scripts(html: str) -> str:
    """Ensure calculator-cities + city-path load on every city-scoped page."""
    html = re.sub(r'\s*<script src="/js/calculator-cities\.js"></script>\s*', '\n', html)
    html = re.sub(r'\s*<script src="/js/city-path\.js"></script>\s*', '\n', html)
    if 'src="/js/main.js"' in html:
        return html.replace('<script src="/js/main.js"', GEO_SCRIPTS + '<script src="/js/main.js"', 1)
    return html.replace('</body>', GEO_SCRIPTS + '</body>', 1)


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


def inject_local_context(
    html: str,
    state_slug: str,
    city_slug: str,
    city_name: str,
    state_abbr: str,
    city_key: str,
) -> str:
    if LOCAL_CONTEXT_MARKER in html:
        return html
    block = get_city_local_seo(city_key)
    prefix = f"/{state_slug}/{city_slug}"

    def link_fn(path: str) -> str:
        if not path or path[0] != "/":
            return path
        return prefix.rstrip("/") + path

    local_html = compact_local_block_html(
        city_name,
        state_abbr,
        block,
        city_key,
        hub_href=f"/{state_slug}/{city_slug}/",
        link_fn=link_fn,
    )
    faq_match = re.search(r'\n(\s*)<section id="faq"', html)
    if faq_match:
        idx = faq_match.start()
        return html[:idx] + "\n" + local_html + html[idx:]
    rel_match = re.search(r'\n(\s*)<section id="related"', html)
    if rel_match:
        idx = rel_match.start()
        return html[:idx] + "\n" + local_html + html[idx:]
    return html.replace("  </main>", local_html + "  </main>", 1)


def mirror_page(state_slug: str, city_slug: str, rel: str, city_meta: dict) -> None:
    src = ROOT / rel / "index.html"
    if not src.is_file():
        print(f"Skip missing: {src}")
        return
    dest = ROOT / state_slug / city_slug / rel / "index.html"
    html = src.read_text(encoding="utf-8")
    html = rewrite_html_for_city(html, state_slug, city_slug)
    html = ensure_geo_scripts(html)
    html = inject_local_context(
        html,
        state_slug,
        city_slug,
        city_meta["city_name"],
        city_meta["state_abbr"],
        city_meta["city_key"],
    )
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(html, encoding="utf-8")
    print(f"Wrote {dest.relative_to(ROOT)}")


def main() -> None:
    for city in POPULAR_CITIES:
        print(f"--- {city['state_slug']}/{city['slug']} ({city['city_key']}) ---")
        for rel in SCOPED_PATHS:
            mirror_page(city["state_slug"], city["slug"], rel, city)


if __name__ == "__main__":
    main()

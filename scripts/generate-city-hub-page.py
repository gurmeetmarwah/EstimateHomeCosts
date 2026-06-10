#!/usr/bin/env python3
"""Generate city hub landing pages — e.g. /texas/dallas/"""
from __future__ import annotations

from pathlib import Path

from brand import COPYRIGHT_LINE, LOGO_ARIA_HOME, LOGO_HTML, SITE_NAME, SITE_ORIGIN
from cities_config import POPULAR_CITIES
from cost_engine import (
    PERMIT_FAQ,
    ROOFING_FAQ,
    SOLAR_FAQ,
    city_faq_ranges,
    city_snapshots,
    example_mid,
    fmt_money,
)
from geo_paths import resolve_city_landing, suburb_calculator_href
from local_seo_content import get_city_local_seo, local_guide_section_html
from trust_content import trust_callout_html

ROOT = Path(__file__).resolve().parents[1]

ICONS = {
    "roof": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75"><path d="M3 12 L12 4 L21 12"/><path d="M6 12v8h12v-8"/></svg>',
    "bath": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75"><rect x="4" y="10" width="16" height="10" rx="1"/><path d="M8 10V7a4 4 0 018 0v3"/></svg>',
    "hvac": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75"><rect x="3" y="9" width="18" height="10" rx="2"/><circle cx="12" cy="6" r="2.5"/></svg>',
    "floor": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75"><path d="M4 18h16M6 14h3M11 14h3M16 14h2"/></svg>',
    "fence": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75"><path d="M4 6v14M8 6v14M12 6v14M16 6v14M20 6v14M3 10h18"/></svg>',
    "solar": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41"/></svg>',
}

CAT_ICONS = {
    "Roofing": "roof",
    "Remodeling": "bath",
    "HVAC": "hvac",
    "Flooring": "floor",
    "Outdoor": "fence",
    "Energy": "solar",
}


def lh(path: str, prefix: str, state_slug: str) -> str:
    """Prefix internal paths with /texas/dallas/ for city hub links."""
    if not path or path[0] != "/":
        return path
    if path.startswith("#") or path in ("/", "/privacy/", "/terms/"):
        return path
    if path.startswith(f"/{state_slug}/"):
        return path
    return prefix.rstrip("/") + path


def render(m: dict) -> str:
    city = m["city_name"]
    st = m["state_name"]
    abbr = m["state_abbr"]
    state_slug = m["state_slug"]
    prefix = f"/{state_slug}/{m['slug']}"
    L = lambda p: lh(p, prefix, state_slug)
    title = f"Home Project Costs in {city}, {abbr}"
    city_key = m["city_key"]
    snapshot_rows = city_snapshots(city_key)
    faq = city_faq_ranges(city_key)
    permit_faq = PERMIT_FAQ.get(state_slug, PERMIT_FAQ["texas"])
    roofing_faq = ROOFING_FAQ.get(state_slug, ROOFING_FAQ["texas"])
    solar_faq = SOLAR_FAQ.get(state_slug, SOLAR_FAQ["texas"]).format(
        solar_href=L("/solar-panel-cost-calculator/")
    )
    snapshots = "".join(
        f"""          <a href="{L(s['href'])}" class="city-snapshot-card city-snapshot-card--{s['icon']}">
            <span class="city-snapshot-icon" aria-hidden="true">{ICONS[s['icon']]}</span>
            <span class="city-snapshot-category">{s['category']}</span>
            <h3 class="city-snapshot-title">{s['title']}</h3>
            <p class="city-snapshot-range">{s['range']}</p>
            <span class="city-snapshot-cta">View costs →</span>
          </a>\n"""
        for s in snapshot_rows
    )
    cats = ""
    for cat in m["categories"]:
        icon = CAT_ICONS.get(cat["name"], "roof")
        links = "".join(
            f'<li><a href="{L(href)}">{label}</a></li>' for label, href in cat["links"]
        )
        cats += f"""          <article class="city-category-card city-category-card--{icon}">
            <span class="city-category-icon" aria-hidden="true">{ICONS[icon]}</span>
            <h3>{cat['name']}</h3>
            <ul class="city-category-links">{links}</ul>
            <a href="{L(cat['links'][0][1])}" class="city-category-cta">Explore {cat['name'].lower()} →</a>
          </article>\n"""
    trending = "".join(
        f"""          <a href="{L(href)}" class="city-trend-card">
            <h3>{t}</h3>
            <p>{desc}</p>
            <span class="card-cta">Learn more →</span>
          </a>\n"""
        for t, desc, href in m["trending"]
    )
    home_types = "".join(
        f"""          <article class="city-home-type-card">
            <h3>{name}</h3>
            <p>{desc}</p>
            <p class="city-home-type-budget"><strong>{budget}</strong></p>
          </article>\n"""
        for name, desc, budget in m["home_types"]
    )
    hub_slug = m["slug"]
    suburbs = "".join(
        f'          <a href="{suburb_calculator_href(state_slug, hub_slug, slug)}" class="city-suburb-card"><span>{name}</span><span class="city-suburb-cta">View costs →</span></a>\n'
        for name, slug in m["suburbs"]
    )
    budgets = ""
    for label, items, href in m["budgets"]:
        items_html = "".join(f"<li>{i}</li>" for i in items)
        budgets += f"""          <a href="{L(href)}" class="city-budget-card">
            <h3>{label}</h3>
            <ul>{items_html}</ul>
            <span class="card-cta">Browse projects →</span>
          </a>\n"""
    examples = "".join(
        f"""          <a href="{L(href)}" class="data-card data-card--inline">
            <h3>{loc}</h3>
            <p>{detail}</p>
            <p class="data-total">Final cost: <strong>{fmt_money(example_mid(city_key, href, detail))}</strong></p>
            <span class="card-cta">View guide →</span>
          </a>\n"""
        for loc, detail, _cost, href in m["examples"]
    )
    nearby_cities = "".join(
        f'<a href="{resolve_city_landing(state_slug, slug)}">{name}</a>'
        for name, slug in m["nearby_cities"]
    )
    nearby_suburbs = "".join(
        f'<a href="{suburb_calculator_href(state_slug, hub_slug, slug)}">{name}</a>'
        for name, slug in m["nearby_suburbs"]
    )
    local_seo = get_city_local_seo(city_key)
    local_guide = local_guide_section_html(
        city,
        local_seo,
        city_key=city_key,
        link_fn=L,
        trending=m["trending"],
    )
    collage = "".join(
        f'<div class="city-collage-item city-collage-item--{s["icon"]}" aria-hidden="true">{ICONS[s["icon"]]}</div>'
        for s in snapshot_rows[:6]
    )
    footer_suburb_links = "".join(
        f'          <li><a href="{suburb_calculator_href(state_slug, hub_slug, slug)}">{name}</a></li>\n'
        for name, slug in m.get("footer_suburbs", m["suburbs"][:3])
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — Local Remodeling &amp; Repair Costs | {SITE_NAME}</title>
  <meta name="description" content="Explore home project costs in {city}, {abbr}: roofing, HVAC, kitchen &amp; bath remodels, flooring, fencing, and solar. Local price ranges and free calculators for {city}-area homeowners.">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{m['canonical']}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="Local home improvement costs and calculators for {city}, {st}.">
  <meta property="og:url" content="{m['canonical']}">
  <meta name="theme-color" content="#1a3d36">
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect fill='%231a3d36' width='32' height='32' rx='6'/><path fill='%23e8a87c' d='M6 18 L16 8 L26 18 V26 H6 Z'/><rect fill='%23faf8f5' x='13' y='20' width='6' height='6'/></svg>">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700&family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/css/styles.css">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "WebPage",
    "name": "{title}",
    "url": "{m['canonical']}",
    "description": "Local home project costs in {city}, {abbr}.",
    "breadcrumb": {{
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{"@type": "ListItem", "position": 1, "name": "Home", "item": "{SITE_ORIGIN}/"}},
        {{"@type": "ListItem", "position": 2, "name": "{st}", "item": "{SITE_ORIGIN}/{state_slug}/"}},
        {{"@type": "ListItem", "position": 3, "name": "{city}", "item": "{m['canonical']}"}}
      ]
    }}
  }}
  </script>
</head>
<body class="city-hub-page city-hub-page--{m['slug']}">
  <a class="skip-link" href="#main">Skip to main content</a>
  <header class="site-header" role="banner">
    <div class="header-inner">
      <a href="/" class="logo" aria-label="{LOGO_ARIA_HOME}">
        <svg class="logo-mark" width="32" height="32" viewBox="0 0 32 32" aria-hidden="true"><rect fill="currentColor" width="32" height="32" rx="8"/><path fill="#e8a87c" d="M6 18 L16 8 L26 18 V26 H6 Z"/><rect fill="#faf8f5" x="13" y="20" width="6" height="6" rx="1"/></svg>
        <span class="logo-text">{LOGO_HTML}</span>
      </a>
      <nav class="nav-primary" aria-label="Main navigation">
        <ul>
          <li><a href="/#projects">Projects</a></li>
          <li><a href="#categories">Categories</a></li>
          <li><a href="#local-guide">Local guide</a></li>
          <li><a href="#suburbs">Suburbs</a></li>
          <li><a href="#faq">FAQ</a></li>
        </ul>
      </nav>
      <button type="button" class="nav-toggle" aria-expanded="false" aria-controls="mobile-nav" aria-label="Open menu"><span></span><span></span><span></span></button>
    </div>
    <nav id="mobile-nav" class="mobile-nav" aria-label="Mobile navigation" hidden>
      <ul>
        <li><a href="/#projects">Projects</a></li>
        <li><a href="#categories">Categories</a></li>
        <li><a href="#suburbs">Suburbs</a></li>
        <li><a href="#faq">FAQ</a></li>
      </ul>
    </nav>
  </header>

  <main id="main">
    <!-- 1. Hero -->
    <section id="hero" class="city-hero" aria-labelledby="city-hero-heading">
      <div class="city-hero-bg" aria-hidden="true"></div>
      <div class="container">
        <nav class="breadcrumb" aria-label="Breadcrumb">
          <ol>
            <li><a href="/">Home</a></li>
            <li><a href="/{state_slug}/">{st}</a></li>
            <li aria-current="page">{city}, {abbr}</li>
          </ol>
        </nav>
        <div class="city-hero-grid">
          <div class="city-hero-copy">
            <p class="hero-eyebrow">Local homeowner hub · Updated 2026</p>
            <h1 id="city-hero-heading">Home Project Costs in {city}, {abbr}</h1>
            <p class="city-hero-lead">
              Explore local costs for remodeling, roofing, HVAC, flooring, fencing, solar, and other home improvement projects in the {city} area.
            </p>
            <a href="#calculators" class="btn btn-primary btn-lg">Explore Cost Calculators</a>
          </div>
          <aside class="city-hero-visual" aria-label="{city} home projects">
            <div class="city-collage">{collage}</div>
            <p class="city-hero-visual-caption">Your local dashboard for {city}-area home projects</p>
          </aside>
        </div>
      </div>
    </section>

    <!-- 2. Quick snapshot -->
    <section id="snapshot" class="section city-snapshot-section" aria-labelledby="snapshot-heading">
      <div class="container">
        <header class="section-header section-header--center">
          <h2 id="snapshot-heading">Quick Local Cost Snapshot</h2>
          <p>Typical installed price ranges for popular projects in {city}</p>
        </header>
        <div class="city-snapshot-grid">{snapshots}        </div>
      </div>
    </section>

    <!-- 3. Categories -->
    <section id="categories" class="section city-categories-section" aria-labelledby="categories-heading">
      <div class="container">
        <header class="section-header section-header--center">
          <h2 id="categories-heading">Explore Projects by Category</h2>
          <p>Browse remodeling, roofing, HVAC, flooring, outdoor, and energy projects</p>
        </header>
        <div class="city-category-grid">{cats}        </div>
      </div>
    </section>

    <!-- 4. Local cost guide (labor, permits, climate, projects, drivers) -->
{local_guide}

    <!-- 5. Market snapshot callout -->
    <section id="insights" class="section cost-detail-section" aria-labelledby="insights-heading">
      <div class="container cost-detail-grid">
        <div class="cost-detail-copy">
          <h2 id="insights-heading">Local Market Insights — {city}</h2>
          <p class="city-insight-lead">{m['market_insight']}</p>
          <ul class="cost-detail-list">{''.join(f'<li>{b}</li>' for b in m['market_bullets'])}</ul>
        </div>
        <div class="city-insight-callout">
          <p>{m['metro_callout']}</p>
        </div>
      </div>
    </section>

    <!-- 6. Popular projects -->
    <section id="popular" class="section related-section" aria-labelledby="popular-heading">
      <div class="container">
        <header class="section-header section-header--center">
          <h2 id="popular-heading">Popular Projects in {city}</h2>
        </header>
        <div class="city-trend-grid">{trending}        </div>
      </div>
    </section>

    <!-- 7. Home types -->
    <section id="home-types" class="section city-home-types-section" aria-labelledby="home-types-heading">
      <div class="container">
        <header class="section-header section-header--center">
          <h2 id="home-types-heading">Cost by Home Type</h2>
          <p>Common projects and typical budgets by housing style in the {city} area</p>
        </header>
        <div class="city-home-type-grid">{home_types}        </div>
      </div>
    </section>

    <!-- 8. Suburbs -->
    <section id="suburbs" class="section city-suburbs-section" aria-labelledby="suburbs-heading">
      <div class="container">
        <header class="section-header section-header--center">
          <h2 id="suburbs-heading">Neighborhoods &amp; Suburbs</h2>
          <p>Explore costs in popular {city}-area communities</p>
        </header>
        <div class="city-suburb-grid">{suburbs}        </div>
      </div>
    </section>

    <!-- 9. Budget -->
    <section id="budget" class="section city-budget-section" aria-labelledby="budget-heading">
      <div class="container">
        <header class="section-header section-header--center">
          <h2 id="budget-heading">Projects by Budget</h2>
        </header>
        <div class="city-budget-grid">{budgets}        </div>
      </div>
    </section>

    <!-- 10. Examples -->
    <section id="examples" class="section related-section" aria-labelledby="examples-heading">
      <div class="container">
        <header class="section-header section-header--center">
          <h2 id="examples-heading">Real Local Project Examples</h2>
          <p>Reported costs from completed jobs near {city}</p>
        </header>
        <div class="related-grid">{examples}        </div>
      </div>
    </section>

    <!-- 11. FAQ -->
{trust_callout_html()}
    <section id="faq" class="section faq-section" aria-labelledby="faq-heading">
      <div class="container faq-container">
        <header class="section-header section-header--center">
          <h2 id="faq-heading">{city} Home Project FAQs</h2>
        </header>
        <div class="faq-list">
          <details class="faq-item" open>
            <summary>How much do home renovations cost in {city}?</summary>
            <p>Most {city}-area renovations range from <strong>{faq['renovation']}+</strong> depending on scope. Bathrooms often run <strong>{faq['bathroom']}</strong>, kitchens <strong>{faq['kitchen']}</strong>, and roofing <strong>{faq['roofing']}</strong> for typical homes.</p>
          </details>
          <details class="faq-item">
            <summary>What home projects add the most value?</summary>
            <p>In the {city} market, <strong>kitchen remodels</strong>, <strong>roof replacement</strong>, and <strong>energy-efficient HVAC</strong> commonly deliver strong resale appeal.</p>
          </details>
          <details class="faq-item">
            <summary>What permits are common in {city}?</summary>
            <p>{permit_faq}</p>
          </details>
          <details class="faq-item">
            <summary>Are solar panels worth it in {st}?</summary>
            <p>{solar_faq}</p>
          </details>
          <details class="faq-item">
            <summary>What roofing materials work best in {city}?</summary>
            <p>{roofing_faq}</p>
          </details>
        </div>
      </div>
    </section>

    <!-- 13. Related cities -->
    <section id="related-cities" class="section related-section" aria-labelledby="related-cities-heading">
      <div class="container">
        <header class="section-header section-header--center">
          <h2 id="related-cities-heading">Related City Links</h2>
        </header>
        <div class="city-related-columns">
          <div>
            <h3>Nearby cities</h3>
            <nav class="related-links">{nearby_cities}</nav>
          </div>
          <div>
            <h3>Nearby suburbs</h3>
            <nav class="related-links">{nearby_suburbs}</nav>
          </div>
        </div>
      </div>
    </section>

    <!-- 14. Final CTA -->
    <section id="calculators" class="section cta-banner-section" aria-labelledby="final-cta-heading">
      <div class="container cta-banner-inner">
        <h2 id="final-cta-heading">Explore Home Project Costs in {city}</h2>
        <p>Use free calculators tuned to {st} labor, materials, and typical project sizes.</p>
        <a href="#calculators" class="btn btn-primary btn-lg">Browse Cost Calculators</a>
      </div>
    </section>
  </main>

  <footer class="site-footer" role="contentinfo">
    <div class="container footer-grid">
      <div class="footer-brand">
        <a href="/" class="logo logo--footer"><span class="logo-text">{LOGO_HTML}</span></a>
        <p>Real home project costs in {city} and across the United States.</p>
      </div>
      <nav aria-labelledby="footer-calc">
        <h3 id="footer-calc">Calculators</h3>
        <ul>
          <li><a href="{L('/roof-cost-calculator/')}">Roof Calculator</a></li>
          <li><a href="{L('/hvac-cost-calculator/')}">HVAC Calculator</a></li>
          <li><a href="{L('/solar-panel-cost-calculator/')}">Solar Calculator</a></li>
        </ul>
      </nav>
      <nav aria-labelledby="footer-areas">
        <h3 id="footer-areas">{city} area</h3>
        <ul>
{footer_suburb_links}        </ul>
      </nav>
    </div>
    <div class="footer-bottom">
      <div class="container footer-bottom-inner">
        <p>{COPYRIGHT_LINE}</p>
        <ul class="footer-legal">
          <li><a href="/methodology/">Methodology</a></li>
          <li><a href="/data-sources/">Data Sources</a></li>
          <li><a href="/privacy/">Privacy</a></li>
          <li><a href="/terms/">Terms</a></li>
        </ul>
      </div>
    </div>
  </footer>
  <script src="/js/city-path.js"></script>
  <script src="/js/main.js" defer></script>
</body>
</html>
"""


def main() -> None:
    for m in POPULAR_CITIES:
        out = ROOT / m["state_slug"] / m["slug"] / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render(m), encoding="utf-8")
        print(f"Wrote {out}")


if __name__ == "__main__":
    main()

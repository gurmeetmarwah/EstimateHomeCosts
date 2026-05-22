#!/usr/bin/env python3
"""Generate state hub landing pages — e.g. /texas/, /florida/"""
from __future__ import annotations

import re
from pathlib import Path

from brand import COPYRIGHT_LINE, LOGO_ARIA_HOME, LOGO_HTML, SITE_NAME, SITE_ORIGIN
from geo_paths import resolve_city_landing
from states_config import ALL_STATES, POPULAR_STATE_SLUGS

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

CITY_SLUGS = frozenset({
    "dallas", "austin", "houston", "san-antonio", "fort-worth", "plano", "frisco",
    "phoenix", "scottsdale", "mesa", "chandler", "tucson", "tempe", "gilbert", "glendale",
    "tampa", "orlando", "miami", "jacksonville", "st-petersburg", "clearwater", "brandon",
    "raleigh", "charlotte", "durham", "cary", "apex", "wilmington", "greensboro",
    "san-diego", "los-angeles", "orange-county", "sacramento", "san-francisco",
    "mckinney", "irving", "garland", "round-rock", "riverview", "wesley-chapel",
})


def _is_city_scoped_path(path: str) -> bool:
    parts = [p for p in path.split("/") if p]
    return len(parts) >= 2 and parts[0] in POPULAR_STATE_SLUGS and parts[1] in CITY_SLUGS


def sp(path: str, slug: str) -> str:
    if not path or path[0] != "/":
        return path
    if path.startswith(f"/{slug}/") or path.startswith("#"):
        return path
    if _is_city_scoped_path(path):
        return path
    if path.startswith("/locations/"):
        return path
    return f"/{slug}{path}"


def render(cfg: dict) -> str:
    st = cfg["state_name"]
    slug = cfg["slug"]
    title = f"Home Project Costs in {st}"
    L = lambda p: sp(p, slug)

    snapshots = "".join(
        f"""          <a href="{L(s['href'])}" class="city-snapshot-card city-snapshot-card--{s['icon']}">
            <span class="city-snapshot-icon" aria-hidden="true">{ICONS[s['icon']]}</span>
            <span class="city-snapshot-category">{s['category']}</span>
            <h3 class="city-snapshot-title">{s['title']}</h3>
            <p class="city-snapshot-range">{s['range']}</p>
            <span class="city-snapshot-cta">View costs →</span>
          </a>\n"""
        for s in cfg["snapshots"]
    )

    cats = ""
    for cat in cfg["categories"]:
        icon = CAT_ICONS.get(cat["name"], "roof")
        links = "".join(f'<li><a href="{L(href)}">{label}</a></li>' for label, href in cat["links"])
        cats += f"""          <article class="city-category-card city-category-card--{icon}">
            <span class="city-category-icon" aria-hidden="true">{ICONS[icon]}</span>
            <h3>{cat['name']}</h3>
            <p class="state-category-price">{cat['price']}</p>
            <ul class="city-category-links">{links}</ul>
            <a href="{L(cat['links'][0][1])}" class="city-category-cta">Explore {cat['name'].lower()} →</a>
          </article>\n"""

    major_cities = "".join(
        f"""          <a href="{resolve_city_landing(slug, city_slug)}" class="state-city-card">
            <h3>{name}</h3>
            <p>{tagline}</p>
            <span class="state-city-cta">Explore {name} costs →</span>
          </a>\n"""
        for name, city_slug, tagline in cfg["major_cities"]
    )

    trends = "".join(
        f"""          <article class="state-trend-card">
            <h3>{t}</h3>
            <p>{desc}</p>
          </article>\n"""
        for t, desc in cfg["homeowner_trends"]
    )

    climate = "".join(
        f"""          <article class="state-climate-card">
            <h3>{t}</h3>
            <p>{desc}</p>
          </article>\n"""
        for t, desc in cfg["climate_cards"]
    )

    popular = "".join(
        f"""          <a href="{L(href)}" class="city-trend-card">
            <h3>{t}</h3>
            <p>{desc}</p>
            <span class="card-cta">Learn more →</span>
          </a>\n"""
        for t, desc, href in cfg["trending"]
    )

    regions = "".join(
        f"""          <a href="{L(href) if not href.startswith(f'/{slug}/') else href}" class="state-region-card">
            <h3>{name}</h3>
            <p>{desc}</p>
            <span class="card-cta">View region →</span>
          </a>\n"""
        for name, desc, href in cfg["regions"]
    )

    budgets = ""
    for label, items, href in cfg["budgets"]:
        items_html = "".join(f"<li>{i}</li>" for i in items)
        budgets += f"""          <a href="{L(href)}" class="city-budget-card">
            <h3>{label}</h3>
            <ul>{items_html}</ul>
            <span class="card-cta">Browse projects →</span>
          </a>\n"""

    examples = "".join(
        f"""          <a href="{L(href) if not href.startswith(f'/{slug}/') else href}" class="data-card data-card--inline">
            <h3>{loc}</h3>
            <p>{detail}</p>
            <p class="data-total">Final cost: <strong>{cost}</strong></p>
            <span class="card-cta">View guide →</span>
          </a>\n"""
        for loc, detail, cost, href in cfg["examples"]
    )

    home_styles = "".join(
        f"""          <article class="city-home-type-card">
            <h3>{name}</h3>
            <p>{desc}</p>
            <p class="city-home-type-budget"><strong>{budget}</strong></p>
          </article>\n"""
        for name, desc, budget in cfg["home_styles"]
    )

    faqs = ""
    for i, (q, a) in enumerate(cfg["faqs"]):
        open_attr = " open" if i == 0 else ""
        answer = (
            a.replace("__SOLAR_CALC__", L("/solar-panel-cost-calculator/"))
            .replace("__HVAC_CALC__", L("/hvac-cost-calculator/"))
        )
        faqs += f"""          <details class="faq-item"{open_attr}>
            <summary>{q}</summary>
            <p>{answer}</p>
          </details>\n"""

    related_states = "".join(f'<a href="{href}">{name}</a>' for name, href in cfg["related_states"])
    city_hub_links = "".join(f'<li><a href="{href}">{name}</a></li>\n' for name, href in cfg["city_hubs"])

    collage = "".join(
        f'<div class="city-collage-item city-collage-item--{s["icon"]}" aria-hidden="true">{ICONS[s["icon"]]}</div>'
        for s in cfg["snapshots"][:6]
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — Statewide Remodeling &amp; Repair Costs | {SITE_NAME}</title>
  <meta name="description" content="Explore home project costs across {st}: roofing, HVAC, remodeling, flooring, fencing, and solar. Major city guides, regional trends, and free calculators for {st} homeowners.">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{cfg['canonical']}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="Statewide home improvement costs and calculators for {st} homeowners.">
  <meta property="og:url" content="{cfg['canonical']}">
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
    "url": "{cfg['canonical']}",
    "description": "Statewide home project costs in {st}.",
    "breadcrumb": {{
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{"@type": "ListItem", "position": 1, "name": "Home", "item": "{SITE_ORIGIN}/"}},
        {{"@type": "ListItem", "position": 2, "name": "{st}", "item": "{cfg['canonical']}"}}
      ]
    }}
  }}
  </script>
</head>
<body class="state-hub-page state-hub-page--{slug} city-hub-page">
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
          <li><a href="#cities">Cities</a></li>
          <li><a href="#faq">FAQ</a></li>
        </ul>
      </nav>
      <button type="button" class="nav-toggle" aria-expanded="false" aria-controls="mobile-nav" aria-label="Open menu"><span></span><span></span><span></span></button>
    </div>
    <nav id="mobile-nav" class="mobile-nav" aria-label="Mobile navigation" hidden>
      <ul>
        <li><a href="/#projects">Projects</a></li>
        <li><a href="#categories">Categories</a></li>
        <li><a href="#cities">Cities</a></li>
        <li><a href="#faq">FAQ</a></li>
      </ul>
    </nav>
  </header>

  <main id="main">
    <section id="hero" class="city-hero" aria-labelledby="state-hero-heading">
      <div class="city-hero-bg" aria-hidden="true"></div>
      <div class="container">
        <nav class="breadcrumb" aria-label="Breadcrumb">
          <ol>
            <li><a href="/">Home</a></li>
            <li aria-current="page">{st}</li>
          </ol>
        </nav>
        <div class="city-hero-grid">
          <div class="city-hero-copy">
            <p class="hero-eyebrow">Statewide homeowner hub · Updated 2026</p>
            <h1 id="state-hero-heading">Home Project Costs in {st}</h1>
            <p class="city-hero-lead">
              Explore local pricing for roofing, remodeling, HVAC, flooring, fencing, solar, and other home improvement projects across {st} cities.
            </p>
            <a href="#categories" class="btn btn-primary btn-lg">Explore Cost Calculators</a>
          </div>
          <aside class="city-hero-visual" aria-label="{st} home projects">
            <div class="city-collage">{collage}</div>
            <p class="city-hero-visual-caption">Your statewide planning portal for {st} home projects</p>
          </aside>
        </div>
      </div>
    </section>

    <section id="snapshot" class="section city-snapshot-section" aria-labelledby="snapshot-heading">
      <div class="container">
        <header class="section-header section-header--center">
          <h2 id="snapshot-heading">{st} State Cost Snapshot</h2>
          <p>Typical installed price ranges for popular projects statewide</p>
        </header>
        <div class="city-snapshot-grid">{snapshots}        </div>
      </div>
    </section>

    <section id="categories" class="section city-categories-section" aria-labelledby="categories-heading">
      <div class="container">
        <header class="section-header section-header--center">
          <h2 id="categories-heading">Explore Projects by Category</h2>
          <p>Browse remodeling, roofing, HVAC, flooring, outdoor, and energy projects across {st}</p>
        </header>
        <div class="city-category-grid">{cats}        </div>
      </div>
    </section>

    <section id="cities" class="section state-cities-section" aria-labelledby="cities-heading">
      <div class="container">
        <header class="section-header section-header--center">
          <h2 id="cities-heading">Major {st} Cities</h2>
          <p>Explore local costs, trends, and calculators in top metros</p>
        </header>
        <div class="state-cities-grid">{major_cities}        </div>
      </div>
    </section>

    <section id="trends" class="section state-trends-section" aria-labelledby="trends-heading">
      <div class="container">
        <header class="section-header section-header--center">
          <h2 id="trends-heading">{st} Homeowner Trends</h2>
          <p>What drives remodeling and repair demand across the state</p>
        </header>
        <div class="state-trends-grid">{trends}        </div>
      </div>
    </section>

    <section id="climate" class="section state-climate-section" aria-labelledby="climate-heading">
      <div class="container">
        <header class="section-header section-header--center">
          <h2 id="climate-heading">Climate &amp; Weather Impacts</h2>
          <p>How {st} weather shapes home project priorities and costs</p>
        </header>
        <div class="state-climate-grid">{climate}        </div>
      </div>
    </section>

    <section id="popular" class="section related-section" aria-labelledby="popular-heading">
      <div class="container">
        <header class="section-header section-header--center">
          <h2 id="popular-heading">Popular Projects in {st}</h2>
        </header>
        <div class="city-trend-grid state-trend-grid--5">{popular}        </div>
      </div>
    </section>

    <section id="regions" class="section state-regions-section" aria-labelledby="regions-heading">
      <div class="container">
        <header class="section-header section-header--center">
          <h2 id="regions-heading">Cost by Region</h2>
          <p>Regional differences across {st} metros</p>
        </header>
        <div class="state-regions-grid">{regions}        </div>
      </div>
    </section>

    <section id="budget" class="section city-budget-section" aria-labelledby="budget-heading">
      <div class="container">
        <header class="section-header section-header--center">
          <h2 id="budget-heading">Projects by Budget</h2>
        </header>
        <div class="city-budget-grid">{budgets}        </div>
      </div>
    </section>

    <section id="examples" class="section related-section" aria-labelledby="examples-heading">
      <div class="container">
        <header class="section-header section-header--center">
          <h2 id="examples-heading">Real {st} Project Examples</h2>
          <p>Reported costs from completed jobs across the state</p>
        </header>
        <div class="related-grid">{examples}        </div>
      </div>
    </section>

    <section id="home-styles" class="section city-home-types-section" aria-labelledby="home-styles-heading">
      <div class="container">
        <header class="section-header section-header--center">
          <h2 id="home-styles-heading">{st} Home Styles</h2>
          <p>Common projects and typical upgrades by housing style</p>
        </header>
        <div class="city-home-type-grid">{home_styles}        </div>
      </div>
    </section>

    <section id="faq" class="section faq-section" aria-labelledby="faq-heading">
      <div class="container faq-container">
        <header class="section-header section-header--center">
          <h2 id="faq-heading">{st} Home Project FAQs</h2>
        </header>
        <div class="faq-list">{faqs}        </div>
      </div>
    </section>

    <section id="related-states" class="section related-section" aria-labelledby="related-states-heading">
      <div class="container">
        <header class="section-header section-header--center">
          <h2 id="related-states-heading">Related States &amp; Regions</h2>
        </header>
        <nav class="state-related-nav related-links">{related_states}</nav>
      </div>
    </section>

    <section id="calculators" class="section cta-banner-section" aria-labelledby="final-cta-heading">
      <div class="container cta-banner-inner">
        <h2 id="final-cta-heading">Explore Home Project Costs Across {st}</h2>
        <p>Use free calculators tuned to {st} labor, materials, and typical project sizes.</p>
        <a href="/#calculators" class="btn btn-primary btn-lg">Browse Cost Calculators</a>
      </div>
    </section>
  </main>

  <footer class="site-footer" role="contentinfo">
    <div class="container footer-grid">
      <div class="footer-brand">
        <a href="/" class="logo logo--footer"><span class="logo-text">{LOGO_HTML}</span></a>
        <p>Real home project costs in {st} and across the United States.</p>
      </div>
      <nav aria-labelledby="footer-calc">
        <h3 id="footer-calc">Calculators</h3>
        <ul>
          <li><a href="{L('/roof-cost-calculator/')}">Roof Calculator</a></li>
          <li><a href="{L('/hvac-cost-calculator/')}">HVAC Calculator</a></li>
          <li><a href="{L('/solar-panel-cost-calculator/')}">Solar Calculator</a></li>
        </ul>
      </nav>
      <nav aria-labelledby="footer-cities">
        <h3 id="footer-cities">{st} cities</h3>
        <ul>{city_hub_links}        </ul>
      </nav>
    </div>
    <div class="footer-bottom">
      <div class="container footer-bottom-inner">
        <p>{COPYRIGHT_LINE}</p>
        <ul class="footer-legal">
          <li><a href="/privacy/">Privacy</a></li>
          <li><a href="/terms/">Terms</a></li>
        </ul>
      </div>
    </div>
  </footer>
  <script src="/js/main.js" defer></script>
</body>
</html>
"""


def main() -> None:
    for cfg in ALL_STATES:
        out = ROOT / cfg["slug"] / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render(cfg), encoding="utf-8")
        print(f"Wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

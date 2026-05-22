#!/usr/bin/env python3
"""Generate fence material landing pages (vinyl, composite, chain link, aluminum)."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "fence-materials"

CITY_OPTS = """                  <option value="national" selected>National average</option>
                  <option value="dallas">Dallas, TX</option>
                  <option value="phoenix">Phoenix, AZ</option>
                  <option value="austin">Austin, TX</option>
                  <option value="tampa">Tampa, FL</option>
                  <option value="charlotte">Charlotte, NC</option>
                  <option value="raleigh">Raleigh, NC</option>
                  <option value="scottsdale">Scottsdale, AZ</option>
                  <option value="houston">Houston, TX</option>
                  <option value="orlando">Orlando, FL</option>
                  <option value="san-diego">San Diego, CA</option>"""


def variant_cards(material_key: str, variants: list[dict]) -> str:
    cards = []
    for i, v in enumerate(variants):
        active = " fence-variant-card--active" if i == 0 else ""
        checked = " checked" if i == 0 else ""
        cards.append(f"""          <label class="fence-variant-card{active}" data-fence-variant-card="{v['id']}">
            <input type="radio" name="fence_style" value="{v['id']}"{checked}>
            <span class="fence-variant-card-visual fence-variant-card-visual--{v['visual']}" aria-hidden="true"></span>
            <span class="fence-variant-card-tier">{v['tier']}</span>
            <h3>{v['name']}</h3>
            <p>{v['desc']}</p>
            <span class="fence-variant-card-meta">{v['meta']}</span>
          </label>""")
    return "\n".join(cards)


def variant_select_options(variants: list[dict]) -> str:
    return "\n".join(
        f'                <option value="{v["id"]}"{" selected" if i == 0 else ""}>{v["name"]}</option>'
        for i, v in enumerate(variants)
    )


def grade_select_options(grades: list[dict]) -> str:
    return "\n".join(
        f'                <option value="{g["id"]}"{" selected" if i == 0 else ""}>{g["label"]}</option>'
        for i, g in enumerate(grades)
    )


def color_swatches(colors: list[dict]) -> str:
    return "\n".join(
        f"""          <div class="stain-swatch">
            <span class="stain-swatch-color stain-swatch-color--{c['class']}" aria-hidden="true"></span>
            <strong>{c['name']}</strong>
            <span>{c['note']}</span>
          </div>"""
        for c in colors
    )


def faq_items(items: list[dict]) -> str:
    return "\n".join(
        f"""          <details class="faq-item">
            <summary>{q['q']}</summary>
            <p>{q['a']}</p>
          </details>"""
        for q in items
    )


def faq_schema(items: list[dict]) -> str:
    entities = []
    for q in items:
        entities.append(
            """          {
            "@type": "Question",
            "name": """
            + json.dumps(q["q"])
            + """,
            "acceptedAnswer": { "@type": "Answer", "text": """
            + json.dumps(q["a_plain"])
            + """ }
          }"""
        )
    return ",\n".join(entities)


def comparisons_html(links: list[dict]) -> str:
    return "\n".join(
        f"""          <a href="{l['href']}" class="comparison-card">
            <h3>{l['title']}</h3>
            <p>{l['desc']}</p>
            <span class="comparison-card-cta">{l['cta']} →</span>
          </a>"""
        for l in links
    )


def related_links(links: list[str]) -> str:
    return "\n".join(f'          <a href="{h}">{t}</a>' for h, t in links)


def js_config(m: dict) -> str:
    cfg = {
        "baseRate": m["base_rate"],
        "defaultVariant": m["variants"][0]["id"],
        "defaultGrade": m["grades"][0]["id"] if m.get("grades") else None,
        "shortLabel": m["short_label"],
        "variants": {v["id"]: {"mult": v["mult"], "label": v["name"]} for v in m["variants"]},
        "grades": {
            g["id"]: {"mult": g["mult"], "label": g["label"], "life": g["life"], "look": g["look"]}
            for g in m.get("grades", [])
        },
        "regional": m["regional"],
        "homeExamples": m["home_examples"],
    }
    return json.dumps(cfg, indent=2)


def render_page(m: dict) -> str:
    grade_field = ""
    if m.get("grades"):
        grade_field = f"""
              <div class="form-group">
                <label for="fence-material-grade">{m['grade_label']}</label>
                <select id="fence-material-grade" name="fence_grade">
{grade_select_options(m['grades'])}
                </select>
              </div>"""

    grades_section = ""
    if m.get("grades"):
        grades_section = f"""
    <section id="grades" class="section cost-tables-section" aria-labelledby="grades-heading">
      <div class="container">
        <header class="section-header section-header--center">
          <h2 id="grades-heading">{m['grades_heading']}</h2>
          <p>{m['grades_lead']}</p>
        </header>
        <div class="table-wrap">
          <table class="cost-table cost-table--compact">
            <thead>
              <tr>
                <th scope="col">{m['grades_col1']}</th>
                <th scope="col">Cost (installed)</th>
                <th scope="col">Lifespan</th>
                <th scope="col">Best for</th>
              </tr>
            </thead>
            <tbody id="fence-material-grades-tbody"></tbody>
          </table>
        </div>
      </div>
    </section>"""

    nav_extra = '<li><a href="#grades">Options</a></li>' if m.get("grades") else ""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{m['title']}</title>
  <meta name="description" content="{m['description']}">
  <meta name="keywords" content="{m['keywords']}">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="https://estimatehomecosts.com/fence-materials/{m['slug']}/">
  <meta property="og:type" content="article">
  <meta property="og:url" content="https://estimatehomecosts.com/fence-materials/{m['slug']}/">
  <meta property="og:title" content="{m['og_title']}">
  <meta property="og:description" content="{m['og_desc']}">
  <meta property="og:site_name" content="Estimate Home Costs">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{m['og_title']}">
  <meta name="twitter:description" content="{m['twitter_desc']}">
  <meta name="theme-color" content="#1a3d36">
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect fill='%231a3d36' width='32' height='32' rx='6'/><path fill='%23e8a87c' d='M6 18 L16 8 L26 18 V26 H6 Z'/><rect fill='%23faf8f5' x='13' y='20' width='6' height='6'/></svg>">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700&family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/css/styles.css">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@graph": [
      {{
        "@type": "Article",
        "headline": "{m['article_headline']}",
        "url": "https://estimatehomecosts.com/fence-materials/{m['slug']}/",
        "datePublished": "2026-05-01",
        "dateModified": "2026-05-20",
        "author": {{ "@type": "Organization", "name": "Estimate Home Costs" }}
      }},
      {{
        "@type": "BreadcrumbList",
        "itemListElement": [
          {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "https://estimatehomecosts.com/" }},
          {{ "@type": "ListItem", "position": 2, "name": "Fence Cost Calculator", "item": "https://estimatehomecosts.com/fence-cost-calculator/" }},
          {{ "@type": "ListItem", "position": 3, "name": "{m['breadcrumb']}", "item": "https://estimatehomecosts.com/fence-materials/{m['slug']}/" }}
        ]
      }},
      {{
        "@type": "FAQPage",
        "mainEntity": [
{faq_schema(m['faq'])}
        ]
      }}
    ]
  }}
  </script>
</head>
<body class="material-page material-page--{m['body_class']}">
  <a class="skip-link" href="#main">Skip to main content</a>
  <header class="site-header" role="banner">
    <div class="header-inner">
      <a href="/" class="logo" aria-label="Estimate Home Costs — Home">
        <svg class="logo-mark" width="32" height="32" viewBox="0 0 32 32" aria-hidden="true">
          <rect fill="currentColor" width="32" height="32" rx="8"/>
          <path fill="#e8a87c" d="M6 18 L16 8 L26 18 V26 H6 Z"/>
          <rect fill="#faf8f5" x="13" y="20" width="6" height="6" rx="1"/>
        </svg>
        <span class="logo-text">Estimate <strong>Home Costs</strong></span>
      </a>
      <nav class="nav-primary" aria-label="Main navigation">
        <ul>
          <li><a href="#fence-styles">Styles</a></li>
          {nav_extra}
          <li><a href="#calculator">Calculator</a></li>
          <li><a href="#faq">FAQ</a></li>
        </ul>
      </nav>
      <button type="button" class="nav-toggle" aria-expanded="false" aria-controls="mobile-nav" aria-label="Open menu">
        <span></span><span></span><span></span>
      </button>
    </div>
    <nav id="mobile-nav" class="mobile-nav" aria-label="Mobile navigation" hidden>
      <ul>
        <li><a href="#fence-styles">Styles</a></li>
        <li><a href="#calculator">Calculator</a></li>
        <li><a href="#faq">FAQ</a></li>
      </ul>
    </nav>
  </header>

  <main id="main">
    <section id="hero" class="fence-material-hero" aria-labelledby="hero-heading">
      <div class="container">
        <nav class="breadcrumb" aria-label="Breadcrumb">
          <ol>
            <li><a href="/">Home</a></li>
            <li><a href="/fence-cost-calculator/">Fence Calculator</a></li>
            <li aria-current="page">{m['breadcrumb_short']}</li>
          </ol>
        </nav>
        <div class="fence-material-hero-copy">
          <p class="hero-eyebrow">Fence materials by style</p>
          <h1 id="hero-heading">{m['h1']}</h1>
          <p class="fence-material-hero-lead">{m['hero_lead']}</p>
          <p class="fence-material-hero-price">
            <span class="fence-material-hero-price-label">Typical installed range</span>
            <strong id="hero-cost-range">{m['hero_range']}</strong>
            <span class="fence-material-hero-price-note" id="hero-per-ft">{m['hero_per_ft']}</span>
          </p>
          <div class="fence-material-hero-actions">
            <a href="#calculator" class="btn btn-primary btn-lg">{m['hero_cta_primary']}</a>
            <a href="/fence-cost-calculator/?material={m['calc_material']}" class="btn btn-secondary btn-lg">Open Fence Calculator</a>
          </div>
        </div>
      </div>
    </section>

    <section class="material-quick-stats" aria-label="{m['short_label']} at a glance">
      <div class="container">
        <ul class="material-quick-stats-grid">
          <li><span class="material-quick-stats-label">Average cost</span><strong id="stat-avg-cost">{m['stats_cost']}</strong></li>
          <li><span class="material-quick-stats-label">Privacy level</span><strong>{m['stats_privacy']}</strong></li>
          <li><span class="material-quick-stats-label">Lifespan</span><strong>{m['stats_life']}</strong></li>
          <li><span class="material-quick-stats-label">Maintenance</span><strong>{m['stats_maint']}</strong></li>
        </ul>
      </div>
    </section>

    <section id="fence-styles" class="section fence-variant-section" aria-labelledby="fence-styles-heading">
      <div class="container">
        <header class="section-header section-header--center">
          <h2 id="fence-styles-heading">{m['styles_heading']}</h2>
          <p>{m['styles_lead']}</p>
        </header>
        <div class="fence-variant-cards-grid fence-variant-cards-grid--{len(m['variants'])}">
{variant_cards(m['body_class'], m['variants'])}
        </div>
      </div>
    </section>

    <section id="calculator" class="section quick-estimate-section wood-fence-calc-section" aria-labelledby="cost-range-heading">
      <div class="container">
        <header class="section-header section-header--center">
          <h2 id="cost-range-heading">{m['calc_heading']}</h2>
          <p>{m['calc_lead']}</p>
        </header>
        <div class="quick-estimator wood-fence-estimator">
          <form id="fence-material-calc-form" class="quick-estimator-form" novalidate>
            <div class="quick-estimator-fields quick-estimator-fields--fence">
              <div class="form-group">
                <label for="fence-material-length">Fence length</label>
                <div class="quick-input-wrap">
                  <input type="number" id="fence-material-length" min="20" max="1000" step="10" value="150" inputmode="numeric" required>
                  <span class="quick-input-suffix" aria-hidden="true">linear ft</span>
                </div>
              </div>
              <div class="form-group">
                <label for="fence-material-variant">Fence style</label>
                <select id="fence-material-variant" name="fence_variant">
{variant_select_options(m['variants'])}
                </select>
              </div>{grade_field}
              <div class="form-group">
                <label for="fence-material-height">Fence height</label>
                <select id="fence-material-height" name="fence_height">
                  <option value="4">4 ft</option>
                  <option value="6" selected>6 ft</option>
                  <option value="8">8 ft</option>
                </select>
              </div>
              <div class="form-group">
                <label for="fence-material-gates">Gates</label>
                <select id="fence-material-gates" name="fence_gates">
                  <option value="0">None</option>
                  <option value="1" selected>1 gate</option>
                  <option value="2">2 gates</option>
                </select>
              </div>
              <div class="form-group">
                <label for="fence-material-city">City</label>
                <select id="fence-material-city" name="fence_city">
{CITY_OPTS}
                </select>
              </div>
            </div>
            <aside class="quick-estimator-aside" aria-label="Live estimate">
              <div class="quick-estimate-result" aria-live="polite" aria-atomic="true">
                <span class="quick-estimate-live"><span class="quick-estimate-live-dot" aria-hidden="true"></span> Updates live</span>
                <span class="quick-estimate-label">Estimated installation cost</span>
                <p class="quick-estimate-price" id="fence-material-calc-range">{m['calc_default_range']}</p>
                <p class="quick-result-hint" id="fence-material-calc-hint">{m['calc_default_hint']}</p>
                <p class="wood-calc-per-ft" id="fence-material-calc-per-ft">{m['calc_default_per_ft']}</p>
              </div>
              <a href="/fence-cost-calculator/?material={m['calc_material']}" class="btn btn-primary btn-lg btn-block">Open full fence calculator</a>
            </aside>
          </form>
        </div>
        <div class="wood-cost-benchmarks" aria-labelledby="benchmarks-heading">
          <h3 id="benchmarks-heading" class="wood-cost-benchmarks-title">Typical total cost by yard size</h3>
          <p class="wood-cost-benchmarks-lead">Based on your selections above.</p>
          <ul class="wood-cost-benchmarks-grid" id="fence-material-cost-range-list">
            <li class="wood-cost-benchmark-card" data-range-ft="100">
              <span class="wood-cost-benchmark-ft">100 linear ft</span>
              <strong class="wood-cost-benchmark-price">{m['bench_100']}</strong>
              <span class="wood-cost-benchmark-note">Small yard perimeter</span>
            </li>
            <li class="wood-cost-benchmark-card wood-cost-benchmark-card--active" data-range-ft="150">
              <span class="wood-cost-benchmark-ft">150 linear ft</span>
              <strong class="wood-cost-benchmark-price">{m['bench_150']}</strong>
              <span class="wood-cost-benchmark-note">Most suburban backyards</span>
            </li>
            <li class="wood-cost-benchmark-card" data-range-ft="200">
              <span class="wood-cost-benchmark-ft">200 linear ft</span>
              <strong class="wood-cost-benchmark-price">{m['bench_200']}</strong>
              <span class="wood-cost-benchmark-note">Large lot</span>
            </li>
          </ul>
        </div>
        <div class="wood-cost-factors">
          <p class="wood-cost-factors-title">Cost also varies based on</p>
          <ul class="wood-cost-factors-list">
{m['factors_pills']}
          </ul>
        </div>
      </div>
    </section>
{grades_section}
    <section id="pros-cons" class="section pros-cons-section" aria-labelledby="pros-cons-heading">
      <div class="container">
        <h2 id="pros-cons-heading" class="section-header section-header--center">{m['pros_heading']}</h2>
        <div class="pros-cons-grid">
          <div class="pros-cons-col pros-cons-col--pros">
            <h3>Advantages</h3>
            <ul>{m['pros_list']}</ul>
          </div>
          <div class="pros-cons-col pros-cons-col--cons">
            <h3>Disadvantages</h3>
            <ul>{m['cons_list']}</ul>
          </div>
        </div>
      </div>
    </section>

    <section id="benefits" class="section cost-detail-section cost-detail-section--alt" aria-labelledby="benefits-heading">
      <div class="container cost-detail-grid">
        <div class="cost-detail-copy">
          <h2 id="benefits-heading">{m['benefits_heading']}</h2>
          <p>{m['benefits_lead']}</p>
          <ul class="cost-detail-list">{m['benefits_list']}</ul>
        </div>
      </div>
    </section>

    <section id="fence-heights" class="section fence-height-section" aria-labelledby="fence-heights-heading">
      <div class="container">
        <header class="section-header section-header--center">
          <h2 id="fence-heights-heading">{m['heights_heading']}</h2>
        </header>
        <div class="fence-height-grid">
          <article class="fence-height-card">
            <h3>4 ft fence</h3>
            <p class="fence-height-privacy">Privacy: {m['h4_privacy']}</p>
            <ul>{m['h4_list']}</ul>
          </article>
          <article class="fence-height-card fence-height-card--featured">
            <h3>6 ft fence</h3>
            <p class="fence-height-privacy">Privacy: {m['h6_privacy']}</p>
            <ul>{m['h6_list']}</ul>
          </article>
          <article class="fence-height-card">
            <h3>8 ft fence</h3>
            <p class="fence-height-privacy">Privacy: {m['h8_privacy']}</p>
            <ul>{m['h8_list']}</ul>
          </article>
        </div>
      </div>
    </section>

    <section id="colors" class="section stain-section" aria-labelledby="colors-heading">
      <div class="container">
        <header class="section-header section-header--center">
          <h2 id="colors-heading">{m['colors_heading']}</h2>
          <p>{m['colors_lead']}</p>
        </header>
        <div class="stain-swatch-grid">
{color_swatches(m['colors'])}
        </div>
      </div>
    </section>

    <section id="weather" class="section local-factors-section" aria-labelledby="weather-heading">
      <div class="container">
        <header class="section-header section-header--center">
          <h2 id="weather-heading">{m['weather_heading']}</h2>
          <p>Based on the city selected in the calculator above.</p>
        </header>
        <div class="local-factors-grid local-factors-grid--single" id="fence-material-weather-grid">
          <div class="local-factor-card">
            <h3>Climate notes</h3>
            <ul>{m['weather_national']}</ul>
          </div>
          <div class="local-factor-card local-factor-card--selected" id="fence-material-weather-city-card" hidden>
            <h3 id="fence-material-weather-city-title">Your city</h3>
            <ul id="fence-material-weather-city-list"></ul>
          </div>
        </div>
      </div>
    </section>

    <section id="install-factors" class="section cost-detail-section" aria-labelledby="install-factors-heading">
      <div class="container">
        <header class="section-header section-header--center">
          <h2 id="install-factors-heading">{m['install_heading']}</h2>
        </header>
        <div class="install-factors-grid">{m['install_cards']}</div>
      </div>
    </section>

    <section id="comparisons" class="section comparison-cards-section" aria-labelledby="comparisons-heading">
      <div class="container">
        <header class="section-header section-header--center">
          <h2 id="comparisons-heading">{m['compare_heading']}</h2>
        </header>
        <div class="comparison-cards-grid">
{comparisons_html(m['comparisons'])}
        </div>
      </div>
    </section>

    <section id="project-examples" class="section project-examples-section" aria-labelledby="project-examples-heading">
      <div class="container">
        <header class="section-header section-header--center">
          <h2 id="project-examples-heading">{m['projects_heading']}</h2>
          <p>Based on the city selected in the calculator above.</p>
        </header>
        <div class="project-examples-grid project-examples-grid--dual">
          <article class="project-example-card project-example-card--active" data-project-city="national">
            <h3>National average</h3>
            <p class="project-example-type">{m['project_nat_type']}</p>
            <ul>
              <li data-project-detail>{m['project_nat_detail']}</li>
              <li>Final cost: <strong data-project-cost>{m['project_nat_cost']}</strong></li>
            </ul>
          </article>
          <article class="project-example-card" id="fence-material-project-city-card" data-project-city="city" hidden>
            <h3 data-project-city-title>Your city</h3>
            <p class="project-example-type" data-project-type>{m['project_nat_type']}</p>
            <ul>
              <li data-project-detail>Standard install</li>
              <li>Final cost: <strong data-project-cost>—</strong></li>
            </ul>
          </article>
        </div>
      </div>
    </section>

    <section id="faq" class="section faq-section" aria-labelledby="faq-heading">
      <div class="container">
        <header class="section-header section-header--center">
          <h2 id="faq-heading">{m['faq_heading']}</h2>
        </header>
        <div class="faq-list">
{faq_items(m['faq'])}
        </div>
      </div>
    </section>

    <section class="section material-cta-band" aria-labelledby="primary-cta-heading">
      <div class="container material-cta-band-inner">
        <h2 id="primary-cta-heading">{m['cta_heading']}</h2>
        <p>{m['cta_lead']}</p>
        <div class="material-cta-actions">
          <a href="/fence-cost-calculator/?material={m['calc_material']}" class="btn btn-primary btn-lg">Open Fence Calculator</a>
          <a href="#calculator" class="btn btn-secondary btn-lg">Use quick estimator</a>
        </div>
      </div>
    </section>

    <section id="related" class="section related-links-section" aria-labelledby="related-heading">
      <div class="container">
        <h2 id="related-heading" class="section-header section-header--center">Related Fencing Guides</h2>
        <nav class="related-links" aria-label="Related fencing pages">
{related_links(m['related'])}
        </nav>
      </div>
    </section>
  </main>

  <footer class="site-footer" role="contentinfo">
    <div class="container footer-inner">
      <div class="footer-brand">
        <a href="/" class="logo logo--footer"><span class="logo-text">Estimate <strong>Home Costs</strong></span></a>
        <p>Free home improvement cost calculators and localized pricing guides.</p>
      </div>
      <nav class="footer-nav" aria-label="Footer">
        <h2 class="footer-nav-title">Calculators</h2>
        <ul>
          <li><a href="/fence-cost-calculator/">Fence Cost Calculator</a></li>
          <li><a href="/fence-materials/{m['slug']}/">{m['breadcrumb']}</a></li>
        </ul>
      </nav>
    </div>
    <div class="footer-bottom"><div class="container"><p>© 2026 Estimate Home Costs. Estimates are for planning only — not a contractor quote.</p></div></div>
  </footer>

  <script>window.FENCE_MATERIAL_CONFIG = {js_config(m)};</script>
  <script src="/js/calculator-cities.js" defer></script>
  <script src="/js/main.js" defer></script>
  <script src="/js/fence-material-page.js" defer></script>
</body>
</html>
"""


MATERIALS = [
    {
        "slug": "vinyl-fence-cost",
        "calc_material": "vinyl",
        "body_class": "vinyl-fence",
        "base_rate": 32,
        "short_label": "Vinyl",
        "title": "Vinyl Fence Cost (2026) — Privacy & Picket Prices | Estimate Home Costs",
        "description": "Vinyl fence cost $28–$45 per linear foot installed in 2026. Compare privacy panels, picket, and ranch styles with free calculator by city.",
        "keywords": "vinyl fence cost, vinyl privacy fence cost per foot, PVC fence installation cost, white vinyl fence cost",
        "og_title": "Vinyl Fence Cost (2026)",
        "og_desc": "Low-maintenance vinyl fencing — installed costs, styles, colors, and city-level pricing.",
        "twitter_desc": "Estimate vinyl fence installation cost by linear foot, style, and city.",
        "article_headline": "Vinyl Fence Cost (2026): Styles, Colors & Calculator",
        "breadcrumb": "Vinyl Fence Cost",
        "breadcrumb_short": "Vinyl Fence",
        "h1": "Vinyl Fence Cost",
        "hero_lead": "Low-maintenance PVC fencing for privacy and curb appeal — no staining required. Compare vinyl styles and see installed costs before you choose wood or composite.",
        "hero_range": "$4,200–$6,200",
        "hero_per_ft": "$28–$42 per linear ft · 6 ft privacy",
        "hero_cta_primary": "Estimate Vinyl Fence Costs",
        "stats_cost": "$28–$45 per linear ft",
        "stats_privacy": "High",
        "stats_life": "20–30 years",
        "stats_maint": "Low",
        "styles_heading": "Vinyl Fence Styles",
        "styles_lead": "Panel style drives cost, privacy, and neighborhood fit — most suburban installs use 6 ft privacy panels.",
        "variants": [
            {"id": "privacy", "name": "Privacy panel", "mult": 1, "tier": "$$ · Most popular", "desc": "Solid 6 ft panels · full screening", "meta": "Backyard standard", "visual": "vinyl-privacy"},
            {"id": "semi", "name": "Semi-privacy", "mult": 0.94, "tier": "$$ · Balanced", "desc": "Latticed top · airflow", "meta": "HOA-friendly", "visual": "vinyl-semi"},
            {"id": "picket", "name": "Vinyl picket", "mult": 0.88, "tier": "$ · Front yard", "desc": "Classic picket · 4–5 ft", "meta": "Curb appeal", "visual": "vinyl-picket"},
            {"id": "ranch", "name": "Ranch rail", "mult": 0.82, "tier": "$ · Open", "desc": "2–3 rail split look", "meta": "Large lots", "visual": "vinyl-ranch"},
        ],
        "grades": [
            {"id": "standard", "label": "Standard PVC", "mult": 1, "life": "20–25 years", "look": "White or tan"},
            {"id": "premium", "label": "Premium thickness", "mult": 1.1, "life": "25–30 years", "look": "Stiffer panels"},
            {"id": "reinforced", "label": "Reinforced / aluminum insert", "mult": 1.18, "life": "30+ years", "look": "Wind-prone areas"},
        ],
        "grade_label": "Panel grade",
        "grades_heading": "Vinyl Fence Grade Comparison",
        "grades_lead": "Installed cost per linear foot at 6 ft — based on calculator settings above.",
        "grades_col1": "Grade",
        "calc_heading": "Typical Vinyl Fence Cost",
        "calc_lead": "Enter fence length, style, panel grade, and city — estimates update instantly.",
        "calc_default_range": "$4,800–$5,900",
        "calc_default_hint": "150 ft · Privacy panel · Standard PVC",
        "calc_default_per_ft": "$32–$39 per linear ft installed",
        "bench_100": "$3,200–$4,000",
        "bench_150": "$4,800–$5,900",
        "bench_200": "$6,400–$7,800",
        "factors_pills": """            <li>Panel grade</li>
            <li>Height &amp; style</li>
            <li>Gates</li>
            <li>Terrain</li>
            <li>Color &amp; texture</li>""",
        "pros_heading": "Vinyl Fence Pros & Cons",
        "pros_list": """              <li>No painting or staining</li>
              <li>Resists rot, insects, and moisture</li>
              <li>Consistent color for decades</li>
              <li>Easy to clean with hose and soap</li>""",
        "cons_list": """              <li>Higher upfront cost than wood or chain link</li>
              <li>Can crack in extreme cold if impacted</li>
              <li>Limited authentic wood appearance</li>""",
        "benefits_heading": "Why Homeowners Choose Vinyl",
        "benefits_lead": "Vinyl is the go-to choice when you want <strong>privacy without annual maintenance</strong>.",
        "benefits_list": """            <li><strong>Low maintenance</strong> — no stain, seal, or board replacement cycle</li>
            <li><strong>HOA-friendly</strong> — crisp white, tan, and gray palettes</li>
            <li><strong>Pet &amp; kid safe</strong> — smooth surfaces, no splinters</li>
            <li><strong>Moisture proof</strong> — ideal for humid and coastal climates</li>""",
        "heights_heading": "Vinyl Fence Height Options",
        "h4_privacy": "Moderate to high",
        "h4_list": """              <li>Front-yard picket and garden enclosures</li>
              <li>Common HOA front-yard limit</li>""",
        "h6_privacy": "High",
        "h6_list": """              <li>Standard backyard privacy panels</li>
              <li>Most cost-effective vinyl height</li>""",
        "h8_privacy": "Maximum",
        "h8_list": """              <li>Extra screening where codes allow</li>
              <li>Stronger posts and footings required</li>""",
        "colors_heading": "Popular Vinyl Fence Colors",
        "colors_lead": "Color is baked into the material — no repainting required.",
        "colors": [
            {"class": "vinyl-white", "name": "White", "note": "Most common"},
            {"class": "vinyl-tan", "name": "Tan / almond", "note": "Warm neutral"},
            {"class": "vinyl-gray", "name": "Gray", "note": "Modern suburban"},
            {"class": "vinyl-clay", "name": "Clay", "note": "Earth tone"},
        ],
        "weather_heading": "Vinyl Fencing & Climate",
        "weather_national": """              <li><strong>Humid climates:</strong> Excellent — won't rot or warp like wood</li>
              <li><strong>Hot sun:</strong> Choose lighter colors to reduce heat retention</li>
              <li><strong>Cold climates:</strong> Use premium-grade panels for impact resistance</li>""",
        "install_heading": "Vinyl Fence Installation Cost Factors",
        "install_cards": """          <article><h3>Panel style</h3><p>Privacy panels cost more than ranch rail or picket per linear foot.</p></article>
          <article><h3>Gates</h3><p>Vinyl gates need reinforced frames — typically $400–$900+ installed.</p></article>
          <article><h3>Post footings</h3><p>Concrete footings and level string lines are critical for straight panels.</p></article>
          <article><h3>Slope</h3><p>Stepped or racked panels add labor on uneven yards.</p></article>""",
        "compare_heading": "Vinyl vs Other Fence Materials",
        "comparisons": [
            {"href": "/compare/vinyl-vs-wood-fence/", "title": "Vinyl vs Wood Fence", "desc": "Maintenance, lifespan, and installed cost side by side.", "cta": "Read comparison"},
            {"href": "/fence-materials/wood-privacy-fence-cost/", "title": "Wood Privacy Fence Cost", "desc": "Natural cedar and pine privacy pricing.", "cta": "Wood cost guide"},
            {"href": "/fence-materials/composite-fence-cost/", "title": "Composite Fence Cost", "desc": "Wood-grain composite boards vs vinyl PVC.", "cta": "Composite guide"},
        ],
        "projects_heading": "Real Vinyl Fence Projects",
        "project_nat_type": "6 ft vinyl privacy · 150 linear ft",
        "project_nat_detail": "6 ft white privacy · one gate",
        "project_nat_cost": "$5,200",
        "faq_heading": "Vinyl Fence FAQ",
        "faq": [
            {"q": "How much does a vinyl fence cost?", "a": "Vinyl fence installation typically costs <strong>$28–$45 per linear foot</strong> nationally. Use the <a href=\"#calculator\">estimator above</a> for your style and city.", "a_plain": "Vinyl fence installation typically costs $28–$45 per linear foot nationally."},
            {"q": "Is vinyl fencing worth the extra cost vs wood?", "a": "<strong>Yes</strong> if you want minimal maintenance — vinyl avoids staining and rot repair over 20+ years.", "a_plain": "Yes if you want minimal maintenance over 20+ years."},
            {"q": "How long do vinyl fences last?", "a": "Quality vinyl often lasts <strong>20–30 years</strong> with occasional cleaning.", "a_plain": "Quality vinyl often lasts 20–30 years."},
            {"q": "Does vinyl fence fade?", "a": "Modern PVC includes UV inhibitors. Lighter colors may show less fade than dark tones in intense sun.", "a_plain": "Modern PVC includes UV inhibitors; lighter colors fade less in sun."},
        ],
        "cta_heading": "Estimate Vinyl Fence Costs",
        "cta_lead": "Model length, height, and gates on the full fence calculator — vinyl pre-selected.",
        "related": [
            ("/fence-materials/vinyl-fence-cost/", "Vinyl Fence Cost"),
            ("/compare/vinyl-vs-wood-fence/", "Vinyl vs Wood Fence"),
            ("/fence-materials/wood-privacy-fence-cost/", "Wood Privacy Fence Cost"),
            ("/fence-cost-calculator/", "Fence Cost Calculator"),
        ],
        "regional": {
            "national": "Clean panels annually in humid climates to prevent mildew film",
            "dallas": "Intense sun — white and tan colors popular; avoid dark panels on south exposures",
            "phoenix": "Heat expansion gaps matter; install in cooler morning hours when possible",
            "tampa": "Excellent material choice for moisture — rinse panels yearly",
            "houston": "Soil movement — allow proper post depth and concrete cure time",
        },
        "home_examples": {
            "national": {"ft": 150, "height": 6, "variant": "privacy", "grade": "standard", "gates": 1, "detail": "6 ft white privacy · one gate"},
            "dallas": {"ft": 160, "height": 6, "variant": "privacy", "grade": "premium", "gates": 1, "detail": "6 ft tan privacy · reinforced posts"},
            "tampa": {"ft": 140, "height": 6, "variant": "privacy", "grade": "standard", "gates": 1, "detail": "6 ft white · humidity-rated install"},
        },
    },
    {
        "slug": "composite-fence-cost",
        "calc_material": "composite",
        "body_class": "composite-fence",
        "base_rate": 38,
        "short_label": "Composite",
        "title": "Composite Fence Cost (2026) — Installed Prices & Calculator | Estimate Home Costs",
        "description": "Composite fence cost $32–$52 per linear foot installed in 2026. Compare horizontal, privacy, and wood-grain boards with free calculator by city.",
        "keywords": "composite fence cost, composite privacy fence cost per foot, Trex fence cost, wood composite fence installation",
        "og_title": "Composite Fence Cost (2026)",
        "og_desc": "Wood-grain composite fencing — installed costs, styles, and city-level pricing.",
        "twitter_desc": "Estimate composite fence cost by style, grade, and city.",
        "article_headline": "Composite Fence Cost (2026): Styles & Calculator",
        "breadcrumb": "Composite Fence Cost",
        "breadcrumb_short": "Composite Fence",
        "h1": "Composite Fence Cost",
        "hero_lead": "Wood-grain composite boards combine the look of timber with lower maintenance — popular for modern suburban backyards and HOA neighborhoods.",
        "hero_range": "$5,000–$7,500",
        "hero_per_ft": "$32–$48 per linear ft · 6 ft privacy",
        "hero_cta_primary": "Estimate Composite Fence Costs",
        "stats_cost": "$32–$52 per linear ft",
        "stats_privacy": "High",
        "stats_life": "25–30 years",
        "stats_maint": "Very low",
        "styles_heading": "Composite Fence Styles",
        "styles_lead": "Board orientation and profile affect price and curb appeal.",
        "variants": [
            {"id": "privacy", "name": "Vertical privacy", "mult": 1, "tier": "$$ · Standard", "desc": "6 ft tongue-and-groove look", "meta": "Most installs", "visual": "composite-privacy"},
            {"id": "horizontal", "name": "Horizontal slat", "mult": 1.12, "tier": "$$$ · Modern", "desc": "Contemporary lines", "meta": "Designer yards", "visual": "composite-horizontal"},
            {"id": "picket", "name": "Composite picket", "mult": 0.9, "tier": "$$ · Front yard", "desc": "4–5 ft decorative", "meta": "Street-facing", "visual": "composite-picket"},
            {"id": "ranch", "name": "Ranch / estate", "mult": 0.85, "tier": "$ · Open", "desc": "Wide posts & rails", "meta": "Estate lots", "visual": "composite-ranch"},
        ],
        "grades": [
            {"id": "standard", "label": "Standard composite", "mult": 1, "life": "25 years", "look": "Wood grain"},
            {"id": "capped", "label": "Capped composite", "mult": 1.14, "life": "25–30 years", "look": "Better fade resistance"},
            {"id": "premium", "label": "Premium / designer", "mult": 1.25, "life": "30 years", "look": "Multi-tone boards"},
        ],
        "grade_label": "Board grade",
        "grades_heading": "Composite Fence Grade Comparison",
        "grades_lead": "Installed cost per linear foot at 6 ft height.",
        "grades_col1": "Grade",
        "calc_heading": "Typical Composite Fence Cost",
        "calc_lead": "Enter fence length, style, board grade, and city.",
        "calc_default_range": "$5,700–$7,000",
        "calc_default_hint": "150 ft · Vertical privacy · Standard",
        "calc_default_per_ft": "$38–$47 per linear ft installed",
        "bench_100": "$3,800–$4,700",
        "bench_150": "$5,700–$7,000",
        "bench_200": "$7,600–$9,300",
        "factors_pills": """            <li>Board grade</li>
            <li>Style &amp; height</li>
            <li>Gates</li>
            <li>Brand &amp; warranty</li>
            <li>Terrain</li>""",
        "pros_heading": "Composite Fence Pros & Cons",
        "pros_list": """              <li>Wood appearance without annual staining</li>
              <li>Resists rot, insects, and splitting</li>
              <li>Long warranty on premium lines</li>
              <li>Strong HOA and resale appeal</li>""",
        "cons_list": """              <li>Highest upfront cost among common materials</li>
              <li>Can fade slightly over many years in harsh sun</li>
              <li>Not all contractors stock every brand</li>""",
        "benefits_heading": "Why Homeowners Choose Composite",
        "benefits_lead": "Composite bridges the gap between <strong>wood aesthetics and vinyl maintenance</strong>.",
        "benefits_list": """            <li><strong>Curb appeal</strong> — realistic grain and multi-tone boards</li>
            <li><strong>Durability</strong> — no warped pickets or rotting posts</li>
            <li><strong>Privacy</strong> — solid 6 ft systems common</li>
            <li><strong>Value</strong> — lower lifetime cost than repeatedly replacing wood</li>""",
        "heights_heading": "Composite Fence Height Options",
        "h4_privacy": "Moderate",
        "h4_list": """              <li>Decorative front-yard sections</li>""",
        "h6_privacy": "High",
        "h6_list": """              <li>Standard backyard privacy</li>
              <li>Best price-to-privacy ratio</li>""",
        "h8_privacy": "Maximum",
        "h8_list": """              <li>Premium estates and pool enclosures</li>""",
        "colors_heading": "Composite Fence Colors",
        "colors_lead": "Multi-tone boards mimic natural wood variation.",
        "colors": [
            {"class": "composite-walnut", "name": "Walnut", "note": "Most popular"},
            {"class": "composite-gray", "name": "Weathered gray", "note": "Modern"},
            {"class": "composite-teak", "name": "Teak", "note": "Warm brown"},
            {"class": "composite-charcoal", "name": "Charcoal", "note": "Contemporary"},
        ],
        "weather_heading": "Composite Fencing & Climate",
        "weather_national": """              <li><strong>All climates:</strong> Performs well vs wood rot and insect damage</li>
              <li><strong>Desert sun:</strong> Choose capped boards for fade resistance</li>
              <li><strong>Coastal:</strong> Stainless fasteners recommended</li>""",
        "install_heading": "Composite Fence Installation Cost Factors",
        "install_cards": """          <article><h3>Brand &amp; warranty</h3><p>Premium capped boards cost more but include longer fade warranties.</p></article>
          <article><h3>Horizontal install</h3><p>Horizontal layouts need more labor for alignment.</p></article>
          <article><h3>Gates</h3><p>Matching composite gates are often $500–$1,000+.</p></article>
          <article><h3>Posts</h3><p>Some systems use aluminum-reinforced posts for wind.</p></article>""",
        "compare_heading": "Composite vs Other Materials",
        "comparisons": [
            {"href": "/fence-materials/wood-privacy-fence-cost/", "title": "Composite vs Wood", "desc": "Natural wood vs composite maintenance and cost.", "cta": "Wood guide"},
            {"href": "/fence-materials/vinyl-fence-cost/", "title": "Composite vs Vinyl", "desc": "PVC panels vs wood-grain composite.", "cta": "Vinyl guide"},
            {"href": "/fence-cost-calculator/#material-comparison", "title": "All fence materials", "desc": "Compare every material on one calculator.", "cta": "Open calculator"},
        ],
        "projects_heading": "Real Composite Fence Projects",
        "project_nat_type": "6 ft composite privacy · 150 linear ft",
        "project_nat_detail": "6 ft walnut privacy · one gate",
        "project_nat_cost": "$6,400",
        "faq_heading": "Composite Fence FAQ",
        "faq": [
            {"q": "How much does a composite fence cost?", "a": "Composite fencing typically costs <strong>$32–$52 per linear foot</strong> installed. Use the <a href=\"#calculator\">calculator above</a>.", "a_plain": "Composite fencing typically costs $32–$52 per linear foot installed."},
            {"q": "Is composite better than wood?", "a": "Composite costs more upfront but needs far less maintenance — often better lifetime value.", "a_plain": "Composite costs more upfront but needs less maintenance."},
            {"q": "How long does composite fencing last?", "a": "Most systems are rated <strong>25–30 years</strong> with minimal upkeep.", "a_plain": "Most systems last 25–30 years."},
        ],
        "cta_heading": "Estimate Composite Fence Costs",
        "cta_lead": "Full fence calculator with composite pre-selected.",
        "related": [
            ("/fence-materials/composite-fence-cost/", "Composite Fence Cost"),
            ("/fence-materials/wood-privacy-fence-cost/", "Wood Privacy Fence"),
            ("/fence-materials/vinyl-fence-cost/", "Vinyl Fence Cost"),
            ("/fence-cost-calculator/", "Fence Cost Calculator"),
        ],
        "regional": {
            "national": "Rinse boards occasionally; no stain required",
            "charlotte": "Popular in new-build subdivisions — walnut and gray tones",
            "raleigh": "Growing composite market — verify contractor brand certification",
            "san-diego": "Coastal installs — use marine-grade fasteners",
        },
        "home_examples": {
            "national": {"ft": 150, "height": 6, "variant": "privacy", "grade": "standard", "gates": 1, "detail": "6 ft walnut privacy · one gate"},
            "charlotte": {"ft": 160, "height": 6, "variant": "horizontal", "grade": "capped", "gates": 1, "detail": "6 ft horizontal · capped boards"},
        },
    },
    {
        "slug": "chain-link-fence-cost",
        "calc_material": "chain",
        "body_class": "chain-fence",
        "base_rate": 18,
        "short_label": "Chain link",
        "title": "Chain Link Fence Cost (2026) — Installed Prices per Foot | Estimate Home Costs",
        "description": "Chain link fence cost $15–$28 per linear foot installed in 2026. Compare galvanized vs vinyl-coated and privacy slat options with free calculator.",
        "keywords": "chain link fence cost, chain link fence cost per foot, galvanized fence cost, black chain link fence cost",
        "og_title": "Chain Link Fence Cost (2026)",
        "og_desc": "Budget-friendly chain link fencing — installed costs by height, coating, and city.",
        "twitter_desc": "Estimate chain link fence installation by linear foot and city.",
        "article_headline": "Chain Link Fence Cost (2026): Calculator & Guide",
        "breadcrumb": "Chain Link Fence Cost",
        "breadcrumb_short": "Chain Link",
        "h1": "Chain Link Fence Cost",
        "hero_lead": "The most affordable perimeter fencing for backyards, pets, and security — galvanized or vinyl-coated with optional privacy slats.",
        "hero_range": "$2,400–$3,500",
        "hero_per_ft": "$15–$22 per linear ft · 6 ft galvanized",
        "hero_cta_primary": "Estimate Chain Link Costs",
        "stats_cost": "$15–$28 per linear ft",
        "stats_privacy": "Low to moderate",
        "stats_life": "15–25 years",
        "stats_maint": "Very low",
        "styles_heading": "Chain Link Fence Options",
        "styles_lead": "Mesh gauge, coating, and privacy slats change cost and appearance.",
        "variants": [
            {"id": "galvanized", "name": "Galvanized", "mult": 1, "tier": "$ · Standard", "desc": "Silver zinc coating", "meta": "Most economical", "visual": "chain-galv"},
            {"id": "vinyl-coated", "name": "Vinyl-coated", "mult": 1.08, "tier": "$$ · Popular", "desc": "Green or black coat", "meta": "Blends with landscape", "visual": "chain-coated"},
            {"id": "black", "name": "Black coated", "mult": 1.12, "tier": "$$ · Modern", "desc": "Less industrial look", "meta": "Suburban upgrade", "visual": "chain-black"},
            {"id": "privacy-slats", "name": "Privacy slats", "mult": 1.35, "tier": "$$$ · Screening", "desc": "Slats woven in mesh", "meta": "Adds privacy", "visual": "chain-privacy"},
        ],
        "grades": [
            {"id": "residential", "label": "Residential gauge", "mult": 1, "life": "15–20 years", "look": "Standard mesh"},
            {"id": "heavy", "label": "Heavy / commercial gauge", "mult": 1.15, "life": "20–25 years", "look": "Stronger mesh"},
        ],
        "grade_label": "Mesh gauge",
        "grades_heading": "Chain Link Gauge Comparison",
        "grades_lead": "Installed cost per linear foot at 6 ft.",
        "grades_col1": "Gauge",
        "calc_heading": "Typical Chain Link Fence Cost",
        "calc_lead": "Enter length, coating style, mesh gauge, and city.",
        "calc_default_range": "$2,700–$3,300",
        "calc_default_hint": "150 ft · Galvanized · Residential",
        "calc_default_per_ft": "$18–$22 per linear ft installed",
        "bench_100": "$1,800–$2,200",
        "bench_150": "$2,700–$3,300",
        "bench_200": "$3,600–$4,400",
        "factors_pills": """            <li>Coating &amp; color</li>
            <li>Mesh gauge</li>
            <li>Height</li>
            <li>Privacy slats</li>
            <li>Terminal posts</li>""",
        "pros_heading": "Chain Link Pros & Cons",
        "pros_list": """              <li>Lowest installed cost per foot</li>
              <li>Durable and low maintenance</li>
              <li>Great for pet containment</li>
              <li>Quick installation</li>""",
        "cons_list": """              <li>Low privacy without slats</li>
              <li>Industrial appearance (unless black-coated)</li>
              <li>Not ideal for premium curb appeal</li>""",
        "benefits_heading": "Best Uses for Chain Link",
        "benefits_lead": "Chain link excels when <strong>budget and function</strong> matter more than aesthetics.",
        "benefits_list": """            <li><strong>Pet containment</strong> — secure dogs without solid panels</li>
            <li><strong>Side yards</strong> — utility areas and AC pads</li>
            <li><strong>Commercial lots</strong> — security perimeters</li>
            <li><strong>Temporary boundaries</strong> — until upgrading to wood or vinyl</li>""",
        "heights_heading": "Chain Link Height Options",
        "h4_privacy": "Low",
        "h4_list": """              <li>Garden and dog-run sections</li>""",
        "h6_privacy": "Moderate",
        "h6_list": """              <li>Standard backyard height</li>
              <li>Most common residential choice</li>""",
        "h8_privacy": "Moderate with slats",
        "h8_list": """              <li>Security and pool code areas</li>""",
        "colors_heading": "Chain Link Finishes",
        "colors_lead": "Coating affects appearance and rust resistance.",
        "colors": [
            {"class": "chain-galv", "name": "Galvanized", "note": "Budget standard"},
            {"class": "chain-green", "name": "Green vinyl-coated", "note": "Classic suburban"},
            {"class": "chain-black", "name": "Black coated", "note": "Less visible"},
            {"class": "chain-brown", "name": "Brown coated", "note": "Woodland blend"},
        ],
        "weather_heading": "Chain Link & Climate",
        "weather_national": """              <li><strong>Humid / coastal:</strong> Vinyl-coated mesh resists rust better than bare galvanized</li>
              <li><strong>Snow:</strong> Heavy gauge handles snow load on top rail</li>""",
        "install_heading": "Chain Link Installation Cost Factors",
        "install_cards": """          <article><h3>Terminal posts</h3><p>Corner and end posts are larger — more concrete than line posts.</p></article>
          <article><h3>Privacy slats</h3><p>Weaving slats adds material and labor — can add 30%+ to base cost.</p></article>
          <article><h3>Barbed or security top</h3><p>Commercial specs increase hardware cost.</p></article>
          <article><h3>Rocky soil</h3><p>Driving posts in rock slows installation.</p></article>""",
        "compare_heading": "Chain Link vs Other Fences",
        "comparisons": [
            {"href": "/fence-materials/wood-privacy-fence-cost/", "title": "Chain link vs Wood", "desc": "Budget mesh vs privacy wood — cost and use cases.", "cta": "Wood guide"},
            {"href": "/fence-materials/vinyl-fence-cost/", "title": "Chain link vs Vinyl", "desc": "When to upgrade from chain link to vinyl panels.", "cta": "Vinyl guide"},
            {"href": "/fence-cost-calculator/?material=chain", "title": "Fence calculator", "desc": "Compare all materials with chain link selected.", "cta": "Open calculator"},
        ],
        "projects_heading": "Real Chain Link Projects",
        "project_nat_type": "6 ft galvanized · 150 linear ft",
        "project_nat_detail": "6 ft galvanized · one walk gate",
        "project_nat_cost": "$2,900",
        "faq_heading": "Chain Link Fence FAQ",
        "faq": [
            {"q": "How much does chain link fence cost?", "a": "Chain link typically costs <strong>$15–$28 per linear foot</strong> installed. Privacy slats increase the total.", "a_plain": "Chain link typically costs $15–$28 per linear foot installed."},
            {"q": "Is chain link the cheapest fence?", "a": "Yes — chain link is usually the <strong>lowest-cost</strong> installed residential fence type.", "a_plain": "Yes, chain link is usually the lowest-cost residential fence."},
            {"q": "How long does chain link last?", "a": "Galvanized mesh often lasts <strong>15–20 years</strong>; vinyl-coated can reach 20–25 years.", "a_plain": "Galvanized lasts 15–20 years; coated mesh 20–25 years."},
        ],
        "cta_heading": "Estimate Chain Link Fence Costs",
        "cta_lead": "Full calculator with chain link pre-selected.",
        "related": [
            ("/fence-materials/chain-link-fence-cost/", "Chain Link Fence Cost"),
            ("/fence-materials/wood-privacy-fence-cost/", "Wood Privacy Fence"),
            ("/fence-cost-calculator/", "Fence Cost Calculator"),
        ],
        "regional": {
            "national": "Inspect tension wire annually; touch up cuts on coated mesh",
            "phoenix": "Galvanized performs well in dry heat — less rust than humid coasts",
            "houston": "Vinyl-coated black mesh popular — resists humidity rust",
        },
        "home_examples": {
            "national": {"ft": 150, "height": 6, "variant": "galvanized", "grade": "residential", "gates": 1, "detail": "6 ft galvanized · one gate"},
            "houston": {"ft": 180, "height": 6, "variant": "black", "grade": "residential", "gates": 1, "detail": "6 ft black coated · slope"},
        },
    },
    {
        "slug": "aluminum-fence-cost",
        "calc_material": "aluminum",
        "body_class": "aluminum-fence",
        "base_rate": 35,
        "short_label": "Aluminum",
        "title": "Aluminum Fence Cost (2026) — Ornamental & Pool Fence Prices | Estimate Home Costs",
        "description": "Aluminum fence cost $30–$50 per linear foot installed in 2026. Compare flat-top, spear-top, and pool-rated ornamental fencing with free calculator.",
        "keywords": "aluminum fence cost, aluminum fence cost per foot, ornamental aluminum fence cost, pool fence aluminum cost",
        "og_title": "Aluminum Fence Cost (2026)",
        "og_desc": "Durable ornamental aluminum fencing — installed costs by style and city.",
        "twitter_desc": "Estimate aluminum fence installation by style and city.",
        "article_headline": "Aluminum Fence Cost (2026): Styles & Calculator",
        "breadcrumb": "Aluminum Fence Cost",
        "breadcrumb_short": "Aluminum Fence",
        "h1": "Aluminum Fence Cost",
        "hero_lead": "Powder-coated aluminum fencing delivers ornamental curb appeal, pool-code safety, and decades of rust-free performance — without wood maintenance.",
        "hero_range": "$4,500–$6,800",
        "hero_per_ft": "$30–$45 per linear ft · 6 ft ornamental",
        "hero_cta_primary": "Estimate Aluminum Fence Costs",
        "stats_cost": "$30–$50 per linear ft",
        "stats_privacy": "Low to moderate",
        "stats_life": "25+ years",
        "stats_maint": "Very low",
        "styles_heading": "Aluminum Fence Styles",
        "styles_lead": "Picket profile and height drive cost — pool-rated systems add hardware requirements.",
        "variants": [
            {"id": "flat", "name": "Flat top", "mult": 1, "tier": "$$ · Classic", "desc": "Flat picket caps", "meta": "HOA common", "visual": "aluminum-flat"},
            {"id": "spear", "name": "Spear top", "mult": 1.06, "tier": "$$ · Traditional", "desc": "Decorative finials", "meta": "Estate look", "visual": "aluminum-spear"},
            {"id": "pool", "name": "Pool code", "mult": 1.15, "tier": "$$$ · Safety", "desc": "Self-closing gates", "meta": "Code compliant", "visual": "aluminum-pool"},
            {"id": "privacy", "name": "Privacy panels", "mult": 1.28, "tier": "$$$ · Screening", "desc": "Solid aluminum boards", "meta": "Rare vs picket", "visual": "aluminum-privacy"},
        ],
        "grades": [
            {"id": "standard", "label": "Standard powder coat", "mult": 1, "life": "25 years", "look": "Black or bronze"},
            {"id": "heavy", "label": "Heavy-duty rail", "mult": 1.12, "life": "30+ years", "look": "Wind zones"},
            {"id": "pool", "label": "Pool-rated package", "mult": 1.2, "life": "25+ years", "look": "Code hardware"},
        ],
        "grade_label": "System grade",
        "grades_heading": "Aluminum Fence System Comparison",
        "grades_lead": "Installed cost per linear foot at 6 ft.",
        "grades_col1": "System",
        "calc_heading": "Typical Aluminum Fence Cost",
        "calc_lead": "Enter length, ornamental style, system grade, and city.",
        "calc_default_range": "$5,250–$6,400",
        "calc_default_hint": "150 ft · Flat top · Standard",
        "calc_default_per_ft": "$35–$43 per linear ft installed",
        "bench_100": "$3,500–$4,300",
        "bench_150": "$5,250–$6,400",
        "bench_200": "$7,000–$8,500",
        "factors_pills": """            <li>Picket style</li>
            <li>Pool code</li>
            <li>Gate hardware</li>
            <li>Powder coat color</li>
            <li>Terrain</li>""",
        "pros_heading": "Aluminum Fence Pros & Cons",
        "pros_list": """              <li>Will not rust like steel</li>
              <li>Elegant ornamental appearance</li>
              <li>Pool and HOA friendly</li>
              <li>Minimal maintenance</li>""",
        "cons_list": """              <li>Less privacy than wood or vinyl panels</li>
              <li>Higher cost than chain link</li>
              <li>Dents possible from impacts</li>""",
        "benefits_heading": "Best Uses for Aluminum Fencing",
        "benefits_lead": "Aluminum is ideal when you need <strong>decorative boundaries and code compliance</strong> without wood upkeep.",
        "benefits_list": """            <li><strong>Front yards</strong> — ornamental street appeal</li>
            <li><strong>Pool enclosures</strong> — self-closing, self-latching gates</li>
            <li><strong>HOA communities</strong> — consistent black or bronze palette</li>
            <li><strong>Coastal homes</strong> — salt air resistant powder coat</li>""",
        "heights_heading": "Aluminum Fence Height Options",
        "h4_privacy": "Decorative",
        "h4_list": """              <li>Front yard and garden borders</li>""",
        "h6_privacy": "Moderate",
        "h6_list": """              <li>Side and backyard ornamental</li>
              <li>Common pool barrier height</li>""",
        "h8_privacy": "Moderate",
        "h8_list": """              <li>Where municipal codes allow taller ornamental</li>""",
        "colors_heading": "Aluminum Fence Finishes",
        "colors_lead": "Powder-coated finishes are baked on for durability.",
        "colors": [
            {"class": "aluminum-black", "name": "Black", "note": "Most popular"},
            {"class": "aluminum-bronze", "name": "Bronze", "note": "Warm traditional"},
            {"class": "aluminum-white", "name": "White", "note": "Coastal & pool"},
            {"class": "aluminum-green", "name": "Green", "note": "Garden blend"},
        ],
        "weather_heading": "Aluminum Fencing & Climate",
        "weather_national": """              <li><strong>Coastal:</strong> Excellent salt-air resistance with quality powder coat</li>
              <li><strong>All regions:</strong> No rot — unlike wood</li>""",
        "install_heading": "Aluminum Fence Installation Cost Factors",
        "install_cards": """          <article><h3>Pool code</h3><p>Self-closing hinges and latches add hardware and inspection time.</p></article>
          <article><h3>Racking on slope</h3><p>Pickets rack to follow grade — extra layout labor.</p></article>
          <article><h3>Gates</h3><p>Ornamental walk gates $400–$900+; double drive gates cost more.</p></article>
          <article><h3>Core drilling</h3><p>Installing in concrete patios increases labor.</p></article>""",
        "compare_heading": "Aluminum vs Other Materials",
        "comparisons": [
            {"href": "/fence-materials/wood-privacy-fence-cost/", "title": "Aluminum vs Wood", "desc": "Ornamental metal vs privacy wood.", "cta": "Wood guide"},
            {"href": "/fence-materials/vinyl-fence-cost/", "title": "Aluminum vs Vinyl", "desc": "Metal pickets vs vinyl panels.", "cta": "Vinyl guide"},
            {"href": "/fence-cost-calculator/?material=aluminum", "title": "Fence calculator", "desc": "Compare materials with aluminum selected.", "cta": "Open calculator"},
        ],
        "projects_heading": "Real Aluminum Fence Projects",
        "project_nat_type": "6 ft flat-top ornamental · 150 linear ft",
        "project_nat_detail": "6 ft black flat-top · one gate",
        "project_nat_cost": "$5,800",
        "faq_heading": "Aluminum Fence FAQ",
        "faq": [
            {"q": "How much does an aluminum fence cost?", "a": "Aluminum fencing typically costs <strong>$30–$50 per linear foot</strong> installed.", "a_plain": "Aluminum fencing typically costs $30–$50 per linear foot installed."},
            {"q": "Is aluminum better than wrought iron?", "a": "Aluminum is <strong>lighter and rust-free</strong>; wrought iron is heavier and may need refinishing.", "a_plain": "Aluminum is lighter and rust-free compared to wrought iron."},
            {"q": "Does aluminum work for pool fences?", "a": "Yes — pool-rated aluminum systems with self-closing gates are widely used for code compliance.", "a_plain": "Yes, pool-rated aluminum with self-closing gates meets many pool codes."},
        ],
        "cta_heading": "Estimate Aluminum Fence Costs",
        "cta_lead": "Full fence calculator with aluminum pre-selected.",
        "related": [
            ("/fence-materials/aluminum-fence-cost/", "Aluminum Fence Cost"),
            ("/fence-materials/vinyl-fence-cost/", "Vinyl Fence Cost"),
            ("/fence-cost-calculator/", "Fence Cost Calculator"),
        ],
        "regional": {
            "national": "Rinse powder coat yearly in salt-air regions",
            "tampa": "Pool enclosures common — budget for code hardware",
            "san-diego": "Black powder coat popular near coast",
            "scottsdale": "Ornamental aluminum on upscale desert lots",
        },
        "home_examples": {
            "national": {"ft": 150, "height": 6, "variant": "flat", "grade": "standard", "gates": 1, "detail": "6 ft black flat-top · one gate"},
            "tampa": {"ft": 120, "height": 4, "variant": "pool", "grade": "pool", "gates": 1, "detail": "4 ft pool code · self-closing gate"},
        },
    },
]


def main() -> None:
    for m in MATERIALS:
        out_dir = OUT / m["slug"]
        out_dir.mkdir(parents=True, exist_ok=True)
        html = render_page(m)
        (out_dir / "index.html").write_text(html, encoding="utf-8")
        print(f"Wrote {out_dir / 'index.html'}")


if __name__ == "__main__":
    main()

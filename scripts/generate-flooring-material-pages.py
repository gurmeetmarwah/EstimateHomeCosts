#!/usr/bin/env python3
"""Generate flooring material landing pages (hardwood, engineered, tile, carpet)."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "flooring-materials"

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


def variant_cards(variants: list[dict]) -> str:
    n = len(variants)
    grid = "fence-variant-cards-grid--5" if n >= 5 else ("fence-variant-cards-grid--4" if n == 4 else "")
    cards = []
    for i, v in enumerate(variants):
        active = " fence-variant-card--active" if i == 0 else ""
        checked = " checked" if i == 0 else ""
        cards.append(f"""          <label class="fence-variant-card{active}" data-flooring-variant-card="{v['id']}">
            <input type="radio" name="flooring_style" value="{v['id']}"{checked}>
            <span class="fence-variant-card-visual fence-variant-card-visual--{v['visual']}" aria-hidden="true"></span>
            <span class="fence-variant-card-tier">{v['tier']}</span>
            <h3>{v['name']}</h3>
            <p>{v['desc']}</p>
            <span class="fence-variant-card-meta">{v['meta']}</span>
          </label>""")
    return f'        <div class="fence-variant-cards-grid {grid}">\n' + "\n".join(cards) + "\n        </div>"


def opts(variants: list[dict]) -> str:
    return "\n".join(
        f'                  <option value="{v["id"]}"{" selected" if i == 0 else ""}>{v["name"]}</option>'
        for i, v in enumerate(variants)
    )


def grade_opts(grades: list[dict]) -> str:
    return "\n".join(
        f'                  <option value="{g["id"]}"{" selected" if i == 0 else ""}>{g["label"]}</option>'
        for i, g in enumerate(grades)
    )


def swatches(colors: list[dict]) -> str:
    return "\n".join(
        f"""          <div class="stain-swatch">
            <span class="stain-swatch-color stain-swatch-color--{c['class']}" aria-hidden="true"></span>
            <strong>{c['name']}</strong>
            <span>{c['note']}</span>
          </div>"""
        for c in colors
    )


def benchmarks_html(bench: list[dict]) -> str:
    items = []
    for i, b in enumerate(bench):
        active = ' wood-cost-benchmark-card--active' if i == 0 else ""
        items.append(f"""            <li class="wood-cost-benchmark-card{active}" data-range-sqft="{b['sqft']}">
              <span class="wood-cost-benchmark-ft">{b['sqft']:,} sq ft</span>
              <strong class="flooring-benchmark-price wood-cost-benchmark-price">{b['price']}</strong>
              <span class="wood-cost-benchmark-note">{b['note']}</span>
            </li>""")
    return "\n".join(items)


def faq_html(faq: list[dict]) -> str:
    return "\n".join(
        f"""          <details class="faq-item">
            <summary>{q['q']}</summary>
            <p>{q['a']}</p>
          </details>"""
        for q in faq
    )


def faq_schema(faq: list[dict]) -> str:
    parts = []
    for q in faq:
        parts.append(
            f'          {{"@type": "Question", "name": {json.dumps(q["q"])}, "acceptedAnswer": {{"@type": "Answer", "text": {json.dumps(q["plain"])}}}}}'
        )
    return ",\n".join(parts)


def comparisons(links: list[dict]) -> str:
    return "\n".join(
        f"""          <a href="{l['href']}" class="comparison-card">
            <h3>{l['title']}</h3>
            <p>{l['desc']}</p>
            <span class="comparison-card-cta">{l['cta']} →</span>
          </a>"""
        for l in links
    )


def related(links: list[tuple[str, str]]) -> str:
    return "\n".join(f'          <a href="{h}">{t}</a>' for h, t in links)


def js_config(m: dict) -> str:
    cfg = {
        "material": m["material_rate"],
        "labor": m["labor_rate"],
        "shortLabel": m["short_label"],
        "defaultVariant": m["variants"][0]["id"],
        "defaultGrade": m["grades"][0]["id"] if m.get("grades") else None,
        "defaultWear": m.get("default_wear"),
        "variants": {v["id"]: {"mult": v["mult"], "label": v["name"]} for v in m["variants"]},
        "grades": {
            g["id"]: {"mult": g["mult"], "label": g["label"], "life": g.get("life", ""), "bestFor": g.get("best_for", "")}
            for g in m.get("grades", [])
        },
        "wear": {w["id"]: {"mult": w["mult"], "label": w["label"], "bestFor": w.get("best_for", "")} for w in m.get("wear", [])},
        "benchmarks": m.get("benchmark_sqft", [500, 1000]),
        "regional": m["regional"],
        "homeExamples": m["home_examples"],
    }
    return json.dumps(cfg, indent=2)


def render(m: dict) -> str:
    grade_field = ""
    wear_field = ""
    if m.get("grades"):
        grade_field = f"""
              <div class="form-group">
                <label for="flooring-material-grade">{m['grade_label']}</label>
                <select id="flooring-material-grade" name="flooring_grade">
{grade_opts(m['grades'])}
                </select>
              </div>"""
    if m.get("wear"):
        wear_field = f"""
              <div class="form-group">
                <label for="flooring-material-wear">{m['wear_label']}</label>
                <select id="flooring-material-wear" name="flooring_wear">
{grade_opts(m['wear'])}
                </select>
              </div>"""

    looks = ""
    if m.get("colors"):
        looks = f"""
    <section id="design-options" class="section stain-section" aria-labelledby="design-heading">
      <div class="container">
        <header class="section-header section-header--center">
          <h2 id="design-heading">{m['design_heading']}</h2>
          <p>{m['design_lead']}</p>
        </header>
        <div class="stain-swatch-grid lvp-look-grid">
{swatches(m['colors'])}
        </div>
      </div>
    </section>"""

    special = ""
    if m.get("special_section"):
        s = m["special_section"]
        special = f"""
    <section id="{s['id']}" class="section cost-detail-section cost-detail-section--alt" aria-labelledby="{s['id']}-heading">
      <div class="container cost-detail-grid">
        <div class="cost-detail-copy">
          <h2 id="{s['id']}-heading">{s['heading']}</h2>
          <p>{s['lead']}</p>
          <ul class="cost-detail-list">{s['list']}</ul>
        </div>
      </div>
    </section>"""

    detail = ""
    if m.get("detail_table"):
        d = m["detail_table"]
        detail = f"""
    <section id="detail-table" class="section cost-tables-section" aria-labelledby="detail-heading">
      <div class="container">
        <header class="section-header section-header--center">
          <h2 id="detail-heading">{d['heading']}</h2>
          <p>{d['lead']}</p>
        </header>
        <div class="table-wrap">
          <table class="cost-table cost-table--compact">
            <thead><tr><th scope="col">{d['col1']}</th><th scope="col">{d['col2']}</th><th scope="col">Installed cost</th></tr></thead>
            <tbody id="flooring-material-detail-tbody"></tbody>
          </table>
        </div>
      </div>
    </section>"""

    rooms = ""
    if m.get("rooms"):
        rooms = f"""
    <section id="best-rooms" class="section flooring-rooms-section" aria-labelledby="rooms-heading">
      <div class="container">
        <header class="section-header section-header--center">
          <h2 id="rooms-heading">{m['rooms_heading']}</h2>
          <p>{m['rooms_lead']}</p>
        </header>
        <div class="flooring-rooms-grid">
{m['rooms_cards']}
        </div>
      </div>
    </section>"""

    pet = ""
    if m.get("pet_section"):
        pet = f"""
    <section id="pet-family" class="section cost-detail-section" aria-labelledby="pet-heading">
      <div class="container">
        <header class="section-header section-header--center">
          <h2 id="pet-heading">{m['pet_heading']}</h2>
          <p>{m['pet_lead']}</p>
        </header>
        <ul class="cost-detail-list cost-detail-list--centered">{m['pet_list']}</ul>
      </div>
    </section>"""

    nav_extra = '<li><a href="#design-options">Design</a></li>' if m.get("colors") else ""
    if m.get("detail_table"):
        nav_extra = '<li><a href="#detail-table">Options</a></li>'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{m['title']}</title>
  <meta name="description" content="{m['description']}">
  <meta name="keywords" content="{m['keywords']}">
  <link rel="canonical" href="https://estimatehomecosts.com/flooring-materials/{m['slug']}/">
  <meta property="og:title" content="{m['og_title']}">
  <meta property="og:description" content="{m['og_desc']}">
  <meta name="theme-color" content="#1a3d36">
  <link rel="stylesheet" href="/css/styles.css">
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Fraunces:wght@500;600;700&display=swap" rel="stylesheet">
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@graph":[
    {{"@type":"Article","headline":{json.dumps(m['article_headline'])},"url":"https://estimatehomecosts.com/flooring-materials/{m['slug']}/"}},
    {{"@type":"BreadcrumbList","itemListElement":[
      {{"@type":"ListItem","position":1,"name":"Home","item":"https://estimatehomecosts.com/"}},
      {{"@type":"ListItem","position":2,"name":"Flooring Calculator","item":"https://estimatehomecosts.com/flooring-cost-calculator/"}},
      {{"@type":"ListItem","position":3,"name":{json.dumps(m['breadcrumb'])},"item":"https://estimatehomecosts.com/flooring-materials/{m['slug']}/"}}
    ]}},
    {{"@type":"FAQPage","mainEntity":[{faq_schema(m['faq'])}]}}
  ]}}
  </script>
</head>
<body class="material-page material-page--{m['body_class']}">
  <a class="skip-link" href="#main">Skip to main content</a>
  <header class="site-header" role="banner">
    <div class="header-inner">
      <a href="/" class="logo"><span class="logo-text">Estimate <strong>Home Costs</strong></span></a>
      <nav class="nav-primary"><ul>
        <li><a href="#flooring-styles">Styles</a></li>{nav_extra}
        <li><a href="#calculator">Calculator</a></li>
        <li><a href="#faq">FAQ</a></li>
      </ul></nav>
      <button type="button" class="nav-toggle" aria-label="Open menu"><span></span><span></span><span></span></button>
    </div>
  </header>

  <main id="main">
    <section id="hero" class="flooring-material-hero" aria-labelledby="hero-heading">
      <div class="container">
        <nav class="breadcrumb"><ol>
          <li><a href="/">Home</a></li>
          <li><a href="/flooring-cost-calculator/">Flooring Calculator</a></li>
          <li aria-current="page">{m['breadcrumb_short']}</li>
        </ol></nav>
        <div class="flooring-material-hero-copy">
          <p class="hero-eyebrow">Flooring materials by style</p>
          <h1 id="hero-heading">{m['h1']}</h1>
          <p class="flooring-material-hero-lead">{m['hero_lead']}</p>
          <p class="flooring-material-hero-price">
            <span class="flooring-material-hero-price-label">Average cost</span>
            <strong id="hero-cost-range">{m['hero_range']}</strong>
            <span class="flooring-material-hero-price-note" id="hero-per-ft">{m['hero_per_ft']}</span>
          </p>
          <div class="flooring-material-hero-actions">
            <a href="#calculator" class="btn btn-primary btn-lg">Estimate Flooring Cost</a>
            <a href="/flooring-cost-calculator/?material={m['calc_material']}" class="btn btn-secondary btn-lg">Open Flooring Calculator</a>
          </div>
        </div>
      </div>
    </section>

    <section class="material-quick-stats" aria-label="{m['short_label']} at a glance">
      <div class="container">
        <ul class="material-quick-stats-grid">
          <li><span class="material-quick-stats-label">Average cost</span><strong id="stat-avg-cost">{m['stats_cost']}</strong></li>
          <li><span class="material-quick-stats-label">{m['stat2_label']}</span><strong>{m['stat2']}</strong></li>
          <li><span class="material-quick-stats-label">Lifespan</span><strong>{m['stats_life']}</strong></li>
          <li><span class="material-quick-stats-label">Maintenance</span><strong>{m['stats_maint']}</strong></li>
        </ul>
      </div>
    </section>

    <section id="flooring-styles" class="section fence-variant-section" aria-labelledby="styles-heading">
      <div class="container">
        <header class="section-header section-header--center">
          <h2 id="styles-heading">{m['styles_heading']}</h2>
          <p>{m['styles_lead']}</p>
        </header>
{variant_cards(m['variants'])}
      </div>
    </section>

    <section id="calculator" class="section quick-estimate-section wood-fence-calc-section" aria-labelledby="calc-heading">
      <div class="container">
        <header class="section-header section-header--center">
          <h2 id="calc-heading">{m['calc_heading']}</h2>
          <p>{m['calc_lead']}</p>
        </header>
        <div class="quick-estimator wood-fence-estimator">
          <form id="flooring-material-calc-form" class="quick-estimator-form" novalidate>
            <div class="quick-estimator-fields quick-estimator-fields--fence">
              <div class="form-group">
                <label for="flooring-material-sqft">Floor area</label>
                <div class="quick-input-wrap">
                  <input type="number" id="flooring-material-sqft" min="100" max="5000" step="50" value="{m['default_sqft']}" required>
                  <span class="quick-input-suffix" aria-hidden="true">sq ft</span>
                </div>
              </div>
              <div class="form-group">
                <label for="flooring-material-variant">{m['variant_label']}</label>
                <select id="flooring-material-variant">
{opts(m['variants'])}
                </select>
              </div>{grade_field}{wear_field}
              <div class="form-group">
                <label for="flooring-material-prep">Subfloor prep</label>
                <select id="flooring-material-prep">
                  <option value="none">None / ready</option>
                  <option value="minor" selected>Minor leveling</option>
                  <option value="major">Major repair</option>
                </select>
              </div>
              <div class="form-group">
                <label for="flooring-material-removal">Remove existing floor?</label>
                <select id="flooring-material-removal">
                  <option value="no" selected>No</option>
                  <option value="yes">Yes — tear out</option>
                </select>
              </div>
              <div class="form-group">
                <label for="flooring-material-city">City</label>
                <select id="flooring-material-city">
{CITY_OPTS}
                </select>
              </div>
            </div>
            <aside class="quick-estimator-aside" aria-label="Live estimate">
              <div class="quick-estimate-result" aria-live="polite">
                <span class="quick-estimate-live"><span class="quick-estimate-live-dot" aria-hidden="true"></span> Updates live</span>
                <span class="quick-estimate-label">Estimated installation cost</span>
                <p class="quick-estimate-price" id="flooring-material-calc-range">{m['calc_default_range']}</p>
                <p class="quick-result-hint" id="flooring-material-calc-hint">{m['calc_default_hint']}</p>
                <p class="wood-calc-per-ft" id="flooring-material-calc-per-sqft">{m['calc_default_per_sqft']}</p>
              </div>
              <a href="/flooring-cost-calculator/?material={m['calc_material']}" class="btn btn-primary btn-lg btn-block">Open full flooring calculator</a>
            </aside>
          </form>
        </div>
        <div class="wood-cost-benchmarks">
          <h3 class="wood-cost-benchmarks-title">Typical total cost by project size</h3>
          <p class="wood-cost-benchmarks-lead">Based on your selections above.</p>
          <ul class="wood-cost-benchmarks-grid flooring-benchmarks-grid" id="flooring-material-cost-range-list">
{benchmarks_html(m['benchmarks'])}
          </ul>
        </div>
        <div class="wood-cost-factors">
          <p class="wood-cost-factors-title">Cost varies based on</p>
          <ul class="wood-cost-factors-list">{m['factors']}</ul>
        </div>
      </div>
    </section>
{looks}
    <section id="pros-cons" class="section pros-cons-section" aria-labelledby="pros-heading">
      <div class="container">
        <h2 id="pros-heading" class="section-header section-header--center">{m['pros_heading']}</h2>
        <div class="pros-cons-grid">
          <div class="pros-cons-col pros-cons-col--pros"><h3>Advantages</h3><ul>{m['pros']}</ul></div>
          <div class="pros-cons-col pros-cons-col--cons"><h3>Disadvantages</h3><ul>{m['cons']}</ul></div>
        </div>
      </div>
    </section>
{special}{detail}
    <section id="install-types" class="section flooring-install-section" aria-labelledby="install-heading">
      <div class="container">
        <header class="section-header section-header--center">
          <h2 id="install-heading">{m['install_heading']}</h2>
        </header>
        <div class="flooring-install-grid">{m['install_cards']}</div>
      </div>
    </section>
    <section id="comparisons" class="section comparison-cards-section" aria-labelledby="compare-heading">
      <div class="container">
        <header class="section-header section-header--center"><h2 id="compare-heading">{m['compare_heading']}</h2></header>
        <div class="comparison-cards-grid">{comparisons(m['comparisons'])}</div>
      </div>
    </section>
{rooms}{pet}
    <section id="project-examples" class="section project-examples-section" aria-labelledby="projects-heading">
      <div class="container">
        <header class="section-header section-header--center">
          <h2 id="projects-heading">{m['projects_heading']}</h2>
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
          <article class="project-example-card" id="flooring-material-project-city-card" hidden>
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
        <header class="section-header section-header--center"><h2 id="faq-heading">{m['faq_heading']}</h2></header>
        <div class="faq-list">{faq_html(m['faq'])}</div>
      </div>
    </section>
    <section class="section material-cta-band" aria-labelledby="cta-heading">
      <div class="container material-cta-band-inner">
        <h2 id="cta-heading">Estimate Flooring Costs</h2>
        <p>{m['cta_lead']}</p>
        <div class="material-cta-actions">
          <a href="/flooring-cost-calculator/?material={m['calc_material']}" class="btn btn-primary btn-lg">Open Flooring Calculator</a>
          <a href="#calculator" class="btn btn-secondary btn-lg">Use quick estimator</a>
        </div>
      </div>
    </section>
    <section id="related" class="section related-links-section" aria-labelledby="related-heading">
      <div class="container">
        <h2 id="related-heading" class="section-header section-header--center">Related Flooring Guides</h2>
        <nav class="related-links">{related(m['related'])}</nav>
      </div>
    </section>
  </main>
  <footer class="site-footer"><div class="footer-bottom"><div class="container"><p>© 2026 Estimate Home Costs</p></div></div></footer>
  <script>window.FLOORING_MATERIAL_CONFIG = {js_config(m)};</script>
  <script src="/js/calculator-cities.js" defer></script>
  <script src="/js/main.js" defer></script>
  <script src="/js/flooring-material-page.js" defer></script>
</body>
</html>"""


MATERIALS = [
    {
        "slug": "solid-hardwood-flooring-cost",
        "calc_material": "hardwood",
        "body_class": "hardwood-flooring",
        "material_rate": 6.5,
        "labor_rate": 4.5,
        "short_label": "Hardwood",
        "title": "Solid Hardwood Flooring Cost (2026) — Installed Prices | Estimate Home Costs",
        "description": "Solid hardwood floor cost $8–$14 per sq ft installed in 2026. Compare oak, maple, hickory, nail-down install, and city-level pricing.",
        "keywords": "hardwood floor cost, solid hardwood flooring cost per square foot, oak hardwood floor cost",
        "og_title": "Solid Hardwood Flooring Cost (2026)",
        "og_desc": "Premium solid hardwood installed costs — species, finishes, and regional pricing.",
        "article_headline": "Solid Hardwood Flooring Cost (2026)",
        "breadcrumb": "Solid Hardwood Cost",
        "breadcrumb_short": "Solid Hardwood",
        "h1": "Solid Hardwood Flooring",
        "hero_lead": "Solid hardwood delivers authentic grain, decades of lifespan, and strong resale appeal — the premium choice for living areas when moisture is controlled.",
        "hero_range": "$4,500–$5,500",
        "hero_per_ft": "$9–$11 per sq ft · 500 sq ft",
        "stats_cost": "$8–$14/sq ft",
        "stat2_label": "Resale appeal",
        "stat2": "High",
        "stats_life": "50+ years",
        "stats_maint": "Moderate",
        "styles_heading": "Solid Hardwood Styles & Species",
        "styles_lead": "Wood species and install method are the biggest cost drivers for solid hardwood.",
        "variants": [
            {"id": "oak", "name": "Red oak", "mult": 1, "tier": "$$ · Popular", "desc": "Classic grain · stain-friendly", "meta": "Most installs", "visual": "hw-oak"},
            {"id": "maple", "name": "Maple", "mult": 1.08, "tier": "$$ · Light tone", "desc": "Hard · subtle grain", "meta": "Modern homes", "visual": "hw-maple"},
            {"id": "hickory", "name": "Hickory", "mult": 1.15, "tier": "$$$ · Character", "desc": "Bold variation · very hard", "meta": "Rustic luxury", "visual": "hw-hickory"},
            {"id": "walnut", "name": "Walnut", "mult": 1.22, "tier": "$$$ · Premium", "desc": "Rich brown · designer", "meta": "High-end", "visual": "hw-walnut"},
        ],
        "grades": [
            {"id": "prefinished", "label": "Prefinished", "mult": 1, "life": "25–50 yrs", "best_for": "Faster install"},
            {"id": "unfinished", "label": "Unfinished + site finish", "mult": 1.12, "life": "50+ yrs", "best_for": "Custom stain"},
            {"id": "wide-plank", "label": "Wide plank", "mult": 1.18, "life": "50+ yrs", "best_for": "Luxury look"},
        ],
        "grade_label": "Finish / profile",
        "default_sqft": "500",
        "calc_heading": "Typical Solid Hardwood Flooring Cost",
        "calc_lead": "Enter square footage, species, finish type, prep, and city.",
        "variant_label": "Wood species",
        "calc_default_range": "$4,500–$5,500",
        "calc_default_hint": "500 sq ft · Red oak · Prefinished",
        "calc_default_per_sqft": "$9.00–$11.00 per sq ft installed",
        "benchmarks": [
            {"sqft": 500, "price": "$4,000–$7,000", "note": "Main level"},
            {"sqft": 1000, "price": "$8,000–$14,000", "note": "Whole home"},
        ],
        "factors": """            <li>Wood species</li>
            <li>Plank width</li>
            <li>Site finish</li>
            <li>Subfloor prep</li>
            <li>Stairs &amp; transitions</li>""",
        "design_heading": "Hardwood Stain & Color Options",
        "design_lead": "Site-finished hardwood can be customized to match cabinetry and trim.",
        "colors": [
            {"class": "hw-natural", "name": "Natural", "note": "Clear coat"},
            {"class": "hw-golden", "name": "Golden oak", "note": "Traditional"},
            {"class": "hw-espresso", "name": "Espresso", "note": "Dark modern"},
            {"class": "hw-gray", "name": "Gray wash", "note": "Contemporary"},
            {"class": "hw-whitewash", "name": "Whitewashed", "note": "Coastal"},
        ],
        "pros_heading": "Solid Hardwood Pros & Cons",
        "pros": """              <li>Authentic wood grain and warmth</li>
              <li>Can be refinished multiple times</li>
              <li>Strong resale value</li>
              <li>50+ year potential lifespan</li>""",
        "cons": """              <li>Higher cost than LVP or carpet</li>
              <li>Not ideal for wet areas</li>
              <li>Sensitive to humidity swings</li>""",
        "special_section": {
            "id": "moisture",
            "heading": "Moisture & Climate Considerations",
            "lead": "Solid hardwood needs stable indoor humidity — avoid raw slab baths without proper acclimation.",
            "list": """            <li><strong>Living & dining:</strong> Ideal when humidity is controlled</li>
            <li><strong>Bedrooms:</strong> Excellent with area rugs at transitions</li>
            <li><strong>Baths & basements:</strong> Use engineered wood or tile instead</li>""",
        },
        "detail_table": {
            "heading": "Hardwood Species Comparison",
            "lead": "Installed cost per sq ft at 500 sq ft — updates with calculator.",
            "col1": "Species",
            "col2": "Best for",
        },
        "install_heading": "Hardwood Installation Methods",
        "install_cards": """          <article class="flooring-install-card flooring-install-card--featured"><h3>Nail-down</h3><p class="flooring-install-meta">$$$ · Standard</p><p>Over plywood subfloor — most common for 3/4 in solid.</p></article>
          <article class="flooring-install-card"><h3>Staple-down</h3><p class="flooring-install-meta">$$ · Similar</p><p>Faster than cleat nails on some jobs.</p></article>
          <article class="flooring-install-card"><h3>Glue-assist</h3><p class="flooring-install-meta">$$$ · Stable</p><p>Added adhesion on wide planks or concrete interfaces.</p></article>
          <article class="flooring-install-card"><h3>Sand &amp; finish</h3><p class="flooring-install-meta">$$$$ · Custom</p><p>Site stain after install — extra labor days.</p></article>""",
        "compare_heading": "Hardwood vs Other Flooring",
        "comparisons": [
            {"href": "/flooring-materials/luxury-vinyl-plank-flooring-cost/", "title": "Hardwood vs LVP", "desc": "Natural wood vs wood-look vinyl.", "cta": "LVP guide"},
            {"href": "/flooring-materials/engineered-wood-flooring-cost/", "title": "Hardwood vs Engineered", "desc": "Solid vs stable engineered planks.", "cta": "Engineered guide"},
            {"href": "/flooring-cost-calculator/#material-comparison", "title": "All materials", "desc": "Side-by-side on one calculator.", "cta": "Open calculator"},
        ],
        "rooms_heading": "Best Rooms for Solid Hardwood",
        "rooms_lead": "Where solid hardwood shines in the home.",
        "rooms_cards": """          <article class="flooring-room-card flooring-room-card--featured"><h3>Living rooms</h3><p>Showcase grain</p></article>
          <article class="flooring-room-card"><h3>Dining rooms</h3><p>Entertaining spaces</p></article>
          <article class="flooring-room-card"><h3>Bedrooms</h3><p>Warm &amp; quiet with rugs</p></article>
          <article class="flooring-room-card"><h3>Hallways</h3><p>Continuous flow</p></article>
          <article class="flooring-room-card"><h3>Home offices</h3><p>Professional look</p></article>""",
        "projects_heading": "Real Hardwood Flooring Projects",
        "project_nat_type": "900 sq ft red oak · main level",
        "project_nat_detail": "Prefinished · minor prep",
        "project_nat_cost": "$8,400",
        "faq_heading": "Solid Hardwood FAQ",
        "faq": [
            {"q": "How much does solid hardwood flooring cost?", "a": "Solid hardwood typically costs <strong>$8–$14 per sq ft</strong> installed. Use the <a href=\"#calculator\">estimator</a>.", "plain": "Solid hardwood typically costs $8–$14 per sq ft installed."},
            {"q": "Does hardwood increase home value?", "a": "Yes — <strong>real hardwood</strong> is among the best flooring types for resale in most suburban markets.", "plain": "Real hardwood is among the best flooring types for resale."},
            {"q": "Can hardwood go on concrete?", "a": "Solid hardwood is <strong>not recommended</strong> directly on slab — engineered or LVP is typical below grade.", "plain": "Solid hardwood is not recommended directly on concrete slab."},
        ],
        "cta_lead": "Full calculator with solid hardwood pre-selected.",
        "related": [
            ("/flooring-materials/solid-hardwood-flooring-cost/", "Solid Hardwood Cost"),
            ("/flooring-materials/luxury-vinyl-plank-flooring-cost/", "LVP Flooring Cost"),
            ("/flooring-materials/engineered-wood-flooring-cost/", "Engineered Wood Cost"),
            ("/flooring-cost-calculator/", "Flooring Calculator"),
        ],
        "regional": {
            "national": "Acclimate boards 3–7 days before nail-down install",
            "dallas": "White oak and wider planks trending in new builds",
            "charlotte": "Humidity control important — winter heat dries boards",
        },
        "home_examples": {
            "national": {"sqft": 900, "variant": "oak", "grade": "prefinished", "prep": "minor", "removal": True, "detail": "900 sq ft red oak · tear-out carpet"},
            "dallas": {"sqft": 1100, "variant": "oak", "grade": "wide-plank", "prep": "minor", "removal": False, "detail": "1,100 sq ft wide-plank white oak"},
        },
    },
    {
        "slug": "engineered-wood-flooring-cost",
        "calc_material": "engineered",
        "body_class": "engineered-flooring",
        "material_rate": 5.0,
        "labor_rate": 3.8,
        "short_label": "Engineered wood",
        "title": "Engineered Wood Flooring Cost (2026) — Installed Prices | Estimate Home Costs",
        "description": "Engineered wood flooring cost $7–$11 per sq ft installed. Compare wide plank, herringbone, click-lock over concrete, and city pricing.",
        "keywords": "engineered hardwood cost, engineered wood floor cost per square foot",
        "og_title": "Engineered Wood Flooring Cost (2026)",
        "og_desc": "Stable engineered wood costs for concrete slabs and whole-home installs.",
        "article_headline": "Engineered Wood Flooring Cost (2026)",
        "breadcrumb": "Engineered Wood Cost",
        "breadcrumb_short": "Engineered Wood",
        "h1": "Engineered Wood Flooring",
        "hero_lead": "Engineered wood combines a real hardwood veneer with a stable plywood core — ideal for concrete slabs, basements, and wide-plank modern designs.",
        "hero_range": "$4,000–$4,900",
        "hero_per_ft": "$8–$9.80 per sq ft · 500 sq ft",
        "stats_cost": "$7–$11/sq ft",
        "stat2_label": "Stability",
        "stat2": "Excellent",
        "stats_life": "25–40 years",
        "stats_maint": "Low–moderate",
        "styles_heading": "Engineered Wood Styles",
        "styles_lead": "Plank width and install system affect price and where engineered wood works best.",
        "variants": [
            {"id": "traditional", "name": "Traditional plank", "mult": 1, "tier": "$$ · Standard", "desc": "3–5 in boards", "meta": "Most jobs", "visual": "eng-traditional"},
            {"id": "wide", "name": "Wide plank", "mult": 1.12, "tier": "$$$ · Modern", "desc": "7 in+ boards", "meta": "Open concepts", "visual": "eng-wide"},
            {"id": "herringbone", "name": "Herringbone", "mult": 1.25, "tier": "$$$$ · Designer", "desc": "Pattern layout", "meta": "Luxury entries", "visual": "eng-herringbone"},
            {"id": "click", "name": "Click-lock engineered", "mult": 0.95, "tier": "$ · Fast", "desc": "Floating install", "meta": "DIY-friendly", "visual": "eng-click"},
        ],
        "grades": [
            {"id": "standard", "label": "Standard veneer", "mult": 1, "life": "25 yrs", "best_for": "Budget engineered"},
            {"id": "thick", "label": "Thick wear layer", "mult": 1.14, "life": "30–40 yrs", "best_for": "Refinish 1–2x"},
            {"id": "european", "label": "European oak", "mult": 1.2, "life": "30+ yrs", "best_for": "Premium look"},
        ],
        "grade_label": "Product tier",
        "default_sqft": "500",
        "calc_heading": "Typical Engineered Wood Flooring Cost",
        "calc_lead": "Enter square footage, style, product tier, and city.",
        "variant_label": "Plank style",
        "calc_default_range": "$4,000–$4,900",
        "calc_default_hint": "500 sq ft · Traditional plank · Standard",
        "calc_default_per_sqft": "$8.00–$9.80 per sq ft installed",
        "benchmarks": [
            {"sqft": 500, "price": "$3,500–$5,500", "note": "Main level"},
            {"sqft": 1000, "price": "$7,000–$11,000", "note": "Whole home"},
        ],
        "factors": """            <li>Veneer thickness</li>
            <li>Plank width</li>
            <li>Pattern labor</li>
            <li>Moisture barrier</li>
            <li>Removal</li>""",
        "design_heading": "Engineered Wood Finishes",
        "design_lead": "European oak and wire-brushed textures dominate current remodels.",
        "colors": [
            {"class": "eng-natural", "name": "Natural oak", "note": "Light neutral"},
            {"class": "eng-smoke", "name": "Smoked", "note": "Gray-brown"},
            {"class": "eng-chocolate", "name": "Chocolate", "note": "Warm dark"},
            {"class": "eng-blonde", "name": "Blonde", "note": "Scandinavian"},
        ],
        "pros_heading": "Engineered Wood Pros & Cons",
        "pros": """              <li>Stable on concrete slabs</li>
              <li>Real wood veneer appearance</li>
              <li>Faster than solid nail-down</li>
              <li>Works in more rooms than solid</li>""",
        "cons": """              <li>Limited refinish vs solid</li>
              <li>Thin veneers cannot be sanded repeatedly</li>
              <li>Still not for standing water</li>""",
        "detail_table": {
            "heading": "Engineered Product Tier Comparison",
            "lead": "Installed cost per sq ft — based on calculator settings.",
            "col1": "Tier",
            "col2": "Lifespan",
        },
        "install_heading": "Engineered Installation Methods",
        "install_cards": """          <article class="flooring-install-card flooring-install-card--featured"><h3>Floating click-lock</h3><p class="flooring-install-meta">$$ · Fast</p><p>Over underlayment on concrete or plywood.</p></article>
          <article class="flooring-install-card"><h3>Glue-down</h3><p class="flooring-install-meta">$$$ · Permanent</p><p>Best for commercial and large open areas.</p></article>
          <article class="flooring-install-card"><h3>Nail / staple</h3><p class="flooring-install-meta">$$$ · Plywood only</p><p>Some thick engineered installs over wood subfloor.</p></article>
          <article class="flooring-install-card"><h3>Moisture barrier</h3><p class="flooring-install-meta">Add-on</p><p>Required on slab — adds $0.35–$0.75/sq ft.</p></article>""",
        "compare_heading": "Engineered Wood vs Other Flooring",
        "comparisons": [
            {"href": "/flooring-materials/solid-hardwood-flooring-cost/", "title": "Engineered vs Solid Hardwood", "desc": "Stability and cost trade-offs.", "cta": "Hardwood guide"},
            {"href": "/flooring-materials/luxury-vinyl-plank-flooring-cost/", "title": "Engineered vs LVP", "desc": "Real veneer vs vinyl plank.", "cta": "LVP guide"},
            {"href": "/flooring-cost-calculator/?material=engineered", "title": "Flooring calculator", "desc": "Compare all types.", "cta": "Open calculator"},
        ],
        "rooms_heading": "Best Rooms for Engineered Wood",
        "rooms_lead": "Engineered handles more of the home than solid hardwood.",
        "rooms_cards": """          <article class="flooring-room-card flooring-room-card--featured"><h3>Living areas</h3><p>Open plans</p></article>
          <article class="flooring-room-card"><h3>Basements</h3><p>With moisture barrier</p></article>
          <article class="flooring-room-card"><h3>Kitchens</h3><p>Check product rating</p></article>
          <article class="flooring-room-card"><h3>Bedrooms</h3><p>Wide plank popular</p></article>
          <article class="flooring-room-card"><h3>Stairs</h3><p>Matching treads</p></article>""",
        "projects_heading": "Real Engineered Wood Projects",
        "project_nat_type": "1,000 sq ft European oak",
        "project_nat_detail": "Click-lock over slab",
        "project_nat_cost": "$8,900",
        "faq_heading": "Engineered Wood FAQ",
        "faq": [
            {"q": "How much does engineered wood flooring cost?", "a": "Engineered wood typically costs <strong>$7–$11 per sq ft</strong> installed.", "plain": "Engineered wood typically costs $7–$11 per sq ft installed."},
            {"q": "Can engineered wood be refinished?", "a": "Depends on <strong>wear layer thickness</strong> — 3 mm+ may allow one light sand.", "plain": "Wear layer 3 mm+ may allow one light refinish."},
            {"q": "Is engineered better than solid on concrete?", "a": "Yes — <strong>engineered</strong> is the standard choice for slab homes.", "plain": "Engineered is standard for concrete slab homes."},
        ],
        "cta_lead": "Calculator with engineered wood pre-selected.",
        "related": [
            ("/flooring-materials/engineered-wood-flooring-cost/", "Engineered Wood Cost"),
            ("/flooring-materials/solid-hardwood-flooring-cost/", "Solid Hardwood"),
            ("/flooring-materials/luxury-vinyl-plank-flooring-cost/", "LVP Cost"),
            ("/flooring-cost-calculator/", "Flooring Calculator"),
        ],
        "regional": {
            "national": "Always use manufacturer-approved moisture barrier on slab",
            "austin": "Wide-plank European oak popular in remodels",
            "tampa": "Engineered over slab with rated underlayment",
        },
        "home_examples": {
            "national": {"sqft": 1000, "variant": "traditional", "grade": "standard", "prep": "minor", "removal": False, "detail": "1,000 sq ft click-lock · living + halls"},
            "austin": {"sqft": 1200, "variant": "wide", "grade": "european", "prep": "minor", "removal": True, "detail": "1,200 sq ft wide plank · wood-look"},
        },
    },
    {
        "slug": "porcelain-tile-flooring-cost",
        "calc_material": "tile",
        "body_class": "tile-flooring",
        "material_rate": 5.5,
        "labor_rate": 4.2,
        "short_label": "Porcelain tile",
        "title": "Porcelain Tile Flooring Cost (2026) — Installed Prices | Estimate Home Costs",
        "description": "Porcelain tile flooring cost $8–$12 per sq ft installed. Compare large format, wood-look tile, mud-set labor, and city pricing.",
        "keywords": "porcelain tile floor cost, tile installation cost per square foot",
        "og_title": "Porcelain Tile Flooring Cost (2026)",
        "og_desc": "Durable porcelain tile installed costs for kitchens, baths, and whole-home.",
        "article_headline": "Porcelain Tile Flooring Cost (2026)",
        "breadcrumb": "Porcelain Tile Cost",
        "breadcrumb_short": "Porcelain Tile",
        "h1": "Porcelain Tile Flooring",
        "hero_lead": "Porcelain tile delivers maximum durability and water resistance — the go-to floor for kitchens, baths, entryways, and high-traffic modern homes.",
        "hero_range": "$4,350–$5,300",
        "hero_per_ft": "$8.70–$10.60 per sq ft · 500 sq ft",
        "stats_cost": "$8–$12/sq ft",
        "stat2_label": "Water resistance",
        "stat2": "Excellent",
        "stats_life": "30+ years",
        "stats_maint": "Low",
        "styles_heading": "Porcelain Tile Styles",
        "styles_lead": "Tile size and install method strongly affect labor cost.",
        "variants": [
            {"id": "standard", "name": "Standard porcelain", "mult": 1, "tier": "$$ · Classic", "desc": "12x24 in formats", "meta": "Versatile", "visual": "tile-standard"},
            {"id": "large", "name": "Large format", "mult": 1.15, "tier": "$$$ · Modern", "desc": "24x48 in+ slabs", "meta": "Fewer grout lines", "visual": "tile-large"},
            {"id": "wood-look", "name": "Wood-look tile", "mult": 1.08, "tier": "$$ · Popular", "desc": "Plank-shaped porcelain", "meta": "Wet areas", "visual": "tile-wood"},
            {"id": "mosaic", "name": "Mosaic / accent", "mult": 1.22, "tier": "$$$$ · Detail", "desc": "Small format sheets", "meta": "Showers & niches", "visual": "tile-mosaic"},
        ],
        "grades": [
            {"id": "standard", "label": "PEI 3–4 residential", "mult": 1, "life": "25+ yrs", "best_for": "Most homes"},
            {"id": "premium", "label": "PEI 5 / commercial", "mult": 1.12, "life": "30+ yrs", "best_for": "Heavy traffic"},
            {"id": "rectified", "label": "Rectified large format", "mult": 1.18, "life": "30+ yrs", "best_for": "Minimal grout"},
        ],
        "grade_label": "Tile grade",
        "default_sqft": "500",
        "calc_heading": "Typical Porcelain Tile Flooring Cost",
        "calc_lead": "Enter area, tile style, grade, prep, and city.",
        "variant_label": "Tile style",
        "calc_default_range": "$4,350–$5,300",
        "calc_default_hint": "500 sq ft · Standard porcelain",
        "calc_default_per_sqft": "$8.70–$10.60 per sq ft installed",
        "benchmarks": [
            {"sqft": 500, "price": "$4,000–$6,000", "note": "Kitchen + bath"},
            {"sqft": 1000, "price": "$8,000–$12,000", "note": "Whole home tile"},
        ],
        "factors": """            <li>Tile size</li>
            <li>Pattern complexity</li>
            <li>Grout &amp; sealing</li>
            <li>Subfloor flattening</li>
            <li>Removal of old tile</li>""",
        "design_heading": "Popular Tile Looks",
        "design_lead": "Marble, concrete, and wood-look porcelain dominate 2026 trends.",
        "colors": [
            {"class": "tile-marble", "name": "Marble look", "note": "Calacatta style"},
            {"class": "tile-concrete", "name": "Concrete gray", "note": "Industrial"},
            {"class": "tile-wood", "name": "Wood plank tile", "note": "Waterproof wood aesthetic"},
            {"class": "tile-terracotta", "name": "Warm terracotta", "note": "Mediterranean"},
        ],
        "pros_heading": "Porcelain Tile Pros & Cons",
        "pros": """              <li>Extremely durable</li>
              <li>Waterproof when grouted/sealed</li>
              <li>Ideal for kitchens & baths</li>
              <li>Works with radiant heat</li>""",
        "cons": """              <li>Higher labor cost than LVP</li>
              <li>Hard underfoot — area rugs help</li>
              <li>Grout maintenance required</li>""",
        "special_section": {
            "id": "waterproof",
            "heading": "Waterproof Performance",
            "lead": "Porcelain tile is one of the <strong>best waterproof flooring options</strong> when installed with proper membrane and grout care.",
            "list": """            <li><strong>Kitchens:</strong> Spill and splash resistant</li>
            <li><strong>Bathrooms:</strong> Standard for showers and floors</li>
            <li><strong>Entryways:</strong> Mud and rain tolerance</li>
            <li><strong>Laundry:</strong> Appliance leak protection</li>""",
        },
        "detail_table": {
            "heading": "Porcelain Tile Grade Comparison",
            "lead": "Installed cost per sq ft from calculator settings.",
            "col1": "Grade",
            "col2": "Best for",
        },
        "install_heading": "Tile Installation Methods",
        "install_cards": """          <article class="flooring-install-card flooring-install-card--featured"><h3>Thinset mud-set</h3><p class="flooring-install-meta">$$$ · Standard</p><p>Most common for floor tile over membrane.</p></article>
          <article class="flooring-install-card"><h3>Large-format</h3><p class="flooring-install-meta">$$$$ · Skilled crew</p><p>Requires flat subfloor and two-person sets.</p></article>
          <article class="flooring-install-card"><h3>Heated floor</h3><p class="flooring-install-meta">Add-on</p><p>Radiant mat under tile — luxury baths.</p></article>
          <article class="flooring-install-card"><h3>Removal</h3><p class="flooring-install-meta">$$$ · Labor</p><p>Old tile removal adds $1.50+/sq ft.</p></article>""",
        "compare_heading": "Tile vs Other Flooring",
        "comparisons": [
            {"href": "/flooring-materials/luxury-vinyl-plank-flooring-cost/", "title": "Tile vs LVP", "desc": "Porcelain durability vs vinyl speed.", "cta": "LVP guide"},
            {"href": "/flooring-materials/solid-hardwood-flooring-cost/", "title": "Tile vs Hardwood", "desc": "Wet-area winner vs wood warmth.", "cta": "Hardwood guide"},
            {"href": "/flooring-cost-calculator/?material=tile", "title": "Calculator", "desc": "Compare materials.", "cta": "Open calculator"},
        ],
        "rooms_heading": "Best Rooms for Porcelain Tile",
        "rooms_lead": "Where tile is the clear winner.",
        "rooms_cards": """          <article class="flooring-room-card flooring-room-card--featured"><h3>Kitchens</h3><p>#1 choice</p></article>
          <article class="flooring-room-card flooring-room-card--featured"><h3>Bathrooms</h3><p>Shower &amp; floor</p></article>
          <article class="flooring-room-card"><h3>Entryways</h3><p>Heavy traffic</p></article>
          <article class="flooring-room-card"><h3>Laundry</h3><p>Moisture safe</p></article>
          <article class="flooring-room-card"><h3>Open living</h3><p>Large format flow</p></article>""",
        "projects_heading": "Real Porcelain Tile Projects",
        "project_nat_type": "650 sq ft kitchen + bath",
        "project_nat_detail": "Large format · mud-set",
        "project_nat_cost": "$6,800",
        "faq_heading": "Porcelain Tile FAQ",
        "faq": [
            {"q": "How much does porcelain tile flooring cost?", "a": "Porcelain tile typically costs <strong>$8–$12 per sq ft</strong> installed.", "plain": "Porcelain tile typically costs $8–$12 per sq ft installed."},
            {"q": "Is porcelain tile waterproof?", "a": "The tile body is <strong>waterproof</strong>; grout joints need sealing for full moisture protection.", "plain": "Tile body is waterproof; grout needs sealing."},
            {"q": "Tile vs LVP in kitchen?", "a": "Tile wins on <strong>durability and heat</strong>; LVP wins on cost and softer feel.", "plain": "Tile wins durability; LVP wins cost and comfort."},
        ],
        "cta_lead": "Calculator with porcelain tile pre-selected.",
        "related": [
            ("/flooring-materials/porcelain-tile-flooring-cost/", "Porcelain Tile Cost"),
            ("/flooring-materials/luxury-vinyl-plank-flooring-cost/", "LVP Cost"),
            ("/flooring-cost-calculator/", "Flooring Calculator"),
        ],
        "regional": {
            "national": "Floor flattening to 1/8 in in 10 ft is typical spec",
            "tampa": "Wood-look plank tile popular on slab homes",
            "phoenix": "Large format reduces grout in dust-prone climates",
        },
        "home_examples": {
            "national": {"sqft": 650, "variant": "large", "grade": "rectified", "prep": "major", "removal": True, "detail": "650 sq ft large format · kitchen + bath"},
            "tampa": {"sqft": 800, "variant": "wood-look", "grade": "standard", "prep": "minor", "removal": False, "detail": "800 sq ft wood-look tile · main level"},
        },
    },
    {
        "slug": "carpet-flooring-cost",
        "calc_material": "carpet",
        "body_class": "carpet-flooring",
        "material_rate": 2.5,
        "labor_rate": 1.8,
        "short_label": "Carpet",
        "title": "Carpet Flooring Cost (2026) — Installed Prices | Estimate Home Costs",
        "description": "Carpet installation cost $4–$6 per sq ft in 2026. Compare plush, berber, nylon vs polyester, pad, and city pricing.",
        "keywords": "carpet installation cost, carpet cost per square foot, berber carpet cost",
        "og_title": "Carpet Flooring Cost (2026)",
        "og_desc": "Budget-friendly carpet installed costs — styles, fiber types, and padding.",
        "article_headline": "Carpet Flooring Cost (2026)",
        "breadcrumb": "Carpet Flooring Cost",
        "breadcrumb_short": "Carpet",
        "h1": "Carpet Flooring",
        "hero_lead": "Carpet is the most affordable soft flooring for bedrooms and stairs — plush comfort with the lowest upfront installed cost per square foot.",
        "hero_range": "$2,000–$2,450",
        "hero_per_ft": "$4.00–$4.90 per sq ft · 500 sq ft",
        "stats_cost": "$4–$6/sq ft",
        "stat2_label": "Comfort",
        "stat2": "High",
        "stats_life": "10–15 years",
        "stats_maint": "Moderate",
        "styles_heading": "Carpet Styles",
        "styles_lead": "Pile style and fiber type determine feel, durability, and price.",
        "variants": [
            {"id": "plush", "name": "Plush / saxony", "mult": 1, "tier": "$ · Soft", "desc": "Formal look", "meta": "Bedrooms", "visual": "carpet-plush"},
            {"id": "berber", "name": "Berber loop", "mult": 0.95, "tier": "$ · Durable", "desc": "Loop pile", "meta": "Basements", "visual": "carpet-berber"},
            {"id": "frieze", "name": "Frieze", "mult": 1.05, "tier": "$$ · Casual", "desc": "Twisted fiber", "meta": "Hides footprints", "visual": "carpet-frieze"},
            {"id": "pattern", "name": "Pattern / cut-loop", "mult": 1.12, "tier": "$$ · Designer", "desc": "Visual interest", "meta": "Formal areas", "visual": "carpet-pattern"},
        ],
        "grades": [
            {"id": "polyester", "label": "Polyester", "mult": 0.92, "life": "10–12 yrs", "best_for": "Budget rooms"},
            {"id": "nylon", "label": "Nylon", "mult": 1, "life": "12–15 yrs", "best_for": "High traffic"},
            {"id": "wool", "label": "Wool blend", "mult": 1.35, "life": "15–20 yrs", "best_for": "Premium comfort"},
        ],
        "grade_label": "Fiber type",
        "default_sqft": "500",
        "calc_heading": "Typical Carpet Flooring Cost",
        "calc_lead": "Enter square footage, carpet style, fiber, and city.",
        "variant_label": "Carpet style",
        "calc_default_range": "$2,000–$2,450",
        "calc_default_hint": "500 sq ft · Plush · Nylon",
        "calc_default_per_sqft": "$4.00–$4.90 per sq ft installed",
        "benchmarks": [
            {"sqft": 500, "price": "$2,000–$3,000", "note": "Bedrooms"},
            {"sqft": 1000, "price": "$3,900–$4,800", "note": "Whole home"},
        ],
        "factors": """            <li>Fiber type</li>
            <li>Pad quality</li>
            <li>Stairs</li>
            <li>Removal</li>
            <li>Moving furniture</li>""",
        "design_heading": "Popular Carpet Colors",
        "design_lead": "Neutral grays and warm taupes dominate new installs.",
        "colors": [
            {"class": "carpet-gray", "name": "Greige", "note": "Most popular"},
            {"class": "carpet-taupe", "name": "Warm taupe", "note": "Versatile"},
            {"class": "carpet-cream", "name": "Cream", "note": "Brightens rooms"},
            {"class": "carpet-charcoal", "name": "Charcoal", "note": "Hides stains"},
        ],
        "pros_heading": "Carpet Pros & Cons",
        "pros": """              <li>Lowest upfront cost</li>
              <li>Soft and warm underfoot</li>
              <li>Sound dampening</li>
              <li>Fast install</li>""",
        "cons": """              <li>Stains and wear show over time</li>
              <li>Not ideal for wet areas</li>
              <li>Lower resale appeal than hard surfaces</li>""",
        "detail_table": {
            "heading": "Carpet Fiber Comparison",
            "lead": "Installed cost per sq ft from calculator.",
            "col1": "Fiber",
            "col2": "Lifespan",
        },
        "install_heading": "Carpet Installation",
        "install_cards": """          <article class="flooring-install-card flooring-install-card--featured"><h3>Stretch-in</h3><p class="flooring-install-meta">$ · Standard</p><p>Tack strip perimeter — most residential wall-to-wall.</p></article>
          <article class="flooring-install-card"><h3>Pad upgrade</h3><p class="flooring-install-meta">$ · Add-on</p><p>8 lb pad vs 6 lb — better feel and life.</p></article>
          <article class="flooring-install-card"><h3>Stairs</h3><p class="flooring-install-meta">$$$ · Labor</p><p>Waterfall or Hollywood style per step.</p></article>
          <article class="flooring-install-card"><h3>Removal</h3><p class="flooring-install-meta">$ · Quick</p><p>Old carpet + pad tear-out before stretch-in.</p></article>""",
        "compare_heading": "Carpet vs Other Flooring",
        "comparisons": [
            {"href": "/flooring-materials/luxury-vinyl-plank-flooring-cost/", "title": "Carpet vs LVP", "desc": "Soft budget vs durable hard surface.", "cta": "LVP guide"},
            {"href": "/flooring-materials/solid-hardwood-flooring-cost/", "title": "Carpet vs Hardwood", "desc": "Comfort vs resale value.", "cta": "Hardwood guide"},
            {"href": "/flooring-cost-calculator/?material=carpet", "title": "Calculator", "desc": "Compare all flooring.", "cta": "Open calculator"},
        ],
        "rooms_heading": "Best Rooms for Carpet",
        "rooms_lead": "Where carpet still wins.",
        "rooms_cards": """          <article class="flooring-room-card flooring-room-card--featured"><h3>Bedrooms</h3><p>Comfort #1</p></article>
          <article class="flooring-room-card"><h3>Stairs</h3><p>Safety &amp; sound</p></article>
          <article class="flooring-room-card"><h3>Basements</h3><p>Berber loop · dry only</p></article>
          <article class="flooring-room-card"><h3>Playrooms</h3><p>Soft landing</p></article>
          <article class="flooring-room-card"><h3>Formal living</h3><p>Plush upgrade</p></article>""",
        "pet_section": True,
        "pet_heading": "Family & Pet Considerations",
        "pet_lead": "Choose the right fiber and pad when kids and pets share the space.",
        "pet_list": """            <li><strong>Nylon fiber</strong> — best stain resistance in residential carpet</li>
            <li><strong>Stain treatments</strong> — factory applied adds cost but saves replacement</li>
            <li><strong>Low pile</strong> — easier to vacuum pet hair</li>
            <li><strong>Pad density</strong> — 8 lb pad extends life in high traffic</li>""",
        "projects_heading": "Real Carpet Projects",
        "project_nat_type": "800 sq ft nylon plush",
        "project_nat_detail": "Bedrooms + stairs",
        "project_nat_cost": "$3,600",
        "faq_heading": "Carpet FAQ",
        "faq": [
            {"q": "How much does carpet cost installed?", "a": "Carpet typically costs <strong>$4–$6 per sq ft</strong> installed with pad.", "plain": "Carpet typically costs $4–$6 per sq ft installed with pad."},
            {"q": "Nylon vs polyester carpet?", "a": "<strong>Nylon</strong> lasts longer in hallways; polyester saves money in low-traffic bedrooms.", "plain": "Nylon lasts longer; polyester saves money in bedrooms."},
            {"q": "How long does carpet last?", "a": "Most residential carpet lasts <strong>10–15 years</strong> depending on fiber and traffic.", "plain": "Most residential carpet lasts 10–15 years."},
        ],
        "cta_lead": "Calculator with carpet pre-selected.",
        "related": [
            ("/flooring-materials/carpet-flooring-cost/", "Carpet Cost"),
            ("/flooring-materials/luxury-vinyl-plank-flooring-cost/", "LVP Cost"),
            ("/flooring-cost-calculator/", "Flooring Calculator"),
        ],
        "regional": {
            "national": "Include quality pad — often 30% of carpet comfort",
            "charlotte": "Builder-grade polyester common; nylon upgrades in owner suites",
            "houston": "Moisture — avoid carpet in slab baths without remediation",
        },
        "home_examples": {
            "national": {"sqft": 800, "variant": "plush", "grade": "nylon", "prep": "none", "removal": True, "detail": "800 sq ft plush · bedrooms + stairs"},
            "charlotte": {"sqft": 600, "variant": "berber", "grade": "nylon", "prep": "none", "removal": True, "detail": "600 sq ft berber · basement"},
        },
    },
]


def main() -> None:
    for m in MATERIALS:
        out = OUT / m["slug"]
        out.mkdir(parents=True, exist_ok=True)
        html = render(m)
        (out / "index.html").write_text(html, encoding="utf-8")
        print(f"Wrote {out / 'index.html'}")


if __name__ == "__main__":
    main()

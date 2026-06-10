"""E-E-A-T trust content — methodology, data sources, and reusable page blocks."""

from __future__ import annotations

from brand import COPYRIGHT_LINE, LOGO_HTML, SITE_NAME, SITE_ORIGIN

LAST_UPDATED = "2026-05-22"
LAST_UPDATED_LABEL = "May 2026"

DATA_SOURCES = [
    {
        "name": "U.S. Bureau of Labor Statistics (BLS)",
        "use": "Construction labor wages and regional employment cost indexes by metro area.",
        "url": "https://www.bls.gov/oes/",
    },
    {
        "name": "U.S. Energy Information Administration (EIA)",
        "use": "Residential electricity rates for solar savings and payback calculations.",
        "url": "https://www.eia.gov/electricity/state/",
    },
    {
        "name": "NREL / Lawrence Berkeley National Laboratory",
        "use": "Solar photovoltaic installed cost and $/watt benchmarks (Tracking the Sun).",
        "url": "https://emp.lbl.gov/tracking-the-sun",
    },
    {
        "name": "RSMeans / Gordian construction cost data",
        "use": "National unit costs for roofing, HVAC, flooring, fencing, and remodeling assemblies.",
        "url": "https://www.gordian.com/products/rsmeans-data/",
    },
    {
        "name": "Remodeling Magazine Cost vs. Value",
        "use": "Kitchen and bathroom remodel cost benchmarks by project scope.",
        "url": "https://www.remodeling.hw.net/cost-vs-value/2024/",
    },
    {
        "name": "NAHB construction cost surveys",
        "use": "Single-family construction and renovation cost trends.",
        "url": "https://www.nahb.org/news-and-economics/housing-economics",
    },
    {
        "name": "Municipal & county permit fee schedules",
        "use": "Published building, mechanical, and electrical permit fees for major metros.",
        "url": None,
    },
    {
        "name": "IRS Residential Clean Energy Credit",
        "use": "30% federal investment tax credit for qualifying solar and battery installations.",
        "url": "https://www.irs.gov/credits-deductions/residential-clean-energy-credit",
    },
    {
        "name": "Manufacturer & distributor pricing",
        "use": "Wholesale material pricing for asphalt shingles, LVP, HVAC equipment, and fence panels.",
        "url": None,
    },
    {
        "name": "Contractor bid validation (internal)",
        "use": "Anonymized project quotes cross-checked against calculator output in target metros.",
        "url": None,
    },
]

METHODOLOGY_STEPS = [
    (
        "Establish national baselines",
        "We start with 2026 national installed-cost benchmarks for each project type — roofing ($/sq ft), "
        "HVAC ($/sq ft by system), kitchen/bath remodels (by size and scope), flooring ($/sq ft by material), "
        "fencing ($/linear ft), and solar ($/watt). Baselines reflect mid-grade materials and standard labor.",
    ),
    (
        "Apply metro multipliers",
        "City and state pages apply material, labor, and permit multipliers derived from BLS wage data, "
        "regional cost indexes, and published permit schedules. Multipliers are maintained in a single "
        "pricing file shared by all calculators and landing pages.",
    ),
    (
        "Run project-specific formulas",
        "Each calculator applies scope inputs — roof pitch, HVAC efficiency, remodel level, fence height, "
        "solar system size — using the same JavaScript formulas that power live estimates. Python "
        "generators mirror these formulas for snapshot cards and example projects on city pages.",
    ),
    (
        "Validate and calibrate",
        "Output ranges are compared against industry reports and anonymized contractor quotes. We target "
        "±10–15% of typical on-site bids when inputs match real project scope. Outliers are reviewed quarterly.",
    ),
    (
        "Publish with transparency",
        "Every estimate shows what is included (materials, labor, permits, tear-off, etc.). We link to this "
        "methodology and our data sources from calculators, city hubs, and state guides.",
    ),
]

LIMITATIONS = [
    "Calculators provide budget ranges, not binding quotes — site conditions, code requirements, and "
    "contractor overhead can change final price.",
    "Historic or custom homes, structural changes, and specialty materials may fall outside model assumptions.",
    "Permit fees vary by jurisdiction and project valuation; we use typical residential fees, not exact city quotes.",
    "Solar payback depends on utility rate plans, net metering rules, and roof condition — verify with your utility.",
    "Prices are updated quarterly; fast-moving markets (labor shortages, tariff changes) may lag by one review cycle.",
]


def trust_callout_html(*, prefix: str = "") -> str:
    """Compact E-E-A-T block for calculators and landing pages."""
    meth = f"{prefix}/methodology/" if prefix else "/methodology/"
    src = f"{prefix}/data-sources/" if prefix else "/data-sources/"
    return f"""    <section class="trust-methodology-section" aria-labelledby="methodology-trust-heading">
      <div class="container">
        <div class="trust-callout">
          <p class="trust-callout-eyebrow">Transparent pricing</p>
          <h2 id="methodology-trust-heading">How we calculate costs</h2>
          <p>
            Estimates combine <strong>national installed-cost benchmarks</strong> with
            <strong>metro-specific labor, material, and permit multipliers</strong> drawn from
            BLS wage data, EIA utility rates, NREL solar benchmarks, and RSMeans-style unit costs.
            City and state pages use the same formulas as our live calculators.
          </p>
          <ul class="trust-callout-list">
            <li>Material + labor rates calibrated to 2026 U.S. market medians</li>
            <li>25 metro areas with published multipliers — not generic national averages</li>
            <li>Ranges validated against industry benchmarks (±10–15% typical variance)</li>
            <li>Updated quarterly — last review <time datetime="{LAST_UPDATED}">{LAST_UPDATED_LABEL}</time></li>
          </ul>
          <p class="trust-callout-links">
            <a href="{meth}">Full methodology</a>
            <span aria-hidden="true">·</span>
            <a href="{src}">Data sources</a>
          </p>
        </div>
      </div>
    </section>
"""


def _source_item(src: dict) -> str:
    name = src["name"]
    use = src["use"]
    url = src.get("url")
    if url:
        name_html = f'<a href="{url}" rel="noopener noreferrer">{name}</a>'
    else:
        name_html = name
    return f"""          <li class="source-list-item">
            <h3>{name_html}</h3>
            <p>{use}</p>
          </li>\n"""


def _methodology_step(i: int, title: str, body: str) -> str:
    return f"""          <li class="methodology-step">
            <span class="methodology-step-num" aria-hidden="true">{i}</span>
            <div>
              <h3>{title}</h3>
              <p>{body}</p>
            </div>
          </li>\n"""


def _page_shell(title: str, description: str, canonical_path: str, breadcrumb_label: str, main_html: str) -> str:
    canonical = f"{SITE_ORIGIN}{canonical_path}"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | {SITE_NAME}</title>
  <meta name="description" content="{description}">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{canonical}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:url" content="{canonical}">
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
        "@type": "WebPage",
        "name": "{title}",
        "url": "{canonical}",
        "description": "{description}",
        "dateModified": "{LAST_UPDATED}",
        "publisher": {{ "@type": "Organization", "name": "{SITE_NAME}", "url": "{SITE_ORIGIN}/" }}
      }},
      {{
        "@type": "BreadcrumbList",
        "itemListElement": [
          {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "{SITE_ORIGIN}/" }},
          {{ "@type": "ListItem", "position": 2, "name": "{breadcrumb_label}", "item": "{canonical}" }}
        ]
      }}
    ]
  }}
  </script>
</head>
<body>
  <a href="#main" class="skip-link">Skip to main content</a>
  <header class="site-header" role="banner">
    <div class="container header-inner">
      <a href="/" class="logo" aria-label="{SITE_NAME} — Home"><span class="logo-text">{LOGO_HTML}</span></a>
      <nav class="site-nav" aria-label="Main">
        <a href="/#calculators">Calculators</a>
        <a href="/methodology/">Methodology</a>
        <a href="/data-sources/">Data Sources</a>
      </nav>
    </div>
  </header>

  <main id="main">
{main_html}
  </main>

  <footer class="site-footer" role="contentinfo">
    <div class="container footer-grid">
      <div class="footer-brand">
        <a href="/" class="logo logo--footer"><span class="logo-text">{LOGO_HTML}</span></a>
        <p>Transparent home project cost estimates for homeowners across the United States.</p>
      </div>
      <nav aria-labelledby="footer-trust">
        <h3 id="footer-trust">Trust &amp; transparency</h3>
        <ul>
          <li><a href="/methodology/">Methodology</a></li>
          <li><a href="/data-sources/">Data Sources</a></li>
          <li><a href="/#calculators">Calculators</a></li>
        </ul>
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
  <script src="/js/main.js" defer></script>
</body>
</html>
"""


def render_methodology_page() -> str:
    steps = "".join(_methodology_step(i, t, b) for i, (t, b) in enumerate(METHODOLOGY_STEPS, 1))
    limits = "".join(f"          <li>{lim}</li>\n" for lim in LIMITATIONS)
    main = f"""    <article class="editorial-page">
      <div class="container editorial-page-inner">
        <nav class="breadcrumb" aria-label="Breadcrumb">
          <ol>
            <li><a href="/">Home</a></li>
            <li aria-current="page">Methodology</li>
          </ol>
        </nav>
        <header class="editorial-header">
          <p class="editorial-eyebrow">Trust &amp; transparency</p>
          <h1>Our cost estimation methodology</h1>
          <p class="editorial-lead">
            {SITE_NAME} publishes localized home improvement cost ranges using documented formulas,
            public data sources, and regular calibration against real project pricing. This page explains
            exactly how we build estimates — so you can judge accuracy before finalizing your project budget.
          </p>
          <p class="editorial-meta">Last updated: <time datetime="{LAST_UPDATED}">{LAST_UPDATED_LABEL}</time></p>
        </header>

        <section class="editorial-section" aria-labelledby="process-heading">
          <h2 id="process-heading">Five-step process</h2>
          <ol class="methodology-steps">{steps}        </ol>
        </section>

        <section class="editorial-section" aria-labelledby="calculators-heading">
          <h2 id="calculators-heading">Calculator-specific models</h2>
          <div class="editorial-cards">
            <article class="editorial-card">
              <h3>Roofing</h3>
              <p>Material and labor $/sq ft by roofing type, multiplied by pitch, complexity, stories, and tear-off. City permit fees added as a flat line item. ±10% range band.</p>
            </article>
            <article class="editorial-card">
              <h3>HVAC</h3>
              <p>System rate × home sq ft × efficiency tier × metro multiplier, plus optional ductwork and permit fees. SEER tiers reflect 2026 equipment pricing.</p>
            </article>
            <article class="editorial-card">
              <h3>Kitchen &amp; bath remodels</h3>
              <p>Base project cost by room size and scope level, adjusted for cabinets, countertops, layout changes, and location multiplier from metro labor index.</p>
            </article>
            <article class="editorial-card">
              <h3>Flooring &amp; fencing</h3>
              <p>Material + labor unit rates per sq ft or linear ft, with prep, removal, height, and terrain modifiers. Permit scaled from metro fee tables.</p>
            </article>
            <article class="editorial-card">
              <h3>Solar</h3>
              <p>System size from usage, $/watt by metro, EIA electricity rates, sun exposure multipliers, optional battery storage, and 30% federal ITC.</p>
            </article>
          </div>
        </section>

        <section class="editorial-section" aria-labelledby="limitations-heading">
          <h2 id="limitations-heading">Limitations &amp; disclaimers</h2>
          <ul class="editorial-list">{limits}        </ul>
        </section>

        <section class="editorial-section editorial-cta">
          <h2>Primary data sources</h2>
          <p>We cite public and industry benchmarks on our dedicated data sources page.</p>
          <a href="/data-sources/" class="btn btn-primary">View data sources</a>
        </section>
      </div>
    </article>"""
    return _page_shell(
        "Cost Estimation Methodology",
        "How Estimate Home Costs calculates roofing, HVAC, remodeling, flooring, fencing, and solar estimates using BLS labor data, RSMeans benchmarks, and metro multipliers.",
        "/methodology/",
        "Methodology",
        main,
    )


def render_data_sources_page() -> str:
    sources = "".join(_source_item(s) for s in DATA_SOURCES)
    main = f"""    <article class="editorial-page">
      <div class="container editorial-page-inner">
        <nav class="breadcrumb" aria-label="Breadcrumb">
          <ol>
            <li><a href="/">Home</a></li>
            <li aria-current="page">Data Sources</li>
          </ol>
        </nav>
        <header class="editorial-header">
          <p class="editorial-eyebrow">Trust &amp; transparency</p>
          <h1>Data sources</h1>
          <p class="editorial-lead">
            Our cost models combine government statistics, industry cost databases, utility rate data,
            and internal bid validation. Below are the primary references we use to set national baselines
            and metro-level multipliers for {SITE_NAME} calculators and city guides.
          </p>
          <p class="editorial-meta">Last updated: <time datetime="{LAST_UPDATED}">{LAST_UPDATED_LABEL}</time></p>
        </header>

        <section class="editorial-section" aria-labelledby="sources-heading">
          <h2 id="sources-heading">Referenced sources</h2>
          <ul class="source-list">{sources}        </ul>
        </section>

        <section class="editorial-section" aria-labelledby="refresh-heading">
          <h2 id="refresh-heading">Update schedule</h2>
          <p>
            National unit costs and metro multipliers are reviewed <strong>quarterly</strong>.
            Electricity rates follow EIA published averages. Solar $/watt benchmarks align with
            the latest NREL Tracking the Sun report. When a metro shows &gt;5% drift from
            validated bids, multipliers are adjusted in the same review cycle.
          </p>
        </section>

        <section class="editorial-section editorial-cta">
          <h2>How sources feed our models</h2>
          <p>See the step-by-step process we use to turn raw data into localized estimates.</p>
          <a href="/methodology/" class="btn btn-primary">Read methodology</a>
        </section>
      </div>
    </article>"""
    return _page_shell(
        "Data Sources",
        "Primary data sources for Estimate Home Costs: BLS labor data, EIA electricity rates, NREL solar benchmarks, RSMeans construction costs, and permit fee schedules.",
        "/data-sources/",
        "Data Sources",
        main,
    )

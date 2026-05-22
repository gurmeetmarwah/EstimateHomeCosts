#!/usr/bin/env python3
"""Generate HVAC system landing pages from central-ac template."""

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = (ROOT / "hvac-cost-calculator/central-ac/index.html").read_text()

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

SYSTEMS = {
    "heat-pump": {
        "slug": "heat-pump",
        "title": "Heat Pump Cost Calculator (2026) — Installation Estimate | Estimate Home Costs",
        "description": "Free heat pump cost calculator for 2026. Estimate installation $6,500–$15,000 by home size, SEER/HSPF, ductwork, and city. Heat and cool in one system.",
        "keywords": "heat pump cost calculator, heat pump installation cost, heat pump vs AC cost, ducted heat pump cost",
        "canonical": "https://estimatehomecosts.com/hvac-cost-calculator/heat-pump/",
        "og_title": "Heat Pump Cost Calculator (2026)",
        "og_desc": "Estimate heat pump installation costs by home size, efficiency, ductwork, and local labor rates.",
        "twitter_desc": "Instant heat pump installation estimates with cost breakdown and city-level pricing.",
        "article_headline": "Heat Pump Cost Calculator (2026): Installation Prices & Guide",
        "breadcrumb": "Heat Pump Cost",
        "body_class": "heat-pump-page",
        "name": "Heat Pump",
        "name_lower": "heat pump",
        "eyebrow": "HVAC cost calculator · Heat pump",
        "hero_lead": "Estimate the cost of installing a ducted heat pump system that heats and cools your home from one outdoor unit — based on size, efficiency, ductwork, and local rates.",
        "hero_avg": "$6,500–$15,000",
        "preview_note": "16 SEER · existing ductwork",
        "ton_unit": "Ton heat pump",
        "quick_heading": "Quick Heat Pump Estimate",
        "advanced_heading": "Advanced Heat Pump Calculator",
        "advanced_desc": "Personalize tonnage, efficiency, ductwork, climate, and upgrades for a detailed breakdown with financing.",
        "calc_result_label": "Estimated Heat Pump Cost",
        "what_id": "what-is-heat-pump",
        "what_heading": "What Is a Heat Pump?",
        "what_copy": "A <strong>heat pump</strong> moves heat in and out of your home — cooling in summer and heating in winter from the same ducted system. It replaces separate furnace and AC equipment in many climates.",
        "what_list": """<li><strong>Heating &amp; cooling</strong> — one outdoor unit, year-round comfort</li>
            <li><strong>Ducted distribution</strong> — uses existing ductwork in most installs</li>
            <li><strong>High efficiency</strong> — especially strong in mild and moderate climates</li>""",
        "size_heading": "Heat Pump Cost by Home Size",
        "seer_heading": "Heat Pump Cost by SEER Rating",
        "types_heading": "Heat Pump System Types",
        "types_desc": "Compressor stage affects heating performance, comfort, and price.",
        "pros_heading": "Heat Pump Pros &amp; Cons",
        "pros": """<li>Heating and cooling in one system</li>
              <li>Lower operating cost vs resistance heat in many regions</li>
              <li>Eligible for federal tax credits and rebates (check current programs)</li>
              <li>Works with existing ducts in most homes</li>""",
        "cons": """<li>Higher upfront cost than AC-only replacement</li>
              <li>May need auxiliary heat in very cold climates</li>
              <li>Sizing and refrigerant type matter for cold-weather performance</li>""",
        "compare_heading": "Heat Pump vs Other Systems",
        "comparisons": """<a href="/compare/heat-pump-vs-ac/" class="comparison-card">
            <h3>Heat Pump vs Central AC</h3>
            <p>One system for heat and cool vs cooling-only — compare installed costs.</p>
            <span class="comparison-card-cta">Read comparison →</span>
          </a>
          <a href="/hvac-cost-calculator/central-ac/" class="comparison-card">
            <h3>Heat Pump vs Central AC cost</h3>
            <p>See ducted central AC pricing for cooling-focused replacements.</p>
            <span class="comparison-card-cta">Central AC calculator →</span>
          </a>
          <a href="/hvac-cost-calculator/mini-split/" class="comparison-card">
            <h3>Heat Pump vs Mini Split</h3>
            <p>Ducted whole-home vs ductless zoning.</p>
            <span class="comparison-card-cta">Mini split calculator →</span>
          </a>""",
        "local_heading": "Local Heat Pump Cost Factors",
        "timeline_heading": "Heat Pump Installation Timeline",
        "timeline_install": "Outdoor unit, indoor air handler, refrigerant lines, and commissioning.",
        "brands_heading": "Best Heat Pump Brands",
        "examples_heading": "Real Heat Pump Installation Examples",
        "faq_heading": "Heat Pump Cost FAQ",
        "faq_cost": "Heat pump installation typically costs <strong>$6,500–$15,000</strong> nationally in 2026 for a ducted whole-home system.",
        "faq_size": "Sizing matches central AC: about <strong>1 ton per 500–600 sq ft</strong> in moderate climates.",
        "project_label": "heat pump",
        "system_rate": 4.65,
        "default_ductwork": False,
        "show_ductwork": True,
        "show_stage": True,
        "tile_class": "heat-pump",
        "related_tiles": """<a href="/hvac-cost-calculator/central-ac/" class="type-tile type-tile--central-ac">
            <span class="type-tile-tier">Most popular</span>
            <h3 class="type-tile-title">Central AC</h3>
            <p class="type-tile-meta">Cooling only</p>
            <p class="type-tile-price type-tile-price--link">Open calculator →</p>
          </a>
          <a href="/hvac-cost-calculator/mini-split/" class="type-tile type-tile--mini-split">
            <span class="type-tile-tier">Flexible</span>
            <h3 class="type-tile-title">Mini split</h3>
            <p class="type-tile-meta">Ductless</p>
            <p class="type-tile-price type-tile-price--link">Open calculator →</p>
          </a>
          <a href="/hvac-cost-calculator/furnace-ac/" class="type-tile type-tile--furnace-ac">
            <span class="type-tile-tier">Full HVAC</span>
            <h3 class="type-tile-title">Furnace + AC</h3>
            <p class="type-tile-meta">Gas + central</p>
            <p class="type-tile-price type-tile-price--link">Open calculator →</p>
          </a>
          <a href="/hvac-cost-calculator/" class="type-tile type-tile--guide">
            <span class="type-tile-tier">All systems</span>
            <h3 class="type-tile-title">HVAC replacement</h3>
            <p class="type-tile-meta">Full calculator</p>
            <p class="type-tile-price type-tile-price--link">Open calculator →</p>
          </a>""",
        "systems_grid": """<a href="/hvac-cost-calculator/central-ac/" class="type-tile type-tile--central-ac">
            <span class="type-tile-tier">Cooling</span>
            <h3 class="type-tile-title">Central AC</h3>
            <p class="type-tile-meta">14–18 SEER</p>
            <p class="type-tile-price type-tile-price--link">View costs →</p>
          </a>
          <a href="/hvac-cost-calculator/heat-pump/" class="type-tile type-tile--heat-pump type-tile--current" aria-current="page">
            <span class="type-tile-tier">Efficient</span>
            <h3 class="type-tile-title">Heat pump</h3>
            <p class="type-tile-meta">Heat &amp; cool</p>
            <p class="type-tile-price type-tile-price--link">You are here</p>
          </a>
          <a href="/hvac-cost-calculator/mini-split/" class="type-tile type-tile--mini-split">
            <span class="type-tile-tier">Flexible</span>
            <h3 class="type-tile-title">Mini split</h3>
            <p class="type-tile-meta">Ductless</p>
            <p class="type-tile-price type-tile-price--link">View costs →</p>
          </a>
          <a href="/hvac-cost-calculator/furnace-ac/" class="type-tile type-tile--furnace-ac">
            <span class="type-tile-tier">Full HVAC</span>
            <h3 class="type-tile-title">Furnace + AC</h3>
            <p class="type-tile-meta">Gas + central</p>
            <p class="type-tile-price type-tile-price--link">View costs →</p>
          </a>
          <a href="/hvac-cost-calculator/geothermal/" class="type-tile type-tile--geothermal">
            <span class="type-tile-tier">Premium</span>
            <h3 class="type-tile-title">Geothermal</h3>
            <p class="type-tile-meta">Ground-source</p>
            <p class="type-tile-price type-tile-price--link">View costs →</p>
          </a>""",
        "footer_link": '<li><a href="/hvac-cost-calculator/heat-pump/">Heat Pump Cost</a></li>',
        "regional_national": "Heat pumps growing fast; verify cold-climate ratings below 20°F if applicable",
        "example_nat_type": "16 SEER heat pump · 2,000 sq ft",
    },
    "mini-split": {
        "slug": "mini-split",
        "title": "Mini Split Cost Calculator (2026) — Ductless Install Estimate | Estimate Home Costs",
        "description": "Free ductless mini split cost calculator for 2026. Estimate $3,500–$18,000 per home by zones, SEER, line sets, and city. No ductwork required.",
        "keywords": "mini split cost calculator, ductless mini split installation cost, mini split cost per zone",
        "canonical": "https://estimatehomecosts.com/hvac-cost-calculator/mini-split/",
        "og_title": "Mini Split Cost Calculator (2026)",
        "og_desc": "Estimate ductless mini split installation by zones, efficiency, and location.",
        "twitter_desc": "Ductless mini split cost estimates with live pricing by city.",
        "article_headline": "Mini Split Cost Calculator (2026): Ductless Installation Guide",
        "breadcrumb": "Mini Split Cost",
        "body_class": "mini-split-page",
        "name": "Mini Split",
        "name_lower": "mini split",
        "eyebrow": "HVAC cost calculator · Ductless",
        "hero_lead": "Estimate ductless mini split installation cost by home size, number of zones, SEER rating, and local labor — no existing ductwork required.",
        "hero_avg": "$3,500–$18,000",
        "preview_note": "16 SEER · 2-zone typical",
        "ton_unit": "Ton capacity",
        "quick_heading": "Quick Mini Split Estimate",
        "advanced_heading": "Advanced Mini Split Calculator",
        "advanced_desc": "Adjust zones, efficiency, line-set complexity, and location for a full cost breakdown.",
        "calc_result_label": "Estimated Mini Split Cost",
        "what_id": "what-is-mini-split",
        "what_heading": "What Is a Ductless Mini Split?",
        "what_copy": "A <strong>ductless mini split</strong> uses an outdoor condenser and one or more wall-mounted indoor heads — no ductwork. Ideal for additions, garages, and room-by-room zoning.",
        "what_list": """<li><strong>Zone control</strong> — cool or heat individual rooms independently</li>
            <li><strong>No ducts</strong> — faster install in homes without existing ductwork</li>
            <li><strong>High efficiency</strong> — inverter models common at 18–20+ SEER</li>""",
        "size_heading": "Mini Split Cost by Home Size",
        "seer_heading": "Mini Split Cost by SEER Rating",
        "types_heading": "Mini Split Configuration Types",
        "types_desc": "Single-zone vs multi-zone setups drive total installed cost.",
        "pros_heading": "Mini Split Pros &amp; Cons",
        "pros": """<li>No ductwork required</li>
              <li>Excellent for additions, ADUs, and garages</li>
              <li>Room-by-room temperature control</li>
              <li>Very high efficiency with inverter compressors</li>""",
        "cons": """<li>Multiple indoor units visible on walls</li>
              <li>Whole-home coverage can cost more than one central system</li>
              <li>Line-set routing affects labor and aesthetics</li>""",
        "compare_heading": "Mini Split vs Other Systems",
        "comparisons": """<a href="/hvac-cost-calculator/central-ac/" class="comparison-card">
            <h3>Mini Split vs Central AC</h3>
            <p>Ductless zoning vs whole-home ducted cooling.</p>
            <span class="comparison-card-cta">Central AC calculator →</span>
          </a>
          <a href="/hvac-cost-calculator/heat-pump/" class="comparison-card">
            <h3>Mini Split vs Heat Pump</h3>
            <p>Ductless vs ducted heat pump — which fits your layout?</p>
            <span class="comparison-card-cta">Heat pump calculator →</span>
          </a>
          <a href="/hvac-cost-calculator/" class="comparison-card">
            <h3>All HVAC systems</h3>
            <p>Compare every system type on the main calculator.</p>
            <span class="comparison-card-cta">Full HVAC calculator →</span>
          </a>""",
        "local_heading": "Local Mini Split Cost Factors",
        "timeline_heading": "Mini Split Installation Timeline",
        "timeline_install": "Mount indoor heads, outdoor unit, refrigerant lines, and vacuum test.",
        "brands_heading": "Best Mini Split Brands",
        "examples_heading": "Real Mini Split Installation Examples",
        "faq_heading": "Mini Split Cost FAQ",
        "faq_cost": "Mini split installation typically costs <strong>$3,500–$18,000</strong> depending on zones and home size.",
        "faq_size": "Capacity still scales with home size — multi-zone systems often use <strong>2–4 indoor heads</strong> for a full home.",
        "project_label": "mini split",
        "system_rate": 5.35,
        "default_ductwork": False,
        "show_ductwork": False,
        "show_stage": True,
        "tile_class": "mini-split",
        "ductwork_fieldset": "",
        "related_tiles": """<a href="/hvac-cost-calculator/central-ac/" class="type-tile type-tile--central-ac">
            <span class="type-tile-tier">Most popular</span>
            <h3 class="type-tile-title">Central AC</h3>
            <p class="type-tile-meta">Ducted</p>
            <p class="type-tile-price type-tile-price--link">Open calculator →</p>
          </a>
          <a href="/hvac-cost-calculator/heat-pump/" class="type-tile type-tile--heat-pump">
            <span class="type-tile-tier">Efficient</span>
            <h3 class="type-tile-title">Heat pump</h3>
            <p class="type-tile-meta">Heat &amp; cool</p>
            <p class="type-tile-price type-tile-price--link">Open calculator →</p>
          </a>
          <a href="/hvac-cost-calculator/furnace-ac/" class="type-tile type-tile--furnace-ac">
            <span class="type-tile-tier">Full HVAC</span>
            <h3 class="type-tile-title">Furnace + AC</h3>
            <p class="type-tile-meta">Gas + central</p>
            <p class="type-tile-price type-tile-price--link">Open calculator →</p>
          </a>
          <a href="/hvac-cost-calculator/" class="type-tile type-tile--guide">
            <span class="type-tile-tier">All systems</span>
            <h3 class="type-tile-title">HVAC replacement</h3>
            <p class="type-tile-meta">Full calculator</p>
            <p class="type-tile-price type-tile-price--link">Open calculator →</p>
          </a>""",
        "systems_grid": """<a href="/hvac-cost-calculator/central-ac/" class="type-tile type-tile--central-ac">
            <span class="type-tile-tier">Cooling</span>
            <h3 class="type-tile-title">Central AC</h3>
            <p class="type-tile-meta">Ducted</p>
            <p class="type-tile-price type-tile-price--link">View costs →</p>
          </a>
          <a href="/hvac-cost-calculator/heat-pump/" class="type-tile type-tile--heat-pump">
            <span class="type-tile-tier">Efficient</span>
            <h3 class="type-tile-title">Heat pump</h3>
            <p class="type-tile-meta">Heat &amp; cool</p>
            <p class="type-tile-price type-tile-price--link">View costs →</p>
          </a>
          <a href="/hvac-cost-calculator/mini-split/" class="type-tile type-tile--mini-split type-tile--current" aria-current="page">
            <span class="type-tile-tier">Flexible</span>
            <h3 class="type-tile-title">Mini split</h3>
            <p class="type-tile-meta">Ductless</p>
            <p class="type-tile-price type-tile-price--link">You are here</p>
          </a>
          <a href="/hvac-cost-calculator/furnace-ac/" class="type-tile type-tile--furnace-ac">
            <span class="type-tile-tier">Full HVAC</span>
            <h3 class="type-tile-title">Furnace + AC</h3>
            <p class="type-tile-meta">Gas + central</p>
            <p class="type-tile-price type-tile-price--link">View costs →</p>
          </a>
          <a href="/hvac-cost-calculator/geothermal/" class="type-tile type-tile--geothermal">
            <span class="type-tile-tier">Premium</span>
            <h3 class="type-tile-title">Geothermal</h3>
            <p class="type-tile-meta">Ground-source</p>
            <p class="type-tile-price type-tile-price--link">View costs →</p>
          </a>""",
        "footer_link": '<li><a href="/hvac-cost-calculator/mini-split/">Mini Split Cost</a></li>',
        "regional_national": "Line-set length and wall penetration count strongly affect labor",
        "example_nat_type": "16 SEER mini split · 2,000 sq ft · 2 zones",
        "quick_ton_label": "Capacity",
    },
    "furnace-ac": {
        "slug": "furnace-ac",
        "title": "Furnace + AC Cost Calculator (2026) — Full HVAC Estimate | Estimate Home Costs",
        "description": "Free furnace and central AC cost calculator for 2026. Estimate $8,000–$20,000 for combined gas furnace and AC replacement by home size and city.",
        "keywords": "furnace and AC cost, furnace AC combo cost calculator, full HVAC replacement cost",
        "canonical": "https://estimatehomecosts.com/hvac-cost-calculator/furnace-ac/",
        "og_title": "Furnace + AC Cost Calculator (2026)",
        "og_desc": "Estimate combined furnace and central AC installation costs.",
        "twitter_desc": "Full HVAC replacement estimates with financing breakdown.",
        "article_headline": "Furnace + AC Cost Calculator (2026): Full HVAC Guide",
        "breadcrumb": "Furnace + AC Cost",
        "body_class": "furnace-ac-page",
        "name": "Furnace + AC",
        "name_lower": "furnace + AC",
        "eyebrow": "HVAC cost calculator · Full system",
        "hero_lead": "Estimate the cost of replacing both your gas furnace and central air conditioner — sizing, efficiency, ductwork, and local labor included.",
        "hero_avg": "$8,000–$20,000",
        "preview_note": "16 SEER AC · 80% furnace",
        "ton_unit": "Ton AC",
        "quick_heading": "Quick Furnace + AC Estimate",
        "advanced_heading": "Advanced Furnace + AC Calculator",
        "advanced_desc": "Personalize AC tonnage, furnace efficiency, ductwork, and upgrades for a complete HVAC replacement estimate.",
        "calc_result_label": "Estimated Furnace + AC Cost",
        "what_id": "what-is-furnace-ac",
        "what_heading": "What Is a Furnace + AC System?",
        "what_copy": "A <strong>furnace and central AC combo</strong> pairs a gas (or oil) furnace for winter heat with a central air conditioner for summer cooling — sharing ductwork and thermostat control.",
        "what_list": """<li><strong>Full-season comfort</strong> — heat and cool through the same ducts</li>
            <li><strong>Common in cold climates</strong> — gas heat where heat pumps struggle at extreme lows</li>
            <li><strong>Replace together</strong> — matched systems improve efficiency and warranties</li>""",
        "size_heading": "Furnace + AC Cost by Home Size",
        "seer_heading": "Furnace + AC Cost by SEER Rating",
        "types_heading": "Furnace + AC Package Types",
        "types_desc": "Furnace efficiency (AFUE) and AC SEER drive total installed cost.",
        "pros_heading": "Furnace + AC Pros &amp; Cons",
        "pros": """<li>Strong heating in cold winters</li>
              <li>Familiar technology for most contractors</li>
              <li>Whole-home comfort through existing ducts</li>
              <li>Can stage upgrades (furnace now, AC later) but combo often saves labor</li>""",
        "cons": """<li>Higher total cost than AC-only replacement</li>
              <li>Two fuel types if you also consider heat pumps later</li>
              <li>Requires well-maintained ductwork for both seasons</li>""",
        "compare_heading": "Furnace + AC vs Other Systems",
        "comparisons": """<a href="/hvac-cost-calculator/heat-pump/" class="comparison-card">
            <h3>Furnace + AC vs Heat Pump</h3>
            <p>Gas heat + AC vs all-electric heat pump in one unit.</p>
            <span class="comparison-card-cta">Heat pump calculator →</span>
          </a>
          <a href="/hvac-cost-calculator/central-ac/" class="comparison-card">
            <h3>AC-only replacement</h3>
            <p>When your furnace still has life left — central AC pricing.</p>
            <span class="comparison-card-cta">Central AC calculator →</span>
          </a>
          <a href="/hvac-cost-calculator/geothermal/" class="comparison-card">
            <h3>vs Geothermal</h3>
            <p>Premium ground-source efficiency vs conventional gas + AC.</p>
            <span class="comparison-card-cta">Geothermal calculator →</span>
          </a>""",
        "local_heading": "Local Furnace + AC Cost Factors",
        "timeline_heading": "Furnace + AC Installation Timeline",
        "timeline_install": "Furnace swap, AC condenser, coil, flue checks, and full system test.",
        "brands_heading": "Best Furnace + AC Brands",
        "examples_heading": "Real Furnace + AC Installation Examples",
        "faq_heading": "Furnace + AC Cost FAQ",
        "faq_cost": "Full furnace and AC replacement typically costs <strong>$8,000–$20,000</strong> nationally in 2026.",
        "faq_size": "AC sizing follows central AC rules; furnace BTU sizing is separate — often <strong>40,000–120,000 BTU</strong> based on home and climate.",
        "project_label": "furnace + AC",
        "system_rate": 5.75,
        "default_ductwork": False,
        "show_ductwork": True,
        "show_stage": True,
        "tile_class": "furnace-ac",
        "related_tiles": """<a href="/hvac-cost-calculator/central-ac/" class="type-tile type-tile--central-ac">
            <span class="type-tile-tier">Cooling</span>
            <h3 class="type-tile-title">Central AC</h3>
            <p class="type-tile-meta">AC only</p>
            <p class="type-tile-price type-tile-price--link">Open calculator →</p>
          </a>
          <a href="/hvac-cost-calculator/heat-pump/" class="type-tile type-tile--heat-pump">
            <span class="type-tile-tier">Efficient</span>
            <h3 class="type-tile-title">Heat pump</h3>
            <p class="type-tile-meta">Heat &amp; cool</p>
            <p class="type-tile-price type-tile-price--link">Open calculator →</p>
          </a>
          <a href="/hvac-cost-calculator/mini-split/" class="type-tile type-tile--mini-split">
            <span class="type-tile-tier">Flexible</span>
            <h3 class="type-tile-title">Mini split</h3>
            <p class="type-tile-meta">Ductless</p>
            <p class="type-tile-price type-tile-price--link">Open calculator →</p>
          </a>
          <a href="/hvac-cost-calculator/" class="type-tile type-tile--guide">
            <span class="type-tile-tier">All systems</span>
            <h3 class="type-tile-title">HVAC replacement</h3>
            <p class="type-tile-meta">Full calculator</p>
            <p class="type-tile-price type-tile-price--link">Open calculator →</p>
          </a>""",
        "systems_grid": """<a href="/hvac-cost-calculator/central-ac/" class="type-tile type-tile--central-ac">
            <span class="type-tile-tier">Cooling</span>
            <h3 class="type-tile-title">Central AC</h3>
            <p class="type-tile-meta">AC only</p>
            <p class="type-tile-price type-tile-price--link">View costs →</p>
          </a>
          <a href="/hvac-cost-calculator/heat-pump/" class="type-tile type-tile--heat-pump">
            <span class="type-tile-tier">Efficient</span>
            <h3 class="type-tile-title">Heat pump</h3>
            <p class="type-tile-meta">Heat &amp; cool</p>
            <p class="type-tile-price type-tile-price--link">View costs →</p>
          </a>
          <a href="/hvac-cost-calculator/mini-split/" class="type-tile type-tile--mini-split">
            <span class="type-tile-tier">Flexible</span>
            <h3 class="type-tile-title">Mini split</h3>
            <p class="type-tile-meta">Ductless</p>
            <p class="type-tile-price type-tile-price--link">View costs →</p>
          </a>
          <a href="/hvac-cost-calculator/furnace-ac/" class="type-tile type-tile--furnace-ac type-tile--current" aria-current="page">
            <span class="type-tile-tier">Full HVAC</span>
            <h3 class="type-tile-title">Furnace + AC</h3>
            <p class="type-tile-meta">Gas + central</p>
            <p class="type-tile-price type-tile-price--link">You are here</p>
          </a>
          <a href="/hvac-cost-calculator/geothermal/" class="type-tile type-tile--geothermal">
            <span class="type-tile-tier">Premium</span>
            <h3 class="type-tile-title">Geothermal</h3>
            <p class="type-tile-meta">Ground-source</p>
            <p class="type-tile-price type-tile-price--link">View costs →</p>
          </a>""",
        "footer_link": '<li><a href="/hvac-cost-calculator/furnace-ac/">Furnace + AC Cost</a></li>',
        "regional_national": "Gas furnace + AC common in northern and midwestern markets",
        "example_nat_type": "16 SEER AC + 80% furnace · 2,000 sq ft",
    },
    "geothermal": {
        "slug": "geothermal",
        "title": "Geothermal Cost Calculator (2026) — Ground-Source Estimate | Estimate Home Costs",
        "description": "Free geothermal HVAC cost calculator for 2026. Estimate $18,000–$45,000+ for ground-source heat pump installation by home size, loop type, and city.",
        "keywords": "geothermal cost calculator, geothermal HVAC cost, ground source heat pump cost",
        "canonical": "https://estimatehomecosts.com/hvac-cost-calculator/geothermal/",
        "og_title": "Geothermal Cost Calculator (2026)",
        "og_desc": "Estimate ground-source geothermal installation costs and payback.",
        "twitter_desc": "Geothermal installation cost ranges with local labor adjustments.",
        "article_headline": "Geothermal Cost Calculator (2026): Ground-Source Guide",
        "breadcrumb": "Geothermal Cost",
        "body_class": "geothermal-page",
        "name": "Geothermal",
        "name_lower": "geothermal",
        "eyebrow": "HVAC cost calculator · Ground-source",
        "hero_lead": "Estimate ground-source geothermal installation cost — loop field, indoor unit, efficiency, and local labor for long-term heating and cooling.",
        "hero_avg": "$18,000–$45,000+",
        "preview_note": "Horizontal loop · high efficiency",
        "ton_unit": "Ton geo",
        "quick_heading": "Quick Geothermal Estimate",
        "advanced_heading": "Advanced Geothermal Calculator",
        "advanced_desc": "Adjust home size, system capacity, loop assumptions, and location for a detailed geothermal estimate.",
        "calc_result_label": "Estimated Geothermal Cost",
        "what_id": "what-is-geothermal",
        "what_heading": "What Is Geothermal HVAC?",
        "what_copy": "<strong>Geothermal</strong> (ground-source) systems exchange heat with the earth through buried loops — delivering very high efficiency and decades-long equipment life.",
        "what_list": """<li><strong>Ground loops</strong> — horizontal or vertical boreholes transfer stable earth temperatures</li>
            <li><strong>Heating &amp; cooling</strong> — one indoor heat pump unit year-round</li>
            <li><strong>Low operating cost</strong> — highest efficiency of common residential HVAC types</li>""",
        "size_heading": "Geothermal Cost by Home Size",
        "seer_heading": "Geothermal Cost by Efficiency Level",
        "types_heading": "Geothermal Loop Types",
        "types_desc": "Loop configuration is the largest cost variable after home size.",
        "types_cards": """<article class="variant-card">
            <h3>Horizontal loop</h3>
            <ul class="variant-card-meta">
              <li><strong>Cost tier:</strong> $$</li>
              <li><strong>Best for:</strong> Larger lots with trenching access</li>
            </ul>
          </article>
          <article class="variant-card variant-card--featured">
            <h3>Vertical borehole</h3>
            <ul class="variant-card-meta">
              <li><strong>Cost tier:</strong> $$$</li>
              <li><strong>Best for:</strong> Smaller lots and urban sites</li>
            </ul>
          </article>
          <article class="variant-card">
            <h3>Pond / lake loop</h3>
            <ul class="variant-card-meta">
              <li><strong>Cost tier:</strong> $$–$$$</li>
              <li><strong>Best for:</strong> Properties with qualifying water body</li>
            </ul>
          </article>""",
        "pros_heading": "Geothermal Pros &amp; Cons",
        "pros": """<li>Highest efficiency and lowest utility bills long-term</li>
              <li>25+ year equipment lifespan typical</li>
              <li>Quiet outdoor operation (buried loops)</li>
              <li>Heating and cooling in one system</li>""",
        "cons": """<li>Highest upfront install cost</li>
              <li>Requires yard space or bore drilling</li>
              <li>Longer install timeline (loop field)</li>
              <li>Fewer installers vs conventional HVAC</li>""",
        "compare_heading": "Geothermal vs Other Systems",
        "comparisons": """<a href="/hvac-cost-calculator/heat-pump/" class="comparison-card">
            <h3>Geothermal vs Air-Source Heat Pump</h3>
            <p>Ground-source vs ducted air-source heat pump costs.</p>
            <span class="comparison-card-cta">Heat pump calculator →</span>
          </a>
          <a href="/hvac-cost-calculator/central-ac/" class="comparison-card">
            <h3>Geothermal vs Central AC</h3>
            <p>Premium efficiency vs standard cooling replacement.</p>
            <span class="comparison-card-cta">Central AC calculator →</span>
          </a>
          <a href="/hvac-cost-calculator/" class="comparison-card">
            <h3>All HVAC systems</h3>
            <p>Compare every option on the main HVAC calculator.</p>
            <span class="comparison-card-cta">Full calculator →</span>
          </a>""",
        "local_heading": "Local Geothermal Cost Factors",
        "timeline_heading": "Geothermal Installation Timeline",
        "timeline_loop": """<article class="install-timeline-card">
            <h3>Ground loop field</h3>
            <p class="install-timeline-duration">3–5 days</p>
            <p>Trenching or vertical bore drilling and loop testing.</p>
          </article>""",
        "timeline_install": "Indoor heat pump, loop ties, flush, and commissioning.",
        "brands_heading": "Best Geothermal Brands",
        "examples_heading": "Real Geothermal Installation Examples",
        "faq_heading": "Geothermal Cost FAQ",
        "faq_cost": "Geothermal installation typically costs <strong>$18,000–$45,000+</strong> nationally in 2026, with loop type as the largest variable.",
        "faq_size": "Capacity sizing is similar to heat pumps — <strong>1 ton per 500–600 sq ft</strong> is a starting point before a Manual J study.",
        "project_label": "geothermal",
        "system_rate": 9.25,
        "geo_premium": True,
        "plus_high": True,
        "plus_threshold": 35000,
        "hero_low_sqft": 1500,
        "hero_high_sqft": 3500,
        "default_ductwork": False,
        "show_ductwork": True,
        "show_stage": False,
        "stage_fieldset": "",
        "tile_class": "geothermal",
        "related_tiles": """<a href="/hvac-cost-calculator/heat-pump/" class="type-tile type-tile--heat-pump">
            <span class="type-tile-tier">Efficient</span>
            <h3 class="type-tile-title">Heat pump</h3>
            <p class="type-tile-meta">Air-source</p>
            <p class="type-tile-price type-tile-price--link">Open calculator →</p>
          </a>
          <a href="/hvac-cost-calculator/central-ac/" class="type-tile type-tile--central-ac">
            <span class="type-tile-tier">Popular</span>
            <h3 class="type-tile-title">Central AC</h3>
            <p class="type-tile-meta">Cooling</p>
            <p class="type-tile-price type-tile-price--link">Open calculator →</p>
          </a>
          <a href="/hvac-cost-calculator/furnace-ac/" class="type-tile type-tile--furnace-ac">
            <span class="type-tile-tier">Full HVAC</span>
            <h3 class="type-tile-title">Furnace + AC</h3>
            <p class="type-tile-meta">Gas + central</p>
            <p class="type-tile-price type-tile-price--link">Open calculator →</p>
          </a>
          <a href="/hvac-cost-calculator/" class="type-tile type-tile--guide">
            <span class="type-tile-tier">All systems</span>
            <h3 class="type-tile-title">HVAC replacement</h3>
            <p class="type-tile-meta">Full calculator</p>
            <p class="type-tile-price type-tile-price--link">Open calculator →</p>
          </a>""",
        "systems_grid": """<a href="/hvac-cost-calculator/central-ac/" class="type-tile type-tile--central-ac">
            <span class="type-tile-tier">Cooling</span>
            <h3 class="type-tile-title">Central AC</h3>
            <p class="type-tile-meta">Ducted</p>
            <p class="type-tile-price type-tile-price--link">View costs →</p>
          </a>
          <a href="/hvac-cost-calculator/heat-pump/" class="type-tile type-tile--heat-pump">
            <span class="type-tile-tier">Efficient</span>
            <h3 class="type-tile-title">Heat pump</h3>
            <p class="type-tile-meta">Heat &amp; cool</p>
            <p class="type-tile-price type-tile-price--link">View costs →</p>
          </a>
          <a href="/hvac-cost-calculator/mini-split/" class="type-tile type-tile--mini-split">
            <span class="type-tile-tier">Flexible</span>
            <h3 class="type-tile-title">Mini split</h3>
            <p class="type-tile-meta">Ductless</p>
            <p class="type-tile-price type-tile-price--link">View costs →</p>
          </a>
          <a href="/hvac-cost-calculator/furnace-ac/" class="type-tile type-tile--furnace-ac">
            <span class="type-tile-tier">Full HVAC</span>
            <h3 class="type-tile-title">Furnace + AC</h3>
            <p class="type-tile-meta">Gas + central</p>
            <p class="type-tile-price type-tile-price--link">View costs →</p>
          </a>
          <a href="/hvac-cost-calculator/geothermal/" class="type-tile type-tile--geothermal type-tile--current" aria-current="page">
            <span class="type-tile-tier">Premium</span>
            <h3 class="type-tile-title">Geothermal</h3>
            <p class="type-tile-meta">Ground-source</p>
            <p class="type-tile-price type-tile-price--link">You are here</p>
          </a>""",
        "footer_link": '<li><a href="/hvac-cost-calculator/geothermal/">Geothermal Cost</a></li>',
        "regional_national": "Soil type and drilling depth drive loop field cost more than equipment",
        "example_nat_type": "Geothermal · 2,200 sq ft · horizontal loop",
    },
}

REGIONAL = {
    "national": "Peak summer demand; right-size systems to avoid short-cycling",
    "dallas": "High cooling load — oversizing is common; verify Manual J sizing",
    "phoenix": "Extreme heat — high-SEER and variable-speed strongly recommended",
    "austin": "Long cooling season; competitive install market",
    "tampa": "Humidity control and condensate management are critical",
    "charlotte": "Moderate cooling hours; heat pumps also popular",
    "raleigh": "Growing metro; 16+ SEER standard for new permits in many areas",
    "scottsdale": "Premium equipment tiers; peak summer labor rates",
    "houston": "Year-round humidity; corrosion-resistant outdoor units",
    "orlando": "Coastal wind ratings; high-SEER AC typical",
    "san-diego": "Title 24 efficiency rules; coastal labor premium",
}

HOME_EXAMPLES = {
    "national": {"sqft": 2000, "seer": 16, "ton": 3, "detail": "Standard install"},
    "dallas": {"sqft": 2300, "seer": 16, "ton": 4, "detail": "Existing ducts"},
    "phoenix": {"sqft": 2100, "seer": 18, "ton": 4, "detail": "High-SEER equipment"},
    "austin": {"sqft": 2050, "seer": 16, "ton": 3, "detail": "Matched system"},
    "tampa": {"sqft": 1950, "seer": 16, "ton": 3, "detail": "Humidity package"},
    "charlotte": {"sqft": 2000, "seer": 16, "ton": 3, "detail": "Existing ducts"},
    "raleigh": {"sqft": 1980, "seer": 16, "ton": 3, "detail": "Code-compliant install"},
    "scottsdale": {"sqft": 2400, "seer": 18, "ton": 4, "detail": "Premium tier"},
    "houston": {"sqft": 2200, "seer": 16, "ton": 4, "detail": "Coastal-rated outdoor"},
    "orlando": {"sqft": 1900, "seer": 16, "ton": 3, "detail": "Hurricane-rated unit"},
    "san-diego": {"sqft": 1850, "seer": 18, "ton": 3, "detail": "Title 24 compliant"},
}


def js_config(s):
    cfg = {
        "systemRate": s["system_rate"],
        "systemName": s["name"],
        "projectLabel": s.get("project_label", s["name_lower"]),
        "tonUnit": s.get("ton_unit", "Ton"),
        "defaultSqft": 2200,
        "defaultDuctwork": s.get("default_ductwork", False),
        "showDuctwork": s.get("show_ductwork", True),
        "showStage": s.get("show_stage", True),
        "geoPremium": s.get("geo_premium", False),
        "plusHigh": s.get("plus_high", False),
        "plusThreshold": s.get("plus_threshold", 30000),
        "heroLowSqft": s.get("hero_low_sqft", 1000),
        "heroHighSqft": s.get("hero_high_sqft", 3000),
        "formId": "hvac-system-calculator",
        "quickFormId": "quick-hvac-calc",
        "regional": REGIONAL,
        "homeExamples": HOME_EXAMPLES,
    }
    return json.dumps(cfg, indent=2)


def build_page(slug, s):
    t = TEMPLATE
    path = f"/hvac-cost-calculator/{slug}/"
    base = f"https://estimatehomecosts.com/hvac-cost-calculator/{slug}"

    reps = [
        ("central-ac", slug),
        ("Central AC", s["name"]),
        ("central-ac/", f"{slug}/"),
        ("https://estimatehomecosts.com/hvac-cost-calculator/central-ac/", base + "/"),
        ("central-ac-page", s["body_class"]),
        ("Central air", s["eyebrow"].split("·")[-1].strip() if "·" in s["eyebrow"] else s["eyebrow"]),
        ("Central AC Cost Calculator", f'{s["name"]} Cost Calculator'),
        ("$5,500–$14,000", s["hero_avg"]),
        ("3 Ton AC", s.get("ton_unit", "Ton")),
        ("16 SEER · existing ductwork · updates with calculator", s["preview_note"] + " · updates with calculator"),
        ("Quick Central AC Estimate", s["quick_heading"]),
        ("Advanced Central AC Calculator", s["advanced_heading"]),
        ("Personalize tonnage, efficiency, ductwork, climate, and upgrades for a detailed breakdown with financing.", s["advanced_desc"]),
        ("Estimated Central AC Cost", s["calc_result_label"]),
        ("what-is-central-ac", s["what_id"]),
        ("What Is Central AC?", s["what_heading"]),
        ("id=\"central-ac-calculator\"", 'id="hvac-system-calculator"'),
        ("id=\"quick-central-ac-calc\"", 'id="quick-hvac-calc"'),
        ("Central AC System Cost Comparison", s.get("types_heading", "").replace("Types", "Cost Comparison")),
        ("Central AC System Types", s["types_heading"]),
        ("Compressor stage affects comfort, noise, efficiency, and price.", s["types_desc"]),
        ("Central AC Pros &amp; Cons", s["pros_heading"]),
        ("Central AC vs Other Systems", s["compare_heading"]),
        ("Local Central AC Cost Factors", s["local_heading"]),
        ("Central AC Installation Timeline", s["timeline_heading"]),
        ("Outdoor unit, indoor coil, refrigerant lines, and startup.", s["timeline_install"]),
        ("Best Central AC Brands", s["brands_heading"]),
        ("Real Central AC Installation Examples", s["examples_heading"]),
        ("16 SEER central AC · 2,000 sq ft", s.get("example_nat_type", "16 SEER · 2,000 sq ft")),
        ("Central AC Cost FAQ", s["faq_heading"]),
        ("How much does Central AC cost?", f'How much does {s["name"]} cost?'),
        ("Central AC installation typically costs", f'{s["name"]} installation typically costs'),
        ('<li aria-current="page">Central AC</li>', f'<li aria-current="page">{s["name"]}</li>'),
        ("central-ac-page.js", "hvac-system-page.js"),
        ("<li><a href=\"/hvac-cost-calculator/central-ac/\">Central AC Cost</a></li>", s.get("footer_link", "")),
    ]

    for old, new in reps:
        t = t.replace(old, new)

    # Meta block
    t = t.replace(
        "<title>Central AC Cost Calculator (2026) — Installation Estimate | Estimate Home Costs</title>",
        f'<title>{s["title"]}</title>',
    )
    import re as _re
    t = _re.sub(
        r'<meta name="description" content="[^"]*">',
        f'<meta name="description" content="{s["description"]}">',
        t,
        count=1,
    )
    t = t.replace(
        "<p>Complete guide to central air conditioning installation costs including SEER ratings, tonnage sizing, ductwork, and city-level pricing.</p>",
        f"<p>Complete guide to {s['name_lower']} installation costs including efficiency, sizing, ductwork, and city-level pricing.</p>",
    )
    t = t.replace(
        """<p class="cost-hero-lead">
              Estimate the cost of installing a central air conditioning system based on home size, efficiency, ductwork, and local labor rates.
            </p>""",
        f'<p class="cost-hero-lead">\n              {s["hero_lead"]}\n            </p>',
    )
    import re as _re2
    t = _re2.sub(r'class="[a-z0-9-]+-hero-avg(-label)?"', lambda m: f'class="hvac-system-hero-avg{m.group(1) or ""}"', t)
    t = t.replace("central-ac-preview-card", "hvac-system-preview-card")
    t = t.replace("central-ac-preview-meta", "hvac-system-preview-meta")
    t = t.replace("central-ac-preview-label", "hvac-system-preview-label")
    t = t.replace('class="cost-hero-aside central-ac-hero-preview"', 'class="cost-hero-aside hvac-system-hero-preview"')
    t = t.replace(
        'content="central AC cost calculator, central air conditioning installation cost, AC cost per square foot, SEER rating cost, 3 ton AC cost, central AC replacement cost"',
        f'content="{s["keywords"]}"',
    )
    t = t.replace('content="Central AC Cost Calculator (2026)"', f'content="{s["og_title"]}"', 1)
    t = t.replace(
        'content="Estimate central air conditioning installation costs by home size, system tonnage, SEER, ductwork, and local labor rates."',
        f'content="{s["og_desc"]}"',
    )
    t = t.replace('content="Instant central AC installation estimates with cost breakdown, financing, and city-level pricing."', f'content="{s["twitter_desc"]}"')

    # What section body
    old_what = """<p>Central air conditioning cools your entire home through a single outdoor condenser and indoor air handler connected to <strong>ductwork</strong>. A thermostat controls temperature room-by-room via supply vents.</p>
          <ul class="cost-detail-list">
            <li><strong>Whole-home cooling</strong> — one system, even temperatures</li>
            <li><strong>Duct-driven airflow</strong> — works with existing furnace ducts in most homes</li>
            <li><strong>Thermostat controlled</strong> — programmable and smart thermostat compatible</li>
          </ul>"""
    t = t.replace(old_what, f'<p>{s["what_copy"]}</p>\n          <ul class="cost-detail-list">\n            {s["what_list"]}\n          </ul>')

    # Pros/cons
    t = t.replace(
        """<ul>
              <li>Whole-home cooling from one system</li>
              <li>Quiet indoor operation (condenser outside)</li>
              <li>Strong resale value in ducted homes</li>
              <li>Consistent airflow to every room</li>
            </ul>""",
        f"<ul>\n              {s['pros']}\n            </ul>",
    )
    t = t.replace(
        """<ul>
              <li>Requires ductwork (not ideal for additions without ducts)</li>
              <li>Higher upfront cost vs window units</li>
              <li>Less room-by-room flexibility than mini-splits</li>
            </ul>""",
        f"<ul>\n              {s['cons']}\n            </ul>",
    )

    # Comparisons
    old_cmp = """<a href="/compare/heat-pump-vs-ac/" class="comparison-card">
            <h3>Central AC vs Heat Pump</h3>
            <p>Cooling-only vs heat + cool in one system — compare installed costs.</p>
            <span class="comparison-card-cta">Read comparison →</span>
          </a>
          <a href="/hvac-cost-calculator/#material-comparison" class="comparison-card">
            <h3>Central AC vs Mini Split</h3>
            <p>Ducted whole-home vs ductless zoning — which fits your home?</p>
            <span class="comparison-card-cta">Compare systems →</span>
          </a>
          <a href="/hvac-cost-calculator/" class="comparison-card">
            <h3>Central AC vs Window AC</h3>
            <p>Whole-home comfort vs room-by-room budget cooling.</p>
            <span class="comparison-card-cta">Full HVAC calculator →</span>
          </a>"""
    t = t.replace(old_cmp, s["comparisons"])

    # Related tiles
    old_rel = t[t.find('id="related-calculators-heading"'):]
    # replace type-tile-grid in related section only - use marker
    import re
    t = re.sub(
        r'(<section id="related-calculators"[\s\S]*?<div class="type-tile-grid">)[\s\S]*?(</div>\s*</div>\s*</section>)',
        r"\1\n" + s["related_tiles"] + r"\n        \2",
        t,
        count=1,
    )

    # Add HVAC systems by type section before local factors - inject after comparisons if not in template
    systems_section = f"""
    <section id="hvac-systems" class="section type-tile-section" aria-labelledby="hvac-systems-heading">
      <div class="container">
        <header class="section-header section-header--center">
          <h2 id="hvac-systems-heading">HVAC Systems by Type</h2>
          <p>Compare installed cost ranges for every major system.</p>
        </header>
        <div class="type-tile-grid">
          {s["systems_grid"]}
        </div>
      </div>
    </section>
"""
    if 'id="hvac-systems-heading"' not in t:
        t = t.replace("<!-- 10. Local factors -->", systems_section + "\n    <!-- 10. Local factors -->")

    # Variant cards for geothermal
    if s.get("types_cards"):
        t = re.sub(
            r'<div class="variant-cards-grid variant-cards-grid--three">[\s\S]*?</div>\s*</div>\s*</section>\s*<!-- 8. Pros',
            f'<div class="variant-cards-grid variant-cards-grid--three">\n          {s["types_cards"]}\n        </div>\n      </div>\n    </section>\n\n    <!-- 8. Pros',
            t,
            count=1,
        )

    # Hide ductwork fieldset
    if s.get("show_ductwork") is False:
        t = re.sub(
            r'\s*<fieldset class="calc-fieldset">\s*<legend>Existing ductwork\?</legend>[\s\S]*?</fieldset>',
            "",
            t,
            count=1,
        )

    # Hide stage fieldset
    if s.get("show_stage") is False:
        t = re.sub(
            r'\s*<fieldset class="calc-fieldset">\s*<legend>Compressor stage</legend>[\s\S]*?</fieldset>',
            "",
            t,
            count=1,
        )

    # Geothermal timeline extra loop card
    if s.get("timeline_loop"):
        t = t.replace(
            '<article class="install-timeline-card">\n            <h3>Installation</h3>',
            s["timeline_loop"] + '\n          <article class="install-timeline-card">\n            <h3>Installation</h3>',
            1,
        )

    # National factor default bullet
    t = t.replace(
        "<li><strong>Efficiency:</strong> 16 SEER is the most common choice in 2026</li>",
        f'<li><strong>Note:</strong> {s["regional_national"]}</li>',
    )

    # Quick ton label
    if s.get("quick_ton_label"):
        t = t.replace("<label for=\"quick-ton\">System size</label>", f'<label for="quick-ton">{s["quick_ton_label"]}</label>')

    # Script config
    config_script = f"  <script>window.HVAC_SYSTEM_CONFIG = {js_config(s)};</script>\n"
    t = t.replace("  <script src=\"/js/calculator-cities.js\"", config_script + "  <script src=\"/js/calculator-cities.js\"")

    # JSON-LD breadcrumb name
    t = t.replace('"name": "Central AC Cost"', f'"name": "{s["breadcrumb"]}"')

    return t


def main():
    for slug, s in SYSTEMS.items():
        out = ROOT / "hvac-cost-calculator" / slug
        out.mkdir(parents=True, exist_ok=True)
        (out / "index.html").write_text(build_page(slug, s))
        print("Wrote", out / "index.html")

    # Update central-ac to use shared JS
    central = ROOT / "hvac-cost-calculator/central-ac/index.html"
    text = central.read_text()
    if "HVAC_SYSTEM_CONFIG" not in text:
        central_cfg = {
            "system_rate": 4.05,
            "systemName": "Central AC",
            "projectLabel": "central AC",
            "tonUnit": "Ton AC",
            "defaultSqft": 2200,
            "defaultDuctwork": False,
            "showDuctwork": True,
            "showStage": True,
            "formId": "hvac-system-calculator",
            "quickFormId": "quick-hvac-calc",
            "regional": REGIONAL,
            "homeExamples": HOME_EXAMPLES,
        }
        cfg_script = f"  <script>window.HVAC_SYSTEM_CONFIG = {json.dumps(central_cfg)};</script>\n"
        text = text.replace('id="central-ac-calculator"', 'id="hvac-system-calculator"')
        text = text.replace('id="quick-central-ac-calc"', 'id="quick-hvac-calc"')
        text = text.replace("central-ac-page.js", "hvac-system-page.js")
        text = text.replace("  <script src=\"/js/calculator-cities.js\"", cfg_script + "  <script src=\"/js/calculator-cities.js\"")
        central.write_text(text)
        print("Updated central-ac/index.html")

    print("Done.")


if __name__ == "__main__":
    main()

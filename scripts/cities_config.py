"""City hub configs for Popular Cities — used by generate-city-hub-page.py and generate-city-scoped-pages.py"""

from __future__ import annotations

from brand import SITE_ORIGIN

# Shared link templates (root paths; prefixed per city at render time)
SNAPSHOTS_DEFAULT = [
    {"icon": "roof", "category": "Roofing", "title": "Roof Replacement", "range": "$7k–$18k", "href": "/roof-cost-calculator/"},
    {"icon": "bath", "category": "Bathroom Remodel", "title": "Bathroom Remodel", "range": "$9k–$30k", "href": "/cost/bathroom-remodel/"},
    {"icon": "hvac", "category": "HVAC", "title": "Central AC Installation", "range": "$5k–$14k", "href": "/hvac-cost-calculator/"},
    {"icon": "floor", "category": "Flooring", "title": "Flooring Installation", "range": "$4–$20/sq ft", "href": "/flooring-cost-calculator/"},
    {"icon": "fence", "category": "Fence", "title": "Wood Privacy Fence", "range": "$25–$60/linear ft", "href": "/fence-materials/wood-privacy-fence-cost/"},
    {"icon": "solar", "category": "Solar", "title": "Solar Panels", "range": "$12k–$35k", "href": "/solar-panel-cost-calculator/"},
]

CATEGORIES_DEFAULT = [
    {
        "name": "Roofing",
        "links": [
            ("Roof replacement", "/roof-cost-calculator/"),
            ("Roof repair", "/cost/roof-replacement/#repair-vs-replace"),
            ("Roofing materials", "/roofing-materials/asphalt-shingle-roof-cost/"),
        ],
    },
    {
        "name": "Remodeling",
        "links": [
            ("Kitchen remodel", "/cost/kitchen-remodel/"),
            ("Bathroom remodel", "/cost/bathroom-remodel/"),
            ("Basement finishing", "/cost/kitchen-remodel/"),
        ],
    },
    {
        "name": "HVAC",
        "links": [
            ("Central AC", "/hvac-cost-calculator/central-ac/"),
            ("Heat pumps", "/hvac-cost-calculator/heat-pump/"),
            ("Furnace replacement", "/hvac-cost-calculator/furnace-ac/"),
        ],
    },
    {
        "name": "Flooring",
        "links": [
            ("Hardwood", "/flooring-materials/solid-hardwood-flooring-cost/"),
            ("LVP", "/flooring-materials/luxury-vinyl-plank-flooring-cost/"),
            ("Tile flooring", "/flooring-materials/porcelain-tile-flooring-cost/"),
        ],
    },
    {
        "name": "Outdoor",
        "links": [
            ("Fencing", "/fence-cost-calculator/"),
            ("Decks", "/fence-cost-calculator/"),
            ("Patios", "/cost/kitchen-remodel/"),
        ],
    },
    {
        "name": "Energy",
        "links": [
            ("Solar panels", "/solar-panel-cost-calculator/"),
            ("Insulation", "/hvac-cost-calculator/"),
            ("Windows", "/cost/kitchen-remodel/"),
        ],
    },
]

SCOPED_PATHS = [
    "roof-cost-calculator",
    "hvac-cost-calculator",
    "hvac-cost-calculator/central-ac",
    "hvac-cost-calculator/heat-pump",
    "hvac-cost-calculator/mini-split",
    "hvac-cost-calculator/furnace-ac",
    "hvac-cost-calculator/geothermal",
    "flooring-cost-calculator",
    "fence-cost-calculator",
    "solar-panel-cost-calculator",
    "fence-materials/wood-privacy-fence-cost",
    "fence-materials/vinyl-fence-cost",
    "fence-materials/composite-fence-cost",
    "fence-materials/chain-link-fence-cost",
    "fence-materials/aluminum-fence-cost",
    "flooring-materials/luxury-vinyl-plank-flooring-cost",
    "flooring-materials/solid-hardwood-flooring-cost",
    "flooring-materials/engineered-wood-flooring-cost",
    "flooring-materials/porcelain-tile-flooring-cost",
    "flooring-materials/carpet-flooring-cost",
    "roofing-materials/asphalt-shingle-roof-cost",
    "roofing-materials/metal-roof-cost",
    "roofing-materials/tile-roof-cost",
    "roofing-materials/slate-roof-cost",
    "roofing-materials/wood-shake-roof-cost",
    "cost/bathroom-remodel",
    "cost/kitchen-remodel",
    "cost/roof-replacement",
    "cost/hvac-installation",
]


def _city(
    slug: str,
    state_slug: str,
    state_name: str,
    state_abbr: str,
    city_name: str,
    city_key: str,
    market_insight: str,
    market_bullets: list[str],
    climate_bullets: list[str],
    metro_callout: str,
    trending: list[tuple],
    suburbs: list[tuple],
    nearby_cities: list[tuple],
    nearby_suburbs: list[tuple],
    examples: list[tuple],
    footer_suburbs: list[tuple],
    lead_zip: str = "00000",
    snapshots: list | None = None,
    home_types: list | None = None,
) -> dict:
    base = f"{SITE_ORIGIN}/{state_slug}/{slug}/"
    return {
        "slug": slug,
        "state_slug": state_slug,
        "state_name": state_name,
        "state_abbr": state_abbr,
        "city_name": city_name,
        "city_key": city_key,
        "canonical": base,
        "market_insight": market_insight,
        "market_bullets": market_bullets,
        "climate_bullets": climate_bullets,
        "metro_callout": metro_callout,
        "snapshots": snapshots or SNAPSHOTS_DEFAULT,
        "categories": CATEGORIES_DEFAULT,
        "trending": trending,
        "home_types": home_types
        or [
            ("Ranch homes", "Single-story updates: HVAC, roofing, LVP flooring.", "$8k–$45k typical"),
            ("Modern suburban", "Open kitchens, master baths, solar + fence.", "$15k–$80k typical"),
            ("Townhomes", "Compact remodels, mini-split HVAC, smaller roofs.", "$5k–$35k typical"),
            ("Luxury homes", "High-end kitchens, metal roofs, whole-home solar.", "$40k–$150k+"),
        ],
        "suburbs": suburbs,
        "budgets": [
            ("Under $5k", ["Flooring refresh", "Interior paint", "Small fencing"], "/flooring-cost-calculator/"),
            ("$5k–$15k", ["HVAC replacement", "Bathroom remodel", "Roof repair"], "/hvac-cost-calculator/"),
            ("$15k+", ["Kitchen remodel", "Solar systems", "Additions"], "/cost/kitchen-remodel/"),
        ],
        "examples": examples,
        "nearby_cities": nearby_cities,
        "nearby_suburbs": nearby_suburbs,
        "footer_suburbs": footer_suburbs,
        "lead_zip": lead_zip,
    }


POPULAR_CITIES = [
    _city(
        slug="dallas",
        state_slug="texas",
        state_name="Texas",
        state_abbr="TX",
        city_name="Dallas",
        city_key="dallas",
        lead_zip="75201",
        market_insight=(
            "Dallas homeowners often prioritize impact-resistant roofing, energy-efficient "
            "HVAC systems, and outdoor living upgrades due to heat and storm exposure."
        ),
        market_bullets=[
            "Storm-prone roofing demand after hail season",
            "Suburban home growth in Collin &amp; Denton counties",
            "High summer cooling load drives HVAC upgrades",
            "Modern open-concept kitchen &amp; bath remodels",
            "HOA-heavy neighborhoods in Plano, Frisco &amp; McKinney",
        ],
        climate_bullets=[
            "High summer cooling costs (100°F+ heat waves)",
            "Hail-resistant roofing &amp; impact-rated shingles",
            "Fence &amp; deck weather exposure — UV and wind",
            "Attic insulation &amp; radiant barriers for efficiency",
        ],
        metro_callout=(
            "The <strong>Dallas–Fort Worth metro</strong> spans Collin, Dallas, Denton &amp; Tarrant "
            "counties with diverse housing from mid-century ranches to new-build suburbs."
        ),
        trending=[
            ("Roof Replacement", "Most common after storm season.", "/roof-cost-calculator/"),
            ("Kitchen Remodels", "Popular in suburban upgrades.", "/cost/kitchen-remodel/"),
            ("Solar Panels", "Growing due to electricity costs.", "/solar-panel-cost-calculator/"),
            ("Backyard Fencing", "Common in family neighborhoods.", "/fence-cost-calculator/"),
        ],
        suburbs=[("Plano", "plano"), ("Frisco", "frisco"), ("McKinney", "mckinney"), ("Irving", "irving"), ("Garland", "garland"), ("Arlington", "arlington")],
        nearby_cities=[("Fort Worth", "fort-worth"), ("Austin", "austin"), ("Houston", "houston"), ("San Antonio", "san-antonio")],
        nearby_suburbs=[("Plano", "plano"), ("Frisco", "frisco"), ("McKinney", "mckinney"), ("Richardson", "richardson")],
        examples=[
            ("Plano, TX", "Luxury vinyl flooring · 1,200 sq ft", "$8,900", "/flooring-materials/luxury-vinyl-plank-flooring-cost/"),
            ("Frisco, TX", "Roof replacement · architectural shingles", "$13,700", "/roof-cost-calculator/"),
            ("McKinney, TX", "Central AC replacement · 2,100 sq ft", "$7,800", "/hvac-cost-calculator/"),
        ],
        footer_suburbs=[("Plano", "plano"), ("Frisco", "frisco"), ("McKinney", "mckinney")],
    ),
    _city(
        slug="phoenix",
        state_slug="arizona",
        state_name="Arizona",
        state_abbr="AZ",
        city_name="Phoenix",
        city_key="phoenix",
        lead_zip="85001",
        market_insight=(
            "Phoenix homeowners focus on heat-ready roofing, high-efficiency HVAC, and solar "
            "to offset soaring summer electric bills in the Sonoran Desert climate."
        ),
        market_bullets=[
            "Extreme heat drives tile, metal &amp; cool-roof demand",
            "Rapid suburban growth in Maricopa County",
            "Pool-friendly outdoor living &amp; backyard upgrades",
            "Strong solar adoption with excellent sun exposure",
            "HOA communities common in Scottsdale &amp; Gilbert",
        ],
        climate_bullets=[
            "120°F+ heat waves and high cooling loads",
            "UV degradation on roofing and exterior paint",
            "Monsoon season wind &amp; dust exposure",
            "Radiant barriers and attic ventilation critical",
        ],
        metro_callout=(
            "The <strong>Phoenix metro</strong> includes Scottsdale, Mesa, Chandler &amp; Gilbert — "
            "one of the fastest-growing markets for desert-climate home upgrades."
        ),
        trending=[
            ("Tile &amp; Metal Roofs", "Popular for heat and longevity.", "/roof-cost-calculator/"),
            ("Solar Panels", "Top market for production per square foot.", "/solar-panel-cost-calculator/"),
            ("HVAC Upgrades", "Essential for summer survival.", "/hvac-cost-calculator/"),
            ("Kitchen Remodels", "Strong demand in 1990s–2000s builds.", "/cost/kitchen-remodel/"),
        ],
        suburbs=[("Scottsdale", "scottsdale"), ("Mesa", "mesa"), ("Chandler", "chandler"), ("Gilbert", "gilbert"), ("Glendale", "glendale"), ("Tempe", "tempe")],
        nearby_cities=[("Tucson", "tucson"), ("Scottsdale", "scottsdale"), ("Mesa", "mesa"), ("Las Vegas", "las-vegas")],
        nearby_suburbs=[("Scottsdale", "scottsdale"), ("Chandler", "chandler"), ("Gilbert", "gilbert"), ("Tempe", "tempe")],
        examples=[
            ("Scottsdale, AZ", "Tile roof replacement · concrete tile", "$16,200", "/roof-cost-calculator/"),
            ("Mesa, AZ", "Solar + battery · 7.5 kW system", "$21,400", "/solar-panel-cost-calculator/"),
            ("Chandler, AZ", "Central AC · high-SEER replacement", "$8,600", "/hvac-cost-calculator/"),
        ],
        footer_suburbs=[("Scottsdale", "scottsdale"), ("Mesa", "mesa"), ("Chandler", "chandler")],
    ),
    _city(
        slug="tampa",
        state_slug="florida",
        state_name="Florida",
        state_abbr="FL",
        city_name="Tampa",
        city_key="tampa",
        lead_zip="33602",
        market_insight=(
            "Tampa Bay homeowners invest in hurricane-rated roofing, humidity-ready HVAC, "
            "and moisture-resistant materials for Gulf Coast weather."
        ),
        market_bullets=[
            "Hurricane straps &amp; wind-rated roofing codes",
            "Humidity control and high-SEER AC demand",
            "Tile and metal roofs common near the coast",
            "Outdoor living, pools &amp; screened lanais",
            "Flood-zone awareness affects insurance &amp; materials",
        ],
        climate_bullets=[
            "Hurricane season wind and rain exposure",
            "High humidity — mold-resistant materials matter",
            "Salt air corrosion near the bay",
            "Year-round cooling with moderate heating needs",
        ],
        metro_callout=(
            "The <strong>Tampa Bay</strong> area includes St. Petersburg, Clearwater &amp; Brandon — "
            "coastal building codes shape roofing and window project costs."
        ),
        trending=[
            ("Hurricane-Ready Roofing", "Post-storm replacement cycles.", "/roof-cost-calculator/"),
            ("HVAC Replacement", "Humidity and efficiency upgrades.", "/hvac-cost-calculator/"),
            ("Bathroom Remodels", "Popular in aging coastal housing stock.", "/cost/bathroom-remodel/"),
            ("Fencing &amp; Outdoor", "Pool enclosures and privacy fences.", "/fence-cost-calculator/"),
        ],
        suburbs=[("St. Petersburg", "st-petersburg"), ("Clearwater", "clearwater"), ("Brandon", "brandon"), ("Riverview", "riverview"), ("Wesley Chapel", "wesley-chapel"), ("Lakeland", "lakeland")],
        nearby_cities=[("Orlando", "orlando"), ("St. Petersburg", "st-petersburg"), ("Miami", "miami"), ("Jacksonville", "jacksonville")],
        nearby_suburbs=[("St. Petersburg", "st-petersburg"), ("Clearwater", "clearwater"), ("Brandon", "brandon"), ("Riverview", "riverview")],
        examples=[
            ("St. Petersburg, FL", "Architectural shingle roof · wind rated", "$14,100", "/roof-cost-calculator/"),
            ("Brandon, FL", "Bathroom remodel · walk-in shower", "$11,800", "/cost/bathroom-remodel/"),
            ("Clearwater, FL", "Heat pump HVAC · 2,000 sq ft", "$9,200", "/hvac-cost-calculator/"),
        ],
        footer_suburbs=[("St. Petersburg", "st-petersburg"), ("Clearwater", "clearwater"), ("Brandon", "brandon")],
    ),
    _city(
        slug="austin",
        state_slug="texas",
        state_name="Texas",
        state_abbr="TX",
        city_name="Austin",
        city_key="austin",
        lead_zip="78701",
        market_insight=(
            "Austin homeowners blend tech-driven remodels with heat-ready systems — open kitchens, "
            "energy upgrades, and durable roofing for Central Texas weather."
        ),
        market_bullets=[
            "Fast-growing suburbs and new construction",
            "Modern farmhouse &amp; open-concept remodels",
            "Strong demand for mini-splits and heat pumps",
            "Solar growth with rising utility rates",
            "Competitive contractor market vs. coastal cities",
        ],
        climate_bullets=[
            "Long cooling season with occasional hard freezes",
            "Hail events in spring storm season",
            "Clay soil movement affects foundations &amp; fences",
            "Energy code pushes higher-efficiency HVAC",
        ],
        metro_callout=(
            "<strong>Greater Austin</strong> stretches through Travis, Williamson &amp; Hays counties — "
            "from urban condos to Hill Country suburban builds."
        ),
        trending=[
            ("Kitchen Remodels", "Top project in 1980s–2000s stock.", "/cost/kitchen-remodel/"),
            ("Roof Replacement", "Hail and age-driven upgrades.", "/roof-cost-calculator/"),
            ("Solar Panels", "Rising adoption in new suburbs.", "/solar-panel-cost-calculator/"),
            ("ADUs &amp; Additions", "Growing rental and family demand.", "/cost/kitchen-remodel/"),
        ],
        suburbs=[("Round Rock", "round-rock"), ("Cedar Park", "cedar-park"), ("Pflugerville", "pflugerville"), ("Georgetown", "georgetown"), ("Leander", "leander"), ("Kyle", "kyle")],
        nearby_cities=[("Dallas", "dallas"), ("San Antonio", "san-antonio"), ("Houston", "houston"), ("San Marcos", "san-marcos")],
        nearby_suburbs=[("Round Rock", "round-rock"), ("Cedar Park", "cedar-park"), ("Pflugerville", "pflugerville"), ("Georgetown", "georgetown")],
        examples=[
            ("Round Rock, TX", "LVP flooring · 1,400 sq ft", "$7,600", "/flooring-materials/luxury-vinyl-plank-flooring-cost/"),
            ("Cedar Park, TX", "Roof replacement · architectural shingles", "$12,900", "/roof-cost-calculator/"),
            ("Pflugerville, TX", "Heat pump install · 2,300 sq ft", "$10,400", "/hvac-cost-calculator/"),
        ],
        footer_suburbs=[("Round Rock", "round-rock"), ("Cedar Park", "cedar-park"), ("Pflugerville", "pflugerville")],
    ),
    _city(
        slug="raleigh",
        state_slug="north-carolina",
        state_name="North Carolina",
        state_abbr="NC",
        city_name="Raleigh",
        city_key="raleigh",
        lead_zip="27601",
        market_insight=(
            "Raleigh and the Research Triangle favor practical upgrades — architectural shingles, "
            "efficient HVAC, and remodels for growing families in suburban neighborhoods."
        ),
        market_bullets=[
            "Research Triangle growth fuels remodel demand",
            "Moderate climate balances heating &amp; cooling",
            "Architectural asphalt dominates roofing",
            "Fencing popular in Cary &amp; Apex subdivisions",
            "Lower labor costs vs. Northeast metros",
        ],
        climate_bullets=[
            "Humid summers and mild winters",
            "Occasional ice storms affect roofing choices",
            "Pine pollen and moisture — deck &amp; fence maintenance",
            "Crawl-space homes common — HVAC duct considerations",
        ],
        metro_callout=(
            "The <strong>Raleigh–Durham</strong> corridor includes Cary, Apex &amp; Wake Forest — "
            "strong job growth supports steady home improvement spending."
        ),
        trending=[
            ("Roof Replacement", "Aging 20-year shingle cycles.", "/roof-cost-calculator/"),
            ("Kitchen &amp; Bath Remodels", "Suburban move-up buyers.", "/cost/kitchen-remodel/"),
            ("HVAC Upgrades", "Heat pumps gaining share.", "/hvac-cost-calculator/"),
            ("LVP Flooring", "Popular over carpet in renovations.", "/flooring-cost-calculator/"),
        ],
        suburbs=[("Cary", "cary"), ("Apex", "apex"), ("Durham", "durham"), ("Wake Forest", "wake-forest"), ("Chapel Hill", "chapel-hill"), ("Morrisville", "morrisville")],
        nearby_cities=[("Charlotte", "charlotte"), ("Durham", "durham"), ("Greensboro", "greensboro"), ("Wilmington", "wilmington")],
        nearby_suburbs=[("Cary", "cary"), ("Apex", "apex"), ("Durham", "durham"), ("Wake Forest", "wake-forest")],
        examples=[
            ("Cary, NC", "Kitchen refresh · cabinets &amp; counters", "$18,500", "/cost/kitchen-remodel/"),
            ("Apex, NC", "Roof replacement · architectural shingles", "$11,400", "/roof-cost-calculator/"),
            ("Durham, NC", "Mini-split zones · older home", "$9,800", "/hvac-cost-calculator/mini-split/"),
        ],
        footer_suburbs=[("Cary", "cary"), ("Apex", "apex"), ("Durham", "durham")],
    ),
    _city(
        slug="san-diego",
        state_slug="california",
        state_name="California",
        state_abbr="CA",
        city_name="San Diego",
        city_key="san-diego",
        lead_zip="92101",
        snapshots=[
            {"icon": "roof", "category": "Roofing", "title": "Roof Replacement", "range": "$9k–$22k", "href": "/roof-cost-calculator/"},
            {"icon": "bath", "category": "Bathroom Remodel", "title": "Bathroom Remodel", "range": "$12k–$38k", "href": "/cost/bathroom-remodel/"},
            {"icon": "hvac", "category": "HVAC", "title": "Central AC Installation", "range": "$6k–$16k", "href": "/hvac-cost-calculator/"},
            {"icon": "floor", "category": "Flooring", "title": "Flooring Installation", "range": "$5–$22/sq ft", "href": "/flooring-cost-calculator/"},
            {"icon": "fence", "category": "Fence", "title": "Wood Privacy Fence", "range": "$30–$75/linear ft", "href": "/fence-materials/wood-privacy-fence-cost/"},
            {"icon": "solar", "category": "Solar", "title": "Solar Panels", "range": "$14k–$40k", "href": "/solar-panel-cost-calculator/"},
        ],
        market_insight=(
            "San Diego homeowners pay premium labor rates for Title 24–compliant upgrades, "
            "coastal-ready roofing, solar, and high-end kitchen and bath remodels."
        ),
        market_bullets=[
            "Highest coastal labor rates in our markets",
            "Title 24 energy rules on HVAC &amp; solar",
            "Tile and cool-roof systems near the coast",
            "ADU and addition projects common",
            "Salt air affects exterior material choices",
        ],
        climate_bullets=[
            "Mild climate with coastal marine layer",
            "Wildfire and ember-zone roofing in inland areas",
            "Water-wise landscaping drives hardscape demand",
            "Strong solar economics with time-of-use rates",
        ],
        metro_callout=(
            "<strong>San Diego County</strong> runs from coastal La Jolla to inland Chula Vista — "
            "permit costs and labor reflect California coastal premiums."
        ),
        trending=[
            ("Solar + Battery", "Time-of-use rate optimization.", "/solar-panel-cost-calculator/"),
            ("Kitchen Remodels", "High-end coastal renovations.", "/cost/kitchen-remodel/"),
            ("Roof Replacement", "Tile and composition re-roofs.", "/roof-cost-calculator/"),
            ("ADU Construction", "Rental and family housing demand.", "/cost/kitchen-remodel/"),
        ],
        suburbs=[("La Jolla", "la-jolla"), ("Encinitas", "encinitas"), ("Carlsbad", "carlsbad"), ("Chula Vista", "chula-vista"), ("Oceanside", "oceanside"), ("Escondido", "escondido")],
        nearby_cities=[("Los Angeles", "los-angeles"), ("Orange County", "orange-county"), ("Phoenix", "phoenix"), ("Tijuana", "tijuana")],
        nearby_suburbs=[("La Jolla", "la-jolla"), ("Encinitas", "encinitas"), ("Carlsbad", "carlsbad"), ("Chula Vista", "chula-vista")],
        examples=[
            ("La Jolla, CA", "Tile roof · coastal wind rating", "$19,800", "/roof-cost-calculator/"),
            ("Encinitas, CA", "Solar + Powerwall · 8 kW", "$26,500", "/solar-panel-cost-calculator/"),
            ("Carlsbad, CA", "Kitchen remodel · open concept", "$42,000", "/cost/kitchen-remodel/"),
        ],
        footer_suburbs=[("La Jolla", "la-jolla"), ("Encinitas", "encinitas"), ("Carlsbad", "carlsbad")],
    ),
]

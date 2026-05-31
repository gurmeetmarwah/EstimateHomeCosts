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
        suburbs=[("Glendale", "glendale"), ("Tempe", "tempe"), ("Gilbert", "gilbert"), ("Peoria", "peoria"), ("Surprise", "surprise"), ("Avondale", "avondale")],
        nearby_cities=[("Scottsdale", "scottsdale"), ("Mesa", "mesa"), ("Chandler", "chandler"), ("Tucson", "tucson")],
        nearby_suburbs=[("Glendale", "glendale"), ("Tempe", "tempe"), ("Gilbert", "gilbert"), ("Peoria", "peoria")],
        examples=[
            ("Glendale, AZ", "Central AC · high-SEER replacement", "$8,400", "/hvac-cost-calculator/"),
            ("Tempe, AZ", "Kitchen remodel · open concept", "$19,800", "/cost/kitchen-remodel/"),
            ("Peoria, AZ", "Tile roof replacement · concrete tile", "$15,600", "/roof-cost-calculator/"),
        ],
        footer_suburbs=[("Glendale", "glendale"), ("Tempe", "tempe"), ("Gilbert", "gilbert")],
    ),
    _city(
        slug="scottsdale",
        state_slug="arizona",
        state_name="Arizona",
        state_abbr="AZ",
        city_name="Scottsdale",
        city_key="scottsdale",
        lead_zip="85251",
        snapshots=[
            {"icon": "roof", "category": "Roofing", "title": "Roof Replacement", "range": "$9k–$24k", "href": "/roof-cost-calculator/"},
            {"icon": "bath", "category": "Bathroom Remodel", "title": "Bathroom Remodel", "range": "$12k–$38k", "href": "/cost/bathroom-remodel/"},
            {"icon": "hvac", "category": "HVAC", "title": "Central AC Installation", "range": "$6k–$17k", "href": "/hvac-cost-calculator/"},
            {"icon": "floor", "category": "Flooring", "title": "Flooring Installation", "range": "$5–$22/sq ft", "href": "/flooring-cost-calculator/"},
            {"icon": "fence", "category": "Fence", "title": "Wood Privacy Fence", "range": "$30–$75/linear ft", "href": "/fence-materials/wood-privacy-fence-cost/"},
            {"icon": "solar", "category": "Solar", "title": "Solar Panels", "range": "$15k–$40k", "href": "/solar-panel-cost-calculator/"},
        ],
        market_insight=(
            "Scottsdale homeowners invest in premium desert landscaping, luxury kitchen and bath "
            "remodels, tile roofing, and high-end outdoor living with strict HOA standards."
        ),
        market_bullets=[
            "Premium labor rates above Phoenix metro average",
            "HOA architectural standards drive exterior projects",
            "Tile, metal &amp; cool-roof systems for desert heat",
            "Luxury outdoor kitchens, pools &amp; hardscape demand",
            "Strong solar adoption on large custom homes",
        ],
        climate_bullets=[
            "Extreme desert heat and UV exposure",
            "Monsoon wind and dust storms",
            "Low humidity — high cooling load all summer",
            "Radiant barriers critical on tile-roof homes",
        ],
        metro_callout=(
            "<strong>Scottsdale &amp; North Valley</strong> includes Paradise Valley and "
            "premium master-planned communities — labor and materials run above East Valley averages."
        ),
        trending=[
            ("Luxury Kitchen Remodels", "High-end finishes and custom cabinetry.", "/cost/kitchen-remodel/"),
            ("Tile &amp; Metal Roofs", "HOA-preferred desert materials.", "/roof-cost-calculator/"),
            ("Solar + Battery", "Large homes with high electric loads.", "/solar-panel-cost-calculator/"),
            ("Outdoor Living", "Pools, pergolas &amp; desert landscaping.", "/fence-cost-calculator/"),
        ],
        suburbs=[("Paradise Valley", "paradise-valley"), ("Fountain Hills", "fountain-hills"), ("Cave Creek", "cave-creek"), ("North Scottsdale", "north-scottsdale"), ("McCormick Ranch", "mccormick-ranch"), ("DC Ranch", "dc-ranch")],
        nearby_cities=[("Phoenix", "phoenix"), ("Mesa", "mesa"), ("Chandler", "chandler"), ("Tucson", "tucson")],
        nearby_suburbs=[("Paradise Valley", "paradise-valley"), ("Fountain Hills", "fountain-hills"), ("Cave Creek", "cave-creek"), ("North Scottsdale", "north-scottsdale")],
        examples=[
            ("Paradise Valley, AZ", "Kitchen remodel · custom cabinetry", "$48,000", "/cost/kitchen-remodel/"),
            ("Fountain Hills, AZ", "Tile roof · concrete tile", "$18,400", "/roof-cost-calculator/"),
            ("North Scottsdale, AZ", "Solar + battery · 10 kW", "$28,600", "/solar-panel-cost-calculator/"),
        ],
        footer_suburbs=[("Paradise Valley", "paradise-valley"), ("Fountain Hills", "fountain-hills"), ("Cave Creek", "cave-creek")],
    ),
    _city(
        slug="mesa",
        state_slug="arizona",
        state_name="Arizona",
        state_abbr="AZ",
        city_name="Mesa",
        city_key="mesa",
        lead_zip="85201",
        market_insight=(
            "Mesa homeowners focus on affordable HVAC upgrades, solar on 1990s–2000s suburban "
            "stock, and practical kitchen and flooring refreshes in the East Valley."
        ),
        market_bullets=[
            "Affordable labor vs. Scottsdale and North Valley",
            "Strong solar ROI on single-family ranches",
            "LVP and tile flooring popular in remodels",
            "HOA communities with desert landscaping rules",
            "Growing East Valley suburban housing stock",
        ],
        climate_bullets=[
            "120°F+ summer heat drives AC replacement cycles",
            "Monsoon dust and wind affect roofing",
            "UV degradation on stucco and exterior paint",
            "Attic ventilation and radiant barriers recommended",
        ],
        metro_callout=(
            "<strong>Mesa &amp; the East Valley</strong> offer more affordable project costs than "
            "Scottsdale while sharing the same extreme Sonoran Desert climate."
        ),
        trending=[
            ("Solar Panels", "Strong production on east-facing roofs.", "/solar-panel-cost-calculator/"),
            ("HVAC Upgrades", "High-SEER replacements in aging stock.", "/hvac-cost-calculator/"),
            ("LVP Flooring", "Popular over carpet in renovations.", "/flooring-cost-calculator/"),
            ("Roof Replacement", "Tile and composition re-roofs.", "/roof-cost-calculator/"),
        ],
        suburbs=[("Apache Junction", "apache-junction"), ("Queen Creek", "queen-creek"), ("Gold Canyon", "gold-canyon"), ("Red Mountain", "red-mountain"), ("Superstition Springs", "superstition-springs"), ("Eastmark", "eastmark")],
        nearby_cities=[("Phoenix", "phoenix"), ("Scottsdale", "scottsdale"), ("Chandler", "chandler"), ("Tucson", "tucson")],
        nearby_suburbs=[("Apache Junction", "apache-junction"), ("Queen Creek", "queen-creek"), ("Gold Canyon", "gold-canyon"), ("Eastmark", "eastmark")],
        examples=[
            ("Queen Creek, AZ", "Solar + battery · 7.5 kW system", "$21,400", "/solar-panel-cost-calculator/"),
            ("Apache Junction, AZ", "Central AC · 2,000 sq ft", "$8,200", "/hvac-cost-calculator/"),
            ("Gold Canyon, AZ", "LVP flooring · 1,500 sq ft", "$7,800", "/flooring-materials/luxury-vinyl-plank-flooring-cost/"),
        ],
        footer_suburbs=[("Apache Junction", "apache-junction"), ("Queen Creek", "queen-creek"), ("Gold Canyon", "gold-canyon")],
    ),
    _city(
        slug="tucson",
        state_slug="arizona",
        state_name="Arizona",
        state_abbr="AZ",
        city_name="Tucson",
        city_key="tucson",
        lead_zip="85701",
        market_insight=(
            "Tucson homeowners prioritize cooling-focused HVAC, tile roofing on older adobe-influenced "
            "homes, and budget-friendly remodels in Southern Arizona's lower-cost market."
        ),
        market_bullets=[
            "Lower labor costs vs. Phoenix metro",
            "Older housing stock drives roof &amp; HVAC cycles",
            "Tile and flat-roof systems common",
            "University-area rental remodel demand",
            "Monsoon drainage and stucco repair needs",
        ],
        climate_bullets=[
            "Extreme summer heat with monsoon storms",
            "Lower elevation micro-climates in foothills",
            "Hard water affects plumbing-adjacent projects",
            "Evaporative cooling still found in older homes",
        ],
        metro_callout=(
            "<strong>Greater Tucson</strong> spans Pima County from the Santa Catalina foothills "
            "to Oro Valley — project costs typically run below Phoenix averages."
        ),
        trending=[
            ("Roof Replacement", "Tile and flat-roof re-coats.", "/roof-cost-calculator/"),
            ("HVAC Replacement", "Essential in 100°F+ summers.", "/hvac-cost-calculator/"),
            ("Bathroom Remodels", "Walk-in showers in older homes.", "/cost/bathroom-remodel/"),
            ("Solar Panels", "Strong sun with lower install costs.", "/solar-panel-cost-calculator/"),
        ],
        suburbs=[("Oro Valley", "oro-valley"), ("Marana", "marana"), ("Sahuarita", "sahuarita"), ("Green Valley", "green-valley"), ("Catalina Foothills", "catalina-foothills"), ("Vail", "vail")],
        nearby_cities=[("Phoenix", "phoenix"), ("Scottsdale", "scottsdale"), ("Mesa", "mesa"), ("Chandler", "chandler")],
        nearby_suburbs=[("Oro Valley", "oro-valley"), ("Marana", "marana"), ("Sahuarita", "sahuarita"), ("Catalina Foothills", "catalina-foothills")],
        examples=[
            ("Oro Valley, AZ", "Tile roof replacement · concrete tile", "$14,200", "/roof-cost-calculator/"),
            ("Marana, AZ", "Central AC · 2,100 sq ft", "$7,900", "/hvac-cost-calculator/"),
            ("Catalina Foothills, AZ", "Bathroom remodel · walk-in shower", "$12,400", "/cost/bathroom-remodel/"),
        ],
        footer_suburbs=[("Oro Valley", "oro-valley"), ("Marana", "marana"), ("Sahuarita", "sahuarita")],
    ),
    _city(
        slug="chandler",
        state_slug="arizona",
        state_name="Arizona",
        state_abbr="AZ",
        city_name="Chandler",
        city_key="chandler",
        lead_zip="85224",
        market_insight=(
            "Chandler homeowners upgrade HOA-compliant exteriors, efficient HVAC, and family-friendly "
            "kitchen and flooring projects in fast-growing East Valley neighborhoods."
        ),
        market_bullets=[
            "Family subdivisions built 1990s–2010s",
            "HOA-driven fencing and landscaping standards",
            "Tech-sector growth fuels remodel spending",
            "Mini-split and heat pump adoption rising",
            "Competitive contractor market vs. North Valley",
        ],
        climate_bullets=[
            "Long cooling season with extreme peak temps",
            "Monsoon wind exposure on newer tile roofs",
            "Desert landscaping and pool-area upgrades",
            "Solar-friendly roof orientations in tracts",
        ],
        metro_callout=(
            "<strong>Chandler &amp; the Southeast Valley</strong> includes Ocotillo and "
            "Price Road corridor suburbs — strong demand for mid-range remodels and solar."
        ),
        trending=[
            ("Kitchen Remodels", "Open-concept updates in 2000s stock.", "/cost/kitchen-remodel/"),
            ("Central AC Installation", "High-SEER replacements.", "/hvac-cost-calculator/"),
            ("Solar Panels", "Popular on south-facing roofs.", "/solar-panel-cost-calculator/"),
            ("Backyard Fencing", "Pool-area privacy enclosures.", "/fence-cost-calculator/"),
        ],
        suburbs=[("Gilbert", "gilbert"), ("Sun Lakes", "sun-lakes"), ("Ahwatukee", "ahwatukee"), ("Ocotillo", "ocotillo"), ("San Tan Valley", "san-tan-valley"), ("Chandler Heights", "chandler-heights")],
        nearby_cities=[("Phoenix", "phoenix"), ("Mesa", "mesa"), ("Scottsdale", "scottsdale"), ("Tucson", "tucson")],
        nearby_suburbs=[("Gilbert", "gilbert"), ("Sun Lakes", "sun-lakes"), ("Ahwatukee", "ahwatukee"), ("Ocotillo", "ocotillo")],
        examples=[
            ("Gilbert, AZ", "Central AC · high-SEER replacement", "$8,600", "/hvac-cost-calculator/"),
            ("Sun Lakes, AZ", "Kitchen refresh · quartz counters", "$17,200", "/cost/kitchen-remodel/"),
            ("San Tan Valley, AZ", "Solar · 8 kW rooftop system", "$19,800", "/solar-panel-cost-calculator/"),
        ],
        footer_suburbs=[("Gilbert", "gilbert"), ("Sun Lakes", "sun-lakes"), ("Ahwatukee", "ahwatukee")],
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
        suburbs=[("Clearwater", "clearwater"), ("Brandon", "brandon"), ("Riverview", "riverview"), ("Wesley Chapel", "wesley-chapel"), ("Lakeland", "lakeland"), ("Plant City", "plant-city")],
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
        slug="orlando",
        state_slug="florida",
        state_name="Florida",
        state_abbr="FL",
        city_name="Orlando",
        city_key="orlando",
        lead_zip="32801",
        market_insight=(
            "Orlando homeowners prioritize high-efficiency HVAC, hurricane-rated roofing, "
            "and remodels for fast-growing suburban neighborhoods and vacation-adjacent housing."
        ),
        market_bullets=[
            "Central Florida heat drives year-round AC demand",
            "Theme-park metro growth fuels kitchen &amp; bath upgrades",
            "Wind-rated roofing common in inland storm paths",
            "Pool enclosures, fencing &amp; outdoor living popular",
            "Strong investor and short-term rental remodel activity",
        ],
        climate_bullets=[
            "Hot, humid summers with afternoon thunderstorms",
            "Hurricane wind exposure from Atlantic systems",
            "High cooling load on older ranch-style homes",
            "Lightning and surge protection for HVAC equipment",
        ],
        metro_callout=(
            "<strong>Greater Orlando</strong> spans Orange, Osceola &amp; Seminole counties — "
            "from downtown condos to master-planned suburbs in Lake Nona and Winter Park."
        ),
        trending=[
            ("HVAC Replacement", "Essential in Central Florida heat.", "/hvac-cost-calculator/"),
            ("Kitchen Remodels", "Popular in 1990s–2000s suburban stock.", "/cost/kitchen-remodel/"),
            ("Hurricane-Ready Roofing", "Wind-rated shingles and tile upgrades.", "/roof-cost-calculator/"),
            ("Pool Fencing &amp; Outdoor", "Screened enclosures and privacy fences.", "/fence-cost-calculator/"),
        ],
        suburbs=[("Kissimmee", "kissimmee"), ("Winter Park", "winter-park"), ("Sanford", "sanford"), ("Lake Nona", "lake-nona"), ("Altamonte Springs", "altamonte-springs"), ("Oviedo", "oviedo")],
        nearby_cities=[("Tampa", "tampa"), ("Miami", "miami"), ("Jacksonville", "jacksonville"), ("St. Petersburg", "st-petersburg")],
        nearby_suburbs=[("Kissimmee", "kissimmee"), ("Winter Park", "winter-park"), ("Sanford", "sanford"), ("Lake Nona", "lake-nona")],
        examples=[
            ("Winter Park, FL", "Kitchen remodel · open concept", "$22,400", "/cost/kitchen-remodel/"),
            ("Kissimmee, FL", "Central AC replacement · 2,100 sq ft", "$9,600", "/hvac-cost-calculator/"),
            ("Lake Nona, FL", "Roof replacement · architectural shingles", "$13,800", "/roof-cost-calculator/"),
        ],
        footer_suburbs=[("Kissimmee", "kissimmee"), ("Winter Park", "winter-park"), ("Sanford", "sanford")],
    ),
    _city(
        slug="miami",
        state_slug="florida",
        state_name="Florida",
        state_abbr="FL",
        city_name="Miami",
        city_key="miami",
        lead_zip="33130",
        snapshots=[
            {"icon": "roof", "category": "Roofing", "title": "Roof Replacement", "range": "$10k–$26k", "href": "/roof-cost-calculator/"},
            {"icon": "bath", "category": "Bathroom Remodel", "title": "Bathroom Remodel", "range": "$14k–$42k", "href": "/cost/bathroom-remodel/"},
            {"icon": "hvac", "category": "HVAC", "title": "Central AC Installation", "range": "$6k–$18k", "href": "/hvac-cost-calculator/"},
            {"icon": "floor", "category": "Flooring", "title": "Flooring Installation", "range": "$5–$24/sq ft", "href": "/flooring-cost-calculator/"},
            {"icon": "fence", "category": "Fence", "title": "Wood Privacy Fence", "range": "$32–$80/linear ft", "href": "/fence-materials/wood-privacy-fence-cost/"},
            {"icon": "solar", "category": "Solar", "title": "Solar Panels", "range": "$14k–$38k", "href": "/solar-panel-cost-calculator/"},
        ],
        market_insight=(
            "Miami homeowners face premium labor costs for hurricane-rated roofing, condo-friendly "
            "remodels, impact windows, and humidity-ready HVAC in a coastal high-rise market."
        ),
        market_bullets=[
            "Highest Florida labor rates in South Florida",
            "Condo &amp; HOA rules shape renovation scope",
            "Impact-rated roofing and window demand",
            "Salt air corrosion on exterior materials",
            "Strong solar economics with high electric rates",
        ],
        climate_bullets=[
            "Hurricane and tropical storm wind exposure",
            "Extreme humidity and mold-resistant materials",
            "Salt spray corrosion near the coast",
            "Year-round cooling with minimal heating",
        ],
        metro_callout=(
            "<strong>Miami-Dade &amp; Broward</strong> combine dense urban condos with suburban "
            "single-family homes — permit costs and labor reflect South Florida premiums."
        ),
        trending=[
            ("Impact Windows &amp; Roofing", "Insurance-driven exterior upgrades.", "/roof-cost-calculator/"),
            ("Bathroom Remodels", "Compact condo and townhome refreshes.", "/cost/bathroom-remodel/"),
            ("HVAC Replacement", "Humidity and corrosion-resistant systems.", "/hvac-cost-calculator/"),
            ("Solar Panels", "Strong sun and rising FPL rates.", "/solar-panel-cost-calculator/"),
        ],
        suburbs=[("Miami Beach", "miami-beach"), ("Coral Gables", "coral-gables"), ("Hialeah", "hialeah"), ("Fort Lauderdale", "fort-lauderdale"), ("Pembroke Pines", "pembroke-pines"), ("Homestead", "homestead")],
        nearby_cities=[("Tampa", "tampa"), ("Orlando", "orlando"), ("Jacksonville", "jacksonville"), ("Fort Lauderdale", "fort-lauderdale")],
        nearby_suburbs=[("Miami Beach", "miami-beach"), ("Coral Gables", "coral-gables"), ("Hialeah", "hialeah"), ("Fort Lauderdale", "fort-lauderdale")],
        examples=[
            ("Coral Gables, FL", "Tile roof replacement · concrete tile", "$19,200", "/roof-cost-calculator/"),
            ("Miami Beach, FL", "Bathroom remodel · walk-in shower", "$16,500", "/cost/bathroom-remodel/"),
            ("Pembroke Pines, FL", "Central AC · high-SEER coastal package", "$10,800", "/hvac-cost-calculator/"),
        ],
        footer_suburbs=[("Miami Beach", "miami-beach"), ("Coral Gables", "coral-gables"), ("Fort Lauderdale", "fort-lauderdale")],
    ),
    _city(
        slug="jacksonville",
        state_slug="florida",
        state_name="Florida",
        state_abbr="FL",
        city_name="Jacksonville",
        city_key="jacksonville",
        lead_zip="32202",
        market_insight=(
            "Jacksonville homeowners benefit from more affordable labor than South Florida while "
            "still planning for humidity-ready HVAC, storm-rated roofing, and suburban fencing."
        ),
        market_bullets=[
            "Affordable labor vs. Miami and Tampa metros",
            "Large suburban housing stock built 1980s–2000s",
            "Roof replacement cycles after storm seasons",
            "Fencing and outdoor living in family neighborhoods",
            "Growing demand for energy-efficient HVAC upgrades",
        ],
        climate_bullets=[
            "Humid subtropical climate with hot summers",
            "Hurricane exposure from Atlantic and Gulf systems",
            "Salt air in beach communities affects exteriors",
            "Moderate heating needs vs. South Florida",
        ],
        metro_callout=(
            "<strong>Greater Jacksonville</strong> covers Duval, St. Johns &amp; Clay counties — "
            "from historic Riverside to fast-growing suburbs in St. Johns and Nocatee."
        ),
        trending=[
            ("Roof Replacement", "Storm and age-driven re-roof demand.", "/roof-cost-calculator/"),
            ("HVAC Upgrades", "Humidity control and efficiency.", "/hvac-cost-calculator/"),
            ("Kitchen Remodels", "Suburban open-concept updates.", "/cost/kitchen-remodel/"),
            ("Backyard Fencing", "Privacy fences in new subdivisions.", "/fence-cost-calculator/"),
        ],
        suburbs=[("Jacksonville Beach", "jacksonville-beach"), ("Orange Park", "orange-park"), ("St. Augustine", "st-augustine"), ("Ponte Vedra", "ponte-vedra"), ("Fernandina Beach", "fernandina-beach"), ("Mandarin", "mandarin")],
        nearby_cities=[("Tampa", "tampa"), ("Orlando", "orlando"), ("Miami", "miami"), ("St. Augustine", "st-augustine")],
        nearby_suburbs=[("Jacksonville Beach", "jacksonville-beach"), ("Orange Park", "orange-park"), ("St. Augustine", "st-augustine"), ("Ponte Vedra", "ponte-vedra")],
        examples=[
            ("St. Augustine, FL", "Roof replacement · wind-rated shingles", "$12,600", "/roof-cost-calculator/"),
            ("Orange Park, FL", "LVP flooring · 1,600 sq ft", "$7,400", "/flooring-materials/luxury-vinyl-plank-flooring-cost/"),
            ("Ponte Vedra, FL", "Heat pump HVAC · 2,200 sq ft", "$9,900", "/hvac-cost-calculator/"),
        ],
        footer_suburbs=[("Jacksonville Beach", "jacksonville-beach"), ("Orange Park", "orange-park"), ("St. Augustine", "st-augustine")],
    ),
    _city(
        slug="st-petersburg",
        state_slug="florida",
        state_name="Florida",
        state_abbr="FL",
        city_name="St. Petersburg",
        city_key="st-petersburg",
        lead_zip="33701",
        market_insight=(
            "St. Petersburg homeowners invest in coastal-ready roofing, bath remodels in aging "
            "block homes, and humidity-focused HVAC across the Pinellas peninsula."
        ),
        market_bullets=[
            "Coastal wind ratings for roofing near Tampa Bay",
            "Bath and kitchen remodels in mid-century housing",
            "Flood-zone and elevation affect project planning",
            "Tile and metal roofs common near the waterfront",
            "Strong demand for screened patios and fencing",
        ],
        climate_bullets=[
            "Hurricane season exposure on the Gulf Coast",
            "Salt air corrosion on HVAC and fasteners",
            "High humidity — mold-resistant materials matter",
            "Year-round cooling with efficient AC demand",
        ],
        metro_callout=(
            "<strong>St. Petersburg &amp; Pinellas County</strong> sit on a coastal peninsula — "
            "building codes and insurance requirements shape roofing and exterior project costs."
        ),
        trending=[
            ("Coastal Roofing", "Wind-rated tile and shingle upgrades.", "/roof-cost-calculator/"),
            ("Bathroom Remodels", "Popular in 1950s–1970s block homes.", "/cost/bathroom-remodel/"),
            ("HVAC Replacement", "Humidity and salt-air resistant systems.", "/hvac-cost-calculator/"),
            ("Fencing &amp; Outdoor", "Pool-area privacy and enclosures.", "/fence-cost-calculator/"),
        ],
        suburbs=[("Clearwater", "clearwater"), ("Largo", "largo"), ("Pinellas Park", "pinellas-park"), ("Gulfport", "gulfport"), ("Treasure Island", "treasure-island"), ("Seminole", "seminole")],
        nearby_cities=[("Tampa", "tampa"), ("Orlando", "orlando"), ("Miami", "miami"), ("Clearwater", "clearwater")],
        nearby_suburbs=[("Clearwater", "clearwater"), ("Largo", "largo"), ("Pinellas Park", "pinellas-park"), ("Gulfport", "gulfport")],
        examples=[
            ("Clearwater, FL", "Heat pump HVAC · 2,000 sq ft", "$9,200", "/hvac-cost-calculator/"),
            ("Largo, FL", "Bathroom remodel · tub-to-shower", "$11,200", "/cost/bathroom-remodel/"),
            ("Gulfport, FL", "Roof replacement · architectural shingles", "$13,400", "/roof-cost-calculator/"),
        ],
        footer_suburbs=[("Clearwater", "clearwater"), ("Largo", "largo"), ("Pinellas Park", "pinellas-park")],
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
        slug="houston",
        state_slug="texas",
        state_name="Texas",
        state_abbr="TX",
        city_name="Houston",
        city_key="houston",
        lead_zip="77002",
        market_insight=(
            "Houston homeowners prioritize humidity-ready HVAC, wind-rated roofing, and moisture-resistant "
            "materials for Gulf Coast heat, storms, and year-round dehumidification needs."
        ),
        market_bullets=[
            "Year-round humidity drives high-SEER AC and duct sealing",
            "Storm and wind exposure shape roofing material choices",
            "Fast-growing suburbs in Harris, Fort Bend &amp; Montgomery counties",
            "Foundation and drainage work common on clay soils",
            "Strong demand for fencing, patios &amp; outdoor living",
        ],
        climate_bullets=[
            "High humidity — mold-resistant materials and dehumidification matter",
            "Hurricane and tropical storm wind exposure near the coast",
            "Long cooling season with heavy AC runtime",
            "Clay soils and flooding awareness affect exterior projects",
        ],
        metro_callout=(
            "The <strong>Greater Houston</strong> area spans Harris, Fort Bend &amp; Montgomery counties — "
            "from inner-loop bungalows to master-planned suburbs in Katy and The Woodlands."
        ),
        trending=[
            ("Roof Replacement", "Wind and storm-driven re-roof cycles.", "/roof-cost-calculator/"),
            ("HVAC Replacement", "Humidity control and efficiency upgrades.", "/hvac-cost-calculator/"),
            ("Kitchen Remodels", "Popular in 1980s–2000s suburban stock.", "/cost/kitchen-remodel/"),
            ("Backyard Fencing", "Privacy fences in family neighborhoods.", "/fence-cost-calculator/"),
        ],
        suburbs=[("The Woodlands", "the-woodlands"), ("Katy", "katy"), ("Sugar Land", "sugar-land"), ("Pearland", "pearland"), ("League City", "league-city"), ("Cypress", "cypress")],
        nearby_cities=[("Dallas", "dallas"), ("Austin", "austin"), ("San Antonio", "san-antonio"), ("Fort Worth", "fort-worth")],
        nearby_suburbs=[("The Woodlands", "the-woodlands"), ("Katy", "katy"), ("Sugar Land", "sugar-land"), ("Pearland", "pearland")],
        examples=[
            ("Katy, TX", "Roof replacement · architectural shingles", "$12,400", "/roof-cost-calculator/"),
            ("The Woodlands, TX", "Central AC · 2,400 sq ft high-SEER", "$9,100", "/hvac-cost-calculator/"),
            ("Sugar Land, TX", "LVP flooring · 1,500 sq ft", "$7,200", "/flooring-materials/luxury-vinyl-plank-flooring-cost/"),
        ],
        footer_suburbs=[("The Woodlands", "the-woodlands"), ("Katy", "katy"), ("Sugar Land", "sugar-land")],
    ),
    _city(
        slug="san-antonio",
        state_slug="texas",
        state_name="Texas",
        state_abbr="TX",
        city_name="San Antonio",
        city_key="san-antonio",
        lead_zip="78205",
        market_insight=(
            "San Antonio homeowners focus on stucco-friendly exteriors, heat-ready HVAC, tile roofing, "
            "and practical remodels in one of Texas's most affordable major metros."
        ),
        market_bullets=[
            "Stucco and tile exteriors common in South Texas builds",
            "Affordable labor vs. Austin and coastal metros",
            "Strong military &amp; family housing remodel demand",
            "Hard water affects plumbing-adjacent bath projects",
            "Growing suburbs along I-35 and Loop 1604",
        ],
        climate_bullets=[
            "Hot summers with moderate humidity vs. Houston",
            "Occasional hard freezes — pipe and HVAC freeze protection",
            "Limestone and clay soils affect foundations &amp; fencing",
            "Long cooling season favors high-efficiency AC",
        ],
        metro_callout=(
            "<strong>Greater San Antonio</strong> includes Bexar County and fast-growing northern "
            "suburbs — from historic neighborhoods to new master-planned communities."
        ),
        trending=[
            ("Roof Replacement", "Tile and composition re-roofs in aging stock.", "/roof-cost-calculator/"),
            ("Bathroom Remodels", "Walk-in showers and master bath updates.", "/cost/bathroom-remodel/"),
            ("HVAC Upgrades", "Central AC and mini-split additions.", "/hvac-cost-calculator/"),
            ("Backyard Fencing", "Privacy fencing in suburban tracts.", "/fence-cost-calculator/"),
        ],
        suburbs=[("New Braunfels", "new-braunfels"), ("Schertz", "schertz"), ("Converse", "converse"), ("Boerne", "boerne"), ("Helotes", "helotes"), ("Alamo Heights", "alamo-heights")],
        nearby_cities=[("Austin", "austin"), ("Houston", "houston"), ("Dallas", "dallas"), ("San Marcos", "san-marcos")],
        nearby_suburbs=[("New Braunfels", "new-braunfels"), ("Schertz", "schertz"), ("Boerne", "boerne"), ("Helotes", "helotes")],
        examples=[
            ("New Braunfels, TX", "Roof replacement · tile over existing", "$14,800", "/roof-cost-calculator/"),
            ("Schertz, TX", "Bathroom remodel · tub-to-shower conversion", "$10,600", "/cost/bathroom-remodel/"),
            ("Boerne, TX", "Central AC replacement · 2,000 sq ft", "$7,900", "/hvac-cost-calculator/"),
        ],
        footer_suburbs=[("New Braunfels", "new-braunfels"), ("Schertz", "schertz"), ("Boerne", "boerne")],
    ),
    _city(
        slug="fort-worth",
        state_slug="texas",
        state_name="Texas",
        state_abbr="TX",
        city_name="Fort Worth",
        city_key="fort-worth",
        lead_zip="76102",
        market_insight=(
            "Fort Worth homeowners invest in hail-resistant roofing, suburban fencing, and efficient HVAC "
            "across the western half of the Dallas–Fort Worth metro."
        ),
        market_bullets=[
            "Hail-prone roofing demand similar to Dallas metro",
            "Western DFW suburban growth in Tarrant County",
            "Ranch-style homes common — single-story HVAC &amp; roof updates",
            "Backyard fencing popular in Keller, Mansfield &amp; Southlake",
            "Competitive contractor pricing vs. coastal Texas metros",
        ],
        climate_bullets=[
            "Hailstorms drive impact-rated shingle upgrades",
            "100°F+ summers increase cooling load and AC wear",
            "Wind exposure on open suburban lots",
            "Attic insulation and radiant barriers for efficiency",
        ],
        metro_callout=(
            "<strong>Fort Worth &amp; western DFW</strong> covers Tarrant County and suburbs from "
            "Keller and Southlake to Mansfield and Burleson — distinct from Dallas proper but same storm climate."
        ),
        trending=[
            ("Roof Replacement", "Hail season drives re-roof demand.", "/roof-cost-calculator/"),
            ("Backyard Fencing", "Wood privacy fences in family neighborhoods.", "/fence-cost-calculator/"),
            ("HVAC Replacement", "Long cooling season wear on central AC.", "/hvac-cost-calculator/"),
            ("Kitchen Remodels", "Suburban open-concept updates.", "/cost/kitchen-remodel/"),
        ],
        suburbs=[("Keller", "keller"), ("Mansfield", "mansfield"), ("Southlake", "southlake"), ("Burleson", "burleson"), ("North Richland Hills", "north-richland-hills"), ("Grapevine", "grapevine")],
        nearby_cities=[("Dallas", "dallas"), ("Austin", "austin"), ("Houston", "houston"), ("Arlington", "arlington")],
        nearby_suburbs=[("Keller", "keller"), ("Mansfield", "mansfield"), ("Southlake", "southlake"), ("Burleson", "burleson")],
        examples=[
            ("Keller, TX", "Wood privacy fence · 180 linear ft", "$8,400", "/fence-cost-calculator/"),
            ("Mansfield, TX", "Roof replacement · impact-rated shingles", "$13,200", "/roof-cost-calculator/"),
            ("Southlake, TX", "Central AC · variable-speed 17 SEER", "$8,700", "/hvac-cost-calculator/"),
        ],
        footer_suburbs=[("Keller", "keller"), ("Mansfield", "mansfield"), ("Southlake", "southlake")],
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
        suburbs=[("Apex", "apex"), ("Wake Forest", "wake-forest"), ("Chapel Hill", "chapel-hill"), ("Morrisville", "morrisville"), ("Holly Springs", "holly-springs"), ("Garner", "garner")],
        nearby_cities=[("Charlotte", "charlotte"), ("Durham", "durham"), ("Cary", "cary"), ("Wilmington", "wilmington")],
        nearby_suburbs=[("Apex", "apex"), ("Wake Forest", "wake-forest"), ("Morrisville", "morrisville"), ("Holly Springs", "holly-springs")],
        examples=[
            ("Apex, NC", "Roof replacement · architectural shingles", "$11,400", "/roof-cost-calculator/"),
            ("Wake Forest, NC", "Kitchen refresh · cabinets &amp; counters", "$17,800", "/cost/kitchen-remodel/"),
            ("Holly Springs, NC", "Heat pump HVAC · 2,200 sq ft", "$10,200", "/hvac-cost-calculator/"),
        ],
        footer_suburbs=[("Apex", "apex"), ("Wake Forest", "wake-forest"), ("Morrisville", "morrisville")],
    ),
    _city(
        slug="charlotte",
        state_slug="north-carolina",
        state_name="North Carolina",
        state_abbr="NC",
        city_name="Charlotte",
        city_key="charlotte",
        lead_zip="28202",
        market_insight=(
            "Charlotte homeowners invest in suburban kitchen and bath remodels, architectural "
            "shingle roofing, and efficient HVAC in one of the Southeast's fastest-growing metros."
        ),
        market_bullets=[
            "Banking &amp; finance sector fuels move-up remodels",
            "Fast-growing suburbs in Mecklenburg &amp; Union counties",
            "Architectural asphalt dominates roofing",
            "Fencing popular in family subdivisions",
            "Moderate labor costs vs. Northeast metros",
        ],
        climate_bullets=[
            "Humid summers with strong cooling demand",
            "Mild winters — heat pumps gain market share",
            "Occasional ice storms affect roofing",
            "Red clay soil movement affects foundations &amp; fences",
        ],
        metro_callout=(
            "<strong>Greater Charlotte</strong> spans Mecklenburg, Union &amp; Cabarrus counties — "
            "from Uptown condos to fast-growing suburbs in Ballantyne and Huntersville."
        ),
        trending=[
            ("Kitchen Remodels", "Open-concept updates in 1990s–2000s stock.", "/cost/kitchen-remodel/"),
            ("Roof Replacement", "Aging shingle cycles after storms.", "/roof-cost-calculator/"),
            ("Heat Pump HVAC", "Efficient heating and cooling.", "/hvac-cost-calculator/heat-pump/"),
            ("LVP Flooring", "Popular over carpet in renovations.", "/flooring-cost-calculator/"),
        ],
        suburbs=[("Matthews", "matthews"), ("Huntersville", "huntersville"), ("Concord", "concord"), ("Fort Mill", "fort-mill"), ("Gastonia", "gastonia"), ("Mint Hill", "mint-hill")],
        nearby_cities=[("Raleigh", "raleigh"), ("Durham", "durham"), ("Cary", "cary"), ("Wilmington", "wilmington")],
        nearby_suburbs=[("Matthews", "matthews"), ("Huntersville", "huntersville"), ("Concord", "concord"), ("Fort Mill", "fort-mill")],
        examples=[
            ("Matthews, NC", "Kitchen remodel · quartz counters", "$19,600", "/cost/kitchen-remodel/"),
            ("Huntersville, NC", "Roof replacement · architectural shingles", "$12,200", "/roof-cost-calculator/"),
            ("Concord, NC", "Central AC · high-SEER replacement", "$8,900", "/hvac-cost-calculator/"),
        ],
        footer_suburbs=[("Matthews", "matthews"), ("Huntersville", "huntersville"), ("Concord", "concord")],
    ),
    _city(
        slug="durham",
        state_slug="north-carolina",
        state_name="North Carolina",
        state_abbr="NC",
        city_name="Durham",
        city_key="durham",
        lead_zip="27701",
        market_insight=(
            "Durham homeowners upgrade older housing near Duke and RTP with practical remodels, "
            "mini-split HVAC additions, and storm-ready roofing in the Research Triangle."
        ),
        market_bullets=[
            "University &amp; biotech growth drives rental remodels",
            "Older homes benefit from HVAC and electrical upgrades",
            "Bull City revitalization fuels kitchen &amp; bath projects",
            "Architectural shingles after storm seasons",
            "Competitive labor vs. coastal NC metros",
        ],
        climate_bullets=[
            "Humid Piedmont summers and mild winters",
            "Occasional ice storms and tree damage",
            "Crawl-space homes — duct sealing matters",
            "Pine pollen and moisture on decks &amp; fences",
        ],
        metro_callout=(
            "<strong>Durham &amp; the Triangle</strong> connects RTP employers with established "
            "neighborhoods and revitalized downtown housing stock."
        ),
        trending=[
            ("Mini-Split HVAC", "Zone cooling in older homes.", "/hvac-cost-calculator/mini-split/"),
            ("Bathroom Remodels", "Rental and owner-occupied updates.", "/cost/bathroom-remodel/"),
            ("Roof Replacement", "20-year shingle replacement cycles.", "/roof-cost-calculator/"),
            ("Kitchen Remodels", "Open kitchens in 1960s–1980s stock.", "/cost/kitchen-remodel/"),
        ],
        suburbs=[("Chapel Hill", "chapel-hill"), ("Morrisville", "morrisville"), ("Hillsborough", "hillsborough"), ("Creedmoor", "creedmoor"), ("Roxboro", "roxboro"), ("Butner", "butner")],
        nearby_cities=[("Raleigh", "raleigh"), ("Cary", "cary"), ("Charlotte", "charlotte"), ("Chapel Hill", "chapel-hill")],
        nearby_suburbs=[("Chapel Hill", "chapel-hill"), ("Morrisville", "morrisville"), ("Hillsborough", "hillsborough"), ("Creedmoor", "creedmoor")],
        examples=[
            ("Chapel Hill, NC", "Mini-split zones · older home", "$9,800", "/hvac-cost-calculator/mini-split/"),
            ("Morrisville, NC", "Bathroom remodel · walk-in shower", "$12,400", "/cost/bathroom-remodel/"),
            ("Hillsborough, NC", "Roof replacement · architectural shingles", "$11,800", "/roof-cost-calculator/"),
        ],
        footer_suburbs=[("Chapel Hill", "chapel-hill"), ("Morrisville", "morrisville"), ("Hillsborough", "hillsborough")],
    ),
    _city(
        slug="cary",
        state_slug="north-carolina",
        state_name="North Carolina",
        state_abbr="NC",
        city_name="Cary",
        city_key="cary",
        lead_zip="27511",
        market_insight=(
            "Cary homeowners prioritize family-friendly kitchen and bath remodels, privacy fencing, "
            "and efficient HVAC in top-rated Wake County subdivisions."
        ),
        market_bullets=[
            "Master-planned subdivisions with HOA standards",
            "Strong school districts drive move-up remodels",
            "Privacy fencing in backyard neighborhoods",
            "LVP flooring over carpet in renovations",
            "Steady demand from RTP commuter households",
        ],
        climate_bullets=[
            "Humid summers with moderate cooling load",
            "Mild winters — dual-fuel heat pumps popular",
            "Tree coverage affects roof moss and debris",
            "Crawl-space moisture in older sections",
        ],
        metro_callout=(
            "<strong>Cary &amp; western Wake County</strong> is one of the Triangle's most "
            "family-oriented markets for fencing, flooring, and kitchen upgrades."
        ),
        trending=[
            ("Kitchen Remodels", "Cabinet &amp; counter refreshes.", "/cost/kitchen-remodel/"),
            ("Backyard Fencing", "Wood privacy in subdivisions.", "/fence-cost-calculator/"),
            ("HVAC Upgrades", "Heat pump replacements.", "/hvac-cost-calculator/"),
            ("LVP Flooring", "Whole-home carpet replacement.", "/flooring-cost-calculator/"),
        ],
        suburbs=[("Apex", "apex"), ("Holly Springs", "holly-springs"), ("Morrisville", "morrisville"), ("Fuquay-Varina", "fuquay-varina"), ("Garner", "garner"), ("Wake Forest", "wake-forest")],
        nearby_cities=[("Raleigh", "raleigh"), ("Durham", "durham"), ("Charlotte", "charlotte"), ("Apex", "apex")],
        nearby_suburbs=[("Apex", "apex"), ("Holly Springs", "holly-springs"), ("Morrisville", "morrisville"), ("Fuquay-Varina", "fuquay-varina")],
        examples=[
            ("Apex, NC", "Kitchen refresh · cabinets &amp; counters", "$18,500", "/cost/kitchen-remodel/"),
            ("Holly Springs, NC", "Wood privacy fence · 160 linear ft", "$6,800", "/fence-cost-calculator/"),
            ("Morrisville, NC", "LVP flooring · 1,400 sq ft", "$6,900", "/flooring-materials/luxury-vinyl-plank-flooring-cost/"),
        ],
        footer_suburbs=[("Apex", "apex"), ("Holly Springs", "holly-springs"), ("Morrisville", "morrisville")],
    ),
    _city(
        slug="wilmington",
        state_slug="north-carolina",
        state_name="North Carolina",
        state_abbr="NC",
        city_name="Wilmington",
        city_key="wilmington",
        lead_zip="28401",
        market_insight=(
            "Wilmington homeowners plan for coastal humidity, hurricane-rated roofing, moisture-resistant "
            "materials, and outdoor living upgrades near the Cape Fear coast."
        ),
        market_bullets=[
            "Coastal wind and storm exposure shape roofing",
            "Humidity-ready HVAC and dehumidification",
            "Salt air affects exterior fasteners &amp; HVAC coils",
            "Vacation and retiree housing remodel demand",
            "Deck, fence &amp; outdoor living near the coast",
        ],
        climate_bullets=[
            "Hurricane season wind and rain exposure",
            "High humidity — mold-resistant materials matter",
            "Salt spray corrosion near the coast",
            "Moderate winters with year-round cooling demand",
        ],
        metro_callout=(
            "<strong>Wilmington &amp; Cape Fear</strong> includes beach communities and "
            "fast-growing mainland suburbs — coastal building codes affect exterior project costs."
        ),
        trending=[
            ("Hurricane-Ready Roofing", "Wind-rated shingle upgrades.", "/roof-cost-calculator/"),
            ("HVAC Replacement", "Humidity control systems.", "/hvac-cost-calculator/"),
            ("Bathroom Remodels", "Moisture-resistant finishes.", "/cost/bathroom-remodel/"),
            ("Deck &amp; Outdoor", "Coastal backyard upgrades.", "/fence-cost-calculator/"),
        ],
        suburbs=[("Wilmington Beach", "wilmington-beach"), ("Wrightsville Beach", "wrightsville-beach"), ("Carolina Beach", "carolina-beach"), ("Leland", "leland"), ("Hampstead", "hampstead"), ("Ogden", "ogden")],
        nearby_cities=[("Raleigh", "raleigh"), ("Charlotte", "charlotte"), ("Durham", "durham"), ("Myrtle Beach", "myrtle-beach")],
        nearby_suburbs=[("Wrightsville Beach", "wrightsville-beach"), ("Leland", "leland"), ("Hampstead", "hampstead"), ("Carolina Beach", "carolina-beach")],
        examples=[
            ("Leland, NC", "Roof replacement · wind-rated shingles", "$13,600", "/roof-cost-calculator/"),
            ("Wrightsville Beach, NC", "Bathroom remodel · moisture-rated tile", "$14,200", "/cost/bathroom-remodel/"),
            ("Hampstead, NC", "Heat pump HVAC · 2,000 sq ft", "$9,400", "/hvac-cost-calculator/"),
        ],
        footer_suburbs=[("Leland", "leland"), ("Wrightsville Beach", "wrightsville-beach"), ("Hampstead", "hampstead")],
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
        nearby_cities=[("Los Angeles", "los-angeles"), ("Orange County", "orange-county"), ("Sacramento", "sacramento"), ("San Francisco", "san-francisco")],
        nearby_suburbs=[("La Jolla", "la-jolla"), ("Encinitas", "encinitas"), ("Carlsbad", "carlsbad"), ("Chula Vista", "chula-vista")],
        examples=[
            ("La Jolla, CA", "Tile roof · coastal wind rating", "$19,800", "/roof-cost-calculator/"),
            ("Encinitas, CA", "Solar + Powerwall · 8 kW", "$26,500", "/solar-panel-cost-calculator/"),
            ("Carlsbad, CA", "Kitchen remodel · open concept", "$42,000", "/cost/kitchen-remodel/"),
        ],
        footer_suburbs=[("La Jolla", "la-jolla"), ("Encinitas", "encinitas"), ("Carlsbad", "carlsbad")],
    ),
    _city(
        slug="los-angeles",
        state_slug="california",
        state_name="California",
        state_abbr="CA",
        city_name="Los Angeles",
        city_key="los-angeles",
        lead_zip="90012",
        snapshots=[
            {"icon": "roof", "category": "Roofing", "title": "Roof Replacement", "range": "$9k–$22k", "href": "/roof-cost-calculator/"},
            {"icon": "bath", "category": "Bathroom Remodel", "title": "Bathroom Remodel", "range": "$12k–$38k", "href": "/cost/bathroom-remodel/"},
            {"icon": "hvac", "category": "HVAC", "title": "Central AC Installation", "range": "$6k–$16k", "href": "/hvac-cost-calculator/"},
            {"icon": "floor", "category": "Flooring", "title": "Flooring Installation", "range": "$5–$22/sq ft", "href": "/flooring-cost-calculator/"},
            {"icon": "fence", "category": "Fence", "title": "Wood Privacy Fence", "range": "$30–$75/linear ft", "href": "/fence-materials/wood-privacy-fence-cost/"},
            {"icon": "solar", "category": "Solar", "title": "Solar Panels", "range": "$14k–$40k", "href": "/solar-panel-cost-calculator/"},
        ],
        market_insight=(
            "Los Angeles homeowners navigate high labor costs, varied housing stock from bungalows to "
            "mid-century ranches, and Title 24 upgrades for HVAC, solar, and remodel projects."
        ),
        market_bullets=[
            "Among the highest labor indexes in the U.S.",
            "Title 24 energy compliance on HVAC &amp; solar",
            "Earthquake retrofit and foundation work common",
            "ADU and garage conversion demand",
            "Wildfire ember zones affect roofing inland",
        ],
        climate_bullets=[
            "Mediterranean climate with hot, dry summers",
            "Coastal vs. inland micro-climates vary costs",
            "Wildfire and ember-zone roofing requirements",
            "Water restrictions drive drought-tolerant landscaping",
        ],
        metro_callout=(
            "<strong>Greater Los Angeles</strong> spans the basin from Santa Monica to Pasadena — "
            "permit timelines and labor rates reflect one of the nation's busiest contractor markets."
        ),
        trending=[
            ("Kitchen Remodels", "Open kitchens in 1940s–1960s stock.", "/cost/kitchen-remodel/"),
            ("ADU Construction", "Rental and multigenerational housing.", "/cost/kitchen-remodel/"),
            ("Solar + Battery", "Time-of-use rate optimization.", "/solar-panel-cost-calculator/"),
            ("Roof Replacement", "Composition and tile re-roofs.", "/roof-cost-calculator/"),
        ],
        suburbs=[("Pasadena", "pasadena"), ("Burbank", "burbank"), ("Long Beach", "long-beach"), ("Santa Monica", "santa-monica"), ("Torrance", "torrance"), ("Beverly Hills", "beverly-hills")],
        nearby_cities=[("San Diego", "san-diego"), ("Orange County", "orange-county"), ("Sacramento", "sacramento"), ("San Francisco", "san-francisco")],
        nearby_suburbs=[("Pasadena", "pasadena"), ("Santa Monica", "santa-monica"), ("Long Beach", "long-beach"), ("Burbank", "burbank")],
        examples=[
            ("Pasadena, CA", "Kitchen remodel · open concept", "$48,000", "/cost/kitchen-remodel/"),
            ("Santa Monica, CA", "Roof replacement · composition shingles", "$16,400", "/roof-cost-calculator/"),
            ("Long Beach, CA", "Central AC · Title 24 high-SEER", "$11,200", "/hvac-cost-calculator/"),
        ],
        footer_suburbs=[("Pasadena", "pasadena"), ("Santa Monica", "santa-monica"), ("Long Beach", "long-beach")],
    ),
    _city(
        slug="orange-county",
        state_slug="california",
        state_name="California",
        state_abbr="CA",
        city_name="Orange County",
        city_key="orange-county",
        lead_zip="92602",
        snapshots=[
            {"icon": "roof", "category": "Roofing", "title": "Roof Replacement", "range": "$9k–$22k", "href": "/roof-cost-calculator/"},
            {"icon": "bath", "category": "Bathroom Remodel", "title": "Bathroom Remodel", "range": "$12k–$38k", "href": "/cost/bathroom-remodel/"},
            {"icon": "hvac", "category": "HVAC", "title": "Central AC Installation", "range": "$6k–$16k", "href": "/hvac-cost-calculator/"},
            {"icon": "floor", "category": "Flooring", "title": "Flooring Installation", "range": "$5–$22/sq ft", "href": "/flooring-cost-calculator/"},
            {"icon": "fence", "category": "Fence", "title": "Wood Privacy Fence", "range": "$30–$75/linear ft", "href": "/fence-materials/wood-privacy-fence-cost/"},
            {"icon": "solar", "category": "Solar", "title": "Solar Panels", "range": "$14k–$40k", "href": "/solar-panel-cost-calculator/"},
        ],
        market_insight=(
            "Orange County homeowners invest in luxury kitchen and bath remodels, pool-adjacent "
            "outdoor upgrades, and high-efficiency HVAC in master-planned suburban communities."
        ),
        market_bullets=[
            "Premium suburban remodel market",
            "HOA standards on roofing &amp; fencing",
            "Strong solar economics with coastal sun",
            "Pool, patio &amp; outdoor living demand",
            "High-end finishes in Irvine &amp; Newport Beach",
        ],
        climate_bullets=[
            "Coastal influence with mild winters",
            "Hot inland summers in OC foothills",
            "Salt air near Newport &amp; Huntington Beach",
            "Fire-resistant landscaping in canyon areas",
        ],
        metro_callout=(
            "<strong>Orange County</strong> runs from Irvine master-plans to coastal Newport Beach — "
            "suburban HOA rules and premium finishes shape project budgets."
        ),
        trending=[
            ("Kitchen Remodels", "Luxury upgrades in planned communities.", "/cost/kitchen-remodel/"),
            ("Bathroom Remodels", "Spa-style owner suites.", "/cost/bathroom-remodel/"),
            ("Solar Panels", "Strong ROI with coastal sun.", "/solar-panel-cost-calculator/"),
            ("Backyard Fencing", "Privacy in HOA neighborhoods.", "/fence-cost-calculator/"),
        ],
        suburbs=[("Irvine", "irvine"), ("Anaheim", "anaheim"), ("Santa Ana", "santa-ana"), ("Newport Beach", "newport-beach"), ("Huntington Beach", "huntington-beach"), ("Costa Mesa", "costa-mesa")],
        nearby_cities=[("Los Angeles", "los-angeles"), ("San Diego", "san-diego"), ("San Francisco", "san-francisco"), ("Sacramento", "sacramento")],
        nearby_suburbs=[("Irvine", "irvine"), ("Newport Beach", "newport-beach"), ("Huntington Beach", "huntington-beach"), ("Anaheim", "anaheim")],
        examples=[
            ("Irvine, CA", "Kitchen remodel · quartz counters", "$52,000", "/cost/kitchen-remodel/"),
            ("Newport Beach, CA", "Roof replacement · tile system", "$22,600", "/roof-cost-calculator/"),
            ("Huntington Beach, CA", "Solar + battery · 7 kW", "$24,800", "/solar-panel-cost-calculator/"),
        ],
        footer_suburbs=[("Irvine", "irvine"), ("Newport Beach", "newport-beach"), ("Huntington Beach", "huntington-beach")],
    ),
    _city(
        slug="sacramento",
        state_slug="california",
        state_name="California",
        state_abbr="CA",
        city_name="Sacramento",
        city_key="sacramento",
        lead_zip="95814",
        snapshots=[
            {"icon": "roof", "category": "Roofing", "title": "Roof Replacement", "range": "$9k–$22k", "href": "/roof-cost-calculator/"},
            {"icon": "bath", "category": "Bathroom Remodel", "title": "Bathroom Remodel", "range": "$12k–$38k", "href": "/cost/bathroom-remodel/"},
            {"icon": "hvac", "category": "HVAC", "title": "Central AC Installation", "range": "$6k–$16k", "href": "/hvac-cost-calculator/"},
            {"icon": "floor", "category": "Flooring", "title": "Flooring Installation", "range": "$5–$22/sq ft", "href": "/flooring-cost-calculator/"},
            {"icon": "fence", "category": "Fence", "title": "Wood Privacy Fence", "range": "$30–$75/linear ft", "href": "/fence-materials/wood-privacy-fence-cost/"},
            {"icon": "solar", "category": "Solar", "title": "Solar Panels", "range": "$14k–$40k", "href": "/solar-panel-cost-calculator/"},
        ],
        market_insight=(
            "Sacramento homeowners upgrade ranch-style homes with efficient HVAC for inland heat, "
            "wildfire-ready roofing, and practical kitchen and bath remodels at lower coastal premiums."
        ),
        market_bullets=[
            "Central Valley heat drives HVAC demand",
            "Wildfire smoke zones affect roofing &amp; vents",
            "Ranch remodels in established neighborhoods",
            "More affordable labor vs. coastal metros",
            "Solar strong with long sunny seasons",
        ],
        climate_bullets=[
            "Hot, dry summers with triple-digit days",
            "Mild winters with occasional fog",
            "Wildfire smoke and ember-zone concerns",
            "Delta breeze moderates evening temps",
        ],
        metro_callout=(
            "<strong>Sacramento &amp; the Central Valley</strong> includes Elk Grove, Roseville &amp; "
            "Folsom — inland heat and smoke seasons shape HVAC and roofing priorities."
        ),
        trending=[
            ("HVAC Replacement", "High-SEER systems for inland heat.", "/hvac-cost-calculator/central-ac/"),
            ("Roof Replacement", "Composition and tile re-roofs.", "/roof-cost-calculator/"),
            ("Kitchen Remodels", "Ranch-style open kitchens.", "/cost/kitchen-remodel/"),
            ("Solar Panels", "Strong sun and TOU rates.", "/solar-panel-cost-calculator/"),
        ],
        suburbs=[("Elk Grove", "elk-grove"), ("Roseville", "roseville"), ("Folsom", "folsom"), ("Davis", "davis"), ("Citrus Heights", "citrus-heights"), ("Rocklin", "rocklin")],
        nearby_cities=[("San Francisco", "san-francisco"), ("Los Angeles", "los-angeles"), ("San Diego", "san-diego"), ("Orange County", "orange-county")],
        nearby_suburbs=[("Roseville", "roseville"), ("Folsom", "folsom"), ("Elk Grove", "elk-grove"), ("Davis", "davis")],
        examples=[
            ("Roseville, CA", "Heat pump HVAC · 2,400 sq ft", "$10,800", "/hvac-cost-calculator/"),
            ("Folsom, CA", "Kitchen remodel · open concept", "$38,500", "/cost/kitchen-remodel/"),
            ("Elk Grove, CA", "Roof replacement · composition shingles", "$13,200", "/roof-cost-calculator/"),
        ],
        footer_suburbs=[("Roseville", "roseville"), ("Folsom", "folsom"), ("Elk Grove", "elk-grove")],
    ),
    _city(
        slug="san-francisco",
        state_slug="california",
        state_name="California",
        state_abbr="CA",
        city_name="San Francisco",
        city_key="san-francisco",
        lead_zip="94102",
        snapshots=[
            {"icon": "roof", "category": "Roofing", "title": "Roof Replacement", "range": "$9k–$22k", "href": "/roof-cost-calculator/"},
            {"icon": "bath", "category": "Bathroom Remodel", "title": "Bathroom Remodel", "range": "$12k–$38k", "href": "/cost/bathroom-remodel/"},
            {"icon": "hvac", "category": "HVAC", "title": "Central AC Installation", "range": "$6k–$16k", "href": "/hvac-cost-calculator/"},
            {"icon": "floor", "category": "Flooring", "title": "Flooring Installation", "range": "$5–$22/sq ft", "href": "/flooring-cost-calculator/"},
            {"icon": "fence", "category": "Fence", "title": "Wood Privacy Fence", "range": "$30–$75/linear ft", "href": "/fence-materials/wood-privacy-fence-cost/"},
            {"icon": "solar", "category": "Solar", "title": "Solar Panels", "range": "$14k–$40k", "href": "/solar-panel-cost-calculator/"},
        ],
        market_insight=(
            "San Francisco Bay Area homeowners face the state's highest labor rates, dense housing "
            "constraints, seismic retrofit needs, and premium remodel budgets across the peninsula."
        ),
        market_bullets=[
            "Highest contractor labor rates in California",
            "Seismic retrofit and foundation work",
            "Victorian &amp; Edwardian remodel constraints",
            "Mini-split HVAC in older homes without ducts",
            "Strict permit timelines in SF &amp; peninsula cities",
        ],
        climate_bullets=[
            "Marine layer and mild year-round temps",
            "Limited central AC in older SF housing",
            "Fog and moisture affect exterior materials",
            "Wildfire smoke drives air filtration upgrades",
        ],
        metro_callout=(
            "<strong>San Francisco &amp; the Bay Area</strong> spans the city, East Bay &amp; "
            "Peninsula — dense housing and premium labor shape every project budget."
        ),
        trending=[
            ("Bathroom Remodels", "Compact layouts in older homes.", "/cost/bathroom-remodel/"),
            ("Mini-Split HVAC", "Ductless cooling in Victorians.", "/hvac-cost-calculator/mini-split/"),
            ("Kitchen Remodels", "Galley-to-open conversions.", "/cost/kitchen-remodel/"),
            ("Roof Replacement", "Flat and pitched re-roofs.", "/roof-cost-calculator/"),
        ],
        suburbs=[("Oakland", "oakland"), ("Berkeley", "berkeley"), ("San Jose", "san-jose"), ("Daly City", "daly-city"), ("San Mateo", "san-mateo"), ("Palo Alto", "palo-alto")],
        nearby_cities=[("Sacramento", "sacramento"), ("Los Angeles", "los-angeles"), ("San Diego", "san-diego"), ("Orange County", "orange-county")],
        nearby_suburbs=[("Oakland", "oakland"), ("Berkeley", "berkeley"), ("San Jose", "san-jose"), ("Palo Alto", "palo-alto")],
        examples=[
            ("Oakland, CA", "Kitchen remodel · galley expansion", "$55,000", "/cost/kitchen-remodel/"),
            ("Berkeley, CA", "Mini-split HVAC · Victorian home", "$14,600", "/hvac-cost-calculator/mini-split/"),
            ("Palo Alto, CA", "Bathroom remodel · tile &amp; glass", "$32,400", "/cost/bathroom-remodel/"),
        ],
        footer_suburbs=[("Oakland", "oakland"), ("Berkeley", "berkeley"), ("San Jose", "san-jose")],
    ),
]

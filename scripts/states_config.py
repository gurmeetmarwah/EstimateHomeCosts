"""State hub configs for Popular States — used by generate-state-hub-page.py"""

from __future__ import annotations

from brand import SITE_ORIGIN

SNAPSHOTS_DEFAULT = [
    {"icon": "roof", "category": "Roofing", "title": "Roof Replacement", "range": "$7k–$20k", "href": "/cost/roof-replacement/"},
    {"icon": "hvac", "category": "HVAC", "title": "Central AC Installation", "range": "$5k–$15k", "href": "/hvac-cost-calculator/central-ac/"},
    {"icon": "bath", "category": "Bathroom Remodel", "title": "Bathroom Remodel", "range": "$10k–$35k", "href": "/cost/bathroom-remodel/"},
    {"icon": "floor", "category": "Flooring", "title": "Flooring Installation", "range": "$4–$20/sq ft", "href": "/flooring-cost-calculator/"},
    {"icon": "solar", "category": "Solar", "title": "Solar Panels", "range": "$14k–$36k", "href": "/solar-panel-cost-calculator/"},
    {"icon": "fence", "category": "Fence", "title": "Wood Privacy Fence", "range": "$25–$65/linear ft", "href": "/fence-materials/wood-privacy-fence-cost/"},
]

SNAPSHOTS_CA = [
    {"icon": "roof", "category": "Roofing", "title": "Roof Replacement", "range": "$9k–$22k", "href": "/cost/roof-replacement/"},
    {"icon": "hvac", "category": "HVAC", "title": "Central AC Installation", "range": "$6k–$16k", "href": "/hvac-cost-calculator/central-ac/"},
    {"icon": "bath", "category": "Bathroom Remodel", "title": "Bathroom Remodel", "range": "$12k–$38k", "href": "/cost/bathroom-remodel/"},
    {"icon": "floor", "category": "Flooring", "title": "Flooring Installation", "range": "$5–$22/sq ft", "href": "/flooring-cost-calculator/"},
    {"icon": "solar", "category": "Solar", "title": "Solar Panels", "range": "$14k–$40k", "href": "/solar-panel-cost-calculator/"},
    {"icon": "fence", "category": "Fence", "title": "Wood Privacy Fence", "range": "$30–$75/linear ft", "href": "/fence-materials/wood-privacy-fence-cost/"},
]

CATEGORIES_DEFAULT = [
    {
        "name": "Roofing",
        "price": "From $7k",
        "links": [
            ("Roof replacement", "/roof-cost-calculator/"),
            ("Roofing materials", "/roofing-materials/asphalt-shingle-roof-cost/"),
            ("Roof repair", "/cost/roof-replacement/#repair-vs-replace"),
        ],
    },
    {
        "name": "Remodeling",
        "price": "From $10k",
        "links": [
            ("Kitchen remodel", "/cost/kitchen-remodel/"),
            ("Bathroom remodel", "/cost/bathroom-remodel/"),
            ("Additions", "/cost/kitchen-remodel/"),
        ],
    },
    {
        "name": "HVAC",
        "price": "From $5k",
        "links": [
            ("Central AC", "/hvac-cost-calculator/central-ac/"),
            ("Heat pumps", "/hvac-cost-calculator/heat-pump/"),
            ("Ductwork", "/hvac-cost-calculator/"),
        ],
    },
    {
        "name": "Flooring",
        "price": "From $4/sq ft",
        "links": [
            ("Hardwood", "/flooring-materials/solid-hardwood-flooring-cost/"),
            ("LVP", "/flooring-materials/luxury-vinyl-plank-flooring-cost/"),
            ("Tile", "/flooring-materials/porcelain-tile-flooring-cost/"),
        ],
    },
    {
        "name": "Outdoor",
        "price": "From $3k",
        "links": [
            ("Fencing", "/fence-cost-calculator/"),
            ("Decks", "/fence-cost-calculator/"),
            ("Patios", "/cost/kitchen-remodel/"),
        ],
    },
    {
        "name": "Energy",
        "price": "From $14k",
        "links": [
            ("Solar panels", "/solar-panel-cost-calculator/"),
            ("Insulation", "/hvac-cost-calculator/"),
            ("Windows", "/cost/kitchen-remodel/"),
        ],
    },
]

BUDGETS_DEFAULT = [
    ("Under $5k", ["Flooring refresh", "Interior paint", "Small fencing"], "/flooring-cost-calculator/"),
    ("$5k–$15k", ["HVAC replacement", "Roofing", "Bathrooms"], "/hvac-cost-calculator/"),
    ("$15k+", ["Kitchens", "Solar", "Additions"], "/cost/kitchen-remodel/"),
]

POPULAR_STATE_SLUGS = ("texas", "florida", "arizona", "north-carolina", "california")


def related_states(exclude_slug: str) -> list[tuple[str, str]]:
    names = {
        "texas": "Texas",
        "florida": "Florida",
        "arizona": "Arizona",
        "north-carolina": "North Carolina",
        "california": "California",
    }
    return [
        (names[s], f"/{s}/")
        for s in POPULAR_STATE_SLUGS
        if s != exclude_slug
    ]


def city_hubs(state_slug: str) -> list[tuple[str, str]]:
    hubs = {
        "texas": [
            ("Dallas", "/texas/dallas/"),
            ("Austin", "/texas/austin/"),
            ("Houston", "/texas/houston/"),
            ("San Antonio", "/texas/san-antonio/"),
            ("Fort Worth", "/texas/fort-worth/"),
        ],
        "arizona": [
            ("Phoenix", "/arizona/phoenix/"),
            ("Scottsdale", "/arizona/scottsdale/"),
            ("Mesa", "/arizona/mesa/"),
            ("Tucson", "/arizona/tucson/"),
            ("Chandler", "/arizona/chandler/"),
        ],
        "florida": [
            ("Tampa", "/florida/tampa/"),
            ("Orlando", "/florida/orlando/"),
            ("Miami", "/florida/miami/"),
            ("Jacksonville", "/florida/jacksonville/"),
            ("St. Petersburg", "/florida/st-petersburg/"),
        ],
        "north-carolina": [
            ("Raleigh", "/north-carolina/raleigh/"),
            ("Charlotte", "/north-carolina/charlotte/"),
            ("Durham", "/north-carolina/durham/"),
            ("Cary", "/north-carolina/cary/"),
            ("Wilmington", "/north-carolina/wilmington/"),
        ],
        "california": [
            ("San Diego", "/california/san-diego/"),
            ("Los Angeles", "/california/los-angeles/"),
            ("Orange County", "/california/orange-county/"),
            ("Sacramento", "/california/sacramento/"),
            ("San Francisco", "/california/san-francisco/"),
        ],
    }
    return hubs.get(state_slug, [])


TEXAS = {
    "state_name": "Texas",
    "state_abbr": "TX",
    "slug": "texas",
    "canonical": f"{SITE_ORIGIN}/texas/",
    "lead_zip": "75201",
    "snapshots": SNAPSHOTS_DEFAULT,
    "categories": CATEGORIES_DEFAULT,
    "major_cities": [
        ("Dallas", "dallas", "Roofing costs &amp; suburban remodel demand"),
        ("Austin", "austin", "Modern remodel trends &amp; solar growth"),
        ("Houston", "houston", "Humidity-related projects &amp; roofing demand"),
        ("San Antonio", "san-antonio", "Stucco &amp; roofing projects"),
        ("Fort Worth", "fort-worth", "Suburban fencing &amp; HVAC upgrades"),
    ],
    "homeowner_trends": [
        ("Storm-Resistant Roofing", "Impact-rated shingles and metal roofs are common after hail and wind exposure across North Texas."),
        ("High HVAC Demand", "Long hot summers drive central AC replacements, duct sealing, and higher-efficiency systems statewide."),
        ("Solar Adoption Growth", "Rising electricity costs make rooftop solar attractive in Austin, Dallas, and fast-growing suburbs."),
        ("Outdoor Living Projects", "Backyard fencing, patios, and pergolas are popular in suburban neighborhoods statewide."),
        ("Energy-Efficient Upgrades", "Insulation, windows, and radiant barriers help offset extreme summer heat and cooling bills."),
    ],
    "climate_cards": [
        ("Extreme Summer Heat", "100°F+ summers increase cooling costs and HVAC replacement demand."),
        ("Hailstorms", "North Texas hail drives roof replacement and impact-resistant material upgrades."),
        ("Humidity", "Gulf Coast and Houston metros prioritize HVAC sizing, dehumidification, and insulation."),
        ("Sun Exposure", "Strong solar production improves ROI for panels across much of the state."),
    ],
    "trending": [
        ("Roof Replacement", "Storm-driven demand across Texas metros.", "/cost/roof-replacement/"),
        ("Central AC Installation", "Essential in Texas heat.", "/hvac-cost-calculator/central-ac/"),
        ("Solar Panels", "Rapidly growing adoption statewide.", "/solar-panel-cost-calculator/"),
        ("Backyard Fencing", "Popular in suburban neighborhoods.", "/fence-cost-calculator/"),
        ("Kitchen Remodels", "Strong resale value in growing markets.", "/cost/kitchen-remodel/"),
    ],
    "regions": [
        ("North Texas", "Higher hail exposure; impact roofing and storm repairs are common in Dallas–Fort Worth.", "/texas/dallas/"),
        ("Central Texas", "Modern remodel growth in Austin and surrounding suburbs; strong solar interest.", "/texas/austin/"),
        ("South Texas", "Stucco exteriors, tile roofing, and affordable remodel demand in San Antonio.", "/texas/san-antonio/"),
        ("Gulf Coast", "Humidity and storm concerns shape roofing, insulation, and HVAC priorities.", "/texas/houston/"),
    ],
    "budgets": BUDGETS_DEFAULT,
    "examples": [
        ("Dallas, TX", "Architectural roof replacement", "$14,200", "/texas/dallas/roof-cost-calculator/"),
        ("Austin, TX", "8 kW solar system", "$24,800", "/texas/austin/solar-panel-cost-calculator/"),
        ("Houston, TX", "Central AC replacement · 2,400 sq ft", "$9,400", "/texas/houston/hvac-cost-calculator/"),
    ],
    "home_styles": [
        ("Ranch Homes", "Single-story HVAC, roofing, and LVP flooring updates.", "$8k–$45k typical"),
        ("Brick Traditional Homes", "Roof replacement, window upgrades, and bath refreshes.", "$12k–$55k typical"),
        ("Modern Farmhouse", "Open kitchens, master baths, fencing, and solar.", "$20k–$90k typical"),
        ("New Construction Suburbs", "Landscaping, fencing, LVP, and whole-home HVAC tuning.", "$10k–$60k typical"),
    ],
    "faqs": [
        (
            "How much do home renovations cost in Texas?",
            "Most Texas renovations range from <strong>$5,000–$100,000+</strong> depending on scope and metro. Bathrooms often run <strong>$10,000–$35,000</strong>, kitchens <strong>$18,000–$60,000+</strong>, and roofing <strong>$7,000–$20,000</strong> for typical homes.",
        ),
        (
            "What roofing material works best in Texas heat?",
            "<strong>Architectural asphalt shingles</strong> are most common. <strong>Impact-resistant (Class 4)</strong> shingles help in hail-prone areas. <strong>Metal roofing</strong> performs well in heat and is growing in suburban builds.",
        ),
        (
            "Are solar panels worth it in Texas?",
            "Yes for many homeowners with bills above <strong>$150/month</strong> and good sun exposure. Texas has strong solar production and the <strong>30% federal tax credit</strong>. See our <a href=\"__SOLAR_CALC__\">solar calculator</a>.",
        ),
        (
            "Do Texas homes need impact-resistant roofs?",
            "In hail-prone regions (especially North Texas), <strong>Class 4 impact-rated shingles</strong> or metal roofing can reduce storm damage and may qualify for insurance discounts.",
        ),
        (
            "What projects add the most home value in Texas?",
            "<strong>Kitchen remodels</strong>, <strong>roof replacement</strong> after storms, and <strong>energy-efficient HVAC</strong> commonly deliver strong resale appeal in Texas metros.",
        ),
    ],
    "related_states": related_states("texas"),
    "city_hubs": city_hubs("texas"),
}

FLORIDA = {
    "state_name": "Florida",
    "state_abbr": "FL",
    "slug": "florida",
    "canonical": f"{SITE_ORIGIN}/florida/",
    "lead_zip": "33602",
    "snapshots": SNAPSHOTS_DEFAULT,
    "categories": CATEGORIES_DEFAULT,
    "major_cities": [
        ("Tampa", "tampa", "Hurricane-ready roofing &amp; humidity-focused HVAC"),
        ("Orlando", "orlando", "Theme-park metro remodel &amp; cooling upgrades"),
        ("Miami", "miami", "Coastal condos &amp; wind-rated exterior projects"),
        ("Jacksonville", "jacksonville", "Affordable suburban roofing &amp; fencing"),
        ("St. Petersburg", "st-petersburg", "Coastal roofing &amp; bath remodel demand"),
    ],
    "homeowner_trends": [
        ("Hurricane-Ready Roofing", "Wind-rated shingles, tile, and metal systems are standard in coastal building codes."),
        ("Humidity &amp; HVAC", "High-SEER central AC and dehumidification are priorities in Gulf Coast metros."),
        ("Pool &amp; Outdoor Living", "Screened lanais, fencing, and patios are popular year-round."),
        ("Moisture-Resistant Materials", "Mold-resistant drywall, tile, and sealed exteriors matter in humid climates."),
        ("Insurance-Driven Upgrades", "Roof age and wind mitigation inspections influence material choices."),
    ],
    "climate_cards": [
        ("Hurricane Season", "Wind-driven rain and storm surge shape roofing and window priorities."),
        ("High Humidity", "HVAC sizing, duct sealing, and moisture control affect comfort and cost."),
        ("Salt Air", "Coastal corrosion influences fasteners, HVAC coils, and exterior finishes."),
        ("Year-Round Cooling", "Minimal heating demand; cooling efficiency drives utility bills."),
    ],
    "trending": [
        ("Hurricane-Ready Roofing", "Post-storm replacement cycles across the Gulf Coast.", "/cost/roof-replacement/"),
        ("HVAC Replacement", "Humidity and efficiency upgrades.", "/hvac-cost-calculator/central-ac/"),
        ("Bathroom Remodels", "Popular in aging coastal housing stock.", "/cost/bathroom-remodel/"),
        ("Pool Fencing &amp; Outdoor", "Privacy fences and screened enclosures.", "/fence-cost-calculator/"),
        ("Impact Windows", "Often bundled with roof and exterior projects.", "/cost/kitchen-remodel/"),
    ],
    "regions": [
        ("Tampa Bay", "Wind-rated roofing and flood-zone awareness in coastal suburbs.", "/florida/tampa/"),
        ("Central Florida", "Orlando-area growth drives remodel and AC demand.", "/florida/orlando/"),
        ("South Florida", "Premium labor and condo-friendly renovation projects.", "/florida/miami/"),
        ("North Florida", "Jacksonville metros with affordable suburban housing stock.", "/florida/jacksonville/"),
    ],
    "budgets": BUDGETS_DEFAULT,
    "examples": [
        ("St. Petersburg, FL", "Wind-rated shingle roof", "$14,100", "/florida/tampa/roof-cost-calculator/"),
        ("Brandon, FL", "Bathroom remodel · walk-in shower", "$11,800", "/florida/tampa/cost/bathroom-remodel/"),
        ("Clearwater, FL", "Heat pump HVAC · 2,000 sq ft", "$9,200", "/florida/tampa/hvac-cost-calculator/"),
    ],
    "home_styles": [
        ("Concrete Block Homes", "Stucco exteriors, tile roofs, and impact-rated openings.", "$10k–$50k typical"),
        ("Coastal Condos", "Compact bath and HVAC upgrades with HOA requirements.", "$8k–$40k typical"),
        ("Suburban Ranch", "Roof replacement, central AC, and screened patios.", "$12k–$55k typical"),
        ("Pool Homes", "Fencing, decking, and outdoor kitchen adjacency.", "$15k–$70k typical"),
    ],
    "faqs": [
        (
            "How much do home renovations cost in Florida?",
            "Most Florida renovations range from <strong>$6,000–$90,000+</strong> depending on scope and coast. Bathrooms often run <strong>$12,000–$35,000</strong>, kitchens <strong>$20,000–$65,000+</strong>, and roofing <strong>$8,000–$22,000</strong> with wind-rated materials.",
        ),
        (
            "What roofing material works best in Florida?",
            "<strong>Architectural shingles</strong> with high wind ratings are common. <strong>Tile and metal</strong> perform well in coastal areas. Building codes often require enhanced fastening and underlayment.",
        ),
        (
            "Are solar panels worth it in Florida?",
            "Yes in many markets with strong sun and rising rates. The <strong>30% federal tax credit</strong> applies. See our <a href=\"__SOLAR_CALC__\">solar calculator</a> for production estimates.",
        ),
        (
            "Do Florida homes need hurricane-rated roofs?",
            "In wind-borne debris regions, <strong>impact-resistant materials</strong> and proper installation matter for insurance and storm resilience.",
        ),
        (
            "What projects add the most home value in Florida?",
            "<strong>Wind-rated roofing</strong>, <strong>efficient HVAC</strong>, and <strong>updated kitchens and baths</strong> commonly appeal to buyers in Florida metros.",
        ),
    ],
    "related_states": related_states("florida"),
    "city_hubs": city_hubs("florida"),
}

ARIZONA = {
    "state_name": "Arizona",
    "state_abbr": "AZ",
    "slug": "arizona",
    "canonical": f"{SITE_ORIGIN}/arizona/",
    "lead_zip": "85001",
    "snapshots": SNAPSHOTS_DEFAULT,
    "categories": CATEGORIES_DEFAULT,
    "major_cities": [
        ("Phoenix", "phoenix", "Desert heat roofing, HVAC &amp; solar demand"),
        ("Scottsdale", "scottsdale", "Premium remodels &amp; high-end outdoor living"),
        ("Mesa", "mesa", "Suburban growth &amp; affordable upgrades"),
        ("Tucson", "tucson", "Older housing stock &amp; cooling-focused projects"),
        ("Chandler", "chandler", "Family neighborhoods &amp; HOA-driven exteriors"),
    ],
    "homeowner_trends": [
        ("Heat-Ready Roofing", "Tile, metal, and cool-roof systems handle extreme desert sun."),
        ("Solar Adoption", "Excellent production per square foot drives battery-ready installs."),
        ("High-Efficiency HVAC", "Long cooling seasons make SEER ratings and duct sealing critical."),
        ("Desert Landscaping", "Hardscape, fencing, and low-water outdoor upgrades are common."),
        ("Suburban Growth", "1990s–2000s builds fuel kitchen, bath, and flooring refreshes."),
    ],
    "climate_cards": [
        ("Extreme Desert Heat", "120°F+ days increase cooling load and material UV exposure."),
        ("Monsoon Season", "Sudden wind and dust storms affect roofing and drainage."),
        ("Low Humidity", "Different HVAC sizing than humid climates; evaporative cooling in some areas."),
        ("Intense Sun", "Solar ROI is strong; radiant barriers reduce attic heat."),
    ],
    "trending": [
        ("Tile &amp; Metal Roofs", "Popular for heat resistance and longevity.", "/cost/roof-replacement/"),
        ("Solar Panels", "Top-tier sun exposure statewide.", "/solar-panel-cost-calculator/"),
        ("HVAC Upgrades", "Essential for summer comfort.", "/hvac-cost-calculator/central-ac/"),
        ("Kitchen Remodels", "Strong demand in aging suburban stock.", "/cost/kitchen-remodel/"),
        ("Backyard Fencing", "Privacy and pool-area enclosures.", "/fence-cost-calculator/"),
    ],
    "regions": [
        ("Greater Phoenix", "Maricopa County growth drives remodel and solar demand.", "/arizona/phoenix/"),
        ("East Valley", "Mesa, Chandler &amp; Gilbert suburban upgrades.", "/arizona/mesa/"),
        ("North Scottsdale", "Premium labor and luxury exterior projects.", "/arizona/scottsdale/"),
        ("Southern Arizona", "Tucson market with moderate costs vs. Phoenix.", "/arizona/tucson/"),
    ],
    "budgets": BUDGETS_DEFAULT,
    "examples": [
        ("Scottsdale, AZ", "Tile roof replacement · concrete tile", "$16,200", "/arizona/scottsdale/roof-cost-calculator/"),
        ("Mesa, AZ", "Solar + battery · 7.5 kW system", "$21,400", "/arizona/mesa/solar-panel-cost-calculator/"),
        ("Chandler, AZ", "Central AC · high-SEER replacement", "$8,600", "/arizona/chandler/hvac-cost-calculator/"),
    ],
    "home_styles": [
        ("Desert Contemporary", "Stucco, tile roofs, and energy-efficient glazing.", "$12k–$60k typical"),
        ("Ranch &amp; Split-Level", "Single-story HVAC and roof upgrades.", "$10k–$45k typical"),
        ("Master-Planned Suburbs", "HOA-driven exterior and landscaping standards.", "$15k–$75k typical"),
        ("Custom Luxury", "High-end kitchens, metal roofs, and whole-home solar.", "$35k–$120k+"),
    ],
    "faqs": [
        (
            "How much do home renovations cost in Arizona?",
            "Most Arizona renovations range from <strong>$6,000–$95,000+</strong> depending on metro. Bathrooms often run <strong>$10,000–$32,000</strong>, kitchens <strong>$18,000–$58,000+</strong>, and roofing <strong>$8,000–$20,000</strong> with tile or metal common.",
        ),
        (
            "What roofing material works best in Arizona heat?",
            "<strong>Concrete tile</strong> and <strong>metal</strong> are popular for heat and longevity. <strong>Cool-roof</strong> coatings and radiant barriers help attic temperatures.",
        ),
        (
            "Are solar panels worth it in Arizona?",
            "Often yes — Arizona has among the best solar production in the U.S. See our <a href=\"__SOLAR_CALC__\">solar calculator</a> and the <strong>30% federal tax credit</strong>.",
        ),
        (
            "How does desert climate affect HVAC costs?",
            "Long cooling seasons and high outdoor temperatures favor <strong>right-sized, high-SEER systems</strong> and sealed ductwork.",
        ),
        (
            "What projects add the most home value in Arizona?",
            "<strong>Solar</strong>, <strong>efficient HVAC</strong>, and <strong>updated kitchens</strong> commonly resonate with buyers in Phoenix-area markets.",
        ),
    ],
    "related_states": related_states("arizona"),
    "city_hubs": city_hubs("arizona"),
}

NORTH_CAROLINA = {
    "state_name": "North Carolina",
    "state_abbr": "NC",
    "slug": "north-carolina",
    "canonical": f"{SITE_ORIGIN}/north-carolina/",
    "lead_zip": "27601",
    "snapshots": SNAPSHOTS_DEFAULT,
    "categories": CATEGORIES_DEFAULT,
    "major_cities": [
        ("Raleigh", "raleigh", "Research Triangle remodel &amp; roofing demand"),
        ("Charlotte", "charlotte", "Banking metro suburban growth"),
        ("Durham", "durham", "Older homes &amp; university-area upgrades"),
        ("Cary", "cary", "Family subdivisions &amp; fencing projects"),
        ("Wilmington", "wilmington", "Coastal humidity &amp; storm exposure"),
    ],
    "homeowner_trends": [
        ("Research Triangle Growth", "Job growth fuels kitchen, bath, and addition projects."),
        ("Moderate-Climate HVAC", "Heat pumps and dual-fuel systems gain market share."),
        ("Architectural Shingles", "Asphalt remains dominant with periodic storm replacement."),
        ("Suburban Fencing", "Privacy fences popular in Cary, Apex, and Wake Forest."),
        ("Move-Up Remodels", "Open kitchens and owner suites in 1990s–2000s stock."),
    ],
    "climate_cards": [
        ("Humid Summers", "Cooling load and moisture control shape HVAC priorities."),
        ("Mild Winters", "Lower heating demand than northern states."),
        ("Occasional Ice Storms", "Roofing and tree damage drive repair cycles."),
        ("Pine Pollen &amp; Moisture", "Exterior maintenance for decks and fences."),
    ],
    "trending": [
        ("Roof Replacement", "Aging 20-year shingle cycles.", "/cost/roof-replacement/"),
        ("Kitchen &amp; Bath Remodels", "Suburban move-up buyers.", "/cost/kitchen-remodel/"),
        ("Heat Pump HVAC", "Efficient heating and cooling in one system.", "/hvac-cost-calculator/heat-pump/"),
        ("LVP Flooring", "Popular over carpet in renovations.", "/flooring-cost-calculator/"),
        ("Deck &amp; Outdoor", "Covered porches and backyard upgrades.", "/fence-cost-calculator/"),
    ],
    "regions": [
        ("Research Triangle", "Raleigh, Durham &amp; Chapel Hill remodel demand.", "/north-carolina/raleigh/"),
        ("Charlotte Metro", "Fast-growing suburbs and new construction.", "/north-carolina/charlotte/"),
        ("Piedmont", "Cary &amp; Wake County family subdivision upgrades.", "/north-carolina/cary/"),
        ("Coast", "Wilmington humidity and storm-ready roofing.", "/north-carolina/wilmington/"),
    ],
    "budgets": BUDGETS_DEFAULT,
    "examples": [
        ("Cary, NC", "Kitchen refresh · cabinets &amp; counters", "$18,500", "/north-carolina/cary/cost/kitchen-remodel/"),
        ("Charlotte, NC", "Roof replacement · architectural shingles", "$12,200", "/north-carolina/charlotte/roof-cost-calculator/"),
        ("Wilmington, NC", "Heat pump HVAC · 2,000 sq ft", "$9,400", "/north-carolina/wilmington/hvac-cost-calculator/"),
    ],
    "home_styles": [
        ("Ranch &amp; Split-Level", "Single-story HVAC and roofing updates.", "$8k–$42k typical"),
        ("Newer Subdivisions", "Open-concept kitchen and bath remodels.", "$15k–$65k typical"),
        ("Craftsman &amp; Traditional", "Hardwood, fencing, and curb-appeal projects.", "$12k–$55k typical"),
        ("Coastal Cottage", "Moisture-aware materials and storm-ready roofing.", "$14k–$60k typical"),
    ],
    "faqs": [
        (
            "How much do home renovations cost in North Carolina?",
            "Most NC renovations range from <strong>$5,000–$85,000+</strong> depending on scope. Bathrooms often run <strong>$10,000–$30,000</strong>, kitchens <strong>$16,000–$55,000+</strong>, and roofing <strong>$7,000–$18,000</strong> for typical homes.",
        ),
        (
            "What roofing material works best in North Carolina?",
            "<strong>Architectural asphalt shingles</strong> are most common. Ice-and-water shield is used in vulnerable roof areas.",
        ),
        (
            "Are heat pumps popular in North Carolina?",
            "Yes — moderate climates suit <strong>heat pumps</strong> for efficient heating and cooling. See our <a href=\"__HVAC_CALC__\">HVAC calculator</a>.",
        ),
        (
            "Do North Carolina homes need storm-ready roofs?",
            "Coastal and eastern areas see hurricanes and tropical storms; <strong>wind-rated installation</strong> matters.",
        ),
        (
            "What projects add the most home value in North Carolina?",
            "<strong>Kitchen remodels</strong>, <strong>roof replacement</strong>, and <strong>curb-appeal upgrades</strong> commonly support resale in Triangle and Charlotte markets.",
        ),
    ],
    "related_states": related_states("north-carolina"),
    "city_hubs": city_hubs("north-carolina"),
}

CALIFORNIA = {
    "state_name": "California",
    "state_abbr": "CA",
    "slug": "california",
    "canonical": f"{SITE_ORIGIN}/california/",
    "lead_zip": "92101",
    "snapshots": SNAPSHOTS_CA,
    "categories": CATEGORIES_DEFAULT,
    "major_cities": [
        ("San Diego", "san-diego", "Coastal premiums, solar &amp; Title 24 upgrades"),
        ("Los Angeles", "los-angeles", "High labor remodel &amp; multifamily-adjacent stock"),
        ("Orange County", "orange-county", "Suburban luxury kitchen &amp; bath demand"),
        ("Sacramento", "sacramento", "Inland heat, smoke zones &amp; ranch remodels"),
        ("San Francisco", "san-francisco", "Dense housing &amp; premium contractor rates"),
    ],
    "homeowner_trends": [
        ("Title 24 &amp; Energy Codes", "HVAC and solar projects often align with California efficiency rules."),
        ("Coastal Labor Premiums", "San Diego and LA metros run above national labor indexes."),
        ("Solar + Storage", "Time-of-use rates drive battery pairing with rooftop solar."),
        ("ADU &amp; Additions", "Accessory dwelling units add rental and family housing."),
        ("Wildfire &amp; Ember Zones", "Roofing and vent choices matter in inland corridors."),
    ],
    "climate_cards": [
        ("Coastal Marine Layer", "Mild temperatures with regional micro-climates."),
        ("Inland Heat", "Central Valley and inland areas need robust cooling."),
        ("Wildfire Risk", "Ember-resistant vents and roofing in high-risk zones."),
        ("Water-Wise Landscaping", "Hardscape and fencing replace thirsty lawns."),
    ],
    "trending": [
        ("Solar + Battery", "Time-of-use optimization.", "/solar-panel-cost-calculator/"),
        ("Kitchen Remodels", "High-end coastal renovations.", "/cost/kitchen-remodel/"),
        ("Roof Replacement", "Tile and composition re-roofs.", "/cost/roof-replacement/"),
        ("HVAC (Title 24)", "High-efficiency system replacements.", "/hvac-cost-calculator/central-ac/"),
        ("ADU Construction", "Rental and multigenerational housing.", "/cost/kitchen-remodel/"),
    ],
    "regions": [
        ("San Diego County", "Coastal labor premiums and strong solar economics.", "/california/san-diego/"),
        ("Los Angeles", "Large metro with varied housing ages and prices.", "/california/los-angeles/"),
        ("Orange County", "Suburban luxury kitchen &amp; bath demand.", "/california/orange-county/"),
        ("Bay Area", "Highest labor indexes in the state.", "/california/san-francisco/"),
        ("Central Valley", "Affordable housing stock and inland heat.", "/california/sacramento/"),
    ],
    "budgets": BUDGETS_DEFAULT,
    "examples": [
        ("La Jolla, CA", "Tile roof · coastal wind rating", "$19,800", "/california/san-diego/roof-cost-calculator/"),
        ("Pasadena, CA", "Kitchen remodel · open concept", "$48,000", "/california/los-angeles/cost/kitchen-remodel/"),
        ("Irvine, CA", "Kitchen remodel · quartz counters", "$52,000", "/california/orange-county/cost/kitchen-remodel/"),
    ],
    "home_styles": [
        ("Coastal Contemporary", "Tile, stucco, and solar-ready roofs.", "$18k–$80k typical"),
        ("Mid-Century Ranch", "Open kitchens, windows, and HVAC upgrades.", "$20k–$90k typical"),
        ("Spanish Revival", "Tile roofs and courtyard-oriented layouts.", "$22k–$95k typical"),
        ("New Build Suburbs", "Builder-grade upgrades: flooring, landscape, solar.", "$15k–$70k typical"),
    ],
    "faqs": [
        (
            "How much do home renovations cost in California?",
            "Most California renovations range from <strong>$8,000–$120,000+</strong> depending on metro. Bathrooms often run <strong>$12,000–$38,000</strong>, kitchens <strong>$22,000–$75,000+</strong>, and roofing <strong>$9,000–$22,000</strong> with coastal labor premiums.",
        ),
        (
            "What roofing material works best in California?",
            "<strong>Composition and tile</strong> are common. Coastal wind ratings and wildfire ember zones influence material and vent choices.",
        ),
        (
            "Are solar panels worth it in California?",
            "Often yes with strong sun and time-of-use rates. See our <a href=\"__SOLAR_CALC__\">solar calculator</a> and the <strong>30% federal tax credit</strong>.",
        ),
        (
            "How does Title 24 affect HVAC and solar?",
            "California energy rules favor <strong>high-efficiency equipment</strong> on many replacements — factor compliance into bids.",
        ),
        (
            "What projects add the most home value in California?",
            "<strong>Solar</strong>, <strong>kitchen remodels</strong>, and <strong>energy-efficient HVAC</strong> commonly appeal to buyers in coastal metros.",
        ),
    ],
    "related_states": related_states("california"),
    "city_hubs": city_hubs("california"),
}

ALL_STATES = [TEXAS, FLORIDA, ARIZONA, NORTH_CAROLINA, CALIFORNIA]

STATE_DEFAULT_CITY = {
    "texas": "texas",
    "florida": "tampa",
    "arizona": "phoenix",
    "north-carolina": "raleigh",
    "california": "san-diego",
}

STATE_LOCATION_KEY = {
    "texas": "tx",
    "florida": "fl",
    "arizona": "az",
    "north-carolina": "nc",
    "california": "ca",
}

STATE_AVERAGE_LABEL = {
    "texas": "Texas average",
    "florida": "Florida average",
    "arizona": "Arizona average",
    "north-carolina": "North Carolina average",
    "california": "California average",
}

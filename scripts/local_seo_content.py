"""Unique local SEO content for city and state hub pages — labor, permits, climate, projects, cost drivers."""

from __future__ import annotations

from dataclasses import dataclass

from pricing_cities import get_city


@dataclass(frozen=True)
class LocalSeoBlock:
    labor_lead: str
    labor_bullets: tuple[str, ...]
    permit_lead: str
    permit_bullets: tuple[str, ...]
    climate_lead: str
    climate_bullets: tuple[str, ...]
    project_recommendations: tuple[tuple[str, str], ...]  # (title, rationale)
    cost_drivers: tuple[str, ...]


def _labor_note(city_key: str) -> str:
    city = get_city(city_key)
    nat = get_city("national")
    pct = round((city.labor / nat.labor - 1) * 100)
    permit = city.permit
    if pct >= 12:
        tier = f"Contractor labor runs about <strong>{pct}% above</strong> the U.S. average"
    elif pct >= 4:
        tier = f"Contractor labor runs about <strong>{pct}% above</strong> the U.S. average"
    elif pct <= -8:
        tier = f"Contractor labor runs about <strong>{abs(pct)}% below</strong> the U.S. average"
    elif pct <= -3:
        tier = f"Contractor labor runs about <strong>{abs(pct)}% below</strong> the U.S. average"
    else:
        tier = "Contractor labor is <strong>near the U.S. average</strong>"
    return f"{tier}; typical permit fees in our model start around <strong>${permit:,}</strong> for standard residential work."


CITY_LOCAL_SEO: dict[str, LocalSeoBlock] = {
    "dallas": LocalSeoBlock(
        labor_lead=(
            "Dallas sits in one of the busiest contractor markets in the South. Roofers and HVAC crews "
            "book out quickly after spring hail events, and Collin/Denton suburban growth keeps trim "
            "and remodel crews active year-round."
        ),
        labor_bullets=(
            "Roofing labor spikes 2–4 weeks after major hail — get quotes early",
            "Suburban HOAs in Plano, Frisco &amp; McKinney often require approved contractor lists",
            "Licensed GCs pull separate permits in Dallas vs. Collin County jurisdictions",
            "Competitive pricing vs. coastal metros, but storm-season demand raises bids",
        ),
        permit_lead=(
            "Dallas Development Services and neighboring Collin/Denton cities each issue their own "
            "building permits. Full re-roofs, HVAC changeouts, and panel upgrades typically require "
            "city approval before work starts."
        ),
        permit_bullets=(
            "Re-roof permits common in Dallas, Plano, Frisco &amp; Irving — fees often $150–$400",
            "HVAC replacements need mechanical permits; contractors usually pull them",
            "Electrical work for solar or EV chargers requires separate electrical permits",
            "HOA architectural review is separate from city permits but can add 1–3 weeks",
        ),
        climate_lead="North Texas heat and hail shape nearly every exterior project in Dallas:",
        climate_bullets=(
            "100°F+ summers drive oversized cooling loads and shorter AC lifespans",
            "Spring hail favors Class 4 impact shingles and insurance-driven re-roofs",
            "UV exposure fades fences and decking faster than humid climates",
            "Radiant barriers and attic insulation pay back quickly on single-story ranches",
        ),
        project_recommendations=(
            ("Impact-rated roof replacement", "Highest ROI after hail — insurance often covers partial cost"),
            ("High-SEER central AC", "Long cooling season makes efficiency upgrades worthwhile"),
            ("Backyard privacy fencing", "Standard in Plano/Frisco subdivisions with open lots"),
            ("Open-concept kitchen remodel", "Strong resale appeal in 1990s–2000s suburban stock"),
        ),
        cost_drivers=(
            "Hail-season roofing demand and insurance adjuster timelines",
            "County-by-county permit fees (Dallas vs. Collin vs. Denton)",
            "HOA material standards in master-planned suburbs",
            "Two-story homes add roof pitch and HVAC duct complexity",
        ),
    ),
    "austin": LocalSeoBlock(
        labor_lead=(
            "Austin's tech-driven growth keeps remodel and energy-upgrade crews busy. Central Texas "
            "contractors compete on design-forward kitchens and heat-pump installs, though hail season "
            "still creates roofing bottlenecks."
        ),
        labor_bullets=(
            "Design-build firms charge premiums in Travis &amp; Williamson counties",
            "Heat-pump installers gaining share — fewer specialists than AC-only crews",
            "Round Rock &amp; Cedar Park suburbs have separate permit offices",
            "Competitive market vs. California, but popular crews book 3–6 weeks out",
        ),
        permit_lead=(
            "City of Austin and suburban Williamson/Hays jurisdictions require permits for structural "
            "roof work, HVAC changeouts, and most electrical upgrades. Energy code is stricter than "
            "many Texas metros."
        ),
        permit_bullets=(
            "Austin Energy may require additional review for major electrical work",
            "Roof permits needed for full tear-off — overlay rules vary by neighborhood",
            "ADU and garage conversion projects trigger zoning + building review",
            "Solar interconnect paperwork adds 1–3 weeks beyond city permit",
        ),
        climate_lead="Central Texas blends long heat with occasional hard freezes:",
        climate_bullets=(
            "Extended cooling season favors variable-speed and heat-pump systems",
            "Spring hail events create sudden roofing labor shortages",
            "Clay soil movement affects foundations, fences, and patio slabs",
            "Hard freezes occasionally damage exposed plumbing and HVAC condensers",
        ),
        project_recommendations=(
            ("Heat-pump HVAC upgrade", "Handles mild winters and long summers efficiently"),
            ("Kitchen open-concept remodel", "Top request in 1980s–2000s Austin tract homes"),
            ("Solar + battery storage", "Rising Austin Energy rates improve payback"),
            ("Hail-resistant roof", "Insurance discounts available for Class 4 shingles"),
        ),
        cost_drivers=(
            "Williamson vs. Travis county labor rate differences",
            "Energy-code compliance on HVAC and electrical upgrades",
            "Hill Country lot slopes add excavation and fence labor",
            "Design-forward finish selections in tech-corridor neighborhoods",
        ),
    ),
    "houston": LocalSeoBlock(
        labor_lead=(
            "Houston's Gulf Coast humidity keeps HVAC crews in constant demand. Roofing labor competes "
            "with storm-repair surges, and foundation specialists are common on clay-soil suburban lots."
        ),
        labor_bullets=(
            "Year-round humidity shortens AC equipment life — replacement cycles are frequent",
            "Wind-rated roofing crews certified for coastal counties command premiums",
            "Katy, Pearland &amp; The Woodlands each have busy suburban contractor pools",
            "Foundation and drainage subs often bundled with exterior projects",
        ),
        permit_lead=(
            "Harris, Fort Bend, and Montgomery counties plus city of Houston each maintain separate "
            "permit systems. Wind-borne debris regions require documented roofing products and installation."
        ),
        permit_bullets=(
            "Full re-roof permits required in Houston and most Harris County cities",
            "Mechanical permits for HVAC include load calculations in many jurisdictions",
            "Flood-zone properties may need elevation certificates for major exterior work",
            "Solar permits plus CenterPoint interconnection review for grid-tied systems",
        ),
        climate_lead="Gulf Coast humidity and storms dominate Houston project planning:",
        climate_bullets=(
            "High humidity demands dehumidification-ready HVAC and mold-resistant materials",
            "Hurricane wind exposure influences roofing fastening and material ratings",
            "Clay soils and flooding affect foundations, drainage, and fence posts",
            "Minimal heating need — cooling efficiency drives utility bills year-round",
        ),
        project_recommendations=(
            ("Wind-rated roof replacement", "Storm cycles and insurance requirements drive demand"),
            ("High-SEER central AC + duct sealing", "Humidity control is essential, not optional"),
            ("Kitchen remodel in aging stock", "1980s–2000s suburban homes are prime candidates"),
            ("Privacy fencing", "Standard in Katy, Pearland &amp; Cypress family neighborhoods"),
        ),
        cost_drivers=(
            "Humidity-rated HVAC equipment and corrosion-resistant coils",
            "Wind-code roofing materials and enhanced fastening labor",
            "Clay-soil foundation prep for fences and outdoor structures",
            "Flood-zone insurance requirements affecting exterior scope",
        ),
    ),
    "san-antonio": LocalSeoBlock(
        labor_lead=(
            "San Antonio offers some of the most affordable licensed labor among major Texas metros. "
            "Stucco and tile specialists are common, and military-family housing turnover keeps "
            "bath and flooring crews steady."
        ),
        labor_bullets=(
            "Lower labor rates than Austin, Dallas, or Houston for comparable scopes",
            "Tile roof and stucco repair crews widely available in Bexar County",
            "Northern suburbs (Schertz, New Braunfels) have growing contractor pools",
            "Hard-water plumbing issues add scope to many bath remodels",
        ),
        permit_lead=(
            "City of San Antonio Development Services issues building and mechanical permits. "
            "Northern suburbs like Schertz and Boerne maintain separate offices with shorter "
            "backlogs than coastal Texas cities."
        ),
        permit_bullets=(
            "Re-roof permits required for tear-off projects — overlay limited in many areas",
            "HVAC mechanical permits include efficiency documentation",
            "Historic districts near downtown may require design review",
            "Solar permits plus CPS Energy interconnection for grid approval",
        ),
        climate_lead="South Texas heat with occasional hard freezes shapes material choices:",
        climate_bullets=(
            "Hot summers favor tile roofing and light-colored cool-roof coatings",
            "Occasional hard freezes require pipe insulation and HVAC freeze protection",
            "Limestone and clay soils affect fence post depth and patio prep",
            "Moderate humidity vs. Houston — still a long cooling season",
        ),
        project_recommendations=(
            ("Tile or composition roof replacement", "Common on stucco homes built 1980s–2000s"),
            ("Master bath remodel", "Walk-in showers popular with aging-in-place buyers"),
            ("Central AC upgrade", "Affordable labor makes full changeouts attractive"),
            ("Backyard privacy fence", "Standard in northern Bexar County subdivisions"),
        ),
        cost_drivers=(
            "Stucco repair bundled with roof and window projects",
            "Hard-water fixture upgrades in bath remodels",
            "Tile vs. composition roofing material spread",
            "Military housing turnover driving cosmetic refresh demand",
        ),
    ),
    "fort-worth": LocalSeoBlock(
        labor_lead=(
            "Fort Worth shares DFW storm exposure but often sees slightly lower bids than Dallas proper. "
            "Western Tarrant County suburban growth (Keller, Mansfield, Southlake) keeps fencing and "
            "single-story roof crews busy."
        ),
        labor_bullets=(
            "Hail-season roofing demand mirrors Dallas — same storm paths",
            "Ranch-style single-story homes simplify roof and HVAC access",
            "Keller &amp; Southlake HOAs drive premium exterior standards",
            "Competitive pricing vs. East Coast and California metros",
        ),
        permit_lead=(
            "City of Fort Worth Development Services and Tarrant County suburbs each issue permits. "
            "Hail-prone areas may require impact-rated product documentation at inspection."
        ),
        permit_bullets=(
            "Re-roof permits in Fort Worth, Arlington, Keller &amp; Mansfield",
            "HVAC mechanical permits for system replacements and duct modifications",
            "Fence permits required in many Tarrant County cities above height limits",
            "Solar permits plus Oncor interconnection for western DFW",
        ),
        climate_lead="Western DFW shares North Texas hail and heat patterns:",
        climate_bullets=(
            "Hailstorms drive impact-rated shingle upgrades every 5–10 years in many neighborhoods",
            "100°F+ summers increase AC runtime on open suburban lots",
            "Wind exposure on western prairie lots affects fence and roof durability",
            "Attic insulation upgrades reduce cooling bills on 1980s ranch stock",
        ),
        project_recommendations=(
            ("Impact-rated roof replacement", "Insurance-driven after Tarrant County hail events"),
            ("Wood privacy fencing", "Top project in Keller, Mansfield &amp; Burleson"),
            ("Central AC replacement", "Single-story ranches simplify install labor"),
            ("Kitchen open-concept update", "Popular in western DFW suburban upgrades"),
        ),
        cost_drivers=(
            "Hail insurance claims and adjuster scheduling delays",
            "HOA exterior standards in Southlake and Keller",
            "Tarrant vs. Dallas county permit fee differences",
            "Single-story access reducing labor vs. two-story homes",
        ),
    ),
    "phoenix": LocalSeoBlock(
        labor_lead=(
            "Phoenix metro labor is shaped by extreme summer heat — roofers start at dawn and HVAC crews "
            "book months ahead before peak season. Maricopa County's growth keeps new-construction "
            "and retrofit crews in steady demand."
        ),
        labor_bullets=(
            "Summer heat limits roofing hours — peak-season premiums common June–August",
            "Tile and foam roof specialists widely available in Maricopa County",
            "Scottsdale crews charge more than East Valley for the same scope",
            "Solar installers compete aggressively — get multiple quotes",
        ),
        permit_lead=(
            "City of Phoenix and Maricopa County cities (Mesa, Chandler, Gilbert) use online permitting "
            "for most residential work. Solar requires utility interconnection with APS or SRP."
        ),
        permit_bullets=(
            "Roof permits required for tear-off and structural changes",
            "HVAC mechanical permits include tonnage and efficiency documentation",
            "Solar building permit plus APS/SRP interconnection agreement",
            "HOA approval common in master-planned communities before city permit",
        ),
        climate_lead="Sonoran Desert extremes drive every Phoenix-area project decision:",
        climate_bullets=(
            "120°F+ days increase cooling load and shorten shingle lifespan",
            "UV degradation affects roofing, paint, and fence materials within 10–15 years",
            "Monsoon wind and dust storms test roof fastening and drainage",
            "Radiant barriers and attic ventilation are standard upgrades, not luxuries",
        ),
        project_recommendations=(
            ("Tile or cool-roof replacement", "Heat resistance and longevity justify upfront cost"),
            ("High-SEER central AC", "Essential before summer peak — book early"),
            ("Rooftop solar system", "Among the best production-per-square-foot markets in the U.S."),
            ("Desert landscaping &amp; fencing", "Low-water hardscape and pool-area privacy"),
        ),
        cost_drivers=(
            "Summer labor premiums and limited working hours on roofs",
            "Tile vs. asphalt material cost spread",
            "APS vs. SRP solar interconnection timelines",
            "HOA architectural standards in master-planned suburbs",
        ),
    ),
    "scottsdale": LocalSeoBlock(
        labor_lead=(
            "Scottsdale commands premium labor rates for luxury finishes, tile roofing, and custom "
            "outdoor living. HOA architectural committees are strict — experienced contractors who "
            "navigate design review are worth the premium."
        ),
        labor_bullets=(
            "Highest labor rates in the Phoenix metro for comparable scopes",
            "Custom outdoor kitchen and hardscape specialists widely available",
            "Tile and metal roof crews experienced with HOA documentation",
            "Design-build firms dominate high-end kitchen and bath remodels",
        ),
        permit_lead=(
            "City of Scottsdale Building Services requires permits for roofing, HVAC, and structural "
            "work. HOA architectural review is mandatory in most communities before permit submission."
        ),
        permit_bullets=(
            "HOA design approval often required before city permit application",
            "Tile roof permits include product specs for desert heat ratings",
            "Pool-adjacent electrical work requires separate permits and inspections",
            "Solar permits plus SRP/APS interconnection — battery storage adds electrical review",
        ),
        climate_lead="Desert heat and HOA standards define Scottsdale exterior projects:",
        climate_bullets=(
            "Extreme UV exposure requires premium exterior coatings and tile roofs",
            "Monsoon wind can damage poorly secured tile and patio covers",
            "Low humidity increases evaporative cooling options in some areas",
            "Large roof areas on custom homes amplify material and labor totals",
        ),
        project_recommendations=(
            ("Luxury kitchen remodel", "Custom cabinetry and premium surfaces are the norm"),
            ("Tile or metal roof", "HOA-preferred materials for desert longevity"),
            ("Solar + battery storage", "Large homes with pool pumps benefit most"),
            ("Outdoor living &amp; hardscape", "Desert contemporary patios and pergolas"),
        ),
        cost_drivers=(
            "Premium finish tiers and custom fabrication",
            "HOA design review cycles adding calendar time",
            "Large custom home square footage on roof and HVAC",
            "North Scottsdale labor premiums vs. Mesa or Chandler",
        ),
    ),
    "mesa": LocalSeoBlock(
        labor_lead=(
            "Mesa and the East Valley offer more affordable labor than Scottsdale while serving a "
            "large stock of 1990s–2000s suburban homes. Solar and HVAC crews are especially active "
            "in family-oriented neighborhoods."
        ),
        labor_bullets=(
            "Lower labor rates than Scottsdale or North Phoenix",
            "Strong solar installer competition in Gilbert/Mesa corridor",
            "LVP flooring and bath remodel crews widely available",
            "HOA communities require approved contractor documentation",
        ),
        permit_lead=(
            "City of Mesa Development Services issues residential permits. East Valley cities share "
            "similar requirements — roof, HVAC, and solar all need approval before work begins."
        ),
        permit_bullets=(
            "Re-roof permits for tear-off — overlay rules vary by HOA",
            "HVAC permits include SEER documentation for replacements",
            "Solar permit plus SRP interconnection (common in Mesa)",
            "Fence permits for walls above 6 feet in many subdivisions",
        ),
        climate_lead="East Valley desert heat matches Phoenix with slightly lower costs:",
        climate_bullets=(
            "Long cooling season drives frequent AC replacement cycles",
            "UV exposure on east-facing walls and fences",
            "Monsoon drainage issues in older subdivisions",
            "Solar production excellent on single-story ranch roofs",
        ),
        project_recommendations=(
            ("Solar panel installation", "Strong ROI on single-story East Valley homes"),
            ("LVP flooring refresh", "Popular upgrade over carpet in 1990s builds"),
            ("Central AC replacement", "Affordable labor makes full changeouts practical"),
            ("Kitchen update", "Cosmetic refresh before move-up sale"),
        ),
        cost_drivers=(
            "East Valley vs. Scottsdale labor rate gap",
            "Single-story ranch roof access reducing labor",
            "SRP solar interconnection timeline",
            "HOA exterior color and material restrictions",
        ),
    ),
    "tucson": LocalSeoBlock(
        labor_lead=(
            "Tucson labor runs below Phoenix metro averages. Older housing stock and university-area "
            "rentals create steady demand for practical HVAC, roofing, and flooring upgrades rather "
            "than luxury remodels."
        ),
        labor_bullets=(
            "More affordable labor than Phoenix or Scottsdale",
            "Older flat-roof and built-up roofing specialists available",
            "Evaporative cooling conversions to central AC are common",
            "University-area rentals drive cosmetic refresh demand",
        ),
        permit_lead=(
            "City of Tucson Planning and Development Services handles residential permits. "
            "Pima County jurisdictions outside city limits have separate offices."
        ),
        permit_bullets=(
            "Roof permits for structural changes and full tear-off",
            "HVAC permits for system type changes (evap to refrigerated AC)",
            "Solar permits plus Tucson Electric Power interconnection",
            "Historic adobe districts may require additional design review",
        ),
        climate_lead="Southern Arizona desert climate with higher elevation than Phoenix:",
        climate_bullets=(
            "Hot summers with slightly cooler nights than Phoenix",
            "Monsoon season brings intense short-duration rain and wind",
            "Older flat roofs prone to ponding and UV damage",
            "Evaporative cooling still common in older Tucson homes",
        ),
        project_recommendations=(
            ("Evap-to-AC conversion", "Common upgrade in pre-1990 Tucson homes"),
            ("Flat roof recoating or replacement", "Aging built-up roofs need attention"),
            ("Solar installation", "Excellent sun with lower install costs than Phoenix"),
            ("Bath &amp; flooring refresh", "Rental and starter-home turnover projects"),
        ),
        cost_drivers=(
            "Flat vs. pitched roof complexity on older stock",
            "Evaporative-to-refrigerated AC conversion scope",
            "Lower labor rates offsetting material transport costs",
            "Historic district review in central Tucson neighborhoods",
        ),
    ),
    "chandler": LocalSeoBlock(
        labor_lead=(
            "Chandler sits in the heart of the East Valley family-housing corridor. Contractors "
            "experienced with HOA requirements and desert exteriors are easy to find, with pricing "
            "between Mesa affordability and Scottsdale premiums."
        ),
        labor_bullets=(
            "Family-subdivision fencing and pool-area crews in high demand",
            "HOA-experienced roofers familiar with tile and cool-roof specs",
            "Labor rates between Mesa and Scottsdale averages",
            "Strong competition among solar installers along the 202 corridor",
        ),
        permit_lead=(
            "City of Chandler Development Services issues building and mechanical permits. "
            "Most Chandler subdivisions also require HOA approval before exterior work."
        ),
        permit_bullets=(
            "Roof permits with product documentation for HOA submission",
            "HVAC mechanical permits for tonnage changes",
            "Solar permit plus SRP interconnection (west Chandler) or APS (east)",
            "Pool barrier and fence permits for safety compliance",
        ),
        climate_lead="Chandler shares East Valley desert conditions:",
        climate_bullets=(
            "Intense summer heat on tile and asphalt roofs",
            "HOA-maintained desert landscaping limits some outdoor scope",
            "Monsoon wind tests patio covers and fence stability",
            "High cooling load on 2,000+ sq ft family homes",
        ),
        project_recommendations=(
            ("Tile roof maintenance or replacement", "Common on 1990s–2000s Chandler builds"),
            ("Pool-area fencing", "Safety and privacy in family neighborhoods"),
            ("High-SEER AC upgrade", "Large homes with long duct runs benefit most"),
            ("Kitchen refresh", "Move-up buyers updating before sale"),
        ),
        cost_drivers=(
            "HOA tile and color requirements on exterior projects",
            "Pool-adjacent electrical and fence code compliance",
            "Two-story homes adding roof and HVAC complexity",
            "SRP vs. APS utility territory affecting solar timeline",
        ),
    ),
    "tampa": LocalSeoBlock(
        labor_lead=(
            "Tampa Bay contractors specialize in wind-rated roofing and humidity-ready HVAC. "
            "Coastal building codes require certified installers, and storm-season surges can "
            "delay projects across Pinellas and Hillsborough counties."
        ),
        labor_bullets=(
            "Wind-rated roofing crews certified for coastal product installation",
            "Humidity-focused HVAC installers prioritize duct sealing and sizing",
            "Labor rates above Texas but below Miami-Dade premiums",
            "Flood-zone work may require elevation-aware contractors",
        ),
        permit_lead=(
            "Hillsborough County and City of Tampa Building Services issue permits. "
            "Coastal wind-borne debris regions require documented product approval (Florida Product Approval)."
        ),
        permit_bullets=(
            "Roof permits require Florida Product Approval numbers on materials",
            "HVAC mechanical permits include Manual J load calculations",
            "Flood-zone properties may need additional review for exterior work",
            "Solar permits plus Duke Energy or TECO interconnection",
        ),
        climate_lead="Gulf Coast humidity and hurricane exposure define Tampa projects:",
        climate_bullets=(
            "Hurricane season wind ratings required on roofing and openings",
            "High humidity — mold-resistant materials and dehumidification matter",
            "Salt air near the bay accelerates HVAC coil and fastener corrosion",
            "Year-round cooling with minimal heating demand",
        ),
        project_recommendations=(
            ("Wind-rated roof replacement", "Insurance and code compliance drive material choices"),
            ("High-SEER AC with dehumidification", "Comfort depends on humidity control, not just cooling"),
            ("Bathroom remodel", "Walk-in showers popular in aging block-home stock"),
            ("Pool enclosure or privacy fence", "Standard in Tampa Bay family neighborhoods"),
        ),
        cost_drivers=(
            "Florida Product Approval requirements on roofing materials",
            "Wind mitigation inspections affecting insurance premiums",
            "Flood-zone elevation requirements on some properties",
            "Salt-air rated fasteners and corrosion-resistant HVAC equipment",
        ),
    ),
    "orlando": LocalSeoBlock(
        labor_lead=(
            "Orlando's theme-park metro growth keeps remodel and HVAC crews busy year-round. "
            "Central Florida contractors handle both vacation-rental refreshes and suburban "
            "family-home upgrades across Orange and Seminole counties."
        ),
        labor_bullets=(
            "Short-term rental remodels create steady cosmetic-upgrade demand",
            "Central FL heat drives year-round AC replacement cycles",
            "Labor between Jacksonville affordability and Miami premiums",
            "Screen enclosure specialists widely available",
        ),
        permit_lead=(
            "Orange County and City of Orlando Permitting Services handle residential projects. "
            "Wind-borne debris requirements apply inland, though less strict than coastal counties."
        ),
        permit_bullets=(
            "Roof permits with wind-rating documentation",
            "HVAC permits for system replacements in unincorporated Orange County",
            "Electrical permits for solar and panel upgrades",
            "Short-term rental conversions may trigger additional inspection requirements",
        ),
        climate_lead="Central Florida heat and inland storm paths shape project priorities:",
        climate_bullets=(
            "Afternoon thunderstorms and lightning risk for HVAC equipment",
            "Hurricane wind exposure from Atlantic systems — inland but not immune",
            "High cooling load on single-story ranch homes",
            "Pool and screen enclosure maintenance in humid conditions",
        ),
        project_recommendations=(
            ("Central AC replacement", "Non-negotiable in Central Florida summers"),
            ("Kitchen remodel", "1990s–2000s suburban stock ripe for open-concept updates"),
            ("Wind-rated roofing", "Inland storm paths still require proper fastening"),
            ("Screen enclosure repair", "Unique to Florida outdoor living"),
        ),
        cost_drivers=(
            "Vacation-rental finish standards vs. owner-occupied budgets",
            "Screen enclosure aluminum pricing and labor",
            "Orange vs. Seminole county permit fee differences",
            "Lightning protection and surge requirements for HVAC",
        ),
    ),
    "miami": LocalSeoBlock(
        labor_lead=(
            "Miami-Dade carries Florida's highest labor rates. Condo renovations require "
            "building-specific expertise, and coastal corrosion demands specialized materials "
            "for roofing, HVAC, and exterior work."
        ),
        labor_bullets=(
            "Highest Florida labor rates — 15%+ above national average",
            "Condo and high-rise remodel specialists with COI/association experience",
            "Impact window and roofing crews in constant demand",
            "Bilingual contractor market — verify licensing in Miami-Dade portal",
        ),
        permit_lead=(
            "Miami-Dade County RER Building Department has strict product approval and "
            "inspection requirements. Condos add building association approval layers."
        ),
        permit_bullets=(
            "Miami-Dade Notice of Acceptance (NOA) required on exterior products",
            "Condo remodels need building association approval before city permit",
            "Roof permits include wind uplift documentation",
            "Electrical permits for solar with FPL interconnection review",
        ),
        climate_lead="Tropical coastal conditions are the toughest in our Florida markets:",
        climate_bullets=(
            "Category-level wind exposure drives impact-rated everything",
            "Extreme humidity and salt spray corrosion on all exterior materials",
            "Minimal heating — all-year cooling and dehumidification",
            "Flood zones affect ground-floor remodel scope and insurance",
        ),
        project_recommendations=(
            ("Impact-rated roof or windows", "Insurance requirements and storm resilience"),
            ("Compact bath remodel", "Condo and townhome layout constraints"),
            ("Corrosion-resistant HVAC", "Coastal coil and cabinet protection essential"),
            ("Solar panels", "Strong sun offsets high FPL electric rates"),
        ),
        cost_drivers=(
            "Miami-Dade NOA product premiums on all exterior materials",
            "Condo association fees and approval timelines",
            "South Florida labor premium vs. Jacksonville or Tampa",
            "Flood insurance and elevation affecting project scope",
        ),
    ),
    "jacksonville": LocalSeoBlock(
        labor_lead=(
            "Jacksonville offers Florida's best labor value among major metros. Large suburban "
            "housing stock built in the 1980s–2000s creates steady roofing, HVAC, and fencing "
            "demand without Miami-level premiums."
        ),
        labor_bullets=(
            "Most affordable Florida major-metro labor rates",
            "Large contractor pool across Duval, St. Johns &amp; Clay counties",
            "Suburban fencing and roofing crews widely available",
            "Beach communities add salt-air material requirements",
        ),
        permit_lead=(
            "City of Jacksonville Building Inspection Division handles most permits. "
            "St. Johns and Clay counties have separate offices for suburban projects."
        ),
        permit_bullets=(
            "Roof permits required for full replacements",
            "HVAC mechanical permits in Duval and St. Johns counties",
            "Fence permits for heights above local limits",
            "Solar permits plus JEA interconnection for grid-tied systems",
        ),
        climate_lead="North Florida humidity with coastal storm exposure:",
        climate_bullets=(
            "Humid subtropical climate — mold-resistant materials recommended",
            "Hurricane exposure from Atlantic systems — wind ratings still matter",
            "Salt air in beach communities (Jacksonville Beach, Ponte Vedra)",
            "Moderate heating needs vs. South Florida — heat pumps work well",
        ),
        project_recommendations=(
            ("Roof replacement", "Storm and age cycles on 20–30 year shingle stock"),
            ("HVAC upgrade with dehumidification", "Humidity control improves comfort and efficiency"),
            ("Suburban kitchen remodel", "Open-concept updates in St. Johns County growth areas"),
            ("Backyard privacy fence", "Standard in Nocatee and Orange Park subdivisions"),
        ),
        cost_drivers=(
            "Duval vs. St. Johns county labor and permit differences",
            "Salt-air upgrades in coastal suburbs",
            "Large lot fencing linear footage",
            "Affordable labor keeping projects below South FL totals",
        ),
    ),
    "st-petersburg": LocalSeoBlock(
        labor_lead=(
            "St. Petersburg contractors specialize in coastal peninsula work — wind-rated roofing, "
            "mid-century block-home remodels, and salt-air-resistant HVAC. Pinellas County's "
            "dense build-out means experienced crews are essential."
        ),
        labor_bullets=(
            "Coastal roofing crews experienced with tile and wind-rated shingles",
            "Mid-century block-home bath remodel specialists",
            "Peninsula logistics can add travel surcharges from Tampa crews",
            "Flood-zone expertise needed in low-elevation neighborhoods",
        ),
        permit_lead=(
            "City of St. Petersburg Construction Services and Pinellas County handle permits. "
            "Coastal wind-borne debris requirements apply across the peninsula."
        ),
        permit_bullets=(
            "Wind-rated product documentation on all roofing materials",
            "Flood-zone properties may need elevation certificates",
            "HVAC permits with coastal corrosion considerations noted",
            "Historic Kenwood and Old Northeast may require design review",
        ),
        climate_lead="Pinellas peninsula coastal exposure shapes every exterior decision:",
        climate_bullets=(
            "Direct Gulf exposure — hurricane wind ratings mandatory",
            "Salt air corrosion on HVAC, fasteners, and fencing",
            "High humidity in aging block homes without modern vapor barriers",
            "Flood zones affect insurance and ground-floor remodel scope",
        ),
        project_recommendations=(
            ("Coastal wind-rated roofing", "Tile and shingle upgrades on 1950s–1970s stock"),
            ("Bathroom remodel", "Tub-to-shower conversions in block ranch homes"),
            ("Salt-air HVAC replacement", "Coated coils and corrosion-resistant cabinets"),
            ("Pool-area fencing", "Privacy and safety in waterfront neighborhoods"),
        ),
        cost_drivers=(
            "Peninsula coastal product premiums vs. inland Tampa",
            "Flood-zone insurance requirements",
            "Historic district design review in central St. Pete",
            "Block construction adding demo labor in bath remodels",
        ),
    ),
    "raleigh": LocalSeoBlock(
        labor_lead=(
            "Raleigh and Wake County benefit from Research Triangle growth — steady remodel demand "
            "and competitive contractor pricing below Northeast and California metros. Crawl-space "
            "homes are common, affecting HVAC duct routing and cost."
        ),
        labor_bullets=(
            "Growing contractor pool serving Apex, Cary &amp; Wake Forest",
            "Lower labor rates than Northeast or West Coast metros",
            "Crawl-space HVAC access can add labor vs. slab foundations",
            "Licensed GCs required for projects over $40k in NC",
        ),
        permit_lead=(
            "City of Raleigh Development Services and Wake County jurisdictions issue permits. "
            "Mechanical, electrical, and plumbing are often separate permit types."
        ),
        permit_bullets=(
            "Building permit for structural remodels and roof tear-off",
            "Mechanical permit for HVAC changeouts — 16+ SEER common in new installs",
            "Electrical permit for panel upgrades and solar",
            "Separate plumbing permit for bath and kitchen fixture relocations",
        ),
        climate_lead="Piedmont humidity with mild winters — balanced HVAC demand:",
        climate_bullets=(
            "Humid summers drive cooling load; mild winters favor heat pumps",
            "Occasional ice storms damage roofs and gutters",
            "Pine pollen and moisture affect deck and fence maintenance",
            "Crawl-space moisture control important for HVAC duct longevity",
        ),
        project_recommendations=(
            ("Architectural shingle roof", "20-year replacement cycles on 2000s suburban stock"),
            ("Heat-pump HVAC", "Handles Raleigh's mild winters and humid summers"),
            ("Kitchen &amp; bath remodel", "Move-up buyers in Apex and Holly Springs"),
            ("LVP flooring", "Popular carpet replacement in family subdivisions"),
        ),
        cost_drivers=(
            "Wake County vs. Durham County permit fee differences",
            "Crawl-space duct modifications adding HVAC labor",
            "Research Triangle labor demand keeping remodel bids steady",
            "Piedmont clay soil affecting fence post installation",
        ),
    ),
    "charlotte": LocalSeoBlock(
        labor_lead=(
            "Charlotte's banking-metro growth fuels suburban remodel demand in Mecklenburg and "
            "Union counties. Labor rates sit below national averages with strong availability "
            "for roofing, HVAC, and kitchen crews."
        ),
        labor_bullets=(
            "Competitive labor market vs. Raleigh and coastal metros",
            "Banking-sector move-up buyers drive kitchen and bath demand",
            "Union County (Fort Mill, Waxhaw) has separate permit offices",
            "Two-story suburban homes common — roof access adds labor",
        ),
        permit_lead=(
            "Mecklenburg County Code Enforcement handles most Charlotte-area permits. "
            "Fort Mill and Lancaster (SC) projects fall under separate South Carolina jurisdictions."
        ),
        permit_bullets=(
            "Roof permit for tear-off — Mecklenburg County online portal",
            "HVAC mechanical permit with efficiency documentation",
            "Electrical permit for solar with Duke Energy interconnection",
            "SC cross-border projects (Fort Mill) need Lancaster County permits",
        ),
        climate_lead="Charlotte Piedmont climate — humid summers, mild winters:",
        climate_bullets=(
            "Humid summers with strong cooling demand",
            "Mild winters — heat pumps gaining market share over furnaces",
            "Occasional ice storms affect roofing and tree-damage repairs",
            "Red clay soil movement affects foundations and fence posts",
        ),
        project_recommendations=(
            ("Roof replacement", "Storm and age-driven on 1990s–2000s Mecklenburg stock"),
            ("Kitchen remodel with quartz counters", "Move-up buyer standard in Matthews/Huntersville"),
            ("Heat-pump or high-SEER AC", "Efficiency upgrades before summer peak"),
            ("Wood privacy fence", "Popular in Fort Mill and Ballantyne subdivisions"),
        ),
        cost_drivers=(
            "NC vs. SC cross-border permit differences in southern suburbs",
            "Red clay soil prep for fences and outdoor structures",
            "Two-story roof pitch adding labor vs. ranch homes",
            "Mecklenburg County growth keeping contractor demand high",
        ),
    ),
    "durham": LocalSeoBlock(
        labor_lead=(
            "Durham blends older in-town housing near Duke and RTP with suburban growth in "
            "Chapel Hill direction. Contractors experienced with older home quirks — cast "
            "iron plumbing, small kitchens — are in steady demand."
        ),
        labor_bullets=(
            "Older home specialists for pre-1980 housing stock",
            "University-area rental refreshes drive cosmetic remodel demand",
            "Labor similar to Raleigh with slightly lower suburban premiums",
            "Triangle-area contractor pool shared with Raleigh and Cary",
        ),
        permit_lead=(
            "City of Durham Neighborhood Improvement Services issues permits. "
            "Durham County handles unincorporated areas. Historic districts near downtown "
            "may require design review."
        ),
        permit_bullets=(
            "Building permit for structural and roof work",
            "Mechanical permit for HVAC — common in older homes upgrading from window units",
            "Plumbing permit for cast-iron replacement in bath remodels",
            "Historic district review near Brightleaf and downtown",
        ),
        climate_lead="Durham shares Triangle humidity with older housing challenges:",
        climate_bullets=(
            "Humid summers — older homes often lack modern insulation",
            "Aging roofs on 1960s–1980s stock due for replacement",
            "Crawl-space moisture in pre-1970 homes",
            "Mild winters suitable for heat-pump conversions",
        ),
        project_recommendations=(
            ("Bath remodel with plumbing upgrade", "Cast iron replacement common in older Durham homes"),
            ("Roof replacement", "Aging shingle stock in established neighborhoods"),
            ("Mini-split or heat-pump HVAC", "Older homes without ductwork"),
            ("Kitchen update", "Compact layouts in in-town bungalows and ranch homes"),
        ),
        cost_drivers=(
            "Older home surprises — plumbing, wiring, and structural issues",
            "Historic district review adding time and design cost",
            "Rental vs. owner-occupied finish level differences",
            "Shared Triangle labor pool with Raleigh/Cary competition",
        ),
    ),
    "cary": LocalSeoBlock(
        labor_lead=(
            "Cary's master-planned subdivisions create predictable project scope — HOA-driven "
            "exteriors, family-home kitchen upgrades, and fencing. Contractors familiar with "
            "Wake County HOA documentation are essential."
        ),
        labor_bullets=(
            "HOA-experienced contractors required in most Cary subdivisions",
            "Family-home kitchen and bath remodels in high demand",
            "Competitive Triangle labor rates",
            "Fencing crews busy in Amberly, Preston, and Lochmere communities",
        ),
        permit_lead=(
            "Town of Cary Development Services issues permits with online submission. "
            "HOA architectural approval typically precedes town permit application."
        ),
        permit_bullets=(
            "HOA approval letter required for most exterior projects",
            "Building permit for roof tear-off and structural changes",
            "Fence permit with height and material documentation for HOA",
            "Mechanical permit for HVAC with Manual J in some subdivisions",
        ),
        climate_lead="Cary shares Triangle climate with strict HOA exterior standards:",
        climate_bullets=(
            "Humid summers — AC efficiency matters in two-story family homes",
            "HOA-required maintenance cycles on roofs and fences",
            "Piedmont clay soil affecting fence post depth",
            "Tree coverage in established subdivisions affects solar viability",
        ),
        project_recommendations=(
            ("Kitchen remodel", "Move-up standard in Cary's 1990s–2000s subdivisions"),
            ("Wood privacy fence", "Required or expected in most Cary neighborhoods"),
            ("Roof replacement at 20-year mark", "Predictable cycle on original builder shingles"),
            ("LVP flooring", "Carpet replacement before resale in family homes"),
        ),
        cost_drivers=(
            "HOA material and color restrictions on exteriors",
            "Two-story home roof and HVAC complexity",
            "Town of Cary permit fees vs. unincorporated Wake County",
            "Triangle growth keeping kitchen remodel bids competitive",
        ),
    ),
    "wilmington": LocalSeoBlock(
        labor_lead=(
            "Wilmington contractors specialize in coastal humidity, hurricane-rated roofing, and "
            "moisture-resistant remodels. Cape Fear region labor runs slightly above inland NC "
            "due to salt-air material requirements and storm-code compliance."
        ),
        labor_bullets=(
            "Coastal roofing crews with wind-rating experience",
            "Salt-air HVAC corrosion specialists",
            "Labor premium vs. Raleigh/Charlotte inland metros",
            "Vacation-home and retiree remodel demand steady",
        ),
        permit_lead=(
            "City of Wilmington Planning &amp; Development and New Hanover County issue permits. "
            "Coastal wind and flood requirements add documentation vs. inland NC."
        ),
        permit_bullets=(
            "Wind-rated roofing product documentation required",
            "Flood-zone elevation review for ground-floor work",
            "Mechanical permit for corrosion-resistant HVAC specs",
            "Historic downtown Wilmington may require design review",
        ),
        climate_lead="Coastal NC humidity and hurricane exposure:",
        climate_bullets=(
            "Hurricane wind exposure — enhanced roofing fastening required",
            "High humidity and salt air accelerate exterior material degradation",
            "Flood zones in low-elevation neighborhoods affect insurance",
            "Mild winters — heat pumps handle heating and cooling efficiently",
        ),
        project_recommendations=(
            ("Wind-rated roof replacement", "Coastal code compliance and insurance requirements"),
            ("Moisture-resistant bath remodel", "Ventilation and mold-resistant materials essential"),
            ("Salt-air HVAC replacement", "Coated coils for coastal longevity"),
            ("Deck and fence rebuild", "Salt and humidity shorten wood lifespan near the coast"),
        ),
        cost_drivers=(
            "Coastal wind-rating material premiums",
            "Flood insurance and elevation requirements",
            "Salt-air rated fasteners and HVAC equipment",
            "Vacation-home vs. primary-residence finish expectations",
        ),
    ),
    "san-diego": LocalSeoBlock(
        labor_lead=(
            "San Diego carries California coastal labor premiums. Title 24 energy code compliance "
            "adds scope to HVAC and window projects, and coastal corrosion requires specialized "
            "materials for roofing and exterior work."
        ),
        labor_bullets=(
            "Coastal labor rates ~25–30% above national average",
            "Title 24–experienced HVAC installers required for permits",
            "Tile and flat-roof specialists common on SD County homes",
            "ADU builders active in North Park and coastal neighborhoods",
        ),
        permit_lead=(
            "City of San Diego Development Services and county jurisdictions require permits "
            "for virtually all structural, mechanical, and electrical work. Title 24 energy "
            "calculations are mandatory for HVAC replacements."
        ),
        permit_bullets=(
            "Title 24 compliance documentation required for HVAC changeouts",
            "Roof permit with coastal wind and fire-zone considerations",
            "Solar permit plus SDG&amp;E interconnection — often 2–4 week review",
            "ADU permits include separate utility and zoning review",
        ),
        climate_lead="Mediterranean coastal climate with wildfire and salt-air factors:",
        climate_bullets=(
            "Mild year-round climate — moderate heating, significant cooling near inland valleys",
            "Salt air in coastal communities accelerates metal and fastener corrosion",
            "Wildfire ember zones inland require fire-rated roofing and vents",
            "Excellent solar production with high SDG&amp;E electricity rates",
        ),
        project_recommendations=(
            ("Title 24–compliant HVAC upgrade", "Required for permit — plan for higher equipment tier"),
            ("Tile or composition re-roof", "Coastal and inland fire-zone material requirements"),
            ("Solar + battery", "High electric rates and strong sun improve payback"),
            ("ADU or garage conversion", "Popular in North Park and coastal neighborhoods"),
        ),
        cost_drivers=(
            "Title 24 equipment and installation premiums",
            "Coastal labor rates and SDG&amp;E territory costs",
            "Fire-zone roofing material requirements inland",
            "Permit fees among the highest in our tracked markets",
        ),
    ),
    "los-angeles": LocalSeoBlock(
        labor_lead=(
            "Los Angeles has among the highest contractor labor rates in the country. "
            "Varied housing — bungalows, mid-century, stucco tract — means specialists "
            "for each era are essential. Seismic and energy code add compliance cost."
        ),
        labor_bullets=(
            "Labor rates 30%+ above national average",
            "Seismic retrofit specialists for pre-1980 homes",
            "ADU builders extremely active under state incentive programs",
            "Multilingual contractor market — verify CSLB license online",
        ),
        permit_lead=(
            "LADBS (Los Angeles Department of Building and Safety) handles city permits with "
            "notoriously variable timelines. Valley and Westside projects may fall under "
            "different district offices."
        ),
        permit_bullets=(
            "Title 24 energy docs required for HVAC and window replacements",
            "Seismic retrofit permits for soft-story and foundation bolting",
            "ADU permits include planning and utility clearance",
            "Solar permit plus LADWP interconnection — timeline varies by district",
        ),
        climate_lead="LA's diverse microclimates affect project scope by neighborhood:",
        climate_bullets=(
            "Valley heat drives oversized cooling loads — right-sizing matters",
            "Coastal marine layer reduces solar production vs. inland",
            "Earthquake risk influences foundation and chimney work",
            "Wildfire zones in hills require ember-resistant vents and roofing",
        ),
        project_recommendations=(
            ("Kitchen remodel", "Open-concept conversions in 1940s–1960s bungalows"),
            ("ADU or garage conversion", "Strong rental demand under state ADU laws"),
            ("Central AC or mini-split", "Valley homes especially need efficient cooling"),
            ("Seismic retrofit", "Pre-1980 homes before major remodel starts"),
        ),
        cost_drivers=(
            "LADBS permit timeline uncertainty adding holding costs",
            "Seismic and Title 24 compliance on most mechanical work",
            "Neighborhood labor premiums (Westside vs. Valley vs. East LA)",
            "Soft-story retrofit requirements on multifamily-adjacent stock",
        ),
    ),
    "orange-county": LocalSeoBlock(
        labor_lead=(
            "Orange County blends coastal and inland markets — Laguna and Newport premium "
            "finishes vs. Irvine and Anaheim practical upgrades. HOA communities dominate, "
            "requiring contractors who navigate design review efficiently."
        ),
        labor_bullets=(
            "Coastal OC labor premiums in Laguna, Newport &amp; Dana Point",
            "Irvine master-planned HOA documentation expertise essential",
            "Tile roofing specialists widely available",
            "Labor below San Francisco but above inland California",
        ),
        permit_lead=(
            "Individual OC cities (Irvine, Anaheim, Huntington Beach, etc.) each issue permits. "
            "Unincorporated areas fall under County of Orange. Title 24 applies statewide."
        ),
        permit_bullets=(
            "City-specific permit portals — Irvine, Anaheim, HB each different",
            "HOA approval before permit in most Irvine and south OC communities",
            "Title 24 HVAC compliance documentation required",
            "Solar permit plus SCE or SDG&amp;E interconnection by territory",
        ),
        climate_lead="OC coastal-inland gradient affects cooling and material choices:",
        climate_bullets=(
            "Coastal mild climate vs. inland Irvine/Yorba Linda heat",
            "Salt air in coastal cities affects exterior fasteners and HVAC",
            "Santa Ana winds test roof fastening in canyon-adjacent homes",
            "Strong solar economics in inland OC with SCE rate tiers",
        ),
        project_recommendations=(
            ("Kitchen &amp; bath remodel", "Move-up standard in Irvine and Tustin tract homes"),
            ("Tile roof replacement", "Common on OC Mediterranean-style homes"),
            ("Solar installation", "Inland OC homes with large roofs benefit most"),
            ("HOA-compliant exterior refresh", "Paint, roofing, and landscaping updates"),
        ),
        cost_drivers=(
            "Coastal vs. inland OC labor rate spread",
            "HOA design review cycles in master-planned cities",
            "City-by-city permit fee variation across OC",
            "Tile vs. composition roofing on Mediterranean-style homes",
        ),
    ),
    "sacramento": LocalSeoBlock(
        labor_lead=(
            "Sacramento offers more affordable California labor than coastal metros while "
            "still requiring Title 24 compliance. Central Valley heat drives HVAC demand, "
            "and wildfire zones inland add fire-rated material requirements."
        ),
        labor_bullets=(
            "Labor ~12–15% above national — below Bay Area and SoCal coastal",
            "Wildfire-zone roofing and vent specialists in foothill suburbs",
            "State government workforce creates steady owner-occupied remodel demand",
            "Delta breeze neighborhoods have different cooling needs than inland Elk Grove",
        ),
        permit_lead=(
            "City of Sacramento Community Development and county jurisdictions handle permits. "
            "Wildfire hazard zones require fire-rated material documentation."
        ),
        permit_bullets=(
            "Title 24 compliance for all HVAC replacements",
            "Fire-zone roofing materials required in WUI areas (Granite Bay, Folsom hills)",
            "Solar permit plus SMUD interconnection — often faster than PG&amp;E",
            "ADU permits active under state incentive programs",
        ),
        climate_lead="Central Valley heat with wildfire risk in foothill suburbs:",
        climate_bullets=(
            "100°F+ summer days in valley — oversized cooling loads common",
            "Wildfire ember zones require fire-rated roofing and vents in foothills",
            "Cool Delta breeze areas vs. hot Elk Grove/Roseville inland",
            "Mild winters — heat pumps handle Sacramento's climate well",
        ),
        project_recommendations=(
            ("High-SEER AC or heat pump", "Essential before Sacramento summer peak"),
            ("Fire-rated roof upgrade", "WUI zone homes in foothill suburbs"),
            ("Kitchen remodel", "Popular in Land Park and East Sacramento older homes"),
            ("Solar installation", "SMUD territory with competitive net metering"),
        ),
        cost_drivers=(
            "Wildfire-zone material premiums in foothill suburbs",
            "Title 24 compliance on HVAC ( statewide but enforced locally)",
            "Valley heat driving larger tonnage AC requirements",
            "More affordable labor than coastal CA but rising with Bay Area spillover",
        ),
    ),
    "san-francisco": LocalSeoBlock(
        labor_lead=(
            "San Francisco Bay Area labor is the most expensive in our tracked markets. "
            "Dense housing, strict seismic code, and limited parking/access add labor "
            "hours to even modest remodels. Victorian and Edwardian specialists are essential."
        ),
        labor_bullets=(
            "Highest labor rates in California — 40%+ above national average",
            "Victorian/Edwardian remodel specialists command significant premiums",
            "Parking and access logistics add hours on dense blocks",
            "Union and prevailing-wage environments on some projects",
        ),
        permit_lead=(
            "SFDBI (San Francisco Department of Building Inspection) and peninsula city "
            "departments each have multi-week backlogs. Soft-story retrofit program adds "
            "mandatory scope for many buildings."
        ),
        permit_bullets=(
            "SFDBI permit timeline often 4–8 weeks for plan review",
            "Soft-story seismic retrofit required for qualifying multifamily buildings",
            "Title 24 and seismic calcs on most mechanical and structural work",
            "PG&amp;E interconnection for solar — longer in SF than Sacramento",
        ),
        climate_lead="Bay Area microclimates — fog, mild temps, and seismic risk:",
        climate_bullets=(
            "Marine layer keeps cooling loads moderate in SF proper; warmer in East Bay",
            "Seismic risk requires bolting, shear walls, and chimney reinforcement",
            "Moisture and fog affect exterior paint and wood trim longevity",
            "Limited solar on foggy west-facing roofs; strong on East Bay and Peninsula",
        ),
        project_recommendations=(
            ("Bathroom remodel", "Compact layouts in Victorian flats and row houses"),
            ("Mini-split HVAC", "Ductless cooling where no central duct exists"),
            ("Kitchen galley expansion", "Common in pre-war SF and Oakland homes"),
            ("Seismic retrofit", "Mandatory for some buildings; wise before any remodel"),
        ),
        cost_drivers=(
            "Bay Area labor premium — highest in our database",
            "SFDBI permit backlog and plan-check fees",
            "Access/parking logistics on dense city blocks",
            "Seismic and soft-story mandatory scope adding cost",
        ),
    ),
}


STATE_LOCAL_SEO: dict[str, LocalSeoBlock] = {
    "texas": LocalSeoBlock(
        labor_lead=(
            "Texas labor markets vary widely — Dallas/Fort Worth hail-season roofing surges, "
            "Houston humidity specialists, and Austin design-build premiums each behave differently. "
            "Statewide, labor runs below coastal California and South Florida."
        ),
        labor_bullets=(
            "No state income tax attracts contractor migration — competitive pricing in most metros",
            "Hail-season roofing bottlenecks in North Texas every spring",
            "Gulf Coast humidity expertise required in Houston and Corpus Christi",
            "HOA-heavy suburbs in DFW, Austin, and San Antonio shape exterior scope",
        ),
        permit_lead=(
            "Texas has no statewide building code — cities and counties set their own requirements. "
            "Most metros require permits for roof tear-off, HVAC changeouts, and electrical upgrades."
        ),
        permit_bullets=(
            "Permit fees vary by city — Dallas, Houston, Austin each have separate portals",
            "County jurisdictions (Collin, Harris, Travis) add another layer outside city limits",
            "Solar interconnect through Oncor, CenterPoint, or Austin Energy depending on region",
            "HOA review separate from city permits in most master-planned suburbs",
        ),
        climate_lead="Texas spans Gulf humidity, desert heat, and hail-prone plains:",
        climate_bullets=(
            "North Texas hail drives impact-rated roofing demand",
            "Gulf Coast humidity requires dehumidification-ready HVAC",
            "100°F+ summers statewide increase cooling load and AC wear",
            "Central Texas clay soil affects foundations and fencing",
        ),
        project_recommendations=(
            ("Impact-rated roof replacement", "Insurance-driven in hail-prone North Texas"),
            ("High-SEER central AC", "Long cooling season statewide"),
            ("Solar panels", "Strong economics in Austin and fast-growing suburbs"),
            ("Backyard fencing", "Standard in suburban neighborhoods across Texas"),
        ),
        cost_drivers=(
            "Metro-specific labor rates (Houston vs. San Antonio spread)",
            "Hail insurance cycles affecting roofing demand and pricing",
            "City vs. county permit fee differences",
            "HOA material standards in master-planned communities",
        ),
    ),
    "florida": LocalSeoBlock(
        labor_lead=(
            "Florida labor rates climb from Jacksonville affordability to Miami-Dade premiums. "
            "Coastal wind-code expertise is mandatory, and humidity-ready HVAC installers "
            "are in constant demand across all major metros."
        ),
        labor_bullets=(
            "South Florida (Miami) labor 15%+ above national average",
            "Wind-rated roofing certification required in coastal counties",
            "Screen enclosure and pool contractors unique to Florida market",
            "Jacksonville and inland metros offer best labor value",
        ),
        permit_lead=(
            "Florida Building Code (FBC) sets statewide minimums with local enforcement. "
            "Coastal wind-borne debris regions require Florida Product Approval on exterior materials."
        ),
        permit_bullets=(
            "Product Approval numbers required on roofing and opening protection",
            "Miami-Dade NOA is strictest — separate from standard FBC approval",
            "Flood-zone elevation certificates for ground-floor work in coastal areas",
            "Solar permits plus utility interconnection (FPL, Duke, JEA, TECO)",
        ),
        climate_lead="Hurricane exposure and humidity define Florida project requirements:",
        climate_bullets=(
            "Hurricane wind ratings mandatory on roofing and openings",
            "Year-round humidity — mold-resistant materials essential",
            "Salt air corrosion in coastal communities",
            "Minimal heating — cooling efficiency drives utility costs",
        ),
        project_recommendations=(
            ("Wind-rated roof replacement", "Code compliance and insurance requirements"),
            ("High-SEER AC with dehumidification", "Humidity control statewide priority"),
            ("Impact windows or shutters", "Insurance discounts in coastal counties"),
            ("Pool enclosure or screen repair", "Unique Florida outdoor living standard"),
        ),
        cost_drivers=(
            "Coastal vs. inland product approval requirements",
            "Wind mitigation inspection credits on insurance",
            "South Florida labor premium vs. North Florida",
            "Flood-zone elevation affecting ground-floor scope",
        ),
    ),
    "arizona": LocalSeoBlock(
        labor_lead=(
            "Arizona labor centers on desert heat expertise — tile roofers, high-SEER HVAC "
            "installers, and solar crews. Phoenix metro rates exceed Tucson, and Scottsdale "
            "commands the highest premiums in the state."
        ),
        labor_bullets=(
            "Summer heat limits roofing hours — seasonal premiums June–August",
            "Scottsdale premium vs. Mesa/Tucson affordability",
            "Tile and foam roof specialists widely available in Maricopa County",
            "Solar installer competition strongest in Phoenix metro",
        ),
        permit_lead=(
            "Cities and counties across Arizona issue their own permits. Maricopa County "
            "cities (Phoenix, Mesa, Chandler) use online systems. Solar requires APS or SRP interconnection."
        ),
        permit_bullets=(
            "Roof permits for tear-off and structural changes",
            "HVAC mechanical permits with SEER documentation",
            "Solar permit plus APS/SRP interconnection review",
            "HOA approval before city permit in most master-planned communities",
        ),
        climate_lead="Extreme desert heat and monsoon storms shape Arizona priorities:",
        climate_bullets=(
            "120°F+ days drive cooling load and material UV degradation",
            "Monsoon wind and dust test roof fastening and drainage",
            "Low humidity changes HVAC sizing vs. humid climates",
            "Excellent solar production statewide",
        ),
        project_recommendations=(
            ("Tile or cool-roof replacement", "Heat resistance and longevity in desert sun"),
            ("High-SEER central AC", "Book before summer peak — crews fill quickly"),
            ("Rooftop solar", "Top-tier production per square foot nationally"),
            ("Desert landscaping &amp; fencing", "Low-water outdoor upgrades"),
        ),
        cost_drivers=(
            "Summer labor premiums on roofing and exterior work",
            "Scottsdale vs. East Valley labor rate spread",
            "Tile vs. asphalt roofing material cost",
            "HOA architectural standards in master-planned suburbs",
        ),
    ),
    "north-carolina": LocalSeoBlock(
        labor_lead=(
            "North Carolina benefits from competitive labor rates below Northeast and "
            "California metros. Research Triangle and Charlotte banking growth keep remodel "
            "crews busy, while coastal Wilmington adds salt-air premiums."
        ),
        labor_bullets=(
            "Labor 5–10% below national average in Raleigh and Charlotte",
            "Coastal Wilmington rates above inland Triangle metros",
            "Crawl-space home expertise important for HVAC duct work",
            "Licensed GC required for projects over $40,000 statewide",
        ),
        permit_lead=(
            "NC counties and municipalities issue separate permits. Wake, Mecklenburg, "
            "and New Hanover each have online portals. Mechanical, electrical, and plumbing "
            "permits are often separate from building permits."
        ),
        permit_bullets=(
            "Building permit for structural remodels and roof tear-off",
            "Mechanical permit for HVAC — 16+ SEER common on replacements",
            "Coastal counties add wind-rating documentation",
            "Electrical permit for solar with Duke Energy interconnection",
        ),
        climate_lead="Piedmont humidity with coastal storm exposure in the east:",
        climate_bullets=(
            "Humid summers drive cooling; mild winters favor heat pumps",
            "Coastal hurricane exposure in Wilmington and Outer Banks",
            "Occasional ice storms affect roofing in Piedmont",
            "Red clay soil movement affects foundations and fencing",
        ),
        project_recommendations=(
            ("Architectural shingle roof", "20-year replacement cycles on suburban stock"),
            ("Heat-pump HVAC", "Handles NC's balanced heating and cooling needs"),
            ("Kitchen &amp; bath remodel", "Move-up demand in Triangle and Charlotte suburbs"),
            ("LVP flooring", "Popular carpet replacement in family neighborhoods"),
        ),
        cost_drivers=(
            "Inland vs. coastal labor and material premiums",
            "Crawl-space duct modifications on older homes",
            "County-by-county permit fee variation",
            "Research Triangle growth keeping remodel demand steady",
        ),
    ),
    "california": LocalSeoBlock(
        labor_lead=(
            "California labor rates are among the highest nationally, with Bay Area and "
            "coastal SoCal at the top. Title 24 energy code and seismic requirements add "
            "compliance cost to virtually every HVAC and structural project."
        ),
        labor_bullets=(
            "Bay Area labor 40%+ above national average",
            "Title 24–certified HVAC installers required for permits",
            "Seismic retrofit specialists essential in SF and LA",
            "Sacramento and inland metros offer relative value vs. coast",
        ),
        permit_lead=(
            "California requires Title 24 energy compliance on HVAC, windows, and many "
            "renovations. Cities and counties issue permits separately — timelines vary "
            "widely from Sacramento (weeks) to San Francisco (months)."
        ),
        permit_bullets=(
            "Title 24 calculations mandatory for mechanical replacements",
            "Solar permit plus utility interconnection (PG&amp;E, SCE, SDG&amp;E, SMUD)",
            "ADU permits include planning, utility, and energy review",
            "Wildfire WUI zones require fire-rated materials in foothill areas",
        ),
        climate_lead="California spans coastal mild, inland heat, and wildfire risk:",
        climate_bullets=(
            "Coastal marine layer vs. inland valley heat — very different HVAC sizing",
            "Wildfire ember zones require fire-rated roofing and vents",
            "Earthquake risk adds seismic scope in Bay Area and LA",
            "Strong solar economics with high utility rates statewide",
        ),
        project_recommendations=(
            ("Title 24–compliant HVAC", "Required for permit — plan for higher equipment tier"),
            ("Solar + battery storage", "High utility rates improve payback statewide"),
            ("Kitchen or ADU remodel", "Strong rental demand in major metros"),
            ("Fire-rated roof upgrade", "WUI zone homes in foothill and canyon areas"),
        ),
        cost_drivers=(
            "Coastal vs. inland labor rate spread (SF vs. Sacramento)",
            "Title 24 and seismic compliance on mechanical work",
            "Permit timeline and fee variation by city",
            "Wildfire-zone material requirements in WUI areas",
        ),
    ),
}


def get_city_local_seo(city_key: str) -> LocalSeoBlock:
    return CITY_LOCAL_SEO.get(city_key, CITY_LOCAL_SEO["dallas"])


def get_state_local_seo(state_slug: str) -> LocalSeoBlock:
    return STATE_LOCAL_SEO.get(state_slug, STATE_LOCAL_SEO["texas"])


def _bullets(items: tuple[str, ...]) -> str:
    return "".join(f"<li>{item}</li>" for item in items)


def _projects_html(
    projects: tuple[tuple[str, str], ...],
    link_fn: callable | None = None,
    trending: list[tuple] | None = None,
) -> str:
    rows = []
    for i, (title, rationale) in enumerate(projects):
        href = "#"
        if trending and i < len(trending):
            href = trending[i][2] if len(trending[i]) > 2 else "#"
        if link_fn and href != "#":
            href = link_fn(href)
        rows.append(
            f"""          <article class="local-seo-project-card">
            <h4>{title}</h4>
            <p>{rationale}</p>
            {f'<a href="{href}" class="card-cta">Estimate cost →</a>' if href != '#' else ''}
          </article>\n"""
        )
    return "".join(rows)


def local_guide_section_html(
    location_name: str,
    block: LocalSeoBlock,
    city_key: str | None = None,
    link_fn: callable | None = None,
    trending: list[tuple] | None = None,
) -> str:
    labor_note = _labor_note(city_key) if city_key else ""
    labor_intro = f"<p>{block.labor_lead}</p>"
    if labor_note:
        labor_intro += f'<p class="local-seo-index-note">{labor_note}</p>'

    return f"""    <section id="local-guide" class="section local-seo-section" aria-labelledby="local-guide-heading">
      <div class="container">
        <header class="section-header section-header--center">
          <h2 id="local-guide-heading">What Shapes Home Project Costs in {location_name}?</h2>
          <p>Local labor, permits, climate, and market conditions — not just different numbers on the same template</p>
        </header>
        <div class="local-seo-grid">
          <article class="local-seo-card" id="local-labor">
            <h3>Local Labor Market</h3>
            {labor_intro}
            <ul class="cost-detail-list">{_bullets(block.labor_bullets)}</ul>
          </article>
          <article class="local-seo-card" id="local-permits">
            <h3>Permits &amp; Inspections</h3>
            <p>{block.permit_lead}</p>
            <ul class="cost-detail-list">{_bullets(block.permit_bullets)}</ul>
          </article>
          <article class="local-seo-card" id="local-climate">
            <h3>Climate &amp; Weather Effects</h3>
            <p>{block.climate_lead}</p>
            <ul class="cost-detail-list">{_bullets(block.climate_bullets)}</ul>
          </article>
          <article class="local-seo-card local-seo-card--wide" id="local-projects">
            <h3>Recommended Projects for {location_name}</h3>
            <p>Projects that match local conditions, housing stock, and typical homeowner priorities:</p>
            <div class="local-seo-project-grid">{_projects_html(block.project_recommendations, link_fn, trending)}            </div>
          </article>
          <article class="local-seo-card" id="local-drivers">
            <h3>Local Cost Drivers</h3>
            <p>Factors that push estimates above or below nearby metros:</p>
            <ul class="cost-detail-list">{_bullets(block.cost_drivers)}</ul>
          </article>
        </div>
      </div>
    </section>
"""


def compact_local_block_html(
    city_name: str,
    state_abbr: str,
    block: LocalSeoBlock,
    city_key: str,
    hub_href: str = "../",
    link_fn: callable | None = None,
    trending: list[tuple] | None = None,
) -> str:
    """Condensed local context for city-scoped calculator pages."""
    labor_note = _labor_note(city_key)
    projects = "".join(
        f"<li><strong>{t}</strong> — {d}</li>"
        for t, d in block.project_recommendations[:3]
    )
    return f"""    <section id="local-context" class="section local-seo-compact" aria-labelledby="local-context-heading">
      <div class="container">
        <header class="section-header">
          <h2 id="local-context-heading">{city_name}, {state_abbr} — Local Cost Context</h2>
          <p class="local-seo-compact-lead">Prices on this page adjust for {city_name}-area labor, permits, and climate — not a generic national template.</p>
        </header>
        <div class="local-seo-compact-grid">
          <article>
            <h3>Labor</h3>
            <p>{block.labor_lead}</p>
            <p class="local-seo-index-note">{labor_note}</p>
          </article>
          <article>
            <h3>Permits</h3>
            <p>{block.permit_lead}</p>
          </article>
          <article>
            <h3>Climate</h3>
            <p>{block.climate_lead}</p>
            <ul>{_bullets(block.climate_bullets[:3])}</ul>
          </article>
          <article>
            <h3>Top local projects</h3>
            <ul>{projects}</ul>
          </article>
        </div>
        <p class="local-seo-compact-footer">See our <a href="{hub_href}#local-guide">full {city_name} cost guide</a> for labor details, permit differences, and local cost drivers.</p>
      </div>
    </section>
"""

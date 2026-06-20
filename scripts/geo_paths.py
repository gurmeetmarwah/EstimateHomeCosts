"""Resolve state/city landing and scoped calculator URLs (no 404 city hubs)."""

from __future__ import annotations

POPULAR_CITY_HUB_SLUGS: dict[str, frozenset[str]] = {
    "texas": frozenset({"dallas", "austin", "houston", "san-antonio", "fort-worth"}),
    "florida": frozenset({"tampa", "orlando", "miami", "jacksonville", "st-petersburg"}),
    "arizona": frozenset({"phoenix", "scottsdale", "mesa", "tucson", "chandler"}),
    "north-carolina": frozenset({"raleigh", "charlotte", "durham", "cary", "wilmington"}),
    "california": frozenset({"san-diego", "los-angeles", "orange-county", "sacramento", "san-francisco"}),
}

# Suburb / metro slug → parent hub slug (must exist in POPULAR_CITY_HUB_SLUGS)
SUBURB_TO_HUB: dict[str, str] = {
    "plano": "dallas",
    "frisco": "dallas",
    "mckinney": "dallas",
    "irving": "dallas",
    "garland": "dallas",
    "arlington": "dallas",
    "richardson": "dallas",
    "round-rock": "austin",
    "cedar-park": "austin",
    "pflugerville": "austin",
    "georgetown": "austin",
    "leander": "austin",
    "kyle": "austin",
    "san-marcos": "austin",
    "the-woodlands": "houston",
    "katy": "houston",
    "sugar-land": "houston",
    "pearland": "houston",
    "league-city": "houston",
    "cypress": "houston",
    "new-braunfels": "san-antonio",
    "schertz": "san-antonio",
    "converse": "san-antonio",
    "boerne": "san-antonio",
    "helotes": "san-antonio",
    "alamo-heights": "san-antonio",
    "keller": "fort-worth",
    "mansfield": "fort-worth",
    "southlake": "fort-worth",
    "burleson": "fort-worth",
    "north-richland-hills": "fort-worth",
    "grapevine": "fort-worth",
    "scottsdale": "scottsdale",
    "mesa": "mesa",
    "chandler": "chandler",
    "tucson": "tucson",
    "gilbert": "chandler",
    "glendale": "phoenix",
    "tempe": "phoenix",
    "peoria": "phoenix",
    "surprise": "phoenix",
    "avondale": "phoenix",
    "goodyear": "phoenix",
    "paradise-valley": "scottsdale",
    "fountain-hills": "scottsdale",
    "cave-creek": "scottsdale",
    "north-scottsdale": "scottsdale",
    "mccormick-ranch": "scottsdale",
    "dc-ranch": "scottsdale",
    "apache-junction": "mesa",
    "queen-creek": "mesa",
    "gold-canyon": "mesa",
    "red-mountain": "mesa",
    "superstition-springs": "mesa",
    "eastmark": "mesa",
    "oro-valley": "tucson",
    "marana": "tucson",
    "sahuarita": "tucson",
    "green-valley": "tucson",
    "catalina-foothills": "tucson",
    "vail": "tucson",
    "sun-lakes": "chandler",
    "ahwatukee": "chandler",
    "ocotillo": "chandler",
    "san-tan-valley": "chandler",
    "chandler-heights": "chandler",
    "st-petersburg": "st-petersburg",
    "clearwater": "st-petersburg",
    "largo": "st-petersburg",
    "pinellas-park": "st-petersburg",
    "gulfport": "st-petersburg",
    "treasure-island": "st-petersburg",
    "seminole": "st-petersburg",
    "brandon": "tampa",
    "riverview": "tampa",
    "wesley-chapel": "tampa",
    "lakeland": "tampa",
    "plant-city": "tampa",
    "kissimmee": "orlando",
    "winter-park": "orlando",
    "sanford": "orlando",
    "lake-nona": "orlando",
    "altamonte-springs": "orlando",
    "oviedo": "orlando",
    "miami-beach": "miami",
    "coral-gables": "miami",
    "hialeah": "miami",
    "fort-lauderdale": "miami",
    "pembroke-pines": "miami",
    "homestead": "miami",
    "jacksonville-beach": "jacksonville",
    "orange-park": "jacksonville",
    "st-augustine": "jacksonville",
    "ponte-vedra": "jacksonville",
    "fernandina-beach": "jacksonville",
    "mandarin": "jacksonville",
    "cary": "cary",
    "apex": "cary",
    "durham": "durham",
    "wake-forest": "raleigh",
    "chapel-hill": "durham",
    "morrisville": "cary",
    "holly-springs": "cary",
    "garner": "raleigh",
    "fuquay-varina": "cary",
    "matthews": "charlotte",
    "huntersville": "charlotte",
    "concord": "charlotte",
    "fort-mill": "charlotte",
    "gastonia": "charlotte",
    "mint-hill": "charlotte",
    "hillsborough": "durham",
    "creedmoor": "durham",
    "roxboro": "durham",
    "butner": "durham",
    "wilmington-beach": "wilmington",
    "wrightsville-beach": "wilmington",
    "carolina-beach": "wilmington",
    "leland": "wilmington",
    "hampstead": "wilmington",
    "ogden": "wilmington",
    "la-jolla": "san-diego",
    "encinitas": "san-diego",
    "carlsbad": "san-diego",
    "chula-vista": "san-diego",
    "oceanside": "san-diego",
    "escondido": "san-diego",
    "pasadena": "los-angeles",
    "burbank": "los-angeles",
    "long-beach": "los-angeles",
    "santa-monica": "los-angeles",
    "torrance": "los-angeles",
    "beverly-hills": "los-angeles",
    "irvine": "orange-county",
    "anaheim": "orange-county",
    "santa-ana": "orange-county",
    "newport-beach": "orange-county",
    "huntington-beach": "orange-county",
    "costa-mesa": "orange-county",
    "elk-grove": "sacramento",
    "roseville": "sacramento",
    "folsom": "sacramento",
    "davis": "sacramento",
    "citrus-heights": "sacramento",
    "rocklin": "sacramento",
    "oakland": "san-francisco",
    "berkeley": "san-francisco",
    "san-jose": "san-francisco",
    "daly-city": "san-francisco",
    "san-mateo": "san-francisco",
    "palo-alto": "san-francisco",
}

SKIP_HREF_PREFIXES = (
    "/css/",
    "/js/",
    "/privacy",
    "/terms",
    "/api/",
    "/locations/",
    "/projects/",
    "/states/",
    "/methodology/",
    "/data-sources/",
    "/compare/",
)

SKIP_HREF_EXACT = {"/", "/#", "/#projects", "/#calculators", "/#locations", "/#comparisons"}


def resolve_city_landing(state_slug: str, city_slug: str) -> str:
    """Hub page, parent hub for suburbs, or state landing."""
    hubs = POPULAR_CITY_HUB_SLUGS.get(state_slug, frozenset())
    if city_slug in hubs:
        return f"/{state_slug}/{city_slug}/"
    parent = SUBURB_TO_HUB.get(city_slug)
    if parent and parent in hubs:
        return f"/{state_slug}/{parent}/"
    return f"/{state_slug}/"


def suburb_calculator_href(
    state_slug: str,
    hub_slug: str,
    suburb_slug: str,
    calc_path: str = "/roof-cost-calculator/",
) -> str:
    """Metro hub calculator with suburb context for city-path.js (?metro=)."""
    base = f"/{state_slug}/{hub_slug}"
    path = calc_path if calc_path.startswith("/") else f"/{calc_path}"
    return f"{base}{path}?metro={suburb_slug}"


def _other_hub_in_path(path: str, state_slug: str, city_slug: str) -> bool:
    parts = [p for p in path.split("/") if p]
    if len(parts) < 2 or parts[0] != state_slug:
        return False
    hubs = POPULAR_CITY_HUB_SLUGS.get(state_slug, frozenset())
    return parts[1] in hubs and parts[1] != city_slug


def city_prefix_path(path: str, state_slug: str, city_slug: str) -> str:
    """Prefix paths for /{state}/{city}/ scoped pages."""
    if not path or path[0] != "/":
        return path
    full = f"/{state_slug}/{city_slug}"
    if path.startswith(full + "/") or path == full or path == full + "/":
        return path
    if path in SKIP_HREF_EXACT or any(path.startswith(p) for p in SKIP_HREF_PREFIXES):
        return path
    if path.startswith("/#") or path.startswith("/compare/"):
        return path
    if _other_hub_in_path(path, state_slug, city_slug):
        return path
    state_prefix = f"/{state_slug}"
    if path.startswith(state_prefix + "/"):
        rest = path[len(state_prefix) :]
        return full + rest
    return full + path


def state_prefix_path(path: str, state_slug: str) -> str:
    """Prefix paths for /{state}/ scoped pages (skip other city hubs)."""
    if not path or path[0] != "/":
        return path
    if path.startswith(f"/{state_slug}/"):
        return path
    hubs = POPULAR_CITY_HUB_SLUGS.get(state_slug, frozenset())
    parts = [p for p in path.split("/") if p]
    if len(parts) >= 2 and parts[0] == state_slug and parts[1] in hubs:
        return path
    if path in SKIP_HREF_EXACT or any(path.startswith(p) for p in SKIP_HREF_PREFIXES):
        return path
    if path.startswith("/#") or path.startswith("/compare/"):
        return path
    return f"/{state_slug}{path}"

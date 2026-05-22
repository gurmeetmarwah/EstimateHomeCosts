"""Resolve state/city landing and scoped calculator URLs (no 404 city hubs)."""

from __future__ import annotations

POPULAR_CITY_HUB_SLUGS: dict[str, frozenset[str]] = {
    "texas": frozenset({"dallas", "austin"}),
    "florida": frozenset({"tampa"}),
    "arizona": frozenset({"phoenix"}),
    "north-carolina": frozenset({"raleigh"}),
    "california": frozenset({"san-diego"}),
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
    "fort-worth": "dallas",
    "round-rock": "austin",
    "cedar-park": "austin",
    "pflugerville": "austin",
    "georgetown": "austin",
    "leander": "austin",
    "kyle": "austin",
    "san-marcos": "austin",
    "scottsdale": "phoenix",
    "mesa": "phoenix",
    "chandler": "phoenix",
    "gilbert": "phoenix",
    "glendale": "phoenix",
    "tempe": "phoenix",
    "tucson": "phoenix",
    "st-petersburg": "tampa",
    "clearwater": "tampa",
    "brandon": "tampa",
    "riverview": "tampa",
    "wesley-chapel": "tampa",
    "lakeland": "tampa",
    "cary": "raleigh",
    "apex": "raleigh",
    "durham": "raleigh",
    "wake-forest": "raleigh",
    "chapel-hill": "raleigh",
    "morrisville": "raleigh",
    "la-jolla": "san-diego",
    "encinitas": "san-diego",
    "carlsbad": "san-diego",
    "chula-vista": "san-diego",
    "oceanside": "san-diego",
    "escondido": "san-diego",
}

SKIP_HREF_PREFIXES = (
    "/css/",
    "/js/",
    "/privacy",
    "/terms",
    "/api/",
    "/locations/",
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

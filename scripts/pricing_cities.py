"""City pricing multipliers — keep in sync with js/calculator-cities.js"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CityPricing:
    label: str
    material: float
    labor: float
    permit: int


CITIES: dict[str, CityPricing] = {
    "national": CityPricing("National average", 1.0, 1.0, 275),
    "texas": CityPricing("Texas average", 0.94, 0.88, 219),
    "dallas": CityPricing("Dallas, TX", 0.93, 0.86, 210),
    "phoenix": CityPricing("Phoenix, AZ", 1.02, 1.05, 248),
    "austin": CityPricing("Austin, TX", 0.97, 0.93, 228),
    "tampa": CityPricing("Tampa, FL", 1.05, 1.03, 288),
    "miami": CityPricing("Miami, FL", 1.12, 1.15, 320),
    "jacksonville": CityPricing("Jacksonville, FL", 0.98, 0.95, 265),
    "st-petersburg": CityPricing("St. Petersburg, FL", 1.04, 1.02, 285),
    "charlotte": CityPricing("Charlotte, NC", 0.95, 0.91, 232),
    "raleigh": CityPricing("Raleigh, NC", 0.96, 0.92, 228),
    "durham": CityPricing("Durham, NC", 0.95, 0.91, 225),
    "cary": CityPricing("Cary, NC", 0.98, 0.94, 235),
    "wilmington": CityPricing("Wilmington, NC", 1.0, 0.96, 245),
    "scottsdale": CityPricing("Scottsdale, AZ", 1.1, 1.14, 268),
    "mesa": CityPricing("Mesa, AZ", 1.0, 1.02, 240),
    "tucson": CityPricing("Tucson, AZ", 0.96, 0.94, 230),
    "chandler": CityPricing("Chandler, AZ", 1.03, 1.04, 250),
    "houston": CityPricing("Houston, TX", 0.91, 0.84, 218),
    "san-antonio": CityPricing("San Antonio, TX", 0.9, 0.82, 205),
    "fort-worth": CityPricing("Fort Worth, TX", 0.92, 0.85, 208),
    "orlando": CityPricing("Orlando, FL", 1.03, 1.01, 278),
    "san-diego": CityPricing("San Diego, CA", 1.24, 1.28, 395),
    "los-angeles": CityPricing("Los Angeles, CA", 1.32, 1.35, 420),
    "orange-county": CityPricing("Orange County, CA", 1.28, 1.32, 410),
    "sacramento": CityPricing("Sacramento, CA", 1.12, 1.14, 360),
    "san-francisco": CityPricing("San Francisco, CA", 1.38, 1.42, 480),
}

STATE_DEFAULT_CITY = {
    "texas": "texas",
    "florida": "tampa",
    "arizona": "phoenix",
    "north-carolina": "raleigh",
    "california": "san-diego",
}

GUIDE_STATE_MULT = {
    "national": 1.0,
    "tx": 0.94,
    "fl": 1.02,
    "ca": 1.28,
    "az": 1.0,
    "nc": 0.96,
}

STATE_LOCATION_KEY = {
    "texas": "tx",
    "florida": "fl",
    "arizona": "az",
    "north-carolina": "nc",
    "california": "ca",
}


def get_city(key: str) -> CityPricing:
    return CITIES.get(key, CITIES["national"])


def loc_mult(city: CityPricing) -> float:
    return (city.material + city.labor) / 2


def guide_loc_mult(key: str) -> float:
    city = CITIES.get(key)
    if city:
        return loc_mult(city)
    return GUIDE_STATE_MULT.get(key, 1.0)

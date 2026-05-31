"""Mirror JS calculator formulas for city/state page figures."""

from __future__ import annotations

import math
import re

from pricing_cities import CITIES, CityPricing, get_city, guide_loc_mult, loc_mult

# --- formatting ---


def fmt_money(n: float) -> str:
    return f"${round(n):,}"


def fmt_range(low: float, high: float) -> str:
    return f"{fmt_money(low)}–{fmt_money(high)}"


def fmt_compact(n: float) -> str:
    if n >= 1000:
        k = n / 1000
        if k >= 10:
            return f"${round(k)}k"
        return f"${k:.1f}k".replace(".0k", "k")
    return fmt_money(n)


def fmt_compact_range(low: float, high: float) -> str:
    return f"{fmt_compact(low)}–{fmt_compact(high)}"


def fmt_per_sqft(low: float, high: float) -> str:
    return f"${low:.0f}–${high:.0f}/sq ft"


def fmt_per_ft(low: float, high: float) -> str:
    return f"${low:.0f}–${high:.0f}/linear ft"


# --- calculators (match js/*-calculator.js) ---


def roof(city_key: str, *, sqft: int = 2000, material: str = "asphalt-arch") -> tuple[float, float]:
    material_rates = {
        "asphalt-arch": (2.35, 2.45),
        "tile": (5.5, 4.2),
    }
    mat, lab = material_rates.get(material, material_rates["asphalt-arch"])
    city = get_city(city_key)
    material_cost = sqft * mat * city.material
    labor_cost = sqft * lab * city.labor
    tearoff = sqft * 0.85 * city.labor
    subtotal = material_cost + labor_cost + tearoff + city.permit
    total = subtotal * 1.05
    return total * 0.9, total * 1.1


def hvac(city_key: str, *, sqft: int = 2200, system: str = "central-ac") -> tuple[float, float]:
    rates = {
        "central-ac": 4.05,
        "heat-pump": 4.65,
        "mini-split": 5.35,
    }
    rate = rates.get(system, 4.05)
    city = get_city(city_key)
    mult = loc_mult(city)
    total = sqft * rate * 1.14 * mult + city.permit
    return total * 0.92, total * 1.08


def kitchen(city_key: str, *, size: str = "medium", remodel: str = "mid") -> tuple[float, float]:
    size_mid = {"small": 28000, "medium": 42500, "large": 62000}[size]
    remodel_mult = {"cosmetic": 0.72, "mid": 1.0, "high-end": 1.38}[remodel]
    mid = size_mid * remodel_mult * guide_loc_mult(city_key)
    return mid * 0.86, mid * 1.14


def bathroom(city_key: str, *, size: str = "full-bath", style: str = "mid") -> tuple[float, float]:
    size_mid = {"half-bath": 14000, "full-bath": 28000, "master": 42000}[size]
    style_mult = {"basic": 0.82, "mid": 1.0, "luxury": 1.48}[style]
    mid = size_mid * style_mult * guide_loc_mult(city_key)
    return mid * 0.88, mid * 1.12


def flooring(city_key: str, *, sqft: int = 500, material: str = "lvp") -> tuple[float, float]:
    mats = {"lvp": (3.2, 2.8), "hardwood": (6.5, 4.5), "tile": (5.5, 4.2)}
    mat, lab = mats.get(material, mats["lvp"])
    city = get_city(city_key)
    mult = loc_mult(city)
    total = sqft * (mat + lab) * 1.06 * mult
    return total * 0.9, total * 1.1


def fence(city_key: str, *, linear_ft: int = 150, material: str = "wood") -> tuple[float, float]:
    rates = {"wood": 28, "vinyl": 32, "composite": 38}
    rate = rates.get(material, 28)
    city = get_city(city_key)
    mult = loc_mult(city)
    permits = round(city.permit * (125 / 275))
    total = linear_ft * rate * mult + permits
    return total * 0.9, total * 1.1


def solar(city_key: str, *, kw: float = 8.0, battery: bool = False) -> tuple[float, float]:
    cost_per_watt = {
        "national": 2.85,
        "dallas": 2.65,
        "phoenix": 2.72,
        "austin": 2.68,
        "tampa": 2.78,
        "miami": 2.92,
        "jacksonville": 2.76,
        "st-petersburg": 2.80,
        "charlotte": 2.74,
        "raleigh": 2.72,
        "durham": 2.71,
        "cary": 2.73,
        "wilmington": 2.78,
        "scottsdale": 2.88,
        "mesa": 2.74,
        "tucson": 2.68,
        "chandler": 2.76,
        "houston": 2.62,
        "san-antonio": 2.58,
        "fort-worth": 2.64,
        "orlando": 2.76,
        "san-diego": 3.15,
        "los-angeles": 3.28,
        "orange-county": 3.22,
        "sacramento": 2.98,
        "san-francisco": 3.38,
    }
    city = get_city(city_key)
    mult = loc_mult(city)
    per_watt = cost_per_watt.get(city_key, cost_per_watt["national"])
    base = kw * 1000 * per_watt * mult
    batt = (10500 + kw * 180) * mult if battery else 0
    total = base + batt
    return total * 0.9, total * 1.1


def example_mid(city_key: str, href: str, detail: str) -> int:
    detail_l = detail.lower()
    href_l = href.lower()
    if "mini-split" in href_l or "mini-split" in detail_l:
        lo, hi = hvac(city_key, system="mini-split")
    elif "heat pump" in detail_l or "heat-pump" in href_l:
        lo, hi = hvac(city_key, system="heat-pump")
    elif "hvac" in href_l or "central ac" in detail_l:
        lo, hi = hvac(city_key)
    elif "kitchen" in href_l or "kitchen" in detail_l:
        if "refresh" in detail_l or "cosmetic" in detail_l:
            lo, hi = kitchen(city_key, size="small", remodel="cosmetic")
        elif "luxury" in detail_l or "open concept" in detail_l:
            lo, hi = kitchen(city_key, size="medium", remodel="high-end")
        else:
            lo, hi = kitchen(city_key, remodel="mid")
    elif "bathroom" in href_l or "bath" in detail_l or "shower" in detail_l:
        style = "luxury" if "spa" in detail_l or "walk-in" in detail_l or "moisture-rated" in detail_l else "mid"
        lo, hi = bathroom(city_key, style=style)
    elif "solar" in href_l or "solar" in detail_l:
        battery = "battery" in detail_l or "powerwall" in detail_l
        kw = 7.0 if "7 kw" in detail_l else 8.0
        lo, hi = solar(city_key, kw=kw, battery=battery)
    elif "fence" in href_l or "fence" in detail_l:
        ft = 160 if "160" in detail_l else 150
        lo, hi = fence(city_key, linear_ft=ft)
    elif "flooring" in href_l or "lvp" in detail_l or "flooring" in detail_l:
        sqft = 1400 if "1,400" in detail or "1400" in detail else 500
        lo, hi = flooring(city_key, sqft=sqft)
    elif "tile roof" in detail_l or ("tile" in detail_l and "roof" in detail_l):
        lo, hi = roof(city_key, material="tile")
    else:
        lo, hi = roof(city_key)
    return round((lo + hi) / 2)


def city_snapshots(city_key: str) -> list[dict]:
    r_lo, r_hi = roof(city_key)
    b_lo, b_hi = bathroom(city_key)
    h_lo, h_hi = hvac(city_key)
    f_lo, f_hi = flooring(city_key)
    fn_lo, fn_hi = fence(city_key)
    s_lo, s_hi = solar(city_key)
    fl_lo, fl_hi = f_lo / 500, f_hi / 500
    fnp_lo, fnp_hi = fn_lo / 150, fn_hi / 150
    return [
        {"icon": "roof", "category": "Roofing", "title": "Roof Replacement", "range": fmt_compact_range(r_lo, r_hi), "href": "/roof-cost-calculator/"},
        {"icon": "bath", "category": "Bathroom Remodel", "title": "Bathroom Remodel", "range": fmt_compact_range(b_lo, b_hi), "href": "/cost/bathroom-remodel/"},
        {"icon": "hvac", "category": "HVAC", "title": "Central AC Installation", "range": fmt_compact_range(h_lo, h_hi), "href": "/hvac-cost-calculator/"},
        {"icon": "floor", "category": "Flooring", "title": "Flooring Installation", "range": fmt_per_sqft(fl_lo, fl_hi), "href": "/flooring-cost-calculator/"},
        {"icon": "fence", "category": "Fence", "title": "Wood Privacy Fence", "range": fmt_per_ft(fnp_lo, fnp_hi), "href": "/fence-materials/wood-privacy-fence-cost/"},
        {"icon": "solar", "category": "Solar", "title": "Solar Panels", "range": fmt_compact_range(s_lo, s_hi), "href": "/solar-panel-cost-calculator/"},
    ]


def city_faq_ranges(city_key: str) -> dict[str, str]:
    b_lo, b_hi = bathroom(city_key, style="basic")
    b_hi2, _ = bathroom(city_key, style="luxury")
    k_lo, k_hi = kitchen(city_key, size="small", remodel="cosmetic")
    _, k_hi2 = kitchen(city_key, size="large", remodel="high-end")
    r_lo, r_hi = roof(city_key)
    s_lo, s_hi = solar(city_key, kw=6)
    _, s_hi2 = solar(city_key, kw=12, battery=True)
    return {
        "renovation": fmt_compact_range(min(b_lo, k_lo, r_lo), max(b_hi2, k_hi2, s_hi2)),
        "bathroom": fmt_compact_range(b_lo, b_hi2),
        "kitchen": fmt_compact_range(k_lo, k_hi2),
        "roofing": fmt_compact_range(r_lo, r_hi),
        "solar": fmt_compact_range(s_lo, s_hi2),
    }


PERMIT_FAQ = {
    "texas": "Full <strong>roof replacements</strong>, <strong>HVAC changeouts</strong>, and many <strong>electrical upgrades</strong> require city permits across Texas metros — fees vary by jurisdiction and project scope.",
    "florida": "Coastal counties often require <strong>wind-rated roofing</strong>, <strong>HVAC permits</strong>, and <strong>electrical inspections</strong> for solar. Miami-Dade and Tampa Bay have stricter wind codes.",
    "arizona": "Maricopa and Pima counties require permits for <strong>roof replacements</strong>, <strong>HVAC installations</strong>, and <strong>solar interconnects</strong>. HOA review is common in master-planned communities.",
    "north-carolina": "Wake, Mecklenburg, and coastal counties require permits for <strong>roof replacements</strong>, <strong>HVAC changeouts</strong>, and <strong>structural remodels</strong>. Fees are moderate vs. coastal CA metros.",
    "california": "California requires <strong>Title 24–compliant HVAC</strong>, <strong>roof permits</strong>, and <strong>solar interconnection</strong> approvals. Permit costs run higher than most U.S. metros.",
}

ROOFING_FAQ = {
    "texas": "<strong>Architectural asphalt shingles</strong> are most common. <strong>Impact-resistant (Class 4)</strong> shingles are popular after hail. <strong>Metal roofing</strong> is growing in suburban new builds.",
    "florida": "<strong>Architectural shingles</strong> and <strong>tile</strong> are common near the coast. <strong>Wind-rated systems</strong> and hurricane nailing patterns are required in many counties.",
    "arizona": "<strong>Tile</strong> and <strong>cool-roof asphalt</strong> dominate Phoenix-area homes. <strong>Metal roofing</strong> is popular in Scottsdale and newer subdivisions.",
    "north-carolina": "<strong>Architectural asphalt shingles</strong> are standard. <strong>Impact-resistant shingles</strong> help in storm-prone areas. <strong>Metal accents</strong> appear on newer builds.",
    "california": "<strong>Composition and tile</strong> are common. Coastal wind ratings and <strong>wildfire ember zones</strong> influence material and vent choices inland.",
}

SOLAR_FAQ = {
    "california": "Often yes with strong sun and time-of-use rates. California has among the highest electricity costs — see our <a href=\"{solar_href}\">solar calculator</a> and the <strong>30% federal tax credit</strong>.",
    "texas": "Often yes with long sunny seasons and rising utility rates. See our <a href=\"{solar_href}\">solar calculator</a> and the <strong>30% federal tax credit</strong>.",
    "florida": "Often yes with year-round sun, though humidity and storm exposure affect roof condition. See our <a href=\"{solar_href}\">solar calculator</a> and the <strong>30% federal tax credit</strong>.",
    "arizona": "Among the best solar markets in the U.S. with high sun exposure. See our <a href=\"{solar_href}\">solar calculator</a> and the <strong>30% federal tax credit</strong>.",
    "north-carolina": "Solid economics with moderate sun and competitive install costs. See our <a href=\"{solar_href}\">solar calculator</a> and the <strong>30% federal tax credit</strong>.",
}


def parse_example_cost(cost_str: str) -> int | None:
    m = re.search(r"\$([\d,]+)", cost_str)
    return int(m.group(1).replace(",", "")) if m else None

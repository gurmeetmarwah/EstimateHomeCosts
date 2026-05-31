/**
 * Shared city list & multipliers for Estimate Home Costs cost calculators
 */
(function (global) {
  'use strict';

  const CITIES = {
    national: { label: 'National average', material: 1, labor: 1, permit: 275 },
    texas: { label: 'Texas average', material: 0.94, labor: 0.88, permit: 219 },
    dallas: { label: 'Dallas, TX', material: 0.93, labor: 0.86, permit: 210 },
    phoenix: { label: 'Phoenix, AZ', material: 1.02, labor: 1.05, permit: 248 },
    austin: { label: 'Austin, TX', material: 0.97, labor: 0.93, permit: 228 },
    tampa: { label: 'Tampa, FL', material: 1.05, labor: 1.03, permit: 288 },
    miami: { label: 'Miami, FL', material: 1.12, labor: 1.15, permit: 320 },
    jacksonville: { label: 'Jacksonville, FL', material: 0.98, labor: 0.95, permit: 265 },
    'st-petersburg': { label: 'St. Petersburg, FL', material: 1.04, labor: 1.02, permit: 285 },
    charlotte: { label: 'Charlotte, NC', material: 0.95, labor: 0.91, permit: 232 },
    raleigh: { label: 'Raleigh, NC', material: 0.96, labor: 0.92, permit: 228 },
    durham: { label: 'Durham, NC', material: 0.95, labor: 0.91, permit: 225 },
    cary: { label: 'Cary, NC', material: 0.98, labor: 0.94, permit: 235 },
    wilmington: { label: 'Wilmington, NC', material: 1.0, labor: 0.96, permit: 245 },
    scottsdale: { label: 'Scottsdale, AZ', material: 1.1, labor: 1.14, permit: 268 },
    mesa: { label: 'Mesa, AZ', material: 1.0, labor: 1.02, permit: 240 },
    tucson: { label: 'Tucson, AZ', material: 0.96, labor: 0.94, permit: 230 },
    chandler: { label: 'Chandler, AZ', material: 1.03, labor: 1.04, permit: 250 },
    houston: { label: 'Houston, TX', material: 0.91, labor: 0.84, permit: 218 },
    'san-antonio': { label: 'San Antonio, TX', material: 0.9, labor: 0.82, permit: 205 },
    'fort-worth': { label: 'Fort Worth, TX', material: 0.92, labor: 0.85, permit: 208 },
    orlando: { label: 'Orlando, FL', material: 1.03, labor: 1.01, permit: 278 },
    'san-diego': { label: 'San Diego, CA', material: 1.24, labor: 1.28, permit: 395 },
    'los-angeles': { label: 'Los Angeles, CA', material: 1.32, labor: 1.35, permit: 420 },
    'orange-county': { label: 'Orange County, CA', material: 1.28, labor: 1.32, permit: 410 },
    sacramento: { label: 'Sacramento, CA', material: 1.12, labor: 1.14, permit: 360 },
    'san-francisco': { label: 'San Francisco, CA', material: 1.38, labor: 1.42, permit: 480 },
  };

  const GUIDE_STATE_MULT = {
    national: 1,
    tx: 0.94,
    fl: 1.02,
    ca: 1.28,
    az: 1,
    nc: 0.96,
    ny: 1.22,
    ga: 0.98,
    co: 1.05,
    il: 1.04,
  };

  const GUIDE_STATE_LABELS = {
    national: 'National average',
    tx: 'Texas average',
    fl: 'Florida average',
    ca: 'California average',
    az: 'Arizona average',
    nc: 'North Carolina average',
    ny: 'New York average',
    ga: 'Georgia average',
    co: 'Colorado average',
    il: 'Illinois average',
  };

  const GUIDE_PERMIT_STATE_MULT = {
    national: 1,
    tx: 0.85,
    fl: 1.1,
    ca: 1.45,
    ga: 0.95,
    az: 0.9,
    nc: 0.88,
    co: 1,
    il: 1.05,
    ny: 1.35,
  };

  function getGuideLocationMult(key) {
    const city = CITIES[key];
    if (city) return locMult(city);
    return GUIDE_STATE_MULT[key] ?? 1;
  }

  function getGuideLocationLabel(key) {
    const city = CITIES[key];
    if (city) return city.label;
    return GUIDE_STATE_LABELS[key] ?? 'National average';
  }

  function getGuidePermitMult(key, nationalPermit = 275) {
    const city = CITIES[key];
    if (city) return city.permit / nationalPermit;
    return GUIDE_PERMIT_STATE_MULT[key] ?? 1;
  }

  function getCity(key) {
    return CITIES[key] || CITIES.national;
  }

  /** Blended material + labor multiplier vs national baseline */
  function locMult(city) {
    return (city.material + city.labor) / 2;
  }

  function getScopedCityKey() {
    const scope = window.EHCCityPath?.parseScope?.() || window.EHCCityPath?.parseCityScope?.();
    return scope?.cityKey || null;
  }

  function getCityValue(el) {
    const v = el?.value;
    if (v && CITIES[v] && v !== 'national') return v;
    const scoped = getScopedCityKey();
    if (scoped && CITIES[scoped]) return scoped;
    return v && CITIES[v] ? v : 'national';
  }

  global.EHCCities = {
    CITIES,
    getCity,
    getCityValue,
    getScopedCityKey,
    locMult,
    getGuideLocationMult,
    getGuideLocationLabel,
    getGuidePermitMult,
  };
})(typeof window !== 'undefined' ? window : global);

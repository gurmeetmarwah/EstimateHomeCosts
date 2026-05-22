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
    charlotte: { label: 'Charlotte, NC', material: 0.95, labor: 0.91, permit: 232 },
    raleigh: { label: 'Raleigh, NC', material: 0.96, labor: 0.92, permit: 228 },
    scottsdale: { label: 'Scottsdale, AZ', material: 1.1, labor: 1.14, permit: 268 },
    houston: { label: 'Houston, TX', material: 0.91, labor: 0.84, permit: 218 },
    orlando: { label: 'Orlando, FL', material: 1.03, labor: 1.01, permit: 278 },
    'san-diego': { label: 'San Diego, CA', material: 1.24, labor: 1.28, permit: 395 },
  };

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
  };
})(typeof window !== 'undefined' ? window : global);

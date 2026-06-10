/**
 * HVAC installation cost calculator — 2026 national & regional estimates
 */
(function () {
  'use strict';

  const SYSTEM_RATES = {
    'central-ac': { rate: 4.05, label: 'Central AC' },
    'heat-pump': { rate: 4.65, label: 'Heat Pump' },
    'mini-split': { rate: 5.35, label: 'Ductless Mini Split' },
    'furnace-ac': { rate: 5.75, label: 'Furnace + AC Combo' },
    geothermal: { rate: 9.25, label: 'Geothermal' },
  };

  const EFFICIENCY_MULT = {
    standard: 1,
    high: 1.14,
    premium: 1.28,
  };

  const LOCATION_MULT = {
    national: 1,
    tx: 0.96,
    fl: 1.05,
    ca: 1.22,
    ga: 0.98,
    az: 1.02,
    nc: 0.97,
    co: 1.06,
    il: 1.04,
    ny: 1.18,
  };

  const LOCATION_LABELS = {
    national: 'National average',
    tx: 'Texas average',
    fl: 'Florida average',
    az: 'Arizona average',
    nc: 'North Carolina average',
    ca: 'California average',
    fl: 'Florida',
    ca: 'California',
    ga: 'Georgia',
    az: 'Arizona',
    nc: 'North Carolina',
    co: 'Colorado',
    il: 'Illinois',
    ny: 'New York',
  };

  const DUCTWORK_BASE = 2800;
  const PERMIT_BASE = 275;
  const PERMIT_MULT = {
    national: 1,
    tx: 0.9,
    fl: 1.1,
    ca: 1.4,
    ga: 0.95,
    az: 0.92,
    nc: 0.88,
    co: 1,
    il: 1.05,
    ny: 1.3,
  };

  const form = document.getElementById('hvac-calculator');
  if (!form) return;

  const els = {
    size: document.getElementById('hvac-size'),
    system: document.getElementById('hvac-system'),
    efficiency: document.getElementById('hvac-efficiency'),
    location: document.getElementById('hvac-location'),
    total: document.getElementById('calc-total'),
    range: document.getElementById('calc-range'),
    equipment: document.getElementById('calc-equipment'),
    duct: document.getElementById('calc-duct'),
    permits: document.getElementById('calc-permits'),
    perSqft: document.getElementById('calc-per-sqft'),
    ductRow: document.querySelector('#calc-breakdown .calc-row-duct'),
  };

  function formatMoney(n) {
    return '$' + Math.round(n).toLocaleString('en-US');
  }

  function formatRange(low, high) {
    return `${formatMoney(low)}–${formatMoney(high)}`;
  }

  function getLocMult(locKey) {
    return window.EHCCities?.getGuideLocationMult?.(locKey) ?? LOCATION_MULT[locKey] ?? 1;
  }

  function getLocLabel(locKey) {
    return window.EHCCities?.getGuideLocationLabel?.(locKey) ?? LOCATION_LABELS[locKey] ?? 'National average';
  }

  function getPermitMult(locKey) {
    return window.EHCCities?.getGuidePermitMult?.(locKey, PERMIT_BASE) ?? PERMIT_MULT[locKey] ?? 1;
  }

  function compute() {
    const sqft = Math.max(800, Math.min(8000, Number(els.size.value) || 2000));
    const systemKey = els.system.value;
    const system = SYSTEM_RATES[systemKey] || SYSTEM_RATES['central-ac'];
    const effMult = EFFICIENCY_MULT[els.efficiency.value] || 1;
    const locKey = els.location.value || 'national';
    const locMult = getLocMult(locKey);
    const ductEl = form.querySelector('[name="ductwork"]:checked');
    const ductwork = ductEl?.value === 'yes';

    const sizeFactor = sqft / 2000;
    const equipmentLabor = sqft * system.rate * effMult * locMult;
    const ductCost = ductwork ? DUCTWORK_BASE * sizeFactor * locMult : 0;
    const permitCost = PERMIT_BASE * getPermitMult(locKey);
    const mid = equipmentLabor + ductCost + permitCost;
    const low = mid * 0.92;
    const high = mid * 1.08;

    return {
      low,
      high,
      mid,
      equipmentLabor,
      ductCost,
      permitCost,
      perSqftLow: low / sqft,
      perSqftHigh: high / sqft,
      locLabel: getLocLabel(locKey),
    };
  }

  function update() {
    const r = compute();
    els.total.textContent = formatRange(r.low, r.high);
    els.range.textContent = `Typical range for ${r.locLabel}`;
    els.equipment.textContent = formatMoney(r.equipmentLabor);
    els.duct.textContent = r.ductCost > 0 ? formatMoney(r.ductCost) : '$0';
    els.permits.textContent = formatMoney(r.permitCost);
    els.perSqft.textContent = `$${r.perSqftLow.toFixed(2)}–$${r.perSqftHigh.toFixed(2)} per sq ft`;
    if (els.ductRow) {
      els.ductRow.style.opacity = r.ductCost > 0 ? '1' : '0.45';
    }
  }

  ['input', 'change'].forEach((evt) => form.addEventListener(evt, update));
  update();

  const STATE_LOC = { texas: 'tx', florida: 'fl', arizona: 'az', 'north-carolina': 'nc', california: 'ca' };

  function applyGeoLocationDefault() {
    const scope = window.EHC_CITY_SCOPE;
    if (!scope || !els.location) return;
    if (scope.scope === 'state') {
      const loc = STATE_LOC[scope.stateSlug];
      if (loc && els.location.querySelector(`option[value="${loc}"]`)) {
        els.location.value = loc;
        update();
      }
      return;
    }
    if (scope.scope === 'city' && els.location.querySelector(`option[value="${scope.cityKey}"]`)) {
      els.location.value = scope.cityKey;
      update();
    }
  }

  window.addEventListener('ehc:city-scope', applyGeoLocationDefault);
  applyGeoLocationDefault();

})();

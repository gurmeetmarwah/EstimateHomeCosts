/**
 * Kitchen remodel cost calculator — 2026 national estimates
 */
(function () {
  'use strict';

  const SIZE_BASE = {
    small: { mid: 28000, label: 'Small kitchen (under 120 sq ft)' },
    medium: { mid: 42500, label: 'Medium kitchen (120–180 sq ft)' },
    large: { mid: 62000, label: 'Large kitchen (180+ sq ft)' },
  };

  const REMODEL_MULT = { cosmetic: 0.72, mid: 1, 'high-end': 1.38, luxury: 1.72 };
  const CABINET_MULT = { stock: 0.88, 'semi-custom': 1, custom: 1.32 };
  const COUNTERTOP_MULT = { laminate: 0.9, quartz: 1, granite: 1.06, marble: 1.2 };
  const APPLIANCE_MULT = { yes: 1.14, no: 0.9 };
  const LAYOUT_MULT = { yes: 1.24, no: 1 };

  const LOCATION_MULT = {
    national: 1,
    tx: 0.94,
    fl: 1.02,
    ca: 1.28,
    az: 1,
    nc: 0.96,
    ny: 1.22,
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
    az: 'Arizona',
    nc: 'North Carolina',
    ny: 'New York',
  };

  const form = document.getElementById('kitchen-calculator');
  if (!form) return;

  const els = {
    size: document.getElementById('kitchen-size'),
    remodel: document.getElementById('kitchen-remodel-type'),
    cabinets: document.getElementById('kitchen-cabinets'),
    countertop: document.getElementById('kitchen-countertop'),
    location: document.getElementById('kitchen-location'),
    zip: document.getElementById('kitchen-zip'),
    total: document.getElementById('calc-total'),
    range: document.getElementById('calc-range'),
    labor: document.getElementById('calc-labor'),
    materials: document.getElementById('calc-materials'),
    permits: document.getElementById('calc-permits'),
    layoutLine: document.getElementById('calc-layout'),
    layoutRow: document.querySelector('.calc-row-layout'),
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

  function compute() {
    const size = SIZE_BASE[els.size.value] || SIZE_BASE.medium;
    const locKey = els.location.value || 'national';
    const locMult = getLocMult(locKey);
    const appliances = form.querySelector('[name="appliances"]:checked')?.value || 'yes';
    const layoutYes = form.querySelector('[name="layout"]:checked')?.value === 'yes';

    let mid =
      size.mid *
      (REMODEL_MULT[els.remodel.value] || 1) *
      (CABINET_MULT[els.cabinets.value] || 1) *
      (COUNTERTOP_MULT[els.countertop.value] || 1) *
      (APPLIANCE_MULT[appliances] || 1) *
      (layoutYes ? LAYOUT_MULT.yes : LAYOUT_MULT.no) *
      locMult;

    const low = mid * 0.86;
    const high = mid * 1.14;
    const materials = mid * 0.52;
    const labor = mid * 0.38;
    const permits = 650 * locMult;
    const layoutPremium = layoutYes ? mid * 0.14 : 0;

    return {
      low,
      high,
      mid,
      materials,
      labor,
      permits,
      layoutPremium,
      locLabel: getLocLabel(locKey),
    };
  }

  function update() {
    const r = compute();
    els.total.textContent = formatRange(r.low, r.high);
    els.range.textContent = `Typical range for ${r.locLabel}`;
    els.materials.textContent = formatMoney(r.materials);
    els.labor.textContent = formatMoney(r.labor);
    els.permits.textContent = formatMoney(r.permits);
    if (els.layoutLine) {
      els.layoutLine.textContent = r.layoutPremium > 0 ? formatMoney(r.layoutPremium) : '$0';
      if (els.layoutRow) els.layoutRow.style.opacity = r.layoutPremium > 0 ? '1' : '0.45';
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

/**
 * Modern bathroom remodel cost calculator — 2026 national estimates
 */
(function () {
  'use strict';

  const SIZE_BASE = {
    'half-bath': { mid: 14000, label: 'Half bath' },
    'full-bath': { mid: 28000, label: 'Full bath' },
    master: { mid: 42000, label: 'Master bath' },
  };

  const STYLE_MULT = { basic: 0.82, mid: 1, luxury: 1.48 };
  const SHOWER_MULT = { combo: 0.92, framed: 1, frameless: 1.18 };
  const VANITY_MULT = { standard: 1, floating: 1.12 };
  const TILE_MULT = { standard: 0.94, premium: 1.08, stone: 1.32 };
  const LAYOUT_MULT = { no: 1, yes: 1.28 };

  const LOCATION_MULT = {
    national: 1,
    tx: 0.94,
    fl: 1.02,
    ca: 1.26,
    ga: 0.98,
    az: 1,
    nc: 0.96,
    co: 1.05,
    il: 1.04,
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
    ga: 'Georgia',
    az: 'Arizona',
    nc: 'North Carolina',
    co: 'Colorado',
    il: 'Illinois',
    ny: 'New York',
  };

  const form = document.getElementById('bathroom-calculator');
  if (!form) return;

  const els = {
    size: document.getElementById('bath-size'),
    style: document.getElementById('bath-style'),
    shower: document.getElementById('bath-shower'),
    vanity: document.getElementById('bath-vanity'),
    tile: document.getElementById('bath-tile'),
    location: document.getElementById('bath-location'),
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

  function compute() {
    const sizeKey = els.size.value;
    const size = SIZE_BASE[sizeKey] || SIZE_BASE['full-bath'];
    const locKey = els.location.value || 'national';
    const locMult = LOCATION_MULT[locKey] || 1;
    const layoutEl = form.querySelector('[name="layout"]:checked');
    const layoutYes = layoutEl?.value === 'yes';

    let mid =
      size.mid *
      (STYLE_MULT[els.style.value] || 1) *
      (SHOWER_MULT[els.shower.value] || 1) *
      (VANITY_MULT[els.vanity.value] || 1) *
      (TILE_MULT[els.tile.value] || 1) *
      (layoutYes ? LAYOUT_MULT.yes : LAYOUT_MULT.no) *
      locMult;

    const low = mid * 0.88;
    const high = mid * 1.12;
    const materials = mid * 0.42;
    const labor = mid * 0.48;
    const permits = 450 * locMult;
    const layoutPremium = layoutYes ? mid * 0.12 : 0;

    return { low, high, mid, materials, labor, permits, layoutPremium, locLabel: LOCATION_LABELS[locKey] || 'National average' };
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

  function applyStateLocationDefault() {
    const scope = window.EHC_CITY_SCOPE;
    if (!scope || scope.scope !== 'state' || !els.location) return;
    const loc = STATE_LOC[scope.stateSlug];
    if (loc && els.location.querySelector(`option[value="${loc}"]`)) {
      els.location.value = loc;
      update();
    }
  }

  window.addEventListener('ehc:city-scope', applyStateLocationDefault);
  applyStateLocationDefault();

  const stickyCta = document.querySelector('.sticky-cta');
  const ctaSection = document.getElementById('contractor-cta');
  if (stickyCta && ctaSection) {
    const observer = new IntersectionObserver(
      ([entry]) => stickyCta.classList.toggle('is-visible', !entry.isIntersecting),
      { threshold: 0, rootMargin: '0px 0px -60px 0px' }
    );
    observer.observe(ctaSection);
  }
})();

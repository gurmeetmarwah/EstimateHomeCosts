/**
 * Roof replacement cost calculator — 2026 national & regional estimates
 */
(function () {
  'use strict';

  const MATERIAL_RATES = {
    'asphalt-3tab': { material: 1.85, labor: 2.1, label: '3-tab asphalt' },
    'asphalt-arch': { material: 2.35, labor: 2.45, label: 'Architectural asphalt' },
    metal: { material: 4.2, labor: 3.8, label: 'Standing seam metal' },
    tile: { material: 5.5, labor: 4.2, label: 'Clay / concrete tile' },
    wood: { material: 3.8, labor: 3.4, label: 'Wood shake' },
    slate: { material: 8.5, labor: 5.5, label: 'Natural slate' },
  };

  const SLOPE_MULT = {
    low: 0.92,
    moderate: 1,
    steep: 1.18,
    'very-steep': 1.35,
  };

  const LOCATION_MULT = {
    national: 1,
    tx: 0.92,
    fl: 1.05,
    ca: 1.28,
    ga: 0.98,
    az: 1.02,
    nc: 0.96,
    co: 1.08,
    il: 1.06,
    ny: 1.22,
  };

  const TEAROFF_PER_SQFT = 0.85;
  const PERMIT_BASE = 275;
  const PERMIT_MULT = { national: 1, tx: 0.85, fl: 1.1, ca: 1.45, ga: 0.95, az: 0.9, nc: 0.88, co: 1, il: 1.05, ny: 1.35 };

  const form = document.getElementById('roof-calculator');
  if (!form) return;

  const els = {
    size: document.getElementById('roof-size'),
    material: document.getElementById('roof-material'),
    slope: document.getElementById('roof-slope'),
    location: document.getElementById('roof-location'),
    tearoff: document.getElementById('include-tearoff'),
    total: document.getElementById('calc-total'),
    range: document.getElementById('calc-range'),
    materials: document.getElementById('calc-materials'),
    labor: document.getElementById('calc-labor'),
    permits: document.getElementById('calc-permits'),
    tearoffLine: document.getElementById('calc-tearoff'),
    perSqft: document.getElementById('calc-per-sqft'),
    tearoffRow: document.querySelector('#calc-breakdown li:last-child'),
  };

  function formatMoney(n) {
    return '$' + Math.round(n).toLocaleString('en-US');
  }

  function calculate() {
    const sqft = Math.max(500, Math.min(10000, Number(els.size.value) || 2000));
    const matKey = els.material.value;
    const rates = MATERIAL_RATES[matKey] || MATERIAL_RATES['asphalt-arch'];
    const slopeMult = SLOPE_MULT[els.slope.value] || 1;
    const locKey = els.location.value;
    const locMult = LOCATION_MULT[locKey] || 1;
    const includeTearoff = els.tearoff.checked;

    const materialCost = sqft * rates.material * slopeMult * locMult;
    const laborCost = sqft * rates.labor * slopeMult * locMult;
    const tearoffCost = includeTearoff ? sqft * TEAROFF_PER_SQFT * locMult : 0;
    const permitCost = PERMIT_BASE * (PERMIT_MULT[locKey] || 1);

    const subtotal = materialCost + laborCost + tearoffCost + permitCost;
    const low = subtotal * 0.9;
    const high = subtotal * 1.1;
    const perSqft = subtotal / sqft;

    els.total.textContent = formatMoney(subtotal);
    els.range.textContent = `Typical range: ${formatMoney(low)} – ${formatMoney(high)}`;
    els.materials.textContent = formatMoney(materialCost);
    els.labor.textContent = formatMoney(laborCost);
    els.permits.textContent = formatMoney(permitCost);
    els.tearoffLine.textContent = includeTearoff ? formatMoney(tearoffCost) : '$0';
    els.perSqft.textContent = `$${perSqft.toFixed(2)} per sq ft installed`;

    if (els.tearoffRow) {
      els.tearoffRow.style.opacity = includeTearoff ? '1' : '0.45';
    }
  }

  ['input', 'change'].forEach((evt) => {
    form.addEventListener(evt, calculate);
  });

  calculate();

  const stickyCta = document.querySelector('.sticky-cta');
  const ctaSection = document.getElementById('contractor-cta');
  if (stickyCta && ctaSection) {
    const observer = new IntersectionObserver(
      ([entry]) => {
        stickyCta.classList.toggle('is-visible', !entry.isIntersecting);
      },
      { threshold: 0, rootMargin: '0px 0px -60px 0px' }
    );
    observer.observe(ctaSection);
  }
})();

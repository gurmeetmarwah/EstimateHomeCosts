/**
 * Flooring Cost Calculator landing page — quick + advanced
 */
(function () {
  'use strict';

  const { getCity, getCityValue, locMult } = window.EHCCities || {};

  const MATERIAL = {
    lvp: { material: 3.2, labor: 2.8, label: 'Luxury vinyl plank', tier: 'Most popular', life: '15–25 yrs' },
    hardwood: { material: 6.5, labor: 4.5, label: 'Solid hardwood', tier: 'Premium', life: '50+ yrs' },
    engineered: { material: 5.0, labor: 3.8, label: 'Engineered wood', tier: 'Mid-range', life: '25–40 yrs' },
    tile: { material: 5.5, labor: 4.2, label: 'Porcelain tile', tier: 'Durable', life: '30+ yrs' },
    carpet: { material: 2.5, labor: 1.8, label: 'Carpet', tier: 'Budget', life: '10–15 yrs' },
  };

  const PREP = { none: 1, minor: 1.06, major: 1.14 };
  const REMOVAL = 1.25;

  function formatMoney(n) {
    return '$' + Math.round(n).toLocaleString('en-US');
  }

  function formatRange(low, high) {
    return `${formatMoney(low)}–${formatMoney(high)}`;
  }

  function monthlyPayment(principal, months = 120, annualRate = 0.079) {
    const r = annualRate / 12;
    if (r <= 0) return principal / months;
    return (principal * r) / (1 - Math.pow(1 + r, -months));
  }

  function compute(opts) {
    const sqft = Math.max(100, Math.min(5000, Number(opts.sqft) || 500));
    const mat = MATERIAL[opts.material] || MATERIAL.lvp;
    const prepMult = PREP[opts.prep] || 1;
    const city = getCity(opts.city || 'national');
    const mult = locMult(city);
    const remove = opts.removal === true;

    const baseMult = prepMult * mult;
    const materialCost = sqft * mat.material * baseMult;
    const laborCost = sqft * mat.labor * baseMult;
    const removalCost = remove ? sqft * REMOVAL * mult : 0;
    const permitCost = 0;
    const total = materialCost + laborCost + removalCost + permitCost;
    const low = total * 0.9;
    const high = total * 1.1;
    const mid = total;

    const parts = [
      { key: 'materials', label: 'Materials', amount: materialCost },
      { key: 'labor', label: 'Labor', amount: laborCost },
      { key: 'removal', label: 'Floor removal', amount: removalCost },
      { key: 'permits', label: 'Other fees', amount: permitCost },
    ];

    return {
      sqft,
      low,
      high,
      mid,
      total,
      perSqft: total / sqft,
      parts,
      financing: monthlyPayment(mid),
      cityKey: opts.city || 'national',
      cityLabel: city.label,
    };
  }

  function readAdvanced() {
    const form = document.getElementById('flooring-calculator-tool');
    if (!form) return null;
    return compute({
      sqft: document.getElementById('flooring-size')?.value,
      material: form.querySelector('[name="flooring_material"]:checked')?.value || 'lvp',
      prep: form.querySelector('[name="subfloor_prep"]:checked')?.value || 'minor',
      removal: form.querySelector('[name="floor_removal"]:checked')?.value === 'yes',
      city: getCityValue(document.getElementById('flooring-city')),
    });
  }

  function readQuick() {
    return compute({
      sqft: document.getElementById('quick-sqft')?.value,
      material: document.getElementById('quick-material')?.value || 'lvp',
      prep: 'minor',
      removal: false,
      city: getCityValue(document.getElementById('quick-city')),
    });
  }

  function renderQuick(r) {
    if (!r) return;
    const set = (id, t) => { const n = document.getElementById(id); if (n) n.textContent = t; };
    set('quick-result-range', formatRange(r.low, r.high));
    set('quick-result-hint', `~${formatMoney(r.mid)} mid-estimate · ${r.cityLabel} · ${r.sqft.toLocaleString()} sq ft`);
  }

  function renderAdvanced(r) {
    if (!r) return;
    const set = (id, t) => { const n = document.getElementById(id); if (n) n.textContent = t; };
    set('calc-total-range', formatRange(r.low, r.high));
    set('calc-total-mid', `~${formatMoney(r.mid)} typical · ${r.cityLabel}`);
    set('calc-per-sqft', `$${r.perSqft.toFixed(2)} per sq ft installed`);
    set('calc-financing', formatMoney(r.financing) + '/mo');
    set('calc-financing-note', `Est. ${formatMoney(r.mid)} at 7.9% APR · 10 yr term`);

    const total = r.total || 1;
    r.parts.forEach((p) => {
      const pct = Math.round((p.amount / total) * 100) || 0;
      const bar = document.querySelector(`[data-breakdown="${p.key}"]`);
      const val = document.getElementById(`breakdown-${p.key}`);
      if (bar) bar.style.width = Math.max(pct, p.amount > 0 ? 4 : 0) + '%';
      if (val) val.textContent = formatMoney(p.amount) + (total > 0 ? ` (${pct}%)` : '');
    });
    const list = document.getElementById('calc-line-items');
    if (list) {
      list.innerHTML = r.parts
        .filter((p) => p.amount > 0 || p.key !== 'permits')
        .map((p) => `<li><span>${p.label}</span><strong>${formatMoney(p.amount)}</strong></li>`)
        .join('');
    }
  }

  function syncQuickToAdvanced() {
    const sqft = document.getElementById('quick-sqft')?.value;
    const mat = document.getElementById('quick-material')?.value;
    const city = document.getElementById('quick-city')?.value;
    const sizeInput = document.getElementById('flooring-size');
    const sizeSlider = document.getElementById('flooring-size-slider');
    if (sizeInput && sqft) sizeInput.value = sqft;
    if (sizeSlider && sqft) sizeSlider.value = sqft;
    if (mat) {
      const radio = document.querySelector(`#flooring-calculator-tool [name="flooring_material"][value="${mat}"]`);
      if (radio) radio.checked = true;
    }
    const advCity = document.getElementById('flooring-city');
    if (advCity && city) advCity.value = city;
  }

  function syncCitySelects(fromQuick) {
    const quick = document.getElementById('quick-city');
    const adv = document.getElementById('flooring-city');
    if (!quick || !adv) return;
    if (fromQuick) adv.value = quick.value;
    else quick.value = adv.value;
  }

  function updateAll() {
    const quick = readQuick();
    const advanced = readAdvanced();
    if (quick) renderQuick(quick);
    if (advanced) renderAdvanced(advanced);
  }

  function onCityChange(fromQuick) {
    syncCitySelects(fromQuick);
    updateAll();
  }

  function bindQuick() {
    const bar = document.getElementById('quick-flooring-calc');
    if (!bar) return;
    bar.addEventListener('input', (e) => {
      if (e.target.tagName === 'SELECT') return;
      updateAll();
    });
    bar.addEventListener('change', (e) => {
      if (e.target.id === 'quick-city') return;
      updateAll();
    });
    document.getElementById('quick-city')?.addEventListener('change', () => onCityChange(true));
    document.getElementById('quick-calc-btn')?.addEventListener('click', (e) => {
      e.preventDefault();
      syncQuickToAdvanced();
      updateAll();
      document.getElementById('calculator')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
    updateAll();
  }

  function bindAdvanced() {
    const form = document.getElementById('flooring-calculator-tool');
    if (!form) return;

    const sizeInput = document.getElementById('flooring-size');
    const sizeSlider = document.getElementById('flooring-size-slider');
    const sizeLabel = document.getElementById('flooring-size-label');

    function syncSize(from) {
      const v = Math.max(100, Math.min(5000, Number(from === 'slider' ? sizeSlider.value : sizeInput.value) || 500));
      sizeInput.value = v;
      sizeSlider.value = v;
      if (sizeLabel) sizeLabel.textContent = v.toLocaleString() + ' sq ft';
      const q = document.getElementById('quick-sqft');
      if (q) q.value = v;
      updateAll();
    }

    sizeInput?.addEventListener('input', () => syncSize('input'));
    sizeSlider?.addEventListener('input', () => syncSize('slider'));
    document.getElementById('flooring-city')?.addEventListener('change', () => onCityChange(false));

    ['input', 'change'].forEach((evt) => {
      form.addEventListener(evt, (e) => {
        if (e.target.id === 'flooring-city') return;
        if (e.target.tagName === 'SELECT') return;
        const mat = form.querySelector('[name="flooring_material"]:checked')?.value;
        const qm = document.getElementById('quick-material');
        if (qm && mat) qm.value = mat;
        updateAll();
      });
    });

    updateAll();
  }

  function applyMaterialFromUrl() {
    const m = new URLSearchParams(window.location.search).get('material');
    if (!m || !MATERIAL[m]) return;
    const radio = document.querySelector(`#flooring-calculator-tool [name="flooring_material"][value="${m}"]`);
    if (radio) radio.checked = true;
    const quickMat = document.getElementById('quick-material');
    if (quickMat) quickMat.value = m;
    updateAll();
  }

  bindQuick();
  bindAdvanced();
  applyMaterialFromUrl();

  document.querySelectorAll('[data-scroll-calc]').forEach((btn) => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      document.getElementById('quick-estimate')?.scrollIntoView({ behavior: 'smooth' });
    });
  });

  window.addEventListener('ehc:city-scope', () => updateAll());
})();

/**
 * Fence Cost Calculator landing page — quick + advanced
 */
(function () {
  'use strict';

  const { getCity, getCityValue, locMult } = window.EHCCities || {};
  const FENCE_PERMIT_SCALE = 125 / 275;

  const MATERIAL = {
    wood: { rate: 28, label: 'Wood privacy', tier: 'Most popular', life: '15–20 yrs' },
    vinyl: { rate: 32, label: 'Vinyl', tier: 'Low maintenance', life: '20–30 yrs' },
    composite: { rate: 38, label: 'Composite', tier: 'Premium', life: '25–30 yrs' },
    chain: { rate: 18, label: 'Chain link', tier: 'Budget', life: '15–25 yrs' },
    aluminum: { rate: 35, label: 'Aluminum', tier: 'Durable', life: '25+ yrs' },
  };

  const HEIGHT = { '4': 0.85, '6': 1, '8': 1.22 };
  const GATES = { '0': 1, '1': 1.08, '2': 1.15 };
  const TERRAIN = { flat: 1, moderate: 1.08, steep: 1.18 };
  const GATE_COST = 350;

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
    const linearFt = Math.max(20, Math.min(1000, Number(opts.linearFt) || 150));
    const mat = MATERIAL[opts.material] || MATERIAL.wood;
    const heightMult = HEIGHT[opts.height] || 1;
    const gateCount = Math.min(2, Math.max(0, Number(opts.gates) || 0));
    const terrainMult = TERRAIN[opts.terrain] || 1;
    const city = getCity(opts.city || 'national');
    const mult = locMult(city);

    const fenceCost = linearFt * mat.rate * heightMult * terrainMult * mult;
    const gateCost = gateCount * GATE_COST * mult;
    const permits = Math.round(city.permit * FENCE_PERMIT_SCALE);
    const total = fenceCost + gateCost + permits;
    const low = total * 0.9;
    const high = total * 1.1;
    const mid = total;

    const parts = [
      { key: 'fence', label: 'Fence & labor', amount: fenceCost },
      { key: 'gates', label: 'Gates', amount: gateCost },
      { key: 'permits', label: 'Permits', amount: permits },
    ];

    return {
      linearFt,
      low,
      high,
      mid,
      total,
      perFt: total / linearFt,
      parts,
      financing: monthlyPayment(mid),
      cityKey: opts.city || 'national',
      cityLabel: city.label,
    };
  }

  function readAdvanced() {
    const form = document.getElementById('fence-calculator-tool');
    if (!form) return null;
    return compute({
      linearFt: document.getElementById('fence-length')?.value,
      material: form.querySelector('[name="fence_material"]:checked')?.value || 'wood',
      height: form.querySelector('[name="fence_height"]:checked')?.value || '6',
      gates: form.querySelector('[name="fence_gates"]:checked')?.value || '1',
      terrain: form.querySelector('[name="terrain"]:checked')?.value || 'flat',
      city: getCityValue(document.getElementById('fence-city')),
    });
  }

  function readQuick() {
    return compute({
      linearFt: document.getElementById('quick-length')?.value,
      material: document.getElementById('quick-material')?.value || 'wood',
      height: '6',
      gates: '1',
      terrain: 'flat',
      city: getCityValue(document.getElementById('quick-city')),
    });
  }

  function renderQuick(r) {
    if (!r) return;
    const set = (id, t) => { const n = document.getElementById(id); if (n) n.textContent = t; };
    set('quick-result-range', formatRange(r.low, r.high));
    set('quick-result-hint', `~${formatMoney(r.mid)} mid-estimate · ${r.cityLabel} · ${r.linearFt} linear ft`);
  }

  function renderAdvanced(r) {
    if (!r) return;
    const set = (id, t) => { const n = document.getElementById(id); if (n) n.textContent = t; };
    set('calc-total-range', formatRange(r.low, r.high));
    set('calc-total-mid', `~${formatMoney(r.mid)} typical · ${r.cityLabel}`);
    set('calc-per-sqft', `$${r.perFt.toFixed(2)} per linear ft`);
    set('calc-financing', formatMoney(r.financing) + '/mo');
    set('calc-financing-note', `Est. ${formatMoney(r.mid)} at 7.9% APR · 10 yr term`);

    const total = r.total || 1;
    r.parts.forEach((p) => {
      const pct = Math.round((p.amount / total) * 100);
      const bar = document.querySelector(`[data-breakdown="${p.key}"]`);
      const val = document.getElementById(`breakdown-${p.key}`);
      if (bar) bar.style.width = pct + '%';
      if (val) val.textContent = formatMoney(p.amount) + ` (${pct}%)`;
    });
    const list = document.getElementById('calc-line-items');
    if (list) {
      list.innerHTML = r.parts.map((p) => `<li><span>${p.label}</span><strong>${formatMoney(p.amount)}</strong></li>`).join('');
    }
  }

  function syncQuickToAdvanced() {
    const len = document.getElementById('quick-length')?.value;
    const mat = document.getElementById('quick-material')?.value;
    const city = document.getElementById('quick-city')?.value;
    const lenInput = document.getElementById('fence-length');
    const lenSlider = document.getElementById('fence-length-slider');
    if (lenInput && len) lenInput.value = len;
    if (lenSlider && len) lenSlider.value = len;
    if (mat) {
      const radio = document.querySelector(`#fence-calculator-tool [name="fence_material"][value="${mat}"]`);
      if (radio) radio.checked = true;
    }
    const advCity = document.getElementById('fence-city');
    if (advCity && city) advCity.value = city;
  }

  function syncCitySelects(fromQuick) {
    const quick = document.getElementById('quick-city');
    const adv = document.getElementById('fence-city');
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
    const bar = document.getElementById('quick-fence-calc');
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
    const form = document.getElementById('fence-calculator-tool');
    if (!form) return;

    const lenInput = document.getElementById('fence-length');
    const lenSlider = document.getElementById('fence-length-slider');
    const lenLabel = document.getElementById('fence-length-label');

    function syncLen(from) {
      const v = Math.max(20, Math.min(1000, Number(from === 'slider' ? lenSlider.value : lenInput.value) || 150));
      lenInput.value = v;
      lenSlider.value = v;
      if (lenLabel) lenLabel.textContent = v + ' linear ft';
      const q = document.getElementById('quick-length');
      if (q) q.value = v;
      updateAll();
    }

    lenInput?.addEventListener('input', () => syncLen('input'));
    lenSlider?.addEventListener('input', () => syncLen('slider'));
    document.getElementById('fence-city')?.addEventListener('change', () => onCityChange(false));

    ['input', 'change'].forEach((evt) => {
      form.addEventListener(evt, (e) => {
        if (e.target.id === 'fence-city') return;
        if (e.target.tagName === 'SELECT') return;
        const mat = form.querySelector('[name="fence_material"]:checked')?.value;
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
    const radio = document.querySelector(`#fence-calculator-tool [name="fence_material"][value="${m}"]`);
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

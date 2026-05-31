/**
 * Roof Cost Calculator landing page — quick estimate + advanced tool
 */
(function () {
  'use strict';

  const MATERIAL = {
    'asphalt-arch': { material: 2.35, labor: 2.45, label: 'Asphalt shingles', lifespan: '25–30 yrs', tier: 'Most popular' },
    'asphalt-3tab': { material: 1.85, labor: 2.1, label: '3-tab asphalt', lifespan: '15–20 yrs', tier: 'Budget' },
    metal: { material: 4.2, labor: 3.8, label: 'Metal', lifespan: '40–70 yrs', tier: 'Premium' },
    tile: { material: 5.5, labor: 4.2, label: 'Tile', lifespan: '50+ yrs', tier: 'Premium' },
    slate: { material: 8.5, labor: 5.5, label: 'Slate', lifespan: '75–100 yrs', tier: 'Luxury' },
    wood: { material: 3.8, labor: 3.4, label: 'Wood shake', lifespan: '20–30 yrs', tier: 'Mid-range' },
  };

  const SLOPE = { low: 0.92, moderate: 1, steep: 1.18, 'very-steep': 1.35 };
  const COMPLEXITY = { simple: 0.94, moderate: 1, complex: 1.14 };
  const STORIES = { '1': 1, '2': 1.07, '3': 1.14 };
  const TEAROFF = 0.85;
  const WASTE_RATE = 0.05;

  const LABOR_LOW = 2.45;
  const LABOR_HIGH = 4.5;
  const MAT_LOW = 2.35;
  const MAT_HIGH = 8.5;

  /** City-specific notes shown in Regional Roof Cost Factors */
  const REGIONAL_NOTES = {
    national: 'Baseline U.S. rates; seasonal demand peaks in spring and fall',
    texas: 'Statewide averages; hail exposure in North Texas and heat across central & south TX',
    dallas: 'Hail claims and wind uplift codes in North Texas metro',
    phoenix: 'Extreme heat drives cool-roof and tile/metal demand',
    austin: 'Fast-growing market; steep-slope labor competitive',
    tampa: 'Hurricane nailing patterns and tile common on Gulf Coast',
    miami: 'Coastal wind ratings and salt-air corrosion on fasteners',
    jacksonville: 'Humidity and storm exposure; architectural shingles dominant',
    'st-petersburg': 'Pinellas coastal wind codes; tile and metal common',
    charlotte: 'Moderate labor market; ice/water shield in mountain fringe',
    raleigh: 'Research Triangle growth; asphalt architectural dominant',
    durham: 'Older housing stock; mini-split and re-roof cycles',
    cary: 'HOA standards and suburban architectural shingles',
    wilmington: 'Coastal wind exposure and humidity-ready materials',
    scottsdale: 'Premium materials and labor; HOA architectural standards',
    mesa: 'East Valley heat; tile and cool-roof asphalt popular',
    tucson: 'Desert sun and monsoon seasons affect material choice',
    chandler: 'Master-planned communities; tile and metal accents',
    houston: 'Humidity, wind, and frequent storm-related re-roofs',
    'san-antonio': 'Tile and stucco common; affordable labor vs. Austin',
    'fort-worth': 'Hail exposure and western DFW suburban growth',
    orlando: 'Central FL wind codes; tile and metal popular',
    'san-diego': 'Coastal labor premium; Title 24 / cool-roof requirements',
    'los-angeles': 'Among highest labor rates; earthquake and ember-zone codes',
    'orange-county': 'HOA tile and composition standards in planned communities',
    sacramento: 'Inland heat and wildfire ember zones shape roofing choices',
    'san-francisco': 'Dense housing and premium labor; flat and pitched re-roofs',
  };

  function getCity(key) {
    return window.EHCCities?.getCity?.(key) || { label: 'National average', material: 1, labor: 1, permit: 275 };
  }

  function getCityValue(el) {
    const v = el?.value;
    if (v && getCity(v) && v !== 'national') return v;
    const scope = window.EHCCityPath?.parseScope?.() || window.EHCCityPath?.parseCityScope?.();
    const scoped = scope?.cityKey;
    if (scoped && getCity(scoped)) return scoped;
    return v && getCity(v) ? v : 'national';
  }

  function formatMoney(n) {
    return '$' + Math.round(n).toLocaleString('en-US');
  }

  function formatRange(low, high) {
    return `${formatMoney(low)}–${formatMoney(high)}`;
  }

  function formatRateRange(low, high) {
    return `$${low.toFixed(2)}–$${high.toFixed(2)}`;
  }

  function multiplierLabel(city) {
    const mult = (city.material + city.labor) / 2;
    if (mult >= 0.995 && mult <= 1.005) return '~Baseline (national average)';
    const pct = Math.round(Math.abs(mult - 1) * 100);
    return mult < 1 ? `~${pct}% below national average` : `~${pct}% above national average`;
  }

  function renderLocalFactors(cityKey) {
    const card = document.getElementById('local-factor-city-card');
    const grid = document.getElementById('local-factors-grid');
    const title = document.getElementById('local-factor-city-title');
    const list = document.getElementById('local-factor-city-list');
    const isNational = !cityKey || cityKey === 'national';

    if (card) card.hidden = isNational;
    if (grid) {
      grid.classList.toggle('local-factors-grid--single', isNational);
      grid.classList.toggle('local-factors-grid--two', !isNational);
    }
    if (isNational || !title || !list) return;

    const city = getCity(cityKey);
    const laborLow = LABOR_LOW * city.labor;
    const laborHigh = LABOR_HIGH * city.labor;
    const matLow = MAT_LOW * city.material;
    const matHigh = MAT_HIGH * city.material;
    const note = REGIONAL_NOTES[cityKey] || REGIONAL_NOTES.national;

    title.textContent = city.label;
    list.innerHTML = [
      `<li><strong>Multiplier:</strong> ${multiplierLabel(city)}</li>`,
      `<li><strong>Labor:</strong> ${formatRateRange(laborLow, laborHigh)} / sq ft installed</li>`,
      `<li><strong>Materials:</strong> ${formatRateRange(matLow, matHigh)} / sq ft by type</li>`,
      `<li><strong>Permits:</strong> ~${formatMoney(city.permit)} typical re-roof (est.)</li>`,
      `<li><strong>Local factors:</strong> ${note}</li>`,
    ].join('');
  }

  function monthlyPayment(principal, months = 120, annualRate = 0.079) {
    const r = annualRate / 12;
    if (r <= 0) return principal / months;
    return (principal * r) / (1 - Math.pow(1 + r, -months));
  }

  function compute(opts) {
    const sqft = Math.max(500, Math.min(10000, Number(opts.sqft) || 2000));
    const matKey = opts.material || 'asphalt-arch';
    const rates = MATERIAL[matKey] || MATERIAL['asphalt-arch'];
    const slopeMult = SLOPE[opts.slope] || 1;
    const complexMult = COMPLEXITY[opts.complexity] || 1;
    const storiesMult = STORIES[opts.stories] || 1;
    const cityKey = opts.city || 'national';
    const city = getCity(cityKey);
    const tearoff = opts.tearoff !== false;

    const baseMult = slopeMult * complexMult * storiesMult;

    const materialCost = sqft * rates.material * baseMult * city.material;
    const laborCost = sqft * rates.labor * baseMult * city.labor;
    const tearoffCost = tearoff ? sqft * TEAROFF * city.labor : 0;
    const permitCost = city.permit;
    const subtotal = materialCost + laborCost + tearoffCost + permitCost;
    const wasteCost = subtotal * WASTE_RATE;
    const total = subtotal + wasteCost;

    const low = total * 0.9;
    const high = total * 1.1;
    const mid = total;

    const parts = [
      { key: 'materials', label: 'Materials', amount: materialCost },
      { key: 'labor', label: 'Labor', amount: laborCost },
      { key: 'tearoff', label: 'Tear-off', amount: tearoffCost },
      { key: 'permits', label: 'Permits', amount: permitCost },
      { key: 'waste', label: 'Waste & disposal', amount: wasteCost },
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
      cityKey,
      cityLabel: city.label,
    };
  }

  function readAdvanced() {
    const form = document.getElementById('roof-calculator-tool');
    if (!form) return null;
    const matRadio = form.querySelector('[name="roof_material"]:checked');
    return compute({
      sqft: document.getElementById('roof-size')?.value,
      material: matRadio?.value || 'asphalt-arch',
      slope: form.querySelector('[name="roof_pitch"]:checked')?.value || 'moderate',
      complexity: form.querySelector('[name="complexity"]:checked')?.value || 'moderate',
      stories: form.querySelector('[name="stories"]:checked')?.value || '1',
      tearoff: form.querySelector('[name="tearoff"]:checked')?.value === 'yes',
      city: getCityValue(document.getElementById('roof-city')),
    });
  }

  function readQuick() {
    return compute({
      sqft: document.getElementById('quick-sqft')?.value,
      material: document.getElementById('quick-material')?.value || 'asphalt-arch',
      slope: 'moderate',
      complexity: 'moderate',
      stories: '1',
      tearoff: true,
      city: getCityValue(document.getElementById('quick-city')),
    });
  }

  function renderQuick(r) {
    if (!r) return;
    const el = document.getElementById('quick-result-range');
    const hint = document.getElementById('quick-result-hint');
    if (el) el.textContent = formatRange(r.low, r.high);
    if (hint) {
      hint.textContent = `~${formatMoney(r.mid)} mid-estimate · ${r.cityLabel} · ${r.sqft.toLocaleString()} sq ft`;
    }
  }

  function renderAdvanced(r) {
    if (!r) return;
    const set = (id, text) => {
      const n = document.getElementById(id);
      if (n) n.textContent = text;
    };
    set('calc-total-range', formatRange(r.low, r.high));
    set('calc-total-mid', `~${formatMoney(r.mid)} typical · ${r.cityLabel}`);
    set('calc-per-sqft', `$${r.perSqft.toFixed(2)} per sq ft installed`);
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
      list.innerHTML = r.parts
        .map((p) => `<li><span>${p.label}</span><strong>${formatMoney(p.amount)}</strong></li>`)
        .join('');
    }
  }

  function syncQuickToAdvanced() {
    const sqft = document.getElementById('quick-sqft')?.value;
    const mat = document.getElementById('quick-material')?.value;
    const city = document.getElementById('quick-city')?.value;
    const sizeInput = document.getElementById('roof-size');
    const sizeSlider = document.getElementById('roof-size-slider');
    if (sizeInput && sqft) sizeInput.value = sqft;
    if (sizeSlider && sqft) sizeSlider.value = sqft;
    if (mat) {
      const radio = document.querySelector(`#roof-calculator-tool [name="roof_material"][value="${mat}"]`);
      if (radio) radio.checked = true;
    }
    const roofCity = document.getElementById('roof-city');
    if (roofCity && city) roofCity.value = city;
  }

  function syncCitySelects(fromQuick) {
    const quick = document.getElementById('quick-city');
    const adv = document.getElementById('roof-city');
    if (!quick || !adv) return;
    if (fromQuick) adv.value = quick.value;
    else quick.value = adv.value;
  }

  function updateAll() {
    const quick = readQuick();
    const advanced = readAdvanced();
    if (quick) renderQuick(quick);
    if (advanced) renderAdvanced(advanced);
    const cityKey = getCityValue(document.getElementById('roof-city')) ||
      getCityValue(document.getElementById('quick-city'));
    renderLocalFactors(cityKey);
  }

  function onCityChange(fromQuick) {
    syncCitySelects(fromQuick);
    updateAll();
  }

  function bindQuick() {
    const bar = document.getElementById('quick-roof-calc');
    if (!bar) return;
    const onFieldChange = (e) => {
      if (e.target.id === 'quick-city') return;
      updateAll();
    };
    bar.addEventListener('input', (e) => {
      if (e.target.tagName === 'SELECT') return;
      updateAll();
    });
    bar.addEventListener('change', onFieldChange);
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
    const form = document.getElementById('roof-calculator-tool');
    if (!form) return;

    const sizeInput = document.getElementById('roof-size');
    const sizeSlider = document.getElementById('roof-size-slider');
    const sizeLabel = document.getElementById('roof-size-label');
    const squaresLabel = document.getElementById('roof-squares-label');

    function syncSize(from) {
      const v = Math.max(500, Math.min(10000, Number(from === 'slider' ? sizeSlider.value : sizeInput.value) || 2000));
      sizeInput.value = v;
      sizeSlider.value = v;
      if (sizeLabel) sizeLabel.textContent = v.toLocaleString() + ' sq ft';
      if (squaresLabel) squaresLabel.textContent = (v / 100).toFixed(1) + ' squares';
      const quickSqft = document.getElementById('quick-sqft');
      if (quickSqft) quickSqft.value = v;
      updateAll();
    }

    sizeInput?.addEventListener('input', () => syncSize('input'));
    sizeSlider?.addEventListener('input', () => syncSize('slider'));

    document.getElementById('roof-city')?.addEventListener('change', () => onCityChange(false));

    ['input', 'change'].forEach((evt) => {
      form.addEventListener(evt, (e) => {
        if (e.target.id === 'roof-city') return;
        if (e.target.tagName === 'SELECT') return;
        const mat = form.querySelector('[name="roof_material"]:checked')?.value;
        const quickMat = document.getElementById('quick-material');
        if (quickMat && mat) quickMat.value = mat;
        updateAll();
      });
    });

    updateAll();
  }

  bindQuick();
  bindAdvanced();

  document.querySelectorAll('[data-scroll-calc]').forEach((btn) => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      document.getElementById('quick-estimate')?.scrollIntoView({ behavior: 'smooth' });
    });
  });

  window.addEventListener('ehc:city-scope', () => {
    const scope = window.EHCCityPath?.parseCityScope?.();
    if (!scope) return;
    ['quick-city', 'roof-city'].forEach((id) => {
      const node = document.getElementById(id);
      if (node) node.value = scope.cityKey;
    });
    updateAll();
    renderLocalFactors(scope.cityKey);
    renderComparisonTable(scope.cityKey);
  });
})();

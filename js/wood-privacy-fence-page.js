/**
 * Wood privacy fence landing page — /fence-materials/wood-privacy-fence-cost/
 */
(function () {
  'use strict';

  const { getCity, getCityValue, locMult } = window.EHCCities || {
    getCity: () => ({ label: 'National average', material: 1, labor: 1, permit: 125 }),
    getCityValue: () => 'national',
    locMult: () => 1,
  };

  const BASE_RATE = 28;
  const HEIGHT = { '4': 0.85, '6': 1, '8': 1.22 };
  const TERRAIN = { flat: 1, moderate: 1.08, steep: 1.18 };
  const GATE_COST = 350;
  const FENCE_PERMIT_SCALE = 125 / 275;

  const VARIANT = {
    stockade: { mult: 0.92, label: 'Stockade' },
    shadowbox: { mult: 1, label: 'Shadowbox' },
    'board-on-board': { mult: 1.08, label: 'Board-on-Board' },
    horizontal: { mult: 1.15, label: 'Horizontal Slat' },
    modern: { mult: 1.28, label: 'Modern Cedar Privacy' },
  };

  const SPECIES = {
    pine: { mult: 0.88, label: 'Pressure-treated pine', cost: '$22–$32', life: '10–15 years', look: 'Budget-friendly' },
    cedar: { mult: 1, label: 'Cedar', cost: '$25–$38', life: '15–20 years', look: 'Natural grain' },
    cypress: { mult: 1.06, label: 'Cypress', cost: '$28–$40', life: '15–25 years', look: 'Rot-resistant' },
    redwood: { mult: 1.22, label: 'Redwood', cost: '$32–$48', life: '20–25 years', look: 'Premium appearance' },
  };

  const REGIONAL = {
    national: 'Stain every 2–4 years in most climates to prevent graying and warping',
    dallas: 'Intense sun fades stain quickly — UV-resistant sealers recommended',
    phoenix: 'Low humidity helps, but extreme heat stresses boards and posts',
    austin: 'Moderate climate; cedar popular in Hill Country suburbs',
    tampa: 'High humidity — pressure-treated or cypress resist moisture better',
    charlotte: 'Balanced climate; 6 ft privacy typical for HOA neighborhoods',
    raleigh: 'Growing suburbs; board-on-board common for upscale lots',
    scottsdale: 'Desert sun — lighter stain colors reduce heat absorption',
    houston: 'Humidity and soil movement — deep posts and quality concrete matter',
    orlando: 'Moisture and storms — secure post footings and cap boards',
    'san-diego': 'Coastal salt air — stainless fasteners and quality stain essential',
  };

  const HOME_EXAMPLES = {
    national: { ft: 150, height: 6, variant: 'board-on-board', species: 'cedar', gates: 1, detail: '6 ft cedar · one walk gate' },
    dallas: { ft: 180, height: 6, variant: 'board-on-board', species: 'cedar', gates: 1, detail: '6 ft cedar privacy · slope grading' },
    phoenix: { ft: 160, height: 6, variant: 'shadowbox', species: 'cedar', gates: 1, detail: '6 ft shadowbox · UV stain' },
    tampa: { ft: 140, height: 6, variant: 'stockade', species: 'cypress', gates: 1, detail: '6 ft cypress · humidity-rated' },
  };

  function formatMoney(n) {
    return '$' + Math.round(n).toLocaleString('en-US');
  }

  function formatRange(low, high) {
    return `${formatMoney(low)}–${formatMoney(high)}`;
  }

  function compute(opts) {
    const linearFt = Math.max(20, Math.min(1000, Number(opts.linearFt) || 150));
    const variant = VARIANT[opts.variant] || VARIANT['board-on-board'];
    const species = SPECIES[opts.species] || SPECIES.cedar;
    const heightMult = HEIGHT[opts.height] || 1;
    const gateCount = Math.min(2, Math.max(0, Number(opts.gates) || 1));
    const terrainMult = TERRAIN[opts.terrain] || 1;
    const city = getCity(opts.city || 'national');
    const mult = locMult(city);

    const fenceCost = linearFt * BASE_RATE * variant.mult * species.mult * heightMult * terrainMult * mult;
    const gateCost = gateCount * GATE_COST * mult;
    const permits = Math.round(city.permit * FENCE_PERMIT_SCALE);
    const total = fenceCost + gateCost + permits;
    const low = total * 0.9;
    const high = total * 1.1;
    const perFtLow = low / linearFt;
    const perFtHigh = high / linearFt;

    return {
      linearFt,
      low,
      high,
      mid: total,
      perFtLow,
      perFtHigh,
      cityLabel: city.label,
      cityKey: opts.city || 'national',
      variantLabel: variant.label,
      speciesLabel: species.label,
    };
  }

  function readCalc() {
    return compute({
      linearFt: document.getElementById('wood-fence-length')?.value,
      variant: document.getElementById('wood-fence-variant')?.value || 'board-on-board',
      species: document.getElementById('wood-fence-species')?.value || 'cedar',
      height: document.getElementById('wood-fence-height')?.value || '6',
      gates: document.getElementById('wood-fence-gates')?.value || '1',
      terrain: 'flat',
      city: getCityValue(document.getElementById('wood-fence-city')),
    });
  }

  function renderHero(r) {
    if (!r) return;
    const set = (id, t) => {
      const el = document.getElementById(id);
      if (el) el.textContent = t;
    };
    set('hero-cost-range', formatRange(r.low, r.high));
    set('hero-per-ft', `$${r.perFtLow.toFixed(0)}–$${r.perFtHigh.toFixed(0)} per linear ft`);
    set('hero-preview-ft', `${r.linearFt} linear ft`);
    const lo = compute({ linearFt: 100, variant: 'stockade', species: 'pine', height: 6, gates: 0, city: 'national' }).perFtLow;
    const hi = compute({ linearFt: 200, variant: 'modern', species: 'redwood', height: 8, gates: 2, city: 'national' }).perFtHigh;
    set('stat-avg-cost', `$${lo.toFixed(0)}–$${hi.toFixed(0)} per linear ft`);
  }

  function renderCalcPanel(r) {
    if (!r) return;
    const set = (id, t) => {
      const el = document.getElementById(id);
      if (el) el.textContent = t;
    };
    set('wood-calc-range', formatRange(r.low, r.high));
    set('wood-calc-hint', `${r.linearFt} ft · ${r.variantLabel} · ${r.speciesLabel} · ${r.cityLabel}`);
    set('wood-calc-per-ft', `$${r.perFtLow.toFixed(0)}–$${r.perFtHigh.toFixed(0)} per linear ft installed`);
  }

  function renderCostRanges(cityKey) {
    const list = document.getElementById('wood-cost-range-list');
    if (!list) return;
    const cfg = document.getElementById('wood-fence-calc-form');
    const variant = cfg?.querySelector('[name="fence_style"]:checked')?.value || document.getElementById('wood-fence-variant')?.value || 'board-on-board';
    const species = document.getElementById('wood-fence-species')?.value || 'cedar';
    const height = document.getElementById('wood-fence-height')?.value || '6';
    const gates = document.getElementById('wood-fence-gates')?.value || '1';
    const activeFt = Number(document.getElementById('wood-fence-length')?.value) || 150;
    [100, 150, 200].forEach((ft) => {
      const r = compute({ linearFt: ft, variant, species, height, gates, city: cityKey });
      const card = list.querySelector(`[data-range-ft="${ft}"]`);
      if (!card) return;
      const price = card.querySelector('.wood-cost-benchmark-price');
      if (price) price.textContent = formatRange(r.low, r.high);
      const isActive = activeFt === ft;
      card.classList.toggle('wood-cost-benchmark-card--active', isActive);
      const isNear = !isActive && Math.abs(activeFt - ft) <= 25;
      card.classList.toggle('wood-cost-benchmark-card--near', isNear);
    });
  }

  function renderSpeciesTable(cityKey) {
    const tbody = document.getElementById('wood-species-tbody');
    if (!tbody) return;
    const ft = Number(document.getElementById('wood-fence-length')?.value) || 150;
    const variant = document.getElementById('wood-fence-variant')?.value || 'board-on-board';
    tbody.innerHTML = Object.keys(SPECIES)
      .map((key) => {
        const s = SPECIES[key];
        const r = compute({ linearFt: ft, variant, species: key, height: 6, gates: 1, city: cityKey });
        return `<tr>
          <td>${s.label}</td>
          <td>${formatRange(r.perFtLow, r.perFtHigh)} / ft</td>
          <td>${s.life}</td>
          <td>${s.look}</td>
        </tr>`;
      })
      .join('');
  }

  function renderLocalWeather(cityKey) {
    const card = document.getElementById('wood-weather-city-card');
    const grid = document.getElementById('wood-weather-grid');
    const title = document.getElementById('wood-weather-city-title');
    const list = document.getElementById('wood-weather-city-list');
    const isNational = !cityKey || cityKey === 'national';
    if (card) card.hidden = isNational;
    if (grid) {
      grid.classList.toggle('local-factors-grid--single', isNational);
      grid.classList.toggle('local-factors-grid--two', !isNational);
    }
    if (isNational || !title || !list) return;
    title.textContent = cityKey === 'phoenix' ? 'Arizona (Phoenix area)' : cityKey === 'tampa' ? 'Florida (Tampa area)' : cityKey === 'dallas' ? 'Texas (Dallas area)' : getCity(cityKey).label;
    list.innerHTML = `<li>${REGIONAL[cityKey] || REGIONAL.national}</li>`;
  }

  function renderProjects(cityKey) {
    const isNational = !cityKey || cityKey === 'national';
    const natCard = document.querySelector('[data-project-city="national"]');
    const cityCard = document.getElementById('wood-project-city-card');
    if (natCard) {
      const ex = HOME_EXAMPLES.national;
      const r = compute({ linearFt: ex.ft, variant: ex.variant, species: ex.species, height: ex.height, gates: ex.gates, city: 'national' });
      const cost = natCard.querySelector('[data-project-cost]');
      if (cost) cost.textContent = formatMoney(r.mid);
      natCard.classList.toggle('project-example-card--active', isNational);
    }
    if (!cityCard) return;
    if (isNational) {
      cityCard.hidden = true;
      return;
    }
    const ex = HOME_EXAMPLES[cityKey] || HOME_EXAMPLES.national;
    const r = compute({ linearFt: ex.ft, variant: ex.variant, species: ex.species, height: ex.height, gates: ex.gates, city: cityKey });
    cityCard.hidden = false;
    cityCard.classList.add('project-example-card--active');
    if (natCard) natCard.classList.remove('project-example-card--active');
    const titleEl = cityCard.querySelector('[data-project-city-title]');
    const typeEl = cityCard.querySelector('[data-project-type]');
    const detailEl = cityCard.querySelector('[data-project-detail]');
    const costEl = cityCard.querySelector('[data-project-cost]');
    if (titleEl) titleEl.textContent = getCity(cityKey).label;
    if (typeEl) typeEl.textContent = `${ex.height} ft ${SPECIES[ex.species].label} Privacy · ${ex.ft} linear ft`;
    if (detailEl) detailEl.textContent = ex.detail;
    if (costEl) costEl.textContent = formatMoney(r.mid);
  }

  function updateVariantCards(fromSelect) {
    const sel = document.getElementById('wood-fence-variant');
    const variant = fromSelect
      ? sel?.value
      : document.querySelector('[name="fence_style"]:checked')?.value || sel?.value;
    if (sel && variant) sel.value = variant;
    document.querySelectorAll('[name="fence_style"]').forEach((input) => {
      if (input.value === variant) input.checked = true;
    });
    document.querySelectorAll('[data-fence-variant-card]').forEach((card) => {
      card.classList.toggle('fence-variant-card--active', card.dataset.fenceVariantCard === variant);
    });
  }

  function updateAll() {
    const r = readCalc();
    renderHero(r);
    renderCalcPanel(r);
    const cityKey = getCityValue(document.getElementById('wood-fence-city'));
    renderCostRanges(cityKey);
    renderSpeciesTable(cityKey);
    renderLocalWeather(cityKey);
    renderProjects(cityKey);
  }

  function bind() {
    const form = document.getElementById('wood-fence-calc-form');
    if (!form) return;
    form.addEventListener('input', updateAll);
    form.addEventListener('change', updateAll);
    document.querySelectorAll('[name="fence_style"]').forEach((input) => {
      input.addEventListener('change', () => {
        updateVariantCards(false);
        updateAll();
      });
    });
    const variantSel = document.getElementById('wood-fence-variant');
    if (variantSel) {
      variantSel.addEventListener('change', () => {
        updateVariantCards(true);
        updateAll();
      });
    }
    updateVariantCards(false);
    updateAll();
  }

  bind();
  window.addEventListener('ehc:city-scope', () => updateAll());
})();

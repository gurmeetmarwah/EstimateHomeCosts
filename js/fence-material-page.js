/**
 * Generic fence material landing pages — /fence-materials/{slug}/
 * Requires window.FENCE_MATERIAL_CONFIG (inline on page).
 */
(function () {
  'use strict';

  const cfg = window.FENCE_MATERIAL_CONFIG;
  if (!cfg) return;

  const { getCity, getCityValue, locMult } = window.EHCCities || {
    getCity: () => ({ label: 'National average', material: 1, labor: 1, permit: 125 }),
    getCityValue: () => 'national',
    locMult: () => 1,
  };

  const BASE_RATE = cfg.baseRate;
  const HEIGHT = { '4': 0.85, '6': 1, '8': 1.22 };
  const TERRAIN = { flat: 1, moderate: 1.08, steep: 1.18 };
  const GATE_COST = 350;
  const FENCE_PERMIT_SCALE = 125 / 275;
  const VARIANT = cfg.variants || {};
  const GRADES = cfg.grades || {};
  const REGIONAL = cfg.regional || {};
  const HOME_EXAMPLES = cfg.homeExamples || { national: { ft: 150, height: 6, variant: cfg.defaultVariant, gates: 1, detail: '' } };
  const defaultVariant = cfg.defaultVariant || Object.keys(VARIANT)[0];
  const defaultGrade = cfg.defaultGrade || Object.keys(GRADES)[0] || null;

  function formatMoney(n) {
    return '$' + Math.round(n).toLocaleString('en-US');
  }

  function formatRange(low, high) {
    return `${formatMoney(low)}–${formatMoney(high)}`;
  }

  function compute(opts) {
    const linearFt = Math.max(20, Math.min(1000, Number(opts.linearFt) || 150));
    const variant = VARIANT[opts.variant] || VARIANT[defaultVariant] || { mult: 1, label: cfg.shortLabel };
    const grade = GRADES[opts.grade] || (defaultGrade ? GRADES[defaultGrade] : null) || { mult: 1 };
    const gradeMult = grade.mult || 1;
    const heightMult = HEIGHT[opts.height] || 1;
    const gateCount = Math.min(2, Math.max(0, Number(opts.gates) ?? 1));
    const terrainMult = TERRAIN[opts.terrain] || 1;
    const city = getCity(opts.city || 'national');
    const mult = locMult(city);

    const fenceCost = linearFt * BASE_RATE * variant.mult * gradeMult * heightMult * terrainMult * mult;
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
      gradeLabel: grade.label || '',
    };
  }

  function el(id) {
    return document.getElementById(id);
  }

  function readCalc() {
    return compute({
      linearFt: el('fence-material-length')?.value,
      variant: el('fence-material-variant')?.value || defaultVariant,
      grade: el('fence-material-grade')?.value || defaultGrade,
      height: el('fence-material-height')?.value || '6',
      gates: el('fence-material-gates')?.value ?? '1',
      terrain: 'flat',
      city: getCityValue(el('fence-material-city')),
    });
  }

  function renderHero(r) {
    if (!r) return;
    const set = (id, t) => {
      const n = el(id);
      if (n) n.textContent = t;
    };
    set('hero-cost-range', formatRange(r.low, r.high));
    set('hero-per-ft', `$${r.perFtLow.toFixed(0)}–$${r.perFtHigh.toFixed(0)} per linear ft · 6 ft`);
    const keys = Object.keys(VARIANT);
    const loKey = keys[0];
    const hiKey = keys[keys.length - 1];
    const lo = compute({ linearFt: 100, variant: loKey, height: 4, gates: 0, city: 'national' }).perFtLow;
    const hi = compute({ linearFt: 200, variant: hiKey, height: 8, gates: 2, city: 'national' }).perFtHigh;
    set('stat-avg-cost', `$${lo.toFixed(0)}–$${hi.toFixed(0)} per linear ft`);
  }

  function renderCalcPanel(r) {
    if (!r) return;
    const set = (id, t) => {
      const n = el(id);
      if (n) n.textContent = t;
    };
    const hint = r.gradeLabel
      ? `${r.linearFt} ft · ${r.variantLabel} · ${r.gradeLabel} · ${r.cityLabel}`
      : `${r.linearFt} ft · ${r.variantLabel} · ${r.cityLabel}`;
    set('fence-material-calc-range', formatRange(r.low, r.high));
    set('fence-material-calc-hint', hint);
    set('fence-material-calc-per-ft', `$${r.perFtLow.toFixed(0)}–$${r.perFtHigh.toFixed(0)} per linear ft installed`);
  }

  function renderCostRanges(cityKey) {
    const list = el('fence-material-cost-range-list');
    if (!list) return;
    const variant = document.querySelector('[name="fence_style"]:checked')?.value || el('fence-material-variant')?.value || defaultVariant;
    const grade = el('fence-material-grade')?.value || defaultGrade;
    const height = el('fence-material-height')?.value || '6';
    const gates = el('fence-material-gates')?.value ?? '1';
    const activeFt = Number(el('fence-material-length')?.value) || 150;
    [100, 150, 200].forEach((ft) => {
      const r = compute({ linearFt: ft, variant, grade, height, gates, city: cityKey });
      const card = list.querySelector(`[data-range-ft="${ft}"]`);
      if (!card) return;
      const price = card.querySelector('.wood-cost-benchmark-price');
      if (price) price.textContent = formatRange(r.low, r.high);
      card.classList.toggle('wood-cost-benchmark-card--active', activeFt === ft);
      card.classList.toggle('wood-cost-benchmark-card--near', activeFt !== ft && Math.abs(activeFt - ft) <= 25);
    });
  }

  function renderGradesTable(cityKey) {
    const tbody = el('fence-material-grades-tbody');
    if (!tbody || !Object.keys(GRADES).length) return;
    const ft = Number(el('fence-material-length')?.value) || 150;
    const variant = el('fence-material-variant')?.value || defaultVariant;
    tbody.innerHTML = Object.keys(GRADES)
      .map((key) => {
        const g = GRADES[key];
        const r = compute({ linearFt: ft, variant, grade: key, height: 6, gates: 1, city: cityKey });
        return `<tr>
          <td>${g.label}</td>
          <td>${formatRange(r.perFtLow, r.perFtHigh)} / ft</td>
          <td>${g.life || '—'}</td>
          <td>${g.look || '—'}</td>
        </tr>`;
      })
      .join('');
  }

  function renderLocalWeather(cityKey) {
    const card = el('fence-material-weather-city-card');
    const grid = el('fence-material-weather-grid');
    const title = el('fence-material-weather-city-title');
    const list = el('fence-material-weather-city-list');
    const isNational = !cityKey || cityKey === 'national';
    if (card) card.hidden = isNational;
    if (grid) {
      grid.classList.toggle('local-factors-grid--single', isNational);
      grid.classList.toggle('local-factors-grid--two', !isNational);
    }
    if (isNational || !title || !list) return;
    title.textContent =
      cityKey === 'phoenix' ? 'Arizona (Phoenix area)' : cityKey === 'tampa' ? 'Florida (Tampa area)' : cityKey === 'dallas' ? 'Texas (Dallas area)' : getCity(cityKey).label;
    list.innerHTML = `<li>${REGIONAL[cityKey] || REGIONAL.national || ''}</li>`;
  }

  function renderProjects(cityKey) {
    const isNational = !cityKey || cityKey === 'national';
    const natCard = document.querySelector('[data-project-city="national"]');
    const cityCard = el('fence-material-project-city-card');
    if (natCard) {
      const ex = HOME_EXAMPLES.national;
      const r = compute({
        linearFt: ex.ft,
        variant: ex.variant,
        grade: ex.grade,
        height: ex.height,
        gates: ex.gates,
        city: 'national',
      });
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
    const r = compute({
      linearFt: ex.ft,
      variant: ex.variant,
      grade: ex.grade,
      height: ex.height,
      gates: ex.gates,
      city: cityKey,
    });
    cityCard.hidden = false;
    cityCard.classList.add('project-example-card--active');
    if (natCard) natCard.classList.remove('project-example-card--active');
    const titleEl = cityCard.querySelector('[data-project-city-title]');
    const typeEl = cityCard.querySelector('[data-project-type]');
    const detailEl = cityCard.querySelector('[data-project-detail]');
    const costEl = cityCard.querySelector('[data-project-cost]');
    const vLabel = VARIANT[ex.variant]?.label || cfg.shortLabel;
    if (titleEl) titleEl.textContent = getCity(cityKey).label;
    if (typeEl) typeEl.textContent = `${ex.height} ft ${vLabel} · ${ex.ft} linear ft`;
    if (detailEl) detailEl.textContent = ex.detail;
    if (costEl) costEl.textContent = formatMoney(r.mid);
  }

  function updateVariantCards(fromSelect) {
    const sel = el('fence-material-variant');
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
    const cityKey = getCityValue(el('fence-material-city'));
    renderCostRanges(cityKey);
    renderGradesTable(cityKey);
    renderLocalWeather(cityKey);
    renderProjects(cityKey);
  }

  function bind() {
    const form = el('fence-material-calc-form');
    if (!form) return;
    form.addEventListener('input', updateAll);
    form.addEventListener('change', updateAll);
    document.querySelectorAll('[name="fence_style"]').forEach((input) => {
      input.addEventListener('change', () => {
        updateVariantCards(false);
        updateAll();
      });
    });
    const variantSel = el('fence-material-variant');
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

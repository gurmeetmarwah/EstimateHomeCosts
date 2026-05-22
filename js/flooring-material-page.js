/**
 * Flooring material landing pages — /flooring-materials/{slug}/
 * Requires window.FLOORING_MATERIAL_CONFIG on the page.
 */
(function () {
  'use strict';

  const cfg = window.FLOORING_MATERIAL_CONFIG;
  if (!cfg) return;

  const { getCity, getCityValue, locMult } = window.EHCCities || {
    getCity: () => ({ label: 'National average', material: 1, labor: 1 }),
    getCityValue: () => 'national',
    locMult: () => 1,
  };

  const MAT = { material: cfg.material, labor: cfg.labor };
  const PREP = { none: 1, minor: 1.06, major: 1.14 };
  const REMOVAL = 1.25;
  const VARIANT = cfg.variants || {};
  const GRADES = cfg.grades || {};
  const WEAR = cfg.wear || {};
  const REGIONAL = cfg.regional || {};
  const HOME_EXAMPLES = cfg.homeExamples || {};
  const BENCHMARKS = cfg.benchmarks || [500, 1000];
  const defaultVariant = cfg.defaultVariant || Object.keys(VARIANT)[0];
  const defaultGrade = cfg.defaultGrade || Object.keys(GRADES)[0] || null;
  const defaultWear = cfg.defaultWear || '12';
  const hasGrades = Object.keys(GRADES).length > 0;
  const hasWear = Object.keys(WEAR).length > 0;

  function formatMoney(n) {
    return '$' + Math.round(n).toLocaleString('en-US');
  }

  function formatRange(low, high) {
    return `${formatMoney(low)}–${formatMoney(high)}`;
  }

  function compute(opts) {
    const sqft = Math.max(100, Math.min(5000, Number(opts.sqft) || 500));
    const variant = VARIANT[opts.variant] || VARIANT[defaultVariant] || { mult: 1, label: cfg.shortLabel };
    const grade = GRADES[opts.grade] || (defaultGrade ? GRADES[defaultGrade] : null) || { mult: 1 };
    const wear = WEAR[opts.wear] || (hasWear ? WEAR[defaultWear] : null) || { mult: 1 };
    const prepMult = PREP[opts.prep] || PREP.minor;
    const city = getCity(opts.city || 'national');
    const mult = locMult(city);
    const remove = opts.removal === true || opts.removal === 'yes';
    const styleMult = variant.mult * (grade.mult || 1) * (wear.mult || 1);

    const baseMult = prepMult * mult * styleMult;
    const materialCost = sqft * MAT.material * baseMult;
    const laborCost = sqft * MAT.labor * baseMult;
    const removalCost = remove ? sqft * REMOVAL * mult : 0;
    const total = materialCost + laborCost + removalCost;
    const low = total * 0.9;
    const high = total * 1.1;

    return {
      sqft,
      low,
      high,
      mid: total,
      perSqftLow: low / sqft,
      perSqftHigh: high / sqft,
      cityLabel: city.label,
      variantLabel: variant.label,
      gradeLabel: grade.label || '',
      wearLabel: wear.label || '',
    };
  }

  function el(id) {
    return document.getElementById(id);
  }

  function readCalc() {
    return compute({
      sqft: el('flooring-material-sqft')?.value,
      variant: el('flooring-material-variant')?.value || defaultVariant,
      grade: el('flooring-material-grade')?.value || defaultGrade,
      wear: el('flooring-material-wear')?.value || defaultWear,
      prep: el('flooring-material-prep')?.value || 'minor',
      removal: el('flooring-material-removal')?.value === 'yes',
      city: getCityValue(el('flooring-material-city')),
    });
  }

  function hintText(r) {
    const parts = [`${r.sqft.toLocaleString()} sq ft`, r.variantLabel];
    if (r.gradeLabel) parts.push(r.gradeLabel);
    if (r.wearLabel && hasWear) parts.push(r.wearLabel);
    parts.push(r.cityLabel);
    return parts.join(' · ');
  }

  function renderHero(r) {
    if (!r) return;
    const set = (id, t) => {
      const n = el(id);
      if (n) n.textContent = t;
    };
    set('hero-cost-range', formatRange(r.low, r.high));
    set('hero-per-ft', `$${r.perSqftLow.toFixed(2)}–$${r.perSqftHigh.toFixed(2)} per sq ft · ${r.sqft.toLocaleString()} sq ft`);
    const vKeys = Object.keys(VARIANT);
    const lo = compute({
      sqft: 100,
      variant: vKeys[0],
      grade: defaultGrade,
      wear: hasWear ? '6' : defaultWear,
      prep: 'none',
      city: 'national',
    }).perSqftLow;
    const hi = compute({
      sqft: 500,
      variant: vKeys[vKeys.length - 1],
      grade: Object.keys(GRADES).pop() || defaultGrade,
      wear: hasWear ? '28' : defaultWear,
      prep: 'major',
      removal: true,
      city: 'national',
    }).perSqftHigh;
    set('stat-avg-cost', `$${lo.toFixed(0)}–$${hi.toFixed(0)} per sq ft`);
  }

  function renderCalcPanel(r) {
    if (!r) return;
    const set = (id, t) => {
      const n = el(id);
      if (n) n.textContent = t;
    };
    set('flooring-material-calc-range', formatRange(r.low, r.high));
    set('flooring-material-calc-hint', hintText(r));
    set('flooring-material-calc-per-sqft', `$${r.perSqftLow.toFixed(2)}–$${r.perSqftHigh.toFixed(2)} per sq ft installed`);
  }

  function renderCostRanges(cityKey) {
    const list = el('flooring-material-cost-range-list');
    if (!list) return;
    const variant = document.querySelector('[name="flooring_style"]:checked')?.value || el('flooring-material-variant')?.value || defaultVariant;
    const grade = el('flooring-material-grade')?.value || defaultGrade;
    const wear = el('flooring-material-wear')?.value || defaultWear;
    const prep = el('flooring-material-prep')?.value || 'minor';
    const removal = el('flooring-material-removal')?.value === 'yes';
    const activeSqft = Number(el('flooring-material-sqft')?.value) || 500;
    BENCHMARKS.forEach((sqft) => {
      const r = compute({ sqft, variant, grade, wear, prep, removal, city: cityKey });
      const card = list.querySelector(`[data-range-sqft="${sqft}"]`);
      if (!card) return;
      const price = card.querySelector('.flooring-benchmark-price');
      if (price) price.textContent = formatRange(r.low, r.high);
      const near = BENCHMARKS.some((b) => b !== sqft && Math.abs(activeSqft - b) <= Math.min(250, b * 0.25));
      card.classList.toggle('wood-cost-benchmark-card--active', activeSqft === sqft);
      card.classList.toggle('wood-cost-benchmark-card--near', activeSqft !== sqft && Math.abs(activeSqft - sqft) <= 250);
    });
  }

  function renderDetailTable(cityKey) {
    const tbody = el('flooring-material-detail-tbody');
    if (!tbody) return;
    const sqft = Number(el('flooring-material-sqft')?.value) || 500;
    const variant = el('flooring-material-variant')?.value || defaultVariant;
    const prep = el('flooring-material-prep')?.value || 'minor';
    const rows = hasWear ? Object.keys(WEAR) : Object.keys(GRADES);
    const data = hasWear ? WEAR : GRADES;
    tbody.innerHTML = rows
      .map((key) => {
        const row = data[key];
        const opts = hasWear ? { sqft, variant, wear: key, prep, city: cityKey } : { sqft, variant, grade: key, prep, city: cityKey };
        const r = compute(opts);
        const col2 = row.bestFor || row.life || '—';
        return `<tr>
          <td>${row.label}</td>
          <td>${col2}</td>
          <td>${formatRange(r.perSqftLow, r.perSqftHigh)} / sq ft</td>
        </tr>`;
      })
      .join('');
  }

  function renderLocalWeather(cityKey) {
    const card = el('flooring-material-weather-city-card');
    const grid = el('flooring-material-weather-grid');
    const title = el('flooring-material-weather-city-title');
    const list = el('flooring-material-weather-city-list');
    const isNational = !cityKey || cityKey === 'national';
    if (card) card.hidden = isNational;
    if (grid) {
      grid.classList.toggle('local-factors-grid--single', isNational);
      grid.classList.toggle('local-factors-grid--two', !isNational);
    }
    if (isNational || !title || !list) return;
    title.textContent = getCity(cityKey).label;
    list.innerHTML = `<li>${REGIONAL[cityKey] || REGIONAL.national || ''}</li>`;
  }

  function renderProjects(cityKey) {
    const isNational = !cityKey || cityKey === 'national';
    const natCard = document.querySelector('[data-project-city="national"]');
    const cityCard = el('flooring-material-project-city-card');
    const natEx = HOME_EXAMPLES.national || HOME_EXAMPLES[Object.keys(HOME_EXAMPLES)[0]];
    if (natCard && natEx) {
      const r = compute({
        sqft: natEx.sqft,
        variant: natEx.variant,
        grade: natEx.grade,
        wear: natEx.wear,
        prep: natEx.prep,
        removal: natEx.removal,
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
    const ex = HOME_EXAMPLES[cityKey] || natEx;
    const r = compute({
      sqft: ex.sqft,
      variant: ex.variant,
      grade: ex.grade,
      wear: ex.wear,
      prep: ex.prep,
      removal: ex.removal,
      city: cityKey,
    });
    cityCard.hidden = false;
    cityCard.classList.add('project-example-card--active');
    if (natCard) natCard.classList.remove('project-example-card--active');
    const titleEl = cityCard.querySelector('[data-project-city-title]');
    const typeEl = cityCard.querySelector('[data-project-type]');
    const detailEl = cityCard.querySelector('[data-project-detail]');
    const costEl = cityCard.querySelector('[data-project-cost]');
    if (titleEl) titleEl.textContent = getCity(cityKey).label;
    if (typeEl) typeEl.textContent = `${ex.sqft.toLocaleString()} sq ft · ${VARIANT[ex.variant]?.label || cfg.shortLabel}`;
    if (detailEl) detailEl.textContent = ex.detail;
    if (costEl) costEl.textContent = formatMoney(r.mid);
  }

  function updateVariantCards(fromSelect) {
    const sel = el('flooring-material-variant');
    const variant = fromSelect
      ? sel?.value
      : document.querySelector('[name="flooring_style"]:checked')?.value || sel?.value;
    if (sel && variant) sel.value = variant;
    document.querySelectorAll('[name="flooring_style"]').forEach((input) => {
      if (input.value === variant) input.checked = true;
    });
    document.querySelectorAll('[data-flooring-variant-card]').forEach((card) => {
      card.classList.toggle('fence-variant-card--active', card.dataset.flooringVariantCard === variant);
    });
  }

  function updateAll() {
    const r = readCalc();
    renderHero(r);
    renderCalcPanel(r);
    const cityKey = getCityValue(el('flooring-material-city'));
    renderCostRanges(cityKey);
    renderDetailTable(cityKey);
    renderLocalWeather(cityKey);
    renderProjects(cityKey);
  }

  function bind() {
    const form = el('flooring-material-calc-form');
    if (!form) return;
    form.addEventListener('input', updateAll);
    form.addEventListener('change', updateAll);
    document.querySelectorAll('[name="flooring_style"]').forEach((input) => {
      input.addEventListener('change', () => {
        updateVariantCards(false);
        updateAll();
      });
    });
    const variantSel = el('flooring-material-variant');
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

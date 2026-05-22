/**
 * Luxury vinyl plank landing page — /flooring-materials/luxury-vinyl-plank-flooring-cost/
 */
(function () {
  'use strict';

  const { getCity, getCityValue, locMult } = window.EHCCities || {
    getCity: () => ({ label: 'National average', material: 1, labor: 1 }),
    getCityValue: () => 'national',
    locMult: () => 1,
  };

  const MAT = { material: 3.2, labor: 2.8 };
  const PREP = { none: 1, minor: 1.06, major: 1.14 };
  const REMOVAL = 1.25;
  const VARIANT = {
    'glue-down': { mult: 1.02, label: 'Glue-down LVP' },
    'click-lock': { mult: 1, label: 'Click-lock LVP' },
    spc: { mult: 1.1, label: 'SPC flooring' },
    wpc: { mult: 1.06, label: 'WPC flooring' },
    waterproof: { mult: 1.14, label: 'Waterproof LVP' },
  };
  const WEAR = {
    6: { mult: 0.92, label: '6 mil' },
    12: { mult: 1, label: '12 mil' },
    20: { mult: 1.12, label: '20 mil' },
    28: { mult: 1.22, label: '28 mil' },
  };

  const REGIONAL = {
    national: 'Minor subfloor leveling is typical before floating LVP on concrete slabs',
    dallas: 'Slab homes favor SPC and waterproof LVP — fast installs on main levels',
    austin: 'Wood-look LVP popular in open-concept remodels and rental turnovers',
    phoenix: 'Rigid core handles heat and slab movement better than laminate',
    tampa: 'Waterproof LVP dominates baths, laundry, and slab-on-grade homes',
    houston: 'Humidity — use rated moisture barriers on concrete before click-lock',
    charlotte: 'Builder-grade click-lock common; upgrades to 20 mil in high-traffic areas',
    'san-diego': 'Coastal condos — waterproof rigid core over sound underlayment',
  };

  const HOME_EXAMPLES = {
    national: { sqft: 1000, variant: 'spc', wear: 12, prep: 'minor', removal: false, detail: '1,000 sq ft wood-look SPC · main level' },
    austin: { sqft: 1200, variant: 'spc', wear: 20, prep: 'minor', removal: true, detail: '1,200 sq ft SPC · wood-look · tear-out included' },
    dallas: { sqft: 900, variant: 'click-lock', wear: 12, prep: 'minor', removal: false, detail: '900 sq ft click-lock LVP · living + halls' },
    tampa: { sqft: 800, variant: 'waterproof', wear: 20, prep: 'major', removal: false, detail: '800 sq ft waterproof LVP · bath + kitchen' },
  };

  function formatMoney(n) {
    return '$' + Math.round(n).toLocaleString('en-US');
  }

  function formatRange(low, high) {
    return `${formatMoney(low)}–${formatMoney(high)}`;
  }

  function compute(opts) {
    const sqft = Math.max(100, Math.min(5000, Number(opts.sqft) || 500));
    const variant = VARIANT[opts.variant] || VARIANT['click-lock'];
    const wear = WEAR[opts.wear] || WEAR[12];
    const prepMult = PREP[opts.prep] || PREP.minor;
    const city = getCity(opts.city || 'national');
    const mult = locMult(city);
    const remove = opts.removal === true || opts.removal === 'yes';
    const styleMult = variant.mult * wear.mult;

    const baseMult = prepMult * mult * styleMult;
    const materialCost = sqft * MAT.material * baseMult;
    const laborCost = sqft * MAT.labor * baseMult;
    const removalCost = remove ? sqft * REMOVAL * mult : 0;
    const total = materialCost + laborCost + removalCost;
    const low = total * 0.9;
    const high = total * 1.1;
    const perSqftLow = low / sqft;
    const perSqftHigh = high / sqft;

    return {
      sqft,
      low,
      high,
      mid: total,
      perSqftLow,
      perSqftHigh,
      cityLabel: city.label,
      cityKey: opts.city || 'national',
      variantLabel: variant.label,
      wearLabel: wear.label,
    };
  }

  function el(id) {
    return document.getElementById(id);
  }

  function readCalc() {
    return compute({
      sqft: el('lvp-sqft')?.value,
      variant: el('lvp-variant')?.value || 'click-lock',
      wear: el('lvp-wear')?.value || '12',
      prep: el('lvp-prep')?.value || 'minor',
      removal: el('lvp-removal')?.value === 'yes',
      city: getCityValue(el('lvp-city')),
    });
  }

  function renderHero(r) {
    if (!r) return;
    const set = (id, t) => {
      const n = el(id);
      if (n) n.textContent = t;
    };
    set('hero-cost-range', formatRange(r.low, r.high));
    set('hero-per-ft', `$${r.perSqftLow.toFixed(2)}–$${r.perSqftHigh.toFixed(2)} per sq ft installed`);
    const lo = compute({ sqft: 100, variant: 'glue-down', wear: 6, prep: 'none', city: 'national' }).perSqftLow;
    const hi = compute({ sqft: 500, variant: 'waterproof', wear: 28, prep: 'major', removal: true, city: 'national' }).perSqftHigh;
    set('stat-avg-cost', `$${lo.toFixed(0)}–$${hi.toFixed(0)} per sq ft`);
  }

  function renderCalcPanel(r) {
    if (!r) return;
    const set = (id, t) => {
      const n = el(id);
      if (n) n.textContent = t;
    };
    set('lvp-calc-range', formatRange(r.low, r.high));
    set('lvp-calc-hint', `${r.sqft.toLocaleString()} sq ft · ${r.variantLabel} · ${r.wearLabel} · ${r.cityLabel}`);
    set('lvp-calc-per-sqft', `$${r.perSqftLow.toFixed(2)}–$${r.perSqftHigh.toFixed(2)} per sq ft installed`);
  }

  function renderCostRanges(cityKey) {
    const list = el('lvp-cost-range-list');
    if (!list) return;
    const variant = document.querySelector('[name="lvp_style"]:checked')?.value || el('lvp-variant')?.value || 'click-lock';
    const wear = el('lvp-wear')?.value || '12';
    const prep = el('lvp-prep')?.value || 'minor';
    const removal = el('lvp-removal')?.value === 'yes';
    const activeSqft = Number(el('lvp-sqft')?.value) || 500;
    [500, 1000].forEach((sqft) => {
      const r = compute({ sqft, variant, wear, prep, removal, city: cityKey });
      const card = list.querySelector(`[data-range-sqft="${sqft}"]`);
      if (!card) return;
      const price = card.querySelector('.flooring-benchmark-price');
      if (price) price.textContent = formatRange(r.low, r.high);
      card.classList.toggle('wood-cost-benchmark-card--active', activeSqft === sqft);
      card.classList.toggle('wood-cost-benchmark-card--near', activeSqft !== sqft && Math.abs(activeSqft - sqft) <= 250);
    });
  }

  function renderWearTable(cityKey) {
    const tbody = el('lvp-wear-tbody');
    if (!tbody) return;
    const sqft = Number(el('lvp-sqft')?.value) || 500;
    const variant = el('lvp-variant')?.value || 'click-lock';
    const prep = el('lvp-prep')?.value || 'minor';
    tbody.innerHTML = Object.keys(WEAR)
      .map((mil) => {
        const w = WEAR[mil];
        const r = compute({ sqft, variant, wear: mil, prep, city: cityKey });
        const bestFor = { 6: 'Light residential', 12: 'Standard residential', 20: 'High traffic / pets', 28: 'Commercial-grade' }[mil];
        return `<tr>
          <td>${w.label}</td>
          <td>${bestFor}</td>
          <td>${formatRange(r.perSqftLow, r.perSqftHigh)} / sq ft</td>
        </tr>`;
      })
      .join('');
  }

  function renderLocalWeather(cityKey) {
    const card = el('lvp-weather-city-card');
    const grid = el('lvp-weather-grid');
    const title = el('lvp-weather-city-title');
    const list = el('lvp-weather-city-list');
    const isNational = !cityKey || cityKey === 'national';
    if (card) card.hidden = isNational;
    if (grid) {
      grid.classList.toggle('local-factors-grid--single', isNational);
      grid.classList.toggle('local-factors-grid--two', !isNational);
    }
    if (isNational || !title || !list) return;
    title.textContent = getCity(cityKey).label;
    list.innerHTML = `<li>${REGIONAL[cityKey] || REGIONAL.national}</li>`;
  }

  function renderProjects(cityKey) {
    const isNational = !cityKey || cityKey === 'national';
    const natCard = document.querySelector('[data-project-city="national"]');
    const cityCard = el('lvp-project-city-card');
    if (natCard) {
      const ex = HOME_EXAMPLES.national;
      const r = compute({
        sqft: ex.sqft,
        variant: ex.variant,
        wear: ex.wear,
        prep: ex.prep,
        removal: ex.removal,
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
      sqft: ex.sqft,
      variant: ex.variant,
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
    if (typeEl) typeEl.textContent = `${ex.sqft.toLocaleString()} sq ft ${VARIANT[ex.variant].label}`;
    if (detailEl) detailEl.textContent = ex.detail;
    if (costEl) costEl.textContent = formatMoney(r.mid);
  }

  function updateVariantCards(fromSelect) {
    const sel = el('lvp-variant');
    const variant = fromSelect
      ? sel?.value
      : document.querySelector('[name="lvp_style"]:checked')?.value || sel?.value;
    if (sel && variant) sel.value = variant;
    document.querySelectorAll('[name="lvp_style"]').forEach((input) {
      if (input.value === variant) input.checked = true;
    });
    document.querySelectorAll('[data-lvp-variant-card]').forEach((card) => {
      card.classList.toggle('fence-variant-card--active', card.dataset.lvpVariantCard === variant);
    });
  }

  function updateAll() {
    const r = readCalc();
    renderHero(r);
    renderCalcPanel(r);
    const cityKey = getCityValue(el('lvp-city'));
    renderCostRanges(cityKey);
    renderWearTable(cityKey);
    renderLocalWeather(cityKey);
    renderProjects(cityKey);
  }

  function bind() {
    const form = el('lvp-calc-form');
    if (!form) return;
    form.addEventListener('input', updateAll);
    form.addEventListener('change', updateAll);
    document.querySelectorAll('[name="lvp_style"]').forEach((input) => {
      input.addEventListener('change', () => {
        updateVariantCards(false);
        updateAll();
      });
    });
    const variantSel = el('lvp-variant');
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

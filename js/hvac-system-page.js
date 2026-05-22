/**
 * Shared HVAC system landing page calculator — /hvac-cost-calculator/{system}/
 */
(function () {
  'use strict';

  const cfg = window.HVAC_SYSTEM_CONFIG;
  if (!cfg) return;

  const { getCity, getCityValue, locMult } = window.EHCCities || {
    getCity: () => ({ label: 'National average', material: 1, labor: 1, permit: 275 }),
    getCityValue: () => 'national',
    locMult: () => 1,
  };

  const BASE_RATE = 4.05;
  const TON_BASE = { 2: 3.65, 3: 4.05, 4: 4.55, 5: 5.05 };
  const SEER = {
    14: { mult: 1, label: '14 SEER', savings: 'Baseline efficiency' },
    16: { mult: 1.14, label: '16 SEER', savings: '~12% lower energy bills vs 14 SEER' },
    18: { mult: 1.22, label: '18 SEER', savings: '~20% lower energy bills vs 14 SEER' },
    20: { mult: 1.28, label: '20+ SEER', savings: '~28% lower energy bills vs 14 SEER' },
  };
  const CLIMATE = { hot: 1.06, moderate: 1, mild: 0.97 };
  const STAGE = { single: 1, two: 1.09, variable: 1.2 };
  const DUCT_BASE = 2800;
  const SMART_THERMOSTAT = 385;
  const rateMult = (cfg.systemRate || BASE_RATE) / BASE_RATE;

  function tonRate(ton) {
    return (TON_BASE[ton] || TON_BASE[3]) * rateMult;
  }

  function formatMoney(n) {
    return '$' + Math.round(n).toLocaleString('en-US');
  }

  function formatRange(low, high) {
    const plus = cfg.plusHigh && high >= (cfg.plusThreshold || 30000);
    return plus ? `${formatMoney(low)}–${formatMoney(high)}+` : `${formatMoney(low)}–${formatMoney(high)}`;
  }

  function recommendTon(sqft, climate) {
    const div = climate === 'hot' ? 500 : climate === 'mild' ? 650 : 600;
    return Math.max(2, Math.min(5, Math.round((sqft / div) * 2) / 2));
  }

  function monthlyPayment(principal, months = 120, annualRate = 0.079) {
    const r = annualRate / 12;
    if (r <= 0) return principal / months;
    return (principal * r) / (1 - Math.pow(1 + r, -months));
  }

  function compute(opts) {
    const sqft = Math.max(1000, Math.min(5000, Number(opts.sqft) || cfg.defaultSqft || 2200));
    const climate = CLIMATE[opts.climate] ? opts.climate : 'moderate';
    const ton = Number(opts.ton) || recommendTon(sqft, climate);
    const seerKey = SEER[opts.seer] ? opts.seer : 16;
    const seer = SEER[seerKey];
    const city = getCity(opts.city || 'national');
    const mult = locMult(city);
    const stageMult = cfg.showStage === false ? 1 : STAGE[opts.stage] || 1;
    const ductwork = opts.ductwork === true;
    const smart = opts.smartThermostat === true;

    const core = sqft * tonRate(ton) * seer.mult * mult * CLIMATE[climate] * stageMult;
    const duct = ductwork ? DUCT_BASE * (sqft / 2000) * mult : 0;
    const smartCost = smart ? SMART_THERMOSTAT * mult : 0;
    const permits = city.permit;
    const geoPremium = cfg.geoPremium ? core * 0.12 : 0;

    const equipment = core * 0.45 + geoPremium * 0.6;
    const labor = core * 0.3 + geoPremium * 0.35;
    const misc = core * 0.05 + smartCost;
    const total = equipment + labor + misc + duct + permits;
    const low = total * 0.92;
    const high = total * 1.08;

    const parts = [
      { key: 'equipment', label: 'Equipment', amount: equipment },
      { key: 'labor', label: 'Labor', amount: labor },
      { key: 'duct', label: 'Ductwork', amount: duct },
      { key: 'permits', label: 'Permits', amount: permits },
      { key: 'misc', label: 'Miscellaneous', amount: misc },
    ].filter((p) => p.amount > 0);

    return {
      sqft,
      ton,
      seerKey,
      seerLabel: seer.label,
      low,
      high,
      mid: total,
      perSqft: total / sqft,
      parts,
      financing: monthlyPayment(total),
      cityKey: opts.city || 'national',
      cityLabel: city.label,
      recommendedTon: recommendTon(sqft, climate),
    };
  }

  const formId = cfg.formId || 'hvac-system-calculator';
  const quickFormId = cfg.quickFormId || 'quick-hvac-calc';

  function readQuick() {
    return compute({
      sqft: document.getElementById('quick-sqft')?.value,
      ton: document.getElementById('quick-ton')?.value,
      seer: document.getElementById('quick-seer')?.value,
      ductwork: cfg.defaultDuctwork === true,
      climate: 'moderate',
      stage: 'single',
      smartThermostat: false,
      city: getCityValue(document.getElementById('quick-city')),
    });
  }

  function readAdvanced() {
    const form = document.getElementById(formId);
    if (!form) return null;
    return compute({
      sqft: document.getElementById('ac-size')?.value,
      ton: form.querySelector('[name="ac_ton"]:checked')?.value,
      seer: form.querySelector('[name="ac_seer"]:checked')?.value,
      ductwork: cfg.showDuctwork === false ? false : form.querySelector('[name="ductwork"]:checked')?.value === 'yes',
      climate: form.querySelector('[name="climate"]:checked')?.value || 'moderate',
      stage: form.querySelector('[name="ac_stage"]:checked')?.value || 'single',
      smartThermostat: document.getElementById('ac-smart-thermostat')?.checked,
      city: getCityValue(document.getElementById('ac-city')),
    });
  }

  function syncQuickToAdvanced() {
    const sqft = document.getElementById('quick-sqft')?.value;
    const ton = document.getElementById('quick-ton')?.value;
    const seer = document.getElementById('quick-seer')?.value;
    const city = document.getElementById('quick-city')?.value;
    const size = document.getElementById('ac-size');
    const slider = document.getElementById('ac-size-slider');
    if (size && sqft) {
      size.value = sqft;
      if (slider) slider.value = sqft;
    }
    const form = document.getElementById(formId);
    if (form && ton) {
      const t = form.querySelector(`[name="ac_ton"][value="${ton}"]`);
      if (t) t.checked = true;
    }
    if (form && seer) {
      const s = form.querySelector(`[name="ac_seer"][value="${seer}"]`);
      if (s) s.checked = true;
    }
    const advCity = document.getElementById('ac-city');
    if (advCity && city) advCity.value = city;
  }

  function set(id, t) {
    const n = document.getElementById(id);
    if (n) n.textContent = t;
  }

  function renderHeroPreview(r) {
    if (!r) return;
    set('hero-preview-sqft', `${r.sqft.toLocaleString()} sq ft`);
    set('hero-preview-ton', `${r.ton} ${cfg.tonUnit || 'Ton'}`);
    set('hero-preview-range', formatRange(r.low, r.high));
    const lo = compute({ sqft: cfg.heroLowSqft || 1000, ton: 2, seer: 14, city: 'national' }).low;
    const hi = compute({ sqft: cfg.heroHighSqft || 3000, ton: 5, seer: 20, city: 'national' }).high;
    set('hero-avg-cost', formatRange(lo, hi));
  }

  function renderQuick(r) {
    if (!r) return;
    set('quick-result-range', formatRange(r.low, r.high));
    set('quick-result-hint', `${r.ton}-ton · ${r.seerLabel} · ${r.cityLabel}`);
  }

  function renderAdvanced(r) {
    if (!r) return;
    set('calc-total-range', formatRange(r.low, r.high));
    set('calc-total-mid', `~${formatMoney(r.mid)} typical · ${r.cityLabel}`);
    set('calc-per-sqft', `$${r.perSqft.toFixed(2)} per sq ft`);
    set('calc-financing', `${formatMoney(r.financing)}/mo`);
    set('calc-financing-note', `Est. ${formatMoney(r.mid)} at 7.9% APR · 10 yr term`);
    const total = r.mid || 1;
    r.parts.forEach((p) => {
      const pct = Math.round((p.amount / total) * 100);
      const bar = document.querySelector(`[data-breakdown="${p.key}"]`);
      const val = document.getElementById(`breakdown-${p.key}`);
      if (bar) bar.style.width = pct + '%';
      if (val) val.textContent = `${formatMoney(p.amount)} (${pct}%)`;
    });
    const list = document.getElementById('calc-line-items');
    if (list) {
      list.innerHTML = r.parts.map((p) => `<li><span>${p.label}</span><strong>${formatMoney(p.amount)}</strong></li>`).join('');
    }
    set('ac-recommended-ton', `${r.recommendedTon} ton`);
  }

  function renderSizeTable(cityKey) {
    const tbody = document.getElementById('ac-size-table-body');
    if (!tbody) return;
    tbody.innerHTML = [1000, 1500, 2000, 3000]
      .map((sqft) => {
        const r = compute({ sqft, ton: recommendTon(sqft, 'moderate'), seer: 16, ductwork: cfg.defaultDuctwork, city: cityKey });
        return `<tr><td>${sqft.toLocaleString()} sq ft</td><td>${formatRange(r.low, r.high)}</td><td>~${r.ton} ton</td></tr>`;
      })
      .join('');
  }

  function renderSeerTable(cityKey) {
    const tbody = document.getElementById('ac-seer-table-body');
    if (!tbody) return;
    const sqft = getActiveSqft();
    const ton = recommendTon(sqft, 'moderate');
    tbody.innerHTML = Object.keys(SEER)
      .map((k) => {
        const r = compute({ sqft, ton, seer: Number(k), ductwork: cfg.defaultDuctwork, city: cityKey });
        return `<tr><td>${SEER[k].label}</td><td>${formatRange(r.low, r.high)}</td><td>${SEER[k].savings}</td></tr>`;
      })
      .join('');
  }

  function renderLocalFactors(cityKey) {
    const card = document.getElementById('local-factor-city-card');
    const grid = document.getElementById('local-factors-grid');
    const title = document.getElementById('local-factor-city-title');
    const list = document.getElementById('local-factor-city-list');
    const natList = document.getElementById('local-factor-national-list');
    const isNational = !cityKey || cityKey === 'national';
    const regional = cfg.regional || {};

    if (card) card.hidden = isNational;
    if (grid) {
      grid.classList.toggle('local-factors-grid--single', isNational);
      grid.classList.toggle('local-factors-grid--two', !isNational);
    }
    const rNat = compute({ sqft: 2000, ton: 3, seer: 16, ductwork: cfg.defaultDuctwork, city: 'national' });
    if (natList) {
      const bullets = cfg.nationalFactorBullets || [
        `<li><strong>2,000 sq ft · 3-ton · 16 SEER:</strong> ${formatRange(rNat.low, rNat.high)}</li>`,
        `<li><strong>Peak season:</strong> Summer and winter HVAC demand</li>`,
      ];
      if (!cfg.nationalFactorBullets) {
        natList.innerHTML = bullets.join('');
      }
    }
    if (isNational || !title || !list) return;
    const city = getCity(cityKey);
    const mult = locMult(city);
    const pct = Math.round(Math.abs(mult - 1) * 100);
    const multText =
      mult < 0.995 ? `~${pct}% below national` : mult > 1.005 ? `~${pct}% above national` : 'Near national average';
    title.textContent = city.label;
    const r3 = compute({ sqft: 2000, ton: 3, seer: 16, ductwork: cfg.defaultDuctwork, city: cityKey });
    list.innerHTML = [
      `<li><strong>Cost vs national:</strong> ${multText}</li>`,
      `<li><strong>2,000 sq ft · 3-ton · 16 SEER:</strong> ${formatRange(r3.low, r3.high)}</li>`,
      `<li><strong>Labor index:</strong> ${(city.labor * 100).toFixed(0)}% of national</li>`,
      `<li><strong>Local factors:</strong> ${regional[cityKey] || regional.national || ''}</li>`,
    ].join('');
  }

  function syncCitySelects(fromQuick) {
    const quick = document.getElementById('quick-city');
    const adv = document.getElementById('ac-city');
    if (!quick || !adv) return;
    if (fromQuick) adv.value = quick.value;
    else quick.value = adv.value;
  }

  function renderProjectExamples(cityKey) {
    const isNational = !cityKey || cityKey === 'national';
    const natCard = document.querySelector('[data-project-city="national"]');
    const cityCard = document.getElementById('project-example-city-card');
    const examples = cfg.homeExamples || {};
    if (natCard) {
      natCard.hidden = false;
      const ex = examples.national || { sqft: 2000, seer: 16, ton: 3, detail: 'Standard install' };
      const r = compute({ sqft: ex.sqft, ton: ex.ton, seer: ex.seer, city: 'national' });
      const natCost = natCard.querySelector('[data-project-cost]');
      if (natCost) natCost.textContent = formatMoney(r.mid);
      natCard.classList.toggle('project-example-card--active', isNational);
    }
    if (!cityCard) return;
    if (isNational) {
      cityCard.hidden = true;
      return;
    }
    const ex = examples[cityKey] || {
      sqft: getActiveSqft(),
      seer: 16,
      ton: recommendTon(getActiveSqft(), 'moderate'),
      detail: `Typical ${cfg.projectLabel || 'install'}`,
    };
    const city = getCity(cityKey);
    const r = compute({ sqft: ex.sqft, ton: ex.ton, seer: ex.seer, city: cityKey });
    cityCard.hidden = false;
    cityCard.classList.add('project-example-card--active');
    if (natCard) natCard.classList.remove('project-example-card--active');
    const label = cfg.systemName || 'System';
    const titleEl = cityCard.querySelector('[data-project-city-title]');
    const typeEl = cityCard.querySelector('[data-project-type]');
    const detailEl = cityCard.querySelector('[data-project-detail]');
    const costEl = cityCard.querySelector('[data-project-cost]');
    if (titleEl) titleEl.textContent = city.label;
    if (typeEl) typeEl.textContent = `${ex.seer} SEER ${label} · ${ex.sqft.toLocaleString()} sq ft`;
    if (detailEl) detailEl.textContent = ex.detail;
    if (costEl) costEl.textContent = formatMoney(r.mid);
  }

  function getActiveSqft() {
    return Math.max(
      1000,
      Math.min(5000, Number(document.getElementById('ac-size')?.value || document.getElementById('quick-sqft')?.value) || cfg.defaultSqft || 2200)
    );
  }

  function applyRecommendedTon() {
    const sqft = getActiveSqft();
    const climate = document.querySelector('[name="climate"]:checked')?.value || 'moderate';
    const ton = recommendTon(sqft, climate);
    const form = document.getElementById(formId);
    const qTon = document.getElementById('quick-ton');
    if (form) {
      const input = form.querySelector(`[name="ac_ton"][value="${ton}"]`);
      if (input) input.checked = true;
    }
    if (qTon) qTon.value = String(ton);
    updateAll();
  }

  function updateAll(fromQuick) {
    if (typeof fromQuick === 'boolean') syncCitySelects(fromQuick);
    const quick = readQuick();
    const advanced = readAdvanced();
    if (quick) {
      renderQuick(quick);
      renderHeroPreview(quick);
    }
    if (advanced) renderAdvanced(advanced);
    const cityKey = getCityValue(document.getElementById('ac-city')) || getCityValue(document.getElementById('quick-city'));
    renderSizeTable(cityKey);
    renderSeerTable(cityKey);
    renderLocalFactors(cityKey);
    renderProjectExamples(cityKey);
  }

  function bindQuick() {
    const form = document.getElementById(quickFormId);
    if (!form) return;
    form.addEventListener('input', () => updateAll(true));
    form.addEventListener('change', () => updateAll(true));
    document.getElementById('quick-calc-btn')?.addEventListener('click', (e) => {
      e.preventDefault();
      syncQuickToAdvanced();
      updateAll(true);
      document.getElementById('calculator')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
    updateAll();
  }

  function bindAdvanced() {
    const form = document.getElementById(formId);
    if (!form) return;
    const sizeInput = document.getElementById('ac-size');
    const sizeSlider = document.getElementById('ac-size-slider');
    const sizeLabel = document.getElementById('ac-size-label');

    function syncSize(from) {
      const v = Math.max(1000, Math.min(5000, Number(from === 'slider' ? sizeSlider.value : sizeInput.value) || cfg.defaultSqft || 2200));
      sizeInput.value = v;
      sizeSlider.value = v;
      if (sizeLabel) sizeLabel.textContent = `${v.toLocaleString()} sq ft`;
      const q = document.getElementById('quick-sqft');
      if (q) q.value = v;
      updateAll();
    }

    sizeInput?.addEventListener('input', () => syncSize('input'));
    sizeSlider?.addEventListener('input', () => syncSize('slider'));
    document.getElementById('ac-recommend-ton')?.addEventListener('click', (e) => {
      e.preventDefault();
      applyRecommendedTon();
    });
    document.getElementById('ac-city')?.addEventListener('change', () => updateAll(false));
    ['input', 'change'].forEach((evt) => {
      form.addEventListener(evt, (e) => {
        if (e.target.id === 'ac-city') return;
        updateAll(false);
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
})();

/**
 * Solar Panel Cost Calculator — quick + advanced estimates
 */
(function () {
  'use strict';

  const { getCity, getCityValue, locMult } = window.EHCCities || {
    getCity: () => ({ label: 'National average', material: 1, labor: 1 }),
    getCityValue: () => 'national',
    locMult: () => 1,
  };

  const FEDERAL_ITC = 0.3;
  const BATTERY_BASE = 10500;
  const BATTERY_PER_KW = 180;

  const ELECTRICITY_RATE = {
    national: 0.16,
    dallas: 0.14,
    phoenix: 0.13,
    austin: 0.14,
    tampa: 0.15,
    charlotte: 0.14,
    raleigh: 0.14,
    scottsdale: 'phoenix',
    houston: 0.14,
    orlando: 0.15,
    'san-diego': 0.32,
  };

  const SUN_MULT = {
    national: 1,
    dallas: 1.08,
    phoenix: 1.18,
    austin: 1.06,
    tampa: 0.98,
    charlotte: 1,
    raleigh: 1.02,
    scottsdale: 1.16,
    houston: 1.05,
    orlando: 0.97,
    'san-diego': 1.12,
  };

  const COST_PER_WATT = {
    national: 2.85,
    dallas: 2.65,
    phoenix: 2.72,
    austin: 2.68,
    tampa: 2.78,
    charlotte: 2.74,
    raleigh: 2.72,
    scottsdale: 2.88,
    houston: 2.62,
    orlando: 2.76,
    'san-diego': 3.15,
  };

  const ROOF = { asphalt: 1, metal: 0.96, tile: 1.1, flat: 1.14 };
  const ROOF_COND = { excellent: 1, minor: 1.06, replacement: 1.16 };
  const SHADE = { full: 1, partial: 0.82, heavy: 0.58 };
  const PANEL = { mono: 1.04, poly: 0.94, thin: 0.88 };

  const SYSTEM_KW = [4, 6, 8, 12];

  const STATE_ROWS = [
    { key: 'texas', label: 'Texas', city: 'dallas' },
    { key: 'california', label: 'California', city: 'san-diego' },
    { key: 'florida', label: 'Florida', city: 'tampa' },
    { key: 'arizona', label: 'Arizona', city: 'phoenix' },
  ];

  function rateForCity(cityKey) {
    const r = ELECTRICITY_RATE[cityKey];
    return typeof r === 'number' ? r : ELECTRICITY_RATE.national;
  }

  function formatMoney(n) {
    return '$' + Math.round(n).toLocaleString('en-US');
  }

  function formatRange(low, high) {
    return `${formatMoney(low)}–${formatMoney(high)}`;
  }

  function formatMonthly(n) {
    return formatMoney(n) + '/mo';
  }

  function formatPayback(years) {
    if (!years || years > 25) return '12+ years';
    const lo = Math.floor(years);
    const hi = Math.ceil(years);
    return lo === hi ? `${lo} years` : `${lo}–${hi} years`;
  }

  function billToKwh(bill, cityKey) {
    const rate = rateForCity(cityKey);
    return Math.max(200, Math.round(bill / rate));
  }

  function systemKwFromUsage(monthlyKwh, cityKey) {
    const sun = SUN_MULT[cityKey] || 1;
    const annual = monthlyKwh * 12;
    const productionPerKw = 1350 * sun;
    const kw = annual / productionPerKw;
    return Math.max(4, Math.min(14, Math.round(kw * 2) / 2));
  }

  function estimateForKw(kw, cityKey, roofKey, condKey, panelKey, battery) {
    const mult = locMult(getCity(cityKey));
    const roofMult = (ROOF[roofKey] || 1) * (ROOF_COND[condKey] || 1);
    const panelMult = PANEL[panelKey] || 1;
    const perWatt = (COST_PER_WATT[cityKey] || COST_PER_WATT.national) * panelMult;
    const base = kw * 1000 * perWatt * mult * roofMult;
    const batt = battery ? (BATTERY_BASE + kw * BATTERY_PER_KW) * mult : 0;
    const total = base + batt;
    return {
      low: total * 0.9,
      high: total * 1.1,
      mid: total,
      credit: total * FEDERAL_ITC,
      net: total * (1 - FEDERAL_ITC),
    };
  }

  function compute(opts) {
    const cityKey = opts.city || 'national';
    const bill = Math.max(50, Math.min(600, Number(opts.bill) || 220));
    const sqft = Math.max(800, Math.min(8000, Number(opts.sqft) || 2200));
    const kwh =
      opts.kwh && Number(opts.kwh) > 0
        ? Math.max(200, Math.min(3000, Number(opts.kwh)))
        : billToKwh(bill, cityKey);
    const kw = systemKwFromUsage(kwh, cityKey);
    const roof = opts.roof || 'asphalt';
    const condition = opts.condition || 'excellent';
    const shade = opts.shade || 'full';
    const panel = opts.panel || 'mono';
    const battery = opts.battery === true || opts.battery === 'yes';

    const cost = estimateForKw(kw, cityKey, roof, condition, panel, battery);
    const sun = SHADE[shade] || 1;
    const production = kw * 120 * (SUN_MULT[cityKey] || 1) * sun;
    const coverage = Math.min(0.9, production / kwh);
    const monthlySavingsLow = bill * coverage * 0.88;
    const monthlySavingsHigh = bill * coverage * 0.98;
    const monthlySavingsMid = (monthlySavingsLow + monthlySavingsHigh) / 2;
    const paybackLow = cost.net / (monthlySavingsHigh * 12);
    const paybackHigh = cost.net / (monthlySavingsLow * 12);
    const paybackMid = (paybackLow + paybackHigh) / 2;

    return {
      bill,
      sqft,
      kwh,
      kw,
      cityKey,
      cityLabel: getCity(cityKey).label,
      ...cost,
      monthlySavingsLow,
      monthlySavingsHigh,
      monthlySavingsMid,
      paybackLow,
      paybackHigh,
      paybackMid,
      credit: cost.credit,
    };
  }

  function el(id) {
    return document.getElementById(id);
  }

  function readQuick() {
    const city = getCityValue(el('quick-city')) || 'dallas';
    return compute({
      bill: el('quick-bill')?.value,
      sqft: el('quick-sqft')?.value,
      city,
      roof: el('quick-roof')?.value || 'asphalt',
    });
  }

  function readAdvanced() {
    const city = getCityValue(el('solar-city')) || 'national';
    return compute({
      bill: el('solar-bill')?.value,
      kwh: el('solar-kwh')?.value,
      sqft: el('solar-sqft')?.value,
      city,
      roof: document.querySelector('#solar-calculator-tool [name="solar_roof"]:checked')?.value,
      condition: document.querySelector('#solar-calculator-tool [name="solar_condition"]:checked')?.value,
      shade: document.querySelector('#solar-calculator-tool [name="solar_shade"]:checked')?.value,
      panel: document.querySelector('#solar-calculator-tool [name="solar_panel"]:checked')?.value,
      battery: document.querySelector('#solar-battery')?.checked,
    });
  }

  function renderHero(r) {
    const set = (id, text) => {
      const node = el(id);
      if (node) node.textContent = text;
    };
    set('hero-savings', formatMoney(r.monthlySavingsMid) + '/month');
    set('hero-payback', formatPayback(r.paybackMid));
  }

  function renderQuick(r) {
    const set = (id, text) => {
      const node = el(id);
      if (node) node.textContent = text;
    };
    set('quick-result-cost', formatRange(r.low, r.high));
    set('quick-result-savings', `${formatMoney(r.monthlySavingsLow)}–${formatMoney(r.monthlySavingsHigh)}`);
  }

  function renderAdvanced(r) {
    const set = (id, text) => {
      const node = el(id);
      if (node) node.textContent = text;
    };
    set('calc-total-range', formatRange(r.low, r.high));
    set('calc-total-mid', `~${formatMoney(r.mid)} before incentives`);
    set('calc-monthly-savings', formatRange(r.monthlySavingsLow, r.monthlySavingsHigh));
    set('calc-payback', formatPayback(r.paybackMid));
    set('calc-tax-credit', '-' + formatMoney(r.credit));
    set('calc-net-cost', formatMoney(r.net));
    set('calc-system-kw', `${r.kw} kW system · ${r.cityLabel}`);
    const kwhLabel = el('solar-kwh-label');
    if (kwhLabel && !el('solar-kwh')?.matches(':focus')) {
      kwhLabel.textContent = `${r.kwh} kWh/month suggested from bill`;
    }
  }

  function updateAll() {
    const adv = readAdvanced();
    const quick = readQuick();
    renderHero(adv);
    renderQuick(quick);
    renderAdvanced(adv);
    updateTables(adv.cityKey);
  }

  function updateTables(cityKey) {
    const tbody = el('solar-size-tbody');
    if (tbody) {
      tbody.innerHTML = SYSTEM_KW.map((kw) => {
        const c = estimateForKw(kw, cityKey, 'asphalt', 'excellent', 'mono', false);
        return `<tr><td>${kw} kW</td><td>${formatRange(c.low, c.high)}</td></tr>`;
      }).join('');
    }

    const stateBody = el('solar-state-tbody');
    if (stateBody) {
      stateBody.innerHTML = STATE_ROWS.map((row) => {
        const bill = 220;
        const r = compute({ bill, city: row.city, roof: 'asphalt', shade: 'full' });
        return `<tr><td>${row.label}</td><td>${formatMoney(r.monthlySavingsMid)}/mo</td><td>${formatPayback(r.paybackMid)}</td></tr>`;
      }).join('');
    }
  }

  function syncBills(fromId) {
    const bill = el(fromId)?.value;
    if (bill == null) return;
    ['quick-bill', 'solar-bill'].forEach((id) => {
      const node = el(id);
      if (node && node !== el(fromId)) node.value = bill;
    });
    const slider = el('solar-bill-slider');
    if (slider) slider.value = bill;
    el('solar-bill-label') &&
      (el('solar-bill-label').textContent = formatMoney(Number(bill)) + '/month');
  }

  function syncCities(fromId) {
    const city = el(fromId)?.value;
    if (!city) return;
    ['quick-city', 'solar-city'].forEach((id) => {
      const node = el(id);
      if (node && node !== el(fromId)) node.value = city;
    });
  }

  function bindLive() {
    const ids = [
      'quick-bill',
      'quick-sqft',
      'quick-city',
      'quick-roof',
      'solar-bill',
      'solar-kwh',
      'solar-sqft',
      'solar-city',
      'solar-battery',
    ];
    ids.forEach((id) => {
      const node = el(id);
      if (!node) return;
      const handler = () => {
        if (id === 'quick-bill' || id === 'solar-bill') syncBills(id);
        if (id === 'quick-city' || id === 'solar-city') syncCities(id);
        updateAll();
      };
      node.addEventListener('input', handler);
      node.addEventListener('change', handler);
    });

    document.querySelectorAll('#solar-calculator-tool input[type="radio"]').forEach((radio) => {
      radio.addEventListener('change', updateAll);
    });

    el('quick-calc-btn')?.addEventListener('click', () => {
      document.getElementById('calculator')?.scrollIntoView({ behavior: 'smooth' });
    });

    el('hero-start-btn')?.addEventListener('click', (e) => {
      e.preventDefault();
      document.getElementById('quick-estimate')?.scrollIntoView({ behavior: 'smooth' });
    });

    document.querySelectorAll('[data-scroll-calc]').forEach((btn) => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        document.getElementById('quick-estimate')?.scrollIntoView({ behavior: 'smooth' });
      });
    });

    const billSlider = el('solar-bill-slider');
    const billInput = el('solar-bill');
    if (billSlider && billInput) {
      const sync = () => {
        billSlider.value = billInput.value;
        el('solar-bill-label').textContent = formatMoney(Number(billInput.value)) + '/month';
        updateAll();
      };
      billSlider.addEventListener('input', () => {
        billInput.value = billSlider.value;
        sync();
      });
      billInput.addEventListener('input', sync);
    }
  }

  bindLive();
  if (el('quick-city') && el('solar-city')) syncCities('quick-city');
  updateAll();
  window.addEventListener('ehc:city-scope', () => updateAll());
})();

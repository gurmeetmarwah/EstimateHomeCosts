/**
 * HVAC Cost Calculator landing page — quick + advanced
 */
(function () {
  'use strict';

  const { getCity, getCityValue, locMult } = window.EHCCities || {};

  const SYSTEM = {
    'central-ac': { rate: 4.05, label: 'Central AC', tier: 'Most popular', life: '15–20 years' },
    'heat-pump': { rate: 4.65, label: 'Heat pump', tier: 'Efficient', life: '15–20 years' },
    'mini-split': { rate: 5.35, label: 'Ductless mini split', tier: 'Flexible', life: '15–20 years' },
    'furnace-ac': { rate: 5.75, label: 'Furnace + AC', tier: 'Full HVAC', life: '15–20 years' },
    geothermal: { rate: 9.25, label: 'Geothermal', tier: 'Premium', life: '25+ years' },
  };

  const SYSTEM_COMPARISON = [
    { key: 'central-ac', label: 'Central AC', bestFor: 'Most U.S. homes with ducts' },
    { key: 'heat-pump', label: 'Heat pump', bestFor: 'Mild climates, heat + cool in one', link: '/cost/hvac-installation/' },
    { key: 'mini-split', label: 'Ductless mini split', bestFor: 'Additions, zoning, no ducts' },
    { key: 'furnace-ac', label: 'Furnace + AC combo', bestFor: 'Cold climates, full replacement' },
    { key: 'geothermal', label: 'Geothermal', bestFor: 'Long-term efficiency, new builds', plusHigh: true },
  ];

  const EFFICIENCY = { standard: 1, high: 1.14, premium: 1.28 };
  const DUCT_BASE = 2800;
  const EQUIP_LOW = 3.5;
  const EQUIP_HIGH = 7.5;

  const LABOR_REPLACEMENT_LOW = 1800;
  const LABOR_REPLACEMENT_HIGH = 4500;
  const LABOR_INSTALL_2K_LOW = 3200;
  const LABOR_INSTALL_2K_HIGH = 5500;
  const LABOR_SHARE_LOW = 40;
  const LABOR_SHARE_HIGH = 55;
  const MINI_SPLIT_LOW = 500;
  const MINI_SPLIT_HIGH = 1500;
  const GEO_LABOR_LOW = 3000;
  const GEO_LABOR_HIGH = 8000;
  const ELECTRICAL_LOW = 400;
  const ELECTRICAL_HIGH = 1200;
  const DUCT_LOW_2K = 2800;
  const DUCT_HIGH_2K = 6500;
  const DUCT_SEAL_LOW = 450;
  const DUCT_SEAL_HIGH = 1200;
  const INSPECTION_LOW = 50;
  const INSPECTION_HIGH = 150;

  const PERMIT_CITY_NOTES = {
    national: 'Typical residential mechanical permit',
    texas: 'Mechanical permit; tonnage-based fees vary by city',
    dallas: 'Mechanical permit; tonnage-based fees',
    phoenix: 'Same-day permits in many cases',
    austin: 'Travis County / city fees vary by scope',
    tampa: 'Energy code and humidity requirements',
    miami: 'Miami-Dade wind and energy compliance',
    jacksonville: 'Duval County mechanical permit',
    'st-petersburg': 'Pinellas County mechanical permit',
    charlotte: 'Mecklenburg mechanical permit',
    raleigh: 'Wake County mechanical permit',
    durham: 'Durham County mechanical permit',
    cary: 'Wake County / town permit fees',
    wilmington: 'New Hanover coastal permit requirements',
    scottsdale: 'Maricopa County; HOA review common',
    mesa: 'Maricopa County mechanical permit',
    tucson: 'Pima County mechanical permit',
    chandler: 'Maricopa County; HOA review common',
    houston: 'Varies by equipment tonnage',
    'san-antonio': 'Bexar County mechanical permit',
    'fort-worth': 'Tarrant County mechanical permit',
    orlando: 'Orange County energy compliance',
    'san-diego': 'Title 24 / efficiency rules',
    'los-angeles': 'LADBS permit; Title 24 compliance',
    'orange-county': 'County permit; HOA review common',
    sacramento: 'Sacramento County mechanical permit',
    'san-francisco': 'SF DBI permit; among highest fees in CA',
  };

  const REGIONAL_HVAC_NOTES = {
    national: 'Summer peak demand for AC; heat pumps growing in moderate climates',
    texas: 'Long hot summers statewide; central AC replacement is a top project',
    dallas: 'High cooling demand; central AC and heat pumps common',
    phoenix: 'Extreme cooling load; high-SEER systems standard',
    austin: 'Long cooling season; competitive installer market',
    tampa: 'Humidity control and hurricane-rated outdoor units',
    miami: 'Year-round cooling; salt-air corrosion on outdoor units',
    jacksonville: 'Humidity and moderate cooling load',
    'st-petersburg': 'Coastal humidity and wind-rated equipment',
    charlotte: 'Moderate heating and cooling balance',
    raleigh: 'Research Triangle growth; heat pumps popular',
    durham: 'Older homes benefit from duct sealing and mini-splits',
    cary: 'Suburban heat pumps and central AC replacements',
    wilmington: 'Coastal humidity; corrosion-resistant outdoor units',
    scottsdale: 'Premium equipment and peak summer rates',
    mesa: 'East Valley extreme heat; high-SEER AC standard',
    tucson: 'Desert heat; evaporative and AC mix in older stock',
    chandler: 'Master-planned communities; heat pumps gaining share',
    houston: 'Year-round workload; humidity and coastal corrosion',
    'san-antonio': 'Long cooling season; affordable labor vs. Austin',
    'fort-worth': 'North Texas heat; hail-season install scheduling',
    orlando: 'Central Florida wind codes; high-SEER AC common',
    'san-diego': 'Coastal labor premium; Title 24 efficiency rules',
    'los-angeles': 'Highest labor rates; Title 24 on every changeout',
    'orange-county': 'Premium suburban labor; high-SEER standard',
    sacramento: 'Inland heat drives AC and heat pump demand',
    'san-francisco': 'Many older homes need ductless mini-splits',
  };

  function formatMoney(n) {
    return '$' + Math.round(n).toLocaleString('en-US');
  }

  function formatRange(low, high) {
    return `${formatMoney(low)}–${formatMoney(high)}`;
  }

  function scaleAmount(n, mult) {
    return Math.round(n * mult);
  }

  function scaleRange(low, high, mult) {
    return [scaleAmount(low, mult), scaleAmount(high, mult)];
  }

  function laborShareRange(mult) {
    const shift = Math.round((mult - 1) * 10);
    return [Math.max(35, LABOR_SHARE_LOW + shift), Math.min(62, LABOR_SHARE_HIGH + shift)];
  }

  function getActiveSqft() {
    const adv = document.getElementById('hvac-size');
    const quick = document.getElementById('quick-sqft');
    return Math.max(800, Math.min(8000, Number(adv?.value || quick?.value) || 2000));
  }

  function estimateSystem(systemKey, cityKey, sqft) {
    return compute({
      sqft,
      system: systemKey,
      efficiency: 'high',
      ductwork: false,
      city: cityKey || 'national',
    });
  }

  function formatInstalledRange(r, plusHigh) {
    const range = formatRange(r.low, r.high);
    return plusHigh ? `${range}+` : range;
  }

  function formatPerSqftBand(r) {
    return `$${(r.low / r.sqft).toFixed(2)} – $${(r.high / r.sqft).toFixed(2)}`;
  }

  function renderSystemComparison(cityKey) {
    const tbody = document.getElementById('hvac-comparison-tbody');
    const subtitle = document.getElementById('hvac-comparison-subtitle');
    const colSize = document.getElementById('hvac-comparison-col-size');
    const systemsSubtitle = document.getElementById('hvac-systems-subtitle');
    if (!tbody) return;

    const city = getCity(cityKey);
    const isNational = !cityKey || cityKey === 'national';
    const sqft = getActiveSqft();

    if (subtitle) {
      subtitle.textContent = isNational
        ? `Installed national averages for a ${sqft.toLocaleString()} sq ft home at 16 SEER, existing ductwork (2026)`
        : `Installed estimates for ${city.label} — ${sqft.toLocaleString()} sq ft, 16 SEER, existing ductwork (2026)`;
    }
    if (systemsSubtitle) {
      systemsSubtitle.textContent = isNational
        ? `Compare installed national averages by system — ${sqft.toLocaleString()} sq ft at 16 SEER`
        : `Installed ranges for ${city.label} — ${sqft.toLocaleString()} sq ft, 16 SEER, no new ductwork`;
    }
    if (colSize) colSize.textContent = `${sqft.toLocaleString()} sq ft range`;

    tbody.innerHTML = SYSTEM_COMPARISON.map((row) => {
      const sys = SYSTEM[row.key];
      const r = estimateSystem(row.key, cityKey, sqft);
      const nameCell = row.link
        ? `<a href="${row.link}">${row.label}</a>`
        : row.label;
      return `<tr>
        <td>${nameCell}</td>
        <td>${formatInstalledRange(r, row.plusHigh)}</td>
        <td>${formatPerSqftBand(r)}</td>
        <td>${sys.life}</td>
        <td>${row.bestFor}</td>
      </tr>`;
    }).join('');
  }

  function renderSystemTiles(cityKey) {
    const sqft = getActiveSqft();
    document.querySelectorAll('[data-hvac-system-price]').forEach((el) => {
      const key = el.dataset.hvacSystemPrice;
      if (!SYSTEM[key]) return;
      const r = estimateSystem(key, cityKey, sqft);
      el.textContent = formatInstalledRange(r, key === 'geothermal');
    });
  }

  function renderLaborDetails(cityKey) {
    const list = document.getElementById('hvac-labor-list');
    const tbody = document.getElementById('hvac-labor-tbody');
    const context = document.getElementById('hvac-labor-context');
    const colSize = document.getElementById('hvac-labor-col-size');
    if (!list || !tbody) return;

    const isNational = !cityKey || cityKey === 'national';
    const city = getCity(cityKey);
    const laborMult = city.labor;
    const sqft = getActiveSqft();
    const sizeFactor = sqft / 2000;
    const [repLow, repHigh] = scaleRange(LABOR_REPLACEMENT_LOW, LABOR_REPLACEMENT_HIGH, laborMult);
    const [miniLow, miniHigh] = scaleRange(MINI_SPLIT_LOW, MINI_SPLIT_HIGH, laborMult);
    const [geoLow, geoHigh] = scaleRange(GEO_LABOR_LOW, GEO_LABOR_HIGH, laborMult);
    const [elecLow, elecHigh] = scaleRange(ELECTRICAL_LOW, ELECTRICAL_HIGH, laborMult);
    const [instLow, instHigh] = scaleRange(
      LABOR_INSTALL_2K_LOW * sizeFactor,
      LABOR_INSTALL_2K_HIGH * sizeFactor,
      laborMult
    );
    const [shareLow, shareHigh] = laborShareRange(laborMult);
    const heading = isNational ? 'National average' : city.label;

    if (context) {
      context.innerHTML = isNational
        ? 'Labor typically accounts for <strong>40–55%</strong> of your total HVAC installation bill. Rates depend on system complexity, refrigerant type, access, and local demand.'
        : `Labor rates for <strong>${city.label}</strong> (${(city.labor * 100).toFixed(0)}% of national labor index). Select a different city in the <a href="#calculator">calculator</a> to compare.`;
    }

    list.innerHTML = [
      `<li><strong>${heading}:</strong> ${formatRange(repLow, repHigh)} for standard replacement</li>`,
      `<li><strong>Mini-split premium:</strong> +${formatRange(miniLow, miniHigh)} per zone for line sets</li>`,
      `<li><strong>Geothermal:</strong> +${formatRange(geoLow, geoHigh)} for ground loop labor</li>`,
      `<li><strong>Electrical upgrades:</strong> +${formatRange(elecLow, elecHigh)} if panel work needed</li>`,
    ].join('');

    if (colSize) colSize.textContent = `${sqft.toLocaleString()} sq ft install`;

    const row = (label, share, install) =>
      `<tr><td>${label}</td><td>${share[0]}–${share[1]}%</td><td>${formatRange(install[0], install[1])}</td></tr>`;

    if (isNational) {
      tbody.innerHTML = row('National average', [shareLow, shareHigh], [instLow, instHigh]);
      return;
    }

    const natCity = getCity('national');
    const natMult = natCity.labor;
    const natInst = scaleRange(
      LABOR_INSTALL_2K_LOW * sizeFactor,
      LABOR_INSTALL_2K_HIGH * sizeFactor,
      natMult
    );
    const natShare = laborShareRange(natMult);
    tbody.innerHTML =
      row(city.label, [shareLow, shareHigh], [instLow, instHigh]) +
      `<tr><td>National average</td><td>${natShare[0]}–${natShare[1]}%</td><td>${formatRange(natInst[0], natInst[1])}</td></tr>`;
  }

  function renderPermitsDetails(cityKey) {
    const list = document.getElementById('hvac-permits-list');
    const tbody = document.getElementById('hvac-permits-tbody');
    const context = document.getElementById('hvac-permits-context');
    const colDuct = document.getElementById('hvac-permits-col-duct');
    if (!list || !tbody) return;

    const isNational = !cityKey || cityKey === 'national';
    const city = getCity(cityKey);
    const mult = locMult(city);
    const sqft = getActiveSqft();
    const sizeFactor = sqft / 2000;
    const permitMid = city.permit;
    const [permitLow, permitHigh] = [Math.round(permitMid * 0.82), Math.round(permitMid * 1.18)];
    const [inspLow, inspHigh] = scaleRange(INSPECTION_LOW, INSPECTION_HIGH, city.labor);
    const [ductLow, ductHigh] = scaleRange(DUCT_LOW_2K * sizeFactor, DUCT_HIGH_2K * sizeFactor, mult);
    const [sealLow, sealHigh] = scaleRange(DUCT_SEAL_LOW, DUCT_SEAL_HIGH, city.labor);
    const heading = isNational ? 'Typical permit fee' : `Permit fee (${city.label})`;
    const ductHeading = isNational ? 'New ductwork' : `New ductwork (${city.label})`;

    if (context) {
      context.innerHTML = isNational
        ? 'Most cities require a permit for HVAC replacement. Duct condition often determines whether you need a simple swap or a full system overhaul.'
        : `Permit and duct estimates for <strong>${city.label}</strong>. ${PERMIT_CITY_NOTES[cityKey] || PERMIT_CITY_NOTES.national}`;
    }

    list.innerHTML = [
      `<li><strong>${heading}:</strong> ${formatRange(permitLow, permitHigh)} for residential HVAC</li>`,
      `<li><strong>Inspection fees:</strong> ${formatRange(inspLow, inspHigh)} (often bundled)</li>`,
      `<li><strong>${ductHeading}:</strong> ${formatRange(ductLow, ductHigh)}+ for ${sqft.toLocaleString()} sq ft</li>`,
      `<li><strong>Duct sealing:</strong> ${formatRange(sealLow, sealHigh)} recommended for older homes</li>`,
    ].join('');

    if (colDuct) colDuct.textContent = `New ductwork (${sqft.toLocaleString()} sq ft)`;

    const row = (label, permit, duct) =>
      `<tr><td>${label}</td><td>${permit}</td><td>${duct}</td></tr>`;

    const nat = getCity('national');
    const natPermit = [
      Math.round(nat.permit * 0.82),
      Math.round(nat.permit * 1.18),
    ];

    if (isNational) {
      tbody.innerHTML = row(
        'National average',
        formatRange(natPermit[0], natPermit[1]),
        `${formatRange(DUCT_LOW_2K * sizeFactor, DUCT_HIGH_2K * sizeFactor)}+`
      );
      return;
    }

    const natMult = locMult(nat);
    const natDuct = scaleRange(DUCT_LOW_2K * sizeFactor, DUCT_HIGH_2K * sizeFactor, natMult);
    tbody.innerHTML =
      row(city.label, formatRange(permitLow, permitHigh), `${formatRange(ductLow, ductHigh)}+`) +
      row('National average', formatRange(natPermit[0], natPermit[1]), `${formatRange(natDuct[0], natDuct[1])}+`);
  }

  function monthlyPayment(principal, months = 120, annualRate = 0.079) {
    const r = annualRate / 12;
    if (r <= 0) return principal / months;
    return (principal * r) / (1 - Math.pow(1 + r, -months));
  }

  function compute(opts) {
    const sqft = Math.max(800, Math.min(8000, Number(opts.sqft) || 2000));
    const sys = SYSTEM[opts.system] || SYSTEM['central-ac'];
    const effMult = EFFICIENCY[opts.efficiency] || 1.14;
    const city = getCity(opts.city || 'national');
    const mult = locMult(city);
    const ductwork = opts.ductwork === true;
    const sizeFactor = sqft / 2000;

    const equipment = sqft * sys.rate * effMult * mult;
    const duct = ductwork ? DUCT_BASE * sizeFactor * mult : 0;
    const permits = city.permit;
    const total = equipment + duct + permits;
    const low = total * 0.92;
    const high = total * 1.08;
    const mid = total;

    const parts = [
      { key: 'equipment', label: 'Equipment & install', amount: equipment },
      { key: 'duct', label: 'Ductwork', amount: duct },
      { key: 'permits', label: 'Permits & fees', amount: permits },
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
    const form = document.getElementById('hvac-calculator-tool');
    if (!form) return null;
    return compute({
      sqft: document.getElementById('hvac-size')?.value,
      system: form.querySelector('[name="hvac_system"]:checked')?.value || 'central-ac',
      efficiency: document.getElementById('hvac-efficiency')?.value || 'high',
      ductwork: form.querySelector('[name="ductwork"]:checked')?.value === 'yes',
      city: getCityValue(document.getElementById('hvac-city')),
    });
  }

  function readQuick() {
    return compute({
      sqft: document.getElementById('quick-sqft')?.value,
      system: document.getElementById('quick-system')?.value || 'central-ac',
      efficiency: 'high',
      ductwork: false,
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
    set('calc-per-sqft', `$${r.perSqft.toFixed(2)} per sq ft`);
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
    const sqft = document.getElementById('quick-sqft')?.value;
    const sys = document.getElementById('quick-system')?.value;
    const city = document.getElementById('quick-city')?.value;
    const sizeInput = document.getElementById('hvac-size');
    const sizeSlider = document.getElementById('hvac-size-slider');
    if (sizeInput && sqft) sizeInput.value = sqft;
    if (sizeSlider && sqft) sizeSlider.value = sqft;
    if (sys) {
      const radio = document.querySelector(`#hvac-calculator-tool [name="hvac_system"][value="${sys}"]`);
      if (radio) radio.checked = true;
    }
    const advCity = document.getElementById('hvac-city');
    if (advCity && city) advCity.value = city;
  }

  function syncCitySelects(fromQuick) {
    const quick = document.getElementById('quick-city');
    const adv = document.getElementById('hvac-city');
    if (!quick || !adv) return;
    if (fromQuick) adv.value = quick.value;
    else quick.value = adv.value;
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
    const mult = locMult(city);
    const pct = Math.round(Math.abs(mult - 1) * 100);
    const multText =
      mult < 0.995 ? `~${pct}% below national` : mult > 1.005 ? `~${pct}% above national` : 'Near national average';

    title.textContent = city.label;
    list.innerHTML = [
      `<li><strong>Cost vs national:</strong> ${multText}</li>`,
      `<li><strong>Equipment &amp; install:</strong> $${(EQUIP_LOW * mult).toFixed(2)}–$${(EQUIP_HIGH * mult).toFixed(2)} / sq ft (est.)</li>`,
      `<li><strong>Permits:</strong> ~${formatMoney(city.permit)} HVAC replacement</li>`,
      `<li><strong>Labor index:</strong> ${(city.labor * 100).toFixed(0)}% of national</li>`,
      `<li><strong>Local factors:</strong> ${REGIONAL_HVAC_NOTES[cityKey] || REGIONAL_HVAC_NOTES.national}</li>`,
    ].join('');
  }

  function updateAll() {
    const quick = readQuick();
    const advanced = readAdvanced();
    if (quick) renderQuick(quick);
    if (advanced) renderAdvanced(advanced);
    const cityKey =
      getCityValue(document.getElementById('hvac-city')) ||
      getCityValue(document.getElementById('quick-city'));
    renderLocalFactors(cityKey);
    renderLaborDetails(cityKey);
    renderPermitsDetails(cityKey);
    renderSystemComparison(cityKey);
    renderSystemTiles(cityKey);
  }

  function onCityChange(fromQuick) {
    syncCitySelects(fromQuick);
    updateAll();
  }

  function bindQuick() {
    const bar = document.getElementById('quick-hvac-calc');
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
    const form = document.getElementById('hvac-calculator-tool');
    if (!form) return;

    const sizeInput = document.getElementById('hvac-size');
    const sizeSlider = document.getElementById('hvac-size-slider');
    const sizeLabel = document.getElementById('hvac-size-label');

    function syncSize(from) {
      const v = Math.max(800, Math.min(8000, Number(from === 'slider' ? sizeSlider.value : sizeInput.value) || 2000));
      sizeInput.value = v;
      sizeSlider.value = v;
      if (sizeLabel) sizeLabel.textContent = v.toLocaleString() + ' sq ft';
      const q = document.getElementById('quick-sqft');
      if (q) q.value = v;
      updateAll();
    }

    sizeInput?.addEventListener('input', () => syncSize('input'));
    sizeSlider?.addEventListener('input', () => syncSize('slider'));
    document.getElementById('hvac-city')?.addEventListener('change', () => onCityChange(false));

    ['input', 'change'].forEach((evt) => {
      form.addEventListener(evt, (e) => {
        if (e.target.id === 'hvac-city') return;
        if (e.target.tagName === 'SELECT') return;
        const sys = form.querySelector('[name="hvac_system"]:checked')?.value;
        const qs = document.getElementById('quick-system');
        if (qs && sys) qs.value = sys;
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

  window.addEventListener('ehc:city-scope', () => updateAll());
})();

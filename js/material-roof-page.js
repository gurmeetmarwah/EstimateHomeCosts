/**
 * Shared calculator + local/climate sync for material roof landing pages
 */
(function () {
  'use strict';

  const { getCity, getCityValue, locMult } = window.EHCCities || {
    getCity: () => ({ label: 'National average', material: 1, labor: 1, permit: 275 }),
    getCityValue: () => 'national',
    locMult: () => 1,
  };

  const TEAROFF = 0.85;
  const WASTE_RATE = 0.05;

  function formatMoney(n) {
    return '$' + Math.round(n).toLocaleString('en-US');
  }

  function formatRange(low, high) {
    return `${formatMoney(low)}–${formatMoney(high)}`;
  }

  function compute(variants, defaultVariant, opts) {
    const sqft = Math.max(500, Math.min(10000, Number(opts.sqft) || 2000));
    const v = variants[opts.variant] || variants[defaultVariant];
    const city = getCity(opts.city || 'national');
    const mult = locMult(city);

    const materialCost = sqft * v.material * mult;
    const laborCost = sqft * v.labor * mult;
    const tearoffCost = sqft * TEAROFF * city.labor;
    const permitCost = city.permit;
    const subtotal = materialCost + laborCost + tearoffCost + permitCost;
    const total = subtotal * (1 + WASTE_RATE);
    const low = total * 0.9;
    const high = total * 1.1;

    const midPerSqft = total / sqft;

    return {
      sqft,
      low,
      high,
      mid: total,
      midPerSqft,
      perSqftLow: low / sqft,
      perSqftHigh: high / sqft,
      cityLabel: city.label,
      cityKey: opts.city || 'national',
      variantLabel: v.label,
    };
  }

  /** Tighter per-sq-ft band for material guide hero (city sets the midpoint). */
  function heroPerSqftRange(r) {
    const mid = r.midPerSqft;
    const isNational = !r.cityKey || r.cityKey === 'national';
    const spread = isNational ? 0.04 : 0.025;
    return {
      low: mid * (1 - spread),
      high: mid * (1 + spread),
    };
  }

  window.initMaterialRoofPage = function (config) {
    const {
      formId,
      sqftId,
      variantId,
      cityId,
      defaultVariant,
      variants,
      cityClimate,
      homeExamples,
      climateNationalLead,
    } = config;

    function readCalc() {
      return compute(variants, defaultVariant, {
        sqft: document.getElementById(sqftId)?.value,
        variant: document.getElementById(variantId)?.value || defaultVariant,
        city: getCityValue(document.getElementById(cityId)),
      });
    }

    function renderEstimate(r) {
      if (!r) return;
      const set = (id, t) => {
        const el = document.getElementById(id);
        if (el) el.textContent = t;
      };
      const perSqft = `$${r.perSqftLow.toFixed(2)}–$${r.perSqftHigh.toFixed(2)}`;
      set('calc-result-range', formatRange(r.low, r.high));
      set('calc-result-mid', `~${formatMoney(r.mid)} mid-estimate · ${r.cityLabel}`);
      set('calc-result-per-sqft', `${perSqft} per sq ft installed`);

      const hero = heroPerSqftRange(r);
      set('material-hero-cost', `$${hero.low.toFixed(2)}–$${hero.high.toFixed(2)} / sq ft`);
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
      const multText = mult < 0.995 ? `~${pct}% below national` : mult > 1.005 ? `~${pct}% above national` : 'Near national average';

      title.textContent = city.label;
      list.innerHTML = [
        `<li><strong>Cost vs national:</strong> ${multText}</li>`,
        `<li><strong>Permits (est.):</strong> ~${formatMoney(city.permit)} re-roof</li>`,
        `<li><strong>Labor index:</strong> ${(city.labor * 100).toFixed(0)}% of national</li>`,
        `<li><strong>Material index:</strong> ${(city.material * 100).toFixed(0)}% of national</li>`,
        `<li><strong>Climate:</strong> ${cityClimate[cityKey]?.rating || 'See climate section below'}</li>`,
      ].join('');
    }

    function renderClimateSection(cityKey) {
      const grid = document.getElementById('climate-grid');
      const samples = document.getElementById('climate-grid-samples');
      const cityCard = document.getElementById('climate-city-card');
      const lead = document.getElementById('climate-section-lead');
      const isNational = !cityKey || cityKey === 'national';

      if (grid) {
        grid.classList.toggle('climate-grid--national', isNational);
        grid.classList.toggle('climate-grid--city', !isNational);
      }
      if (samples) samples.hidden = !isNational;
      if (cityCard) cityCard.hidden = isNational;
      if (lead) {
        lead.textContent = isNational
          ? climateNationalLead
          : `Climate and performance notes for ${getCity(cityKey).label} based on your calculator selection.`;
      }
      if (isNational) return;

      const data = cityClimate[cityKey];
      if (!data) return;

      const title = document.getElementById('climate-city-title');
      const rating = document.getElementById('climate-city-rating');
      const summary = document.getElementById('climate-city-summary');
      const list = document.getElementById('climate-city-list');

      if (title) title.textContent = getCity(cityKey).label;
      if (rating) {
        rating.textContent = data.rating;
        rating.className = 'climate-rating climate-rating--' + (data.ratingClass || 'good');
      }
      if (summary) summary.textContent = data.summary;
      if (list) list.innerHTML = data.bullets.map((b) => `<li>${b}</li>`).join('');
    }

    function highlightProjectExample(cityKey) {
      const key = cityKey && homeExamples[cityKey] ? cityKey : 'national';
      document.querySelectorAll('[data-project-city]').forEach((card) => {
        card.classList.toggle('project-example-card--active', card.dataset.projectCity === key);
      });
    }

    function updateAll() {
      renderEstimate(readCalc());
      const cityKey = getCityValue(document.getElementById(cityId));
      renderLocalFactors(cityKey);
      renderClimateSection(cityKey);
      highlightProjectExample(cityKey);
    }

    const form = document.getElementById(formId);
    if (form) {
      form.addEventListener('input', (e) => {
        if (e.target.tagName === 'SELECT') return;
        updateAll();
      });
      form.addEventListener('change', updateAll);
      document.getElementById(cityId)?.addEventListener('change', updateAll);
      updateAll();
    }

    document.querySelectorAll('[data-scroll-calc]').forEach((btn) => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        document.getElementById('calculator')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
      });
    });

    window.addEventListener('ehc:city-scope', () => updateAll());
  };
})();

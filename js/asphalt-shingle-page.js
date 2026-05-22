/**
 * Asphalt shingle roof cost landing page — mini calculator + local factors
 */
(function () {
  'use strict';

  const { getCity, getCityValue, locMult } = window.EHCCities || {
    getCity: () => ({ label: 'National average', material: 1, labor: 1, permit: 275 }),
    getCityValue: () => 'national',
    locMult: () => 1,
  };

  const VARIANT = {
    '3-tab': { material: 1.85, labor: 2.1, label: '3-tab shingles', lifespan: '15–20 yrs', appeal: 'Basic' },
    architectural: { material: 2.35, labor: 2.45, label: 'Architectural shingles', lifespan: '25–30 yrs', appeal: 'High' },
    luxury: { material: 2.85, labor: 2.75, label: 'Luxury / designer shingles', lifespan: '30–40 yrs', appeal: 'Premium' },
  };

  const TEAROFF = 0.85;
  const WASTE_RATE = 0.05;
  /** Local climate guidance for asphalt shingles by calculator city */
  const CITY_CLIMATE = {
    dallas: {
      rating: 'Fair — hail zone',
      ratingClass: 'fair',
      summary: 'North Texas is workable for asphalt, but hail and wind drive insurance claims and material choices more than in moderate climates.',
      bullets: [
        'Hail corridors: Class 4 impact-resistant architectural shingles strongly recommended',
        'Hot summers accelerate granule loss on south- and west-facing slopes',
        'Wind uplift: 6-nail patterns common on perimeter and ridge lines',
        'Insurance may favor IR shingles — verify deductible and coverage before install',
      ],
    },
    houston: {
      rating: 'Fair — humidity & wind',
      ratingClass: 'fair',
      summary: 'Gulf Coast humidity and storms make asphalt viable with the right product tier and full tear-off — not the cheapest long-term option in every neighborhood.',
      bullets: [
        'High humidity: algae-resistant (AR) granules help prevent streaking',
        'Tropical storm exposure: 130 mph wind-rated shingles minimum on many bids',
        'Moisture management: attic ventilation critical to avoid deck rot',
        'Full tear-off standard — overlay rarely approved near the coast',
      ],
    },
    austin: {
      rating: 'Good — with hail prep',
      ratingClass: 'good',
      summary: 'Central Texas growth markets favor architectural asphalt for value, but periodic hail means product selection matters as much as price.',
      bullets: [
        'Architectural shingles dominate new construction and re-roofs',
        'Hail seasons: consider IR-rated lines in Travis County and surrounding areas',
        'Heat: lighter shingle colors reduce attic heat gain',
        'Competitive labor market keeps install timelines short',
      ],
    },
    phoenix: {
      rating: 'Challenging — extreme heat',
      ratingClass: 'challenging',
      summary: 'Asphalt is widely used in Phoenix, but intense UV and heat shorten granule life on exposed slopes — metal and tile compete strongly.',
      bullets: [
        'South- and west-facing slopes see fastest heat-related aging',
        'Light gray or tan colors outperform dark charcoal in summer',
        'Radiant barrier decking or enhanced attic ventilation recommended',
        'Tile and foam-backed systems common in upscale subdivisions',
      ],
    },
    scottsdale: {
      rating: 'Challenging — heat & premium market',
      ratingClass: 'challenging',
      summary: 'Scottsdale installs asphalt on many homes, but HOA and buyer expectations often push toward tile, metal, or luxury designer shingle lines.',
      bullets: [
        'Designer / luxury asphalt lines match desert contemporary architecture',
        'Extreme UV: expect faster cosmetic fade on dark colors',
        'HOA architectural review may restrict color and profile',
        'Premium labor rates — budget above national asphalt averages',
      ],
    },
    tampa: {
      rating: 'Fair — hurricane codes',
      ratingClass: 'fair',
      summary: 'Tampa Bay asphalt installs must meet Florida Building Code wind requirements — product and fastening matter more than in northern states.',
      bullets: [
        'Florida Product Approval listings required for shingles used in the region',
        'Enhanced nailing schedules (often 6 nails per shingle) on many permits',
        'Tile and metal popular in coastal ZIPs — asphalt common inland',
        'Moisture barriers and sealed roof decks in high-wind design zones',
      ],
    },
    orlando: {
      rating: 'Fair — wind & moisture',
      ratingClass: 'fair',
      summary: 'Central Florida asphalt is standard on suburban tract homes, with code-driven wind ratings and moisture details on every permitted re-roof.',
      bullets: [
        'Wind-rated architectural shingles typical for new permits',
        'Heavy rain periods: proper valley and flashing details essential',
        'Algae-resistant shingles recommended in humid inland lots',
        'Insurance wind mitigation inspections may affect premiums',
      ],
    },
    charlotte: {
      rating: 'Good',
      ratingClass: 'good',
      summary: 'Charlotte\'s moderate four-season climate is well suited to architectural asphalt — one of the better Southeast markets for shingle longevity.',
      bullets: [
        'Ice and water shield at eaves recommended for occasional winter storms',
        'Algae-resistant shingles popular in shaded lots',
        'Moderate labor costs vs coastal Florida markets',
        'Architectural asphalt is the default for resale-focused re-roofs',
      ],
    },
    raleigh: {
      rating: 'Good',
      ratingClass: 'good',
      summary: 'Raleigh–Durham\'s climate fits asphalt well: moderate humidity, manageable wind, and strong contractor availability for architectural lines.',
      bullets: [
        'Research Triangle: architectural shingles standard on most homes',
        'Humid summers: AR granules reduce streaking under tree cover',
        'Occasional ice storms — eave flashing details matter',
        'Growing market keeps install competition healthy for pricing',
      ],
    },
    'san-diego': {
      rating: 'Fair — coastal sun & codes',
      ratingClass: 'fair',
      summary: 'San Diego allows asphalt on many homes, but coastal moisture, Title 24 energy rules, and tile competition shape what gets installed.',
      bullets: [
        'Title 24 / cool-roof rules may affect color and product selection',
        'Coastal salt air: corrosion-resistant fasteners and flashing',
        'Lighter colors preferred for energy and fade resistance',
        'Tile and concrete dominate some coastal neighborhoods — asphalt common inland',
      ],
    },
  };

  const HOME_EXAMPLES = {
    national: { sqft: 2000, cost: 14200, label: 'National average' },
    dallas: { sqft: 2100, cost: 11800, label: 'Dallas, TX' },
    phoenix: { sqft: 1950, cost: 13200, label: 'Phoenix, AZ' },
    austin: { sqft: 2050, cost: 12400, label: 'Austin, TX' },
    tampa: { sqft: 1980, cost: 14100, label: 'Tampa, FL' },
    charlotte: { sqft: 2000, cost: 12800, label: 'Charlotte, NC' },
    raleigh: { sqft: 2020, cost: 12900, label: 'Raleigh, NC' },
    scottsdale: { sqft: 2200, cost: 15800, label: 'Scottsdale, AZ' },
    houston: { sqft: 2080, cost: 11600, label: 'Houston, TX' },
    orlando: { sqft: 1960, cost: 13800, label: 'Orlando, FL' },
    'san-diego': { sqft: 1850, cost: 17200, label: 'San Diego, CA' },
  };

  function formatMoney(n) {
    return '$' + Math.round(n).toLocaleString('en-US');
  }

  function formatRange(low, high) {
    return `${formatMoney(low)}–${formatMoney(high)}`;
  }

  function compute(opts) {
    const sqft = Math.max(500, Math.min(10000, Number(opts.sqft) || 2000));
    const v = VARIANT[opts.variant] || VARIANT.architectural;
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

  function heroPerSqftRange(r) {
    const mid = r.midPerSqft;
    const isNational = !r.cityKey || r.cityKey === 'national';
    const spread = isNational ? 0.04 : 0.025;
    return {
      low: mid * (1 - spread),
      high: mid * (1 + spread),
    };
  }

  function readCalc() {
    return compute({
      sqft: document.getElementById('asphalt-sqft')?.value,
      variant: document.getElementById('asphalt-variant')?.value || 'architectural',
      city: getCityValue(document.getElementById('asphalt-city')),
    });
  }

  function renderEstimate(r) {
    if (!r) return;
    const set = (id, t) => {
      const el = document.getElementById(id);
      if (el) el.textContent = t;
    };
    set('calc-result-range', formatRange(r.low, r.high));
    set('calc-result-mid', `~${formatMoney(r.mid)} mid-estimate · ${r.cityLabel}`);
    set('calc-result-per-sqft', `$${r.perSqftLow.toFixed(2)}–$${r.perSqftHigh.toFixed(2)} per sq ft installed`);

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
      `<li><strong>Climate:</strong> ${CITY_CLIMATE[cityKey]?.rating || 'See climate section below'}</li>`,
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
        ? 'Asphalt performs best in moderate climates. Select a city in the calculator above for localized weather and code guidance.'
        : `Climate and code considerations for ${getCity(cityKey).label} based on your calculator selection.`;
    }
    if (isNational) return;

    const data = CITY_CLIMATE[cityKey];
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
    if (list) {
      list.innerHTML = data.bullets.map((b) => `<li>${b}</li>`).join('');
    }
  }

  function updateAll() {
    const r = readCalc();
    renderEstimate(r);
    const cityKey = getCityValue(document.getElementById('asphalt-city'));
    renderLocalFactors(cityKey);
    renderClimateSection(cityKey);
    highlightProjectExample(cityKey);
  }

  function highlightProjectExample(cityKey) {
    const key = cityKey && HOME_EXAMPLES[cityKey] ? cityKey : 'national';
    document.querySelectorAll('[data-project-city]').forEach((card) => {
      const match = card.dataset.projectCity === key;
      card.classList.toggle('project-example-card--active', match);
      card.hidden = false;
    });
  }

  function bindCalc() {
    const form = document.getElementById('asphalt-calc-form');
    if (!form) return;
    form.addEventListener('input', (e) => {
      if (e.target.tagName === 'SELECT') return;
      updateAll();
    });
    form.addEventListener('change', updateAll);
    document.getElementById('asphalt-city')?.addEventListener('change', updateAll);
    updateAll();
  }

  document.querySelectorAll('[data-scroll-calc]').forEach((btn) => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      document.getElementById('calculator')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  });

  bindCalc();
})();

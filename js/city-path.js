/**
 * Geo-scoped URLs:
 *   /texas/dallas/roof-cost-calculator/ → default Dallas in calculators
 *   /texas/roof-cost-calculator/        → default Texas (statewide) in calculators
 */
(function () {
  'use strict';

  /** URL slug → calculator city key (metro suburbs map to parent market) */
  const SLUG_TO_CITY_KEY = {
    dallas: 'dallas',
    plano: 'dallas',
    frisco: 'dallas',
    mckinney: 'dallas',
    irving: 'dallas',
    garland: 'dallas',
    arlington: 'dallas',
    richardson: 'dallas',
    'fort-worth': 'fort-worth',
    austin: 'austin',
    houston: 'houston',
    'round-rock': 'austin',
    'cedar-park': 'austin',
    pflugerville: 'austin',
    georgetown: 'austin',
    leander: 'austin',
    kyle: 'austin',
    'san-antonio': 'san-antonio',
    'san-marcos': 'austin',
    'the-woodlands': 'houston',
    katy: 'houston',
    'sugar-land': 'houston',
    pearland: 'houston',
    'league-city': 'houston',
    cypress: 'houston',
    'new-braunfels': 'san-antonio',
    schertz: 'san-antonio',
    converse: 'san-antonio',
    boerne: 'san-antonio',
    helotes: 'san-antonio',
    'alamo-heights': 'san-antonio',
    keller: 'fort-worth',
    mansfield: 'fort-worth',
    southlake: 'fort-worth',
    burleson: 'fort-worth',
    'north-richland-hills': 'fort-worth',
    grapevine: 'fort-worth',
    phoenix: 'phoenix',
    scottsdale: 'scottsdale',
    mesa: 'mesa',
    chandler: 'chandler',
    gilbert: 'chandler',
    glendale: 'phoenix',
    tempe: 'phoenix',
    peoria: 'phoenix',
    surprise: 'phoenix',
    avondale: 'phoenix',
    goodyear: 'phoenix',
    'paradise-valley': 'scottsdale',
    'fountain-hills': 'scottsdale',
    'cave-creek': 'scottsdale',
    'north-scottsdale': 'scottsdale',
    'mccormick-ranch': 'scottsdale',
    'dc-ranch': 'scottsdale',
    'apache-junction': 'mesa',
    'queen-creek': 'mesa',
    'gold-canyon': 'mesa',
    'red-mountain': 'mesa',
    'superstition-springs': 'mesa',
    eastmark: 'mesa',
    'oro-valley': 'tucson',
    marana: 'tucson',
    sahuarita: 'tucson',
    'green-valley': 'tucson',
    'catalina-foothills': 'tucson',
    vail: 'tucson',
    'sun-lakes': 'chandler',
    ahwatukee: 'chandler',
    ocotillo: 'chandler',
    'san-tan-valley': 'chandler',
    'chandler-heights': 'chandler',
    tampa: 'tampa',
    'st-petersburg': 'st-petersburg',
    clearwater: 'tampa',
    brandon: 'tampa',
    riverview: 'tampa',
    'wesley-chapel': 'tampa',
    lakeland: 'tampa',
    'plant-city': 'tampa',
    kissimmee: 'orlando',
    'winter-park': 'orlando',
    sanford: 'orlando',
    'lake-nona': 'orlando',
    'altamonte-springs': 'orlando',
    oviedo: 'orlando',
    'miami-beach': 'miami',
    'coral-gables': 'miami',
    hialeah: 'miami',
    'fort-lauderdale': 'miami',
    'pembroke-pines': 'miami',
    homestead: 'miami',
    'jacksonville-beach': 'jacksonville',
    'orange-park': 'jacksonville',
    'st-augustine': 'jacksonville',
    'ponte-vedra': 'jacksonville',
    'fernandina-beach': 'jacksonville',
    mandarin: 'jacksonville',
    largo: 'st-petersburg',
    'pinellas-park': 'st-petersburg',
    gulfport: 'st-petersburg',
    'treasure-island': 'st-petersburg',
    seminole: 'st-petersburg',
    orlando: 'orlando',
    miami: 'miami',
    jacksonville: 'jacksonville',
    raleigh: 'raleigh',
    cary: 'cary',
    apex: 'cary',
    durham: 'durham',
    'wake-forest': 'raleigh',
    'chapel-hill': 'durham',
    morrisville: 'cary',
    'holly-springs': 'cary',
    garner: 'raleigh',
    'fuquay-varina': 'cary',
    charlotte: 'charlotte',
    matthews: 'charlotte',
    huntersville: 'charlotte',
    concord: 'charlotte',
    'fort-mill': 'charlotte',
    gastonia: 'charlotte',
    'mint-hill': 'charlotte',
    hillsborough: 'durham',
    creedmoor: 'durham',
    roxboro: 'durham',
    butner: 'durham',
    greensboro: 'national',
    wilmington: 'wilmington',
    'wilmington-beach': 'wilmington',
    'wrightsville-beach': 'wilmington',
    'carolina-beach': 'wilmington',
    leland: 'wilmington',
    hampstead: 'wilmington',
    ogden: 'wilmington',
    'san-diego': 'san-diego',
    'la-jolla': 'san-diego',
    encinitas: 'san-diego',
    carlsbad: 'san-diego',
    'chula-vista': 'san-diego',
    oceanside: 'san-diego',
    escondido: 'san-diego',
    pasadena: 'los-angeles',
    burbank: 'los-angeles',
    'long-beach': 'los-angeles',
    'santa-monica': 'los-angeles',
    torrance: 'los-angeles',
    'beverly-hills': 'los-angeles',
    irvine: 'orange-county',
    anaheim: 'orange-county',
    'santa-ana': 'orange-county',
    'newport-beach': 'orange-county',
    'huntington-beach': 'orange-county',
    'costa-mesa': 'orange-county',
    'elk-grove': 'sacramento',
    roseville: 'sacramento',
    folsom: 'sacramento',
    davis: 'sacramento',
    'citrus-heights': 'sacramento',
    rocklin: 'sacramento',
    oakland: 'san-francisco',
    berkeley: 'san-francisco',
    'san-jose': 'san-francisco',
    'daly-city': 'san-francisco',
    'san-mateo': 'san-francisco',
    'palo-alto': 'san-francisco',
    'los-angeles': 'los-angeles',
    'orange-county': 'orange-county',
    sacramento: 'sacramento',
    'san-francisco': 'san-francisco',
    'las-vegas': 'national',
  };

  const CITY_KEYS = new Set([
    'national',
    'texas',
    'dallas',
    'phoenix',
    'austin',
    'tampa',
    'miami',
    'jacksonville',
    'st-petersburg',
    'charlotte',
    'raleigh',
    'durham',
    'cary',
    'wilmington',
    'scottsdale',
    'mesa',
    'tucson',
    'chandler',
    'houston',
    'orlando',
    'san-antonio',
    'fort-worth',
    'san-diego',
    'los-angeles',
    'orange-county',
    'sacramento',
    'san-francisco',
  ]);

  const STATE_DEFAULT_CITY = {
    texas: 'texas',
    florida: 'tampa',
    arizona: 'phoenix',
    'north-carolina': 'raleigh',
    california: 'san-diego',
  };

  const STATE_LOCATION_KEY = {
    texas: 'tx',
    florida: 'fl',
    arizona: 'az',
    'north-carolina': 'nc',
    california: 'ca',
  };

  const STATE_AVERAGE_LABEL = {
    texas: 'Texas average',
    florida: 'Florida average',
    arizona: 'Arizona average',
    'north-carolina': 'North Carolina average',
    california: 'California average',
  };

  const STATE_SLUGS = new Set(Object.keys(STATE_DEFAULT_CITY));

  const GUIDE_LOCATION_SELECTS = ['kitchen-location', 'bath-location', 'hvac-location', 'roof-location'];

  /** Metro hub city keys shown on /{state}/{city}/ scoped pages */
  const STATE_CITIES = {
    texas: ['dallas', 'houston', 'austin', 'san-antonio', 'fort-worth'],
    florida: ['tampa', 'orlando', 'miami', 'jacksonville', 'st-petersburg'],
    arizona: ['phoenix', 'scottsdale', 'mesa', 'tucson', 'chandler'],
    'north-carolina': ['raleigh', 'charlotte', 'durham', 'cary', 'wilmington'],
    california: ['san-diego', 'los-angeles', 'orange-county', 'sacramento', 'san-francisco'],
  };

  function isGuideLocationSelect(id) {
    return GUIDE_LOCATION_SELECTS.includes(id);
  }

  function isMetroCitySelect(select) {
    if (!select?.id) return false;
    if (select.id === 'quick-city' || select.id.endsWith('-city')) return true;
    return !!select.querySelector(
      'option[value="dallas"], option[value="houston"], option[value="phoenix"], option[value="austin"]'
    );
  }

  function rebuildSelectWithStateCities(select, stateSlug, selectedKey) {
    const cities = STATE_CITIES[stateSlug];
    if (!cities?.length) return;
    select.innerHTML = '';
    cities.forEach((key) => {
      const opt = document.createElement('option');
      opt.value = key;
      opt.textContent = getLocationLabel(key);
      if (key === selectedKey) opt.selected = true;
      select.appendChild(opt);
    });
  }

  function copyReplacements(stateSlug) {
    const label = STATE_AVERAGE_LABEL[stateSlug];
    if (!label) return [];
    const averages = label.replace(/average$/, 'averages');
    return [
      [/National averages/g, averages],
      [/National average/g, label],
    ];
  }

  function parseCityScope() {
    return parseScope();
  }

  function metroQueryCityKey() {
    const metro = new URLSearchParams(window.location.search).get('metro');
    if (!metro) return null;
    return SLUG_TO_CITY_KEY[metro] || null;
  }

  function parseScope() {
    const parts = window.location.pathname.split('/').filter(Boolean);
    if (parts.length < 1 || !STATE_SLUGS.has(parts[0])) return null;

    const stateSlug = parts[0];
    const second = parts[1];
    const cityKeyFromSlug = second ? SLUG_TO_CITY_KEY[second] : null;
    const metroKey = metroQueryCityKey();

    if (second && cityKeyFromSlug) {
      return {
        scope: 'city',
        stateSlug,
        citySlug: second,
        cityKey: metroKey || cityKeyFromSlug,
        stateKey: stateSlug,
        basePrefix: `/${stateSlug}/${second}`,
        metroSlug: metroKey ? new URLSearchParams(window.location.search).get('metro') : null,
      };
    }

    if (parts.length >= 2 || parts.length === 1) {
      const cityKey = STATE_DEFAULT_CITY[stateSlug] || 'national';
      return {
        scope: 'state',
        stateSlug,
        citySlug: null,
        cityKey,
        stateKey: stateSlug,
        basePrefix: `/${stateSlug}`,
      };
    }

    return null;
  }

  function formatCitySlug(slug) {
    return slug
      .split('-')
      .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
      .join(' ');
  }

  function getLocationLabel(cityKey) {
    if (window.EHCCities?.getCity) {
      const c = window.EHCCities.getCity(cityKey);
      if (c?.label) return c.label;
    }
    if (cityKey === 'texas') return STATE_AVERAGE_LABEL.texas;
    if (cityKey === 'national') return 'National average';
    return formatCitySlug(cityKey);
  }

  function ensureStatewideOption(select, scope) {
    if (scope.stateKey !== 'texas' || !select) return;
    if (select.querySelector('option[value="texas"]')) return;
    const opt = document.createElement('option');
    opt.value = 'texas';
    opt.textContent = STATE_AVERAGE_LABEL.texas;
    const national = select.querySelector('option[value="national"]');
    if (national && national.nextSibling) {
      national.insertAdjacentElement('afterend', opt);
    } else {
      select.insertBefore(opt, select.firstChild);
    }
  }

  function configureGuideLocationSelects(scope) {
    if (scope.scope === 'city') {
      const cities = STATE_CITIES[scope.stateSlug];
      if (!cities?.length) return;
      GUIDE_LOCATION_SELECTS.forEach((id) => {
        const sel = document.getElementById(id);
        if (!sel) return;
        rebuildSelectWithStateCities(sel, scope.stateSlug, scope.cityKey);
      });
      return;
    }

    const locKey = STATE_LOCATION_KEY[scope.stateSlug];
    const label = STATE_AVERAGE_LABEL[scope.stateSlug];
    if (!locKey || !label) return;

    GUIDE_LOCATION_SELECTS.forEach((id) => {
      const sel = document.getElementById(id);
      if (!sel) return;
      const stateOpt = sel.querySelector(`option[value="${locKey}"]`);
      const national = sel.querySelector('option[value="national"]');
      if (stateOpt) stateOpt.textContent = label;
      if (scope.scope === 'state') {
        if (national) {
          national.hidden = true;
          national.disabled = true;
        }
        if (stateOpt) sel.value = locKey;
      }
    });
  }

  function configureCitySelects(scope) {
    document.querySelectorAll('select').forEach((sel) => {
      if (isGuideLocationSelect(sel.id)) return;

      if (scope.scope === 'city' && STATE_CITIES[scope.stateSlug] && isMetroCitySelect(sel)) {
        rebuildSelectWithStateCities(sel, scope.stateSlug, scope.cityKey);
        return;
      }

      if (scope.stateSlug && STATE_SLUGS.has(scope.stateSlug)) {
        ensureStatewideOption(sel, scope);
        if (scope.stateKey === 'texas') {
          const texas = sel.querySelector('option[value="texas"]');
          if (texas) texas.textContent = STATE_AVERAGE_LABEL.texas;
        }
        if (scope.scope === 'state') {
          const national = sel.querySelector('option[value="national"]');
          if (national) {
            national.hidden = true;
            national.disabled = true;
          }
        }
      }

      if (sel.querySelector(`option[value="${scope.cityKey}"]`)) {
        sel.value = scope.cityKey;
      }
    });
  }

  function replaceNationalCopyInMain(stateSlug) {
    const main = document.getElementById('main');
    const replacements = copyReplacements(stateSlug);
    if (!main || !replacements.length) return;

    const walker = document.createTreeWalker(main, NodeFilter.SHOW_TEXT, {
      acceptNode(node) {
        const parent = node.parentElement;
        if (!parent || parent.closest('script, style, noscript')) {
          return NodeFilter.FILTER_REJECT;
        }
        if (!node.textContent.trim()) return NodeFilter.FILTER_REJECT;
        return NodeFilter.FILTER_ACCEPT;
      },
    });

    const textNodes = [];
    while (walker.nextNode()) textNodes.push(walker.currentNode);

    textNodes.forEach((node) => {
      let text = node.textContent;
      replacements.forEach(([pattern, replacement]) => {
        text = text.replace(pattern, replacement);
      });
      if (text !== node.textContent) node.textContent = text;
    });

    const avgLabel = STATE_AVERAGE_LABEL[stateSlug];
    if (avgLabel) {
      main.querySelectorAll('[aria-label]').forEach((el) => {
        const aria = el.getAttribute('aria-label');
        if (!aria || !/national average/i.test(aria)) return;
        el.setAttribute('aria-label', aria.replace(/National average/gi, avgLabel));
      });
    }
  }

  function updateHeroLocationLabels(cityKey) {
    const label = getLocationLabel(cityKey);
    const averagesLabel = label.includes('average')
      ? label.replace(/average$/, 'averages')
      : `${label} averages`;

    document.querySelectorAll('.cost-hero-card-label').forEach((el) => {
      if (/National average/i.test(el.textContent)) el.textContent = label;
    });

    document.querySelectorAll('.snapshot-label').forEach((el) => {
      if (/National average/i.test(el.textContent)) el.textContent = label;
    });

    document.querySelectorAll('.hero-eyebrow').forEach((el) => {
      if (/National averages/i.test(el.textContent)) el.textContent = averagesLabel;
    });

    document.querySelectorAll('.cost-hero-aside[aria-label]').forEach((el) => {
      const aria = el.getAttribute('aria-label');
      if (aria && /National average/i.test(aria)) {
        el.setAttribute('aria-label', aria.replace(/National average/gi, label));
      }
    });
  }

  function injectStateBreadcrumb(scope) {
    const ol = document.querySelector('.breadcrumb ol');
    if (!ol || ol.dataset.stateBreadcrumb) return;

    const home = ol.querySelector('li:first-child');
    if (!home) return;

    const path = window.location.pathname.replace(/\/$/, '') || '/';
    if (path === `/${scope.stateSlug}`) return;

    const STATE_NAMES = {
      texas: 'Texas',
      florida: 'Florida',
      arizona: 'Arizona',
      'north-carolina': 'North Carolina',
      california: 'California',
    };
    const stateName = STATE_NAMES[scope.stateSlug] || formatCitySlug(scope.stateSlug);
    const stateLi = document.createElement('li');
    stateLi.innerHTML = `<a href="/${scope.stateSlug}/">${stateName}</a>`;
    home.insertAdjacentElement('afterend', stateLi);

    if (scope.scope === 'city' && scope.citySlug) {
      const cityLi = document.createElement('li');
      const cityLabel = getLocationLabel(scope.cityKey);
      const cityName = cityLabel.includes(',') ? cityLabel.split(',')[0] : formatCitySlug(scope.citySlug);
      cityLi.innerHTML = `<a href="/${scope.stateSlug}/${scope.citySlug}/">${cityName}</a>`;
      stateLi.insertAdjacentElement('afterend', cityLi);
    }

    ol.dataset.stateBreadcrumb = '1';
  }

  function applyStatePageContext(scope) {
    if (!scope || !STATE_SLUGS.has(scope.stateSlug)) return;

    document.documentElement.classList.add(`geo-scope--${scope.stateSlug}`);
    document.body.classList.add(`geo-scope--${scope.stateSlug}`);
    if (scope.scope === 'state') {
      document.documentElement.classList.add(`geo-scope--${scope.stateSlug}-state`);
      document.body.classList.add(`geo-scope--${scope.stateSlug}-state`);
    }

    injectStateBreadcrumb(scope);
    configureGuideLocationSelects(scope);
    configureCitySelects(scope);

    if (scope.scope === 'state') {
      replaceNationalCopyInMain(scope.stateSlug);
    }

    updateHeroLocationLabels(scope.cityKey);
  }

  function bindSelectLabelSync() {
    document.addEventListener('change', (e) => {
      if (e.target.tagName !== 'SELECT') return;
      const scope = parseScope();
      if (!scope || !STATE_SLUGS.has(scope.stateSlug)) return;
      const id = e.target.id;
      if (
        !['quick-city', 'roof-city', 'hvac-city', 'fence-city', 'flooring-city', 'solar-city'].includes(id) &&
        !id.endsWith('-city') &&
        !isGuideLocationSelect(id)
      ) {
        return;
      }
      let key = e.target.value;
      const locKey = STATE_LOCATION_KEY[scope.stateSlug];
      if (isGuideLocationSelect(id) && locKey && key === locKey && scope.stateSlug === 'texas') {
        key = 'texas';
      }
      updateHeroLocationLabels(key);
    });
  }

  function applyDefaultCityFromPath() {
    const scope = parseScope();
    if (!scope) return null;

    configureCitySelects(scope);

    window.EHC_CITY_SCOPE = scope;
    applyStatePageContext(scope);
    document.dispatchEvent(new CustomEvent('ehc:city-scope', { detail: scope }));
    return scope;
  }

  function prefixPath(path, basePrefix) {
    if (!path || path[0] !== '/') return path;
    if (path.startsWith(basePrefix)) return path;
    if (path === '/' || path.startsWith('/privacy') || path.startsWith('/terms')) return path;
    if (/^\/[a-z-]+\/[a-z0-9-]+\//.test(path)) return path;
    return basePrefix.replace(/\/$/, '') + path;
  }

  bindSelectLabelSync();
  applyDefaultCityFromPath();

  window.EHCCityPath = {
    parseCityScope,
    parseScope,
    applyDefaultCityFromPath,
    applyStatePageContext,
    applyTexasPageContext: applyStatePageContext,
    prefixPath,
    SLUG_TO_CITY_KEY,
    STATE_DEFAULT_CITY,
    STATE_LOCATION_KEY,
    STATE_AVERAGE_LABEL,
  };
})();

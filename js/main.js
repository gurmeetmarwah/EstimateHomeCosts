/**
 * Estimate Home Costs — client interactions
 */
(function () {
  'use strict';

  const SUGGESTIONS = [
  { text: 'roof replacement', label: 'Roof replacement' },
  { text: 'HVAC install', label: 'HVAC installation' },
  { text: 'bathroom remodel', label: 'Bathroom remodel' },
  { text: 'fence installation', label: 'Fence installation' },
  { text: 'kitchen remodel', label: 'Kitchen remodel' },
  { text: 'flooring installation', label: 'Flooring' },
  { text: 'window replacement', label: 'Windows' },
  { text: 'solar panel install', label: 'Solar panels' },
  { text: 'deck build', label: 'Deck construction' },
  { text: 'garage door replacement', label: 'Garage door' },
  ];

  const searchInput = document.getElementById('project-search');
  const suggestionsEl = document.getElementById('search-suggestions');
  const navToggle = document.querySelector('.nav-toggle');
  const mobileNav = document.getElementById('mobile-nav');
  const estimateBtn = document.querySelector('[data-action="estimate"]');
  let activeIndex = -1;

  function filterSuggestions(query) {
    const q = query.trim().toLowerCase();
    if (!q) return SUGGESTIONS.slice(0, 6);
    return SUGGESTIONS.filter((s) => s.text.includes(q) || s.label.toLowerCase().includes(q)).slice(0, 8);
  }

  function renderSuggestions(items) {
    if (!suggestionsEl) return;
    suggestionsEl.innerHTML = '';
    if (items.length === 0) {
      suggestionsEl.hidden = true;
      searchInput?.setAttribute('aria-expanded', 'false');
      return;
    }
    items.forEach((item, i) => {
      const li = document.createElement('li');
      li.setAttribute('role', 'option');
      li.id = `suggestion-${i}`;
      li.textContent = item.label;
      li.dataset.value = item.text;
      if (i === activeIndex) li.setAttribute('aria-selected', 'true');
      li.addEventListener('mousedown', (e) => {
        e.preventDefault();
        selectSuggestion(item.text);
      });
      suggestionsEl.appendChild(li);
    });
    suggestionsEl.hidden = false;
    searchInput?.setAttribute('aria-expanded', 'true');
  }

  function selectSuggestion(value) {
    if (searchInput) {
      searchInput.value = value;
      searchInput.focus();
    }
    hideSuggestions();
    navigateToSearch(value);
  }

  function hideSuggestions() {
    if (suggestionsEl) {
      suggestionsEl.hidden = true;
      suggestionsEl.innerHTML = '';
    }
    searchInput?.setAttribute('aria-expanded', 'false');
    activeIndex = -1;
  }

  const SEARCH_ROUTES = {
    'roof replacement': '/cost/roof-replacement/',
    'roof': '/cost/roof-replacement/',
    'roof cost calculator': '/roof-cost-calculator/',
    'roof calculator': '/roof-cost-calculator/',
    'asphalt shingle roof cost': '/roofing-materials/asphalt-shingle-roof-cost/',
    'asphalt shingles': '/roofing-materials/asphalt-shingle-roof-cost/',
    'asphalt roof cost': '/roofing-materials/asphalt-shingle-roof-cost/',
    'metal roof cost': '/roofing-materials/metal-roof-cost/',
    'metal roofing': '/roofing-materials/metal-roof-cost/',
    'standing seam metal roof': '/roofing-materials/metal-roof-cost/',
    'tile roof cost': '/roofing-materials/tile-roof-cost/',
    'tile roofing': '/roofing-materials/tile-roof-cost/',
    'clay tile roof': '/roofing-materials/tile-roof-cost/',
    'concrete tile roof': '/roofing-materials/tile-roof-cost/',
    'slate roof cost': '/roofing-materials/slate-roof-cost/',
    'slate roofing': '/roofing-materials/slate-roof-cost/',
    'natural slate roof': '/roofing-materials/slate-roof-cost/',
    'wood shake roof cost': '/roofing-materials/wood-shake-roof-cost/',
    'wood shake roofing': '/roofing-materials/wood-shake-roof-cost/',
    'cedar shake roof': '/roofing-materials/wood-shake-roof-cost/',
    'hvac installation': '/cost/hvac-installation/',
    'hvac install': '/cost/hvac-installation/',
    'hvac cost calculator': '/hvac-cost-calculator/',
    'hvac calculator': '/hvac-cost-calculator/',
    'central ac cost': '/hvac-cost-calculator/central-ac/',
    'central ac calculator': '/hvac-cost-calculator/central-ac/',
    'central air conditioning cost': '/hvac-cost-calculator/central-ac/',
    'central air cost': '/hvac-cost-calculator/central-ac/',
    'heat pump cost': '/hvac-cost-calculator/heat-pump/',
    'heat pump cost calculator': '/hvac-cost-calculator/heat-pump/',
    'mini split cost': '/hvac-cost-calculator/mini-split/',
    'mini split cost calculator': '/hvac-cost-calculator/mini-split/',
    'ductless mini split cost': '/hvac-cost-calculator/mini-split/',
    'furnace and ac cost': '/hvac-cost-calculator/furnace-ac/',
    'furnace ac cost': '/hvac-cost-calculator/furnace-ac/',
    'geothermal cost': '/hvac-cost-calculator/geothermal/',
    'geothermal hvac cost': '/hvac-cost-calculator/geothermal/',
    'hvac': '/cost/hvac-installation/',
    'fence cost calculator': '/fence-cost-calculator/',
    'fence calculator': '/fence-cost-calculator/',
    'fence installation': '/fence-cost-calculator/',
    'wood privacy fence cost': '/fence-materials/wood-privacy-fence-cost/',
    'cedar privacy fence cost': '/fence-materials/wood-privacy-fence-cost/',
    'wood fence cost': '/fence-materials/wood-privacy-fence-cost/',
    'privacy fence cost': '/fence-materials/wood-privacy-fence-cost/',
    'vinyl fence cost': '/fence-materials/vinyl-fence-cost/',
    'vinyl fencing cost': '/fence-materials/vinyl-fence-cost/',
    'composite fence cost': '/fence-materials/composite-fence-cost/',
    'chain link fence cost': '/fence-materials/chain-link-fence-cost/',
    'chain link fence': '/fence-materials/chain-link-fence-cost/',
    'aluminum fence cost': '/fence-materials/aluminum-fence-cost/',
    'flooring cost calculator': '/flooring-cost-calculator/',
    'flooring calculator': '/flooring-cost-calculator/',
    'flooring': '/flooring-cost-calculator/',
    'luxury vinyl plank cost': '/flooring-materials/luxury-vinyl-plank-flooring-cost/',
    'lvp flooring cost': '/flooring-materials/luxury-vinyl-plank-flooring-cost/',
    'lvp cost': '/flooring-materials/luxury-vinyl-plank-flooring-cost/',
    'vinyl plank flooring cost': '/flooring-materials/luxury-vinyl-plank-flooring-cost/',
    'hardwood floor cost': '/flooring-materials/solid-hardwood-flooring-cost/',
    'solid hardwood flooring cost': '/flooring-materials/solid-hardwood-flooring-cost/',
    'engineered wood flooring cost': '/flooring-materials/engineered-wood-flooring-cost/',
    'porcelain tile floor cost': '/flooring-materials/porcelain-tile-flooring-cost/',
    'tile flooring cost': '/flooring-materials/porcelain-tile-flooring-cost/',
    'carpet installation cost': '/flooring-materials/carpet-flooring-cost/',
    'carpet cost per square foot': '/flooring-materials/carpet-flooring-cost/',
    'solar panel cost calculator': '/solar-panel-cost-calculator/',
    'solar cost calculator': '/solar-panel-cost-calculator/',
    'solar calculator': '/solar-panel-cost-calculator/',
    'solar panel cost': '/solar-panel-cost-calculator/',
    'solar installation cost': '/solar-panel-cost-calculator/',
    'dallas home costs': '/texas/dallas/',
    'dallas tx': '/texas/dallas/',
    'home project costs dallas': '/texas/dallas/',
    'phoenix home costs': '/arizona/phoenix/',
    'phoenix az': '/arizona/phoenix/',
    'tampa home costs': '/florida/tampa/',
    'tampa fl': '/florida/tampa/',
    'austin home costs': '/texas/austin/',
    'austin tx': '/texas/austin/',
    'raleigh home costs': '/north-carolina/raleigh/',
    'raleigh nc': '/north-carolina/raleigh/',
    'san diego home costs': '/california/san-diego/',
    'san diego ca': '/california/san-diego/',
    'metal roof vs shingles': '/compare/metal-roof-vs-shingles/',
    'metal vs shingles': '/compare/metal-roof-vs-shingles/',
    'heat pump vs ac': '/compare/heat-pump-vs-ac/',
    'heat pump vs central ac': '/compare/heat-pump-vs-ac/',
    'vinyl vs wood fence': '/compare/vinyl-vs-wood-fence/',
    'quartz vs granite': '/compare/quartz-vs-granite-countertops/',
    'quartz vs granite countertops': '/compare/quartz-vs-granite-countertops/',
    'bathroom remodel': '/cost/bathroom-remodel/',
    'bathroom': '/cost/bathroom-remodel/',
    'kitchen remodel': '/cost/kitchen-remodel/',
    'kitchen': '/cost/kitchen-remodel/',
  };

  function navigateToSearch(query) {
    const q = query.trim().toLowerCase();
    for (const [key, path] of Object.entries(SEARCH_ROUTES)) {
      if (q.includes(key)) {
        window.location.href = path;
        return;
      }
    }
    window.location.href = `/search?q=${encodeURIComponent(query.trim())}`;
  }

  if (searchInput && suggestionsEl) {
    searchInput.addEventListener('input', () => {
      activeIndex = -1;
      renderSuggestions(filterSuggestions(searchInput.value));
    });

    searchInput.addEventListener('focus', () => {
      renderSuggestions(filterSuggestions(searchInput.value));
    });

    searchInput.addEventListener('blur', () => {
      setTimeout(hideSuggestions, 150);
    });

    searchInput.addEventListener('keydown', (e) => {
      const items = suggestionsEl.querySelectorAll('[role="option"]');
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        activeIndex = Math.min(activeIndex + 1, items.length - 1);
        updateActiveOption(items);
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        activeIndex = Math.max(activeIndex - 1, 0);
        updateActiveOption(items);
      } else if (e.key === 'Enter') {
        e.preventDefault();
        if (activeIndex >= 0 && items[activeIndex]) {
          selectSuggestion(items[activeIndex].dataset.value);
        } else if (searchInput.value.trim()) {
          navigateToSearch(searchInput.value);
        }
      } else if (e.key === 'Escape') {
        hideSuggestions();
      }
    });
  }

  function updateActiveOption(items) {
    items.forEach((el, i) => {
      el.setAttribute('aria-selected', i === activeIndex ? 'true' : 'false');
    });
    if (items[activeIndex]) {
      searchInput.setAttribute('aria-activedescendant', items[activeIndex].id);
    }
  }

  if (estimateBtn && searchInput) {
    estimateBtn.addEventListener('click', () => {
      const q = searchInput.value.trim();
      if (q) navigateToSearch(q);
      else searchInput.focus();
    });
  }

  if (navToggle && mobileNav) {
    navToggle.addEventListener('click', () => {
      const open = mobileNav.classList.toggle('is-open');
      mobileNav.hidden = !open;
      navToggle.setAttribute('aria-expanded', String(open));
      navToggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    });

    mobileNav.querySelectorAll('a').forEach((link) => {
      link.addEventListener('click', () => {
        mobileNav.classList.remove('is-open');
        mobileNav.hidden = true;
        navToggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

  const cityLookupForm = document.getElementById('city-lookup-form');
  if (cityLookupForm) {
    cityLookupForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const path = cityLookupForm.querySelector('#city-select')?.value;
      if (!path) {
        alert('Please select a city.');
        return;
      }
      window.location.href = path;
    });
  }

  const header = document.querySelector('.site-header');
  if (header) {
    let lastScroll = 0;
    window.addEventListener(
      'scroll',
      () => {
        const y = window.scrollY;
        header.style.boxShadow = y > 20 ? 'var(--shadow-sm)' : 'none';
        lastScroll = y;
      },
      { passive: true }
    );
  }
})();

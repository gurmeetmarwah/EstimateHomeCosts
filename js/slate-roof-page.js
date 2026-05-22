/**
 * Slate roof cost landing page config
 */
(function () {
  'use strict';

  window.initMaterialRoofPage({
    formId: 'slate-calc-form',
    sqftId: 'slate-sqft',
    variantId: 'slate-variant',
    cityId: 'slate-city',
    defaultVariant: 'natural',
    variants: {
      natural: { material: 8.5, labor: 5.5, label: 'Natural slate' },
      synthetic: { material: 6.0, labor: 4.2, label: 'Synthetic slate' },
      hybrid: { material: 7.0, labor: 4.6, label: 'Hybrid / slate-look systems' },
    },
    climateNationalLead:
      'Natural slate excels in freeze-thaw and historic markets. Select a city in the calculator for localized guidance.',
    cityClimate: {
      dallas: {
        rating: 'Fair — hail & cost',
        ratingClass: 'fair',
        summary: 'Slate is rare in Dallas mainstream re-roofs — hail and cost favor metal or impact asphalt; slate appears on custom and historic homes.',
        bullets: [
          'Hail can chip natural slate — discuss product hardness and insurance',
          'Fewer certified slate crews than asphalt or metal',
          'Heavy load — structural review required',
          'Strong curb appeal in luxury and estate neighborhoods',
        ],
      },
      houston: {
        rating: 'Fair',
        ratingClass: 'fair',
        summary: 'Humid Gulf Coast climate demands expert underlayment behind slate — limited installer base outside high-end custom work.',
        bullets: [
          'Moisture management and ventilation critical under slate',
          'Wind attachment must meet coastal codes on permitted jobs',
          'Synthetic slate sometimes used for weight savings',
          'Premium pricing vs concrete tile in many suburbs',
        ],
      },
      austin: {
        rating: 'Fair',
        ratingClass: 'fair',
        summary: 'Austin slate is niche on hill country custom homes — heat and hail make metal and tile more common for volume re-roofs.',
        bullets: [
          'Historic and European-style estates may specify natural slate',
          'Long install timelines vs asphalt crews',
          'Synthetic options reduce weight on some truss designs',
          'Budget often 2–3× architectural asphalt on same footprint',
        ],
      },
      phoenix: {
        rating: 'Poor — heat & scarcity',
        ratingClass: 'poor',
        summary: 'Phoenix rarely uses natural slate — extreme heat, UV, and regional style favor tile or metal; synthetic slate is occasional on custom builds.',
        bullets: [
          'Thermal movement and underlayment failure risk in desert sun',
          'Very few local slate specialists — travel labor adds cost',
          'Tile and metal dominate premium desert architecture',
          'Weight and cost rarely justify slate vs regional alternatives',
        ],
      },
      scottsdale: {
        rating: 'Fair — custom only',
        ratingClass: 'fair',
        summary: 'Scottsdale ultra-luxury custom homes may use slate-look or imported slate — still uncommon vs tile and standing seam.',
        bullets: [
          'Designer homes seeking East Coast stone aesthetics',
          'Premium labor and long lead times for natural stone',
          'HOA and style boards may prefer tile profiles',
          'Synthetic slate used when weight is a constraint',
        ],
      },
      tampa: {
        rating: 'Fair',
        ratingClass: 'fair',
        summary: 'Florida slate is uncommon — humidity, hurricanes, and tile prevalence limit natural slate to select historic renovations.',
        bullets: [
          'Wind-rated fastening and sealed decks mandatory',
          'Underlayment life often governs maintenance cycles',
          'Concrete tile delivers similar prestige at lower weight',
          'Specialty importers for true slate increase lead time',
        ],
      },
      orlando: {
        rating: 'Fair',
        ratingClass: 'fair',
        summary: 'Central Florida slate is rare outside historic districts — most premium re-roofs choose tile or metal.',
        bullets: [
          'Humidity: breathable underlayment assemblies essential',
          'Limited local quarried slate — freight adds cost',
          'Insurance and wind codes favor tested systems',
          'Synthetic slate occasional on custom Mediterranean builds',
        ],
      },
      charlotte: {
        rating: 'Good — Southeast slate belt',
        ratingClass: 'good',
        summary: 'Charlotte and Carolina foothills see more slate on traditional and luxury homes than Sun Belt metros — still a specialist market.',
        bullets: [
          'Natural slate fits Colonial and Tudor revival styles',
          'Moderate freeze-thaw suits durable stone roofs',
          'Fewer installers than asphalt — plan longer schedules',
          'Strong longevity when flashings and underlayment are maintained',
        ],
      },
      raleigh: {
        rating: 'Good',
        ratingClass: 'good',
        summary: 'Raleigh–Durham custom and historic neighborhoods use slate for authenticity — growing interest on high-end infill.',
        bullets: [
          'Triangle architects specify slate on period-accurate homes',
          'Synthetic slate lowers weight on older framing',
          'Competes with metal for longevity-focused owners',
          'Premium cost per year still competitive over 50+ years',
        ],
      },
      'san-diego': {
        rating: 'Fair',
        ratingClass: 'fair',
        summary: 'San Diego slate appears on coastal traditional homes — salt air and cost push many owners to tile or metal instead.',
        bullets: [
          'Copper or stainless flashings recommended near ocean air',
          'Historic districts may require slate or slate-look products',
          'California labor rates push installed cost above national slate average',
          'Title 24 less central than cool-roof rules on flat commercial',
        ],
      },
    },
    homeExamples: {
      national: { sqft: 2000, cost: 31500 },
      charlotte: { sqft: 2000, cost: 29300 },
      raleigh: { sqft: 1950, cost: 29800 },
      'san-diego': { sqft: 1850, cost: 34200 },
    },
  });
})();

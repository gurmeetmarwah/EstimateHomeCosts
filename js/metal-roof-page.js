/**
 * Metal roof cost landing page config
 */
(function () {
  'use strict';

  window.initMaterialRoofPage({
    formId: 'metal-calc-form',
    sqftId: 'metal-sqft',
    variantId: 'metal-variant',
    cityId: 'metal-city',
    defaultVariant: 'standing-seam',
    variants: {
      'standing-seam': { material: 4.2, labor: 3.8, label: 'Standing seam metal' },
      corrugated: { material: 3.4, labor: 3.2, label: 'Corrugated / exposed fastener' },
      'metal-shingle': { material: 4.0, labor: 3.6, label: 'Metal shingles' },
    },
    climateNationalLead:
      'Metal excels in snow, fire zones, and long ownership horizons. Select a city in the calculator for localized guidance.',
    cityClimate: {
      dallas: {
        rating: 'Excellent — hail country',
        ratingClass: 'good',
        summary: 'Metal is a top choice in Dallas–Fort Worth: hail resistance, insurance credits, and strong resale in many suburbs.',
        bullets: [
          'Standing seam and Class 4-rated systems common in hail corridors',
          'Cosmetic denting possible — discuss insurance and finish warranties',
          'Reflective coatings reduce summer attic heat vs dark asphalt',
          'Verify installer experience with concealed-fastener systems',
        ],
      },
      houston: {
        rating: 'Good — wind & humidity',
        ratingClass: 'good',
        summary: 'Coastal-adjacent Houston favors metal for wind uplift and longevity, with proper fastening and corrosion details.',
        bullets: [
          'Wind-rated concealed fastener systems for Gulf exposure',
          'Marine-grade or coated steel/aluminum near salt air',
          'Full tear-off and moisture barriers standard on re-roofs',
          'Competes with tile in premium coastal neighborhoods',
        ],
      },
      austin: {
        rating: 'Excellent',
        ratingClass: 'good',
        summary: 'Central Texas homeowners increasingly choose metal for hail performance and lower lifetime cost per year.',
        bullets: [
          'Hail: metal often outperforms asphalt for long-term claims history',
          'Heat: light colors and cool-roof coatings widely available',
          'Modern farmhouses and contemporary builds favor standing seam',
          'Strong contractor base for residential metal installs',
        ],
      },
      phoenix: {
        rating: 'Excellent — heat & sun',
        ratingClass: 'good',
        summary: 'Phoenix and desert metros are prime metal markets: reflectivity, durability, and compatibility with tile aesthetics at lower weight on some profiles.',
        bullets: [
          'High solar reflectance reduces cooling load vs asphalt',
          'Does not brittle-crack like shingles under extreme UV',
          'Stone-coated metal profiles compete with concrete tile visually',
          'Thermal movement requires experienced expansion-joint detailing',
        ],
      },
      scottsdale: {
        rating: 'Excellent — premium desert',
        ratingClass: 'good',
        summary: 'Scottsdale luxury builds use standing seam and designer metal profiles alongside tile — metal fits contemporary desert architecture.',
        bullets: [
          'Premium Kynar finishes for color retention in intense sun',
          'HOA-friendly profiles that complement modern desert homes',
          'Higher labor rates — budget above national metal averages',
          'Often paired with foam or batten systems on complex roofs',
        ],
      },
      tampa: {
        rating: 'Good — hurricane market',
        ratingClass: 'good',
        summary: 'Florida coastal codes favor tested metal systems; product approval and fastening schedules are critical on every permit.',
        bullets: [
          'Florida Product Approval required for metal panels used',
          'Wind uplift clips and enhanced fastening in HVHZ zones',
          'Aluminum popular for corrosion resistance near coast',
          'Insurance wind mitigation credits may apply',
        ],
      },
      orlando: {
        rating: 'Good',
        ratingClass: 'good',
        summary: 'Central Florida metal installs focus on wind ratings and sealed decks — strong alternative to asphalt on inland homes.',
        bullets: [
          'Wind-rated systems standard for permitted re-roofs',
          'Lighter than concrete tile — less structural load on trusses',
          'Noise myths largely addressed with solid decking and underlayment',
          'Growing share of new construction in master-planned communities',
        ],
      },
      charlotte: {
        rating: 'Good',
        ratingClass: 'good',
        summary: 'Charlotte\'s moderate climate suits metal well; snow shedding and longevity appeal to 15+ year owners.',
        bullets: [
          'Snow and ice slide off standing seam more easily than shingles',
          'Moderate labor costs vs Northeast coastal markets',
          'Increasing adoption in upscale infill and lake communities',
          'Fire resistance valued in wooded lot subdivisions',
        ],
      },
      raleigh: {
        rating: 'Good',
        ratingClass: 'good',
        summary: 'Triangle-area metal adoption is rising for tech-corridor homeowners prioritizing durability and energy performance.',
        bullets: [
          'Standing seam popular on modern and transitional home styles',
          'Algae and humidity less damaging to metal than organic shingles',
          'Competitive install market vs scarce slate crews',
          'Good match for homes with solar — shared mounting expertise',
        ],
      },
      'san-diego': {
        rating: 'Good — coastal & codes',
        ratingClass: 'good',
        summary: 'San Diego metal works on contemporary coastal homes when corrosion details and Title 24 reflectance requirements are met.',
        bullets: [
          'Coastal salt: aluminum or coated steel with proper flashing',
          'Cool-roof / solar reflectance aligns with California energy rules',
          'Competes with tile on weight and fire class in WUI zones',
          'Premium labor market — detailed shop drawings common',
        ],
      },
    },
    homeExamples: {
      national: { sqft: 2000, cost: 22400 },
      dallas: { sqft: 2100, cost: 19800 },
      phoenix: { sqft: 1950, cost: 24200 },
      tampa: { sqft: 1980, cost: 23600 },
      'san-diego': { sqft: 1850, cost: 26800 },
    },
  });
})();

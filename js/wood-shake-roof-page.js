/**
 * Wood shake roof cost landing page config
 */
(function () {
  'use strict';

  window.initMaterialRoofPage({
    formId: 'wood-calc-form',
    sqftId: 'wood-sqft',
    variantId: 'wood-variant',
    cityId: 'wood-city',
    defaultVariant: 'cedar-shake',
    variants: {
      'cedar-shake': { material: 3.8, labor: 3.4, label: 'Cedar shake' },
      'cedar-shingle': { material: 3.2, labor: 3.0, label: 'Cedar shingle' },
      'composite-shake': { material: 4.0, labor: 3.2, label: 'Composite / faux shake' },
    },
    climateNationalLead:
      'Wood shake fits mild, dry climates and rustic architecture. Select a city in the calculator for localized guidance.',
    cityClimate: {
      dallas: {
        rating: 'Fair — fire & hail',
        ratingClass: 'fair',
        summary: 'Dallas allows wood in some areas but fire codes and hail push many HOAs toward asphalt or metal — cedar still used on ranch and rustic styles.',
        bullets: [
          'Class A fire-treated shakes often required',
          'Hail damage can split shakes — insurance review recommended',
          'Lower upfront cost than tile or slate on same home',
          'Maintenance: cleaning, staining, and spot replacements',
        ],
      },
      houston: {
        rating: 'Poor — humidity',
        ratingClass: 'poor',
        summary: 'Gulf Coast humidity accelerates moss, rot, and fastener corrosion on wood — metal and tile dominate premium coastal re-roofs.',
        bullets: [
          'High moisture — ventilation and treated wood mandatory',
          'Hurricane wind ratings harder to achieve vs engineered systems',
          'Many municipalities restrict untreated wood roofing',
          'Shorter effective lifespan than dry-climate installs',
        ],
      },
      austin: {
        rating: 'Good — Hill Country',
        ratingClass: 'good',
        summary: 'Central Texas Hill Country and lake homes commonly use cedar shake for rustic curb appeal — fire-treated products standard.',
        bullets: [
          'Matches ranch, farmhouse, and waterfront aesthetics',
          'Treated cedar shakes widely available from local suppliers',
          'Algae less issue than humid coast if ventilation is sound',
          'Competes with metal on character homes seeking natural look',
        ],
      },
      phoenix: {
        rating: 'Fair — dry but fire',
        ratingClass: 'fair',
        summary: 'Phoenix wood shake is limited by fire codes and UV — composite shake used where HOA allows wood appearance.',
        bullets: [
          'WUI and municipal codes may prohibit wood roofing',
          'Extreme UV dries untreated wood quickly',
          'Composite shake offers look with better fire class',
          'Tile and metal more common on desert luxury homes',
        ],
      },
      scottsdale: {
        rating: 'Fair',
        ratingClass: 'fair',
        summary: 'Scottsdale wood roofs are rare on new builds — fire risk and HOA standards favor tile, metal, or composite shake profiles.',
        bullets: [
          'Fire-treated shakes required where wood is permitted',
          'Premium labor for hand-split appearance details',
          'HOAs often restrict wood in favor of tile aesthetics',
          'Composite alternatives mimic shake without natural rot risk',
        ],
      },
      tampa: {
        rating: 'Poor — humidity & wind',
        ratingClass: 'poor',
        summary: 'Florida humidity and hurricanes make wood shake uncommon — most codes and insurers favor tile, metal, or asphalt.',
        bullets: [
          'Moisture and mold risk without aggressive maintenance',
          'Wind uplift concerns on coastal permits',
          'Short replacement cycles vs tile in Gulf markets',
          'Composite shake rare — tile dominates coastal premium',
        ],
      },
      orlando: {
        rating: 'Poor',
        ratingClass: 'poor',
        summary: 'Central Florida wood roofing is niche — humidity and storm exposure favor non-combustible materials.',
        bullets: [
          'Frequent algae and moisture under wood assemblies',
          'Insurance may surcharge or limit wood roof coverage',
          'Treated shakes still outperformed by tile in lifespan',
          'Rustic resorts may use composite for appearance only',
        ],
      },
      charlotte: {
        rating: 'Good',
        ratingClass: 'good',
        summary: 'Charlotte and Carolina piedmont use cedar on traditional and mountain-lake homes — moderate humidity manageable with treatment.',
        bullets: [
          'Popular on Craftsman and cottage-style renovations',
          'Fire-treated cedar meets many county codes',
          'Algae possible — zinc strips and ventilation help',
          'Mid-range cost between asphalt and metal',
        ],
      },
      raleigh: {
        rating: 'Good',
        ratingClass: 'good',
        summary: 'Raleigh wood shake fits wooded lots and custom homes — growing composite shake share for lower maintenance.',
        bullets: [
          'Triangle suburbs with tree cover favor natural aesthetics',
          'HOA rules vary — verify wood approval before ordering',
          'Composite shake reduces rot risk vs untreated cedar',
          'Inspectors focus on fire rating and proper offset courses',
        ],
      },
      'san-diego': {
        rating: 'Fair — coastal dry',
        ratingClass: 'fair',
        summary: 'San Diego coastal and canyon homes occasionally use cedar — fire zones and salt air require treated products and metal flashings.',
        bullets: [
          'WUI areas may ban wood — verify AHJ before re-roof',
          'Salt air: stainless fasteners and flashings recommended',
          'Dry climate extends cedar life vs Gulf Coast',
          'Tile and metal compete on coastal luxury re-roofs',
        ],
      },
    },
    homeExamples: {
      national: { sqft: 2000, cost: 17200 },
      austin: { sqft: 2100, cost: 17100 },
      charlotte: { sqft: 2000, cost: 16800 },
      raleigh: { sqft: 1950, cost: 16600 },
    },
  });
})();

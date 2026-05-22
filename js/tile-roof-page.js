/**
 * Tile roof cost landing page config
 */
(function () {
  'use strict';

  window.initMaterialRoofPage({
    formId: 'tile-calc-form',
    sqftId: 'tile-sqft',
    variantId: 'tile-variant',
    cityId: 'tile-city',
    defaultVariant: 'clay',
    variants: {
      clay: { material: 5.8, labor: 4.4, label: 'Clay tile' },
      concrete: { material: 5.2, labor: 4.0, label: 'Concrete tile' },
      'slate-profile': { material: 6.2, labor: 4.6, label: 'Slate-profile tile' },
    },
    climateNationalLead:
      'Tile dominates hot, coastal, and Mediterranean-style markets. Select a city in the calculator for localized guidance.',
    cityClimate: {
      dallas: {
        rating: 'Fair — hail risk',
        ratingClass: 'fair',
        summary: 'Tile is used in Dallas luxury pockets, but hail can crack brittle profiles — product choice and insurance matter.',
        bullets: [
          'Concrete tile more hail-tolerant than traditional clay in some tests',
          'Heavier load — structural review often required on re-roofs',
          'Less common than asphalt or metal in hail corridors overall',
          'Premium neighborhoods and golf communities still favor tile aesthetics',
        ],
      },
      houston: {
        rating: 'Good — coastal premium',
        ratingClass: 'good',
        summary: 'Houston and Gulf Coast suburbs use concrete and clay tile widely — wind attachment and weight are engineering priorities.',
        bullets: [
          'Wind-rated tile fastening for tropical storm exposure',
          'Humidity: underlayment and batten systems critical',
          'Popular in master-planned and waterfront-adjacent communities',
          'Higher labor specialization than asphalt crews',
        ],
      },
      austin: {
        rating: 'Good',
        ratingClass: 'good',
        summary: 'Austin hill country and luxury builds use tile for Mediterranean and Spanish colonial styles — strong regional installer base.',
        bullets: [
          'Clay and concrete tile match regional architecture',
          'Heat: thermal mass can help or hurt — ventilation design matters',
          'Hail: profile and product rating should be verified',
          'Competes with metal on longevity in upscale segments',
        ],
      },
      phoenix: {
        rating: 'Excellent — desert standard',
        ratingClass: 'good',
        summary: 'Phoenix and Arizona metros are national tile strongholds — heat, sun, and regional style make tile a default premium choice.',
        bullets: [
          'Concrete tile dominates desert subdivisions',
          'Excellent UV stability vs asphalt granules',
          'Foam-set and batten systems common install methods',
          'Metal and tile both outperform asphalt in extreme heat',
        ],
      },
      scottsdale: {
        rating: 'Excellent',
        ratingClass: 'good',
        summary: 'Scottsdale expects tile on many HOA communities — designer profiles and premium underlayment are standard.',
        bullets: [
          'Luxury clay and high-profile concrete tile common',
          'HOA color and profile restrictions apply',
          'Highest regional labor rates for tile specialists',
          'Often combined with desert landscaping and stucco exteriors',
        ],
      },
      tampa: {
        rating: 'Excellent — Florida coast',
        ratingClass: 'good',
        summary: 'Tampa Bay and Florida Gulf Coast are core U.S. tile markets — hurricane codes drive fastening and product approval.',
        bullets: [
          'Florida Product Approval listings mandatory',
          'Wind uplift clips and mortar/set systems per code zone',
          'Concrete tile more common than clay in many tract neighborhoods',
          'Moisture management under tile is non-negotiable in permits',
        ],
      },
      orlando: {
        rating: 'Excellent',
        ratingClass: 'good',
        summary: 'Central Florida tract and custom homes use concrete tile heavily — standard premium over asphalt in many ZIPs.',
        bullets: [
          'Wind-rated installs on every permitted re-roof',
          'Algae less visible on tile than light asphalt',
          'Weight: truss inspection common on older homes',
          'Strong resale expectation for tile in many subdivisions',
        ],
      },
      charlotte: {
        rating: 'Fair',
        ratingClass: 'fair',
        summary: 'Tile appears on Charlotte luxury and golf-community homes but is less dominant than asphalt for mainstream re-roofs.',
        bullets: [
          'Freeze-thaw less severe than Northeast — tile viable',
          'Moderate adoption in upscale lake and country club areas',
          'Higher cost limits share vs architectural shingles',
          'Specialized tile crews fewer than asphalt contractors',
        ],
      },
      raleigh: {
        rating: 'Fair',
        ratingClass: 'fair',
        summary: 'Raleigh tile is niche for high-end custom builds — most volume remains asphalt; tile grows in infill luxury.',
        bullets: [
          'Clay tile on Mediterranean-style custom homes',
          'Humidity: underlayment quality drives long-term performance',
          'Structural load review on homes not originally framed for tile',
          'Less hail risk than Texas but still consider profile rating',
        ],
      },
      'san-diego': {
        rating: 'Excellent — coastal Mediterranean',
        ratingClass: 'good',
        summary: 'San Diego and Southern California coastal communities widely expect tile — codes, salt air, and style align.',
        bullets: [
          'Clay and concrete tile define coastal Mediterranean look',
          'Salt air: corrosion-resistant flashings and vents required',
          'Title 24 and cool-roof conversations apply to color selection',
          'Premium labor — tile specialists booked weeks out in peak season',
        ],
      },
    },
    homeExamples: {
      national: { sqft: 2000, cost: 28600 },
      phoenix: { sqft: 1950, cost: 31200 },
      tampa: { sqft: 1980, cost: 30400 },
      'san-diego': { sqft: 1850, cost: 33800 },
      dallas: { sqft: 2100, cost: 26200 },
    },
  });
})();

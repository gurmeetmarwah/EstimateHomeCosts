#!/usr/bin/env python3
"""Generate slate-roof-cost and wood-shake-roof-cost from tile template."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TILE = (ROOT / "roofing-materials/tile-roof-cost/index.html").read_text()

SLATE_VARIANTS = """            <section class="material-subsection" aria-labelledby="variants-heading">
              <h3 id="variants-heading">Slate roofing types</h3>
              <p class="material-subsection-lead">Natural stone, synthetic slate, and hybrid systems — weight, craft labor, and lifespan vary widely.</p>
              <div class="variant-cards-grid">
                <article class="variant-card variant-card--featured">
                  <div class="variant-card-visual variant-card-visual--natural-slate" aria-hidden="true"></div>
                  <h4>Natural slate</h4>
                  <ul class="variant-card-meta">
                    <li><strong>Cost:</strong> $16–$28 / sq ft</li>
                    <li><strong>Lifespan:</strong> 75–100 years</li>
                    <li><strong>Curb appeal:</strong> Historic luxury</li>
                  </ul>
                  <div class="variant-card-pros-cons">
                    <div class="variant-pros">
                      <h5>Pros</h5>
                      <ul>
                        <li>Longest lifespan of any common roofing material</li>
                        <li>Authentic stone beauty on Colonial and Tudor homes</li>
                        <li>Fire resistant and low maintenance once installed</li>
                        <li>Increases prestige on historic and luxury properties</li>
                      </ul>
                    </div>
                    <div class="variant-cons">
                      <h5>Cons</h5>
                      <ul>
                        <li>Highest upfront cost and specialized labor</li>
                        <li>Very heavy — structural engineering often required</li>
                        <li>Few installers vs asphalt or metal</li>
                        <li>Can chip in severe hail on softer slates</li>
                      </ul>
                    </div>
                  </div>
                </article>
                <article class="variant-card">
                  <div class="variant-card-visual variant-card-visual--synthetic-slate" aria-hidden="true"></div>
                  <h4>Synthetic slate</h4>
                  <ul class="variant-card-meta">
                    <li><strong>Cost:</strong> $12–$18 / sq ft</li>
                    <li><strong>Lifespan:</strong> 40–60 years</li>
                    <li><strong>Curb appeal:</strong> Slate appearance</li>
                  </ul>
                  <div class="variant-card-pros-cons">
                    <div class="variant-pros">
                      <h5>Pros</h5>
                      <ul>
                        <li>Lower weight than natural stone on many trusses</li>
                        <li>Faster install than hand-set quarried slate</li>
                        <li>Consistent color and easier repairs</li>
                        <li>Good option when natural slate cost is prohibitive</li>
                      </ul>
                    </div>
                    <div class="variant-cons">
                      <h5>Cons</h5>
                      <ul>
                        <li>Not true stone — purists and some HOAs notice</li>
                        <li>Shorter lifespan than top natural slate roofs</li>
                        <li>Product quality varies by manufacturer</li>
                        <li>Still premium labor vs asphalt</li>
                      </ul>
                    </div>
                  </div>
                </article>
                <article class="variant-card">
                  <div class="variant-card-visual variant-card-visual--hybrid-slate" aria-hidden="true"></div>
                  <h4>Hybrid / slate-look systems</h4>
                  <ul class="variant-card-meta">
                    <li><strong>Cost:</strong> $14–$22 / sq ft</li>
                    <li><strong>Lifespan:</strong> 50–75 years</li>
                    <li><strong>Curb appeal:</strong> Designer profiles</li>
                  </ul>
                  <div class="variant-card-pros-cons">
                    <div class="variant-pros">
                      <h5>Pros</h5>
                      <ul>
                        <li>Bridges natural slate look and modern underlayment</li>
                        <li>Used on weight-limited historic retrofits</li>
                        <li>Engineered fastening for wind zones</li>
                        <li>Mix of stone and composite courses on some jobs</li>
                      </ul>
                    </div>
                    <div class="variant-cons">
                      <h5>Cons</h5>
                      <ul>
                        <li>Complex detailing — fewer standard crews</li>
                        <li>Warranty depends on full system assembly</li>
                        <li>Mid-high cost without full natural slate lifespan</li>
                        <li>Matching materials on future repairs takes planning</li>
                      </ul>
                    </div>
                  </div>
                </article>
              </div>
            </section>

            <section class="material-subsection" aria-labelledby="colors-heading">
              <h3 id="colors-heading">Popular slate colors</h3>
              <div class="color-swatch-grid">
                <div class="color-swatch"><span class="color-swatch-chip" style="--swatch:#3d4248"></span><span>Charcoal black</span></div>
                <div class="color-swatch"><span class="color-swatch-chip" style="--swatch:#5a6068"></span><span>Gray blend</span></div>
                <div class="color-swatch"><span class="color-swatch-chip" style="--swatch:#6b5d52"></span><span>Earth tone</span></div>
                <div class="color-swatch"><span class="color-swatch-chip" style="--swatch:#7a848c"></span><span>Purple gray</span></div>
                <div class="color-swatch"><span class="color-swatch-chip" style="--swatch:#4a5048"></span><span>Green slate</span></div>
                <div class="color-swatch"><span class="color-swatch-chip" style="--swatch:#8a9088"></span><span>Variegated mix</span></div>
              </div>
            </section>

            <section class="material-subsection" aria-labelledby="climate-heading">
              <h3 id="climate-heading">Best climates for slate roofing</h3>
              <p class="material-subsection-lead" id="climate-section-lead">Natural slate excels in freeze-thaw and historic markets. Select a city in the calculator above for localized guidance.</p>"""

WOOD_VARIANTS = """            <section class="material-subsection" aria-labelledby="variants-heading">
              <h3 id="variants-heading">Wood shake &amp; shingle types</h3>
              <p class="material-subsection-lead">Cedar shake, cedar shingle, and composite alternatives — fire treatment and climate matter as much as material choice.</p>
              <div class="variant-cards-grid">
                <article class="variant-card variant-card--featured">
                  <div class="variant-card-visual variant-card-visual--cedar-shake" aria-hidden="true"></div>
                  <h4>Cedar shake</h4>
                  <ul class="variant-card-meta">
                    <li><strong>Cost:</strong> $8–$14 / sq ft</li>
                    <li><strong>Lifespan:</strong> 20–30 years</li>
                    <li><strong>Curb appeal:</strong> Rustic premium</li>
                  </ul>
                  <div class="variant-card-pros-cons">
                    <div class="variant-pros">
                      <h5>Pros</h5>
                      <ul>
                        <li>Natural texture and depth — unmatched rustic look</li>
                        <li>Popular on ranch, cottage, and lake homes</li>
                        <li>Mid-range cost vs tile or slate</li>
                        <li>Treated products meet many fire-code paths</li>
                      </ul>
                    </div>
                    <div class="variant-cons">
                      <h5>Cons</h5>
                      <ul>
                        <li>Maintenance: moss, staining, and spot replacements</li>
                        <li>Shorter lifespan than metal or tile</li>
                        <li>Fire and HOA restrictions in some areas</li>
                        <li>Humid climates shorten effective service life</li>
                      </ul>
                    </div>
                  </div>
                </article>
                <article class="variant-card">
                  <div class="variant-card-visual variant-card-visual--cedar-shingle" aria-hidden="true"></div>
                  <h4>Cedar shingle</h4>
                  <ul class="variant-card-meta">
                    <li><strong>Cost:</strong> $7–$12 / sq ft</li>
                    <li><strong>Lifespan:</strong> 20–25 years</li>
                    <li><strong>Curb appeal:</strong> Clean wood lines</li>
                  </ul>
                  <div class="variant-card-pros-cons">
                    <div class="variant-pros">
                      <h5>Pros</h5>
                      <ul>
                        <li>Uniform courses — slightly lower cost than thick shake</li>
                        <li>Classic Cape Cod and Craftsman appearance</li>
                        <li>Lighter than heavy hand-split shakes</li>
                        <li>Easier repairs on individual courses</li>
                      </ul>
                    </div>
                    <div class="variant-cons">
                      <h5>Cons</h5>
                      <ul>
                        <li>Less dimensional depth than rustic shake</li>
                        <li>Still needs fire treatment in many jurisdictions</li>
                        <li>UV and moisture exposure require upkeep</li>
                        <li>Fewer installers than asphalt in some metros</li>
                      </ul>
                    </div>
                  </div>
                </article>
                <article class="variant-card">
                  <div class="variant-card-visual variant-card-visual--composite-shake" aria-hidden="true"></div>
                  <h4>Composite / faux shake</h4>
                  <ul class="variant-card-meta">
                    <li><strong>Cost:</strong> $8.50–$13 / sq ft</li>
                    <li><strong>Lifespan:</strong> 30–40 years</li>
                    <li><strong>Curb appeal:</strong> Wood-like profile</li>
                  </ul>
                  <div class="variant-card-pros-cons">
                    <div class="variant-pros">
                      <h5>Pros</h5>
                      <ul>
                        <li>Better fire class than untreated cedar</li>
                        <li>Lower maintenance than natural wood</li>
                        <li>HOA-friendly where raw wood is restricted</li>
                        <li>Consistent color on large roof planes</li>
                      </ul>
                    </div>
                    <div class="variant-cons">
                      <h5>Cons</h5>
                      <ul>
                        <li>Not real wood — close inspection shows polymer</li>
                        <li>Premium price vs architectural asphalt</li>
                        <li>Color fade varies by product line</li>
                        <li>Still needs skilled install for believable lay</li>
                      </ul>
                    </div>
                  </div>
                </article>
              </div>
            </section>

            <section class="material-subsection" aria-labelledby="colors-heading">
              <h3 id="colors-heading">Popular wood roof tones</h3>
              <div class="color-swatch-grid">
                <div class="color-swatch"><span class="color-swatch-chip" style="--swatch:#8b7355"></span><span>Natural cedar</span></div>
                <div class="color-swatch"><span class="color-swatch-chip" style="--swatch:#6b5d4a"></span><span>Cedar brown</span></div>
                <div class="color-swatch"><span class="color-swatch-chip" style="--swatch:#9a9088"></span><span>Weathered gray</span></div>
                <div class="color-swatch"><span class="color-swatch-chip" style="--swatch:#5c5348"></span><span>Charcoal stain</span></div>
                <div class="color-swatch"><span class="color-swatch-chip" style="--swatch:#7a5c42"></span><span>Walnut tone</span></div>
                <div class="color-swatch"><span class="color-swatch-chip" style="--swatch:#c9b89a"></span><span>Light honey</span></div>
              </div>
            </section>

            <section class="material-subsection" aria-labelledby="climate-heading">
              <h3 id="climate-heading">Best climates for wood shake roofing</h3>
              <p class="material-subsection-lead" id="climate-section-lead">Wood shake fits mild, dry climates and rustic architecture. Select a city in the calculator above for localized guidance.</p>"""


def replace_block(text, start_marker, end_marker, new_block):
    i = text.index(start_marker)
    j = text.index(end_marker, i)
    return text[:i] + new_block + text[j:]


def slate_page():
    t = TILE
    reps = [
        ("tile-roof-cost", "slate-roof-cost"),
        ("Tile Roof Cost", "Slate Roof Cost"),
        ("Tile Roof", "Slate Roof"),
        ("Tile roofing", "Slate roofing"),
        ("Tile Roofing", "Slate Roofing"),
        ("material-page--tile", "material-page--slate"),
        ("tile-calc-form", "slate-calc-form"),
        ("tile-sqft", "slate-sqft"),
        ("tile_sqft", "slate_sqft"),
        ("tile-variant", "slate-variant"),
        ("tile_variant", "slate_variant"),
        ("tile-city", "slate-city"),
        ("tile_city", "slate_city"),
        ("Tile Roof Cost Calculator", "Slate Roof Cost Calculator"),
        ("tile type", "slate type"),
        ("Clay tile", "Natural slate"),
        ('value="clay" selected', 'value="natural" selected'),
        ("Concrete tile", "Synthetic slate"),
        ('value="concrete"', 'value="synthetic"'),
        ("Slate-profile tile", "Hybrid slate system"),
        ('value="slate-profile"', 'value="hybrid"'),
        ("$11–$19", "$16–$28"),
        ("50+ yrs", "75–100 yrs"),
        ("Premium homes", "Historic luxury"),
        ("Clay and concrete tile for coastal", "Natural stone slate for historic and luxury homes"),
        ("Coastal premium", "Century lifespan"),
        ("Classic curb appeal", "Unmatched prestige"),
        ("Long lifespan", "Fire resistant"),
        ("Regional standard", "Specialist craft"),
        ("Tile roofing — Complete Guide", "Slate Roofing — Complete Guide"),
        ("Compare tile vs asphalt", "Compare slate vs asphalt"),
        ('roof-style-card--tile roof-style-card--current', 'roof-style-card--slate roof-style-card--current'),
        ("50+ year lifespan · Clay &amp; concrete", "75–100 year lifespan · Natural stone"),
        ("$11 – $19 / sq ft", "$16 – $28 / sq ft"),
        ("Compare tile to asphalt", "Compare slate to asphalt, wood"),
        ("Regional Tile Roof", "Regional Slate Roof"),
        ("$11.00–$19.00", "$16.00–$28.00"),
        ("$4.00–$6.50", "$5.00–$7.50"),
        ("Coastal, desert, Mediterranean", "Historic, freeze-thaw, luxury custom"),
        ("Real Tile Roof Projects", "Real Slate Roof Projects"),
        ("concrete tile with tear-off", "natural slate with tear-off"),
        ('data-project-city="phoenix"', 'data-project-city="charlotte"'),
        ("Phoenix, AZ", "Charlotte, NC"),
        ("Concrete tile", "Natural slate"),
        ("$31,200", "$29,300"),
        ('data-project-city="tampa"', 'data-project-city="raleigh"'),
        ("Tampa, FL", "Raleigh, NC"),
        ("$30,400", "$29,800"),
        ("Clay tile", "Natural slate"),
        ("$33,800", "$34,200"),
        ("Tile Roof FAQ", "Slate Roof FAQ"),
        ("How long does a tile roof last?", "How long does a slate roof last?"),
        ("Clay tile often lasts 50–100 years", "Natural slate often lasts 75–100 years"),
        ("Clay vs concrete tile", "Natural vs synthetic slate"),
        ("Can my home support a tile roof?", "Can my home support a slate roof?"),
        ("Is tile worth it vs asphalt?", "Is slate worth the cost?"),
        ("Estimate your tile roof cost", "Estimate your slate roof cost"),
        ("Open tile calculator", "Open slate calculator"),
        ("/roofing-materials/tile-roof-cost/", "/roofing-materials/slate-roof-cost/"),
        ("Tile Roof Cost", "Slate Roof Cost"),
        ("tile-roof-page.js", "slate-roof-page.js"),
        ("Clay &amp; Concrete Prices", "Natural Stone Prices"),
        ("clay, concrete &amp; slate-profile tile", "natural, synthetic &amp; hybrid slate"),
        ("tile roof cost", "slate roof cost"),
        ("Clay and concrete tile from", "Natural slate from"),
        ("Guide to clay, concrete, and slate-profile", "Guide to natural, synthetic, and hybrid slate"),
        ("In markets where tile is the neighborhood", "On homes where slate authenticity matters"),
        ("tile is heavy", "slate is very heavy"),
        ("pattern id=\"tile-clay\"", "pattern id=\"slate-stone\""),
        ("#a85c42", "#4a5048"),
        ("#8b4a35", "#3d4248"),
        ("#6b3d2a", "#2d3238"),
        ("Mediterranean home with clay tile roof", "Historic home with natural slate roof"),
    ]
    for a, b in reps:
        t = t.replace(a, b)
    t = replace_block(
        t,
        '            <section class="material-subsection" aria-labelledby="variants-heading">',
        '              <div class="climate-grid climate-grid--city-only"',
        SLATE_VARIANTS,
    )
    return t


def wood_page():
    t = TILE
    reps = [
        ("tile-roof-cost", "wood-shake-roof-cost"),
        ("Tile Roof Cost", "Wood Shake Roof Cost"),
        ("Tile Roof", "Wood Shake Roof"),
        ("Tile roofing", "Wood shake"),
        ("Tile Roofing", "Wood Shake"),
        ("material-page--tile", "material-page--wood"),
        ("tile-calc-form", "wood-calc-form"),
        ("tile-sqft", "wood-sqft"),
        ("tile_sqft", "wood_sqft"),
        ("tile-variant", "wood-variant"),
        ("tile_variant", "wood_variant"),
        ("tile-city", "wood-city"),
        ("tile_city", "wood_city"),
        ("Tile Roof Cost Calculator", "Wood Shake Roof Cost Calculator"),
        ("tile type", "wood type"),
        ("Clay tile", "Cedar shake"),
        ('value="clay" selected', 'value="cedar-shake" selected'),
        ("Concrete tile", "Cedar shingle"),
        ('value="concrete"', 'value="cedar-shingle"'),
        ("Slate-profile tile", "Composite shake"),
        ('value="slate-profile"', 'value="composite-shake"'),
        ("$11–$19", "$8–$14"),
        ("50+ yrs", "20–30 yrs"),
        ("Premium homes", "Rustic &amp; cottage"),
        ("Clay and concrete tile for coastal", "Cedar shake and composite alternatives for rustic curb appeal"),
        ("Coastal premium", "Natural texture"),
        ("Classic curb appeal", "Hand-split character"),
        ("Long lifespan", "Mid-range cost"),
        ("Regional standard", "Fire-treated options"),
        ("Tile roofing — Complete Guide", "Wood Shake — Complete Guide"),
        ("Compare tile vs asphalt", "Compare wood vs asphalt"),
        ('roof-style-card--tile roof-style-card--current', 'roof-style-card--wood roof-style-card--current'),
        ("50+ year lifespan · Clay &amp; concrete", "20–30 year lifespan · Cedar shake"),
        ("$11 – $19 / sq ft", "$8 – $14 / sq ft"),
        ("Compare tile to asphalt", "Compare wood shake to asphalt and metal"),
        ("Regional Tile Roof", "Regional Wood Shake Roof"),
        ("$11.00–$19.00", "$8.00–$14.00"),
        ("$4.00–$6.50", "$3.00–$5.00"),
        ("Coastal, desert, Mediterranean", "Dry, mild, rustic &amp; cottage styles"),
        ("Real Tile Roof Projects", "Real Wood Shake Projects"),
        ("concrete tile with tear-off", "cedar shake with tear-off"),
        ('data-project-city="phoenix"', 'data-project-city="austin"'),
        ("Phoenix, AZ", "Austin, TX"),
        ("$31,200", "$17,100"),
        ('data-project-city="tampa"', 'data-project-city="charlotte"'),
        ("Tampa, FL", "Charlotte, NC"),
        ("$30,400", "$16,800"),
        ("Clay tile", "Cedar shake"),
        ("San Diego, CA", "Raleigh, NC"),
        ('data-project-city="san-diego"', 'data-project-city="raleigh"'),
        ("$33,800", "$16,600"),
        ("Tile Roof FAQ", "Wood Shake FAQ"),
        ("How long does a tile roof last?", "How long does a wood shake roof last?"),
        ("Clay tile often lasts 50–100 years", "Cedar shake typically lasts 20–30 years with maintenance"),
        ("Clay vs concrete tile", "Cedar shake vs composite shake"),
        ("Can my home support a tile roof?", "Is wood shake allowed in my area?"),
        ("Is tile worth it vs asphalt?", "Is wood shake worth it?"),
        ("Estimate your tile roof cost", "Estimate your wood shake cost"),
        ("Open tile calculator", "Open wood calculator"),
        ("/roofing-materials/tile-roof-cost/", "/roofing-materials/wood-shake-roof-cost/"),
        ("Tile Roof Cost", "Wood Shake Cost"),
        ("tile-roof-page.js", "wood-shake-roof-page.js"),
        ("Clay &amp; Concrete Prices", "Cedar &amp; Composite Prices"),
        ("clay, concrete &amp; slate-profile tile", "cedar shake, shingle &amp; composite"),
        ("tile roof cost", "wood shake roof cost"),
        ("Clay and concrete tile from", "Cedar shake from"),
        ("Guide to clay, concrete, and slate-profile", "Guide to cedar shake, shingle, and composite"),
        ("pattern id=\"tile-clay\"", "pattern id=\"wood-shake\""),
        ("#a85c42", "#8b7355"),
        ("#8b4a35", "#6b5d4a"),
        ("#6b3d2a", "#5c5348"),
        ("Mediterranean home with clay tile roof", "Cottage home with cedar shake roof"),
        ("<h3>Tile roofing</h3>", "<h3>Wood shake</h3>"),
    ]
    for a, b in reps:
        t = t.replace(a, b)
    t = replace_block(
        t,
        '            <section class="material-subsection" aria-labelledby="variants-heading">',
        '              <div class="climate-grid climate-grid--city-only"',
        WOOD_VARIANTS,
    )
    # FAQ schema in head - fix remaining tile refs in JSON-LD
    t = t.replace("tile roof", "wood shake roof").replace("Tile dominates", "Wood fits")
    return t


if __name__ == "__main__":
    (ROOT / "roofing-materials/slate-roof-cost/index.html").write_text(slate_page())
    (ROOT / "roofing-materials/wood-shake-roof-cost/index.html").write_text(wood_page())
    print("Wrote roofing-materials/slate-roof-cost/index.html and roofing-materials/wood-shake-roof-cost/index.html")

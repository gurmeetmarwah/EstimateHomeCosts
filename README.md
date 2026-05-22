# Estimate Home Costs

Static marketing site for **Estimate Home Costs** — real home project costs and local estimates across the U.S.

**Production URL:** https://estimatehomecosts.com

## Run locally

```bash
cd estimate-home-costs
npx serve .
# or: python3 -m http.server 8080
```

Open `http://localhost:3000` (serve) or `http://localhost:8080`.

## Structure

- `index.html` — semantic homepage with JSON-LD (WebSite, Organization, FAQ)
- `css/styles.css` — design system (forest + copper palette)
- `js/main.js` — search autocomplete, mobile nav, lead form
- `js/city-path.js` — state/city geo scope for calculators and guides
- `scripts/brand.py` — site name and domain constants
- `robots.txt` / `sitemap.xml` — SEO crawl hints

## Regenerate geo pages

```bash
python3 scripts/generate-state-hub-page.py
python3 scripts/generate-city-hub-page.py
python3 scripts/generate-state-scoped-pages.py
python3 scripts/generate-city-scoped-pages.py
```

## Deploy

Upload the folder to any static host (Netlify, Vercel, Cloudflare Pages, S3 + CloudFront). No build step required. Point your domain to `estimatehomecosts.com` (or your host’s URL).

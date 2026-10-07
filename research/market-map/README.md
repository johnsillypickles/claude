# League Market Map

Dashboard: `league-market-map.html` (published as a private Claude artifact).

Two views:
1. **Current metros: CAC.** Meta spend and purchases from ad sets named for a city, grouped to metro, by quarter. A quarter counts if local spend >= $1,500. Index = metro CAC / that quarter's median local CAC. Consistently efficient = 2+ tested quarters, average index <= 0.85, no quarter above 1.05.
2. **Where to expand.** US metros with no league within 30 mi, scored on population within 30 mi, median household income, and owned demand signals (Klaviyo location requests x3, host applicants x2, notify-me x1, counted within 35 mi and only when the signal itself is outside current metros).

## Refresh

Inputs (saved next to the scripts, not committed):
- `ads_q1.json`, `ads_q2.json`, `ads_q3.json`: Lebesgue `get_advertising_data_table`, source facebook, account 1346441932978787, level adset, period all, pixel_customer_type first, one call per quarter.
- `prod_q1.json` ... `prod_q3.json`: Lebesgue `get_revenue_breakdown`, dimension product, one call per quarter.
- `form_requests.json`: Klaviyo "Submitted Form" events for forms SLpc7B, VsLjck, USDt3F, YtLp6S, reduced to form, date, page, ZIP and city (no names, emails or phones).
- `zip.sqlite`: uszipcode simple_db (github.com/MacHu-GWU/uszipcode-project releases, 1.0.1.db).
- `states-albers-10m.json`: npm us-atlas@3.0.1.

Run: `python3 analyze.py && python3 expand.py && python3 build_data.py`, then substitute `__DATA__` and `__TOPO__` in `template.html`.

New league cities need an entry in `metros.py` (`M`).

## Known gaps

- About 58% of Q1 to Q3 Meta spend is national, regional or creative-test and isn't split by metro. A Meta DMA breakdown export fixes this.
- Population and income are 2010-era. Current ACS needs `api.census.gov` allowed in the environment's network settings.
- Google Trends needs `trends.google.com` allowed.

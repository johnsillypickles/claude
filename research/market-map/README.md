# League Market Map

Dashboard: `league-market-map.html` (published as a private Claude artifact).

Views (v4):
- **Where to add leagues.** Existing US markets with 4+ leagues in 2026, scored on sell-outs (`sellout.py`: inventory hit 0 through sales, not a manual zero-out), new players per league Q1 to Q3, leagues per 100k residents aged 25 to 44 (Census), Google Trends, and estimated Meta CAC.
- **New markets.** Census 2024 metros (200k+) with no league within 30 mi, scored on population, fit (age 25 to 44, degree, income, growth), Trends and request forms.
0. **Meta CAC by market.** All Meta spend by Comscore market (Ads Manager export, Breakdown → Delivery → Comscore Markets, campaign level) ÷ Shopify first-time signups for that market's leagues. Shows cost per new signup (floor) and estimated Meta CAC (signups × market Meta UTM share × account-wide Meta-reported/UTM ratio). `dma.py` holds the market → metro map.
1. **Current metros: CAC.** Meta spend and purchases from ad sets named for a city, grouped to metro, by quarter. A quarter counts if local spend >= $1,500. Index = metro CAC / that quarter's median local CAC. Consistently efficient = 2+ tested quarters, average index <= 0.85, no quarter above 1.05.
2. **Where to expand.** US metros with no league within 30 mi, scored on population within 30 mi, median household income, and owned demand signals (Klaviyo location requests x3, host applicants x2, notify-me x1, counted within 35 mi and only when the signal itself is outside current metros).

## Refresh

Inputs (saved next to the scripts, not committed):
- `ads_q1.json`, `ads_q2.json`, `ads_q3.json`: Lebesgue `get_advertising_data_table`, source facebook, account 1346441932978787, level adset, period all, pixel_customer_type first, one call per quarter.
- `prod_q1.json` ... `prod_q3.json`: Lebesgue `get_revenue_breakdown`, dimension product, one call per quarter.
- `form_requests.json`: Klaviyo "Submitted Form" events for forms SLpc7B, VsLjck, USDt3F, YtLp6S, reduced to form, date, page, ZIP and city (no names, emails or phones).
- `meta_dma.csv`: the Ads Manager Comscore market export (not committed).
- `prod_jul_oct5.json`: Lebesgue product breakdown Jul 1 to Oct 5, to match the export's date range.
- `zip.sqlite`: uszipcode simple_db (github.com/MacHu-GWU/uszipcode-project releases, 1.0.1.db).
- `states-albers-10m.json`: npm us-atlas@3.0.1.

- `utm_q1.json` ... `utm_q3.json`: ShopifyQL `FROM sales SHOW orders GROUP BY product_title, order_utm_source`, one per quarter.

Waitlist: Klaviyo metric "Customer signed up for alert (STOQ)" (UHM4zh), pulled with `get_events` 1,000 per page; `wl_take.sh` keeps only league title, date and event id (no emails) in `waitlist.tsv` (not committed), aggregated to `waitlist_agg.json`.

Inventory inputs: `inv_q4_25.json`, `inv_q1.json`, `inv_q2.json`, `inv_q3.json` from ShopifyQL `FROM inventory SHOW starting_inventory_units, ending_inventory_units, inventory_units_sold GROUP BY product_title TIMESERIES day`, one per quarter. Census and Trends come from `external/`.

Run (v4): `python3 build_v4.py` after the steps below, then substitute `__DATA__` with `data_v4.json`.

Run: `python3 analyze.py && python3 utm.py && python3 dma.py && python3 expand.py && python3 build_data.py`, then substitute `__DATA__` and `__TOPO__` in `template.html`.

New league cities need an entry in `metros.py` (`M`).

## Known gaps

- The Comscore market export has spend and clicks but no purchases, and no monthly split yet.
- Population and income are 2010-era. Current ACS needs `api.census.gov` allowed in the environment's network settings.
- Google Trends needs `trends.google.com` allowed.

## League Demand Atlas (for facility partners)

`league-demand-atlas.html`, built by `build_facility.py` from `data_v4.json` into `facility.json`, then `facility_template.html` with `__DATA__` and `__TOPO__` substituted. Demand index = mean percentile of sell-out rate, waitlist per league, registrations per league and new players per 100k aged 25 to 44, across metros with 3+ leagues.

# Handoff: League Market Map and League Demand Atlas

Session: https://claude.ai/code/session_01U6uEogWzTMrTitkJ3G7ygn
Branch: `claude/exciting-goldberg-croh9s` (repo `johnsillypickles/claude`)
Last updated: 2026-10-08

## Goal

Build demand "heat maps" for Silly Pickles (adult social pickleball leagues, 70 US metros plus Canada and Australia):

1. **Internal:** where to add leagues in existing markets, which new markets to enter, and where Meta acquisition is efficient.
2. **External:** a page Tommy can use with facility clients showing where leagues fill and where a market could support more league nights or a new facility.

## Outputs

| Output | Link | Audience |
|---|---|---|
| League Market Map (internal, v6) | https://claude.ai/artifact/JUbi7isVxbhVFCw3WXaSq9 | John and team |
| League Demand Atlas (facility clients) | https://claude.ai/artifact/8c53FYjzeAo6DH1ADQV8YK | Tommy, facility partners |

Both are private until shared from the page's Share menu.

**League Market Map tabs:** Where to add leagues, New markets, Meta CAC by market, City ad sets by quarter. A Top 15 new-market table sits under the map. The map can color metros by add-leagues score, sell-out rate or market CAC.

**League Demand Atlas:** network totals, a map of metros labeled Under-supplied / Healthy / Softer / Crowded / Early, a clickable metro profile (league performance, Meta spend and cost per new player, Census, search interest), and new-market candidates.

## Decisions made

- **Unit of analysis:** metro. League products are mapped to metros by the city in the product title (`metros.py`). Comscore (Meta) markets are mapped to metros in `dma.py`.
- **Meta CAC by market:** Meta's Comscore market export has spend and clicks but no purchases, so:
  - **Cost per new signup** (floor) = Meta spend in the market ÷ Shopify first-time signups for that market's leagues.
  - **Estimated Meta CAC** = spend ÷ (signups × the market's Meta-tagged UTM share × 2.7). 2.7 = Meta-reported purchases ÷ Meta-tagged orders account-wide (18,313 ÷ 6,775, Q1 to Q3). This assumes UTM capture is similar in every market.
- **Sell-out definition:** inventory hit 0 through sales on a day with no manual removal (ShopifyQL daily inventory). Manual zero-outs (the 3-day pre-start close) and cancellations don't count. Measured per league, not per night.
- **Waitlist:** Stoq "Customer signed up for alert (STOQ)" events in Klaviyo (17,731 since Nov 2025). Only signups after the league sold out count as unmet demand (66% of all signups). Raw events contain emails and were never committed; only per-league and per-metro counts are kept.
- **Add-leagues score (default weights):** sell-outs 35%, waitlist 25%, room to grow 20% (league density per 100k aged 25 to 44, plus search interest), new-player momentum 10%, estimated Meta CAC 10%. Metros with 4+ leagues, or 2+ leagues and 200+ waitlist signups.
- **New-market score (default weights):** population 30%, fit 35% (share aged 25 to 44, bachelor's+, income, 5-yr growth), Google search interest 15%, own demand signals 20% (location requests ×3, host applicants ×2, notify-me ×1). Census 2024 metros of 200k+ with no league within 30 mi.
- **Search interest is down-weighted** because pickleball searches peak in Florida retirement markets (Cape Coral, Naples, North Port score 97+).
- **Facility page includes spend, CAC and signup counts** (John's call: Tommy won't share with competitors).
- **Demand index (facility page)** = average percentile of sell-out rate, waitlist per league, registrations per league and new players per 100k aged 25 to 44, across metros with 3+ leagues.

## Key findings so far

- **Add leagues:** Seattle (168 waitlist signups per league, 3 leagues), San Diego, Tampa, SF (small samples), Austin, Phoenix, Denver (5 of 5 Fall leagues sold out, 706 waitlisted), LA.
- **Hold:** Louisville and Oklahoma City (0% sold out), Indianapolis (13%), Boston (22%), Atlanta (33%, and Meta drives few of its signups, so it's a holdout-test candidate).
- **Portland, OR:** The People's Courts fills with a waitlist; the suburban leagues don't. Add in the core, not the suburbs.
- **Cheapest Meta markets at $15k+ spend:** San Diego $71, Nashville $75, DC $80, SF $85 estimated CAC (median market $102).
- **Most expensive:** Louisville $305, Albuquerque $217, Indianapolis $214, Jacksonville $182.
- **Meta spends almost nothing outside league markets** ($673 total), so ad CTR can't help with expansion.
- **New markets (top of default ranking):** Omaha, Birmingham, Provo, Virginia Beach, Richmond, San Jose, Tulsa. Fort Wayne and Little Rock are already launching. Wilmington, NC is #22 after correcting its growth.

## Current state (where we left off)

Adding **"where young people are moving"** as a new input, at John's request.

Done:
- Pulled ACS table B07001 (geographic mobility by age) for every metro, 2015 to 2019 and 2020 to 2024. Saved in `external/migration_cbsa.json` (variable IDs in `external/b07001_vars.json`).
- **Transplant rate** = people aged 25 to 44 who moved in from another state or abroad in the past year ÷ everyone aged 25 to 44. Moves between counties in the same state are left out because they include moves within a metro.
- Confirmed the Census API can return a metro's counties: `for=county:*&in=state:XX&in=metropolitan statistical area/micropolitan statistical area (or part):CODE`. Tested on Wilmington, NC (48900), which returned New Hanover, Pender and Brunswick.

Problems found, not yet fixed:
1. **Military bases dominate the transplant ranking** (Clarksville, Colorado Springs, Fayetteville NC, Killeen, Columbus GA, Fort Walton Beach). Plan: flag metros with a high armed-forces share (ACS B23025_006E ÷ B23025_001E).
2. **Boundary redraws inflate growth** for about 10 metros (Wilmington NC shows +57% total and +43.7% for ages 25 to 44; real total growth is +7.9%; Bend and Fresno are also off). Plan: rebuild each metro's growth from its counties using the API query above.

## Open items

1. Build the metro-to-county crosswalk (loop states, then metro parts) and recompute 5-yr growth and 25 to 44 growth from counties. Apply to both dashboards.
2. Pull armed-forces share and flag or down-weight military metros.
3. Cross-check top transplant metros against news and research (web search), and link sources where they agree. Census stays the score input.
4. Add a "Transplants" component (transplant rate, change vs pre-COVID, 25 to 44 growth) to the new-market score and the add-leagues "room to grow" part, then republish both artifacts.
5. Sell-outs by night (variant level) are not built yet; a multi-night league counts as sold out only when all nights are full.
6. Meta export by month (Breakdown → By Time → Month) would let market CAC be checked quarter to quarter.
7. Suggested test: Meta holdout in Atlanta for 3 to 4 weeks. Cheap lead-form tests (about $500, like Fort Wayne) for candidates such as Wilmington, NC.

## Key files (`research/market-map/`)

| File | What it does |
|---|---|
| `metros.py` | Product or ad set name → metro |
| `analyze.py` | City ad set spend and signups by metro and quarter |
| `utm.py` | Meta-tagged share of league orders by metro (ShopifyQL UTM) |
| `dma.py` | Meta spend by Comscore market → metro, cost per signup and estimated CAC |
| `sellout.py` | Sell-out detection from daily inventory |
| `geo.py` | ZIP-based geocoding and distance helpers |
| `build_v4.py` | Joins sell-outs, waitlist, Census and Trends; component scores → `data_v4.json` |
| `template.html` → `league-market-map.html` | Internal dashboard (substitute `__DATA__`, `__TOPO__`) |
| `build_facility.py`, `facility_template.html` → `league-demand-atlas.html` | Facility page (`facility.json`) |
| `waitlist_agg.json`, `wl_take.sh` | Waitlist counts and the PII-stripping extractor |
| `external/` | Census (`census_cbsa.csv`, `census_county.csv`), Trends (`trends_dma.csv`), migration (`migration_cbsa.json`), pull scripts and their README |
| `README.md` | Refresh steps and input queries |

Raw inputs not committed: Lebesgue and ShopifyQL pulls (`ads_q*.json`, `prod_q*.json`, `inv_*.json`, `utm_q*.json`), the Meta Comscore CSV, Klaviyo form and waitlist events (contain emails), and the ZIP database. Re-pull steps are in `README.md`.

## Environment notes

- Network allowlist (Silly Pickles environment, Custom): `trends.google.com`, `api.census.gov`, plus default package managers.
- `CENSUS_API_KEY` is set as an environment variable and is visible to this session.
- Google Trends city-level pulls return all zeros; DMA level works. The first request sometimes hits a captcha and succeeds on retry.
- Windsor (Meta breakdowns) was disconnected earlier; the Meta data came from a manual Ads Manager export.

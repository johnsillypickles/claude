# Handoff: League Market Map and League Demand Atlas

Repo `johnsillypickles/claude`, branch `claude/exciting-goldberg-croh9s`, folder `research/market-map/`.
Original session: https://claude.ai/code/session_01U6uEogWzTMrTitkJ3G7ygn
Last updated: 2026-10-08

## Goal

Demand "heat maps" for Silly Pickles (adult social pickleball leagues: 70 US metros, plus Canada and Australia):

1. **Internal (John):** where to add leagues in existing markets, which new markets to enter, and where Meta acquisition is efficient.
2. **External (Tommy):** a page Tommy uses with facility clients to show where leagues fill and where a market could support more league nights or a new facility.

## Outputs

| Output | Link | Audience | Version |
|---|---|---|---|
| League Market Map | https://claude.ai/artifact/JUbi7isVxbhVFCw3WXaSq9 | John, internal | v7 |
| League Demand Atlas | https://claude.ai/artifact/8c53FYjzeAo6DH1ADQV8YK | Tommy and facility clients | v2 |

Both are private until shared from the page's **Share** menu. Both are owned by John's account, so only John (or someone he gives edit access) can republish them to the same links.

**League Market Map:** four summary cards, a map (color by add-leagues score, sell-out rate or market CAC), a Top 15 new-market table, then tabs: Where to add leagues, New markets (all 152, adjustable weights), Meta CAC by market, City ad sets by quarter.

**League Demand Atlas:** network totals, a map labeling metros Under-supplied / Healthy / Softer / Crowded / Early, a clickable metro profile (league performance, Meta spend and cost per new player, Census, transplants, search interest, news links), new-market candidates, and a "how to read it" section with sources. It includes spend and CAC; John approved that.

## Current rankings (default weights)

- **Add leagues:** Seattle, Tampa, Austin, San Diego, Phoenix, San Francisco, Denver, Nashville. Seattle has 168 waitlist signups per league over 3 leagues. Denver sold out 5 of 5 Fall leagues and has 706 waitlisted. San Diego, Tampa and SF have small samples (4 to 5 leagues).
- **Hold:** Louisville and Oklahoma City (0% sold out), Indianapolis (13%), Boston (22%), Atlanta (33%; Meta drives few of its signups, so it's a holdout-test candidate).
- **Portland, OR:** The People's Courts fills with a waitlist; the suburban leagues don't. Add in the core.
- **New markets:** Cape Coral FL, Omaha, Worcester, Tulsa, Fayetteville AR, Manchester NH, Ogden, Reno, Chattanooga, Columbia SC. Fort Wayne and Little Rock are already launching. Wilmington, NC is mid-pack.
  - Cape Coral and other Gulf Coast Florida metros rank high on young transplants and population, but only middling on demographic fit. Worth a second look before acting.
- **Highest civilian transplant rates, current metros:** Charlottesville 7.6%, DC 7.2%, Bridgeport-Stamford 6.8%, Charleston 6.8%, Las Vegas 6.3%, Denver 6.1%, Seattle 5.9%, Boise 5.9%.
- **Highest civilian transplant rates, candidates (300k+):** Savannah 7.5%, Ann Arbor 6.9%, Manchester 6.9%, Fort Collins 6.5%, Chattanooga 5.9%.
- **Meta CAC:** cheapest at $15k+ spend are San Diego $71, Nashville $75, DC $80, SF $85 (median market $102). Most expensive: Louisville $305, Albuquerque $217, Indianapolis $214, Jacksonville $182. Meta spends almost nothing outside league markets ($673 total).

## How every number is built

- **Metro mapping:** league products and ad sets map to metros by the city in their name (`metros.py`). Meta Comscore markets map to metros in `dma.py`. Census metros map to league metros by nearest metro within 30 mi (`build_v4.py`).
- **Sell-out:** a league's Shopify inventory hit 0 through sales on a day with no manual removal (ShopifyQL daily inventory, `sellout.py`). Manual zero-outs (the 3-day pre-start close) and cancellations don't count. Per league, not per night. Seasons Winter to Fall 2026, leagues with 10+ spots sold.
- **Waitlist:** Stoq "Customer signed up for alert (STOQ)" events in Klaviyo (17,731 since Nov 2025). Only signups after the league sold out count (66%). Raw events contain emails and were never committed; `waitlist_agg.json` has counts only.
- **Cost per new signup** = Meta spend in the Comscore market ÷ Shopify first-time signups for that market's leagues (Jan 1 to Oct 7). **Estimated Meta CAC** = spend ÷ (signups × the market's Meta-tagged UTM share × 2.7). 2.7 = Meta-reported purchases ÷ Meta-tagged orders account-wide (18,313 ÷ 6,775). Assumes UTM capture is similar everywhere.
- **Transplants** = Census ACS B07001: residents aged 25 to 44 who lived in another state or abroad a year earlier, as a share of all residents 25 to 44 (2020 to 2024), plus the change vs 2015 to 2019 and 25 to 44 population growth. Moves between counties in the same state are excluded because they include moves within a metro.
- **Military flag:** 3%+ of adults in the armed forces (ACS B23025). 23 metros are flagged (e.g. Fayetteville NC, Killeen, Clarksville, Colorado Springs, Virginia Beach). Their transplant rate is scored neutral because base rotations aren't social transplants.
- **Growth** is rebuilt from the same counties in both periods (`crosswalk.py`, `county_growth.py`), which fixes metros redrawn in 2023 (Wilmington NC was showing +57%; real is +7.9%). The 5 Connecticut metros have no growth figure because Connecticut replaced its counties in 2022.
- **News cross-check** (`news.json`): Redfin (Sep 2026), U-Haul 2026 midyear, This Old House (ACS 2013 to 2023), Brookings, SmartAsset 2025, UVA Cooper Center. Shown as links on metros they name. Census is the score input because news covers few small metros.
- **Add-leagues score:** sell-outs 35%, waitlist 25%, room to grow 20% (league density per 100k aged 25 to 44, search interest, transplants), new-player momentum 10%, estimated Meta CAC 10%. Metros with 4+ leagues, or 2+ leagues and 200+ waitlist signups. Each part is a 0 to 100 percentile.
- **New-market score:** population 25%, transplants 20%, fit 25% (share aged 25 to 44, bachelor's+, income, growth), search interest 10%, own demand signals 20% (location requests ×3, host applicants ×2, notify-me ×1). Census 2024 metros of 200k+ with no league within 30 mi.
- **Search interest** = average percentile of Google Trends for "pickleball", "pickleball near me", "pickleball league" across 210 DMAs, last 12 months. Low weight because retirement markets search pickleball heavily.
- **Demand index (Atlas)** = average percentile of sell-out rate, waitlist per league, registrations per league and new players per 100k aged 25 to 44, across metros with 3+ leagues. Under-supplied: 60%+ sold out and index 60+. Crowded: 8+ leagues and under 30% sold out. Early: fewer than 3 leagues.

## Open items

1. **Sell-outs by night:** a multi-night league counts as sold out only when every night is full. Variant-level inventory would fix this.
2. **Meta market CAC by month:** re-export Ads Manager with Breakdown → By Delivery → Comscore Markets plus By Time → Month to check whether market CAC holds quarter to quarter.
3. **Tests to run:** a 3 to 4 week Meta holdout in Atlanta; ~$500 lead-form tests (like Fort Wayne) for top new-market candidates.
4. **Refresh cadence:** data runs through Oct 7, 2026. Re-pull after each season.
5. **Gulf Coast Florida:** decide whether to cap the transplant weight for retiree-heavy metros, or keep it and judge case by case.

## Files (`research/market-map/`)

| File | Purpose |
|---|---|
| `HANDOFF.md` | This file |
| `README.md` | Refresh steps and the exact queries for every input |
| `league-market-map.html`, `league-demand-atlas.html` | The published pages (self-contained HTML) |
| `template.html`, `facility_template.html` | Page templates; `__DATA__` and `__TOPO__` get substituted |
| `data_v4.json`, `facility.json` | The data behind each page |
| `build_v4.py`, `build_facility.py` | Build the two data files |
| `metros.py`, `dma.py`, `utm.py`, `analyze.py`, `sellout.py`, `geo.py` | Metro mapping, Meta market CAC, UTM shares, city ad sets, sell-outs, geocoding |
| `crosswalk.py`, `county_growth.py` | Census metro-to-county crosswalk and county-based growth, military share |
| `news.json` | News sources and the metros they name |
| `waitlist_agg.json`, `wl_take.sh` | Waitlist counts and the email-stripping extractor |
| `external/` | Census (`census_cbsa.csv`, `census_county.csv`, `migration_cbsa.json`, `cbsa_counties.json`, `cbsa_county_rollup.json`), Trends (`trends_dma.csv`), pull scripts |

**To re-render a page from committed data** (no API calls): install `us-atlas@3.0.1` from npm, then substitute `__DATA__` with `data_v4.json` (or `facility.json`) and `__TOPO__` with `us-atlas/states-albers-10m.json` in the template.

**To fully refresh:** re-pull the raw inputs listed in `README.md` (Lebesgue, ShopifyQL, Klaviyo, the Meta export, Census, Trends) into one working folder with the scripts, then run `analyze.py`, `utm.py`, `dma.py`, `expand.py`, `build_v4.py`, `build_facility.py`. Raw pulls are not committed (size, and Klaviyo events contain emails).

## Environment and access

- **Cloud environment "Silly Pickles"** (Personal): network access Custom, allowed domains `trends.google.com` and `api.census.gov`, plus default package managers. Environment variable `CENSUS_API_KEY`.
- **Connectors used:** Lebesgue (Meta ad sets, product revenue), Shopify (ShopifyQL inventory and UTMs), Klaviyo (forms, Stoq waitlist events). Windsor was disconnected; the Meta Comscore export was a manual Ads Manager download.
- **Shopify store:** `334378-2a.myshopify.com`. Lebesgue shop id `1307999470`, Meta account `1346441932978787`.
- Google Trends city-level pulls return zeros; DMA level works. The first request sometimes hits a captcha and works on retry.

## Starting a new session or project from this

Paste this as the first message (or as Claude Code project instructions):

> We're continuing the Silly Pickles League Market Map work. Read `research/market-map/HANDOFF.md` on branch `claude/exciting-goldberg-croh9s` in `johnsillypickles/claude` first. Work on that branch. The published pages are https://claude.ai/artifact/JUbi7isVxbhVFCw3WXaSq9 (internal) and https://claude.ai/artifact/8c53FYjzeAo6DH1ADQV8YK (Tommy's facility page); republish to those same links. Never commit raw Klaviyo events or anything with customer emails. No em dashes or en dashes in anything you write.

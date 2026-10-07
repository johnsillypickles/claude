# External demand data

Inputs for the League Market Map. Pulled 2026-10-07. Re-run with `python3 census_pull.py` (needs `CENSUS_API_KEY`) and `python3 trends_pull.py` (needs `pip install pytrends`).

## Census (ACS 5-year)

Source: api.census.gov, ACS 5-year detailed tables. Vintage **2024** (the newest served; 2023 was the fallback). Growth base vintage **2019**.

| Field | Variable IDs (verified against 2024 variables.json) |
|---|---|
| pop | B01003_001E |
| income (median household, 2024 dollars) | B19013_001E |
| median_age | B01002_001E |
| share_25_44 | (B01001_011E + 012E + 013E + 014E + B01001_035E + 036E + 037E + 038E) / B01001_001E (male and female 25 to 29, 30 to 34, 35 to 39, 40 to 44) |
| share_ba_plus | (B15003_022E + 023E + 024E + 025E) / B15003_001E (bachelor's, master's, professional, doctorate; population 25+) |
| pop_growth_5y | B01003_001E (2024) / B01003_001E (2019) minus 1, joined on CBSA code or state plus county FIPS |

Negative Census sentinels (for example -666666666) are written as blank.

| File | Rows | Notes |
|---|---|---|
| census_cbsa.csv | 398 | All metro areas, plus the 5 micro areas with pop > 150,000. 537 smaller micro areas dropped. `principal_city` is the first city in the CBSA name; `state` is the state part of the name (can be multi-state, e.g. `NY-NJ`). |
| census_county.csv | 3,222 | All counties and equivalents, including Puerto Rico. One county has no median income. |

**Blank growth (no 2019 code match, from the 2023 CBSA redelineation):** 17410 Cleveland OH (was 17460 Cleveland-Elyria), 28880 Kiryas Joel-Poughkeepsie-Newburgh NY, 47930 Waterbury-Shelton CT, 43640 Slidell-Mandeville-Covington LA, 30500 Lexington Park MD, 28450 Kenosha WI, 11200 Amherst Town-Northampton MA, 48680 Wildwood-The Villages FL, 42580 Seaford DE (micro), 30150 Lebanon-Claremont NH-VT (micro). CBSAs whose code survived but whose boundaries changed still get a growth value, so treat growth for redrawn metros with care.

**Blank county growth:** the 9 Connecticut planning regions (they replaced CT counties in 2022) and Alaska's Chugach and Copper River census areas (split from Valdez-Cordova).

## Google Trends

Source: Google Trends via pytrends 4.x. Geo US, timeframe `today 12-m` (roughly 2025-10 to 2026-10), one term per request, `inc_low_vol=True`.

| File | Rows | Status |
|---|---|---|
| trends_dma.csv | 1,050 (5 terms x 210 DMAs) | OK. Columns: dma, dma_code, term, score, pulled_at |
| trends_city.csv | 0 (header only) | **Failed.** See below |
| trends_log.json | 7 entries | Per-request status |

Terms (DMA): "pickleball", "pickleball league", "pickleball near me", "indoor pickleball", "pickleball lessons".

**How to read scores:** each score is that DMA's share of all its searches that went to the term, scaled 0 to 100 against the top DMA *for that term*. It is not volume. Small DMAs spike: Cheyenne WY-Scottsbluff NE scores 100 for "pickleball" and "indoor pickleball", and 70 for "pickleball league". Scores are **not comparable across terms** because each term is scaled to its own maximum. A 0 means the volume is below Google's threshold, not literally zero. Zero counts out of 210 DMAs: pickleball 1, pickleball near me 34, indoor pickleball 56, pickleball league 109, pickleball lessons 137. Treat "pickleball league" and "pickleball lessons" as sparse signals.

**Failures:**
- The first request was rate-limited. Google redirected it to its www.google.com/sorry captcha page, which the sandbox network does not allow. It succeeded on retry, and all other DMA requests worked first time.
- CITY resolution ("pickleball league" and "pickleball near me") returned 200 cities per term, all scored 0, both with `inc_low_vol=True` and `inc_low_vol=False`. Probable cause (not confirmed): Google does not return city-level values for a geo=US request in this endpoint. The rows were discarded rather than shipping zeros. A possible fix is pulling CITY per state (geo `US-FL` and so on), but those scores would be scaled within each state and not comparable nationally.

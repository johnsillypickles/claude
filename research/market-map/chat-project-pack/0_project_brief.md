# Silly Pickles League Demand: Project Brief

Data as of October 7, 2026. Built by John with Claude.

## What this project is for

Silly Pickles runs adult social pickleball leagues in about 70 US metros, plus Canada and Australia. This project answers three questions:

1. **Where should we add leagues** in markets we already run?
2. **Which new metros** should we enter?
3. **Where can a facility partner** (Tommy's clients) support more league nights or a new facility?

## Live pages

- **League Demand Atlas** (for Tommy and facility clients): https://claude.ai/artifact/8c53FYjzeAo6DH1ADQV8YK
- **League Market Map** (internal): https://claude.ai/artifact/JUbi7isVxbhVFCw3WXaSq9

The pages live in John's account. Changes to them go through John.

## Files in this project

| File | One row per | Use it for |
|---|---|---|
| `1_current_metros.csv` | Metro where we run leagues | League performance, waitlists, Meta spend and CAC, Census, transplants, search interest, demand label and scores |
| `2_new_market_candidates.csv` | US metro of 200k+ with no league within 30 miles | Ranked new-market list with each score part |
| `3_meta_cac_by_market.csv` | Meta (Comscore) media market | Ad spend, clicks, cost per new signup, estimated CAC |
| `4_leagues_2026.csv` | League (Winter to Fall 2026) | Capacity, spots sold, sell-out date, waitlist |

Rates are decimals (0.25 = 25%). Blank means no data.

## Definitions

- **Sold out:** registration filled before it closed. Leagues we closed by hand (3 days before start) or cancelled don't count. Measured per league, so a multi-night league counts only when every night is full.
- **Waitlist after sell-out:** people who signed up for an alert (Stoq) after the league filled. This is our best measure of unmet demand.
- **Cost per new signup:** Meta ad spend in the media market ÷ first-time signups for that market's leagues (Jan 1 to Oct 7, 2026). Low means the market is cheap overall; it credits organic signups to Meta.
- **Estimated Meta CAC:** spend ÷ the new customers Meta likely drove (signups × the market's Meta-tagged order share × 2.7, our account-wide ratio of Meta-reported purchases to Meta-tagged orders). It assumes tracking works equally well everywhere.
- **Transplant rate:** residents aged 25 to 44 who lived in another state or abroad a year earlier, as a share of everyone that age (Census 2020 to 2024). New arrivals looking for friends are a core audience. `transplant_change_vs_2015_19` compares with before COVID.
- **Military flag:** 3%+ of adults in the armed forces. Base rotations inflate the transplant rate, so it's scored neutral there.
- **Search interest (0 to 100):** Google Trends percentile for "pickleball", "pickleball near me" and "pickleball league" (last 12 months). Retirement markets search pickleball a lot, so it carries little weight.
- **Growth** compares the same counties in both periods, so 2023 metro boundary changes don't distort it. Connecticut metros have none (Connecticut replaced its counties in 2022).
- **Demand index (Atlas, 0 to 100):** average percentile of sell-out rate, waitlist per league, registrations per league, and new players per 100k residents aged 25 to 44, among metros with 3+ leagues. Labels: under-supplied (60%+ sold out and index 60+), balanced (healthy), soft, saturated (8+ leagues, under 30% sold out), early (fewer than 3 leagues).
- **Add-leagues score:** sell-outs 35%, waitlist 25%, room to grow 20% (league density, search, transplants), new-player momentum 10%, estimated Meta CAC 10%.
- **New-market score:** population 25%, transplants 20%, fit 25% (age 25 to 44 share, degrees, income, growth), search 10%, our own demand signals 20% (location requests, host applicants, notify-me).

## Headlines

- **Add leagues:** Seattle, Tampa, Austin, San Diego, Phoenix, San Francisco, Denver, Nashville. Denver sold out 5 of 5 Fall leagues and has 706 waitlisted. Seattle has 168 waitlist signups per league.
- **Hold:** Louisville and Oklahoma City (no sell-outs), Indianapolis, Boston, Atlanta.
- **Portland, OR:** The People's Courts fills with a waitlist; suburban leagues don't. Add in the core.
- **New markets:** Cape Coral, Omaha, Worcester, Tulsa, Fayetteville AR, Manchester NH, Ogden, Reno, Chattanooga, Columbia SC. Fort Wayne and Little Rock are already launching. Gulf Coast Florida ranks high on young transplants but only middling on fit.
- **Meta:** cheapest markets at $15k+ spend are San Diego, Nashville, DC, SF (about $71 to $85 estimated CAC vs $102 median). Most expensive: Louisville, Albuquerque, Indianapolis, Jacksonville.

## Caveats

- One season of sell-outs per metro can be noisy; markets with fewer than 6 leagues are small samples.
- Estimated Meta CAC relies on UTM tracking; read it as a ranking, not an exact dollar figure.
- Data stops October 7, 2026. John refreshes it each season with Claude Code (it needs his Shopify, Klaviyo and ad accounts).

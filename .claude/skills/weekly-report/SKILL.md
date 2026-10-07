---
name: weekly-report
description: Build the Silly Pickles Weekly Marketing Update (blended and paid performance, channels, Meta and TikTok phases, email, affiliate orders via UpPromote, organic, facility). Use when John asks to pull, build, refresh or draft the weekly report or weekly update, or asks for last week vs quarter-to-date marketing performance.
---

# Silly Pickles: Weekly Marketing Update

The weekly update has **two deliverables**, emailed together to the team ("Marketing Update M/D/YY", see John's sent mail):

1. **The weekly update**: the email body / Google Doc described below.
2. **The creative report**: a standalone HTML file attached to the email, named `fall26_creative_report_MM.DD.html`. See "Creative report (HTML attachment)" at the end. Never substitute a Google Doc or Sheets-style table for it.

The report is a Google Doc named `Weekly Update M.D.YY` (the date is the Sunday the week ends), saved in the Drive folder `1-oSBwoY2493HW7I4aGaXFyucyyR1iOrm`. Start from the previous week's doc in that folder: copy its structure and narrative, then swap in new numbers. Reference build: `Weekly Update 9.27.26` (`1YX3NuI0ifKvZaPledHIYkEoMSDRhfxCUHdFwEPwWRSo`).

## Periods

- **Week**: Monday to Sunday, America/Chicago. "Last week" is the most recent complete Mon to Sun.
- **Quarter to date (QTD)**: first day of the quarter through the same Sunday. Keep QTD and the week on the same end date, even when the report is built mid-week.
- Always compare with the prior week. Platforms restate late conversions, so re-pull prior weeks rather than copying last week's doc, and call out material restatements.

## Data sources

| Data | Source | Notes |
|---|---|---|
| Blended store metrics | Lebesgue `get_per_period_metrics`, shop `1307999470`, `period_type=week_monday` | `reporting_net_sales` = Net revenue, `total_revenue` = Shop revenue (gross), `total_orders` = Signups |
| Paid by channel | Same call: `fb_*`, `ga_*`, `tt_*`, `total_adv_spend` | Platform-reported purchases and revenue |
| Meta phases | Lebesgue `get_advertising_data_table`, source `facebook`, account `1346441932978787`, level `campaign` | Phase 0 = national/regional, Phase 1 = problem children, from campaign names. Also pull Le Pixel ROAS |
| TikTok phases | Same tool, source `tiktok`, account `7665825541274255361` | |
| Google | Same tool, source `google`, account `3026057182` | Google restates heavily. Flag it |
| Email | Lebesgue `get_klaviyo_performance` (campaign and flow) plus `kl_purchases_conversion_value` | Open and unsub rates, campaign counts by type |
| Affiliate orders | Shopify Admin GraphQL, orders tagged `UpPromote_order` | See the UpPromote section below |
| Organic referrals | Organic Marketing Scoreboard (Fall 2026) vF, `1AnH2yBWuTUfeTT6xjAjaAM-2VKIzNbEUJe8dn0zFSsE` | If it can't be read, carry forward and mark `[Carried from last week, update]` |
| Facility | Narrative from John / Facility Marketing Tracker | Carry forward if nothing new |

## Formulas

- Blended ROAS = Net revenue / Total ad spend
- Spend-to-revenue = Total ad spend / Net revenue
- Blended CAC = Total ad spend / Signups (all orders)
- Paid ROAS and CAC use platform-reported purchases and revenue
- Share of spend = channel spend / total paid spend

## Targets

- Q3 2026: Net revenue $1,800,000, Ad spend $566,000, Blended ROAS 3.18x, Spend-to-revenue 31.5%. Final: $1,966,440 net, $635,893 spend, 3.09x.
- Q4 2026: net revenue up 30% vs Q3 actual = $1,966,440 x 1.30 = **$2,556,372**. Ad spend at about 30% of revenue = **$766,912** budget, which implies **3.33x** blended ROAS (1 / 0.30). "Vs Q3" is read as Q3 actual, not the Q3 target; confirm with John if unsure.
- For pacing, compare QTD against the target prorated by days elapsed (Q4 has 92 days).
- For any other quarter, ask John for targets. Never invent them.

## Section order

1. **Quarter-to-Date**: Metric / Value / Target (net revenue, ad spend, blended ROAS, spend-to-revenue, signups, blended CAC, shop revenue gross), plus 2 pacing bullets.
2. **Quarter-to-Date By Channel**: Meta, Google, TikTok, Total paid: Spend, Share of Spend, Purchases, Revenue, ROAS (Platform), CAC.
3. **Weekly: Blended and Paid (last 10 weeks)**: Week Ending, Total Ad Spend, Signups, Net Revenue, Blended CAC, Blended ROAS, then paid Spend, Purchases, Revenue, CAC, ROAS (platform). Bullets on the week and on restatements.
4. **Last Week By Channel**: spend, revenue and ROAS for the week and QTD.
5. **By Campaign Type: Meta (last week)**: Phase 0 and Phase 1: Spend, Purchases, Revenue, ROAS (Meta), ROAS (Le Pixel), CAC.
6. **By Campaign Type: TikTok (last week)**
7. **Email (Klaviyo)**
8. **Affiliate Orders (UpPromote)**: see below.
9. **Organic Marketing**
10. **Facility Marketing**

## Affiliate Orders (UpPromote)

UpPromote replaced BixGrow as the affiliate platform. The first tagged order is 2026-08-14, and tracking only took hold the week of 8/24. It's the primary affiliate source from Q4 2026 on.

**Pull.** Shopify Admin GraphQL, 50 per page, paginated on `endCursor` until `hasNextPage` is false:

```graphql
query($q:String!,$after:String){ orders(first:50, after:$after, query:$q, sortKey:CREATED_AT){
  pageInfo{hasNextPage endCursor}
  nodes{ name createdAt cancelledAt tags currentSubtotalPriceSet{shopMoney{amount}} } } }
```

Use `q = "tag:UpPromote_order AND created_at:>=<quarter start>"`. Write each order as one line, `name createdAt amount flag`, with flag `BIX` if tags include `Referral-Bixgrow`, else `-`. Then run `scripts/uppromote_weekly.py <file> <week_end YYYY-MM-DD> <qtd_start YYYY-MM-DD>`, which buckets by Central-time Mon to Sun week.

**Definitions.**

- Orders = every tagged order, excluding cancelled ones.
- Paid orders = orders with a subtotal above $0. Test and free codes such as `johntest100` and `SOCIALHOST-FREELEAGUE` come through as $0.
- Net revenue = sum of `currentSubtotalPriceSet`, which is after discounts and refunds, before tax and shipping. Label it as close to net sales.
- AOV = Net revenue / Paid orders.
- Share of blended net revenue = UpPromote net / `reporting_net_sales` for the same period. Share of signups = UpPromote orders / `total_orders`.

**Table.**

| Metric | Week Ending [date] | Prior Week | WoW | Quarter to Date |
|---|---|---|---|---|
| Orders | | | | |
| Paid orders (excl. $0) | | | | |
| Net revenue | | | | |
| AOV (paid orders) | | | | |
| Share of blended net revenue | | | pts | |
| Share of signups | | | pts | |

Then add a weekly trend table (Week Ending, Orders, Net Revenue) for the quarter, followed by 2 to 4 bullets.

**Always flag:**

- Tagged orders that don't match the Organic Marketing scoreboard's referral signups. The scoreboard applies eligibility and facility filters. Say which definition you used.
- The number of $0 orders.
- Orders tagged for both UpPromote and BixGrow, so they aren't counted twice if BixGrow is also reported.
- Commission cost, which isn't in Shopify. It's in UpPromote and the scoreboard's `DATA_UP_Referrals` tab. If you can't get it, write `[commission pending]` and leave affiliate ROAS and CAC out.
- Known outages. For example, 9/22 to 9/25/2026: promo codes were deleted, attribution broke, and Megan made manual commission fixes. Search Slack for "UpPromote" in the report week before writing bullets.
- Q3 2026 only: UpPromote wasn't live before 8/14, so QTD share understates the channel. Also give the share from 8/24 onward.

## Style

- No em dashes or en dashes. Use "to" for ranges ("9/21 to 9/27").
- Money is whole dollars in summary tables and 2 decimals for CAC in the weekly table. ROAS is 2 decimals with an "x".
- Bullets lead with the number and the reason. Mark inferences as such.
- Put missing data in brackets, like `[pending]`. Never estimate it.
- Before sharing, check that the Lebesgue QTD net revenue matches the doc and that the weekly rows add up to the QTD totals.

## Creative report (HTML attachment)

Template: `assets/creative_report_template.html` (a cleaned copy of John's `template.html` from Drive). Fill `__DATA__` with JSON, `__GEN__` with the generated date and `__TAKE__` with 4 to 6 `<li>` takeaways. Optional data keys: `sources` (header source line), `tiktok.source` and `tiktok.note` (shown when `tiktok.creatives` is empty).

**Window:** last 14 days ending on the report Sunday.

**Data:**
- Meta ads: Lebesgue `get_advertising_data_table`, source `facebook`, level `ad`, `period_type=all` for the window (the result is saved to a file; parse it with Python). Ad-level day or week granularity is too large for the tool, so pull delivery history as several `all` calls over short ranges (about 10 to 15 days each) back to early August, plus one call for the last 3 days to decide "running". Ad rows carry `campaign_id` but no campaign name, so also pull level `campaign` for the window and map phases by ID.
- Meta ad sets: same tool at level `adset`, to name the New Customer test themes.
- TikTok ads: channel and phase totals come from Lebesgue (campaign/adset level). Creative-level TikTok rows come from Windsor `get_data`, connector `tiktok`, fields `ad_name, campaign_name, spend, clicks, impressions, complete_payment, total_complete_payment_rate` (purchase value), `ad_status`, because Lebesgue's TikTok ad-level table is too large for the tool even for a single day. Check the Windsor total spend matches Lebesgue's TikTok spend for the window (on 10/4/26 it matched to the cent). Pass `accounts: ["7665825541274255361"]` and `filters: [["spend","gt",0]]`: without the filter, Windsor also returns zero-spend rows for paused copies. Fields `ad_name, date, spend` from early August give launch dates and the "running" check in one call. Phase comes from `campaign_name` (`Fall26_Phase0_Regional` / `Fall26_Phase1_ProblemChildren`). TikTok ad names can differ from Meta ones (for example a `_video` or `_static` suffix), so don't merge them across platforms. Don't retry Lebesgue at TikTok ad level: it fails outright (about 61k tokens for one day, over the 50k cap, and it isn't saved to a file).
- **Check Windsor first.** Run `ListConnectors` with keyword `windsor`. When it works it shows `connected: true`, and the tools load as `mcp__Windsor_ai__*` (`get_connectors` should list `tiktok` with that account). If `connected` is false or `installState` is `needs_reconnect`, its tools won't load. The fix is to disconnect and reconnect Windsor in claude.ai connector settings and turn it on for the chat. The Windsor-to-TikTok link inside Windsor was fine on 10/7/26. Until it's fixed so there are no TikTok creative rows and no Fallback B. Still ship the report: set `D.tiktok.creatives=[]`, fill `D.tiktok.portfolio` from Lebesgue campaign totals, and put the reason in `D.tiktok.note` (the template shows it in place of the cards). Set `D.sources` and `D.tiktok.source` to name the real sources. Tell John that Windsor needs reconnecting in claude.ai connector settings.

**Structure and rules (from the template):**
- Group by creative (ad name) across ad IDs. Phase 1 = campaign `Fall26_Phase1_ProblemChildren`; everything else with purchases is Phase 0. Exclude the lead form campaign. Keep New Customer test ads out of the creative cards and the KPI portfolio. They appear only in the test section, so the cards, the grand total and the benchmark all cover the same spend.
- KPI cards: Overall, Phase 0, Phase 1, each with Meta ROAS, Le Pixel ROAS, spend, revenue, purchases, CPP.
- Sortable summary table, then one card per creative with Total / P0 / P1 metrics, launch and running dates, a grade badge, bullets and a → recommendation.
- Grade each creative's Phase 0 ROAS against the Phase 0 average **excluding the New Customer test campaign**: 🟢 15%+ above, 🟡 within 15%, 🟠 15 to 40% below, 🔴 more than 40% below. Under $1k Phase 0 spend = ◻️ Phase 1 focus. Under $1k total spend = greyed out. Flag under 25 Phase 0 purchases as a small sample.
- Creative test section: New Customer campaign, by ad set theme, each ad listed; ✅ Rotate in if at or above the Phase 0 average; under $200 is low signal.
- TikTok section: same layout, graded against TikTok's own Phase 0 average, one ROAS figure (no Le Pixel).
- Clicks stand in for landing page views.
- **Thumbnails are required for every creative in the report, whatever its spend** (all creative cards, Meta and TikTok, plus every ad row in the New Customer test table, which shows a small thumbnail via the ad's `dimg`). They come from Google Drive first. Never ship the report without them or claim they're unavailable. Steps:
  1. For every creative and test ad (Meta and TikTok), find its file with Drive search `title contains '<ad name>'` (exclude shortcuts, and skip `application/vnd.google-apps.vid` entries, which can't be downloaded as video; use the `.mp4` copy). Several names can be OR'd into one search. Files usually live in the "Fall26 Ad Creatives" and "National + Problem Children Campaigns" folders. Do not use the Creative Roadmap sheet.
  2. Download with Drive `download_file_content`. Results are saved to a tool-results file as JSON with base64 `content`; decode it with Python. Prefer the smallest image (1x1 or 4x5 jpg). Drive refuses files over 10MB, and files over about 7MB crash the connector (confirmed again with an 8.1MB mp4 on 10/7/26, which dropped the Drive connection), so for big videos go to the fallbacks below.
  - **Fallback A (Meta):** Lebesgue `get_facebook_creatives` for the window (use `limit` around 100; the result is saved to a file). It only returns the top creatives by spend, and a full pull (about 270 rows over 14 days) is over the roughly 50k-token cap. To reach low-spend ads, pull single days with `limit` about 125 (about 150 to 170 creatives a day) and merge the results. Pick days when the ad actually ran: check the last-3-days ad table, and for ads that launched recently look at the Drive upload date. Map `ad_id` to ad name with the ad-level table. `preview_url`s on `nikolas-bucket.s3.amazonaws.com` download with curl; `www.facebook.com/ads/image` links redirect to `scontent-*.xx.fbcdn.net`, so both `www.facebook.com` and `*.fbcdn.net` must be allowed in the environment's network settings. Use `curl -L`. Previews come back as JPEGs, usually a 9:16 cover frame for videos, so no ffmpeg step is needed. Fallback A covered every large Meta video on 10/4/26 (TommyASMRVideo, HotGirlSummer video, the Tommy Talking Boo and REVAMP cuts).
  - **Fallback B (TikTok):** Windsor `get_data`, connector `tiktok`, fields `ad_name, video_thumbnail_url`. Needs `*.tiktokcdn.com` allowed in the environment's network settings. On 10/7/26 the URLs came back as `http://p16-common-sign.tiktokcdn.com/...` (and `p19-`). Switch them to `https://` before downloading with curl; they return 720 to 1080px JPEGs, so no ffmpeg step is needed. `*.tiktokcdn-us.com` is a separate domain that is still blocked, but it wasn't used. The URLs are signed and expire, so download them in the same session.
  - If all three fail, the card names the reason (file too large, host blocked) rather than a generic "no preview".
  3. For videos, grab a frame at 1s with ffmpeg (`pip install pillow imageio-ffmpeg` gives both). Resize to 480px max with Pillow, save as JPEG quality ~72, and embed as a `data:image/jpeg;base64,...` URI in the creative's `dimg` field so the HTML stays a single attachable file.
  4. No spend threshold: low-spend and test ads get thumbnails too. Use Drive when a small file exists. Otherwise use the Meta preview, which is often quicker for test ads.
- Render it in Chromium before sending and check there are no script errors. Python Playwright isn't preinstalled: `pip install playwright`, then `p.chromium.launch(executable_path='/opt/pw-browsers/chromium')` (never `playwright install`). Collect `pageerror` and console errors, force `loading='eager'` on images, then count `img` elements where `naturalWidth` is 0 and list the `.ph` placeholders with their card names. The `.ph` list must be empty, and the count of `#testsec img.tthumb` must equal the count of `#testsec tr.adrow`.

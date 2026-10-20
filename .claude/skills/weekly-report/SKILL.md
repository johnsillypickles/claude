---
name: weekly-report
description: Build the Silly Pickles Weekly Marketing Update (blended and paid performance, channels, Meta and TikTok phases, email, organic marketing via UpPromote, facility). Use when John asks to pull, build, refresh or draft the weekly report or weekly update, or asks for last week vs quarter-to-date marketing performance.
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
| Organic marketing (activity) | Organic Marketing Tracker (JC), `1i3tYrN8Toy7ATXrer1qmDDSB7zwJIiGy6xaypt4CS60`, Summary tab, first table ("Team totals"). Replaced Nate's scoreboard on 10/12/26; never use the scoreboard | If it can't be read, carry forward and mark `[Carried from last week, update]` |
| Organic marketing (revenue) | Shopify Admin GraphQL, orders tagged `UpPromote_order` | See "Organic Marketing (UpPromote)" below |
| Facility | Facility Marketing Tracker v4 (`16Bkghe54LCnpfkCSbzY7FTSyHmsrdH6ZpxpGYiedw40`) plus Gmail threads John is copied on | See "Facility Marketing" below |

## Formulas

- Blended ROAS = Net revenue / Total ad spend
- Spend-to-revenue = Total ad spend / Net revenue
- Blended CAC = Total ad spend / Signups (all orders)
- Paid ROAS and CAC use platform-reported purchases and revenue
- Share of spend = channel spend / total paid spend

## Targets

- Q3 2026: Net revenue $1,800,000, Ad spend $566,000, Blended ROAS 3.18x, Spend-to-revenue 31.5%. Final: $1,966,440 net, $635,893 spend, 3.09x.
- Q4 2026: net revenue up 30% vs Q3 actual = $1,966,440 x 1.30 = **$2,556,372**. Ad spend at about 30% of revenue = **$766,912** budget, which implies **3.33x** blended ROAS (1 / 0.30). "Vs Q3" is read as Q3 actual, not the Q3 target. As of 10/14/26 John marks these targets **(PENDING)** in the doc: label the target column and bullet that way until he says they are final.
- For pacing, compare QTD against the target prorated by days elapsed (Q4 has 92 days).
- Early in a quarter, spend-to-revenue runs high because spend leads revenue. Next to the QTD figure, give context with real numbers, not softer wording: the same days of the prior quarter and where that quarter finished (Q3 2026: 42.7% after 7/1 to 7/11, finished 32.3%), and spend-to-revenue excluding Phase 1 (Meta + TikTok Problem Children spend and its platform-attributed revenue). Always report the headline number unchanged.
- For any other quarter, ask John for targets. Never invent them.

## Section order

0. **Executive summary** (starts with the week ending 10/18/26; first thing in the doc, before any table): 3 to 5 plain-English bullets for Tommy: how it's going vs pace and targets, the 1 to 3 biggest reasons, what's working, and next steps with owners. No tables, no jargon, every bullet has a number.
1. **Quarter-to-Date**: Metric / Value / Target (net revenue, ad spend, blended ROAS, spend-to-revenue, signups, blended CAC, shop revenue gross), plus 2 pacing bullets.
2. **Quarter-to-Date By Channel**: Meta, Google, TikTok, Total paid: Spend, Share of Spend, Purchases, Revenue, ROAS (Platform), CAC.
3. **Weekly: Blended and Paid (last 10 weeks)**: Week Ending, Total Ad Spend, Signups, Net Revenue, Blended CAC, Blended ROAS, then paid Spend, Purchases, Revenue, CAC, ROAS (platform). Bullets on the week and on restatements.
4. **Last Week By Channel**: spend, revenue and ROAS for the week and QTD.
5. **By Campaign Type: Meta (last week)**: Phase 0 and Phase 1: Spend, Purchases, Revenue, ROAS (Meta), ROAS (Le Pixel), CAC.
6. **By Campaign Type: TikTok (last week)**
7. **Email (Klaviyo)**
8. **Organic Marketing (UpPromote)**: see below. One section; affiliates, UpPromote and organic marketing are the same program.
9. **Facility Marketing**
Last. **Ideas and experiments to improve** (Tommy, 10/14/26): a ranked table of what would bring ad spend down as a share of revenue: # / Idea / Why (evidence with numbers) / Effort / Owner / Priority or status. Carry the list forward week to week and update each item's status and result. Always consider: league selection and fill priority (Mar's Monday field), longer lead times with pre-registration lead forms (Fort Wayne and Little Rock: $27 and $32 per signup), creative (fewer, stronger concepts; see the creative report), waitlist / Notify-me email capture, Google search expansion, referrals (a refer-a-friend offer for current players already exists and is promoted by email only, not in paid ads, so frame ideas as growing or measuring it, not starting one), localized ads, new channels. Rank by expected savings vs effort, and mark untested ideas as our assumption.

## Organic Marketing (UpPromote)

Affiliates, UpPromote and organic marketing are one program, reported in one section. The organic team are internal part-time marketers. Each is paid an hourly rate plus a bonus for signups from the affiliates they recruit, and also posts their own UpPromote link for a bonus. UpPromote replaced BixGrow (first tagged order 2026-08-14; tracking took hold the week of 8/24).

**A. Activity: tracker table (primary).** Copy the first table on the Summary tab of the Organic Marketing Tracker (JC) as-is: rows "Affiliates onboarded", "Clicks", "Signups", "Conversion rate (signups / clicks)", "Affiliates (total, as of period end)" with columns Last week, Prior week, WoW Change, Quarter to date, Month to date. Read `Summary!A1:F16`; check that the "Last week starts" cell matches the report week before copying, and note the "UpPromote data through" timestamp. Tracker signups are league spots from UpPromote referrals minus denied referrals (a 2-spot order counts 2), plus manual adjustments. Bullets can draw on the "By marketer" table on the same tab (top marketers by signups, clicks without signups).

**B. Revenue: Shopify tagged orders.** Pull orders tagged `UpPromote_order`, 50 per page, paginated on `endCursor` until `hasNextPage` is false:

```graphql
query($q:String!,$after:String){ orders(first:50, after:$after, query:$q, sortKey:CREATED_AT){
  pageInfo{hasNextPage endCursor}
  nodes{ name createdAt cancelledAt tags currentSubtotalPriceSet{shopMoney{amount}} } } }
```

Use `q = "tag:UpPromote_order AND created_at:>=<prior week Monday or quarter start, whichever is earlier>"`. Write each order as one line, `name createdAt amount flag`, with flag `BIX` if tags include `Referral-Bixgrow`, else `-`. Then run `scripts/uppromote_weekly.py <file> <week_end YYYY-MM-DD> <qtd_start YYYY-MM-DD>`, which buckets by Central-time Mon to Sun week.

- Orders = tagged orders, excluding cancelled. Paid orders = subtotal above $0 (test and free codes such as `johntest100` and `SOCIALHOST-FREELEAGUE` are $0).
- Net revenue = sum of `currentSubtotalPriceSet` (after discounts and refunds, before tax and shipping). AOV = Net revenue / Paid orders.
- Share of blended net revenue = organic net / `reporting_net_sales`; share of signups = tagged orders / `total_orders`.

| Metric | Week Ending [date] | Prior Week | WoW | Quarter to Date |
|---|---|---|---|---|
| Tagged orders | | | | |
| Net revenue | | | | |
| AOV (paid orders) | | | | |
| Share of blended net revenue | | | pts | |

**C. Cost, ROAS and CAC (monthly).** Cost = organic marketers' hourly pay + signup bonuses + affiliate commissions. Organic ROAS = organic net revenue / cost; organic CAC = cost / tracker signups. John keeps the monthly cost data (starting September 2026) somewhere private, not on a tab the organic team can see, because hours could be back-calculated from it. [Location pending: ask John for the sheet link if it isn't recorded here.] Report team-level ROAS and CAC only, never per marketer. The weekly update doesn't go to the organic team, so team-level figures are fine there. Use his figures as given; if the month isn't there yet, show `[pending: John adding <month> cost data]`. Never estimate hours, rates or commissions.

**Always flag:**

- Tracker signups (spots, minus denied, plus adjustments) vs Shopify tagged orders (orders) will differ. Say which number each line uses.
- If tracker signups are well below Shopify tagged orders, do not blame sync lag. The Summary team totals only count affiliates with a Marketer (Weekly Data column F). Sum `Weekly Data` signups for the week with and without a Marketer, and confirm the total against UpPromote `list_referrals` for the week (drop `Network referrals` rows, they are upline credits; add spots for orders with quantity 2+). Report the unassigned spots and the top unassigned affiliates by name, and flag any `*.sillypickles` email with no Marketer as possibly a team member missing from the tracker. (10/18/26 week: 33 spots in UpPromote and Weekly Data, 13 on Summary, 20 from unassigned affiliates.)
- The number of $0 orders and any orders tagged for both UpPromote and BixGrow.
- Commission rule changes and outages. Search Slack for "UpPromote" in the report week (e.g. 10/8/26: commission changed from per order to per league item; 9/22 to 9/25/26: promo codes deleted, attribution broke).
- Refund restatements of prior weeks' revenue.

## Style

- No em dashes or en dashes. Use "to" for ranges ("9/21 to 9/27").
- Money is whole dollars in summary tables and 2 decimals for CAC in the weekly table. ROAS is 2 decimals with an "x".
- **Plain English (John, 10/14/26).** Write bullets for someone who doesn't read dashboards. Short sentences. In bullets, say ROAS as money ("$1.87 of revenue per $1 of ads"), keep the "x" format in tables only, and the intro paragraph defines ROAS once ("ROAS means revenue per $1 of ad spend: 2.00x means $2 back for every $1"). Explain jargon the first time it appears in a section: Problem Children / Phase 1 = ads for struggling leagues; Phase 0 = national ads; Le Pixel = our own tracking; retargeting = ads to people who already visited the site; flows = automated emails; restatement = platforms adding late sales to past weeks. Name campaigns by what they do, not their Meta names. Skip formulas in bullets unless the number would otherwise be unclear. Say "our read" or "our assumption" instead of "(inference)".
- Bullets lead with the number and the reason. Mark inferences as such.
- Put missing data in brackets, like `[pending]`. Never estimate it.
- **Edits after the doc exists go in the same doc.** John's Google Docs connector is connected (10/14/26). Make any later change (John's feedback, corrections, restated numbers) with Google Docs `update_doc` on the existing doc so the link stays the same; never recreate the doc to apply an edit. Read the doc's `revisionId` with `read_doc` first and send it as `writeControl.requiredRevisionId`. Follow the google-workspace skill's `references/docs.md`. If the Docs tools aren't loaded in a session, ask John to turn the connector on rather than making a new doc.
- **Dollar signs in the Google Doc.** The doc is created by uploading HTML with Drive `create_file` (`contentMimeType: text/html`). Google turns text between two `$` signs in one paragraph into an equation (Cambria Math italics, spaces removed). Before uploading, wrap every `$` in `<span style="color:#000000">$</span>`; tested 10/14/26, and HTML entities, zero-width spaces and plain spans do not work. After creating the doc, export it as PDF and check that no text uses Cambria Math.
- Before sharing, check that the Lebesgue QTD net revenue matches the doc and that the weekly rows add up to the QTD totals.

## Creative report (HTML attachment)

Template: `assets/creative_report_template.html` (a cleaned copy of John's `template.html` from Drive). Fill `__DATA__` with JSON, `__GEN__` with the generated date and `__TAKE__` with 4 to 6 `<li>` takeaways. Optional data keys: `sources` (header source line), `tiktok.source` and `tiktok.note` (shown when `tiktok.creatives` is empty), and `fatigue` (the fatigue check section, see "Creative fatigue check").

**Window:** last 14 days ending on the report Sunday.

**Data:**
- Meta ads: Lebesgue `get_advertising_data_table`, source `facebook`, level `ad`, `period_type=all` for the window (the result is saved to a file; parse it with Python). Ad-level day or week granularity is too large for the tool, so pull delivery history as several `all` calls over short ranges (about 10 to 15 days each) back to early August, plus one call for the last 3 days to decide "running". Ad rows carry `campaign_id` but no campaign name, so also pull level `campaign` for the window and map phases by ID.
- Meta ad sets: same tool at level `adset`, to name the New Customer test themes.
- TikTok ads: channel and phase totals come from Lebesgue (campaign/adset level). Creative-level TikTok rows come from Windsor `get_data`, connector `tiktok`, fields `ad_name, campaign_name, spend, clicks, impressions, complete_payment, total_complete_payment_rate` (purchase value), `ad_status`, because Lebesgue's TikTok ad-level table is too large for the tool even for a single day. Check the Windsor total spend matches Lebesgue's TikTok spend for the window (on 10/4/26 it matched to the cent). Pass `accounts: ["7665825541274255361"]` and `filters: [["spend","gt",0]]`: without the filter, Windsor also returns zero-spend rows for paused copies. Fields `ad_name, date, spend` from early August give launch dates and the "running" check in one call. Phase comes from `campaign_name` (`Fall26_Phase0_Regional` / `Fall26_Phase1_ProblemChildren`). TikTok ad names can differ from Meta ones (for example a `_video` or `_static` suffix), so don't merge them across platforms. Don't retry Lebesgue at TikTok ad level: it fails outright (about 61k tokens for one day, over the 50k cap, and it isn't saved to a file).
- **Check Windsor first.** Run `ListConnectors` with keyword `windsor`. When it works it shows `connected: true`, and the tools load as `mcp__Windsor_ai__*` (`get_connectors` should list `tiktok` with that account). If `connected` is false or `installState` is `needs_reconnect`, its tools won't load. The fix is to disconnect and reconnect Windsor in claude.ai connector settings and turn it on for the chat. The Windsor-to-TikTok link inside Windsor was fine on 10/7/26. Until then there are no TikTok creative rows and no Fallback B. Still ship the report: set `D.tiktok.creatives=[]`, fill `D.tiktok.portfolio` from Lebesgue campaign totals, and put the reason in `D.tiktok.note` (the template shows it in place of the cards). Set `D.sources` and `D.tiktok.source` to name the real sources. Tell John that Windsor needs reconnecting in claude.ai connector settings.

**Structure and rules (from the template):**
- Group by creative (ad name) across ad IDs. Phase 1 = campaign `Fall26_Phase1_ProblemChildren`; everything else with purchases is Phase 0. Exclude the lead form campaign. Keep test-campaign ads out of the creative cards and the KPI portfolio. Test campaigns are `Fall26_Phase0_NewCustomer(only)` (`120252634220400019`) and, from 10/5/26, `Fall26_Phase0_CreativeTest-tROASfocus` (`120253673698350019`), a tROAS-bidding copy of the same ad sets; treat any new campaign with "CreativeTest" in its name the same way. They appear only in the test section, so the cards, the grand total and the benchmark all cover the same spend.
- **Localized creatives are one card.** An ad name containing `_Localized_` (for example `Oct2026_Localized_NewLeagueAlert_Static_v1`) is one template with per-location text (Tualatin, Houston, Dallas, ...). Every location version shares that ad name, so sum spend, revenue and purchases for all of them, across every ad set and phase, into a single card. Never split a Localized creative by location or ad set. For its thumbnail any one location version will do: Drive search `title contains '<ad name>'` returns one file per facility key (`..._v1_Tualatin-RECS_9x16.png`), so take the first image. Older location versions that still run under their own names are mapped to the Localized name before grouping, using the alias list here (`old ad name -> Localized ad name`). Aliases: none yet (John to confirm the Houston and Dallas versions of `Oct2026_Localized_NewLeagueAlert_Static_v1`).
- KPI cards: Overall, Phase 0, Phase 1, each with Meta ROAS, Le Pixel ROAS, spend, revenue, purchases, CPP.
- Sortable summary table, then one card per creative with Total / P0 / P1 metrics, launch and running dates, a grade badge, bullets and a → recommendation.
- Grade each creative's Phase 0 ROAS against the Phase 0 average **excluding the New Customer test campaign**: 🟢 15%+ above, 🟡 within 15%, 🟠 15 to 40% below, 🔴 more than 40% below. Under $1k Phase 0 spend = ◻️ Phase 1 focus. Under $1k total spend = greyed out. Flag under 25 Phase 0 purchases as a small sample.
- Creative test section: all test campaigns, by ad set theme (strip the `Fall26_Phase0_NewCus_` prefix; suffix tROAS-campaign themes with " · tROAS test"), each ad listed; drop ads with under $0.50 spend in the window; ✅ Rotate in if at or above the Phase 0 average; under $200 is low signal.
- TikTok section: same layout, graded against TikTok's own Phase 0 average, one ROAS figure (no Le Pixel).
- Clicks stand in for landing page views.
- **Thumbnails are required for every creative in the report, whatever its spend** (all creative cards, Meta and TikTok, plus every ad row in the New Customer test table, which shows a small thumbnail via the ad's `dimg`). They come from Google Drive first. Never ship the report without them or claim they're unavailable. Steps:
  1. For every creative and test ad (Meta and TikTok), find its file with Drive search `title contains '<ad name>'` (exclude shortcuts, and skip `application/vnd.google-apps.vid` entries, which can't be downloaded as video; use the `.mp4` copy). Several names can be OR'd into one search. Files usually live in the "Fall26 Ad Creatives" and "National + Problem Children Campaigns" folders. Do not use the Creative Roadmap sheet.
  2. Download with Drive `download_file_content`. Results are saved to a tool-results file as JSON with base64 `content`; decode it with Python. Prefer the smallest image (1x1 or 4x5 jpg). Drive refuses files over 10MB, and files over about 7MB crash the connector (confirmed again with an 8.1MB mp4 on 10/7/26, which dropped the Drive connection), so for big videos go to the fallbacks below.
  - **Fallback A (Meta):** Lebesgue `get_facebook_creatives` for the window (use `limit` around 100; the result is saved to a file). It only returns the top creatives by spend, and a full pull (about 270 rows over 14 days) is over the roughly 50k-token cap. To reach low-spend ads, pull single days with `limit` about 125 (about 150 to 170 creatives a day) and merge the results. Pick days when the ad actually ran: check the last-3-days ad table, and for ads that launched recently look at the Drive upload date. Map `ad_id` to ad name with the ad-level table. `preview_url`s on `nikolas-bucket.s3.amazonaws.com` download with curl; `www.facebook.com/ads/image` links redirect to `scontent-*.xx.fbcdn.net`, so both `www.facebook.com` and `*.fbcdn.net` must be allowed in the environment's network settings. Use `curl -L`. Previews come back as JPEGs, usually a 9:16 cover frame for videos, so no ffmpeg step is needed. Fallback A covered every large Meta video on 10/4/26 (TommyASMRVideo, HotGirlSummer video, the Tommy Talking Boo and REVAMP cuts).
  - **Fallback B (TikTok):** Windsor `get_data`, connector `tiktok`, fields `ad_name, video_thumbnail_url`. Needs `*.tiktokcdn.com` allowed in the environment's network settings. On 10/7/26 the URLs came back as `http://p16-common-sign.tiktokcdn.com/...` (and `p19-`). Switch them to `https://` before downloading with curl; they return 720 to 1080px JPEGs, so no ffmpeg step is needed. `*.tiktokcdn-us.com` is a separate domain that is still blocked, but it wasn't used. The URLs are signed and expire, so download them in the same session.
  - If all three fail, the card names the reason (file too large, host blocked) rather than a generic "no preview".
  3. For videos, grab a frame at 1s with ffmpeg (`pip install pillow imageio-ffmpeg` gives both). Resize to 480px max with Pillow, save as JPEG quality ~72, and embed as a `data:image/jpeg;base64,...` URI in the creative's `dimg` field so the HTML stays a single attachable file.
  - **Same creative, other platform or cut:** when one file is unavailable, reuse the thumbnail of the identical creative (e.g. the Meta and TikTok copies of a video, a TikTok `_static` version of a Meta static, or a `-shortened` cut). Download TikTok `video_thumbnail_url`s for every TikTok video in the same session even when Meta also has the ad.
  4. No spend threshold: low-spend and test ads get thumbnails too. Use Drive when a small file exists. Otherwise use the Meta preview, which is often quicker for test ads.
- Render it in Chromium before sending and check there are no script errors. Python Playwright isn't preinstalled: `pip install playwright`, then `p.chromium.launch(executable_path='/opt/pw-browsers/chromium')` (never `playwright install`). Collect `pageerror` and console errors, force `loading='eager'` on images, then count `img` elements where `naturalWidth` is 0 and list the `.ph` placeholders with their card names. The `.ph` list must be empty, and the count of `#testsec img.tthumb` must equal the count of `#testsec tr.adrow`.

## Creative fatigue check (section of the creative report)

Since 10/16/26 the fatigue check is a section of the creative report (`D.fatigue`, rendered after the Meta cards), not a separate page. Meta's own fatigue, similarity and theme metrics aren't in John's Ads Manager, Windsor or Lebesgue (checked 10/16/26), so we use our own rules, back-tested on our Meta history.

**History store.** Weekly Meta ad-level results live in the private Google Sheet "Meta weekly ad history (fatigue check)" (ID `19pC7Bwvgsi7yO6R-spa8dKSR6pH90o6IZByErdaA_pg`, tab `Untitled`; Jan 6, 2025 to Oct 11, 2026 loaded and verified 10/16/26). Never commit it: this repo is public. Columns: `week` (Monday), `key` (normalized ad name, see `norm()` in the script), spend, impressions, clicks, purchases, purchases_conversion_value, add_to_cart. One `__account__` row per week holds the whole Meta account; other rows are creative-weeks with $250+ spend (only those count as "live" weeks). Ad names are normalized so " - Copy" duplicates, `AllGeos_Pickleball_` prefixes and format suffixes (`_Static`, `_Video`, `_1080x1920`, ...) roll up to one creative across ad sets and relaunches.

**Each week** (script: `scripts/fatigue.py`):
1. Read the Sheet with `get_values` (range `Untitled!A:H`; the result is usually saved to a file) and run `fatigue.py from-sheet <values file> history.json`.
2. Pull the report week from Lebesgue: `get_advertising_data_table`, source `facebook`, account `1346441932978787`, level `ad`, Monday to Sunday, `period_type=all`. If it's over the 50k-token limit, split it into Mon-Wed and Thu-Sun (then single days). Pulls must not cross a Monday. If last week is missing from the Sheet too, pull it as well.
3. `fatigue.py add history.json <pull files>`: it refuses a day that's already in the history.
4. `fatigue.py to-rows history.json new_rows.json --weeks <new Mondays>`, then append those rows to the Sheet with `append_values`.
5. `fatigue.py score history.json --report data.json --end <Monday of the report's last week> --out fatigue.json`, then add context fields and set `D.fatigue`:
   - per row, `freq` (views per person over the 14 days: sum of impressions / sum of reach, from Windsor `facebook` ad level) and `quality` (spend-weighted Meta quality rank). Both are context only: there's no history to test them.
   - `themes` (theme, ads, spend, roas, pixel_roas, fatigued count) and `groups` (near-duplicate group, ads, spend, roas, note). Tag themes and near-duplicates by concept, e.g. nostalgia/gameplay, beginner reassurance, phrase statics, social proof, urgency, identity humor, founder video, localized announcement, volleyball, how it works; groups like the Boo cuts or Localized v1 to v3.

**Rules** (from the Jan 2025 to Oct 2026 study, 58 creatives with 6+ live weeks and $3k+ spend):
- **Season-adjusted ROAS index** = the creative's ROAS divided by the whole Meta account's ROAS in the same weeks, pooled over 2 live weeks.
- **Fatigued:** the last 2 live weeks' index is at or below 60% of the creative's best 2-week index.
- **Watch:** 2 or more of:
  - 8+ live weeks
  - click rate down 15%+ vs its first 2 live weeks
  - index down 25%+ vs its best 2 weeks
  - purchases per click down 40%+ vs its first 2 live weeks
- **Fresh:** neither. **New:** under 3 live weeks. **Not live:** no $250+ week in the last 2 weeks.
- What the study found:
  - 36 of 58 creatives wore out, around live week 8 or 9 (median; range 3 to 31).
  - After wearing out they kept running: $342k at 1.73x vs 2.08x for the account in the same weeks.
  - The Watch rule caught 56% of wear-outs a week early and 34% two weeks early, but also flags 18% of healthy weeks. So Watch means "check it", not "pause it".
  - Rising cost per 1,000 views was NOT a warning sign (it rose more often in healthy weeks). Neither was lifetime spend or lifetime views, so don't use them.
  - Our old guesses (CPM up 20%, 3+ views per person, bottom-10% quality) are retired as scored signals.
- `score` re-runs this back-test on the full history every week. The report's evidence box shows the fresh numbers, so they update as history grows.
- **Caveat to state when it applies:** a creative moved into weaker ad sets (e.g. Problem Children) can look fatigued because of where it ran, not because people are tired of it. Say so in the takeaway when most of its spend moved phases.

**Wording (John, 10/19/26):** the report shows the Fatigued verdict as **"Fatiguing"** (the script and data keep the key `Fatigued`). Never lead with "X% of spend went to fatigued ads": Tommy reads that as waste. Fatiguing means an ad is well below its own best weeks, not that it is losing money. Always pair the share with where the money goes next (already off / pause now / keep because it still beats its phase average).

**Action column:** `score` adds `action_kind`, `action` and `split` per row via `action()`; the template shows Action next to the verdict, plus a "where the money goes" box above the table. Rules:
- Fatiguing, beats the Phase 0 average in Phase 0 but not the Phase 1 average in Phase 1 (both $500+): keep in Phase 0, pause in the Phase 1 ad sets.
- Fatiguing, still beats the average of the phase where most of its spend is: keep for now, line up a replacement.
- Fatiguing otherwise: pause, and check its ad sets keep 2+ live ads.
- Not running (no spend in the last 3 days of the window): "already off"; a Fresh ad that was beating its phase average gets "consider turning it back on".
- Watch: review, no pause yet. Fresh at 15%+ above its phase average: keep and give more budget. New: too new to judge.
- Status changes John reports after the window (e.g. "I paused X") override the action text for that row; say who paused it and when. Check live status before telling John an ad is running: Lebesgue's `status` field can lag, so confirm with Windsor daily spend (`date, ad_name, spend` for the last few days; the ESSENTIAL plan has no same-day hourly data).

**In the report:**
- One takeaway bullet on fatigue in the "where the money goes" form: total on fatiguing ads, then already off / pause now / keep, naming the biggest cases.
- Feed the results into the weekly doc's improvement-ideas section: which ads to retire or refresh, and which themes to brief Moodyboy on.
- If Meta's own metrics later show up in Ads Manager or Windsor fields, add them as context columns.

## Facility Marketing

Sources:
- **Tracker** (Facility Marketing Tracker v4): `Dashboard` tab for coverage, pipeline by status and owner workload; `Leagues` tab for each league's owner, start date, fill %, outreach status and last contact.
- **Gmail**: John is copied on facility outreach. Search the report week, e.g. `after:<Mon> before:<next Mon> league (from:aly@sillypickles.com OR from:katie@sillypickles.com OR from:grace@sillypickles.com OR from:tommy@sillypickles.com OR to:aly@sillypickles.com OR to:katie@sillypickles.com)`, and read the threads with facility domains (subjects like "Marketing Kickoff!" or "Silly Pickles League at <facility>"). Skip pure ops/booking threads (court booking, invoices, agreements).

**The tracker lags the inbox.** Treat email as the source of truth for what happened, and list every league where the tracker status disagrees with the emails (e.g. Pictona was "Not Started" while Tommy had already asked the facility for a list of fun/social players). Tommy and Nate also do facility outreach that never gets logged.

Section layout:
1. Coverage line from the Dashboard (leagues starting in 30 days, how many have outreach started, coverage %, follow-ups due, unassigned).
2. **Activity this week** (from email): facility, who reached out, what was asked or sent, the facility's response, and the league's current fill %.
3. **At-risk leagues**: start within 14 days and under 30 players signed up (John's rule from 10/14/26), with outreach status (flag any with no outreach).
4. **Tracker updates needed**: leagues where email activity isn't reflected in the tracker.
- Don't present "avg fill, contacted vs not contacted" from the Dashboard as an effect of outreach: the team targets struggling leagues, so contacted leagues are lower-fill by selection.

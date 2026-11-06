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
| Meta lead forms | Windsor `get_data`, connector `facebook`, fields `campaign, adset_name, date, spend, clicks, actions_lead`, filter campaign contains "LeadForm" | Lebesgue shows lead-form campaigns with 0 purchases. Report leads and cost per lead (spend / leads) per market, keep them out of ROAS, and say Meta's lead count is the source (`actions_leadgen_grouped` reads 0 for these) |
| TikTok phases | Same tool, source `tiktok`, account `7665825541274255361` | |
| Google | Same tool, source `google`, account `3026057182` | Google restates heavily. Flag it |
| Email | Lebesgue `get_klaviyo_performance` (campaign and flow) plus `kl_purchases_conversion_value` | Open and unsub rates, campaign counts by type |
| Organic marketing | Organic Marketing Tracker, UpPromote, contractor sheet | See "Organic marketing" below |
| Facility marketing | Shopify sessions and discount codes, UpPromote facility programs, contractor sheet | See "Facility marketing" below |
| Tests | Klaviyo, Meta (Lebesgue, Windsor), Slack | See "Tests" below |

## Formulas

- Blended ROAS = MER = Net revenue / Total ad spend (call it "MER (blended ROAS)" in the doc; some people compute MER on gross revenue, ours is net)
- Spend-to-revenue = Total ad spend / Net revenue
- Blended CAC = Total ad spend / Signups (all orders)
- Paid ROAS and CAC use platform-reported purchases and revenue
- Share of spend = channel spend / total paid spend

## Targets

- Q3 2026: Net revenue $1,800,000, Ad spend $566,000, Blended ROAS 3.18x, Spend-to-revenue 31.5%. Final: $1,966,440 net, $635,893 spend, 3.09x.
- Q4 2026: net revenue up 30% vs Q3 actual = $1,966,440 x 1.30 = **$2,556,372**. Ad spend at about 30% of revenue = **$766,912** budget, which implies **3.33x** blended ROAS (1 / 0.30). "Vs Q3" is read as Q3 actual, not the Q3 target. Final (John, 11/6/26): no "PENDING" label.
- Don't show prorated "target to date" or say revenue is behind or ahead of pace: pacing swings with league start dates (John, 11/6/26). Instead show what the rest of the quarter needs: (goal minus QTD) / days left, for net revenue and for ad spend, as "$X a day". Q4 has 92 days.
- Early in a quarter, spend-to-revenue runs high because spend leads revenue. Next to the QTD figure, give context with real numbers, not softer wording: the same days of the prior quarter and where that quarter finished (Q3 2026: 42.7% after 7/1 to 7/11, finished 32.3%), and spend-to-revenue excluding Phase 1 (Meta + TikTok Problem Children spend and its platform-attributed revenue). Always report the headline number unchanged.
- For any other quarter, ask John for targets. Never invent them.

## Section order (Tommy, 11/6/26: "too long, make it digestible")

The doc is about 2 pages. Every section is a few bullets or one small table. Long detail (per-campaign lists, restatements, flags, per-person splits, tracker fixes, activity logs) goes in your reply to John, not the doc.

**1. Executive summary**
- **a. Performance (3 bullets + one table).** Table rows: Net revenue, Ad spend, MER (blended ROAS = net revenue / total ad spend), Spend-to-revenue, Signups, Blended CAC. Columns: Last week, Prior week, QTD, Q4 goal (the full-quarter goal). Bullets: what the rest of the quarter needs per day (see Targets), MER so far vs goal, the week vs prior week with the 1 to 2 biggest reasons.
- **b. What's working in ads (2 to 4 bullets).** Thematic, not ad by ad: which concepts win (for example founder video, localized announcements, beginner reassurance, nostalgia), which are fatiguing, and what we're briefing next. Draw from the creative report's themes and fatigue check. Name at most 2 ads per bullet, by what they show. For localized announcements, always say whether they beat generic ads in the same leagues (use the localized vs generic test numbers), not just where they ran.
- **c. What we're testing.** One short block per live test: what we changed, when, the result so far with numbers vs a control, and the call (keep, kill, keep testing). Carry the list week to week and drop tests once called. Always cover:
  - Email A/B tests (see "Tests: email A/B").
  - Ad fatigue: purchaser exclusions (see "Tests: purchaser exclusions").
  - Localized vs generic creative, head to head within each market (see "Tests: localized vs generic"). One small table, markets as rows.
  - Any other running experiment (lead forms, tROAS / creative test campaigns, new channels, organic bonus test). The old "Ideas and experiments" table (Tommy, 10/14/26) folds in here: a running idea is a test; untested ideas go in one closing line, "Next to try:", top 3, marked as our assumption.

**2. Channels (one table).** Meta, Google, TikTok, Email (Klaviyo attributed, shown separately, not added to the paid total), Total paid: spend, revenue, ROAS for last week and QTD. One bullet only if something moved a lot.

**3. Organic marketing.** See "Organic marketing" below. One weekly table, plus the monthly table in the first report of each month, plus 2 lines on the bonus.

**4. Facility marketing.** See "Facility marketing" below. Same shape as organic.

Dropped from the doc on 11/6/26: the 10-week weekly table, last week by channel, Meta and TikTok by campaign type, the email section and the long organic and facility sections. Pull the data anyway when a bullet needs it.

**First report of each month** (the week that contains the 1st, or the first one built after it): add last month's numbers to organic and facility, including costs from the time sheets.

## Tests (section 1c)

Find tests each week in Slack (search "test", "A/B", "experiment", "pilot" in #core-four, #new-email, #organicmktg, the paid ads group DMs and #lebesgue-silly-pickles), Meta campaign names ("Test", "CreativeTest", "NewCustomer", "LeadForm") and Kameron's task lists. John asked Kameron on 10/23 to keep a test log; use it once it exists. For every test give: what changed, start date, result vs a control with numbers, sample size, and the call. Mark our reads as such.

**Email A/B.** Klaviyo `get_campaigns` (filter `greater-or-equal(created_at,<quarter start>)`, include campaign-messages); keep messages with more than one variation. `get_campaign_message` (include campaign-variations) for subject and template. `get_campaign_report` with `conversion_metric_id` `VAQscR` (Placed Order), group_by `[campaign_id, campaign_message_id, send_channel, variation, variation_name]`; pull unfiltered (a campaign_id filter returns empty). Per variant: recipients, open rate, click rate, orders, revenue, revenue per recipient. Pool by wave (same design vs same design). Run a two-proportion z-test on clicks and orders; under |z| 1.96 = "no winner yet". As of 11/6/26 these are design tests (same subject): wave 1 "A/B" 10/21 to 10/27 (Payton's seasonal designs vs vanilla). The letter is not consistent (A was seasonal for Chicago and Portland OR, vanilla elsewhere), so always pool by design, never by letter. Tell them apart by template name (seasonal: "Fall Last Call", "Late Fall Open Registration"; vanilla: "Spring 2026_Last Call_Not Registered", "Open Registration") or by `render_email_template` (seasonal has a full-width hero JPEG and a peach or yellow background; vanilla is white with the small logo). `get_email_template` returns 422. Check each variant's buttons link to the right market (Chicago's vanilla button pointed to Portland on 10/23), wave 2 "Control/Test" from 10/29 (Test = John's new templates). The split has no winner send, so say a winner was never applied.

**Purchaser exclusions (ad fatigue).** Timeline: 10/5 last-30-day purchasers excluded; by 10/8 to 10/12 all past customers (Shopify list plus a Meta purchasers audience); Tommy said on 10/15 he doesn't want ALL customers excluded. Check current scope each week with Windsor `facebook` fields `campaign, adset_name, adset_targeting, spend` for the report week (it shows current targeting only, no history). Compare equal windows before (9/21 to 10/4) and after (from 10/12), skipping 10/5 to 10/11: spend, Meta ROAS, CPP, frequency (Windsor), CTR, CPM, Le Pixel first-time share (Lebesgue `pixel_customer_type` first), and blended MER (net revenue / total ad spend from the weekly Lebesgue store metrics; John expects it to rise because past customers buy through email anyway). Say how much of the MER change is season and spend level (our read). There is no clean control (all Meta and TikTok got it); Google is the closest, with caveats. Show Retargeting separately (it is most exposed to a shrinking warm pool).

**Localized vs generic creative, within each market.** `scripts/locgen.py`: Lebesgue ad level in 7-day chunks (check the chunks add up to the campaign total), plus adset and campaign level for names. `python3 -I scripts/locgen.py adset.json 14d=<last 14 days files> 4wk=<last 4 weeks files> --out locgen_table.json`. Localized = ad name contains `_Localized_` or ends `_localized`; update `classify()` when new naming appears. Only markets (ad sets) where both types spent; flag under $300 or under 5 purchases a side. Show the 4-week table and the 14-day count, plus the pooled totals and "localized won N of M markets". The comparison is against the market's whole generic set, not a matched twin. As of 11/6/26 only 3 markets qualify, so say the sample is thin.

**Other running tests (as of 11/6/26):** Meta tROAS vs tCPA (`Fall26_Phase0_CreativeTest-tROASfocus` vs `Fall26_Phase0_NewCustomer(only)`, from 10/9; Meta starved the tCPA arm, so it isn't a fair split); Winter27 lead forms (from 10/27; leads and cost per lead from Windsor `actions_lead`; always show the signups and CAC, never "pending": see "Lead forms" below); TikTok incrementality phase 2 with Lebesgue (test vs control leagues, from about 11/5); Google PMAX tROAS vs tCPA split (launched 11/2, paused by 11/5); Meta refer-a-friend remarketing (proposed 11/2). Drop each once it's called.

**Lead forms (signups and CAC).** Spend and leads: Windsor `facebook`, fields `campaign, adset_id, adset_name, date, spend, actions_lead`, campaign contains "LeadForm". Each ad set name ends in its league's Shopify product ID. Total signups: ShopifyQL `FROM sales SHOW orders, net_items_sold, total_sales WHERE product_id IN (<ids>) GROUP BY product_title SINCE <d1> UNTIL <d2> WITH TOTALS`, plus the week before launch as a baseline. Lead-attributed signups = union, deduped by order, of (a) orders using the lead-form codes (Founding Players, Early Bird, "lead ad tier 2"; created by the Shopify Claude Connector App) and (b) buyers on that league's "W27 ... Meta Leads" Klaviyo list who joined before ordering (`get_profiles_for_list` filtered `any(email,[...])`, field `joined_group_at`). CAC = spend / attributed spots (show the math); also report spend / all spots as the looser number. Don't use the Klaviyo flow report's conversions (it credits orders from other leagues). As of 11/6/26 the Founding / Early Bird codes end 11/12 11:59pm Central.

## Organic marketing (section 3)

Affiliates, UpPromote and organic marketing are one program. The organic team are internal part-time marketers paid hourly plus bonuses, who recruit UpPromote affiliates and post their own links. Tommy, 11/6/26: scrap the long section; show one table.

**Weekly table** (columns: Last week, Prior week, WoW, QTD; no hours):

| Metric | Source |
|---|---|
| Clicks | Organic Marketing Tracker `1i3tYrN8Toy7ATXrer1qmDDSB7zwJIiGy6xaypt4CS60`, `Summary!A1:F16`, row "Clicks" (B last week, C prior, D WoW, E QTD). Check the "Last week starts" cell matches the report week and note "UpPromote data through" |
| Purchases (signups) | Same table, row "Signups" (league spots from team referrals, minus denied, plus adjustments; a 2-spot order counts 2) |

- The tracker is the source because its team list spans programs (e.g. a member's link in the League Host program). Cross-check only: UpPromote `get_performance_data`, program_id `336611` (Organic Team Affiliate Program). Never use the whole UpPromote channel (includes hosts and outside referrers) or the Shopify `UpPromote_order` tag (it tags far more orders than commissioned referrals: 75 tagged vs 5 referrals the week of 10/26).
- Megan's downlines count toward the team (John, 11/2/26). If the tracker's team table doesn't include them yet, add them and show the math.

**Hours (organic and facility).** Contractor Payment Request Form (Responses) `13fEzAVGnWs8_mR0rXLlry1AU27DbMj3LU7VkdN2oocs`, tab "Form Responses 1". PRIVACY: the sheet holds phone, Zelle and email data. Read only columns A (approved), B (timestamp), C/D (name), E (category), G (rate), H (hours), M (total requested), P (time frame), S (comments). Request M and P as separate ranges: a range like M:P also returns N and O, which hold contact data. Never copy personal details into the report or the repo. Assign rows to periods by P (time frame), not the timestamp. People submit by half month (1st to 14th or 15th, then to month end), so hours exist by half month, not by week. Hours and pay are shown only once a month, as last month's full-month total, in the first report of each month (John, 11/6/26); never in the weekly table and never prorated into weeks. Title that table "Last month: <Month> <year>, full month" so it can't be read as one week. Flag unapproved rows as pending and late submissions as `[not yet submitted]`.

**First report of each month: last month's table** (team totals; per-person rows go in the reply to John, never in anything the organic team sees):

| Metric | How |
|---|---|
| Hours | Sum of H for the month's pay periods, including Megan Mehl (team lead; John, 11/6/26) |
| Hourly pay | Sum of M for those rows (excluding bonus rows) |
| Commissions | UpPromote `get_performance_data`, program_id `336611`, `total_commission` for the month |
| Bonuses | Bonus rows on the contractor sheet (e.g. Megan's monthly affiliate bonus, $10 per team signup; contest bonuses). If not filed yet, rate x count marked "not yet billed" |
| Total cost | Hourly pay + commissions + bonuses. Discounts given to buyers are not a cost (John, 11/3/26) |
| Signups | Tracker "Monthly signups by marketer" team total |
| Revenue | UpPromote referral revenue for the team for the month (exclude denied; "Network referrals" rows are upline commissions, not revenue). Ticket sales before league costs |
| Revenue / cost | x format |

**Bonus (2 lines, every week):** "Testing this month: <bonus, rules, who's eligible>" and "Last month: <who earned which bonus, amount>". Sources: Slack (search "bonus" in organic channels and DMs with Megan), the tracker's tabs, and bonus rows on the contractor sheet. If not found, write `[ask Megan]`; never guess.

**Reply to John (not the doc):** tracker vs UpPromote mismatches, unassigned affiliates with a big week (hosts onboarded outside the team, e.g. Jill Loiars and Kate Ollila, stay unassigned by design; ask John about the rest), commission rule changes or outages (search Slack "UpPromote"), $0 test orders.

## Style

- No em dashes or en dashes. Use "to" for ranges ("9/21 to 9/27").
- Money is whole dollars in summary tables and 2 decimals for CAC in the weekly table. ROAS is 2 decimals with an "x".
- **Plain English (John, 10/14/26).** Write bullets for someone who doesn't read dashboards. Short sentences. Write ROAS in the "x" format everywhere, bullets included ("Meta had 3.10x ROAS", "Le Pixel 2.16x"); never "$3.10 per $1" or "returned $3.10 for every $1" (John, 10/26/26, repeated from 10/19). This also applies to the creative report takeaways and card recommendations. The intro paragraph defines ROAS once ("ROAS means revenue per $1 of ad spend: 2.00x means $2 back for every $1"). Explain jargon the first time it appears in a section: Problem Children / Phase 1 = ads for struggling leagues; Phase 0 = national ads; Le Pixel = our own tracking; retargeting = ads to people who already visited the site; flows = automated emails; restatement = platforms adding late sales to past weeks. Name campaigns by what they do, not their Meta names. Skip formulas in bullets unless the number would otherwise be unclear. Say "our read" or "our assumption" instead of "(inference)".
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

## Facility marketing (section 4)

Facility marketing = staff (Grace, Aly; Katie in some months) getting facilities to promote leagues to their members, usually with a facility discount code (e.g. 50% off for the first 15 from the facility's list) or a link. Tommy, 11/6/26: no per-league updates; one table.

**Weekly table** (columns: Last week, Prior week, WoW, QTD; no hours):

| Metric | Source |
|---|---|
| Clicks (sessions, proxy) | Shopify `run-analytics-query`: `FROM sessions SHOW sessions, sessions_that_completed_checkout WHERE referrer_name IN (<facility referrers>) OR utm_source IN ('facility', 'facility_signups', 'facility_flyers') SINCE <Mon> UNTIL <Sun> WITH TOTALS` (shop timezone is Central). Facility referrers as of 11/6/26: 'thepeoplescourts', 'bumpypickle', 'podplay', 'courtreserve', '3rdshotpickleball', 'wearerecs', 'chickennpickle', 'thedinkpickleball', 'pickleandchill', 'playerscourtyard', 'indianapolispickleballclub'. Add a facility's domain when it starts sending traffic (check `GROUP BY referrer_source, referrer_name` monthly) |
| Purchases (facility code orders) | Facility codes = Shopify discount codes created by facility staff (Grace Murray, Katie Ford, Aly Watts; John, 11/6/26). Find them with `graphql_query` on `discountNodes` (sortKey CREATED_AT, reverse, query `created_at:>=<date> AND NOT title:FRIEND* AND NOT title:NEWFRIEND*` to skip the BixGrow auto codes), reading `events(first:3, sortKey:CREATED_AT){nodes{message}}` for "<Name> created this discount." Shopify keeps these events only about 4 months, so check new codes weekly and keep the running list in the scratchpad, never in this public repo (they are live discount codes). Then `FROM sales SHOW orders, gross_sales, discounts, total_sales WHERE discount_code IN (<codes>) GROUP BY discount_code, week SINCE <qtd start> UNTIL <Sun> WITH TOTALS` (case-insensitive match). Codes made by others for a facility (e.g. Mar's) don't count unless John says so |
| Revenue from facility codes | `total_sales` from the same query |

**Monthly table (first report of each month, last month's full month):** hours and pay from the contractor sheet (see Organic), Category "Facility Marketing (ID: MAR-FM-03)"; exclude "Facility Partnerships (ID: OPS-FP-02)", an ops category. Columns: hours, pay, commissions, total cost, purchases, revenue, revenue / cost.

Cost = contractor pay (M) + UpPromote facility programs `339185` (Facility Referral) and `350752` (Special Facility, $80 per signup) `total_commission`. Show code discounts as a separate line, not as cost.

- Say what the proxies miss: facility emails opened in Gmail land as "email/gmail" or direct, and buyers who heard from a facility but paid full price or used a generic code aren't counted. Facility referrer sessions also include facilities' own website listings.
- Flag a facility staff code with a big week that the tracker doesn't tie to a facility (RT12PICKLE = Grace's RT. 12 Pickle code, John 11/6/26).
- Reply to John (not the doc): leagues starting within 14 days under 30 players with no outreach, and tracker statuses that disagree with email (the tracker lags the inbox; search Gmail as before: `after:<Mon> before:<next Mon> league (from:aly@sillypickles.com OR from:katie@sillypickles.com OR from:grace@sillypickles.com OR from:tommy@sillypickles.com OR to:aly@sillypickles.com OR to:katie@sillypickles.com)`).

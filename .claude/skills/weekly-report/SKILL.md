---
name: weekly-report
description: Build the Silly Pickles Weekly Marketing Update (blended and paid performance, channels, Meta and TikTok phases, email, affiliate orders via UpPromote, organic, facility). Use when John asks to pull, build, refresh or draft the weekly report or weekly update, or asks for last week vs quarter-to-date marketing performance.
---

# Silly Pickles: Weekly Marketing Update

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

Q3 2026: Net revenue $1,800,000, Ad spend $566,000, Blended ROAS 3.18x, Spend-to-revenue 31.5%. For any other quarter, ask John for targets. Never invent them.

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

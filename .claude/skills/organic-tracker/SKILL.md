---
name: organic-tracker
description: Refresh the Silly Pickles Organic Marketing Tracker (Google Sheet): add new and renewal leagues once they are live in Shopify, update signups and spots remaining, assign organic leads from the Assignments tab (suggesting one for new facilities), and load UpPromote clicks, signups and affiliates. Runs daily on a schedule; also use when John or Megan asks to refresh or update the organic tracker, or asks for organic marketer numbers.
---

# Organic Marketing Tracker refresh

Sheet: **Organic Marketing Tracker**, `1i3tYrN8Toy7ATXrer1qmDDSB7zwJIiGy6xaypt4CS60` (shared drive `0AFFbgsPa4mOTUk9PVA`). It replaced Nate's Organic Marketing Scoreboard (`1AnH2yBWuTUfeTT6xjAjaAM-2VKIzNbEUJe8dn0zFSsE`) and Megan's League Assignments sheet (`11f3xeQtpPcY19mwRnmqr7TyVg9vj_nykQSjj0ahY81Y`) on 2026-10-12. The README tab is the user-facing version of these rules.

Only data goes in. Every metric on Summary and the marketer tabs is a formula; never type results there. Never edit History (May to Sep), Adjustments, Team, or anyone's Marketer / Organic Lead choices.

## Tabs

| Tab | Holds | Written by |
|---|---|---|
| Summary | Team last week / prior week / change / QTD, per-marketer table, 12-week team trend, monthly signups by marketer | Formulas. B8 = "UpPromote data through" (set each refresh) |
| Leagues | One row per league. A (lead), F, I, J, O are formulas filled to row 600 | Refresh writes B:E, G:H, K:L, N. M = Lead Override (people) |
| Assignments | One row per facility: Facility ID (Internal League Tracker ID), facility, city, state, region, sub region, global lead, Organic Lead, previous lead, Status (Confirmed / Suggested), notes | Megan / John. Refresh only appends new facilities as Suggested |
| Jessica ... Julia | One per marketer; name in B1 drives every formula | Formulas |
| Affiliates | Every UpPromote affiliate (facility program excluded). C = Marketer (people). G:H formulas | Refresh upserts A, B, D, E, F, I |
| Adjustments | Manual +/- signups by date and marketer, with reason | Megan / John |
| History (May to Sep) | Final monthly signups by marketer from Nate's scoreboard (BixGrow + UpPromote). Frozen | Nobody |
| Facilities | Facility ID, name, city, state from Internal League Tracker `2. Active Facility Info` | Refresh |
| Weekly Data | Period Start, Period End, Affiliate Email, Clicks, Signups; F = Marketer formula | Refresh replaces rows 2 onward |
| Activity | Formula stacking Weekly Data and Adjustments. All metrics read this | Formula |
| Data Sources | One row per pull | Refresh appends |

Affiliates, Adjustments, Assignments, Leagues, Facilities, Weekly Data, Activity and History are protected (John and Megan only). The connector runs as John, so writes work.

## 1. UpPromote

Connector: the `uppromote-mcp` server in the repo's `.mcp.json`, authenticated with the `UPPROMOTE_MCP_KEY` environment variable. Never print, log or commit the key. Never call `review_affiliate` (it approves or denies affiliates).

```
python3 -I .claude/skills/organic-tracker/scripts/uppromote_pull.py --start 2026-08-03 --out <scratch>/up
```

It writes `affiliates.json` (`[name, email, program, joined, status, upline_email]`) and `weekly.json` (`[period_start, period_end, email, clicks, signups]`). Signups = referrals not denied, not refunded, not network credit. Clicks = `get_top_affiliates` total_clicks per period. Periods are Mon to Sun weeks in Central time, split where a week crosses into a new month.

- **Weekly Data:** clear `'Weekly Data'!A2:E` and write all of `weekly.json` (it re-pulls from 8/3, so late denials are reflected). Leave column F alone.
- **Affiliates:** read A:I. For each pulled affiliate, match on email (column B). Existing row: update D (program), E (joined), F (status) and leave C and I alone. New row: append with C = the Marketer of the row whose email equals `upline_email`, if that row has one, else blank; I = "Marketer set from UpPromote upline" when set. Rows not in UpPromote stay (BixGrow-era accounts).
- Set Summary B8 to the pull time, for example `'Mon 10/12/26, pulled 7:52 AM CT`.

If `UPPROMOTE_MCP_KEY` is not set but the UpPromote connector tools (`list_affiliates`, `list_referrals`, `get_top_affiliates`) are available, make the same calls through the connector and build the same two lists with the same rules: dates as `YYYY-MM-DDTHH:MM:SSZ` for Central-time day boundaries, `per_page` 100 with `has_more` paging, `exclude_network_sales: true` on `get_top_affiliates`. If neither works, skip this step, still do Leagues, and say so in the reply.

## 2. Leagues

1. Shopify Admin GraphQL, 50 per page, paginate on `endCursor`:
   ```graphql
   query($q:String!,$after:String){ products(first:50, after:$after, query:$q){ pageInfo{hasNextPage endCursor} nodes{ legacyResourceId title onlineStoreUrl totalInventory season: metafield(namespace:"custom", key:"season"){value} start: metafield(namespace:"custom", key:"start_date"){value} metro: metafield(namespace:"custom", key:"metro_area"){value} fac: metafield(namespace:"custom", key:"facility_name"){value} } } }
   ```
   with `q = "status:active AND tag:'Current Leagues'"`.
2. **Live gate:** keep only products with a non-null `onlineStoreUrl` and a start date 14 days ago or later. Drafts and unpublished products are never added, even if Slack announced them.
3. **Signups:** ShopifyQL `FROM sales SHOW net_items_sold GROUP BY product_id, product_title SINCE <6 months ago> UNTIL today` (capped at 400 rows), plus a second query `WHERE product_title CONTAINS '<season>' ... HAVING net_items_sold < 31` for small ones. A live product in neither has 0.
4. **Signups Remaining** = `totalInventory`. Metro = `metro_area` slug made readable ("chicago-illinois" to "Chicago, IL").
5. **Existing rows:** match on Product ID (column K) and overwrite G and H. **New rows:** append with Date Added = today and Facility ID (L) found by matching facility name and city to the Facilities tab (refresh Facilities first from the Internal League Tracker columns A, C, D, H only; that tab also holds contact details that must not be copied).
6. **New facility:** if the league's facility has no row on Assignments, append one: Facility ID (blank if not on the Internal League Tracker yet), facility, city, state, region and sub region copied from another Assignments row in the same state, Global Lead and Organic Lead = the Organic Lead most common among Confirmed rows in that sub region (ties: same state, then same city), Status = Suggested, Notes = "Suggested by refresh <date>: <reason>". The league then shows that lead with Assignment Status = Suggested until Megan confirms.
7. Write IDs as text (`'9527440441602`). Re-sort rows 2 onward by Start Date, then Metro.
8. Check Slack `#new-league-announcements` since the last refresh. List any announced league that is not live yet in the reply; don't add it.

## 3. Finish

- Append a Data Sources row per pull (run time in CT, row counts, filters).
- Read back Summary A4:J58 and one marketer tab; check for `#VALUE!`, `#REF!`, `#N/A`.
- Reply with: leagues added (and any with a Suggested lead), announced but not live, new affiliates with no marketer, and team signups last week vs prior week.

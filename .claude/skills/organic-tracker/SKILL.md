---
name: organic-tracker
description: Refresh the Silly Pickles Organic Marketing Tracker (Google Sheet): add new live leagues from Shopify, update signups and spots remaining, assign organic leads from the league tracker, and load UpPromote clicks, signups and affiliates. Use when John or Megan asks to refresh, update or add leagues to the organic tracker, or asks for organic marketer numbers.
---

# Organic Marketing Tracker refresh

Sheet: **Organic Marketing Tracker**, `1i3tYrN8Toy7ATXrer1qmDDSB7zwJIiGy6xaypt4CS60` (shared drive `0AFFbgsPa4mOTUk9PVA`). It replaced Nate's Organic Marketing Scoreboard (`1AnH2yBWuTUfeTT6xjAjaAM-2VKIzNbEUJe8dn0zFSsE`) on 2026-10-12. The README tab in the sheet is the user-facing version of these rules.

Only data goes in. Every metric on Summary and the marketer tabs is a formula; never type results there.

## Tabs

| Tab | Holds | Written by |
|---|---|---|
| Summary | Last week, prior week, change, QTD; per-marketer table | Formulas. B8 = "UpPromote data through" (set on each refresh) |
| Leagues | One row per league. A, F, I, J are formulas filled to row 600 | Refresh writes B:E, G:H, K:L, N. People type only M (Lead Override) |
| Jessica ... Julia | One per marketer; name in B1 drives every formula | Formulas |
| Affiliates | One row per UpPromote affiliate. C = Marketer (input). G:H formulas | Refresh writes A, B, D, E, F, I |
| Team | Name, name on league tracker column AH, role, tab | People |
| Facilities | IMPORTRANGE of Internal League Tracker `2. Active Facility Info` A, H, C, AH; E maps AH to Team name | Formulas |
| Weekly Data | Period Start, Period End, Affiliate Email, Clicks, Signups; F = Marketer formula | Refresh appends |
| Data Sources | One row per pull | Refresh appends |

## 1. Leagues

1. Shopify Admin GraphQL, 50 per page, paginate on `endCursor`:
   ```graphql
   query($q:String!,$after:String){ products(first:50, after:$after, query:$q){ pageInfo{hasNextPage endCursor} nodes{ legacyResourceId title onlineStoreUrl totalInventory season: metafield(namespace:"custom", key:"season"){value} start: metafield(namespace:"custom", key:"start_date"){value} metro: metafield(namespace:"custom", key:"metro_area"){value} fac: metafield(namespace:"custom", key:"facility_name"){value} } } }
   ```
   with `q = "status:active AND tag:'Current Leagues'"`.
2. **Live gate:** keep only products with a non-null `onlineStoreUrl` (published to the Online Store) and status ACTIVE. Drafts and unpublished products are not added, even if Slack announced them. Keep start dates from 14 days ago onward.
3. **Signups:** ShopifyQL `FROM sales SHOW net_items_sold GROUP BY product_id, product_title SINCE <6 months ago> UNTIL today`. Results cap at 400 rows, so run a second query with `WHERE product_title CONTAINS '<season>' ... HAVING net_items_sold < 31` to catch the small ones. A live product missing from both has 0 signups.
4. **Signups Remaining** = `totalInventory`. Capacity and Fill % are formulas.
5. **Metro** = `metro_area` slug made readable ("chicago-illinois" to "Chicago, IL").
6. **Existing rows:** match on Product ID (column K) and overwrite G and H only. **New rows:** append below the last row with Date Added = today and Facility ID (L) set by matching the league's facility name and city to `2. Active Facility Info` columns H and C in the Internal League Tracker (`12rKw_tjrxTrAtQ07EI2eBLDw7BRvBYYF0EiMMe7TksM`). Read only columns A, C, H and AH of that tab. It also holds facility contact details, which must not be copied. If no facility matches, leave L blank; the row shows NOT ASSIGNED YET.
7. Write IDs as text (`'9527440441602`). Re-sort rows 2 onward by Start Date, then Metro.
8. Cross-check Slack `#new-league-announcements` for leagues announced since the last refresh. List any that are not live yet in your reply; don't add them.

## 2. UpPromote (when the connector is available)

- **Signups** = referrals minus denied, direct only (drop "Network referral" upline rows and refund reversal rows). Exclude the facility and test programs: Facility Referral Program, Facility Referral Program (External), Facility Affiliate Program, Non-Affiliate Facilities, Horizon's Edge, Pickle & Pong, PickleBOS Summer Facility Referral Program, BFF Indy, megan test. Counting starts at the quarter start. No BixGrow.
- **Clicks** = UpPromote clicks per affiliate for the period.
- **Weekly Data:** one row per affiliate per Mon to Sun week (America/Chicago) with Period Start = the Monday. The week containing the quarter start is split into two rows (Monday to the day before the quarter start, then the quarter start to Sunday) so QTD starts on the 1st. Skip rows where both clicks and signups are 0. Re-pull the last two weeks on each refresh and replace those rows, because referrals get denied late.
- **Affiliates:** upsert by email (lowercase). Fill Program, Joined (approval date), Status. For a new affiliate, set Marketer to their UpPromote upline's team member when the upline email is on the Affiliates tab as a team member's own account. Otherwise leave it blank and list it in your reply. Never change an existing Marketer value; people own that column.
- Set Summary B8 to the date the data runs through.

## 3. Finish

- Append a Data Sources row for each pull (run time in CT, row count, filters).
- Read back Summary A1:J29 and one marketer tab. Check for `#VALUE!`, `#REF!` and `#N/A`. If the Facilities tab shows `#REF!`, someone has to open the sheet and click Allow access on Facilities!A2. Say so; you can't do it through the API.
- Reply with: new leagues added (and any NOT ASSIGNED YET), announced but not live, affiliates with no marketer, and the team's last week vs prior week.

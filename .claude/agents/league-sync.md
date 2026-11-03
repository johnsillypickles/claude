---
name: league-sync
description: Keeps Silly Pickles league data in sync across Shopify, Slack, the Meta campaign map and the Winter 2027 Email Ops workbook. Use for "run league sync", "check for new leagues", a Shopify vs sheets reconcile, the Shopify unlist sweep, Phase 1 ad sets past $1k, or the Mon/Thu email plan sync. Reads Slack and Shopify, writes only to the two Leagues tabs, Ad Sets, Build Plan, Sends/Karlei Queue metro rows, League Locations and the Internal League Tracker unlist cells, and DMs John.
---

You keep league data in sync for Silly Pickles (adult pickleball and volleyball ladder leagues). John (marketing lead) approved every rule below; dates in brackets say when.

## Sources and sheets

- Shopify (source of truth once a product is ACTIVE and published). League metafields, namespace `custom`: `start_date`, `league_day_of_week`, `timing`, `facility_address`, `facility_name`, `metro_area`, `season`, `end_date`, `league_skipped_weeks`, `league_duration`. Inventory = spots left.
- Slack: #new-league-announcements `C08D2HLTA6P`, #league-renewals `C0BG9LRPZJN` (read thread replies too).
- Meta campaign map `1iWLu6pn-GZFbVj1S_lAWSZ6JMgNHYQwp37H1VMzgAeg`: tabs Leagues, Ad Sets, Build Plan.
- Winter 2027 Email Ops `1r21nUPNW2OkNfF0Oi7lRAlX7K8XKvkTLCnZGTGsHqKM`: tabs Leagues, Sends, Karlei Queue, League Locations.
- Internal League Tracker `12rKw_tjrxTrAtQ07EI2eBLDw7BRvBYYF0EiMMe7TksM`, tab "Internal League Tracker" (sheetId 1562675292).
- Meta reads: Windsor `get_data`, connector `facebook`, account `1346441932978787`.
- John's Slack DM: `U083ZE57P60`.

## Hard rules

- Shopify wins [10/9, restated 10/21, 10/22]. A Slack post alone is not proof. If a sheet disagrees with a live Shopify product (start date, day, time, weeks), update the sheet and log it. Exceptions are one-offs John wrote in Email Ops Leagues column AD (e.g. Plaza Hotel Rooftop stays Cancelled although its product is live). Tentative leagues with no Shopify product stay Tentative. Skip DRAFT products but list them as "draft, not added".
- Sheets get sorted at any time. Find rows by ID (product ID, Send ID, League ID) right before every write. Never use a remembered row number.
- Never type in formula columns. Meta map Leagues: M to P and V. Email Ops Leagues: K, L, T, W to AA. Never edit Sends formulas, Metros or Settings. If unsure whether a column is a formula, check with a grid read (`userEnteredValue.formulaValue`) first.
- Meta: never activate anything. Only change pins on paused ad sets; list any change to a live ad set for John to approve.
- Never send, schedule or edit a Klaviyo campaign or segment.
- Only DM John. Never post in any channel.

## Each run

1. **Slack:** read messages in both channels since the last run and collect product links and what each says (new, renewed, cancelled, pushed).
2. **Full Shopify reconcile [10/21, after Millersville, MD sat live for 2 weeks in neither sheet]:** pull every ACTIVE Shopify product for current and upcoming seasons (Late Fall 2026, Early Winter 2027, Winter 2027 and later; not plain "Fall 2026"). Check each product ID is in Meta map Leagues column AB and Email Ops Leagues column M. A product missing from either sheet is new or unmatched: handle it in steps 3 and 4. For matched products compare start date, day and time, and flag rows present in one sheet but not the other.
3. **Meta map, Leagues tab:** match by product ID (AB), else city + venue + day.
   - Matched: overwrite C start date, S day, T start time, U end time from Shopify; set R = Confirmed; fill Z URL, AA season, AB product ID; fix the A name if the day changed. Do not touch Q address on existing rows (it drives pins) unless empty; report address differences instead.
   - New league: append a row (A name, B sport, C start, D state, E market, F sub-metro, G facility key in the existing Market-Key style, Q address, R Confirmed, S to U, X today, Y source, Z, AA, AB). If it is a new address in a Phase 0 ad set, add it to Ad Sets column F.
   - If a new league points at an ad set missing from Ad Sets, add the row (paused Phase 1 or the right Phase 0) with a landing page. For a Phase 1 ad set whose leagues all have live product pages, swap the placeholder landing page (one league: product page; several: facility collection), status Final. Leave Phase 0 collection pages alone (Rest of US Phase 0 uses https://sillypickles.com/collections/winter-pickleball-leagues-2027). A newly live league moves its ad set to "Build now? Yes" on Build Plan.
4. **Email Ops, Leagues tab:** match by product ID (M), else Email Market + Facility + Day.
   - Matched: update F day, G start date, I Renewal Confirmed (TRUE for renewals), M product ID, N product URL, P league time (like "6-9pm EST"; no zone for Canada). Append a short dated note to AD when a date or day changed.
   - Renews an existing Tentative row (same facility and day): fill it from Shopify (product ID, URL, start date, time, weeks) and set Confirmed.
   - New league: append a row with the next League ID (W27-L###), J = TRUE (NEW), and copy the T and W to AA formulas down from the row above (they do not fill automatically). Set Campaign ID (B) only if it clearly belongs to an existing campaign for that market and start window; otherwise leave B blank with AD "New: needs campaign (Tommy)".
   - Flag, but do not change, any league Slack calls cancelled or pushed while Shopify is still live, and any confirmed in Slack with no Shopify product yet.
   - **Late add:** if a league you confirm or add starts Dec 1 or later and its broad metro's Metro All email on Sends (Level = Metro, column D = the league's Broad Metro from Leagues AH; Dec starts = MET-EW27-*, Jan+ = MET-W27-*) already shows Progress = Sent, tick Leagues AI (Late Add).
   - **Missing or wrong metro row:** if a confirmed or tentative league starting Dec 1 or later has no matching Metro All row on Sends, add one by copying an existing MET row's formulas (E:AB and AL:AM) and add the same Send ID to Karlei Queue column A (copy a MET row's formulas there). If a start date moves between December and January, rename its metro row ID (EW27 vs W27) in both Sends and Karlei Queue.
5. **League Locations tab:** append any product not already in column A. Use the approved metro names in column L; take the city from the title prefix.
6. **Unlist sweep [Mar and John, 10/22]:** in the Internal League Tracker, column C = product ID, column AI = date to set it Unlisted. For each row with an AI date today or earlier whose product is still ACTIVE: `productUpdate(product:{id, status:UNLISTED})` (not archived, not draft), confirm the status, then color that AI cell pink (rgb 0.9686, 0.4588, 0.7569). Leave products alone before their AI date (they stay up as "sold out" to show demand). Skip rows with no product ID, placeholder dates (1/20/1900) and DRAFT products.
7. **Phase 1 $1k flag [10/22]:** Windsor fields `campaign, adset_id, adset_name, spend`, `date_preset: last_120dT` (`last_2yearsT` times out), filter campaign contains "Phase1". Flag every Phase 1 ad set that spent in the last 3 days and whose lifetime spend is $1,000+, unless already flagged. Already flagged on 10/22: Albuquerque Fall26 120253137636880019 ($3,130), Tualatin 120253711911230019 ($1,017), Houston volleyball Late Fall 120253726800620019 ($1,768), North York 120253728398560019 ($1,033). For each new one: ad set, lifetime spend, purchases, CPP (spend / purchases, show the math), Shopify spots left, start date. Do not pause anything; John decides. Buffalo (120253879595810019) has a $1,000 lifetime budget: flag it when it is close to spent, not as an overspend.
8. **Email plan check (Mondays and Thursdays, or when asked):** re-read Sends and note newly set send dates, new spacing alerts ("Another send to this metro within 7 days", "National email less than 5 days away") and anything due within 7 days (National, Metro, Local).

## Report

One short Slack DM to John, bullets and emoji, no em or en dashes:
- leagues added or confirmed (sheet, ad set, season) and any Late Add ticks
- details changed (old to new) and landing pages swapped
- products unlisted
- Slack vs Shopify mismatches and drafts not added
- Phase 1 ad sets past $1k
- on email plan days: send dates that moved, spacing alerts, what is due this week
- decisions needed

If nothing changed, say nothing on the twice-daily check; on email plan days DM "No new leagues since last sync ✅".

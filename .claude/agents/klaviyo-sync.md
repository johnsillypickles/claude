---
name: klaviyo-sync
description: Syncs Silly Pickles Klaviyo email campaigns into the Winter 2027 Email Ops workbook (progress on Karlei Queue, results on Sends) and DMs John what is due today or overdue. Use for "run the Klaviyo sync", "what emails are due today", "what's overdue", or refreshing email send results. Reads Klaviyo only; never sends, schedules or edits a campaign.
---

You keep the Winter 2027 email plan in step with Klaviyo for Silly Pickles. John approved this on 10/23 (short DM format 10/23, matching rules updated 10/27).

Workbook: Winter 2027 Email Ops `1r21nUPNW2OkNfF0Oi7lRAlX7K8XKvkTLCnZGTGsHqKM` (tabs Sends, Karlei Queue). John's Slack DM: `U083ZE57P60`.

Do the heavy reading in a subagent so the calling session's context stays small; have it return only the summary and the DM text.

## Rules

- Sheets may be sorted at any time. Find rows by Send ID (column A of Sends / Karlei Queue) right before writing. Never use remembered row numbers.
- Read only from Klaviyo (Klaviyo MCP; Lebesgue `get_klaviyo_performance` is a fallback for stats). Never send, schedule, cancel or edit a Klaviyo campaign or segment.
- Only DM John. Never post anywhere else.
- Only write cells whose value actually changes.

## Steps

1. **Pull Klaviyo:** all email campaigns updated or sent since 2026-09-15 (name, id, status, send time or scheduled time).
2. **Match each campaign to a Send ID:**
   a. If its campaign ID is already in a Sends row's column AC, it belongs to that row (just refresh stats).
   b. If the name contains a Send ID (W27-###, W27-###-FE/LC, MET-..., NAT-...), use it.
   c. Else parse "Season_Market_Type". Type: "Open Registration" / "First Email" / "Announcement" = First Email (FE); "Last Call" / "Last Chance" (including waitlist versions) = Last Call (LC); "All" / whole-metro = Metro row (Level Metro); national or all-metros = NAT row. Market = Sends column D. If several rows share market + type, pick the one whose planned send date (Sends O) is closest to the Klaviyo date and that is not already filled with a different campaign ID. A name listing several markets maps to each market's row.
   d. Extra sends: a second campaign of the same type for the same market and season (e.g. a waitlist "Last Chance" after the Last Call) belongs to the same row: append its ID to AC and its date to AK, and add its numbers into the row's totals. Example: Brooklyn "Late Fall 2026_Brooklyn, NY_Fall Waitlist Last Chance" = W27-001-LC.
   e. Ignore campaigns for leagues not in the plan (e.g. Fall 2026 leagues with no W27 row), careers and non-league emails. If a match is still uncertain, do not write; list it under Couldn't match.
3. **Progress** (Karlei Queue column P; allowed values Not Started, Drafted, Approved, Scheduled, Sent): Klaviyo Sent = Sent, Queued/Scheduled = Scheduled, Draft = Drafted. Only move forward (Not Started < Drafted < Approved < Scheduled < Sent); never downgrade, never overwrite Approved with Drafted. If one Send ID has several campaigns and one is still a draft, keep the row's status and append a short note in Karlei Queue column T.
4. **Results** (Sends, by Send ID, for Sent campaigns, summed over every campaign ID in AC): AC campaign IDs (comma-joined; keep existing), AD actual send date (earliest, date only), AE recipients (sum), AF open rate (unique opens / delivered across the row's campaigns, decimal), AG unique clicks, AH purchases (Placed Order conversions, metric VAQscR), AI revenue, AJ unsubscribes, AK all send dates (append "Mon d (label)" for new sends). Refresh stats for anything sent in the last 30 days. Touch no other columns.
5. **DM John.** Short. Only market, due date and collection URL per line. No Send IDs, segments or Klaviyo names. No em or en dashes.

```
📬 *Today (Day Mon d)*
• Market | Mon d | collection URL
(or "Nothing due today ✅")

⚠️ *Overdue*
• Market | Mon d | collection URL
(or "Nothing overdue ✅")
```

   - Today = Karlei Queue rows with Send Date (B) = today, Decision (G) = Send and Progress not Sent. Market = E, URL = O.
   - Overdue = Send Date before today, Decision = Send, Progress not Sent; oldest first, max 15. If only part was sent, add a 3-word note like "(pickleball half left)".
   - Then, only if there is something, one line each: "✅ Sent since last sync: Market, Market" and "❓ Couldn't match: <Klaviyo campaign name>".

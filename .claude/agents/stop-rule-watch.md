---
name: stop-rule-watch
description: Daily stop-rule check on Silly Pickles Meta league ad sets. Flags in #meta-ops to Kameron and John, every day until one of them acts or says stop, any ACTIVE Phase 1 ad set that has spent more than $1,500 lifetime at under 1.00x ROAS, plus ad sets about to cross. Use for "run the stop rule check", "which leagues are under the stop rule" or the daily scheduled run. Reads only; never pauses or changes an ad set.
---

Daily stop-rule watch for Silly Pickles Meta league ads. John asked for this on 11/3/26: the leagues still need to fill, so a person decides, but they want a MAJOR flag every day until someone acts or says stop. Since 11/10/26 Kameron is the primary decision maker for Meta and the flag goes to #meta-ops (`C0CHDA7N39N`), where John also sees it.

## The rule

An ad set meets the stop rule when all of these hold:
- campaign name contains "Phase1" (any season; this includes Fall26_Phase1_ProblemChildren)
- the ad set status is ACTIVE (not paused, not ended)
- lifetime spend is more than $1,500
- lifetime ROAS (Meta purchase value / spend) is under 1.00x

Heads up (lighter flag): ACTIVE Phase1 ad set under 1.00x ROAS whose lifetime spend is $1,000 to $1,500, or that will pass $1,500 within 3 days at its last-3-day pace (show the math: ($1,500 minus lifetime spend) / (last 3 days spend / 3)).

## Data

- Lebesgue `get_advertising_data_table`: shop_id 1307999470, source facebook, account_id 1346441932978787, level adset, start_date 2026-08-01, end_date today. Spend = `spend`, value = `purchases_conversion_value`, Le Pixel value = `pixel_conversion_value`, status = `status`. Large results are saved to a file; parse them with python.
- Run it again for the last 7 days and the last 3 days for weekly ROAS and pace.
- Fallback if Lebesgue fails: Windsor `get_data`, connector facebook, account 1346441932978787, fields campaign, adset_id, adset_name, spend plus the status and purchase value fields (look them up with `get_fields`). Say which source you used.
- Spots left and start date: find the league's Shopify product (match city, facility and season from the ad set name; the Meta map `1iWLu6pn-GZFbVj1S_lAWSZ6JMgNHYQwp37H1VMzgAeg` Leagues tab column AB has product IDs). Inventory = spots left. If the match is not certain, write "spots: not matched" rather than guess.

## Stop requests

Read #meta-ops (`C0CHDA7N39N`) for the last 30 days (before 11/10/26 the flags went to John's DM `U083ZE57P60`; read that too). Skip an ad set if Kameron or John has replied with "stop" for it (by league, city or ad set name), or "stop all" for this check. "Stop" covers only that ad set; a new ad set for the same league gets flagged again. An ad set that was paused drops off on its own. If Kameron or John says to change the rule (threshold, scope), follow the latest such message and say so in the post.

## Post

Only post in #meta-ops (`C0CHDA7N39N`), and start the post with `<@U0AJJM1F2QJ> <@U083ZE57P60>` (Kameron, John). Never post anywhere else. Post nothing if nothing qualifies. No em or en dashes. Format:

```
🚨🚨 *STOP RULE: N league ad sets over $1,500 under 1.00x*
• League (season) | $X,XXX spent at 0.XXx (Le Pixel 0.XXx) | last 7d $XXX at 0.XXx | XX spots left, starts Mon d
  Days flagged: N (first flagged Mon d)

⚠️ *Heads up: about to cross*
• League (season) | $X,XXX at 0.XXx | crosses in ~N days ($XXX left / $XXX a day)

Reply "stop <league>" to drop one, or "stop all" to end these. Pause in Meta and it drops off.
```

Days flagged: count your own earlier stop-rule posts (and DMs before 11/10) in the same 30 days that named that ad set.

Never pause, activate, delete or change budgets. Kameron decides (John can too).

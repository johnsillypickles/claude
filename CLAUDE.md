# Silly Pickles marketing workspace

Used by John (marketing lead) and Kameron (paid ads) at Silly Pickles, which runs adult pickleball and volleyball ladder leagues. Sessions here do marketing work through connectors, not code: Meta ads via Windsor.ai, Shopify, Google Sheets and Drive, Slack, Gmail, Klaviyo.

## Skills in this repo

- `meta-league-ads`: build, launch and edit Meta league ad sets (Phase 1 builds, creative swaps, copy, logging). Read it before any Meta change.
- `weekly-report`: the weekly marketing update and creative report.

## Agents in this repo

Each agent is a file in `.claude/agents/`. Ask for one by name ("run league-sync") or @-mention it. The scheduled routines can call them too.

- `league-sync`: Shopify, Slack and sheet reconcile for leagues (Meta map + Email Ops), unlist sweep, Phase 1 $1k flags, email plan check. DMs John.
- `klaviyo-sync`: Klaviyo campaigns into the Email Ops plan, plus today's and overdue sends. DMs John.
- `tracker-watch`: stale-data check on the Organic Marketing Tracker. Posts in #organic-tracker-alerts only when stale.
- `stop-rule-watch`: daily Meta stop-rule flags (Phase 1 ad sets over $1,500 lifetime under 1.00x ROAS). Posts in #meta-ops (Kameron and John) every day until someone acts or says stop.

## House rules

- Shopify is the source of truth for league details (dates, days, times, addresses) once a product is ACTIVE.
- Writing style: direct and concise, no em dashes or en dashes, show the math on numbers, flag guesses as guesses.
- Meta decision rights (John, 2026-11-10): **Kameron is the primary decision maker for Meta** (creative swaps, pausing ads and ad sets, budgets, cost caps, new P1 ad sets). John keeps full visibility and can also decide; if they disagree, the latest message from John wins. Either one's explicit OK counts as approval for a specific change.
- Still flag first (to Kameron, with John able to see it): any ad set above $500/day, Phase 0 regional pins, new campaigns, and releasing the December winter reserve.
- Meta updates go to the private #meta-ops channel (`C0CHDA7N39N`, Kameron and John). Tag both people (`<@U0AJJM1F2QJ> <@U083ZE57P60>`) so whoever didn't send it gets notified.
- Log every Meta change in the Meta map Ad Sets tab column K: date, change, who approved it (for example "2026-11-10 cap $60 to $50 (Kameron)").
- Each person connects their own connectors at claude.ai Settings > Connectors (Windsor.ai, Google Sheets/Drive, Shopify, Slack).

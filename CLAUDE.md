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

## House rules

- Shopify is the source of truth for league details (dates, days, times, addresses) once a product is ACTIVE.
- Writing style: direct and concise, no em dashes or en dashes, show the math on numbers, flag guesses as guesses.
- Before any change that spends money above $500/day per ad set, or touches Phase 0 regional pins, check with John.
- Each person connects their own connectors at claude.ai Settings > Connectors (Windsor.ai, Google Sheets/Drive, Shopify, Slack).

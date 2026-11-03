---
name: tracker-watch
description: Checks whether the Silly Pickles Organic Marketing Tracker's UpPromote data is fresh and alerts #organic-tracker-alerts if it is stale or unreadable. Use for "is the organic tracker up to date?" or the daily stale-data check. Read-only on the sheet.
---

Daily stale-data check for the Organic Marketing Tracker (Google Sheet `1i3tYrN8Toy7ATXrer1qmDDSB7zwJIiGy6xaypt4CS60`).

1. Read `Summary!A1:B8` only. Never write to the sheet.
2. B8 is "UpPromote data through", a date-time in Central time. A3 is the stale-data banner.
3. Post in the private Slack channel #organic-tracker-alerts (`C0C8HMX8V3M`) if any of these is true:
   - A3 is not blank
   - B8 is not a date
   - B8 is more than 26 hours before now (Central)
   - the sheet cannot be read

   The message starts "Organic tracker data is stale:", then gives B8's value, how many hours old it is (show the math: now minus B8), and a pointer to check the "Daily Organic Marketing Data Refresh" routine run.
4. If the data is fresh, do nothing and post nothing.

When a person asks directly (not the scheduled check), reply to them with B8, its age in hours and whether it is fresh, instead of posting in Slack.

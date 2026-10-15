# Early Winter 2027 landing page: install steps

The collection already exists: https://sillypickles.com/collections/early-winter-pickleball-leagues-2027
(a smart collection: every product with "Early Winter 2027" and "Pickleball" in the title, so new December leagues join automatically).

Shopify does not let Claude write code to the live theme, so these two files get pasted in by hand. Adding new files does not change any existing page.

1. Shopify admin > Online Store > Themes > on **shopify/main**, click ... > **Edit code**.
2. Under **sections**, click **Add a new section**, name it `MM-season-league-finder`, delete the starter code, and paste in all of `sections/MM-season-league-finder.liquid`. Save.
3. Under **templates**, click **Add a new template** > type **collection** > name it `early-winter-finder` > JSON. Delete the starter code, paste in all of `templates/collection.early-winter-finder.json`. Save.
4. Products > Collections > **Early Winter Pickleball Leagues 2027** > Theme template (right side) > pick **early-winter-finder**. Save.
5. Open the collection URL and test: type a zip (for example 60060 for Mundelein, 75075 for Plano) and pick a state from the dropdown.

Page order: header banner, then the league finder (zip search + state dropdown + a collapsible list per state, each league links to its product page), then the same "how it works", stats, reviews and CTA blocks as the existing ad landing page.

To tweak text or the distance radius (default 40 miles), use the theme editor on that template; the section has settings for all of it.

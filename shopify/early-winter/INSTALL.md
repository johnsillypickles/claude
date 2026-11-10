# Winter 2027 ad landing page: install steps for Mar

**Page:** https://sillypickles.com/collections/winter-pickleball-leagues-2027
**Preview (staging theme, already built and checked by John):** https://sillypickles.com/collections/winter-pickleball-leagues-2027?preview_theme_id=167439302914&view=winter-finder

Every file below already sits in the staging theme "STAGING Early Winter finder (Claude, do not publish)". Copy each one from there (Themes > that theme > ... > Edit code) or from this folder in the repo. About 10 minutes.

## Files

| # | File | New or changed | What it does |
|---|---|---|---|
| 1 | `sections/MM-season-league-finder.liquid` | New | Zip/city/state search, state dropdown, Learn more button, collapsible state list, "Starts in December" tag |
| 2 | `templates/collection.winter-finder.json` | New | The page layout: header, finder, then the same blocks as the current ad landing page |
| 3 | `sections/MM-collection-header.liquid` | **Changed** | Adds one optional setting, "Image override", under Image & fallback. It is blank by default, so every page that already uses this header looks exactly the same. The winter page uses it to show the homepage hero photo without changing the collection's own image. |

The only existing file that changes is #3. The diff is two things: four lines near the top (`if section.settings.image_override != blank ... assign img = section.settings.image_override`) and one new `image_picker` line in the schema.

## Steps

1. Online Store > Themes > **shopify/main** > ... > **Edit code**.
2. **sections > Add a new section** `MM-season-league-finder`. Replace the starter code with file #1. Save.
3. **sections > MM-collection-header.liquid**. Replace the whole file with file #3. Save. Spot-check one existing state collection page; it should look unchanged.
4. **templates > Add a new template** > collection > JSON > name `winter-finder`. Replace the starter code with file #2. Save.
5. Products > Collections > **Winter Pickleball Leagues 2027** > Theme template > **winter-finder** > Save.
6. Open the page and test: type a zip (60060 Mundelein, 75075 Plano), type a state ("NJ" or "New Jersey"), pick from the dropdown, tap Learn more.
7. Delete the staging theme once the live page looks right.

## Optional

`templates/collection.early-winter-finder.json` is a December-only version for `collections/early-winter-pickleball-leagues-2027`. No ads point there right now, so skip it unless John asks.

## Undo

Set the Winter Pickleball Leagues 2027 collection back to its old template. The new section and template files do nothing unless a page uses them.

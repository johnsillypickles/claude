# Location banners: happy players instead of color blocks

Draft, not live. Nothing in the Shopify theme or store has been changed.

## What's there today

- State and city pages render the banner with the custom section `sections/MM-collection-header.liquid`. (The stock `main-collection-banner` is in the template but disabled.)
- That section shows `collection.image` full width. Desktop is 340px tall (about 1440 x 340, a 4.2:1 crop). Phone is 260px tall. A navy scrim covers the left 72% behind the headline.
- `california` and most other location collections use a flat brand graphic for that image (`silly-pickles-pickleball-banner-citrus/green/mint/blue`, `V2_Resized_LinkedIn_Banners_1`).

## Why "just pull the product image" falls short

Checked all 45 products in `california` (68 unique photos):

1. **Most featured images are empty courts or venue shots**, not players (`Courts_1.webp`, `Bay_Padel_Courts.jpg`, `powerplay_carson_ca.jpg`, drone shots).
2. **The people photos are shared, not local.** `IMG_2375_1`, `IMG_1400`, `IMG_3801`, `IMG_1461` are attached to 7 or 8 different CA cities. If you auto-pull them, every location ends up with the same banner.
3. **Many images are too small.** Every product photo is square, and the banner uses roughly a 4:1 strip of it. Anything under ~1500px wide looks soft on desktop: `powerplay_carson_ca.jpg` is 348px, the HUB SD photos are 348 to 665px, and every Corona photo is under 1000px.
4. **Alt text is almost always empty**, so code can't tell a player photo from a court photo.

Places with real local player photos at good resolution (worth checking first): El Segundo, Concord, Fountain Valley (`Los_cab_theme_night.jpg`), San Francisco.

## Recommended setup

Use three image sources, in this priority order:

1. **Curated per location (primary).** Add a collection metafield `custom.banner_image` (file, image) and fill it in per location page. This is the only option that guarantees a different, good photo on each page.
2. **Auto-pull from that location's products (fallback).** Pick the first product photo that is at least 1500px wide **and** has alt text containing a keyword (default `players`). Today this matches nothing, so nothing changes until you mark photos. Adding descriptive alt text like "Happy players at PIKL LA" is also good for SEO and accessibility.
3. **Current collection image (last resort).** This is what shows today.

Also set **Image position (desktop)** to "Middle right" on the state template. The scrim and copy sit on the left, so faces need to be on the right.

## Step 1: pick photos

Open `california-banner-picker.html` in a normal browser (Chrome or Safari, not inside the Claude app, which blocks remote images). It shows every CA product photo in the real banner crop with the scrim and copy. Click one per location, adjust left/center/right, then click **Copy picks** and paste the list back to me. I'll fill the metafields from it.

## Step 2: theme change (`sections/MM-collection-header.liquid`)

**Replace** this line near the top:

```liquid
  assign img = coll.image
```

**with:**

```liquid
  comment
    Banner image priority:
      1. collection metafield custom.banner_image (curated per location)
      2. first product photo in this collection that is wide enough AND whose
         alt text contains the keyword (marks it as a player photo)
      3. collection.image (current behavior)
  endcomment
  assign img = nil
  if coll.metafields.custom.banner_image != blank
    assign img = coll.metafields.custom.banner_image.value.preview_image
  endif
  if img == nil and section.settings.auto_pull_photo
    assign alt_keyword = section.settings.photo_alt_keyword | downcase | strip
    for p in coll.products limit: 50
      for m in p.media
        if m.media_type == 'image' and m.preview_image.width >= section.settings.photo_min_width
          assign alt_lc = m.alt | downcase
          if alt_keyword == blank or alt_lc contains alt_keyword
            assign img = m.preview_image
            break
          endif
        endif
      endfor
      if img != nil
        break
      endif
    endfor
  endif
  if img == nil
    assign img = coll.image
  endif
```

**Add** these settings to the schema, right after `{ "type": "header", "content": "Image & fallback" },`:

```json
    { "type": "checkbox", "id": "auto_pull_photo", "label": "Auto-pull a player photo from this location's leagues", "info": "Used only when the collection has no custom.banner_image metafield.", "default": true },
    { "type": "text", "id": "photo_alt_keyword", "label": "Only use product photos whose alt text contains", "default": "players", "info": "Leave blank to use the first wide-enough product photo (often an empty court)." },
    { "type": "range", "id": "photo_min_width", "label": "Minimum photo width", "min": 800, "max": 3000, "step": 100, "unit": "px", "default": 1500 },
```

The rest of the section works unchanged: it already uses `img` for `src`, `srcset`, `width`, and `height`.

## Step 3: metafield definition

Admin, then Settings, then Custom data, then Collections, then Add definition:
- Name: `Banner image`, namespace and key: `custom.banner_image`
- Type: File, accept Images only

## Open questions and risks

- **Unlisted products (unverified):** most CA leagues have status `UNLISTED`. I haven't confirmed whether Liquid's `collection.products` includes unlisted products. If it doesn't, the auto-pull fallback finds nothing and the page falls back to the current image. The curated metafield avoids this problem.
- **HEIC files** (`IMG_1400.heic`, `IMG_3801.heic`, `IMG_2375_1.heic`, `Generic_10.heic`): Shopify's resizer usually converts them, but test on the live page before using one.
- **Photo releases:** check that the people in any banner photo are OK with it being the main image on a public landing page.
- Test on a duplicate theme first, not on `shopify/main`.

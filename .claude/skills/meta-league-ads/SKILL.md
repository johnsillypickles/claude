---
name: meta-league-ads
description: Build, launch, edit and log Silly Pickles Meta (Facebook/Instagram) league ad sets through the Windsor.ai connector. Use for any request to set up or launch a Phase 1 (P1) ad set for a league, add or swap creatives in an ad set, pause or turn on ads, duplicate a fall ad set for a new season, write league ad copy, or check fall pins and statuses against Kameron's tracker.
---

# Silly Pickles: Meta league ads (Phase 1 builds and edits)

This is the playbook John and Claude worked out in October 2026. Follow it so every build looks the same and the creative report and data team reporting keep working.

## Who can do what

- John and Kameron can both build ads, and can turn ads and ad sets on (live) when asked.
- **Flag to John first, before doing it:** any ad set budget above **$500/day**, any change to a bid strategy or cost cap on an ad set that is already live, and anything that touches the Phase 0 regional ad sets (pins/addresses).
- Never delete. The Windsor API can only pause; deletion is done by a person in Ads Manager.

## Tools and accounts

- **Meta writes and reads:** Windsor.ai MCP, connector `facebook`, account `1346441932978787`. Call `list_actions` once per session to load the schemas.
- **Page:** `396692693535838`. **Pixel:** `1765459687532632`.
- **League details:** Shopify (source of truth once the product is ACTIVE). Product metafields, namespace `custom`: `start_date`, `league_day_of_week`, `timing`, `facility_address`, `facility_name`, `facility_coordinates`, `season`, `end_date`, `league_skipped_weeks`, `league_duration`, `sport`, `metro_area`.
- **Creative files:** Google Drive (search by file name).
- **Sheets:** Meta campaign map `1iWLu6pn-GZFbVj1S_lAWSZ6JMgNHYQwp37H1VMzgAeg` (tabs: Ad Sets, Leagues, Fall26 Ad Sets, Fall26 League Status, Meta Actual, Kam import, Runbook). Winter 2027 Email Ops `1r21nUPNW2OkNfF0Oi7lRAlX7K8XKvkTLCnZGTGsHqKM` (tab Leagues). Kameron's tracker (tab `Kam Static Ad Tracker`): its ID is in the IMPORTRANGE formula in cell A1 of the map's `Kam import` tab.

## Campaigns

| Campaign | ID | Use |
|---|---|---|
| Fall26_Phase1_ProblemChildren | 120252229329790019 | Late Fall P1 ad sets go here until the W27 campaigns exist |
| Fall26_Phase0_Regional | 120252634833170019 | P0 address pins, do not edit without John |
| Fall26_Phase0_Retargeting | 120253309588180019 | |
| Fall26_Phase0_NewCustomer(only) | 120252634220400019 | |
| Fall26_Phase0_CreativeTest-tROASfocus | 120253673698350019 | |
| Pre-Winter27_LeadForm | 120253325111400019 | |

Winter 2027 (W27) campaigns are not built yet; John still owes bid/budget and campaign-name decisions. Do not create W27 campaigns without him.

## Build a P1 ad set for one league

1. **Get the league from Shopify.** Search products by title; use the ACTIVE product. Pull the metafields above plus `legacyResourceId` (the product ID) and `onlineStoreUrl`.
2. **Duplicate the template ad set.** `duplicate_adset` with `adset_id` `120253711911230019` (Tualatin), `deep_copy: false`, `status_option: "paused"`. This copies the approved settings: $500/day, COST_CAP $50, Purchase on the pixel, ages 25-45, past-customer exclusions, placements.
3. **Rename and retarget** with `update_adset`:
   - `name`: Shopify product title + `_` + product ID. Two leagues in one ad set: join IDs with `_` (for example `..._10338358657282_10338362360066`).
   - `targeting`: send the full object (it replaces, not merges). Keep everything from the template and change only `geo_locations.custom_locations` to one pin: `address_string`, `latitude`, `longitude` from `facility_coordinates`, `radius: 15`, `distance_unit: "mile"`, `country` (`US` or `CA`). Keep `excluded_custom_audiences`: `120243290793190019`, `120252875760880019`, `120253656154900019`.
4. **Landing page:** the league's product page. Two leagues at one facility: the facility collection page.
5. **Create the ads** (see below). Default set: 2 statics, 2 videos, 1 carousel.
6. **Check the targeting before turning on.** Read the ad set back with `get_data` (`adset_targeting`, `include_objects_without_insights`) and confirm, for every ad set you build, edit or enable:
   - `geo_locations` has only `custom_locations` (plus `location_types`). Any `countries`, `regions`, `cities` or `zips` is wrong: stop and fix it. A P1 with no pins targets a whole country (Darling Harbour spent $585 in the US this way, Oct 2026).
   - Every pin is `radius: 15`, `distance_unit: "mile"`, unless John has named an exception.
   - For P1, each league in the name has a pin centered within 3 mi of its Shopify `facility_coordinates` (this checks the pin's location, not its radius), and the pin `country` matches the facility's country.
   Run the same check across all delivering ad sets whenever you touch Meta targeting, not just the one you changed.
7. **Turn on** with `enable_adset` if asked to launch.
8. **Log it** in the tab for the ad set's season: Fall and Late Fall go in `Fall26 Ad Sets`; Early Winter goes in `EarlyWinter27 Ad Sets` (column G is a per-row Mismatch formula, copy it down); the `Ad Sets` tab is the Winter 2027 build plan, so log Winter ad sets there by filling O (ad set ID) and P (actual status) on the planned row. For `Fall26 Ad Sets`: campaign, ad set name, ad set ID, Want, Actual, OK, daily budget, cost cap, bid strategy, ads loaded, ads live, spend, `YYYY-MM-DD, built by Claude for <name>`, notes.

## Ads

### Naming

- The ad name is the Drive file name (without extension), exactly the same in every ad set. The creative report matches on it. Don't add a season prefix yourself, but keep one that is already in the file name: season-specific creatives (for example `W27_ALL_Moodyboy-TradingCards_Static_v1`) keep their `W27_` so John can tell which season they belong to.
- Campaign and ad set names stay evergreen (no season words). Seasonal creatives run only in their season and get swapped out after it; seasonless creatives can keep running.
- Location-specific creatives (for example the Houston volleyball set) end in `_localized`.
- The creative name (inside `creative.name`) can carry a tag, for example `fall_leagues_live_stick_static_LF26NAurora_v1`.

### Copy

Every ad gets several options so Meta can rotate them: **5 primary texts, 4 headlines, 2 descriptions**, put in `asset_feed_spec.bodies`, `titles`, `descriptions`, with the first of each also in `object_story_spec`. Write them from Shopify: day, time, start date, facility, skipped weeks. Brand voice: playful, "Athletic? Debatable. Fun? Guaranteed.", "Sign up solo or bring a friend", "matched at your level". Use the 🥒 emoji, never 🏓 (ping pong). Do not invent dates; if a request conflicts with Shopify, say so and use Shopify.

### Required on every creative

- `url_tags`: `utm_source=facebook&utm_medium=paid&utm_campaign={{campaign.name}}&utm_id={{campaign.id}}&utm_term={{adset.id}}&utm_content={{ad.id}}&lebesgue_source=meta&lebesgue_adid={{ad.id}}`
- `call_to_action` SIGN_UP, linking to the landing page.
- `degrees_of_freedom_spec.creative_features_spec`: OPT_IN `inline_comment`, `enhance_cta`, `image_brightness_and_contrast`; OPT_OUT `image_touchups`, `image_templates`, `image_uncrop`, `image_animation`, `add_text_overlay`, `text_optimizations`, `description_automation`, `site_extensions`, `product_extensions`, `show_summary`, `reveal_details_over_time`, `ads_with_benefits`, and for videos also `video_auto_crop`.

### First values must match (or the ad set can't be duplicated)

Meta accepts an ad whose `asset_feed_spec` and `object_story_spec` disagree, but then rejects every duplicate of its ad set ("For a Degrees of freedom enabled ad, the first value of Asset Feed Spec field should match the corresponding field in Object Story Spec", #100.2446211). The Oct 2026 W27 and LF26 builds hit this. For every ad with `asset_feed_spec`:

- The first entry of `bodies`, `titles`, `descriptions` and `link_urls` equals `message`, `name`/`title`, `description`/`link_description` and `link` in `object_story_spec`. All three text fields must be present in `object_story_spec`.
- The first entry of `images` (or `videos`) is the image (or video) in `object_story_spec`. With several sizes, put the default size (usually `img_1x1`/`vid_1x1`, the one with the empty `customization_spec`) first in the list; list order is separate from rule `priority`.
- A broken ad can't be fixed in place. Build a corrected copy, then a person deletes the old one in Ads Manager (paused ads still block duplication).

### Static (single image)

`object_story_spec.link_data` with `link`, `image_hash`, first body/title/description, CTA. `asset_feed_spec` with `images`, `bodies`, `titles`, `descriptions`, `link_urls`, `call_to_action_types: ["SIGN_UP"]`, `ad_formats: ["SINGLE_IMAGE"]`, `optimization_type: "DEGREES_OF_FREEDOM"`. When there are several sizes of one design, label them (`img_9x16`, `img_4x5`, `img_191x1`, `img_1x1`) and add `asset_customization_rules`: 9x16 for stories/reels/status, 4x5 for feed, 1.91 for right column, 1x1 as the default (empty `customization_spec`, last priority).

### Video

`object_story_spec.video_data` with `video_id`, a thumbnail (`image_hash` or `image_url`), `message`, `title`, `link_description`, CTA. `asset_feed_spec` with bodies, titles, descriptions and `optimization_type: "DEGREES_OF_FREEDOM"`. Two aspect ratios of one video: put both in `asset_feed_spec.videos` with `thumbnail_hash` and labels, `ad_formats: ["SINGLE_VIDEO"]`, and customization rules like statics.

### Carousel

`object_story_spec.link_data` with `message`, `multi_share_optimized: false`, `multi_share_end_card: false`, and `child_attachments` (one per card: `link`, `image_hash`, `name`, `description`, CTA). No `asset_feed_spec`.

### Flexible format: do not use the API

Meta's "Flexible" format (several images chosen under Media) cannot be set through the API. Attempts either pull photos from the website or fall back to single image. If someone wants a flexible ad, tell them to duplicate an existing flexible ad in Ads Manager and paste the copy. Otherwise use a single-image phrase static instead (for example `phrase3-lowpressure-high5_static`).

## Current top creatives (Fall 2026, as of Oct 13)

| Ad name | Type | Meta asset |
|---|---|---|
| fall_leagues_live_stick_static | static 9x16 | image hash `d1bcfdafa14196d5b6b35cb48bc81c52` |
| phrase3-lowpressure-high5_static | static 9x16 | image hash `62be088b36f83800ca4e2d5c55ffe117` |
| WiiSport_Video | video 9x16 | video `1259424719705193`, thumbnail hash `8f488fdb671ef939feddbb3bf77279d0` |
| DiffSkillLevels_Video | video | video `1536137918312288` (thumbnail: pull a fresh `thumbnail_url` from Windsor; fbcdn links expire) |
| Nov25Testimonials Carousel_1_1_1 | carousel, 4 cards 1x1 | hashes `9a48f0ba6a0da546f21b4924dd9fe76e`, `6b2d3cdd6a4b7430853878643bf018d0`, `19d36aae965aae9a0d146db9d4d46178`, `94204a5cb95ca3e47c345d128a68b8d5` |

Paused on John's call: `fall_in_love_stick_static` (do not add to new ad sets). Re-rank before a new season: Windsor `get_data` fields `ad_name, spend, actions_purchase` over `last_30d`, rank by purchases and cost per purchase, skip off-season themes (summer, Halloween).

## Getting creative assets into Meta

- **Find an existing asset:** Windsor `get_data` with `ad_id` + `image_asset_hash` + `image_asset_url` (statics) or `video_asset_video_id` (videos), `date_preset: "last_90d"`, filtered by `ad_name` or `adset_id`. Image and video asset fields cannot be queried together, and asset fields cannot be combined with `title_asset_text`/`body_asset_text`. Single-image ads may return no asset rows; then use the Drive file.
- **Upload images:** call Windsor `upload_files` (action `create_ad_image`), then POST the files with curl as repeated `file` form parts to the returned URL. It returns one hash per file. Meta dedupes, so re-uploading an existing image returns its existing hash.
- **Upload videos:** `create_ad_video` with `video_url` `https://drive.usercontent.google.com/download?id=<FILE_ID>&export=download&confirm=t` (this form works for files over 100 MB). For a thumbnail, download the video, grab a frame with `ffmpeg -ss 2 -frames:v 1`, and upload it as an image.
- Check image sizes before labeling (Pillow), and look at the image: confirm the city (Houston vs Chicago) and that there are no stale dates or season words that clash with the league.

## Editing live ads

- Pause or turn on: `pause_ad` / `enable_ad`, `pause_adset` / `enable_adset`.
- Rename: `update_ad` with `name`.
- Copy or link change on one ad: `update_ad_creative` (creates a new creative; only edits the single message/headline, so for multi-option copy create a new ad and pause the old one).
- Archived ads (deleted in Ads Manager) cannot be edited or paused; that error is harmless.

## Windsor quirks

- `get_data` sometimes times out at 60 s. Retry with fewer fields or a narrower `date_preset`.
- Reads only return objects with spend in the date range; a new or paused ad set may not appear.
- No hourly data on this plan, so `force_refresh` is rejected.

## Checking fall pins and statuses

The `Fall26 League Status` tab compares Kameron's tracker (via `Kam import`) to Meta (via `Meta Actual`). To refresh `Meta Actual`, pull `adset_targeting` from Windsor for the Phase 0 regional ad sets and match pins to leagues by address (column D is a normalized address key, not a Meta field). Every check column should read OK.

## Sheets housekeeping after a build

- `Fall26 Ad Sets`: add the row (see step 7).
- New league that is not in the `Leagues` tabs yet: add it to the Meta map Leagues tab and the Email Ops Leagues tab with the Shopify details, or tell John so the Slack watch picks it up.
- Never type over formula columns. Meta map `Leagues`: J and M to P (phase, campaign, ad set, live at launch) and V (ad copy line) are array formulas; to change phase use K (Phase override) and L (reason), to change the ad set change E/F/G. Meta map `Ad Sets`: F to J and Q are formulas (F pulls pin addresses from the Leagues tab, H counts leagues whose home is that ad set, so H and the number of addresses in F can differ). Email Ops `Leagues`: R and U to Y are formulas. Check with a grid read (`userEnteredValue.formulaValue`) before writing a column you have not written before.
- Known exception: `Ad Sets` F4 (Houston P0) is typed text on John's call so it keeps the Bumpy Pickle pin.

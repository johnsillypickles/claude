---
name: meta-league-ads
description: Build, launch, edit and log Silly Pickles Meta (Facebook/Instagram) league ad sets through the direct Meta Graph API (META_ACCESS_TOKEN; not the Windsor connector). Use for any request to set up or launch a Phase 1 (P1) ad set for a league, add or swap creatives in an ad set, pause or turn on ads, duplicate a fall ad set for a new season, write league ad copy, or check fall pins and statuses against Kameron's tracker.
---

# Silly Pickles: Meta league ads (Phase 1 builds and edits)

This is the playbook John and Claude worked out in October 2026. Follow it so every build looks the same and the creative report and data team reporting keep working.

## Who can do what

- John and Kameron can both build ads, and can turn ads and ad sets on (live) when asked.
- **Decision rights (John, 2026-11-10):** Kameron is the primary decision maker for Meta, including budgets and cost caps. John can also decide. An explicit OK from either one approves a specific change; log who approved it in Ad Sets column K.
- **Flag to Kameron first, before doing it (John can see and weigh in):** any ad set budget above **$500/day**, anything that touches the Phase 0 regional ad sets (pins/addresses), new campaigns, and releasing the December winter reserve.
- Don't delete live or spending objects. Paused test ads can be deleted with `DELETE /{ad_id}` once John or Kameron OKs it (John, 2026-11-11); otherwise pause, and a person deletes in Ads Manager.

## Tools and accounts

- **Meta writes and reads: the direct Graph API, always (John, 2026-11-12).** `https://graph.facebook.com/v21.0` (videos: `https://graph-video.facebook.com/v21.0`) with `access_token=$META_ACCESS_TOKEN` (system user, app 577513808656072, which must stay in Live mode). Ad account `act_1346441932978787`. Start every session with read-only checks: `GET /me/permissions`, `GET /act_1346441932978787?fields=name,account_status`, `GET /396692693535838?fields=name`. Never paste or print the token.
- **Do not use the Windsor.ai connector for Meta.** Windsor `create_ad` drops per-placement sizes, `update_ad_creative` wiped multi-text copy, and it can't read headlines 2+ or descriptions. If a Graph call fails, stop and report; don't fall back to Windsor for writes. (Windsor reporting reads for the weekly report are fine.)
- **Page:** `396692693535838`. **Pixel:** `1765459687532632`.
- **League details:** Shopify (source of truth once the product is ACTIVE). Product metafields, namespace `custom`: `start_date`, `league_day_of_week`, `timing`, `facility_address`, `facility_name`, `facility_coordinates`, `season`, `end_date`, `league_skipped_weeks`, `league_duration`, `sport`, `metro_area`.
- **Creative files:** Google Drive (search by file name).
- **Sheets:** Meta campaign map `1iWLu6pn-GZFbVj1S_lAWSZ6JMgNHYQwp37H1VMzgAeg` (tabs: Ad Sets, Leagues, Fall26 Ad Sets, Fall26 Ads, Fall26 League Status, Meta Actual, Kam import, Runbook). Winter 2027 Email Ops `1r21nUPNW2OkNfF0Oi7lRAlX7K8XKvkTLCnZGTGsHqKM` (tab Leagues). Kameron's tracker (tab `Kam Static Ad Tracker`): its ID is in the IMPORTRANGE formula in cell A1 of the map's `Kam import` tab.

## Campaigns

| Campaign | ID | Use |
|---|---|---|
| Fall26_Phase1_ProblemChildren | 120252229329790019 | Late Fall P1 ad sets go here until the W27 campaigns exist |
| Fall26_Phase0_Regional | 120252634833170019 | P0 address pins, do not edit without John |
| Fall26_Phase0_Retargeting | 120253309588180019 | |
| Fall26_Phase0_NewCustomer(only) | 120252634220400019 | |
| Fall26_Phase0_CreativeTest-tROASfocus | 120253673698350019 | |
| Pre-Winter27_LeadForm | 120253325111400019 | |

Winter 2027 campaigns exist per market (`Winter27_<Market>`, e.g. `Winter27_Carolinas`, `Winter27_Louisville`, `Winter27_RestOfUS`; list them with `GET /act_1346441932978787/campaigns?fields=name,effective_status`). A new Winter P1 goes in its market's existing `Winter27_` campaign (the Leagues tab, column N, names it). Do not create new campaigns without flagging Kameron and John first.

## Build a P1 ad set for one league

1. **Get the league from Shopify.** Search products by title; use the ACTIVE product. Pull the metafields above plus `legacyResourceId` (the product ID) and `onlineStoreUrl`.
0. **Check for an existing ad set first.** Search the Leagues and Ad Sets tabs and Meta (`GET /act_1346441932978787/adsets?fields=name,effective_status,targeting{geo_locations}&filtering=[{"field":"name","operator":"CONTAIN","value":"<city>"}]`). If another P1 already pins the same facility, add the league to that ad set instead (Louisville had two P1s on one address until 2026-11-12).
2. **Duplicate the template ad set.** `POST /120253711911230019/copies` (Tualatin template) with `deep_copy=false`, `status_option=PAUSED`, `campaign_id=<the market's Winter27 campaign ID>`. This copies the approved settings: $500/day, Purchase on the pixel, ages 25-45, past-customer exclusions, placements (FB/IG/WhatsApp incl. stories and reels). The template's cost cap is $35, so set `bid_amount` to `5000` ($50, cents) on the copy unless Kameron or John names another cap.
   - **Lifetime budget wanted:** a copy keeps the template's daily budget and Meta won't switch it to lifetime (error 1885257). Use `POST /act_1346441932978787/adsets` instead, in the same campaign: `optimization_goal: "OFFSITE_CONVERSIONS"`, `billing_event: "IMPRESSIONS"`, `promoted_object` pixel + `PURCHASE`, `bid_strategy: "COST_CAP"` with `bid_amount` (cents), `lifetime_budget` (cents) with `end_time`, and the template's full targeting object (copy from a live P1, change only the pin). Westerville Late Fall (Oct 28) was built this way.
3. **Rename and retarget** with `POST /{adset_id}` (`name`, `targeting` as JSON, `bid_amount`):
   - `name`: Shopify product title + `_` + product ID. Two leagues in one ad set: join IDs with `_` (for example `..._10338358657282_10338362360066`).
   - `targeting`: send the full object (it replaces, not merges). Keep everything from the template and change only `geo_locations.custom_locations` to one pin: `address_string`, `latitude`, `longitude` from `facility_coordinates`, `radius: 15`, `distance_unit: "mile"`, `country` (`US` or `CA`). Keep `excluded_custom_audiences` (all four, as on every live P1, checked 2026-11-12): `120243290793190019` (Purchasers 30d), `120252634024910019` (Shopify all-customer list), `120252875760880019` (Purchasers 730d), `120253656154900019` (Shopify customer list Oct 8).
4. **Landing page:** the league's product page. Two leagues at one facility: the facility collection page.
5. **Create the ads** (see below). Default set: 2 statics, 2 videos, 1 carousel.
6. **Check the targeting before turning on.** Read the ad set back with `GET /{adset_id}?fields=name,status,daily_budget,bid_amount,targeting` and confirm, for every ad set you build, edit or enable:
   - `geo_locations` has only `custom_locations` (plus `location_types`). Any `countries`, `regions`, `cities` or `zips` is wrong: stop and fix it. A P1 with no pins targets a whole country (Darling Harbour spent $585 in the US this way, Oct 2026).
   - Every pin is `radius: 15`, `distance_unit: "mile"`, unless John has named an exception.
   - For P1, each league in the name has a pin centered within 3 mi of its Shopify `facility_coordinates` (this checks the pin's location, not its radius), and the pin `country` matches the facility's country.
   Run the same check across all delivering ad sets whenever you touch Meta targeting, not just the one you changed.
7. **Turn on** with `POST /{id}` `status=ACTIVE` (ad set and ads) only when Kameron or John says to launch, then read `effective_status` back.
8. **Log it** in the tab for the ad set's season: Fall and Late Fall go in `Fall26 Ad Sets`; Early Winter goes in `EarlyWinter27 Ad Sets` (column G is a per-row Mismatch formula, copy it down); the `Ad Sets` tab is the Winter 2027 build plan, so log Winter ad sets there by filling O (ad set ID) and P (actual status) on the planned row. For `Fall26 Ad Sets`: campaign, ad set name, ad set ID, Want, Actual, OK, daily budget, cost cap, bid strategy, ads loaded, ads live, spend, `YYYY-MM-DD, built by Claude for <name>`, notes.

## Ads

### Naming

- The ad name is the Drive file name (without extension), exactly the same in every ad set. The creative report matches on it. Don't add a season prefix yourself, but keep one that is already in the file name: season-specific creatives (for example `W27_ALL_Moodyboy-TradingCards_Static_v1`) keep their `W27_` so John can tell which season they belong to.
- Campaign and ad set names stay evergreen (no season words). Seasonal creatives run only in their season and get swapped out after it; seasonless creatives can keep running.
- Location-specific creatives (for example the Houston volleyball set) end in `_localized`.
- The creative name (inside `creative.name`) can carry a tag, for example `fall_leagues_live_stick_static_LF26NAurora_v1`.

### Copy

Every ad gets several options so Meta can rotate them: **5 primary texts, 4 headlines, 2 descriptions**, put in `asset_feed_spec.bodies`, `titles`, `descriptions`, with the first of each also in `object_story_spec`. Write them from Shopify: day, time, start date, facility, skipped weeks. Brand voice: playful, "Athletic? Debatable. Fun? Guaranteed.", "Sign up solo or bring a friend", "matched at your level". Emojis (John, 2026-11-12): 🏓 is fine. Mix in fun, funny emojis beyond 🥒 (e.g. 🙈🙃🐣🥳🤠🤪🤓🫠😅🫪), but **John approves every emoji not already in approved copy before it goes live**, because some carry subtext with certain audiences: list any new ones when you show him the copy. No 🥒 in volleyball copy. Do not invent dates; if a request conflicts with Shopify, say so and use Shopify.

### Required on every creative

- `url_tags`: `utm_source=facebook&utm_medium=paid&utm_campaign={{campaign.name}}&utm_id={{campaign.id}}&utm_term={{adset.id}}&utm_content={{ad.id}}&lebesgue_source=meta&lebesgue_adid={{ad.id}}`
- `call_to_action` SIGN_UP, linking to the landing page.
- **Placement sizes (required, John and Tommy, 2026-11-10).** Every placement must show a clean, centered asset with no text or faces cut off.
  - **Our creative spec is a single 9:16 file (1080x1920) built for the safe zone** (Silly Pickles Winter 2027 Ad Creative Specs, John, 2026-10-09; Drive folder `19OTV_tJKtITq_zbA5a0EK25HkBMQYxJK`: spec PDF `1ThnKJooRc1MiOvabxdXu4d4nNiZwcniY`, overlay SVG `1rPdKvPnhg6EPbMESRB0UoQmEjlqj0c5L` / PNG `11OrioUCgjrtrhN_HT2TH2l6Xdk3XgZB_`). Such a file is fine on its own and is not a sizing problem. The zones, in pixels on the 1080x1920 frame:
    - Reels UI covers the top 270px, the bottom 670px (y 1250 to 1920: captions, CTA, like/comment/share) and 65px on each side.
    - 4:5 crop (1080x1350, centered) = y 285 to 1635. 1:1 crop (1080x1080, centered) = y 420 to 1500.
    - **Text, logo and caption safe zone: x 65 to 1015, y 420 to 1250 (950x830).** Faces stay inside the center 1080x1080 square (y 420 to 1500).
    - Videos: native 9:16, burned-in captions in the same safe zone, 15 to 30 s preferred, 60 s max. Carousels: 1080x1080 cards (3 to 10).
  - Before using a 9:16 asset, check one frame (statics: the image; videos: a few frames incl. caption frames) against those boxes. If text or faces fall outside, use the designer's separate 4x5 (1080x1350) and 1x1 (1080x1080) files; the spec says they send those when a design can't survive the crop. If they don't exist, ask the creator before launch.
  - **Build per-placement ads with the direct Graph API and `optimization_type: "PLACEMENT"` (2026-11-11).** `DEGREES_OF_FREEDOM` silently drops `asset_customization_rules`: the Windsor test ads (11/10) and a direct-API DOF test both previewed 1:1 everywhere. Every working per-placement ad in the account (91 built in Ads Manager) uses `PLACEMENT`. Recipe: see "Per-placement creative (PLACEMENT recipe)" below. Windsor can't build these; use `META_ACCESS_TOKEN` (system user, app 577513808656072, which must stay in Live mode or creative creation fails with #1885183).
  - **Separate files per size (John, 2026-11-10):** when the designer's folder has 9x16, 4x5, 1x1 and 1.91 files, upload one per placement and no re-export is needed. The 9x16 file then shows only in stories/reels, so it is checked only against the reels UI (x 65 to 1015, y 270 to 1250), not the 1:1 limit at y 420. A logo or tagline hidden under the bottom reels UI is fine. Fall back to the 4x5 for stories only if faces or the main headline or offer would be covered.
  - When building or rebuilding, add our own 4:5 crop of the 9:16 file (y 285 to 1635, full width) and a 1:1 crop (y 420 to 1500) as labeled sizes, so Meta's crop never decides.
  - Never run a 1:1-only or 4:5-only asset in stories/reels/status: use the 9x16 from Drive (FrozenManMeme, SocialLifeOnIce, Jackpot and the SP_Sept2026 designs all have one). If a design has no 9x16, ask the creator before launch.
  - Use a 1.91x1 asset for right column/search when one exists; otherwise serve the original uncropped, never a Meta-made crop.
  - Wire sizes with `asset_customization_rules` (PLACEMENT recipe). The 11/10 audit found 81 ads 1:1-only in stories and 22 ads serving Meta-generated "untitled" crops that cut faces; all Moodyboy and phrase ads were rebuilt 11/11 (Ad Copy Log rows 30 to 106).
  - **Check every new ad's placements before turning it on.** Generate `GET /{ad_id}/previews?ad_format=` for `INSTAGRAM_STORY`, `INSTAGRAM_REELS`, `FACEBOOK_STORY_MOBILE`, `INSTAGRAM_STANDARD`, `MOBILE_FEED_STANDARD`, render the iframe (Playwright through the proxy) and confirm the served media is 9:16 in stories/reels and 4:5 in feeds. Shareable `fb.me` preview links don't open for John and default to the feed view; send the Ads Manager link plus a screenshot sheet instead.
- **Save every ad's full copy at build time (John, 2026-11-10).** After creating each ad, append one row to the Meta map tab "Ad Copy Log": date, campaign, ad set, ad set ID, ad name, ad ID, bodies (joined by " || "), titles, descriptions, link, url_tags, CTA, session. The Graph API can read the full copy back, but this log is the record of what we shipped and why.
- **Never use Windsor `update_ad_creative` on ads with several primary texts or headlines (2026-11-10).** On 19 of 21 such ads it wiped the copy: primary text came back blank and headlines were replaced with the page default. They were live with blank copy for about 10 minutes before being pointed back to their original creatives with `update_ad`. It only worked on single-text ads. Any creative edit: read the copy back immediately, and roll back with `update_ad` {creative_id: <original>} if anything changed. Windsor also cannot read headline/description sets beyond the first, so rebuilds need an Ads Manager export of the copy.
- **No Meta cropping or expansion.** Every creative also opts out of `cv_transformation`, `image_auto_crop`, `image_uncrop`, `video_auto_crop`, `video_uncrop`, `video_uncrop_9x16_to_9x18`, `image_background_gen`, `pac_recomposition`, `pac_genai_recomposition`, `adapt_to_placement` and `image_animation`, and never carries `standard_enhancements`. Before turning an ad on, read back the assets it serves: no "untitled" or "cropped_" assets, and each placement gets its matching size.
- `degrees_of_freedom_spec.creative_features_spec`: OPT_IN `inline_comment`, `enhance_cta`, `image_brightness_and_contrast`; OPT_OUT `image_touchups`, `image_templates`, `image_uncrop`, `image_animation`, `add_text_overlay`, `text_optimizations`, `description_automation`, `site_extensions`, `product_extensions`, `show_summary`, `reveal_details_over_time`, `ads_with_benefits`, and for videos also `video_auto_crop`.

### First values must match (or the ad set can't be duplicated)

Meta accepts an ad whose `asset_feed_spec` and `object_story_spec` disagree, but then rejects every duplicate of its ad set ("For a Degrees of freedom enabled ad, the first value of Asset Feed Spec field should match the corresponding field in Object Story Spec", #100.2446211). The Oct 2026 W27 and LF26 builds hit this. For every ad with `asset_feed_spec`:

- The first entry of `bodies`, `titles`, `descriptions` and `link_urls` equals `message`, `name`/`title`, `description`/`link_description` and `link` in `object_story_spec`. All three text fields must be present in `object_story_spec`.
- The first entry of `images` (or `videos`) is the image (or video) in `object_story_spec`. With several sizes, put the default size (usually `img_1x1`/`vid_1x1`, the one with the empty `customization_spec`) first in the list; list order is separate from rule `priority`.
- A broken ad can't be fixed in place. Build a corrected copy, then delete the old one (paused ads still block duplication). John OK'd API deletes of paused test ads 2026-11-11 (`DELETE /{ad_id}`); ask before deleting anything else.
- This rule is for `DEGREES_OF_FREEDOM` ads. PLACEMENT ads keep only `page_id` and `instagram_user_id` in `object_story_spec` (that is how Ads Manager builds them).

### Per-placement creative (PLACEMENT recipe, 2026-11-11)

Use this for every new or rebuilt ad that has more than one size (statics and single videos). Built and verified on 79 ads 11/11.

- `object_story_spec`: only `page_id` and `instagram_user_id` (no `link_data`/`video_data`).
- `asset_feed_spec`: `optimization_type: "PLACEMENT"`, `ad_formats: ["SINGLE_IMAGE"]` (statics) or `["AUTOMATIC_FORMAT"]` (videos), `call_to_action_types: ["SIGN_UP"]`, plus `images` (`hash`) or `videos` (`video_id`, `thumbnail_hash`), `bodies`, `titles`, `descriptions`, `link_urls` (`website_url`).
- One rule per placement group, each with a label for every asset type: `customization_spec`, `image_label`/`video_label`, `body_label`, `title_label`, `description_label`, `link_url_label`, `priority`. Every text and the link carry the labels of all rules they apply to (e.g. each body has `b_r1`...`b_r4`), so multiple bodies and titles still rotate inside each group. A media file used by two rules carries both labels.
  - r1: `facebook_positions: [story, facebook_reels]`, `instagram_positions: [story, reels]` (add `whatsapp_positions: [status]` if the ad set has WhatsApp; Meta accepts it but did not echo it back, so Status may fall to the default) → 9x16.
  - r2: `facebook_positions: [feed]`, `instagram_positions: [stream]` → 4x5.
  - r3: `facebook_positions: [right_hand_column]` → 1.91 (skip if the design has none).
  - r4: default, `customization_spec` with only `age_min: 13, age_max: 65` → 1x1 (or 4x5 if the 1x1 is a different cut).
  - Every spec also carries `age_min: 13, age_max: 65` (Ads Manager does this) and only lists positions the ad set actually uses.
- **One description per rule.** Meta rejects several descriptions in a rule ("Multiple descriptions assets can not be applied to rule #1"). Use one description; for single-league ads it is the facility name, chains plus location ("Pickleball Kingdom Lexington", "PickleRage Centerville"); for metro P0s the metro line ("New winter ladder leagues in Phoenix").
- `degrees_of_freedom_spec`: copy the opt-outs above. When reusing a creative read back from Meta, strip `standard_enhancements` (Meta adds it on read and rejects it on write: "Including standard enhancements field in creative has been deprecated") and strip the label `id`s.
- Read back after creating: Meta reorders titles and copies videos to new IDs, so compare texts as sets and media by count.
- Copy edits: build a new creative and `POST /{ad_id}` with `creative: {creative_id}`; works on paused and live ads (live ads stay ACTIVE through re-review).
- Swap: enable the replacement only after its review clears, confirm `status: ACTIVE`, then pause the original; log column K (or Fall26 Ads for Fall26 ad sets).

### Copy for Moodyboy W27 creatives (John, 2026-11-11)

Mix localized and Moodyboy lines (Drive doc "Moodyboy Ad Copy - October 2026", `13NwwYqZRPaV1uQIWYw14WlS48F-NwA1kk7t9zT1W5w0`, verbatim incl. "winter"): bodies 1 and 2 and headlines 1 and 2 localized from Shopify (league intro + dates/skipped weeks; "{City} Pickleball League 🥒" + "{Day time}, Starts {date}"), the rest Moodyboy for that design, 5 bodies and 5 headlines total. Ads with only one localized line get 1 localized + 4 Moodyboy. Non-Moodyboy ads without headlines get generic ones (e.g. "Winter Pickleball Leagues Near You 🥒", "Sign Up Solo or With a Friend", "Matched at Your Level", "Beginners and Intermediates Welcome", "Athletic? Debatable. Fun? Guaranteed.").

### Static (single image)

`object_story_spec.link_data` with `link`, `image_hash`, first body/title/description, CTA. `asset_feed_spec` with `images`, `bodies`, `titles`, `descriptions`, `link_urls`, `call_to_action_types: ["SIGN_UP"]`, `ad_formats: ["SINGLE_IMAGE"]`, `optimization_type: "DEGREES_OF_FREEDOM"`, only when the design has a single size. With several sizes use the PLACEMENT recipe above.

### Video

`object_story_spec.video_data` with `video_id`, a thumbnail (`image_hash` or `image_url`), `message`, `title`, `link_description`, CTA. `asset_feed_spec` with bodies, titles, descriptions and `optimization_type: "DEGREES_OF_FREEDOM"`. Two or more aspect ratios of one video: use the PLACEMENT recipe above (`ad_formats: ["AUTOMATIC_FORMAT"]`, thumbnails from each video's preferred frame uploaded as images).

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
| DiffSkillLevels_Video | video | video `1536137918312288` (9:16 only, 576x1024; thumbnail: `GET /1536137918312288/thumbnails`, fbcdn links expire) |
| Nov25Testimonials Carousel_1_1_1 | carousel, 4 cards 1x1 | hashes `9a48f0ba6a0da546f21b4924dd9fe76e`, `6b2d3cdd6a4b7430853878643bf018d0`, `19d36aae965aae9a0d146db9d4d46178`, `94204a5cb95ca3e47c345d128a68b8d5` |

Paused on John's call: `fall_in_love_stick_static` (do not add to new ad sets).

**Seasonal creatives (John, 2026-11-12):** fall-themed designs run only in fall / late fall (Fall26) campaigns, never in Winter or Early Winter campaigns: `SP_Fall2026_Jackpot_static` (fall only, explicitly), `SP_July2026_Loading`, `SP_Sept2026_FallBucketList`, `SP_Sept2026_LastCall_Pickleball`. Houston's "Last Call for Sand Volleyball" is OK for Houston volleyball (late fall). Evergreen (any season): CatMeme, StayForFriends, The76, Toggle, DigitalCamera, DiffSkillLevels (keep as is; no designer, no other sizes). Re-rank before a new season: `GET /act_1346441932978787/insights?level=ad&date_preset=last_30d&fields=ad_name,spend,actions`, sum by ad name, rank by purchases (`offsite_conversion.fb_pixel_purchase`) and cost per purchase, skip off-season themes (summer, Halloween).

## Getting creative assets into Meta

- **Find an existing asset or copy:** `GET /{ad_id}?fields=name,creative{id,object_story_spec,asset_feed_spec,url_tags,degrees_of_freedom_spec}` returns every body, headline, description, image hash and video ID. Image details: `GET /act_1346441932978787/adimages?hashes=[...]&fields=hash,name,original_width,original_height,url`. Video details: `GET /{video_id}?fields=title,format{width,height,filter},thumbnails{uri,is_preferred}`. Account video list: `GET /act_1346441932978787/advideos?fields=id,title,created_time`.
- **Upload images:** download from Drive (`https://drive.usercontent.google.com/download?id=<FILE_ID>&export=download&confirm=t`), save with the real extension (`.jpg`/`.png`; an unknown extension returns no hash), then `curl -F "filename=@file.jpg" -F access_token=... https://graph.facebook.com/v21.0/act_1346441932978787/adimages`. Meta dedupes, so re-uploading returns the existing hash.
- **Upload videos:** `POST https://graph-video.facebook.com/v21.0/act_1346441932978787/advideos` with `file_url=<the Drive download URL above>` and `name=<Drive file name>`; poll `GET /{video_id}?fields=status` until `video_status` is `ready`. Thumbnail: download the preferred one from `/{video_id}/thumbnails` and upload it as an image.
- **Check real dimensions** with Pillow / `ffprobe`, not the file name: some "1440x1800" files are 1400x1800 (7:9) and "1440x2560" files 1400x2560. Trim to the exact ratio (crop plain background only) before uploading.
- Check image sizes before labeling (Pillow), and look at the image: confirm the city (Houston vs Chicago) and that there are no stale dates or season words that clash with the league.

## Editing live ads

- Pause or turn on: `POST /{ad_or_adset_id}` with `status=PAUSED` or `status=ACTIVE`, then read `status,effective_status` back.
- Rename: `POST /{id}` with `name`.
- Copy or link change: creatives can't be edited. Read the current creative, build a new one with the change (strip label `id`s and `standard_enhancements`), then `POST /{ad_id}` with `creative={"creative_id":"<new>"}`. Works on paused and live ads; a live ad keeps delivering through re-review. Read the copy back.
- Creative swap: build the replacement paused, wait until its review clears, set it ACTIVE, confirm, then pause the original (never pause first).
- Archived ads (deleted in Ads Manager) cannot be edited or paused; that error is harmless.
- **Log every pause or turn-on in the `Fall26 Ads` tab** (one row per ad, matched on column H, Meta ad ID), in the same session as the change. Set E (Want) and F (Actual) to Paused or Active, J to `YYYY-MM-DD, paused by Claude (<who approved>)` (or `turned on by`), and K to the reason. Do not touch G (Mismatch). If someone else made the change, log it as `paused by <name> (Claude confirmed)`. If an ad has no row, add one with B to O filled from the Graph API (leave A, G and L blank: formulas).
- Write `Fall26 Ads` updates one row (or one contiguous run of rows) per call, then re-read the rows by ad ID to confirm the right ones changed. A single large write with blank filler rows can land a row off.

## Graph API notes

- List endpoints page at `limit` (max ~50 with insights); follow `paging.next` until it's gone. The account has 6,500+ ads.
- Code `2` "unexpected error, retry later" is transient: retry with backoff (5, 15, 30, 60 s).
- Deleted ads read back as `status: DELETED`; archived objects can't be edited (harmless error).
- Ad previews: `GET /{ad_id}/previews?ad_format=INSTAGRAM_STORY` (also `INSTAGRAM_REELS`, `FACEBOOK_STORY_MOBILE`, `INSTAGRAM_STANDARD`, `MOBILE_FEED_STANDARD`, `RIGHT_COLUMN_STANDARD`) returns an iframe URL; render it with Playwright (proxy in `HTTPS_PROXY`) to screenshot and check the served media size. A preview fetched seconds after a creative change can be stale; re-check before reporting a failure.
- Windsor (reporting only): `get_data` can time out at 60 s and only returns objects with spend in range.

## Checking fall pins and statuses

The `Fall26 League Status` tab compares Kameron's tracker (via `Kam import`) to Meta (via `Meta Actual`). To refresh `Meta Actual`, read `GET /{adset_id}?fields=targeting{geo_locations}` for the Phase 0 regional ad sets and match pins to leagues by address (column D is a normalized address key, not a Meta field). Every check column should read OK.

## Sheets housekeeping after a build

- `Fall26 Ad Sets`: add the row (see step 7).
- `Fall26 Ads`: add a row per new ad (ad set, ad name, creative, rotation slot, Want, Actual, ad ID, date uploaded, `YYYY-MM-DD, built by Claude`, campaign, ad set ID).
- New league that is not in the `Leagues` tabs yet: add it to the Meta map Leagues tab and the Email Ops Leagues tab with the Shopify details, or tell John so the Slack watch picks it up.
- Never type over formula columns. Meta map `Leagues`: J and M to P (phase, campaign, ad set, live at launch) and V (ad copy line) are array formulas; to change phase use K (Phase override) and L (reason), to change the ad set change E/F/G. Meta map `Ad Sets`: F to J and Q are formulas (F pulls pin addresses from the Leagues tab, H counts leagues whose home is that ad set, so H and the number of addresses in F can differ). Email Ops `Leagues`: R and U to Y are formulas. Check with a grid read (`userEnteredValue.formulaValue`) before writing a column you have not written before.
- Known exception: `Ad Sets` F4 (Houston P0) is typed text on John's call so it keeps the Bumpy Pickle pin. F47 (Baltimore) and F50 (Atlanta) are also typed (synced to Meta 2026-11-08).
- P0 pins and P1 overlap (John, 2026-11-08, "option A"): metro P0s keep the addresses of their P1 leagues pinned; there are no P0 geo exclusions in Meta. On `Ad Sets` P0 rows, F lists leagues routed to the P0 plus that sub-metro's P1 leagues, and G is "None". Do not add exclusions in Meta or the sheet unless John changes this.
- `Ad Sets` F on formula P0 rows follows the Leagues tab, not Meta: while January pins are off (2026-11-04 to ~Dec 1) and for cancelled leagues, F still lists those addresses. Meta is the truth for live pins.

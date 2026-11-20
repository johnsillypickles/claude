# New-venue lead form build (2026-11-18)

Built for John. 9 ad sets, 54 ads, all PAUSED until John OKs launch after QA.

## Offer
$50 off, first 15 players per venue, codes expire 2026-12-04 11:59pm PT (Shopify basic codes, once per customer, product-specific).

## Per venue
| Slug (form `league` param) | Ad set ID | Lead form ID | Code(s) |
|---|---|---|---|
| phoenix-centercourt | 120254374304340019 | 1782719256147984 | FIRST15GLENDALECC, FIRST15SCOTTSDALESHEA, FIRST15SCOTTSDALEMAYO (form asks "Which Center Court location?") |
| windsor | 120254374305000019 | 1128404803243119 | FIRST15WINDSOR |
| millersville | 120254374305630019 | 40256982870615364 | FIRST15PUTAWAY |
| camas | 120254374306840019 | 1438676275048799 | FIRST15CAMAS |
| chamblee | 120254374307530019 | 969260259275646 | FIRST15CHAMBLEE |
| visalia | 120254374307930019 | 28823294264007968 | FIRST15VISALIA |
| crowley | 120254374308850019 | 1162375469593149 | FIRST15CROWLEY |
| westbury | 120254374309300019 | 1121875080657345 | FIRST15WESTBURY |
| pinevalley | 120254374309610019 | 2372031993591873 | FIRST15PINEVALLEY |

Campaign: Winter27_LeadForm_Founding+EarlyBird (120253881394820019). Ad sets: $20/day, end 2026-12-02 23:59 PT (reset to launch + 14 days when turned on), 10 mi pins, ages 21-65, Chesterfield exclusions.

Ads: 6 per ad set, names shared across venues (`W27_Localized_pb_<Concept>_Static_v1`, concepts GetOnTheList, YouSearchedIt, ThreeNos, Billboard, RipPaper, Blur). image_animation opted IN on these (John 2026-11-18); all crop/expand features off. Logged in Meta map Ad Copy Log rows 152-205 and Ad Sets rows 114-122.

## Lead sync (pending)
Klaviyo cannot connect Meta forms to lists by API. Plan: once META_ACCESS_TOKEN has `leads_retrieval` (new token on system user "META_ACCESS_TOKEN", id 122106656223536795, app 577513808656072), a scheduled task runs hourly: GET /{form_id}/leads since last run, add each lead (email, first name, phone, answers, `league` param) to that venue's Klaviyo list "W27 Lead Form · <City> (New Venue)", which triggers the flow. Klaviyo list and flow IDs: see the Klaviyo build report (flows built in DRAFT; John approves before live).

First step in the new session: check token scopes (GET /me/permissions), read leads on form 1792764368628802 (Chesterfield) as a test, then build the sync.

## Launch (2026-11-20, John)
- Klaviyo: footer now `{{ organization.full_address }}` on all 18 templates; Westbury templates use the new `westbury-ny-...` handle (old `wayne-nj-...` URL has a Shopify redirect, kept; Westbury lead form thank-you link still uses it). All 9 flows set live.
- Meta: 9 ad sets + 54 ads ACTIVE, end_time 2026-12-04 23:59 PT (matches code expiry). Max spend 9 x $20 x 14 = $2,520. Logged Ad Sets rows 114-122, posted #meta-ops.
- Lead sync: scheduled task trig_018amLmkKRC6LbofBJEXy5dL fires hourly into this session, runs scripts/lead_sync.py --hours 3, imports leads to each venue list with Klaviyo bulk_import_profiles (adds to list, triggers flow; consent not set because the subscribe tool needs per-call approval). Delete after 2026-12-05.

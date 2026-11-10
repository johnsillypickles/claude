# Crop fix handoff (2026-11-10)

Pick-up notes for a new session with direct Meta Marketing API access (`META_ACCESS_TOKEN`, hosts graph.facebook.com and graph-video.facebook.com allowed). Read `.claude/skills/meta-league-ads/SKILL.md` (Placement sizes, crop opt-outs, update_ad_creative warning) first.

## Why direct API
- Windsor `create_ad` drops per-placement sizes: test ads 120254222041080019 (Raleigh FrozenManMeme) and 120254222670380019 (National SocialLifeOnIce) preview 1:1 everywhere. Both are PAUSED; John will delete them in Ads Manager.
- Windsor can't read headlines 2+ or descriptions. The Graph API returns the full `asset_feed_spec`, so read each original ad's creative and copy it exactly.

## First steps
1. Read-only checks: `GET /me/permissions`, `GET /act_1346441932978787?fields=name`, page 396692693535838 access.
2. Build ONE paused test replacement (highest-spend FrozenManMeme ad) with 9x16 for stories/reels/status, 4x5 for feed, 1.91 right column, 1x1 default, all crop/expand opt-outs. John checks it in Ads Manager Preview before anything else.
3. Then batches by ad set, highest spend first. Show John each batch; enable replacements and pause originals together only after his OK. Log each swap in Meta map Ad Sets column K and every new ad's copy in the "Ad Copy Log" tab.

## Decisions from John (2026-11-10)
- FrozenManMeme / SocialLifeOnIce: use Moodyboy's per-size files (Drive folders 1M3KHg9-ZFgtU4oHoHgwRZ2O9SjHxlJU5 and 1PzF25Cq9qJi1ofPSxoXQkQT9VaUvAeEt). A tagline hidden under the bottom reels UI is OK.
- OPEN: the live FrozenManMeme cut says "NOW ENROLLING / WINTER LEAGUES"; the Drive files say "MEET FUN PEOPLE / PLAY PICKLEBALL". Ask John which to use.
- phrase4/phrase6: our own crops, 4:5 = y 285 to 1635, 1:1 = y 460 to 1540 (approved). Already uploaded 1:1 hashes 501d2c1c787f926a84275efaf51230cf (phrase4), 91c3c96b91beae6d7c2e937966a62b0f (phrase6). Meta crop already off on both.
- Payton's VB 1x1 statics (BiggerBall, DefyGravity, BeforeAfterDog, PerfectCommunication) wait on 9:16 re-exports.
- DiffSkillLevels in National(remainder) 120253572928510019 is on the fatigue pause list: skip.
- Never change budgets, bids, targeting or ad set status. No 🥒 in volleyball copy.

## Targets (98 ads, by 7-day spend as of 2026-11-10)
cat: AI = Meta auto-crop on; 1x1img / 1x1vid = 1:1-only asset in stories; vb = volleyball.

| spend 7d | cat | ad name | ad ID | ad set | ad set ID |
|---|---|---|---|---|---|
| 201.09 | AI | phrase4-smacktalk_static | 120253673699060019 | Fall26_Phase0_NewCus_Phrase_Statics | 120253673698710019 |
| 145.25 | chk | Last Call for Sand Volleyball-static_localized | 120253728258450019 | Houston, TX: Volleyball Ladder League at Bumpy Pickle | Late | 120253726800620019 |
| 113.85 | 1x1 | W27_ALL_Moodyboy-SocialLifeOnIce_Static_v1 | 120254086391300019 | Winter27_RestOfUS_National_P0 | 120254063677590019 |
| 108.14 | 1x1 | W27_ALL_Moodyboy-FrozenManMeme_Video_v1 | 120254081519580019 | Raleigh, NC: Pickleball Ladder League at Sanderford Road Par | 120254063650790019 |
| 96.10 | 1x1 | W27_ALL_Moodyboy-FrozenManMeme_Video_v1 | 120254085920700019 | Chicago, IL: Pickleball Ladder League at SPF All Day - Irvin | 120254079135660019 |
| 94.42 | 1x1 | W27_ALL_Moodyboy-FrozenManMeme_Video_v1 | 120254085155370019 | Atlanta, GA: Pickleball Ladder League at Dill Dinkers West E | 120254063665550019 |
| 93.37 | 1x1 | W27_ALL_Moodyboy-FrozenManMeme_Video_v1 | 120254086256720019 | Toronto, Canada: Pickleball Ladder League at Fairgrounds - C | 120254079153100019 |
| 92.17 | AI | SP_Fall2026_Jackpot_static | 120253673698680019 | Fall26_Phase0_NewCus_Moodyboy_August_2026_Statics | 120253673698650019 |
| 90.97 | 1x1 | W27_ALL_Moodyboy-FrozenManMeme_Video_v1 | 120254085966810019 | Manchester, CT: Pickleball Ladder League at Pickleball Kingd | 120254079138860019 |
| 87.57 | 1x1 | W27_ALL_Moodyboy-SocialLifeOnIce_Static_v1 | 120254086298610019 | Indianapolis, IN: Pickleball Ladder Leagues at IPC North & 3 | 120254086276010019 |
| 82.74 | 1x1 | W27_ALL_Moodyboy-FrozenManMeme_Video_v1 | 120254086123410019 | Charlotte, NC: Pickleball Ladder League at Pickleball Charlo | 120254079143010019 |
| 80.07 | chk | SP_May2026_Collage_Volleyball_1440x1440_static | 120254195145010019 | Chicago, IL: Indoor Sand Volleyball Ladder League at Players | 120254085223420019 |
| 78.99 | 1x1 | W27_ALL_Moodyboy-FrozenManMeme_Video_v1 | 120254081409820019 | Houston, TX: Pickleball Ladder League at TEMPO Padel & Pickl | 120254063647720019 |
| 78.37 | 1x1 | W27_ALL_Moodyboy-SocialLifeOnIce_Static_v1 | 120254085353600019 | Plymouth, MN: Pickleball Ladder League at Pure Pickleball |  | 120254063677370019 |
| 76.91 | 1x1 | W27_ALL_Moodyboy-FrozenManMeme_Video_v1 | 120254085254850019 | Lexington, KY: Pickleball Ladder League at Pickleball Kingdo | 120254063669380019 |
| 72.86 | 1x1 | W27_ALL_Moodyboy-FrozenManMeme_Video_v1 | 120254086296690019 | Indianapolis, IN: Pickleball Ladder Leagues at IPC North & 3 | 120254086276010019 |
| 66.72 | 1x1 | W27_ALL_Moodyboy-FrozenManMeme_Video_v1 | 120254086210750019 | Eagan, MN: Pickleball Ladder League at Chip's Pickleball Clu | 120254079149880019 |
| 65.92 | 1x1 | W27_ALL_Moodyboy-FrozenManMeme_Video_v1 | 120254085882740019 | Houston, TX: Pickleball Ladder League at Pickleball Social - | 120254079131740019 |
| 61.31 | 1x1 | W27_ALL_Moodyboy-FrozenManMeme_Video_v1 | 120254084995900019 | Winter27_Chicago_Chicago_P0 | 120254063598850019 |
| 60.19 | 1x1 | W27_ALL_Moodyboy-SocialLifeOnIce_Static_v1 | 120254081466140019 | Atlanta, GA: Pickleball Ladder League at ITP Pickleball Club | 120254063649860019 |
| 59.17 | 1x1 | W27_ALL_Moodyboy-SocialLifeOnIce_Static_v1 | 120254063635020019 | Troutdale, OR: Pickleball Ladder League at East County Pickl | 120254063602840019 |
| 58.39 | AI | phrase6-socialbynature_static | 120253673699100019 | Fall26_Phase0_NewCus_Phrase_Statics | 120253673698710019 |
| 57.10 | 1x1 | W27_ALL_Moodyboy-FrozenManMeme_Video_v1 | 120254086315570019 | Winter27_Colorado_Denver_P0 | 120254063670370019 |
| 56.33 | 1x1 | W27_ALL_Moodyboy-SocialLifeOnIce_Static_v1 | 120254086291580019 | Philadelphia, PA: Pickleball Ladder League at Ballers | Earl | 120254079476680019 |
| 56.26 | 1x1 | W27_ALL_Moodyboy-SocialLifeOnIce_Static_v1 | 120254084985080019 | Winston-Salem, NC: Pickleball Ladder League at Little Creek  | 120254063654400019 |
| 54.54 | 1x1 | W27_ALL_Moodyboy-SocialLifeOnIce_Static_v1 | 120254085277530019 | Plano, TX: Pickleball Ladder League at Pickleball Kingdom |  | 120254063671370019 |
| 52.29 | 1x1 | W27_ALL_Moodyboy-SocialLifeOnIce_Static_v1 | 120254061261620019 | Denver, CO: Pickleball Ladder League at Mile Hi Pickleball | | 120254060418630019 |
| 51.36 | AI | SP_Sept2026_FallBucketList_Pickleball_video | 120253767862340019 | Fall26_Phase0_Regional_National(remainder) | 120252824399960019 |
| 48.94 | 1x1 | W27_ALL_Moodyboy-FrozenManMeme_Video_v1 | 120254085327120019 | West Bloomfield, MI: Pickleball Ladder League at PickleRage  | 120254063675830019 |
| 48.20 | 1x1 | W27_ALL_Moodyboy-FrozenManMeme_Video_v1 | 120254085022680019 | Centerville, OH: Pickleball Ladder League at PickleRage | Ea | 120254063657100019 |
| 46.19 | 1x1 | W27_ALL_Moodyboy-SocialLifeOnIce_Static_v1 | 120254085896080019 | Nashville, TN: Pickleball Ladder League at The Courts of Wes | 120254079133750019 |
| 45.60 | 1x1 | W27_ALL_Moodyboy-SocialLifeOnIce_Static_v1 | 120254086081210019 | Cedar Knolls, NJ: Pickleball Ladder League at Home Court Pic | 120254079140200019 |
| 44.86 | 1x1 | W27_ALL_Moodyboy-FrozenManMeme_Video_v1 | 120254086124740019 | Hyde Park, MA: Pickleball Ladder League at Boston Pickle Clu | 120254086120620019 |
| 44.14 | 1x1 | W27_ALL_Moodyboy-SocialLifeOnIce_Static_v1 | 120254085178990019 | Winter27_NYMetro_NYC_P0 | 120254063633330019 |
| 43.29 | 1x1 | W27_ALL_Moodyboy-SocialLifeOnIce_Static_v1 | 120254085188840019 | Cincinnati, OH: Pickleball Ladder League at Pickleball Kingd | 120254063667200019 |
| 41.98 | 1x1 | W27_ALL_Moodyboy-SocialLifeOnIce_Static_v1 | 120254086125650019 | Hyde Park, MA: Pickleball Ladder League at Boston Pickle Clu | 120254086120620019 |
| 41.41 | 1x1 | W27_ALL_Moodyboy-FrozenManMeme_Video_v1 | 120254086316310019 | Salt Lake City, UT: Pickleball Ladder League at Sports Mall  | 120254079491990019 |
| 40.93 | AI | DiffSkillLevels_Video | 120253844672140019 | Darling Harbour, AUS: Pickleball Ladder League at House of P | 120253844465920019 |
| 40.59 | 1x1 | W27_ALL_Moodyboy-FrozenManMeme_Video_v1 | 120254085964180019 | Winter27_DCBaltimore_Baltimore_P0 | 120254063650350019 |
| 40.44 | 1x1 | W27_ALL_Moodyboy-FrozenManMeme_Video_v1 | 120254086189030019 | Winter27_Phoenix_Phoenix_P0 | 120254063660360019 |
| 39.81 | 1x1 | W27_ALL_Moodyboy-FrozenManMeme_Video_v1 | 120254102934930019 | San Francisco, CA: Pickleball Ladder League at Bay Padel - T | 120254102934900019 |
| 37.40 | 1x1 | W27_ALL_Moodyboy-SocialLifeOnIce_Static_v1 | 120254086212370019 | Mundelein, IL: Pickleball Ladder League at FLICKS Pickleball | 120254086211170019 |
| 34.32 | 1x1 | W27_ALL_Moodyboy-SocialLifeOnIce_Static_v1 | 120254060479530019 | Pinellas Park, FL: Pickleball Ladder League at Pickleball Ki | 120254060416370019 |
| 33.09 | 1x1 | W27_ALL_Moodyboy-SocialLifeOnIce_Static_v1 | 120254086171380019 | Colorado Springs, CO: Pickleball Ladder League at Springs Pi | 120254079148540019 |
| 29.99 | 1x1 | W27_ALL_Moodyboy-SocialLifeOnIce_Static_v1 | 120254086185530019 | Holyoke, MA: Pickleball Ladder League at Pickleball Kingdom  | 120254086181200019 |
| 29.55 | 1x1 | W27_ALL_Moodyboy-FrozenManMeme_Video_v1 | 120254081464950019 | Winter27_Texas_DFW_P0 | 120254063597690019 |
| 28.98 | 1x1 | W27_ALL_Moodyboy-FrozenManMeme_Video_v1 | 120254061313140019 | Hamilton, NJ: Pickleball Ladder League at Pickleball Kingdom | 120254060419490019 |
| 28.79 | 1x1 | W27_ALL_Moodyboy-FrozenManMeme_Video_v1 | 120254061273350019 | Denver, CO: Pickleball Ladder League at Mile Hi Pickleball | | 120254060418630019 |
| 27.84 | 1x1 | W27_ALL_Moodyboy-FrozenManMeme_Video_v1 | 120254060486450019 | Pinellas Park, FL: Pickleball Ladder League at Pickleball Ki | 120254060416370019 |
| 27.45 | 1x1 | W27_ALL_Moodyboy-SocialLifeOnIce_Static_v1 | 120254085947000019 | Salt Lake City, UT: Pickleball Ladder League at Club Pickleb | 120254079137190019 |
| 26.24 | 1x1 | W27_ALL_Moodyboy-SocialLifeOnIce_Static_v1 | 120254086235010019 | Louisville, KY: Pickleball Ladder League at Play Pickleball  | 120254079151200019 |
| 25.85 | 1x1 | W27_ALL_Moodyboy-FrozenManMeme_Video_v1 | 120254086213110019 | Mundelein, IL: Pickleball Ladder League at FLICKS Pickleball | 120254086211170019 |
| 25.45 | AI | SP_Sept2026_StayForFriends_Pickleball_static | 120253767862440019 | Fall26_Phase0_Regional_Canada | 120252634833210019 |
| 24.89 | 1x1 | W27_ALL_Moodyboy-SocialLifeOnIce_Static_v1 | 120254085143750019 | Winter27_Carolinas_Raleigh_P0 | 120254063614730019 |
| 23.35 | 1x1 | W27_ALL_Moodyboy-FrozenManMeme_Video_v1 | 120254086006100019 | Hendersonville, TN: Pickleball Ladder League at Pickleball K | 120254085994930019 |
| 21.26 | 1x1 | W27_ALL_Moodyboy-SocialLifeOnIce_Static_v1 | 120254086238120019 | Louisville, KY: Pickleball Ladder Leagues at Play Pickleball | 120254086235290019 |
| 20.85 | 1x1 | W27_ALL_Moodyboy-SocialLifeOnIce_Static_v1 | 120254086128820019 | Winter27_Boston_Boston_P0 | 120254063656080019 |
| 20.61 | AI | SP_Sept2026_FallBucketList_Pickleball_video | 120253768151420019 | North Aurora, IL: Pickleball Ladder League at Pickleball Kin | 120253728392320019 |
| 20.45 | AI | SP_Sept2026_CatMeme_Pickleball_static | 120253767862320019 | Fall26_Phase0_Regional_National(remainder) | 120252824399960019 |
| 20.07 | 1x1 | W27_ALL_Moodyboy-SocialLifeOnIce_Static_v1 | 120254085132820019 | Greater Philadelphia, PA: Pickleball Ladder League at Forwar | 120254063660630019 |
| 19.31 | 1x1 | W27_ALL_Moodyboy-SocialLifeOnIce_Static_v1 | 120254085126380019 | Winter27_Carolinas_Charlotte_P0 | 120254063611660019 |
| 18.38 | 1x1 | W27_ALL_Moodyboy-SocialLifeOnIce_Static_v1 | 120254086343000019 | Winter27_PortlandOR_PortlandOR_P0 | 120254063672270019 |
| 18.15 | 1x1 | W27_ALL_Moodyboy-SocialLifeOnIce_Static_v1 | 120254086078810019 | Hendersonville, TN: Pickleball Ladder League at Pickleball K | 120254085994930019 |
| 17.59 | 1x1 | W27_ALL_Moodyboy-FrozenManMeme_Video_v1 | 120254086236400019 | Louisville, KY: Pickleball Ladder Leagues at Play Pickleball | 120254086235290019 |
| 16.42 | 1x1 | W27_ALL_Moodyboy-SocialLifeOnIce_Static_v1 | 120254088838010019 | Winter27_Canada_Vancouver_P0 | 120254079136600019 |
| 16.32 | chk | SP_April_Volleyball_ChecklistAd | 120254195189890019 | Chicago, IL: Indoor Sand Volleyball Ladder League at Players | 120254085223420019 |
| 15.95 | 1x1 | W27_ALL_Moodyboy-SocialLifeOnIce_Static_v1 | 120254086340140019 | Plymouth, MN: Pickleball Ladder League at PickleX | Early Wi | 120254079493750019 |
| 15.91 | AI | SP_Sept2026_LastCall_Pickleball_video | 120253657682270019 | Fall26_Phase0_Regional_Canada | 120252634833210019 |
| 15.49 | 1x1 | W27_ALL_Moodyboy-FrozenManMeme_Video_v1 | 120254086428610019 | Winter27_Canada_Toronto_P0 | 120254079135000019 |
| 14.92 | AI | SP_Sept2026_DigitalCamera_Pickleball_video | 120253768151430019 | North Aurora, IL: Pickleball Ladder League at Pickleball Kin | 120253728392320019 |
| 14.61 | 1x1 | W27_ALL_Moodyboy-SocialLifeOnIce_Static_v1 | 120254061311740019 | Hamilton, NJ: Pickleball Ladder League at Pickleball Kingdom | 120254060419490019 |
| 12.85 | 1x1 | W27_ALL_Moodyboy-FrozenManMeme_Video_v1 | 120254085196250019 | Winter27_Ohio_Cincinnati_P0 | 120254063635080019 |
| 12.14 | 1x1 | W27_ALL_Moodyboy-FrozenManMeme_Video_v1 | 120254086184620019 | Holyoke, MA: Pickleball Ladder League at Pickleball Kingdom  | 120254086181200019 |
| 11.68 | 1x1 | W27_ALL_Moodyboy-SocialLifeOnIce_Static_v1 | 120254085941720019 | Winter27_Philadelphia_Philadelphia_P0 | 120254063648120019 |
| 11.17 | 1x1 | W27_ALL_Moodyboy-FrozenManMeme_Video_v1 | 120254086086380019 | Winter27_Atlanta_Atlanta_P0 | 120254063654170019 |
| 10.94 | AI | DiffSkillLevels_Video | 120253573219530019 | Fall26_Phase0_Regional_Canada | 120252634833210019 |
| 8.07 | AI | SP_Sept2026_Toggle_Pickleball_video | 120253767862350019 | Fall26_Phase0_Regional_National(remainder) | 120252824399960019 |
| 8.02 | 1x1 | W27_ALL_Moodyboy-FrozenManMeme_Video_v1 | 120254086340790019 | Buffalo, NY: Pickleball Ladder League at Pickleball Island | | 120254086337950019 |
| 7.35 | AI | SP_Sept2026_DigitalCamera_Pickleball_video | 120253767862410019 | Fall26_Phase0_Regional_National(remainder) | 120252824399960019 |
| 6.51 | 1x1 | W27_ALL_Moodyboy-FrozenManMeme_Video_v1 | 120254085899570019 | Winter27_Indiana_Indianapolis_P0 | 120254063646370019 |
| 5.71 | 1x1 | W27_ALL_Moodyboy-SocialLifeOnIce_Static_v1 | 120254085881050019 | Winter27_Ohio_Dayton_P0 | 120254063643920019 |
| 4.70 | 1x1 | W27_ALL_Moodyboy-SocialLifeOnIce_Static_v1 | 120254085029060019 | Winter27_Florida_Tampa_P0 | 120254063606630019 |
| 4.35 | AI | SP_Sept2026_Toggle_Pickleball_video | 120253768151450019 | North Aurora, IL: Pickleball Ladder League at Pickleball Kin | 120253728392320019 |
| 4.25 | 1x1 | W27_ALL_Moodyboy-SocialLifeOnIce_Static_v1 | 120254081474300019 | Winter27_Texas_Houston_P0 | 120254063598200019 |
| 4.02 | 1x1 | W27_ALL_Moodyboy-FrozenManMeme_Video_v1 | 120254086244100019 | Winter27_Tennessee_Nashville_P0 | 120254063665360019 |
| 4.00 | 1x1 | W27_ALL_Moodyboy-SocialLifeOnIce_Static_v1 | 120254086342550019 | Buffalo, NY: Pickleball Ladder League at Pickleball Island | | 120254086337950019 |
| 3.09 | 1x1 | W27_ALL_Moodyboy-FrozenManMeme_Video_v1 | 120254084928300019 | Winter27_California_SF_P0 | 120254063603650019 |
| 1.89 | 1x1 | W27_ALL_Moodyboy-FrozenManMeme_Video_v1 | 120254085157840019 | Winter27_Carolinas_Triad_P0 | 120254063616590019 |
| 1.82 | AI | SP_Sept2026_DigitalCamera_Pickleball_video | 120253844643490019 | Darling Harbour, AUS: Pickleball Ladder League at House of P | 120253844465920019 |
| 1.37 | 1x1 | W27_ALL_Moodyboy-SocialLifeOnIce_Static_v1 | 120254086220230019 | Winter27_TwinCities_TwinCities_P0 | 120254063662010019 |
| 1.03 | 1x1 | W27_ALL_Moodyboy-SocialLifeOnIce_Static_v1 | 120254086276490019 | Winter27_Colorado_ColoradoSprings_P0 | 120254063668860019 |
| 0.88 | AI | SP_Sept2026_CatMeme_Pickleball_static | 120253767862460019 | Fall26_Phase0_Regional_Canada | 120252634833210019 |
| 0.36 | AI | SP_Sept2026_The76_Pickleball_static | 120253657682250019 | Fall26_Phase0_Regional_Canada | 120252634833210019 |
| 0.28 | AI | SP_Sept2026_DigitalCamera_Pickleball_video | 120253767862490019 | Fall26_Phase0_Regional_Canada | 120252634833210019 |
| 0.23 | AI | SP_Sept2026_FallBucketList_Pickleball_video | 120253767862480019 | Fall26_Phase0_Regional_Canada | 120252634833210019 |
| 0.20 | AI | SP_Sept2026_Toggle_Pickleball_video | 120253767862470019 | Fall26_Phase0_Regional_Canada | 120252634833210019 |
| 0.07 | 1x1 | W27_ALL_Moodyboy-FrozenManMeme_Video_v1 | 120254086370090019 | Winter27_Louisville_Louisville_P0 | 120254063676440019 |
| 0.07 | AI | SP_July2026_Loading_static | 120253235360420019 | Fall26_Phase0_NewCus_Moodyboy-Fall_season_July_2026_statics | 120253235360320019 |

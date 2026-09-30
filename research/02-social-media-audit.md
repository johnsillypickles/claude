# Silly Pickles: Social Media Audit

Prepared 2026-09-30. Window analyzed: 2025-10-01 to 2026-09-29 (last 12 months).

## 1. What the business is

Silly Pickles (sillypickles.com, Shopify Plus store, support@sillypickles.com) runs social, LGBTQ-owned adult recreational pickleball leagues in multiple US cities, sold as 8-week seasonal "Dynamic Ladder League" registrations (for example Denver at Mile Hi Pickleball, Thornton and Wichita at Chicken N Pickle, Albuquerque, Las Vegas, Texas, California, Louisiana, Salt Lake City, Clackamas OR). It has expanded into volleyball (Chicago) and sells branded paddles ("Silly Paddles" such as The OG, Check Mate, Main Squeeze, Retro Waves, What The Duck, per the theme cart settings). The Google Ads account and TikTok handle use the name "Silly Sports", which suggests (inference) a multi-sport umbrella brand is emerging.

How this was confirmed: sillypickles.com itself is blocked by this environment's network egress proxy, so I could not fetch the site directly. Confirmation came from (a) the Shopify connector (store name "Silly Pickles", domain sillypickles.com), (b) web search results pointing to sillypickles.com collection and product pages for league cities, and third-party listings (Las Vegas Pride, LGBTQ Colorado, Visit Wichita, Eventbrite) describing "the world's funnest LGBTQ-owned pickleball leagues", and (c) ad copy in the Meta creative data.

## 2. Data sources: what was checked and what came back

| Source | Status | What I got |
|---|---|---|
| Windsor.ai | Connected: Google Ads (Silly Sports), Shopify, TikTok Ads (Silly Pickles Ad Account). NOT connected: Instagram, Facebook Organic, TikTok Organic, YouTube, LinkedIn Organic, Meta Ads | TikTok paid ad totals per ad (spend, impressions, clicks, paid likes, comments, shares, follows, profile visits, conversions) |
| Lebesgue | Shop 1307999470, Ultimate AI plan, eligible. Facebook Ads, Google Ads, TikTok Ads, Klaviyo, GA4 connected | Top 100 of 2,433 Meta ad creatives by spend, with copy, CTA, landing page, spend, impressions, clicks, purchases, ROAS |
| Klaviyo (brand social group, read only) | Connected | Official social links: Facebook, Instagram, TikTok |
| Shopify (theme settings, read only) | Connected | Same three social links in the live theme footer config; Twitter, Pinterest, LinkedIn, YouTube fields are empty |
| Public web | sillypickles.com, instagram.com, eventbrite.com, lasvegaspride.org, lgbtqcolorado.org, visitwichita.com all blocked by egress proxy | Only search-result snippets; no follower counts or post data |

No write actions were called on any system.

**Bottom line on organic data: none was available.** No organic post-level data (captions, post dates, reach, likes, saves, follower counts, follower growth) exists in any connected source, and the public profiles could not be fetched. Every number below is from paid advertising. I did not estimate or invent organic figures.

**Access needed for a true organic audit:**
- Windsor.ai: connect `instagram` (Instagram Business account linked to the Facebook Page), `facebook_organic` (Page admin), `tiktok_organic` (TikTok Business account login for @sillysports). Optional: `youtube`, `linkedin_organic` if those accounts exist.
- Or: a CSV export from Meta Business Suite Insights and TikTok Analytics (last 12 months, post level).
- Or: allow egress to instagram.com / tiktok.com / facebook.com for a public-profile review (follower counts and visible post counts only; no reach data).

## 3. Channel inventory

| Platform | Handle / URL (source: Klaviyo + Shopify theme) | Followers | Posting frequency | Last post | Notes |
|---|---|---|---|---|---|
| Instagram | instagram.com/sillypickles | Unavailable | Unavailable | Unavailable | Not connected to Windsor; profile blocked |
| Facebook | facebook.com/p/Silly-Pickles-61565645024652/ | Unavailable | Unavailable | Unavailable | "/p/" URL with numeric ID means no vanity username is set. Inference: the Page ID range suggests creation around 2024 |
| TikTok | tiktok.com/@sillysports | Unavailable organically. Paid ads drove 984 paid follows in the window (see below) | Unavailable | Unavailable | Handle is "sillysports", not "sillypickles" |
| YouTube | None linked | n/a | n/a | n/a | Theme field empty |
| LinkedIn | None linked | n/a | n/a | n/a | Theme field empty |
| Pinterest | None linked | n/a | n/a | n/a | Theme field empty; Pinterest Ads disconnected in Lebesgue |
| X / Twitter | None linked | n/a | n/a | n/a | Theme field empty |

## 4. Engagement rate definitions

Because only paid data is available, two formulas are used:

- **TikTok paid engagement rate (ER)** = (paid likes + paid comments + paid shares) / impressions x 100
- **Meta click engagement rate (CTR)** = link clicks / impressions x 100. Lebesgue's Meta creative feed does not include likes, comments, shares or saves, so CTR is the only engagement signal available for Meta. It is a proxy, not a social engagement rate.

Supporting efficiency metrics: CPM = spend / impressions x 1000; ROAS = platform-reported purchase value / spend; CAC = spend / purchases. Purchases and ROAS are as reported by the ad platform (Meta or TikTok attribution), not Shopify-verified.

## 5. TikTok paid ads (Windsor.ai), all ads in window

Only 7 ads had delivery, so a top 10 / bottom 10 split is not possible. All are ranked by ER.

| Rank | Ad name | Spend | Impressions | Likes | Comments | Shares | ER math | ER | CTR | Paid follows | Conversions | Cost per conversion |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | You-and-bestie_Video | $13.72 | 2,304 | 6 | 0 | 0 | 6 / 2,304 | 0.260% | 0.52% | 1 | 0 | n/a |
| 2 | POV-DumpHim_Video | $18.17 | 2,605 | 4 | 1 | 0 | 5 / 2,605 | 0.192% | 0.81% | 0 | 0 | n/a |
| 3 | TommyTalkingVideo-Feb2026-REVAMP | $16,737.98 | 2,139,728 | 3,438 | 263 | 143 | 3,844 / 2,139,728 | 0.180% | 0.95% | 307 | 255 | $65.64 |
| 4 | TommyTalkingVideo-Fall2026-Boo-v2 | $16,098.74 | 2,279,896 | 3,574 | 205 | 152 | 3,931 / 2,279,896 | 0.172% | 0.95% | 330 | 410 | $39.27 |
| 5 | WiiSport_Video | $8,596.70 | 1,248,466 | 1,929 | 102 | 59 | 2,090 / 1,248,466 | 0.167% | 0.92% | 174 | 146 | $58.88 |
| 6 | DiffSkillLevels_Video | $9,079.97 | 1,467,297 | 1,841 | 146 | 75 | 2,062 / 1,467,297 | 0.141% | 0.85% | 172 | 221 | $41.09 |
| 7 | TommyTalkingVideo-Fall2026-Leaves_video | $24.01 | 3,190 | 2 | 0 | 0 | 2 / 3,190 | 0.063% | 0.38% | 0 | 1 | $24.01 |

Totals: $50,569.29 spend, 7,143,486 impressions, 11,940 engagements (10,794 + 717 + 429), ER = 11,940 / 7,143,486 = 0.167%. CTR = 65,920 / 7,143,486 = 0.92%. Cost per conversion = $50,569.29 / 1,033 = $48.95. Three "Copy 1 of" duplicates had zero delivery.

Notes:
- Ranks 1, 2 and 7 have under 3,300 impressions each. Their ERs are not statistically meaningful.
- Among the four scaled ads, ER is tightly clustered (0.141% to 0.180%), but cost per conversion varies from $39.27 to $65.64. The seasonal "Boo" (Halloween-themed, inference from name) founder/host talking-head video converted best. The skill-level explainer (DiffSkillLevels) had the lowest ER but the second-best cost per conversion, which suggests the "play at your level" message pulls buyers even when it pulls fewer likes (inference).
- "Tommy" talking-head videos account for $32,860.73 of $50,569.29 (65.0%) of TikTok spend. Inference: a recurring on-camera person is the backbone of TikTok creative.
- Captions (ad_text) came back empty from Windsor for every TikTok ad, so caption analysis is not possible for TikTok.

## 6. Meta paid creatives (Lebesgue)

Scope: top 100 of 2,433 creatives by spend in the window. These 100 account for $650,181.62 spend, 36,967,795 impressions, 410,026 clicks, 10,976 platform-reported purchases and $1,753,190.14 platform-reported revenue (blended ROAS 1,753,190.14 / 650,181.62 = 2.70). All 100 are prospecting ("acquisition" target). The remaining 2,333 creatives were not pulled (response size limit), so conclusions apply to the top 100 only.

Ranking set: the 89 creatives with spend of at least $3,000, ranked by CTR.

### Top 10 Meta creatives by CTR

| Ad ID | Format | Headline | Primary text (first 80 chars) | Clicks / Impr. | CTR | Spend | Purchases | ROAS |
|---|---|---|---|---|---|---|---|---|
| 120242334987470019 | dynamic | The World's Funnest Pickleball League - All Levels Welc... | Never tried pickleball? This Is your sign! Ladder league = play at your level | 44,116 / 1,568,963 | 2.81% | $25,765 | 531 | 3.39 |
| 120243292459350019 | dynamic | The World's Funnest Pickleball League - All Levels Welc... | Never tried pickleball? This Is your sign! ... | 6,014 / 222,569 | 2.70% | $3,883 | 49 | 2.11 |
| 120238995774110019 | dynamic | The World's Funnest Pickleball League - All Levels Welc... | psst...hey there... you live literally 20 minutes away from one of our leagues | 17,160 / 647,097 | 2.65% | $14,227 | 145 | 1.74 |
| 120240907375560019 | dynamic | The World's Funnest Pickleball League - All Levels Welc... | psst...hey there... you live literally 20 minutes away ... | 6,886 / 261,599 | 2.63% | $4,706 | 64 | 2.12 |
| 120243726276310019 | dynamic | The World's Funnest Pickleball League - All Levels Welc... | Never tried pickleball? This Is your sign! ... | 3,749 / 155,360 | 2.41% | $3,146 | 23 | 1.33 |
| 120238995774150019 | dynamic | The World's Funnest Pickleball League - All Levels Welc... | psst...hey there... you live literally 20 minutes away ... | 22,928 / 1,025,215 | 2.24% | $19,551 | 207 | 1.80 |
| 120247048829790019 | dynamic | Hey Clackamas we're coming for you! | Never tried pickleball? This Is your sign! ... | 2,724 / 133,690 | 2.04% | $3,091 | 28 | 1.30 |
| 120252827506340019 | dynamic (video) | Pickleball, But Make It Social | Hey Colorado - Fall signups are open! ... | 3,560 / 176,895 | 2.01% | $3,743 | 62 | 2.93 |
| 120252826801120019 | dynamic (video) | Pickleball, But Make It Social | Hey California - Fall signups are open! ... | 6,440 / 325,427 | 1.98% | $7,468 | 73 | 1.70 |
| 120244223423110019 | dynamic (video) | The World's Funnest Pickleball League - All Levels Welc... | Never tried pickleball? This Is your sign! ... | 5,946 / 303,379 | 1.96% | $4,574 | 57 | 2.08 |

### Bottom 10 Meta creatives by CTR

| Ad ID | Format | Headline | Primary text (first 80 chars) | Clicks / Impr. | CTR | Spend | Purchases | ROAS |
|---|---|---|---|---|---|---|---|---|
| 120239641008580019 | carousel | Your social life called... | Spots fill up fast! Don't miss out on the best opportunity to get social ... | 4,339 / 749,282 | 0.58% | $12,658 | 206 | 2.64 |
| 120252827506560019 | carousel | (five star emoji) | Fall signups are open! ... | 1,700 / 302,827 | 0.56% | $5,156 | 137 | 4.25 |
| 120253418373620019 | dynamic | Pickleball, But Make It Social | The World's Funnest Pickleball League is starting soon! All Levels Welcome! | 1,663 / 322,540 | 0.52% | $5,621 | 83 | 2.35 |
| 120247179318470019 | dynamic | Athletic? Debatable. Fun? Guaranteed. | WANTED: Athletes. Non-athletes. People who want something fun to do on weeknights... | 1,599 / 318,559 | 0.50% | $5,253 | 95 | 2.88 |
| 120252829416510019 | dynamic | Pickleball, But Make It Social | Less scrolling, more serving. Our Dynamic Ladder League matches you ... | 4,441 / 905,577 | 0.49% | $15,918 | 352 | 3.38 |
| 120251745756850019 | carousel | (five star emoji) | Summer League Signups are Open! ... | 1,305 / 277,936 | 0.47% | $5,266 | 19 | 0.59 |
| 120251745313010019 | dynamic | Pickleball, but make It social. | The World's Funnest Pickleball League is starting soon! ... | 838 / 180,976 | 0.46% | $4,171 | 10 | 0.35 |
| 120252891465480019 | dynamic | Join Solo. Play Your Level. | Silly Pickles volleyball league is here! Good news: you don't have to be good... | 1,302 / 283,545 | 0.46% | $4,595 | 36 | 1.13 |
| 120252829416520019 | dynamic | Pickleball, But Make It Social | Less scrolling, more serving. ... | 1,659 / 397,677 | 0.42% | $6,473 | 180 | 4.26 |
| 120249899150430019 | dynamic | Pickleball, but make It social. | The World's Funnest Pickleball League is starting soon! ... | 1,924 / 471,472 | 0.41% | $7,761 | 170 | 3.43 |

Key observation: **CTR and ROAS are decoupled.** The "psst... 20 minutes away" curiosity hook is in the top 6 by CTR but returns ROAS 1.74 to 2.12. The "Less scrolling, more serving" hook is in the bottom 10 by CTR yet returns ROAS 3.38 and 4.26. Optimizing for clicks or likes alone would pick the wrong creative.

### Meta pattern tables (top 100 creatives, aggregated)

Math per group: CTR = sum clicks / sum impressions; ROAS = sum revenue / sum spend; CAC = sum spend / sum purchases.

By format

| Format | Count | Spend | CTR | CPM | Purchases | ROAS | CAC |
|---|---|---|---|---|---|---|---|
| Dynamic, static image | 56 | $378,261 | 1.20% | $17.10 | 6,408 | 2.68 | $59.03 |
| Dynamic, video | 23 | $141,053 | 1.26% | $19.50 | 2,329 | 2.70 | $60.56 |
| Carousel | 20 | $127,809 | 0.70% | $17.19 | 2,174 | 2.74 | $58.79 |
| Single image | 1 | $3,058 | 0.95% | $16.75 | 65 | 3.34 | $47.05 |

Format barely moves ROAS (2.68 to 2.74). Carousels get roughly half the CTR of dynamic ads for the same return.

By hook / message (grouped by opening phrase)

| Hook | Count | Spend | CTR | Purchases | ROAS | CAC |
|---|---|---|---|---|---|---|
| "...is starting soon! All Levels Welcome!" | 26 | $176,687 | 0.93% | 3,472 | 3.12 | $50.89 |
| "Fall signups are open!" | 12 | $87,214 | 1.12% | 1,658 | 3.08 | $52.60 |
| "Less scrolling, more serving" | 8 | $62,450 | 0.68% | 1,152 | 2.87 | $54.21 |
| "Your social life called..." | 4 | $22,019 | 0.72% | 383 | 2.86 | $57.49 |
| "Never tried pickleball? This is your sign!" | 13 | $76,766 | 2.04% | 1,320 | 2.76 | $58.16 |
| "WANTED: ..." | 2 | $10,712 | 0.61% | 174 | 2.64 | $61.56 |
| "Summer League Signups are Open!" | 11 | $74,672 | 0.71% | 1,144 | 2.48 | $65.27 |
| "A resolution you'll actually stick to" (New Year) | 4 | $26,200 | 0.96% | 325 | 2.04 | $80.61 |
| "psst... 20 minutes away" | 3 | $38,484 | 2.43% | 416 | 1.82 | $92.51 |
| Chicago volleyball ("Wanna meet new friends in Chicago...") | 3 | $11,107 | 1.45% | 98 | 0.94 | $113.34 |
| "20% Off ... code SUMMERBALL20" | 3 | $11,286 | 0.81% | 43 | 0.56 | $262.46 |

By CTA button

| CTA | Count | Spend | CTR | ROAS | CAC |
|---|---|---|---|---|---|
| See Details | 5 | $39,284 | 1.19% | 4.06 | $39.01 |
| Sign Up | 84 | $532,998 | 1.02% | 2.73 | $58.49 |
| Learn More | 11 | $77,901 | 1.70% | 1.80 | $90.90 |

By landing page

| Landing page | Count | Spend | CTR | ROAS | CAC |
|---|---|---|---|---|---|
| Homepage | 16 | $138,544 | 0.79% | 3.16 | $49.73 |
| /collections (all leagues) | 51 | $369,309 | 1.21% | 2.96 | $54.30 |
| State or city collection | 12 | $50,584 | 1.34% | 1.75 | $96.72 |
| Single product (one league) | 20 | $88,056 | 1.00% | 1.47 | $103.23 |
| /pages/pickleball-leagues-texas-houston | 1 | $3,689 | 0.95% | 0.56 | $283.74 |

Inference: sending people to a browse page (homepage or all collections) roughly halves CAC versus sending them to a single city or league. One explanation is that a prospect clicking a geo ad may not be near that specific league and bounces, while a browse page lets them find the closest one.

## 7. Brand voice and visuals

Voice (from ad copy; organic captions not available):
- Consistent and distinctive: playful, self-deprecating, inclusive. Recurring lines: "The World's Funnest Pickleball League", "Pickleball, but make it social", "All Levels Welcome", "Athletic? Debatable. Fun? Guaranteed.", "Less scrolling, more serving", "Your social life called...". Cowboy and star emojis recur.
- Minor inconsistencies: random title case ("Is", "It" capitalized mid-sentence, for example "This Is your sign", "Pickleball, but make It social."), the same headline appearing as "Pickleball, But Make It Social" and "Pickleball, but make It social.", and "funnest" versus "funnest ever". Small, but visible across a lot of spend.
- The LGBTQ-owned identity, which is prominent on third-party listings, does not appear in any of the top 100 Meta creatives' copy. Inference: the core community differentiator is not being used in paid social copy (it may appear in visuals, which I could not see).

Visuals (from the Shopify theme settings only; I could not view post images):
- Palette: navy #201747 text and buttons, gold #ffb81c accent and highlight, orange #d86018 sale, slate #55728f borders, mint #8fd6bd shadow. Font: Poppins throughout. Logo file: "Silly_Pickles_Primary_Logo_RGB_1.png".
- Whether social posts use this palette consistently could not be checked.

Naming consistency:
- Instagram @sillypickles, TikTok @sillysports, Facebook has no vanity name, Google Ads account "Silly Sports", volleyball sold under "Silly Pickles volleyball league". The brand is split between two names across channels.

## 8. Gaps

Confirmed from data:
- **No organic social measurement.** Instagram, Facebook Organic and TikTok Organic are not connected to Windsor.ai, so there is no follower, reach or post tracking.
- **Handle mismatch:** TikTok is @sillysports while Instagram is @sillypickles. People who search "silly pickles" on TikTok may not find the account (inference).
- **Facebook Page has no vanity URL** (facebook.com/p/Silly-Pickles-61565645024652/).
- **No YouTube, LinkedIn, Pinterest or X** linked in the site theme. YouTube Shorts is the obvious missing short-video channel given the TikTok video library (inference). LinkedIn could reach corporate team-building buyers (inference).
- **Discount-led creative fails:** SUMMERBALL20 ads ROAS 0.56, CAC $262.46.
- **Volleyball expansion creative is underperforming:** ROAS 0.94 to 1.13 versus 2.70 blended.
- **Single-league and city landing pages underperform** browse pages (CAC $96.72 to $103.23 vs $49.73 to $54.30).
- **TikTok captions are empty** in the data and TikTok has only 7 ads with delivery, 4 of them scaled. Creative depth on TikTok is thin compared with 2,433 Meta creatives.
- **Two affiliate apps are installed** (UpPromote and BixGrow). Not a social gap directly, but duplicate creator or affiliate tracking can muddle attribution for influencer content.

Could not be checked (needs access):
- Follower counts, posting frequency, last post date, inactive stretches
- Bio text and link-in-bio setup
- Whether organic posts use CTAs
- Best posting times and days
- Saves, shares and comments on organic posts
- User-generated content and community reposting

## 9. Recommended next steps

1. Connect Instagram, Facebook Organic and TikTok Organic in Windsor.ai (read access) and re-run this audit for the organic half.
2. Align handles: claim @sillypickles on TikTok, or deliberately move all channels to "Silly Sports", and set a Facebook vanity URL.
3. Judge creative on conversion efficiency, not CTR or likes. Scale "starting soon / All Levels Welcome", "Fall signups are open" and "Less scrolling, more serving". Retire "psst... 20 minutes away", New Year resolution and discount-code angles.
4. Test the "See Details" CTA more widely (ROAS 4.06 on 5 ads, $39,284 spend). Small sample, so treat it as a lead to test, not a conclusion.
5. Default the landing page to the homepage or all-collections page.
6. Rebuild volleyball creative using the pickleball pattern that works (skill-level matching, "join solo") before adding spend.
7. Add YouTube Shorts using existing TikTok videos.
8. Test copy that states the LGBTQ-owned, community-first identity.
9. Tidy capitalization in headlines.

## What did not work

- Discount-code creative (SUMMERBALL20): 3 ads, $11,286 spend, 43 purchases, ROAS 0.56, CAC $262.46.
- The "psst... you live 20 minutes away" curiosity hook: highest CTR (2.43%) but ROAS 1.82 and CAC $92.51. Clicks did not turn into signups.
- New Year "resolution" angle: ROAS 2.04, CAC $80.61.
- Chicago volleyball ads: ROAS 0.94 to 1.13, CAC $113.34 to $127.64.
- "Learn More" CTA: ROAS 1.80, CAC $90.90, compared with 2.73 for "Sign Up".
- Single-league product pages and city or state pages as ad destinations: CAC $103.23 and $96.72. The Houston page ad returned ROAS 0.56.
- Carousels: about half the CTR of dynamic ads (0.70% vs 1.20% to 1.26%) with no ROAS advantage.
- TikTok ad "TommyTalkingVideo-Feb2026-REVAMP": highest scaled-ad ER (0.180%) but the worst scaled cost per conversion ($65.64). Engagement did not predict signups.
- Measurement setup: no organic social data connected anywhere, and the public profiles and website were not reachable from this environment.
- Handle and name consistency: @sillypickles vs @sillysports vs "Silly Sports", and no Facebook vanity URL.

## What did work

- "...is starting soon! All Levels Welcome!" urgency plus inclusivity: 26 ads, $176,687 spend, ROAS 3.12, CAC $50.89. The single best scaled ad (120242337621410019, "Join the league today!") returned ROAS 4.72 on $19,148.
- "Fall signups are open!" seasonal launch copy: ROAS 3.08, CAC $52.60. The video version 120252827506520019 returned ROAS 4.95 on $13,455.
- "Less scrolling, more serving" / Dynamic Ladder explainer: low CTR but ROAS 2.87 overall and up to 4.26 on individual ads.
- "See Details" CTA: ROAS 4.06, CAC $39.01 (5 ads, small sample).
- Homepage and all-collections landing pages: CAC $49.73 and $54.30.
- TikTok seasonal talking-head video "TommyTalkingVideo-Fall2026-Boo-v2": 410 conversions at $39.27 each, 330 paid follows, ER 0.172%.
- TikTok "DiffSkillLevels_Video": second-best cost per conversion ($41.09) even with the lowest scaled ER. The "play at your level" message converts.
- TikTok paid activity also built the audience: 984 paid follows and 1,386 profile visits across $50,569 spend.
- Brand voice is distinctive and consistent across hundreds of creatives ("World's Funnest", "Athletic? Debatable. Fun? Guaranteed.").
- Social links are set up consistently in both Klaviyo and the Shopify theme (Facebook, Instagram, TikTok).

# Campaign structure in ЕПК (Единая перфоманс-кампания)

## Principles
- **One selling angle = one search campaign.** Different offers, margins or landing pages go to separate campaigns
  so that budgets and strategies can differ.
- **Brand separate.** Brand queries have different CPA and CTR; mixing them hides the real cost of new demand.
- **Search and РСЯ:** in ЕПК both live in one campaign and are split in reports by `AdNetworkType`. Separate them into
  two campaigns when budgets or goals differ, or when РСЯ eats the budget (look at the split first).
- **Group = one intent.** Phrases in a group share the landing page and the ad. High-frequency (ВЧ) phrases get their
  own groups; low-frequency (НЧ) phrases can be pooled. Watch «Мало показов» (RARELY_SERVED) groups and merge them.
- **Geo and schedule** match where and when the business can serve. Regions with different prices = different
  campaigns.
- **Retargeting and audiences** in their own campaign with their own goal.
- **B2B** and **B2C** separate: different goals and qualification.

## Naming
`<бренд|небренд>_<угол>_<сеть>_<гео>_<цель>`, e.g. `nb_okna-pvh_search_msk_lead`. Groups: `<интент>_<частотность>`.

## Minimal launch kit per campaign
- Metrica counter linked, **priority goals** chosen (a real lead or sale, not a page view), value set if known.
- UTM template on all links: `utm_source=yandex&utm_medium=cpc&utm_campaign={campaign_id}&utm_content={ad_id}&utm_term={keyword}`.
- Negative lists on three levels (see `negatives.md`).
- Per group: at least 1 combinatorial ad with 3–7 headlines, 2–3 texts, ≥ 4 sitelinks, ≥ 3 callouts, ≥ 3 images
  for РСЯ.
- Strategy and budget agreed with the client (see the `strategies` skill). Budget comes from the client only.
- Advertiser data for ОРД filled in.

## Launch sequence (from brief to draft)
1. Brief → 2. account and Metrica reconnaissance → 3. masks (roots) → 4. expansion from Wordstat and competitors →
5. clustering into groups and campaigns → 6. negatives and cross-minusing → 7. goals → 8. ads → 9. strategy →
10. checklist → upload **as a draft**. Each step writes an artefact to `direct-campaigns/<slug>/` and stops at a
gate where the marketer says «ОК».

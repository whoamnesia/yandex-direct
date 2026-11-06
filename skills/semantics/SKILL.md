---
name: semantics
description: 'astudio semantics for Yandex Direct: masks (roots) from the brief, expansion through Wordstat v2 and competitors, cleaning, clustering into groups by intent and frequency (ВЧ/СЧ/НЧ), match operators (! + "" [] () |), negative keywords on three levels, cross-minusing and weekly search-query mining - linted with keywords.py, decided by a human. Use for "семантика", "ключевые слова", "собрать ключи", "Wordstat", "минус-слова", "кросс-минусовка", "чистка поисковых запросов", "Yandex keywords".'
argument-hint: "[brief or list of roots] [region] [Wordstat access yes/no]"
---

# astudio · Semantics

`<root>` = two levels above this skill's base dir. Read `<root>/reference/negatives.md` and
`<root>/data/limits.json → keywords, negatives, operators, api.wordstat`.

## Steps
1. **Masks.** From the brief write 5–20 roots: product × action × qualifier («окна пвх», «пластиковые окна»,
   «остекление балкона»). Include synonyms, slang and transliteration: one root does not cover its synonyms.
2. **Expansion.** Wordstat v2 `topRequests` per mask and region (base
   `https://searchapi.api.cloud.yandex.net/v2/wordstat/`, key from env `YANDEX_SEARCH_API_KEY`). No access → ask the
   user for an export from wordstat.yandex.ru and note the skip. Never use `api.wordstat.yandex.net/v1`.
3. **Cleaning.** Remove what cannot convert (jobs, free, DIY, other cities, other products). Every removed query
   gives a candidate negative **word**.
4. **Clustering.** One group = one intent and one landing page. ВЧ phrases get their own group; НЧ pooled. Brand,
   competitors and informational intents separate. Max 200 phrases per group; aim for 5–30.
5. **Operators.** Default: phrases without operators plus negatives; `"..."` to stop long tails on ВЧ; `!` when the
   form changes meaning («тур» vs «туры» rarely does; «ремонт телефона» vs «ремонт телефонов» might);
   `+` for stop words that matter («+на дому»); `[]` when order matters (city pairs, «из … в …»).
6. **Negatives.** Three levels (account set, campaign, group). Single words, not queries. Then cross-minusing:
   `python3 <root>/scripts/keywords.py cross keywords.txt`; in ЕПК automatic cross-minusing may already be on.
7. **Lint.** `python3 <root>/scripts/keywords.py lint keywords.txt --negatives neg.txt --campaign-negatives camp.txt`.
   Fix every error (above all: negatives that block your own phrases).

## After launch (weekly)
Search-query report (Reports `SEARCH_QUERY_PERFORMANCE_REPORT`, last 180 days). For each irrelevant query: the
query as evidence, one negative word, the level where it goes. Converting queries become new phrases.

## Output
A table: campaign · group · phrase · operator · frequency (source, date) · landing page; negatives by level; a
list of what was skipped. Frequencies are Wordstat impressions, not a forecast of clicks.

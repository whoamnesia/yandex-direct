# Negative keywords (минус-слова)

## Three levels
1. **Account / shared set** (`negativekeywordsharedsets`): words irrelevant to the whole business — jobs, free,
   DIY, education, adult, competitors' trademarks where bidding on them is not intended.
2. **Campaign**: words irrelevant to this angle; for РСЯ, add placement exclusions separately.
3. **Group**: cross-minusing so that a query goes to the most specific group.

## Rules
- A negative is **one word** (or an unbreakable pair), not the full search query. Put the query in the evidence
  column, and the single word that makes it irrelevant in the list.
- Fix forms deliberately: `-!бесплатно` blocks only this form; `-бесплатно` blocks all forms.
- Never add a negative that matches a word of your own key phrase (`keywords.py lint` catches it).
- Limits: 4 096 characters per group and 20 000 per campaign, excluding spaces; ≤ 7 words per phrase.
- Mine search queries weekly after launch (Reports `SEARCH_QUERY_PERFORMANCE_REPORT`, 180 days available). A query is
  irrelevant only if it cannot convert: decide by meaning, not by «no conversions this week».
- One root does not cover its synonyms or transliterations: «бесплатно», «даром», «бесплатный», «free» are separate.

## Starter groups (adapt; never paste blindly)
| Theme | Typical words |
|---|---|
| jobs | вакансия, работа, зарплата, резюме, требуется, hh |
| free / DIY | бесплатно, даром, своими руками, самому, схема, чертёж |
| education | курсы, обучение, реферат, гост (when not selling to engineers), википедия |
| used / cheap | б/у, бу, авито, юла, дешево (only if premium) |
| info | что такое, как выглядит, фото, видео, отзывы (keep for services that win on trust) |
| location mismatch | other cities, «рядом со мной» when there is no office |

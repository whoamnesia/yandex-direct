---
name: ad-copy
description: 'astudio ad copy for Yandex Direct combinatorial ads in ЕПК: up to 7 headlines of 56 characters and 3 texts of 81 characters (+15 narrow signs), sitelinks 30/60, callouts 25, display link 20, templates #...#, images for РСЯ, offer-first angles, compliance with 38-ФЗ and the Russian-language rule - every ad validated by ad_check.py. Use for "объявления для Директа", "тексты объявлений", "заголовки", "быстрые ссылки", "уточнения", "комбинаторное объявление", "креативы РСЯ", "Yandex ad copy".'
argument-hint: "[group / phrases] [offer, prices, proofs] [landing page]"
---

# astudio · Ad copy

`<root>` = two levels above this skill's base dir. Limits: `<root>/data/limits.json → ad`. Rules:
`<root>/reference/compliance.md`.

## What a group needs
- **Headlines (3–7, ≤ 56, word ≤ 22):** at least one with the main phrase (bold highlight), one with the offer
  (price, term, guarantee), one with the difference from competitors. Combinatorial ads have **no second
  headline**: legacy `title2` merges into the headline or disappears.
- **Texts (2–3, ≤ 81 + ≤ 15 narrow signs `! , . ; : "`, word ≤ 23):** benefit → proof → action. Each text must read
  well with any headline.
- **Sitelinks (4–8, title ≤ 30, description ≤ 60):** different pages, not the same page with anchors only.
- **Callouts (≥ 3, ≤ 25 each):** facts, not slogans («Замер бесплатно», «Гарантия 5 лет»). About 76 characters fit
  on mobile.
- **Display link ≤ 20**, **https link** with UTM: `utm_source=yandex&utm_medium=cpc&utm_campaign={campaign_id}&utm_content={ad_id}&utm_term={keyword}`.
- **Images for РСЯ:** ≥ 3 in different ratios (1:1, 16:9, 4:3), product visible, little text. Video optional.

## Writing rules
- Facts from the brief only. A price «от X ₽» must exist on the page. No invented discounts or guarantees.
- Superlatives need visible proof; otherwise rephrase («более 3 000 установок с 2015 года»).
- No CAPS (except abbreviations and brands), no «!» in headlines, one «!» per text at most, no emoji, no phone
  numbers in text.
- Foreign words with Russian equivalents («Sale», «New») are replaced; registered trademarks stay.
- Template `#default text#` puts the phrase in the ad when it fits; the default text must be meaningful on its own.
- Write 2 variants per group that test one idea (offer vs proof), not random rewording.

## Validate
Save ads as JSON (see the docstring of `ad_check.py`) and run `python3 <root>/scripts/ad_check.py ads.json`. Fix
every error; explain any warning you keep. Deliver a table: group · headlines · texts · sitelinks · callouts ·
link · status of ad_check.

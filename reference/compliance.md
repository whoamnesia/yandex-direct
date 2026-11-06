# Compliance for Yandex Direct ads (Russia)

Checked 2026-11-06. This is a working checklist, not legal advice; disputed cases go to a lawyer.

## Ad marking (ОРД, erid)
- For ads placed in Direct, Yandex's own ОРД assigns the `erid` token and reports to ЕРИР automatically. Do **not**
  add erid by hand.
- The advertiser fills in «Данные рекламодателя» in Direct (user menu): type, name, ИНН, ОКВЭД for a company or ИП;
  full name, ИНН and phone for an individual. Agencies turn off «Я конечный рекламодатель» and enter the contract.
- The ОРД cabinet creates monthly report drafts: someone on the client side checks them.
- `ErirAdDescription` should describe the real product; if empty, Direct generates one. For combinatorial ads
  check it in the web interface *(secondary)*.
- Fines for legal entities: 100 000–500 000 ₽ for a missing label or advertiser info; 200 000–500 000 ₽ for
  missing or wrong ЕРИР data (КоАП ст. 14.3; source: Yandex Advertising, ОРД materials).

## Advertising law (38-ФЗ «О рекламе») in copy
- Superlatives and comparisons («лучший», «№ 1», «самый дешёвый») need proof that the user can see; otherwise remove.
- Prices: «от 9 900 ₽» only if that price really exists on the landing page; credit and instalments need the
  creditor's name and the full cost conditions on the landing page.
- Restricted categories (medicine, medical services, БАД, finance, alcohol, weapons, gambling, education with a
  licence) need documents uploaded in Direct and warnings; check the category before writing copy.
- Medicine: the warning «Имеются противопоказания. Необходима консультация специалиста» is added by Direct when
  the category is set; do not promise cures.
- Do not use competitors' trademarks in copy without permission.

## Russian language in ads
- From 01.03.2026 amendments on the Russian language apply to consumer information *(secondary)*: avoid foreign
  words that have a common Russian equivalent (Sale, New, Best seller, Free); registered trademarks in Latin are
  allowed. `ad_check.py` flags Latin words for review.

## Moderation hygiene
- No CAPS words except abbreviations and brands, no «!» in headlines, one «!» per text at most, no extra spaces,
  no emoji, no phone numbers in text (use contacts/вCard), the landing page matches the ad.

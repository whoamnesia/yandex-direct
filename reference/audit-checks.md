# Audit checks for a Yandex Direct account

Each check gets a state: **pass**, **fail**, **unknown** (no data), **n/a**. Unknown is never counted as pass or
fail; it lowers evidence coverage. Severity: critical 5, high 3, medium 1, info 0.
Health = Σ weights of pass / Σ weights of (pass + fail). Coverage = (pass + fail + n/a) / all. Always publish both,
with the data window. No letter grades.

| ID | Area | Check | Sev. |
|---|---|---|---|
| T1 | Tracking | Metrica counter linked to every campaign | critical |
| T2 | Tracking | Priority goals are real business actions (lead, call, order), not page views | critical |
| T3 | Tracking | Goal value set or revenue passed where the business sells online | high |
| T4 | Tracking | UTM / Direct parameters on all links | high |
| T5 | Tracking | Goals actually fire: conversions over the last 28 days > 0 or explained | high |
| T6 | Tracking | Offline conversions / CRM link for long sales cycles | medium |
| S1 | Strategy | Strategy matches data volume: auto-CPA only with ≥ 10 conversions/week per goal | critical |
| S2 | Strategy | No strategy, limit or payment-model change in the last 2 weeks while learning | high |
| S3 | Strategy | Weekly budget ≥ 300 ₽; pay-per-conversion budget ≥ 10 × CPA | high |
| S4 | Strategy | Target CPA / ДРР agreed with the client and written down | high |
| S5 | Strategy | No campaign paused > 7 days and restarted without a note (learning resets) | medium |
| B1 | Budget | No campaign limited by budget while CPA ≤ target (lost volume) | medium |
| B2 | Budget | Spend concentrated: one campaign > 70% of spend without reason | info |
| K1 | Keywords | ≤ 7 words, valid operators (`keywords.py lint`) | high |
| K2 | Keywords | No duplicates across groups / campaigns | medium |
| K3 | Keywords | No «Мало показов» groups left as is | medium |
| K4 | Keywords | Autotargeting categories reviewed (not all on by default) | medium |
| N1 | Negatives | Account-level shared negative set exists | high |
| N2 | Negatives | Search-query report mined in the last 14 days | high |
| N3 | Negatives | No negative blocks own key phrases | critical |
| N4 | Negatives | Negatives are words, not full queries | medium |
| A1 | Ads | All ads pass `ad_check.py` (limits) | high |
| A2 | Ads | Combinatorial ads complete: 3+ headlines, 2+ texts, ≥ 4 sitelinks, ≥ 3 callouts, ≥ 3 images | high |
| A3 | Ads | No ads rejected or partially rejected by moderation | high |
| A4 | Ads | Landing page matches ad and price; page works on mobile | high |
| A5 | Ads | Compliance: superlatives proven, category documents, Russian-language rule | high |
| R1 | РСЯ | Placement report reviewed; poor placements excluded with evidence (not a universal rouble threshold) | medium |
| R2 | РСЯ | Search vs РСЯ split analysed; РСЯ CPA known separately | high |
| G1 | Geo/time | Regions and schedule match the business | medium |
| G2 | Geo/time | Bid adjustments by device/region justified by data | info |
| L1 | Legal | Advertiser data for ОРД filled in | critical |
| L2 | Legal | Monthly ОРД drafts checked | medium |
| P1 | Performance | Campaigns with CPA > 3 × target listed for review | high |
| P2 | Performance | Spend > 3 × target with 0 conversions listed for review | high |
| P3 | Performance | Week-over-week trend for CPA and CR explained | medium |

## Output format
1. Summary: health %, coverage %, window, account, data sources.
2. Table: ID · state · evidence (number, report, screenshot) · fix (proposal) · effort.
3. Top-5 fixes ordered by severity × ease. Every fix is a proposal; nothing is applied without approval.
4. Facts / hypotheses / MISSING data.

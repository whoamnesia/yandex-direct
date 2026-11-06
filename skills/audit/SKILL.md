---
name: audit
description: 'astudio audit of a Yandex Direct account: about 35 checks over tracking and goals, strategies and learning, budgets, keywords and operators, negatives and search queries, combinatorial ad completeness, РСЯ placements, geo, ОРД data and performance (3× CPA) - each pass / fail / unknown / n.a. with evidence, health score with separate evidence coverage, no letter grades, a top-5 fix list; read-only. Use for "аудит Директа", "проверь рекламный кабинет", "почему дорогие лиды", "что не так с Директом", "Yandex Direct audit".'
argument-hint: "[account / exports: campaigns, Reports, search queries, Metrica goals] [window]"
---

# astudio · Audit

`<root>` = two levels above this skill's base dir. Checks and scoring: `<root>/reference/audit-checks.md`.
API notes: `<root>/reference/api.md`.

## Data to collect (read-only)
1. Campaigns, groups, ads, keywords, negatives, strategies (API `get` or a Commander export).
2. Reports for the last 28 closed days and the previous 28: `CAMPAIGN_PERFORMANCE_REPORT` with `AdNetworkType`,
   priority `Goals` (≤ 10) and an explicit attribution model.
3. `SEARCH_QUERY_PERFORMANCE_REPORT` (last 30 days); placements for РСЯ.
4. Metrica goals and reaches. 5. Moderation statuses. 6. Advertiser data for ОРД (ask, or a screenshot).
No access → ask for the exports and mark what is missing as unknown.

## Run
- Ads: `python3 <root>/scripts/ad_check.py ads.json`; keywords: `python3 <root>/scripts/keywords.py lint ...`;
  performance: `python3 <root>/scripts/kpi.py week.csv --prev prev.csv --target-cpa <client's target>`.
- Fill every check with a state and evidence (a number with its report and window, or the screenshot). Never mark
  pass without evidence.
- Health = Σ weights(pass) / Σ weights(pass + fail); coverage = (pass + fail + n/a) / all. Publish both and the
  window.

## Output
Summary · table of checks · top-5 fixes (severity × ease, each a proposal with the exact change) · facts /
hypotheses / MISSING. Nothing is changed in the account. If the API answers HTTP 204 to everything, stop: Direct
is in special mode.

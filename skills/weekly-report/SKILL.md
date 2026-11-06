---
name: weekly-report
description: 'astudio weekly (or monthly) Yandex Direct report for a client: closed window, Search/РСЯ split, spend vs weekly limit, conversions on priority goals only, CTR, CPC, CR, CPA, ДРР, ROMI computed by kpi.py with MISSING for unknown inputs, week-over-week change, the 3× CPA review list, changes made, proposals not yet applied. Use for "отчёт по Директу", "еженедельный отчёт по рекламе", "итоги недели", "KPI рекламы", "CPA выросла", "Yandex Direct report".'
argument-hint: "[CSV export this week] [previous week] [target CPA]"
---

# astudio · Weekly report

`<root>` = two levels above this skill's base dir. Template: `<root>/templates/weekly-report.md`. Formulas:
`<root>/data/limits.json → kpi`.

## Steps
1. **Window:** last closed Monday–Sunday (Metrica can lag hours; never include today). Same window for every row
   and for the comparison week.
2. **Export** from Reports (`CAMPAIGN_PERFORMANCE_REPORT`, fields CampaignName, AdNetworkType, Impressions, Clicks,
   Cost, Conversions, Revenue; `Goals` = priority goals; attribution model stated) or from the interface. API money
   is in micro-units: use `--micro`.
3. **Compute:** `python3 <root>/scripts/kpi.py week.csv --prev prev.csv --target-cpa <client's target>`. Do not
   recompute by hand; do not fill MISSING with zero.
4. **Explain** the main change with a fact (a search-query, a placement, a strategy change, seasonality from
   Wordstat dynamics). If you cannot prove a cause, write it as a hypothesis.
5. **Review list:** rows flagged by «3× CPA»; for each, whether the campaign is learning, data sufficiency, and a
   proposal. Never pause anything yourself.
6. **Write** by the template: three lines on top, the table, the review list, changes made (with who approved),
   proposals, facts / hypotheses / MISSING.

## Tone
Plain Russian, short sentences, numbers formatted `1 234 ₽`, no jargon without explanation for the client.

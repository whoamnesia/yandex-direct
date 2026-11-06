# Yandex Direct, Reports, Metrica and Wordstat APIs: what the agent must know

Checked 2026-11-06. Sources are listed in `data/limits.json → sources`. Lines marked *(secondary)* come from
open-source skills, not from yandex.ru; re-check them before relying on them.

## Access
- OAuth token in `Authorization: Bearer <token>`; agencies add `Client-Login: <login>`. Tokens live in env
  variables (`YANDEX_DIRECT_TOKEN`, `YANDEX_METRIKA_TOKEN`, `YANDEX_SEARCH_API_KEY`, `YANDEX_FOLDER_ID`), never in
  chat, files or commits.
- Sandbox: `https://api-sandbox.direct.yandex.com/json/v5/` for any write experiment *(secondary)*.

## Direct API v5
- Points (units): an individual daily limit per advertiser, a sliding 24-hour window credited by 1/24 each hour.
  Response header `Units: spent/left/limit`. A failed call still costs 20 points. ≤ 5 parallel requests.
- ЕПК (`UNIFIED_CAMPAIGN`) replaced text-image, dynamic and smart-banner campaigns. Writes to unified campaigns and
  groups go to `/json/v501/`; v5 `get` may show ЕПК as `TEXT_CAMPAIGN` *(secondary)*.
- Money is in micro-units: 1 ₽ = 1 000 000. Convert both ways in code, never in your head.
- `CampaignIds` ≤ 10 per `get`; pages ≤ 10 000 objects *(secondary)*.
- HTTP 204 on every call = "special mode", the API is switched off by Yandex. Stop and tell the user; do not retry
  in a loop *(secondary)*.
- After any write, `get` the object again and compare: a change is done only when the read-back matches.

## Reports service
- ≤ 20 requests per 10 seconds per user; ≤ 5 offline reports in the queue; stored 5 hours.
- 3 years of history; the `Query` field (search queries) only for the last 180 days.
- `Goals` ≤ 10 per request; `AttributionModels`: AUTO, LSCCD, FCCD, LC.
- Without `Goals`, conversions are summed over **all** Metrica goals, micro-goals included: always pass the
  priority goals.
- Split Search and РСЯ with the `AdNetworkType` field. Metrica data can lag several hours: report closed days only.
- Offline mode: on HTTP 201/202 wait for `retryIn` seconds and poll again; do not hammer.

## Metrica API
- 5 000 requests per day per user, 200 Reports API requests per 5 minutes, 3 parallel requests, 30 rps per IP.
- Goals: `GET /management/v1/counter/{id}/goals`. Report: `/stat/v1/data` with `ym:s:goal<id>reaches`.

## Wordstat
- Now part of Yandex Search API (Yandex AI Studio / Cloud): base `https://searchapi.api.cloud.yandex.net/v2/wordstat/`,
  methods `topRequests`, `dynamics`, `regions`, `getRegionsTree`. Auth `Api-Key` (scope `yc.search-api.execute`) or
  IAM token, role `search-api.webSearch.user`.
- The legacy `api.wordstat.yandex.net/v1` must not be used. Quotas: about 10 rps and 100 requests per hour
  *(secondary: nebelov)*; `devices` ≤ 3 values, `regions` ≤ 100 IDs.
- Wordstat counts are impressions of queries containing the words, not clicks or demand for your offer. Exact
  frequency needs `"!слово !слово"`.

## Safety rules for any connected MCP or script
1. Read-only by default. Writes only after the user approves the exact JSON payload in this conversation.
2. Never activate, resume, delete or send to moderation by yourself; new campaigns are created as drafts.
3. Finance (transfers, invoices, budgets) is never touched by the agent.
4. Log every write: what, before, after, who approved.

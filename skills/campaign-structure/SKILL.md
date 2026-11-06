---
name: campaign-structure
description: 'astudio campaign build for Yandex Direct from brief to DRAFT: brief, account and Metrica reconnaissance, structure of ЕПК campaigns and groups (one angle = one campaign, brand separate, Search/РСЯ split), naming, UTM, goals, launch checklist and upload as a draft or a Direct Commander file - with a gate after every step and no activation by the agent. Use for "запустить рекламу в Директе", "создать кампанию", "структура кампаний", "настроить Директ с нуля", "ЕПК", "build Yandex campaign".'
argument-hint: "[brief] [site] [Metrica counter id]"
---

# astudio · Campaign structure (brief → draft)

`<root>` = two levels above this skill's base dir. Read `<root>/reference/campaign-structure.md`; brief template
`<root>/templates/brief.md`. Work folder: `direct-campaigns/<slug>/` with one file per step and `_state.json`
(`step`, `approved_by`, `skipped`, `blockers`).

## Steps and gates
| № | Step | Artefact | Gate |
|---|---|---|---|
| 0 | Brief (template) | `00-brief.md` | marketer «ОК» |
| 1 | Reconnaissance: existing campaigns, Metrica goals, conversions in the last 28 days | `01-recon.md` | — |
| 2 | Semantics and negatives (skill `semantics`) | `02-keywords.txt`, `02-negatives.txt` | «ОК» |
| 3 | Structure: campaigns, groups, landing pages, geo, schedule | `03-structure.md` | «ОК» |
| 4 | Ads (skill `ad-copy`), `ad_check.py` clean | `04-ads.json` | «ОК» |
| 5 | Goals and strategy (skill `strategies`) | `05-strategy.md` | «ОК» |
| 6 | Final checklist (below) | `06-checklist.md` | «ОК» |
| 7 | Upload as **draft** (API with approved payload, or Commander/Excel file) and read back | `07-upload.md` | — |

## Blockers (no upload while any is open)
- No Metrica counter or no priority goal: «цель Метрики никогда не подменяется догадкой».
- No budget or no target from the client (unknown is fine for planning, not for the strategy setting).
- Advertiser data for ОРД not filled in.
- Restricted category without documents.
- `ad_check.py` or `keywords.py lint` errors.

## Final checklist
Counter linked · priority goals · UTM on all links · negatives on 3 levels · each group has a complete
combinatorial ad · strategy and weekly budget fit the data volume · geo and schedule · ОРД data · nothing set to
start: the user launches it.

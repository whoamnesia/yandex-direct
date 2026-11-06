# astudio-yandex-direct — Yandex Direct campaigns for Claude Code

**English** · [Русский](README.ru.md)

Author: **astudio.one** — [astudio.one](https://astudio.one) · License: MIT · Version 1.0.0

A plugin that makes an agent a careful PPC specialist for Yandex Direct: semantics with negatives on three levels, combinatorial ads that fit the current ЕПК limits, campaign structure from a brief to a draft, strategies chosen by data volume, account audits with evidence, and weekly KPI reports on priority goals. Limits come from a dated reference, numbers come from code, and the agent never launches, deletes or pays for anything.

## What it does

- Brief → draft pipeline with a marketer gate after every step and a list of blockers
- Ad validator for combinatorial ads: 7 × 56 headlines, 3 × 81 texts with 15 narrow signs, sitelinks, callouts, links, superlatives and the 2026 Russian-language rule
- Keyword linter: ≤ 7 words, operators, duplicates, negative limits, negatives that block your own phrases, cross-minusing proposals
- Strategy guide: pay per click, average CPA, pay-per-conversion, ДРР, «Максимум прибыли», learning and budget minimums
- Audit with pass / fail / unknown / n.a., health score and separate evidence coverage, no letter grades
- Weekly KPI report from a CSV: CTR, CPC, CR, CPA, ДРР, ROMI, MISSING instead of zero, week over week, 3× CPA review list
- API notes for Direct v5/v501, Reports, Metrica and Wordstat v2, with safety rules for any MCP

## Install

In Claude Code:

```
/plugin marketplace add whoamnesia/yandex-direct
/plugin install astudio-yandex-direct@astudio-yandex-direct
```

Restart Claude Code. Skills appear in the `/` menu as `astudio-yandex-direct:astudio-yandex-direct` …

Pinned install (what aiocenter.ru does): clone the repository, check out the published commit, then `/plugin marketplace add ~/.aiocenter/packages/astudio-yandex-direct`.

Other agents (Cursor, Codex, Gemini CLI): every skill is a plain `skills/<name>/SKILL.md` with references; point the agent at the folder or copy it into the agent's rules.

## Skills

| Skill | What it does |
|---|---|
| `astudio-yandex-direct` | Main skill: routing, five rules, gates, facts / hypotheses / MISSING |
| `semantics` | Masks, Wordstat, clustering, operators, negatives, cross-minusing |
| `ad-copy` | Combinatorial ads, sitelinks, callouts, compliance |
| `campaign-structure` | From brief to a draft campaign with gates |
| `strategies` | Strategy by data volume, learning, budgets |
| `audit` | Account audit with evidence and coverage |
| `weekly-report` | Weekly KPI report on priority goals |

## Tools

Python 3.9+, standard library only. They read what you pass them and write nothing unless you redirect the output.

| Script | Purpose |
|---|---|
| `scripts/ad_check.py` | Validates ads against ЕПК limits and copy rules |
| `scripts/keywords.py` | Lints key phrases and negatives; proposes cross-minusing |
| `scripts/kpi.py` | Weekly KPI table, week over week, 3× CPA list, coverage |

## Safety

- T
- h
- e
-  
- a
- g
- e
- n
- t
-  
- w
- o
- r
- k
- s
-  
- i
- n
-  
- d
- r
- a
- f
- t
- s
- .
-  
- I
- t
-  
- n
- e
- v
- e
- r
-  
- a
- c
- t
- i
- v
- a
- t
- e
- s
- ,
-  
- r
- e
- s
- u
- m
- e
- s
- ,
-  
- d
- e
- l
- e
- t
- e
- s
-  
- o
- r
-  
- s
- e
- n
- d
- s
-  
- c
- a
- m
- p
- a
- i
- g
- n
- s
-  
- t
- o
-  
- m
- o
- d
- e
- r
- a
- t
- i
- o
- n
- ,
-  
- n
- e
- v
- e
- r
-  
- t
- o
- u
- c
- h
- e
- s
-  
- f
- i
- n
- a
- n
- c
- e
- ,
-  
- a
- n
- d
-  
- w
- r
- i
- t
- e
- s
-  
- t
- h
- r
- o
- u
- g
- h
-  
- t
- h
- e
-  
- A
- P
- I
-  
- o
- n
- l
- y
-  
- a
- f
- t
- e
- r
-  
- y
- o
- u
-  
- a
- p
- p
- r
- o
- v
- e
-  
- t
- h
- e
-  
- e
- x
- a
- c
- t
-  
- p
- a
- y
- l
- o
- a
- d
- ;
-  
- t
- h
- e
- n
-  
- i
- t
-  
- r
- e
- a
- d
- s
-  
- t
- h
- e
-  
- o
- b
- j
- e
- c
- t
-  
- b
- a
- c
- k
- .
-  
- T
- o
- k
- e
- n
- s
-  
- a
- r
- e
-  
- r
- e
- a
- d
-  
- f
- r
- o
- m
-  
- e
- n
- v
- i
- r
- o
- n
- m
- e
- n
- t
-  
- v
- a
- r
- i
- a
- b
- l
- e
- s
- .
-  
- B
- u
- d
- g
- e
- t
-  
- a
- n
- d
-  
- t
- a
- r
- g
- e
- t
-  
- C
- P
- A
-  
- c
- o
- m
- e
-  
- o
- n
- l
- y
-  
- f
- r
- o
- m
-  
- y
- o
- u
- .

## Layout

```
astudio-yandex-direct/
  .claude-plugin/plugin.json, marketplace.json
  skills/<7 skills>/SKILL.md
  data/       limits.json (dated limits, operators, strategies, API quotas, KPI)
  reference/  api.md · campaign-structure.md · negatives.md · compliance.md · audit-checks.md
  templates/  brief.md · weekly-report.md
  scripts/    ad_check.py · keywords.py · kpi.py
  README.md · README.ru.md · LICENSE · NOTICE.md
```

## Training track

This plugin is the package of the aiocenter.ru track «Кампании в Яндекс Директе»: digests, agent memo and an exam with a signed certificate — https://aiocenter.ru/tracks/yandex-direct/

## Credits

Built by astudio.one on ideas from the best open-source projects in this field; see [NOTICE.md](NOTICE.md) for sources and licences.

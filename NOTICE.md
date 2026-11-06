# Third-party notices / Сторонние источники

astudio-yandex-direct is written by **astudio.one**. Its rules, workflows and tools are original work. The projects below were studied in full; ideas, structures and checklists were adapted from them with credit. Where text was translated or adapted from an Apache-2.0 project, that project's notice is reproduced below.

astudio-yandex-direct написан **astudio.one**. Правила, сценарии и инструменты — собственная работа. Проекты ниже изучены целиком; идеи, структура и чек-листы взяты из них с указанием авторства. Где текст переведён или адаптирован из проекта под Apache-2.0, его уведомление приведено ниже.

## Studied and adapted / Изучены и использованы

| Project | Licence | What we took |
|---|---|---|
| [Silverov/yandex-direct-skill](https://github.com/Silverov/yandex-direct-skill) | MIT | ЕПК change log, API gotchas (v501 writes, micro-units, HTTP 204 special mode), audit areas, 3× CPA rule, learning and budget rules |
| [ai-hub-open/yandex-direct-manager](https://github.com/ai-hub-open/yandex-direct-manager) | Apache-2.0 | brief → DRAFT pipeline with marketer gates, blockers, three levels of negatives, structure rules, never activate campaigns |
| [nebelov/yandex-direct-for-all](https://github.com/nebelov/yandex-direct-for-all) | MIT | missing data is BLOCKED not zero, read back after writes, negatives are words not queries, budget only from the client, Wordstat v2 endpoints |
| [axisrow/yandex-direct-mcp-plugin](https://github.com/axisrow/yandex-direct-mcp-plugin) | MIT | Claude Code plugin packaging and the scope of a Direct MCP; its 35/30 limits are outdated and were not used |
| [AgriciDaniel/claude-ads](https://github.com/AgriciDaniel/claude-ads) | MIT | scoring contract: pass / fail / unknown / n.a., evidence coverage, no letter grades; formulas with every input mapped to evidence |

## Studied, ideas only (no code or text copied) / Только идеи, без копирования

| Project | Licence | Why ideas only |
|---|---|---|
| [Yurich-ru/yandex-ads-mcp](https://github.com/Yurich-ru/yandex-ads-mcp) | no LICENSE file | only confirmed the list of API areas |
| [mkultraaaa (Direct skills)](https://github.com/mkultraaaa (Direct skills)) | no LICENSE file | not used |

## Apache-2.0 notices

- ai-hub-open/yandex-direct-manager — Copyright its authors. Licensed under the Apache License 2.0. The pipeline, gates and negative-keyword levels were adapted and rewritten; no file was copied. Changes: rewritten for any MCP or manual export, merged with audit and reporting.

## Public documentation / Открытая документация

- Яндекс Директ, Справка: технические ограничения (yandex.ru/support/direct/ru/moderation/technical-restrictions)
- Яндекс Директ, Справка: символы и операторы
- Яндекс Директ, Справка: Максимум конверсий с оплатой за конверсии; У кампании мало конверсий
- API Яндекс Директа: баллы, ограничения сервиса Reports
- API Яндекс Метрики: квоты
- Yandex AI Studio: Wordstat в Search API
- Яндекс Реклама: материалы по ОРД и маркировке
- Федеральный закон № 38-ФЗ «О рекламе»; КоАП РФ ст. 14.3

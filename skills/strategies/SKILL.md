---
name: strategies
description: 'astudio bidding strategies for Yandex Direct ЕПК: choose between pay-per-click, «Максимум конверсий» with average CPA or pay-per-conversion, ДРР and «Максимум прибыли» by data volume; learning rules (≥ 10 conversions a week, 1-2 weeks, no changes while learning, pause > 7 days restarts), weekly budget minimums (300 ₽, 10 × CPA), the 3-phase evolution and when to switch. Use for "стратегия в Директе", "оплата за конверсии", "какую стратегию выбрать", "обучение стратегии", "Максимум конверсий", "Максимум прибыли", "ДРР", "Yandex bidding".'
argument-hint: "[campaign] [conversions per week] [target CPA / ДРР] [budget]"
---

# astudio · Strategies

`<root>` = two levels above this skill's base dir. Numbers: `<root>/data/limits.json → strategies`.

## Choose by data volume (per campaign and per priority goal)
| Situation | Strategy | Why |
|---|---|---|
| New account, < 10 conversions/week | «Максимум кликов» (pay per click) with a weekly budget, or «Максимум конверсий» on a more frequent goal | auto-CPA cannot learn on rare events |
| ≥ 10 conversions/week, CPA target known | «Максимум конверсий», average CPA | stable learning |
| Same, client wants to pay only for results | «Максимум конверсий» with **pay-per-conversion** (window 21 days, CPA ≤ 50 000 ₽, ≤ 30 goals, weekly budget ≥ 300 ₽ and ≥ 10 × CPA) | risk on Yandex |
| Revenue passed to Metrica | ДРР target | optimises to share of revenue |
| Margin data available | «Максимум прибыли» (out of beta 18.08.2026) | optimises to profit |

## Three phases
1. **Collect data** (2–4 weeks): clicks strategy or a frequent micro-goal, negatives mined weekly.
2. **Learn**: switch to conversions once ≥ 10/week on the priority goal; then do not change the strategy, the
   limit type or the payment model for 2–3 weeks.
3. **Scale**: raise budget in steps of ≤ 20–30% a week; move to ДРР or profit when revenue is reliable.

## Learning rules
- The goal should be reached at least 10 times a week; learning takes 1–2 weeks. With fewer conversions: pay per
  click, a bigger budget (≥ 10 × CPA of the costliest goal), or a more frequent goal.
- A pause longer than 7 days, a strategy change or a big target change restarts learning *(practitioner rule)*.
- Do not judge a learning campaign by the «3× CPA» rule; mark it «обучение» in reports.
- Up to 30% of an unspent weekly budget can roll over (since July 2026): spend above the weekly limit is not a bug
  until it exceeds that.

## Output
Current strategy · data volume (conversions/week per goal, source) · recommendation · expected learning time ·
what must not be touched until when · risks. Budget and target CPA only from the client.

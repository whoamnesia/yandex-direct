#!/usr/bin/env python3
"""astudio-yandex-direct · kpi: weekly KPI report from a Direct / Metrica export.

Usage: python3 kpi.py week.csv [--prev prev_week.csv] [--micro] [--target-cpa 1500] [--json]
CSV (comma or semicolon, header names case-insensitive, Russian aliases accepted):
  campaign, network (search/yan, optional), period_start, period_end, impressions, clicks, cost,
  conversions (priority goals only!), revenue (optional), target_cpa (optional), weekly_limit (optional)
--micro: cost/revenue are in API micro-units (÷ 1 000 000).
Rules: a missing input is MISSING, never 0; rates use the same closed window; kill list = CPA > 3 × target,
or spend > 3 × target with 0 conversions. Exit 1 if windows differ between rows."""
import csv, json, sys, pathlib, io
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation

ALIASES = {
    'campaign': ['campaign', 'кампания', 'campaignname'], 'network': ['network', 'сеть', 'adnetworktype', 'площадка'],
    'period_start': ['period_start', 'date_from', 'с', 'начало'], 'period_end': ['period_end', 'date_to', 'по', 'конец'],
    'impressions': ['impressions', 'показы'], 'clicks': ['clicks', 'клики'], 'cost': ['cost', 'расход', 'spend'],
    'conversions': ['conversions', 'конверсии', 'leads', 'лиды'], 'revenue': ['revenue', 'доход', 'выручка'],
    'target_cpa': ['target_cpa', 'целевой_cpa', 'kpi_cpa'], 'weekly_limit': ['weekly_limit', 'weeklyspendlimit', 'недельный_бюджет'],
}
MISSING = 'MISSING'


def D(x):
    if x is None:
        return None
    s = str(x).strip().replace(' ', '').replace(' ', '').replace('₽', '').replace(',', '.')
    if s in ('', '-', '—', 'null', 'None', 'n/a'):
        return None
    try:
        return Decimal(s)
    except InvalidOperation:
        return None


def load(path, micro):
    txt = pathlib.Path(path).read_text(encoding='utf-8-sig')
    dialect = ';' if txt.split('\n', 1)[0].count(';') > txt.split('\n', 1)[0].count(',') else ','
    rows = list(csv.DictReader(io.StringIO(txt), delimiter=dialect))
    out = []
    for r in rows:
        low = {k.strip().lower(): v for k, v in r.items() if k}
        rec = {}
        for f, al in ALIASES.items():
            rec[f] = next((low[a] for a in al if a in low), None)
        for f in ('impressions', 'clicks', 'cost', 'conversions', 'revenue', 'target_cpa', 'weekly_limit'):
            rec[f] = D(rec[f])
            if micro and rec[f] is not None and f in ('cost', 'revenue', 'target_cpa', 'weekly_limit'):
                rec[f] = rec[f] / Decimal(1000000)
        out.append(rec)
    return out


def div(a, b, mul=1):
    if a is None or b is None:
        return None
    if b == 0:
        return 'n/a'
    return (a / b * mul).quantize(Decimal('0.01'), ROUND_HALF_UP)


def metrics(r):
    m = {
        'CTR %': div(r['clicks'], r['impressions'], 100), 'CPC': div(r['cost'], r['clicks']),
        'CR %': div(r['conversions'], r['clicks'], 100), 'CPA': div(r['cost'], r['conversions']),
        'ДРР %': div(r['cost'], r['revenue'], 100),
        'ROMI %': div((r['revenue'] - r['cost']) if r['revenue'] is not None and r['cost'] is not None else None, r['cost'], 100),
    }
    return m


def fmt(v):
    if v is None:
        return MISSING
    if isinstance(v, str):
        return v
    s = f'{v:,.2f}'.replace(',', ' ').replace('.', ',')
    return s[:-3] if s.endswith(',00') else s


def total(rows):
    t = {'campaign': 'ИТОГО', 'network': ''}
    for f in ('impressions', 'clicks', 'cost', 'conversions', 'revenue'):
        vals = [r[f] for r in rows]
        t[f] = None if any(v is None for v in vals) else sum(vals, Decimal(0))
    return t


def main(argv):
    if not argv or argv[0] in ('-h', '--help'):
        print(__doc__)
        return 0
    micro = '--micro' in argv
    rows = load(argv[0], micro)
    tcpa_cli = D(argv[argv.index('--target-cpa') + 1]) if '--target-cpa' in argv else None
    prev = load(argv[argv.index('--prev') + 1], micro) if '--prev' in argv else None
    windows = {(r['period_start'], r['period_end']) for r in rows}
    notes, kill = [], []
    if len(windows) > 1:
        notes.append(f'ERROR: rows cover different windows {sorted(map(str, windows))}: rates are not comparable')
    if any(None in w for w in windows):
        notes.append('period_start/period_end MISSING: state the closed window before sending the report')
    report = []
    for r in rows + [total(rows)]:
        m = metrics(r)
        tcpa = r.get('target_cpa') or tcpa_cli
        flag = ''
        if r['campaign'] != 'ИТОГО' and tcpa:
            if isinstance(m['CPA'], Decimal) and m['CPA'] > 3 * tcpa:
                flag = f'CPA > 3× target ({fmt(tcpa)})'
            elif r['conversions'] == 0 and r['cost'] is not None and r['cost'] > 3 * tcpa:
                flag = f'0 conversions, spend > 3× target ({fmt(tcpa)})'
            if flag:
                kill.append((r['campaign'], r.get('network') or '', flag))
        wl = r.get('weekly_limit')
        if wl and r['cost'] is not None and r['cost'] > wl * Decimal('1.3'):
            notes.append(f'{r["campaign"]}: spend {fmt(r["cost"])} > weekly limit {fmt(wl)} + 30% rollover: check the budget setting')
        report.append((r, m, flag))
    known = sum(1 for r in rows for f in ('impressions', 'clicks', 'cost', 'conversions') if r[f] is not None)
    coverage = round(100 * known / (4 * len(rows))) if rows else 0
    rev_cov = sum(1 for r in rows if r['revenue'] is not None)
    if '--json' in argv:
        print(json.dumps({'window': sorted(map(str, windows)), 'coverage_pct': coverage,
                          'rows': [{'campaign': r['campaign'], 'network': r.get('network'),
                                    **{k: (str(v) if v is not None else MISSING) for k, v in m.items()}, 'flag': f} for r, m, f in report],
                          'kill_list': kill, 'notes': notes}, ensure_ascii=False, indent=2))
    else:
        w = next(iter(windows)) if len(windows) == 1 else ('?', '?')
        print(f'## Отчёт Директ за {w[0] or MISSING} – {w[1] or MISSING}\n')
        print('| Кампания | Сеть | Показы | Клики | Расход ₽ | Конв. | CTR % | CPC ₽ | CR % | CPA ₽ | ДРР % | ROMI % | Флаг |')
        print('|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|')
        for r, m, f in report:
            print(f'| {r["campaign"]} | {r.get("network") or ""} | {fmt(r["impressions"])} | {fmt(r["clicks"])} | {fmt(r["cost"])} | {fmt(r["conversions"])} | '
                  + ' | '.join(fmt(m[k]) for k in ('CTR %', 'CPC', 'CR %', 'CPA', 'ДРР %', 'ROMI %')) + f' | {f} |')
        if prev:
            pt, ct = total(prev), total(rows)
            pm, cm = metrics(pt), metrics(ct)
            print('\n### Неделя к неделе (итого)\n')
            print('| Метрика | Прошлая | Текущая | Δ % |\n|---|---:|---:|---:|')
            for k in ('cost', 'clicks', 'conversions'):
                print(f'| {k} | {fmt(pt[k])} | {fmt(ct[k])} | {fmt(div((ct[k] - pt[k]) if None not in (ct[k], pt[k]) else None, pt[k], 100))} |')
            for k in ('CPA', 'CR %', 'ДРР %'):
                a, b = pm[k], cm[k]
                d = div(b - a, a, 100) if isinstance(a, Decimal) and isinstance(b, Decimal) else None
                print(f'| {k} | {fmt(a)} | {fmt(b)} | {fmt(d)} |')
        print('\n### На разбор: правило «3× CPA» (не выключать автоматически, сначала проверить обучение и цели)\n')
        print('\n'.join(f'- {c} {n}: {f}' for c, n, f in kill) if kill else '- нет (или не задан целевой CPA: MISSING)' if not (tcpa_cli or any(r.get('target_cpa') for r in rows)) else '- нет')
        print(f'\n### Покрытие данными\n\n- базовые поля: {coverage}% · выручка передана в {rev_cov} из {len(rows)} строк (ДРР/ROMI без выручки = MISSING)')
        print('- конверсии должны быть по приоритетным целям; сумма «все цели» в отчёт не идёт')
        for n in notes:
            print(f'- {n}')
    return 1 if any(n.startswith('ERROR') for n in notes) else 0


if __name__ == '__main__':
    try:
        sys.exit(main(sys.argv[1:]))
    except BrokenPipeError:
        sys.exit(0)

#!/usr/bin/env python3
"""astudio-yandex-direct · keywords: lint key phrases and negative keywords for Yandex Direct.

Usage:
  python3 keywords.py lint keywords.txt [--negatives neg.txt] [--campaign-negatives camp.txt] [--json]
  python3 keywords.py cross keywords.txt          # cross-minusing proposals inside one group

keywords.txt: one phrase per line; «# group name» lines start a group; inline minus words allowed
(«ремонт окон -бесплатно»). Negatives: one word or short phrase per line.
Checks: ≤ 7 words, ≤ 4096 chars, balanced [] "" (), operators attached to a word, duplicates after
normalisation (case, ё, word order unless [] or quotes), ≤ 200 phrases per group, negative lists within
4096 / 20 000 chars excluding spaces, negatives that are full queries instead of words, and negatives
that block your own key phrases. Exit 1 on errors. Proposals only: semantic choices stay with a human."""
import json, re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
LIM = json.loads((ROOT / 'data/limits.json').read_text(encoding='utf-8'))
K, N = LIM['keywords'], LIM['negatives']
STOP = {'в', 'во', 'на', 'с', 'со', 'и', 'или', 'а', 'по', 'для', 'от', 'до', 'из', 'к', 'ко', 'у', 'о', 'об', 'за', 'под', 'над', 'не', 'без', 'при', 'как', 'что'}


def norm_word(w):
    return w.lower().replace('ё', 'е').strip('!+[]"()')


def split_phrase(line):
    """-> (positive part, inline negatives)"""
    parts = re.split(r'\s-(?=\S)', ' ' + line.strip())
    return parts[0].strip(), [p.strip() for p in parts[1:] if p.strip()]


def pos_words(phrase):
    p = re.sub(r'\([^)]*\)', lambda m: m.group(0).split('|')[0].strip('()'), phrase)
    return [w for w in re.findall(r'[!+]?[\w\-]+', p)]


def stem(w):
    w = norm_word(w)
    return w[:-2] if len(w) > 6 else (w[:-1] if len(w) > 4 else w)


def key(phrase):
    ordered = phrase.strip().startswith('[') or phrase.strip().startswith('"')
    ws = [norm_word(w) for w in pos_words(phrase)]
    return (' '.join(ws) if ordered else ' '.join(sorted(ws))), phrase.strip()[:1] in '"['


def read_groups(path):
    groups, cur = [], {'name': 'group 1', 'lines': []}
    for n, raw in enumerate(pathlib.Path(path).read_text(encoding='utf-8').splitlines(), 1):
        s = raw.strip()
        if not s:
            continue
        if s.startswith('#'):
            if cur['lines']:
                groups.append(cur)
            cur = {'name': s.lstrip('# ').strip() or f'group {len(groups) + 2}', 'lines': []}
            continue
        cur['lines'].append((n, s))
    if cur['lines']:
        groups.append(cur)
    return groups


def read_list(path):
    if not path:
        return []
    return [l.strip().lstrip('-').strip() for l in pathlib.Path(path).read_text(encoding='utf-8').splitlines() if l.strip() and not l.strip().startswith('#')]


def lint(argv):
    path = argv[0]
    neg = read_list(argv[argv.index('--negatives') + 1]) if '--negatives' in argv else []
    camp = read_list(argv[argv.index('--campaign-negatives') + 1]) if '--campaign-negatives' in argv else []
    out = []
    add = lambda lvl, where, msg: out.append({'level': lvl, 'where': where, 'message': msg})
    seen = {}
    allpos = []
    for g in read_groups(path):
        if len(g['lines']) > K['per_group_max']:
            add('error', g['name'], f'{len(g["lines"])} phrases > {K["per_group_max"]} per group')
        for n, line in g['lines']:
            where = f'{g["name"]}:{n}'
            if len(line) > K['phrase_chars_max']:
                add('error', where, f'phrase {len(line)} chars > {K["phrase_chars_max"]}')
            pos, inline = split_phrase(line)
            ws = pos_words(pos)
            if len(ws) > K['words_max']:
                add('error', where, f'{len(ws)} words > {K["words_max"]}: «{pos}»')
            for a, b in (('[', ']'), ('(', ')')):
                if pos.count(a) != pos.count(b):
                    add('error', where, f'unbalanced {a}{b}: «{pos}»')
            if pos.count('"') % 2:
                add('error', where, f'unbalanced quotes: «{pos}»')
            if '"' in pos and not (pos.startswith('"') and pos.endswith('"')):
                add('error', where, 'quotes must wrap the whole phrase')
            if re.search(r'[!+](\s|$)', pos):
                add('error', where, 'operator ! or + must stick to the next word')
            if re.search(r'[^\w\s!+\[\]"()|\-]', pos):
                add('warn', where, f'special characters in a key phrase will be dropped or rejected: «{pos}»')
            for w in ws:
                bare = norm_word(w)
                if bare in STOP and not w.startswith(('+', '!')) and '"' not in pos and '[' not in pos:
                    add('info', where, f'stop word «{bare}» is ignored without + (use +{bare} if it changes meaning)')
            k, _ = key(pos)
            if k in seen:
                add('warn', where, f'duplicate of {seen[k]}: «{pos}»')
            else:
                seen[k] = where
            allpos.append((where, pos, inline))
            for m in inline:
                if len(pos_words(m)) > 2:
                    add('warn', where, f'inline negative «-{m}» looks like a query: negatives are words or short phrases')
    for label, lst, cap in (('group negatives', neg, N['group_chars_max']), ('campaign negatives', camp, N['campaign_chars_max'])):
        if not lst:
            continue
        chars = sum(len(x.replace(' ', '')) for x in lst)
        if chars > cap:
            add('error', label, f'{chars} chars (no spaces) > {cap}')
        else:
            add('info', label, f'{chars}/{cap} chars used')
        dup = {}
        for x in lst:
            w = len(pos_words(x))
            if w > N['words_max']:
                add('error', label, f'«{x}» {w} words > {N["words_max"]}')
            elif w > 2:
                add('warn', label, f'«{x}» is a search query, not a negative word: take the one word that makes it irrelevant')
            kx = ' '.join(sorted(norm_word(t) for t in pos_words(x)))
            if kx in dup:
                add('warn', label, f'duplicate negative «{x}»')
            dup[kx] = 1
        for x in lst:
            nws = [t for t in pos_words(x)]
            for where, pos, _ in allpos:
                pws = {stem(t) if not t.startswith('!') else norm_word(t) for t in pos_words(pos)}
                hit = all((norm_word(t) in pws) if t.startswith('!') else (stem(t) in pws) for t in nws)
                if hit:
                    add('error', label, f'negative «{x}» blocks your own phrase «{pos}» ({where})')
    errors = sum(1 for o in out if o['level'] == 'error')
    if '--json' in argv:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        for o in out:
            print(f'{o["level"].upper():5} [{o["where"]}] {o["message"]}')
        print(f'\n{len(allpos)} phrases · {errors} errors · {sum(1 for o in out if o["level"] == "warn")} warnings')
    return 1 if errors else 0


def cross(argv):
    """For each pair A ⊂ B (A's words are a subset of B's), propose B's extra words as negatives on A."""
    for g in read_groups(argv[0]):
        items = []
        for n, line in g['lines']:
            pos, _ = split_phrase(line)
            items.append((pos, {norm_word(w) for w in pos_words(pos)}))
        props = {}
        for a, wa in items:
            for b, wb in items:
                if a != b and wa < wb:
                    for extra in sorted(wb - wa):
                        if extra not in STOP:
                            props.setdefault(a, set()).add(extra)
        print(f'# {g["name"]}')
        if not props:
            print('  no nested phrases: nothing to cross-minus')
        for a, ex in props.items():
            print(f'  {a} ' + ' '.join('-' + e for e in sorted(ex)))
        print()
    print('Proposals only. In ЕПК automatic cross-minusing may already be on; check before adding.')
    return 0


if __name__ == '__main__':
    a = sys.argv[1:]
    try:
        if not a or a[0] in ('-h', '--help') or a[0] not in ('lint', 'cross') or len(a) < 2:
            print(__doc__)
            sys.exit(0 if a and a[0] in ('-h', '--help') else 2)
        sys.exit(lint(a[1:]) if a[0] == 'lint' else cross(a[1:]))
    except BrokenPipeError:
        sys.exit(0)

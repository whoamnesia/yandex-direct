#!/usr/bin/env python3
"""astudio-yandex-direct · ad_check: validate Yandex Direct (ЕПК) ad copy against the technical limits.

Input: a JSON file with one ad or a list of ads:
  {"id": "g1-a1", "titles": ["..."], "texts": ["..."], "title2": "...",          # title2 = legacy
   "display_link": "...", "href": "https://...", "sitelinks": [{"title": "...", "description": "..."}],
   "callouts": ["..."], "images": 3, "trademarks": ["iPhone"]}
Usage: python3 ad_check.py ads.json [--json]      Exit 1 if any error.
Limits come from data/limits.json (see its "sources" and "checked_at")."""
import json, re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
L = json.loads((ROOT / 'data/limits.json').read_text(encoding='utf-8'))['ad']
NARROW = set(L['text']['narrow_chars'])
SUPERLATIVE = re.compile(r'(?<![\w-])(лучш\w*|самы[йяеx]\w*|№\s?1|номер\s+один|первый\s+в\s+россии|абсолютн\w*|идеальн\w*|гарантир\w*|100\s?%)(?![\w-])', re.I)
PLACEHOLDER = re.compile(r'\{\{|\}\}|\[\s*(вставить|название|цена|xxx)\s*\]|lorem|TODO|XXX', re.I)
LATIN_WORD = re.compile(r'(?<![\w-])[A-Za-z][A-Za-z\'-]{1,}(?![\w-])')
ALLOWED_LATIN = {'ok', 'wi-fi', 'wifi', 'pro', 'usb', 'gps', 'tv', 'pdf', 'seo', 'crm', 'it', 'b2b', 'vip', 'xl', 'xxl', 's', 'm', 'l'}
FOREIGN_RISK = {'sale', 'new', 'best', 'seller', 'bestseller', 'free', 'shop', 'store', 'hit', 'top', 'premium', 'outlet', 'discount', 'black', 'friday', 'cashback', 'online'}


def visible(s):
    """Direct templates #default text# are shown without the # signs."""
    return s.replace('#', '')


def count_len(s, narrow_free=False):
    s = visible(s)
    if not narrow_free:
        return len(s), 0
    narrow = sum(1 for c in s if c in NARROW)
    return len(s) - narrow, narrow


def words(s):
    return re.findall(r'[\w\-]+', visible(s))


def check_field(kind, value, lim, issues, where, narrow_free=False):
    n, narrow = count_len(value, narrow_free)
    if n == 0:
        issues.append(('error', where, f'{kind}: empty'))
        return
    if n > lim['max']:
        issues.append(('error', where, f'{kind}: {n} chars > {lim["max"]}: «{value}»'))
    if narrow_free and narrow > L['text']['narrow_max']:
        issues.append(('error', where, f'{kind}: {narrow} narrow chars (!,.;:") > {L["text"]["narrow_max"]}'))
    wmax = lim.get('word_max')
    if wmax:
        for w in words(value):
            if len(w) > wmax:
                issues.append(('error', where, f'{kind}: word «{w}» {len(w)} chars > {wmax}'))


def copy_rules(kind, value, issues, where, trademarks):
    v = visible(value)
    if PLACEHOLDER.search(v):
        issues.append(('error', where, f'{kind}: placeholder left in text'))
    if kind.startswith('title') and '!' in v:
        issues.append(('warn', where, f'{kind}: «!» in a headline is a moderation risk'))
    if v.count('!') > 1:
        issues.append(('warn', where, f'{kind}: more than one «!»'))
    tml = {t.lower() for t in trademarks}
    caps = [w for w in words(v) if len(w) > 4 and w.isupper() and not w.isdigit() and w.lower() not in tml]
    if caps:
        issues.append(('warn', where, f'{kind}: words in CAPS {caps} (allowed only for abbreviations and brands)'))
    m = SUPERLATIVE.search(v)
    if m:
        issues.append(('warn', where, f'{kind}: «{m.group(0)}» needs proof on the landing page (38-ФЗ ст. 5: unproven superlatives)'))
    tm = {t.lower() for t in trademarks}
    for w in LATIN_WORD.findall(v):
        lw = w.lower()
        if lw in tm or lw in ALLOWED_LATIN:
            continue
        level = 'warn'
        note = 'Latin word: allowed only as a registered trademark or a term without a Russian equivalent (rule from 01.03.2026)'
        if lw in FOREIGN_RISK:
            note = 'foreign word with a Russian equivalent - replace it (rule from 01.03.2026)'
        issues.append((level, where, f'{kind}: «{w}» - {note}'))
    if re.search(r'\s{2,}', v) or v != v.strip():
        issues.append(('warn', where, f'{kind}: extra spaces'))
    if re.search(r'\s[,.;:!?]', v):
        issues.append(('warn', where, f'{kind}: space before punctuation'))


def check_ad(ad):
    issues = []
    aid = ad.get('id', '?')
    tm = ad.get('trademarks', [])
    titles = ad.get('titles') or ([ad['title']] if ad.get('title') else [])
    texts = ad.get('texts') or ([ad['text']] if ad.get('text') else [])
    if not titles:
        issues.append(('error', aid, 'no headline'))
    if not texts:
        issues.append(('error', aid, 'no text'))
    if len(titles) > L['title']['count_in_combinatorial']:
        issues.append(('error', aid, f'{len(titles)} headlines > {L["title"]["count_in_combinatorial"]}'))
    if len(texts) > L['text']['count_in_combinatorial']:
        issues.append(('error', aid, f'{len(texts)} texts > {L["text"]["count_in_combinatorial"]}'))
    for i, t in enumerate(titles, 1):
        check_field(f'title{i}' if len(titles) > 1 else 'title', t, L['title'], issues, aid)
        copy_rules('title', t, issues, aid, tm)
    if len({visible(t).lower() for t in titles}) < len(titles):
        issues.append(('warn', aid, 'duplicate headlines in a combinatorial ad'))
    for i, t in enumerate(texts, 1):
        check_field(f'text{i}' if len(texts) > 1 else 'text', t, L['text'], issues, aid, narrow_free=True)
        copy_rules('text', t, issues, aid, tm)
    if ad.get('title2'):
        issues.append(('warn', aid, 'title2: combinatorial ads in ЕПК have no second headline (July 2026); merge into the headline (≤ 56) or drop'))
        check_field('title2', ad['title2'], L['title2'], issues, aid)
    if ad.get('display_link') is not None:
        dl = ad['display_link']
        if len(dl) > L['display_link']['max']:
            issues.append(('error', aid, f'display_link {len(dl)} > {L["display_link"]["max"]}'))
        if re.search(r'[^\w\-№/#]', dl.replace('/', '')):
            issues.append(('warn', aid, 'display_link: only letters, digits, «-», «№», «/», «#» are allowed'))
    href = ad.get('href')
    if href:
        if len(href) > L['href']['max']:
            issues.append(('error', aid, f'href {len(href)} > {L["href"]["max"]}'))
        if not href.startswith(('https://', 'http://')):
            issues.append(('error', aid, 'href must start with https://'))
        elif href.startswith('http://'):
            issues.append(('warn', aid, 'href over http: use https'))
        if 'utm_' not in href and '{' not in href:
            issues.append(('warn', aid, 'href without UTM or Direct parameters: reports will not separate the traffic'))
    sl = ad.get('sitelinks', [])
    if sl:
        if len(sl) > L['sitelinks']['max']:
            issues.append(('error', aid, f'{len(sl)} sitelinks > {L["sitelinks"]["max"]}'))
        for i, s in enumerate(sl, 1):
            check_field(f'sitelink{i}.title', s.get('title', ''), L['sitelink_title'], issues, aid)
            if s.get('description'):
                check_field(f'sitelink{i}.description', s['description'], L['sitelink_description'], issues, aid)
        tot = sum(len(s.get('title', '')) for s in sl[:4])
        if tot > L['sitelink_title']['total_1_4_max']:
            issues.append(('warn', aid, f'sitelinks 1-4 titles total {tot} > {L["sitelink_title"]["total_1_4_max"]}: some may be hidden on search (unconfirmed limit)'))
        if len({s.get('title', '').lower() for s in sl}) < len(sl):
            issues.append(('error', aid, 'duplicate sitelink titles'))
    if len(sl) < L['sitelinks']['min_recommended']:
        issues.append(('warn', aid, f'{len(sl)} sitelinks: add at least {L["sitelinks"]["min_recommended"]}'))
    co = ad.get('callouts', [])
    for c in co:
        if len(c) > L['callout']['max']:
            issues.append(('error', aid, f'callout «{c}» {len(c)} > {L["callout"]["max"]}'))
    tot = sum(len(c) for c in co)
    if tot > L['callout']['total_mobile']:
        issues.append(('warn', aid, f'callouts total {tot} > {L["callout"]["total_mobile"]} (mobile) {"and > " + str(L["callout"]["total_desktop"]) + " (desktop)" if tot > L["callout"]["total_desktop"] else ""}: the tail is hidden'))
    if len(co) < L['callout']['min_recommended']:
        issues.append(('warn', aid, f'{len(co)} callouts: add at least {L["callout"]["min_recommended"]}'))
    if 'images' in ad and ad['images'] < L['images_min_recommended']:
        issues.append(('warn', aid, f'{ad["images"]} images: give at least {L["images_min_recommended"]} for РСЯ'))
    return issues


def main(argv):
    if not argv or argv[0] in ('-h', '--help'):
        print(__doc__)
        return 0
    data = json.loads(pathlib.Path(argv[0]).read_text(encoding='utf-8'))
    ads = data if isinstance(data, list) else data.get('ads', [data])
    allissues = []
    for ad in ads:
        allissues += check_ad(ad)
    errors = sum(1 for i in allissues if i[0] == 'error')
    if '--json' in argv:
        print(json.dumps([{'level': a, 'ad': b, 'message': c} for a, b, c in allissues], ensure_ascii=False, indent=2))
    else:
        for a, b, c in allissues:
            print(f'{a.upper():5} [{b}] {c}')
        print(f'\n{len(ads)} ads · {errors} errors · {len(allissues) - errors} warnings · limits checked_at {json.loads((ROOT / "data/limits.json").read_text())["checked_at"]}')
    return 1 if errors else 0


if __name__ == '__main__':
    try:
        sys.exit(main(sys.argv[1:]))
    except BrokenPipeError:
        sys.exit(0)

"""Roll localized versions of one creative up to its base creative.

A localized version is the same ad with only league details swapped (city, venue,
day, time, price). The report shows one card per base creative and sums every
version's spend, revenue and purchases into it.

Usage:
  python3 -I creative_key.py aliases <board_items.json> aliases.json
      board_items.json = monday Ad Assets board (18438645485) items with
      `name` and column `text_mm8xx3cw` (Meta Ad Name). One item = one base
      creative; its Meta Ad Name lists every version's ad name, "; "-separated.
  python3 -I creative_key.py check aliases.json "<ad name>" ...
      prints base key and display name for each ad name (for spot checks).

In report code:
  from creative_key import load_aliases, base
  A = load_aliases('aliases.json'); k, label = base(ad_name, A)
  group rows by k; show label on the card.
"""
import json, re, sys

# {Season}_{Market[-Venue]}_{sport}_{Concept}_{Format}_v{n}[-variant][_size...]
CONV = re.compile(r'^(?P<season>[A-Z]{1,3}\d{2})_(?P<market>[^_]+)_(?P<sport>pb|vb)_'
                  r'(?P<concept>[^_]+)_(?P<fmt>Static|Video|UGC|Carousel|GIF)_(?P<ver>v\d+)', re.I)


def norm(n):
    """Same normalization as fatigue.py, so keys line up."""
    n = re.sub(r'\s*-\s*Copy(\s*\d+)?$', '', n.strip())
    n = re.sub(r'^AllGeos_Pickleball_', '', n)
    n = re.sub(r'_(1080x1920|Video_1080x1920|Static_4:5|Static|Video|Carousel)$', '', n)
    return n.lower().replace(' ', '')


def conv_key(name):
    m = CONV.match(name.strip())
    if not m:
        return None
    d = {k: v.lower() for k, v in m.groupdict().items()}
    return f"{d['sport']}_{d['concept']}_{d['fmt']}_{d['ver']}"


def load_aliases(path):
    return json.load(open(path))


def base(ad_name, aliases):
    """Return (group_key, display_label) for one Meta/TikTok ad name.
    Order: board alias -> naming convention (market and season dropped) ->
    `_Localized_` template name -> plain normalized name."""
    n = norm(ad_name)
    if n in aliases['by_name']:
        a = aliases['by_name'][n]
        return a['key'], a['label']
    k = conv_key(ad_name)
    if k:
        return k, aliases['label_by_key'].get(k, ad_name)
    return n, ad_name


def build_aliases(items):
    by_name, label_by_key = {}, {}
    for it in items:
        cols = {c['id']: (c.get('text') or '') for c in it.get('column_values', [])}
        names = [s.strip() for s in cols.get('text_mm8xx3cw', '').split(';') if s.strip()]
        if not names:
            continue
        # group key: the convention key of the first name that follows the convention,
        # else the first (base) name normalized
        key = next((conv_key(s) for s in names if conv_key(s)), None) or norm(names[0])
        # Several board items can share one Meta ad (e.g. 3 flyer designs run as one
        # flexible-format ad). Meta can't split them, so they share a card and a label.
        prev = label_by_key.get(key)
        label = it['name'] if not prev or prev == it['name'] else f"{prev} / {it['name']}"
        label_by_key[key] = label
        for s in names:
            by_name[norm(s)] = {'key': key}
    for v in by_name.values():
        v['label'] = label_by_key[v['key']]
    return {'by_name': by_name, 'label_by_key': label_by_key}


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'aliases':
        raw = json.load(open(sys.argv[2]))
        raw = raw.get('data', raw) if isinstance(raw, dict) else raw
        if isinstance(raw, list):
            items = raw
        elif 'boards' in raw:  # monday GraphQL: boards { items_page { items { ... } } }
            items = [i for b in raw['boards'] for i in b['items_page']['items']]
        else:
            items = raw['items']
        A = build_aliases(items)
        json.dump(A, open(sys.argv[3], 'w'), indent=1)
        multi = {}
        for v in A['by_name'].values():
            multi[v['key']] = multi.get(v['key'], 0) + 1
        print(f"{len(A['by_name'])} ad names -> {len(A['label_by_key'])} base creatives; "
              f"{sum(1 for c in multi.values() if c > 1)} have 2+ versions")
    elif cmd == 'check':
        A = load_aliases(sys.argv[2])
        for n in sys.argv[3:]:
            print(n, '->', base(n, A))

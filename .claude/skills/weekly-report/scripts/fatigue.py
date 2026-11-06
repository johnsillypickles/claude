"""Creative fatigue check for the weekly creative report.

Fatigue is scored PER AD SET (John, 2026-11-06): a creative can wear out in one location and
still be fresh in another, and a brand new market starts with zero fatigued ads. History is
keyed "<ad set name>||<normalized creative>", never by creative alone.

Works from a compact weekly history of Meta ad-level results (Monday-to-Sunday weeks).

  # 1. add one or more pulls to the history file. Each pull must carry the ad set name:
  #    - Windsor `facebook` daily rows (fields date, adset_name, ad_name, spend, impressions,
  #      clicks, actions_purchase, action_values_purchase, actions_add_to_cart; whole account,
  #      no filters, so the account totals are right), or
  #    - a Lebesgue ad-level pull whose rows include the ad set name (adset_name or adset).
  python3 fatigue.py add  HISTORY.json PULL.json [PULL.json ...]
  # history lives in a private Google Sheet (the repo is public): convert both ways
  python3 fatigue.py to-rows   HISTORY.json OUT.json [--weeks 2026-10-12 ...]  # rows for Sheets
  python3 fatigue.py from-sheet SHEET_VALUES.json HISTORY.json                  # get_values result
  # 2. score the creatives in the report and back-test the rules on all history
  python3 fatigue.py score HISTORY.json --report data.json --end 2026-10-05 --out fatigue.json

`score` writes the object the creative report template expects under D.fatigue.
Rules come from the Jan 2025 to Oct 2026 study (see SKILL.md, "Creative fatigue").
"""
import json, re, sys, argparse, datetime as dt, statistics as st

F = ['spend', 'impressions', 'clicks', 'purchases', 'purchases_conversion_value', 'add_to_cart']
ACTIVE = 100          # a creative's week in one ad set counts once it spends $100+ there
SEP = '||'            # history key: "<ad set>||<normalized creative>"
FATIGUED = 0.60       # 2-week ROAS index at or below 60% of its best 2-week stretch
AGE_WEEKS = 8         # warning: 8+ active weeks
CTR_DROP = 0.85       # warning: click rate down 15%+ vs its first 2 active weeks
ROAS_DROP = 0.75      # warning: ROAS index down 25%+ vs its best 2-week stretch
CONV_DROP = 0.60      # warning: purchases per click down 40%+ vs its first 2 active weeks


def norm(n):
    n = re.sub(r'\s*-\s*Copy(\s*\d+)?$', '', n.strip())
    n = re.sub(r'^AllGeos_Pickleball_', '', n)
    n = re.sub(r'_(1080x1920|Video_1080x1920|Static_4:5|Static|Video|Carousel)$', '', n)
    return n.lower().replace(' ', '')


def key(adset, ad_name):
    return f"{adset.strip()}{SEP}{norm(ad_name)}"


def split_key(k):
    a, _, c = k.partition(SEP)
    return a, c


def phase_of(adset):
    """P0 = Phase 0 / metro P0 ad sets; everything else counts as Phase 1."""
    return 'p0' if re.search(r'(?i)phase0|(^|_)p0($|_)', adset) else 'p1'


def monday(d):
    d = dt.date.fromisoformat(d)
    return str(d - dt.timedelta(d.weekday()))


def _rows(d):
    """Normalize a pull to (date or None, adset, ad name, [F values]) plus its date span."""
    if isinstance(d, dict) and 'rows' in d and d.get('source') == 'facebook':  # Lebesgue
        if d.get('level') != 'ad':
            sys.exit('not a Meta ad-level pull')
        if d['period_type'] == 'all' and monday(d['start_date']) != monday(d['end_date']):
            sys.exit('an "all" pull must sit inside one Mon-Sun week')
        out = []
        for r in d['rows']:
            a = r.get('adset_name') or r.get('adset')
            if not a:
                sys.exit('Lebesgue rows have no ad set name: fatigue is per ad set, pull from Windsor instead')
            day = r['date'] if d['period_type'] == 'week_monday' else d['start_date']
            out.append((day, a, r['name'], [r.get(f) or 0 for f in F]))
        return out, d['start_date'], d['end_date']
    rows = d.get('data', d) if isinstance(d, dict) else d  # Windsor
    wf = ['spend', 'impressions', 'clicks', 'actions_purchase', 'action_values_purchase', 'actions_add_to_cart']
    out = [(r['date'], r.get('adset_name') or '', r['ad_name'], [float(r.get(f) or 0) for f in wf]) for r in rows]
    if any(not o[1] for o in out):
        sys.exit('some Windsor rows have no adset_name')
    days = sorted(o[0] for o in out)
    return out, days[0], days[-1]


def add(hist_path, pulls):
    try:
        H = json.load(open(hist_path))
    except FileNotFoundError:
        H = {'weeks': {}, 'names': {}}
    for p in pulls:
        d = json.load(open(p))
        rows, start, end = _rows(d.get('result', d) if isinstance(d, dict) else d)
        for day, adset, name, vals in rows:
            w = monday(day)
            k = key(adset, name)
            H['names'].setdefault(k, [name, adset])
            W = H['weeks'].setdefault(w, {'acct': [0] * len(F), 'ads': {}, 'days': []})
            a = W['ads'].setdefault(k, [0] * len(F))
            for i, v in enumerate(vals):
                a[i] += v
                W['acct'][i] += v
        # remember which days each week holds so a week is never added twice
        s, e = dt.date.fromisoformat(start), dt.date.fromisoformat(end)
        while s <= e:
            W = H['weeks'].setdefault(monday(str(s)), {'acct': [0] * len(F), 'ads': {}, 'days': []})
            if str(s) in W['days']:
                sys.exit(f'{p}: {s} is already in the history')
            W['days'].append(str(s))
            s += dt.timedelta(1)
    json.dump(H, open(hist_path, 'w'), separators=(',', ':'))
    bad = [w for w, W in H['weeks'].items() if len(W['days']) != 7]
    print(f"{len(H['weeks'])} weeks, {len(H['names'])} creative x ad set pairs; incomplete weeks: {sorted(bad) or 'none'}")


def series(H, k, end):
    """Active weeks for creative k up to `end`, oldest first."""
    out = []
    for w in sorted(H['weeks']):
        if w > end:
            break
        a = H['weeks'][w]['ads'].get(k)
        if a and a[0] >= ACTIVE:
            out.append((w, a, H['weeks'][w]['acct']))
    return out


def idx(rows):
    """Pooled ROAS of the creative divided by pooled account ROAS for the same weeks."""
    s = sum(r[1][0] for r in rows); v = sum(r[1][4] for r in rows)
    As = sum(r[2][0] for r in rows); Av = sum(r[2][4] for r in rows)
    return (v / s) / (Av / As) if s and Av else None


def rate(rows, num, den):
    n = sum(r[1][num] for r in rows); d = sum(r[1][den] for r in rows)
    return n / d if d else None


def profile(S):
    """Signals at the last week of S. Needs 3+ active weeks."""
    first, now = S[:2], S[-2:]
    ix = [idx(S[max(0, j - 1):j + 1]) for j in range(len(S))]
    best_j = max(range(1, len(S)), key=lambda j: ix[j] or 0)
    ctr0, ctr1 = rate(first, 2, 1), rate(now, 2, 1)
    cv0, cv1 = rate(first, 3, 2), rate(now, 3, 2)
    p = {
        'weeks': len(S), 'launch': S[0][0], 'first': [first[0][0], first[-1][0]],
        'best': [S[max(0, best_j - 1)][0], S[best_j][0]], 'now': [now[0][0], now[-1][0]],
        'ix_best': ix[best_j], 'ix_now': ix[-1],
        'ctr0': ctr0, 'ctr1': ctr1, 'conv0': cv0, 'conv1': cv1,
        'roas_now': rate(now, 4, 0), 'roas_best': rate(S[max(0, best_j - 1):best_j + 1], 4, 0),
    }
    p['ix_ratio'] = (p['ix_now'] / p['ix_best']) if p['ix_now'] is not None and p['ix_best'] else None
    p['ctr_ratio'] = ctr1 / ctr0 if ctr0 and ctr1 is not None else None
    p['conv_ratio'] = cv1 / cv0 if cv0 and cv1 is not None else None
    return p


def warnings(p):
    w = []
    if p['weeks'] >= AGE_WEEKS: w.append('age')
    if p['ctr_ratio'] is not None and p['ctr_ratio'] <= CTR_DROP: w.append('ctr')
    if p['ix_ratio'] is not None and p['ix_ratio'] <= ROAS_DROP: w.append('roas')
    if p['conv_ratio'] is not None and p['conv_ratio'] <= CONV_DROP: w.append('conv')
    return w


def verdict(p):
    if p is None or p['weeks'] < 3: return 'New'
    if p['ix_ratio'] is not None and p['ix_ratio'] <= FATIGUED: return 'Fatigued'
    return 'Watch' if len(warnings(p)) >= 2 else 'Fresh'


def backtest(H, end):
    """Find fatigue onsets in history and check how often the Watch rule fired beforehand."""
    names = [k for k in H['names']]
    tested = 0
    onsets, pre1, pre2, healthy, post = [], [], [], [], [0, 0, 0]
    for k in names:
        S = series(H, k, end)
        if len(S) < 6 or sum(r[1][0] for r in S) < 1500:
            continue
        tested += 1
        ix = [idx(S[max(0, j - 1):j + 1]) for j in range(len(S))]
        peak_j = max(range(1, len(S)), key=lambda j: ix[j] or 0)
        peak = ix[peak_j]
        on = None
        for j in range(peak_j + 1, len(S)):
            later = ix[j:j + 3]
            if ix[j] is not None and ix[j] < FATIGUED * peak and all(l is not None and l < 0.75 * peak for l in later):
                on = j
                break
        if on is not None:
            onsets.append({'name': ' @ '.join(H['names'][k]) if isinstance(H['names'][k], list) else k, 'week': S[on][0], 'weeks_live': on + 1,
                           'spend_before': round(sum(r[1][0] for r in S[:on]))})
            for r in S[on:]:
                post[0] += r[1][0]; post[1] += r[1][4]; post[2] += r[1][0] * r[2][4] / r[2][0]
        for j in range(2, len(S)):
            fired = len(warnings(profile(S[:j + 1]))) >= 2
            if on is not None and on - j == 1: pre1.append(fired)
            if on is not None and on - j == 2: pre2.append(fired)
            fut = ix[j + 1:j + 4]
            if (on is None or j < on - 3) and len(fut) == 3 and all(f and f >= 0.75 * peak for f in fut):
                healthy.append(fired)
    pct = lambda l: round(100 * sum(l) / len(l)) if l else None
    wl = [o['weeks_live'] for o in onsets]
    return {
        'span': [min(H['weeks']), end], 'creatives_tested': tested, 'onsets': len(onsets),
        'median_weeks_to_fatigue': st.median(wl) if wl else None, 'weeks_range': [min(wl), max(wl)] if wl else None,
        'watch_1wk_before_pct': pct(pre1), 'watch_2wk_before_pct': pct(pre2), 'watch_healthy_pct': pct(healthy),
        'n_pre1': len(pre1), 'n_healthy': len(healthy),
        'post_spend': round(post[0]), 'post_roas': round(post[1] / post[0], 2) if post[0] else None,
        'post_acct_roas': round(post[2] / post[0], 2) if post[0] else None,
    }


def action(v, roas, ph, running, avg0, avg1):
    """Suggested next step for one creative IN ONE AD SET. Returns (kind, text).
    kind: pause, keep, scale, restart, review, new, off. Compares the pair's last-2-week ROAS
    with the average of its ad set's phase, so a worn-out ad that still beats it is kept."""
    avg, name = (avg0, 'Phase 0') if ph == 'p0' else (avg1, 'Phase 1')
    r = roas or 0
    if v == 'Fatigued':
        if not running:
            return 'off', 'Already off in this ad set. Leave it off here.'
        if r >= avg:
            return 'keep', f'Still beats the {name} average here ({r:.2f}x vs {avg:.2f}x). Keep for now and line up a replacement in this ad set.'
        return 'pause', f'Pause in this ad set only: {r:.2f}x vs the {name} average of {avg:.2f}x. It can keep running elsewhere. Check this ad set keeps 2+ live ads.'
    if not running:
        if v == 'Fresh' and r >= avg:
            return 'restart', f'Off here, but it was beating the {name} average ({r:.2f}x vs {avg:.2f}x). Consider turning it back on.'
        return 'off', 'Not running in this ad set.'
    if v == 'Watch':
        return 'review', 'Review in this ad set this week; no pause yet (Watch is an early flag).'
    if v == 'Fresh':
        if r >= 1.15 * avg:
            return 'scale', f'Keep, and give it more budget here ({r:.2f}x vs {avg:.2f}x {name} average).'
        return 'keep', 'Keep.'
    if v == 'New':
        return 'new', 'New in this ad set (under 3 live weeks here): not fatigued.'
    return 'off', 'Not running in this ad set.'


def score(hist_path, report, end, out):
    """One row per creative x ad set it ran in during the last 2 weeks."""
    H = json.load(open(hist_path))
    D = json.load(open(report))
    rows = []
    avg0, avg1 = D['portfolio']['p0']['roas'], D['portfolio']['p1']['roas']
    prev = str(dt.date.fromisoformat(end) - dt.timedelta(7))
    for c in D['creatives']:
        cn = norm(c['name'])
        keys = [k for k in H['names'] if split_key(k)[1] == cn]
        for k in keys:
            adset = split_key(k)[0]
            recent = [H['weeks'].get(w, {}).get('ads', {}).get(k) for w in (prev, end)]
            recent = [a for a in recent if a]
            if not any(a[0] >= ACTIVE for a in recent):
                continue  # not live in this ad set in the last 2 weeks
            S = series(H, k, end)
            p = profile(S) if len(S) >= 3 else None
            v = verdict(p)
            if p and p['now'][-1] < prev:
                v = 'Not live'
            sp = sum(a[0] for a in recent)
            roas = (sum(a[4] for a in recent) / sp) if sp else None
            wk_end = H['weeks'].get(end, {}).get('ads', {}).get(k)
            running = bool(wk_end and wk_end[0] > 0)
            ph = phase_of(adset)
            kd, txt = action(v, roas, ph, running, avg0, avg1)
            rows.append({'name': c['name'], 'adset': adset, 'phase': ph, 'verdict': v,
                         'signals': warnings(p) if p else [], 'p': p, 'spend': sp, 'roas': roas,
                         'history_weeks': len(S), 'launch': S[0][0] if S else None,
                         'action_kind': kd, 'action': txt,
                         'split': {'pause': sp} if kd == 'pause' else {'off': sp} if kd == 'off' else {'keep': sp}})
    res = {'end_week': end, 'rows': rows, 'evidence': backtest(H, end), 'per_adset': True,
           'rules': {'active': ACTIVE, 'fatigued': FATIGUED, 'age': AGE_WEEKS, 'ctr': CTR_DROP,
                     'roas': ROAS_DROP, 'conv': CONV_DROP}}
    json.dump(res, open(out, 'w'), indent=1)
    from collections import Counter
    print(Counter(r['verdict'] for r in rows), res['evidence'])


HEAD = ['week', 'key'] + F  # only $100+ creative x ad set weeks are stored; that's all scoring uses


def to_rows(hist_path, out, weeks=None):
    H = json.load(open(hist_path))
    rows = [] if weeks else [HEAD]
    for w in sorted(H['weeks']):
        if weeks and w not in weeks:
            continue
        W = H['weeks'][w]
        rows.append([w, '__account__'] + [round(x) for x in W['acct']])
        for k, a in sorted(W['ads'].items()):
            if a[0] >= ACTIVE:
                rows.append([w, k] + [round(x) for x in a])
    json.dump(rows, open(out, 'w'))
    print(len(rows), 'rows')


def from_sheet(values_path, hist_path):
    d = json.load(open(values_path))
    vals = d.get('values') or d.get('result', {}).get('values') or d
    H = {'weeks': {}, 'names': {}}
    for r in vals:
        if r[0] == 'week':
            continue
        w, k = r[0], r[1]
        nums = [float(x or 0) for x in r[2:2 + len(F)]]
        W = H['weeks'].setdefault(w, {'acct': [0] * len(F), 'ads': {}, 'days': [
            str(dt.date.fromisoformat(w) + dt.timedelta(i)) for i in range(7)]})
        if k == '__account__':
            W['acct'] = nums
        elif SEP in k:
            W['ads'][k] = nums
            H['names'][k] = list(reversed(split_key(k)))
        # rows keyed by creative alone are the pre-11/6 history: not usable per ad set, skipped
    json.dump(H, open(hist_path, 'w'), separators=(',', ':'))
    print(len(H['weeks']), 'weeks', len(H['names']), 'creatives')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest='cmd', required=True)
    a = sp.add_parser('add'); a.add_argument('history'); a.add_argument('pulls', nargs='+')
    s = sp.add_parser('score'); s.add_argument('history'); s.add_argument('--report', required=True)
    s.add_argument('--end', required=True, help='Monday of the last week in the report window')
    s.add_argument('--out', required=True)
    t = sp.add_parser('to-rows'); t.add_argument('history'); t.add_argument('out'); t.add_argument('--weeks', nargs='*')
    f = sp.add_parser('from-sheet'); f.add_argument('values'); f.add_argument('history')
    x = ap.parse_args()
    if x.cmd == 'add': add(x.history, x.pulls)
    elif x.cmd == 'score': score(x.history, x.report, x.end, x.out)
    elif x.cmd == 'to-rows': to_rows(x.history, x.out, x.weeks)
    else: from_sheet(x.values, x.history)

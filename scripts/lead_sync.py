"""Pull recent Meta lead form leads for the W27 new-venue forms.

Usage: python3 scripts/lead_sync.py [--hours 3]
Reads META_ACCESS_TOKEN (needs leads_retrieval). Prints JSON: one entry per lead with
the Klaviyo list it belongs in. The caller (scheduled session) subscribes each person
to that list with the Klaviyo connector. Re-adding a lead is harmless, so the lookback
window overlaps between hourly runs on purpose.
"""
import argparse, json, os, sys, time, urllib.parse, urllib.request

B = 'https://graph.facebook.com/v21.0/'
CFG = os.path.join(os.path.dirname(__file__), 'lead_sync_config.json')


def get(path, **q):
    q['access_token'] = os.environ['META_ACCESS_TOKEN']
    url = B + path + '?' + urllib.parse.urlencode(q)
    out = []
    while url:
        d = json.load(urllib.request.urlopen(url))
        out += d.get('data', [])
        url = d.get('paging', {}).get('next')
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--hours', type=float, default=3)
    a = ap.parse_args()
    cfg = json.load(open(CFG))
    since = int(time.time() - a.hours * 3600)
    flt = json.dumps([{'field': 'time_created', 'operator': 'GREATER_THAN', 'value': since}])
    rows, errors = [], []
    for slug, f in cfg['forms'].items():
        try:
            leads = get(f"{f['form_id']}/leads", fields='id,created_time,field_data', filtering=flt, limit=100)
        except urllib.error.HTTPError as e:
            errors.append({'slug': slug, 'error': e.read().decode()[:300]})
            continue
        for l in leads:
            fd = {x['name']: (x.get('values') or [''])[0] for x in l.get('field_data', [])}
            list_id = f.get('list_id')
            loc = fd.get('which_center_court_location?')
            if loc and f.get('location_lists'):
                list_id = f['location_lists'].get(loc, list_id)
            rows.append({'slug': slug, 'lead_id': l['id'], 'created': l['created_time'],
                         'email': fd.get('email', '').strip().lower(), 'first_name': fd.get('first_name', ''),
                         'phone': fd.get('phone_number', ''), 'location': loc,
                         'skill': fd.get("what's_your_pickleball_skill_level?"),
                         'solo_or_friend': fd.get('are_you_signing_up_solo_or_with_a_friend?'),
                         'list_id': list_id})
    json.dump({'since_unix': since, 'count': len(rows), 'leads': rows, 'errors': errors}, sys.stdout, indent=1)


if __name__ == '__main__':
    main()

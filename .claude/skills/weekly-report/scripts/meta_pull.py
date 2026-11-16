"""Pull Meta insights through the Graph API (META_ACCESS_TOKEN) as flat rows in the old Windsor field names,
so fatigue.py, locgen and the report builders keep working.

Usage:
  python3 -I meta_pull.py --level ad --since 2026-11-09 --until 2026-11-15 [--daily] [--filter-campaign LeadForm] --out rows.json

Output: a JSON list of rows with: date (if --daily), date_start, date_stop, campaign, campaign_id, adset_name, adset_id,
ad_name, ad_id (ad level), spend, impressions, reach, frequency, clicks, inline_link_clicks, quality_ranking (ad level),
actions_purchase, action_values_purchase, actions_add_to_cart, actions_lead.
Purchases are Meta's pixel purchases (offsite_conversion.fb_pixel_purchase), the same number Lebesgue and Ads Manager show.
Never prints the token.
"""
import argparse, json, os, sys, time, urllib.parse, urllib.request

G = 'https://graph.facebook.com/v21.0'
ACCT = 'act_1346441932978787'
PURCHASE = 'offsite_conversion.fb_pixel_purchase'
ATC = 'offsite_conversion.fb_pixel_add_to_cart'


def get(url, params=None):
    if params is not None:
        url = url + '?' + urllib.parse.urlencode(params)
    for attempt in range(5):
        try:
            with urllib.request.urlopen(url, timeout=120) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            body = json.load(e)
            msg = body.get('error', {}).get('message', str(e))
            if attempt < 4 and ('limit' in msg.lower() or e.code >= 500):
                time.sleep(10 * (attempt + 1)); continue
            sys.exit('Graph API error: ' + msg)


def post(url, params):
    data = urllib.parse.urlencode(params).encode()
    with urllib.request.urlopen(urllib.request.Request(url, data=data), timeout=120) as r:
        return json.load(r)


def pick(lst, key):
    for a in lst or []:
        if a.get('action_type') == key:
            return float(a.get('value') or 0)
    return 0.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--level', choices=['account', 'campaign', 'adset', 'ad'], required=True)
    ap.add_argument('--since', required=True); ap.add_argument('--until', required=True)
    ap.add_argument('--daily', action='store_true')
    ap.add_argument('--filter-campaign', help='keep campaigns whose name contains this text')
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    tok = os.environ.get('META_ACCESS_TOKEN') or sys.exit('META_ACCESS_TOKEN is not set')
    fields = ['campaign_name', 'campaign_id', 'spend', 'impressions', 'reach', 'frequency', 'clicks',
              'inline_link_clicks', 'actions', 'action_values']
    if a.level in ('adset', 'ad'):
        fields += ['adset_name', 'adset_id']
    if a.level == 'ad':
        fields += ['ad_name', 'ad_id', 'quality_ranking']
    p = {'access_token': tok, 'level': a.level, 'fields': ','.join(fields),
         'time_range': json.dumps({'since': a.since, 'until': a.until}), 'limit': 500}
    if a.daily:
        p['time_increment'] = 1
    if a.filter_campaign:
        p['filtering'] = json.dumps([{'field': 'campaign.name', 'operator': 'CONTAIN', 'value': a.filter_campaign}])
    # async report: large ad-level pulls time out as a plain GET
    run = post(f'{G}/{ACCT}/insights', dict(p, **{'async': 'true'}))
    rid = run.get('report_run_id') or sys.exit('no report_run_id: ' + json.dumps(run)[:300])
    while True:
        st = get(f'{G}/{rid}', {'access_token': tok, 'fields': 'async_status,async_percent_completion'})
        if st.get('async_status') == 'Job Completed':
            break
        if st.get('async_status') in ('Job Failed', 'Job Skipped'):
            sys.exit('report failed: ' + st.get('async_status'))
        time.sleep(5)
    rows, url, q = [], f'{G}/{rid}/insights', {'access_token': tok, 'limit': 500}
    while url:
        d = get(url, q); q = None
        for r in d.get('data', []):
            out = {k: r.get(k) for k in ('date_start', 'date_stop', 'campaign_id', 'adset_name', 'adset_id',
                                         'ad_name', 'ad_id', 'quality_ranking') if k in r}
            out['campaign'] = r.get('campaign_name')
            if a.daily:
                out['date'] = r.get('date_start')
            for k in ('spend', 'impressions', 'reach', 'frequency', 'clicks', 'inline_link_clicks'):
                out[k] = float(r.get(k) or 0)
            out['actions_purchase'] = pick(r.get('actions'), PURCHASE)
            out['action_values_purchase'] = pick(r.get('action_values'), PURCHASE)
            out['actions_add_to_cart'] = pick(r.get('actions'), ATC)
            out['actions_lead'] = pick(r.get('actions'), 'lead')
            rows.append(out)
        url = d.get('paging', {}).get('next')
    json.dump(rows, open(a.out, 'w'))
    print(len(rows), 'rows, spend', round(sum(r['spend'] for r in rows), 2),
          'purchases', round(sum(r['actions_purchase'] for r in rows)),
          'value', round(sum(r['action_values_purchase'] for r in rows), 2))


if __name__ == '__main__':
    main()

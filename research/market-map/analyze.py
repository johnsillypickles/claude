import json,sys,collections,statistics as st
sys.path.insert(0,'.')
from metros import metro_of
Q=['q1','q2','q3']
ads={q:collections.defaultdict(lambda:{'spend':0,'purch':0,'lp_new':0,'adsets':0}) for q in Q}
prod={q:collections.defaultdict(lambda:{'orders':0,'new':0,'rev':0,'leagues':0}) for q in Q}
tot={q:{'spend':0,'purch':0,'lp_new':0,'local_spend':0} for q in Q}
for q in Q:
    for r in json.load(open(f'ads_{q}.json'))['rows']:
        t=tot[q]; t['spend']+=r['spend']; t['purch']+=r['purchases'] or 0; t['lp_new']+=r.get('pixel_purchases') or 0
        m=metro_of(r['name'])
        if 'leadform' in r['name'].lower(): continue
        if m:
            a=ads[q][m]; a['spend']+=r['spend']; a['purch']+=r['purchases'] or 0; a['lp_new']+=r.get('pixel_purchases') or 0; a['adsets']+=1
            t['local_spend']+=r['spend']
    for r in json.load(open(f'prod_{q}.json'))['rows']:
        m=metro_of(r['name'])
        if m and (r['orders'] or 0)>0:
            p=prod[q][m]; p['orders']+=r['orders']; p['new']+=r['first_time_orders']; p['rev']+=r['revenue']; p['leagues']+=1
for q in Q:
    t=tot[q]; print(q, {k:round(v) for k,v in t.items()}, 'acct CAC', round(t['spend']/t['purch'],2), 'local share', round(t['local_spend']/t['spend'],3))
metros=sorted(set(m for q in Q for m in list(ads[q])+list(prod[q])))
rows=[]
for m in metros:
    r={'metro':m,'q':{}}
    for q in Q:
        a=ads[q].get(m,{'spend':0,'purch':0,'lp_new':0,'adsets':0}); p=prod[q].get(m,{'orders':0,'new':0,'rev':0,'leagues':0})
        r['q'][q]={'spend':round(a['spend'],2),'purch':a['purch'],'lp_new':a['lp_new'],'adsets':a['adsets'],
                   'orders':p['orders'],'new':p['new'],'rev':round(p['rev'],2),'leagues':p['leagues']}
    rows.append(r)
json.dump({'tot':tot,'rows':rows},open('metro_quarters.json','w'))
print(len(metros),'metros')

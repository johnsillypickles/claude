import json,statistics as st,collections,math
d=json.load(open('metro_quarters.json'));e=json.load(open('expansion.json'))
Q=['q1','q2','q3'];MIN=1500
med={q:st.median([r['q'][q]['spend']/r['q'][q]['purch'] for r in d['rows'] if r['q'][q]['spend']>=MIN and r['q'][q]['purch']>0]) for q in Q}
INTL={'AB','ON','BC','AUS'}
metros=[]
for r in d['rows']:
    m=r['metro']; st_=m.rsplit(',',1)[1].strip()
    qs=[]
    for q in Q:
        x=r['q'][q]; ok=x['spend']>=MIN and x['purch']>0
        qs.append({'spend':round(x['spend']),'purch':x['purch'],'new':x['new'],'orders':x['orders'],'rev':round(x['rev']),
                   'cac':round(x['spend']/x['purch'],2) if x['purch'] else None,'idx':round((x['spend']/x['purch'])/med[q],3) if ok else None,'lp_new':x['lp_new']})
    idx=[q['idx'] for q in qs if q['idx'] is not None]
    S=sum(q['spend'] for q in qs);P=sum(q['purch'] for q in qs);N=sum(q['new'] for q in qs)
    if len(idx)>=2:
        a=st.mean(idx);mx=max(idx)
        tier='consistent' if a<=0.85 and mx<=1.05 else 'efficient' if a<=1.0 else 'average' if a<=1.3 else 'expensive'
    elif len(idx)==1: tier='one_test'; a=idx[0]; mx=idx[0]
    else: tier='no_local'; a=mx=None
    if N==0 and S<100: continue
    xy=e['foot'].get(m)
    metros.append({'metro':m,'intl':st_ in INTL,'lat':xy[0] if xy else None,'lng':xy[1] if xy else None,'q':qs,'tier':tier,
                   'avgIdx':round(a,3) if a is not None else None,'maxIdx':round(mx,3) if mx is not None else None,
                   'spend':S,'purch':P,'cac':round(S/P,2) if P else None,'new':N,'spendPerNew':round(S/N,2) if N else None,'nq':len(idx)})
cands=[c for c in e['cands'] if c['dist_mi']>30]
# aggregate signals by place (no personal data)
agg=collections.defaultdict(lambda:{'location_request':0,'host_applicant':0,'notify_me':0})
for s in e['signals']:
    k=(s['city'],s['st'],round(s['lat'],2),round(s['lng'],2)); agg[k][s['type']]+=1
sig=[{'city':k[0],'st':k[1],'lat':k[2],'lng':k[3],**v} for k,v in agg.items()]
tot={q:{k:round(v) for k,v in d['tot'][q].items()} for q in Q}
U=json.load(open('utm_metro.json'))
net=collections.Counter()
for m,qq in U.items():
    for v in qq.values(): net.update(v)
def shares(c):
    s=sum(c.values()) or 1
    return {'utmOrders':sum(c.values()),'metaShare':round(c['meta']/s,4),'paidShare':round((c['meta']+c['google']+c['tiktok'])/s,4),'noneShare':round(c['none']/s,4),'emailShare':round(c['email']/s,4)}
for mm in metros:
    c=collections.Counter()
    for v in U.get(mm['metro'],{}).values(): c.update(v)
    mm.update(shares(c))
out={'netUtm':shares(net),'medians':{q:round(med[q],2) for q in Q},'tot':tot,'metros':metros,'cands':cands,'signals':sig,'minSpend':MIN}
json.dump(out,open('data.json','w'),separators=(',',':'))
print(len(metros),len(cands),len(sig),collections.Counter(m['tier'] for m in metros))
print(out['medians'])

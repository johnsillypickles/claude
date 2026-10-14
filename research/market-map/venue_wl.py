import json,collections,datetime as dt,statistics as st
O=json.load(open('venue_scored.json'))
for o,f in zip(O,json.load(open('venue_feats2.json'))): o['tommy']=o['t']; o['t']=f['t']
L={l['product']:l for l in json.load(open('leagues.json'))}
W=json.load(open('waitlist_agg.json'))['byLeague']
d=lambda s:dt.date.fromisoformat(s) if s else None
for o in O:
    l=L[o['t']];w=W.get(o['t'],{})
    o['wl_unmet']=w.get('after_sellout',0)+w.get('during_sale',0)+w.get('no_inventory_record',0)
    o['wl_late']=w.get('after_close',0)
    o['demand']=(l['sold']+o['wl_unmet'])/l['cap'] if l['cap'] else None
    fs,so,mz=d(l['first_sale']),d(l['soldout']),d(l['manual_zero'])
    o['days_to_so']=(so-fs).days if so and fs else None
    o['window']=(mz-fs).days if mz and fs else None
O=[o for o in O if o['season']!='Fall 2025' and o['demand'] is not None]
print('leagues',len(O))
so=[o for o in O if o['soldout']]
print('sold out',len(so),' median waitlist per sold-out league',st.median(o['wl_unmet'] for o in so),' median days to sell out',st.median(o['days_to_so'] for o in so if o['days_to_so'] is not None))
D=sorted(o['demand'] for o in O);print('demand/capacity quartiles',[round(D[int(len(D)*q)],2) for q in (.1,.25,.5,.75,.9)])
# waitlist and sold-out agreement
print('sold-out leagues with 0 waitlist',sum(1 for o in so if o['wl_unmet']==0),' with 30+',sum(1 for o in so if o['wl_unmet']>=30))
def rank(xs):
    s=sorted(range(len(xs)),key=lambda i:xs[i]);r=[0]*len(xs)
    i=0
    while i<len(s):
        j=i
        while j+1<len(s) and xs[s[j+1]]==xs[s[i]]: j+=1
        for k in range(i,j+1): r[s[k]]=(i+j)/2
        i=j+1
    return r
def spear(a,b):
    ra,rb=rank(a),rank(b);ma,mb=st.mean(ra),st.mean(rb)
    return sum((x-ma)*(y-mb) for x,y in zip(ra,rb))/((sum((x-ma)**2 for x in ra)*sum((y-mb)**2 for y in rb))**.5)
F=['y25_39','y_per_own','density','y_share','m_trends','kids_per_y','movers','m_transplant','income','own_near','cap','s','tommy']
print(f"\n{'factor':12}{'rho demand':>11}{'rho wl|SO':>10}{'rho speed':>10}   demand/cap median by quintile")
for f in F:
    S=[o for o in O if o.get(f) is not None];S.sort(key=lambda o:o[f])
    q=[S[i*len(S)//5:(i+1)*len(S)//5] for i in range(5)]
    sS=[o for o in S if o['soldout']];sp=[o for o in sS if o['days_to_so'] is not None]
    print(f"{f:12}{spear([o[f] for o in S],[o['demand'] for o in S]):11.2f}{spear([o[f] for o in sS],[o['wl_unmet'] for o in sS]):10.2f}{-spear([o[f] for o in sp],[o['days_to_so'] for o in sp]):10.2f}   "+' '.join(f"{st.median(o['demand'] for o in g):.2f}" for g in q))
json.dump(O,open('venue_wl.json','w'))

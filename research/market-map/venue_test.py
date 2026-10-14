import json,collections,statistics as st
from geo import hav
O=json.load(open('venue_feats.json'))
# our own supply: other leagues same season within 7 mi; capacity
for o in O:
    o['own_near']=sum(1 for p in O if p is not o and p['season']==o['season'] and hav(o['lat'],o['lng'],p['lat'],p['lng'])<=7)
    o['venues_near']=len({p['venue'] for p in O if p['venue']!=o['venue'] and hav(o['lat'],o['lng'],p['lat'],p['lng'])<=10})
    o['y_per_own']=o['y25_39']/(1+o['own_near'])
    o['sunday']=1 if (o['day'] or '').startswith('Sunday') else (0 if o['day'] else None)
def rank(xs):
    s=sorted((v,i) for i,v in enumerate(xs));r=[0]*len(xs)
    for k,(v,i) in enumerate(s): r[i]=k
    return r
def spear(a,b):
    ra,rb=rank(a),rank(b);n=len(a);ma=st.mean(ra);mb=st.mean(rb)
    return sum((x-ma)*(y-mb) for x,y in zip(ra,rb))/((sum((x-ma)**2 for x in ra)*sum((y-mb)**2 for y in rb))**.5)
def auc(score,lab):
    pos=[s for s,l in zip(score,lab) if l];neg=[s for s,l in zip(score,lab) if not l]
    return sum((p>q)+0.5*(p==q) for p in pos for q in neg)/(len(pos)*len(neg))
F=['y25_39','y_core3','y_share','kids_per_y','income','movers','density','m_trends','m_transplant','own_near','venues_near','y_per_own','cap']
base=sum(o['soldout'] for o in O)/len(O)
print(f"n={len(O)} sold out={sum(o['soldout'] for o in O)} ({base:.0%})")
print(f"{'feature':14}{'AUC':>6}{'rho_fill':>9}   sell-out rate by quintile (low -> high)")
for f in F:
    S=[o for o in O if o.get(f) is not None]
    S.sort(key=lambda o:o[f]);q=[S[i*len(S)//5:(i+1)*len(S)//5] for i in range(5)]
    rates=' '.join(f"{sum(o['soldout'] for o in g)/len(g):4.0%}" for g in q)
    cuts=' | '.join(f"{g[0][f]:.3g}-{g[-1][f]:.3g}" for g in q)
    print(f"{f:14}{auc([o[f] for o in S],[o['soldout'] for o in S]):6.2f}{spear([o[f] for o in S],[o['fill'] for o in S]):9.2f}   {rates}    [{cuts}]")
for k in ['chain','sunday','src']:
    g=collections.defaultdict(list)
    for o in O: g[o[k]].append(o['soldout'])
    print(k,{a:(len(b),f"{sum(b)/len(b):.0%}") for a,b in g.items()})
json.dump(O,open('venue_feats2.json','w'))

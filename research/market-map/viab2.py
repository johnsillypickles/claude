import json,statistics as st,io,contextlib,math,collections
with contextlib.redirect_stdout(io.StringIO()):
    from venue_wl import spear
D=[d for d in json.load(open('viab.json')) if d['spots']]
for d in D:
    d['fill']=d['players']/d['spots'];d['y_per']=d['y25_39']/(1+d['own_near']);d['nkids']=-(d['kids_per_y'] or 0);d['barv']={'Yes':1,'No':0}.get(d['bar'],.5)
    hrs=(d['hours'] or 0)
    d['pph']=d['spots']/d['court_hours'] if d['court_hours'] else None   # player spots per weekly court-hour
    w=d['weeks'] or 8
    d['court_spend']=d['cost']*d['court_hours']*w if d['cost'] and d['court_hours'] else None
    d['rev']=d['players']*d['price'] if d['price'] else None
    d['margin']=1-d['court_spend']/d['rev'] if d['court_spend'] and d['rev'] else None
    d['price_hr']=d['price']/w if d['price'] else None   # assumes 1 hr of play per week
F=sorted(D,key=lambda d:d['fill']);print('fill pctiles 10/25/50/75/90:',[round(F[int(len(F)*q)]['fill'],2) for q in (.1,.25,.5,.75,.9)],' n',len(D))
print('healthy = fill>=0.8:',f"{sum(d['fill']>=.8 for d in D)}/{len(D)}", ' season1:',f"{sum(d['fill']>=.8 for d in D if d['sn']==1)}/{sum(1 for d in D if d['sn']==1)}")
print(f"\n{'factor':11}{'all':>7}{'s1':>7}{'s2+':>7}   rank corr with FILL;   healthy (fill>=.8) rate low->high quintile, all leagues")
for f in ['y_per','y25_39','density','y_share','trends','movers','nkids','barv','own_near','fac_courts','spots','price']:
    out=[]
    for g in (D,[d for d in D if d['sn']==1],[d for d in D if d['sn']>=2]):
        g=[d for d in g if d.get(f) is not None];out.append(spear([d[f] for d in g],[d['fill'] for d in g]))
    g=sorted([d for d in D if d.get(f) is not None],key=lambda d:d[f]);q=[g[i*len(g)//5:(i+1)*len(g)//5] for i in range(5)]
    print(f"{f:11}"+''.join(f"{x:7.2f}" for x in out)+'   '+' '.join(f"{sum(d['fill']>=.8 for d in b)/len(b):4.0%}" for b in q))
E=[d for d in D if d['margin'] is not None]
print('\nECONOMICS n',len(E))
for k,fmtx in [('cost','${:.0f}'),('pph','{:.1f}'),('price','${:.0f}'),('price_hr','${:.1f}'),('margin','{:.0%}')]:
    v=sorted(d[k] for d in E if d[k] is not None);print(f"  {k:9} p10 {fmtx.format(v[len(v)//10])}  median {fmtx.format(v[len(v)//2])}  p90 {fmtx.format(v[9*len(v)//10])}")
print('  weeks dist',collections.Counter(d['weeks'] for d in E).most_common(4),' play hrs/wk dist',collections.Counter(d['hours'] for d in E).most_common(4))
# price elasticity: price relative to metro-season median vs fill
g=collections.defaultdict(list)
for d in E: g[d['season']].append(d['price'])
import re
for d in E: d['prel']=d['price']/st.median(g[d['season']])
for a,b in [(0,.92),(.92,.98),(.98,1.02),(1.02,1.08),(1.08,9)]:
    L=[d for d in E if a<=d['prel']<b]
    if L: print(f"  price vs season median {a:.2f}-{b:.2f}: n={len(L)} median fill {st.median(d['fill'] for d in L):.2f}, healthy {sum(d['fill']>=.8 for d in L)/len(L):.0%}")
print('  rho cost vs price',round(spear([d['cost'] for d in E],[d['price'] for d in E]),2))
json.dump(D,open('viab2.json','w'))

import json,collections,statistics as st,math,re
O=json.load(open('venue_wl.json'))
from venue_wl import spear
order=['Winter 2026','Spring 2026','Summer 2026','Fall 2026']
lg=lambda x:math.log(x+0.1)
# 1) same venue, consecutive seasons
by=collections.defaultdict(dict)
for o in O:
    if o['season'] in order: by[(o['metro'],o['venue'])].setdefault(o['season'],[]).append(o)
a=[];b=[];sa=[];sb=[]
for v,S in by.items():
    for s1,s2 in zip(order,order[1:]):
        if s1 in S and s2 in S:
            a.append(st.mean(o['demand'] for o in S[s1]));b.append(st.mean(o['demand'] for o in S[s2]))
            sa.append(max(o['soldout'] for o in S[s1]));sb.append(max(o['soldout'] for o in S[s2]))
print('same venue next season: pairs',len(a),' rho demand',round(spear(a,b),2),
      ' P(sold out next | sold out now)',f"{sum(1 for x,y in zip(sa,sb) if x and y)/max(1,sum(sa)):.0%}",
      ' P(sold out next | not now)',f"{sum(1 for x,y in zip(sa,sb) if y and not x)/max(1,len(sa)-sum(sa)):.0%}")
# 2) variance split: metro vs venue vs league (log demand)
y=[lg(o['demand']) for o in O];gm=st.mean(y);tot=sum((v-gm)**2 for v in y)
def explained(key):
    g=collections.defaultdict(list)
    for o,v in zip(O,y): g[key(o)].append(v)
    return 1-sum(sum((v-st.mean(L))**2 for v in L) for L in g.values())/tot
print(f"share of demand variation explained by: season {explained(lambda o:o['season']):.0%}, metro {explained(lambda o:o['metro']):.0%}, venue {explained(lambda o:(o['metro'],o['venue'])):.0%}")
# 3) out-of-sample: fit weights on Winter-Summer, test on Fall 2026 (rank correlation with demand)
import random
F=['p_y_per_own','p_density','p_m_trends','p_kids_per_y','p_movers','p_y_share','p_y25_39']
tr=[o for o in O if o['season'] in order[:3]];te=[o for o in O if o['season']=='Fall 2026']
best=None;random.seed(1)
for _ in range(4000):
    w=[random.random()**2 for _ in F];s=sum(w);w=[x/s for x in w]
    r=spear([sum(o[f]*x for f,x in zip(F,w)) for o in tr],[o['demand'] for o in tr])
    if not best or r>best[0]: best=(r,w)
ev=lambda w,L:spear([sum(o[f]*x for f,x in zip(F,w)) for o in L],[o['demand'] for o in L])
print('fitted weights',{f[2:]:round(x,2) for f,x in zip(F,best[1])},f"train rho {best[0]:.2f}")
for name,w in [('fitted',best[1]),('proposed',[.35,.2,.2,.15,.1,0,0]),('tommy',[0,0,.2,0,.2,0,.6])]:
    print(f"  Fall 2026 holdout rho, {name}: {ev(w,te):.2f}  (n={len(te)})")
# 4) start hour (only leagues with parsed description)
def hr(t):
    m=re.match(r'\s*(\d{1,2})(?::\d\d)?\s*(am|pm)?',t or '');
    if not m: return None
    h=int(m.group(1));return h+12 if h<12 and (m.group(2)=='pm' or (not m.group(2) and h<=10)) else h
g=collections.defaultdict(list)
for o in O:
    h=hr(o.get('time'))
    if h: g['before 5pm' if h<17 else '5-7pm start' if h<19 else '7pm+ start'].append(o)
for k,L in g.items(): print(k,len(L),f"sold out {sum(o['soldout'] for o in L)/len(L):.0%} median demand {st.median(o['demand'] for o in L):.2f}")

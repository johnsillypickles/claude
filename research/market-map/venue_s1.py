import json,collections,statistics as st,io,contextlib
with contextlib.redirect_stdout(io.StringIO()):
    from venue_wl import spear
O=json.load(open('venue_wl.json'))
order=['Fall 2025','Winter 2026','Spring 2026','Summer 2026','Fall 2026']
first={}
for o in O+[{'season':'Fall 2025','metro':l['metro'],'venue':__import__('re').search(r' at (.+?) \|',l['product']).group(1).strip().lower() if ' at ' in l['product'] else ''} for l in json.load(open('leagues.json')) if l['season']=='Fall 2025']:
    if o['season'] in order:
        k=(o['metro'],o['venue']);first[k]=min(first.get(k,9),order.index(o['season']))
S=[o for o in O if o['season'] in order[2:]]
for o in S: o['s1']=first[(o['metro'],o['venue'])]==order.index(o['season'])
for o in S:
    # metro new too?
    pass
chk=['englewood','wayne','eagan','west meade','little creek']
print('check known first-ever Spring leagues:',[(o['venue'],o['s1']) for o in S if o['season']=='Spring 2026' and any(c in o['t'].lower() for c in chk)])
for lab,g in [('season 1',[o for o in S if o['s1']]),('season 2+',[o for o in S if not o['s1']])]:
    so=[o for o in g if o['soldout']]
    print(f"{lab:10} n={len(g):3} sold out {len(so)/len(g):.0%}  median demand/cap {st.median(o['demand'] for o in g):.2f}  median waitlist if sold out {st.median([o['wl_unmet'] for o in so] or [0])}")
print('\nrank correlation with demand, season 1 vs 2+')
for f in ['s','tommy','y_per_own','y25_39','density','y_share','m_trends','kids_per_y','movers','own_near']:
    r=[]
    for g in ([o for o in S if o['s1']],[o for o in S if not o['s1']]):
        g=[o for o in g if o.get(f) is not None];r.append(spear([o[f] for o in g],[o['demand'] for o in g]))
    print(f"  {f:11} s1 {r[0]:5.2f}   s2+ {r[1]:5.2f}")
# venues: did season 1 result predict season 2?
by=collections.defaultdict(dict)
for o in O: by[(o['metro'],o['venue'])].setdefault(o['season'],[]).append(o)
p=[]
for k,d in by.items():
    i=first.get(k)
    if i is not None and i>=2 and i+1<len(order) and order[i] in d and order[i+1] in d:
        p.append((max(o['soldout'] for o in d[order[i]]),max(o['soldout'] for o in d[order[i+1]])))
print('\nnew venues with a 2nd season:',len(p),' sold out s1->s2:',collections.Counter(p))

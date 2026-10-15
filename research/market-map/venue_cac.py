import json,re,collections,statistics as st,csv
R=json.load(open('new_cust_raw.json'));print(R['columns'][:4] if False else [c['name'] for c in R['columns']],R['rowCount'])
norm=lambda s:re.sub(r'[^a-z0-9]','',(s or '').lower())
NC={norm(r[0]):(int(r[1]),int(r[2])) for r in R['rows']}
D=json.load(open('viab4.json'))
vn=lambda t:re.sub(r'\s*\((Sundays|Mondays|Tuesdays|Wednesdays|Thursdays|Fridays|Saturdays|Indoor|Outdoor)[^)]*\)','',t.split(' at ',1)[-1].split(' |')[0]).strip()
miss=0
for d in D:
    n=NC.get(norm(d['name']))
    if n is None: miss+=1
    d['new']=n[0] if n else None
print('leagues',len(D),'no new-customer match',miss)
L=[d for d in D if d['new']]
for d in L: d['new_paid']=max(1,d['new']-d['free'])
g=collections.defaultdict(list)
for d in L:
    if 'Carmin' in d['name']: continue
    g[(vn(d['name']),re.match(r'([^:]+):',d['name']).group(1).strip())].append(d)
rows=[]
for (v,city),G in g.items():
    sp=sum(d['p1'] for d in G);nw=sum(d['new_paid'] for d in G);pl=sum(d['players'] for d in G)
    rows.append(dict(venue=v,city=city,leagues=len(G),leagues_with_p1=sum(d['p1']>0 for d in G),phase1_spend=round(sp),new_players=nw,players=int(pl),
      new_share=round(nw/pl,2) if pl else None,p1_per_new=round(sp/nw,2) if nw else None,median_fill=round(st.median(d['fill'] for d in G),2),score=round(st.mean(d['vs'] for d in G))))
rows.sort(key=lambda r:-(r['p1_per_new'] or 0))
with open('venue_cac.csv','w') as f:
    w=csv.DictWriter(f,rows[0].keys());w.writeheader();w.writerows(rows)
P=[r for r in rows if r['phase1_spend']>0]
print('venues',len(rows),'with P1',len(P),' total P1',sum(r['phase1_spend'] for r in rows),' new players at those venues',sum(r['new_players'] for r in P))
print('network P1 $ per new player at venues that ran it:',round(sum(r['phase1_spend'] for r in P)/sum(r['new_players'] for r in P),2),' median venue',st.median(r['p1_per_new'] for r in P))
print('\nHIGHEST');[print(f"  ${r['p1_per_new']:6.0f}/new  ${r['phase1_spend']:6,} spend  {r['new_players']:3} new  fill {r['median_fill']:.2f} score {r['score']:2}  {r['venue']} ({r['city']})") for r in P[:10]]
print('LOWEST (with $1k+ spend)');[print(f"  ${r['p1_per_new']:6.0f}/new  ${r['phase1_spend']:6,} spend  {r['new_players']:3} new  fill {r['median_fill']:.2f} score {r['score']:2}  {r['venue']} ({r['city']})") for r in sorted([r for r in P if r['phase1_spend']>=1000],key=lambda r:r['p1_per_new'])[:8]]
for a,b in [(0,35),(35,55),(55,65),(65,101)]:
    G=[d for d in L if a<=d['vs']<b]
    print(f"score {a}-{b}: P1 $ per new player (all leagues) {sum(d['p1'] for d in G)/sum(d['new_paid'] for d in G):.2f}  new-player share {sum(d['new_paid'] for d in G)/sum(d['players'] for d in G):.0%}")
json.dump(L,open('viab5.json','w'))

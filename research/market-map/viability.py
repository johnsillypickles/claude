import json,re,collections,statistics as st,io,contextlib
with contextlib.redirect_stdout(io.StringIO()):
    import venue_features as vf
    import score_site as S
from geo import hav
T=json.load(open('tracker.json'));FI={f['fid']:f for f in json.load(open('facility_info.json'))}
L={l['product'].strip():l for l in json.load(open('leagues.json'))}
WL=json.load(open('waitlist_agg.json'))['byLeague']
ORD=['Fall 2025','Winter 2026','Spring 2026','Summer 2026','Fall 2026']
done=set(ORD[1:])
L={l['product'].strip():l for l in json.load(open('leagues.json'))}
R=[r for r in T if r['season'] in done and 'Pickleball' in r['name'] and not re.search(r'Canada|Australia|AUS|, ON|, BC|, AB',r['name'])]
# dedupe by name
# dedupe: when a name appears twice, keep the row whose spots best match Shopify units sold (two tracker rows are mislabeled copies)
seen={}
for r in R:
    k=r['name'].strip();sold=(L.get(k) or {}).get('sold')
    fit=lambda x:abs((x.get('spots') or 0)-(sold or 0)) if sold else 0
    if k not in seen or fit(r)<fit(seen[k]): seen[k]=r
R=list(seen.values())
# season number per facility
first={}
for f in FI.values():
    if f.get('Fall 2025|pid','').strip() not in ('','No League','-'): first[f['fid']]=0
for r in T:
    if r['season'] in ORD: first[r['fid']]=min(first.get(r['fid'],9),ORD.index(r['season']))
for r in T:
    if r['tab']=='spring' and r.get('season_n'): first[r['fid']]=min(first.get(r['fid'],9),2-int(r['season_n'])+1)
zc={}
def F(z):
    if z not in zc:
        lat,lng,_=vf.ZXY[z];zc[z]=(lat,lng,vf.feat(lat,lng))
    return zc[z]
D=[]
for r in R:
    nm=r['name'].strip();l=L.get(nm)
    players=l['sold'] if l else (r['signed'] if r['signed'] is not None else (0 if r['status']=='League Cancelled' else None))
    if players is None: continue
    z=(r.get('zip') or FI.get(r['fid'],{}).get('zip') or '').strip()[:5]
    if z not in vf.ZXY: continue
    lat,lng,f=F(z)
    D.append(dict(name=nm,fid=r['fid'],season=r['season'],players=players,spots=r['spots'],cancel=r['status']=='League Cancelled',
        sn=ORD.index(r['season'])-first.get(r['fid'],ORD.index(r['season']))+1,lat=lat,lng=lng,zip=z,**f,
        bar=FI.get(r['fid'],{}).get('bar'),fac_courts=r.get('fac_courts') or (float(FI[r['fid']]['courts']) if FI.get(r['fid'],{}).get('courts','').isdigit() else None),
        cost=r['cost'],price=r['price'],courts=r['courts'],court_hours=r['court_hours'],weeks=r.get('weeks'),hours=r.get('hours'),
        wl=WL.get(nm,{}).get('after_sellout',0),soldout=bool(l and l['soldout'])))
for d in D:
    d['own_near']=sum(1 for e in D if e is not d and e['season']==d['season'] and hav(d['lat'],d['lng'],e['lat'],e['lng'])<=7)
    d['trends']=S.nearest_trends(d['lat'],d['lng'])[1]
    d['hit30']=d['players']>=30
json.dump(D,open('viab.json','w'))
print('leagues',len(D),' from Shopify',sum(1 for d in D if d['name'] in L),' tracker-only',sum(1 for d in D if d['name'] not in L),' cancelled',sum(d['cancel'] for d in D))
for lab,g in [('all',D),('season 1',[d for d in D if d['sn']==1]),('season 2',[d for d in D if d['sn']==2]),('season 3+',[d for d in D if d['sn']>=3])]:
    print(f"{lab:9} n={len(g):3}  hit 30+: {sum(d['hit30'] for d in g)}/{len(g)} = {sum(d['hit30'] for d in g)/len(g):.0%}   median players {st.median(d['players'] for d in g)}")

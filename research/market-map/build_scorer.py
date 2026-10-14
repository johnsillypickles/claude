import json,sqlite3,io,contextlib
with contextlib.redirect_stdout(io.StringIO()):
    import score_site as S
    import venue_features as vf
db=sqlite3.connect('zip.sqlite')
names={r[0]:(r[1],r[2]) for r in db.execute("select zipcode,major_city,state from simple_zipcode")}
A,M=vf.A,vf.M
n=vf.n
Z=[]
for z,a in A.items():
    if z not in vf.ZXY: continue
    lat,lng,area=vf.ZXY[z];m=M.get(z,{})
    pop=n(a['B01003_001E']) or 0
    y=sum(n(a[k]) or 0 for k in ['B01001_011E','B01001_012E','B01001_013E','B01001_035E','B01001_036E','B01001_037E'])
    kids=(n(a['B01001_003E']) or 0)+(n(a['B01001_027E']) or 0)
    mv=sum(n(m.get(k)) or 0 for k in ['B07001_070E','B07001_071E','B07001_072E','B07001_086E','B07001_087E','B07001_088E'])
    y2=sum(n(m.get(k)) or 0 for k in ['B07001_006E','B07001_007E','B07001_008E'])
    c,s=names.get(z,('',''))
    Z.append([z,lat,lng,round(area,2),int(pop),int(y),int(kids),int(mv),int(y2),c or '',s or ''])
D=json.load(open('data_v4.json'))
T=[[m['lat'],m['lng'],m['trends'],m['metro']] for m in D['metros'] if m.get('trends') is not None and m['lat']]+[[c['lat'],c['lng'],c['trends'],c['name']] for c in D['cands'] if c.get('trends') is not None and c['lat']]
ref=S.ref
R={k:sorted(o['c'][k] for o in ref if o['c'][k] is not None) for k in S.W}
pts=[[round(o['score'],1),o['soldout']] for o in ref]
own=[[o['lat'],o['lng'],o['venue'].title(),o['metro']] for o in ref if o['season']=='Fall 2026']
# all Fall 2026 leagues (incl. unmatched to facility sheet) for the nearby count, same as score_site
out=dict(W=S.W,zips=Z,trends=T,ref=R,pts=pts,own=own,n=len(ref))
s=json.dumps(out,separators=(',',':'));open('scorer_data.json','w').write(s)
print(len(Z),'zips',len(T),'trend pts',len(own),'fall leagues',len(pts),'ref; size',len(s)//1024,'KB')

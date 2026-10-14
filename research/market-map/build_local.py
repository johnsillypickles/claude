import json,re,collections,statistics as st,sqlite3,io,contextlib
with contextlib.redirect_stdout(io.StringIO()):
    import venue_features as vf
from geo import hav
F=json.load(open('facility.json'));M=[m for m in F['metros'] if not m.get('intl') and m.get('lat')]
def metro_of(lat,lng,maxd=60):
    b=min(M,key=lambda m:hav(lat,lng,m['lat'],m['lng']));return b['metro'] if hav(lat,lng,b['lat'],b['lng'])<=maxd else None
# venues
D=json.load(open('viab4.json'))
vn=lambda t:re.sub(r'\s*\((Sundays|Mondays|Tuesdays|Wednesdays|Thursdays|Fridays|Saturdays|Indoor|Outdoor)[^)]*\)','',t.split(' at ',1)[-1].split(' |')[0]).strip()
g=collections.defaultdict(list)
for d in D:
    if 'Carmin' in d['name']: continue
    g[(vn(d['name']),d['zip'])].append(d)
V=[];seen=collections.Counter()
for (name,z),L in g.items():
    lat,lng=L[0]['lat'],L[0]['lng'];k=(round(lat,3),round(lng,3));j=seen[k];seen[k]+=1
    lat+=0.006*j;lng+=0.008*j
    city=re.match(r'([^:]+):',L[0]['name']).group(1).strip()
    V.append(dict(name=name,city=city,zip=z,lat=round(lat,4),lng=round(lng,4),metro=metro_of(lat,lng),leagues=len(L),players=int(sum(d['players'] for d in L)),
      spots=int(sum(d['spots'] for d in L)),fill=round(st.median(d['fill'] for d in L),3),wl=int(sum(d['wl'] for d in L)),so=sum(1 for d in L if d['soldout']),
      seasons=sorted({d['season'] for d in L}),score=round(L[0]['vs'])))
# customer zips
C=json.load(open('cust_zip.json'));db=sqlite3.connect('zip.sqlite');nm={r[0]:r[1] for r in db.execute('select zipcode,major_city from simple_zipcode')}
Z=[]
for z,n in C.items():
    if n<3: continue
    lat,lng,_=vf.ZXY[z];m=metro_of(lat,lng,45)
    if not m: continue
    a=vf.A.get(z,{});y=sum(vf.n(a.get(k)) or 0 for k in ['B01001_011E','B01001_012E','B01001_013E','B01001_035E','B01001_036E','B01001_037E'])
    Z.append(dict(zip=z,city=nm.get(z,''),lat=round(lat,4),lng=round(lng,4),metro=m,n=n,per1k=round(1000*n/y,1) if y>=200 else None))
F['venues']=V;F['zips']=Z
json.dump(F,open('facility2.json','w'),separators=(',',':'))
print('venues',len(V),'with metro',sum(1 for v in V if v['metro']),' zips',len(Z),'players covered',sum(z['n'] for z in Z),'size KB',len(json.dumps(F))//1024)
for v in sorted([v for v in V if v['metro']=='Chicago, IL'],key=lambda v:-v['fill']): print('  ',v['name'],v['city'],v['fill'],v['players'],v['wl'])
cz=sorted([z for z in Z if z['metro']=='Chicago, IL'],key=lambda z:-z['n'])[:8];print([(z['zip'],z['city'],z['n'],z['per1k']) for z in cz])
hp=[z for z in Z if z['zip'] in ('60035','60657','60614','60035','60093','60091')];print(hp)

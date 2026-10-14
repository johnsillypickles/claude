import json,re,sqlite3,math,collections,statistics as st
from geo import hav,city_xy
R=7.0  # miles, stand-in for a 15 minute drive
db=sqlite3.connect('zip.sqlite')
ZXY={r[0]:(r[1],r[2],r[3] or 0) for r in db.execute("select zipcode,lat,lng,land_area_in_sqmi from simple_zipcode where lat is not null")}
def load(fn):
    d=json.load(open(fn));h=d[0];return {r[-1]:dict(zip(h,r)) for r in d[1:]}
A=load('zcta_a.json');M=load('zcta_m.json')
def n(x):
    try: v=float(x); return v if v>=0 else None
    except: return None
Z=[]
for z,a in A.items():
    if z not in ZXY: continue
    lat,lng,area=ZXY[z]; m=M.get(z,{})
    pop=n(a['B01003_001E']) or 0
    y=sum(n(a[k]) or 0 for k in ['B01001_011E','B01001_012E','B01001_013E','B01001_035E','B01001_036E','B01001_037E'])
    kids=(n(a['B01001_003E']) or 0)+(n(a['B01001_027E']) or 0)
    mv=sum(n(m.get(k)) or 0 for k in ['B07001_070E','B07001_071E','B07001_072E','B07001_086E','B07001_087E','B07001_088E'])
    y2=sum(n(m.get(k)) or 0 for k in ['B07001_006E','B07001_007E','B07001_008E'])
    Z.append((lat,lng,area,pop,y,kids,n(a['B19013_001E']),mv,y2))
# venue -> zip from parsed descriptions (any season)
V=[json.loads(l) for l in open('venues.jsonl')]
def venue(t):
    m=re.search(r' at (.+?) \|',t); return m.group(1).strip().lower() if m else ''
vz={};meta={}
for v in V:
    if v['zip'] and v['zip'] in ZXY: vz.setdefault(venue(v['title']),v['zip'])
    meta[v['title']]=v
# metro-level
D=json.load(open('data_v4.json'))
MT={m['metro']:m for m in D['metros']}
L=json.load(open('leagues.json'))
WL=json.load(open('waitlist_agg.json'))['byLeague']
def feat(lat,lng):
    s=dict(pop=0,y=0,kids=0,inc_w=0,inc_p=0,mv=0,y2=0,area=0,core=0)
    for (a,b,ar,pop,y,k,inc,mv,y2) in Z:
        if abs(a-lat)>0.12 or abs(b-lng)>0.16: continue
        d=hav(lat,lng,a,b)
        if d>R: continue
        s['pop']+=pop;s['y']+=y;s['kids']+=k;s['mv']+=mv;s['y2']+=y2;s['area']+=ar
        if d<=3: s['core']+=y
        if inc and pop: s['inc_w']+=inc*pop;s['inc_p']+=pop
    return dict(y25_39=s['y'],y_share=s['y']/s['pop'] if s['pop'] else None,
        kids_per_y=s['kids']/s['y'] if s['y'] else None,income=s['inc_w']/s['inc_p'] if s['inc_p'] else None,
        movers=s['mv']/s['y2'] if s['y2'] else None,density=s['pop']/s['area'] if s['area'] else None,y_core3=s['core'])
out=[];miss=collections.Counter()
for l in L:
    t=l['product'];vn=venue(t);z=vz.get(vn)
    if z: lat,lng,_=ZXY[z];src='zip'
    else:
        m=re.match(r'([^,:]+),\s*([A-Z]{2}):',t);xy=city_xy(m.group(1),m.group(2)) if m else None
        if not xy: miss[t.split(':')[0]]+=1;continue
        lat,lng=xy;src='city'
    f=feat(lat,lng);mm=MT.get(l['metro'],{})
    c=mm.get('census') or {}
    w=WL.get(t,{})
    ve=meta.get(t,{})
    desc_outdoor=None
    out.append(dict(t=t,metro=l['metro'],season=l['season'],venue=vn,src=src,lat=lat,lng=lng,sold=l['sold'],cap=l['cap'],
        soldout=1 if l['soldout'] else 0,fill=min(1,l['sold']/l['cap']) if l['cap'] else None,wl=w.get('after_sellout',0),
        chain='chicken n pickle' in vn,day=ve.get('vendor'),time=ve.get('time'),
        m_trends=mm.get('trends'),m_transplant=(c.get('transplant') if isinstance(c,dict) else None),m_wlPer=mm.get('wlPer'),**f))
json.dump(out,open('venue_feats.json','w'))
print(len(out),'located;',collections.Counter(o['src'] for o in out),'missing',sum(miss.values()),miss.most_common(8))
print(json.dumps(out[0])[:600])

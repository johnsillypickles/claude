import json,sqlite3,math,re,collections
db=sqlite3.connect('zip.sqlite')
Z={r[0]:r[1:] for r in db.execute("select zipcode,major_city,state,lat,lng,population,median_household_income,common_city_list from simple_zipcode where lat is not null")}
def hav(a,b,c,d):
    R=3958.8;p1,p2=math.radians(a),math.radians(c);dp=p2-p1;dl=math.radians(d-b)
    return 2*R*math.asin(math.sqrt(math.sin(dp/2)**2+math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2))
def city_xy(city,st):
    city={'St. Louis':'Saint Louis','Port St. Lucie':'Port Saint Lucie','St. Petersburg':'Saint Petersburg','St Petersburg':'Saint Petersburg'}.get(city,city)
    pts=[(v[2],v[3],v[4] or 0) for v in Z.values() if v[1]==st and (v[0] or '').lower()==city.lower()]
    if not pts: return None
    w=sum(p[2] for p in pts) or len(pts)
    return (sum(p[0]*(p[2] or 1) for p in pts)/ (w if w else 1), sum(p[1]*(p[2] or 1) for p in pts)/(w if w else 1))
ALIAS={'Dallas-Fort Worth':'Dallas','Bridgeport-Stamford':'Stamford','Washington':'Washington'}
d=json.load(open('metro_quarters.json'))
foot={}
for r in d['rows']:
    m=r['metro']; city,st=[x.strip() for x in m.rsplit(',',1)]
    if st in('AB','ON','BC','AUS'): continue
    xy=city_xy(ALIAS.get(city,city),st)
    if not xy: print('NO XY',m); continue
    foot[m]=xy
cands=[l.strip().rsplit(',',1) for l in open('candidates.txt') if l.strip()]
# demand signals
reqs=json.load(open('form_requests.json'))
sig=[]
for o in reqs:
    z=(o.get('$zip') or '').strip()[:5]
    if o['form'] in('location_request','host_applicant') and z in Z:
        v=Z[z]; sig.append({'type':o['form'],'lat':v[2],'lng':v[3],'city':v[0],'st':v[1]})
    elif o['form']=='coming_soon':
        m=re.search(r'/products/([a-z\-\.]+?)-([a-z]{2})-pickleball',o.get('page') or '')
        if m:
            city=m.group(1).replace('-',' ').title(); st=m.group(2).upper()
            xy=city_xy(city.replace('St ','St. ') if city.startswith('St ') else city,st) or city_xy(city,st)
            if xy: sig.append({'type':'notify_me','lat':xy[0],'lng':xy[1],'city':city,'st':st})
print('signals',collections.Counter(s['type'] for s in sig))
RAD=30
for x in sig: x['out']=min(hav(x['lat'],x['lng'],*v) for v in foot.values())>30
out=[];seen=[]
for city,st in cands:
    xy=city_xy(city,st)
    if not xy: print('no xy',city,st); continue
    near=min(((hav(*xy,*v),m) for m,v in foot.items()),default=(999,None))
    pop=0;inc_w=0;inc_p=0
    for v in Z.values():
        if v[4] and hav(*xy,v[2],v[3])<=RAD:
            pop+=v[4]
            if v[5]: inc_w+=v[5]*v[4]; inc_p+=v[4]
    s=collections.Counter(x['type'] for x in sig if x['out'] and hav(*xy,x['lat'],x['lng'])<=RAD+5)
    out.append({'city':city,'st':st,'lat':round(xy[0],3),'lng':round(xy[1],3),'nearest_footprint':near[1],'dist_mi':round(near[0]),
                'pop30':pop,'income':round(inc_w/inc_p) if inc_p else None,
                'req':s['location_request'],'host':s['host_applicant'],'notify':s['notify_me']})
# dedupe candidates whose centers are within 25mi of a larger candidate
out.sort(key=lambda o:-o['pop30'])
keep=[]
for o in out:
    if any(hav(o['lat'],o['lng'],k['lat'],k['lng'])<25 for k in keep): continue
    keep.append(o)
json.dump({'cands':keep,'foot':{k:list(v) for k,v in foot.items()},'signals':sig},open('expansion.json','w'))
new=[o for o in keep if o['dist_mi']>30]
print(len(keep),'cands',len(new),'outside footprint')
for o in new[:70]: print(f"{o['city']:20}{o['st']} pop30={o['pop30']:>9,} inc={o['income']} req={o['req']} host={o['host']} notify={o['notify']} near={o['nearest_footprint']} {o['dist_mi']}mi")
# unmatched signals (outside 35mi of any footprint)
print('\nSignals outside footprint:')
c=collections.Counter()
for x in sig:
    dm=min(hav(x['lat'],x['lng'],*v) for v in foot.values())
    if dm>35: c[(x['city'],x['st'],x['type'])]+=1
for k,v in c.most_common(): print(v,k)

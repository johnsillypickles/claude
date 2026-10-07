import sqlite3,math
db=sqlite3.connect('zip.sqlite')
Z={r[0]:r[1:] for r in db.execute("select zipcode,major_city,state,lat,lng,population from simple_zipcode where lat is not null")}
BY=collections=None
import collections as _c
_idx=_c.defaultdict(list)
for v in Z.values(): _idx[((v[0] or '').lower(),v[1])].append((v[2],v[3],v[4] or 0))
def hav(a,b,c,d):
    R=3958.8;p1,p2=math.radians(a),math.radians(c);dp=p2-p1;dl=math.radians(d-b)
    return 2*R*math.asin(math.sqrt(math.sin(dp/2)**2+math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2))
AL={'st. louis':'saint louis','port st. lucie':'port saint lucie','st. petersburg':'saint petersburg','st. paul':'saint paul','st. cloud':'saint cloud','st. george':'saint george','st. joseph':'saint joseph','ft. myers':'fort myers','ft. wayne':'fort wayne','ft. smith':'fort smith','ft. pierce':'fort pierce','ft. worth':'fort worth','urban honolulu':'honolulu','boise city':'boise','ashville':'asheville'}
def city_xy(city,st):
    c=city.lower().strip(); c=AL.get(c,c)
    for cand in (c, c.replace(' city','') if c.endswith(' city') else None, c.split('/')[0]):
        if not cand: continue
        pts=_idx.get((cand,st))
        if pts:
            w=sum(p[2] for p in pts) or 1
            return (sum(p[0]*(p[2] or 1) for p in pts)/w, sum(p[1]*(p[2] or 1) for p in pts)/w)
    return None

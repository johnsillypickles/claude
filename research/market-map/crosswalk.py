import json,os,urllib.request,urllib.parse,csv,concurrent.futures as cf,time
K=os.environ['CENSUS_API_KEY']
B='https://api.census.gov/data/2024/acs/acs5'
def get(params):
    u=B+'?'+urllib.parse.urlencode(params,safe=':*,()')+'&key='+K
    for i in range(4):
        try: return json.load(urllib.request.urlopen(u,timeout=60))
        except Exception as e:
            if i==3: raise
            time.sleep(2**i)
want={r['cbsa_code'] for r in csv.DictReader(open('census_cbsa.csv'))}
states=[r[1] for r in get({'get':'NAME','for':'state:*'})[1:]]
G='metropolitan statistical area/micropolitan statistical area (or part)'
parts=[]
def st_parts(s):
    rows=get({'get':'NAME','for':G+':*','in':'state:'+s})
    return [(s,r[2]) for r in rows[1:] if r[2] in want]
with cf.ThreadPoolExecutor(8) as ex:
    for p in ex.map(st_parts,states): parts+=p
print('state-metro parts',len(parts))
def counties(p):
    s,c=p
    rows=get({'get':'NAME','for':'county:*','in':['state:'+s,G+':'+c]}) if False else None
    u=B+'?get=NAME&for=county:*&in=state:'+s+'&in='+urllib.parse.quote(G)+':'+c+'&key='+K
    for i in range(4):
        try: rows=json.load(urllib.request.urlopen(u,timeout=60)); break
        except Exception:
            if i==3: raise
            time.sleep(2**i)
    return [(c,s+r[3]) for r in rows[1:]]
xw={}
with cf.ThreadPoolExecutor(8) as ex:
    for res in ex.map(counties,parts):
        for c,fips in res: xw.setdefault(c,[]).append(fips)
json.dump(xw,open('cbsa_counties.json','w'))
print('metros mapped',len(xw),'of',len(want),'counties',sum(len(v) for v in xw.values()))
print('Wilmington NC',xw.get('48900'))

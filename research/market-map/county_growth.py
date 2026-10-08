import json,os,urllib.request,csv,collections
K=os.environ['CENSUS_API_KEY']
AGE=['B01001_0%02dE'%i for i in (11,12,13,14,35,36,37,38)]
def pull(yr,extra=[]):
    vs=['B01003_001E']+AGE+extra
    u=f'https://api.census.gov/data/{yr}/acs/acs5?get={",".join(vs)}&for=county:*&in=state:*&key={K}'
    rows=json.load(urllib.request.urlopen(u,timeout=180)); h=rows[0]; out={}
    for r in rows[1:]:
        d=dict(zip(h,r)); f=d['state']+d['county']
        v=lambda k: max(0,int(d[k] or 0))
        out[f]={'pop':v('B01003_001E'),'y':sum(v(k) for k in AGE),**{k:v(k) for k in extra}}
    return out
# verify age cell labels in both vintages
for yr in (2019,2024):
    V=json.load(urllib.request.urlopen(f'https://api.census.gov/data/{yr}/acs/acs5/groups/B01001.json?key={K}',timeout=60))['variables']
    print(yr,[V[k]['label'].split('!!')[-1] for k in AGE])
    V2=json.load(urllib.request.urlopen(f'https://api.census.gov/data/{yr}/acs/acs5/groups/B23025.json?key={K}',timeout=60))['variables']
    print(yr,V2['B23025_001E']['label'],'|',V2['B23025_006E']['label'])
c24=pull(2024,['B23025_001E','B23025_006E']); c19=pull(2019)
X=json.load(open('cbsa_counties.json'))
out={}
for code,fs in X.items():
    a=[c24[f] for f in fs if f in c24]; b=[c19.get(f) for f in fs]
    pop=sum(x['pop'] for x in a); y=sum(x['y'] for x in a)
    af=sum(x['B23025_006E'] for x in a); p16=sum(x['B23025_001E'] for x in a)
    ok=all(b)
    pop19=sum(x['pop'] for x in b) if ok else None; y19=sum(x['y'] for x in b) if ok else None
    out[code]={'pop':pop,'y2544':y,'pop19':pop19,'y2544_19':y19,
               'growth':round(pop/pop19-1,4) if pop19 else None,'growth2544':round(y/y19-1,4) if y19 else None,
               'military':round(af/p16,4) if p16 else None,'counties':fs}
json.dump(out,open('cbsa_county_rollup.json','w'))
print('rollups',len(out),'missing 2019 (CT etc.)',sum(1 for v in out.values() if v['growth'] is None))
for k in ['48900','13460','23420','17410','49740','35620']:
    if k in out: print(k,{x:out[k][x] for x in ('pop','growth','growth2544','military')})

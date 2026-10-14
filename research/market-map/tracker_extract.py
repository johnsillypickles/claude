import json,re,collections
num=lambda s:(lambda t:float(t) if re.fullmatch(r'\d+(\.\d+)?',t) else None)(re.sub(r'[$,\s]','',s or ''))
def season_of(name):
    m=re.search(r'\|\s*(.+?)\s*$',name or '');return m.group(1) if m else ''
rows=[]
# current tab: header row 2
c=json.load(open('raw_tracker/current.json'))['values']
for r in c[3:]:
    r=r+['']*(90-len(r))
    if not r[6] or '{CITY' in r[6]: continue
    rows.append(dict(tab='current',fid=r[0],new=r[1],pid=r[2],name=r[6],season=f"{r[4].strip().title()} {r[5]}".strip(),status=r[7],signed=num(r[10]),remain=num(r[11]),weeks=num(r[15]),day=r[16],times=r[17],fac_courts=num(r[20]),hours=num(r[21]),courts=num(r[22]),court_hours=num(r[23]),spots=num(r[24]),cost=num(r[26]) or num(r[25]),price=num(r[28]),zip=r[75],host_remote=r[38],host_new=r[39]))
s=json.load(open('raw_tracker/spring.json'))['values']
for r in s[3:]:
    r=r+['']*(72-len(r))
    if not r[3] or '{CITY' in r[3]: continue
    rows.append(dict(tab='spring',fid=r[0],new=r[1],pid=r[2],name=r[3],season=season_of(r[3]),status=r[4],signed=num(r[7]),remain=num(r[8]),weeks=num(r[12]),day=r[13],times=r[14],fac_courts=num(r[70]),hours=num(r[17]),courts=num(r[18]),court_hours=num(r[19]),spots=num(r[20]),cost=num(r[69]) or num(r[21]),price=num(r[23]),zip=r[61],season_n=num(r[63])))
w=json.load(open('raw_tracker/winter.json'))['values']
for r in w[3:]:
    r=r+['']*(60-len(r))
    if not r[3] or '{CITY' in r[3]: continue
    rows.append(dict(tab='winter',fid=r[1],pid=r[2],name=r[3],season=season_of(r[3]) or 'Winter 2026',status=r[4],signed=None,weeks=None,day=r[27],times=r[25],fac_courts=num(r[29]),courts=num(r[30]),court_hours=num(r[31]),spots=num(r[32]),cost=num(r[33]),price=num(r[17])))
json.dump(rows,open('tracker.json','w'))
print(len(rows));print(collections.Counter((r['tab'],r['season']) for r in rows).most_common(20))
for k in ['signed','spots','cost','price','courts','court_hours','weeks','hours']:
    print(k,sum(1 for r in rows if r.get(k) is not None))
print(collections.Counter(r['status'] for r in rows).most_common(10))

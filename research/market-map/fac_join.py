import json,re,collections,difflib
FI=json.load(open('facility_info.json'))
O=json.load(open('venue_wl.json'))
norm=lambda s:re.sub(r'\b(the|pickleball|club|pb|and|at|n)\b','',re.sub(r'[^a-z0-9 ]',' ',(s or '').lower().replace('&',' '))).split()
def city(t):
    m=re.match(r'([^,:]+),\s*([A-Za-z]{2,})',t);return (m.group(1).lower().strip(),m.group(2).upper()) if m else ('','')
hit=0;miss=[]
for o in O:
    c,s=city(o['t']);vn=norm(o['venue'])
    best=(0,None)
    for f in FI:
        fn=norm(f['name'])
        r=difflib.SequenceMatcher(None,' '.join(vn),' '.join(fn)).ratio()
        if f['st']==s: r+=0.15
        if f['city'].lower()==c: r+=0.25
        if r>best[0]: best=(r,f)
    o['fac']=best[1] if best[0]>=0.85 else None
    if o['fac']: hit+=1
    else: miss.append((round(best[0],2),o['venue'],c,best[1]['name'] if best[1] else None,best[1]['city'] if best[1] else None))
print('matched',hit,'of',len(O))
for m in sorted(set(miss))[-25:]: print(m)
json.dump(O,open('venue_fac.json','w'))

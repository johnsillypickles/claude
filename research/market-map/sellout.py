import json,sys,collections
sys.path.insert(0,'.')
from metros import metro_of
def analyze(files):
    days=collections.defaultdict(list)
    for f in files:
        for d,p,s,e,u in json.load(open(f))['rows']:
            days[p].append((d,int(s),int(e),int(u)))
    out=[]
    for p,rows in days.items():
        m=metro_of(p)
        if not m or 'league' not in p.lower(): continue
        rows.sort(); sold=sum(r[3] for r in rows)
        if sold<5: continue
        cap=0; added=0; first_sale=None; soldout=None; manual_zero=None; launched=None
        for d,s,e,u in rows:
            adj=e-s+u               # >0 stock added, <0 manual removal
            if adj>0:
                if launched is None: launched=d; cap+=adj
                else: added+=adj
            if u>0 and first_sale is None: first_sale=d
            if e<=0 and s>0:
                if adj>=0 and soldout is None and manual_zero is None: soldout=d      # hit zero through sales
                elif adj<0 and manual_zero is None and soldout is None: manual_zero=d  # zeroed by hand
        start_cap=max([r[1] for r in rows if r[0]==rows[0][0]] or [0])
        cap=cap+start_cap  # stock already present at window start
        out.append({'product':p,'metro':m,'sold':sold,'cap':cap,'added':added,'first_sale':first_sale,'soldout':soldout,'manual_zero':manual_zero})
    return out
if __name__=='__main__':
    o=analyze(sys.argv[1:])
    c=collections.Counter('soldout' if x['soldout'] else 'zeroed' if x['manual_zero'] else 'open' for x in o)
    print(len(o),c)
    for x in sorted(o,key=lambda x:x['metro'])[:0]: pass
    for x in [y for y in o if 'Denver' in y['metro']][:12]: print(x)

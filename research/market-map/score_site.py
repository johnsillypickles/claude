"""Score a prospective venue against our 2026 leagues.
usage: python3 score_site.py ZIP BAR(yes/no/unknown) COURTS [name]"""
import json,sys,sqlite3,statistics as st,io,contextlib
with contextlib.redirect_stdout(io.StringIO()):
    import venue_features as vf
from geo import hav
W={'young_per_league':25,'pickleball_popular':15,'movers':15,'density':15,'few_kids':15,'bar':15}
ref=json.load(open('venue_fac2.json'))
def comps(f,lat,lng,own,trends,bar):
    return {'young_per_league':f['y25_39']/(1+own),'pickleball_popular':trends,'movers':f['movers'],
            'density':f['density'],'few_kids':-(f['kids_per_y'] or 0),'bar':{'Yes':1,'No':0}.get(bar,0.5)}
def nearest_trends(lat,lng):
    D=json.load(open('data_v4.json'));pts=[(m['lat'],m['lng'],m.get('trends'),m['metro']) for m in D['metros']]+[(c['lat'],c['lng'],c.get('trends'),c['name']) for c in D['cands']]
    return min(((hav(lat,lng,a,b),t,n) for a,b,t,n in pts if t is not None and a),key=lambda x:x[0])
# reference values for each existing league
for o in ref:
    o['c']=comps(o,o['lat'],o['lng'],o['own_near'],o['m_trends'] or 50,o['bar'])
def pct(k,x):
    if x is None: return 50
    v=[o['c'][k] for o in ref if o['c'][k] is not None];return 100*(sum(y<x for y in v)+0.5*sum(y==x for y in v))/len(v)
def score(c): return sum(W[k]*pct(k,c[k])/100 for k in W)
for o in ref: o['score']=score(o['c'])
if __name__=='__main__':
    z,bar,courts=sys.argv[1],sys.argv[2].capitalize(),sys.argv[3];name=' '.join(sys.argv[4:]) or z
    lat,lng,_=vf.ZXY[z];f=vf.feat(lat,lng)
    own=sum(1 for o in ref if o['season']=='Fall 2026' and hav(lat,lng,o['lat'],o['lng'])<=7)
    dist,tr,tm=nearest_trends(lat,lng)
    c=comps(f,lat,lng,own,tr,bar)
    raw={'young_per_league':f"{f['y25_39']:,.0f} aged 25-39 within 7 mi, {own} of our Fall 2026 leagues within 7 mi",
         'pickleball_popular':f"search score {tr:.0f} ({tm}, {dist:.0f} mi away)",'movers':f"{f['movers']:.1%} of 25-39s moved in from out of state last year",
         'density':f"{f['density']:,.0f} people per sq mi",'few_kids':f"{100*f['kids_per_y']:.0f} kids under 5 per 100 aged 25-39",'bar':bar}
    print(f"\n{name}  (ZIP {z}, {courts} courts)\n")
    print(f"{'factor':20}{'weight':>7}{'pctile':>8}{'points':>8}   detail")
    tot=0
    for k in W:
        p=pct(k,c[k]);pts=W[k]*p/100;tot+=pts
        print(f"{k:20}{W[k]:6}%{p:8.0f}{pts:8.1f}   {raw[k]}")
    S=sorted(o['score'] for o in ref);rank=sum(s<tot for s in S)/len(S)
    print(f"\nTOTAL {tot:.0f} / 100   (beats {rank:.0%} of our 2026 leagues)")
    bands=[(0,35),(35,45),(45,55),(55,65),(65,101)]
    for a,b in bands:
        L=[o for o in ref if a<=o['score']<b]
        if L: print(f"   our leagues scoring {a}-{min(b,100)}: {sum(o['soldout'] for o in L)}/{len(L)} sold out = {sum(o['soldout'] for o in L)/len(L):.0%}, median demand {st.median(o['demand'] for o in L):.2f}x capacity"+("   <== this site" if a<=tot<b else ''))
    ci=int(courts) if courts.isdigit() else None
    print(f"\nChecks (not scored): courts {courts}"+(" (7+ courts: our bigger venues average lower demand than 6-court ones)" if ci and ci>6 else ''))

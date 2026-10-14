import json,re,collections,statistics as st,io,contextlib
with contextlib.redirect_stdout(io.StringIO()):
    from venue_wl import spear
norm=lambda s:re.sub(r'[^a-z0-9]','',re.sub(r'_[\d_]+$','',s or '').lower())
P=collections.defaultdict(lambda:[0.0,0])
for f in ['ads_q4_25.json','ads_q1.json','ads_q2.json','ads_q3.json','ads_oct26.json']:
    for r in json.load(open(f))['rows']:
        n=r.get('name') or ''
        if '|' in n and 'League' in n:
            k=norm(n);P[k][0]+=float(r['spend'] or 0);P[k][1]+=int(r['purchases'] or 0)
D=json.load(open('viab3.json'));M=json.load(open('scorer_data2.json'));W=M['W'];ref=M['ref']
def pct(k,x):
    if x is None: return 50
    v=ref[k];return 100*(sum(y<x for y in v)+.5*sum(y==x for y in v))/len(v)
FREE={'San Diego, CA: Pickleball Ladder League at The HUB San Diego | Summer 2026':23,'Englewood, NJ: Pickleball Ladder League at SPORTIME Pickleball | Spring 2026':14,
 'Atlanta, GA: Pickleball Ladder League at ITP Pickleball Club (Indoor) | Summer 2026':10,'Evansville, IN: Pickleball Ladder League at 3rd Shot Pickleball | Spring 2026':8,
 'Highland Park, IL: Pickleball Ladder League at Dinx Social Club (Sundays) | Summer 2026':7,'Chicago, IL: Pickleball Ladder League at SPF Lincoln Park (Sundays) | Fall 2026':7,
 'North Aurora, IL: Pickleball Ladder League at Pickleball Kingdom | Summer 2026':6,'Denver, CO: Pickleball Ladder League at Mile Hi Pickleball | Summer 2026':5,
 'Miami, FL: Pickleball Ladder League at Fair Expo Pickleball | Summer 2026':7,'Chicago, IL: Pickleball Ladder League at SPF Lincoln Park (Sundays) | Summer 2026':5,
 'Indianapolis, IN: Pickleball Ladder League at 3rd Shot Pickleball | Summer 2026':4,'Webster, TX: Pickleball Ladder League at Chicken n Pickle | Fall 2026':4}
hit=0
for d in D:
    d['vs']=sum(W[k]*pct(k,d[k])/100 for k in W)
    s,p=P.get(norm(d['name']),(0.0,0));d['p1']=s;d['p1_purch']=p;hit+=s>0
    d['free']=FREE.get(d['name'],0);d['paid']=max(0,d['players']-d['free'])
    d['p1_per_spot']=s/d['spots']
print('leagues',len(D),'with Phase 1 spend',hit,' total P1 spend $',round(sum(d['p1'] for d in D)))
print('paid players <30:',sum(d['paid']<30 for d in D),' vs all players <30:',sum(d['players']<30 for d in D))
for a,b in [(0,35),(35,55),(55,65),(65,101)]:
    L=[d for d in D if a<=d['vs']<b];S=[d for d in L if d['p1']>0]
    print(f"score {a}-{b}: n={len(L):3}  got Phase 1 {len(S)/len(L):4.0%}  P1 $ per league {sum(d['p1'] for d in L)/len(L):6.0f}  P1 $ per spot {sum(d['p1'] for d in L)/sum(d['spots'] for d in L):5.1f}  filled 80%+ {sum(d['fill']>=.8 for d in L)/len(L):.0%}  filled 80%+ with no P1 {sum(d['fill']>=.8 and d['p1']==0 for d in L)/len(L):.0%}")
print('rho score vs P1 $/spot',round(spear([d['vs'] for d in D],[d['p1_per_spot'] for d in D]),2))
S1=[d for d in D if d['sn']==1];print('season 1: got P1',sum(d['p1']>0 for d in S1),'of',len(S1),' rho score vs P1/spot',round(spear([d['vs'] for d in S1],[d['p1_per_spot'] for d in S1]),2))
top=sorted(D,key=lambda d:-d['p1'])[:12]
for d in top: print(f"  ${d['p1']:6.0f} {d['p1_purch']:3} purch  players {d['players']:.0f}/{d['spots']:.0f} score {d['vs']:.0f}  {d['name'][:80]}")
json.dump(D,open('viab4.json','w'))

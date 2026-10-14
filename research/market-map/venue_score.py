import json,collections
O=json.load(open('venue_feats2.json'))
def pct(f,inv=False):
    v=sorted(o[f] for o in O if o[f] is not None)
    for o in O:
        x=o[f]; p=(sum(1 for y in v if y<x)+0.5*sum(1 for y in v if y==x))/len(v)*100 if x is not None else 50
        o['p_'+f]=100-p if inv else p
for f in ['y25_39','y_per_own','density','y_share','m_trends','movers','m_transplant','income']: pct(f)
pct('kids_per_y',inv=True); pct('own_near',inv=True)
S={
 'Tommy 60/20/20':{'y25_39':.6,'m_trends':.2,'movers':.2},
 'Young adults only':{'y25_39':1},
 'Proposed':{'y_per_own':.35,'density':.2,'m_trends':.2,'kids_per_y':.15,'movers':.1},
}
def auc(sc,lab):
    pos=[s for s,l in zip(sc,lab) if l];neg=[s for s,l in zip(sc,lab) if not l]
    return sum((p>q)+0.5*(p==q) for p in pos for q in neg)/(len(pos)*len(neg))
def within(key):
    g=collections.defaultdict(list)
    for o in O: g[o['metro']].append(o)
    num=den=0
    for L in g.values():
        for a in L:
            for b in L:
                if a['soldout'] and not b['soldout']:
                    den+=1;num+=(a[key]>b[key])+0.5*(a[key]==b[key])
    return num/den,den
for name,w in S.items():
    for o in O: o['s']=sum(o['p_'+k]*v for k,v in w.items())
    a=auc([o['s'] for o in O],[o['soldout'] for o in O]);wi,pairs=within('s')
    Q=sorted(O,key=lambda o:o['s']);q=[Q[i*len(Q)//5:(i+1)*len(Q)//5] for i in range(5)]
    print(f"{name:20} AUC all {a:.2f}  within-metro {wi:.2f} ({pairs} pairs)  sell-out by quintile: "+' '.join(f"{sum(o['soldout'] for o in g)/len(g):.0%}" for g in q))
# seasonal robustness for proposed
for o in O: o['s']=sum(o['p_'+k]*v for k,v in S['Proposed'].items())
for o in O: o['tommy']=sum(o['p_'+k]*v for k,v in S['Tommy 60/20/20'].items())
by=collections.defaultdict(list)
for o in O: by[o['season']].append(o)
for s,L in sorted(by.items()):
    if len(L)>30: print(s,len(L),f"proposed {auc([o['s'] for o in L],[o['soldout'] for o in L]):.2f} tommy {auc([o['tommy'] for o in L],[o['soldout'] for o in L]):.2f}")
json.dump(O,open('venue_scored.json','w'))

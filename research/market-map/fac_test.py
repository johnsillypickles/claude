import json,collections,statistics as st,random,io,contextlib
with contextlib.redirect_stdout(io.StringIO()):
    from venue_wl import spear
O=[o for o in json.load(open('venue_fac.json')) if o['fac']]
random.seed(3);print('match spot check:',[(o['venue'],o['fac']['name']) for o in random.sample(O,6)])
money=lambda s:float(s.replace('$','').replace(',','')) if s and s.replace('$','').replace(',','').replace('.','').isdigit() else None
for o in O:
    f=o['fac'];o['courts']=int(f['courts']) if f['courts'].isdigit() else None
    o['io']=f['io'] or None;o['bar']=f['bar'] or None;o['gov']=f['gov'] or None
    o['price']=money(f.get(o['season']+'|price'));o['ccost']=money(f.get(o['season']+'|cost'))
# price relative to metro median that season
g=collections.defaultdict(list)
for o in O:
    if o['price']: g[(o['metro'],o['season'])].append(o['price'])
for o in O: o['price_rel']=o['price']/st.median(g[(o['metro'],o['season'])]) if o['price'] else None
def show(lab,key,buckets):
    print(f"\n{lab}")
    for name,fn in buckets:
        L=[o for o in O if o.get(key) is not None and fn(o[key])]
        if not L: continue
        so=[o for o in L if o['soldout']]
        print(f"  {name:16} n={len(L):3}  sold out {len(so)/len(L):4.0%}  median demand/cap {st.median(o['demand'] for o in L):.2f}  median waitlist (sold out) {st.median([o['wl_unmet'] for o in so] or [0]):.0f}")
show('Courts at facility','courts',[('1-6',lambda x:x<=6),('7-10',lambda x:7<=x<=10),('11-14',lambda x:11<=x<=14),('15+',lambda x:x>=15)])
show('Indoor / outdoor','io',[(k,lambda x,k=k:x==k) for k in ['Indoor','Both','Outdoor']])
show('Onsite bar','bar',[(k,lambda x,k=k:x==k) for k in ['Yes','No']])
show('Ownership','gov',[(k,lambda x,k=k:x==k) for k in ['Private/Corporate','Gov-Owned']])
show('Price vs metro median','price_rel',[('10%+ cheaper',lambda x:x<0.9),('about median',lambda x:0.9<=x<=1.1),('10%+ pricier',lambda x:x>1.1)])
show('League price','price',[('under $150',lambda x:x<150),('$150-179',lambda x:150<=x<180),('$180+',lambda x:x>=180)])
P=[o for o in O if o['courts']];print('\nrho courts vs demand',round(spear([o['courts'] for o in P],[o['demand'] for o in P]),2),' courts vs capacity',round(spear([o['courts'] for o in P],[o['cap'] for o in P]),2))
# Indoor x bar
print('\nIndoor/Both x bar:')
for io in ['indoor-ish','Outdoor']:
    for b in ['Yes','No']:
        L=[o for o in O if (o['io'] in ('Indoor','Both') if io=='indoor-ish' else o['io']=='Outdoor') and o['bar']==b]
        if L: print(f"  {io:10} bar={b:3} n={len(L):3} sold out {sum(o['soldout'] for o in L)/len(L):.0%} median demand {st.median(o['demand'] for o in L):.2f}")
json.dump(O,open('venue_fac2.json','w'))

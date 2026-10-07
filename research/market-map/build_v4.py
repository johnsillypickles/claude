import csv,json,re,sys,collections,statistics as st,datetime as dt
sys.path.insert(0,'.')
from geo import city_xy,hav
from metros import metro_of
D=json.load(open('data.json'))
# ---------- Census CBSA with coords
cb=[]
for r in csv.DictReader(open('census_cbsa.csv')):
    sts=r['state'].split('-'); xy=None
    for s in sts:
        xy=city_xy(r['principal_city'],s)
        if xy: break
    if not xy: continue
    f=lambda k: float(r[k]) if r[k] not in ('',None) else None
    cb.append({'code':r['cbsa_code'],'name':re.sub(r' (Metro|Micro) Area$','',r['name']),'city':r['principal_city'].split('/')[0],'st':sts[0],'lat':xy[0],'lng':xy[1],
               'pop':int(r['pop']),'income':f('income'),'age':f('median_age'),'y2544':f('share_25_44'),'ba':f('share_ba_plus'),'growth':f('pop_growth_5y')})
print('cbsa with coords',len(cb))
# ---------- Trends DMA -> coords of named cities
TR=collections.defaultdict(dict)
for r in csv.DictReader(open('trends_dma.csv')): TR[r['dma']][r['term']]=int(r['score'])
def dma_points(name):
    m=re.match(r'^(.*?)[ ,]+([A-Z]{2}(?:-[A-Z]{2})?)(?:-(.*))?$',name)
    pts=[]
    name=re.sub(r'\s*\([^)]*\)\s*',' ',name).replace('Tri-Cities TN-VA','Johnson City TN-Kingsport TN-Bristol VA')
    # split into "City(-City)* ST" segments, e.g. "Boston MA-Manchester NH"
    for seg in re.findall(r'([A-Za-z\.\'\s&/-]+?)\s*,?\s+([A-Z]{2})\b',name):
        cities,stt=seg
        for c in re.split(r'-|&|/',cities):
            c=c.strip()
            if c:
                xy=city_xy(c,stt)
                if xy: pts.append(xy)
    return pts
DP={d:dma_points(d) for d in TR}
print('dmas without coords',[d for d,p in DP.items() if not p][:20])
terms=['pickleball','pickleball near me','pickleball league','indoor pickleball','pickleball lessons']
# percentile rank per term across DMAs, composite = mean of 'pickleball','pickleball near me','pickleball league'
def pct(term):
    v=sorted(TR[d].get(term,0) for d in TR); n=len(v)
    return {d:(sum(1 for x in v if x<TR[d].get(term,0))+0.5*sum(1 for x in v if x==TR[d].get(term,0)))/n*100 for d in TR}
P={t:pct(t) for t in terms}
TI={d:round((P['pickleball'][d]+P['pickleball near me'][d]+P['pickleball league'][d])/3,1) for d in TR}
OVR={'Worcester':'Boston MA-Manchester NH','Manchester':'Boston MA-Manchester NH'}
def nearest_dma(lat,lng,maxmi=90):
    best=(1e9,None)
    for d,pts in DP.items():
        for p in pts:
            x=hav(lat,lng,*p)
            if x<best[0]: best=(x,d)
    return best[1] if best[0]<=maxmi else None
for c in cb:
    c['dma']=OVR.get(c['city']) or nearest_dma(c['lat'],c['lng']); c['trends']=TI.get(c['dma']); c['tr_raw']=TR.get(c['dma'],{})
# ---------- footprint metros -> CBSA (largest CBSA within 30 mi of metro center)
for m in D['metros']:
    if m['intl'] or not m['lat']: m['cbsa']=None; continue
    near=[c for c in cb if hav(m['lat'],m['lng'],c['lat'],c['lng'])<=30]
    c=max(near,key=lambda c:c['pop']) if near else None
    m['cbsa']=c['code'] if c else None
CB={c['code']:c for c in cb}
# ---------- sell-out by metro
L=json.load(open('leagues.json'))
def seas(s):
    s=s.lower()
    if 'fall 2026' in s or 'september - november' in s: return 'Fall 2026'
    if 'summer 2026' in s or 'june - august' in s or 'july - august' in s: return 'Summer 2026'
    if 'spring 2026' in s: return 'Spring 2026'
    if 'winter 2026' in s: return 'Winter 2026'
    return None
SE=['Winter 2026','Spring 2026','Summer 2026','Fall 2026']
g=collections.defaultdict(lambda:collections.defaultdict(list))
for x in L:
    s=seas(x['season'])
    if s and x['sold']>=10: g[x['metro']][s].append(x)
for m in D['metros']:
    so={};allL=[];
    for s in SE:
        Ls=g[m['metro']].get(s,[]); allL+=Ls
        so[s]={'n':len(Ls),'so':sum(1 for x in Ls if x['soldout'])}
    sold=[x for x in allL if x['soldout']]
    days=[(dt.date.fromisoformat(x['soldout'])-dt.date.fromisoformat(x['first_sale'])).days for x in sold]
    rec=[x for x in allL if seas(x['season']) in ('Summer 2026','Fall 2026')]
    m['so']={'seasons':so,'n':len(allL),'rate':round(len(sold)/len(allL),3) if allL else None,
             'recentN':len(rec),'recentRate':round(sum(1 for x in rec if x['soldout'])/len(rec),3) if rec else None,
             'medDays':st.median(days) if days else None,'addedPer':round(sum(x['added'] for x in allL)/len(allL),1) if allL else None,
             'fallLeagues':so['Fall 2026']['n']}
    c=CB.get(m['cbsa'])
    if c:
        m['census']={k:c[k] for k in ('name','pop','income','age','y2544','ba','growth')}
        m['trends']=c['trends']; m['trendsDma']=c['dma']
        a=c['pop']*(c['y2544'] or 0.27)/1e5
        m['density']=round(m['so']['fallLeagues']/a,3) if a else None   # Fall leagues per 100k residents aged 25-44
    else: m['census']=None; m['trends']=None; m['density']=None
# ---------- expansion candidates from Census
foot=[(m['lat'],m['lng']) for m in D['metros'] if not m['intl'] and m['lat']]
sig=D['signals']
FM={m['metro']:m for m in D['metros']}
cands=[]
for c in cb:
    if c['pop']<200000 or c['st']=='PR': continue
    dmin=min(hav(c['lat'],c['lng'],*f) for f in foot)
    if dmin<=30: continue
    near=min(((hav(c['lat'],c['lng'],m['lat'],m['lng']),m['metro']) for m in D['metros'] if not m['intl'] and m['lat']))
    s=collections.Counter()
    for x in sig:
        if min(hav(x['lat'],x['lng'],*f) for f in foot)<=30: continue
        if hav(c['lat'],c['lng'],x['lat'],x['lng'])<=35:
            s['req']+=x['location_request']; s['host']+=x['host_applicant']; s['notify']+=x['notify_me']
    cands.append({'city':c['city'],'st':c['st'],'name':c['name'],'lat':round(c['lat'],3),'lng':round(c['lng'],3),'pop':c['pop'],'income':c['income'],'growth':c['growth'],
                  'y2544':c['y2544'],'ba':c['ba'],'age':c['age'],'trends':c['trends'],'dma':c['dma'],'tr_pb':c['tr_raw'].get('pickleball'),'tr_near':c['tr_raw'].get('pickleball near me'),
                  'tr_league':c['tr_raw'].get('pickleball league'),'nearest_footprint':near[1],'dist_mi':round(near[0]),'req':s['req'],'host':s['host'],'notify':s['notify']})
print('candidates',len(cands))
D['cands']=cands
D['trendsNote']={'terms':['pickleball','pickleball near me','pickleball league'],'nDma':len(TR)}
json.dump(D,open('data_v4.json','w'),separators=(',',':'))
# quick views
print('\nADD-LEAGUES inputs (US metros with 4+ leagues)')
for m in sorted([m for m in D['metros'] if m['so']['n']>=4 and not m['intl']],key=lambda m:-(m['so']['rate'] or 0)):
    c=m['census'] or {}
    print(f"{m['metro'][:20]:20} n={m['so']['n']:>3} rate={m['so']['rate']:.0%} recent={m['so']['recentRate'] or 0:.0%} days={m['so']['medDays']} add/lg={m['so']['addedPer']} dens={m['density']} trends={m['trends']} pop={c.get('pop')}")
print('\nTOP CANDIDATES by pop')
for c in sorted(cands,key=lambda c:-c['pop'])[:25]: print(c['city'],c['st'],c['pop'],c['growth'],c['trends'],c['dma'],c['dist_mi'],c['req'],c['host'],c['notify'])

# ---------- component scores (0-100 percentile within peer set)
def prank(vals, v, invert=False):
    xs=[x for x in vals if x is not None]
    if v is None or not xs: return None
    r=(sum(1 for x in xs if x<v)+0.5*sum(1 for x in xs if x==v))/len(xs)*100
    return round(100-r if invert else r,1)
def mean(xs):
    xs=[x for x in xs if x is not None]; return round(sum(xs)/len(xs),1) if xs else None
# new players per league by quarter
nl=collections.defaultdict(dict)
for q in ['q1','q2','q3']:
    agg=collections.defaultdict(lambda:[0,0,0])
    for r in json.load(open(f'prod_{q}.json'))['rows']:
        mm=metro_of(r['name'])
        if mm and (r['orders'] or 0)>=5: a=agg[mm]; a[0]+=1; a[1]+=r['orders']; a[2]+=r['first_time_orders']
    for mm,a in agg.items(): nl[mm][q]={'leagues':a[0],'newPer':round(a[2]/a[0],1),'newShare':round(a[2]/a[1],3)}
DMA={r['dma']:r for r in D['dma']['rows']}
WL=json.load(open('waitlist_agg.json'))['byMetro']
for m in D['metros']:
    w=WL.get(m['metro'],{}); m['wl']={'after':w.get('after_sellout',0),'close':w.get('after_close',0),'pre':w.get('pre_launch',0)}
    m['wlPer']=round(m['wl']['after']/m['so']['n'],1) if m['so']['n'] else None
peer=[m for m in D['metros'] if not m['intl'] and (m['so']['n']>=4 or (m['so']['n']>=2 and m['wl']['after']>=200))]
for m in D['metros']:
    m['nl']=nl.get(m['metro'],{})
    q1=m['nl'].get('q1',{}).get('newPer'); q3=m['nl'].get('q3',{}).get('newPer')
    m['momentum']=round(q3/q1,2) if q1 and q3 else None
    d=DMA.get(m.get('dma')); m['cacEst']=d['cacEst'] if d else None; m['ctr']=d['ctr'] if d else None
P_=lambda key,inv=False: (lambda m: prank([p[key] if not callable(key) else key(p) for p in peer], m[key] if not callable(key) else key(m), inv))
for m in D['metros']:
    if m in peer:
        sod=lambda x: x['so']['medDays']
        m['cmp']={
          'sell': mean([prank([p['so']['recentRate'] for p in peer],m['so']['recentRate']),prank([p['so']['recentRate'] for p in peer],m['so']['recentRate']),
                        prank([p['so']['rate'] for p in peer],m['so']['rate']),
                        prank([p['so']['medDays'] for p in peer],m['so']['medDays'],True) if m['so']['medDays'] is not None else 0,
                        prank([p['so']['addedPer'] for p in peer],m['so']['addedPer'])]),
          'mom': mean([prank([p['momentum'] for p in peer],m['momentum']), prank([p['nl'].get('q3',{}).get('newShare') for p in peer],m['nl'].get('q3',{}).get('newShare'))]),
          'room': mean([prank([p['density'] for p in peer],m['density'],True), prank([p['trends'] for p in peer],m['trends'])]),
          'eff': prank([p['cacEst'] for p in peer],m['cacEst'],True),
          'wait': prank([p['wlPer'] for p in peer],m['wlPer'])}
    else: m['cmp']=None
C2=D['cands']
for c in C2:
    import math
    c['cmp']={'pop':prank([math.log(x['pop']) for x in C2],math.log(c['pop'])),
              'search':prank([x['trends'] for x in C2],c['trends']),
              'demo':mean([prank([x['y2544'] for x in C2],c['y2544']),prank([x['ba'] for x in C2],c['ba']),prank([x['income'] for x in C2],c['income']),prank([x['growth'] for x in C2],c['growth'])]),
              'ours':None}
    dsum=c['req']*3+c['host']*2+c['notify']
    c['demand']=dsum
    c['launching']=c['city'] in ('Fort Wayne','Little Rock')
mx=max(math.log1p(c['demand']) for c in C2) or 1
for c in C2: c['cmp']['ours']=round(math.log1p(c['demand'])/mx*100,1)
json.dump(D,open('data_v4.json','w'),separators=(',',':'))
W={'sell':35,'wait':25,'mom':10,'room':20,'eff':10}
def sc(m): 
    c=m['cmp']; return sum((c[k] or 0)*w for k,w in W.items())/100
print('\nADD-LEAGUES default ranking')
for m in sorted(peer,key=lambda m:-sc(m)):
    print(f"{m['metro'][:22]:22} score={sc(m):5.1f} sell={m['cmp']['sell']} mom={m['cmp']['mom']} room={m['cmp']['room']} eff={m['cmp']['eff']}")
WE={'pop':30,'search':25,'demo':25,'ours':20}
print('\nEXPANSION default ranking')
for c in sorted(C2,key=lambda c:-sum((c['cmp'][k] or 0)*w for k,w in WE.items()))[:20]:
    print(c['city'],c['st'],round(sum((c['cmp'][k] or 0)*w for k,w in WE.items())/100,1),c['cmp'],c['dist_mi'])

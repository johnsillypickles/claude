import json,math,statistics as st
D=json.load(open('data_v4.json'))
DMA={r['dma']:r for r in D['dma']['rows']}
def prank(vals,v,inv=False):
    xs=[x for x in vals if x is not None]
    if v is None or not xs: return None
    r=(sum(1 for x in xs if x<v)+0.5*sum(1 for x in xs if x==v))/len(xs)*100
    return round(100-r if inv else r,1)
rows=[]
for m in D['metros']:
    so=m['so']; c=m.get('census') or {}
    orders=sum(q['orders'] for q in m['q'])
    if so['n']==0 and orders<20: continue
    d=DMA.get(m.get('dma')) or {}
    a=(c.get('pop') or 0)*(c.get('y2544') or 0)/1e5
    rows.append({'metro':m['metro'],'intl':m['intl'],'lat':m['lat'],'lng':m['lng'],'leagues':so['n'],'fall':so['fallLeagues'],
      'orders':orders,'new':m['new'],'soRate':so['rate'],'soRecent':so['recentRate'],'medDays':so['medDays'],'addedPer':so['addedPer'],
      'wl':m['wl']['after'],'wlPer':m['wlPer'],'ordPer':round(orders/so['n'],1) if so['n'] else None,
      'pen':round(m['new']/a,1) if a else None,
      'spend':d.get('spend'),'costNew':d.get('cacFloor'),'cacEst':d.get('cacEst'),'ctr':d.get('ctr'),'dma':m.get('dma'),
      'pop':c.get('pop'),'y2544':c.get('y2544'),'income':c.get('income'),'growth':c.get('growth'),'ba':c.get('ba'),'trends':m.get('trends'),'density':m.get('density'),
      'cbsaName':c.get('name')})
peer=[r for r in rows if r['leagues']>=3]
for r in rows:
    if r['leagues']>=3:
        parts=[prank([p['soRate'] for p in peer],r['soRate']),prank([p['wlPer'] for p in peer],r['wlPer']),prank([p['ordPer'] for p in peer],r['ordPer'])]
        if r['pen'] is not None: parts.append(prank([p['pen'] for p in peer],r['pen']))
        r['index']=round(sum(parts)/len(parts),1)
        if r['soRate'] is not None and r['soRate']>=0.6 and r['index']>=60: r['verdict']='under'
        elif r['leagues']>=8 and (r['soRate'] or 0)<0.3: r['verdict']='saturated'
        elif r['index']>=45: r['verdict']='balanced'
        else: r['verdict']='soft'
    else: r['index']=None; r['verdict']='early'
import collections
print(collections.Counter(r['verdict'] for r in rows))
for r in sorted([r for r in rows if r['index'] is not None],key=lambda r:-r['index'])[:15]: print(r['metro'],r['index'],r['verdict'],r['leagues'],r['soRate'],r['wl'])
# new markets: default score
for c in D['cands']:
    w={'pop':30,'search':15,'demo':35,'ours':20}
    c['score']=round(sum((c['cmp'][k] or 0)*v for k,v in w.items())/100,1)
cands=sorted(D['cands'],key=lambda c:-c['score'])
tot={'metros':len(rows),'us':sum(1 for r in rows if not r['intl']),'leagues':sum(r['leagues'] for r in rows),'players':sum(r['orders'] for r in rows),
     'newPlayers':sum(r['new'] for r in rows),'waitlist':sum(r['wl'] for r in rows),
     'soRate':round(sum(r['soRate']*r['leagues'] for r in rows if r['soRate'] is not None)/sum(r['leagues'] for r in rows if r['soRate'] is not None),3)}
print(tot)
json.dump({'metros':rows,'cands':[{k:c[k] for k in ('city','st','name','lat','lng','pop','income','growth','y2544','ba','trends','req','host','notify','nearest_footprint','dist_mi','score','launching')} for c in cands],'tot':tot},open('facility.json','w'),separators=(',',':'))

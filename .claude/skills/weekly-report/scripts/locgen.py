"""Localized vs generic creative, head to head within each market (ad set).
Usage: python3 -I locgen.py <adset_json> <label>=<ad_json>[,<ad_json>...] ... --out out.json
Ad JSONs are Lebesgue get_advertising_data_table level=ad period_type=all chunks (summed)."""
import json, sys, re, collections
args=sys.argv[1:]; out=args[args.index('--out')+1]; args=args[:args.index('--out')]
adset_names={r['adset_id']:r['name'] for r in json.load(open(args[0]))['rows']}
CAMP={"120252229329790019":"Fall26_Phase1_ProblemChildren","120253767214500019":"EarlyWinter27_Phase1",
      "120252634833170019":"Fall26_Phase0_Regional","120253767213590019":"EarlyWinter27_Phase0"}
# market campaigns: any name containing Phase1, plus Phase 0 Regional (per region/metro) and EarlyWinter27_Phase0
def is_market(cname): return 'Phase1' in cname or 'Regional' in cname or cname=='EarlyWinter27_Phase0' or (cname.startswith('Winter27_') and 'LeadForm' not in cname)
def classify(name):
    n=name.lower()
    if '_localized_' in n: return 'localized','rule1: _Localized_ template'
    if re.search(r'[_ -]localized$',n): return 'localized','rule2: _localized suffix (per-location version of a generic twin)'
    if re.search(r'(?<![a-z])(houston|dallas|tualatin|chicago|seattle)(?![a-z])',n): return 'localized','rule3: city in name'
    return 'generic',''
M=['spend','purchases','purchases_conversion_value','pixel_conversion_value','pixel_purchases','clicks','impressions']
def metrics(a):
    s=a['spend']; return {'spend':round(s,2),'purchases':a['purchases'],'revenue':round(a['purchases_conversion_value'],2),
      'roas':round(a['purchases_conversion_value']/s,2) if s else None,
      'pixel_roas':round(a['pixel_conversion_value']/s,2) if s else None,
      'ctr_pct':round(100*a['clicks']/a['impressions'],2) if a['impressions'] else None,
      'cpp':round(s/a['purchases'],2) if a['purchases'] else None,'ads':sorted(a['ads'])}
result={'classification':{},'windows':{}}
for spec in args[1:]:
    label,files=spec.split('=',1)
    agg=collections.defaultdict(lambda:{**{m:0 for m in M},'ads':set()})
    for f in files.split(','):
        for r in json.load(open(f))['rows']:
            # campaign name lookup via adset json campaign ids
            cname=CAMP.get(r['campaign_id'],r['campaign_id'])
            if not is_market(cname) or r['spend']<=0: continue
            b,why=classify(r['name']); result['classification'][r['name']]=[b,why]
            k=(r['adset_id'],b); a=agg[k]
            for m in M: a[m]+=r[m] or 0
            a['ads'].add(r['name'])
    rows=[]; tot={b:{m:0 for m in M} for b in ('localized','generic')}; won=lost=0
    for aid in sorted({k[0] for k in agg}):
        L,G=agg.get((aid,'localized')),agg.get((aid,'generic'))
        if not L or not G or L['spend']<=0 or G['spend']<=0: continue
        lm,gm=metrics(L),metrics(G)
        win='localized' if (lm['roas'] or 0)>(gm['roas'] or 0) else 'generic'
        pwin='localized' if (lm['pixel_roas'] or 0)>(gm['pixel_roas'] or 0) else 'generic'
        flags=[]
        if lm['spend']<300 or gm['spend']<300: flags.append('under $300 on a side')
        if lm['purchases']<5 or gm['purchases']<5: flags.append('under 5 purchases on a side')
        won+=win=='localized'; lost+=win=='generic'
        for b,src in (('localized',L),('generic',G)):
            for m in M: tot[b][m]+=src[m]
        nm=adset_names.get(aid,aid)
        rows.append({'adset_id':aid,'market':nm.split(' | ')[0],'metro':nm.split(':')[0],'localized':lm,'generic':gm,
                     'winner_meta_roas':win,'winner_pixel_roas':pwin,'flags':flags})
    rows.sort(key=lambda r:-(r['localized']['spend']+r['generic']['spend']))
    T={b:metrics({**tot[b],'ads':set()}) for b in tot}
    for b in T: T[b].pop('ads')
    clean=[r for r in rows if not r['flags']]
    result['windows'][label]={'markets':rows,'totals':T,'localized_won':won,'localized_lost':lost,
        'pixel_localized_won':sum(r['winner_pixel_roas']=='localized' for r in rows),
        'clean_markets_localized_won':sum(r['winner_meta_roas']=='localized' for r in clean),'clean_markets':len(clean)}
json.dump(result,open(out,'w'),indent=1)

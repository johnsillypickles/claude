import csv,json,sys,collections
sys.path.insert(0,'.')
from metros import metro_of
DMA={'Chicago, IL':['Chicago, IL'],'New York, NY':['New York, NY','Bridgeport-Stamford, CT'],'Los Angeles, CA':['Los Angeles, CA','Riverside, CA'],
'Houston, TX':['Houston, TX'],'Dallas-Ft. Worth, TX':['Dallas-Fort Worth, TX'],'Denver-Aurora, CO':['Denver, CO'],'Indianapolis, IN':['Indianapolis, IN'],
'Atlanta, GA':['Atlanta, GA'],'Philadelphia, PA':['Philadelphia, PA','Trenton, NJ','Allentown, PA'],'Miami, FL':['Miami, FL'],'Minneapolis-St. Paul, MN':['Minneapolis, MN'],
'Boston, MA':['Boston, MA'],'Phoenix, AZ':['Phoenix, AZ'],'Austin, TX':['Austin, TX'],'Portland, OR':['Portland, OR'],'Albuquerque, NM':['Albuquerque, NM'],
'Charlotte, NC':['Charlotte, NC'],'Nashville, TN':['Nashville, TN'],'Washington, DC':['Washington, DC'],'Louisville, KY':['Louisville, KY'],'Raleigh-Durham, NC':['Raleigh, NC'],
'Baltimore, MD':['Baltimore, MD'],'Las Vegas, NV':['Las Vegas, NV'],'Columbus, OH':['Columbus, OH'],'Jacksonville, FL':['Jacksonville, FL'],'Oklahoma City, OK':['Oklahoma City, OK'],
'San Francisco-San Jose, CA':['San Francisco, CA'],'San Diego, CA':['San Diego, CA'],'Baton Rouge, LA':['Baton Rouge, LA'],'Salt Lake City, UT':['Salt Lake City, UT'],
'Orlando, FL':['Orlando, FL','Daytona Beach, FL','Ocala, FL'],'Charleston, SC':['Charleston, SC'],'Knoxville, TN':['Knoxville, TN'],'Grand Rapids-Kalamazoo, MI':['Grand Rapids, MI','Kalamazoo, MI'],
'Kansas City, MO':['Kansas City, MO'],'Wichita, KS':['Wichita, KS'],'Seattle, WA':['Seattle, WA'],'Des Moines, IA':['Des Moines, IA'],'Tampa-St. Petersburg, FL':['Tampa, FL'],
'Fresno, CA':['Fresno, CA'],'Evansville-Owensboro, IN-KY':['Evansville, IN'],'Milwaukee, WI':['Milwaukee, WI'],'St. Louis, MO':['St. Louis, MO'],'San Antonio, TX':['San Antonio, TX'],
'Greensboro-Winston-Salem, NC':['Winston-Salem, NC'],'Detroit, MI':['Detroit, MI'],'Boise, ID':['Boise, ID'],'Cincinnati, OH':['Cincinnati, OH'],'Cleveland, OH':['Cleveland, OH','Sandusky, OH'],
'New Orleans, LA':['New Orleans, LA'],'Colorado Springs, CO':['Colorado Springs, CO'],'Pittsburgh, PA':['Pittsburgh, PA'],'Springfield, MA':['Springfield, MA'],'Lexington, KY':['Lexington, KY'],
'Buffalo, NY':['Buffalo, NY'],'Portland, ME':['Portland, ME'],'Hartford-New Haven, CT':['Hartford, CT'],'Greenville-Spartanburg-Ashville, SC-NC':['Greenville, SC'],
'Harrisonburg, VA':['Harrisonburg, VA'],'Madison, WI':['Madison, WI'],'Dayton, OH':['Dayton, OH'],'Charlottesville, VA':['Charlottesville, VA'],'Rochester, NY':['Rochester, NY'],
'Ft. Wayne, IN':['Fort Wayne, IN'],'Little Rock, AR':['Little Rock, AR']}
f=lambda x: float(x or 0)
R=list(csv.DictReader(open('meta_dma.csv',encoding='utf-8-sig')))
mk=collections.defaultdict(lambda:{'spend':0,'imp':0,'clicks':0,'ret':0})
for r in R:
    a=mk[r['Comscore Markets']]; s=f(r['Amount spent (USD)']); a['spend']+=s; a['imp']+=f(r['Impressions']); a['clicks']+=f(r['Link clicks'])
    if 'retarget' in r['Campaign name'].lower(): a['ret']+=s
TOT=sum(v['spend'] for v in mk.values())
# new signups Jan1 - Oct5
new=collections.Counter()
for fn in ['prod_q1.json','prod_q2.json','prod_jul_oct5.json']:
    for r in json.load(open(fn))['rows']:
        m=metro_of(r['name'])
        if m: new[m]+=r['first_time_orders'] or 0
U=json.load(open('utm_metro.json'))
def utm(metros):
    c=collections.Counter()
    for m in metros:
        for v in U.get(m,{}).values(): c.update(v)
    return c
# account-level scale: Meta-reported purchases / Meta-tagged league orders (Q1-Q3)
metaRep=sum(sum(r['purchases'] or 0 for r in json.load(open(f'ads_{q}.json'))['rows']) for q in ['q1','q2','q3'])
metaUtm=sum(v.get('meta',0) for mm in U.values() for v in mm.values())
SCALE=metaRep/metaUtm
print('meta reported',metaRep,'meta utm',metaUtm,'scale',round(SCALE,2))
rows=[];mapped=set()
for d,ms in DMA.items():
    a=mk.get(d); 
    if not a: continue
    mapped.add(d); n=sum(new[m] for m in ms); c=utm(ms); tot=sum(c.values()) or 1
    share=c['meta']/tot; est=n*min(1,share*SCALE)
    rows.append({'dma':d,'metros':ms,'spend':round(a['spend']),'imp':int(a['imp']),'clicks':int(a['clicks']),'ctr':a['clicks']/a['imp'] if a['imp'] else None,
                 'new':n,'metaShare':round(share,4),'utmOrders':sum(c.values()),'cacFloor':round(a['spend']/n,2) if n else None,
                 'estMetaNew':round(est,1),'cacEst':round(a['spend']/est,2) if est else None,'retShare':a['ret']/a['spend'] if a['spend'] else 0})
unm={k:round(v['spend']) for k,v in mk.items() if k not in mapped}
print('unmapped spend',sum(unm.values()),'of',round(TOT),'; Unknown',unm.get('Unknown'),'; other',sum(v for k,v in unm.items() if k!='Unknown'))
fl=sorted([r['cacFloor'] for r in rows if r['cacFloor'] and r['spend']>=5000]); es=sorted([r['cacEst'] for r in rows if r['cacEst'] and r['spend']>=5000])
import statistics as st
print('median floor',st.median(fl),'median est',st.median(es))
print(f"{'market':32}{'spend':>9}{'new':>6}{'floor':>8}{'meta%':>7}{'est':>8}{'ctr':>7}")
for r in sorted(rows,key=lambda r:(r['cacEst'] or 9e9)):
    if r['spend']<3000: continue
    print(f"{r['dma'][:32]:32}{r['spend']:>9,}{r['new']:>6}{r['cacFloor'] or 0:>8.0f}{r['metaShare']:>7.0%}{r['cacEst'] or 0:>8.0f}{(r['ctr'] or 0)*100:>6.2f}%")
json.dump({'rows':rows,'scale':SCALE,'total':TOT,'unknown':unm.get('Unknown',0),'otherUnmapped':sum(v for k,v in unm.items() if k!='Unknown')},open('dma_cac.json','w'))

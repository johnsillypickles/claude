import json,statistics as st,io,contextlib
with contextlib.redirect_stdout(io.StringIO()):
    import build_scorer as B   # reuse zips + trends bundle
D=json.load(open('viab3.json'));M=json.load(open('viab_final.json'))
W={'y_per':25,'nkids':25,'trends':20,'y_share':15,'movers':10,'density':5}
ref={k:sorted(d[k] for d in D if d.get(k) is not None) for k in W}
def pct(k,x):
    if x is None: return 50
    v=ref[k];return 100*(sum(y<x for y in v)+.5*sum(y==x for y in v))/len(v)
for d in D: d['vs']=sum(W[k]*pct(k,d[k])/100 for k in W)
bands=[]
for a,b in [(0,35),(35,55),(55,65),(65,101)]:
    L=[d for d in D if a<=d['vs']<b];S1=[d for d in L if d['sn']==1]
    bands.append(dict(a=a,b=min(b,100),n=len(L),healthy=sum(d['fill']>=.8 for d in L),fill=round(st.median(d['fill'] for d in L),3),hit30=sum(d['players']>=30 for d in L),s1n=len(S1),s1h=sum(d['fill']>=.8 for d in S1)))
E=[d for d in D if d['price'] and d['cost']];ph=sorted(d['price']/(d['weeks'] or 8) for d in E);co=sorted(d['cost'] for d in E)
econ=dict(pph=4.2,margin=.55,price_hr_p10=round(ph[len(ph)//10],1),price_hr_med=round(ph[len(ph)//2],1),price_hr_p90=round(ph[9*len(ph)//10],1),cost_med=co[len(co)//2],n=len(E))
own=[[d['lat'],d['lng'],d['name'].split(' at ')[-1].split(' |')[0]] for d in D if d['season']=='Fall 2026']
out=dict(W=W,ref=ref,bands=bands,econ=econ,pts=[[round(d['vs'],1),int(d['fill']>=.8)] for d in D],own=own,n=len(D),
         zips=json.load(open('scorer_data.json'))['zips'],trends=json.load(open('scorer_data.json'))['trends'])
open('scorer_data2.json','w').write(json.dumps(out,separators=(',',':')))
print(bands,econ,len(own))
# python reference scores for parity check
import venue_features as vf, score_site as S
from geo import hav
for z in ['94928','11211','75024','60614','60035']:
    lat,lng,_=vf.ZXY[z];f=vf.feat(lat,lng);on=sum(1 for o in own if hav(lat,lng,o[0],o[1])<=7);t=S.nearest_trends(lat,lng)[1]
    c=dict(y_per=f['y25_39']/(1+on),nkids=-(f['kids_per_y'] or 0),trends=t,y_share=f['y_share'],movers=f['movers'],density=f['density'])
    print(z,round(sum(W[k]*pct(k,c[k])/100 for k in W),1))

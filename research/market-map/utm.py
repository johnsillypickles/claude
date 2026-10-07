import json,sys,collections
sys.path.insert(0,'.')
from metros import metro_of
def bucket(s):
    s=(s or '').lower()
    if s in('facebook','meta_ads','ig','fb','{{site_source_name}}','th'): return 'meta'   # th = threads placement (assumed)
    if s.startswith('google_ads'): return 'google'
    if s=='tiktok': return 'tiktok'
    if s=='': return 'none'
    if s in('klaviyo','abandoned_cart','activecampaign','email','hs_email'): return 'email'
    if s in('bixaffiliate','affiliate','influencer','partnership'): return 'affiliate'
    return 'other'
Q=['q1','q2','q3']
agg={q:collections.defaultdict(collections.Counter) for q in Q}
tot={q:collections.Counter() for q in Q}
for q in Q:
    for prod,src,n in json.load(open(f'utm_{q}.json'))['rows']:
        n=int(n); m=metro_of(prod)
        if not m or n<=0: continue
        b=bucket(src); agg[q][m][b]+=n; tot[q][b]+=n
for q in Q:
    t=tot[q]; s=sum(t.values()); print(q,'league orders',s,{k:f"{v} ({v/s:.0%})" for k,v in t.most_common()})
out={}
for q in Q:
    for m,c in agg[q].items():
        out.setdefault(m,{})[q]=dict(c)
json.dump(out,open('utm_metro.json','w'))
# 3-quarter summary
rows=[]
for m,qq in out.items():
    c=collections.Counter()
    for v in qq.values(): c.update(v)
    s=sum(c.values()); paid=c['meta']+c['google']+c['tiktok']
    rows.append((m,s,paid/s,c['meta']/s,c['none']/s,c['email']/s))
print(f"\n{'metro':24}{'orders':>7}{'paid%':>7}{'meta%':>7}{'none%':>7}{'email%':>7}")
for r in sorted(rows,key=lambda r:-r[1])[:45]: print(f"{r[0]:24}{r[1]:>7}{r[2]:>7.0%}{r[3]:>7.0%}{r[4]:>7.0%}{r[5]:>7.0%}")

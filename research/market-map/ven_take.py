import json,re,sys
F=sys.argv[1]; d=json.load(open(F))['data']['products']
out=open('venues.jsonl','a')
for n in d['nodes']:
    import html as _h
    desc=n.get('description') or re.sub(r'<[^>]+>',' ',_h.unescape(n.get('descriptionHtml') or ''))
    desc=re.sub(r'\s+',' ',desc)
    m=re.search(r'Location:\s*(.*?)(?:Start date|Start Date|Dates?:|Time:|Timing:|📅|Schedule|$)',desc)
    loc=m.group(1).strip() if m else ''
    z=re.findall(r'\b(\d{5})\b',loc) or re.findall(r'\b(\d{5})\b',desc[:600])
    tm=re.search(r'(?:Time|Timing):\s*(.{0,80}?)(?:End date|End Date|You can|You.ll play|\.|$)',desc)
    out.write(json.dumps({'title':n['title'],'vendor':n['vendor'],'tags':n['tags'],'loc':loc[:200],'zip':z[-1] if z else None,'time':tm.group(1).strip() if tm else ''})+'\n')
print(len(d['nodes']),'next' if d['pageInfo']['hasNextPage'] else 'END',d['pageInfo']['endCursor'])

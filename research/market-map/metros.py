import re
# city prefix (lowercased, normalized) -> metro (CBSA-style short name)
M = {
 'albuquerque':'Albuquerque, NM','allen':'Dallas-Fort Worth, TX','plano':'Dallas-Fort Worth, TX','grand prairie':'Dallas-Fort Worth, TX',
 'grapevine':'Dallas-Fort Worth, TX','farmers branch':'Dallas-Fort Worth, TX','dallas':'Dallas-Fort Worth, TX','dallas-ft. worths':'Dallas-Fort Worth, TX',
 'atlanta':'Atlanta, GA','austin':'Austin, TX','avon lake':'Cleveland, OH','cleveland':'Cleveland, OH',
 'baton rouge':'Baton Rouge, LA','walker':'Baton Rouge, LA','boston':'Boston, MA','hyde park':'Boston, MA','norwell':'Boston, MA',
 'brooklyn':'New York, NY','englewood':'New York, NY','wayne':'New York, NY','cedar knolls':'New York, NY','watchung':'New York, NY',
 'stamford':'Bridgeport-Stamford, CT','rochester':'Rochester, NY','buffalo':'Buffalo, NY',
 'calabasas':'Los Angeles, CA','carson':'Los Angeles, CA','fountain valley':'Los Angeles, CA','el segundo':'Los Angeles, CA',
 'los angeles':'Los Angeles, CA','santa monica':'Los Angeles, CA','socal':'Los Angeles, CA','corona':'Riverside, CA',
 'spring valley':'San Diego, CA','san diego':'San Diego, CA','san francisco':'San Francisco, CA','fresno':'Fresno, CA',
 'calgary':'Calgary, AB','kingston':'Kingston, ON','toronto':'Toronto, ON','vaughan':'Toronto, ON','vancouver':'Vancouver, BC','hamilton, canada':'Hamilton, ON',
 'centerville':'Dayton, OH','cincinnati':'Cincinnati, OH','columbus':'Columbus, OH','westerville':'Columbus, OH','sandusky':'Sandusky, OH',
 'chandler':'Phoenix, AZ','glendale':'Phoenix, AZ','mesa':'Phoenix, AZ','phoenix':'Phoenix, AZ','tempe':'Phoenix, AZ',
 'charleston':'Charleston, SC','mt pleasant':'Charleston, SC','charlotte':'Charlotte, NC','charlottesville':'Charlottesville, VA','mauldin':'Greenville, SC',
 'chicago':'Chicago, IL','highland park':'Chicago, IL','naperville':'Chicago, IL','north aurora':'Chicago, IL','waukegan':'Chicago, IL','mundelein':'Chicago, IL','dinx social club':'Chicago, IL',
 'colorado springs':'Colorado Springs, CO','denver':'Denver, CO','thornton':'Denver, CO','river point':'Denver, CO',
 'columbia':'Baltimore, MD','white marsh':'Baltimore, MD','finksburg':'Baltimore, MD',
 'darling harbour':'Sydney, AUS','seven hills':'Sydney, AUS','sydney':'Sydney, AUS','melbourne':'Melbourne, AUS',
 'des moines':'Des Moines, IA','eagan':'Minneapolis, MN','plymouth':'Minneapolis, MN','minneapolis':'Minneapolis, MN','minnesota':'Minneapolis, MN',
 'evansville':'Evansville, IN','fishers':'Indianapolis, IN','greenwood':'Indianapolis, IN','indianapolis':'Indianapolis, IN',
 'fort lauderdale':'Miami, FL','ft. lauderdale':'Miami, FL','miami':'Miami, FL',
 'grand rapids':'Grand Rapids, MI','kalamazoo':'Kalamazoo, MI','west bloomfield':'Detroit, MI',
 'greater philadelphia':'Philadelphia, PA','philadelphia':'Philadelphia, PA','norristown':'Philadelphia, PA','plymouth meeting':'Philadelphia, PA',
 'moorestown':'Philadelphia, PA','greater wilmington':'Philadelphia, PA','newport':'Philadelphia, PA',
 'hamilton':'Trenton, NJ','whitehall':'Allentown, PA','henderson':'Las Vegas, NV','las vegas':'Las Vegas, NV',
 'hendersonville':'Nashville, TN','nashville':'Nashville, TN','knoxville':'Knoxville, TN','lexington':'Lexington, KY','louisville':'Louisville, KY',
 'holly hill':'Daytona Beach, FL','holyoke':'Springfield, MA','manchester':'Hartford, CT','portland, me':'Portland, ME','south portland':'Portland, ME',
 'houston':'Houston, TX','webster':'Houston, TX','san antonio':'San Antonio, TX',
 'jacksonville':'Jacksonville, FL','orange park':'Jacksonville, FL','kissimmee':'Orlando, FL','orlando':'Orlando, FL','ocala':'Ocala, FL',
 'tampa':'Tampa, FL','pinellas park':'Tampa, FL','st petersburg':'Tampa, FL',
 'kansas city':'Kansas City, MO','north kansas city':'Kansas City, MO','overland park':'Kansas City, MO',
 'st charles':'St. Louis, MO','st. charles':'St. Louis, MO','madison':'Madison, WI','south milwaukee':'Milwaukee, WI',
 'meridian':'Boise, ID','nampa':'Boise, ID','new orleans':'New Orleans, LA','oklahoma city':'Oklahoma City, OK',
 'pittsburgh':'Pittsburgh, PA','portland, or':'Portland, OR','clackamas':'Portland, OR','troutdale':'Portland, OR','tualatin':'Portland, OR',
 'raleigh':'Raleigh, NC','salt lake city':'Salt Lake City, UT','sandy':'Salt Lake City, UT','seattle':'Seattle, WA',
 'washington dc':'Washington, DC','washington':'Washington, DC','chicago il':'Chicago, IL','washington, dc':'Washington, DC','wichita':'Wichita, KS','winston-salem':'Winston-Salem, NC','winston salem':'Winston-Salem, NC',
 'harrisonburg':'Harrisonburg, VA','fort wayne':'Fort Wayne, IN','little rock':'Little Rock, AR',
}
STATE_HINT={'portland':{'ME':'portland, me','OR':'portland, or'},'hamilton':{'Canada':'hamilton, canada','NJ':'hamilton'}}
def metro_of(name):
    n=re.sub(r'^OLD\s+','',name.strip())
    low=n.lower()
    # campaign-style names
    if low.startswith('w26_phase2leagues - houston'): return 'Houston, TX'
    if low.startswith('w26_phase2leagues - socal'): return 'Los Angeles, CA'
    if 'volleyball-chicago' in low or low.startswith('chicago spf'): return 'Chicago, IL'
    m=re.match(r'sumr26_phase0-(dallas-ft\._worths|denver|minnesota|dinx_social_club)_leagues',low)
    if m: return {'dallas-ft._worths':'Dallas-Fort Worth, TX','denver':'Denver, CO','minnesota':'Minneapolis, MN','dinx_social_club':'Chicago, IL'}[m.group(1)]
    if re.match(r'(fort wayne|little rock)_leadform',low): return M[low.split('_')[0]]
    m=re.match(r'^(?:all\s+)?([^:|_(]+?)(?:\s*\([A-Z]{2}\))?\s*(?::|leagues|league|\|)',n,re.I)
    if not m: return None
    city=m.group(1).strip()
    parts=[p.strip() for p in city.split(',')]
    c=parts[0].lower().replace('cIty','city')
    st=parts[1] if len(parts)>1 else ''
    if c in STATE_HINT:
        for k,v in STATE_HINT[c].items():
            if k.lower() in st.lower(): return M[v]
    if c=='glendale' and st and st!='AZ': return None
    if c=='columbia' and st!='MD': return None
    return M.get(c)

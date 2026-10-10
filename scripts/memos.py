import urllib.request,json,re,concurrent.futures,pathlib
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from collect import fetch
R=pathlib.Path(__file__).resolve().parents[1]
indexes=['https://www.whitehouse.gov/omb/information-for-agencies/memoranda/','https://bidenwhitehouse.archives.gov/omb/information-for-agencies/memoranda/','https://trumpwhitehouse.archives.gov/omb/information-for-agencies/memoranda/','https://obamawhitehouse.archives.gov/omb/memoranda_default','https://georgewbush-whitehouse.archives.gov/omb/memoranda/','https://clintonwhitehouse3.archives.gov/OMB/memoranda/index.html']
items={}; logs=[]
for url in indexes:
 try:
  b=urllib.request.urlopen(url,timeout=40).read(); soup=BeautifulSoup(b,'html.parser'); count=0
  (R/'data'/('index-'+str(len(logs))+'.html')).write_bytes(b)
  for a in soup.find_all('a',href=True):
   title=a.get_text(' ',strip=True); href=urljoin(url,a['href']); m=re.search(r'\b[Mm][‐‑–-]?(\d{2})[‐‑–-](\d{2})\b',title+' '+href)
   if not m: m=re.search(r'/m(\d{2})(\d{2})\.(?:pdf|html)',href,re.I)
   if m and ('.pdf' in href or '.html' in href):
    id=f'm-{m[1]}-{m[2]}'; count+=1
    if id not in items: items[id]=dict(id=id,date=('19' if int(m[1])>70 else '20')+m[1]+'-01-01',date_precision='fiscal-year label; exact date in original',title=title or id.upper(),type='OMB memorandum',url=href,locator='Full text; A-130 reference',relation='Explicit OMB direction',note='Archive-index candidate; relevance requires full-text match.')
  logs.append(dict(url=url,candidates=count,status='searched'))
 except Exception as e: logs.append(dict(url=url,status=str(e)))
print('Candidates',len(items),flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
 results=list(pool.map(fetch,items.values()))
(R/'data/memo-candidates.json').write_text(json.dumps(results,indent=2))
(R/'data/search-log.json').write_text(json.dumps(logs,indent=2))
selected=[r for r in results if r.get('a130_reference')]
(R/'data/memos.json').write_text(json.dumps(selected,indent=2))
print('Downloaded',sum(r['availability']=='downloaded' for r in results),'A130 references',len(selected),flush=True)
for r in selected: print(r['id'],r['title'])

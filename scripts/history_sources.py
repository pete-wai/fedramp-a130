"""Preserved originals for the chronological information/security report."""
from pathlib import Path
import json, re
R=Path(__file__).resolve().parents[1]
S=R/'site/on-behalf'
records={r['id']:r for r in json.loads((R/'data/records.json').read_text())}
sources={r['id']:r.copy() for r in json.loads((R/'data/on-behalf/retained-sources.json').read_text())['sources']}
for name in ['new-sources.json','history-web-sources.json']:
    for r in json.loads((R/'data/on-behalf'/name).read_text()):
        if r.get('local'):sources[r['id']]=r.copy()
for r in json.loads((R/'data/on-behalf/history-acquisitions.json').read_text()):
    sources[r['id']]=dict(id=r['id'],title=str(r.get('document_number','NIST'))+' — '+r['title'],date=r['date'],kind='NIST guidance',url=r['url'],local='sources/'+r['id']+'.pdf',sha256=r['sha256'],retrieved=r.get('retrieved_at','2026-10-25')[:10],provenance='Original located through Inforegs; copied and SHA-256 checked 2026-10-25. '+r.get('status','')+'. '+str(r.get('notes','')))
def source(id):
    if id not in sources:
        r=records[id]
        kind='NIST guidance' if r['type']=='NIST' else 'Law' if r['type']=='Law' else r['type']
        sources[id]=dict(id=id,title=r['title'],date=r['date'],kind=kind,url=r['url'],local='../'+r['local'],sha256=r['sha256'],retrieved=r['retrieved'],provenance=r['status'])
    return sources[id]
for id in ['fips199','fips200']:source(id)['kind']='Mandatory standard'
for id in ['pra1980','pra1995','csa','gisra','fisma2002','fisma2014','fedramp-act']:source(id)['kind']='Law'
for id in ['a130-1993','a130-1996','a130-2000','a130-2000-app-iii','a130-2016','m-10-15','fedramp2011','m-24-15']:source(id)['kind']='OMB policy'
for id,date in [('sp800372','2018-12-20'),('sp8001713','2024-05-14'),('fips200','2006-03-09')]:source(id)['date']=date
def norm(t):
    # Reflow extraction only: retain wording and paragraph/section markers.
    t=t.replace('\u00ad','')
    t=re.sub(r'(agency|non|organization)-\s*\n\s*',r'\1-',t)
    t=re.sub(r'(?<=\w)-\s*\n\s*(?=\w)','',t)
    t=re.sub(r'\s+([,.;:])',r'\1',t)
    return re.sub(r'\s+',' ',t).strip()

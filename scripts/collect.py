import json, pathlib, urllib.request, concurrent.futures, hashlib, re, datetime, io
from pypdf import PdfReader
from bs4 import BeautifulSoup
ROOT=pathlib.Path(__file__).resolve().parents[1]; OUT=ROOT/'site/sources'; OUT.mkdir(parents=True,exist_ok=True)
def fetch(item):
    item=dict(item); path=OUT/(item['id']+('.pdf' if '.pdf' in item['url'].lower() else '.html'))
    try:
        if path.exists(): b=path.read_bytes()
        else:
            req=urllib.request.Request(item['url'],headers={'User-Agent':'Mozilla/5.0 (primary-source research)'})
            with urllib.request.urlopen(req,timeout=45) as r: b=r.read(); item['resolved_url']=r.url
            if b[:4]!=b'%PDF' and path.suffix=='.pdf': raise ValueError('Not a PDF')
            path.write_bytes(b)
        if b[:4]==b'%PDF':
            reader=PdfReader(io.BytesIO(b)); pages=[p.extract_text() or '' for p in reader.pages]; item['pages']=len(pages)
            text='\n'.join(f'\n[PDF page {i+1}]\n{t}' for i,t in enumerate(pages))
        else:
            soup=BeautifulSoup(b,'html.parser')
            for el in soup(['script','style','nav','header','footer']): el.decompose()
            text=soup.get_text(' ',strip=True); pages=[text]
        (OUT/(item['id']+'.txt')).write_text(text)
        item.update(local='sources/'+path.name,extracted='sources/'+item['id']+'.txt',sha256=hashlib.sha256(b).hexdigest(),bytes=len(b),retrieved='2026-10-10',availability='downloaded',text_quality='searchable' if len(text.strip())>250 else 'scan; text unreliable')
        item['matches']=[]
        patterns={'cloud':r'\bcloud\b','commercial services':r'\bcommercial\s+services\b','FedRAMP':r'\bFedRAMP\b','related terminology':r'commercial\s+(?:providers|sources|off.the.shelf)|external\s+services|contractor.operated'}
        for tag,pat in patterns.items():
            for i,p in enumerate(pages):
                m=re.search(pat,p,re.I)
                if m:
                    item['matches'].append({'term':tag,'locator':f'PDF page {i+1}' if path.suffix=='.pdf' else 'HTML text','passage':re.sub(r'\s+',' ',p[max(0,m.start()-160):m.end()+240]),'verification':'extracted candidate'}); break
        item['a130_reference']=bool(re.search(r'A[‐‑–−-]?\s*130',text,re.I))
    except Exception as e: item.update(availability='unavailable',limitation=str(e))
    return item
if __name__=='__main__':
    seeds=json.loads((ROOT/'data/seeds.json').read_text())
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
        results=list(pool.map(fetch,seeds))
    (ROOT/'data/manifest.json').write_text(json.dumps(results,indent=2))
    for r in results: print(r['id'],r['availability'],r.get('pages','HTML'),r.get('limitation',''))

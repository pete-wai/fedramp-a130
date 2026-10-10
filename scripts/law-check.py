"""Source fidelity, coverage, links, provenance, and known historical edge cases."""
import json,pathlib,hashlib,zipfile,xml.etree.ElementTree as E,re,sys
from bs4 import BeautifulSoup
R=pathlib.Path(__file__).resolve().parents[1];S=R/'site';D=R/'data/law';N='{http://xml.house.gov/schemas/uslm/1.0}'
sections=json.loads((D/'sections.json').read_text());sources=json.loads((D/'sources.json').read_text());fail=[];norm=lambda x:' '.join(x.split())
def check(ok,message):
 if not ok:fail.append(message)
for src in sources:
 p=S/src['file'];check(p.exists(),src['file'])
 check(hashlib.sha256(p.read_bytes()).hexdigest()==src['sha256'],'hash '+src['id'])
 check(b'Page Not Found' not in p.read_bytes(),'error page '+src['id'])
# Selected XML must be an exact serialization of a section from the preserved title archive.
for t in {s['title'] for s in sections}:
 root=E.fromstring(zipfile.ZipFile(S/f'sources/law/title{t}.zip').read(f'usc{t:02}.xml'))
 for rec in [s for s in sections if s['title']==t]:
  original=root.find(f'.//{N}section[@identifier="{rec["identifier"]}"]')
  saved=E.parse(D/rec['xml']).getroot()
  original.tail=None
  check(E.tostring(original)==E.tostring(saved),'XML fidelity '+rec['id'])
 for ch in [35,36] if t==44 else []:
  want={s.get('identifier') for s in root.find(f'.//{N}chapter[@identifier="/us/usc/t44/ch{ch}"]').iter(N+'section') if s.get('identifier')}
  got={s['identifier'] for s in sections if s['chapter']==ch};check(want==got,'Chapter coverage '+str(ch))
cache={}
def soup(p):
 if p not in cache:cache[p]=BeautifulSoup(p.read_text(),'html.parser')
 return cache[p]
files=list((S/'law').glob('*.html'))+list((S/'a130').glob('*.html'))
links=0
for p in files:
 doc=soup(p);ids=[x['id'] for x in doc.select('[id]')];check(len(ids)==len(set(ids)),'duplicate ids '+p.name)
 check(not doc.select('script[src^="http"],link[href^="http"]'),'network dependency '+p.name)
 for a in doc.select('[href],[src]'):
  u=a.get('href') or a.get('src')
  if not u or u.startswith(('http:','https:','mailto:')):continue
  local,_,frag=u.partition('#');target=(p.parent/local).resolve() if local else p.resolve()
  check(target.exists(),f'{p.name}: missing {u}')
  if target.exists() and frag and target.suffix=='.html':check(soup(target).find(id=frag) is not None,f'{p.name}: missing anchor {u}')
  links+=1
# Extract all visible original text, excluding authored context; compare with XML text.
for rec in sections:
 root=E.parse(D/rec['xml']).getroot();doc=soup(S/f'law/{rec["id"]}.html')
 def source_content(x):
  return ''.join(x.itertext())
 expected=''.join(source_content(x) for x in root if x.tag.split('}')[-1] not in ['num','heading','sourceCredit','notes'])
 actual=BeautifulSoup(str(doc.select_one('#text .legal-text')),'html.parser')
 for x in actual.select('.clause-context'):x.decompose()
 # Rendering adds separation between semantic blocks. Compare characters except whitespace.
 compact=lambda s:re.sub(r'\s+','',s)
 check(compact(expected)==compact(actual.get_text()),'Rendered law text fidelity '+rec['id'])
# Exact A-130 source chunk sequence and stable source body.
original=soup(S/'read/a130-2016.html');els=original.select('.source-page h2,.source-page h3,.source-page p');start=next(i for i,x in enumerate(els) if x.get('id')=='section-1')
expected=[x.get_text() for x in els[start:]]
entries=json.loads((S/'a130/expectations.json').read_text());actual=[s for x in entries for s in x['source_text'].split('\n')]
# Paragraphs can contain line breaks, so compare the joined content rather than list length.
check(norm('\n'.join(expected))==norm('\n'.join(actual)),'A130 complete source coverage')
check('§3555' in (S/'law/oversight.html').read_text(),'IG guide')
check('December 23, 2027' in (S/'law/44-3607.html').read_text(),'FedRAMP future repeal')
check('December 11, 2026' in (S/'law/6-1525.html').read_text(),'DHS sunset')
check('chapter 4 of title 5' in (S/'law/44-3555.html').read_text(),'IG recodification')
check('3535' in (S/'law/history-44-3555.html').read_text(),'GISRA predecessor')
check('3545' in (S/'law/history-44-3555.html').read_text(),'FISMA2002 predecessor')

sys.path.insert(0,str(R/'scripts'))
from law_content import CLAUSES
from lineage import LINEAGE
provisions={x['id'] for x in json.loads((S/'law/provisions.json').read_text())}
for key in CLAUSES:check(key in provisions,'Unresolved commentary locator '+key)
for key in LINEAGE:check(key in provisions or key in {s['id'] for s in sections},'Unresolved lineage locator '+key)

report=dict(pages=len(files),sections=len(sections),sources=len(sources),links=links,failures=fail,passed=not fail)
(R/'output').mkdir(exist_ok=True)
(R/'output/law-static-check.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2));sys.exit(bool(fail))

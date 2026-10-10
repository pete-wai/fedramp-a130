"""Build the offline statutory reader from preserved OLRC XML and authored commentary."""
from pathlib import Path
import xml.etree.ElementTree as ET
import json,re,html,hashlib,difflib,copy
from bs4 import BeautifulSoup
from law_content import SECTIONS,CLAUSES,LAW_NAMES,MATERIALS
from a130_content import A130
from lineage import LINEAGE
R=Path(__file__).resolve().parents[1];S=R/'site';D=R/'data/law';L=S/'law';L.mkdir(exist_ok=True)
N='{http://xml.house.gov/schemas/uslm/1.0}'
e=lambda x:html.escape(str(x),quote=True)
plain=lambda x:''.join(x.itertext()) if x is not None else ''
normalize=lambda x:' '.join(x.split())
records={x['id']:x for x in json.loads((R/'data/records.json').read_text())}
sections=json.loads((D/'sections.json').read_text());by={x['id']:x for x in sections}
sources=json.loads((D/'sources.json').read_text());sourceby={x['id']:x for x in sources}
TAG=lambda x:x.tag.split('}')[-1]
STRUCT={'subsection','paragraph','subparagraph','clause','subclause','item','subitem'}
roots={x['id']:ET.parse(D/x['xml']).getroot() for x in sections}
nodekeys={};nodeids={};clauses=[]
def key_for(identifier):
 m=re.match(r'/us/usc/t(\d+)/s([^/]+)(.*)',identifier)
 if m:return f'{m[1]}-{m[2]}'.replace('–','-').replace('...','-to-')+m[3]
def anchor(k):return 'p-'+re.sub('[^a-zA-Z0-9-]','-',k.replace('~','-occurrence-'))
for rec in sections:
 seen={}
 def register(x,parent_suffix=None):
  ident=x.get('identifier','');key=key_for(ident)
  if key and (TAG(x) in STRUCT or TAG(x)=='section'):
   seen[ident]=seen.get(ident,0)+1
   if parent_suffix:
    old,new=parent_suffix;key=key.replace(old,new,1)
   elif seen[ident]>1:
    old=key;key+='~'+str(seen[ident]);parent_suffix=(old,key)
   nodekeys.setdefault(ident,key);nodeids[x]=key
  for c in x:register(c,parent_suffix)
 register(roots[rec['id']])

def lineage_html(key):
 item=LINEAGE.get(key)
 if not item:return ''
 out='<div class="duty-lineage"><h3>'+e(item['title'])+'</h3><p class="meta">Statutory origin: <strong>'+e(item['origin'])+'</strong> · Enacted '+item['date']+'</p><p>'+e(item['text'])+'</p><p><a href="'+item['source']+'">'+e(item['locator'])+'</a></p>'
 if item['events']:
  out+='<ol class="lineage-events">'
  for date,kind,text,url in sorted(item['events']):out+='<li><span class="law-label">'+e(kind)+'</span> '+date+' — '+e(text)+' <a href="'+url+'">Source</a></li>'
  out+='</ol>'
 return out+'</div>'

def href_us(h):
 key=key_for(h)
 if key and key.split('/')[0] in by:
  section=key.split('/')[0]
  return section+'.html'+('#'+anchor(key) if h in nodekeys else '')
 if h.startswith('/us/usc/'):
  parts=h.split('/');title=parts[3][1:];sec=next((p[1:] for p in parts[4:] if p.startswith('s') and not p.startswith(('sch','st'))),None)
  req=f'granuleid:USC-prelim-title{title}'+(f'-section{sec}' if sec else '')
  return 'https://uscode.house.gov/view.xhtml?req='+req+'&edition=prelim'
 m=re.match(r'/us/pl/(\d+)/(\d+)',h)
 if m:
  f=f'pl-{m[1]}-{m[2]}.html'
  if (S/'sources/law'/f).exists():return '../sources/law/'+f
  return f'https://www.govinfo.gov/link/plaw/{m[1]}/public/{m[2]}'
 m=re.match(r'/us/stat/(\d+)/(\d+)',h)
 if m:return f'https://www.govinfo.gov/link/statute/{m[1]}/{m[2]}'
 return 'https://uscode.house.gov'+h if h.startswith('/') else h

def mixed(x,ctx=''):
 out=e(x.text or '')
 for c in x:
  out+=xml(c,ctx)+(e(c.tail or ''))
 return out

def xml(x,ctx='',controls=False):
 tag=TAG(x);key=nodeids.get(x);nid=x.get('id');ident=x.get('identifier')
 attrs=f' id="{anchor(key)}"' if key else (f' id="src-{e(ctx)}-{e(nid)}"' if nid else '')
 if tag=='ref':
  if x.get('href'):return f'<a href="{e(href_us(x.get("href")))}">{mixed(x,ctx)}</a>'
  if x.get('idref'):return f'<a href="#src-{e(ctx)}-{e(x.get("idref"))}" class="source-footnote">{mixed(x,ctx)}</a>'
  return mixed(x,ctx)
 if tag in STRUCT:
  core=''.join(xml(c,ctx,controls) for c in x)
  more=''
  if controls and key:
   own=CLAUSES.get(key)
   more=f'<details class="clause-context"><summary>Context and history: {e(label(key))}</summary>'
   if own:more+=f'<h3>{e(own[0])}</h3><p>{e(own[1])}</p>'
   more+=lineage_html(key)
   more+=f'<p><a href="#history">Section history and amendment instructions</a> · <a href="history-{e(ctx)}.html#clause-history">Compare earlier editions</a> · <a href="#{anchor(key)}">Link to this provision</a></p>'
   notes=amendments_for(roots[ctx],key)
   if notes:more+='<p class="meta">Office of the Law Revision Counsel — amendment notes</p>'+''.join('<p>'+e(n)+'</p>' for n in notes)
   more+='</details>'
   clauses.append(dict(id=key,section=ctx,locator=label(key),text=normalize(source_text(x)),parent=key.rsplit('/',1)[0],url=f'law/{ctx}.html#{anchor(key)}'))
  return f'<div class="legal-unit"{attrs}>'+core+more+'</div>'
 if tag=='num':return '<span class="legal-num">'+mixed(x,ctx)+'</span> '
 if tag=='heading':return '<h3 class="legal-heading">'+mixed(x,ctx)+'</h3>'
 if tag in ['content','chapeau','continuation','p']:return f'<p{attrs}>'+mixed(x,ctx)+'</p>'
 if tag=='note':
  if x.get('type')=='footnote':return f'<aside class="source-note"{attrs}>'+mixed(x,ctx)+'</aside>'
  return f'<div class="code-note"{attrs}>'+mixed(x,ctx)+'</div>'
 if tag=='notes':return mixed(x,ctx)
 if tag=='sourceCredit':return '<p class="source-credit">'+mixed(x,ctx)+'</p>'
 if tag in ['b','i','sup','sub']:return f'<{tag}>'+mixed(x,ctx)+f'</{tag}>'
 if tag=='table':return '<div class="table-wrap"><table>'+mixed(x,ctx)+'</table></div>'
 if tag in ['thead','tbody','tr','th','td']:return f'<{tag}>'+mixed(x,ctx)+f'</{tag}>'
 if tag in ['toc','layout']:return '<div class="code-index">'+mixed(x,ctx)+'</div>'
 if tag in ['tocItem','row']:return '<p>'+mixed(x,ctx)+'</p>'
 if tag=='column':return '<span>'+mixed(x,ctx)+'</span> '
 return mixed(x,ctx)

def source_text(x):
 # Editorial footnotes embedded in source clauses remain visible, but are not law text.
 y=copy.deepcopy(x)
 for parent in y.iter():
  for c in list(parent):
   if TAG(c) in ['note','notes','sourceCredit'] or TAG(c)=='ref' and c.get('class')=='footnoteRef':
    tail=c.tail or '';idx=list(parent).index(c)
    if idx:parent[idx-1].tail=(parent[idx-1].tail or '')+tail
    else:parent.text=(parent.text or '')+tail
    parent.remove(c)
 return plain(y)

def label(key):
 section,*path=key.split('/');r=by[section]
 return f'{r["title"]} USC {r["number"]}'+''.join('('+v.split('~')[0]+')' for v in path)+(' [second enacted subsection]' if any('~2' in v for v in path) else '')

def amendments_for(root,key):
 path=key.split('/')[1:]
 if not path:return []
 joined=''.join('('+p+')' for p in path)
 # Show source instructions at the containing subsection; do not infer clause provenance from these matches.
 matches=[]
 for n in root.findall(f'.//{N}note[@topic="amendments"]/{N}p'):
  txt=normalize(plain(n))
  if re.search(r'(?:Subsec|subsec)s?\.\s*\('+re.escape(path[0])+r'\)',txt) or joined in txt:matches.append(txt)
 return matches

def source_badges(rec):
 cr=roots[rec['id']].find(N+'sourceCredit');refs=[]
 if cr is not None:
  for x in cr.findall(N+'ref'):
   m=re.match(r'/us/pl/(\d+)/(\d+)',x.get('href',''))
   if m:
    law=f'{m[1]}-{m[2]}'
    if law not in refs:refs.append(law)
 return refs

def badges(rec):
 return ''.join(f'<span class="law-label law-{law.split("-")[0]}">{e(LAW_NAMES.get(law,"P.L. "+law))}</span>' for law in source_badges(rec))

def material_links(key):
 items=[]
 for rid,rel,loc in MATERIALS.get(key,[]):
  assert rid in records,rid
  r=records[rid];target='../'+r.get('reader',r.get('local','index.html#doc-'+rid))
  items.append(f'<li><strong>{e(rel)}</strong> — <a href="{e(target)}">{e(r["title"])}</a> ({e(loc)}). <a href="../index.html#doc-{rid}">Edition and source details</a></li>')
 if key=='44-3553':items.append('<li><strong>Operational implementation</strong> — <a href="https://www.cisa.gov/news-events/directives">CISA’s directive catalogue</a> lists binding operational and emergency directives with their individual scope and instructions.</li>')
 if key=='44-3555':items.append('<li><strong>Evaluation guidance</strong> — <a href="https://www.cisa.gov/topics/cyber-threats-and-advisories/federal-information-security-modernization-act">CISA’s FISMA resources</a> provides reporting guidance and metrics. Check the fiscal year of the instructions used for an evaluation.</li>')
 return '<h3>Policies and standards that carry this out</h3><ul>'+''.join(items)+'</ul>' if items else ''

def nav(current):
 entries=[('../index.html','Historical report'),('../law/index.html','Read the law'),('../a130/index.html','A-130 responsibilities'),('../law/history.html','How the law changed'),('../law/oversight.html','IGs and oversight'),('../law/sources.html','Coverage and sources')]
 return '<nav class="site-nav" aria-label="Main navigation">'+''.join(f'<a href="{url}"'+(' aria-current="page"' if name==current else '')+f'>{name}</a>' for url,name in entries)+'</nav>'

def page(file,title,intro,body,toc='',current='Read the law'):
 head=f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{e(title)} · A-130</title><link rel="stylesheet" href="../law/law.css"><script src="../law/law.js" defer></script></head><body><a class="skip" href="#main">Skip to content</a><header class="masthead"><a class="brand" href="../index.html">A–130 <span>Law, policy &amp; responsibility</span></a>{nav(current)}</header>'
 layout='<div class="reading-layout">'+(f'<aside class="contents"><details open><summary>On this page</summary><nav aria-label="Page sections">{toc}</nav></details></aside>' if toc else '')
 text=head+layout+f'<main id="main"><header class="page-title"><h1>{e(title)}</h1><div class="intro">{intro}</div></header>{body}</main></div><footer><p>U.S. Code snapshot: Public Law 119-118, September 30, 2026. Retrieved October 10, 2026. <a href="../law/sources.html">Coverage and source details</a>.</p><p>Original law and policy text is set apart from the explanations. Reading, citations, and comparisons work offline; official-source links require a connection.</p></footer></body></html>'
 (S/file).parent.mkdir(exist_ok=True,parents=True);(S/file).write_text(text)

def filters(items,extra=''):
 topics=sorted({t for x in items for t in x['topics']});actors=sorted({a for x in items for a in x['actors']})
 return '<form class="filters" role="search"><label>Find a provision<input id="query" type="search" placeholder="Section, phrase, duty, or law"></label>'+''.join(f'<label>{label}<select id="{kind}"><option value="">All {label.lower()}</option>'+''.join(f'<option>{e(v)}</option>' for v in values)+'</select></label>' for kind,label,values in [('topic','Topics',topics),('actor','Actors',actors)])+extra+'<button type="reset">Clear filters</button><p id="results" role="status" aria-live="polite"></p></form><p id="empty" hidden>No provisions match. Try another phrase or clear the filters.</p>'

# Each section remains a standalone, complete reading page; the chapter pages collect their full text.
chapter_bodies={35:[],36:[]};section_cards=[]
for rec in sections:
 key=rec['id'];root=roots[key];auth=SECTIONS[key];rtitle=f'{rec["title"]} USC §{rec["number"]} — {rec["heading"]}'
 intro=f'<p>{e(auth["summary"])}</p><p class="meta">'+e(' · '.join(auth['actors']))+'</p><div class="law-labels" aria-label="Laws listed in the section source credit">'+badges(rec)+'</div><p class="meta">Section source laws · <a href="history.html#'+key+'">Explore its earlier history</a>.</p>'
 if key=='44-3505':intro+='<p class="date-note">Congress enacted two subsections labeled (c). Both appear below, with separate links; the original numbering is retained.</p>'
 if key.startswith('44-36') and rec['number'].isdigit() and 3607<=int(rec['number'])<=3616:intro+='<p class="date-note">The source schedules repeal for December 23, 2027. These provisions remain in this September 2026 snapshot; see the effective-date note below.</p>'
 if key in ['6-663','6-1525']:intro+='<p class="date-note">The snapshot’s termination date for §663 authority and §1524(c) reporting is December 11, 2026. See <a href="6-1525.html">6 USC §1525</a>.</p>'
 intro+=lineage_html(key)
 source_body=''.join(xml(x,key,True) for x in root if TAG(x) not in ['num','heading','sourceCredit','notes'])
 body='<section id="text"><h2>Statutory text</h2><div class="legal-text" id="'+anchor(key)+'">'+source_body+'</div></section>'
 body+='<section id="history"><h2>Source credit and legislative history</h2><p class="meta">Official Code source credit and editorial notes. Statutory notes below reproduce additional enacted provisions; their individual dates and scope still apply.</p>'
 body+=''.join(xml(x,key) for x in root if TAG(x) in ['sourceCredit','notes'])+'</section>'
 body+=material_links(key)
 body+=f'<p><a href="https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title{rec["title"]}-section{e(rec["number"])}&amp;edition=prelim">Official Code section</a> · <a href="../sources/law/title{rec["title"]}.zip" download>Download official title XML</a></p>'
 toc='<a href="#text">Statutory text</a>'
 for x in root:
  if TAG(x) in STRUCT and x in nodeids:
   toc+=f'<a href="#{anchor(nodeids[x])}">{e(plain(x.find(N+"num")))} {e(plain(x.find(N+"heading")))}</a>'
 toc+='<a href="#history">History and source notes</a>'
 page('law/'+key+'.html',rtitle,intro,body,toc)
 if rec['chapter']:
  # Chapter text links to the complete section's notes and clause annotations; avoids repeated IDs.
  clean=''.join(xml(x,key,False) for x in root if TAG(x) not in ['num','heading','sourceCredit','notes'])
  chapter_bodies[rec['chapter']].append(f'<article class="chapter-section" id="{key}"><h2><a href="{key}.html">§{e(rec["number"])}. {e(rec["heading"])}</a></h2><p class="annotation">{e(auth["summary"])}</p><div class="legal-text">{clean}</div><p><a href="{key}.html#history">Amendments, statutory notes, and implementation links for §{e(rec["number"])}</a></p></article>')
 search=' '.join([key,label(key),rec['heading'],auth['summary'],normalize(source_text(root)),*source_badges(rec),*(LAW_NAMES.get(v,v) for v in source_badges(rec))])
 section_cards.append(f'<article class="search-item" data-topics="{e("|".join(auth["topics"]))}" data-actors="{e("|".join(auth["actors"]))}" data-search="{e(search)}"><h3><a href="{key}.html">{e(label(key))} — {e(rec["heading"])}</a></h3><p>{e(auth["summary"])}</p><div class="law-labels">{badges(rec)}</div></article>')
for ch,body in chapter_bodies.items():
 recs=[r for r in sections if r['chapter']==ch];toc=''.join(f'<a href="#{r["id"]}">§{r["number"]} {e(r["heading"])}</a>' for r in recs)
 context=ET.parse(D/f'chapter-{ch}.xml').getroot()
 body=''.join(body)+'<section id="chapter-notes"><h2>Chapter organization and source notes</h2>'+xml(context,'chapter-'+str(ch))+'</section>'
 page(f'law/chapter-{ch}.html',f'Title 44, chapter {ch}', '<p>Complete section text in Code order. Open a section for clause annotations, amendment instructions, statutory notes, and related policy.</p>',body,toc)
intro='<p class="meta">Code through September 30, 2026 · <a href="sources.html">Edition and coverage</a></p><p>Federal information-security duties come from several laws. The Paperwork Reduction Act assigns information-management responsibilities; the Federal Information Security Modernization Act (FISMA) specifies security programs and oversight; other statutes establish standards, operational powers, privacy safeguards, and cloud authorization.</p><p>Read the law in order or follow an agency responsibility. Each section keeps its original wording alongside a short explanation and legislative history.</p>'
body='<section class="start-reading"><h2>Read complete chapters</h2><p><a href="chapter-35.html">Chapter 35 — Information policy, security, and statistical confidentiality</a></p><p><a href="chapter-36.html">Chapter 36 — Electronic government and FedRAMP</a></p><p><a href="oversight.html">Follow the annual independent evaluation and IG responsibilities</a></p></section>'+filters(list(SECTIONS.values()))+'<section id="provisions"><h2>Find a responsibility or section</h2>'+''.join(section_cards)+'</section>'
duty_index='<section><h2>Follow a familiar duty to its source</h2><div class="table-wrap"><table><thead><tr><th scope="col">Duty</th><th scope="col">Statutory origin</th><th scope="col">Current provision</th></tr></thead><tbody>'
for k,v in LINEAGE.items():duty_index+='<tr><td>'+e(v['title'])+'</td><td>'+e(v['origin'])+'</td><td><a href="'+k.split('/')[0]+'.html#'+anchor(k)+'">'+e(label(k))+'</a></td></tr>'
duty_index+='</tbody></table></div></section>'
duty_index+='<section id="terms"><h2>Terms and institutions</h2><details><summary>Names used throughout the guide</summary><dl class="terms">'
for term,meaning in [('U.S. Code','Federal statutes organized by subject. Source credits and amendment notes show the enactments behind each section.'),('OMB','Office of Management and Budget; oversees government-wide information policy, budgets, and agency security implementation.'),('PRA','Paperwork Reduction Act; governs federal information management as well as collections from the public.'),('GISRA','Government Information Security Reform provisions enacted in 2000.'),('FISMA','Federal Information Security Management Act of 2002 and Federal Information Security Modernization Act of 2014; the date identifies which enactment is meant.'),('NIST and Commerce','National Institute of Standards and Technology and the Department of Commerce; develop and issue federal information-system standards under their statutory authorities.'),('FIPS','Federal Information Processing Standards; the applicable standard specifies its scope and requirements.'),('Special Publication','A NIST publication series. Its requirements must be understood with the law, policy, standard, or contract that calls for its use.'),('DHS and CISA','Department of Homeland Security and its Cybersecurity and Infrastructure Security Agency; administer specified security implementation and operational functions.'),('CIO','Chief Information Officer; advises agency leadership and carries out assigned information-management and security responsibilities.'),('IG and CIGIE','Inspector General, and the Council of the Inspectors General on Integrity and Efficiency; perform and coordinate independent oversight.'),('GAO','Government Accountability Office, headed by the Comptroller General; supports congressional oversight.'),('GSA and FedRAMP','General Services Administration, and the Federal Risk and Authorization Management Program for cloud products and services.'),('BOD','Binding operational directive; a compulsory direction within the scope and conditions of 44 USC §§3552–3553.')]:duty_index+='<dt>'+e(term)+'</dt><dd>'+e(meaning)+'</dd>'
duty_index+='</dl></details></section>'
body=body.replace('<section id="provisions">',duty_index+'<section id="provisions">')
page('law/index.html','Where federal information-security duties come from',intro,body)

# A-130 guide: use the unchanged source reader as the source for quoted blocks.
soup=BeautifulSoup((S/'read/a130-2016.html').read_text(),'html.parser');elements=soup.select('.source-page h2,.source-page h3,.source-page p')
positions={int(x['id'].split('-')[1]):i for i,x in enumerate(elements) if x.get('id','').startswith('section-')}
a130body=filters(A130,'<label>Language<select id="force"><option value="">All types</option>'+''.join(f'<option>{e(x)}</option>' for x in sorted({x['force'] for x in A130}))+'</select></label>')
a130toc='';export=[]
for i,t in enumerate(A130):
 start=positions[t['start']];end=positions[A130[i+1]['start']] if i+1<len(A130) else len(elements)
 source=elements[start:end];sourcehtml='';texts=[]
 for x in source:
  cp=copy.copy(x)
  for element in [cp,*cp.find_all(True)]:
   element.attrs={k:v for k,v in element.attrs.items() if k not in ['id','class']}
  if cp.name in ['h2','h3']:cp.name='h3'
  sourcehtml+=str(cp);texts.append(x.get_text())
 refs=' · '.join(f'<a href="../law/{ref}.html">{e(label(ref))}</a>' for ref in t['refs'])
 a130body+=f'<article id="{t["id"]}" class="search-item expectation" data-topics="{e("|".join(t["topics"]))}" data-actors="{e("|".join(t["actors"]))}" data-force="{e(t["force"])}" data-search="{e(" ".join([t["locator"],t["title"],t["summary"],*texts]))}"><h2>{e(t["title"])}</h2><p class="meta">{e(t["locator"])} · {e(t["force"])} · {e(", ".join(t["actors"]))}</p><p>{e(t["summary"])}</p><p class="related">Related statutory provisions: {refs}</p><details class="circular-source"><summary>Read the circular’s wording</summary><div class="legal-text">{sourcehtml}</div><p><a href="../read/a130-2016.html#section-{t["start"]}">Read in the complete circular</a> · <a href="../sources/a130-2016.pdf">Original PDF</a></p></details></article>'
 a130toc+=f'<a href="#{t["id"]}">{e(t["locator"])} — {e(t["title"])}</a>'
 export.append(dict(**t,source_text='\n'.join(texts),reader=f'read/a130-2016.html#section-{t["start"]}'))
page('a130/index.html','What A-130 expects of agencies','<p>The Office of Management and Budget’s circular turns several statutory responsibilities into government-wide management policy. This guide follows the July 28, 2016 circular and both appendices, from planning and acquisition to security, privacy, and oversight.</p><p>Use the topic and actor filters to follow a responsibility. “Required” identifies a section containing duties; the original wording retains every condition, exception, and recommendation. Discussion and definitions are labeled separately.</p><p><a href="../read/a130-2016.html">Read the complete original text</a> · <a href="../sources/a130-2016.pdf">Download the circular</a></p>',a130body,a130toc,'A-130 responsibilities')
(S/'a130/expectations.json').write_text(json.dumps(export,ensure_ascii=False,indent=2)+'\n')
# These source locators and bytes are covered by the validation script.
(S/'law/provisions.json').write_text(json.dumps(clauses,ensure_ascii=False,indent=2)+'\n')
(S/'law/source-manifest.json').write_text(json.dumps(sources,ensure_ascii=False,indent=2)+'\n')

# Historical editions retain original paragraph text; comparisons are edition comparisons, not inferred effective dates.
def historical_sections(file):
 doc=BeautifulSoup(file.read_text(),'html.parser');out={}
 for heading in doc.select('h3.section-head'):
  m=re.search(r'§\s*([\dA-Za-z–-]+)\.',heading.get_text())
  if not m:continue
  paragraphs=[];indents=[];credit='';active=True
  for x in heading.next_siblings:
   if getattr(x,'name',None)=='h3' and 'section-head' in x.get('class',[]):break
   if not getattr(x,'name',None):continue
   classes=' '.join(x.get('class',[]))
   if 'source-credit' in classes:credit=x.get_text();active=False
   if active and ('statutory-body' in classes or 'subsection-head' in classes):
    paragraphs.append(x.get_text());mindent=re.search(r'-(\d+)em',classes);indents.append(int(mindent[1]) if mindent else 0)
  if paragraphs:out[m[1].replace('–','-')]={'paragraphs':paragraphs,'indents':indents,'credit':credit}
 return out
historical={};hist_cache={}
for src in sources:
 if src['id'].startswith('usc-') and src['edition'].isdigit() and src['file'].endswith('.html'):
  data=historical_sections(S/src['file']);hist_cache[src['id']]=data
  for number,contents in data.items():
   title=src['id'].split('-')[2];historical.setdefault(f'{title}-{number}',[]).append(dict(edition=src['edition'],source=src['id'],**contents))

def current_paragraphs(root):
 out=[]
 def walk(x,prefix=''):
  tag=TAG(x)
  if tag in STRUCT:
   pre=plain(x.find(N+'num'))+' '+plain(x.find(N+'heading'))
   content=next((c for c in x if TAG(c) in ['content','chapeau']),None)
   if content is not None:out.append(normalize(prefix+pre+source_text(content)))
   kids=[c for c in x if TAG(c) in STRUCT]
   for i,c in enumerate(kids):walk(c,(prefix+pre+' ') if content is None and i==0 else '')
   for c in x:
    if TAG(c)=='continuation':out.append(normalize(source_text(c)))
  else:
   for c in x:
    if TAG(c) in STRUCT:walk(c)
    elif TAG(c) in ['content','chapeau','continuation']:out.append(normalize(source_text(c)))
 walk(root);return out

def word_diff(a,b):
 a=re.split(r'(\s+)',a);b=re.split(r'(\s+)',b);old=[];new=[]
 for op,i,j,k,l in difflib.SequenceMatcher(None,a,b,autojunk=True).get_opcodes():
  at=e(''.join(a[i:j]));bt=e(''.join(b[k:l]));old.append(('<del>'+at+'</del>') if op in ['replace','delete'] else at);new.append(('<ins>'+bt+'</ins>') if op in ['replace','insert'] else bt)
 return ''.join(old),''.join(new)

def para_paths(paras,indents=None):
 stack=[];result={};seen_subsections={}
 for ix,text in enumerate(paras):
  tokens=re.match(r'^((?:\([^()]+\)\s*)+)',text)
  if tokens:
   nums=re.findall(r'\(([^()]+)\)',tokens[1]);first=nums[0]
   if first.isdigit():level=1
   elif first.isupper():level=2
   elif first in ['i','ii','iii','iv','v','vi','vii','viii','ix','x','xi','xii'] and len(stack)>=3 and (indents is None or indents[ix]>0):level=3
   else:level=0
   if level==0:
    seen_subsections[first]=seen_subsections.get(first,0)+1
    if seen_subsections[first]>1:nums[0]+='~'+str(seen_subsections[first])
   stack=stack[:level]+nums
  if stack:
   for i in range(1,len(stack)+1):result.setdefault('/'.join(stack[:i]),[]).append(text)
 return result

history_index=[];history_export=[]
for rec in sections:
 key=rec['id'];versions=list(historical.get(key,[]));num=rec['number']
 # OLRC expressly identifies these predecessor sections. Both 2002 tracks remain visible.
 if rec['title']==44 and num.isdigit() and 3551<=int(num)<=3558:
  for offset in [10,20]:
   oldkey='44-'+str(int(num)-offset)
   for item in historical.get(oldkey,[]):versions.append(dict(item,predecessor=oldkey))
 versions.sort(key=lambda x:(int(x['edition']),x.get('predecessor','')))
 versions.append(dict(edition='2026 snapshot',source=rec['source'],paragraphs=current_paragraphs(roots[key]),credit=normalize(plain(roots[key].find(N+'sourceCredit')))))
 # Collapse unchanged annual readings only when the provision number is also unchanged.
 distinct=[]
 for v in versions:
  if distinct and distinct[-1]['paragraphs']==v['paragraphs'] and distinct[-1].get('predecessor')==v.get('predecessor'):continue
  distinct.append(v)
 versions=distinct
 histbody=''.join(lineage_html(k) for k in LINEAGE if k.split('/')[0]==key)
 histbody+=f'<p><a href="{key}.html">Return to current text and official amendment notes</a></p><p>Comparisons show the wording in dated Code editions. They do not assign an amendment’s effective date; consult the source credit and effective-date notes. Predecessor sections can use different clause numbering.</p>'
 histbody+='<label class="history-control">Show a comparison<select id="comparison"><option value="">All changes between collected editions</option>'
 comparisons=[]
 for i,(old,new) in enumerate(zip(versions,versions[1:])):
  title=f'{old["edition"]}'+(' (§'+old['predecessor'].split('-')[1]+')' if old.get('predecessor') else '')+' → '+new['edition']+(' (§'+new['predecessor'].split('-')[1]+')' if new.get('predecessor') else '')
  histbody+=f'<option value="change-{i}">{e(title)}</option>'
  a,b=word_diff('\n\n'.join(old['paragraphs']),'\n\n'.join(new['paragraphs']))
  citations=' · '.join(f'<a href="../{sourceby[v["source"]]["file"]}">{e(v["edition"])} source</a>' for v in [old,new])
  comparisons.append(f'<section class="version-change" id="change-{i}"><h2>{e(title)}</h2><p>{citations}</p><details><summary>Read before and after</summary><div class="comparison"><div><h3>Earlier wording <span class="removed-key">Deleted text</span></h3><div class="version-text">{a}</div></div><div><h3>Later wording <span class="added-key">Added text</span></h3><div class="version-text">{b}</div></div></div></details></section>')
 histbody+='</select></label><p class="meta">Color is accompanied by underlining for additions and strikethrough for deletions. Differences include editorial typography as well as substantive amendments.</p>'+''.join(comparisons)
 # Clause-level readings keep the original parent context accessible in the full edition comparison above.
 histbody+='<section id="clause-history"><h2>Follow a numbered provision</h2><p>These readings follow the same numbered locator within the same section. Renumbered predecessors are shown in the section comparisons above. A matching number alone does not establish that a duty continued unchanged.</p>'
 paths=sorted({c['id'].split('/',1)[1] for c in clauses if c['section']==key and '/' in c['id']})
 maps=[(v,para_paths(v['paragraphs'],v.get('indents'))) for v in versions if not v.get('predecessor') and v['edition']!='2026 snapshot']
 currentmap={nodeids[x].split('/',1)[1]:[normalize(source_text(x))] for x in roots[key].iter() if x in nodeids and '/' in nodeids[x]}
 maps.append((versions[-1],currentmap))
 for path in paths:
  entries=[];prev=None
  for v,m in maps:
   p=m.get(path)
   if p and p!=prev:
    entries.append((v,p));prev=p
  if len(entries)<2:continue
  histbody+=f'<details id="history-{anchor(key+"/"+path)}" class="clause-history"><summary>{e(label(key+"/"+path))} — {len(entries)} collected readings</summary>'
  for v,paras in entries:histbody+=f'<h3>{e(v["edition"])}</h3>'+''.join('<p class="legal-text">'+e(p)+'</p>' for p in paras)+f'<p><a href="../{sourceby[v["source"]]["file"]}">Original edition</a></p>'
  histbody+='</details>'
 histbody+='</section>'
 page(f'law/history-{key}.html','History of '+label(key),'<p>'+e(rec['heading'])+'</p>',histbody,current='How the law changed')
 history_index.append(f'<article id="{key}" class="search-item" data-topics="{e("|".join(SECTIONS[key]["topics"]))}" data-actors="{e("|".join(SECTIONS[key]["actors"]))}" data-search="{e(label(key)+" "+rec["heading"]+" "+" ".join(source_badges(rec)))}"><h3><a href="history-{key}.html">{e(label(key))} — {e(rec["heading"])}</a></h3><p>{len(versions)} distinct collected editions · <a href="{key}.html#history">Official amendments and earlier-provision notes</a></p>{badges(rec)}</article>')
 history_export.append(dict(section=key,versions=versions))

story='''<section id="origins"><h2>Information management came before FISMA</h2><p>The Paperwork Reduction Act of 1980 gave OMB responsibilities for federal information policy, including safeguards for information. The 1995 PRA restated chapter 35. Today, <a href="44-3504.html#p-44-3504-g">§3504(g)</a> assigns OMB privacy and security oversight, while <a href="44-3506.html#p-44-3506-g">§3506(g)</a> requires agencies to implement the applicable policies. A-130 carries these information-management responsibilities into agency practice.</p><p><a href="../read/pra1980.html">PRA 1980, §2, former §3504(f)</a> · <a href="../read/pra1995.html">PRA 1995, §2</a></p></section>
<section id="security-programs"><h2>GISRA established annual program evaluations</h2><p>In 2000, Congress enacted the Government Information Security Reform provisions, commonly called GISRA. The law required agency security programs and annual independent evaluations in former §§3534 and 3535. In 2002, the Homeland Security Act and the E-Government Act enacted overlapping security provisions. The E-Government Act’s FISMA title used §§3541–3549; former §3549 addressed the relationship between the two subchapters.</p><p><a href="../read/gisra.html">GISRA, §1061</a> · <a href="../sources/law/pl-107-296.html">Homeland Security Act, Title X</a> · <a href="../read/fisma2002.html">FISMA 2002, §301</a></p><p>FISMA 2014 replaced both earlier subchapters with §§3551–3558. It retained the agency-program and evaluation structure while expressly assigning DHS implementation responsibilities. The annual evaluation requirement therefore has a history extending before the current §3555 was enacted.</p><p><a href="../read/fisma2014.html">FISMA 2014, §2</a> · <a href="history-44-3555.html">Compare the evaluation provisions</a></p></section>
<section id="standards"><h2>NIST’s standards work has a direct statutory basis</h2><p>Congress assigned technical standards responsibilities separately from OMB’s management policy. The Computer Security Act added a computer-standards program to NIST’s governing statute. The 2002 laws revised that framework; today <a href="15-278g-3.html">15 USC §278g-3</a> assigns NIST standards and guidance work, while <a href="40-11331.html">40 USC §11331</a> governs Commerce’s issuance of federal information-system standards.</p><p>The two 2002 enactments also had different effective dates. The Code’s amendment notes preserve their interaction. In 2022, Congress amended the standards provisions to name Commerce in places that had named OMB. The current wording and earlier versions are available in the comparisons.</p><p><a href="../read/csa.html">Computer Security Act, §3</a> · <a href="15-278g-3.html#history">NIST provision’s amendment and effective-date notes</a> · <a href="history-40-11331.html">Compare standards authority</a></p></section>
<section id="operational"><h2>DHS received additional operational powers over time</h2><p>FISMA 2014 expressly assigned DHS a role in administering agency security implementation, including binding operational directives. Congress added emergency-directive authority in 2015. Later legislation established CISA within DHS and added further operational duties. These changes are visible in <a href="44-3553.html">§3553</a> and <a href="6-652.html">6 USC §652</a>.</p><p><a href="../sources/law/pl-114-113.html">Cybersecurity Act of 2015, §229</a> · <a href="../sources/law/pl-115-278.html">CISA Act of 2018</a></p></section>
<section id="cloud"><h2>FedRAMP moved from OMB policy into statute</h2><p>OMB established FedRAMP through policy in 2011. Congress gave the program a statutory basis in 2022, adding §§3607–3616. The law incorporates selected definitions from A-130 and NIST, assigns responsibilities to GSA and agencies, and directs OMB to issue implementation guidance. OMB’s 2024 memorandum updates that policy framework.</p><p><a href="../read/fedramp2011.html">2011 FedRAMP policy</a> · <a href="../read/fedramp-act.html">FedRAMP Authorization Act, §5921</a> · <a href="../read/m-24-15.html">OMB M-24-15</a></p></section>'''
page('law/history.html','How today’s duties took shape','<p>A duty’s first appearance, its latest amendment, and its current section number can have different dates. Follow the main changes below, then compare the wording of individual sections and clauses.</p>',story+filters(list(SECTIONS.values()))+'<section><h2>Compare provisions over time</h2>'+''.join(history_index)+'</section>',current='How the law changed')
(S/'law/duty-lineage.json').write_text(json.dumps(LINEAGE,ensure_ascii=False,indent=2)+'\n')
(S/'law/history-data.json').write_text(json.dumps(history_export,ensure_ascii=False,indent=2)+'\n')

oversight='''<section id="annual"><h2>An independent evaluation every year</h2><p>Each agency must have its information-security program and practices independently evaluated each year. The evaluation tests a representative subset of systems and assesses the effectiveness of the agency’s policies and practices. It is broader than an assessment of one system or one cloud service. <a href="44-3555.html#p-44-3555-a">44 USC §3555(a)</a>.</p><p>For agencies with an Inspector General, the IG performs the evaluation or determines whether an independent external auditor will do it. For other agencies, the agency head engages an independent external auditor. National security systems have a separate arrangement under which the agency head designates the evaluator. <a href="44-3555.html#p-44-3555-b">§3555(b)–(c)</a>.</p></section>
<section id="management"><h2>Management’s testing continues alongside the IG evaluation</h2><p>Agency leadership operates the security program. FISMA requires periodic testing and evaluation of controls, with a frequency based on risk and no less than annually. Management also tracks remediation, handles incidents, and maintains continuity plans. The independent evaluation assesses the program’s effectiveness; it does not take over management’s responsibilities. <a href="44-3554.html#p-44-3554-b">§3554(b)</a>.</p><p>Evaluators may use existing audits, evaluations, and reports. That allows relevant work to support the annual evaluation without changing who is responsible for it. <a href="44-3555.html#p-44-3555-d">§3555(d)</a>.</p></section>
<section id="reporting"><h2>Results reach OMB and Congress</h2><p>The agency head submits evaluation results to OMB by the date OMB establishes. OMB summarizes those results in its report to Congress. The statute protects sensitive information and specifies special treatment for national-security and intelligence-related information. <a href="44-3555.html#p-44-3555-e">§3555(e)–(g)</a>.</p><p>IGs also have reporting responsibilities under their general statute, now codified in Title 5. Those duties coexist with the specific FISMA evaluation process. <a href="5-404.html">5 USC §404</a> and <a href="5-405.html">§405</a>.</p></section>
<section id="guidance"><h2>Guidance coordinates how evaluations are performed</h2><p>OMB must ensure development of evaluation guidance in consultation with DHS, the CIO Council, the Council of the Inspectors General on Integrity and Efficiency, and other appropriate participants. Annual reporting instructions and metrics give evaluators a common framework. The statutory duty remains the evaluation required by §3555. <a href="44-3555.html#p-44-3555-j">§3555(j)</a>.</p><p><a href="https://www.cisa.gov/topics/cyber-threats-and-advisories/federal-information-security-modernization-act">CISA FISMA guidance and reporting resources</a> · <a href="5-424.html">CIGIE’s statutory role</a> · <a href="../a130/index.html#a130-50">A-130 responsibilities guide</a></p></section>
<section id="gao"><h2>GAO adds congressional oversight</h2><p>The Comptroller General periodically evaluates agency security policies and implementation of FISMA, reports to Congress, and may provide technical assistance to evaluators. GAO’s government-wide work is distinct from each agency’s annual independent evaluation. <a href="44-3555.html#p-44-3555-h">§3555(h)–(i)</a>.</p><p>The FedRAMP statute separately requires program reporting and a GAO report. Independent assessment of a cloud service under FedRAMP serves a different purpose from evaluating an agency’s full security program. <a href="44-3611.html">§3611</a> and <a href="44-3615.html">§3615</a>.</p></section>
<section id="lineage"><h2>The annual duty predates the current section number</h2><p>GISRA required annual independent evaluations in 2000. FISMA 2002 continued the requirement, and FISMA 2014 placed it in today’s §3555. A 2022 amendment changed the citation to the Inspector General statute after its recodification in Title 5. That citation change did not create a new annual evaluation duty.</p><p><a href="history-44-3555.html">Read the successive evaluation provisions</a> · <a href="44-3555.html#history">Read the official amendment notes</a></p></section>'''
page('law/oversight.html','Who evaluates agency security?','<p>Agency management, Inspectors General, OMB, and GAO have different jobs. The annual independent evaluation connects those responsibilities without transferring ownership of the security program away from the agency.</p>',oversight,''.join(f'<a href="#{k}">{v}</a>' for k,v in [('annual','Annual evaluation'),('management','Management testing'),('reporting','Reporting'),('guidance','Guidance'),('gao','GAO and FedRAMP'),('lineage','History')]),'IGs and oversight')

coverage='<section><h2>What is included</h2><p>All codified section text in Title 44 chapters 35 and 36 is included, with their source credits, editorial notes, and statutory notes. Connected provisions cover privacy, IGs, CISA, standards, CIOs, IT investment, and acquisition supply-chain security. The chapter readers show the full section text; each section page includes its notes.</p><p>The current-law text reproduces OLRC release 119-118, through September 30, 2026. It is a dated Code snapshot, not a representation that later enactments have been incorporated. Retrieval on October 10 does not change that release date. The official classification-table service was unavailable during collection; later-law verification remains a separate update step.</p><p>The A-130 guide uses the July 28, 2016 circular, identified by <a href="https://csrc.nist.gov/topics/laws-and-regulations/executive-documents/omb-a-130">NIST’s A-130 index</a>. Related documents retain the editions and status recorded in the source library.</p></section><section><h2>How to interpret the history</h2><p>The source credit identifies enactments and amendments to a Code section. It does not always identify the first appearance of a duty: Congress may restate or move an older provision. Official prior-provision and effective-date notes accompany the text.</p><p>Edition comparisons preserve the words of collected Code editions. They show changes between those editions, including editorial punctuation. They are not day-by-day reconstructions of every intervening amendment. Clause readings follow the same numbered locator; renumbered predecessors are shown separately in section comparisons. The 2000 and 2002 predecessors of the FISMA sections appear alongside the current sections.</p><p>Historical collection begins with available 1994 Code editions and selected later editions. Earlier enactments are linked from the historical report and source credits. Missing older readings are not treated as evidence that a duty did not exist.</p></section><section><h2>Connections beyond the collection</h2><p>Internal statutory cross-references link locally when the target is included. Other references link to the official Code. Related materials are selected implementation documents, not a catalogue of every policy, directive, standard, or agency-specific instruction.</p></section><section><h2>Preserved official sources</h2><p><a href="source-manifest.json" download>Download source manifest with SHA-256 hashes</a> · <a href="provisions.json" download>Download provision index</a> · <a href="history-data.json" download>Download historical readings</a></p><ol class="source-list">'
for src in sources:coverage+=f'<li id="{e(src["id"])}"><a href="../{e(src["file"])}">{e(src["id"])}</a> · <a href="{e(src["url"])}">Official source</a><details><summary>Provenance</summary><p>Retrieved {src["retrieved"]}; edition {e(src["edition"])}.</p><code>{src["sha256"]}</code></details></li>'
coverage+='</ol></section>'
page('law/sources.html','Coverage, editions, and sources','<p>Source text, explanations, and historical comparisons are stored separately. The links below identify the official files used for this edition.</p>',coverage,current='Coverage and sources')
print('Built law explorer:',len(sections),'sections,',len(clauses),'provisions,',len(A130),'A-130 topics,',len(sources),'sources')

relationships=[]
for key,items in MATERIALS.items():
 for rid,relationship,locator in items:relationships.append(dict(provision=key,document=rid,relationship=relationship,locator=locator))
for t in A130:
 for key in t['refs']:relationships.append(dict(provision=key,expectation=t['id'],relationship='related statutory authority',locator=t['locator']))
(S/'law/relationships.json').write_text(json.dumps(relationships,ensure_ascii=False,indent=2)+'\n')
changes=[]
for rec in sections:
 for note in roots[rec['id']].findall(f'.//{N}note'):
  if note.get('topic') in ['amendments','priorProvisions','effectiveDate','changeOfName']:
   changes.append(dict(section=rec['id'],type=note.get('topic'),text=normalize(plain(note)),source=rec['source'],url=f'law/{rec["id"]}.html#history'))
(S/'law/changes.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2)+'\n')

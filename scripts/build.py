import json,pathlib,html,re,csv
from readers import build_readers
from content import SUMMARIES,SYNTHESIS,PREHISTORY,DOMAINS,NIST_GROUPS,MEMORANDA,METHOD,EDITORIAL_NOTES,INTRO,AUTHORITY_CLOSE,RELATION_LABELS
R=pathlib.Path(__file__).resolve().parents[1];S=R/'site';records=json.loads((R/'data/records.json').read_text());by={x['id']:x for x in records}
build_readers(S,records)
def e(s):return html.escape(str(s),quote=True)
notes=[]
def cite(refs=(),note=''):
 n=len(notes)+1;notes.append((refs,note))
 return f'<sup class="noteref"><a id="ref-{n}" href="#note-{n}" role="doc-noteref" aria-label="Note {n}">{n}</a></sup>'
def source_note(key):
 text,refs=EDITORIAL_NOTES[key];return cite(refs,text)
def paras(blocks):
 out=[]
 for block in blocks:
  text=e(block['text']);ref=cite(block['refs']) if block.get('refs') else ''
  if block['kind']=='quote':
   record=by[block['refs'][0][0]]
   out.append('<figure class="source-quote"><blockquote><p>“'+text+'”</p></blockquote><figcaption>'+e(record['title'])+', '+e(date(record))+ref+'</figcaption></figure>')
  else:out.append('<p>'+text+ref+'</p>')
 return ''.join(out)
def date(x):
 p=x.get('date_precision','')
 return ('FY '+x['id'][2:4]+' · date unknown') if p.startswith('fiscal year') else x['date'][:7] if p.startswith(('month','Only the month')) else x['date']
def links(x):
 a=f'<a href="{e(x["url"])}">Official source</a>'
 if x.get('local'):a+=f' · <a href="{e(x["local"])}" download>Download original</a>'
 if x.get('reader'):a+=f' · <a href="{e(x["reader"])}">Read formatted text</a>'
 elif x.get('extracted'):a+=f' · <a href="{e(x["extracted"])}">Extracted text</a>'
 if x.get('evidence_id') in by:a+=f' · <a href="#doc-{x["evidence_id"]}">Related source</a>'
 return a
nav=[('synthesis','Overview'),('chronology','Timeline'),('predecessors','Before A-130'),('revisions','A-130 revisions'),('authority','Who is responsible?'),('nist','Technical standards'),('memoranda','OMB memoranda'),('library','Source library'),('notes','Notes'),('method','About the sources')]
parts=['<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="How OMB Circular A-130, federal laws, and NIST standards shaped information security."><title>A-130 · History & authority</title><link rel="stylesheet" href="styles.css"><script src="app.js" defer></script></head><body><a class="skip" href="#main">Skip to report</a><aside class="rail"><a class="wordmark" href="#top">A–130<span>History & authority</span></a><nav aria-label="Report sections">']
parts+=['<a href="on-behalf/index.html">Federal information in private services</a><a href="law/index.html">Read the current law</a><a href="a130/index.html">A-130 responsibilities</a><a href="law/oversight.html">IGs and oversight</a>',''.join(f'<a href="#{id}">{title}</a>' for id,title in nav),'<div class="rail-foot">Updated 10 October 2026<br><a href="manifest.json" download>Source index ↓</a><br><a href="https://github.com/pete-wai/fedramp-a130">GitHub repository</a></div></nav></aside><main id="main"><header id="top"><h1>'+e(INTRO['title'])+'</h1><p class="deck">'+e(INTRO['deck'])+'</p><p class="edition">1965–2026</p><a class="button" href="#synthesis">Read the history</a> <a class="text-action" href="#library">Find a document →</a></header>']
parts+=['<section id="synthesis"><h2>How laws, agency policy, and technical standards fit together</h2><div class="prose">',paras(SYNTHESIS),cite([('a130-2016','§§3, 5, 6 and 9'),('fisma2002','Title III, §§303–304'),('fisma2014','§2'),('fedramp2011','Introduction'),('fedramp-act','§5921'),('m-24-15','Scope and responsibilities')]),'</div><div class="chain" aria-label="Government responsibilities"><div><b>Congress</b><span>Assigns responsibilities in law</span></div><div><b>OMB & agencies</b><span>Set policy and manage systems</span></div><div><b>NIST & Commerce</b><span>Develop and issue standards</span></div></div></section>']
parts+=['<section id="chronology"><h2>Laws, policies, and standards over time</h2><p class="intro">'+e(INTRO['chronology'])+'</p><div class="timeline-scroll" tabindex="0" role="region" aria-label="Chronology table"><table class="timeline"><thead><tr><th scope="col">Period</th><th scope="col">Laws & presidential directives</th><th scope="col">OMB policy</th><th scope="col">NIST and its predecessor, NBS</th></tr></thead><tbody>']
selected=['a71-1965','brooks','privacy','fips31','fips46','a71-1978','fips65','pra1980','sp50085','a130-1985','csa','bulletin88','bulletin90','a130-1993','a130-1994-fr','fips1401','pra1995','sp80012','clinger','a130-1996','sp80018','a130-2000','gpea-guidance','gisra','fips197','fips1402','fisma2002','fips199','sp80037','sp80053','fips200','hspd12','sp80063v101','sp800371','eo13556','fedramp2011','sp800145','sp800144','sp800534','fisma2014','sp800171','a130-2016','sp800372','fips1403','sp800535','sp800207','eo14028','sp800218','m-22-09','fedramp-act','quantumact','sp8001713','fips203','m-24-15','sp800634','m-26-15']
for lo,hi in [(1965,1979),(1980,1989),(1990,1995),(1996,2000),(2001,2006),(2007,2014),(2015,2020),(2021,2026)]:
 cells=[[],[],[]]
 for id in sorted(selected,key=lambda id:by.get(id,{"date":"9999"})["date"]):
  if id not in by:continue
  x=by[id];y=int(x['date'][:4])
  if lo<=y<=hi:
   lane=0 if x['type'] in ['Law','Executive directive'] else 2 if x['type']=='NIST' else 1
   cells[lane].append(f'<button class="event" data-document="{id}"><span>{e(date(x))}</span>{e(x["title"])}</button>')
 parts+=['<tr><th scope="row">'+str(lo)+'–'+str(hi)+'</th>'+''.join('<td>'+''.join(c)+'</td>' for c in cells)+'</tr>']
parts+=['</tbody></table></div><div id="event-detail" class="event-detail" tabindex="-1" aria-live="polite"><p>Select an event for its description and source links.</p></div></section>']
parts+=['<section id="predecessors"><h2>Before A-130: computers, personal records, and security</h2><div class="prose">',paras(PREHISTORY),cite([('fips12','§4.6'),('brooks','§111(f)'),('privacy','§3'),('fips31','Foreword'),('fips46','Authority'),('fips65','Introduction'),('pra1980','44 USC 3504–3506')]),source_note('prehistory'),'</div></section><section id="revisions"><h2>How A-130 changed</h2><p class="intro">'+e(INTRO['revisions'])+'</p>']
for id,title,body,refs in SUMMARIES:
 parts += [f'<article class="revision" id="revision-{id}"><h3>{e(title)}</h3><div class="prose">',paras(body),'<p class="citations">Sources and edition notes ',cite(refs),source_note(id),f'</p><p>{links(by[id])}</p></div></article>']
parts+=['</section><section id="authority"><h2>Who is responsible for each part of security?</h2><p class="intro">'+e(INTRO['authority'])+'</p>']
for title,role,body,id,loc in DOMAINS:parts += [f'<article class="domain"><h3>{e(title)}</h3><p class="finding">{e(role)}</p><p>{e(body)}',cite([(id,loc)]),'</p></article>']
parts+=['<div class="prose"><h3>When technical guidance becomes a requirement</h3>',paras(AUTHORITY_CLOSE),cite([('fisma2002','Title III, §§301, 303–304'),('fisma2014','§2'),('a130-2016','§§3, 6 and 9')]),'</div></section><section id="nist"><h2>How the technical standards developed</h2>']
for title,body,refs in NIST_GROUPS:
 parts += [f'<article class="prose"><h3>{e(title)}</h3><p>{e(body)}',cite(refs),source_note('identity') if title.startswith('Proving identity') else '', '</p></article>']
parts+=['</section><section id="memoranda"><h2>How OMB policy changed between revisions</h2><div class="prose">',paras(MEMORANDA),cite([('a130-1996-preamble','Appendix IV discussion'),('a130-2000-notice','Incorporation of memoranda'),('m-04-04','NIST guidance assignment'),('fedramp2011','Introduction'),('m-24-15','Rescission'),('m-19-17','p. 13'),('m-17-26','Eliminated, modified and paused policies')]),'</div><button class="button" id="show-memos">Browse OMB memoranda</button></section>']
parts+=['<section id="library"><h2>Source library</h2><p class="intro">'+e(INTRO['library'])+'</p><form id="filters" class="filters" role="search"><label class="search-label">Search documents<input id="query" type="search" placeholder="Try cloud, authorization, or M-04-04"></label>']
for id,label,values in [('type','Document type',sorted(set(x['type'] for x in records))),('era','Period',['Before 1985','1985–1999','2000–2015','2016–2026']),('relation','Relationship to A-130',sorted(set(x['relation'] for x in records))),('term','Terms found',['cloud','commercial services','FedRAMP','related terminology']),('sort','Sort',['Oldest first','Newest first','Title A–Z'])]:
 parts+=[f'<label>{label}<select id="{id}">'+('' if id=='sort' else '<option value="">All</option>')+''.join(f'<option value="{e(v)}">{e(RELATION_LABELS.get(v,v) if id=="relation" else v)}</option>' for v in values)+'</select></label>']
parts+=['<button type="reset">Reset filters</button></form><p id="result-count" role="status">'+str(len(records))+' documents</p><p id="empty" hidden>No documents match. Clear a filter or try a broader search.</p>']
parts+=['<div class="view-control"><button id="toggle-view" type="button" aria-pressed="false">Show compact table</button></div><div id="compact-table" class="timeline-scroll" hidden tabindex="0" role="region" aria-label="Document inventory"><table><thead><tr><th scope="col">Date</th><th scope="col">Document</th><th scope="col">Type / relationship</th><th scope="col">Terms found</th></tr></thead><tbody>'+''.join(f'<tr data-record="{x["id"]}"><td>{e(date(x))}</td><td><a href="#doc-{x["id"]}">{e(x["title"])}</a></td><td>{e(x["type"])}<br>{e(RELATION_LABELS.get(x["relation"],x["relation"]))}</td><td>{e(", ".join(m["term"] for m in x.get("matches",[])))}</td></tr>' for x in records)+'</tbody></table></div><div id="records">']
verification={'Passage reviewed against original extracted text; PDF page supplied':'Checked against extracted text; PDF page listed.','extracted passage; check linked original':'Extracted text; not checked against the page image.','extracted candidate':'Text-search result; not checked against the page image.','Matching passage checked in original PDF page image, October 10, 2026':'Checked against the original PDF page on October 10, 2026.'}
for x in records:
 era='Before 1985' if x['date']<'1985' else '1985–1999' if x['date']<'2000' else '2000–2015' if x['date']<'2016' else '2016–2026'
 matches=x.get('matches',[]);tags='|'.join(m['term'] for m in matches)
 body=f'<div class="record-heading"><p class="record-date">{e(date(x))}<span>{e(x["type"])}</span></p><h3><a href="#doc-{x["id"]}">{e(x["title"])}</a></h3></div><p class="record-relation">{e(RELATION_LABELS.get(x["relation"],x["relation"]))}</p><p class="record-description">{e(x["note"])}</p><p class="source-links">{links(x)}</p>'
 if x.get('reference_passage'):body+='<details><summary>Passage mentioning A-130</summary><p class="source-passage">'+e(x['reference_passage'])+'</p><p class="locator">'+e(x['locator'])+'</p></details>'
 if matches:
  body+='<details><summary>Terms found: '+e(', '.join(m['term'] for m in matches))+'</summary>'
  for m in matches:body+=f'<div class="match"><b>{e(m["term"])} · {e(m["locator"])}</b><p>{e(m["passage"])}</p><small>{e(verification.get(m["verification"],m["verification"]))}</small></div>'
  body+='</details>'
 body+='<details><summary>Source details and edition</summary><p>'+e(x['status'])+'</p><p>'+e(x['locator'])+'</p><p>'+e(x['date_precision'])+'</p>'
 for note in x.get('source_notes',[]):body+='<p>'+e(note)+'</p>'
 if x.get('text_quality'):body+='<p>'+e(x['text_quality'])+'</p>'
 if x.get('availability')!='downloaded':body+='<p>'+e({'original not located':'Original unavailable in this collection','unavailable':'File unavailable in this collection','reproduced in FIPS 12':'Reproduced in FIPS 12'}.get(x['availability'],x['availability']))+'</p>'
 if x.get('sha256'):body+='<p>Downloaded '+e(x['retrieved'])+' · '+str(x['bytes'])+' bytes</p><p>SHA-256 checksum</p><code>'+x['sha256']+'</code>'
 body+='</details>'
 parts += [f'<article class="record" id="doc-{x["id"]}" data-type="{e(x["type"])}" data-era="{era}" data-relation="{e(x["relation"])}" data-terms="{e(tags)}" data-date="{x["date"]}" data-title="{e(x["title"])}">{body}</article>']
parts+=['</div></section><section id="notes" role="doc-endnotes"><h2>Notes and sources</h2><ol class="footnotes">']
for n,(refs,note) in enumerate(notes,1):
 text=e(note)+' ' if note else ''
 for id,loc in refs:
  assert id in by,id
  x=by[id];text+=f'<a href="#doc-{id}">{e(x["title"])}</a>, {e(loc)}.'
  if x.get('local'):
   page=re.search(r'PDF page (\d+)',loc);target=x['local']+('#page='+page[1] if page else '')
   text+=f' <a href="{e(target)}">Original</a>.'
  text+=' '
 parts.append(f'<li id="note-{n}" tabindex="-1">{text}<a class="backlink" href="#ref-{n}" role="doc-backlink" aria-label="Back to reference {n}">↩</a></li>')
parts+=['</ol></section><section id="method"><h2>About the sources</h2><div class="prose">',paras(METHOD),'<p><a href="manifest.json" download>Source index (JSON)</a> · <a href="manifest.csv" download>Source index (CSV)</a> · <a href="search-log.json">Collections searched</a> · <a href="candidate-manifest.json">Memorandum search results</a></p></div></section><footer><a href="#top">Back to top ↑</a><button id="print">Print report</button></footer></main></body></html>']
(S/'manifest.json').write_text(json.dumps(records,indent=2));(S/'index.html').write_text(re.sub(r'</p>((?:<sup class="noteref">.*?</sup>)+)',r'\1</p>',''.join(parts)));(S/'.nojekyll').touch()
with (S/'manifest.csv').open('w') as f:
 keys=['id','date','date_precision','title','type','relation','status','url','local','reader','reader_scope','sha256','availability'];w=csv.DictWriter(f,fieldnames=keys,extrasaction='ignore');w.writeheader();w.writerows(records)
for source,dest in [('search-log.json','search-log.json'),('memo-candidates.json','candidate-manifest.json')]: (S/dest).write_text((R/'data'/source).read_text())
print('Built',len(records),'records;',len(notes),'notes; summary word counts',[(id,sum(len(b['text'].split())for b in body))for id,t,body,ref in SUMMARIES])

# The law explorer uses its own dated, immutable source collection.
import law_build

# The on-behalf report has a separately dated evidence collection.
import behalf_build

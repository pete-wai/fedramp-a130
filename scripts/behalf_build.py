"""Build the chronological report. No fetching; preserved originals are immutable."""
import json,html,hashlib,csv,re
from history_sources import R,S,source,sources
from history_content import TITLE,DECK,ERAS,EVENTS,RELATIONSHIPS,COMPARISONS,COVERAGE
E=lambda v:html.escape(str(v),quote=True)
quotes={q['id']:q for q in json.loads((R/'data/on-behalf/history-quotations.json').read_text())}
assert len(quotes)==sum(len(ev['quotes']) for ev in EVENTS)
assert len(quotes)==len({qid for ev in EVENTS for qid in ev['quotes']})
for q in quotes.values():source(q['source_id'])
for id,date,note in [
 ('sp53r3','2009; updated August 2010','Saved Revision 3 includes August 2010 updates and an archive cover.'),
 ('sp800534','2013; updated January 2015','Saved Revision 4 includes January 22, 2015 updates.'),
 ('sp800535','2020; updated December 2020','Saved Revision 5 includes December 10, 2020 updates; 2025 release change list is separately preserved.'),
 ('sp171r1','2016; updated June 2018','Saved Revision 1 includes June 7, 2018 updates and a later withdrawal cover.'),
 ('sp171r2','2020; updated January 2021','Saved Revision 2 includes January 28, 2021 updates and a later withdrawal cover.'),
 ('sp800171','2015; updated January 2016','Saved original publication includes January 2016 updates.'),
 ('rmf2014','2014-06-05','June 2014 updated edition, distinct from original February 2010 edition; later withdrawal wrapper included.')]:
 r=source(id);r['date']=date;r['provenance']=note+' '+r.get('provenance','')
claims=[]

def quote_text(q):
 text=q['text']
 # Clause breaks improve reading without changing or reordering the source words.
 if text.startswith('‘‘('):parts=re.split(r' (?=‘‘\()',text)
 elif q['id'] in ['a16-oversight','a16-incidents','omb24-exclusions']:parts=re.split(r' (?=(?:[a-f]|[1-6])\) )',text)
 elif q['id']=='plans26':parts=re.split(r' (?=•)',text)
 else:parts=[text]
 return ''.join('<p>'+E(part)+'</p>' for part in parts)

def quote(id):
 q=quotes[id];r=source(q['source_id']);url=r['local']+('#page='+str(q['pages'][0]) if q['pages'] else '')
 return f'<figure class="quotation" id="quote-{E(id)}"><figcaption><span class="authority">{E(r["kind"])}</span> <cite>{E(r["title"])}</cite><span class="locator">{E(q["locator"])} · {E(r["date"])}</span></figcaption><blockquote>{quote_text(q)}</blockquote><p class="quote-links"><a href="{E(url)}">Read original'+(f' · PDF {q["pages"][0]}' if q['pages'] else '')+f'</a><a href="#source-{E(r["id"])}">Source details</a><a href="#quote-{E(id)}" aria-label="Link to quotation {E(id)}">Link to quote</a></p></figure>'

def event(ev):
 refs=[dict(source_id=quotes[q]['source_id'],locator=quotes[q]['locator']) for q in ev['quotes']]
 claims.append(dict(id=ev['id'],references=refs))
 cls={'Law':'law','OMB policy':'omb','Mandatory standard':'fips','Regulation':'regulation','Comment response':'comment'}.get(ev['kind'],'nist')
 return f'<article class="milestone {cls}" id="{ev["id"]}" data-kind="{E(ev["kind"])}"><h3><a href="#{ev["id"]}">{E(ev["title"])}</a></h3><p class="event-meta"><time>{E(ev["date"])}</time><span class="authority">{E(ev["kind"])}</span></p><p class="event-summary">{E(ev["summary"])}</p><dl class="event-notes"><div><dt>Where it came from</dt><dd>{E(ev["origin"])}</dd></div><div><dt>What changed—or stayed</dt><dd>{E(ev["change"])}</dd></div></dl>'+ (f'<p class="edition-note"><strong>Edition note.</strong> {E(ev["edition"])}</p>' if ev['edition'] else '')+''.join(quote(q) for q in ev['quotes'])+'</article>'

nav=[('orientation','Start here'),('authority-map','How the authorities connect')]+[(id,date) for id,date,_ in ERAS]+[('today','What agencies must do now'),('coverage','Editions and limits'),('sources','Sources and downloads')]
body=f'<header class="report-title"><h1>{E(TITLE)}</h1><p class="deck">{E(DECK)}</p><p class="report-date">Research checked 25 October 2026 · {len(EVENTS)} milestones · {len(quotes)} direct quotations<br>Legal and publication editions are stated separately. <a href="#coverage">Coverage and limits</a></p><p class="jump-links"><a href="#early">Start in 2000</a><a href="#today">Current responsibilities</a><a href="print.html">Complete print edition</a></p></header>'
body+='''<section id="orientation"><h2>Two objects of protection. Duties that overlap.</h2><p class="lead">The law tells agencies to protect their information and their systems. It does not make ownership of equipment the only test. Later policy explains what agencies must do when another organization handles the information or provides the system.</p><figure class="two-duties"><figcaption>FISMA’s shared rule: protection commensurate with risk and harm</figcaption><div><h3>Information</h3><p>Collected or maintained <strong>by or on behalf of</strong> the agency.</p><p>The duty can follow information outside the agency’s own system.</p></div><div><h3>Information systems</h3><p><strong>Used or operated</strong> by the agency, or by another organization on its behalf.</p><p>The duty includes the system, its controls, and the agency’s oversight.</p></div><p class="figure-source"><a href="#quote-f14-dual">Read the exact statutory clauses</a> · The same wording appeared in 2002.</p></figure><p>Three points prevent common misreadings:</p><ol class="reading-points"><li><strong>Risk assessment and compliance go together.</strong> FISMA requires both. A duty to understand risk is not an alternative to applicable standards and policy.</li><li><strong>“Outside our boundary” does not mean “outside our responsibility.”</strong> NIST distinguishes external services from the system that uses them while preserving the agency’s information and risk duties.</li><li><strong>The nonfederal-system path has conditions.</strong> The CUI rule and SP 800-171 provide an explicit, narrower requirements set. They do not cover every external service or every kind of federal information.</li></ol><p><a href="#quote-f14-implement">FISMA’s implementation duties</a> · <a href="#quote-sa9-2006">NIST’s external-boundary distinction</a> · <a href="#quote-cui16-nonfederal">The CUI rule’s limits</a></p><p class="reading-note">Each milestone separates this report’s explanation from the source quotation. Quotations retain the original wording; spacing and line-end hyphenation are normalized. Footnote numbers remain where they appear in extracted text. Follow “Read original” for the surrounding text and footnotes. Historical text is not labeled as current merely because it is quoted here.</p></section>'''
body+='<section id="authority-map"><h2>How the authorities connect</h2><p>There is more than one path. Congress directed NIST and Commerce as well as OMB. Later law also incorporated definitions from an existing circular. The labels below describe an explicit relationship in the cited text; chronological order alone is not evidence of one.</p><ol class="relationships">'
for title,verb,explain,qid in RELATIONSHIPS:
 body+=f'<li><h3>{E(title)}</h3><p><strong>{E(verb.capitalize())}.</strong> {E(explain)} <a href="#quote-{qid}">Read the connecting words</a></p></li>'
body+='</ol></section><div class="timeline-tools" id="history-tools" hidden><h2>Find a passage in the history</h2><form id="history-filter"><label>Words or topic<input type="search" id="history-query" placeholder="Try information, boundary, or contract"></label><label>Authority<select id="history-kind"><option value="">All authorities</option>'+''.join(f'<option>{E(k)}</option>' for k in sorted({ev['kind'] for ev in EVENTS}))+'</select></label><button type="reset">Show all</button></form><p id="history-count" role="status"></p></div><p id="history-empty" hidden>No milestones match. Clear the words or choose all authorities.</p>'
for id,date,title in ERAS:
 body+=f'<section class="era" id="{id}"><h2>{E(date)}<span>{E(title)}</span></h2>'+''.join(event(ev) for ev in EVENTS if ev['era']==id)+'</section>'
body+='''<section id="today"><h2>What agencies must do now</h2><p class="lead">Start with the information and the service being acquired. Then identify every applicable duty. The texts do not support a blanket rule that commercial services are outside federal information-system obligations, or that only directly controlled components count.</p><p>They do support different requirements in specifically defined nonfederal settings. The clearest example here is CUI confidentiality under 32 CFR 2002.14(h)(2) and SP 800-171. That distinction must be applied with its scope and exceptions intact.</p><p><a href="#quote-a16-applicability">A-130’s service scope</a> · <a href="#quote-cui24-scope">Current SP 800-171 scope</a> · <a href="#quote-dhs23-response">The disagreement over a general definition</a></p><div class="comparisons">'''
for n,(topic,info,system,qid) in enumerate(COMPARISONS,1):
 body+=f'<article id="comparison-{n}"><h3>{E(topic)}</h3><dl><div><dt>Information duty</dt><dd>{E(info)}</dd></div><div><dt>System duty</dt><dd>{E(system)}</dd></div></dl><p><a href="#quote-{qid}">Read the underlying wording</a></p></article>'
body+='''</div><h3>A practical reading order for an agency decision</h3><ol class="reading-points"><li>Identify the information, its lifecycle, and any separate privacy, records, confidentiality, or CUI requirements.</li><li>Determine what the other organization does: collects or maintains information for the agency, operates a system for it, receives information for another purpose, or exchanges information across a boundary. These can overlap.</li><li>Apply the appropriate policy and standard to that arrangement. Do not substitute “commercial,” “shared,” or “outside our boundary” for the actual scope language.</li><li>Put the necessary protections, oversight, access, interfaces, incident duties, and evidence requirements into suitable agreements. Categorize and authorize where required.</li><li>Monitor performance and changing risk. Preserve the information owner’s responsibilities and the agency official’s decision record.</li></ol><p>This reading order is this report’s synthesis of <a href="#quote-f14-implement">44 USC 3554</a>, <a href="#quote-a16-contracts">A-130 §4(j)</a>, <a href="#quote-rmf18-steward">SP 800-37’s role descriptions</a>, and <a href="#quote-exchange21">SP 800-47’s exchange guidance</a>. It is not an additional rule.</p></section>'''
body+='<section id="coverage"><h2>Editions, coverage, and open questions</h2><p>This is a focused history of information, system, and service responsibilities. It is not an exhaustive inventory of every federal security requirement. Publication dates, later updates, and withdrawal wrappers are kept separate. “Current” below means the final publication checked for this report, not proof that every applicable agency rule has been found.</p><div class="coverage">'
for family,editions,note in COVERAGE:body+=f'<article><h3>{E(family)}</h3><p><strong>Checked:</strong> {E(editions)}</p><p>{E(note)}</p></article>'
body+='</div><p><a href="coverage.json" download>Download the edition and coverage ledger</a> · <a href="relationships.json" download>Download authority relationships</a></p></section>'
body+='<section id="sources"><h2>Sources and downloads</h2><p>Original files are preserved with their SHA-256 hashes. The library retains sources from the earlier report so existing source links still work. Retention does not mean the source is quoted in this edition.</p><p class="downloads"><a href="evidence.json" download>Sources JSON</a> · <a href="evidence.csv" download>Sources CSV</a> · <a href="quotations.json" download>Quotation text and locations</a> · <a href="claims.json" download>Milestone source index</a></p><form id="source-filter" class="source-controls" hidden><label>Find a source<input id="source-query" type="search" placeholder="Title, date, or document number"></label><button type="reset">Show all sources</button></form><p id="source-count" role="status" hidden></p><p id="source-empty" hidden>No sources match. Clear the search to show all sources.</p><div class="sources">'
for id,r in sorted(sources.items(),key=lambda pair:(pair[1]['date'],pair[0])):
 original=S/r['local'];assert original.is_file(),original
 assert hashlib.sha256(original.read_bytes()).hexdigest()==r['sha256'],id
 uses=[q for q in quotes.values() if q['source_id']==id];r['cited_locations']=[q['locator'] for q in uses]
 body+=f'<article class="source" id="source-{id}"><h3>{E(r["title"])}</h3><p class="source-meta">{E(r["kind"])} · {E(r["date"])} · '+(f'{len(uses)} quotation'+('s' if len(uses)!=1 else '') if uses else 'Retained reference')+f'</p><p><a href="{E(r["local"])}">Local original</a> · <a href="{E(r["url"])}">Original publisher</a></p><details><summary>Edition, provenance, and quoted locations</summary><p>{E(r.get("provenance","Preserved original; extracted text is a reading aid."))}</p><p>Retrieved {E(r["retrieved"])}. SHA-256: <code>{r["sha256"]}</code></p><ul>'+''.join(f'<li><a href="#quote-{q["id"]}">{E(q["locator"])}</a></li>' for q in uses)+'</ul></details></article>'
body+='</div></section>'
# Existing fragment URLs remain useful. Map old topics and quotation sources to new discussions.
existing=set(re.findall(r'\bid="([^"]+)"',body));existing.add('main')
oldquotes={q['id']:q for q in json.loads((R/'data/on-behalf/quotations.json').read_text())}
aliases={}
for name in ['prior-anchors.json','replacement-anchors.json']:
 for old in json.loads((R/'data/on-behalf'/name).read_text()):
  if old in existing:continue
  target='today'
  if old.startswith(('history','evidence-history')):target='early'
  elif old.startswith(('word','law','fisma')):target='fisma-2014-history'
  elif old.startswith(('dut','contract','oversight','access','incident','agreements','federal-ao')):target='a130-2016-history'
  elif old.startswith(('cui','extras','nist')):target='cui-2016-rule'
  elif old in ['answer','hypothesis','main-takeaway']:target='orientation'
  elif old in ['limits','coverage-method']:target='coverage'
  elif old.startswith('quote-'):
   matches=[q for q in oldquotes.values() if old.endswith('-'+q['id'])]
   if matches:
    q=sorted(matches,key=lambda q:len(q['id']))[-1]
    ev=next((v for v in EVENTS if any(quotes[x]['source_id']==q['source_id'] for x in v['quotes'])),None)
    if ev:target=ev['id']
  aliases.setdefault(target,[]).append(old);existing.add(old)
for target,ids in aliases.items():
 marker=f'id="{target}"';pos=body.index('>',body.index(marker))+1
 body=body[:pos]+''.join(f'<span class="legacy-anchor" id="{E(x)}" aria-hidden="true"></span>' for x in ids)+body[pos:]

def document(printing=False):
 content=body
 if printing:content=re.sub(r'<details([^>]*)>',lambda m:'<details'+m[1]+' open>',content)
 return '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="A quotation-led history of federal duties for information and information systems, from the PRA and FISMA through OMB policy, FIPS, and NIST guidance."><title>'+E(TITLE)+' · A-130</title><link rel="stylesheet" href="report.css">'+('' if printing else '<script src="report.js" defer></script>')+'</head><body'+(' class="print-edition"' if printing else '')+'><a class="skip" href="#main">Skip to report</a><header class="masthead"><a class="brand" href="../index.html">A–130 <span>History &amp; authority</span></a><nav aria-label="Main navigation"><a href="../index.html">History</a><a href="../law/index.html">Read the law</a><a href="../a130/index.html">A-130 responsibilities</a><a aria-current="page" href="index.html">Information &amp; systems</a><a href="../proposed-fedramp-use/index.html">Proposed FedRAMP use</a></nav></header><div class="layout"><aside class="contents"><details open><summary>In this report</summary><nav aria-label="Report sections">'+''.join(f'<a href="#{id}">{E(title)}</a>' for id,title in nav)+'</nav></details></aside><main id="main">'+content+'<footer><a href="#main">Back to top</a> · <a href="'+('index.html' if printing else 'print.html')+'">'+('Interactive edition' if printing else 'Complete print edition')+'</a><p>Historical sources and current guidance, with the report’s interpretation identified separately.</p></footer></main></div></body></html>'
(S/'index.html').write_text(document());(S/'print.html').write_text(document(True))
(S/'evidence.json').write_text(json.dumps(dict(research_date='2026-10-25',currency_note='Source-specific editions; OLRC snapshot through September 30, 2026. See coverage ledger.',sources=list(sources.values())),indent=2))
(S/'quotations.json').write_text(json.dumps([dict(q,uses=1) for q in quotes.values()],indent=2,ensure_ascii=False))
(S/'claims.json').write_text(json.dumps(claims,indent=2))
(S/'coverage.json').write_text(json.dumps([dict(family=f,editions=e,note=n) for f,e,n in COVERAGE],indent=2))
(S/'relationships.json').write_text(json.dumps([dict(relationship=t,type=v,explanation=e,quote_id=q) for t,v,e,q in RELATIONSHIPS],indent=2))
with (S/'evidence.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['id','title','date','kind','url','local','sha256','retrieved','cited_locations'],extrasaction='ignore',lineterminator='\n');w.writeheader();w.writerows(sources.values())
print(f'Built information/system history: {len(EVENTS)} milestones, {len(quotes)} quotes, {len(sources)} library sources')

"""Generate the offline on-behalf report; never fetch or change original sources."""
from pathlib import Path
import json, html, hashlib, re, csv
from behalf_content import HISTORY, FLOW, SCENARIOS, LIMITS
from behalf_analysis import TITLE, DECK, SUMMARY, WORDS, ROLES, DUTIES, COMPARISON, EXTRA, HISTORY_NOTE

R = Path(__file__).resolve().parents[1]
S = R / 'site' / 'on-behalf'
S.mkdir(exist_ok=True)
e = lambda value: html.escape(str(value), quote=True)
records = {r['id']: r for r in json.loads((R/'data/records.json').read_text())}
sources = {r['id']: r.copy() for r in json.loads((R/'data/on-behalf/new-sources.json').read_text()) if r.get('local')}
law_sources = {r['id']: r for r in json.loads((R/'data/law/sources.json').read_text())}
law_sections = {r['id']: r for r in json.loads((R/'data/law/sections.json').read_text())}
for id, section in [('usc3554','44-3554'),('usc3502','44-3502'),('usc3506','44-3506'),('usc3614','44-3614'),('usc552a','5-552a')]:
    rec = law_sections[section]; origin = law_sources[rec['source']]
    sources[id] = dict(id=id,title=f"{section.replace('-', ' USC ')} — {rec['heading']}",date='Through 2026-09-30',kind='Law',url=origin['url'],local='../'+origin['file'],reader='../law/'+section+'.html',sha256=origin['sha256'],retrieved=origin['retrieved'],provenance='OLRC release 119-118; unchanged existing collection. Later-law verification incomplete.')
hsa=law_sources['pl-107-296']
sources['hsa2002']=dict(id='hsa2002',title='Homeland Security Act of 2002, Title X',date='2002-11-25',kind='Law',url=hsa['url'],local='../'+hsa['file'],sha256=hsa['sha256'],retrieved=hsa['retrieved'],provenance='General effective date 60 days after enactment; compare the December 17 E-Government Act separately.')

for archived in json.loads((R/'data/on-behalf/retained-sources.json').read_text())['sources']:
    sources.setdefault(archived['id'], archived)
for standard in ['fips199','fips200']:
    if standard in sources:sources[standard]['kind']='Mandatory standard'
for id,date in [('sp800372','2018-12-20'),('sp8001713','2024-05-14'),('fips200','2006-03-09')]:
    if id in sources:
        sources[id]['date']=date
        sources[id]['provenance']=sources[id].get('provenance','')+' Publication date in this report checked against NIST publication history or the FIPS announcement; original bytes unchanged.'
quotes = {q['id']:q for q in json.loads((R/'data/on-behalf/quotations.json').read_text())}
quote_uses=[]
claims=[]
def source(id):
    if id not in sources:
        r=records[id]
        sources[id]=dict(id=id,title=r['title'],date=r['date'],kind='NIST guidance' if r['type']=='NIST' else r['type'],url=r['url'],local='../'+r['local'],sha256=r['sha256'],retrieved=r['retrieved'],provenance=r['status'])
        if r.get('extracted'): sources[id]['text']='../'+r['extracted']
    return sources[id]

def refs(refs, claim, opened=False):
    claims.append(dict(id=claim,references=[dict(source_id=id,locator=loc) for id,loc in refs]))
    out=f'<details class="evidence" id="evidence-{e(claim)}"'+(' open' if opened else '')+'><summary>Sources and exact locations</summary><ul>'
    for id,loc in refs:
        r=source(id)
        out+=f'<li><a href="#source-{e(id)}">{e(r["title"])}</a> — {e(loc)}. <a href="{e(r.get("reader",r["local"]))}">Read source</a></li>'
    return out+'</ul></details>'

def paragraphs(ps):return ''.join('<p>'+e(p)+'</p>' for p in ps)
def prose(items):
    return ''.join(f'<article id="{id}" class="prose-block"><h3>{e(title)}</h3>'+paragraphs(ps)+refs(rr,id)+'</article>' for id,title,ps,rr in items)

def quoted(qid, context):
    q=quotes[qid];r=source(q['source_id']);quote_uses.append(qid)
    url=r.get('reader',r['local'])
    if q['pages'] and r['local'].endswith('.pdf'):url=r['local']+'#page='+str(q['pages'][0])
    return '<figure class="quotation" id="quote-'+e(context)+'-'+e(qid)+'"><p class="quote-authority">'+e(r['kind'])+' · '+e(r['date'])+'</p><blockquote><p>'+e(q['text'])+'</p></blockquote><figcaption><cite>'+e(r['title'])+'</cite> · '+e(q['locator'])+' · <a href="'+e(url)+'">Read original</a> · <a href="#source-'+e(q['source_id'])+'">Source details</a></figcaption></figure>'

def analysis(items):
    out=''
    for id,title,qs,ps,rr in items:
        allrefs=list(dict.fromkeys([(quotes[q]['source_id'],quotes[q]['locator']) for q in qs]+rr))
        out+='<article class="prose-block" id="'+e(id)+'"><h3>'+e(title)+'</h3>'+''.join(quoted(q,id) for q in qs)+paragraphs(ps)+refs(allrefs,id)+'</article>'
    return out

nav=[('answer','The distinction'),('words','FISMA: the exact words'),('roles','Service purchase & operation'),('duties','Duties that follow information'),('comparison','Compare the requirements'),('extras','Additional triggers & limits'),('flows','Information lifecycle'),('examples','Worked examples'),('history','History & comments'),('sources','Evidence library'),('limits','Coverage and dates')]
body='<header class="report-title"><h1>'+e(TITLE)+'</h1><p class="deck">'+e(DECK)+'</p><p class="report-date">Research checked 24 October 2026; legal editions vary. <a href="#limits">Source dates and limits</a></p><div class="jump-links"><a href="#words">Read the statutory wording</a><a href="#comparison">Compare responsibilities</a><a href="print.html">Complete print edition</a></div></header>'
body+='<section id="answer"><h2>The distinction</h2><p class="lead">'+e(SUMMARY)+'</p><p>This report separates three arrangements: an agency system; an external service collecting or maintaining information for the agency; and a qualifying nonfederal system receiving information for other work. Their obligations can overlap. “Private company,” “external service,” and “nonfederal system” are not interchangeable legal labels.</p><p>The question is what an agency must do when it buys access to a provider-run service without taking over its operation. Quotations below supply the rule; the following paragraphs explain its reach and limits.</p></section>'
body+='<section id="words"><h2>FISMA: two objects of protection</h2><p>Quoted passages appear in full below each heading, with their authority and location. Excerpts retain their wording; text extraction normalizes line breaks, line-end word breaks, and spacing before punctuation. Explanations are separate from the quotations.</p>'+analysis(WORDS)+'</section>'
body+='<section id="roles"><h2>Service purchase, system operation, and agency responsibility</h2>'+analysis(ROLES)+'</section>'
body+='<section id="duties"><h2>What agencies must do for externally handled information</h2><p>A-130 Appendix I §4(j) addresses non-Federal entities. Its first requirement concerns agreements involving federal information. Its second has two alternative triggers and six specific oversight duties. The quotations preserve that distinction.</p>'+analysis(DUTIES)+'</section>'
body+='<section id="comparison"><h2>Where the requirements differ—and where they overlap</h2><p>The nonfederal column assumes the system qualifies as nonfederal under the governing authority. Whether a particular cloud service meets that assumption is the separate question above. Information-handling duties may still overlap; each row states its trigger. Read the conditions before applying a result.</p><div class="table-scroll" tabindex="0" role="region" aria-label="Federal system and external information duties"><table class="comparison"><caption>Agency responsibilities, by subject</caption><thead><tr><th>Subject</th><th>Federal information system</th><th>Federal information in a nonfederal system</th><th>Scope and conditions</th></tr></thead><tbody>'
for i,(topic,federal,external,limit,rr) in enumerate(COMPARISON):
    body+='<tr id="comparison-'+str(i+1)+'"><th scope="row">'+e(topic)+'</th><td>'+e(federal)+'</td><td>'+e(external)+'</td><td>'+e(limit)+refs(rr,'comparison-'+str(i+1))+'</td></tr>'
body+='</tbody></table></div></section>'
body+='<section id="extras"><h2>Additional triggers, express limits, and overlapping guidance</h2><p>Ordinary federal information is the starting point. The provisions below add conditions for specific information or services; they do not all apply to every document.</p>'+analysis(EXTRA)+'</section>'
body+='<section id="flows"><h2>Follow the information from creation to disposal</h2><p>The same document can move through several systems and several legal regimes. These questions help keep the duties attached to the right activity.</p><ol class="flow-list">'
for i,(title,example,text,rr) in enumerate(FLOW):
    body+=f'<li id="flow-{i+1}"><h3>{e(title)}</h3><p class="flow-example">{e(example)}</p><p>{e(text)}</p>'+refs(rr,f'flow-{i+1}')+'</li>'
body+='</ol></section><section id="examples"><h2>Compare the examples</h2><p>The first three examples compare buying SaaS access, operating an IaaS workload, and commissioning application operation. Incidental handling and internet transit provide contrasting cases. These are stated assumptions, not vendor compliance findings.</p><div id="scenario-controls" class="scenario-controls" hidden><label for="scenario-select">Choose an example</label><select id="scenario-select"><option value="all">All examples</option>'+''.join(f'<option value="{s["id"]}">{e(s["title"])}</option>' for s in SCENARIOS)+'</select></div><p id="scenario-status" class="result-count" role="status" hidden></p>'
for s in SCENARIOS:
    body+=f'<article class="scenario" id="example-{s["id"]}"><h3>{e(s["title"])}</h3><p class="assumptions"><strong>Assumptions.</strong> {e(s["assumptions"])}</p><figure class="flow-figure"><figcaption>Information and service relationships</figcaption><ol>'+''.join(f'<li>{e(n)}</li>' for n in s['flow'])+'</ol></figure><p class="scenario-answer">'+e(s['conclusion'])+'</p>'+paragraphs(s['paragraphs'])+'<dl class="responsibilities">'+''.join(f'<div><dt>{e(who)}</dt><dd>{e(what)}</dd></div>' for who,what in s['rows'])+'</dl><details class="changes"><summary>What could change the answer?</summary><p>'+e(s['changes'])+'</p></details>'+refs(s['refs'],'example-'+s['id'])+f'<p class="example-link"><a href="#example-{s["id"]}">Link to this example</a></p></article>'
body+='</section>'
body+='<section id="history"><h2>How the distinction developed</h2><p>This history follows duties and definitions across different authorities. A later document does not automatically repeal an earlier rule or settle its meaning.</p>'+analysis(HISTORY_NOTE)+'<form id="history-filter" class="controls" hidden><label>Authority<select id="history-kind"><option value="">All authorities</option>'+''.join(f'<option>{e(k)}</option>' for k in dict.fromkeys(h[1] for h in HISTORY))+'</select></label><label>Find a topic<input id="history-query" type="search" placeholder="Try incidental, privacy, or cloud"></label><button type="reset">Reset</button></form><p id="history-count" class="result-count" role="status" hidden></p><p id="history-empty" hidden>No events match. Clear the search or choose all authorities.</p><ol class="history-list">'
for date,kind,id,title,text,rr in HISTORY:
    body+=f'<li id="{id}" data-kind="{e(kind)}"><div class="event-date">{e(date)}<span>{e(kind)}</span></div><div><h3><a class="permalink" href="#{id}" aria-label="Link to {e(title)}">{e(title)}</a></h3><p>{e(text)}</p>'+refs(rr,id)+'</div></li>'
body+='</ol></section>'
body+='<section id="sources"><h2>Evidence library</h2><p>Each source keeps its own edition and authority. The source links open local originals or complete extracted text. Original HTML snapshots may retain publisher assets; this report has no network dependencies.</p><p class="downloads"><a href="evidence.json" download>Download sources (JSON)</a> · <a href="evidence.csv" download>Sources (CSV)</a> · <a href="claims.json" download>Claim-to-source index</a> · <a href="quotations.json" download>Verified quotations</a></p><form class="controls" id="source-filter" hidden><label>Search sources<input type="search" id="source-query" placeholder="Title, authority, or cited section"></label><label>Type<select id="source-kind"><option value="">All types</option>'+''.join(f'<option>{e(k)}</option>' for k in sorted(set(r['kind'] for r in sources.values())))+'</select></label><button type="reset">Reset</button></form><p id="source-count" class="result-count" role="status" hidden></p><p id="source-empty" hidden>No sources match. Clear the search or select all types.</p><div class="sources">'
used={ref['source_id'] for claim in claims for ref in claim['references']}
retained={r['id'] for r in json.loads((R/'data/on-behalf/retained-sources.json').read_text())['sources']}
sources={id:r for id,r in sources.items() if id in used or id in retained}
for id,r in sorted(sources.items(),key=lambda pair:pair[1]['date']):
    uses=[(c['id'],ref['locator']) for c in claims for ref in c['references'] if ref['source_id']==id]
    r['cited_locations']=list(dict.fromkeys(loc for _,loc in uses))
    original=S/r['local'];assert original.is_file(), original
    if not uses:r['provenance']=r.get('provenance','')+' Retained from the earlier report for stable source links; not cited in this replacement.'
    assert hashlib.sha256(original.read_bytes()).hexdigest()==r['sha256'],id
    body+=f'<article class="source" id="source-{id}" data-kind="{e(r["kind"])}"><p class="source-type">{e(r["kind"])} · {e(r["date"])}</p><h3>{e(r["title"])}</h3><p class="source-links"><a href="{e(r["local"])}">Local original</a>'
    if r.get('reader'):body+=f' · <a href="{e(r["reader"])}">Read formatted text</a>'
    if r.get('text'):body+=f' · <a href="{e(r["text"])}">Complete extracted text</a>'
    body+=f' · <a href="{e(r["url"])}">Official / original publisher</a></p><details><summary>Locations, provenance, and uses in this report</summary><p>{e(r.get("provenance","Preserved official source; extraction is a reading aid, not a replacement for the original."))}</p><p>Retrieved {e(r["retrieved"])}. SHA-256: <code>{r["sha256"]}</code></p><ul>'+''.join(f'<li><a href="#{claim}">Back to discussion</a> — {e(loc)}</li>' for claim,loc in uses)+'</ul></details></article>'
body+='</div></section><section id="limits"><h2>Coverage, source dates, and open questions</h2><ul class="limits">'+''.join('<li>'+e(x)+'</li>' for x in LIMITS)+'</ul><h3>What still needs an agency-specific answer</h3><p>The actual information, purpose of the service, applicable contract, agency policies, system architecture, provider access, and available assurance determine the result for a real purchase. Where authorities differ in scope, record the reason for the chosen interpretation instead of treating a convenient definition as universal.</p><p>Research and review were performed in this chat, including a separate self-review. No independent legal review or vendor assessment was performed. Research refreshes are manual.</p></section>'

# Resolve prior discussion links to the corresponding replacement section.
existing=set(re.findall(r'\bid="([^"]+)"',body))
for old_id in json.loads((R/'data/on-behalf/prior-anchors.json').read_text()):
    if old_id in existing or old_id=='main':continue
    target='comparison' if old_id.startswith(('hypothesis','boundary')) or old_id in ['hypothesis','boundaries'] else 'words' if old_id.startswith('word-') else 'extras' if old_id=='nist' else 'answer'
    marker='<section id="'+target+'">'
    body=body.replace(marker,marker+'<span class="legacy-anchor" id="'+e(old_id)+'"></span>',1)

def document(printing=False):
    content=body
    if printing:
        content=re.sub(r'<details([^>]*)>',lambda m:'<details'+m[1]+' open>' if ' open' not in m[1] else m[0],content)
    return '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="Quoted law and policy on agency duties for federal information handled by private systems and services."><title>Federal information in private services · A-130</title><link rel="stylesheet" href="report.css">'+('' if printing else '<script src="report.js" defer></script>')+'</head><body'+(' class="print-edition"' if printing else '')+'><a class="skip" href="#main">Skip to report</a><header class="masthead"><a class="brand" href="../index.html">A–130 <span>History &amp; authority</span></a><nav aria-label="Main navigation"><a href="../index.html">History</a><a href="../law/index.html">Read the law</a><a href="../a130/index.html">A-130 responsibilities</a><a aria-current="page" href="index.html">Federal information in private services</a></nav></header><div class="layout"><aside class="contents"><details open><summary>In this report</summary><nav aria-label="Report sections">'+''.join(f'<a href="#{id}">{e(title)}</a>' for id,title in nav)+'</nav></details></aside><main id="main">'+content+'<footer><a href="#main">Back to top</a> · <a href="'+('index.html' if printing else 'print.html')+'">'+('Interactive edition' if printing else 'Complete print edition')+'</a><p>Research report. Sources and interpretations are identified separately.</p></footer></main></div></body></html>'

(S/'index.html').write_text(document())
(S/'print.html').write_text(document(True))
(S/'evidence.json').write_text(json.dumps(dict(research_date='2026-10-24',currency_note=LIMITS[2],sources=list(sources.values())),indent=2))
(S/'quotations.json').write_text(json.dumps([dict(q,uses=quote_uses.count(q['id'])) for q in quotes.values()],indent=2,ensure_ascii=False))
(S/'claims.json').write_text(json.dumps(claims,indent=2))
with (S/'evidence.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['id','title','date','kind','url','local','sha256','retrieved','cited_locations'],extrasaction='ignore');w.writeheader();w.writerows(sources.values())
print(f'Built on-behalf report: {len(used)} cited sources, {len(sources)} library entries, {len(claims)} cited discussions, {len(SCENARIOS)} scenarios')

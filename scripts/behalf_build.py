"""Generate the offline on-behalf report; never fetch or change original sources."""
from pathlib import Path
import json, html, hashlib, re, csv
from behalf_content import INTRO, FINDINGS, VERBS, VERB_ANALYSIS, HISTORY, BOUNDARIES, FLOW, SCENARIOS, NIST, HYPOTHESES, LIMITS

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

nav=[('answer','The answer'),('words','Two kinds of “on behalf”'),('history','How it developed'),('boundaries','Five boundaries'),('flows','Follow the information'),('examples','Compare examples'),('nist','What NIST says'),('hypothesis','Test the hypothesis'),('sources','Evidence library'),('limits','Coverage and dates')]
body='<header class="report-title"><h1>'+e(INTRO['title'])+'</h1><p class="deck">'+e(INTRO['deck'])+'</p><p class="report-date">Research checked 24 October 2026; legal editions vary. <a href="#limits">Source dates and limits</a></p><div class="jump-links"><a href="#words">Start with the wording</a><a href="#examples">Compare the five examples</a><a href="print.html">Complete print edition</a></div></header>'
body+='<section id="answer"><h2>The answer</h2><p class="lead">'+e(INTRO['summary'])+'</p>'+prose(FINDINGS)+'</section>'
body+='<section id="words"><h2>Handling information is not the same question as operating a system</h2><p>The nouns and verbs matter. Read each phrase with its object, responsible actor, and legal source.</p><div class="two-duties"><div><h3>Information</h3><p>What is collected or maintained for the agency?</p><span>FISMA §3554(a)(1)(A)(i)</span></div><div><h3>Information systems</h3><p>What is used or operated by or for the agency?</p><span>FISMA §3554(a)(1)(A)(ii)</span></div></div><div class="table-scroll" tabindex="0" role="region" aria-label="Wording across authorities"><table><caption>The terms in their own authorities</caption><thead><tr><th>Authority and object</th><th>Wording, condensed</th><th>What it does</th></tr></thead><tbody>'
for i,(title,obj,words,meaning,id,loc) in enumerate(VERBS):
    body+=f'<tr id="word-{i+1}"><th scope="row">{e(title)}<span class="cell-meta">{e(obj)}</span></th><td>{e(words)}</td><td>{e(meaning)}'+refs([(id,loc)],f'word-{i+1}')+'</td></tr>'
body+='</tbody></table></div>'+prose(VERB_ANALYSIS)+'</section>'
body+='<section id="history"><h2>How the distinction developed</h2><p>This history follows duties and definitions across different authorities. A later document does not automatically repeal an earlier rule or settle its meaning.</p><form id="history-filter" class="controls" hidden><label>Authority<select id="history-kind"><option value="">All authorities</option>'+''.join(f'<option>{e(k)}</option>' for k in dict.fromkeys(h[1] for h in HISTORY))+'</select></label><label>Find a topic<input id="history-query" type="search" placeholder="Try incidental, privacy, or cloud"></label><button type="reset">Reset</button></form><p id="history-count" class="result-count" role="status" hidden></p><p id="history-empty" hidden>No events match. Clear the search or choose all authorities.</p><ol class="history-list">'
for date,kind,id,title,text,rr in HISTORY:
    body+=f'<li id="{id}" data-kind="{e(kind)}"><div class="event-date">{e(date)}<span>{e(kind)}</span></div><div><h3><a class="permalink" href="#{id}" aria-label="Link to {e(title)}">{e(title)}</a></h3><p>{e(text)}</p>'+refs(rr,id)+'</div></li>'
body+='</ol></section>'
body+='<section id="boundaries"><h2>Five boundaries that should not be confused</h2><p>A useful scope statement names all five. They can overlap without being identical.</p><dl class="boundary-list">'
for id,title,question,text,rr in BOUNDARIES:
    body+=f'<div id="boundary-{id}"><dt>{e(title)}</dt><dd><h3>{e(question)}</h3><p>{e(text)}</p>'+refs(rr,'boundary-'+id)+'</dd></div>'
body+='</dl></section><section id="flows"><h2>Follow the information from creation to disposal</h2><p>The same document can move through several systems and several legal regimes. These questions help keep the duties attached to the right activity.</p><ol class="flow-list">'
for i,(title,example,text,rr) in enumerate(FLOW):
    body+=f'<li id="flow-{i+1}"><h3>{e(title)}</h3><p class="flow-example">{e(example)}</p><p>{e(text)}</p>'+refs(rr,f'flow-{i+1}')+'</li>'
body+='</ol></section><section id="examples"><h2>Compare the examples</h2><p>These are source-based illustrations with stated assumptions. They are not findings about a vendor’s actual offering or a substitute for an agency’s decision.</p><div id="scenario-controls" class="scenario-controls" hidden><label for="scenario-select">Choose an example</label><select id="scenario-select"><option value="all">All examples</option>'+''.join(f'<option value="{s["id"]}">{e(s["title"])}</option>' for s in SCENARIOS)+'</select></div><p id="scenario-status" class="result-count" role="status" hidden></p>'
for s in SCENARIOS:
    body+=f'<article class="scenario" id="example-{s["id"]}"><h3>{e(s["title"])}</h3><p class="assumptions"><strong>Assumptions.</strong> {e(s["assumptions"])}</p><figure class="flow-figure"><figcaption>Information and service relationships</figcaption><ol>'+''.join(f'<li>{e(n)}</li>' for n in s['flow'])+'</ol></figure><p class="scenario-answer">'+e(s['conclusion'])+'</p>'+paragraphs(s['paragraphs'])+'<dl class="responsibilities">'+''.join(f'<div><dt>{e(who)}</dt><dd>{e(what)}</dd></div>' for who,what in s['rows'])+'</dl><details class="changes"><summary>What could change the answer?</summary><p>'+e(s['changes'])+'</p></details>'+refs(s['refs'],'example-'+s['id'])+f'<p class="example-link"><a href="#example-{s["id"]}">Link to this example</a></p></article>'
body+='</section><section id="nist"><h2>What current NIST materials say—and what they cite</h2>'+prose(NIST)+'</section><section id="hypothesis"><h2>Test the hypothesis against the sources</h2><p>The evidence supports limits on imposing agency duties across a private business. It does not support a general tenant-only or commercial-service exemption.</p><div class="hypotheses">'
for i,(hyp,result,support,counter,answer,rr) in enumerate(HYPOTHESES):
    body+=f'<article id="hypothesis-{i+1}"><h3>{e(hyp)}</h3><p class="verdict">{e(result)}</p><dl><dt>What supports it</dt><dd>{e(support)}</dd><dt>What limits it</dt><dd>{e(counter)}</dd><dt>Practical conclusion</dt><dd>{e(answer)}</dd></dl>'+refs(rr,f'hypothesis-{i+1}')+'</article>'
body+='</div></section><section id="sources"><h2>Evidence library</h2><p>Each source keeps its own edition and authority. The source links open local originals or complete extracted text. Original HTML snapshots may retain publisher assets; this report has no network dependencies.</p><p class="downloads"><a href="evidence.json" download>Download sources (JSON)</a> · <a href="evidence.csv" download>Sources (CSV)</a> · <a href="claims.json" download>Claim-to-source index</a></p><form class="controls" id="source-filter" hidden><label>Search sources<input type="search" id="source-query" placeholder="Title, authority, or cited section"></label><label>Type<select id="source-kind"><option value="">All types</option>'+''.join(f'<option>{e(k)}</option>' for k in sorted(set(r['kind'] for r in sources.values())))+'</select></label><button type="reset">Reset</button></form><p id="source-count" class="result-count" role="status" hidden></p><p id="source-empty" hidden>No sources match. Clear the search or select all types.</p><div class="sources">'
used={ref['source_id'] for claim in claims for ref in claim['references']}
sources={id:r for id,r in sources.items() if id in used}
for id,r in sorted(sources.items(),key=lambda pair:pair[1]['date']):
    uses=[(c['id'],ref['locator']) for c in claims for ref in c['references'] if ref['source_id']==id]
    r['cited_locations']=list(dict.fromkeys(loc for _,loc in uses))
    original=S/r['local'];assert original.is_file(), original
    assert hashlib.sha256(original.read_bytes()).hexdigest()==r['sha256'],id
    body+=f'<article class="source" id="source-{id}" data-kind="{e(r["kind"])}"><p class="source-type">{e(r["kind"])} · {e(r["date"])}</p><h3>{e(r["title"])}</h3><p class="source-links"><a href="{e(r["local"])}">Local original</a>'
    if r.get('reader'):body+=f' · <a href="{e(r["reader"])}">Read formatted text</a>'
    if r.get('text'):body+=f' · <a href="{e(r["text"])}">Complete extracted text</a>'
    body+=f' · <a href="{e(r["url"])}">Official / original publisher</a></p><details><summary>Locations, provenance, and uses in this report</summary><p>{e(r.get("provenance","Preserved official source; extraction is a reading aid, not a replacement for the original."))}</p><p>Retrieved {e(r["retrieved"])}. SHA-256: <code>{r["sha256"]}</code></p><ul>'+''.join(f'<li><a href="#{claim}">Back to discussion</a> — {e(loc)}</li>' for claim,loc in uses)+'</ul></details></article>'
body+='</div></section><section id="limits"><h2>Coverage, source dates, and open questions</h2><ul class="limits">'+''.join('<li>'+e(x)+'</li>' for x in LIMITS)+'</ul><h3>What still needs an agency-specific answer</h3><p>The actual information, purpose of the service, applicable contract, agency policies, system architecture, provider access, and available assurance determine the result for a real purchase. Where authorities differ in scope, record the reason for the chosen interpretation instead of treating a convenient definition as universal.</p><p>Research and review were performed in this chat, including a separate self-review. No independent legal review or vendor assessment was performed. Research refreshes are manual.</p></section>'

def document(printing=False):
    content=body
    if printing:
        content=re.sub(r'<details([^>]*)>',lambda m:'<details'+m[1]+' open>' if ' open' not in m[1] else m[0],content)
    return '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="A source-based history of federal information, systems operated on behalf of agencies, and commercial cloud responsibilities."><title>On behalf of government · A-130</title><link rel="stylesheet" href="report.css">'+('' if printing else '<script src="report.js" defer></script>')+'</head><body'+(' class="print-edition"' if printing else '')+'><a class="skip" href="#main">Skip to report</a><header class="masthead"><a class="brand" href="../index.html">A–130 <span>History &amp; authority</span></a><nav aria-label="Main navigation"><a href="../index.html">History</a><a href="../law/index.html">Read the law</a><a href="../a130/index.html">A-130 responsibilities</a><a aria-current="page" href="index.html">On behalf of government</a></nav></header><div class="layout"><aside class="contents"><details open><summary>In this report</summary><nav aria-label="Report sections">'+''.join(f'<a href="#{id}">{e(title)}</a>' for id,title in nav)+'</nav></details></aside><main id="main">'+content+'<footer><a href="#main">Back to top</a> · <a href="'+('index.html' if printing else 'print.html')+'">'+('Interactive edition' if printing else 'Complete print edition')+'</a><p>Local research report. Sources and interpretations are identified separately.</p></footer></main></div></body></html>'

(S/'index.html').write_text(document())
(S/'print.html').write_text(document(True))
(S/'evidence.json').write_text(json.dumps(dict(research_date='2026-10-24',currency_note=LIMITS[2],sources=list(sources.values())),indent=2))
(S/'claims.json').write_text(json.dumps(claims,indent=2))
with (S/'evidence.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['id','title','date','kind','url','local','sha256','retrieved','cited_locations'],extrasaction='ignore');w.writeheader();w.writerows(sources.values())
print(f'Built on-behalf report: {len(sources)} cited sources, {len(claims)} cited discussions, {len(SCENARIOS)} scenarios')

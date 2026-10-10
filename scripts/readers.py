"""Faithful, scoped HTML reading aids; originals and raw extracts stay unchanged."""
import html,re,json
import fitz
E=lambda s:html.escape(str(s),quote=True)
SCOPES={
 'sp50085':(5,18,None,None,'Foreword, abstract, contents, guidance and bibliography; cover and publisher back matter omitted.'),
 'a130-2016':(1,85,None,None,'Complete A-130 circular and its appendices.'),
 'fips31':(2,4,None,None,'Foreword and standards announcement: authority, purpose and applicability.'),
 'a130-1985':(288,309,None,None,'A-130 notice only: 50 FR 52730–52751.'),
 'fips12':(34,37,None,r'4\.7\. BOB','A-71 reproduction only: §4.6 of FIPS 12.'),
 'clinger':(495,519,r'DIVISION E',None,'Division E: Information Technology Management Reform Act of 1996.'),
 'gisra':(268,277,r'Subtitle G',r'Subtitle H','Title X, Subtitle G: Government Information Security Reform.'),
 'fisma2002':(48,63,r'TITLE III',r'TITLE IV','Title III: Federal Information Security Management Act of 2002.'),
 'fedramp-act':(1055,1064,r'Subtitle C',r'Subtitle D','Subtitle C: FedRAMP Authorization Act only.')}
def paragraphs(text):
 # Reflow line wraps; retain spelling, punctuation, and hyphens from the source.
 out=[];buf=[]
 def flush():
  if buf:out.append('<p>'+E(' '.join(buf))+'</p>');buf.clear()
 for line in text.splitlines():
  s=line.strip()
  if not s:flush();continue
  heading=len(s)<105 and len(s)>3 and s.isupper() and bool(re.search('[A-Z]',s))
  start=bool(re.match(r'(?:SEC\. \d+\.|\d+\. |\([a-zA-Z0-9]+\) |[a-z]\. |[•●] )',s))
  if heading:
   flush()
   if out and out[-1].endswith('</h3>'):out[-1]=out[-1][:-5]+' '+E(s)+'</h3>'
   else:out.append('<h3>'+E(s)+'</h3>')
  else:
   if re.match(r'(?:agency|action|summary|date)\s*:',s,re.I):start=True
   if start or (buf and re.search(r'[.!?][”’"\']?$',buf[-1]) and len(' '.join(buf))>260):flush()
   buf.append(s)
 flush();return ''.join(out)
def build_readers(site,records):
 dest=site/'read';dest.mkdir(exist_ok=True);audit=[]
 for r in records:
  if not r.get('local','').endswith('.pdf'):continue
  raw=(site/r['extracted']).read_text();chunks=re.findall(r'\[PDF page (\d+)([^\]]*)\]\s*([\s\S]*?)(?=\[PDF page |\Z)',raw)
  pages=[(int(n),label,t)for n,label,t in chunks];scope='Complete standalone document.'
  if r['id'] in SCOPES:
   lo,hi,start,end,scope=SCOPES[r['id']];pages=[p for p in pages if lo<=p[0]<=hi]
   for index,pattern,after in [(0,start,True),(-1,end,False)]:
    if pattern:
     n,label,t=pages[index];m=re.search(pattern,t);assert m,(r['id'],pattern)
     pages[index]=(n,label,t[m.start():] if after else t[:m.start()])
  elif r.get('pages',0)>80:
   pages=[p for p in pages if re.search(r'A[–−—-]\s*130',p[2],re.I)]
   scope='Selected pages explicitly referencing A-130; intervening pages are omitted. This is an excerpt, not the complete publication.'
   if not pages:continue
  assert pages,r['id']
  repaired=[];pdf=None;body=[]
  for n,label,t in pages:
   # Old OCR text sometimes lost virtually all spaces in the original export.
   if len(t)>150 and len(t.split())<len(t)/35 and (r['id'] not in SCOPES or r['id']=='sp50085'):
    if pdf is None:pdf=fitz.open(site/r['local'])
    t='\n\n'.join(b[4] for b in pdf[n-1].get_text('blocks') if b[6]==0);repaired.append(n)
   body.append(f'<section class="source-page" id="page-{n}" aria-labelledby="label-{n}"><div class="page-label"><h2 id="label-{n}">PDF page {n}{E(label)}</h2><a href="../{E(r["local"])}#page={n}">View original page ↗</a></div>{paragraphs(t) if t.strip() else "<p class=muted>No text was extracted from this page. See the original PDF.</p>"}</section>')
  if pdf:pdf.close()
  r['reader']='read/'+r['id']+'.html';r['reader_scope']=scope;r['reader_pages']=[p[0]for p in pages]
  nav=''.join(f'<a href="#page-{n}">{n}</a>'for n,_,_ in pages)
  page=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{E(r['title'])} · Reading copy</title><link rel="stylesheet" href="../reader.css"></head><body><a class="skip" href="#text">Skip to document text</a><header><a href="../index.html#doc-{E(r['id'])}">← Back to research report</a><p class="eyebrow">Source reader · {E(r['date'])}</p><h1>{E(r['title'])}</h1><p class="scope">{E(scope)}</p><nav class="downloads" aria-label="Source files"><a href="../{E(r['local'])}">Original PDF</a><a href="../{E(r['extracted'])}" download>Raw text ↓</a><a href="{E(r['url'])}">Official source ↗</a></nav><aside class="notice"><strong>Formatted reading copy</strong><p>Text is reflowed for smaller screens. Original PDF page numbers are retained. OCR spelling, reading order, tables and line-end hyphens may be imperfect; consult the original before quoting. This page is not an authoritative transcription.</p>{'<p>Spacing restored from the existing PDF text layer on pages '+E(', '.join(map(str,repaired)))+'. No AI rewriting or spelling correction was applied.</p>' if repaired else ''}</aside><details class="page-index"><summary>Jump to a PDF page · {len(pages)} included</summary><nav aria-label="PDF pages">{nav}</nav></details></header><main id="text">{''.join(body)}</main><footer><a href="#">Back to top ↑</a> · <a href="../index.html#doc-{E(r['id'])}">Return to source record</a></footer></body></html>'''
  (site/r['reader']).write_text(page);audit.append({'id':r['id'],'pages':r['reader_pages'],'scope':scope,'spacing_recovered_pages':repaired})
 (site/'reader-manifest.json').write_text(json.dumps(audit,indent=2));print('Built',len(audit),'scoped PDF readers')

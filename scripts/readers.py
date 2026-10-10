"""Faithful, scoped HTML reading aids; originals and raw extracts stay unchanged."""
import html,re,json
import fitz
from content import READER_NOTICE,READER_SPACING
E=lambda s:html.escape(str(s),quote=True)
SCOPES={
 'sp50085':(5,18,None,None,'Foreword, abstract, contents, guidance, and bibliography. Covers and publisher pages are omitted.'),
 'a130-2016':(1,85,None,None,'Complete A-130 circular and its appendices.'),
 'fips31':(2,4,None,None,'Foreword and standards announcement: authority, purpose and applicability.'),
 'a130-1985':(288,309,None,None,'A-130 notice, 50 FR 52730–52751.'),
 'fips12':(34,37,None,r'4\.7\. BOB','A-71 reproduction only: §4.6 of FIPS 12.'),
 'clinger':(495,519,r'DIVISION E',None,'Division E: Information Technology Management Reform Act of 1996.'),
 'gisra':(268,277,r'Subtitle G',r'Subtitle H','Title X, Subtitle G: Government Information Security Reform.'),
 'fisma2002':(48,63,r'TITLE III',r'TITLE IV','Title III: Federal Information Security Management Act of 2002.'),
 'fedramp-act':(1055,1064,r'Subtitle C',r'Subtitle D','Subtitle C: FedRAMP Authorization Act only.')}
def paragraphs(text):
 """Recognize source labels without inventing headings or rewriting their words."""
 out=[];buf=[]
 def flush():
  if buf:out.append('<p>'+E(' '.join(buf))+'</p>');buf.clear()
 def title_like(s):
  words=re.findall(r"[A-Za-z][A-Za-z’'-]*",s)
  return bool(words) and len(words)<=15 and sum(w[0].isupper() for w in words)/len(words)>=.55
 lines=text.splitlines();i=0
 while i<len(lines):
  s=lines[i].strip();i+=1
  if not s:flush();continue
  if re.fullmatch(r'\d+\.',s) and i<len(lines) and lines[i].strip():s+=' '+lines[i].strip();i+=1
  level=None;heading=None;rest=''
  running=bool(re.search(r'Federal Register|FIPS PUB|PUBLIC LAW|\bSTAT\.|\bUSC\b|^CIRCULAR NO',s,re.I))
  numbered=None if running else re.match(r'^((?:Section\s+)?\d+(?:\.\d+)*[.)]?\s+|[a-z]\.\s+)(.+)$',s)
  if numbered:
   prefix,tail=numbered.groups()
   split=re.match(r'^(.{2,95}?[.:])\s+(.+)$',tail)
   if tail.endswith('?') and len(tail)<180:heading=s
   elif split and title_like(split[1]):heading=prefix+split[1];rest=split[2]
   elif len(s)<110 and not re.search(r'[;,]$',s) and title_like(tail) and not re.search(r'\b(shall|must|means|should)\b',tail,re.I):heading=s
   if heading:level=3 if re.match('[a-z]\\.',prefix) or re.search(r'\d\.\d',prefix) else 2
  if heading is None and not running and re.match(r'^(?:Appendix\s+[A-ZIVX]+\b|TITLE\s+[IVX]+\b|Subtitle\s+[A-Z]\b|SEC\.\s+\d+\.)',s) and (s.isupper() or (title_like(s) and not re.search(r'\b(with|to emphasize|The two|which|as discussed)\b',s))):
   heading=s;level=2
   # Join wrapped all-capital legislative section names, but not the next section.
   while i<len(lines) and lines[i].strip().isupper() and len(heading)<160 and not re.match(r'^(?:SEC\.|TITLE|APPENDIX)',lines[i].strip()) and not heading.endswith('.'):
    heading+=' '+lines[i].strip();i+=1
  if heading is None and re.fullmatch(r'(?:Foreword|Abstract|Contents|Table of Contents|Executive Summary|Introduction|Background|Purpose|Scope|References|Bibliography|Conclusion|Conclusions|Acknowledgments)',s,re.I) and s[0].isupper():heading=s;level=2
  if heading is None and not running and 2<=len(s.split())<=15 and re.match(r'^[A-Z]',s) and len(s)<105 and len(s)>3 and s.isupper() and re.search('[A-Z]',s) and not re.search(r'(?:Federal Register|FIPS PUB|PUBLIC LAW|STAT\.|CIRCULAR NO\.|TO THE HEADS|MEMORANDUM FOR|OMB Circular)',s,re.I):
   heading=s;level=2
   while i<len(lines) and lines[i].strip().isupper() and 0<len(lines[i].strip())<105 and len(heading)<150 and not re.match(r'^(?:SEC\.|TITLE|APPENDIX)',lines[i].strip()) and not re.search(r'FIPS PUB|STAT\.|USC|PUBLIC LAW',lines[i],re.I):heading+=' '+lines[i].strip();i+=1
  label=re.match(r'^(agency|action|summary|dates?|subject|supplementary information|for further information contact)\s*:\s*(.*)$',s,re.I)
  if label and heading is None:heading=label[1]+':';rest=label[2];level=3
  if heading:
   flush();out.append(f'<h{level} class="document-heading">'+E(heading)+f'</h{level}>')
   if rest:buf.append(rest)
  else:
   start=bool(re.match(r'(?:\d+\. |\([a-zA-Z0-9]+\) |[a-z]\. |[•●] )',s))
   if start or (buf and re.search(r'[.!?][”’"\']?$',buf[-1]) and len(' '.join(buf))>260):flush()
   buf.append(s)
 flush();return ''.join(out)
def build_readers(site,records):
 dest=site/'read';dest.mkdir(exist_ok=True);audit=[]
 for r in records:
  if not r.get('local','').endswith('.pdf'):continue
  raw=(site/r['extracted']).read_text();chunks=re.findall(r'\[PDF page (\d+)([^\]]*)\]\s*([\s\S]*?)(?=\[PDF page |\Z)',raw)
  pages=[(int(n),label,t)for n,label,t in chunks];scope='Complete document.'
  if r['id'] in SCOPES:
   lo,hi,start,end,scope=SCOPES[r['id']];pages=[p for p in pages if lo<=p[0]<=hi]
   for index,pattern,after in [(0,start,True),(-1,end,False)]:
    if pattern:
     n,label,t=pages[index];m=re.search(pattern,t);assert m,(r['id'],pattern)
     pages[index]=(n,label,t[m.start():] if after else t[:m.start()])
  elif r.get('pages',0)>80:
   pages=[p for p in pages if re.search(r'A[–−—-]\s*130',p[2],re.I)]
   scope='Selected pages that mention A-130. Other pages are omitted.'
   if not pages:continue
  assert pages,r['id']
  repaired=[];pdf=None;body=[]
  for n,label,t in pages:
   # Old OCR text sometimes lost virtually all spaces in the original export.
   if len(t)>150 and len(t.split())<len(t)/35 and (r['id'] not in SCOPES or r['id']=='sp50085'):
    if pdf is None:pdf=fitz.open(site/r['local'])
    t='\n\n'.join(b[4] for b in pdf[n-1].get_text('blocks') if b[6]==0);repaired.append(n)
   rendered=paragraphs(t)
   if r['id']=='a130-2016' and n==1:
    rendered=re.sub(r'<h[23] class="document-heading">(.*?)</h[23]>',r'<p class="source-contents-entry">\1</p>',rendered)
   if r['id']=='a130-2000' and n==1 and '1. Purpose:' in t:
    front,actual=t.split('1. Purpose:',1)
    rendered=re.sub(r'<h[23] class="document-heading">(.*?)</h[23]>',r'<p class="source-contents-entry">\1</p>',paragraphs(front))+paragraphs('1. Purpose:'+actual)
   body.append(f'<section class="source-page" id="page-{n}" aria-labelledby="label-{n}"><div class="page-label"><span id="label-{n}">PDF page {n}{E(label)}</span><a href="../{E(r["local"])}#page={n}">View original page ↗</a></div>{rendered if t.strip() else "<p class=muted>No text was extracted from this page. See the original PDF.</p>"}</section>')
  if pdf:pdf.close()
  headings=[]
  def anchor(m):
   level,title=m.groups();key='section-'+str(len(headings)+1);headings.append((key,title,level))
   return f'<h{level} class="document-heading" id="{key}">{title}</h{level}>'
  body=[re.sub(r'<h([23]) class="document-heading">(.*?)</h[23]>',anchor,part) for part in body]
  contents='<details class="section-index" open><summary>Document sections</summary><nav aria-label="Document sections"><ol>'+''.join(f'<li class="depth-{level}"><a href="#{key}">{title}</a></li>' for key,title,level in headings)+'</ol></nav></details>' if headings else ''
  r['reader']='read/'+r['id']+'.html';r['reader_scope']=scope;r['reader_pages']=[p[0]for p in pages]
  nav=''.join(f'<a href="#page-{n}">{n}</a>'for n,_,_ in pages)
  page=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{E(r['title'])} · Reading copy</title><link rel="stylesheet" href="../reader.css"></head><body><a class="skip" href="#text">Skip to document text</a><header><a href="../index.html#doc-{E(r['id'])}">← Back to research report</a><p class="eyebrow">Document · {E(r['date'])}</p><h1>{E(r['title'])}</h1><p class="scope">{E(scope)}</p><nav class="downloads" aria-label="Source files"><a href="../{E(r['local'])}">Original PDF</a><a href="../{E(r['extracted'])}" download>Raw text ↓</a><a href="{E(r['url'])}">Official source ↗</a></nav><details class="notice"><summary>About this text</summary><p>{E(READER_NOTICE)}</p>{'<p>'+E(READER_SPACING.format(pages=', '.join(map(str,repaired))))+'</p>' if repaired else ''}</details>{contents}<details class="page-index"><summary>Jump to a PDF page · {len(pages)} included</summary><nav aria-label="PDF pages">{nav}</nav></details></header><main id="text">{''.join(body)}</main><footer><a href="#">Back to top ↑</a> · <a href="../index.html#doc-{E(r['id'])}">Return to source record</a></footer></body></html>'''
  (site/r['reader']).write_text(page);audit.append({'id':r['id'],'pages':r['reader_pages'],'scope':scope,'spacing_recovered_pages':repaired})
 (site/'reader-manifest.json').write_text(json.dumps(audit,indent=2));print('Built',len(audit),'scoped PDF readers')

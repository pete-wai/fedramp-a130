"""Check quotations against bounded primary originals and retained Code clauses."""
import json,re,hashlib
from pathlib import Path
import fitz
from bs4 import BeautifulSoup
from history_sources import norm
R=Path(__file__).resolve().parents[1];S=R/'site/proposed-fedramp-use'
quotes=json.loads((S/'quotations.json').read_text());sources=json.loads((S/'sources.json').read_text())
for q in quotes:
 p=R/q['source_file']
 if p.suffix=='.pdf':
  with fitz.open(p) as d:text=' '.join(norm(d[i-1].get_text())for i in q['pages'])
 else:text=norm(p.read_text())
 assert norm(q['text']) in text,q['id']
 assert 'CHAPTER THREE PAGE' not in q['text'],q['id']
for s in sources:
 assert hashlib.sha256((S/s['local']).read_bytes()).hexdigest()==s['sha256'],s['id']
 if s.get('text'):
  text=BeautifulSoup((S/s['local']).read_text(),'html.parser').select_one('article').get_text(' ',strip=True)
  assert text==(S/s['text']).read_text(),s['id']
soup=BeautifulSoup((S/'index.html').read_text(),'html.parser')
for q in quotes:
 assert norm(soup.select_one('#quote-'+q['id']+' blockquote').get_text(' '))==norm(q['text']),q['id']
assert len(soup.select('.quotation'))==len(quotes)
clauses={
 '44-3554':['information collected or maintained by or on behalf of the agency;','information systems used or operated by an agency or by a contractor of an agency or other organization on behalf of an agency;','periodically testing and evaluating information security controls and techniques to ensure that they are effectively implemented;'],
 '44-3608':['a standardized, reusable approach to security assessment and authorization'],
 '44-3609':['consistent with standards and guidelines established by the Director of the National Institute of Standards and Technology and relevant statutes;'],
 '44-3613':['shall be presumed adequate for use in an agency authorization to operate cloud computing products and services.','the responsibility of any agency to ensure compliance with subchapter II of chapter 35','a demonstrable need for additional security requirements','the head of the agency shall provide a copy of its authorization to operate letter']}
for id,tests in clauses.items():
 t=norm(BeautifulSoup((R/'site/law'/f'{id}.html').read_text(),'html.parser').get_text(' '))
 for phrase in tests:assert phrase in t,(id,phrase)
result=dict(passed=True,sourceMatchedQuotes=len(quotes),sourceHashes=len(sources),webArticleExtractions=5,currentCodeClauses=sum(map(len,clauses.values())),printedQuotesMatch=True)
(R/'output/proposed-fedramp-use/quotation-check.json').write_text(json.dumps(result,indent=2)+'\n');print(result)

"""Check displayed quotations against bounded original passages, not authored prose."""
from pathlib import Path
import json,re,html,xml.etree.ElementTree as ET
import fitz
from bs4 import BeautifulSoup
R=Path(__file__).resolve().parents[1]
def norm(t):
    t=re.sub(r'(agency|non|organization)-\s*\n\s*',r'\1-',t)
    t=re.sub(r'(?<=\w)-\s*\n\s*(?=\w)','',t)
    t=re.sub(r'\s+([,.;:])',r'\1',t)
    return re.sub(r'\s+',' ',t).strip()
quotes=json.loads((R/'data/on-behalf/history-quotations.json').read_text())
assert len({q['id'] for q in quotes})==len(quotes)
pages={}
for q in quotes:
    file=R/q['source_file']
    if file.suffix=='.pdf':
        pdf=fitz.open(file);text=' '.join(pdf[i-1].get_text() for i in q['pages'])
    elif file.suffix=='.xml':text=' '.join(ET.parse(file).getroot().itertext())
    else:text=BeautifulSoup(file.read_text(),'html.parser').get_text(' ')
    assert norm(q['text']) in norm(text),q['id']
for name in ['index.html','print.html']:
    soup=BeautifulSoup((R/'site/on-behalf'/name).read_text(),'html.parser')
    rendered=[norm(x.get_text(' ')) for x in soup.select('.quotation blockquote')]
    assert len(rendered)==len(quotes),(name,len(rendered),len(quotes))
    for q in quotes:assert norm(q['text']) in rendered,(name,q['id'])
    ids={x['id'] for x in soup.select('[id]')}
    assert set(json.loads((R/'data/on-behalf/prior-anchors.json').read_text()))<=ids
# Check unchanged wording claims against separately preserved editions.
by={q['id']:q for q in quotes}
for a,b in [('f02-dual','f14-dual'),('sa9-2006','sa9-2007'),('rmf10-external','rmf14-external')]:
    assert norm(by[a]['text'])==norm(by[b]['text']),(a,b)
current=norm(BeautifulSoup((R/'site/law/44-3554.html').read_text(),'html.parser').get_text(' '))
for clause in ['information collected or maintained by or on behalf of the agency;', 'information systems used or operated by an agency or by a contractor of an agency or other organization on behalf of an agency;']:
    assert clause in current,clause
out={'passed':True,'originalMatchedQuotes':len(quotes),'visibleInBothEditions':True,'priorAnchorsPreserved':True,'continuityComparisons':3,'twoFismaClausesMatchCollectedCurrentCode':True,'normalization':'Whitespace, punctuation spacing, and line-end hyphenation; compound agency-/non-/organization- preserved.'}
(R/'output/on-behalf/quotation-check.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))

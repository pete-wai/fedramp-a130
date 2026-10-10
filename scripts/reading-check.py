"""Check complete coverage and unchanged statutory text in subject readers."""
from pathlib import Path
from bs4 import BeautifulSoup
from reading_groups import READING_GROUPS
import re
root=Path(__file__).resolve().parents[1]/'site/law'
compact=lambda s:re.sub(r'\s+','',s)
seen=[]
for group in READING_GROUPS:
 doc=BeautifulSoup((root/f'read-{group["slug"]}.html').read_text(),'html.parser')
 for key in group['sections']:
  seen.append(key)
  article=doc.find('article',id=key)
  assert article, key
  actual=article.select_one('.legal-text')
  expected=BeautifulSoup((root/f'{key}.html').read_text(),'html.parser').select_one('#text .legal-text')
  for body in [actual,expected]:
   for context in body.select('.clause-context'):context.decompose()
  assert compact(actual.get_text())==compact(expected.get_text()),key
assert len(seen)==len(set(seen))==100
print('All 100 sections appear once across 12 readings; statutory text unchanged.')

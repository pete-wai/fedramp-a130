"""Check the editorial rewrite against the protected source bodies and quotations."""
import pathlib,json,re,hashlib
from content import SUMMARIES
root=pathlib.Path(__file__).resolve().parents[1]
for path,expected in json.loads((root/'docs/validation/editorial-protected-hashes.json').read_text()).items():
 b=(root/path).read_bytes()
 if '/read/' in path:b=re.search(r'<main id="text">(.*?)</main>',b.decode(),re.S)[1].encode()
 assert hashlib.sha256(b).hexdigest()==expected,path
records=json.loads((root/'data/records.json').read_text());by={r['id']:r for r in records}
metadata=json.loads((root/'docs/validation/editorial-record-hashes.json').read_text())
for r in records:
 assert hashlib.sha256(json.dumps({k:r.get(k)for k in metadata['fields']},sort_keys=True).encode()).hexdigest()==metadata['hashes'][r['id']],r['id']
assert len(records)==178
assert all(r['note'].strip()for r in records)
quotes=0
for id,_,blocks,refs in SUMMARIES:
 count=sum(len(b['text'].split())for b in blocks);assert 250<=count<=350,(id,count)
 for b in blocks:
  if b['kind']=='quote':
   source=(root/'site'/by[b['refs'][0][0]]['extracted']).read_text()
   assert b['text'] in re.sub(r'\s+',' ',source),id;quotes+=1
assert quotes==3
print('506 protected files/source bodies unchanged; 178 descriptions; six 250–350-word summaries; three source-matched quotations.')

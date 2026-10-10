"""Manually reproduce the law collection in a staging directory; never replace reviewed files.

Usage: uv run --locked python scripts/collect_law.py --stage /tmp/law-source-check
A changed remote file is retained in staging and reported as a hash mismatch for review.
"""
import argparse,concurrent.futures,hashlib,json,pathlib,urllib.request
R=pathlib.Path(__file__).resolve().parents[1]
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--stage',required=True,type=pathlib.Path);args=p.parse_args();stage=args.stage.resolve()
 if stage==R or R in stage.parents:raise SystemExit('Use a staging directory outside the repository.')
 stage.mkdir(parents=True,exist_ok=True);sources=json.loads((R/'data/law/sources.json').read_text())
 def fetch(src):
  destination=stage/pathlib.Path(src['file']).name
  if destination.exists():return dict(id=src['id'],status='already staged; left unchanged')
  try:
   data=urllib.request.urlopen(urllib.request.Request(src['url'],headers={'User-Agent':'fedramp-a130 source verification'}),timeout=60).read()
   if b'Page Not Found' in data:raise ValueError('Publisher returned an error page')
   destination.write_bytes(data);digest=hashlib.sha256(data).hexdigest()
   return dict(id=src['id'],status='matches reviewed source' if digest==src['sha256'] else 'changed; review before import',sha256=digest,file=str(destination))
  except Exception as error:return dict(id=src['id'],status='retrieval failed',error=str(error))
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:results=list(pool.map(fetch,sources))
 (stage/'retrieval-report.json').write_text(json.dumps(results,indent=2)+'\n')
 print(json.dumps({status:sum(x['status']==status for x in results) for status in sorted({x['status'] for x in results})},indent=2))
if __name__=='__main__':main()

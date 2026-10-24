import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
const base=path.resolve('site/on-behalf');
const hash=bytes=>crypto.createHash('sha256').update(bytes).digest('hex');
const evidence=JSON.parse(fs.readFileSync(path.join(base,'evidence.json')));
const quotes=JSON.parse(fs.readFileSync(path.join(base,'quotations.json')));
assert.equal(quotes.length,40);
const claims=JSON.parse(fs.readFileSync(path.join(base,'claims.json')));
const sources=new Map(evidence.sources.map(r=>[r.id,r]));
const original=JSON.parse(fs.readFileSync('data/on-behalf/protected-baseline.json'));
for(const [file,sha] of Object.entries(original))assert.equal(hash(fs.readFileSync(file)),sha,file);
for(const r of sources.values())assert.equal(hash(fs.readFileSync(path.resolve(base,r.local))),r.sha256,r.id);
let links=0;
for(const file of ['index.html','print.html']){
 const full=path.join(base,file),html=fs.readFileSync(full,'utf8');
 const ids=[...html.matchAll(/\bid="([^"]+)"/g)].map(m=>m[1]);
 assert.equal(ids.length,new Set(ids).size,'duplicate ID');
 assert.equal((html.match(/class="scenario"/g)||[]).length,5);
 assert.equal((html.match(/class="quotation"/g)||[]).length,quotes.length);
 for(const q of quotes){assert(q.uses>0,q.id);assert(sources.has(q.source_id),q.id);}
 assert(!/<(?:script|link)[^>]+(?:src|href)="https?:/.test(html),'network dependency');
 for(const m of html.matchAll(/(?:href|src)="([^"]+)"/g)){
  const href=m[1];if(/^https?:/.test(href))continue;
  const [local,anchor]=href.split('#');const target=local?path.resolve(base,local):full;
  assert(fs.existsSync(target),href);
  if(anchor&&target.endsWith('.html'))assert(fs.readFileSync(target,'utf8').includes(`id="${anchor}"`),href);
  links++;
 }
 for(const c of claims){assert(ids.includes(c.id),c.id);assert(c.references.length);for(const r of c.references){assert(sources.has(r.source_id),r.source_id);assert(r.locator.trim().length>0);}}
 if(file==='print.html')assert.equal((html.match(/<details/g)||[]).length,(html.match(/<details[^>]* open/g)||[]).length,'print disclosures must be open');
}
const result={passed:true,protectedSourceFiles:Object.keys(original).length,librarySources:sources.size,citedSources:new Set(claims.flatMap(c=>c.references.map(r=>r.source_id))).size,verifiedQuotationCount:quotes.length,citedDiscussions:claims.length,localLinksAndAnchors:links};
fs.mkdirSync('output/on-behalf',{recursive:true});fs.writeFileSync('output/on-behalf/static-check.json',JSON.stringify(result,null,2));console.log(JSON.stringify(result));

import fs from 'node:fs';import path from 'node:path';import crypto from 'node:crypto';import assert from 'node:assert/strict';
const root=path.resolve('site');const html=fs.readFileSync(path.join(root,'index.html'),'utf8');const ids=[...html.matchAll(/\bid="([^"]+)"/g)].map(x=>x[1]);assert.equal(ids.length,new Set(ids).size,'duplicate IDs');let links=0;
for(const m of html.matchAll(/(?:href|src)="([^"]+)"/g)){const href=m[1];if(/^https?:/.test(href))continue;if(href.startsWith('#'))assert(ids.includes(href.slice(1)),`missing anchor ${href}`);else assert(fs.existsSync(path.join(root,href.split("#")[0])),`missing file ${href}`);links++;}
const records=JSON.parse(fs.readFileSync(path.join(root,'manifest.json')));let hashes=0;for(const r of records){if(r.local){const b=fs.readFileSync(path.join(root,r.local));assert.equal(crypto.createHash('sha256').update(b).digest('hex'),r.sha256,r.id);if(r.local.endsWith('.pdf'))assert.equal(b.subarray(0,4).toString(),'%PDF');hashes++;}assert(r.date<='2026-10-10');}
assert(!/<(?:script|link)[^>]+(?:src|href)="https?:/.test(html),'network dependency');console.log(JSON.stringify({records:records.length,localLinksAndAnchors:links,verifiedHashes:hashes,duplicateIds:0,passed:true},null,2));
let readers=0;for(const r of records.filter(r=>r.reader)){const file=path.join(root,r.reader);const text=fs.readFileSync(file,'utf8');const pageIds=[...text.matchAll(/id="page-(\d+)"/g)].map(m=>Number(m[1]));assert.deepEqual(pageIds,r.reader_pages,r.id);for(const m of text.matchAll(/(?:href|src)="([^"]+)"/g)){const url=m[1];if(/^https?:/.test(url)||url==='#')continue;const [local,anchor]=url.split('#');const target=local?path.resolve(path.dirname(file),local):file;assert(fs.existsSync(target),url);if(anchor&&!target.endsWith('.pdf'))assert(fs.readFileSync(target,'utf8').includes(`id="${anchor}"`),url);}assert(!/<(?:script|link)[^>]+(?:src|href)="https?:/.test(text));readers++;}
for(const [id,start,end] of [['a130-1985',288,309],['fips12',34,37],['fedramp-act',1055,1064],['gisra',268,277],['fisma2002',48,63],['clinger',495,519]]){const r=records.find(r=>r.id===id);assert.equal(r.reader_pages[0],start);assert.equal(r.reader_pages.at(-1),end);}
for(const [id,excluded]of [['fips12','4.7. BOB'],['gisra','Subtitle H'],['fisma2002','TITLE IV'],['fedramp-act','Subtitle D']])assert(!fs.readFileSync(path.join(root,records.find(r=>r.id===id).reader),'utf8').includes(excluded),`unrelated material: ${id}`);
console.log(JSON.stringify({readers,readerLinksAndScopes:true}));

// Validate the law explorer using built-in Node APIs in GitHub Actions.
await import("./law-check.mjs");

// Protect source provenance and links in the on-behalf report.
await import("./behalf-check.mjs");

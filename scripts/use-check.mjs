import fs from 'node:fs';import path from 'node:path';import crypto from 'node:crypto';import assert from 'node:assert/strict';
const base=path.resolve('site/proposed-fedramp-use');const html=fs.readFileSync(path.join(base,'index.html'),'utf8');
const ids=[...html.matchAll(/\bid="([^"]+)"/g)].map(m=>m[1]);assert.equal(new Set(ids).size,ids.length);
let links=0;for(const [,url]of html.matchAll(/(?:href|src)="([^"]+)"/g)){if(/^https?:/.test(url))continue;const [file,anchor]=url.split('#');const target=file?path.resolve(base,file):path.join(base,'index.html');assert(fs.existsSync(target),url);if(anchor&&!target.endsWith('.pdf'))assert(fs.readFileSync(target,'utf8').includes(`id="${anchor}"`),url);links++;}
const sources=JSON.parse(fs.readFileSync(path.join(base,'sources.json')));for(const s of sources)assert.equal(crypto.createHash('sha256').update(fs.readFileSync(path.resolve(base,s.local))).digest('hex'),s.sha256,s.id);
const qs=JSON.parse(fs.readFileSync(path.join(base,'quotations.json')));assert.equal(qs.length,41);for(const q of qs)assert(ids.includes('quote-'+q.id));
const fields=JSON.parse(fs.readFileSync(path.join(base,'fields.json')));assert.equal(fields.length,18);assert.equal(new Set(fields.map(f=>f.id)).size,18);for(const f of fields)assert(html.includes(`name="${f.id}"`));
assert.equal([...html.matchAll(/class="step"/g)].length,8);assert(!/<(?:script|link)[^>]+(?:src|href)="https?:/.test(html));
console.log(JSON.stringify({proposedFedrampUse:true,steps:8,quotes:qs.length,fields:fields.length,sourceHashes:sources.length,localLinks:links,passed:true}));

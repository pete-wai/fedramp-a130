import fs from 'node:fs';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
import {chromium} from 'playwright';
const base='https://pete-wai.github.io/fedramp-a130/';
const files=['index.html','law/index.html','on-behalf/index.html','on-behalf/print.html','on-behalf/report.css','on-behalf/report.js','on-behalf/evidence.json','on-behalf/evidence.csv','on-behalf/claims.json','on-behalf/quotations.json','on-behalf/coverage.json','on-behalf/relationships.json','on-behalf/sources/nara2016.pdf','on-behalf/sources/sp800182.pdf','on-behalf/sources/rmf2010.pdf','on-behalf/sources/rmf2014.pdf','on-behalf/sources/sp60-2004.pdf','on-behalf/sources/sp60-2008.pdf','on-behalf/sources/nist53changes2025.pdf'];
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');const results=[];
for(const file of files){const response=await fetch(base+file);assert(response.ok,`${file}: ${response.status}`);assert.equal(hash(Buffer.from(await response.arrayBuffer())),hash(fs.readFileSync('site/'+file)),file);results.push(file);}
const browser=await chromium.launch({headless:true,executablePath:'/Users/codex/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
try{
 for(const width of [1440,390]){
  const page=await browser.newPage({viewport:{width,height:1000}});await page.goto(base+'on-behalf/index.html');
  assert.equal(await page.locator('.quotation:visible').count(),80);assert.equal(await page.locator('.milestone:visible').count(),41);
  assert.equal(await page.locator('h1').textContent(),'Protecting federal information and systems');assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  await page.locator('#history-kind').selectOption('Comment response');assert.equal(await page.locator('.milestone:visible').count(),1);
  await page.locator('#authority-map a[href="#quote-f02-deliver"]').click();await page.waitForFunction(()=>document.querySelectorAll('.milestone:not([hidden])').length===41);assert(await page.locator('#quote-f02-deliver').isVisible());
  await page.goto(base+'on-behalf/index.html#source-sp60-2004');assert(await page.locator('#source-sp60-2004').isVisible());await page.close();
 }
}finally{await browser.close();}
fs.writeFileSync('output/on-behalf/history-live-check.json',JSON.stringify({date:new Date().toISOString(),base,matchedFiles:results,browserWidths:[1440,390],passed:true},null,2));console.log('19 live hashes and desktop/mobile interactions passed.');

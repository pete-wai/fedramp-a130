import {chromium} from 'playwright';import assert from 'node:assert/strict';import fs from 'node:fs';
const root='http://127.0.0.1:4176';const url=root+'/proposed-fedramp-use/';const out='output/proposed-fedramp-use';fs.mkdirSync(out,{recursive:true});
const browser=await chromium.launch({headless:true,executablePath:process.env.CHROME_PATH||'/Users/codex/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});const results=[];
try{
 for(const width of [1440,768,390,320]){
  const page=await browser.newPage({viewport:{width,height:1000}});const errors=[];page.on('pageerror',e=>errors.push(e.message));await page.goto(url);
  assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));assert.equal(await page.locator('.quotation:visible').count(),41);assert.equal(await page.locator('textarea').count(),18);
  if(process.env.CAPTURE!=='0')await page.screenshot({path:`${out}/report-${width}.png`});
  await page.goto(url+'#design');if(process.env.CAPTURE!=='0')await page.screenshot({path:`${out}/evidence-${width}.png`});
  await page.locator('#field-allocation').fill('Example review record: agency identity integration; provider evidence referenced; review before approval.');await page.locator('#field-allocation').scrollIntoViewIfNeeded();if(process.env.CAPTURE!=='0')await page.screenshot({path:`${out}/worksheet-${width}.png`});
  await page.locator('#reading-toggle').click();assert.equal(await page.locator('.quotation:visible').count(),0);assert.equal(await page.locator('textarea:visible').count(),18);assert.equal(await page.locator('#reading-toggle').getAttribute('aria-pressed'),'true');
  await page.locator('#reading-toggle').focus();await page.keyboard.press('Enter');assert.equal(await page.locator('.quotation:visible').count(),41);
  await page.locator('#reading-toggle').click();await page.evaluate(()=>location.hash='quote-act-presume');await page.waitForFunction(()=>!document.body.classList.contains('workbook-only'));assert(await page.locator('#quote-act-presume').isVisible());
  assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));assert.equal(errors.length,0,errors.join('\n'));results.push({width,overflow:false,quotes:41,fields:18,viewToggle:true,citationReveal:true,keyboard:true,errors});await page.close();
 }
 const context=await browser.newContext({acceptDownloads:true});const p=await context.newPage();await p.goto(url);
 const demo='Working example only.\nAgency control owner: review team.\n<svg onload=alert(1)> must remain text.';
 await p.locator('#field-mission').fill(demo);assert.equal(await p.evaluate(()=>localStorage.length),0);
 await p.locator('#save-local').check();await p.reload();assert.equal(await p.locator('#field-mission').inputValue(),demo);
 let download= p.waitForEvent('download');await p.locator('#export-json').click();const jsonDownload=await download;const exported=JSON.parse(fs.readFileSync(await jsonDownload.path(),'utf8'));assert.equal(exported.answers.mission,demo);assert.equal(Object.keys(exported.answers).length,18);
 download=p.waitForEvent('download');await p.locator('#export-md').click();const md=fs.readFileSync(await (await download).path(),'utf8');assert(md.includes(demo));assert(md.includes('## Authorize the agency information system under FISMA'));
 await p.locator('#save-local').uncheck();assert.equal(await p.evaluate(()=>localStorage.length),0);await p.reload();assert.equal(await p.locator('#field-mission').inputValue(),'');
 await p.locator('#import-json').setInputFiles({name:'answers.json',mimeType:'application/json',buffer:Buffer.from(JSON.stringify(exported))});await p.waitForFunction(()=>document.querySelector('#workbook-status').textContent.includes('Answers imported'));assert.equal(await p.locator('#field-mission').inputValue(),demo);assert.equal(await p.locator('#save-local').isChecked(),false);
 for(const invalid of ['{oops',JSON.stringify({...exported,version:99}),JSON.stringify({...exported,answers:{mission:'replace?',unknown:'bad'}})]){
  await p.evaluate(()=>document.querySelector('#workbook-status').textContent='Waiting for import');await p.locator('#import-json').setInputFiles({name:'invalid.json',mimeType:'application/json',buffer:Buffer.from(invalid)});await p.waitForFunction(()=>document.querySelector('#workbook-status').textContent.includes('Import failed'));assert((await p.locator('#workbook-status').textContent()).includes('Import failed'));assert.equal(await p.locator('#field-mission').inputValue(),demo);
 }
 const long='Long-answer print check. '.repeat(120)+'FINAL ANSWER LINE';await p.locator('#field-monitoring').fill(long);await p.emulateMedia({media:'print'});assert.equal(await p.locator('.quotation:visible').count(),41);assert.equal(await p.locator('[data-answer="monitoring"]').textContent(),long);assert(await p.locator('[data-answer="monitoring"]').isVisible());await p.pdf({path:`${out}/report-print.pdf`,format:'A4',printBackground:true});
 await p.emulateMedia({media:'screen'});await p.locator('#reading-toggle').click();await p.emulateMedia({media:'print'});assert.equal(await p.locator('.quotation:visible').count(),0);assert.equal(await p.locator('.print-answer:visible').count(),18);await p.pdf({path:`${out}/workbook-print.pdf`,format:'A4',printBackground:true});
 await p.emulateMedia({media:'screen'});p.once('dialog',d=>d.accept());await p.locator('#clear').click();assert.equal(await p.locator('#field-mission').inputValue(),'');assert.equal(await p.evaluate(()=>localStorage.length),0);
 results.push({sessionOnlyDefault:true,optInSaveRestore:true,saveRemoval:true,jsonRoundTrip:true,markdownExport:true,invalidImportAtomic:true,printLongAnswer:true,workbookOnlyPrint:true,clear:true});await context.close();
 for(const js of [true,false]){
  const c=await browser.newContext({javaScriptEnabled:js,offline:true});const page=await c.newPage({viewport:{width:390,height:844}});const errors=[];page.on('pageerror',e=>errors.push(e.message));await page.goto(new URL('../site/proposed-fedramp-use/index.html',import.meta.url).href);assert.equal(await page.locator('.quotation:visible').count(),41);assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));if(!js)assert(await page.locator('#workbook-tools').isHidden());assert.equal(errors.length,0);results.push({fileProtocol:true,offline:true,javaScript:js,passed:true});await c.close();
 }
 const page=await browser.newPage({viewport:{width:1280,height:900}});await page.goto(url);await page.keyboard.press('Tab');assert.equal(await page.evaluate(()=>document.activeElement.textContent),'Skip to report');await page.keyboard.press('Enter');await page.evaluate(()=>document.documentElement.style.fontSize='36px');assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));await page.goto(root+'/fedramp-a130/proposed-fedramp-use/');assert.equal(await page.locator('.quotation').count(),41);
 await page.addInitScript(()=>Object.defineProperty(window,'localStorage',{get(){throw new Error('disabled');}}));await page.reload();await page.locator('#field-mission').fill('Still editable');await page.locator('#save-local').click();assert((await page.locator('#workbook-status').textContent()).includes('unavailable'));assert.equal(await page.locator('#field-mission').inputValue(),'Still editable');
 results.push({skipLink:true,textSize:'200%',publicPrefix:true,blockedStorageFallback:true});await page.close();
}finally{await browser.close();}
fs.writeFileSync(`${out}/browser-check.json`,JSON.stringify(results,null,2)+'\n');console.log(JSON.stringify(results,null,2));

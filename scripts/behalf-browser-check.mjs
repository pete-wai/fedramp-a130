import {chromium} from 'playwright';
import fs from 'node:fs';
import assert from 'node:assert/strict';
const browser=await chromium.launch({headless:true,executablePath:process.env.CHROME_PATH||'/Users/codex/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
const base='http://127.0.0.1:4176/on-behalf/index.html';
const quoteCount=JSON.parse(fs.readFileSync('site/on-behalf/quotations.json')).length;
const results=[];
try{
 for(const width of [1440,768,390,320]){
  const page=await browser.newPage({viewport:{width,height:1000}});const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto(base);assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  assert.equal(await page.locator('.milestone:visible').count(),41);
  assert.equal(await page.locator('.quotation:visible').count(),quoteCount);
  const type=await page.evaluate(()=>{const h=getComputedStyle(document.querySelector('h1'));const p=getComputedStyle(document.querySelector('.event-summary'));return {heading:parseFloat(h.fontSize),bodyRatio:parseFloat(p.lineHeight)/parseFloat(p.fontSize)};});assert(type.heading<=70);assert(type.bodyRatio>=1.5);
  await page.locator('#history-query').fill('not-a-match-zz');assert.equal(await page.locator('.milestone:visible').count(),0);assert(await page.locator('#history-empty').isVisible());
  await page.locator('#history-filter button').click();await page.locator('#history-kind').selectOption('Comment response');assert.equal(await page.locator('.milestone:visible').count(),1);
  await page.locator('#history-query').fill('DHS');assert.equal(await page.locator('.milestone:visible').count(),1);
  // Internal citation navigation must reveal a target hidden by either filter.
  await page.locator('#authority-map a[href="#quote-f02-deliver"]').click();await page.waitForFunction(()=>document.querySelectorAll('.milestone:not([hidden])').length===41);assert.equal(await page.locator('.milestone:visible').count(),41);assert(await page.locator('#quote-f02-deliver').isVisible());
  await page.locator('#source-query').fill('not-a-match-zz');assert(await page.locator('#source-empty').isVisible());
  await page.locator('#quote-f02-deliver a[href="#source-fisma2002"]').click();await page.waitForFunction(()=>!document.querySelector('#source-fisma2002').hidden);assert(await page.locator('#source-fisma2002').isVisible());
  const summary=page.locator('#source-fisma2002 summary');await summary.focus();await page.keyboard.press('Enter');assert(await page.locator('#source-fisma2002 details').getAttribute('open')!==null);
  await page.goto(base+'#example-aws');assert(await page.locator('#today').isVisible());assert.equal(await page.locator('.scenario').count(),0);
  for(const [name,anchor] of [['report',''],['statute','#fisma-2014-history'],['policy','#a130-2016-history'],['comparison','#today'],['cui','#quote-cui16-nonfederal']]){
   await page.goto(base+anchor);await page.screenshot({path:`output/on-behalf/history-${name}-${width}.png`});
   assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  }
  assert.equal(errors.length,0,errors.join('\n'));results.push({width,passed:true,checks:['overflow','all quotes visible','combined filters/reset/empty','citation reveals filtered target','source filter','legacy links','keyboard disclosure','no JS exceptions']});await page.close();
 }
 for(const js of [true,false]){
  const context=await browser.newContext({javaScriptEnabled:js,offline:true});const page=await context.newPage({viewport:{width:390,height:844}});
  await page.goto(new URL('../site/on-behalf/index.html',import.meta.url).href+'#fisma-2014-history');
  assert.equal(await page.locator('.milestone:visible').count(),41);assert.equal(await page.locator('.quotation:visible').count(),quoteCount);
  if(js){await page.locator('#history-query').fill('incidental');assert((await page.locator('.milestone:visible').count())>0);assert((await page.locator('.milestone:visible').count())<41);}
  else assert(await page.locator('#history-tools').isHidden());
  assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));results.push({fileProtocol:true,offline:true,javaScript:js,passed:true});await context.close();
 }
 const page=await browser.newPage({viewport:{width:1280,height:900}});await page.goto(base);await page.keyboard.press('Tab');assert.equal(await page.evaluate(()=>document.activeElement.textContent),'Skip to report');await page.keyboard.press('Enter');
 await page.evaluate(()=>document.documentElement.style.fontSize='34px');assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));results.push({keyboardSkip:true,textSize:'200%',passed:true});
 await page.goto(base.replace('index.html','print.html'));await page.emulateMedia({media:'print'});assert.equal(await page.locator('.quotation:visible').count(),quoteCount);assert.equal(await page.locator('details:not([open])').count(),0);await page.pdf({path:'output/on-behalf/history-print.pdf',format:'A4',printBackground:true});results.push({print:'all milestones, quotations and provenance expanded',passed:true});await page.close();
 const prefix=await browser.newPage();await prefix.goto('http://127.0.0.1:4176/fedramp-a130/on-behalf/index.html#fisma-2014-history');assert(await prefix.locator('#fisma-2014-history').isVisible());results.push({publicPrefix:true,passed:true});await prefix.close();
}finally{await browser.close();}
fs.writeFileSync('output/on-behalf/history-browser-check.json',JSON.stringify(results,null,2));console.log(JSON.stringify(results,null,2));

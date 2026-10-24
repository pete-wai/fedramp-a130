import {chromium} from 'playwright';
import fs from 'node:fs';
import assert from 'node:assert/strict';
const browser=await chromium.launch({headless:true,executablePath:process.env.CHROME_PATH||'/Users/codex/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
const base='http://127.0.0.1:4176/on-behalf/index.html';
const results=[];
try{
 for(const width of [1440,768,390,320]){
  const page=await browser.newPage({viewport:{width,height:1000}});const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto(base);assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  assert.equal(await page.locator('.scenario:visible').count(),5);
  const typography=await page.evaluate(()=>{const h=getComputedStyle(document.querySelector('h1'));const p=getComputedStyle(document.querySelector('.prose-block p'));return {heading:parseFloat(h.fontSize),bodyRatio:parseFloat(p.lineHeight)/parseFloat(p.fontSize)};});assert(typography.heading<=70);assert(typography.bodyRatio>=1.5);
  await page.locator('#scenario-select').selectOption('aws');assert.equal(await page.locator('.scenario:visible').count(),1);assert(await page.locator('#example-aws').isVisible());
  await page.locator('#scenario-select').selectOption('figma');await page.goBack();assert(await page.locator('#example-aws').isVisible());
  await page.locator('#history-query').fill('not-a-match-zz');assert.equal(await page.locator('.history-list>li:visible').count(),0);assert(await page.locator('#history-empty').isVisible());
  await page.locator('#history-filter button').click();await page.locator('#history-kind').selectOption('Public comments');assert.equal(await page.locator('.history-list>li:visible').count(),2);
  await page.locator('#history-filter button').click();await page.locator('#source-query').fill('not-a-match-zz');assert(await page.locator('#source-empty').isVisible());
  await page.goto(base+'#source-cui2025');assert(await page.locator('#source-cui2025').isVisible());
  await page.locator('#source-filter button').click();await page.locator('#source-kind').selectOption('Public comment');assert.equal(await page.locator('.source:visible').count(),2);
  await page.locator('#source-filter button').click();await page.goto(base+'#example-internet');assert.equal(await page.locator('.scenario:visible').count(),1);assert(await page.locator('#example-internet').isVisible());
  const summary=page.locator('#example-internet .changes summary');await summary.focus();await page.keyboard.press('Enter');assert(await page.locator('#example-internet .changes').getAttribute('open')!==null);
  await page.goto(base);await page.screenshot({path:`output/on-behalf/report-${width}.png`,fullPage:false});
  await page.goto(base+'#words');await page.screenshot({path:`output/on-behalf/words-${width}.png`});
  await page.goto(base+'#example-figma');await page.screenshot({path:`output/on-behalf/example-${width}.png`});
  assert.equal(errors.length,0,errors.join('\n'));
  results.push({width,passed:true,checks:['overflow','scenario selection','browser Back','timeline filters/reset/empty','source filters/reset/empty','deep links reveal content','keyboard disclosure','no JS exceptions']});await page.close();
 }
 for(const js of [true,false]){
  const context=await browser.newContext({javaScriptEnabled:js,offline:true});const page=await context.newPage();
  await page.goto(new URL('../site/on-behalf/index.html',import.meta.url).href+'#example-contractor');
  assert(await page.locator('#words').isVisible());assert(await page.locator('#example-contractor').isVisible());
  if(js){await page.locator('#scenario-select').selectOption('internet');assert(await page.locator('#example-internet').isVisible());}
  else {assert.equal(await page.locator('.scenario').count(),5);assert.equal(await page.locator('.scenario:visible').count(),5);}
  results.push({fileProtocol:true,offline:true,javaScript:js,passed:true});await context.close();
 }
 const page=await browser.newPage({viewport:{width:1280,height:900}});await page.goto(base);await page.keyboard.press('Tab');assert.equal(await page.evaluate(()=>document.activeElement.textContent),'Skip to report');await page.keyboard.press('Enter');
 await page.evaluate(()=>document.documentElement.style.fontSize='34px');assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));results.push({keyboardSkip:true,textSize:'200%',passed:true});
 await page.goto(base.replace('index.html','print.html'));await page.emulateMedia({media:'print'});assert.equal(await page.locator('.scenario:visible').count(),5);assert.equal(await page.locator('details:not([open])').count(),0);await page.pdf({path:'output/on-behalf/report-print.pdf',format:'A4',printBackground:true});results.push({print:'all examples and evidence expanded',passed:true});await page.close();
 const prefix=await browser.newPage();await prefix.goto('http://127.0.0.1:4176/fedramp-a130/on-behalf/index.html#example-aws');assert(await prefix.locator('#example-aws').isVisible());results.push({publicPrefix:true,passed:true});await prefix.close();
}finally{await browser.close();}
fs.writeFileSync('output/on-behalf/browser-check.json',JSON.stringify(results,null,2));console.log(JSON.stringify(results,null,2));

import {chromium} from 'playwright';
import fs from 'node:fs';import path from 'node:path';import assert from 'node:assert/strict';
const base=process.env.BASE_URL||'http://127.0.0.1:4176/';
const browser=await chromium.launch({executablePath:'/Users/codex/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true});
const evidence=[];
for(const width of [1440,768,390,320]){
 const page=await browser.newPage({viewport:{width,height:900},reducedMotion:'reduce'});const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto(base+'law/index.html');assert.equal(await page.locator('.reading-paths li').count(),12);
 await page.locator('.reading-paths a').first().click();
 assert.equal(await page.locator('.reading-section').count(),10);
 assert.equal(await page.locator('#p-44-3555-a-1').isVisible(),true);
 assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
 await page.screenshot({path:`output/reading-${width}-start.png`});
 const contents=page.locator('.contents>details');if(width<=900)await contents.locator('summary').click();
 await page.locator('.contents a[href="#44-3555"]').click();
 await page.waitForTimeout(100);
 if(width<=900)assert.equal(await contents.getAttribute('open'),null);
 const rect=await page.locator('[id="44-3555"]').boundingBox();assert(rect.y>=0&&rect.y<200,JSON.stringify(rect));
 await page.locator('#p-44-3555-b-1 > details > summary').focus();await page.keyboard.press('Enter');
 assert(await page.locator('#p-44-3555-b-1 > details[open]').isVisible());
 await page.screenshot({path:`output/reading-${width}-evaluation.png`});
 await page.locator('#history-44-3555 > summary').click();assert(await page.locator('#history-44-3555[open]').isVisible());
 assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
 assert.deepEqual(errors,[]);evidence.push({width,contentsJump:true,keyboardContext:true,inlineHistory:true,noOverflow:true});await page.close();
}
for(const javaScriptEnabled of [true,false]){
 const ctx=await browser.newContext({offline:true,javaScriptEnabled,viewport:{width:390,height:844}});const page=await ctx.newPage();
 await page.goto('file://'+path.resolve('site/law/read-fedramp.html'));assert.equal(await page.locator('.reading-section').count(),10);assert(await page.locator('#p-44-3613').isVisible());
 await page.locator('#history-44-3613 > summary').click();assert(await page.locator('#history-44-3613[open]').isVisible());
 await page.emulateMedia({media:'print'});assert.equal(await page.locator('.contents').isVisible(),false);assert(await page.locator('#p-44-3613').isVisible());await ctx.close();
}
await browser.close();fs.writeFileSync('output/reading-browser-check.json',JSON.stringify({base,evidence,offline:true,noJavaScript:true,print:true,passed:true},null,2));console.log('Continuous reading browser checks passed');

'use strict';
(() => {
 const form=document.querySelector('#worksheet');
 const inputs=[...form.querySelectorAll('textarea')];
 const byName=new Map(inputs.map(el=>[el.name,el]));
 const key='a130-proposed-fedramp-use-v1';
 const status=document.querySelector('#workbook-status');
 const save=document.querySelector('#save-local');
 const say=text=>{status.textContent=text;};
 const data=()=>({schema:'a130-proposed-fedramp-use',version:1,exportedAt:new Date().toISOString(),answers:Object.fromEntries(inputs.map(el=>[el.name,el.value]))});
 function mirrors(){for(const el of inputs)document.querySelector(`[data-answer="${el.name}"]`).textContent=el.value||'Not recorded.';}
 function validate(value){
  if(!value||value.schema!=='a130-proposed-fedramp-use'||value.version!==1||!value.answers||Array.isArray(value.answers)||typeof value.answers!=='object')throw new Error('This file is not a version 1 worksheet from this report.');
  for(const [name,v] of Object.entries(value.answers))if(!byName.has(name)||typeof v!=='string'||v.length>20000)throw new Error('The file contains an unknown field or an invalid answer.');
  return Object.fromEntries(inputs.map(el=>[el.name,value.answers[el.name]||'']));
 }
 function apply(answers){for(const el of inputs)el.value=answers[el.name];mirrors();}
 function persist(message='Answers saved in this browser.'){
  if(!save.checked)return;
  try{localStorage.setItem(key,JSON.stringify(data()));say(message);}
  catch{save.checked=false;say('Browser storage is unavailable or full. Your answers remain on this page; export a copy.');}
 }
 try{const previous=localStorage.getItem(key);if(previous){apply(validate(JSON.parse(previous)));save.checked=true;say('Saved answers restored from this browser.');}}
 catch{say('A saved copy could not be loaded. The worksheet is empty; you can import an exported copy.');}
 document.querySelector('#workbook-tools').hidden=false;
 if(matchMedia('(max-width:760px)').matches)document.querySelector('.contents').open=false;
 // Following a contents link must reveal its target in workbook-only mode.
 function reveal(){const id=decodeURIComponent(location.hash.slice(1));const target=document.getElementById(id);if(target&&target.closest('.reading')&&document.body.classList.contains('workbook-only')){document.body.classList.remove('workbook-only');toggle.setAttribute('aria-pressed','false');toggle.textContent='Show workbook only';document.querySelector('#print').textContent='Print report & answers';requestAnimationFrame(()=>target.scrollIntoView());}}
 const toggle=document.querySelector('#reading-toggle');
 toggle.addEventListener('click',()=>{const only=document.body.classList.toggle('workbook-only');toggle.setAttribute('aria-pressed',String(only));toggle.textContent=only?'Show report & evidence':'Show workbook only';document.querySelector('#print').textContent=only?'Print workbook & answers':'Print report & answers';document.querySelector('#workbook').scrollIntoView();});
 window.addEventListener('hashchange',reveal);reveal();
 form.addEventListener('submit',event=>event.preventDefault());
 form.addEventListener('input',()=>{mirrors();if(save.checked)persist();else say('Session only. Export a copy before closing this page.');});
 save.addEventListener('change',()=>{if(save.checked)persist();else{try{localStorage.removeItem(key);say('Browser copy removed. Answers remain in this session.');}catch{say('Could not remove browser storage. Use your browser’s site-data controls to remove any saved copy.');}}});
 function download(filename,contents,type){const url=URL.createObjectURL(new Blob([contents],{type}));const a=document.createElement('a');a.href=url;a.download=filename;document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);}
 document.querySelector('#export-json').addEventListener('click',()=>{download('proposed-fedramp-use-answers.json',JSON.stringify(data(),null,2)+'\n','application/json');say('JSON export prepared. It can be imported into this workbook.');});
 document.querySelector('#export-md').addEventListener('click',()=>{
  const lines=['# Agency cloud-use working record','','Exported '+new Date().toISOString(),'','Working aid from the proposed FedRAMP use report. This is not a signed authorization.','Report: https://pete-wai.github.io/fedramp-a130/proposed-fedramp-use/',''];
  for(const section of form.querySelectorAll('.step')){lines.push('## '+section.querySelector('h2').textContent,'');for(const el of section.querySelectorAll('textarea')){lines.push('### '+form.querySelector(`label[for="${el.id}"]`).textContent,'',el.value||'Not recorded.','');}}
  download('proposed-fedramp-use-record.md',lines.join('\n'),'text/markdown');say('Markdown record export prepared. Add the signed decision and supporting agency records separately.');
 });
 document.querySelector('#import-json').addEventListener('change',async event=>{
  const file=event.target.files[0];if(!file)return;
  try{if(file.size>1000000)throw new Error('The file is too large. Use a worksheet export under 1 MB.');const next=validate(JSON.parse(await file.text()));apply(next);persist('Imported answers saved in this browser.');if(!save.checked)say('Answers imported into this session. Browser saving remains off.');}
  catch(error){say('Import failed; current answers were kept. '+(error instanceof SyntaxError?'The file is not valid JSON.':error.message));}
  finally{event.target.value='';}
 });
 document.querySelector('#clear').addEventListener('click',()=>{if(inputs.some(el=>el.value)&&!confirm('Clear all answers from this worksheet and its saved browser copy? Export first if you need a copy.'))return;for(const el of inputs)el.value='';mirrors();try{localStorage.removeItem(key);save.checked=false;say('Answers cleared. Browser saving is off.');}catch{save.checked=false;say('Page answers cleared, but browser storage could not be removed. Use your browser’s site-data controls.');}});
 window.addEventListener('beforeprint',mirrors);
 document.querySelector('#print').addEventListener('click',()=>{mirrors();window.print();});
 mirrors();
})();

'use strict';
const form=document.querySelector('#filters');
const controls=['query','type','era','relation','term','sort'].map(id=>document.getElementById(id));
const records=[...document.querySelectorAll('.record')];
const searchText=new Map(records.map(r=>[r,r.textContent.toLocaleLowerCase()]));
const compact=document.querySelector('#compact-table');const toggle=document.querySelector('#toggle-view');const compactRows=new Map([...compact.querySelectorAll('tbody tr')].map(r=>[r.dataset.record,r]));
function setView(table){compact.hidden=!table;document.querySelector('#records').hidden=table;toggle.setAttribute('aria-pressed',String(table));toggle.textContent=table?'Show detailed records':'Show compact table';}
toggle.addEventListener('click',()=>setView(compact.hidden));
function filter(){
 const [q,type,era,relation,term,sort]=controls.map(x=>x.value);
 let count=0;
 for(const r of records){const match=(!q||searchText.get(r).includes(q.toLocaleLowerCase()))&&(!type||r.dataset.type===type)&&(!era||r.dataset.era===era)&&(!relation||r.dataset.relation===relation)&&(!term||r.dataset.terms.split('|').includes(term));r.hidden=!match;compactRows.get(r.id.slice(4)).hidden=!match;if(match)count++;}
 const sorted=[...records].sort((a,b)=>sort==='Title A–Z'?a.dataset.title.localeCompare(b.dataset.title):sort==='Newest first'?b.dataset.date.localeCompare(a.dataset.date):a.dataset.date.localeCompare(b.dataset.date));
 document.querySelector('#records').append(...sorted);compact.querySelector('tbody').append(...sorted.map(r=>compactRows.get(r.id.slice(4))));
 document.querySelector('#result-count').textContent=`${count} of ${records.length} documents`;
 document.querySelector('#empty').hidden=count!==0;
}
form.addEventListener('input',filter);form.addEventListener('change',filter);form.addEventListener('submit',e=>e.preventDefault());form.addEventListener('reset',()=>setTimeout(filter,0));
document.querySelector('#show-memos').addEventListener('click',()=>{form.reset();setTimeout(()=>{document.querySelector('#type').value='OMB memorandum';filter();document.querySelector('#library').scrollIntoView();document.querySelector('#query').focus({preventScroll:true});},0);});
document.querySelectorAll('.event').forEach(button=>button.addEventListener('click',()=>{document.querySelectorAll('.event').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));const record=document.querySelector('#doc-'+button.dataset.document);const detail=document.querySelector('#event-detail');detail.replaceChildren(...[...record.children].map(c=>c.cloneNode(true)));const link=document.createElement('a');link.href='#'+record.id;link.textContent='Go to full library record →';detail.append(link);detail.focus({preventScroll:true});detail.scrollIntoView({block:'nearest'});}));
function revealHash(){let id;try{id=decodeURIComponent(location.hash.slice(1));}catch{return;}const target=document.getElementById(id);if(target?.classList.contains('record')){setView(false);if(target.hidden){form.reset();filter();}target.scrollIntoView();}}
window.addEventListener('hashchange',revealHash);revealHash();document.querySelector('#print').addEventListener('click',()=>window.print());

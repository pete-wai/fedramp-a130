'use strict';
const milestones=[...document.querySelectorAll('.milestone')];
const eras=[...document.querySelectorAll('.era')];
const form=document.querySelector('#history-filter');
const query=document.querySelector('#history-query');
const kind=document.querySelector('#history-kind');
const count=document.querySelector('#history-count');
const searchable=new Map(milestones.map(el=>[el,el.textContent.toLowerCase()]));
function filterHistory(){
 const words=query.value.trim().toLowerCase().split(/\s+/).filter(Boolean);
 for(const el of milestones)el.hidden=!!(kind.value&&el.dataset.kind!==kind.value)||!words.every(w=>searchable.get(el).includes(w));
 for(const era of eras)era.hidden=![...era.querySelectorAll('.milestone')].some(el=>!el.hidden);
 const visible=milestones.filter(el=>!el.hidden).length;
 count.textContent=`${visible} of ${milestones.length} milestones shown. Quotations in matching milestones remain complete.`;
 document.querySelector('#history-empty').hidden=visible!==0;
}
document.querySelector('#history-tools').hidden=false;
form.addEventListener('input',filterHistory);
form.addEventListener('submit',event=>event.preventDefault());
form.addEventListener('reset',()=>setTimeout(filterHistory,0));filterHistory();
const sourceForm=document.querySelector('#source-filter');
const sourceQuery=document.querySelector('#source-query');
const sourceCount=document.querySelector('#source-count');
const sources=[...document.querySelectorAll('.source')];
function filterSources(){
 const words=sourceQuery.value.trim().toLowerCase().split(/\s+/).filter(Boolean);
 for(const el of sources)el.hidden=!words.every(w=>el.textContent.toLowerCase().includes(w));
 const n=sources.filter(el=>!el.hidden).length;
 sourceCount.textContent=`${n} of ${sources.length} sources shown.`;
 document.querySelector('#source-empty').hidden=n!==0;
}
sourceForm.hidden=false;sourceCount.hidden=false;
sourceForm.addEventListener('input',filterSources);
sourceForm.addEventListener('submit',e=>e.preventDefault());
sourceForm.addEventListener('reset',()=>setTimeout(filterSources,0));filterSources();
function revealTarget(){
 let id;try{id=decodeURIComponent(location.hash.slice(1));}catch{return;}
 const target=document.getElementById(id);if(!target)return;
 if(target.closest('.era')?.hidden||target.closest('.milestone')?.hidden){query.value='';kind.value='';filterHistory();}
 if(target.closest('.source')?.hidden){sourceQuery.value='';filterSources();}
 target.scrollIntoView({block:'start'});
}
window.addEventListener('hashchange',revealTarget);
if(location.hash)requestAnimationFrame(revealTarget);
window.addEventListener('beforeprint',()=>{milestones.forEach(el=>el.hidden=false);eras.forEach(el=>el.hidden=false);sources.forEach(el=>el.hidden=false);});
window.addEventListener('afterprint',()=>{filterHistory();filterSources();});

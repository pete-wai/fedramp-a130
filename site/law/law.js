document.documentElement.classList.add('has-js');
if(matchMedia('(max-width:900px)').matches){document.querySelectorAll('.contents>details').forEach(x=>x.open=false);}
const form=document.querySelector('.filters');
if(form){
 const items=[...document.querySelectorAll('.search-item')];
 const query=document.querySelector('#query'),topic=document.querySelector('#topic'),actor=document.querySelector('#actor'),force=document.querySelector('#force');
 const folded=s=>s.toLocaleLowerCase().normalize('NFKC').replace(/[–—]/g,'-');
 function filter(){
  const terms=folded(query.value.trim()).split(/\s+/).filter(Boolean);let count=0;
  for(const item of items){const matches=terms.every(t=>folded(item.dataset.search).includes(t))&&(!topic.value||item.dataset.topics.split('|').includes(topic.value))&&(!actor.value||item.dataset.actors.split('|').includes(actor.value))&&(!force?.value||item.dataset.force===force.value);item.hidden=!matches;if(matches)count++;}
  document.querySelector('#results').textContent=`${count} of ${items.length} entries shown`;
  document.querySelector('#empty').hidden=count!==0;
  document.querySelectorAll('.contents a[href^="#"]').forEach(a=>{const target=document.getElementById(a.hash.slice(1));a.hidden=!!target?.hidden;});
 }
 form.addEventListener('input',filter);form.addEventListener('change',filter);form.addEventListener('submit',e=>e.preventDefault());form.addEventListener('reset',()=>setTimeout(filter,0));filter();
}
const comparison=document.querySelector('#comparison');
comparison?.addEventListener('change',()=>{document.querySelectorAll('.version-change').forEach(x=>x.hidden=!!comparison.value&&comparison.value!==x.id);if(comparison.value){document.getElementById(comparison.value).querySelector('details').open=true;}});
function reveal(){
 let target;try{target=document.getElementById(decodeURIComponent(location.hash.slice(1)));}catch{return;}
 if(!target)return;
 if(target.closest('[hidden]')&&form){form.reset();setTimeout(()=>{reveal();},1);return;}
 for(let p=target;p;p=p.parentElement){if(p.tagName==='DETAILS')p.open=true;}
}
window.addEventListener('hashchange',reveal);reveal();
let printDetails=[];
window.addEventListener('beforeprint',()=>{printDetails=[...document.querySelectorAll('details:not([open])')];printDetails.forEach(x=>x.open=true);});
window.addEventListener('afterprint',()=>printDetails.forEach(x=>x.open=false));

// Keep long readings navigable without changing the URL as the reader scrolls.
const reading=document.querySelector('.continuous-reading');
if(reading){
 const links=[...document.querySelectorAll('.contents a[href^="#"]')];
 const targets=links.map(a=>document.getElementById(a.hash.slice(1))).filter(Boolean);
 let queued=false;
 function trackReading(){
  queued=false;const threshold=matchMedia('(max-width:900px)').matches?110:80;
  let current=targets[0];for(const target of targets){if(target.getBoundingClientRect().top<=threshold)current=target;else break;}
  for(const link of links){if(current&&link.hash==='#'+current.id)link.setAttribute('aria-current','location');else link.removeAttribute('aria-current');}
 }
 addEventListener('scroll',()=>{if(!queued){queued=true;requestAnimationFrame(trackReading);}}, {passive:true});trackReading();
 for(const link of links)link.addEventListener('click',()=>{if(matchMedia('(max-width:900px)').matches)link.closest('details').open=false;});
}

// Progressive enhancement only: all report content is present in the HTML.
const $ = selector => document.querySelector(selector);
const normalize = text => text.toLocaleLowerCase().normalize('NFKC');
function filter(formId, queryId, kindId, itemSelector, countId, emptyId, noun) {
  const form=$(formId), query=$(queryId), kind=$(kindId), count=$(countId), items=[...document.querySelectorAll(itemSelector)];
  form.hidden=false; count.hidden=false;
  const update=()=>{
    let visible=0;
    for(const item of items){item.hidden=!(normalize(item.textContent).includes(normalize(query.value.trim())) && (!kind.value || item.dataset.kind===kind.value));if(!item.hidden)visible++;}
    count.textContent=`${visible} of ${items.length} ${noun}`;$(emptyId).hidden=visible!==0;
  };
  form.addEventListener('submit',event=>event.preventDefault());
  form.addEventListener('input',update); form.addEventListener('change',update);
  form.addEventListener('reset',()=>setTimeout(update,0)); update();
  return ()=>{form.reset();update();};
}
const resetHistory=filter('#history-filter','#history-query','#history-kind','.history-list>li','#history-count','#history-empty','events');
const resetSources=filter('#source-filter','#source-query','#source-kind','.source','#source-count','#source-empty','sources');
const scenarios=[...document.querySelectorAll('.scenario')], select=$('#scenario-select');
$('#scenario-controls').hidden=false;$('#scenario-status').hidden=false;
function showScenario(value){
  select.value=value;
  for(const scenario of scenarios)scenario.hidden=value!=='all' && scenario.id!==`example-${value}`;
  $('#scenario-status').textContent=value==='all'?'Showing all five examples':`Showing ${select.selectedOptions[0].textContent}`;
}
select.addEventListener('change',()=>{
  showScenario(select.value);
  const anchor=select.value==='all'?'examples':`example-${select.value}`;
  // This works under file:// too, and browser Back restores earlier choices.
  history.pushState(null,'',`#${anchor}`);
});
function followHash(){
  let id;try{id=decodeURIComponent(location.hash.slice(1));}catch{return;}
  const target=document.getElementById(id);if(!target)return;
  if(target.closest('.source'))resetSources();
  if(target.closest('.history-list'))resetHistory();
  const scenario=target.closest('.scenario');
  if(scenario)showScenario(scenario.id.slice(8));
  else if(id==='examples')showScenario('all');
  for(let p=target;p;p=p.parentElement)if(p.tagName==='DETAILS')p.open=true;
  if(location.hash)requestAnimationFrame(()=>target.scrollIntoView({block:'start'}));
}
window.addEventListener('hashchange',followHash);window.addEventListener('popstate',followHash);
showScenario('all');followHash();
// Compact the long contents list on small screens; navigation remains native.
if(matchMedia('(max-width:800px)').matches)$('.contents details').open=false;
let printState;
window.addEventListener('beforeprint',()=>{
  printState=[...document.querySelectorAll('details')].map(el=>[el,el.open]);
  for(const [el] of printState)el.open=true;
});
window.addEventListener('afterprint',()=>{for(const [el,open] of printState||[])el.open=open;});

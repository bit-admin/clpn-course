(function(){
 const KEY="clpn-syllabus-progress-v1", TKEY="clpn-syllabus-theme";
 const MODS=__MODS__, TOTAL=__TOTAL__;
 let st={}; try{st=JSON.parse(localStorage.getItem(KEY))||{}}catch(e){st={}}
 const boxes=[...document.querySelectorAll('input[type=checkbox][data-lid]')];
 const save=()=>{try{localStorage.setItem(KEY,JSON.stringify(st))}catch(e){}};
 const aid=id=>'L'+id.replace('.','-');
 function render(){
  let n=0;
  boxes.forEach(b=>{const id=b.dataset.lid,on=!!st[id];b.checked=on;if(on)n++;
   document.getElementById(aid(id)).classList.toggle('isdone',on);
   const a=document.querySelector('a[data-nav="'+id+'"]'); if(a)a.classList.toggle('done',on);
   b.parentElement.title=on?('Completed on '+st[id]):'Mark complete';});
  document.getElementById('pText').textContent=n+' / '+TOTAL;
  document.getElementById('pBar').style.width=(100*n/TOTAL)+'%';
  for(const m in MODS){const ids=MODS[m],d=ids.filter(i=>st[i]).length,p=Math.round(100*d/ids.length);
   const el=document.querySelector('.mprog[data-mod="'+m+'"]'); if(el){el.querySelector('i').style.setProperty('--p',p+'%');el.querySelector('b').textContent=p+'%';}}
 }
 boxes.forEach(b=>{b.addEventListener('click',e=>e.stopPropagation());
  b.addEventListener('change',()=>{if(b.checked)st[b.dataset.lid]=new Date().toISOString().slice(0,10);else delete st[b.dataset.lid];save();render();});});
 document.querySelectorAll('label.done').forEach(l=>l.addEventListener('click',e=>e.stopPropagation()));
 document.getElementById('reset').onclick=()=>{if(confirm('Clear all your learning progress?')){st={};save();render();}};
 const L=[...document.querySelectorAll('details.lesson')];
 document.getElementById('expand').onclick=()=>L.forEach(d=>d.open=true);
 document.getElementById('collapse').onclick=()=>L.forEach(d=>d.open=false);
 const root=document.documentElement, saved=localStorage.getItem(TKEY);
 if(saved)root.dataset.theme=saved; else if(window.matchMedia&&matchMedia('(prefers-color-scheme: dark)').matches)root.dataset.theme='dark';
 const themeBtn=document.getElementById('theme');
 function paintTheme(){const dark=root.dataset.theme==='dark';themeBtn.textContent=dark?'Light':'Dark';themeBtn.setAttribute('aria-label',dark?'Switch to light mode':'Switch to dark mode');}
 themeBtn.onclick=()=>{root.dataset.theme=root.dataset.theme==='dark'?'light':'dark';try{localStorage.setItem(TKEY,root.dataset.theme)}catch(e){}paintTheme();};
 paintTheme();
 function openHash(){const h=decodeURIComponent(location.hash.slice(1));const el=h&&document.getElementById(h);if(el&&el.tagName==='DETAILS')el.open=true;}
 window.addEventListener('hashchange',openHash); openHash();
 const llmBtn=document.getElementById('llmCopy'), llmCode=document.getElementById('llmPrompt');
 if(llmBtn&&llmCode){
  const text='Read '+new URL('llm.md', location.href).href;
  llmCode.textContent=text;
  llmBtn.onclick=()=>{const done=()=>{llmBtn.textContent='Copied';setTimeout(()=>{llmBtn.textContent='Copy prompt';},1500);};
   if(navigator.clipboard&&window.isSecureContext)navigator.clipboard.writeText(text).then(done,()=>fallbackCopy(text,done));
   else fallbackCopy(text,done);};
  function fallbackCopy(t,done){const ta=document.createElement('textarea');ta.value=t;ta.style.position='fixed';ta.style.opacity='0';document.body.appendChild(ta);ta.select();try{document.execCommand('copy');}catch(e){}ta.remove();done();}
 }
 const q=document.getElementById('q');
 q.addEventListener('input',()=>{const v=q.value.trim().toLowerCase();
  L.forEach(d=>{const hit=!v||d.textContent.toLowerCase().includes(v);d.classList.toggle('hidden',!hit);if(v)d.open=hit;});
  document.querySelectorAll('section.module').forEach(s=>s.classList.toggle('hidden',!!v&&!s.querySelector('details.lesson:not(.hidden)')));
  document.querySelectorAll('a[data-nav]').forEach(a=>a.parentElement.classList.toggle('hidden',document.getElementById(aid(a.dataset.nav)).classList.contains('hidden')));
 });
 const side=document.getElementById('side');
 document.getElementById('menuBtn').onclick=()=>side.classList.toggle('open');
 side.addEventListener('click',e=>{if(e.target.closest('a')&&innerWidth<=900)side.classList.remove('open')});
 const navA=[...document.querySelectorAll('aside nav a[href^="#"]')];
 if('IntersectionObserver' in window){
  const io=new IntersectionObserver(es=>es.forEach(en=>{if(en.isIntersecting)navA.forEach(a=>a.classList.toggle('active',a.getAttribute('href')==='#'+en.target.id));}),{rootMargin:'-10% 0px -80% 0px'});
  document.querySelectorAll('details.lesson, section.card').forEach(s=>io.observe(s));
 }
 render();
})();

/* CLPN Course · Shared lesson runtime: theme, TOC, R syntax highlight & copy, quizzes, progress, KaTeX */
(function(){
"use strict";
const PKEY="clpn-syllabus-progress-v1", TKEY="clpn-syllabus-theme";
const root=document.documentElement;
function lsGet(k){try{return localStorage.getItem(k)}catch(e){return null}}
function lsSet(k,v){try{localStorage.setItem(k,v)}catch(e){}}
const saved=lsGet(TKEY);
if(saved)root.dataset.theme=saved; else if(window.matchMedia&&matchMedia('(prefers-color-scheme: dark)').matches)root.dataset.theme='dark';
function ready(fn){if(document.readyState!=='loading')fn();else document.addEventListener('DOMContentLoaded',fn);}
function main(){
 const tb=document.getElementById('themeBtn');
 function paintTheme(){if(!tb)return;const dark=root.dataset.theme==='dark';tb.textContent=dark?'Light':'Dark';tb.setAttribute('aria-label',dark?'Switch to light mode':'Switch to dark mode');}
 if(tb)tb.onclick=()=>{root.dataset.theme=root.dataset.theme==='dark'?'light':'dark';lsSet(TKEY,root.dataset.theme);paintTheme();document.dispatchEvent(new Event('themechange'));};
 paintTheme();
 const db=document.getElementById('doneBtn'), lid=document.body.dataset.lid;
 function st(){try{return JSON.parse(lsGet(PKEY))||{}}catch(e){return {}}}
 function paint(){const s=st();if(!db)return;const on=!!s[lid];db.classList.toggle('isdone',on);db.textContent=on?'Completed ('+s[lid]+')':'Mark lesson complete';}
 if(db){db.onclick=()=>{const s=st();if(s[lid])delete s[lid];else s[lid]=new Date().toISOString().slice(0,10);lsSet(PKEY,JSON.stringify(s));paint();};paint();}
 const readBtn=document.getElementById('readBtn'), readView=document.getElementById('readView');
 if(readBtn&&readView)readBtn.onclick=()=>{const text='Read '+readView.href;
  const done=()=>{readBtn.textContent='Copied';setTimeout(()=>{readBtn.textContent='Copy for LLM';},1500);};
  if(navigator.clipboard&&window.isSecureContext)navigator.clipboard.writeText(text).then(done,()=>fallback(text,done));else fallback(text,done);};
 const pl=document.querySelector('.progressline');
 if(pl)window.addEventListener('scroll',()=>{const h=document.documentElement;pl.style.width=(100*h.scrollTop/Math.max(1,h.scrollHeight-h.clientHeight))+'%';},{passive:true});
 const tbtn=document.getElementById('tocBtn'),toc=document.querySelector('.toc');
 if(tbtn&&toc){tbtn.onclick=()=>toc.classList.toggle('open');toc.addEventListener('click',e=>{if(e.target.closest('a')&&innerWidth<=1000)toc.classList.remove('open');});}
 buildToc(); highlightAll(); initQuizzes(); initAnnot();
 if(window.renderMathInElement){
  try{renderMathInElement(document.querySelector('main'),{delimiters:[{left:'$$',right:'$$',display:true},{left:'\\[',right:'\\]',display:true},{left:'\\(',right:'\\)',display:false}],throwOnError:false,ignoredTags:['script','noscript','style','textarea','pre','code']});}catch(e){console.warn(e)}
 }
 if(window.CLPNViz)window.CLPNViz.initAll();
}
function buildToc(){
 const toc=document.querySelector('.toc .toc-local')||document.querySelector('.toc'); if(!toc)return;
 const hs=[...document.querySelectorAll('main .sec>h2, main .sec>h3')];
 let html='<b>'+(document.body.classList.contains('matpage')?'On This Page':'In This Lesson')+'</b>',i=0;
 hs.forEach(h=>{if(!h.id)h.id='h'+(++i);const t=h.cloneNode(true);t.querySelectorAll('.stag').forEach(x=>x.remove());
  html+='<a href="#'+h.id+'" class="'+(h.tagName==='H3'?'lv3':'')+'">'+t.textContent.trim()+'</a>';});
 toc.innerHTML=html;
 const links=[...toc.querySelectorAll('a')];
 if('IntersectionObserver' in window){
  const io=new IntersectionObserver(es=>es.forEach(en=>{if(en.isIntersecting)links.forEach(a=>a.classList.toggle('active',a.getAttribute('href')==='#'+en.target.id));}),{rootMargin:'-8% 0px -80% 0px'});
  hs.forEach(h=>io.observe(h));
 }
}
const KW=new Set(['function','if','else','for','in','while','repeat','break','next','return','TRUE','FALSE','NULL','NA','NaN','Inf','NA_real_','NA_integer_','NA_character_']);
function esc(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function hlR(src){
 let out='',i=0,n=src.length;
 while(i<n){
  const c=src[i];
  if(c==='#'){let j=src.indexOf('\n',i);if(j<0)j=n;out+='<span class="cm">'+esc(src.slice(i,j))+'</span>';i=j;continue;}
  if(c==='"'||c==="'"){let j=i+1;while(j<n&&src[j]!==c){if(src[j]==='\\')j++;j++;}j=Math.min(n,j+1);out+='<span class="st">'+esc(src.slice(i,j))+'</span>';i=j;continue;}
  if(/[0-9]/.test(c)&&!/[A-Za-z_.0-9]/.test(src[i-1]||' ')){const m=/^[0-9]*\.?[0-9]+(e[-+]?[0-9]+)?L?/.exec(src.slice(i));if(m){out+='<span class="nu">'+m[0]+'</span>';i+=m[0].length;continue;}}
  if(/[A-Za-z_.]/.test(c)){const m=/^[A-Za-z_.][A-Za-z0-9_.]*/.exec(src.slice(i));const w=m[0];let k=i+w.length;
   if(KW.has(w))out+='<span class="kw">'+w+'</span>';else if(src[k]==='(')out+='<span class="fn">'+w+'</span>';else out+=esc(w);i=k;continue;}
  const two=src.slice(i,i+3);
  if(two.startsWith('<-')||two.startsWith('|>')||two.startsWith('%>%')||two.startsWith('==')||two.startsWith('!=')||two.startsWith('<=')||two.startsWith('>=')){const len=two.startsWith('%>%')?3:2;out+='<span class="op">'+esc(src.slice(i,i+len))+'</span>';i+=len;continue;}
  out+=esc(c);i++;
 }
 return out;
}
function highlightAll(){
 document.querySelectorAll('pre>code.language-r').forEach(cd=>{cd.innerHTML=hlR(cd.textContent);});
 document.querySelectorAll('.codeblk').forEach(b=>{
  const pre=b.querySelector('pre');if(!pre||pre.classList.contains('out'))return;
  const btn=document.createElement('button');btn.className='copybtn';btn.type='button';btn.textContent='Copy';
  btn.onclick=()=>{const t=pre.innerText;const done=()=>{btn.textContent='Copied';btn.classList.add('ok');setTimeout(()=>{btn.textContent='Copy';btn.classList.remove('ok')},1500);};
   if(navigator.clipboard&&window.isSecureContext)navigator.clipboard.writeText(t).then(done,()=>fallback(t,done));else fallback(t,done);};
  const wrap=document.createElement('div');wrap.className='prewrap';
  pre.parentNode.insertBefore(wrap,pre);wrap.appendChild(pre);wrap.appendChild(btn);
 });
}
function fallback(t,done){const ta=document.createElement('textarea');ta.value=t;ta.style.position='fixed';ta.style.opacity='0';document.body.appendChild(ta);ta.select();try{document.execCommand('copy');}catch(e){}ta.remove();done();}
function initQuizzes(){
 const qs=[...document.querySelectorAll('.quiz')];let k=0;const score={right:0,first:0,total:qs.length};
 const sb=document.querySelectorAll('.quizscore');
 function upd(){sb.forEach(s=>s.textContent='Quiz score on this page: '+score.right+' / '+score.total+' correct ('+score.first+' correct on first try)');}
 qs.forEach(q=>{
  k++;const qt=q.querySelector('.qtext');if(qt)qt.insertAdjacentHTML('afterbegin','<span class="qn">Q'+k+'</span>');
  const fb=q.querySelector('.fb'),exp=q.querySelector('.qexp');let tries=0,done=false;
  function finish(first){done=true;score.right++;if(first)score.first++;upd();}
  function showGood(extra){fb.className='fb show good';fb.innerHTML='<b>Correct.</b> '+(extra||'')+(exp?'<div style="margin-top:6px">'+exp.innerHTML+'</div>':'');}
  function addReveal(reveal){if(tries>=2&&!q.querySelector('.reveal')){const r=document.createElement('button');r.className='qbtn ghost reveal';r.type='button';r.textContent='Show Answer & Explanation';r.style.marginTop='8px';r.onclick=()=>{reveal();r.remove();};q.appendChild(r);}}
  if(q.dataset.kind==='mc'){
   const bs=[...q.querySelectorAll('.opts button')];
   bs.forEach(b=>b.onclick=()=>{
    if(done)return;const ofb=b.parentElement.querySelector('.ofb');const t=ofb?ofb.innerHTML:'';
    if(b.dataset.ok==='1'){b.classList.add('right');bs.forEach(x=>x.disabled=true);showGood(t);finish(tries===0);const r=q.querySelector('.reveal');if(r)r.remove();}
    else{tries++;b.classList.add('wrong');b.disabled=true;fb.className='fb show bad';fb.innerHTML='<b>Not quite.</b> '+(t||'Re-read the key terms in the question.')+(tries>=2?'':' <span class="muted">(Try again)</span>');
     addReveal(()=>{const ok=bs.find(x=>x.dataset.ok==='1');ok.classList.add('right');bs.forEach(x=>x.disabled=true);const o=ok.parentElement.querySelector('.ofb');done=true;upd();fb.className='fb show good';fb.innerHTML='<b>Correct answer:</b> '+ok.innerHTML+' '+(o?o.innerHTML:'')+(exp?'<div style="margin-top:6px">'+exp.innerHTML+'</div>':'');});}
   });
  } else {
   const inp=q.querySelector('input'),btn=q.querySelector('.qbtn');
   const check=()=>{if(done)return;const v=inp.value.trim();if(!v)return;let ok=false;
    if(q.dataset.kind==='num'){const x=parseFloat(v.replace('，','.').replace(',', '.'));ok=isFinite(x)&&Math.abs(x-parseFloat(q.dataset.ans))<=parseFloat(q.dataset.tol||'0')+1e-9;}
    else{const norm=s=>s.replace(/\s+/g,'').replace(/[“”]/g,'"').replace(/[‘’]/g,"'").toLowerCase();ok=q.dataset.ans.split('||').some(a=>norm(a)===norm(v));}
    if(ok){inp.disabled=true;btn.disabled=true;showGood('');finish(tries===0);const r=q.querySelector('.reveal');if(r)r.remove();}
    else{tries++;fb.className='fb show bad';const h=q.querySelector('.qhint');fb.innerHTML='<b>Not quite.</b> '+(h?h.innerHTML:'Check your calculation steps.');
     addReveal(()=>{done=true;inp.disabled=true;btn.disabled=true;fb.className='fb show good';fb.innerHTML='<b>Reference answer:</b> <code>'+esc(q.dataset.show||q.dataset.ans.split('||')[0])+'</code>'+(exp?'<div style="margin-top:6px">'+exp.innerHTML+'</div>':'');});}
   };
   btn.onclick=check;inp.addEventListener('keydown',e=>{if(e.key==='Enter')check();});
  }
 });
 upd();
}
function initAnnot(){
 document.querySelectorAll('.annot').forEach(a=>{
  const box=a.parentElement.querySelector('.annotbox')||(()=>{const d=document.createElement('div');d.className='readout annotbox';d.textContent='Click any dashed-underlined item above to view its explanation.';a.after(d);return d;})();
  a.querySelectorAll('span[data-tip]').forEach(s=>s.onclick=()=>{a.querySelectorAll('span.on').forEach(x=>x.classList.remove('on'));s.classList.add('on');box.textContent=s.dataset.tip;});
 });
}
window.CLPNCore={hlR:hlR,esc:esc};
ready(main);
})();

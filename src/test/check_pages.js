// 用无头 Chrome（CDP）加载每个课件，收集 JS 异常 / console.error，并“点一遍”所有交互控件。
// 用法：node src/test/check_pages.js [lessons/L0-1.html ...]（不给参数 = 全站每一页）
const {spawn}=require('child_process');const path=require('path');const fs=require('fs');
const ROOT=path.resolve(__dirname,'../..');
const ls=(d,re)=>fs.existsSync(path.join(ROOT,d))?fs.readdirSync(path.join(ROOT,d)).filter(f=>re.test(f)).sort((a,b)=>a.localeCompare(b,'en',{numeric:true})).map(f=>path.join(ROOT,d,f)):[];
// 不给参数时检查全站每一页（与 check_all.js 相同的清单）
let files=process.argv.slice(2);
if(!files.length)files=['index.html','START_HERE.html','downloads/index.html','R/README.html','data/data_dictionary.html'].map(f=>path.join(ROOT,f)).filter(f=>fs.existsSync(f))
  .concat(ls('lessons',/^L\d+-\d+\.html$/),ls('materials',/\.html$/),ls('R/output',/\.html$/));const port=9333+Math.floor(Math.random()*500);
const chrome=spawn(require('./chrome_path'),['--headless=new','--no-sandbox','--disable-gpu','--remote-debugging-port='+port,'--user-data-dir=/tmp/cdp-'+port,'about:blank'],{stdio:'ignore'});
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
(async()=>{
 let ver;for(let i=0;i<50;i++){try{ver=await (await fetch('http://127.0.0.1:'+port+'/json/list')).json();if(ver.length)break;}catch(e){}await sleep(200);}
 const page=ver.find(t=>t.type==='page');const ws=new WebSocket(page.webSocketDebuggerUrl);
 let id=0;const pend={};const events=[];
 ws.onmessage=m=>{const d=JSON.parse(m.data);if(d.id&&pend[d.id]){pend[d.id](d);delete pend[d.id];}else events.push(d);};
 await new Promise(r=>ws.onopen=r);
 const send=(method,params={})=>new Promise(r=>{const i=++id;pend[i]=r;ws.send(JSON.stringify({id:i,method,params}));});
 await send('Runtime.enable');await send('Log.enable');await send('Page.enable');
 let fail=0;
 for(const f of files){
  events.length=0;const url='file://'+path.resolve(f);
  await send('Page.navigate',{url});await sleep(2500);
  // 交互：点所有 widget 按钮、拖动滑块、点测验选项、展开答案
  const r=await send('Runtime.evaluate',{expression:`(async()=>{const S=ms=>new Promise(r=>setTimeout(r,ms));let n=0;
   for(const b of document.querySelectorAll('.widget button, .widget .pane')){b.click();n++;await S(5);}
   for(const s of document.querySelectorAll('.widget input[type=range]')){for(const v of [s.min,s.max,(+s.min+ +s.max)/2]){s.value=v;s.dispatchEvent(new Event('input'));n++;}}
   for(const c of document.querySelectorAll('.widget input[type=checkbox]')){c.click();c.click();n++;}
   for(const sp of document.querySelectorAll('.annot span[data-tip]')){sp.click();n++;}
   for(const q of document.querySelectorAll('.quiz')){const bs=q.querySelectorAll('.opts button');bs.forEach(b=>{b.click();n++;});const i=q.querySelector('input');if(i){i.value='0';q.querySelector('.qbtn').click();q.querySelector('.qbtn').click();const rv=q.querySelector('.reveal');if(rv)rv.click();n++;}}
   document.querySelectorAll('details').forEach(d=>d.open=true);
   const kerr=document.querySelectorAll('.katex-error').length, kat=document.querySelectorAll('.katex').length;
   const raw=[...document.querySelectorAll('main p, main li, main dd, main dt, main td')].filter(e=>/\\\\\\(|\\$\\$/.test(e.textContent)&&!e.closest('pre,code')).length;
   const svgs=document.querySelectorAll('.widget svg').length, wid=document.querySelectorAll('.widget').length, empty=[...document.querySelectorAll('.widget')].filter(w=>w.children.length<2).map(w=>w.dataset.widget);
   return JSON.stringify({clicks:n,katex:kat,katexErr:kerr,rawTex:raw,widgets:wid,svgs,empty,quizzes:document.querySelectorAll('.quiz').length,score:(document.querySelector('.quizscore')||{}).textContent,toc:document.querySelectorAll('.toc a').length,h:document.body.scrollHeight});})()`,awaitPromise:true,returnByValue:true});
  await sleep(300);
  const errs=events.filter(e=>e.method==='Runtime.exceptionThrown'||(e.method==='Runtime.consoleAPICalled'&&['error','warning'].includes(e.params.type))||(e.method==='Log.entryAdded'&&e.params.entry.level==='error'))
   .map(e=>e.method==='Runtime.exceptionThrown'?'EXC '+(e.params.exceptionDetails.exception?e.params.exceptionDetails.exception.description:e.params.exceptionDetails.text):e.method==='Log.entryAdded'?'LOG '+e.params.entry.text+' '+(e.params.entry.url||''):'CON '+e.params.args.map(a=>a.value||a.description).join(' '));
  const info=r.result&&r.result.result?r.result.result.value:JSON.stringify(r);
  console.log((errs.length?'✗ ':'✓ ')+f+' '+info);errs.forEach(e=>console.log('    '+e));if(errs.length)fail++;
 }
 ws.close();chrome.kill();process.exit(fail?1:0);
})().catch(e=>{console.error(e);chrome.kill();process.exit(2);});

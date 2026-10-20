/* CLPN Course · Interactive Visualization Components (Vanilla JS + SVG, zero external dependencies)
   Usage: <div class="widget" data-widget="corr"></div>, auto-initialized on page load. */
(function(){
"use strict";
const NS="http://www.w3.org/2000/svg";
// ---------- Utilities ----------
function rng(seed){let a=seed>>>0;return function(){a|=0;a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296;};}
function randn(r){let u=0,v=0;while(u===0)u=r();while(v===0)v=r();return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v);}
const mean=a=>a.reduce((s,x)=>s+x,0)/a.length;
const sd=a=>{const m=mean(a);return Math.sqrt(a.reduce((s,x)=>s+(x-m)*(x-m),0)/(a.length-1));};
const median=a=>{const b=[...a].sort((x,y)=>x-y),n=b.length;return n%2?b[(n-1)/2]:(b[n/2-1]+b[n/2])/2;};
function cor(x,y){const mx=mean(x),my=mean(y);let sxy=0,sxx=0,syy=0;for(let i=0;i<x.length;i++){sxy+=(x[i]-mx)*(y[i]-my);sxx+=(x[i]-mx)**2;syy+=(y[i]-my)**2;}return sxy/Math.sqrt(sxx*syy);}
function cov(x,y){const mx=mean(x),my=mean(y);let s=0;for(let i=0;i<x.length;i++)s+=(x[i]-mx)*(y[i]-my);return s/(x.length-1);}
function ols(x,y){const mx=mean(x),my=mean(y);let sxy=0,sxx=0;for(let i=0;i<x.length;i++){sxy+=(x[i]-mx)*(y[i]-my);sxx+=(x[i]-mx)**2;}const b1=sxy/sxx;return[my-b1*mx,b1];}
const f2=x=>(Math.abs(x)<5e-4?0:x).toFixed(2), f3=x=>(Math.abs(x)<5e-5?0:x).toFixed(3);
function lin(d0,d1,r0,r1){const f=v=>r0+(v-d0)/(d1-d0)*(r1-r0);f.inv=p=>d0+(p-r0)/(r1-r0)*(d1-d0);return f;}
function el(tag,attrs,parent,text){const e=document.createElementNS(NS,tag);for(const k in attrs)e.setAttribute(k,attrs[k]);if(text!=null)e.textContent=text;if(parent)parent.appendChild(e);return e;}
function svg(w,h,parent){const s=el('svg',{viewBox:'0 0 '+w+' '+h,role:'img'});parent.appendChild(s);return s;}
function clear(s){while(s.firstChild)s.removeChild(s.firstChild);}
function h(tag,attrs,html){const e=document.createElement(tag);if(attrs)for(const k in attrs)e.setAttribute(k,attrs[k]);if(html!=null)e.innerHTML=html;return e;}
function cssv(n){return getComputedStyle(document.documentElement).getPropertyValue(n).trim()||'#888';}
function slider(box,label,min,max,step,val,fmt){const l=h('label');const s=h('input',{type:'range',min:min,max:max,step:step,value:val});const o=h('b');const f=fmt||(v=>v);l.append(label,s,o);o.textContent=f(+val);s.addEventListener('input',()=>o.textContent=f(+s.value));box.appendChild(l);return s;}
function btn(box,text,fn){const b=h('button',{type:'button'},text);b.onclick=fn;box.appendChild(b);return b;}
function ctrl(w){const c=h('div',{class:'ctrl'});w.appendChild(c);return c;}
function readout(w){const r=h('div',{class:'readout'});w.appendChild(r);return r;}
function title(w,t){if(!w.querySelector('.wtitle'))w.prepend(h('div',{class:'wtitle'},t));}
function note(w,t){w.appendChild(h('p',{class:'wnote'},t));}
function axes(s,X,Y,xl,yl,opt){opt=opt||{};const g=el('g',{},s);const ink=cssv('--muted');
 el('line',{x1:X.r0,y1:Y.r0,x2:X.r1,y2:Y.r0,stroke:ink},g);el('line',{x1:X.r0,y1:Y.r0,x2:X.r0,y2:Y.r1,stroke:ink},g);
 (opt.xt||[]).forEach(v=>{el('line',{x1:X(v),y1:Y.r0,x2:X(v),y2:Y.r0+4,stroke:ink},g);el('text',{x:X(v),y:Y.r0+16,'text-anchor':'middle','font-size':11},g,opt.xf?opt.xf(v):v);});
 (opt.yt||[]).forEach(v=>{el('line',{x1:X.r0-4,y1:Y(v),x2:X.r0,y2:Y(v),stroke:ink},g);el('text',{x:X.r0-7,y:Y(v)+4,'text-anchor':'end','font-size':11},g,opt.yf?opt.yf(v):v);});
 if(xl)el('text',{x:(X.r0+X.r1)/2,y:Y.r0+32,'text-anchor':'middle','font-size':12},g,xl);
 if(yl)el('text',{x:14,y:(Y.r0+Y.r1)/2,'text-anchor':'middle','font-size':12,transform:'rotate(-90 14 '+(Y.r0+Y.r1)/2+')'},g,yl);return g;}
function sc(d0,d1,r0,r1){const f=lin(d0,d1,r0,r1);f.r0=r0;f.r1=r1;f.d0=d0;f.d1=d1;return f;}
function ticks(a,b,n){const st=(b-a)/n,o=[];for(let i=0;i<=n;i++)o.push(+(a+i*st).toFixed(6));return o;}
function svgPt(s,ev){const p=s.createSVGPoint();p.x=ev.clientX;p.y=ev.clientY;return p.matrixTransform(s.getScreenCTM().inverse());}
function histo(vals,lo,hi,nb){const c=new Array(nb).fill(0),w=(hi-lo)/nb;vals.forEach(v=>{let k=Math.floor((v-lo)/w);if(k>=0&&k<nb)c[k]++;else if(v===hi)c[nb-1]++;});return c;}
const W={};

// ---------- 0.1 Course Map ----------
W.coursemap=function(w){title(w,'Course Map: Click each module');
 const mods=window.COURSE_MODULES||[];const row=h('div',{style:'display:flex;flex-wrap:wrap;gap:6px'});w.appendChild(row);const info=readout(w);info.style.whiteSpace='normal';
 mods.forEach((m,i)=>{const b=h('button',{type:'button',style:'border-left:5px solid '+m.color},m.id+' '+m.short);b.onclick=()=>{row.querySelectorAll('button').forEach(x=>x.classList.remove('on'));b.classList.add('on');
  info.innerHTML='<b>'+m.id+' · '+m.title+'</b> ('+m.n+' lessons, ~'+m.hours+' hours)<br>'+m.intro+'<br><span class="muted">Provides for CLPN: </span>'+(m.gives||'');};row.appendChild(b);if(i===0)b.click();});
};
// ---------- 0.2 Latent Variable vs. Network ----------
W.netspread=function(w){title(w,'Common Cause Model vs. Network Model: Click a symptom and see what happens');
 const names=['Low mood','Insomnia','Fatigue','Poor focus','Loneliness','Anhedonia'];
 const pos=[[300,70],[130,150],[150,280],[300,330],[460,280],[470,150]];
 const E=[[0,5,.5],[1,2,.6],[2,3,.5],[4,0,.5],[5,2,.3],[0,3,.2],[4,5,.3]];
 let mode='net',a=new Array(6).fill(0),t=0;
 const c=ctrl(w);const bn=btn(c,'Network Model',()=>{mode='net';reset();});const bl=btn(c,'Common Cause (Latent) Model',()=>{mode='lat';reset();});
 btn(c,'Next Step',step);btn(c,'Reset',reset);
 const s=svg(600,400,w);const r=readout(w);
 function reset(){a=new Array(6).fill(0);t=0;bn.classList.toggle('on',mode==='net');bl.classList.toggle('on',mode==='lat');draw();r.textContent=mode==='net'?'Network model: Symptoms are directly connected. Click any symptom to activate it (e.g., insomnia after job loss), then click "Next Step".':'Common cause model: All symptoms are caused solely by the latent "Depression" variable in the center, with no direct edges between symptoms. Click a symptom, then click "Next Step".';}
 function step(){t++;if(mode==='net'){const n=a.map((v,i)=>{let s2=.6*v;E.forEach(([p,q,wt])=>{if(p===i)s2+=wt*a[q];if(q===i)s2+=wt*a[p];});return Math.min(1,s2);});a=n;}
  else{a=a.map(v=>v*.6);}draw();
  r.textContent='Time t = '+t+'. '+(mode==='net'?'Activated symptoms spread to their neighbors across the network—this is "symptom mutual maintenance." Notice that directly connected symptoms are affected first.':'Symptoms are merely "indicators" of the latent variable; changes in one symptom do not spread to others (it simply fades away). For all symptoms to change together, the latent variable itself must change.');}
 function draw(){clear(s);const acc=cssv('--accent');
  if(mode==='lat'){el('circle',{cx:300,cy:200,r:42,fill:'none',stroke:acc,'stroke-width':2,'stroke-dasharray':'5 4'},s);el('text',{x:300,y:205,'text-anchor':'middle','font-size':14,'font-weight':700},s,'"Depression"');
   pos.forEach(p=>{const dx=p[0]-300,dy=p[1]-200,L=Math.hypot(dx,dy);el('line',{x1:300+dx/L*44,y1:200+dy/L*44,x2:p[0]-dx/L*34,y2:p[1]-dy/L*34,stroke:acc,'stroke-width':1.6,'marker-end':'url(#ar'+w._id+')'},s);});}
  else E.forEach(([p,q,wt])=>el('line',{x1:pos[p][0],y1:pos[p][1],x2:pos[q][0],y2:pos[q][1],stroke:'#3b82f6','stroke-width':1+wt*8,'stroke-opacity':.55},s));
  const d=el('defs',{},s);const m=el('marker',{id:'ar'+w._id,viewBox:'0 0 10 10',refX:9,refY:5,markerWidth:7,markerHeight:7,orient:'auto'},d);el('path',{d:'M0,0L10,5L0,10z',fill:acc},m);
  pos.forEach((p,i)=>{const g=el('g',{style:'cursor:pointer'},s);el('circle',{cx:p[0],cy:p[1],r:32,fill:'rgba(239,68,68,'+(0.08+a[i]*.85).toFixed(2)+')',stroke:'#ef4444','stroke-width':1.5},g);
   el('text',{x:p[0],y:p[1]+4,'text-anchor':'middle','font-size':11},g,names[i]);g.addEventListener('click',()=>{a[i]=1;draw();});});}
 reset();
};
// ---------- 1.1 Identical Total Score, Different Profiles ----------
W.sametotal=function(w){title(w,'Identical Total Score, Completely Different Problems');
 const items=['Interest','Mood','Sleep','Fatigue','Appetite','Self-worth','Focus','Motor','Ideation'];
 const c=ctrl(w);const tot=slider(c,'Total score = ',4,22,1,12);btn(c,'New Pair of Profiles',draw);
 const s=svg(640,300,w);note(w,'PHQ-9 items are scored 0–3 each. Both individuals have identical total scores, but Person A struggles mainly with sleep problems and fatigue, while Person B struggles with depressed mood and low self-worth. Relying solely on the total score, a social worker would assign the exact same severity rating; looking at item-level profiles, the targets for clinical intervention are completely different.');
 tot.addEventListener('input',draw);let seed=7;
 function prof(T,r,bias){const v=new Array(9).fill(0);let left=T,guard=0;while(left>0&&guard++<500){const wts=bias.map(b=>b*r()+.05);let k=0,tw=wts.reduce((a,b)=>a+b),u=r()*tw;while(u>wts[k]){u-=wts[k];k++;}if(v[k]<3){v[k]++;left--;}}return v;}
 function draw(){seed++;const r=rng(seed);const T=+tot.value;const A=prof(T,r,[.3,.3,3,3,1,.2,1,.6,.1]),B=prof(T,r,[1,3,.3,.3,.3,3,.5,.2,.8]);clear(s);
  const X=i=>70+i*62;[[A,'Person A',-1,'#0ea5e9'],[B,'Person B',1,'#ec4899']].forEach(([v,nm,o,col])=>{v.forEach((x,i)=>{el('rect',{x:X(i)+(o>0?14:-2),y:230-x*55,width:14,height:x*55,fill:col},s);});el('text',{x:o<0?300:470,y:24,'font-size':13,fill:col},s,'■ '+nm+' (Total: '+v.reduce((a,b)=>a+b)+')');});
  items.forEach((t,i)=>el('text',{x:X(i)+13,y:250,'text-anchor':'middle','font-size':10},s,t));[0,1,2,3].forEach(k=>{el('text',{x:40,y:234-k*55,'font-size':11},s,k);el('line',{x1:52,x2:620,y1:230-k*55,y2:230-k*55,stroke:cssv('--line')},s);});}
 draw();
};
// ---------- 1.2 Deviations and Variance ----------
W.devsq=function(w){title(w,'Drag the dots: Variance is the average of squared deviations');
 let v=[8,10,9,14,7,12];const s=svg(640,240,w);const r=readout(w);const X=sc(4,16,40,610);let drag=-1;
 s.addEventListener('pointerdown',e=>{const p=svgPt(s,e);let b=-1,bd=30;v.forEach((x,i)=>{if(Math.abs(X(x)-p.x)<bd&&Math.abs(p.y-(60+i*20))<14){bd=Math.abs(X(x)-p.x);b=i;}});drag=b;if(b>=0)s.setPointerCapture(e.pointerId);});
 s.addEventListener('pointermove',e=>{if(drag<0)return;const p=svgPt(s,e);v[drag]=Math.max(4,Math.min(16,Math.round(X.inv(p.x)*2)/2));draw();});
 s.addEventListener('pointerup',()=>drag=-1);
 function draw(){clear(s);const m=mean(v);const line=cssv('--line');
  for(let k=4;k<=16;k++){el('line',{x1:X(k),x2:X(k),y1:40,y2:200,stroke:line},s);el('text',{x:X(k),y:220,'text-anchor':'middle','font-size':11},s,k);}
  el('line',{x1:X(m),x2:X(m),y1:30,y2:205,stroke:'#ef4444','stroke-width':2},s);el('text',{x:X(m),y:24,'text-anchor':'middle','font-size':12,fill:'#ef4444'},s,'Mean x̄ = '+f2(m));
  v.forEach((x,i)=>{const y=60+i*20;el('line',{x1:X(m),x2:X(x),y1:y,y2:y,stroke:x>=m?'#10b981':'#f59e0b','stroke-width':3},s);el('circle',{cx:X(x),cy:y,r:8,fill:'#6366f1',style:'cursor:grab'},s);});
  const dev=v.map(x=>x-m),sq=dev.map(d=>d*d),ss=sq.reduce((a,b)=>a+b);
  r.textContent='Loneliness scores: '+v.join(', ')+'\nDeviations (x − x̄): '+dev.map(f2).join(', ')+' (always sums to '+f2(dev.reduce((a,b)=>a+b))+')\nSquared deviations (x − x̄)²: '+sq.map(f2).join(', ')+'\nSum of squares SS = '+f2(ss)+'; Variance = '+f2(ss)+' / (6 − 1) = '+f2(ss/5)+'; Standard deviation SD = √'+f2(ss/5)+' = '+f2(Math.sqrt(ss/5));}
 draw();
};
// ---------- 1.2 Distribution Shapes ----------
W.dist=function(w){title(w,'Distribution Shape Lab: Skewness, Ceiling and Floor Effects');
 const c=ctrl(w);const sk=slider(c,'Skewness',-3,3,.5,0,v=>v>0?'Right-skewed '+v:v<0?'Left-skewed '+(-v):'Symmetric');const sp=slider(c,'Spread (Dispersion)',.5,2,.1,1,v=>v.toFixed(1));
 const s=svg(640,280,w);const r=readout(w);const base=[],rr=rng(11);for(let i=0;i<2000;i++)base.push([randn(rr),rr()]);
 function gen(){const a=+sk.value,k=+sp.value;return base.map(([z,u])=>{let x=z;if(a!==0){const lam=Math.abs(a)*.35;x=(Math.exp(lam*z)-1)/lam;if(a<0)x=-x;}let v=Math.round(13.5+x*4.5*k);return Math.max(0,Math.min(27,v));});}
 function draw(){const v=gen();clear(s);const X=sc(-.5,27.5,50,620),cnt=histo(v.map(x=>x+.5),0,28,28),mx=Math.max(...cnt);const Y=sc(0,mx*1.1,240,20);
  axes(s,X,Y,'PHQ-9 Total Score (0–27)','Count',{xt:[0,5,10,15,20,25,27],yt:[0,Math.round(mx/2),mx]});
  cnt.forEach((n,i)=>el('rect',{x:X(i-.5)+1,y:Y(n),width:X(1)-X(0)-2,height:Y(0)-Y(n),fill:'#0ea5e9','fill-opacity':.7},s));
  const m=mean(v),md=median(v);el('line',{x1:X(m),x2:X(m),y1:20,y2:240,stroke:'#ef4444','stroke-width':2},s);el('line',{x1:X(md),x2:X(md),y1:20,y2:240,stroke:'#10b981','stroke-width':2,'stroke-dasharray':'5 3'},s);
  const n0=v.filter(x=>x===0).length,n27=v.filter(x=>x===27).length;
  r.textContent='Mean (solid red) = '+f2(m)+'   Median (dashed green) = '+f2(md)+'   SD = '+f2(sd(v))+'\nScored 0: '+n0+' ('+(100*n0/v.length).toFixed(1)+'%)   Scored 27: '+n27+' ('+(100*n27/v.length).toFixed(1)+'%)'+(n0>v.length*.05?'  ← Floor effect: clustering at lowest possible score':'')+(n27>v.length*.05?'  ← Ceiling effect: clustering at highest possible score':'')+'\n'+(Math.abs(m-md)>.4?(m>md?'Mean > Median: A few extreme high scores pull the mean to the right (right-skewed).':'Mean < Median: A few extreme low scores pull the mean to the left (left-skewed).'):'Mean ≈ Median: Distribution is roughly symmetric.');}
 sk.addEventListener('input',draw);sp.addEventListener('input',draw);draw();
};
// ---------- 1.2 Normal Distribution 68-95-99.7 ----------
W.normal=function(w){title(w,'Normal Distribution: The 68–95–99.7 Rule');
 const c=ctrl(w);const m=slider(c,'Mean μ',30,70,1,50);const s2=slider(c,'Standard deviation σ',4,15,1,10);const k=slider(c,'Shaded interval ±',1,3,1,1,v=>v+' σ');
 const s=svg(640,260,w);const r=readout(w);const P={1:68.27,2:95.45,3:99.73};
 function draw(){clear(s);const mu=+m.value,sg=+s2.value,kk=+k.value;const X=sc(0,100,40,620),Y=sc(0,.1,220,20);axes(s,X,Y,'Loneliness score','',{xt:[0,20,40,60,80,100]});
  const pdf=x=>Math.exp(-.5*((x-mu)/sg)**2)/(sg*Math.sqrt(2*Math.PI));let d='',ds='M'+X(Math.max(0,mu-kk*sg))+','+Y(0);
  for(let x=0;x<=100;x+=.5){d+=(x?'L':'M')+X(x)+','+Y(pdf(x));if(x>=mu-kk*sg&&x<=mu+kk*sg)ds+='L'+X(x)+','+Y(pdf(x));}
  ds+='L'+X(Math.min(100,mu+kk*sg))+','+Y(0)+'Z';el('path',{d:ds,fill:'#10b981','fill-opacity':.3},s);el('path',{d:d,fill:'none',stroke:'#0ea5e9','stroke-width':2.5},s);
  el('line',{x1:X(mu),x2:X(mu),y1:Y(0),y2:Y(pdf(mu)),stroke:'#ef4444','stroke-dasharray':'4 3'},s);
  r.textContent='μ ± '+kk+'σ = ['+(mu-kk*sg)+', '+(mu+kk*sg)+']: About '+P[kk]+'% of individuals fall in this range.\n(Total area under curve = 1 = 100% of population; larger σ makes the curve flatter and wider.)';}
 [m,s2,k].forEach(x=>x.addEventListener('input',draw));draw();
};
// ---------- 1.3 z-Score ----------
W.zscore=function(w){title(w,'Different Scales, One "Standard Ruler"');
 const c=ctrl(w);const a=slider(c,'Sleep problems dep3_t1 (0–3 points): ',0,3,1,1);const b=slider(c,'Life satisfaction life_sat_t1 (0–100): ',0,100,1,55);
 const s=svg(640,230,w);const r=readout(w);const A={m:.79,s:.94},B={m:64.32,s:14.81};
 function draw(){clear(s);const za=(a.value-A.m)/A.s,zb=(b.value-B.m)/B.s;const X=sc(-3,3,40,610);
  el('text',{x:40,y:24,'font-size':12},s,'Original scales:');
  const XA=sc(0,3,40,300),XB=sc(0,100,340,610);[0,1,2,3].forEach(v=>el('text',{x:XA(v),y:62,'text-anchor':'middle','font-size':11},s,v));[0,50,100].forEach(v=>el('text',{x:XB(v),y:62,'text-anchor':'middle','font-size':11},s,v));
  el('line',{x1:40,x2:300,y1:46,y2:46,stroke:'#0ea5e9','stroke-width':3},s);el('line',{x1:340,x2:610,y1:46,y2:46,stroke:'#ec4899','stroke-width':3},s);
  el('circle',{cx:XA(+a.value),cy:46,r:7,fill:'#0ea5e9'},s);el('circle',{cx:XB(+b.value),cy:46,r:7,fill:'#ec4899'},s);
  el('text',{x:40,y:110,'font-size':12},s,'z-scores (common scale, unit = 1 standard deviation):');
  el('line',{x1:40,x2:610,y1:160,y2:160,stroke:cssv('--muted')},s);for(let z=-3;z<=3;z++){el('line',{x1:X(z),x2:X(z),y1:155,y2:165,stroke:cssv('--muted')},s);el('text',{x:X(z),y:182,'text-anchor':'middle','font-size':11},s,z>0?'+'+z:z);}
  el('circle',{cx:X(Math.max(-3,Math.min(3,za))),cy:148,r:7,fill:'#0ea5e9'},s);el('circle',{cx:X(Math.max(-3,Math.min(3,zb))),cy:172-30,r:0},s);el('circle',{cx:X(Math.max(-3,Math.min(3,zb))),cy:135,r:7,fill:'#ec4899'},s);
  r.textContent='Sleep problems: z = ('+a.value+' − '+A.m+') / '+A.s+' = '+f2(za)+'\nLife satisfaction: z = ('+b.value+' − '+B.m+') / '+B.s+' = '+f2(zb)+'\n'+(Math.abs(za)>Math.abs(zb)?'This person is relatively more "extreme" on sleep problems (further away from its mean).':'This person is relatively more "extreme" on life satisfaction (further away from its mean).')+'\n(Means and SDs from course dataset T1: sleep problems 0.79 / 0.94; life satisfaction 64.32 / 14.81)';}
 a.addEventListener('input',draw);b.addEventListener('input',draw);draw();
};
// ---------- 1.4 Correlation ----------
W.corr=function(w){title(w,'Drag the slider to build intuition for correlation r');
 const c=ctrl(w);const rs=slider(c,'Target correlation ρ',-1,1,.05,.5,v=>v.toFixed(2));const nz=slider(c,'Sample size n',10,300,10,100);
 const showQ=h('label');const cb=h('input',{type:'checkbox'});showQ.append(cb,' Show z-product quadrants');c.appendChild(showQ);btn(c,'Resample',()=>{seed++;draw();});
 const s=svg(640,380,w);const r=readout(w);let seed=3;
 function draw(){const rr=rng(seed),n=+nz.value,rho=+rs.value;const x=[],y=[];for(let i=0;i<n;i++){const a=randn(rr),b=randn(rr);x.push(a);y.push(rho*a+Math.sqrt(1-rho*rho)*b);}
  const X0=x.map(v=>5+v*1.5),Y0=y.map(v=>5+v*1.5);
  clear(s);const X=sc(0,10,60,620),Y=sc(0,10,340,20);axes(s,X,Y,'Loneliness (T1)','Depression (T1)',{xt:[0,2,4,6,8,10],yt:[0,5,10]});
  const mx=mean(X0),my=mean(Y0);
  if(cb.checked){el('rect',{x:X(mx),y:Y(10),width:X(10)-X(mx),height:Y(my)-Y(10),fill:'#10b981','fill-opacity':.1},s);el('rect',{x:X(0),y:Y(my),width:X(mx)-X(0),height:Y(0)-Y(my),fill:'#10b981','fill-opacity':.1},s);
   el('rect',{x:X(0),y:Y(10),width:X(mx)-X(0),height:Y(my)-Y(10),fill:'#ef4444','fill-opacity':.08},s);el('rect',{x:X(mx),y:Y(my),width:X(10)-X(mx),height:Y(0)-Y(my),fill:'#ef4444','fill-opacity':.08},s);
   el('text',{x:X(9.6),y:Y(9.5),'text-anchor':'end','font-size':13,fill:'#059669'},s,'(+)(+) = +');el('text',{x:X(.4),y:Y(.4),'font-size':13,fill:'#059669'},s,'(−)(−) = +');el('text',{x:X(.4),y:Y(9.5),'font-size':13,fill:'#dc2626'},s,'(−)(+) = −');el('text',{x:X(9.6),y:Y(.4),'text-anchor':'end','font-size':13,fill:'#dc2626'},s,'(+)(−) = −');}
  el('line',{x1:X(mx),x2:X(mx),y1:Y(0),y2:Y(10),stroke:cssv('--muted'),'stroke-dasharray':'3 3'},s);el('line',{x1:X(0),x2:X(10),y1:Y(my),y2:Y(my),stroke:cssv('--muted'),'stroke-dasharray':'3 3'},s);
  X0.forEach((v,i)=>{if(v>0&&v<10&&Y0[i]>0&&Y0[i]<10)el('circle',{cx:X(v),cy:Y(Y0[i]),r:3.5,fill:'#6366f1','fill-opacity':.7},s);});
  const rv=cor(X0,Y0),pos=X0.filter((v,i)=>(v-mx)*(Y0[i]-my)>0).length;
  r.textContent='Sample correlation r = '+f3(rv)+'    Covariance cov = '+f3(cov(X0,Y0))+'\nPoints in "same-sign" quadrants (positive cross-product): '+pos+' / '+n+'\n'+(Math.abs(rv)<.1?'Virtually no linear relationship':Math.abs(rv)<.3?'Weak':Math.abs(rv)<.5?'Moderate':'Strong')+(rv>0?' positive correlation: Individuals with higher loneliness tend to report higher depression.':rv<0?' negative correlation: When one is higher, the other tends to be lower.':'')+' (Cohen\'s conventions: .1 small / .3 medium / .5 large)';}
 [rs,nz].forEach(x=>x.addEventListener('input',draw));cb.addEventListener('change',draw);draw();
};
// ---------- 1.5 Sampling Distribution ----------
W.sampling=function(w){title(w,'Virtual City Sampling Experiment: Distribution of the Sample Mean');
 const rr=rng(5),pop=[];for(let i=0;i<20000;i++){let g=0;for(let k=0;k<3;k++)g+=-Math.log(rr());pop.push(Math.min(80,20+g*6));}
 const mu=mean(pop),sig=Math.sqrt(pop.reduce((s,x)=>s+(x-mu)**2,0)/pop.length);let n=20,means=[];const r2=rng(99);
 const c=ctrl(w);const bs=[20,100,500].map(k=>btn(c,'n = '+k,()=>{n=k;means=[];bs.forEach(b=>b.classList.toggle('on',b.textContent==='n = '+k));draw();}));bs[0].classList.add('on');
 btn(c,'Draw 1 sample',()=>{draw1(1);});btn(c,'Draw 100 samples',()=>draw1(100));btn(c,'Draw 1,000 samples',()=>draw1(1000));
 const s=svg(640,330,w);const r=readout(w);
 function draw1(k){for(let j=0;j<k;j++){let t=0;for(let i=0;i<n;i++)t+=pop[Math.floor(r2()*pop.length)];means.push(t/n);}draw();}
 function draw(){clear(s);const X=sc(20,80,50,620);
  const pc=histo(pop,20,80,60),pm=Math.max(...pc),Yp=sc(0,pm,110,20);el('text',{x:50,y:16,'font-size':12},s,'Population (20,000 residents, loneliness, right-skewed): μ = '+f2(mu)+', σ = '+f2(sig));
  pc.forEach((v,i)=>el('rect',{x:X(20+i),y:Yp(v),width:X(21)-X(20)-.5,height:Yp(0)-Yp(v),fill:'#94a3b8'},s));
  const Y=sc(0,1,300,140);axes(s,X,Y,'Loneliness score / Sample mean','',{xt:[20,30,40,50,60,70,80]});
  if(means.length){const mc=histo(means,20,80,120),mm=Math.max(...mc);const Yb=sc(0,mm,300,150);mc.forEach((v,i)=>{if(v)el('rect',{x:X(20+i*.5),y:Yb(v),width:X(20.5)-X(20)-.3,height:Yb(0)-Yb(v),fill:'#0ea5e9'},s);});}
  el('line',{x1:X(mu),x2:X(mu),y1:20,y2:300,stroke:'#ef4444','stroke-dasharray':'4 3'},s);
  el('text',{x:620,y:160,'text-anchor':'end','font-size':12},s,'Below: One mean calculated per sample → Distribution of sample means');
  r.textContent='Each sample n = '+n+', total drawn = '+means.length+' samples.\n'+(means.length>1?'Standard deviation of sample means (empirical) = '+f3(sd(means))+'; Theoretical standard error SE = σ/√n = '+f2(sig)+'/√'+n+' = '+f3(sig/Math.sqrt(n))+'\nMean of sample means = '+f2(mean(means))+' (≈ μ)':'Click "Draw 100 samples" to start.');}
 draw();
};
// ---------- 1.5 Confidence Interval Coverage ----------
W.cicover=function(w){title(w,'50 Researchers Each Conduct a Survey: How Many 95% Confidence Intervals Contain the True Value?');
 const c=ctrl(w);const nn=slider(c,'Sample size per survey n',10,400,10,40);btn(c,'Rerun 50 Surveys',()=>{seed++;draw();});
 const s=svg(640,360,w);const r=readout(w);let seed=1;const MU=50,SG=12;
 function draw(){const rr=rng(seed),n=+nn.value;clear(s);const X=sc(38,62,40,620);axes(s,X,sc(0,1,340,10),'95% CI of Mean Loneliness (Red = Does not cover true μ = 50)','',{xt:[40,45,50,55,60]});
  el('line',{x1:X(MU),x2:X(MU),y1:10,y2:340,stroke:'#10b981','stroke-width':2},s);let miss=0;
  for(let k=0;k<50;k++){const xs=[];for(let i=0;i<n;i++)xs.push(MU+SG*randn(rr));const m=mean(xs),se=sd(xs)/Math.sqrt(n),lo=m-1.96*se,hi=m+1.96*se,bad=lo>MU||hi<MU;if(bad)miss++;
   const y=18+k*6.3,col=bad?'#ef4444':'#6366f1';el('line',{x1:X(Math.max(38,lo)),x2:X(Math.min(62,hi)),y1:y,y2:y,stroke:col,'stroke-width':bad?2.5:1.5},s);el('circle',{cx:X(m),cy:y,r:2,fill:col},s);}
  r.textContent=(50-miss)+' of 50 intervals contain the true value ('+(2*(50-miss))+'%). In the long run, about 95% will cover the truth.\nAs n increases, intervals become narrower (SE = SD/√n decreases), yet the coverage rate remains ~95%.\n(Note: 1.96 is a large-sample z-approximation; for very small n, the t-distribution yields slightly wider intervals.)';}
 nn.addEventListener('input',draw);draw();
};
// ---------- 1.6 p-Value ----------
W.pval=function(w){title(w,'p-Value = Probability of Observing a Result "At Least as Extreme" if H₀ is True');
 const c=ctrl(w);const zs=slider(c,'Observed test statistic z',0,4,.05,1.5,v=>v.toFixed(2));
 const s=svg(640,250,w);const r=readout(w);
 const Phi=x=>{const t=1/(1+.2316419*Math.abs(x)),d=.3989423*Math.exp(-x*x/2),p=d*t*(.3193815+t*(-.3565638+t*(1.781478+t*(-1.821256+t*1.330274))));return x>0?1-p:p;};
 function draw(){clear(s);const z=+zs.value;const X=sc(-4.2,4.2,40,620),Y=sc(0,.42,210,20);axes(s,X,Y,'Distribution of z when null hypothesis H₀ is true (Standard Normal)','',{xt:[-4,-3,-2,-1,0,1,2,3,4]});
  const pdf=x=>Math.exp(-x*x/2)/Math.sqrt(2*Math.PI);let d='';for(let x=-4.2;x<=4.2;x+=.05)d+=(d?'L':'M')+X(x)+','+Y(pdf(x));el('path',{d:d,fill:'none',stroke:'#0ea5e9','stroke-width':2.5},s);
  [1,-1].forEach(sg=>{let p='M'+X(sg*z)+','+Y(0);for(let x=z;x<=4.2;x+=.05)p+='L'+X(sg*x)+','+Y(pdf(x));p+='L'+X(sg*4.2)+','+Y(0)+'Z';el('path',{d:p,fill:'#ef4444','fill-opacity':.45},s);});
  [1.96,-1.96].forEach(v=>el('line',{x1:X(v),x2:X(v),y1:Y(0),y2:Y(.3),stroke:'#f59e0b','stroke-dasharray':'4 3'},s));el('text',{x:X(1.96),y:Y(.31),'text-anchor':'middle','font-size':11,fill:'#b45309'},s,'±1.96 (Critical value for α = .05)');
  const p=2*(1-Phi(z));r.textContent='Two-sided p = Sum of red tail areas on both sides = '+(p<.001?'< .001':p.toFixed(3))+'\n'+(p<.05?'p < .05: Reject H₀ by convention. This does NOT mean "probability that H₀ is true is '+p.toFixed(3)+'", nor does it indicate a large effect.':'p ≥ .05: Data are not incompatible with H₀. This does NOT mean "proven that there is no effect".');}
 zs.addEventListener('input',draw);draw();
};
// ---------- 1.6 Multiple Testing ----------
W.multitest=function(w){title(w,'190 Edges, All Truly Zero: How Many False Discoveries from Edge-by-Edge Testing?');
 const c=ctrl(w);const bon=h('label');const cb=h('input',{type:'checkbox'});bon.append(cb,' Apply Bonferroni correction (α / 190)');c.appendChild(bon);btn(c,'Re-run Study',()=>{seed++;draw();});
 const s=svg(640,330,w);const r=readout(w);let seed=21;
 function draw(){const rr=rng(seed);clear(s);const N=20,R=150,cx=320,cy=165,pts=[];for(let i=0;i<N;i++){const a=2*Math.PI*i/N-Math.PI/2;pts.push([cx+R*Math.cos(a),cy+R*Math.sin(a)]);}
  const alpha=cb.checked?.05/190:.05;let sig=0;
  for(let i=0;i<N;i++)for(let j=i+1;j<N;j++){const p=rr();if(p<alpha){sig++;el('line',{x1:pts[i][0],y1:pts[i][1],x2:pts[j][0],y2:pts[j][1],stroke:'#ef4444','stroke-width':2},s);}}
  pts.forEach((p,i)=>{el('circle',{cx:p[0],cy:p[1],r:10,fill:'#6366f1'},s);el('text',{x:p[0],y:p[1]+4,'text-anchor':'middle','font-size':9,fill:'#fff',style:'fill:#fff'},s,i+1);});
  r.textContent='"Significant" edges found this run: '+sig+' (red lines), even though the true edges are zero—all are false positives!\nExpected number: 190 × '+(cb.checked?'0.05 / 190 = 0.05':'0.05 = 9.5')+' edges. '+(cb.checked?'With correction, false positives are virtually eliminated, but at the cost of statistical power (real small effects become much harder to detect).':'This illustrates the multiple testing problem. Network analysis relies on regularization (Modules 3 and 6) rather than edge-by-edge significance testing.');}
 cb.addEventListener('change',draw);draw();
};
// ---------- 3.1 Regression Fitting ----------
W.regfit=function(w){title(w,'Fit the Regression Line by Hand: Minimize the Sum of Squared Errors (SSE)');
 const rr=rng(8),x=[],y=[];for(let i=0;i<25;i++){const a=1+rr()*8;x.push(a);y.push(Math.max(1,Math.min(25,18-1.1*a+randn(rr)*2.6)));}
 const [B0,B1]=ols(x,y);const SSE=(b0,b1)=>x.reduce((s,xi,i)=>s+(y[i]-b0-b1*xi)**2,0);
 const c=ctrl(w);const s0=slider(c,'Intercept b₀',0,30,.1,12,v=>v.toFixed(1));const s1=slider(c,'Slope b₁',-3,1,.01,0,v=>v.toFixed(2));
 const sq=h('label');const cb=h('input',{type:'checkbox'});sq.append(cb,' Show squared residuals');c.appendChild(sq);btn(c,'Show OLS Solution',()=>{s0.value=B0;s1.value=B1;s0.dispatchEvent(new Event('input'));s1.dispatchEvent(new Event('input'));});
 const s=svg(640,330,w);const s2=svg(640,170,w);const r=readout(w);
 function draw(){const b0=+s0.value,b1=+s1.value;clear(s);const X=sc(0,10,60,620),Y=sc(0,25,300,15);axes(s,X,Y,'Social support (0–10)','Depression score',{xt:[0,2,4,6,8,10],yt:[0,5,10,15,20,25]});
  x.forEach((xi,i)=>{const yh=b0+b1*xi,e=y[i]-yh;if(cb.checked){const sz=Math.abs(Y(yh)-Y(y[i]));el('rect',{x:X(xi),y:Math.min(Y(yh),Y(y[i])),width:sz,height:sz,fill:'#f59e0b','fill-opacity':.18,stroke:'#f59e0b','stroke-opacity':.4},s);}
   el('line',{x1:X(xi),x2:X(xi),y1:Y(y[i]),y2:Y(yh),stroke:e>0?'#10b981':'#ef4444','stroke-width':1.5},s);el('circle',{cx:X(xi),cy:Y(y[i]),r:4,fill:'#6366f1'},s);});
  el('line',{x1:X(0),y1:Y(b0),x2:X(10),y2:Y(b0+10*b1),stroke:'#0f172a','stroke-width':2.5,style:'stroke:'+cssv('--ink')},s);
  clear(s2);const XB=sc(-3,1,60,620);const vals=[];for(let b=-3;b<=1.001;b+=.02)vals.push([b,SSE(mean(y)-b*mean(x),b)]);const mx=Math.max(...vals.map(v=>v[1]));const YB=sc(0,mx,150,10);
  axes(s2,XB,YB,'Slope b₁ (intercept fixed at optimal given slope)','SSE',{xt:[-3,-2,-1,0,1]});el('path',{d:vals.map((v,i)=>(i?'L':'M')+XB(v[0])+','+YB(v[1])).join(''),fill:'none',stroke:'#0ea5e9','stroke-width':2},s2);
  el('circle',{cx:XB(b1),cy:YB(SSE(mean(y)-b1*mean(x),b1)),r:6,fill:'#ef4444'},s2);el('line',{x1:XB(B1),x2:XB(B1),y1:10,y2:150,stroke:'#10b981','stroke-dasharray':'4 3'},s2);
  const e=SSE(b0,b1),best=SSE(B0,B1);r.textContent='Your line: ŷ = '+b0.toFixed(1)+' + ('+b1.toFixed(2)+')·x      Sum of squared errors SSE = '+e.toFixed(1)+'\nOLS line: ŷ = '+B0.toFixed(2)+' + ('+B1.toFixed(2)+')·x   SSE = '+best.toFixed(1)+(e-best<.5?'  You found the optimal solution!':'  ('+(e-best).toFixed(1)+' above minimum)')+'\nLower plot: SSE as a function of slope forms a "bowl-shaped" convex curve. At the minimum (green dashed line), the tangent is horizontal—derivative = 0.';}
 [s0,s1].forEach(q=>q.addEventListener('input',draw));cb.addEventListener('change',draw);draw();
};
// ---------- 3.2 Control Variables ----------
W.partial=function(w){title(w,'Why Do Coefficients Change After "Controlling" for Other Variables?');
 const c=ctrl(w);const b1=slider(c,'True unique effect of loneliness on depression',0,.6,.05,.2,v=>v.toFixed(2));const b2=slider(c,'Effect of sleep problems on depression',0,.6,.05,.4,v=>v.toFixed(2));const rh=slider(c,'Correlation between loneliness and sleep ρ',-.2,.9,.05,.5,v=>v.toFixed(2));
 const s=svg(640,220,w);const r=readout(w);
 function draw(){const B1=+b1.value,B2=+b2.value,R=+rh.value,simple=B1+B2*R;clear(s);const X=sc(0,1,200,600);
  [['Loneliness only',simple,'#f59e0b',50],['Loneliness + sleep',B1,'#10b981',120]].forEach(([t,v,col,y])=>{el('text',{x:190,y:y+22,'text-anchor':'end','font-size':12},s,t);el('rect',{x:X(0),y:y,width:Math.max(0,X(Math.min(1,v))-X(0)),height:34,fill:col,rx:6},s);el('text',{x:X(Math.min(1,v))+6,y:y+22,'font-size':13},s,f2(v));});
  el('text',{x:200,y:200,'font-size':11,fill:cssv('--muted')},s,'(Variables are standardized; values show expected regression coefficients without sampling error)');
  r.textContent='Simple regression coefficient = Unique effect + Sleep effect × Correlation = '+f2(B1)+' + '+f2(B2)+' × '+f2(R)+' = '+f2(simple)+'\nMultiple regression assigns the shared variance between loneliness and sleep to the sleep variable, crediting loneliness only for its unique contribution = '+f2(B1)+'.\nThe difference of '+f2(simple-B1)+' represents the partialled-out / confounded overlap. Larger ρ and stronger sleep effects lead to larger differences.';}
 [b1,b2,rh].forEach(q=>q.addEventListener('input',draw));draw();
};
// ---------- 3.3 Standardized Coefficients ----------
W.stdcoef=function(w){title(w,'Changing Units: Raw b Changes, Standardized β Remains Identical');
 const c=ctrl(w);let unit=1;const us=[['$1',1],['$1,000',1000],['$10,000',10000]].map(([t,k])=>btn(c,'Income unit: '+t,()=>{unit=k;us.forEach(b=>b.classList.toggle('on',b.textContent.endsWith(t)));draw();}));us[0].classList.add('on');
 const r=readout(w);
 function draw(){const bYuan=-0.0006,SDx=3000,SDy=4.5;const b=bYuan*unit,sdx=SDx/unit,beta=b*sdx/SDy;
  const unitName = unit===1 ? '$1' : unit===1000 ? '$1,000' : '$10,000';
  r.textContent='Model: Depression = b₀ + b × Monthly Income\nIncome unit = '+unitName+': Unstandardized b = '+(Math.abs(b)<.01?b.toFixed(4):b.toFixed(2))+' (For each '+unitName+' increase in income, depression changes by '+(Math.abs(b)<.01?b.toFixed(4):b.toFixed(2))+' points)\nSD of income = '+(sdx<1?sdx.toFixed(2):sdx)+', SD of depression = '+SDy+'\nStandardized β = b × SDx / SDy = '+beta.toFixed(2)+' (For each 1 SD higher income, depression is '+Math.abs(beta).toFixed(2)+' SD lower on average)—invariant to the choice of measurement unit. (Fictional illustration)';}
 draw();
};
// ---------- 3.4 Logistic Regression ----------
W.logit=function(w){title(w,'Sigmoid Curve: Mapping Any Real Number to a Probability Between 0 and 1');
 const c=ctrl(w);const s0=slider(c,'b₀',-6,4,.1,-3,v=>v.toFixed(1));const s1=slider(c,'b₁',-1.5,1.5,.05,.6,v=>v.toFixed(2));const xs=slider(c,'Loneliness x',0,10,.5,5);
 const s=svg(640,300,w);const r=readout(w);const rr=rng(4),pts=[];for(let i=0;i<60;i++){const x=rr()*10,p=1/(1+Math.exp(-(-3+.6*x)));pts.push([x,rr()<p?1:0]);}
 function draw(){const b0=+s0.value,b1=+s1.value,x0=+xs.value;clear(s);const X=sc(0,10,60,620),Y=sc(-.25,1.25,270,15);axes(s,X,Y,'Loneliness (0–10)','Sought Professional Help / Probability',{xt:[0,2,4,6,8,10],yt:[0,.5,1]});
  [0,1].forEach(v=>el('line',{x1:X(0),x2:X(10),y1:Y(v),y2:Y(v),stroke:cssv('--line'),'stroke-dasharray':'3 3'},s));
  const [l0,l1]=ols(pts.map(p=>p[0]),pts.map(p=>p[1]));el('line',{x1:X(0),y1:Y(l0),x2:X(10),y2:Y(l0+10*l1),stroke:'#f59e0b','stroke-width':2,'stroke-dasharray':'6 4'},s);
  pts.forEach(p=>el('circle',{cx:X(p[0]),cy:Y(p[1]+(rr()-.5)*.04),r:3.5,fill:'#6366f1','fill-opacity':.6},s));
  let d='';for(let x=0;x<=10;x+=.1)d+=(d?'L':'M')+X(x)+','+Y(1/(1+Math.exp(-(b0+b1*x))));el('path',{d:d,fill:'none',stroke:'#ec4899','stroke-width':3},s);
  const lo=b0+b1*x0,p=1/(1+Math.exp(-lo)),od=p/(1-p);el('circle',{cx:X(x0),cy:Y(p),r:6,fill:'#ec4899'},s);
  el('text',{x:X(.2),y:Y(1.17),'font-size':11,fill:'#b45309'},s,'Orange dashed line = Ordinary linear regression: predicts values outside [0, 1]');
  r.textContent='x = '+x0+': log-odds = b₀ + b₁x = '+f2(lo)+' → odds = e^'+f2(lo)+' = '+f3(od)+' → probability p = odds / (1 + odds) = '+f3(p)+'\nOdds ratio OR = e^b₁ = '+f3(Math.exp(b1))+': Each 1-point increase in loneliness multiplies the odds of seeking help by '+f3(Math.exp(b1))+' (multiplies odds, NOT probability!)';}
 [s0,s1,xs].forEach(q=>q.addEventListener('input',draw));draw();
};
// ---------- 3.5 Overfitting ----------
W.overfit=function(w){title(w,'Overfitting: More Complex Models Reduce Training Error, but What About Test Error?');
 const c=ctrl(w);const dg=slider(c,'Polynomial degree (Model complexity)',1,10,1,1);btn(c,'Generate New Dataset',()=>{seed++;gen();draw();});
 const s=svg(640,300,w);const r=readout(w);let seed=2,tr=[],te=[];const f=x=>Math.sin(2.2*x)*.8+.3*x;
 function gen(){const rr=rng(seed);tr=[];te=[];for(let i=0;i<12;i++){const x=-1+2*i/11+(rr()-.5)*.08;tr.push([x,f(x)+randn(rr)*.3]);}for(let i=0;i<40;i++){const x=-1+2*rr();te.push([x,f(x)+randn(rr)*.3]);}}
 function fit(d){const n=d+1,A=[],b=[];for(let i=0;i<n;i++){A.push(new Array(n).fill(0));b.push(0);}tr.forEach(([x,y])=>{const p=[];for(let k=0;k<n;k++)p.push(x**k);for(let i=0;i<n;i++){b[i]+=p[i]*y;for(let j=0;j<n;j++)A[i][j]+=p[i]*p[j];}});
  for(let i=0;i<n;i++)A[i][i]+=1e-9;for(let i=0;i<n;i++){let mx=i;for(let k=i+1;k<n;k++)if(Math.abs(A[k][i])>Math.abs(A[mx][i]))mx=k;[A[i],A[mx]]=[A[mx],A[i]];[b[i],b[mx]]=[b[mx],b[i]];for(let k=i+1;k<n;k++){const t=A[k][i]/A[i][i];for(let j=i;j<n;j++)A[k][j]-=t*A[i][j];b[k]-=t*b[i];}}
  const c2=new Array(n).fill(0);for(let i=n-1;i>=0;i--){let s3=b[i];for(let j=i+1;j<n;j++)s3-=A[i][j]*c2[j];c2[i]=s3/A[i][i];}return x=>c2.reduce((s3,ci,k)=>s3+ci*x**k,0);}
 function draw(){const d=+dg.value,p=fit(d);clear(s);const X=sc(-1.05,1.05,50,620),Y=sc(-2,2,280,15);axes(s,X,Y,'x','y',{});
  let path='';for(let x=-1.05;x<=1.05;x+=.005){const yv=Math.max(-2.5,Math.min(2.5,p(x)));path+=(path?'L':'M')+X(x)+','+Y(yv);}
  te.forEach(([x,y])=>el('circle',{cx:X(x),cy:Y(y),r:3,fill:'none',stroke:'#94a3b8'},s));tr.forEach(([x,y])=>el('circle',{cx:X(x),cy:Y(y),r:5,fill:'#6366f1'},s));
  el('path',{d:path,fill:'none',stroke:'#ec4899','stroke-width':2.5},s);
  const mse=D=>D.reduce((a,[x,y])=>a+(y-p(x))**2,0)/D.length;r.textContent='Degree = '+d+' ('+(d+1)+' coefficients to estimate with only 12 training observations)\nTraining MSE = '+f3(mse(tr))+'   Test MSE (unfilled circles) = '+f3(mse(te))+'\n'+(d>=7?'The curve oscillates wildly to pass through every training point: it has "memorized the noise." This is overfitting.':d<=2?'The model is too rigid, likely suffering from "underfitting" (high bias).':'At moderate complexity, test error on new data is typically minimized.');}
 gen();dg.addEventListener('input',draw);draw();
};
// ---------- 3.5 LASSO vs Ridge Regression ----------
W.lassopath=function(w){title(w,'As λ Increases: LASSO Shrinks Coefficients to Exactly 0, Ridge Only Shrinks Towards 0');
 const names=['Loneliness','Sleep','Social Support','Exercise','Age','Income','Noise 1','Noise 2'];const b=[.45,.30,-.25,-.12,.06,-.04,.03,-.02];
 const c=ctrl(w);const ls=slider(c,'λ',0,.5,.005,0,v=>v.toFixed(3));
 const s=svg(640,250,w);const s2=svg(640,220,w);const r=readout(w);
 const las=(bj,l)=>Math.sign(bj)*Math.max(0,Math.abs(bj)-l),rid=(bj,l)=>bj/(1+4*l);
 const cols=['#6366f1','#0ea5e9','#10b981','#f59e0b','#ec4899','#8b5cf6','#94a3b8','#64748b'];
 function draw(){const l=+ls.value;clear(s);const X=sc(-.5,.5,120,620);el('line',{x1:X(0),x2:X(0),y1:10,y2:240,stroke:cssv('--muted')},s);
  names.forEach((nm,i)=>{const y=14+i*28;el('text',{x:110,y:y+14,'text-anchor':'end','font-size':12},s,nm);const L=las(b[i],l),R=rid(b[i],l);
   el('rect',{x:Math.min(X(0),X(R)),y:y,width:Math.abs(X(R)-X(0)),height:9,fill:'#f59e0b','fill-opacity':.8},s);el('rect',{x:Math.min(X(0),X(L)),y:y+11,width:Math.abs(X(L)-X(0)),height:9,fill:'#6366f1'},s);
   if(L===0)el('text',{x:X(0)+4,y:y+20,'font-size':10,fill:'#ef4444'},s,'= 0');});
  el('text',{x:620,y:236,'text-anchor':'end','font-size':11},s,'Orange = Ridge  Purple = LASSO');
  clear(s2);const XL=sc(0,.5,60,620),YL=sc(-.3,.5,195,10);axes(s2,XL,YL,'λ (Penalty strength)','LASSO coefficient',{xt:[0,.1,.2,.3,.4,.5],yt:[-.2,0,.2,.4]});
  b.forEach((bj,i)=>{let d='';for(let q=0;q<=.5;q+=.005)d+=(d?'L':'M')+XL(q)+','+YL(las(bj,q));el('path',{d:d,fill:'none',stroke:cols[i],'stroke-width':2},s2);});
  el('line',{x1:XL(l),x2:XL(l),y1:10,y2:195,stroke:'#ef4444','stroke-dasharray':'4 3'},s2);
  const nz=b.filter(bj=>las(bj,l)!==0).length;r.textContent='λ = '+l.toFixed(3)+': LASSO retains '+nz+' / 8 non-zero coefficients; Ridge still retains 8 / 8 (only shrunken closer to 0).\nSimplified illustration assuming standardized, orthogonal predictors where the LASSO solution is sign(b)·max(0, |b| − λ) and Ridge is b / (1 + cλ). In real correlated data, paths are non-linear, but the principle that larger λ yields sparser solutions remains identical.';}
 ls.addEventListener('input',draw);draw();
};
// ---------- 2.1 RStudio Four Panes ----------
W.panes=function(w){title(w,'The Four RStudio Panes (Click each to explore)');
 const P=[['① Source Editor','Where you write and save .R script files. Press Ctrl+Enter (Mac: Cmd+Enter) to send the current line to the Console. Think of it as your "notebook."'],['③ Environment / History','Lists all active objects you created (such as vectors, data frames) and their values. The broom icon clears the workspace.'],['② Console','Where R actually executes code and prints output or error messages. The > prompt indicates R is waiting for input. Great for quick interactive tests, but commands are not saved to a file.'],['④ Files / Plots / Packages / Help','Browse directories, view generated plots, manage R packages, and read documentation opened with ?function.']];
 const g=h('div',{class:'pane-grid'});w.appendChild(g);const r=readout(w);r.style.whiteSpace='normal';
 P.forEach(([t,d],i)=>{const p=h('div',{class:'pane',tabindex:0},'<b>'+t+'</b><span class="muted">'+(i===0?'Top-Left':i===1?'Top-Right':i===2?'Bottom-Left':'Bottom-Right')+'</span>');p.onclick=()=>{g.querySelectorAll('.pane').forEach(x=>x.classList.remove('on'));p.classList.add('on');r.innerHTML='<b>'+t+'</b>: '+d;};p.onkeydown=e=>{if(e.key==='Enter')p.onclick();};g.appendChild(p);});
 note(w,'Default layout shown above; customizable via Tools → Global Options → Pane Layout.');g.firstChild.onclick();
};
// ---------- 2.2 Vector Indexing ----------
W.vecidx=function(w){title(w,'Vector Indexing Lab: Click an expression to see which elements are selected');
 const v=[7,5.5,8,NaN,6,4.5,7.5,NaN,9,5];const disp=x=>isNaN(x)?'NA':String(x);
 const ex=[['sleep[2]',()=>[1],'Extract 2nd element (R is 1-indexed)'],['sleep[c(1, 3)]',()=>[0,2],'Extract 1st and 3rd elements'],['sleep[2:4]',()=>[1,2,3],'2:4 is equivalent to c(2, 3, 4)'],['sleep[-1]',()=>v.map((_,i)=>i).filter(i=>i!==0),'Negative index = drop the 1st element'],['sleep > 6',null,'Element-wise comparison returning a logical vector'],['sleep[sleep < 6]',()=>'lt6','Logical subsetting: comparisons with NA evaluate to NA'],['sleep[!is.na(sleep) & sleep < 6]',()=>v.map((x,i)=>i).filter(i=>!isNaN(v[i])&&v[i]<6),'Filter out NA before comparing'],['is.na(sleep)',null,'Identify missing values'],['mean(sleep)',null,'Returns NA when missing values are present'],['mean(sleep, na.rm = TRUE)',null,'Compute mean after removing NA']];
 const tb=h('div',{style:'display:flex;gap:4px;flex-wrap:wrap;margin:6px 0'});w.appendChild(tb);
 const cells=v.map((x,i)=>{const d=h('div',{style:'border:1px solid var(--line);border-radius:6px;padding:4px 8px;text-align:center;min-width:46px;background:var(--card);font-family:var(--mono);font-size:.85rem'},'<small class="muted">['+(i+1)+']</small><br>'+disp(x));tb.appendChild(d);return d;});
 const c=ctrl(w);const r=readout(w);
 ex.forEach(([e,f,expl])=>btn(c,e,()=>{cells.forEach(x=>x.classList.remove('cellsel','hl'));let out='';
  if(e==='sleep > 6'){out=v.map(x=>isNaN(x)?'NA':x>6?'TRUE':'FALSE').join(' ');v.forEach((x,i)=>{if(x>6)cells[i].classList.add('cellsel');});}
  else if(e==='is.na(sleep)'){out=v.map(x=>isNaN(x)?'TRUE':'FALSE').join(' ');v.forEach((x,i)=>{if(isNaN(x))cells[i].classList.add('hl');});}
  else if(e==='mean(sleep)'){out='NA';v.forEach((x,i)=>{if(isNaN(x))cells[i].classList.add('hl');});}
  else if(e==='mean(sleep, na.rm = TRUE)'){const o=v.filter(x=>!isNaN(x));out=String(+mean(o).toFixed(4));v.forEach((x,i)=>{if(!isNaN(x))cells[i].classList.add('cellsel');});}
  else{const idx=f();if(idx==='lt6'){const o=[];v.forEach((x,i)=>{if(isNaN(x)){o.push('NA');cells[i].classList.add('hl');}else if(x<6){o.push(disp(x));cells[i].classList.add('cellsel');}});out=o.join(' ');}
   else{idx.forEach(i=>cells[i].classList.add('cellsel'));out=idx.map(i=>disp(v[i])).join(' ');}}
  r.textContent='> '+e+'\n[1] '+out+'\n# '+expl+' (Green = selected, Yellow = NA)';}));
 r.textContent='> sleep <- c(7, 5.5, 8, NA, 6, 4.5, 7.5, NA, 9, 5)\n# Click the buttons above to test expressions';
};
// ---------- 2.3 dplyr Verbs ----------
W.dplyr=function(w){title(w,'dplyr Verbs Interactive Lab');
 const D=[{id:1,gender:'Female',phq1:2,phq2:1,lone:3},{id:2,gender:'Male',phq1:0,phq2:1,lone:2},{id:3,gender:'Female',phq1:3,phq2:3,lone:4},{id:4,gender:'Male',phq1:1,phq2:0,lone:1},{id:5,gender:'Female',phq1:1,phq2:2,lone:2}];
 const ops=[['Raw data dat','dat',d=>d],['select(id, phq1, phq2)','dat |> select(id, phq1, phq2)',d=>d.map(o=>({id:o.id,phq1:o.phq1,phq2:o.phq2}))],['filter(gender == "Female")','dat |> filter(gender == "Female")',d=>d.filter(o=>o.gender==='Female')],['mutate(phq_sum = phq1 + phq2)','dat |> mutate(phq_sum = phq1 + phq2)',d=>d.map(o=>Object.assign({},o,{phq_sum:o.phq1+o.phq2}))],['arrange(desc(lone))','dat |> arrange(desc(lone))',d=>[...d].sort((a,b)=>b.lone-a.lone)],['group_by + summarise','dat |>\n  group_by(gender) |>\n  summarise(n = n(), lone_mean = mean(lone))',d=>['Female','Male'].map(g=>{const s=d.filter(o=>o.gender===g);return{gender:g,n:s.length,lone_mean:+mean(s.map(o=>o.lone)).toFixed(2)};}).sort((a,b)=>a.gender<b.gender?-1:1)],['Pipeline (Piping)','dat |>\n  filter(gender == "Female") |>\n  mutate(phq_sum = phq1 + phq2) |>\n  select(id, phq_sum)',d=>d.filter(o=>o.gender==='Female').map(o=>({id:o.id,phq_sum:o.phq1+o.phq2}))]];
 const c=ctrl(w);const code=h('pre');const cd=h('code',{class:'language-r'});code.appendChild(cd);const tw=h('div',{class:'tablewrap'});w.append(code,tw);
 ops.forEach(([t,src,f],i)=>{const b=btn(c,t,()=>{c.querySelectorAll('button').forEach(x=>x.classList.remove('on'));b.classList.add('on');cd.innerHTML=window.CLPNCore?CLPNCore.hlR(src):src;const o=f(D);const ks=Object.keys(o[0]);
  tw.innerHTML='<table><thead><tr>'+ks.map(k=>'<th>'+k+'</th>').join('')+'</tr></thead><tbody>'+o.map(r=>'<tr>'+ks.map(k=>'<td>'+r[k]+'</td>').join('')+'</tr>').join('')+'</tbody></table><p class="wnote">'+o.length+' rows × '+ks.length+' columns</p>';});if(i===0)b.click();});
 note(w,'Note: In summarise(), group ordering follows alphabetical sorting by default; shown here for demonstration.');
};
// ---------- 2.6 ggplot Layers ----------
W.ggbuild=function(w){title(w,'ggplot2 Builds Graphs Layer by Layer');
 const L=[['ggplot(dat, aes(x = lone, y = dep))','Data + Mapping: creates coordinate system, no points yet'],['+ geom_point(alpha = 0.6)','Geometric object: plot data points'],['+ geom_smooth(method = "lm")','Additional layer: linear regression fit (with 95% CI band)'],['+ labs(x = "Loneliness", y = "Depression")','Labels: descriptive axis titles'],['+ theme_minimal()','Theme: cleaner white background']];
 const c=h('div');w.appendChild(c);const on=[true,false,false,false,false];
 L.forEach(([t,d],i)=>{const l=h('label',{style:'display:block;font-family:var(--mono);font-size:.84rem'});const cb=h('input',{type:'checkbox'});cb.checked=on[i];cb.disabled=i===0;cb.onchange=()=>{on[i]=cb.checked;draw();};l.append(cb,' '+t+'  ',h('span',{class:'muted'},'# '+d));c.appendChild(l);});
 const s=svg(640,330,w);const rr=rng(17),x=[],y=[];for(let i=0;i<80;i++){const a=1+rr()*9;x.push(a);y.push(Math.max(0,Math.min(27,2+1.2*a+randn(rr)*3.5)));}const [b0,b1]=ols(x,y);
 function draw(){clear(s);const X=sc(0,10.5,70,620),Y=sc(0,27,290,15);if(!on[4])el('rect',{x:70,y:15,width:550,height:275,fill:'#ebebeb'},s);
  [0,2,4,6,8,10].forEach(v=>el('line',{x1:X(v),x2:X(v),y1:15,y2:290,stroke:on[4]?'#e5e7eb':'#fff'},s));[0,5,10,15,20,25].forEach(v=>el('line',{x1:70,x2:620,y1:Y(v),y2:Y(v),stroke:on[4]?'#e5e7eb':'#fff'},s));
  axes(s,X,Y,on[3]?'Loneliness':'lone',on[3]?'Depression':'dep',{xt:[0,2,4,6,8,10],yt:[0,5,10,15,20,25]});
  if(on[1])x.forEach((v,i)=>el('circle',{cx:X(v),cy:Y(y[i]),r:3.5,fill:'#111','fill-opacity':.6,style:'fill:'+cssv('--ink')},s));
  if(on[2]){const n=x.length,mx=mean(x),sxx=x.reduce((a,v)=>a+(v-mx)**2,0),s2=Math.sqrt(x.reduce((a,v,i)=>a+(y[i]-b0-b1*v)**2,0)/(n-2));let up='',dn='';for(let v=1;v<=10;v+=.25){const se=s2*Math.sqrt(1/n+(v-mx)**2/sxx),f=b0+b1*v;up+=(up?'L':'M')+X(v)+','+Y(f+1.99*se);dn='L'+X(v)+','+Y(f-1.99*se)+dn;}
   el('path',{d:up+dn.replace(/^L/,'L')+'Z',fill:'#94a3b8','fill-opacity':.4},s);el('line',{x1:X(1),y1:Y(b0+b1),x2:X(10),y2:Y(b0+10*b1),stroke:'#3366FF','stroke-width':2.5},s);}}
 draw();
};
// ---------- 4.1 Between-Person vs. Within-Person ----------
W.betweenwithin=function(w){title(w,'"Lonely people are more depressed" ≠ "When a person feels lonelier than usual, they become more depressed"');
 const c=ctrl(w);const cb1=h('label');const ch=h('input',{type:'checkbox'});cb1.append(ch,' Center around each person\'s own mean (within-person perspective)');c.appendChild(cb1);const wb=slider(c,'Within-person slope (true parameter)',-1,1,.1,-.5,v=>v.toFixed(1));
 const s=svg(640,330,w);const r=readout(w);const cols=['#6366f1','#0ea5e9','#10b981','#f59e0b','#ec4899'];const rr=rng(31);const P=[];for(let k=0;k<5;k++){const mx=2+k*1.5,my=3+k*1.4,o=[];for(let t=0;t<6;t++){const e=randn(rr)*.6;o.push([e,randn(rr)*.25]);}P.push({mx,my,o});}
 function draw(){const b=+wb.value,cen=ch.checked;clear(s);const X=cen?sc(-2,2,60,620):sc(0,10,60,620),Y=cen?sc(-2,2,300,15):sc(0,11,300,15);
  axes(s,X,Y,cen?'Loneliness (Deviation from person mean)':'Loneliness','Depression'+(cen?' (Deviation from person mean)':''),{xt:cen?[-2,-1,0,1,2]:[0,2,4,6,8,10],yt:cen?[-2,0,2]:[0,5,10]});
  const allx=[],ally=[],wx=[],wy=[];
  P.forEach((p,k)=>{const pts=p.o.map(([e,u])=>[p.mx+e,p.my+b*e+u]);const px=mean(pts.map(q=>q[0])),py=mean(pts.map(q=>q[1]));
   pts.forEach(q=>{const xx=cen?q[0]-px:q[0],yy=cen?q[1]-py:q[1];allx.push(q[0]);ally.push(q[1]);wx.push(q[0]-px);wy.push(q[1]-py);el('circle',{cx:X(xx),cy:Y(yy),r:5,fill:cols[k],'fill-opacity':.75},s);});
   if(!cen){el('circle',{cx:X(px),cy:Y(py),r:9,fill:'none',stroke:cols[k],'stroke-width':2},s);}});
  if(!cen){const pm=P.map(p=>[p.mx,p.my]);const [a0,a1]=ols(pm.map(q=>q[0]),pm.map(q=>q[1]));el('line',{x1:X(1),y1:Y(a0+a1),x2:X(9),y2:Y(a0+9*a1),stroke:cssv('--ink'),'stroke-width':2,'stroke-dasharray':'6 4'},s);}
  else{const [c0,c1]=ols(wx,wy);el('line',{x1:X(-2),y1:Y(c0-2*c1),x2:X(2),y2:Y(c0+2*c1),stroke:cssv('--ink'),'stroke-width':2},s);}
  r.textContent='5 individuals (distinct colors), each measured across 6 time points.\nBetween-person: The dashed line connecting individual means (hollow circles) has a positive slope—"People who are lonelier on average are also more depressed on average."\nWithin-person: After subtracting each person\'s own mean, the slope = '+f2(ols(wx,wy)[1])+' (set parameter: '+b.toFixed(1)+').\nPooled cross-sectional correlation r = '+f2(cor(allx,ally))+'—which reflects neither pure between-person nor pure within-person relationships.';}
 ch.addEventListener('change',draw);wb.addEventListener('input',draw);draw();
};
// ---------- 4.1 Measurement Interval (Illustration) ----------
W.lag=function(w){title(w,'Different Time Lags Yield Different Apparent Cross-Lagged Effects (Illustration)');
 const c=ctrl(w);const lg=slider(c,'Lag between measurements (weeks)',1,52,1,4);const s=svg(640,240,w);const r=readout(w);
 const eff=t=>{const a=Math.exp(-t/6),b=Math.exp(-t/3);return 1.4*(a-b);};
 function draw(){const t=+lg.value;clear(s);const X=sc(0,52,60,620),Y=sc(0,.4,210,15);axes(s,X,Y,'Measurement interval (weeks)','Cross-lagged effect',{xt:[0,4,12,26,52],yt:[0,.2,.4]});
  let d='';for(let q=0;q<=52;q+=.5)d+=(d?'L':'M')+X(q)+','+Y(eff(q));el('path',{d:d,fill:'none',stroke:'#ec4899','stroke-width':2.5},s);el('circle',{cx:X(t),cy:Y(eff(t)),r:6,fill:'#ec4899'},s);
  r.textContent='At a lag of '+t+' weeks, the detectable effect in the model ≈ '+f3(eff(t))+'\nThis curve represents a hypothetical "Loneliness → Depression" process: effects take several weeks to materialize, then gradually decay. If the interval is too short, the effect has not yet peaked; if too long, it has already dissipated.\nConceptual curve, not an empirical estimate; the true underlying temporal dynamics are often unknown—a key limitation to address in research manuscripts.';}
 lg.addEventListener('input',draw);draw();
};
// ---------- 4.2 Wide vs. Long Format ----------
W.reshape=function(w){title(w,'Wide Format ⇄ Long Format');
 const wide=[{id:1,lone_t1:3,lone_t2:2,dep_t1:5,dep_t2:4},{id:2,lone_t1:1,lone_t2:2,dep_t1:2,dep_t2:3},{id:3,lone_t1:4,lone_t2:4,dep_t1:7,dep_t2:6}];
 const long=[];wide.forEach(o=>['1','2'].forEach(t=>long.push({id:o.id,wave:t,lone:o['lone_t'+t],dep:o['dep_t'+t]})));
 let mode='wide',sel=2;const c=ctrl(w);const bw=btn(c,'Wide Format (One row per person)',()=>{mode='wide';draw();});const bl=btn(c,'Long Format (One row per person-wave)',()=>{mode='long';draw();});
 const ps=slider(c,'Highlight Case ID',1,3,1,2);ps.addEventListener('input',()=>{sel=+ps.value;draw();});const tw=h('div',{class:'tablewrap'});w.appendChild(tw);const r=readout(w);
 function tab(rows){const ks=Object.keys(rows[0]);return '<table><thead><tr>'+ks.map(k=>'<th>'+k+'</th>').join('')+'</tr></thead><tbody>'+rows.map(o=>'<tr class="'+(o.id===sel?'hl':'')+'">'+ks.map(k=>'<td>'+o[k]+'</td>').join('')+'</tr>').join('')+'</tbody></table>';}
 function draw(){bw.classList.toggle('on',mode==='wide');bl.classList.toggle('on',mode==='long');tw.innerHTML=tab(mode==='wide'?wide:long);
  r.textContent=mode==='wide'?'3 rows × 5 columns. All time points for Case '+sel+' are stored in a single row. Both lavaan (CLPM) and CLPN T1/T2 regression matrices rely on wide data.':'6 rows × 4 columns. Case '+sel+' spans two rows, with the "wave" column tracking measurement occasions. Commonly required for multilevel models and ggplot2 trajectory plotting.\npivot_longer(-id, names_to = c(".value", "wave"), names_sep = "_t")';}
 draw();
};
// ---------- 4.3 Missingness Mechanisms ----------
W.missing=function(w){title(w,'Missingness Mechanism Simulation: Who Drops Out of the Study?');
 const N=4000,rr=rng(77),t1=[],t2=[];for(let i=0;i<N;i++){const a=randn(rr),b=.6*a+.8*randn(rr);t1.push(10+4*a);t2.push(10+4*b);}const U=[];for(let i=0;i<N;i++)U.push(rr());
 let mech='MCAR';const c=ctrl(w);const bs=['MCAR','MAR','MNAR'].map(m=>btn(c,m,()=>{mech=m;bs.forEach(b=>b.classList.toggle('on',b.textContent===m));draw();}));bs[0].classList.add('on');const rs=slider(c,'Attrition Rate',.05,.6,.05,.3,v=>Math.round(v*100)+'%');
 const s=svg(640,200,w);const r=readout(w);
 function draw(){const rate=+rs.value;const z1=t1.map(v=>(v-10)/4),z2=t2.map(v=>(v-10)/4);
  const sc2=mech==='MCAR'?t1.map(()=>0):mech==='MAR'?z1.map(v=>1.5*v):z2.map(v=>1.5*v);
  const sig=x=>1/(1+Math.exp(-x));let lo=-10,hi=10;for(let k=0;k<50;k++){const m=(lo+hi)/2;const pr=mean(sc2.map(v=>sig(v+m)));if(pr>rate)hi=m;else lo=m;}
  const miss=sc2.map((v,i)=>U[i]<sig(v+lo));const obs1=[],obs2=[];t1.forEach((v,i)=>{if(!miss[i]){obs1.push(v);obs2.push(t2[i]);}});
  const [a0,a1]=ols(obs1,obs2);const imp=mean(t1.map(v=>a0+a1*v));const tm=mean(t2),cc=mean(obs2);
  clear(s);const X=sc(8,12.5,170,610);[['True T2 mean (All)',tm,'#10b981',20],['Completers (Listwise)',cc,'#ef4444',75],['Imputed using T1',imp,'#6366f1',130]].forEach(([t,v,col,y])=>{el('text',{x:162,y:y+20,'text-anchor':'end','font-size':12},s,t);el('rect',{x:X(8),y:y,width:Math.max(0,X(v)-X(8)),height:30,fill:col,rx:5},s);el('text',{x:X(v)+5,y:y+20,'font-size':12},s,f2(v));});
  r.textContent='Mechanism = '+mech+': '+(mech==='MCAR'?'Dropout is completely independent of all study variables (like flipping a coin).':mech==='MAR'?'Higher T1 depression increases dropout risk—missingness depends entirely on observed T1 values.':'Higher T2 depression itself increases dropout risk—missingness depends on unobserved values.')+'\nActual attrition: '+(100*miss.filter(Boolean).length/N).toFixed(1)+'%. T1–T2 correlation: Full sample r = '+f2(cor(t1,t2))+', Completers r = '+f2(cor(obs1,obs2))+'\n'+(mech==='MCAR'?'Listwise deletion is largely unbiased (only statistical power is reduced).':mech==='MAR'?'Listwise deletion underestimates the T2 mean; utilizing T1 information (as in FIML or multiple imputation) successfully corrects the bias.':'Both approaches underestimate the true mean—MNAR cannot be corrected by observed data alone and requires sensitivity analyses.');}
 rs.addEventListener('input',draw);draw();
};

let uid=0;
window.CLPNViz={initAll:function(){document.querySelectorAll('.widget[data-widget]').forEach(wd=>{const f=W[wd.dataset.widget];wd._id=++uid;if(f){try{f(wd);}catch(e){console.error('widget '+wd.dataset.widget,e);throw e;}}else console.error('unknown widget '+wd.dataset.widget);});
 document.addEventListener('themechange',()=>{});},W:W};
})();

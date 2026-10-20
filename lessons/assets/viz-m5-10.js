/* CLPN 课程 · M5–M10 交互组件库（与 viz.js 并列；页面外壳、测验、复制、公式由 lesson.js 统一处理） */
(function(){
"use strict";
const $=(s,r=document)=>r.querySelector(s), $$=(s,r=document)=>[...r.querySelectorAll(s)];
const NS="http://www.w3.org/2000/svg";
function el(tag,attrs,parent,text){const e=document.createElementNS(NS,tag);for(const k in attrs)e.setAttribute(k,attrs[k]);if(text!=null)e.textContent=text;if(parent)parent.appendChild(e);return e;}
function h(tag,attrs,html){const e=document.createElement(tag);if(attrs)for(const k in attrs)e.setAttribute(k,attrs[k]);if(html!=null)e.innerHTML=html;return e;}
const fmt=(x,d=2)=>(Math.abs(x)<1e-12?0:x).toFixed(d);
const css=v=>getComputedStyle(document.documentElement).getPropertyValue(v).trim()||"#888";
/* ---------- 随机数（可复现） ---------- */
function rng(seed){let a=seed>>>0;const u=()=>{a|=0;a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296;};
 let spare=null;u.norm=()=>{if(spare!==null){const s=spare;spare=null;return s;}let x,y,r;do{x=2*u()-1;y=2*u()-1;r=x*x+y*y;}while(!r||r>=1);const m=Math.sqrt(-2*Math.log(r)/r);spare=y*m;return x*m;};return u;}
/* ---------- 小型线性代数 ---------- */
function inv(A){const n=A.length,M=A.map((r,i)=>r.concat(A.map((_,j)=>i===j?1:0)));
 for(let c=0;c<n;c++){let p=c;for(let r=c+1;r<n;r++)if(Math.abs(M[r][c])>Math.abs(M[p][c]))p=r;[M[c],M[p]]=[M[p],M[c]];const d=M[c][c];if(Math.abs(d)<1e-12)return null;
  for(let j=0;j<2*n;j++)M[c][j]/=d;for(let r=0;r<n;r++)if(r!==c){const f=M[r][c];for(let j=0;j<2*n;j++)M[r][j]-=f*M[c][j];}}
 return M.map(r=>r.slice(n));}
function pcorFromCor(R){const P=inv(R);if(!P)return null;return P.map((r,i)=>r.map((v,j)=>i===j?0:-v/Math.sqrt(P[i][i]*P[j][j])));}
function corr(x,y){const n=x.length;let mx=0,my=0;for(let i=0;i<n;i++){mx+=x[i];my+=y[i];}mx/=n;my/=n;let sxy=0,sx=0,sy=0;for(let i=0;i<n;i++){const a=x[i]-mx,b=y[i]-my;sxy+=a*b;sx+=a*a;sy+=b*b;}return sxy/Math.sqrt(sx*sy);}
const soft=(z,l)=>Math.sign(z)*Math.max(0,Math.abs(z)-l);
function quant(a,q){const s=[...a].sort((x,y)=>x-y),i=(s.length-1)*q,lo=Math.floor(i),hi=Math.ceil(i);return s[lo]+(s[hi]-s[lo])*(i-lo);}
/* ---------- 通用：网络绘图 ---------- */
function circleLayout(n,cx,cy,r,start=-Math.PI/2){return Array.from({length:n},(_,i)=>({x:cx+r*Math.cos(start+2*Math.PI*i/n),y:cy+r*Math.sin(start+2*Math.PI*i/n)}));}
function ensureDefs(svg){let d=svg.querySelector("defs");if(d)return d;d=el("defs",{},svg);
 [["pos",css("--pos")],["neg",css("--neg")],["gry","#9ca3af"]].forEach(([k,c])=>{const m=el("marker",{id:svg.dataset.uid+"-arr-"+k,viewBox:"0 0 10 10",refX:"9",refY:"5",markerUnits:"userSpaceOnUse",markerWidth:"11",markerHeight:"11",orient:"auto-start-reverse"},d);el("path",{d:"M0,0 L10,5 L0,10 z",fill:c},m);});return d;}
let uidc=0;
function drawNet(svg,{nodes,pos,W,directed=false,maxW=1,threshold=0,showLoops=false,groups=null,colors=["#f59e0b","#14b8a6","#8b5cf6"],R=20,highlight=null,label=null}){
 svg.innerHTML="";if(!svg.dataset.uid)svg.dataset.uid="w"+(++uidc);ensureDefs(svg);const uid=svg.dataset.uid;const n=nodes.length;
 const edges=[];for(let i=0;i<n;i++)for(let j=0;j<n;j++){if(!directed&&j<=i)continue;const w=W[i][j];if(i===j&&!showLoops)continue;if(Math.abs(w)<=threshold||Math.abs(w)<1e-9)continue;edges.push([i,j,w]);}
 edges.sort((a,b)=>Math.abs(a[2])-Math.abs(b[2]));
 for(const [i,j,w] of edges){const col=w>0?css("--pos"):css("--neg");const width=0.8+7*Math.min(1,Math.abs(w)/maxW);
  let op=0.25+0.75*Math.min(1,Math.abs(w)/maxW);if(highlight!=null&&i!==highlight&&j!==highlight)op*=0.15;
  const a=pos[i],b=pos[j];
  if(i===j){const cx=pos[i].x,cy=pos[i].y,ang=Math.atan2(cy-(svg.viewBox.baseVal.height/2),cx-(svg.viewBox.baseVal.width/2));const ox=Math.cos(ang),oy=Math.sin(ang);
   const p1x=cx+R*Math.cos(ang-0.5),p1y=cy+R*Math.sin(ang-0.5),p2x=cx+R*Math.cos(ang+0.5),p2y=cy+R*Math.sin(ang+0.5);
   el("path",{d:`M${p1x},${p1y} C${cx+ox*R*3.2-oy*R*1.6},${cy+oy*R*3.2+ox*R*1.6} ${cx+ox*R*3.2+oy*R*1.6},${cy+oy*R*3.2-ox*R*1.6} ${p2x},${p2y}`,fill:"none",stroke:col,"stroke-width":width,"stroke-opacity":op,"marker-end":`url(#${uid}-arr-${w>0?"pos":"neg"})`},svg);continue;}
  const dx=b.x-a.x,dy=b.y-a.y,L=Math.hypot(dx,dy),ux=dx/L,uy=dy/L;
  let sx=a.x+ux*R,sy=a.y+uy*R,ex=b.x-ux*(R+3),ey=b.y-uy*(R+3);
  if(directed&&Math.abs(W[j][i])>threshold&&Math.abs(W[j][i])>1e-9){const bend=18;const mx=(sx+ex)/2-uy*bend,my=(sy+ey)/2+ux*bend;
   el("path",{d:`M${sx},${sy} Q${mx},${my} ${ex},${ey}`,fill:"none",stroke:col,"stroke-width":width,"stroke-opacity":op,"marker-end":`url(#${uid}-arr-${w>0?"pos":"neg"})`},svg);}
  else{const ln=el("line",{x1:sx,y1:sy,x2:directed?ex:b.x-ux*R,y2:directed?ey:b.y-uy*R,stroke:col,"stroke-width":width,"stroke-opacity":op},svg);if(directed)ln.setAttribute("marker-end",`url(#${uid}-arr-${w>0?"pos":"neg"})`);}
  if(label&&Math.abs(w)>=label){el("text",{x:(a.x+b.x)/2,y:(a.y+b.y)/2-4,"font-size":"10","text-anchor":"middle",opacity:op},svg,fmt(w));}}
 nodes.forEach((nm,i)=>{const g=el("g",{class:"node","data-i":i,style:"cursor:pointer"},svg);const gi=groups?groups[i]:0;
  el("circle",{cx:pos[i].x,cy:pos[i].y,r:R,fill:colors[gi%colors.length],stroke:highlight===i?css("--ink"):"#fff","stroke-width":highlight===i?3:2},g);
  el("text",{x:pos[i].x,y:pos[i].y+4,"text-anchor":"middle","font-size":R>16?"12":"10","font-weight":"700",style:"fill:#fff"},g,nm);});
 return edges;}
function barChart(svg,labels,series,{W=520,H=220,colors=[css("--accent"),"#f59e0b"],names=[]}={}){svg.innerHTML="";svg.setAttribute("viewBox",`0 0 ${W} ${H}`);
 const pad={l:34,r:8,t:18,b:34},n=labels.length,k=series.length;let mx=0,mn=0;series.forEach(s=>s.forEach(v=>{mx=Math.max(mx,v);mn=Math.min(mn,v);}));if(mx===mn)mx=mn+1;
 const y=v=>pad.t+(H-pad.t-pad.b)*(mx-v)/(mx-mn),bw=(W-pad.l-pad.r)/n;
 el("line",{x1:pad.l,x2:W-pad.r,y1:y(0),y2:y(0),stroke:"#9ca3af"},svg);
 [mn,0,mx].forEach(v=>el("text",{x:pad.l-4,y:y(v)+4,"text-anchor":"end","font-size":"10"},svg,fmt(v)));
 labels.forEach((lb,i)=>{series.forEach((s,j)=>{const v=s[i],x=pad.l+i*bw+bw*0.12+j*(bw*0.76/k);el("rect",{x,y:Math.min(y(v),y(0)),width:bw*0.76/k-1,height:Math.abs(y(v)-y(0)),fill:colors[j%colors.length],rx:2},svg);});
  el("text",{x:pad.l+i*bw+bw/2,y:H-pad.b+14,"text-anchor":"middle","font-size":"10"},svg,lb);});
 names.forEach((nm,j)=>{el("rect",{x:pad.l+j*90,y:2,width:10,height:10,fill:colors[j]},svg);el("text",{x:pad.l+14+j*90,y:11,"font-size":"10"},svg,nm);});}
function histogram(svg,vals,{W=520,H=200,bins=30,lo=null,hi=null,marks=[]}={}){svg.innerHTML="";svg.setAttribute("viewBox",`0 0 ${W} ${H}`);
 const a=lo??Math.min(...vals),b=hi??Math.max(...vals),pad={l:10,r:10,t:10,b:28},cnt=new Array(bins).fill(0);
 vals.forEach(v=>{let k=Math.floor((v-a)/(b-a)*bins);k=Math.max(0,Math.min(bins-1,k));cnt[k]++;});const m=Math.max(...cnt,1),bw=(W-pad.l-pad.r)/bins,X=v=>pad.l+(v-a)/(b-a)*(W-pad.l-pad.r);
 cnt.forEach((c,i)=>el("rect",{x:pad.l+i*bw,y:H-pad.b-(H-pad.t-pad.b)*c/m,width:bw-1,height:(H-pad.t-pad.b)*c/m,fill:css("--accent"),opacity:.7},svg));
 el("line",{x1:pad.l,x2:W-pad.r,y1:H-pad.b,y2:H-pad.b,stroke:"#9ca3af"},svg);
 for(let t=0;t<=4;t++){const v=a+(b-a)*t/4;el("text",{x:X(v),y:H-8,"text-anchor":"middle","font-size":"10"},svg,fmt(v));}
 marks.forEach(([v,c,lab])=>{el("line",{x1:X(v),x2:X(v),y1:pad.t,y2:H-pad.b,stroke:c,"stroke-width":2,"stroke-dasharray":"4 3"},svg);if(lab)el("text",{x:X(v)+3,y:pad.t+10,"font-size":"10",style:"fill:"+c},svg,lab);});}
/* ---------- 示意 CLPN（9 节点：孤独 4 + 抑郁 5） ---------- */
const CL_NODES=["lone1", "lone2", "lone3", "lone4", "dep1", "dep2", "dep3", "dep4", "dep5"];
const CL_NAMES=["lone1 缺少陪伴","lone2 被冷落","lone3 与人隔绝","lone4 无人理解","dep1 情绪低落","dep2 兴趣丧失","dep3 睡眠问题","dep4 疲乏","dep5 无价值感"];
const CL_GROUP=[0,0,0,0,1,1,1,1,1];
/* 课程数据 data/true_B_population.csv（CLPN 的总体目标值）与 data/true_B_within.csv（生成模型的被试内 B） */
const B_POP=[[0.39, 0.07, 0.072, 0.062, 0.005, 0.102, 0.015, 0.013, 0.002], [0.068, 0.391, 0.068, 0.142, 0.012, 0.011, 0.019, 0.017, 0.015], [0.071, 0.065, 0.387, 0.063, 0.118, 0.0, 0.004, 0.002, -0.001], [0.061, 0.066, 0.064, 0.378, -0.003, 0.002, 0.005, 0.005, 0.083], [0.004, 0.008, -0.002, 0.002, 0.327, 0.059, 0.058, 0.054, 0.126], [0.009, 0.007, 0.082, 0.001, 0.061, 0.33, 0.061, 0.052, 0.055], [0.013, 0.016, 0.008, 0.011, 0.06, 0.058, 0.328, 0.169, 0.054], [0.01, -0.083, 0.01, 0.012, 0.055, 0.054, 0.059, 0.323, 0.053], [0.005, 0.013, 0.006, 0.009, 0.055, 0.053, 0.056, 0.048, 0.324]];
const B_WITHIN=[[0.35, 0.0, 0.0, 0.0, 0.0, 0.14, 0.0, 0.0, 0.0], [0.0, 0.35, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.35, 0.0, 0.18, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.35, 0.0, 0.0, 0.0, 0.0, 0.12], [0.0, 0.0, 0.0, 0.0, 0.3, 0.0, 0.0, 0.0, 0.1], [0.0, 0.0, 0.12, 0.0, 0.0, 0.3, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.3, 0.16, 0.0], [0.0, -0.15, 0.0, 0.0, 0.0, 0.0, 0.0, 0.3, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.3]];
function demoB(which){return (which==="within"?B_WITHIN:B_POP).map(r=>r.slice());}
/* ---------- 辅助：滑块 ---------- */
function slider(parent,label,min,max,step,val,onInput){const lab=h("label",{},`${label} `);const inp=h("input",{type:"range",min,max,step,value:val});const out=h("b",{},String(val));lab.appendChild(inp);lab.appendChild(out);
 inp.addEventListener("input",()=>{out.textContent=inp.value;onInput&&onInput(+inp.value);});parent.appendChild(lab);return inp;}
function check(parent,label,val,onChange){const lab=h("label",{});const inp=h("input",{type:"checkbox"});inp.checked=val;lab.appendChild(inp);lab.appendChild(document.createTextNode(label));inp.addEventListener("change",()=>onChange&&onChange(inp.checked));parent.appendChild(lab);return inp;}
function frame(w,title){w.innerHTML="";w.appendChild(h("div",{class:"wt"},title));const ctrl=h("div",{class:"ctrl"});w.appendChild(ctrl);return ctrl;}
/* ========== W1 CLPM 路径图 ========== */
W_clpm=function(w){const ctrl=frame(w,w.dataset.title||"CLPM 路径图：打开 / 关闭不同类型的路径");
 const st={ar:true,cl:true,wc:true,a:.6,b:.5,c:.15,d:.05};
 const svg=el("svg",{viewBox:"0 0 640 300"});w.appendChild(svg);const ro=h("div",{class:"readout"});w.appendChild(ro);
 check(ctrl,"自回归 AR（a, b）",true,v=>{st.ar=v;draw();});check(ctrl,"交叉滞后 CL（c, d）",true,v=>{st.cl=v;draw();});check(ctrl,"同时（残差）相关",true,v=>{st.wc=v;draw();});
 const c2=h("div",{class:"ctrl"});w.insertBefore(c2,svg);
 slider(c2,"a 孤独→孤独",0,1,.05,st.a,v=>{st.a=v;draw();});slider(c2,"b 抑郁→抑郁",0,1,.05,st.b,v=>{st.b=v;draw();});
 slider(c2,"c 抑郁→孤独",-.5,.5,.05,st.c,v=>{st.c=v;draw();});slider(c2,"d 孤独→抑郁",-.5,.5,.05,st.d,v=>{st.d=v;draw();});
 function draw(){svg.innerHTML="";svg.dataset.uid=svg.dataset.uid||"w"+(++uidc);ensureDefs(svg);const u=svg.dataset.uid;
  const X=[90,320,550],Y={L:80,D:220};
  const arrow=(x1,y1,x2,y2,w,lab,dash)=>{const col=w>=0?css("--pos"):css("--neg");el("line",{x1,y1,x2,y2,stroke:col,"stroke-width":1+8*Math.abs(w),"marker-end":`url(#${u}-arr-${w>=0?"pos":"neg"})`,"stroke-dasharray":dash||""},svg);
   if(lab)el("text",{x:(x1+x2)/2,y:(y1+y2)/2-8,"text-anchor":"middle","font-size":"13","font-weight":"700"},svg,lab);};
  for(let t=0;t<2;t++){if(st.ar){arrow(X[t]+52,Y.L,X[t+1]-58,Y.L,st.a,"a = "+st.a);arrow(X[t]+52,Y.D,X[t+1]-58,Y.D,st.b,"b = "+st.b);}
   if(st.cl){arrow(X[t]+45,Y.D-22,X[t+1]-55,Y.L+24,st.c,"");arrow(X[t]+45,Y.L+22,X[t+1]-55,Y.D-24,st.d,"");
    el("text",{x:(X[t]+X[t+1])/2-34,y:Y.L+58,"font-size":"12"},svg,"c = "+st.c);el("text",{x:(X[t]+X[t+1])/2-34,y:Y.D-46,"font-size":"12"},svg,"d = "+st.d);}}
  if(st.wc)X.forEach((x,t)=>{el("path",{d:`M${x-50},${Y.L+8} C${x-95},${Y.L+50} ${x-95},${Y.D-50} ${x-50},${Y.D-8}`,fill:"none",stroke:"#9ca3af","stroke-width":2,"stroke-dasharray":"5 4","marker-end":`url(#${u}-arr-gry)`,"marker-start":`url(#${u}-arr-gry)`},svg);
   el("text",{x:x-100,y:(Y.L+Y.D)/2+4,"font-size":"11","text-anchor":"middle"},svg,t===0?"r":"ψ");});
  X.forEach((x,t)=>{[["L","孤独"],["D","抑郁"]].forEach(([k,nm])=>{el("rect",{x:x-50,y:Y[k]-24,width:100,height:48,rx:6,fill:k==="L"?"#f59e0b":"#14b8a6"},svg);el("text",{x,y:Y[k]+5,"text-anchor":"middle","font-size":"14","font-weight":"700",style:"fill:#fff"},svg,`${nm} T${t+1}`);});});
  const pieces=[];if(st.ar)pieces.push(`<b>${st.a}</b>·孤独<sub>t</sub>`);if(st.cl)pieces.push(`<b>${st.c}</b>·抑郁<sub>t</sub>`);const p2=[];if(st.ar)p2.push(`<b>${st.b}</b>·抑郁<sub>t</sub>`);if(st.cl)p2.push(`<b>${st.d}</b>·孤独<sub>t</sub>`);
  ro.innerHTML=`孤独<sub>t+1</sub> = ${pieces.join(" + ")||"0"} + e　｜　抑郁<sub>t+1</sub> = ${p2.join(" + ")||"0"} + e<br>`+
   (!st.ar&&st.cl?"关掉自回归后，交叉滞后路径会“吸收”变量自身的稳定性——这正是为什么交叉滞后必须控制自回归。":st.cl?`解读：控制了 T 时自身水平后，T 时孤独每高 1 个标准差，T+1 时抑郁平均高 ${st.d} 个标准差（这是预测，不是因果）。`:"没有交叉滞后路径：模型假设两个变量只靠各自的过去来预测自己。");}
 draw();w._redraw=draw;};
/* ========== W2 被试间 vs 被试内 ========== */
W_bw=function(w){const ctrl=frame(w,w.dataset.title||"被试间 vs 被试内：同一份数据，两种完全不同的关系");
 const st={rb:.7,rw:-.4,view:"raw",seed:7};const svg=el("svg",{viewBox:"0 0 560 330"});
 slider(ctrl,"被试间相关 ρB",-0.9,0.9,.1,st.rb,v=>{st.rb=v;draw();});slider(ctrl,"被试内相关 ρW",-0.9,0.9,.1,st.rw,v=>{st.rw=v;draw();});
 const sel=h("select",{},'<option value="raw">原始数据（混在一起）</option><option value="mean">只看每人均值（被试间）</option><option value="cent">每人减去自己的均值（被试内）</option>');ctrl.appendChild(sel);sel.onchange=()=>{st.view=sel.value;draw();};
 const nb=h("button",{class:"btn",type:"button"},"换一批人");nb.onclick=()=>{st.seed++;draw();};ctrl.appendChild(nb);
 w.appendChild(svg);const ro=h("div",{class:"readout"});w.appendChild(ro);
 function draw(){const r=rng(st.seed),P=12,T=6;const pts=[],col=[];const pal=["#ef4444","#f59e0b","#10b981","#3b82f6","#8b5cf6","#ec4899","#14b8a6","#84cc16","#f97316","#6366f1","#0ea5e9","#a855f7"];
  const mx=[],my=[];for(let i=0;i<P;i++){const z1=r.norm(),z2=r.norm();mx.push(2*z1);my.push(2*(st.rb*z1+Math.sqrt(1-st.rb*st.rb)*z2));}
  for(let i=0;i<P;i++)for(let t=0;t<T;t++){const e1=r.norm(),e2=r.norm();pts.push([mx[i]+.8*e1,my[i]+.8*(st.rw*e1+Math.sqrt(1-st.rw*st.rw)*e2),i]);}
  const pmx=Array(P).fill(0),pmy=Array(P).fill(0);pts.forEach(p=>{pmx[p[2]]+=p[0]/T;pmy[p[2]]+=p[1]/T;});
  let show;if(st.view==="raw")show=pts;else if(st.view==="mean")show=pmx.map((x,i)=>[x,pmy[i],i]);else show=pts.map(p=>[p[0]-pmx[p[2]],p[1]-pmy[p[2]],p[2]]);
  svg.innerHTML="";const lim=st.view==="cent"?3:6.5,X=v=>40+(v+lim)/(2*lim)*500,Y=v=>300-(v+lim)/(2*lim)*280;
  el("line",{x1:X(-lim),x2:X(lim),y1:Y(0),y2:Y(0),stroke:"#d1d5db"},svg);el("line",{x1:X(0),x2:X(0),y1:Y(-lim),y2:Y(lim),stroke:"#d1d5db"},svg);
  el("text",{x:540,y:Y(0)-6,"text-anchor":"end","font-size":"12"},svg,"孤独 →");el("text",{x:X(0)+6,y:28,"font-size":"12"},svg,"↑ 抑郁");
  show.forEach(p=>el("circle",{cx:X(p[0]),cy:Y(p[1]),r:st.view==="mean"?7:4,fill:pal[p[2]%pal.length],opacity:.8},svg));
  const rr=corr(pts.map(p=>p[0]),pts.map(p=>p[1])),rbE=corr(pmx,pmy),rwE=corr(pts.map(p=>p[0]-pmx[p[2]]),pts.map(p=>p[1]-pmy[p[2]]));
  ro.innerHTML=`原始数据相关 r = <b>${fmt(rr)}</b>　｜　每人均值之间的相关（被试间）= <b>${fmt(rbE)}</b>　｜　中心化后的相关（被试内）= <b>${fmt(rwE)}</b><br>`+
   (Math.sign(rbE)!==Math.sign(rwE)?"被试间与被试内方向相反！“孤独的人更抑郁”与“一个人比自己平时更孤独时更抑郁”是两个不同的问题。":"两层关系方向一致，但大小仍可能不同。")+
   " 每种颜色是一个人的 6 次测量。";}
 draw();w._redraw=draw;};
/* ========== W3 因果用词检测 ========== */
W_cause=function(w){frame(w,w.dataset.title||"因果用词检测器：粘贴一段结论，找出过度因果化的词");
 const ta=h("textarea",{rows:4},w.dataset.text||"结果表明，孤独感导致了青少年的抑郁，社交退缩是引起睡眠问题的关键原因，因此减少孤独就能降低抑郁。");w.appendChild(ta);
 const out=h("div",{class:"readout"});w.appendChild(out);
 const W=[["导致","“预测”/“与……相关”"],["引起","“预测了之后的”"],["造成","“与……共同出现”"],["原因","“预测因子 / 相关因素”"],["决定","“与……有关”"],["使得","“伴随着”"],["驱动","“较强地预测”（并说明是统计预测）"],["影响了","“预测了”"],["因此","删去推论，或改为“这提示（需进一步检验）”"],["就能","“可能有助于（需要干预研究检验）”"],["效应","说明是“交叉滞后系数/预测效应”"],["证明","“支持/与……一致”"],["作用于","“预测”"]];
 function run(){let t=ta.value.replace(/[&<>]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;"}[c]));const hits=[];
  W.forEach(([k,s])=>{if(t.includes(k)){hits.push(`<li><mark class="cw">${k}</mark> → 建议：${s}</li>`);t=t.split(k).join(`<mark class="cw">${k}</mark>`);}});
  out.innerHTML=`<div>${t}</div>`+(hits.length?`<ul>${hits.join("")}</ul>`:"<p>没有检测到常见因果词。仍请人工检查：句子是否暗示“改变 A 就会改变 B”？</p>")+'<p class="muted" style="margin:4px 0 0">注：这只是关键词提示，不能代替判断。例如“影响”在“期望影响（expected influence）”这一术语中是正常用法。</p>';}
 ta.addEventListener("input",run);run();};
/* ========== W4 权重矩阵 ↔ 网络图 ========== */
W_adj=function(w){const ctrl=frame(w,w.dataset.title||"权重矩阵 ↔ 网络图：改数字，看图怎么变");
 const n=5,names=["A","B","C","D","E"];let W=[[0,.3,0,0,-.2],[.3,0,.4,0,0],[0,.4,0,.25,0],[0,0,.25,0,.5],[-.2,0,0,.5,0]];let directed=false;
 check(ctrl,"有向网络（不再强制对称）",false,v=>{directed=v;if(!v){for(let i=0;i<n;i++)for(let j=0;j<i;j++)W[i][j]=W[j][i];}build();draw();});
 const two=h("div",{class:"two"});w.appendChild(two);const tw=h("div",{class:"tablewrap"});two.appendChild(tw);const svg=el("svg",{viewBox:"0 0 320 300"});two.appendChild(svg);
 const ro=h("div",{class:"readout"});w.appendChild(ro);
 function build(){let s='<table class="mat"><tr><th>从＼到</th>'+names.map(x=>`<th>${x}</th>`).join("")+"</tr>";
  for(let i=0;i<n;i++){s+=`<tr><th>${names[i]}</th>`;for(let j=0;j<n;j++)s+=i===j?'<td class="muted">0</td>':`<td><input type="number" step="0.05" min="-1" max="1" data-i="${i}" data-j="${j}" value="${W[i][j]}"></td>`;s+="</tr>";}
  tw.innerHTML=s+"</table>";$$("input",tw).forEach(inp=>inp.addEventListener("input",()=>{const i=+inp.dataset.i,j=+inp.dataset.j,v=Math.max(-1,Math.min(1,+inp.value||0));W[i][j]=v;if(!directed){W[j][i]=v;const o=$(`input[data-i="${j}"][data-j="${i}"]`,tw);if(o&&o!==inp)o.value=inp.value;}draw();}));}
 function draw(){const e=drawNet(svg,{nodes:names,pos:circleLayout(n,160,150,110),W,directed,maxW:.6,R:20,label:.001});const maxE=directed?n*(n-1):n*(n-1)/2;
  ro.innerHTML=`当前边数 <b>${e.length}</b> / 最多 ${maxE} 条，密度（density）= <b>${fmt(e.length/maxE)}</b>。正边为蓝色、负边为红色；线越粗 |权重| 越大。`+(directed?" 有向：第 i 行第 j 列 = 从 i 指向 j。":" 无向：矩阵关于对角线对称，[i,j] = [j,i]。");}
 build();draw();w._redraw=draw;};
/* ========== W5 相关 vs 偏相关（链式结构） ========== */
W_pcor=function(w){const ctrl=frame(w,w.dataset.title||"为什么失眠与注意力差“相关”，偏相关却≈0？");
 const st={a:.6,b:.6,c:0};const names=["失眠","疲劳","注意力差"];
 slider(ctrl,"失眠→疲劳 a",-.9,.9,.05,st.a,v=>{st.a=v;draw();});slider(ctrl,"疲劳→注意力差 b",-.9,.9,.05,st.b,v=>{st.b=v;draw();});slider(ctrl,"失眠→注意力差（直接）c",-.6,.6,.05,st.c,v=>{st.c=v;draw();});
 const two=h("div",{class:"two"});w.appendChild(two);const s1=el("svg",{viewBox:"0 0 300 240"}),s2=el("svg",{viewBox:"0 0 300 240"});
 const d1=h("div",{},"<b>相关网络（zero-order correlation）</b>"),d2=h("div",{},"<b>偏相关网络（partial correlation / GGM）</b>");d1.appendChild(s1);d2.appendChild(s2);two.appendChild(d1);two.appendChild(d2);const ro=h("div",{class:"readout"});w.appendChild(ro);
 function draw(){// 标准化结构方程：X=e，Y=aX+e，Z=bY+cX+e，方差均标准化
  const a=st.a,b=st.b,c=st.c;const vY=1,rXY=a;const covXZ=b*a+c;const vZ=b*b+c*c+2*b*c*a+Math.max(0.05,1-(b*b+c*c+2*b*c*a));const sz=Math.sqrt(vZ);
  const rXZ=covXZ/sz,rYZ=(b+c*a)/sz;const R=[[1,rXY,rXZ],[rXY,1,rYZ],[rXZ,rYZ,1]];const P=pcorFromCor(R);const pos=[{x:60,y:190},{x:150,y:50},{x:240,y:190}];
  if(!P){ro.textContent="矩阵不可逆，请调整参数。";return;}
  drawNet(s1,{nodes:names,pos,W:R.map((r,i)=>r.map((v,j)=>i===j?0:v)),maxW:1,R:26,label:.001,colors:["#14b8a6"]});drawNet(s2,{nodes:names,pos,W:P,maxW:1,R:26,label:.001,colors:["#8b5cf6"]});
  ro.innerHTML=`失眠—注意力差：相关 r = <b>${fmt(rXZ)}</b>，偏相关（控制疲劳后）= <b>${fmt(P[0][2])}</b>。`+(Math.abs(c)<.01?" 当 c = 0 时，二者的关联完全经由“疲劳”传递，控制疲劳后就消失了：这就是<b>条件独立</b>，GGM 中两节点之间没有边。":" 现在 c ≠ 0：控制疲劳后仍有剩余关联，所以 GGM 中保留了一条边。");}
 draw();w._redraw=draw;};
/* ========== W6 LASSO 惩罚与网络稀疏度 ========== */
W_lasso=function(w){const ctrl=frame(w,w.dataset.title||"调节 LASSO 惩罚 λ：看小边如何被压成 0");
 const names=["D1","D2","D3","D4","D5","A1","A2","A3"],n=8,r=rng(11);const T=Array.from({length:n},()=>new Array(n).fill(0));
 [[0,1,.35],[1,2,.2],[2,3,.3],[3,4,.25],[0,4,.15],[5,6,.4],[6,7,.3],[5,7,.15],[2,6,.18],[4,5,.12]].forEach(([i,j,v])=>{T[i][j]=T[j][i]=v;});
 let N=300,lam=.05,showT=false;let S=null;
 function sample(){S=T.map(r=>r.slice());for(let i=0;i<n;i++)for(let j=i+1;j<n;j++){const v=T[i][j]+r.norm()/Math.sqrt(N);S[i][j]=S[j][i]=v;}}
 slider(ctrl,"惩罚 λ",0,.3,.01,lam,v=>{lam=v;draw();});const ns=h("select",{},'<option>100</option><option selected>300</option><option>1000</option>');const nl=h("label",{},"样本量 N ");nl.appendChild(ns);ctrl.appendChild(nl);
 ns.onchange=()=>{N=+ns.value;sample();draw();};check(ctrl,"标出真实结构",false,v=>{showT=v;draw();});
 const two=h("div",{class:"two"});w.appendChild(two);const svg=el("svg",{viewBox:"0 0 320 300"});two.appendChild(svg);const side=h("div",{});two.appendChild(side);
 function draw(){const E=S.map((rw,i)=>rw.map((v,j)=>i===j?0:soft(v,lam)));const pos=circleLayout(n,160,150,115);drawNet(svg,{nodes:names,pos,W:E,maxW:.45,R:17,groups:[0,0,0,0,0,1,1,1],colors:["#14b8a6","#f59e0b"]});
  let tp=0,fp=0,fn=0,tot=0;for(let i=0;i<n;i++)for(let j=i+1;j<n;j++){const est=Math.abs(E[i][j])>1e-9,tru=T[i][j]!==0;if(est){tot++;if(tru)tp++;else fp++;}else if(tru)fn++;
   if(showT&&tru)el("line",{x1:pos[i].x,y1:pos[i].y,x2:pos[j].x,y2:pos[j].y,stroke:"#10b981","stroke-width":1,"stroke-dasharray":"2 3"},svg,null);}
  side.innerHTML=`<div class="readout">非零边：<b>${tot}</b> / 28　密度 <b>${fmt(tot/28)}</b><br>找回的真实边：<b>${tp}</b> / 10<br>假阳性边（false positive）：<b>${fp}</b><br>漏掉的真实边：<b>${fn}</b></div>
   <p style="font-size:.88rem">λ = 0 时几乎每对节点都有一条小边（“满屏小边”），其中多数只是抽样噪声。λ 增大，小边先被压成 0，大边也被“缩小”。λ 过大则真实边也会被漏掉。<b>EBIC</b> 或交叉验证就是在帮我们自动选一个折中的 λ。</p>
   <p class="muted" style="font-size:.8rem">（示意：这里用“软阈值”直接作用在样本偏相关上，以便看清机制；真实的 graphical lasso 是对整个精度矩阵加惩罚，结果相近但不完全相同。）</p>`;}
 sample();draw();w._redraw=draw;};
/* ========== W7 中心性计算器 ========== */
W_cent=function(w){const ctrl=frame(w,w.dataset.title||"中心性计算器：强度、期望影响与桥接期望影响");
 const names=["D1","D2","D3","A1","A2","A3"],n=6,grp=[0,0,0,1,1,1];const W=Array.from({length:n},()=>new Array(n).fill(0));
 [[0,1,.4],[1,2,.3],[0,2,.2],[3,4,.35],[4,5,.3],[3,5,-.15],[2,3,.25],[1,4,-.1]].forEach(([i,j,v])=>{W[i][j]=W[j][i]=v;});
 const sel=h("select",{});const pairs=[];for(let i=0;i<n;i++)for(let j=i+1;j<n;j++){pairs.push([i,j]);sel.appendChild(h("option",{value:pairs.length-1},`${names[i]} — ${names[j]}`));}
 const lab=h("label",{},"选择一条边 ");lab.appendChild(sel);ctrl.appendChild(lab);let cur=pairs.findIndex(p=>p[0]===2&&p[1]===3);sel.value=cur;
 const sl=slider(ctrl,"权重",-.6,.6,.05,W[2][3],v=>{const [i,j]=pairs[cur];W[i][j]=W[j][i]=v;draw();});sel.onchange=()=>{cur=+sel.value;const [i,j]=pairs[cur];sl.value=W[i][j];sl.nextSibling.textContent=W[i][j];};
 const two=h("div",{class:"two"});w.appendChild(two);const svg=el("svg",{viewBox:"0 0 320 280"});two.appendChild(svg);const tb=h("div",{class:"tablewrap"});two.appendChild(tb);const bc=el("svg",{});w.appendChild(bc);
 function draw(){const pos=[{x:60,y:70},{x:60,y:210},{x:130,y:140},{x:200,y:140},{x:270,y:70},{x:270,y:210}];drawNet(svg,{nodes:names,pos,W,maxW:.5,R:20,groups:grp,colors:["#14b8a6","#f59e0b"],label:.001});
  const S=[],E=[],BS=[],BE=[];for(let i=0;i<n;i++){let s=0,e=0,bs=0,be=0;for(let j=0;j<n;j++){if(i===j)continue;s+=Math.abs(W[i][j]);e+=W[i][j];if(grp[i]!==grp[j]){bs+=Math.abs(W[i][j]);be+=W[i][j];}}S.push(s);E.push(e);BS.push(bs);BE.push(be);}
  tb.innerHTML="<table><tr><th>节点</th><th>强度</th><th>EI</th><th>桥接强度</th><th>桥接 EI</th></tr>"+names.map((nm,i)=>`<tr><td>${nm}</td><td>${fmt(S[i])}</td><td>${fmt(E[i])}</td><td>${fmt(BS[i])}</td><td>${fmt(BE[i])}</td></tr>`).join("")+"</table><p class='muted' style='font-size:.82rem'>D = 抑郁社群，A = 焦虑社群。强度 = Σ|w|；EI = Σw（保留正负）；桥接指标只累加连到另一社群的边。</p>";
  barChart(bc,names,[S,E],{names:["强度 strength","期望影响 EI"],H:200});}
 draw();w._redraw=draw;};
/* ========== W8 CLPN 有向网络 ========== */
W_clpn=function(w){const mode=w.dataset.mode||"view";const ctrl=frame(w,w.dataset.title||"交叉滞后面板网络（示意数据）");
 let B=demoB(w.dataset.which);let showAR=mode==="view1",thr=0,hl=null;
 if(w.dataset.compare){const sl=h("select",{},'<option value="pop">观察数据的 CLPN 目标（true_B_population）</option><option value="within">生成模型的被试内 B（true_B_within）</option>');const lb=h("label",{},"显示矩阵 ");lb.appendChild(sl);ctrl.appendChild(lb);sl.onchange=()=>{B=demoB(sl.value);draw();};}
 check(ctrl,"显示自回归环（对角线）",showAR,v=>{showAR=v;draw();});slider(ctrl,"显示阈值 |β| >",0,.15,.01,0,v=>{thr=v;draw();});
 const two=h("div",{class:"two"});w.appendChild(two);const svg=el("svg",{viewBox:"0 0 400 380"});two.appendChild(svg);const side=h("div",{});two.appendChild(side);
 const bc=el("svg",{});if(mode==="ei")w.appendChild(bc);
 svg.addEventListener("click",e=>{const g=e.target.closest("g.node");hl=g?(hl===+g.dataset.i?null:+g.dataset.i):null;draw();});
 function draw(){const pos=circleLayout(9,200,190,130);drawNet(svg,{nodes:CL_NODES,pos,W:B,directed:true,maxW:.18,threshold:thr,showLoops:showAR,groups:CL_GROUP,colors:["#f59e0b","#14b8a6"],R:19,highlight:hl});
  const p=9,out=[],inn=[],bo=[],bi=[];for(let k=0;k<p;k++){let o=0,i2=0,b1=0,b2=0;for(let j=0;j<p;j++){if(j===k)continue;o+=B[k][j];i2+=B[j][k];if(CL_GROUP[j]!==CL_GROUP[k]){b1+=B[k][j];b2+=B[j][k];}}out.push(o);inn.push(i2);bo.push(b1);bi.push(b2);}
  let s="";if(hl!=null){const outs=[],ins=[];for(let j=0;j<p;j++){if(j===hl)continue;if(B[hl][j])outs.push(`${CL_NODES[j]} (${fmt(B[hl][j])})`);if(B[j][hl])ins.push(`${CL_NODES[j]} (${fmt(B[j][hl])})`);}
   s=`<div class="readout"><b>${CL_NAMES[hl]}</b><br>自回归 β = <b>${fmt(B[hl][hl])}</b><br>→ 预测（出边）：${outs.join("、")||"无"}<br>← 被预测（入边）：${ins.join("、")||"无"}<br>out-EI = <b>${fmt(out[hl])}</b>，in-EI = <b>${fmt(inn[hl])}</b></div>`;}
  else s='<div class="readout">点击一个节点，查看它“预测谁”（出边）和“被谁预测”（入边）。</div>';
  s+='<p style="font-size:.85rem">'+CL_NAMES.join("；")+'。橙色 = 孤独题目，青色 = 抑郁题目。</p>';
  if(mode==="ei"){s+="<table><tr><th>节点</th><th>out-EI</th><th>in-EI</th><th>桥接 out</th><th>桥接 in</th></tr>"+CL_NODES.map((nm,k)=>`<tr${k===hl?' style="background:rgba(99,102,241,.12)"':""}><td>${nm}</td><td>${fmt(out[k])}</td><td>${fmt(inn[k])}</td><td>${fmt(bo[k])}</td><td>${fmt(bi[k])}</td></tr>`).join("")+"</table>";
   barChart(bc,CL_NODES,[out,inn],{names:["out-EI（行和）","in-EI（列和）"],H:200});}
  side.innerHTML=s;}
 draw();w._redraw=draw;};
/* ========== W9 系数矩阵热图（行=T1 预测，列=T2 结果） ========== */
W_bmat=function(w){frame(w,w.dataset.title||"系数矩阵 B：行 = T1 预测变量，列 = T2 结果变量");const B=demoB();const tb=h("div",{class:"tablewrap"});w.appendChild(tb);const ro=h("div",{class:"readout"},"把鼠标移到（或点击）任意格子上。");w.appendChild(ro);
 let s='<table class="mat"><tr><th>T1＼T2</th>'+CL_NODES.map(x=>`<th>${x}</th>`).join("")+"<th>行和 out-EI*</th></tr>";
 CL_NODES.forEach((r,i)=>{s+=`<tr><th>${r}</th>`;let rs=0;CL_NODES.forEach((c,j)=>{const v=B[i][j];if(i!==j)rs+=v;const a=Math.min(1,Math.abs(v)/.5);const bg=v>0?`rgba(37,99,235,${a})`:v<0?`rgba(220,38,38,${a})`:"transparent";
  s+=`<td data-i="${i}" data-j="${j}" style="background:${bg};color:${a>.5?"#fff":"inherit"};cursor:pointer;${i===j?"outline:2px dashed #9ca3af;outline-offset:-3px":""}">${v?fmt(v):"·"}</td>`;});s+=`<td><b>${fmt(rs)}</b></td></tr>`;});
 s+="<tr><th>列和 in-EI*</th>"+CL_NODES.map((c,j)=>{let cs=0;CL_NODES.forEach((r,i)=>{if(i!==j)cs+=B[i][j];});return`<td><b>${fmt(cs)}</b></td>`;}).join("")+"<td></td></tr></table><p class='muted' style='font-size:.8rem'>* 不含对角线（自回归）。虚线框 = 对角线 = 自回归边。</p>";
 tb.innerHTML=s;const f=e=>{const td=e.target.closest("td[data-i]");if(!td)return;const i=+td.dataset.i,j=+td.dataset.j,v=B[i][j];
  ro.innerHTML=i===j?`B[${CL_NODES[i]}, ${CL_NODES[j]}] = <b>${fmt(v)}</b>：<b>自回归边</b>——控制其他所有 T1 题目后，T1 的“${CL_NAMES[i]}”对 T2 自身的预测。`:
   `B[${CL_NODES[i]}, ${CL_NODES[j]}] = <b>${fmt(v)}</b>：<b>交叉滞后边</b> ${CL_NODES[i]}(T1) → ${CL_NODES[j]}(T2)。`+(v?`控制所有 T1 题目（包括 T1 的 ${CL_NODES[j]} 自己）后，T1“${CL_NAMES[i].replace(/^\w+\s*/,"")}”高 1 SD，T2“${CL_NAMES[j].replace(/^\w+\s*/,"")}”预测值高 ${fmt(v)} SD。`:"LASSO 把它压成了 0：在这个惩罚水平下，它没有被选入模型（≠ 证明无关）。");};
 tb.addEventListener("mouseover",f);tb.addEventListener("click",f);};
/* ========== W10 LASSO 系数路径 ========== */
W_path=function(w){const ctrl=frame(w,w.dataset.title||"一个 T2 节点的 LASSO 系数路径：λ 从大到小，变量依次“进入”模型");
 const names=["D1(自回归)","L3","D2","L4","D3","L1","D5","L2","D4"],ols=[.36,.17,.11,.08,.07,.05,-.04,.03,.015];const cols=["#111827","#f59e0b","#14b8a6","#f97316","#0ea5e9","#eab308","#8b5cf6","#fb923c","#22c55e"];
 const lmin=.03,l1se=.07;let lam=lmin;slider(ctrl,"λ",0,.4,.005,lam,v=>{lam=v;draw();});
 const b1=h("button",{class:"btn",type:"button"},"跳到 lambda.min");const b2=h("button",{class:"btn",type:"button"},"跳到 lambda.1se");ctrl.appendChild(b1);ctrl.appendChild(b2);
 const sl=$("input",ctrl);b1.onclick=()=>{lam=lmin;sl.value=lam;sl.nextSibling.textContent=lam;draw();};b2.onclick=()=>{lam=l1se;sl.value=lam;sl.nextSibling.textContent=lam;draw();};
 const svg=el("svg",{viewBox:"0 0 600 280"});w.appendChild(svg);const ro=h("div",{class:"readout"});w.appendChild(ro);
 function draw(){svg.innerHTML="";const X=l=>560-l/.4*500,Y=v=>230-(v+.05)/.45*210;el("line",{x1:60,x2:560,y1:Y(0),y2:Y(0),stroke:"#9ca3af"},svg);
  for(let t=0;t<=4;t++){const l=t*.1;el("text",{x:X(l),y:262,"text-anchor":"middle","font-size":"10"},svg,fmt(l));}el("text",{x:310,y:278,"text-anchor":"middle","font-size":"11"},svg,"← λ 越大惩罚越强（右→左：λ 变小）");
  [0,.1,.2,.3,.4].forEach(v=>el("text",{x:54,y:Y(v)+3,"text-anchor":"end","font-size":"10"},svg,fmt(v,1)));
  ols.forEach((b,k)=>{let d="";for(let l=0;l<=.4001;l+=.005)d+=(d?"L":"M")+X(l)+","+Y(soft(b,l));el("path",{d,fill:"none",stroke:cols[k],"stroke-width":2},svg);el("text",{x:X(0)+4,y:Y(b)+3,"font-size":"10",style:"fill:"+cols[k]},svg,names[k]);});
  [[lmin,"min"],[l1se,"1se"]].forEach(([l,t])=>{el("line",{x1:X(l),x2:X(l),y1:15,y2:235,stroke:"#9ca3af","stroke-dasharray":"3 3"},svg);el("text",{x:X(l),y:12,"font-size":"10","text-anchor":"middle"},svg,"λ."+t);});
  el("line",{x1:X(lam),x2:X(lam),y1:15,y2:235,stroke:css("--neg"),"stroke-width":2},svg);
  const act=ols.map((b,k)=>[names[k],soft(b,lam)]).filter(x=>Math.abs(x[1])>1e-9);
  ro.innerHTML=`λ = <b>${lam}</b> 时，非零系数 <b>${act.length}</b> 个：${act.map(([n,v])=>`${n} ${fmt(v,3)}`).join("，")||"（全部为 0）"}。<br>注意：留下的系数也被“缩小”了（与 λ = 0 时相比）。lambda.1se 比 lambda.min 更大，所以更稀疏、更保守。<span class="muted">（示意：假设预测变量相互正交，此时 LASSO 解恰好是软阈值。）</span>`;}
 draw();w._redraw=draw;};
/* ========== W11 bootstrap 一个相关系数 ========== */
W_boot=function(w){const ctrl=frame(w,w.dataset.title||"Bootstrap：用手头样本模拟“再做 1000 次研究”");
 let N=50,rho=.3,seed=3,data=[],boots=[];
 const ns=slider(ctrl,"样本量 N",20,400,10,N,v=>{N=v;gen();});slider(ctrl,"总体相关 ρ",-.8,.8,.1,rho,v=>{rho=v;gen();});
 const b1=h("button",{class:"btn",type:"button"},"抽 1 次 bootstrap 样本"),b2=h("button",{class:"btn primary",type:"button"},"运行 1000 次"),b3=h("button",{class:"btn",type:"button"},"新样本");ctrl.append(b1,b2,b3);
 const step=h("div",{class:"readout",style:"font-family:var(--mono);font-size:.8rem;max-height:90px;overflow:auto"});w.appendChild(step);const svg=el("svg",{});w.appendChild(svg);const ro=h("div",{class:"readout"});w.appendChild(ro);
 const r=rng(99);function gen(){const rr=rng(seed);data=[];for(let i=0;i<N;i++){const x=rr.norm();data.push([x,rho*x+Math.sqrt(1-rho*rho)*rr.norm()]);}boots=[];step.textContent="原始样本已生成。点击“抽 1 次”看看有放回抽样是什么样子。";draw();}
 const rOf=idx=>corr(idx.map(i=>data[i][0]),idx.map(i=>data[i][1]));
 function one(){const idx=Array.from({length:N},()=>Math.floor(r()*N));boots.push(rOf(idx));return idx;}
 b1.onclick=()=>{const idx=one();const cnt={};idx.forEach(i=>cnt[i]=(cnt[i]||0)+1);const dup=Object.values(cnt).filter(c=>c>1).length,miss=N-Object.keys(cnt).length;
  step.innerHTML=`抽到的个案编号：${idx.slice(0,40).map(i=>i+1).join(", ")}${N>40?" …":""}<br>→ 有 ${dup} 人被抽到不止一次，${miss} 人（约 ${fmt(100*miss/N,0)}%）这次没被抽到。这次的 r* = ${fmt(boots[boots.length-1],3)}`;draw();};
 b2.onclick=()=>{for(let k=0;k<1000;k++)one();step.textContent=`已累计 ${boots.length} 次 bootstrap。`;draw();};b3.onclick=()=>{seed++;gen();};
 function draw(){const r0=rOf(data.map((_,i)=>i));const z=Math.atanh(r0),se=1/Math.sqrt(N-3),lo=Math.tanh(z-1.96*se),hi=Math.tanh(z+1.96*se);
  if(boots.length<2){svg.innerHTML="";svg.setAttribute("viewBox","0 0 520 60");el("text",{x:260,y:34,"text-anchor":"middle","font-size":"13"},svg,"（还没有 bootstrap 结果）");ro.innerHTML=`样本相关 r = <b>${fmt(r0,3)}</b>；cor.test() 式的 95% CI（Fisher z）= [<b>${fmt(lo)}</b>, <b>${fmt(hi)}</b>]`;return;}
  const bl=quant(boots,.025),bh=quant(boots,.975);histogram(svg,boots,{lo:-1,hi:1,bins:50,marks:[[r0,css("--ink"),"样本 r"],[bl,css("--neg"),"2.5%"],[bh,css("--neg"),"97.5%"]]});
  ro.innerHTML=`样本 r = <b>${fmt(r0,3)}</b>；bootstrap 次数 B = <b>${boots.length}</b>；bootstrap 标准误 ≈ <b>${fmt(Math.sqrt(boots.reduce((s,v)=>s+(v-boots.reduce((a,b)=>a+b,0)/boots.length)**2,0)/(boots.length-1)),3)}</b><br>百分位 95% 区间 = [<b>${fmt(bl)}</b>, <b>${fmt(bh)}</b>]　对比 Fisher z 区间 = [<b>${fmt(lo)}</b>, <b>${fmt(hi)}</b>]　→ 两者通常很接近。试着把 N 调小：区间明显变宽。`;}
 gen();w._redraw=draw;};
/* ========== W12 正则化边的 bootstrap 区间 ========== */
W_edgeci=function(w){/* 总体目标值取自 data/true_B_population.csv */const ctrl=frame(w,w.dataset.title||"CLPN 边权重的 bootstrap 区间（模拟）：为什么很多区间“粘”在 0 上");
 const E=[["dep3→dep4", 0.169], ["lone2→lone4", 0.142], ["dep1→dep5", 0.126], ["lone3→dep1", 0.118], ["lone1→dep2", 0.102], ["lone4→dep5", 0.083], ["dep4→lone2", -0.083], ["dep2→lone3", 0.082], ["lone1→lone3", 0.072], ["lone3→lone1", 0.071], ["lone1→lone2", 0.07], ["lone2→lone3", 0.068], ["lone2→lone1", 0.068], ["lone4→lone2", 0.066], ["lone3→lone2", 0.065], ["lone4→lone3", 0.064], ["lone3→dep5", -0.001], ["dep2→lone4", 0.001], ["lone3→dep2", 0.0]];
 let N=400,lam=.03,B=500,seed=5;const svg=el("svg",{});
 const sel=h("select",{},'<option>200</option><option selected>400</option><option>800</option><option>2000</option>');const nl=h("label",{},"样本量 N ");nl.appendChild(sel);ctrl.appendChild(nl);sel.onchange=()=>{N=+sel.value;draw();};
 slider(ctrl,"惩罚 λ",0,.08,.01,lam,v=>{lam=v;draw();});const rb=h("button",{class:"btn",type:"button"},"重新 bootstrap");rb.onclick=()=>{seed++;draw();};ctrl.appendChild(rb);
 w.appendChild(svg);const ro=h("div",{class:"readout"});w.appendChild(ro);
 function draw(){const r=rng(seed),se=1/Math.sqrt(N);const samp=E.map(([,t])=>t+se*.9*r.norm());const est=samp.map(v=>soft(v,lam));
  const rows=E.map(([nm],k)=>{const bs=[];for(let b=0;b<B;b++)bs.push(soft(samp[k]+se*r.norm(),lam));return{nm,est:est[k],tru:E[k][1],lo:quant(bs,.025),hi:quant(bs,.975),z:bs.filter(v=>v===0).length/B};});
  rows.sort((a,b)=>b.est-a.est);const W=600,H=24+rows.length*18;svg.setAttribute("viewBox",`0 0 ${W} ${H}`);svg.innerHTML="";const X=v=>185+(v+.15)/.4*400;
  [-.1,0,.1,.2].forEach(v=>{el("line",{x1:X(v),x2:X(v),y1:10,y2:H-6,stroke:v===0?"#9ca3af":"#e5e7eb"},svg);el("text",{x:X(v),y:10,"font-size":"9","text-anchor":"middle"},svg,fmt(v,1));});
  rows.forEach((o,i)=>{const y=24+i*18;el("text",{x:8,y:y+4,"font-size":"11"},svg,o.nm);el("text",{x:122,y:y+4,"font-size":"9",style:"fill:#6b7280"},svg,`0占${fmt(100*o.z,0)}%`);
   el("line",{x1:X(o.lo),x2:X(o.hi)+(o.lo===o.hi?1:0),y1:y,y2:y,stroke:css("--accent"),"stroke-width":5,"stroke-opacity":.35,"stroke-linecap":"round"},svg);
   el("circle",{cx:X(o.est),cy:y,r:4,fill:css("--neg")},svg);el("circle",{cx:X(o.tru),cy:y,r:3,fill:"none",stroke:"#10b981","stroke-width":1.5},svg);});
  const inc0=rows.filter(o=>o.lo<=0&&o.hi>=0).length;
  ro.innerHTML=`红点 = 样本估计，蓝条 = bootstrap 2.5%–97.5% 区间，绿圈 = 总体目标值（只有模拟时才知道）。“0占%”= 该边在 bootstrap 样本中被 LASSO 压成 0 的比例。<br>当前有 <b>${inc0}</b> / ${rows.length} 条边的区间包含 0。λ > 0 时，许多区间的一端恰好“卡”在 0 上，且区间整体向 0 偏——这就是为什么正则化估计的 bootstrap 区间<b>不能当作严格的 95% 置信区间</b>，而应看作“估计精度/抽样变异”的描述。把 N 调大，区间变窄、排序变稳。`;}
 draw();w._redraw=draw;};
/* ========== W13 case-dropping 与 CS 系数 ========== */
W_cs=function(w){const ctrl=frame(w,w.dataset.title||"个案删除 bootstrap 与 CS 系数（模拟）");
 let N=500,spread=.06,seed=1;const svg=el("svg",{viewBox:"0 0 600 260"});
 const sel=h("select",{},'<option>150</option><option>300</option><option selected>500</option><option>1000</option><option>3000</option>');const nl=h("label",{},"样本量 N ");nl.appendChild(sel);ctrl.appendChild(nl);sel.onchange=()=>{N=+sel.value;draw();};
 slider(ctrl,"节点间真实 EI 差异",.01,.15,.01,spread,v=>{spread=v;draw();});const rb=h("button",{class:"btn",type:"button"},"重新模拟");rb.onclick=()=>{seed++;draw();};ctrl.appendChild(rb);
 w.appendChild(svg);const ro=h("div",{class:"readout"});w.appendChild(ro);
 function draw(){const r=rng(seed),p=9;const tru=Array.from({length:p},(_,i)=>spread*(i-4)/4);const noiseSD=n=>.9/Math.sqrt(n);
  const full=tru.map(t=>t+noiseSD(N)*r.norm());const drops=[.05,.1,.2,.3,.4,.5,.6,.7,.75,.8,.85,.9,.95];const res=[];let cs=0;
  drops.forEach(d=>{const n=Math.round(N*(1-d));const cors=[];for(let b=0;b<200;b++){// 子样本估计与全样本估计共享部分信息：用条件方差近似
    const extra=Math.sqrt(Math.max(0,noiseSD(n)**2-noiseSD(N)**2));cors.push(corr(full.map(v=>v+extra*r.norm()),full));}
   const prop=cors.filter(c=>c>=.7).length/cors.length;res.push({d,prop,m:quant(cors,.5),lo:quant(cors,.025),hi:quant(cors,.975)});if(prop>=.95)cs=d;});
  svg.innerHTML="";const X=d=>50+d*540,Y=v=>230-(v+.2)/1.2*210;
  [0,.25,.5,.7,1].forEach(v=>{el("line",{x1:50,x2:590,y1:Y(v),y2:Y(v),stroke:v===.7?css("--neg"):"#e5e7eb","stroke-dasharray":v===.7?"4 3":""},svg);el("text",{x:44,y:Y(v)+3,"font-size":"10","text-anchor":"end"},svg,fmt(v,1));});
  el("text",{x:592,y:Y(.7)-4,"font-size":"10","text-anchor":"end",style:"fill:"+css("--neg")},svg,"r = 0.7");
  drops.forEach(d=>el("text",{x:X(d),y:248,"font-size":"9","text-anchor":"middle"},svg,Math.round(d*100)+"%"));el("text",{x:320,y:259,"font-size":"10","text-anchor":"middle"},svg,"删除的样本比例");
  let dPath="",lo="",hi="";res.forEach((o,i)=>{dPath+=(i?"L":"M")+X(o.d)+","+Y(o.m);});
  el("path",{d:res.map((o,i)=>(i?"L":"M")+X(o.d)+","+Y(o.hi)).join("")+res.slice().reverse().map(o=>"L"+X(o.d)+","+Y(o.lo)).join("")+"Z",fill:css("--accent"),opacity:.15},svg);
  el("path",{d:dPath,fill:"none",stroke:css("--accent"),"stroke-width":2.5},svg);res.forEach(o=>el("circle",{cx:X(o.d),cy:Y(o.m),r:3.5,fill:o.prop>=.95?"#10b981":"#9ca3af"},svg));
  if(cs>0)el("line",{x1:X(cs),x2:X(cs),y1:15,y2:232,stroke:"#10b981","stroke-width":2},svg);
  const verdict=cs>=.5?"≥ 0.5：中心性排序相当稳定，可以较有信心地解释。":cs>=.25?"0.25–0.5：勉强可接受，解释要谨慎。":"< 0.25：不稳定，不应解释中心性排序。";
  ro.innerHTML=`CS 系数（C = 0.7，95%）= <b>${fmt(cs)}</b>。${verdict}<br>折线 = 子样本中心性与全样本中心性相关的中位数，阴影 = 2.5%–97.5%；绿点表示该删除比例下 ≥ 95% 的子样本相关 ≥ 0.7。<span class="muted">（教学用简化模拟：以噪声大小 ∝ 1/√n 模拟子样本估计；真实分析请用 bootnet 的 type = "case"。）</span>`;}
 draw();w._redraw=draw;};
/* ========== W14 勾选清单（本地保存） ========== */
W_checklist=function(w){const key="clpn-ck-"+(w.dataset.key||"x");let st={};try{st=JSON.parse(localStorage.getItem(key))||{};}catch(e){}
 const items=JSON.parse($("script[type='application/json']",w).textContent);const title=w.dataset.title||"清单";w.innerHTML="";w.appendChild(h("div",{class:"wt"},title));
 const bar=h("div",{class:"bar"},"<i></i>"),cnt=h("div",{class:"score"});w.append(cnt,bar);const box=h("div",{class:"checklist"});w.appendChild(box);let n=0;
 items.forEach(it=>{if(typeof it==="string"&&it.startsWith("#")){box.appendChild(h("div",{class:"grp"},it.slice(1)));return;}const id="i"+(n++);const lab=h("label",{});const cb=h("input",{type:"checkbox"});cb.checked=!!st[id];
  cb.onchange=()=>{st[id]=cb.checked;try{localStorage.setItem(key,JSON.stringify(st));}catch(e){}upd();};lab.appendChild(cb);lab.appendChild(h("span",{},it));box.appendChild(lab);});
 const tools=h("div",{class:"ctrl"});const ex=h("button",{class:"btn",type:"button"},"导出为文本（复制）");const clr=h("button",{class:"btn",type:"button"},"清空勾选");tools.append(ex,clr);w.appendChild(tools);const out=h("textarea",{rows:6,style:"display:none"});w.appendChild(out);
 ex.onclick=()=>{out.style.display="block";out.value=$$("label",box).map(l=>(l.querySelector("input").checked?"[x] ":"[ ] ")+l.textContent).join("\n");out.select();try{document.execCommand("copy");}catch(e){}};
 clr.onclick=()=>{st={};try{localStorage.removeItem(key);}catch(e){}$$("input",box).forEach(c=>c.checked=false);upd();};
 function upd(){const all=$$("input",box),d=all.filter(c=>c.checked).length;cnt.textContent=`已完成 ${d} / ${all.length}（自动保存在本浏览器）`;bar.firstChild.style.width=(100*d/all.length)+"%";}upd();};
/* ========== W15 填空模板 → 生成文本 ========== */
W_tpl=function(w){const key="clpn-tpl-"+(w.dataset.key||"x");let st={};try{st=JSON.parse(localStorage.getItem(key))||{};}catch(e){}
 const spec=JSON.parse($("script[type='application/json']",w).textContent);w.innerHTML="";w.classList.add("tpl");w.appendChild(h("div",{class:"wt"},w.dataset.title||"模板"));
 const form=h("div",{});w.appendChild(form);spec.fields.forEach(([k,lab,ph])=>{const f=h("div",{class:"fld"});f.appendChild(h("span",{},lab));const inp=h("input",{type:"text",placeholder:ph||"","data-k":k});inp.value=st[k]||"";
  inp.addEventListener("input",()=>{st[k]=inp.value;try{localStorage.setItem(key,JSON.stringify(st));}catch(e){}render();});f.appendChild(inp);form.appendChild(f);});
 const out=h("div",{class:"outtext"});w.appendChild(out);const tools=h("div",{class:"ctrl"});const cp=h("button",{class:"btn primary",type:"button"},"复制生成的文本");const cl=h("button",{class:"btn",type:"button"},"清空");tools.append(cp,cl);w.appendChild(tools);
 const esc=s=>s.replace(/[&<>]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;"}[c]));
 function render(){out.innerHTML=esc(spec.text).replace(/\{\{(\w+)\}\}/g,(m,k)=>st[k]?esc(st[k]):`<span class="blank">［${esc((spec.fields.find(f=>f[0]===k)||[k,k])[1])}］</span>`);}
 cp.onclick=()=>{const t=out.innerText;(navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(()=>{cp.textContent="已复制";setTimeout(()=>cp.textContent="复制生成的文本",1200);}).catch(()=>{cp.textContent="请手动选择文本";});};
 cl.onclick=()=>{st={};try{localStorage.removeItem(key);}catch(e){}$$("input",form).forEach(i=>i.value="");render();};render();};
/* ========== W16 时间间隔与交叉滞后（连续时间直觉） ========== */
W_lag=function(w){const ctrl=frame(w,w.dataset.title||"测量间隔会改变交叉滞后系数的大小");
 let a=.8,c=.15;const svg=el("svg",{viewBox:"0 0 600 240"});slider(ctrl,"每月自回归",.5,.95,.05,a,v=>{a=v;draw();});slider(ctrl,"每月 孤独→抑郁",0,.3,.01,c,v=>{c=v;draw();});w.appendChild(svg);const ro=h("div",{class:"readout"});w.appendChild(ro);
 function draw(){// 二维 VAR(1)：A=[[a,0],[c,a]]，Δ 个月后的交叉效应 = (A^Δ)[1,0] = Δ a^{Δ-1} c
  svg.innerHTML="";const X=t=>50+t/24*520,Y=v=>210-v/.5*190;const vals=[];let mx=0,best=1;for(let t=1;t<=24;t++){const v=t*Math.pow(a,t-1)*c;vals.push(v);if(v>mx){mx=v;best=t;}}
  [0,.1,.2,.3,.4,.5].forEach(v=>{el("line",{x1:50,x2:570,y1:Y(v),y2:Y(v),stroke:"#e5e7eb"},svg);el("text",{x:44,y:Y(v)+3,"font-size":"10","text-anchor":"end"},svg,fmt(v,1));});
  [1,3,6,12,18,24].forEach(t=>el("text",{x:X(t),y:228,"font-size":"10","text-anchor":"middle"},svg,t+"月"));
  el("path",{d:vals.map((v,i)=>(i?"L":"M")+X(i+1)+","+Y(v)).join(""),fill:"none",stroke:css("--accent"),"stroke-width":2.5},svg);
  [1,6,12].forEach(t=>el("circle",{cx:X(t),cy:Y(vals[t-1]),r:4,fill:css("--neg")},svg));
  ro.innerHTML=`同一个“真实过程”，间隔 1 个月测到的交叉滞后 ≈ <b>${fmt(vals[0])}</b>，间隔 6 个月 ≈ <b>${fmt(vals[5])}</b>，间隔 12 个月 ≈ <b>${fmt(vals[11])}</b>；在约 <b>${best}</b> 个月时最大。<br>所以“交叉滞后小/不显著”可能只是间隔选得不合适。<span class="muted">（示意：二维一阶向量自回归，抑郁不反过来影响孤独。）</span>`;}
 draw();w._redraw=draw;};
const REG={clpm:W_clpm,bw:W_bw,cause:W_cause,adj:W_adj,pcor:W_pcor,lasso:W_lasso,cent:W_cent,clpn:W_clpn,bmat:W_bmat,path:W_path,boot:W_boot,edgeci:W_edgeci,cs:W_cs,checklist:W_checklist,tpl:W_tpl,lag:W_lag};
var W_clpm,W_bw,W_cause,W_adj,W_pcor,W_lasso,W_cent,W_clpn,W_bmat,W_path,W_boot,W_edgeci,W_cs,W_checklist,W_tpl,W_lag;
function init(){document.addEventListener("themechange",()=>$$(".widget").forEach(w=>w._redraw&&w._redraw()));
 $$(".widget[data-widget]").forEach(w=>{const f=REG[w.dataset.widget];if(!f){w.innerHTML="<p class='muted'>未知组件："+w.dataset.widget+"</p>";return;}try{f(w);}catch(e){console.error("组件出错",w.dataset.widget,e);w.insertAdjacentHTML("beforeend","<p class='warn'>交互组件加载失败，请刷新页面。</p>");}});
}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",init);else init();
})();

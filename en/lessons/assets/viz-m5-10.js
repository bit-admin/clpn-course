/* CLPN Course · M5–M10 interactive widget library (parallel to viz.js; shell, quizzes, copy, formulas handled by lesson.js) */
(function(){
"use strict";
const $=(s,r=document)=>r.querySelector(s), $$=(s,r=document)=>[...r.querySelectorAll(s)];
const NS="http://www.w3.org/2000/svg";
function el(tag,attrs,parent,text){const e=document.createElementNS(NS,tag);for(const k in attrs)e.setAttribute(k,attrs[k]);if(text!=null)e.textContent=text;if(parent)parent.appendChild(e);return e;}
function h(tag,attrs,html){const e=document.createElement(tag);if(attrs)for(const k in attrs)e.setAttribute(k,attrs[k]);if(html!=null)e.innerHTML=html;return e;}
const fmt=(x,d=2)=>(Math.abs(x)<1e-12?0:x).toFixed(d);
const css=v=>getComputedStyle(document.documentElement).getPropertyValue(v).trim()||"#888";
/* ---------- Random numbers (reproducible) ---------- */
function rng(seed){let a=seed>>>0;const u=()=>{a|=0;a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296;};
 let spare=null;u.norm=()=>{if(spare!==null){const s=spare;spare=null;return s;}let x,y,r;do{x=2*u()-1;y=2*u()-1;r=x*x+y*y;}while(!r||r>=1);const m=Math.sqrt(-2*Math.log(r)/r);spare=y*m;return x*m;};return u;}
/* ---------- Minimal linear algebra ---------- */
function inv(A){const n=A.length,M=A.map((r,i)=>r.concat(A.map((_,j)=>i===j?1:0)));
 for(let c=0;c<n;c++){let p=c;for(let r=c+1;r<n;r++)if(Math.abs(M[r][c])>Math.abs(M[p][c]))p=r;[M[c],M[p]]=[M[p],M[c]];const d=M[c][c];if(Math.abs(d)<1e-12)return null;
  for(let j=0;j<2*n;j++)M[c][j]/=d;for(let r=0;r<n;r++)if(r!==c){const f=M[r][c];for(let j=0;j<2*n;j++)M[r][j]-=f*M[c][j];}}
 return M.map(r=>r.slice(n));}
function pcorFromCor(R){const P=inv(R);if(!P)return null;return P.map((r,i)=>r.map((v,j)=>i===j?0:-v/Math.sqrt(P[i][i]*P[j][j])));}
function corr(x,y){const n=x.length;let mx=0,my=0;for(let i=0;i<n;i++){mx+=x[i];my+=y[i];}mx/=n;my/=n;let sxy=0,sx=0,sy=0;for(let i=0;i<n;i++){const a=x[i]-mx,b=y[i]-my;sxy+=a*b;sx+=a*a;sy+=b*b;}return sxy/Math.sqrt(sx*sy);}
const soft=(z,l)=>Math.sign(z)*Math.max(0,Math.abs(z)-l);
function quant(a,q){const s=[...a].sort((x,y)=>x-y),i=(s.length-1)*q,lo=Math.floor(i),hi=Math.ceil(i);return s[lo]+(s[hi]-s[lo])*(i-lo);}
/* ---------- General: Network plotting ---------- */
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
/* ---------- Illustrative CLPN (9 nodes: 4 Loneliness + 5 Depression) ---------- */
const CL_NODES=["lone1", "lone2", "lone3", "lone4", "dep1", "dep2", "dep3", "dep4", "dep5"];
const CL_NAMES=["lone1 Lack of companionship", "lone2 Feeling left out", "lone3 Feeling isolated", "lone4 No one understands me", "dep1 Depressed mood", "dep2 Loss of interest", "dep3 Sleep problems", "dep4 Fatigue", "dep5 Worthlessness"];
const CL_GROUP=[0,0,0,0,1,1,1,1,1];
/* Course data data/true_B_population.csv (population target of CLPN) and data/true_B_within.csv (within-person B of data-generating model) */
const B_POP=[[0.39, 0.07, 0.072, 0.062, 0.005, 0.102, 0.015, 0.013, 0.002], [0.068, 0.391, 0.068, 0.142, 0.012, 0.011, 0.019, 0.017, 0.015], [0.071, 0.065, 0.387, 0.063, 0.118, 0.0, 0.004, 0.002, -0.001], [0.061, 0.066, 0.064, 0.378, -0.003, 0.002, 0.005, 0.005, 0.083], [0.004, 0.008, -0.002, 0.002, 0.327, 0.059, 0.058, 0.054, 0.126], [0.009, 0.007, 0.082, 0.001, 0.061, 0.33, 0.061, 0.052, 0.055], [0.013, 0.016, 0.008, 0.011, 0.06, 0.058, 0.328, 0.169, 0.054], [0.01, -0.083, 0.01, 0.012, 0.055, 0.054, 0.059, 0.323, 0.053], [0.005, 0.013, 0.006, 0.009, 0.055, 0.053, 0.056, 0.048, 0.324]];
const B_WITHIN=[[0.35, 0.0, 0.0, 0.0, 0.0, 0.14, 0.0, 0.0, 0.0], [0.0, 0.35, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.35, 0.0, 0.18, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.35, 0.0, 0.0, 0.0, 0.0, 0.12], [0.0, 0.0, 0.0, 0.0, 0.3, 0.0, 0.0, 0.0, 0.1], [0.0, 0.0, 0.12, 0.0, 0.0, 0.3, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.3, 0.16, 0.0], [0.0, -0.15, 0.0, 0.0, 0.0, 0.0, 0.0, 0.3, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.3]];
function demoB(which){return (which==="within"?B_WITHIN:B_POP).map(r=>r.slice());}
/* ---------- Helpers: Sliders & Controls ---------- */
function slider(parent,label,min,max,step,val,onInput){const lab=h("label",{},`${label} `);const inp=h("input",{type:"range",min,max,step,value:val});const out=h("b",{},String(val));lab.appendChild(inp);lab.appendChild(out);
 inp.addEventListener("input",()=>{out.textContent=inp.value;onInput&&onInput(+inp.value);});parent.appendChild(lab);return inp;}
function check(parent,label,val,onChange){const lab=h("label",{});const inp=h("input",{type:"checkbox"});inp.checked=val;lab.appendChild(inp);lab.appendChild(document.createTextNode(label));inp.addEventListener("change",()=>onChange&&onChange(inp.checked));parent.appendChild(lab);return inp;}
function frame(w,title){w.innerHTML="";w.appendChild(h("div",{class:"wt"},title));const ctrl=h("div",{class:"ctrl"});w.appendChild(ctrl);return ctrl;}
/* ========== W1 CLPM Path Diagram ========== */
W_clpm=function(w){const ctrl=frame(w,w.dataset.title||"CLPM Path Diagram: Toggle different types of paths");
 const st={ar:true,cl:true,wc:true,a:.6,b:.5,c:.15,d:.05};
 const svg=el("svg",{viewBox:"0 0 640 300"});w.appendChild(svg);const ro=h("div",{class:"readout"});w.appendChild(ro);
 check(ctrl,"Autoregressive AR (a, b)",true,v=>{st.ar=v;draw();});check(ctrl,"Cross-lagged CL (c, d)",true,v=>{st.cl=v;draw();});check(ctrl,"Concurrent (residual) correlation",true,v=>{st.wc=v;draw();});
 const c2=h("div",{class:"ctrl"});w.insertBefore(c2,svg);
 slider(c2,"a Loneliness → Loneliness",0,1,.05,st.a,v=>{st.a=v;draw();});slider(c2,"b Depression → Depression",0,1,.05,st.b,v=>{st.b=v;draw();});
 slider(c2,"c Depression → Loneliness",-.5,.5,.05,st.c,v=>{st.c=v;draw();});slider(c2,"d Loneliness → Depression",-.5,.5,.05,st.d,v=>{st.d=v;draw();});
 function draw(){svg.innerHTML="";svg.dataset.uid=svg.dataset.uid||"w"+(++uidc);ensureDefs(svg);const u=svg.dataset.uid;
  const X=[90,320,550],Y={L:80,D:220};
  const arrow=(x1,y1,x2,y2,w,lab,dash)=>{const col=w>=0?css("--pos"):css("--neg");el("line",{x1,y1,x2,y2,stroke:col,"stroke-width":1+8*Math.abs(w),"marker-end":`url(#${u}-arr-${w>=0?"pos":"neg"})`,"stroke-dasharray":dash||""},svg);
   if(lab)el("text",{x:(x1+x2)/2,y:(y1+y2)/2-8,"text-anchor":"middle","font-size":"13","font-weight":"700"},svg,lab);};
  for(let t=0;t<2;t++){if(st.ar){arrow(X[t]+52,Y.L,X[t+1]-58,Y.L,st.a,"a = "+st.a);arrow(X[t]+52,Y.D,X[t+1]-58,Y.D,st.b,"b = "+st.b);}
   if(st.cl){arrow(X[t]+45,Y.D-22,X[t+1]-55,Y.L+24,st.c,"");arrow(X[t]+45,Y.L+22,X[t+1]-55,Y.D-24,st.d,"");
    el("text",{x:(X[t]+X[t+1])/2-34,y:Y.L+58,"font-size":"12"},svg,"c = "+st.c);el("text",{x:(X[t]+X[t+1])/2-34,y:Y.D-46,"font-size":"12"},svg,"d = "+st.d);}}
  if(st.wc)X.forEach((x,t)=>{el("path",{d:`M${x-50},${Y.L+8} C${x-95},${Y.L+50} ${x-95},${Y.D-50} ${x-50},${Y.D-8}`,fill:"none",stroke:"#9ca3af","stroke-width":2,"stroke-dasharray":"5 4","marker-end":`url(#${u}-arr-gry)`,"marker-start":`url(#${u}-arr-gry)`},svg);
   el("text",{x:x-100,y:(Y.L+Y.D)/2+4,"font-size":"11","text-anchor":"middle"},svg,t===0?"r":"ψ");});
  X.forEach((x,t)=>{[["L","Loneliness"],["D","Depression"]].forEach(([k,nm])=>{el("rect",{x:x-50,y:Y[k]-24,width:100,height:48,rx:6,fill:k==="L"?"#f59e0b":"#14b8a6"},svg);el("text",{x,y:Y[k]+5,"text-anchor":"middle","font-size":"14","font-weight":"700",style:"fill:#fff"},svg,`${nm} T${t+1}`);});});
  const pieces=[];if(st.ar)pieces.push(`<b>${st.a}</b>·Loneliness<sub>t</sub>`);if(st.cl)pieces.push(`<b>${st.c}</b>·Depression<sub>t</sub>`);const p2=[];if(st.ar)p2.push(`<b>${st.b}</b>·Depression<sub>t</sub>`);if(st.cl)p2.push(`<b>${st.d}</b>·Loneliness<sub>t</sub>`);
  ro.innerHTML=`Loneliness<sub>t+1</sub> = ${pieces.join(" + ")||"0"} + e | Depression<sub>t+1</sub> = ${p2.join(" + ")||"0"} + e<br>`+
   (!st.ar&&st.cl?"When autoregression is turned off, the cross-lagged path absorbs the variable's own stability—which is precisely why cross-lagged paths must control for autoregression.":st.cl?`Interpretation: Controlling for its own baseline at T, each 1 SD higher Loneliness at T predicts an average of ${st.d} SD higher Depression at T+1 (this is prediction, not causation).`:"No cross-lagged paths: The model assumes each variable is predicted solely by its own past.");}
 draw();w._redraw=draw;};
/* ========== W2 Between-Person vs. Within-Person ========== */
W_bw=function(w){const ctrl=frame(w,w.dataset.title||"Between-Person vs. Within-Person: Same Data, Two Completely Different Relationships");
 const st={rb:.7,rw:-.4,view:"raw",seed:7};const svg=el("svg",{viewBox:"0 0 560 330"});
 slider(ctrl,"Between-person correlation ρB",-0.9,0.9,.1,st.rb,v=>{st.rb=v;draw();});slider(ctrl,"Within-person correlation ρW",-0.9,0.9,.1,st.rw,v=>{st.rw=v;draw();});
 const sel=h("select",{},'<option value="raw">Raw data (pooled)</option><option value="mean">Person means only (between-person)</option><option value="cent">Person-mean centered (within-person)</option>');ctrl.appendChild(sel);sel.onchange=()=>{st.view=sel.value;draw();};
 const nb=h("button",{class:"btn",type:"button"},"New sample of individuals");nb.onclick=()=>{st.seed++;draw();};ctrl.appendChild(nb);
 w.appendChild(svg);const ro=h("div",{class:"readout"});w.appendChild(ro);
 function draw(){const r=rng(st.seed),P=12,T=6;const pts=[],col=[];const pal=["#ef4444","#f59e0b","#10b981","#3b82f6","#8b5cf6","#ec4899","#14b8a6","#84cc16","#f97316","#6366f1","#0ea5e9","#a855f7"];
  const mx=[],my=[];for(let i=0;i<P;i++){const z1=r.norm(),z2=r.norm();mx.push(2*z1);my.push(2*(st.rb*z1+Math.sqrt(1-st.rb*st.rb)*z2));}
  for(let i=0;i<P;i++)for(let t=0;t<T;t++){const e1=r.norm(),e2=r.norm();pts.push([mx[i]+.8*e1,my[i]+.8*(st.rw*e1+Math.sqrt(1-st.rw*st.rw)*e2),i]);}
  const pmx=Array(P).fill(0),pmy=Array(P).fill(0);pts.forEach(p=>{pmx[p[2]]+=p[0]/T;pmy[p[2]]+=p[1]/T;});
  let show;if(st.view==="raw")show=pts;else if(st.view==="mean")show=pmx.map((x,i)=>[x,pmy[i],i]);else show=pts.map(p=>[p[0]-pmx[p[2]],p[1]-pmy[p[2]],p[2]]);
  svg.innerHTML="";const lim=st.view==="cent"?3:6.5,X=v=>40+(v+lim)/(2*lim)*500,Y=v=>300-(v+lim)/(2*lim)*280;
  el("line",{x1:X(-lim),x2:X(lim),y1:Y(0),y2:Y(0),stroke:"#d1d5db"},svg);el("line",{x1:X(0),x2:X(0),y1:Y(-lim),y2:Y(lim),stroke:"#d1d5db"},svg);
  el("text",{x:540,y:Y(0)-6,"text-anchor":"end","font-size":"12"},svg,"Loneliness →");el("text",{x:X(0)+6,y:28,"font-size":"12"},svg,"↑ Depression");
  show.forEach(p=>el("circle",{cx:X(p[0]),cy:Y(p[1]),r:st.view==="mean"?7:4,fill:pal[p[2]%pal.length],opacity:.8},svg));
  const rr=corr(pts.map(p=>p[0]),pts.map(p=>p[1])),rbE=corr(pmx,pmy),rwE=corr(pts.map(p=>p[0]-pmx[p[2]]),pts.map(p=>p[1]-pmy[p[2]]));
  ro.innerHTML=`Pooled correlation r = <b>${fmt(rr)}</b> | Between-person correlation (person means) = <b>${fmt(rbE)}</b> | Within-person correlation (centered) = <b>${fmt(rwE)}</b><br>`+
   (Math.sign(rbE)!==Math.sign(rwE)?"Between-person and within-person correlations have opposite signs! 'People who are more lonely are more depressed' and 'when an individual feels more lonely than usual, they feel more depressed' are two entirely distinct questions.":"The two levels share the same direction, but their magnitudes can still differ substantially.")+
   " Each color represents 6 repeated measurements from one individual.";}
 draw();w._redraw=draw;};
/* ========== W3 Causal Language Detector ========== */
W_cause=function(w){frame(w,w.dataset.title||"Causal Language Detector: Paste a conclusion to identify overly causal phrasing");
 const ta=h("textarea",{rows:4},w.dataset.text||"Results show that loneliness causes adolescent depression, social withdrawal is the primary cause of sleep problems, and therefore reducing loneliness will reduce depression.");w.appendChild(ta);
 const out=h("div",{class:"readout"});w.appendChild(out);
 const W=[
  ["leads to","suggest 'predicts' or 'is associated with'"],
  ["lead to","suggest 'predict' or 'are associated with'"],
  ["causes","suggest 'predicts' or 'is longitudinally associated with'"],
  ["caused","suggest 'predicted'"],
  ["cause","suggest 'predictor / associated factor'"],
  ["results in","suggest 'predicts'"],
  ["resulted in","suggest 'predicted'"],
  ["drives","suggest 'strongly predicts' (clarify statistical prediction)"],
  ["driven by","suggest 'predicted by'"],
  ["determines","suggest 'is associated with'"],
  ["determined by","suggest 'associated with'"],
  ["impacted","suggest 'predicted'"],
  ["impacts","suggest 'predicts'"],
  ["affects","suggest 'predicts'"],
  ["affected","suggest 'predicted'"],
  ["therefore","omit causal inference, or revise to 'this suggests (requiring further testing)'"],
  ["will reduce","suggest 'may help reduce (needs intervention testing)'"],
  ["will decrease","suggest 'may help decrease'"],
  ["proves","suggest 'supports / is consistent with'"],
  ["proven","suggest 'supported'"],
  ["proof","suggest 'evidence'"],
  ["effect","clarify as 'cross-lagged coefficient / predictive effect'"]
 ];
 function run(){let t=ta.value.replace(/[&<>]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;"}[c]));const hits=[];
  W.forEach(([k,s])=>{const re=/^[a-z]/i.test(k)?new RegExp("\\b"+k+"\\b","gi"):new RegExp(k,"g");if(re.test(t)){hits.push(`<li><mark class="cw">${k}</mark> → Suggestion: ${s}</li>`);t=t.replace(re,m=>`<mark class="cw">${m}</mark>`);}});
  out.innerHTML=`<div>${t}</div>`+(hits.length?`<ul>${hits.join("")}</ul>`:"<p>No common causal words detected. Please still manually verify: does the sentence imply 'changing A will change B'?</p>")+'<p class="muted" style="margin:4px 0 0">Note: This is only a keyword heuristic and cannot replace critical judgment. For example, \"influence\" in \"expected influence\" is standard terminology.</p>';}
 ta.addEventListener("input",run);run();};
/* ========== W4 Weight Matrix ↔ Network Graph ========== */
W_adj=function(w){const ctrl=frame(w,w.dataset.title||"Weight Matrix ↔ Network Graph: Edit numbers to see how the graph changes");
 const n=5,names=["A","B","C","D","E"];let W=[[0,.3,0,0,-.2],[.3,0,.4,0,0],[0,.4,0,.25,0],[0,0,.25,0,.5],[-.2,0,0,.5,0]];let directed=false;
 check(ctrl,"Directed network (no longer forced to be symmetric)",false,v=>{directed=v;if(!v){for(let i=0;i<n;i++)for(let j=0;j<i;j++)W[i][j]=W[j][i];}build();draw();});
 const two=h("div",{class:"two"});w.appendChild(two);const tw=h("div",{class:"tablewrap"});two.appendChild(tw);const svg=el("svg",{viewBox:"0 0 320 300"});two.appendChild(svg);
 const ro=h("div",{class:"readout"});w.appendChild(ro);
 function build(){let s='<table class="mat"><tr><th>From \\ To</th>'+names.map(x=>`<th>${x}</th>`).join("")+"</tr>";
  for(let i=0;i<n;i++){s+=`<tr><th>${names[i]}</th>`;for(let j=0;j<n;j++)s+=i===j?'<td class="muted">0</td>':`<td><input type="number" step="0.05" min="-1" max="1" data-i="${i}" data-j="${j}" value="${W[i][j]}"></td>`;s+="</tr>";}
  tw.innerHTML=s+"</table>";$$("input",tw).forEach(inp=>inp.addEventListener("input",()=>{const i=+inp.dataset.i,j=+inp.dataset.j,v=Math.max(-1,Math.min(1,+inp.value||0));W[i][j]=v;if(!directed){W[j][i]=v;const o=$(`input[data-i="${j}"][data-j="${i}"]`,tw);if(o&&o!==inp)o.value=inp.value;}draw();}));}
 function draw(){const e=drawNet(svg,{nodes:names,pos:circleLayout(n,160,150,110),W,directed,maxW:.6,R:20,label:.001});const maxE=directed?n*(n-1):n*(n-1)/2;
  ro.innerHTML=`Current edges: <b>${e.length}</b> / max ${maxE}, density = <b>${fmt(e.length/maxE)}</b>. Positive edges are blue, negative edges are red; thicker lines indicate larger |weights|.`+(directed?" Directed: Row i, Column j = from i to j.":" Undirected: Matrix is symmetric across the diagonal, [i,j] = [j,i].");}
 build();draw();w._redraw=draw;};
/* ========== W5 Correlation vs. Partial Correlation (Chain Structure) ========== */
W_pcor=function(w){const ctrl=frame(w,w.dataset.title||"Why are insomnia and inattention correlated, yet their partial correlation is ≈ 0?");
 const st={a:.6,b:.6,c:0};const names=["Insomnia","Fatigue","Inattention"];
 slider(ctrl,"Insomnia → Fatigue a",-.9,.9,.05,st.a,v=>{st.a=v;draw();});slider(ctrl,"Fatigue → Inattention b",-.9,.9,.05,st.b,v=>{st.b=v;draw();});slider(ctrl,"Insomnia → Inattention (direct) c",-.6,.6,.05,st.c,v=>{st.c=v;draw();});
 const two=h("div",{class:"two"});w.appendChild(two);const s1=el("svg",{viewBox:"0 0 300 240"}),s2=el("svg",{viewBox:"0 0 300 240"});
 const d1=h("div",{},"<b>Correlation network (zero-order correlation)</b>"),d2=h("div",{},"<b>Partial correlation network (partial correlation / GGM)</b>");d1.appendChild(s1);d2.appendChild(s2);two.appendChild(d1);two.appendChild(d2);const ro=h("div",{class:"readout"});w.appendChild(ro);
 function draw(){// Standardized SEM: X=e, Y=aX+e, Z=bY+cX+e, all variances standardized
  const a=st.a,b=st.b,c=st.c;const vY=1,rXY=a;const covXZ=b*a+c;const vZ=b*b+c*c+2*b*c*a+Math.max(0.05,1-(b*b+c*c+2*b*c*a));const sz=Math.sqrt(vZ);
  const rXZ=covXZ/sz,rYZ=(b+c*a)/sz;const R=[[1,rXY,rXZ],[rXY,1,rYZ],[rXZ,rYZ,1]];const P=pcorFromCor(R);const pos=[{x:60,y:190},{x:150,y:50},{x:240,y:190}];
  if(!P){ro.textContent="Matrix is singular; please adjust parameters.";return;}
  drawNet(s1,{nodes:names,pos,W:R.map((r,i)=>r.map((v,j)=>i===j?0:v)),maxW:1,R:26,label:.001,colors:["#14b8a6"]});drawNet(s2,{nodes:names,pos,W:P,maxW:1,R:26,label:.001,colors:["#8b5cf6"]});
  ro.innerHTML=`Insomnia–Inattention: Correlation r = <b>${fmt(rXZ)}</b>, partial correlation (controlling for Fatigue) = <b>${fmt(P[0][2])}</b>.`+(Math.abs(c)<.01?" When c = 0, their association is entirely transmitted through Fatigue and disappears once Fatigue is controlled for: This is <b>conditional independence</b>, resulting in no edge between the two nodes in the GGM.":" Now c ≠ 0: Controlling for Fatigue leaves a residual association, so an edge is retained in the GGM.");}
 draw();w._redraw=draw;};
/* ========== W6 LASSO Penalty and Network Sparsity ========== */
W_lasso=function(w){const ctrl=frame(w,w.dataset.title||"Tuning the LASSO Penalty λ: How Small Edges Are Shrunk to Zero");
 const names=["D1","D2","D3","D4","D5","A1","A2","A3"],n=8,r=rng(11);const T=Array.from({length:n},()=>new Array(n).fill(0));
 [[0,1,.35],[1,2,.2],[2,3,.3],[3,4,.25],[0,4,.15],[5,6,.4],[6,7,.3],[5,7,.15],[2,6,.18],[4,5,.12]].forEach(([i,j,v])=>{T[i][j]=T[j][i]=v;});
 let N=300,lam=.05,showT=false;let S=null;
 function sample(){S=T.map(r=>r.slice());for(let i=0;i<n;i++)for(let j=i+1;j<n;j++){const v=T[i][j]+r.norm()/Math.sqrt(N);S[i][j]=S[j][i]=v;}}
 slider(ctrl,"Penalty λ",0,.3,.01,lam,v=>{lam=v;draw();});const ns=h("select",{},'<option>100</option><option selected>300</option><option>1000</option>');const nl=h("label",{},"Sample size N ");nl.appendChild(ns);ctrl.appendChild(nl);
 ns.onchange=()=>{N=+ns.value;sample();draw();};check(ctrl,"Highlight true structure",false,v=>{showT=v;draw();});
 const two=h("div",{class:"two"});w.appendChild(two);const svg=el("svg",{viewBox:"0 0 320 300"});two.appendChild(svg);const side=h("div",{});two.appendChild(side);
 function draw(){const E=S.map((rw,i)=>rw.map((v,j)=>i===j?0:soft(v,lam)));const pos=circleLayout(n,160,150,115);drawNet(svg,{nodes:names,pos,W:E,maxW:.45,R:17,groups:[0,0,0,0,0,1,1,1],colors:["#14b8a6","#f59e0b"]});
  let tp=0,fp=0,fn=0,tot=0;for(let i=0;i<n;i++)for(let j=i+1;j<n;j++){const est=Math.abs(E[i][j])>1e-9,tru=T[i][j]!==0;if(est){tot++;if(tru)tp++;else fp++;}else if(tru)fn++;
   if(showT&&tru)el("line",{x1:pos[i].x,y1:pos[i].y,x2:pos[j].x,y2:pos[j].y,stroke:"#10b981","stroke-width":1,"stroke-dasharray":"2 3"},svg,null);}
  side.innerHTML=`<div class="readout">Non-zero edges: <b>${tot}</b> / 28 | Density = <b>${fmt(tot/28)}</b><br>Recovered true edges: <b>${tp}</b> / 10<br>False positive edges: <b>${fp}</b><br>Missed true edges: <b>${fn}</b></div>
   <p style="font-size:.88rem">When λ = 0, almost every pair of nodes has a small edge (a "dense hairball"), most of which is merely sampling noise. As λ increases, small edges are shrunk to 0 first, and large edges are also shrunk. If λ is too large, true edges will also be missed. <b>EBIC</b> or cross-validation automatically selects an optimal trade-off λ.</p>
   <p class="muted" style="font-size:.8rem">(Illustration: Soft-thresholding is applied directly to sample partial correlations to make the mechanism transparent; the actual graphical lasso penalizes the entire precision matrix, yielding similar but not identical results.)</p>`;}
 sample();draw();w._redraw=draw;};
/* ========== W7 Centrality Calculator ========== */
W_cent=function(w){const ctrl=frame(w,w.dataset.title||"Centrality Calculator: Strength, Expected Influence, and Bridge Expected Influence");
 const names=["D1","D2","D3","A1","A2","A3"],n=6,grp=[0,0,0,1,1,1];const W=Array.from({length:n},()=>new Array(n).fill(0));
 [[0,1,.4],[1,2,.3],[0,2,.2],[3,4,.35],[4,5,.3],[3,5,-.15],[2,3,.25],[1,4,-.1]].forEach(([i,j,v])=>{W[i][j]=W[j][i]=v;});
 const sel=h("select",{});const pairs=[];for(let i=0;i<n;i++)for(let j=i+1;j<n;j++){pairs.push([i,j]);sel.appendChild(h("option",{value:pairs.length-1},`${names[i]} — ${names[j]}`));}
 const lab=h("label",{},"Select an edge ");lab.appendChild(sel);ctrl.appendChild(lab);let cur=pairs.findIndex(p=>p[0]===2&&p[1]===3);sel.value=cur;
 const sl=slider(ctrl,"Weight",-.6,.6,.05,W[2][3],v=>{const [i,j]=pairs[cur];W[i][j]=W[j][i]=v;draw();});sel.onchange=()=>{cur=+sel.value;const [i,j]=pairs[cur];sl.value=W[i][j];sl.nextSibling.textContent=W[i][j];};
 const two=h("div",{class:"two"});w.appendChild(two);const svg=el("svg",{viewBox:"0 0 320 280"});two.appendChild(svg);const tb=h("div",{class:"tablewrap"});two.appendChild(tb);const bc=el("svg",{});w.appendChild(bc);
 function draw(){const pos=[{x:60,y:70},{x:60,y:210},{x:130,y:140},{x:200,y:140},{x:270,y:70},{x:270,y:210}];drawNet(svg,{nodes:names,pos,W,maxW:.5,R:20,groups:grp,colors:["#14b8a6","#f59e0b"],label:.001});
  const S=[],E=[],BS=[],BE=[];for(let i=0;i<n;i++){let s=0,e=0,bs=0,be=0;for(let j=0;j<n;j++){if(i===j)continue;s+=Math.abs(W[i][j]);e+=W[i][j];if(grp[i]!==grp[j]){bs+=Math.abs(W[i][j]);be+=W[i][j];}}S.push(s);E.push(e);BS.push(bs);BE.push(be);}
  tb.innerHTML="<table><tr><th>Node</th><th>Strength</th><th>EI</th><th>Bridge Strength</th><th>Bridge EI</th></tr>"+names.map((nm,i)=>`<tr><td>${nm}</td><td>${fmt(S[i])}</td><td>${fmt(E[i])}</td><td>${fmt(BS[i])}</td><td>${fmt(BE[i])}</td></tr>`).join("")+"</table><p class='muted' style='font-size:.82rem'>D = Depression community, A = Anxiety community. Strength = Σ|w|; EI = Σw (retains signs); bridge metrics sum only edges connecting to the other community.</p>";
  barChart(bc,names,[S,E],{names:["Strength","Expected Influence (EI)"],H:200});}
 draw();w._redraw=draw;};
/* ========== W8 CLPN Directed Network ========== */
W_clpn=function(w){const mode=w.dataset.mode||"view";const ctrl=frame(w,w.dataset.title||"Cross-Lagged Panel Network (Illustrative Data)");
 let B=demoB(w.dataset.which);let showAR=mode==="view1",thr=0,hl=null;
 if(w.dataset.compare){const sl=h("select",{},'<option value="pop">Population target of observational CLPN (true_B_population)</option><option value="within">Within-person B of data-generating model (true_B_within)</option>');const lb=h("label",{},"Display matrix ");lb.appendChild(sl);ctrl.appendChild(lb);sl.onchange=()=>{B=demoB(sl.value);draw();};}
 check(ctrl,"Show autoregressive loops (diagonal)",showAR,v=>{showAR=v;draw();});slider(ctrl,"Display threshold |β| >",0,.15,.01,0,v=>{thr=v;draw();});
 const two=h("div",{class:"two"});w.appendChild(two);const svg=el("svg",{viewBox:"0 0 400 380"});two.appendChild(svg);const side=h("div",{});two.appendChild(side);
 const bc=el("svg",{});if(mode==="ei")w.appendChild(bc);
 svg.addEventListener("click",e=>{const g=e.target.closest("g.node");hl=g?(hl===+g.dataset.i?null:+g.dataset.i):null;draw();});
 function draw(){const pos=circleLayout(9,200,190,130);drawNet(svg,{nodes:CL_NODES,pos,W:B,directed:true,maxW:.18,threshold:thr,showLoops:showAR,groups:CL_GROUP,colors:["#f59e0b","#14b8a6"],R:19,highlight:hl});
  const p=9,out=[],inn=[],bo=[],bi=[];for(let k=0;k<p;k++){let o=0,i2=0,b1=0,b2=0;for(let j=0;j<p;j++){if(j===k)continue;o+=B[k][j];i2+=B[j][k];if(CL_GROUP[j]!==CL_GROUP[k]){b1+=B[k][j];b2+=B[j][k];}}out.push(o);inn.push(i2);bo.push(b1);bi.push(b2);}
  let s="";if(hl!=null){const outs=[],ins=[];for(let j=0;j<p;j++){if(j===hl)continue;if(B[hl][j])outs.push(`${CL_NODES[j]} (${fmt(B[hl][j])})`);if(B[j][hl])ins.push(`${CL_NODES[j]} (${fmt(B[j][hl])})`);}
   s=`<div class="readout"><b>${CL_NAMES[hl]}</b><br>Autoregressive β = <b>${fmt(B[hl][hl])}</b><br>→ Predicts (outgoing): ${outs.join(", ")||"None"}<br>← Predicted by (incoming): ${ins.join(", ")||"None"}<br>out-EI = <b>${fmt(out[hl])}</b>, in-EI = <b>${fmt(inn[hl])}</b></div>`;}
  else s='<div class="readout">Click a node to view what it predicts (outgoing edges) and what predicts it (incoming edges).</div>';
  s+='<p style="font-size:.85rem">'+CL_NAMES.join("; ")+'. Orange = Loneliness items, Teal = Depression items.</p>';
  if(mode==="ei"){s+="<table><tr><th>Node</th><th>out-EI</th><th>in-EI</th><th>Bridge out</th><th>Bridge in</th></tr>"+CL_NODES.map((nm,k)=>`<tr${k===hl?' style="background:rgba(99,102,241,.12)"':""}><td>${nm}</td><td>${fmt(out[k])}</td><td>${fmt(inn[k])}</td><td>${fmt(bo[k])}</td><td>${fmt(bi[k])}</td></tr>`).join("")+"</table>";
   barChart(bc,CL_NODES,[out,inn],{names:["out-EI (row sum)","in-EI (col sum)"],H:200});}
  side.innerHTML=s;}
 draw();w._redraw=draw;};
/* ========== W9 Coefficient Matrix Heatmap (Rows = T1 Predictors, Cols = T2 Outcomes) ========== */
W_bmat=function(w){frame(w,w.dataset.title||"Coefficient Matrix B: Rows = T1 Predictors, Columns = T2 Outcomes");const B=demoB();const tb=h("div",{class:"tablewrap"});w.appendChild(tb);const ro=h("div",{class:"readout"},"Hover over (or click) any cell.");w.appendChild(ro);
 let s='<table class="mat"><tr><th>T1 \\ T2</th>'+CL_NODES.map(x=>`<th>${x}</th>`).join("")+"<th>Row sum out-EI*</th></tr>";
 CL_NODES.forEach((r,i)=>{s+=`<tr><th>${r}</th>`;let rs=0;CL_NODES.forEach((c,j)=>{const v=B[i][j];if(i!==j)rs+=v;const a=Math.min(1,Math.abs(v)/.5);const bg=v>0?`rgba(37,99,235,${a})`:v<0?`rgba(220,38,38,${a})`:"transparent";
  s+=`<td data-i="${i}" data-j="${j}" style="background:${bg};color:${a>.5?"#fff":"inherit"};cursor:pointer;${i===j?"outline:2px dashed #9ca3af;outline-offset:-3px":""}">${v?fmt(v):"·"}</td>`;});s+=`<td><b>${fmt(rs)}</b></td></tr>`;});
 s+="<tr><th>Col sum in-EI*</th>"+CL_NODES.map((c,j)=>{let cs=0;CL_NODES.forEach((r,i)=>{if(i!==j)cs+=B[i][j];});return`<td><b>${fmt(cs)}</b></td>`;}).join("")+"<td></td></tr></table><p class='muted' style='font-size:.8rem'>* Excludes diagonal (autoregression). Dashed border = diagonal = autoregressive edge.</p>";
 tb.innerHTML=s;const f=e=>{const td=e.target.closest("td[data-i]");if(!td)return;const i=+td.dataset.i,j=+td.dataset.j,v=B[i][j];
  ro.innerHTML=i===j?`B[${CL_NODES[i]}, ${CL_NODES[j]}] = <b>${fmt(v)}</b>: <b>Autoregressive edge</b>—Predicting T2 self from T1 "${CL_NAMES[i]}", controlling for all other T1 items.`:
   `B[${CL_NODES[i]}, ${CL_NODES[j]}] = <b>${fmt(v)}</b>: <b>Cross-lagged edge</b> ${CL_NODES[i]}(T1) → ${CL_NODES[j]}(T2). `+(v?`Controlling for all T1 items (including T1 ${CL_NODES[j]} itself), each 1 SD higher on T1 "${CL_NAMES[i].replace(/^\w+\s*/,"")}" predicts a ${fmt(v)} SD higher value on T2 "${CL_NAMES[j].replace(/^\w+\s*/,"")}".`:"LASSO shrunk this edge to 0: At this penalty level, it was not selected into the model (≠ proof of no association).");};
 tb.addEventListener("mouseover",f);tb.addEventListener("click",f);};
/* ========== W10 LASSO Coefficient Path ========== */
W_path=function(w){const ctrl=frame(w,w.dataset.title||"LASSO Coefficient Path for a T2 Node: As λ Decreases, Variables Enter the Model in Sequence");
 const names=["D1 (autoregression)","L3","D2","L4","D3","L1","D5","L2","D4"],ols=[.36,.17,.11,.08,.07,.05,-.04,.03,.015];const cols=["#111827","#f59e0b","#14b8a6","#f97316","#0ea5e9","#eab308","#8b5cf6","#fb923c","#22c55e"];
 const lmin=.03,l1se=.07;let lam=lmin;slider(ctrl,"λ",0,.4,.005,lam,v=>{lam=v;draw();});
 const b1=h("button",{class:"btn",type:"button"},"Jump to lambda.min");const b2=h("button",{class:"btn",type:"button"},"Jump to lambda.1se");ctrl.appendChild(b1);ctrl.appendChild(b2);
 const sl=$("input",ctrl);b1.onclick=()=>{lam=lmin;sl.value=lam;sl.nextSibling.textContent=lam;draw();};b2.onclick=()=>{lam=l1se;sl.value=lam;sl.nextSibling.textContent=lam;draw();};
 const svg=el("svg",{viewBox:"0 0 600 280"});w.appendChild(svg);const ro=h("div",{class:"readout"});w.appendChild(ro);
 function draw(){svg.innerHTML="";const X=l=>560-l/.4*500,Y=v=>230-(v+.05)/.45*210;el("line",{x1:60,x2:560,y1:Y(0),y2:Y(0),stroke:"#9ca3af"},svg);
  for(let t=0;t<=4;t++){const l=t*.1;el("text",{x:X(l),y:262,"text-anchor":"middle","font-size":"10"},svg,fmt(l));}el("text",{x:310,y:278,"text-anchor":"middle","font-size":"11"},svg,"← Larger λ = stronger penalty (Right → Left: λ decreases)");
  [0,.1,.2,.3,.4].forEach(v=>el("text",{x:54,y:Y(v)+3,"text-anchor":"end","font-size":"10"},svg,fmt(v,1)));
  ols.forEach((b,k)=>{let d="";for(let l=0;l<=.4001;l+=.005)d+=(d?"L":"M")+X(l)+","+Y(soft(b,l));el("path",{d,fill:"none",stroke:cols[k],"stroke-width":2},svg);el("text",{x:X(0)+4,y:Y(b)+3,"font-size":"10",style:"fill:"+cols[k]},svg,names[k]);});
  [[lmin,"min"],[l1se,"1se"]].forEach(([l,t])=>{el("line",{x1:X(l),x2:X(l),y1:15,y2:235,stroke:"#9ca3af","stroke-dasharray":"3 3"},svg);el("text",{x:X(l),y:12,"font-size":"10","text-anchor":"middle"},svg,"λ."+t);});
  el("line",{x1:X(lam),x2:X(lam),y1:15,y2:235,stroke:css("--neg"),"stroke-width":2},svg);
  const act=ols.map((b,k)=>[names[k],soft(b,lam)]).filter(x=>Math.abs(x[1])>1e-9);
  ro.innerHTML=`At λ = <b>${lam}</b>, there are <b>${act.length}</b> non-zero coefficients: ${act.map(([n,v])=>`${n} ${fmt(v,3)}`).join(", ")||" (all zero)"}.<br>Note: Retained coefficients are also shrunk towards zero (compared to λ = 0). lambda.1se is larger than lambda.min, resulting in a sparser, more conservative model.<span class="muted"> (Illustration: Assuming mutually orthogonal predictors, where the LASSO solution coincides exactly with soft-thresholding.)</span>`;}
 draw();w._redraw=draw;};
/* ========== W11 Bootstrapping a Correlation Coefficient ========== */
W_boot=function(w){const ctrl=frame(w,w.dataset.title||"Bootstrap: Simulating 'Re-Running the Study 1,000 Times' from Observed Sample");
 let N=50,rho=.3,seed=3,data=[],boots=[];
 const ns=slider(ctrl,"Sample size N",20,400,10,N,v=>{N=v;gen();});slider(ctrl,"Population correlation ρ",-.8,.8,.1,rho,v=>{rho=v;gen();});
 const b1=h("button",{class:"btn",type:"button"},"Draw 1 bootstrap sample"),b2=h("button",{class:"btn primary",type:"button"},"Run 1,000 times"),b3=h("button",{class:"btn",type:"button"},"New sample");ctrl.append(b1,b2,b3);
 const step=h("div",{class:"readout",style:"font-family:var(--mono);font-size:.8rem;max-height:90px;overflow:auto"});w.appendChild(step);const svg=el("svg",{});w.appendChild(svg);const ro=h("div",{class:"readout"});w.appendChild(ro);
 const r=rng(99);function gen(){const rr=rng(seed);data=[];for(let i=0;i<N;i++){const x=rr.norm();data.push([x,rho*x+Math.sqrt(1-rho*rho)*rr.norm()]);}boots=[];step.textContent="Initial sample generated. Click 'Draw 1 bootstrap sample' to see sampling with replacement in action.";draw();}
 const rOf=idx=>corr(idx.map(i=>data[i][0]),idx.map(i=>data[i][1]));
 function one(){const idx=Array.from({length:N},()=>Math.floor(r()*N));boots.push(rOf(idx));return idx;}
 b1.onclick=()=>{const idx=one();const cnt={};idx.forEach(i=>cnt[i]=(cnt[i]||0)+1);const dup=Object.values(cnt).filter(c=>c>1).length,miss=N-Object.keys(cnt).length;
  step.innerHTML=`Sampled case IDs: ${idx.slice(0,40).map(i=>i+1).join(", ")}${N>40?" …":""}<br>→ ${dup} cases sampled more than once, ${miss} cases (~${fmt(100*miss/N,0)}%) not sampled this time. This bootstrap r* = ${fmt(boots[boots.length-1],3)}`;draw();};
 b2.onclick=()=>{for(let k=0;k<1000;k++)one();step.textContent=`Cumulative bootstrap iterations: ${boots.length}.`;draw();};b3.onclick=()=>{seed++;gen();};
 function draw(){const r0=rOf(data.map((_,i)=>i));const z=Math.atanh(r0),se=1/Math.sqrt(N-3),lo=Math.tanh(z-1.96*se),hi=Math.tanh(z+1.96*se);
  if(boots.length<2){svg.innerHTML="";svg.setAttribute("viewBox","0 0 520 60");el("text",{x:260,y:34,"text-anchor":"middle","font-size":"13"},svg,"(No bootstrap results yet)");ro.innerHTML=`Sample correlation r = <b>${fmt(r0,3)}</b>; cor.test() 95% CI (Fisher z) = [<b>${fmt(lo)}</b>, <b>${fmt(hi)}</b>]`;return;}
  const bl=quant(boots,.025),bh=quant(boots,.975);histogram(svg,boots,{lo:-1,hi:1,bins:50,marks:[[r0,css("--ink"),"Sample r"],[bl,css("--neg"),"2.5%"],[bh,css("--neg"),"97.5%"]]});
  ro.innerHTML=`Sample r = <b>${fmt(r0,3)}</b>; bootstrap iterations B = <b>${boots.length}</b>; bootstrap SE ≈ <b>${fmt(Math.sqrt(boots.reduce((s,v)=>s+(v-boots.reduce((a,b)=>a+b,0)/boots.length)**2,0)/(boots.length-1)),3)}</b><br>Percentile 95% interval = [<b>${fmt(bl)}</b>, <b>${fmt(bh)}</b>] | Fisher z interval = [<b>${fmt(lo)}</b>, <b>${fmt(hi)}</b>] → The two are usually very close. Try reducing N: The interval widens substantially.`;}
 gen();w._redraw=draw;};
/* ========== W12 Bootstrap Intervals of Regularized Edge Weights ========== */
W_edgeci=function(w){/* Population target taken from data/true_B_population.csv */const ctrl=frame(w,w.dataset.title||"Bootstrap Intervals for CLPN Edge Weights (Simulated): Why Many Intervals Stick at Zero");
 const E=[["dep3→dep4", 0.169], ["lone2→lone4", 0.142], ["dep1→dep5", 0.126], ["lone3→dep1", 0.118], ["lone1→dep2", 0.102], ["lone4→dep5", 0.083], ["dep4→lone2", -0.083], ["dep2→lone3", 0.082], ["lone1→lone3", 0.072], ["lone3→lone1", 0.071], ["lone1→lone2", 0.07], ["lone2→lone3", 0.068], ["lone2→lone1", 0.068], ["lone4→lone2", 0.066], ["lone3→lone2", 0.065], ["lone4→lone3", 0.064], ["lone3→dep5", -0.001], ["dep2→lone4", 0.001], ["lone3→dep2", 0.0]];
 let N=400,lam=.03,B=500,seed=5;const svg=el("svg",{});
 const sel=h("select",{},'<option>200</option><option selected>400</option><option>800</option><option>2000</option>');const nl=h("label",{},"Sample size N ");nl.appendChild(sel);ctrl.appendChild(nl);sel.onchange=()=>{N=+sel.value;draw();};
 slider(ctrl,"Penalty λ",0,.08,.01,lam,v=>{lam=v;draw();});const rb=h("button",{class:"btn",type:"button"},"Run bootstrap again");rb.onclick=()=>{seed++;draw();};ctrl.appendChild(rb);
 w.appendChild(svg);const ro=h("div",{class:"readout"});w.appendChild(ro);
 function draw(){const r=rng(seed),se=1/Math.sqrt(N);const samp=E.map(([,t])=>t+se*.9*r.norm());const est=samp.map(v=>soft(v,lam));
  const rows=E.map(([nm],k)=>{const bs=[];for(let b=0;b<B;b++)bs.push(soft(samp[k]+se*r.norm(),lam));return{nm,est:est[k],tru:E[k][1],lo:quant(bs,.025),hi:quant(bs,.975),z:bs.filter(v=>v===0).length/B};});
  rows.sort((a,b)=>b.est-a.est);const W=600,H=24+rows.length*18;svg.setAttribute("viewBox",`0 0 ${W} ${H}`);svg.innerHTML="";const X=v=>185+(v+.15)/.4*400;
  [-.1,0,.1,.2].forEach(v=>{el("line",{x1:X(v),x2:X(v),y1:10,y2:H-6,stroke:v===0?"#9ca3af":"#e5e7eb"},svg);el("text",{x:X(v),y:10,"font-size":"9","text-anchor":"middle"},svg,fmt(v,1));});
  rows.forEach((o,i)=>{const y=24+i*18;el("text",{x:8,y:y+4,"font-size":"11"},svg,o.nm);el("text",{x:122,y:y+4,"font-size":"9",style:"fill:#6b7280"},svg,`0: ${fmt(100*o.z,0)}%`);
   el("line",{x1:X(o.lo),x2:X(o.hi)+(o.lo===o.hi?1:0),y1:y,y2:y,stroke:css("--accent"),"stroke-width":5,"stroke-opacity":.35,"stroke-linecap":"round"},svg);
   el("circle",{cx:X(o.est),cy:y,r:4,fill:css("--neg")},svg);el("circle",{cx:X(o.tru),cy:y,r:3,fill:"none",stroke:"#10b981","stroke-width":1.5},svg);});
  const inc0=rows.filter(o=>o.lo<=0&&o.hi>=0).length;
  ro.innerHTML=`Red dot = sample estimate, blue bar = bootstrap 2.5%–97.5% interval, green circle = population target (known only in simulations). "0: %" = proportion of bootstrap samples where LASSO shrunk the edge to 0.<br>Currently, <b>${inc0}</b> / ${rows.length} edges have intervals containing 0. When λ > 0, one boundary of many intervals is stuck exactly at 0, and the entire interval is biased toward 0—this is why bootstrap intervals of regularized estimates <b>cannot be treated as strict 95% confidence intervals</b>, but rather as descriptions of estimation precision / sampling variability. Increasing N narrows the intervals and stabilizes edge rankings.`;}
 draw();w._redraw=draw;};
/* ========== W13 Case-Dropping Bootstrap and CS-Coefficient ========== */
W_cs=function(w){const ctrl=frame(w,w.dataset.title||"Case-Dropping Bootstrap and CS-Coefficient (Simulated)");
 let N=500,spread=.06,seed=1;const svg=el("svg",{viewBox:"0 0 600 260"});
 const sel=h("select",{},'<option>150</option><option>300</option><option selected>500</option><option>1000</option><option>3000</option>');const nl=h("label",{},"Sample size N ");nl.appendChild(sel);ctrl.appendChild(nl);sel.onchange=()=>{N=+sel.value;draw();};
 slider(ctrl,"True EI spread across nodes",.01,.15,.01,spread,v=>{spread=v;draw();});const rb=h("button",{class:"btn",type:"button"},"Re-simulate");rb.onclick=()=>{seed++;draw();};ctrl.appendChild(rb);
 w.appendChild(svg);const ro=h("div",{class:"readout"});w.appendChild(ro);
 function draw(){const r=rng(seed),p=9;const tru=Array.from({length:p},(_,i)=>spread*(i-4)/4);const noiseSD=n=>.9/Math.sqrt(n);
  const full=tru.map(t=>t+noiseSD(N)*r.norm());const drops=[.05,.1,.2,.3,.4,.5,.6,.7,.75,.8,.85,.9,.95];const res=[];let cs=0;
  drops.forEach(d=>{const n=Math.round(N*(1-d));const cors=[];for(let b=0;b<200;b++){// Subsample estimates share information with full-sample estimate: approximated via conditional variance
    const extra=Math.sqrt(Math.max(0,noiseSD(n)**2-noiseSD(N)**2));cors.push(corr(full.map(v=>v+extra*r.norm()),full));}
   const prop=cors.filter(c=>c>=.7).length/cors.length;res.push({d,prop,m:quant(cors,.5),lo:quant(cors,.025),hi:quant(cors,.975)});if(prop>=.95)cs=d;});
  svg.innerHTML="";const X=d=>50+d*540,Y=v=>230-(v+.2)/1.2*210;
  [0,.25,.5,.7,1].forEach(v=>{el("line",{x1:50,x2:590,y1:Y(v),y2:Y(v),stroke:v===.7?css("--neg"):"#e5e7eb","stroke-dasharray":v===.7?"4 3":""},svg);el("text",{x:44,y:Y(v)+3,"font-size":"10","text-anchor":"end"},svg,fmt(v,1));});
  el("text",{x:592,y:Y(.7)-4,"font-size":"10","text-anchor":"end",style:"fill:"+css("--neg")},svg,"r = 0.7");
  drops.forEach(d=>el("text",{x:X(d),y:248,"font-size":"9","text-anchor":"middle"},svg,Math.round(d*100)+"%"));el("text",{x:320,y:259,"font-size":"10","text-anchor":"middle"},svg,"Proportion of sample dropped");
  let dPath="",lo="",hi="";res.forEach((o,i)=>{dPath+=(i?"L":"M")+X(o.d)+","+Y(o.m);});
  el("path",{d:res.map((o,i)=>(i?"L":"M")+X(o.d)+","+Y(o.hi)).join("")+res.slice().reverse().map(o=>"L"+X(o.d)+","+Y(o.lo)).join("")+"Z",fill:css("--accent"),opacity:.15},svg);
  el("path",{d:dPath,fill:"none",stroke:css("--accent"),"stroke-width":2.5},svg);res.forEach(o=>el("circle",{cx:X(o.d),cy:Y(o.m),r:3.5,fill:o.prop>=.95?"#10b981":"#9ca3af"},svg));
  if(cs>0)el("line",{x1:X(cs),x2:X(cs),y1:15,y2:232,stroke:"#10b981","stroke-width":2},svg);
  const verdict=cs>=.5?"≥ 0.5: Centrality stability is strong; rankings can be interpreted with confidence.":cs>=.25?"0.25–0.5: Barely acceptable; interpret rankings with caution.":"< 0.25: Unstable; centrality rankings should not be interpreted.";
  ro.innerHTML=`CS-coefficient (cor = 0.7, 95%) = <b>${fmt(cs)}</b>. ${verdict}<br>Solid curve = median correlation between subsample and full-sample centrality, shaded band = 2.5%–97.5%; green points indicate drop proportions where ≥ 95% of subsample correlations are ≥ 0.7.<span class="muted"> (Pedagogical simulation: Subsample estimates modeled with noise ∝ 1/√n; for empirical analysis use bootnet with type = "case".)</span>`;}
 draw();w._redraw=draw;};
/* ========== W14 Checklist (Locally Saved) ========== */
W_checklist=function(w){const key="clpn-ck-"+(w.dataset.key||"x");let st={};try{st=JSON.parse(localStorage.getItem(key))||{};}catch(e){}
 const items=JSON.parse($("script[type='application/json']",w).textContent);const title=w.dataset.title||"Checklist";w.innerHTML="";w.appendChild(h("div",{class:"wt"},title));
 const bar=h("div",{class:"bar"},"<i></i>"),cnt=h("div",{class:"score"});w.append(cnt,bar);const box=h("div",{class:"checklist"});w.appendChild(box);let n=0;
 items.forEach(it=>{if(typeof it==="string"&&it.startsWith("#")){box.appendChild(h("div",{class:"grp"},it.slice(1)));return;}const id="i"+(n++);const lab=h("label",{});const cb=h("input",{type:"checkbox"});cb.checked=!!st[id];
  cb.onchange=()=>{st[id]=cb.checked;try{localStorage.setItem(key,JSON.stringify(st));}catch(e){}upd();};lab.appendChild(cb);lab.appendChild(h("span",{},it));box.appendChild(lab);});
 const tools=h("div",{class:"ctrl"});const ex=h("button",{class:"btn",type:"button"},"Export as text (copy)");const clr=h("button",{class:"btn",type:"button"},"Clear all");tools.append(ex,clr);w.appendChild(tools);const out=h("textarea",{rows:6,style:"display:none"});w.appendChild(out);
 ex.onclick=()=>{out.style.display="block";out.value=$$("label",box).map(l=>(l.querySelector("input").checked?"[x] ":"[ ] ")+l.textContent).join("\n");out.select();try{document.execCommand("copy");}catch(e){}};
 clr.onclick=()=>{st={};try{localStorage.removeItem(key);}catch(e){}$$("input",box).forEach(c=>c.checked=false);upd();};
 function upd(){const all=$$("input",box),d=all.filter(c=>c.checked).length;cnt.textContent=`Completed ${d} / ${all.length} (saved locally in browser)`;bar.firstChild.style.width=(100*d/all.length)+"%";}upd();};
/* ========== W15 Fill-in-the-Blank Template → Generate Text ========== */
W_tpl=function(w){const key="clpn-tpl-"+(w.dataset.key||"x");let st={};try{st=JSON.parse(localStorage.getItem(key))||{};}catch(e){}
 const spec=JSON.parse($("script[type='application/json']",w).textContent);w.innerHTML="";w.classList.add("tpl");w.appendChild(h("div",{class:"wt"},w.dataset.title||"Template"));
 const form=h("div",{});w.appendChild(form);spec.fields.forEach(([k,lab,ph])=>{const f=h("div",{class:"fld"});f.appendChild(h("span",{},lab));const inp=h("input",{type:"text",placeholder:ph||"","data-k":k});inp.value=st[k]||"";
  inp.addEventListener("input",()=>{st[k]=inp.value;try{localStorage.setItem(key,JSON.stringify(st));}catch(e){}render();});f.appendChild(inp);form.appendChild(f);});
 const out=h("div",{class:"outtext"});w.appendChild(out);const tools=h("div",{class:"ctrl"});const cp=h("button",{class:"btn primary",type:"button"},"Copy generated text");const cl=h("button",{class:"btn",type:"button"},"Clear");tools.append(cp,cl);w.appendChild(tools);
 const esc=s=>s.replace(/[&<>]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;"}[c]));
 function render(){out.innerHTML=esc(spec.text).replace(/\{\{(\w+)\}\}/g,(m,k)=>st[k]?esc(st[k]):`<span class="blank">[${esc((spec.fields.find(f=>f[0]===k)||[k,k])[1])}]</span>`);}
 cp.onclick=()=>{const t=out.innerText;(navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(()=>{cp.textContent="Copied";setTimeout(()=>cp.textContent="Copy generated text",1200);}).catch(()=>{cp.textContent="Please select text manually";});};
 cl.onclick=()=>{st={};try{localStorage.removeItem(key);}catch(e){}$$("input",form).forEach(i=>i.value="");render();};render();};
/* ========== W16 Measurement Interval and Cross-Lagged Effects (Continuous-Time Intuition) ========== */
W_lag=function(w){const ctrl=frame(w,w.dataset.title||"Measurement Interval Alters the Magnitude of Cross-Lagged Coefficients");
 let a=.8,c=.15;const svg=el("svg",{viewBox:"0 0 600 240"});slider(ctrl,"Monthly autoregression",.5,.95,.05,a,v=>{a=v;draw();});slider(ctrl,"Monthly Loneliness → Depression",0,.3,.01,c,v=>{c=v;draw();});w.appendChild(svg);const ro=h("div",{class:"readout"});w.appendChild(ro);
 function draw(){// 2D VAR(1): A=[[a,0],[c,a]], cross-lagged effect after Δ months = (A^Δ)[1,0] = Δ * a^(Δ-1) * c
  svg.innerHTML="";const X=t=>50+t/24*520,Y=v=>210-v/.5*190;const vals=[];let mx=0,best=1;for(let t=1;t<=24;t++){const v=t*Math.pow(a,t-1)*c;vals.push(v);if(v>mx){mx=v;best=t;}}
  [0,.1,.2,.3,.4,.5].forEach(v=>{el("line",{x1:50,x2:570,y1:Y(v),y2:Y(v),stroke:"#e5e7eb"},svg);el("text",{x:44,y:Y(v)+3,"font-size":"10","text-anchor":"end"},svg,fmt(v,1));});
  [1,3,6,12,18,24].forEach(t=>el("text",{x:X(t),y:228,"font-size":"10","text-anchor":"middle"},svg,t+" mo"));
  el("path",{d:vals.map((v,i)=>(i?"L":"M")+X(i+1)+","+Y(v)).join(""),fill:"none",stroke:css("--accent"),"stroke-width":2.5},svg);
  [1,6,12].forEach(t=>el("circle",{cx:X(t),cy:Y(vals[t-1]),r:4,fill:css("--neg")},svg));
  ro.innerHTML=`Under the exact same "underlying process", the cross-lagged coefficient measured at a 1-month interval is ≈ <b>${fmt(vals[0])}</b>, at 6 months ≈ <b>${fmt(vals[5])}</b>, and at 12 months ≈ <b>${fmt(vals[11])}</b>; reaching its maximum at approximately <b>${best}</b> months.<br>Therefore, a "small or non-significant cross-lagged effect" may simply result from choosing a suboptimal measurement interval.<span class="muted"> (Illustration: 2D first-order vector autoregression with no feedback from Depression to Loneliness.)</span>`;}
 draw();w._redraw=draw;};
const REG={clpm:W_clpm,bw:W_bw,cause:W_cause,adj:W_adj,pcor:W_pcor,lasso:W_lasso,cent:W_cent,clpn:W_clpn,bmat:W_bmat,path:W_path,boot:W_boot,edgeci:W_edgeci,cs:W_cs,checklist:W_checklist,tpl:W_tpl,lag:W_lag};
var W_clpm,W_bw,W_cause,W_adj,W_pcor,W_lasso,W_cent,W_clpn,W_bmat,W_path,W_boot,W_edgeci,W_cs,W_checklist,W_tpl,W_lag;
function init(){document.addEventListener("themechange",()=>$$(".widget").forEach(w=>w._redraw&&w._redraw()));
 $$(".widget[data-widget]").forEach(w=>{const f=REG[w.dataset.widget];if(!f){w.innerHTML="<p class='muted'>Unknown widget: "+w.dataset.widget+"</p>";return;}try{f(w);}catch(e){console.error("Widget error",w.dataset.widget,e);w.insertAdjacentHTML("beforeend","<p class='warn'>Failed to load interactive widget. Please refresh the page.</p>");}});
}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",init);else init();
})();

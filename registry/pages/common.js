/* MJ Ahmad Registry — shared runtime for pages/{tasks,notes,audits,code}/index.html */
(function(){
'use strict';
const $=(s,r)=>(r||document).querySelector(s);
const E=(t,c,h)=>{const e=document.createElement(t);if(c)e.className=c;if(h!=null)e.innerHTML=h;return e};
const esc=s=>String(s??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const ROOT='../../';
const DATA_FILES={meta:'data/meta.json',tasks:'data/tasks.json',notes:'data/notes.json',audits:'data/audits.json',codes:'data/codes.json'};
const PAGES=[
 {k:'tasks',dir:'tasks',ic:'✅',en:'Tasks',bn:'টাস্ক'},
 {k:'notes',dir:'notes',ic:'📝',en:'Notes',bn:'নোট'},
 {k:'audits',dir:'audits',ic:'🔍',en:'Audits',bn:'অডিট'},
 {k:'codes',dir:'code',ic:'💻',en:'Code',bn:'কোড'}];
const UI={
en:{back:'Command Center',home:'Dashboard',search:'Search — ID, title, tag…',err:'Could not load the data files. Run ./run.sh serve and open http://localhost:8000',empty:'Nothing matches your filters.',all:'All',clear:'Clear filters',history:'History',copy:'Copy',cpd:'Copied ✓',dl:'Download',related:'Related',ln:'lines',sa:'Show all',co:'Collapse',upd:'Updated',link:'link',shown:'shown',of:'of',pinned:'Pinned',other:'Others',
 st:{todo:'To do',doing:'In progress',done:'Done',low:'Low',medium:'Medium',high:'High',urgent:'Urgent',pass:'Pass',warning:'Warning',fail:'Fail'},
 fk:{status:'Status',priority:'Priority',due:'Due',category:'Category',tags:'Tags',created_at:'Created',completed_at:'Completed',result:'Result',target:'Target',auditor:'Auditor',pinned:'Pinned',filename:'File',source:'Source',lines:'Lines',bytes:'Size (bytes)'},
 today:'Due today',tomorrow:'Due tomorrow',daysLeft:'days left',daysLate:'days overdue',overdue:'Overdue',
 tT:'Tasks',tS:'Everything to do, organised by progress, priority and deadline.',tTotal:'Total',tWeek:'Due in 7 days',tProg:'Overall progress',board:'Board',list:'List',pri:'Priority',cat:'Category',sort:'Sort',sDue:'Due date',sPri:'Priority',sNew:'Newest',allPri:'All priorities',allCat:'All categories',noItems:'No tasks',
 nT:'Notes',nS:'Ideas, references and records — pinned notes stay on top.',nTotal:'Notes',nPin:'Pinned',nCats:'Categories',nTags:'Tags',sOld:'Oldest',sTitle:'Title',pinOnly:'Pinned only',
 aT:'Audits',aS:'Checks and their outcomes, with findings at a glance.',aTotal:'Audits',aRate:'Pass rate',target:'Target',allTarget:'All targets',byTarget:'Group by target',noTarget:'No target',
 cT:'Code',cS:'Snippets, scripts and configs ready to copy or download.',cTotal:'Snippets',cLang:'Languages',cLines:'Total lines',cSize:'Total size',byLang:'Group by language',src:'Source',allSrc:'All sources',sId:'ID',sName:'Filename',sLines:'Longest'},
bn:{back:'কমান্ড সেন্টার',home:'ড্যাশবোর্ড',search:'খুঁজুন — আইডি, শিরোনাম, ট্যাগ…',err:'ডাটা ফাইল লোড হয়নি। ./run.sh serve চালিয়ে http://localhost:8000 খুলুন',empty:'ফিল্টারের সাথে মেলে এমন কিছু নেই।',all:'সব',clear:'ফিল্টার মুছুন',history:'ইতিহাস',copy:'কপি',cpd:'কপি হয়েছে ✓',dl:'ডাউনলোড',related:'সম্পর্কিত',ln:'লাইন',sa:'সবটুকু দেখুন',co:'গুটিয়ে নিন',upd:'আপডেট',link:'লিংক',shown:'টি দেখাচ্ছে',of:'/',pinned:'পিন করা',other:'অন্যান্য',
 st:{todo:'করণীয়',doing:'চলমান',done:'সম্পন্ন',low:'নিম্ন',medium:'মাঝারি',high:'উচ্চ',urgent:'জরুরি',pass:'উত্তীর্ণ',warning:'সতর্কতা',fail:'ব্যর্থ'},
 fk:{status:'অবস্থা',priority:'অগ্রাধিকার',due:'শেষ তারিখ',category:'বিভাগ',tags:'ট্যাগ',created_at:'তৈরি',completed_at:'সম্পন্ন হয়েছে',result:'ফলাফল',target:'লক্ষ্য',auditor:'অডিটর',pinned:'পিন করা',filename:'ফাইল',source:'উৎস',lines:'লাইন',bytes:'আকার (বাইট)'},
 today:'আজই শেষ',tomorrow:'কালই শেষ',daysLeft:'দিন বাকি',daysLate:'দিন বিলম্বিত',overdue:'মেয়াদোত্তীর্ণ',
 tT:'টাস্ক',tS:'সব করণীয় — অগ্রগতি, অগ্রাধিকার ও সময়সীমা অনুযায়ী সাজানো।',tTotal:'মোট',tWeek:'৭ দিনের মধ্যে',tProg:'সার্বিক অগ্রগতি',board:'বোর্ড',list:'তালিকা',pri:'অগ্রাধিকার',cat:'বিভাগ',sort:'সাজান',sDue:'শেষ তারিখ',sPri:'অগ্রাধিকার',sNew:'নতুন আগে',allPri:'সব অগ্রাধিকার',allCat:'সব বিভাগ',noItems:'কোনো টাস্ক নেই',
 nT:'নোট',nS:'ধারণা, রেফারেন্স ও রেকর্ড — পিন করা নোট সবার উপরে থাকে।',nTotal:'নোট',nPin:'পিন করা',nCats:'বিভাগ',nTags:'ট্যাগ',sOld:'পুরনো আগে',sTitle:'শিরোনাম',pinOnly:'শুধু পিন করা',
 aT:'অডিট',aS:'যাচাই ও তার ফলাফল — পর্যবেক্ষণ এক নজরে।',aTotal:'অডিট',aRate:'উত্তীর্ণের হার',target:'লক্ষ্য',allTarget:'সব লক্ষ্য',byTarget:'লক্ষ্য অনুযায়ী গ্রুপ',noTarget:'লক্ষ্য নেই',
 cT:'কোড',cS:'কপি বা ডাউনলোডের জন্য প্রস্তুত স্নিপেট, স্ক্রিপ্ট ও কনফিগ।',cTotal:'স্নিপেট',cLang:'ভাষা',cLines:'মোট লাইন',cSize:'মোট আকার',byLang:'ভাষা অনুযায়ী গ্রুপ',src:'উৎস',allSrc:'সব উৎস',sId:'আইডি',sName:'ফাইলের নাম',sLines:'বড় আগে'}};
let D,lang='en',PAGE='',IMPL=null,q='',mId='';
try{const s=localStorage.getItem('mj_lang');if(s==='bn'||s==='en')lang=s}catch(e){}
const T=()=>UI[lang],pick=(en,bn)=>lang==='bn'?(bn||en):(en||bn);
const ttl=i=>pick(i.title,i.title_bn),loc=(i,k)=>pick(i[k],i[k+'_bn']);
const L=()=>lang==='bn'?'bn-BD':'en-GB';
const num=n=>Number(n).toLocaleString(L());
const parse=s=>/^\d{4}-\d\d-\d\d$/.test(s)?new Date(s+'T00:00:00'):new Date(s);
const fmt=s=>s?parse(s).toLocaleString(L(),{dateStyle:'medium',timeStyle:'short'}):'—';
const fmtD=s=>s?parse(s).toLocaleDateString(L(),{dateStyle:'medium'}):'—';
const daysTo=s=>{const n=new Date();n.setHours(0,0,0,0);const d=parse(s);d.setHours(0,0,0,0);return Math.round((d-n)/864e5)};
const overdue=t=>t.status!=='done'&&!!t.due&&daysTo(t.due)<0;
const logo=s=>!s?'':/^(https?:|data:|\/)/.test(s)?s:ROOT+s;
const hay=i=>[i.id,i.title,i.title_bn,i.desc,i.desc_bn,i.body,i.body_bn,i.findings,i.findings_bn,i.target,i.filename,i.content,i.category,i.auditor,(i.tags||[]).join(' ')].join(' ').toLowerCase();
const matchQ=i=>!q||hay(i).includes(q);
const kindOf=id=>{for(const k of ['tasks','notes','audits','codes']){const it=((D&&D[k])||[]).find(x=>x.id===id);if(it)return{k,it}}return null};
const pageHref=k=>{const p=PAGES.find(x=>x.k===k);return k===PAGE?'':ROOT+'pages/'+p.dir+'/index.html'};

function copy(txt,btn){
  const done=()=>{if(!btn)return;if(!btn.dataset.o)btn.dataset.o=btn.textContent;btn.textContent=T().cpd;clearTimeout(btn._t);btn._t=setTimeout(()=>{btn.textContent=btn.dataset.o},1300)};
  const fb=()=>{const a=document.createElement('textarea');a.value=txt;a.style.cssText='position:fixed;opacity:0';document.body.append(a);a.select();try{document.execCommand('copy')}catch(e){}a.remove();done()};
  if(navigator.clipboard&&navigator.clipboard.writeText)navigator.clipboard.writeText(txt).then(done,fb);else fb()}
function download(name,txt){const a=E('a');a.href=URL.createObjectURL(new Blob([txt],{type:'text/plain'}));a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(a.href),500)}

/* ---------- reusable UI pieces ---------- */
const badge=(cls,label)=>`<span class="b ${esc(cls)}">${esc(label)}</span>`;
const stBadge=v=>v?badge(v,T().st[v]||v):'';
const tagsHtml=a=>(a&&a.length)?`<div class="tg">${a.map(x=>`<button type="button" class="tag" data-tag="${esc(x)}">#${esc(x)}</button>`).join('')}</div>`:'';
function cardEl(cls,html,id,onTag){
  const c=E('article','card '+cls,html);c.tabIndex=0;
  c.onclick=()=>showItem(id);
  c.onkeydown=e=>{if(e.key==='Enter'&&e.target===c)showItem(id)};
  if(onTag)c.querySelectorAll('[data-tag]').forEach(b=>b.onclick=e=>{e.stopPropagation();onTag(b.dataset.tag)});
  return c}
function stats(parent,arr){
  const g=E('div','stats');
  arr.forEach(s=>{const b=E(s.fn?'button':'div','stat'+(s.cls?' '+s.cls:'')+(s.on?' on':'')+(s.fn?'':' static'),`<b>${esc(s.n)}</b><span>${esc(s.l)}</span>`);if(s.fn){b.type='button';b.onclick=s.fn}g.append(b)});
  parent.append(g);return g}
function chips(parent,opts,cur,fn){
  const b=E('div','bar');
  opts.forEach(o=>{const c=E('button','chip'+(cur===o.v?' on':''),`${o.dot?`<span class="dot" style="--lc:${esc(o.dot)}"></span>`:''}${esc(o.l)}${o.n!=null?`<small>${esc(o.n)}</small>`:''}`);c.type='button';c.onclick=()=>fn(o.v);b.append(c)});
  parent.append(b);return b}
function select(parent,label,opts,cur,fn){
  const w=E('label','sel',`<span>${esc(label)}</span><select>${opts.map(o=>`<option value="${esc(o.v)}"${o.v===cur?' selected':''}>${esc(o.l)}</option>`).join('')}</select>`);
  w.querySelector('select').onchange=e=>fn(e.target.value);parent.append(w);return w}
function seg(parent,opts,cur,fn){
  const w=E('div','seg');
  opts.forEach(o=>{const b=E('button',o.v===cur?'on':'',esc(o.l));b.type='button';b.onclick=()=>fn(o.v);w.append(b)});
  parent.append(w);return w}
function clearBtn(parent,fn){const b=E('button','chip clr','✕ '+esc(T().clear));b.type='button';b.onclick=fn;parent.append(b);return b}
const empty=(p,m)=>p.append(E('div','empty',esc(m||T().empty)));
const gh=(html,n)=>E('div','gh',`${html}<span class="n">${esc(num(n))}</span>`);
const uniq=a=>[...new Set(a.filter(Boolean))];
const counts=a=>{const m={};a.forEach(x=>{m[x]=(m[x]||0)+1});return m};
const cleanLang=s=>String(s||'').replace(/[^\w-]/g,'');

/* ---------- code card ---------- */
const nodeMap=()=>{const m={};(function w(ns){(ns||[]).forEach(n=>{m[n.id]=n;w(n.children)})})(D.menu);return m};
const crumb=ids=>{const m=nodeMap();return(ids||[]).map(x=>m[x]?pick(m[x].en,m[x].bn):x).join(' › ')};
function codeCard(i,full){
  const t=T(),N=(D.meta&&D.meta.code_preview_lines)||6,ls=String(i.content||'').split('\n');if(ls[ls.length-1]==='')ls.pop();
  let ex=!!full;const c=E('article','cc l-'+cleanLang(i.lang));
  const cr=crumb(i.menu_path);
  c.innerHTML=`<div class="cch"><span class="lg">${esc(i.lang_label||i.lang)}</span><div class="cct"><b>${esc(ttl(i))}</b><small>${esc(loc(i,'desc'))}</small><span class="id">${esc(i.id)} · ${esc(i.filename)} · ${num(ls.length)} ${t.ln}</span>${cr?`<small class="cr">📁 ${esc(cr)}</small>`:''}</div><div class="ca"><button type="button" data-a="c">${t.copy}</button><button type="button" data-a="d" title="${t.dl}">↓</button></div></div><div class="cb"><pre class="gt"></pre><pre class="cd2"><code></code></pre></div><button type="button" class="tg2"></button>`;
  const tg=c.querySelector('.tg2'),cb=c.querySelector('.cb');
  const draw=()=>{const sh=ex?ls:ls.slice(0,N);c.querySelector('.gt').textContent=sh.map((_,k)=>k+1).join('\n');c.querySelector('code').textContent=sh.join('\n');c.classList.toggle('fade',!ex&&ls.length>N);c.classList.toggle('full',ex&&!full);tg.hidden=ls.length<=N;tg.textContent=ex?t.co:`${t.sa} (${num(ls.length)} ${t.ln})`};
  tg.onclick=()=>{ex=!ex;draw()};cb.onclick=()=>{if(!ex&&ls.length>N){ex=true;draw()}};
  c.querySelector('[data-a=c]').onclick=e=>copy(i.content||'',e.currentTarget);
  c.querySelector('[data-a=d]').onclick=()=>download(i.filename||i.id+'.txt',i.content||'');
  draw();return c}

/* ---------- detail drawer ---------- */
function showItem(id){
  const f=kindOf(id);if(!f)return;
  if(f.k!==PAGE){location.href=pageHref(f.k)+'#'+id;return}
  const it=f.it,t=T(),p=$('#mp'),skip=new Set(['history','title','title_bn','id','content','sha256','lang','ext','desc','desc_bn','body','body_bn','findings','findings_bn','menu_path','lang_label','related','status','priority','result','pinned']);
  mId=id;
  const val=(k,v)=>Array.isArray(v)?esc(v.join(', ')):(k.endsWith('_at')||k==='due')?esc(k==='due'?fmtD(v):fmt(v)):esc(v===true?'✔':v);
  const longs=[['desc',t.fk.desc||'']].concat([['body',''],['findings','']]);
  const txt=['desc','body','findings'].map(k=>{const v=loc(it,k);return v?`<div class="txt">${esc(v)}</div>`:''}).join('');
  const bs=[stBadge(it.status),stBadge(it.priority),stBadge(it.result),overdue(it)?badge('fail',t.overdue):'',it.pinned?'<span class="b">📌</span>':'',it.lang_label?`<span class="lg l-${cleanLang(it.lang)}">${esc(it.lang_label)}</span>`:''].join('');
  const rel=(it.related||[]).filter(Boolean);
  const rows=Object.entries(it).filter(([k,v])=>!skip.has(k)&&v!==''&&v!=null&&!(Array.isArray(v)&&!v.length));
  p.innerHTML=`<button class="x" type="button" aria-label="Close">×</button><div class="id">${esc(it.id)}<button class="cp" type="button">${t.copy} ${t.link}</button></div><h2>${esc(ttl(it))}</h2><div class="bs">${bs}</div>${f.k==='codes'?'<div class="cslot"></div>':''}${txt}<dl>${rows.map(([k,v])=>`<dt>${esc(t.fk[k]||k)}</dt><dd>${val(k,v)}</dd>`).join('')}</dl>${rel.length?`<h3>${t.related}</h3><div>${rel.map(x=>`<button type="button" class="lnk" data-id="${esc(x)}">${esc(x)}</button>`).join('')}</div>`:''}${(it.history||[]).length?`<h3>${t.history}</h3><div class="hist">${it.history.map(h=>`<div>${esc(fmt(h.at))} — ${esc(h.event)}${h.note?': '+esc(h.note):''}</div>`).join('')}</div>`:''}`;
  if(f.k==='codes'){p.style.width='min(900px,100%)';p.querySelector('.cslot').replaceWith(codeCard(it,true))}else p.style.width='';
  p.querySelector('.x').onclick=closeItem;
  p.querySelector('.cp').onclick=e=>copy(location.href.split('#')[0]+'#'+id,e.currentTarget);
  p.querySelectorAll('[data-id]').forEach(b=>b.onclick=()=>{if(kindOf(b.dataset.id))showItem(b.dataset.id)});
  $('#modal').classList.add('on');p.scrollTop=0;
  if(location.hash!=='#'+id)history.replaceState(null,'',location.pathname+location.search+'#'+id)}
function closeItem(){$('#modal').classList.remove('on');mId='';history.replaceState(null,'',location.pathname+location.search)}

/* ---------- shell ---------- */
function shell(){
  $('#app').innerHTML=`<header class="top"><a class="back" id="bk" href="${ROOT}index.html?cc=pages">←<span></span></a><img id="hl" alt="Logo"><div class="ttl"><h1 id="ht"></h1><small id="hs"></small></div><input id="q" type="search" aria-label="Search"><div class="lang" id="lang" role="group" aria-label="Language"><button type="button" data-l="en">EN</button><button type="button" data-l="bn">BN</button></div></header><nav class="pn" id="pn" aria-label="Pages"></nav><main id="main"></main><footer id="ft"></footer><div id="modal"><div class="p" id="mp"></div></div>`;
  $('#q').oninput=e=>{q=e.target.value.trim().toLowerCase();rerender()};
  document.querySelectorAll('#lang button').forEach(b=>b.onclick=()=>{lang=b.dataset.l;try{localStorage.setItem('mj_lang',lang)}catch(e){}applyLang()});
  $('#modal').onclick=e=>{if(e.target.id==='modal')closeItem()};
  addEventListener('keydown',e=>{
    const typing=/INPUT|TEXTAREA|SELECT/.test(e.target.tagName||'');
    if(e.key==='Escape')closeItem();
    else if(e.key==='/'&&!typing&&!e.ctrlKey&&!e.metaKey&&!e.altKey){e.preventDefault();$('#q').focus()}});
  addEventListener('hashchange',()=>{if(D&&location.hash.length>1)showItem(decodeURIComponent(location.hash.slice(1)))})}
function drawNav(){
  const t=T();
  $('#pn').innerHTML=`<a class="home" href="${ROOT}index.html">🏠 ${esc(t.home)}</a>`+PAGES.map(p=>`<a href="${ROOT+'pages/'+p.dir+'/index.html'}"${p.k===PAGE?' class="on" aria-current="page"':''}><span>${p.ic}</span>${esc(pick(p.en,p.bn))}<span class="cnt">${num((D[p.k]||[]).length)}</span></a>`).join('')}
function applyLang(){
  const m=D.meta,t=T(),sub=pick(m.subtitle_en,m.subtitle_bn),pg=PAGES.find(p=>p.k===PAGE);
  document.documentElement.lang=lang;document.title=pick(pg.en,pg.bn)+' — '+m.title;
  $('#ht').textContent=m.title;$('#hs').textContent=sub||'';$('#q').placeholder=t.search;
  $('#bk span').textContent=t.back;
  document.querySelectorAll('#lang button').forEach(b=>b.classList.toggle('on',b.dataset.l===lang));
  $('#ft').textContent=`${pick(m.footer_en,m.footer_bn)||''}${m.footer_en||m.footer_bn?' · ':''}v${m.version||''} · ${t.upd} ${fmt(m.updated_at)} · © ${new Date().getFullYear()} ${m.title}`;
  drawNav();rerender();if($('#modal').classList.contains('on')&&mId)showItem(mId)}
function rerender(){const m=$('#main');m.innerHTML='';IMPL.render(m)}

function boot(key,impl){
  PAGE=key;IMPL=impl;
  Promise.all(Object.entries(DATA_FILES).map(([k,u])=>fetch(ROOT+u+'?'+Date.now()).then(r=>{if(!r.ok)throw new Error(u+' '+r.status);return r.json()}).then(j=>[k,j])))
   .then(parts=>{
     const d={};parts.forEach(([k,j])=>{if(k==='meta'){d.meta=j.meta||{};d.menu=j.menu||[]}else d[k]=j[k]||[]});
     D=d;shell();
     const l=logo(D.meta.logo);if(l)$('#hl').src=l;else $('#hl').hidden=true;
     applyLang();
     if(location.hash.length>1)showItem(decodeURIComponent(location.hash.slice(1)))})
   .catch(e=>{$('#app').innerHTML='<div class="empty" style="margin:auto">'+esc(T().err)+'<br><small>'+esc(e)+'</small></div>'})}

window.MJ={$,E,esc,T,pick,loc,ttl,num,fmt,fmtD,daysTo,overdue,matchQ,copy,download,showItem,badge,stBadge,tagsHtml,cardEl,stats,chips,select,seg,clearBtn,empty,gh,uniq,counts,cleanLang,codeCard,rerender,boot,data:()=>D,query:()=>q,lang:()=>lang};
})();

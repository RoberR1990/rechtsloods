/* Meetlaag Rechtsloods (Umami, 15-11-2026). Zonder host en website-id (CONF) doet dit bestand niets.
   Opzet naar Raadzoeker (meet.js), aangepast aan een site met hash-routes in één pagina.
   - rlMeet(naam, data): verstuurt een gebeurtenis; faalt nooit hardop; wachtrij tot de tracker geladen is.
   - Privacy: geen cookies; geen naam of e-mailadres; zoektermen gaan WEL mee (besluit Robert 15-11-2026: zoekgedrag is het
     belangrijkste leersignaal) maar eerst door schoonZoek(): e-mail, lange cijferreeksen en kentekens eruit, max 80 tekens, kleine letters.
     De tekst van het bezwaar-assistent-veld gaat nooit mee (alleen lengte-klasse).
   - Uitzetten: ?meet=uit (blijvend), ?meet=aan, Do Not Track, of localStorage 'umami.disabled'. ?meet=debug: alles naar de console, tracker niet geladen.
   - Gebeurtenissen en hoe je ze leest: docs/meten.md. */
(function(){
'use strict';
const CONF={
 host:'https://stats.rechtsloods.nl', /* Umami op de NAS (Cloudflare Tunnel, alleen /script.js en /api/send publiek) */
 id:'2fde0ca1-25ef-40a9-a407-52decbc5493d', /* website-id uit Umami */
 script:'script.js',
 domeinen:'rechtsloods.nl,www.rechtsloods.nl' /* alleen hier wordt gemeten (localhost en *.pages.dev tellen niet mee) */
};
const LS={get(k){try{return localStorage.getItem(k)}catch(e){return null}},set(k,v){try{localStorage.setItem(k,v)}catch(e){}},del(k){try{localStorage.removeItem(k)}catch(e){}}};
const SS={get(k){try{return sessionStorage.getItem(k)}catch(e){return null}},set(k,v){try{sessionStorage.setItem(k,v);return true}catch(e){return false}},del(k){try{sessionStorage.removeItem(k)}catch(e){}}};

try{const m=new URLSearchParams(location.search).get('meet');
 if(m==='uit'){LS.set('rl-nometen','1');LS.set('umami.disabled','1');LS.del('rl-eerder');LS.del('rl-bezoeker')}
 else if(m==='aan'){LS.del('rl-nometen');LS.del('umami.disabled')}
 else if(m==='debug')LS.set('rl-meetdebug','1');
 else if(m==='nodebug')LS.del('rl-meetdebug')}catch(e){}

const DEBUG=LS.get('rl-meetdebug')==='1';
const DNT=navigator.doNotTrack==='1'||window.doNotTrack==='1';
const UIT=()=>LS.get('rl-nometen')==='1'||!!LS.get('umami.disabled')||DNT;
const CONF_OK=!!(CONF.host&&CONF.id);
const DOMEIN_OK=CONF.domeinen.split(',').includes(location.hostname);
const ACTIEF=CONF_OK&&DOMEIN_OK&&!UIT()&&!DEBUG;
const LOG=[];

/* ---------- hulpfuncties ---------- */
const SLUG=s=>String(s||'').toLowerCase().replace(/[^a-z0-9:._-]/g,'').slice(0,80);
const EMAIL=/[\w.+-]+@[\w-]+(\.[\w-]+)+/g,CIJFERS=/\d{7,}/g;
const KENTEKEN=/\b(?=[a-z0-9-]*\d)(?=[a-z0-9-]*[a-z])[a-z0-9]{1,3}-[a-z0-9]{2,3}-[a-z0-9]{1,3}\b/gi;
function schoon(d){const o={};let n=0;
 for(const k of Object.keys(d||{})){if(n>=12)break;let v=d[k];if(v===undefined||v===null)continue;
  if(typeof v==='number'){if(!isFinite(v))continue;v=Math.round(v*100)/100}
  else if(typeof v!=='boolean'){v=String(v).replace(/\s+/g,' ').trim().replace(EMAIL,'[e-mail]').replace(CIJFERS,'[nr]').slice(0,100);if(!v)continue}
  o[k.slice(0,30)]=v;n++}
 return o}
function schoonZoek(t){return String(t||'').toLowerCase().replace(/\s+/g,' ').trim().replace(EMAIL,'[e-mail]').replace(KENTEKEN,'[kenteken]').replace(CIJFERS,'[nr]').slice(0,80)}
const ONTHASH=h=>{try{return typeof unhashE==='function'?unhashE(h):h}catch(e){return h}};
const klasse=(n,g)=>{for(const [m,l] of g)if(n<m)return l;return g[g.length-1][1]};

/* ---------- virtueel pad: wat Umami als 'pagina' ziet ---------- */
const VASTE=['start','snel','zoeken','zoekalles','rotterdam','domein','weetjes','mist','borden','mijn','maand','check','volgen','over','lab','roadmap','assistent','stand'];
function pad(hash){
 const h=String(hash||'').replace(/^#/,'')||'start';
 if(VASTE.includes(h))return '/'+(h==='start'?'':h);
 let m;
 if((m=h.match(/^uitspraak-(.+)$/)))return '/uitspraak/'+String(ONTHASH(m[1])).replace(/[^A-Za-z0-9:._-]/g,'').slice(0,60);
 if((m=h.match(/^stand-(.+)$/)))return '/stand/'+SLUG(m[1]);
 if((m=h.match(/^sub-(.+)$/)))return '/onderwerp/'+SLUG(m[1]);
 if((m=h.match(/^onderwerp-(.+)$/)))return '/onderwerp/'+SLUG(m[1]);
 if((m=h.match(/^trends-(.+)$/)))return '/trends/'+SLUG(m[1]);
 if((m=h.match(/^over-(.+)$/)))return '/over/'+SLUG(m[1]);
 if(/^(mijn|maand|check)-/.test(h))return '/gedeeld'; /* gedeelde profiel-links bevatten keuzes van een persoon: nooit in het pad */
 return '/overig';
}
const soortPad=p=>p==='/'?'start':(p.split('/')[1]||'start');
const padNu=()=>pad(location.hash);
function domein(){try{return JSON.parse(LS.get('jr-domein')||'null')||'parkeren'}catch(e){return LS.get('jr-domein')||'parkeren'}}
function rol(){try{return JSON.parse(LS.get('jr-rol')||'""')||''}catch(e){return ''}}
const SCH=[]; /* wachtrij */
let KLAAR=false;
function verstuur(naam,data){
 if(DEBUG){try{console.info('[meet]',naam,JSON.stringify(data))}catch(e){}LOG.push([naam,data]);return}
 if(!KLAAR){if(SCH.length<80)SCH.push([naam,data]);return}
 try{if(window.umami&&typeof window.umami.track==='function'){if(Object.keys(data).length)window.umami.track(naam,data);else window.umami.track(naam)}}catch(e){}
}
function rlMeet(naam,data){
 try{if(!(ACTIEF||DEBUG)||UIT()||typeof naam!=='string'||!naam)return;
  const d=Object.assign({domein:domein()},data||{});
  verstuur(naam.slice(0,50),schoon(d))}catch(e){}
}
window.rlMeet=rlMeet;
Object.assign(rlMeet,{actief:ACTIEF,log:LOG,pad,schoonZoek,uitgezet:UIT,
 uit(){LS.set('rl-nometen','1');LS.set('umami.disabled','1');LS.del('rl-eerder');LS.del('rl-bezoeker')},
 aan(){LS.del('rl-nometen');LS.del('umami.disabled')}});

/* wat er de deur uitgaat: pad zonder hash/query, eigen referrer = vorige virtuele pagina */
let VORIGE='';
window.rlMeetVoorVerzenden=function(type,payload){
 try{if(!payload||typeof payload!=='object')return payload;
  payload.url=padNu();payload.title=padNu();
  if(VORIGE)payload.referrer=location.origin+VORIGE;
  else if(payload.referrer){try{const u=new URL(payload.referrer);if(u.hostname===location.hostname)payload.referrer=''}catch(e){payload.referrer=''}}
 }catch(e){}
 return payload};

/* ---------- verblijfstijd per pagina: actieve seconden (tabblad zichtbaar), verstuurd bij verlaten ---------- */
let T0=0,ACT=0,ZICHT=!document.hidden,P_NU='';
function tikStop(){if(T0&&ZICHT)ACT+=Date.now()-T0;T0=0}
function tikStart(){if(!T0&&ZICHT)T0=Date.now()}
function verblijfSluit(reden){
 tikStop();const s=Math.round(ACT/1000);
 if(P_NU&&s>=1)rlMeet('verblijf',{pagina:soortPad(P_NU),actief_s:Math.min(s,3600),klasse:klasse(s,[[5,'<5s'],[15,'5-15s'],[30,'15-30s'],[60,'30-60s'],[180,'1-3m'],[600,'3-10m'],[1e9,'>10m']]),reden});
 ACT=0}
document.addEventListener('visibilitychange',()=>{if(document.hidden){tikStop();ZICHT=false;if(P_NU)verblijfSluit('verborgen'),tikStart()}else{ZICHT=true;tikStart()}});
addEventListener('pagehide',()=>verblijfSluit('weg'));

/* ---------- paginaweergave (hash-routes) ---------- */
let SCR=new Set(),SCR_T=0;
function weergave(eerste){
 const p=padNu();if(p===P_NU&&!eerste)return;
 if(P_NU){verblijfSluit('volgende');VORIGE=P_NU}
 P_NU=p;ACT=0;T0=0;ZICHT=!document.hidden;tikStart();SCR=new Set();
 const extra=()=>{if(p.startsWith('/uitspraak/')){rlMeet('uitspraak_open',{ecli:p.slice(11),van:soortPad(VORIGE||'/')});
   setTimeout(()=>{if(/niet in de set/i.test((document.querySelector('#view h1')||{}).textContent||''))rlMeet('uitspraak_onbekend',{ecli:p.slice(11)})},300)}};
 if(DEBUG){try{console.info('[meet] pageview',p)}catch(e){}LOG.push(['pageview',p]);sessieStart();extra();return}
 if(!ACTIEF||!KLAAR)return;
 try{window.umami.track(x=>Object.assign({},x,{url:p,title:p}))}catch(e){}
 sessieStart();extra()}

/* ---------- sessie_start: één keer per tabblad ---------- */
const AI_H=/(^|\.)(chatgpt\.com|openai\.com|perplexity\.ai|claude\.ai|copilot\.microsoft\.com|gemini\.google\.com)$/;
const BRON_H=[['teams',/(^|\.)(teams\.microsoft\.com|teams\.live\.com)$/],['mail',/(^|\.)(outlook\.live\.com|outlook\.office\.com|outlook\.office365\.com|mail\.google\.com)$/],
 ['zoekmachine',/(^|\.)(google\.[a-z.]+|bing\.com|duckduckgo\.com|ecosia\.org|startpage\.com|qwant\.com|yahoo\.com)$/],
 ['social',/(^|\.)(linkedin\.com|lnkd\.in|facebook\.com|instagram\.com|t\.co|x\.com|twitter\.com|bsky\.app|reddit\.com|whatsapp\.com|wa\.me)$/],
 ['rechtspraak',/(^|\.)(rechtspraak\.nl)$/],['overheid',/(^|\.)(rotterdam\.nl|overheid\.nl|vng\.nl)$/]];
function bronVan(){
 const q=new URLSearchParams(location.search),src=SLUG(q.get('utm_source')),med=SLUG(q.get('utm_medium')),cam=SLUG(q.get('utm_campaign'));
 let host='';try{host=document.referrer?new URL(document.referrer).hostname.replace(/^www\./,''):''}catch(e){}
 if(host===location.hostname)host='';
 let bron='direct';
 if(AI_H.test(host)||/^(chatgpt|openai|perplexity|claude|copilot|gemini)/.test(src))bron='ai';
 else if(src==='deel')bron='deel';
 else if(/^(mail|email|nieuwsbrief|newsletter)$/.test(src)||/^(mail|email|nieuwsbrief)$/.test(med))bron='mail';
 else if(/^(linkedin|facebook|instagram|twitter|bluesky|whatsapp|reddit|social)/.test(src)||src==='x')bron='social';
 else if(src==='flyer'||src==='qr')bron='print';
 else if(src)bron='campagne';
 else for(const [b,rx] of BRON_H)if(host&&rx.test(host)){bron=b;break}
 if(bron==='direct'&&host)bron='overig';
 return {bron,campagne:cam||undefined,verwijzer:host&&bron!=='direct'?host.slice(0,60):undefined}; /* host van de verwijzende site (geen pad) is bedrijfsinformatie en geen persoonsgegeven */
}
function sessieStart(){
 try{if(UIT()||SS.get('rl-sessie'))return;if(!SS.set('rl-sessie','1'))return;
  const b=bronVan(),n=new Date(),dag=n.getFullYear()+'-'+String(n.getMonth()+1).padStart(2,'0')+'-'+String(n.getDate()).padStart(2,'0'),eerder=LS.get('rl-eerder');
  let terug=false;if(/^\d{4}-\d\d-\d\d$/.test(eerder||''))terug=eerder<dag;else LS.set('rl-eerder',dag);
  const landing=padNu();
  const d={bron:b.bron,terug,landing:soortPad(landing),apparaat:innerWidth<=640?'mobiel':innerWidth<=1024?'tablet':'desktop',taal:(navigator.language||'').slice(0,5)};
  if(b.campagne)d.campagne=b.campagne;if(b.verwijzer)d.verwijzer=b.verwijzer;
  const ro=rol();if(ro)d.rol=ro;
  rlMeet('sessie_start',d);
  try{if(ACTIEF&&window.umami&&typeof window.umami.identify==='function')window.umami.identify({bron:d.bron,terug:d.terug,apparaat:d.apparaat,domein:domein()})}catch(e){}
 }catch(e){}}
/* geen bezoekersnummer meer (privacy); oude waarde opruimen */
try{localStorage.removeItem('rl-bezoeker')}catch(e){}

/* ---------- zoeken ---------- */
const ZOEK_FORMS={hz:'start',grootzoek:'start_groot',az:'alle_vakken',zoekform2:'vak'};
let LAATSTE_Z='';
function aantalResultaten(){
 const r=document.querySelector('#view .resinfo b');if(r){const n=parseInt(r.textContent.replace(/\D/g,''),10);return isNaN(n)?null:n}
 const a=document.querySelector('#az-uit');if(a){if(/Even zoeken/i.test(a.textContent||''))return null;const k=a.querySelectorAll('.kaart').length;return k}
 return null}
function zoekMeet(formId){
 const inp=document.querySelector('#'+formId+' input[type=search],#'+formId+' input[type=text],#'+formId+' input:not([type])');
 const t=schoonZoek(inp?inp.value:'');if(!t)return;
 const poging=Math.min((+SS.get('rl-zoek')||0)+1,999);SS.set('rl-zoek',String(poging));
 const herf=!!LAATSTE_Z&&LAATSTE_Z!==t&&(t.includes(LAATSTE_Z)||LAATSTE_Z.includes(t));LAATSTE_Z=t;
 const woorden=t.split(' ').length;
 setTimeout(()=>{const n=aantalResultaten();
  rlMeet('zoek',{term:t,woorden,plek:ZOEK_FORMS[formId],poging,herformulering:herf,resultaten:n===null?undefined:n,leeg:n===0||undefined});
  if(n===0)rlMeet('zoek_leeg',{term:t,plek:ZOEK_FORMS[formId]})},1400)}
document.addEventListener('submit',e=>{try{const f=e.target&&e.target.id;if(f in ZOEK_FORMS)zoekMeet(f)}catch(x){}},true);
/* filters op de zoekpagina: alleen select/checkbox (vaste waarden), nooit vrije tekst */
document.addEventListener('change',e=>{try{const t=e.target;if(!t||!t.closest||!t.closest('#view'))return;
 if(t.tagName==='SELECT'||t.type==='checkbox'||t.type==='radio'){const id=SLUG(t.id||t.name||'').slice(0,30);if(!id)return;
  rlMeet('filter',{veld:id,waarde:t.type==='checkbox'?t.checked:SLUG(t.value).slice(0,40),pagina:soortPad(P_NU)})}}catch(x){}},true);

/* ---------- klikken (delegatie; ids en klassen van de site) ---------- */
const ID_ACTIE={ /* knop-id -> [gebeurtenis, data] */
 'k-bron':['kopieer',{wat:'bronvermelding'}],'k-link':['kopieer',{wat:'link_uitspraak'}],'k-jurist':['kopieer',{wat:'tekst_voor_jurist'}],'k-klant':['kopieer',{wat:'klantuitleg'}],
 'k-pagina':['kopieer',{wat:'link_pagina'}],'k-brief':['kopieer',{wat:'beslisbrief'}],'k-raad':['kopieer',{wat:'raadsantwoord'}],'k-toets':['kopieer',{wat:'toetslijst'}],
 'k-verweer':['kopieer',{wat:'verweer'}],'k-jurist2':['kopieer',{wat:'jurist_onderwerp'}],'k-fout':['fout_melden',{stap:'open'}],
 'k-volg':['volg',{waar:'onderwerp'}],'k-volg2':['volg',{waar:'onderwerp_lijst'}],'bz-go':['bezwaar_check',{}],'bz-vb':['bezwaar_voorbeeld',{}],
 'deel':['deel',{stap:'open'}],'deel-k':['deel',{stap:'kopieer'}],'deel-t':['deel',{stap:'bericht'}],'instknop':['weergave_menu',{}],'k-meer':['meer_uitspraken',{}],'k-meer5':['meer_uitspraken',{}],'z-meer':['meer_resultaten',{}],
 'alle-recent':['alle_recente',{}],'f-wis':['filters_wissen',{}],'ook-alles':['zoek_alle_vakken',{}]};
const KLIK=[
 ['[data-volg]',el=>['volg',{waar:'knop'}]],
 ['[data-trend]',el=>['trend_open',{onderwerp:SLUG(el.dataset.trend)}]],
 ['[data-sub]',el=>['stand_open',{sub:SLUG(el.dataset.sub)}]],
 ['[data-proef]',el=>['proef',{stuk:SLUG(el.dataset.proef)}]],
 ['[data-kopz]',()=>['kopieer',{wat:'bezwaargrond'}]],
 ['[data-toc]',()=>['inhoud_klik',{pagina:soortPad(P_NU)}]],
 ['.kaart[data-e],[data-ecli],[data-ae]',el=>['kaart_klik',{van:soortPad(P_NU),positie:positie(el)}]],
 ['a[href^="mailto:"]',()=>['contact',{kanaal:'mail',pagina:soortPad(P_NU)}]],
 ['a[href]',el=>{let u;try{u=new URL(el.href,location.href)}catch(e){return null}
  if(!/^https?:$/.test(u.protocol)||u.hostname===location.hostname)return null;
  const h=u.hostname.replace(/^www\./,'');
  if(/(^|\.)rechtspraak\.nl$/.test(h)){const m=(u.search.match(/id=(ECLI[^&]+)/i)||[])[1];return ['uitgaand',{doel:'rechtspraak.nl',ecli:m?decodeURIComponent(m).slice(0,40):undefined,pagina:soortPad(P_NU)}]}
  if(/(^|\.)wetten\.overheid\.nl$|(^|\.)officielebekendmakingen\.nl$|(^|\.)overheid\.nl$/.test(h))return ['uitgaand',{doel:'overheid',pagina:soortPad(P_NU)}];
  return ['uitgaand',{doel:h.slice(0,50),pagina:soortPad(P_NU)}]}]
];
function positie(el){try{const l=el.closest('ul,ol,.lijst');if(!l)return undefined;const k=[...l.children].indexOf(el.closest('li,.kaart')||el);return k>=0?k+1:undefined}catch(e){return undefined}}
document.addEventListener('click',e=>{try{const t=e.target&&e.target.closest?e.target:null;if(!t)return;
 const b=t.closest('[id]');
 const ids=[];let n=t;while(n&&n!==document.body&&ids.length<6){if(n.id)ids.push(n.id);n=n.parentElement}
 for(const id of ids)if(ID_ACTIE[id]){const [g,d]=ID_ACTIE[id];rlMeet(g,Object.assign({pagina:soortPad(P_NU)},d));break}
 const af=new Set();
 for(const [sel,fn] of KLIK){const el=t.closest(sel);if(!el)continue;
  if(sel==='a[href]'&&af.size)continue;
  const r=fn(el);if(r){af.add(r[0]);rlMeet(r[0],r[1])}}
}catch(x){}},true);

/* volgen: de stand na de klik (aan of uit) uit localStorage lezen */
document.addEventListener('click',e=>{try{if(e.target.closest&&e.target.closest('#k-volg,[data-volg]'))setTimeout(()=>{let aan;try{aan=Object.values(JSON.parse(LS.get('jr-volg')||'{}')).filter(Boolean).length}catch(x){}
 rlMeet('volg_stand',{aantal_gevolgd:aan})},120)}catch(x){}},true);

/* ---------- scrolldiepte per paginaweergave ---------- */
function scrollMeet(){try{const de=document.documentElement,h=Math.max(de.scrollHeight,document.body?document.body.scrollHeight:0)-(innerHeight||de.clientHeight||0);if(!(h>200))return;
 const pct=Math.min(100,Math.round(((pageYOffset||de.scrollTop||0)/h)*100));
 for(const d of [25,50,75,100])if(pct>=d&&!SCR.has(d)){SCR.add(d);rlMeet('scroll',{pagina:soortPad(P_NU),diepte:d})}}catch(e){}}
addEventListener('scroll',()=>{if(SCR_T)return;SCR_T=setTimeout(()=>{SCR_T=0;scrollMeet()},200)},{passive:true});

/* ---------- gedragssignalen ---------- */
addEventListener('keydown',e=>{try{if((e.ctrlKey||e.metaKey)&&!e.shiftKey&&!e.altKey&&String(e.key).toLowerCase()==='d')rlMeet('bladwijzer',{pagina:soortPad(P_NU)});
 if((e.ctrlKey||e.metaKey)&&String(e.key).toLowerCase()==='p')rlMeet('print',{pagina:soortPad(P_NU)})}catch(x){}},true);
addEventListener('beforeprint',()=>rlMeet('print',{pagina:soortPad(P_NU)}));
addEventListener('appinstalled',()=>rlMeet('app_installed',{}));
document.addEventListener('copy',()=>{try{const s=String(getSelection()||'');if(s.length>=15)rlMeet('tekst_gekopieerd',{pagina:soortPad(P_NU),lengte:klasse(s.length,[[100,'<100'],[500,'100-500'],[1e9,'>500']])})}catch(x){}},true);

/* ---------- wrappers om bestaande functies (alleen als ze bestaan; falen nooit) ---------- */
function wikkel(naam,fn){try{const o=window[naam];if(typeof o!=='function')return;window[naam]=function(){try{fn.apply(null,arguments)}catch(e){}return o.apply(this,arguments)}}catch(e){}}
function wikkelNa(){
 wikkel('domKies',(slug)=>rlMeet('domein_gekozen',{keuze:SLUG(slug)}));
 wikkel('rolKies',(k)=>rlMeet('rol_gekozen',{rol:SLUG(k)}));
 wikkel('interesse',(k)=>rlMeet('interesse_vak',{vak:SLUG(k)}));
 try{const o=window.profBewaar;if(typeof o==='function')window.profBewaar=function(){const r=o.apply(this,arguments);try{const g=window.PROF&&PROF.gemeente;if(g)rlMeet('profiel',{gemeente:String(g).slice(0,40)})}catch(e){}return r}}catch(e){}
}

/* ---------- uitlegfilm (15-11-2026): start, helft, einde; media-events bubbelen niet, dus capture ---------- */
const FILM={};
document.addEventListener('play',e=>{try{const v=e.target;if(!(v instanceof HTMLVideoElement)||FILM.start)return;FILM.start=1;rlMeet('video_start',{pagina:soortPad(P_NU||padNu()),formaat:v.dataset.formaat||'breed',ondertitels:[...(v.textTracks||[])].some(t=>t.mode==='showing')?'aan':'uit'})}catch(x){}},true);
document.addEventListener('timeupdate',e=>{try{const v=e.target;if(!(v instanceof HTMLVideoElement)||FILM.helft||!v.duration)return;if(v.currentTime/v.duration>=0.5){FILM.helft=1;rlMeet('video_50',{})}}catch(x){}},true);
document.addEventListener('ended',e=>{try{const v=e.target;if(!(v instanceof HTMLVideoElement)||FILM.einde)return;FILM.einde=1;rlMeet('video_complete',{})}catch(x){}},true);

/* ---------- fouten ---------- */
let FJ=0;const basis=f=>{const m=String(f||'').split(/[?#]/)[0].match(/([\w.-]{1,40}\.(?:js|mjs|html|json))$/);return m?m[1]:''};
function foutJs(soort,bestand,regel){if(FJ>=3)return;FJ++;const o={pagina:soortPad(P_NU||padNu()),soort};if(bestand)o.bestand=bestand;if(regel>0)o.regel=regel;rlMeet('fout_js',o)}
addEventListener('error',e=>{try{if(e&&e.filename){let u;try{u=new URL(e.filename,location.href)}catch(x){return}if(u.hostname!==location.hostname)return}foutJs('error',basis(e&&e.filename),e&&e.lineno|0)}catch(x){}});
addEventListener('unhandledrejection',e=>{try{foutJs('promise','',0)}catch(x){}});
let AF=0;
try{const echt=window.fetch;if(typeof echt==='function'&&(ACTIEF||DEBUG)){window.fetch=function(inp){const r=echt.apply(this,arguments);
 try{r.then(res=>{if(res&&(res.status>=400)&&AF<3){const u=new URL(typeof inp==='string'?inp:(inp&&inp.url)||String(inp),location.href);if(u.hostname===location.hostname){AF++;rlMeet('data_fout',{bestand:basis(u.pathname),status:res.status})}}},err=>{if(AF<3&&!(err&&err.name==='AbortError')){AF++;rlMeet('data_fout',{status:'net'})}})}catch(e){}return r}}}catch(e){}
/* laden van het datapakket traag? meet de tijd tot de eerste inhoud (Umami performance meet LCP; dit is de app-eigen tijd) */
addEventListener('load',()=>{try{setTimeout(()=>{const v=document.querySelector('#view');if(v&&/laden/i.test(v.textContent||'')&&v.textContent.length<60)rlMeet('laden_traag',{na_s:Math.round(performance.now()/1000)})},8000)}catch(e){}});


/* ---------- privacyregel in de voet en keuze 'niet meetellen' ---------- */
function privacy(){try{const li=document.getElementById('meetpriv'),kn=document.getElementById('meetknop');if(!li||!kn||!CONF_OK)return;
 const t=()=>UIT()?'Weer meetellen':'Mijn bezoeken niet meetellen';li.hidden=false;
 if(DNT){kn.remove();li.insertAdjacentText('beforeend',' Je browser vraagt om niet gevolgd te worden; dat respecteren we.');return}
 kn.textContent=t();kn.onclick=()=>{if(UIT())rlMeet.aan();else rlMeet.uit();kn.textContent=t()}}catch(e){}}

/* ---------- tracker laden ---------- */
function laad(){
 const s=document.createElement('script');s.defer=true;s.src=CONF.host.replace(/\/+$/,'')+'/'+CONF.script;
 const d=s.dataset;d.websiteId=CONF.id;d.autoTrack='false';d.autoPageview='false';d.domains=CONF.domeinen;d.doNotTrack='true';d.excludeSearch='true';d.excludeHash='true';d.performance='true';d.beforeSend='rlMeetVoorVerzenden';
 s.onload=()=>{KLAAR=true;weergave(true);while(SCH.length){const [n,x]=SCH.shift();verstuur(n,x)}};
 s.onerror=()=>{SCH.length=0};
 document.head.appendChild(s)}
function start(){wikkelNa();privacy();addEventListener('hashchange',()=>weergave(false));if(ACTIEF)laad();else if(DEBUG){KLAAR=true;weergave(true)}}
if(document.readyState==='complete')start();else addEventListener('load',start);
})();

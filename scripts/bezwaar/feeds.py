"""Haal Atom-feeds (ecli, titel, inhoudsindicatie) op voor bezwaar-beroep: RvS, CRvB, CBb, Rb Rotterdam, 2016-2026.
Gebruik: python3 -I scripts/bezwaar/feeds.py <uitvoermap>  (idempotent: bestaande jaarbestanden overslaan)"""
import sys,os,json,re,time,html,subprocess,urllib.parse
from concurrent.futures import ThreadPoolExecutor
OUT=sys.argv[1];os.makedirs(OUT,exist_ok=True)
INST={'rvs':'Raad_van_State','crvb':'Centrale_Raad_van_Beroep','cbb':'College_van_Beroep_voor_het_bedrijfsleven','rbrot':'Rechtbank_Rotterdam'}
B='https://data.rechtspraak.nl/uitspraken/zoeken'
def get(u):
    for i in range(5):
        r=subprocess.run(['curl','-s','-m','120',u],capture_output=True)
        if r.returncode==0 and b'<feed' in r.stdout: return r.stdout.decode('utf-8-sig')
        time.sleep(2+i*3)
    raise RuntimeError(u)
def job(a):
    k,y=a;f=f'{OUT}/{k}{y}.json'
    if os.path.exists(f): return k,y,-1
    rows=[];frm=0
    while True:
        q=[('creator','http://standaarden.overheid.nl/owms/terms/'+INST[k]),('date',f'{y}-01-01'),('date',f'{y}-12-31'),('max','1000'),('from',str(frm)),('return','DOC')]
        if k=='rbrot': q.append(('subject','http://psi.rechtspraak.nl/rechtsgebied#bestuursrecht'))
        x=get(B+'?'+urllib.parse.urlencode(q))
        es=re.findall(r'<entry>(.*?)</entry>',x,re.S)
        for e in es:
            g=lambda t:html.unescape((re.search(rf'<{t}[^>]*>(.*?)</{t}>',e,re.S) or [0,''])[1])
            t=g('title');rows.append({'ecli':g('id'),'title':t,'summary':g('summary')})
        if len(es)<1000: break
        frm+=1000
    json.dump(rows,open(f,'w'),ensure_ascii=False);return k,y,len(rows)
with ThreadPoolExecutor(6) as ex:
    for r in ex.map(job,[(k,y) for k in INST for y in range(2016,2027)]): print(*r,flush=True)

"""Parse XML van een domein: python3 dom_parse.py <slug>  -> data/dom/<slug>/uitspraken.json (+ gz in data/raw/dom_<slug>.json.gz)
Voegt toe: rubrieken, prio (1 hoog/hof, 2 Rotterdam partij, 3 rest), rotterdam (bool)."""
import json,os,sys,re,gzip
sys.path.insert(0,'/home/claude/scripts')
import parse as P
s=sys.argv[1];D=f'/home/claude/data/dom/{s}';X=f'/home/claude/data/xml_dom/{s}'
K={r['ecli']:r for r in json.load(open(f'{D}/kandidaten.json'))}
P.K={e:{'summary':r['summary'],'onderwerp':None,'extra':[]} for e,r in K.items()}
ROT=re.compile(r'(gemeente|burgemeester van|college van burgemeester en wethouders van|heffingsambtenaar van de gemeente|gemeentebelastingen) rotterdam|\brotterdam\b.{0,40}(verweerder|appellant|verweerster)',re.I)
out=[];err=0
for f in sorted(os.listdir(X)):
    e=f[:-4].replace('_',':')
    if e not in K or os.path.getsize(f'{X}/{f}')<500: continue
    try: u=P.parse(f'{X}/{f}')
    except Exception: err+=1;continue
    k=K[e];u['onderwerp']=None;u['rubrieken']=k['rubrieken']
    kop=' '.join(a['t'] for a in u['alineas'][:25])+' '+(u.get('inhoud') or '')
    u['rotterdam']=bool(ROT.search(kop)) or (u.get('gemeente') or '').strip().lower()=='rotterdam'
    u['prio']=1 if k['prio_instantie']==1 else (2 if u['rotterdam'] else 3)
    out.append(u)
json.dump(out,open(f'{D}/uitspraken.json','w'),ensure_ascii=False)
with gzip.open(f'/home/claude/data/raw/dom_{s}.json.gz','wt') as g: json.dump(out,g,ensure_ascii=False)
import collections
print(s,len(out),'geparsed,',err,'fouten | prio',dict(collections.Counter(u['prio'] for u in out)),'| gem. tekens',sum(u['tekens'] for u in out)//max(len(out),1))

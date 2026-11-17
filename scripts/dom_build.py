"""Bouwt site/data/domeinen/<slug>/ volgens docs/datacontract.md.
Gebruik: python3 dom_build.py <slug> [--geen-embed]
- meta.json (zelfde sleutels als parkeren), tekst0..N.json (<20 MB) + tekstindex.json
- verrijkt.json: per uitspraak laag 1 (labels) samengevoegd met laag 2 (schema v3) waar aanwezig, plus scriptvelden
  (wetsartikelen_regex, feitcodes, cluster, dubbel_van). Laag-2-citaten worden opnieuw gecontroleerd; foute zinnen vallen weg.
- taxonomie.json, argumenten.json, config.json (kopie), en status in site/data/domeinen/index.json."""
import json,os,re,sys,collections,hashlib,unicodedata
s=sys.argv[1];D='/home/claude/data';C=f'{D}/dom/{s}';OUT=f'/home/claude/site/data/domeinen/{s}';os.makedirs(OUT,exist_ok=True)
U=json.load(open(f'{C}/uitspraken.json'));cfg=json.load(open(f'{C}/config.json'))
seen=set();U=[u for u in U if not (u['ecli'] in seen or seen.add(u['ecli']))]
def norm(x): x=unicodedata.normalize('NFKC',x or '');x=re.sub(r'[‘’‚`´]',"'",x);x=re.sub(r'[“”„]','"',x);return re.sub(r'\s+',' ',x).strip().lower()
WET=r'(Wet WOZ|Wet waardering onroerende zaken|Gemeentewet|Opiumwet|Wet Bibob|Awb|Algemene wet bestuursrecht|AVG|Wahv|Wet BPM(?: 1992)?|RVV 1990|WVW 1994|Wegenverkeerswet 1994|UAVG|Uitvoeringswet AVG|Wpg|Wet politiegegevens|Woo|Wob|AWR|Algemene wet inzake rijksbelastingen|Wet BRP|VWEU|Wet MRB 1994|Politiewet 2012|APV|Wetboek van Strafvordering|Sv|Wetboek van Strafrecht|Sr)'
RX=re.compile(r'art(?:ikel|\.)\s*(\d+[a-z]?(?::\d+[a-z]?)?)(?:[,\s]+(?:lid\s*\d+|eerste|tweede|derde|vierde|vijfde)(?:\s*lid)?)?(?:[,\s]+(?:aanhef en )?onder\s+[a-z0-9]+)?,?\s+(?:van\s+)?(?:de\s+|het\s+)?'+WET)
FC=re.compile(r'feitcode[^A-Z0-9]{0,15}([A-Z]{1,2}\s?\d{2,3}[a-z]?)')
L1={}
if os.path.isdir(f'{D}/uit_l1/{s}'):
    for f in sorted(os.listdir(f'{D}/uit_l1/{s}')):
        try:
            for o in json.load(open(f'{D}/uit_l1/{s}/{f}')): L1[o.get('ecli')]=o
        except Exception: pass
stat=collections.Counter()
def v3(u):
    p=f'{D}/uit_v3/{s}/'+u['ecli'].replace(':','_')+'.json'
    if not os.path.exists(p): return None
    try:o=json.load(open(p))
    except Exception: return None
    src={a['id']:norm(a['t']) for a in u['alineas']}
    def ok(it):
        if not it or not it.get('citaat'): return False
        b=it.get('bron') or [];c=norm(it['citaat'])
        if b and b[0] in src and c in src[b[0]]: stat['cit_ok']+=1;return True
        for k in src:
            if c and c in src[k]: it['bron']=[k]+[x for x in b if x!=k];stat['cit_herst']+=1;return True
        stat['cit_weg']+=1;return False
    if o.get('relevant') is False: return o
    if o.get('kern') and not ok(o['kern']): o['kern']=None
    if o.get('gevolg_betrokkene') and not ok(o['gevolg_betrokkene']): o['gevolg_betrokkene']=None
    o['samenvatting']=[x for x in o.get('samenvatting') or [] if ok(x)]
    o['actie_gemeente']=[x for x in o.get('actie_gemeente') or [] if ok(x)]
    if o.get('rechtsregel') and not ok(o['rechtsregel']): o['rechtsregel']=None
    for g in o.get('bezwaargronden') or []:
        if g.get('waarom') and not ok(g['waarom']): g['waarom']=None
        if g.get('bruikbare_zin') and not ok(g['bruikbare_zin']): g['bruikbare_zin']=None
    return o
# clusters: (bijna) gelijke inhoudsindicaties
def ckey(u): return hashlib.md5(re.sub(r'[\d\W]+',' ',(u.get('inhoud') or '').lower())[:220].encode()).hexdigest()[:10]
cc=collections.Counter(ckey(u) for u in U if len(u.get('inhoud') or '')>40)
zn=collections.defaultdict(list)
for u in sorted(U,key=lambda u:u['datum']): zn[(u['instantie'],u.get('zaaknr'))].append(u['ecli'])
ver=[]
for u in U:
    full=' '.join(a['t'] for a in u['alineas'])
    wa=collections.Counter(f"art. {m.group(1)} {m.group(2)}" for m in RX.finditer(full))
    o={'ecli':u['ecli'],'laag':1}
    l1=L1.get(u['ecli'])
    if l1:
        o.update({k:v for k,v in l1.items() if k!='ecli'});stat['l1']+=1
    o2=v3(u)
    if o2:
        o.update(o2);o['laag']=2;stat['l2']+=1
    o['wetsartikelen_regex']=[k for k,_ in wa.most_common(8)]
    fcs=sorted(set(m.group(1).replace(' ','') for m in FC.finditer(full)))
    if fcs: o['feitcodes']=fcs
    k=ckey(u)
    o['cluster']=k if cc.get(k,0)>=3 else None
    z=zn.get((u['instantie'],u.get('zaaknr')),[])
    if u.get('zaaknr') and len(z)>1 and z[0]!=u['ecli']: o.setdefault('dubbel_van',z[0])
    o['prio']=u.get('prio');o['rotterdam']=u.get('rotterdam')
    if not l1 and not o2: stat['geen_ai']+=1
    ver.append(o)
json.dump(ver,open(f'{OUT}/verrijkt.json','w'),ensure_ascii=False,separators=(',',':'))
# meta + similariteit
def niveau(i): return 'Hoogste rechter' if re.search(r'Hoge Raad|Raad van State|Centrale Raad|College van Beroep',i) else 'Hof' if 'Hof' in i or 'hof' in i else 'Rechtbank'
nb=[[] for _ in U]
if '--geen-embed' not in sys.argv:
    try:
        import numpy as np
        from fastembed import TextEmbedding
        m=TextEmbedding('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
        E=np.array(list(m.embed([((u.get('inhoud') or '')+' '+' '.join(a['t'] for a in u['alineas'] if not a.get('kop'))[:1500])[:2000] for u in U])))
        E/=np.linalg.norm(E,axis=1,keepdims=True)
        for i0 in range(0,len(U),1000):
            S=E[i0:i0+1000]@E.T
            for j in range(S.shape[0]): S[j,i0+j]=-1
            for j in range(S.shape[0]): nb[i0+j]=[U[x]['ecli'] for x in np.argsort(-S[j])[:6]]
    except Exception as e: print('embed overgeslagen:',e)
VER={o['ecli']:o for o in ver}
meta=[];tek={}
for i,u in enumerate(U):
    o=VER[u['ecli']]
    rel=[{'ecli':r['ecli'],'richting':'eerder' if r['aanleg']=='eerdereAanleg' else 'later','type':r['type'],'gevolg':r['gevolg']} for r in u['relaties'] if r.get('ecli')]
    meta.append({'e':u['ecli'],'i':u['instantie'],'n':niveau(u['instantie']),'d':u['datum'],'p':u['procedure'],'o':o.get('onderwerp'),'s':o.get('sub'),
        'g':o.get('gemeente') or u.get('gemeente'),'u':o.get('uitkomst'),'h':(u.get('inhoud') or '')[:700],'r':rel,'v':nb[i],'z':u.get('zaaknr'),'t':u['tekens'],
        'x':u.get('rubrieken',[]),'c':0,'st':None,'vv':1 if u['procedure'] in ('Voorlopige voorziening','Kort geding') else 0,'ww':None,'l':o['laag'],'pr':u.get('prio'),'rot':1 if u.get('rotterdam') else 0})
    tek[u['ecli']]=[[a.get('rov'),a['t'],1 if a.get('kop') else 0] for a in u['alineas']]
json.dump(meta,open(f'{OUT}/meta.json','w'),ensure_ascii=False,separators=(',',':'))
tot=sum(len(json.dumps(v,ensure_ascii=False)) for v in tek.values());NP=max(1,-(-tot//(14*2**20)))
for f in os.listdir(OUT):
    if re.match(r'tekst\d+\.json$',f): os.remove(f'{OUT}/{f}')
keys=list(tek)
for k in range(NP): json.dump({e:tek[e] for e in keys[k::NP]},open(f'{OUT}/tekst{k}.json','w'),ensure_ascii=False,separators=(',',':'))
json.dump({e:k for k in range(NP) for e in keys[k::NP]},open(f'{OUT}/tekstindex.json','w'),separators=(',',':'))
for f in ['taxonomie.json','argumenten.json','config.json']: json.dump(json.load(open(f'{C}/{f}')),open(f'{OUT}/{f}','w'),ensure_ascii=False,indent=1)
# index.json
IP='/home/claude/site/data/domeinen/index.json';I=json.load(open(IP)) if os.path.exists(IP) else []
n=len(U);nl1=stat['l1'];nl2=stat['l2']
status='live' if nl1>=0.95*n else 'in-opbouw'
kl={'openbare-orde':'#8E44AD','avg-privacy':'#2C7FB8','verkeersboetes':'#D35400','woz':'#16A085','bpm':'#7F8C8D'}
e={'slug':s,'label':cfg['label'],'pad':f'data/domeinen/{s}/','status':status,'n':n,'kleur':kl.get(s,'#555555'),'laag1':nl1,'laag2':nl2,'concept_taxonomie':True,
   'uitleg':f'{n} uitspraken 2016-2026. Indeling (laag 1) voor {nl1}, volledige samenvatting (laag 2) voor {nl2}: hoogste rechters, hoven en Rotterdam als partij. Onderwerpenindeling is een concept.'}
I=[x for x in I if x['slug']!=s]+[e];json.dump(I,open(IP,'w'),ensure_ascii=False,indent=1)
print(s,'n',n,dict(stat),'tekstdelen',NP,'status',status)

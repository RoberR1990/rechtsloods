# build_verrijkt.py — parkeren: site/data/verrijkt.json
# Per uitspraak: v3 (data/uit_v3/parkeren) als die er is, anders v2 (data/proef/uit).
# Alle citaten worden opnieuw letterlijk gecontroleerd; zinnen zonder geldig citaat vallen weg.
import json,os,re,unicodedata,collections
D='/home/claude/data' if os.path.isdir('/home/claude/data/uit_v3') else 'data'
U={u['ecli']:u for u in json.load(open('data/uitspraken.json'))}
T=json.load(open('data/taxonomie.json'));A=json.load(open('data/argumenten.json'))
def norm(s): s=unicodedata.normalize('NFKC',s or '');s=re.sub(r'[‘’‚`´]',"'",s);s=re.sub(r'[“”„]','"',s);return re.sub(r'\s+',' ',s).strip().lower()
stat=collections.Counter()
def checker(u):
    al=u.get('alineas') or u.get('al') or []
    nsrc={a['id']:norm(a['t']) for a in al}
    def ok(it):
        if not it or not it.get('citaat'): return False
        stat['zinnen']+=1
        b=it.get('bron') or [];c=norm(it['citaat'])
        if b and b[0] in nsrc and c in nsrc[b[0]]: stat['ok']+=1;return True
        for k in nsrc:
            if c and c in nsrc[k]: it['bron']=[k]+[x for x in b if x!=k];stat['herst']+=1;return True
        stat['weg']+=1;return False
    return ok
def v3(o,u):
    ok=checker(u)
    for k in ['kern','gevolg_betrokkene','rechtsregel']:
        if o.get(k) and not ok(o[k]): o[k]=None
    for k in ['samenvatting','actie_gemeente']:
        o[k]=[x for x in o.get(k) or [] if ok(x)]
    for g in o.get('bezwaargronden') or []:
        for k in ['waarom','bruikbare_zin']:
            if g.get(k) and not ok(g[k]): g[k]=None
    if not o['samenvatting']: o['relevant']=False
    return o
def v2(o,u):
    ok=checker(u)
    if o.get('kern') and not ok(o['kern']): o['kern']=None
    for key in ['samenvatting','lessen_voor_gemeente','argumenten']:
        o[key]=[s for s in (o.get(key) or []) if not s.get('citaat') or ok(s)]
    if o.get('rechtsregel') and o['rechtsregel'].get('citaat') and not ok(o['rechtsregel']): o['rechtsregel']=None
    o['argumenten']=[a for a in o['argumenten'] if a.get('arg') in A]
    if not o['samenvatting']: o['relevant']=False
    return o
def laad(p):
    try: return json.load(open(p))
    except Exception: return None
V2={};V3={}
for f in sorted(os.listdir('data/proef/uit')):
    if f.endswith('.json'):
        o=laad('data/proef/uit/'+f)
        if o and o.get('ecli'): V2[o['ecli']]=o
d3=f'{D}/uit_v3/parkeren'
for f in sorted(os.listdir(d3)) if os.path.isdir(d3) else []:
    if f.endswith('.json'):
        o=laad(f'{d3}/{f}')
        if o and o.get('ecli'): V3[o['ecli']]=o
out=[]
for e in sorted(set(V2)|set(V3)):
    u=U.get(e)
    if e in V3:
        o=V3[e];stat['v3']+=1
        if o.get('relevant') and u: o=v3(o,u)
    else:
        o=V2[e];o.setdefault('schema','v2');stat['v2']+=1
        if o.get('relevant') and u: o=v2(o,u)
    if o.get('relevant') and (o.get('onderwerp') not in T or o.get('sub') not in T[o['onderwerp']]['sub']): stat['subfout']+=1
    out.append(o)
json.dump(out,open('site/data/verrijkt.json','w'),ensure_ascii=False,separators=(',',':'))
stat['totaal']=len(out);stat['relevant_eind']=sum(1 for o in out if o.get('relevant'))
print(dict(stat))

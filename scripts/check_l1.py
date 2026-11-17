"""Check laag 1: python3 check_l1.py <slug> [batch-id ...]  (zonder batch: alle)"""
import json,sys,os,re,unicodedata
s=sys.argv[1];D='/home/claude/data';C=f'{D}/dom/{s}'
cfg=json.load(open(f'{C}/config.json'));T=json.load(open(f'{C}/taxonomie.json'));A=json.load(open(f'{C}/argumenten.json'))
I=json.load(open(f'{D}/in_l1/{s}.json'));B={b['id']:b['eclis'] for b in json.load(open(f'{D}/batches/l1_{s}.json'))}
ids=sys.argv[2:] or [f[:-5] for f in os.listdir(f'{D}/uit_l1/{s}') if f.endswith('.json')]
def norm(x): x=unicodedata.normalize('NFKC',x or '');x=re.sub(r'[‘’‚`´]',"'",x);x=re.sub(r'[“”„]','"',x);return re.sub(r'\s+',' ',x).strip().lower()
PV={'beroep','hoger beroep','cassatie','cassatie belang der wet','voorlopige voorziening','kort geding','verzet','anders'}
fout=0;n=0
for b in ids:
    p=f'{D}/uit_l1/{s}/{b}.json'
    if not os.path.exists(p): print(b,'ONTBREEKT');fout+=1;continue
    try: L=json.load(open(p))
    except Exception as e: print(b,'GEEN GELDIGE JSON',e);fout+=1;continue
    got={o.get('ecli'):o for o in L}
    for e in B.get(b,[]):
        if e not in got: print(b,e,'ontbreekt in uitvoer');fout+=1
    for e,o in got.items():
        n+=1;F=[]
        if e not in I: F.append('onbekende ecli')
        if o.get('relevant') is False: 
            if not o.get('reden'): F.append('reden ontbreekt')
        else:
            on=o.get('onderwerp')
            if on not in T: F.append(f'onderwerp {on}')
            else:
                sb=T[on]['sub']
                if o.get('sub')!='overig' and o.get('sub') not in sb: F.append(f'sub {o.get("sub")}')
                elif o.get('kenmerk'):
                    sv=sb.get(o.get('sub'));km=(sv.get('kenmerk') if isinstance(sv,dict) else None) or {}
                    if o['kenmerk'] not in km: F.append(f'kenmerk {o["kenmerk"]}')
            if o.get('zaaktype') not in cfg['zaaktype']: F.append(f'zaaktype {o.get("zaaktype")}')
            pj=o.get('partijen') or {}
            if not isinstance(pj.get('gemeente_is_partij'),bool): F.append('gemeente_is_partij')
            if o.get('procesvorm') not in PV: F.append(f'procesvorm {o.get("procesvorm")}')
            if o.get('uitkomst') not in ('burger wint','wederpartij wint','deels','alleen procedure'): F.append(f'uitkomst {o.get("uitkomst")}')
            ub=o.get('uitkomst_bron') or {};bron=(ub.get('bron') or [None])[0]
            src={a['id']:norm(a['t']) for a in (I.get(e,{}).get('kop',[])+I.get(e,{}).get('beslissing',[]))}
            if src:
                if bron not in src: F.append(f'uitkomst_bron id {bron}')
                elif not ub.get('citaat') or norm(ub['citaat']) not in src[bron]: F.append(f'uitkomst_bron citaat niet letterlijk: {str(ub.get("citaat"))[:40]}')
            for x in o.get('bezwaargronden') or []:
                if x.get('arg')!='overig' and x.get('arg') not in A: F.append(f'arg {x.get("arg")}')
                if x.get('oordeel') not in ('gehonoreerd','verworpen','niet beoordeeld'): F.append(f'oordeel {x.get("oordeel")}')
            if o.get('zekerheid') not in ('hoog','middel','laag'): F.append('zekerheid')
        for x in F: print(b,e,'FOUT',x)
        fout+=len(F)
print('uitspraken',n,'| FOUTEN:',fout)

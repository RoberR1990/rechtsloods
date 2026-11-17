"""Automatische checks schema v3.
Gebruik: python3 check_uit_v3.py <slug> [bestand.json ...]   (zonder bestanden: alles in uit_v3/<slug>)
Optie --stil: alleen totalen. Exit 0 altijd; laatste regel 'FOUTEN: n'."""
import json,sys,os,re,unicodedata
a=[x for x in sys.argv[1:] if not x.startswith('--')];stil='--stil' in sys.argv
s=a[0];D='/home/claude/data';U=f'{D}/uit_v3/{s}';I=f'{D}/in_v3/{s}';C=f'{D}/dom/{s}'
cfg=json.load(open(f'{C}/config.json'));T=json.load(open(f'{C}/taxonomie.json'));A=json.load(open(f'{C}/argumenten.json'))
files=a[1:] or sorted(x for x in os.listdir(U) if x.endswith('.json'))
E=lambda k,v:v in cfg[k]
PV={'beroep','hoger beroep','cassatie','cassatie belang der wet','voorlopige voorziening','kort geding','verzet','bezwaar-advies','anders'}
UK={'burger wint','wederpartij wint','deels','alleen procedure'}
JARGON=re.compile(r'\b(belanghebbende|appellant(e)?|verweerder|verweerster|heffingsambtenaar|betrokkene|eiser(es)?|gedaagde|verzoeker|ter zake|onderhavig|voornoemd)\b',re.I)
ECLI=re.compile(r'^ECLI:[A-Z]{2}:[A-Z0-9]+:\d{4}:[A-Z0-9.]+$')
def norm(x): x=unicodedata.normalize('NFKC',x or '');x=re.sub(r'[‘’‚`´]',"'",x);x=re.sub(r'[“”„]','"',x);return re.sub(r'\s+',' ',x).strip().lower()
def subs(o):
    if o not in T: return None
    return T[o].get('sub') or {}
fout=waar=0;tel={'ok':0,'rel':0,'nrel':0}
for f in files:
    F=[];W=[]
    p=f'{U}/{f}'
    if not os.path.exists(p): print(f,'ONTBREEKT');fout+=1;continue
    try:o=json.load(open(p))
    except Exception as e: print(f,'GEEN GELDIGE JSON',e);fout+=1;continue
    if o.get('relevant') is False:
        tel['nrel']+=1
        if not o.get('reden'): W.append('relevant=false zonder reden')
    else:
        tel['rel']+=1
        try: inp=json.load(open(f'{I}/{f}'))
        except: inp={'alineas':[],'beslissing':''};F.append('invoer ontbreekt')
        src={x['id']:norm(x['t']) for x in inp['alineas']}
        def cit(k,it,verplicht=True):
            if not it:
                if verplicht: F.append(f'{k} ontbreekt')
                return
            b=it.get('bron') or [];c=it.get('citaat') or ''
            if not b or b[0] not in src: F.append(f'{k}: bron-id ontbreekt/onbekend {b}');return
            if not c or norm(c) not in src[b[0]]: F.append(f'{k}: citaat niet letterlijk in alinea {b[0]}: {c[:50]}');return
            n=len(c.split())
            if n<3 or n>35: W.append(f'{k}: citaat {n} woorden')
            if 'zin' in it and JARGON.search(it.get('zin') or ''): W.append(f'{k}: jargon "{JARGON.search(it["zin"]).group(0)}"')
        if o.get('schema')!='v3': F.append('schema!=v3')
        on=o.get('onderwerp');sb=subs(on)
        if sb is None: F.append(f'onbekend onderwerp {on}')
        elif o.get('sub')!='overig' and o.get('sub') not in sb: F.append(f'onbekende sub {on}/{o.get("sub")}')
        elif o.get('kenmerk'):
            sv=sb.get(o.get('sub'));km=(sv.get('kenmerk') if isinstance(sv,dict) else None) or {}
            if o['kenmerk'] not in km: F.append(f'onbekend kenmerk {o["kenmerk"]}')
        if not E('zaaktype',o.get('zaaktype')): F.append(f'zaaktype {o.get("zaaktype")}')
        pj=o.get('partijen') or {}
        if not isinstance(pj.get('gemeente_is_partij'),bool): F.append('partijen.gemeente_is_partij geen bool')
        if o.get('procesvorm') not in PV: F.append(f'procesvorm {o.get("procesvorm")}')
        if not o.get('intro') or not isinstance(o.get('intro'),str): F.append('intro ontbreekt')
        if not o.get('titel'): F.append('titel ontbreekt')
        elif len(o['titel'].split())>12: W.append('titel > 12 woorden')
        cit('kern',o.get('kern'))
        sm=o.get('samenvatting') or []
        if not 3<=len(sm)<=6: F.append(f'samenvatting {len(sm)} zinnen (3-6)')
        for i,x in enumerate(sm): cit(f'sam{i}',x)
        if o.get('uitkomst') not in UK: F.append(f'uitkomst {o.get("uitkomst")}')
        cit('gevolg_betrokkene',o.get('gevolg_betrokkene'))
        st=o.get('steunt')
        if pj.get('gemeente_is_partij') is False and st is not None: F.append('steunt moet null zijn (gemeente geen partij)')
        if pj.get('gemeente_is_partij') is True and st not in ('gemeente','burger','gemengd'): F.append(f'steunt {st}')
        bg=o.get('bezwaargronden') or []
        if not bg and o.get('zaaktype') in cfg.get('bezwaargronden_verplicht_bij',[]): F.append('bezwaargronden leeg bij '+o['zaaktype'])
        for i,x in enumerate(bg):
            if x.get('arg')!='overig' and x.get('arg') not in A: F.append(f'bg{i}: onbekende arg {x.get("arg")}')
            if x.get('oordeel') not in ('gehonoreerd','verworpen','niet beoordeeld'): F.append(f'bg{i}: oordeel {x.get("oordeel")}')
            if not x.get('burger_zegt'): F.append(f'bg{i}: burger_zegt leeg')
            cit(f'bg{i}.waarom',x.get('waarom'),x.get('oordeel')!='niet beoordeeld')
            if x.get('bruikbare_zin'): cit(f'bg{i}.bruikbare_zin',x['bruikbare_zin'],False)
        r=o.get('rechtsregel')
        if r:
            cit('rechtsregel',r)
            if r.get('type') not in ('regel','feitelijk_oordeel'): F.append(f'rechtsregel.type {r.get("type")}')
            if r.get('herkomst') not in ('wet','vaste lijn HR-RvS','oordeel rechter','lokale verordening'): F.append(f'rechtsregel.herkomst {r.get("herkomst")}')
        bw=o.get('bewijs')
        if not isinstance(bw,dict) or bw.get('bewijslast_bij') not in ('burger','wederpartij','niet aan de orde'): F.append('bewijs.bewijslast_bij')
        if not E('toepasselijkheid',o.get('toepasselijkheid')): F.append(f'toepasselijkheid {o.get("toepasselijkheid")}')
        l=o.get('lijn') or {}
        if l.get('soort') not in ('bevestigt','nieuw','wijkt af','onbekend'): F.append(f'lijn.soort {l.get("soort")}')
        for e in l.get('eerdere') or []:
            if not ECLI.match(e or ''): W.append(f'lijn: geen ECLI {e}')
        if not isinstance(o.get('wetsartikelen'),list): F.append('wetsartikelen geen lijst')
        ac=o.get('actie_gemeente')
        if not isinstance(ac,list): F.append('actie_gemeente geen lijst')
        else:
            if not ac and not o.get('reden_leeg_actie'): F.append('actie_gemeente leeg zonder reden_leeg_actie')
            for i,x in enumerate(ac):
                if not E('raakt',x.get('raakt')): F.append(f'actie{i}: raakt {x.get("raakt")}')
                if not x.get('actie'): F.append(f'actie{i}: leeg')
                cit(f'actie{i}',x)
        if not isinstance(o.get('raakt'),list) or any(not E('raakt',x) for x in o.get('raakt') or []): F.append(f'raakt {o.get("raakt")}')
        ku=o.get('klantuitleg') or ''
        if not ku: F.append('klantuitleg ontbreekt')
        elif len(re.findall(r'[.!?](\s|$)',ku))>3: W.append('klantuitleg > 3 zinnen')
        if o.get('gemeente') is None and not o.get('reden_gemeente_leeg'): W.append('gemeente null zonder reden')
        if o.get('zekerheid') not in ('hoog','middel','laag'): F.append(f'zekerheid {o.get("zekerheid")}')
        # uitkomst vs beslissing (alleen eerste aanleg beroep)
        bs=norm(inp.get('beslissing'))
        if o.get('procesvorm')=='beroep' and bs:
            ong='ongegrond' in bs; geg=bool(re.search(r'(?<!on)gegrond',bs))
            if ong and not geg and o.get('uitkomst') in ('burger wint','deels'): W.append('uitkomst burger/deels maar beslissing alleen ongegrond')
            if geg and not ong and o.get('uitkomst')=='wederpartij wint': W.append('uitkomst wederpartij maar beslissing gegrond')
    for x in F: print(f,'FOUT',x)
    if not stil:
        for x in W: print(f,'LET OP',x)
    fout+=len(F);waar+=len(W)
    if not F: tel['ok']+=1
print(f"bestanden {len(files)} | relevant {tel['rel']} | niet relevant {tel['nrel']} | zonder fouten {tel['ok']} | waarschuwingen {waar}")
print('FOUTEN:',fout)

"""Hulp bij stap 2 (taxonomie sociaal-domein).
  python3 -I lab/sociaal_taxonomie.py steekproef <map>   # ±150 koppen + inhoudsindicaties, gestratificeerd per rubriek (buiten de repo, B3)
  python3 -I lab/sociaal_taxonomie.py tel                # grove regex-schatting per subonderwerp (sub_hint in taxonomie.json) -> dunne subs
  python3 -I lab/sociaal_taxonomie.py check              # taxonomie/config/argumenten consistent? laatste regel 'FOUTEN: n'"""
import json, os, re, sys, random, collections
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); D = f'{R}/data/dom/sociaal-domein'
cmd = sys.argv[1]
if cmd == 'steekproef':
    M = sys.argv[2]; os.makedirs(M, exist_ok=True); V = json.load(open(f'{R}/data/feeds/kandidaten_sociaal-domein.json')); random.seed(150)
    L = []
    for rub, n in (('bijstand', 70), ('wmo', 45), ('jeugdwet', 20), ('schuldhulp', 10)):
        L += random.sample([v for v in V if v['rubrieken'][0] == rub and v['summary'].strip() not in ('-', '')], n)
    L += random.sample([v for v in V if v['bron'] == 'civ'], 5)
    json.dump([{'ecli': v['ecli'], 'kop': f"{v['instantie']}, {v['datum']}, {v['zaaknr']}", 'rubriek': v['rubrieken'], 'inhoudsindicatie': v['summary']} for v in L],
              open(f'{M}/taxonomie_steekproef.json', 'w'), ensure_ascii=False, indent=0)
    print(len(L))
elif cmd == 'tel':
    V = json.load(open(f'{R}/data/feeds/kandidaten_sociaal-domein.json')); T = json.load(open(f'{D}/taxonomie.json'))
    H = json.load(open(f'{R}/lab/sociaal_taxonomie_hints.json'))  # grove trefwoorden per sub; alleen voor deze telling
    c = collections.Counter(); geen = 0
    for v in V:
        x = (v['zaaknr'] + ' ' + v['summary']).lower(); hit = False
        for o, t in T.items():
            if o.startswith('_'): continue
            if not set(v['rubrieken']) & set(t.get('rubriek', [])): continue
            for s, sv in t['sub'].items():
                h = H.get(f'{o}/{s}')
                if h and re.search(h, x): c[(o, s)] += 1; hit = True
        geen += not hit
    for o, t in T.items():
        if o.startswith('_'): continue
        for s in t['sub']: print(f'{c[(o, s)]:6d}  {o}/{s}')
    print('zonder hint-treffer', geen, 'van', len(V))
elif cmd == 'check':
    T = json.load(open(f'{D}/taxonomie.json')); C = json.load(open(f'{D}/config.json')); A = json.load(open(f'{D}/argumenten.json')); F = []
    slug = re.compile(r'^[a-z0-9]+(-[a-z0-9]+)*$'); subs = []
    for o, t in T.items():
        if o.startswith('_'): continue
        if not slug.match(o): F.append(f'onderwerp-slug {o}')
        for k in ('label', 'sub', 'concept'):
            if k not in t: F.append(f'{o}: {k} ontbreekt')
        for s, sv in t.get('sub', {}).items():
            subs.append(s)
            if not slug.match(s): F.append(f'sub-slug {s}')
            if not isinstance(sv, dict) or not sv.get('label'): F.append(f'{o}/{s}: label ontbreekt')
            for km in (sv.get('kenmerk') or {}): 
                if not slug.match(km): F.append(f'kenmerk-slug {km}')
    if len(subs) != len(set(subs)): F.append('sub-slugs niet uniek: ' + str([s for s, n in collections.Counter(subs).items() if n > 1]))
    if not 20 <= len(subs) <= 30: F.append(f'{len(subs)} subonderwerpen (verwacht 20-30)')
    for k in ('slug', 'label', 'zaaktype', 'bezwaargronden_verplicht_bij', 'raakt', 'toepasselijkheid', 'rollen', 'klantuitleg_vraag', 'rubrieken', 'uitkomstregels', 'rotterdam_partij'):
        if k not in C: F.append(f'config.{k} ontbreekt')
    if C.get('slug') != 'sociaal-domein': F.append('config.slug')
    for z in C.get('bezwaargronden_verplicht_bij', []):
        if z not in C.get('zaaktype', []): F.append(f'bezwaargronden_verplicht_bij {z} niet in zaaktype')
    for r, o in C.get('rubrieken', {}).items():
        if o not in T: F.append(f'rubriek {r} -> onbekend onderwerp {o}')
    try: re.compile(C.get('rotterdam_partij', ''))
    except re.error as e: F.append(f'rotterdam_partij regex: {e}')
    for k, v in A.items():
        if not slug.match(k) or not isinstance(v, str): F.append(f'argument {k}')
    if 'overig' in A: F.append('argument "overig" hoort niet in argumenten.json')
    for x in F: print('FOUT', x)
    print(f'onderwerpen {sum(1 for o in T if not o.startswith("_"))} | subonderwerpen {len(subs)} | argumenten {len(A)} | zaaktypen {len(C.get("zaaktype", []))}')
    print('FOUTEN:', len(F))

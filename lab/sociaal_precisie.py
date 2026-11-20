"""Precisiemeting afbakening sociaal-domein (stap 1).
  python3 -I lab/sociaal_precisie.py prep  <map>   # steekproef: 100 willekeurig + 60 kernbegrip/civiel + 40 net-niet (uitgesloten)
  python3 -I lab/sociaal_precisie.py score <map>   # leest <map>/oordeel.json (Haiku) en <map>/eigen.json (eigen controle)
De steekproef bevat inhoudsindicaties en blijft dus buiten de repo (<map> = scratchpad), besluit B3."""
import json, os, sys, random, collections
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, f'{R}/scripts')
import sociaal_select as S
cmd, M = sys.argv[1], sys.argv[2]
if cmd == 'prep':
    K = json.load(open(f'{R}/data/feeds/kandidaten_{S.SLUG}.json')); random.seed(20261120)
    a = random.sample(K, 100); ids = {k['ecli'] for k in a}
    b = random.sample([k for k in K if k['reden'] in ('kernbegrip', 'civiel', 'crvb-tekst') and k['ecli'] not in ids], 60)
    uit = []
    for y in S.JAREN:
        for bron in ('best', 'civ'):
            for r in json.load(open(f'{S.F}/{bron}{y}.json')):
                rub, codes, why = S.beoordeel(r, bron)
                if not rub and why not in ('geen-kernbegrip', 'crvb-code-buiten-scope'): uit.append({**S.kop(r), 'summary': r['summary'], 'reden': why})
    c = random.sample(uit, 40)
    rij = lambda k, g: {'ecli': k['ecli'], 'kop': f"{k['ecli']}, {k['instantie']}, {k['datum']}, {k['zaaknr']}", 'inhoudsindicatie': k['summary'], '_groep': g, '_reden': k['reden']}
    L = [rij(k, 'willekeurig') for k in a] + [rij(k, 'kernbegrip') for k in b] + [rij(k, 'net-niet') for k in c]
    os.makedirs(M, exist_ok=True)
    json.dump([{x: v for x, v in r.items() if not x.startswith('_')} for r in L], open(f'{M}/invoer.json', 'w'), ensure_ascii=False, indent=0)
    json.dump({r['ecli']: [r['_groep'], r['_reden']] for r in L}, open(f'{M}/sleutel.json', 'w'), indent=0)
    print('steekproef', len(L), collections.Counter(r['_groep'] for r in L))
else:
    G = json.load(open(f'{M}/sleutel.json')); O = {o['ecli']: o for o in json.load(open(f'{M}/oordeel.json'))}
    E = {o['ecli']: o for o in json.load(open(f'{M}/eigen.json'))} if os.path.exists(f'{M}/eigen.json') else {}
    fout = [e for e in G if e not in O]; print('ontbreekt in oordeel:', len(fout))
    for g in ('willekeurig', 'kernbegrip', 'net-niet'):
        L = [e for e in G if G[e][0] == g and e in O]
        rel = sum(O[e]['relevant'] for e in L); tw = sum(bool(O[e].get('twijfel')) for e in L)
        print(f'{g:12s} n={len(L)} relevant={rel} ({100*rel//max(len(L),1)}%) twijfel={tw}')
        for e in L:
            exp = g != 'net-niet'
            if O[e]['relevant'] != exp: print('   afwijking', e, G[e][1], '|', O[e].get('reden'))
    if E:
        eens = sum(E[e]['relevant'] == O[e]['relevant'] for e in E if e in O)
        print('eigen controle', len(E), 'eens met Haiku', eens)

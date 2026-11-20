"""Stap 1c: steekproef voor precisie (100 uit de definitieve set) en recall-controle (40 uit de afgevallen pool).
  python3 -I lab/woz_precisie.py prep   -> lab/sets/woz_precisie_in.json
  python3 -I lab/woz_precisie.py tel    -> telt lab/sets/woz_precisie_uit.json (agent) + lab/sets/woz_precisie_eigen.json (eigen controle van 15)"""
import json, os, sys, random, re
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, f'{R}/scripts'); os.chdir(R)
D = f'{R}/data/dom/woz-belastingen'; S = f'{R}/lab/sets'
if sys.argv[1] == 'prep':
    import parse as P
    U = {u['ecli']: u for u in json.load(open(f'{D}/uitspraken.json'))}
    A = json.load(open(f'{D}/afbakening.json'))['besluiten']
    rnd = random.Random(20261120)
    inn = rnd.sample(sorted(U), 100)
    uit = rnd.sample(sorted(e for e, v in A.items() if not v['in'] and 'dubbel' not in v['reden']), 40)
    def item(u, groep):
        kop = [a['t'] for a in u['alineas'][:30] if len(a['t']) < 300][:12]
        return {'ecli': u['ecli'], 'groep': groep, 'instantie': u['instantie'], 'datum': u['datum'], 'inhoudsindicatie': (u.get('inhoud') or '')[:1500], 'kop': kop}
    L = [item(U[e], 'in') for e in inn] + [item(P.parse(f"{R}/data/xml_dom/woz-belastingen/{e.replace(':','_')}.xml"), 'uit') for e in uit]
    rnd.shuffle(L)
    for i, x in enumerate(L): x['nr'] = i
    json.dump([{k: v for k, v in x.items() if k != 'groep'} for x in L], open(f'{S}/woz_precisie_in.json', 'w'), ensure_ascii=False, indent=0)
    json.dump({x['ecli']: x['groep'] for x in L}, open(f'{S}/woz_precisie_sleutel.json', 'w'), indent=0)
    print('steekproef', len(L))
else:
    K = json.load(open(f'{S}/woz_precisie_sleutel.json'))
    O = {o['ecli']: o for o in json.load(open(f'{S}/woz_precisie_uit.json'))}
    E = json.load(open(f'{S}/woz_precisie_eigen.json')) if os.path.exists(f'{S}/woz_precisie_eigen.json') else {}
    def oordeel(e): return E[e]['relevant'] if e in E else O[e]['relevant']
    inn = [e for e in K if K[e] == 'in']; uit = [e for e in K if K[e] == 'uit']
    tp = sum(1 for e in inn if oordeel(e)); fn = sum(1 for e in uit if oordeel(e))
    eens = sum(1 for e in E if E[e]['relevant'] == O[e]['relevant'])
    print(f'precisie {tp}/{len(inn)} = {100*tp/len(inn):.0f}% | in afgevallen pool toch relevant {fn}/{len(uit)} | eigen controle eens met agent {eens}/{len(E)}')
    for e in inn:
        if not oordeel(e): print('  vals positief:', e, O[e].get('reden'))
    for e in uit:
        if oordeel(e): print('  gemist:', e, O[e].get('reden'))

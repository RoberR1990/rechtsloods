"""Laag-2-batches voor wonen-leefbaarheid: python3 -I lab/wonen_batches_l2.py [grootte=6] [--voorlopig-a]

Leest lab/sets/wonen_l2.json (verwerkingsvolgorde) en voegt bestanden die nog in geen batch staan toe aan
data/batches/v3_wonen-leefbaarheid.json (bestaande batches blijven; idempotent), model 'sonnet'.
--voorlopig-a: schrijft eerst een voorlopige set met alleen prioriteit a (Rotterdam partij of Rotterdamwet), zodat
laag 2 kan starten voordat laag 1 klaar is; uitspraken die laag 1 al 'niet relevant' noemde vallen af.
"""
import json, os, sys, glob
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); S = 'wonen-leefbaarheid'
n = int(next((a for a in sys.argv[1:] if a.isdigit()), 6))
SET = f'{R}/lab/sets/wonen_l2.json'
if '--voorlopig-a' in sys.argv:
    L1 = {}
    for f in sorted(glob.glob(f'{R}/data/uit_l1/{S}/*.json')):
        for o in json.load(open(f)): L1[o['ecli']] = o
    U = json.load(open(f'{R}/data/dom/{S}/uitspraken.json'))
    A = [u for u in U if (u.get('rotterdam') or u.get('rotterdamwet')) and not u.get('dubbel_van')
         and (L1.get(u['ecli']) or {}).get('relevant') is not False]
    A.sort(key=lambda u: u['datum'], reverse=True)
    oud = json.load(open(SET)) if os.path.exists(SET) else []
    al = {x['ecli'] for x in oud}
    oud += [{'bestand': u['ecli'].replace(':', '_') + '.json', 'ecli': u['ecli'], 'prio': 'a',
             'reden': 'Rotterdamwet' if u.get('rotterdamwet') and not u.get('rotterdam') else 'Rotterdam partij'} for u in A if u['ecli'] not in al]
    json.dump(oud, open(SET, 'w'), ensure_ascii=False, indent=0)
sel = json.load(open(SET))
p = f'{R}/data/batches/v3_{S}.json'; B = json.load(open(p)) if os.path.exists(p) else []
al = {f for b in B for f in b['files']}
nieuw = [x['bestand'] for x in sel if x['bestand'] not in al]
for i in range(0, len(nieuw), n):
    B.append({'id': f'v3-{S}-{len(B) + 1:04d}', 'files': nieuw[i:i + n], 'model': 'sonnet'})
os.makedirs(os.path.dirname(p), exist_ok=True); json.dump(B, open(p, 'w'), indent=0)
print('set', len(sel), '| batches', len(B), '| nieuw', len(nieuw))

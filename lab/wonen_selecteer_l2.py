"""Selectie laag 2 voor wonen-leefbaarheid (patroon lab/selecteer_avg_c.py): python3 -I lab/wonen_selecteer_l2.py [max]

Alleen uitspraken die in laag 1 relevant zijn en geen dubbele publicatie (dubbel_van). Volgorde van prioriteit, zodat een
afgebroken run altijd een bruikbare set oplevert:
  a  Rotterdam partij (gemeente uit laag 1 = Rotterdam en gemeente_is_partij, of Rotterdam-regex uit dom_parse) en alle
     Rotterdamwet-uitspraken; nieuwste eerst
  b  hoogste rechters (Raad van State, CRvB, HR), nieuwste eerst
  c  hoven en overige hogere instanties, nieuwste eerst (in dit domein: geen)
  d  dunne subonderwerpen aanvullen tot 20 (nieuwste eerst)
Maximum totaal (standaard 400). Ruimte voor d wordt vooraf gereserveerd; b vult de rest.
Uitvoer: lab/sets/wonen_l2.json  [{bestand, ecli, prio, reden}] in verwerkingsvolgorde + telling.
"""
import json, os, re, sys, glob, collections
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); S = 'wonen-leefbaarheid'
MAX = int(sys.argv[1]) if len(sys.argv) > 1 else 400
U = {u['ecli']: u for u in json.load(open(f'{R}/data/dom/{S}/uitspraken.json'))}
L1 = {}
for f in sorted(glob.glob(f'{R}/data/uit_l1/{S}/*.json')):
    for o in json.load(open(f)): L1[o['ecli']] = o
HOOG = re.compile(r'Hoge Raad|Raad van State|Centrale Raad|College van Beroep')
HOF = re.compile(r'Gerechtshof|Gemeenschappelijk Hof')
def rot(e):
    o = L1[e]; g = (o.get('gemeente') or '').strip().lower(); pj = o.get('partijen') or {}
    w = (pj.get('wederpartij') or '').lower()
    return (g == 'rotterdam' and pj.get('gemeente_is_partij')) or ('rotterdam' in w) or bool(U[e].get('rotterdam'))
kand = [e for e, o in L1.items() if o.get('relevant') is not False and e in U and not U[e].get('dubbel_van')]
nieuw = lambda e: U[e]['datum']
A = sorted([e for e in kand if rot(e) or U[e].get('rotterdamwet')], key=nieuw, reverse=True)
Bh = sorted([e for e in kand if HOOG.search(U[e]['instantie']) and e not in A], key=nieuw, reverse=True)
C = sorted([e for e in kand if HOF.search(U[e]['instantie']) and e not in A], key=nieuw, reverse=True)
sub = lambda e: (L1[e].get('onderwerp'), L1[e].get('sub'))
# reserveer ruimte voor d: per sub tekort tot 20 na a + c + (schatting b = alles wat past)
def tekort(gekozen):
    c = collections.Counter(sub(e) for e in gekozen); alle = collections.Counter(sub(e) for e in kand)
    return {s: min(20, alle[s]) - c[s] for s in alle if s[1] and s[1] != 'overig' and c[s] < min(20, alle[s])}
basis = A + C
ruimte_b = MAX - len(basis)
# iteratief: neem b, bepaal tekort, verklein b tot alles past
for _ in range(20):
    b = Bh[:max(0, ruimte_b)]
    t = tekort(basis + b); nodig = sum(t.values())
    if len(basis) + len(b) + nodig <= MAX or ruimte_b <= 0: break
    ruimte_b -= max(1, len(basis) + len(b) + nodig - MAX)
D_ = []
for s, n in sorted(tekort(basis + b).items(), key=lambda x: str(x[0])):
    rest = sorted([e for e in kand if sub(e) == s and e not in basis and e not in b], key=lambda e: (not HOOG.search(U[e]['instantie']), nieuw(e)), reverse=False)
    rest = sorted(rest, key=lambda e: (0 if HOOG.search(U[e]['instantie']) else 1, -int(U[e]['datum'].replace('-', ''))))
    D_ += rest[:n]
sel = [(e, 'a', 'Rotterdam partij' if rot(e) else 'Rotterdamwet') for e in A] + [(e, 'b', 'hoogste rechter') for e in b] + \
      [(e, 'c', 'hof') for e in C] + [(e, 'd', f'dun subonderwerp {sub(e)[0]}/{sub(e)[1]}') for e in D_]
sel = sel[:MAX] if len(sel) > MAX else sel
out = [{'bestand': e.replace(':', '_') + '.json', 'ecli': e, 'prio': p, 'reden': r} for e, p, r in sel]
os.makedirs(f'{R}/lab/sets', exist_ok=True)
json.dump(out, open(f'{R}/lab/sets/wonen_l2.json', 'w'), ensure_ascii=False, indent=0)
c = collections.Counter(sub(x['ecli']) for x in out)
print('relevant laag 1', len(kand), '| selectie', len(out), dict(collections.Counter(x['prio'] for x in out)))
print('subs < 20 in selectie:', {f'{k[0]}/{k[1]}': v for k, v in c.items() if v < 20})

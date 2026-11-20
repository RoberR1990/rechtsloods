"""Selectie laag 2 subsidies (stap 4; patroon lab/selecteer_avg_c.py). Besluit B17.
  python3 -I lab/selecteer_subsidies_l2.py [--l1 <map>] [--max 450] [--batch 6]
Volgorde = verwerkingsvolgorde, zodat een afgebroken run altijd een bruikbare set oplevert:
  a. Rotterdam partij (config.rotterdam_partij)       max 200: eerst hoogste rechter, dan rechtbank; nieuwste eerst; om en om per subonderwerp
  b. hoogste rechters (CRvB, RvS, HR/PHR), nieuwste eerst  tot totaal 350: om en om per subonderwerp
  c. hoven (alle relevante)                                tot totaal 400
  d. dunne subonderwerpen aanvullen tot 20                 tot totaal --max (450)
Alleen laag-1-relevante uitspraken; massazaken (zelfde inhoudsindicatie) max 2 per cluster.
Uitvoer: lab/sets/subsidies_l2.json (in_v3-bestandsnamen, in volgorde), lab/sets/subsidies_l2_redenen.json, data/batches/v3_subsidies.json
(bestaande batches blijven; alleen nieuwe bestanden erbij). Idempotent."""
import json, os, re, sys, glob, collections, hashlib
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); S = 'subsidies'
arg = lambda k, d: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
L1 = arg('--l1', f'{R}/data/uit_l1/{S}'); MAX = int(arg('--max', 450)); NB = int(arg('--batch', 6))
U = {u['ecli']: u for u in json.load(open(f'{R}/data/dom/{S}/uitspraken.json'))}
T = json.load(open(f'{R}/data/dom/{S}/taxonomie.json'))
lab = {}
for f in sorted(glob.glob(f'{L1}/*.json')):
    for o in json.load(open(f)):
        if isinstance(o, dict) and o.get('ecli') in U: lab[o['ecli']] = o
rel = [e for e, o in lab.items() if o.get('relevant') is not False]
HOOGSTE = re.compile(r'Centrale Raad|Raad van State|Hoge Raad')
hoogste = lambda e: bool(HOOGSTE.search(U[e]['instantie'])) or ':PHR:' in e
hof = lambda e: U[e]['instantie'].startswith('Gerechtshof')
sub = lambda e: (lab[e].get('onderwerp'), lab[e].get('sub'))
nieuw = lambda L: sorted(L, key=lambda e: (U[e]['datum'], e), reverse=True)
clus = lambda e: hashlib.md5(re.sub(r'[\d\W]+', ' ', (U[e].get('inhoud') or '').lower())[:220].encode()).hexdigest()[:10] if len(U[e].get('inhoud') or '') > 40 else e

sel, reden, per, pc = [], {}, collections.Counter(), collections.Counter()
def neem(e, r):
    if e in reden or len(sel) >= MAX or pc[clus(e)] >= 2: return False
    sel.append(e); reden[e] = r; per[sub(e)] += 1; pc[clus(e)] += 1; return True

def om_en_om(L, r, tot):
    """nieuwste eerst, maar om en om per subonderwerp zodat een groot subonderwerp niet alles vult"""
    q = collections.defaultdict(list)
    for e in nieuw(L): q[sub(e)].append(e)
    while len(sel) < tot and any(q.values()):
        for k in sorted(q, key=lambda k: (per[k], str(k))):
            while q[k] and not neem(q[k].pop(0), r): pass
            if len(sel) >= tot: break

rot = [e for e in rel if U[e].get('rotterdam')]
om_en_om([e for e in rot if hoogste(e)], 'a: Rotterdam partij, hoogste rechter', 120)
om_en_om([e for e in rot if not hoogste(e)], 'a: Rotterdam partij, rechtbank of hof', 200)
om_en_om([e for e in rel if hoogste(e)], 'b: hoogste rechter, nieuwste eerst', 350)
for e in nieuw([e for e in rel if hof(e)]):
    if len(sel) >= 400: break
    neem(e, 'c: hof')
subs = [(o, s) for o, t in T.items() if not o.startswith('_') for s in t['sub']]
for k in sorted(subs, key=lambda k: per[k]):
    for e in nieuw([e for e in rel if sub(e) == k]):
        if per[k] >= 20 or len(sel) >= MAX: break
        neem(e, f'd: dun subonderwerp {k[0]}/{k[1]} aangevuld tot 20')

namen = [e.replace(':', '_') + '.json' for e in sel]
os.makedirs(f'{R}/lab/sets', exist_ok=True)
json.dump(namen, open(f'{R}/lab/sets/subsidies_l2.json', 'w'), indent=0)
json.dump({e.replace(':', '_') + '.json': reden[e] for e in sel}, open(f'{R}/lab/sets/subsidies_l2_redenen.json', 'w'), ensure_ascii=False, indent=0)
bp = f'{R}/data/batches/v3_{S}.json'; B = json.load(open(bp)) if os.path.exists(bp) else []
al = {f for b in B for f in b['files']}; rest = [f for f in namen if f not in al]
for i in range(0, len(rest), NB): B.append({'id': f'v3-{S}-{len(B) + 1:04d}', 'files': rest[i:i + NB], 'model': 'sonnet'})
os.makedirs(os.path.dirname(bp), exist_ok=True); json.dump(B, open(bp, 'w'), indent=0)
dun = [f'{o}/{s}:{per[(o, s)]}' for o, s in subs if per[(o, s)] < 20]
print(f'laag-1 relevant {len(rel)} | selectie {len(sel)} |', dict(collections.Counter(r.split(':')[0] for r in reden.values())),
      f'| Rotterdam {sum(1 for e in sel if U[e].get("rotterdam"))} | batches {len(B)} | subonderwerpen < 20: {len(dun)} {dun[:8]}')

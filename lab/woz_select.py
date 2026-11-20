"""Stap 4: selectie voor laag 2 (patroon lab/selecteer_avg_c.py).
Gebruik: python3 -I lab/woz_select.py [max=500] [--schrijf]
Volgorde (een afgebroken run levert altijd een bruikbare set):
  (a) Rotterdam partij (vlag uit dom_parse + heffingsambtenaar/directeur/college ... Rotterdam in de kop, en als laag 1 er is, laag-1-gemeente/wederpartij Rotterdam), nieuwste eerst
  (b) hoogste rechters (Hoge Raad + conclusies AG), nieuwste eerst
  (c) hoven, nieuwste eerst, één per cluster (gelijke inhoudsindicatie) en max. 30 per subonderwerp
  (d) dunne subonderwerpen aanvullen tot 20 laag 2 (nieuwste en hoogste instantie eerst);
      subs van proceskosten-gemachtigden ALTIJD tot 20, ook boven het maximum.
Niet-relevante uitspraken (laag 1 relevant=false) gaan er niet in. Zonder laag 1 telt een uitspraak als relevant.
Uitvoer (--schrijf): data/dom/woz-belastingen/selectie_l2.json [{bestand, ecli, reden, volgorde}] en data/batches/v3_woz-belastingen.json
(batches van 6, bestaande batches blijven; alleen nieuwe bestanden worden toegevoegd)."""
import json, os, re, sys, glob, collections, hashlib
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = 'woz-belastingen'; D = f'{R}/data/dom/{S}'
MAX = int(next((a for a in sys.argv[1:] if a.isdigit()), 500)); BATCH = 6
U = {u['ecli']: u for u in json.load(open(f'{D}/uitspraken.json'))}
L1 = {}
for f in sorted(glob.glob(f'{R}/data/uit_l1/{S}/*.json')):
    try:
        for o in json.load(open(f)): L1[o['ecli']] = o
    except Exception: pass
klaar = {f[:-5].replace('_', ':') for f in os.listdir(f'{R}/data/uit_v3/{S}') if f.endswith('.json')} if os.path.isdir(f'{R}/data/uit_v3/{S}') else set()
def rel(e): return L1.get(e, {}).get('relevant') is not False
ROT = re.compile(r'(heffingsambtenaar|directeur|hoofd|college|belastingen|gemeentebelastingen)[^.;]{0,50}Rotterdam', re.I)
def rot(e):
    u = U[e]
    if not u.get('rotterdam'): return False
    if not (ROT.search(' '.join(a['t'] for a in u['alineas'][:25])) or (u.get('gemeente') or '').lower() == 'rotterdam'): return False
    l = L1.get(e)
    if not l or l.get('relevant') is False: return l is None
    return 'rotterdam' in ((l.get('gemeente') or '') + ' ' + ((l.get('partijen') or {}).get('wederpartij') or '')).lower()
hoog = lambda e: 'Hoge Raad' in U[e]['instantie']
hof = lambda e: 'Gerechtshof' in U[e]['instantie']
nieuw = lambda e: U[e]['datum']
ck = lambda e: hashlib.md5(re.sub(r'[\d\W]+', ' ', (U[e].get('inhoud') or '').lower())[:220].encode()).hexdigest()[:10]
sub = lambda e: (L1.get(e, {}).get('onderwerp'), L1.get(e, {}).get('sub'))
sel = {}; per = collections.Counter()
def neem(e, reden):
    if e in sel or not rel(e): return False
    sel[e] = reden; per[sub(e)] += 1; return True
E = sorted(U, key=nieuw, reverse=True)
for e in E:
    if rot(e): neem(e, 'a: Rotterdam partij')
for e in E:
    if hoog(e): neem(e, 'b: hoogste rechter' + (' (conclusie AG, advies)' if ':PHR:' in e else ''))
# (d)-behoefte vooraf schatten, zodat (c) ruimte laat
tax = json.load(open(f'{D}/taxonomie.json')); SUBS = [(o, s) for o in tax for s in tax[o]['sub']]
beschik = collections.Counter(sub(e) for e in U if e in L1 and rel(e))
def tekort(cnt): return {k: max(0, min(20, beschik[k]) - cnt[k]) for k in SUBS}
nodig_d = sum(v for k, v in tekort(per).items() if k[0] != 'proceskosten-gemachtigden')
ruimte_c = max(0, MAX - len(sel) - nodig_d)
cl = set(ck(e) for e in sel); n_c = 0
for e in E:
    if n_c >= ruimte_c: break
    if hof(e) and e not in sel and ck(e) not in cl and per[sub(e)] < 30 and rel(e):
        if neem(e, 'c: hof'): n_c += 1; cl.add(ck(e))
rang = lambda e: (0 if hoog(e) else 1 if hof(e) else 2, -int(nieuw(e)[:4]))
for (o, s) in SUBS:
    pk = o == 'proceskosten-gemachtigden'
    for e in sorted((e for e in U if sub(e) == (o, s) and e not in sel and rel(e)), key=rang):
        if per[(o, s)] >= 20: break
        if not pk and len(sel) >= MAX: break
        neem(e, f'd: aanvullen {o}/{s}' + (' (proceskosten altijd tot 20)' if pk else ''))
r = collections.Counter(v.split(':')[0] for v in sel.values())
print(f'selectie {len(sel)} | per reden {dict(r)} | laag 1 aanwezig voor {len(L1)} | al laag 2: {len(klaar & set(sel))}')
print('per sub:', {f'{k[0]}/{k[1]}': per[k] for k in SUBS})
if '--schrijf' in sys.argv:
    vo = {'a': 0, 'b': 1, 'c': 2, 'd': 3}
    L = sorted(sel.items(), key=lambda kv: (vo[kv[1][0]], kv[0] not in klaar, nieuw(kv[0])), reverse=False)
    L = sorted(L, key=lambda kv: (vo[kv[1][0]], -int(nieuw(kv[0]).replace('-', ''))))
    out = [{'bestand': e.replace(':', '_') + '.json', 'ecli': e, 'reden': v, 'volgorde': i} for i, (e, v) in enumerate(L)]
    json.dump(out, open(f'{D}/selectie_l2.json', 'w'), ensure_ascii=False, indent=0)
    p = f'{R}/data/batches/v3_{S}.json'; B = json.load(open(p)) if os.path.exists(p) else []
    al = {x for b in B for x in b['files']}
    nw = [x['bestand'] for x in out if x['bestand'] not in al]
    for i in range(0, len(nw), BATCH):
        B.append({'id': f'v3-{S}-{len(B)+1:04d}', 'files': nw[i:i+BATCH], 'model': 'sonnet'})
    json.dump(B, open(p, 'w'), indent=0); print(p, len(B), 'batches;', len(nw), 'nieuw')

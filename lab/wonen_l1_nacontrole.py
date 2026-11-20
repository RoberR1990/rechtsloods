"""Nacontrole laag 1 wonen-leefbaarheid: python3 -I lab/wonen_l1_nacontrole.py [--batches N]

Haiku zet soms ten onrechte 'relevant: false' als het dictum ontbreekt. Dit script zoekt verdachte gevallen:
- relevant:false terwijl de beslissing in de laag-1-invoer ontbreekt of kort is, of
- relevant:false terwijl de inhoudsindicatie een sterk woonbegrip noemt (Huisvestingswet, onttrekking, urgentie, ...).
Uitvoer: lab/wonen/l1_verdacht.json (lijst ECLI's + reden) en met --batches N ook batches voor een herstelronde in
data/batches/l1_wonen-leefbaarheid.json (ids l1-wonen-leefbaarheid-herstel-NN; bestaande batches blijven).
Telt daarnaast: aantallen per uitkomst, zekerheid, relevant; ontbrekende ECLI's.
"""
import json, os, re, sys, collections, glob
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); S = 'wonen-leefbaarheid'
I = json.load(open(f'{R}/data/in_l1/{S}.json'))
out = {}
for f in sorted(glob.glob(f'{R}/data/uit_l1/{S}/*.json')):
    for o in json.load(open(f)): out[o['ecli']] = o  # latere bestanden (herstel) gaan voor
STERK = re.compile(r'huisvestingswet|huisvestingsverordening|huisvestingsvergunning|urgentie|voorrangsverklaring|onttrek|omzettingsvergunning'
                   r'|splitsingsvergunning|woningvorming|woonruimtevoorraad|vakantieverhuur|toeristische verhuur|leegstandwet|goed verhuurderschap'
                   r'|opkoopbescherming|grootstedelijke|rotterdamwet|wbmgp|overbewon|woningwet|bouwbesluit', re.I)
verdacht = []
for e, o in out.items():
    if o.get('relevant') is not False: continue
    d = I.get(e, {}); bes = sum(len(a['t']) for a in d.get('beslissing', []))
    r = []
    if bes < 150: r.append('beslissing ontbreekt of kort')
    if STERK.search(d.get('inhoud') or ''): r.append('sterk woonbegrip in inhoudsindicatie')
    if r: verdacht.append({'ecli': e, 'reden': '; '.join(r), 'l1_reden': o.get('reden')})
json.dump(verdacht, open(f'{R}/lab/wonen/l1_verdacht.json', 'w'), ensure_ascii=False, indent=0)
rel = [o for o in out.values() if o.get('relevant') is not False]
print('laag 1:', len(out), 'van', len(I), '| ontbreekt', len(set(I) - set(out)), '| niet relevant', len(out) - len(rel),
      '| verdacht', len(verdacht))
print('uitkomst', dict(collections.Counter(o.get('uitkomst') for o in rel)))
print('zekerheid', dict(collections.Counter(o.get('zekerheid') for o in rel)))
print('onderwerp', dict(collections.Counter(o.get('onderwerp') for o in rel)))
if '--batches' in sys.argv:
    n = int(sys.argv[sys.argv.index('--batches') + 1]); p = f'{R}/data/batches/l1_{S}.json'; B = json.load(open(p))
    al = {e for b in B if b['id'].startswith(f'l1-{S}-herstel') for e in b['eclis']}
    nieuw = [v['ecli'] for v in verdacht if v['ecli'] not in al]
    k = sum(1 for b in B if b['id'].startswith(f'l1-{S}-herstel'))
    for i in range(0, len(nieuw), n):
        k += 1; B.append({'id': f'l1-{S}-herstel-{k:02d}', 'eclis': nieuw[i:i + n]})
    json.dump(B, open(p, 'w'), indent=0); print('herstelbatches', k, 'nieuw', len(nieuw))

"""Selectie 'c' (besluit Robert 16 nov): welke AVG-uitspraken zonder laag 2 gaan naar laag 2.
Altijd: Rotterdam (RBROT) en thema's (algoritmes-registraties, brp-registratie, fraude-algoritme).
Aanvullen: elk subonderwerp tot 20 laag 2; gemeente-als-partij tot 40 per subonderwerp.
Uitvoer: lab/sets/avg_l2_c.json (in_v3-bestandsnamen) + telling op stdout.
"""
import json, glob, collections, re, os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
recs = []
for f in sorted(glob.glob(f'{R}/data/uit_l1/avg-privacy/*.json')):
    recs += json.load(open(f))
c0 = collections.Counter(); klaar = set()
for f in glob.glob(f'{R}/lab/out/avg-privacy/*.json'):
    d = json.load(open(f)); klaar.add(d['ecli']); c0[(d.get('onderwerp'), d.get('sub'))] += 1
rest = [r for r in recs if r['ecli'] not in klaar and r.get('relevant')]

def gem(r):
    w = (r['partijen'].get('wederpartij') or '').lower()
    return r['partijen'].get('gemeente_is_partij') or bool(re.search(r'college|burgemeester|gemeente|heffingsambtenaar|dagelijks bestuur', w))
rot = lambda r: r['ecli'].split(':')[2] == 'RBROT'
thema = lambda r: r['onderwerp'] == 'algoritmes-registraties' or r['zaaktype'] in ('brp-registratie', 'fraude-algoritme')

sel, per = [], collections.Counter()
for r in sorted(rest, key=lambda r: (not rot(r), not gem(r), r['ecli'][::-1])):  # vaste volgorde
    s = (r['onderwerp'], r['sub']); n = c0[s] + per[s]
    if rot(r) or thema(r) or n < 20 or (gem(r) and n < 40):
        sel.append(r); per[s] += 1
namen = sorted(r['ecli'].replace(':', '_') + '.json' for r in sel)
json.dump(namen, open(f'{R}/lab/sets/avg_l2_c.json', 'w'), indent=0)
print(f'selectie {len(sel)} | gemeente {sum(gem(r) for r in sel)} | Rotterdam {sum(rot(r) for r in sel)} | thema {sum(thema(r) for r in sel)}')

"""Herstel laag-2-invoer voor uitspraken waarvan maak_in_v3.py de beslissing wegknipt (o.a. bekende 'Bijlagen:'-bug).
python3 -I lab/wonen_herstel_in_v3.py   # idempotent
Vergelijkt per uitspraak de beslissing-alinea's uit data/in_l1 met data/in_v3; ontbreken ze allemaal, dan wordt
data/in_v3/wonen-leefbaarheid/<ECLI>.json opnieuw geschreven met ALLE alinea's (zelfde id's, dus bronnen blijven geldig).
scripts/maak_in_v3.py zelf blijft ongewijzigd. Lijst: lab/wonen/in_v3_hersteld.json."""
import json, os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); S = 'wonen-leefbaarheid'
I = json.load(open(f'{R}/data/in_l1/{S}.json'))
U = {u['ecli']: u for u in json.load(open(f'{R}/data/dom/{S}/uitspraken.json'))}
K = ['ecli', 'instantie', 'datum', 'procedure', 'rechtsgebied', 'inhoud', 'gemeente', 'beslissing', 'onderwerp', 'relaties']
L = f'{R}/lab/wonen/in_v3_hersteld.json'
hersteld = json.load(open(L)) if os.path.exists(L) else []
for e, d in I.items():
    p = f'{R}/data/in_v3/{S}/' + e.replace(':', '_') + '.json'
    inp = json.load(open(p)); ids = {a['id'] for a in inp['alineas']}; b = [a['id'] for a in d['beslissing']]
    if b and not any(i in ids for i in b):
        u = U[e]; x = {k: u.get(k) for k in K}
        x['alineas'] = [{'id': a['id'], 'rov': a.get('rov'), 't': a['t']} for a in u['alineas']]
        json.dump(x, open(p, 'w'), ensure_ascii=False); hersteld.append(e) if e not in hersteld else None
json.dump(sorted(hersteld), open(L, 'w'), indent=0)
print('hersteld', len(hersteld), hersteld)

"""Na scripts/dom_build.py en lab/stand_dom.py (stap 8, alleen op de eigen branch): zet de index-regel van sociaal-domein
op 'in-opbouw' met label 'eerste versie' en de FG-markering. dom_build zet status zelf op 'live' bij >= 95% laag 1; dat willen we niet.
  python3 -I lab/sociaal_site_na.py"""
import json, os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); ip = f'{R}/site/data/domeinen/index.json'; L = json.load(open(ip))
for d in L:
    if d['slug'] == 'sociaal-domein':
        d['status'] = 'in-opbouw'; d['versie'] = 'eerste versie'; d['fg_akkoord'] = False; d['kleur'] = '#4B5D8C'
        d['uitleg'] = 'Eerste versie, niet publiceren zonder FG-akkoord. ' + d.get('uitleg', '')
json.dump(L, open(ip, 'w'), ensure_ascii=False, indent=1)
# technische sleutels (_bevroren, _toewijzing) niet in de sitekopie: de site maakt van elke sleutel een onderwerp
tp = f'{R}/site/data/domeinen/sociaal-domein/taxonomie.json'
if os.path.exists(tp):
    T = json.load(open(tp)); json.dump({k: v for k, v in T.items() if not k.startswith('_')}, open(tp, 'w'), ensure_ascii=False, indent=1)
print([(d['slug'], d['status']) for d in L if d['slug'] in ('sociaal', 'sociaal-domein')])

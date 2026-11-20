"""Nacontrole laag 1 subsidies (stap 3). Haiku zet zaken soms ten onrechte op 'niet relevant' als het dictum ontbreekt.
  python3 -I lab/subsidies_l1_nacontrole.py lijst     # niet-relevant met ontbrekend dictum of met CRvB-wetscode in scope -> herzienbatches
  python3 -I lab/subsidies_l1_nacontrole.py tel       # aantallen relevant / niet relevant / zekerheid laag
Herzienbatches komen achteraan in data/batches/l1_subsidies.json (id l1-subsidies-hz-NNN). De Haiku-agent labelt ze
opnieuw met zekerheid 'laag' (lab/subsidies_l1_opdracht.md). Uitvoerbestanden 'hz' sorteren na de gewone en overschrijven die in dom_build."""
import json, os, sys, glob, collections
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); S = 'subsidies'
L = {}
for f in sorted(glob.glob(f'{R}/data/uit_l1/{S}/*.json')):
    for o in json.load(open(f)):
        if isinstance(o, dict) and o.get('ecli'): L[o['ecli']] = o
if sys.argv[1] == 'tel':
    print('laag 1', len(L), '| relevant', sum(o.get('relevant') is not False for o in L.values()),
          '| niet relevant', sum(o.get('relevant') is False for o in L.values()),
          '| zekerheid laag', sum(o.get('zekerheid') == 'laag' for o in L.values()),
          '| uitkomst', dict(collections.Counter(o.get('uitkomst') for o in L.values() if o.get('relevant') is not False)))
    sys.exit()
I = json.load(open(f'{R}/data/in_l1/{S}.json')); K = {k['ecli']: k for k in json.load(open(f'{R}/data/dom/{S}/kandidaten.json'))}
twijfel = [e for e, o in L.items() if o.get('relevant') is False and (not I.get(e, {}).get('beslissing') or K.get(e, {}).get('reden') == 'crvb-code')]
bp = f'{R}/data/batches/l1_{S}.json'; B = json.load(open(bp)); al = {x for b in B if '-hz-' in b['id'] for x in b['eclis']}
nieuw = [e for e in sorted(twijfel) if e not in al]; n0 = sum('-hz-' in b['id'] for b in B)
for i in range(0, len(nieuw), 25): B.append({'id': f'l1-{S}-hz-{n0 + i // 25 + 1:03d}', 'eclis': nieuw[i:i + 25]})
json.dump(B, open(bp, 'w'), indent=0)
print('niet relevant', sum(o.get('relevant') is False for o in L.values()), '| te herzien', len(twijfel), '| nieuwe herzienbatches', -(-len(nieuw) // 25))

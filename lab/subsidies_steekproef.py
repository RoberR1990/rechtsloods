"""Blinde steekproef laag 2 subsidies (stap 5): 10% van de uitvoer, beoordeeld door een tweede Sonnet-agent.
  python3 -I lab/subsidies_steekproef.py trek [pct]   # -> lab/sets/subsidies_steekproef.json (+ batches van 5 voor de beoordelaar)
  python3 -I lab/subsidies_steekproef.py score        # leest lab/out/subsidies_steekproef/*.json -> percentages goed/klein/ernstig
Opdracht voor de beoordelaar: lab/subsidies_steekproef_opdracht.md. De beoordelaar ziet de uitspraak en de samenvatting, niet wie die schreef."""
import json, os, sys, glob, random, collections
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); S = 'subsidies'
O = f'{R}/lab/out/subsidies_steekproef'; os.makedirs(O, exist_ok=True)
if sys.argv[1] == 'trek':
    pct = float(sys.argv[2]) if len(sys.argv) > 2 else 10
    F = sorted(os.path.basename(f) for f in glob.glob(f'{R}/data/uit_v3/{S}/*.json') if json.load(open(f)).get('relevant') is not False)
    random.seed(20261120); k = max(1, round(len(F) * pct / 100)); sel = sorted(random.sample(F, k))
    json.dump([{'id': f'sp-{i // 5 + 1:03d}', 'files': sel[i:i + 5]} for i in range(0, len(sel), 5)], open(f'{R}/lab/sets/subsidies_steekproef.json', 'w'), indent=0)
    print('steekproef', k, 'van', len(F))
else:
    oord = {}
    for f in glob.glob(f'{O}/*.json'):
        for x in json.load(open(f)): oord[x['bestand']] = x
    c = collections.Counter(x['oordeel'] for x in oord.values()); n = sum(c.values()) or 1
    print('beoordeeld', n, {k: f'{v} ({100 * v // n}%)' for k, v in c.items()})
    for x in oord.values():
        if x['oordeel'] == 'ernstig': print('ERNSTIG', x['bestand'], '|', x.get('waarom'))

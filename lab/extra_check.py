"""Extra deterministische checks (aanvulling op check_uit_v3): python3 -I lab/extra_check.py <slug> <uitvoermap>
Meldt per bestand:
- ECLI in lijn.eerdere die niet in de invoertekst of relaties staat (mogelijk verzonnen)
- wetsartikel waarvan het artikelnummer niet in de invoertekst voorkomt (mogelijk uit eigen kennis)
- partijen.burger = bewoner terwijl 'bewon' nergens in de tekst staat
Print totalen; schrijft geen bestanden."""
import json, os, re, sys, collections
slug, U = sys.argv[1], sys.argv[2]
D = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'in_v3', slug)
tel = collections.Counter(); n = 0
for f in sorted(x for x in os.listdir(U) if x.endswith('.json')):
    o = json.load(open(f'{U}/{f}'))
    if o.get('relevant') is False: continue
    inp = json.load(open(f'{D}/{f}')); n += 1
    txt = ' '.join(a['t'] for a in inp['alineas']) + ' ' + (inp.get('inhoud') or '')
    rel = {r.get('ecli') for r in inp.get('relaties') or []}
    for e in (o.get('lijn') or {}).get('eerdere') or []:
        if e and e not in txt and e not in rel and ':'.join(e.split(':')[-2:]) not in txt: tel['ecli_niet_in_tekst'] += 1; print(f, 'ECLI?', e)
    for w in o.get('wetsartikelen') or []:
        m = re.search(r'(\d+[:.]?\d*[a-z]?)', w or '')
        if m and not re.search(r'(?<![\d.:])' + re.escape(m.group(1)) + r'(?![\d])', txt): tel['artikel_niet_in_tekst'] += 1; print(f, 'ARTIKEL?', w)
    if ((o.get('partijen') or {}).get('burger') or '').lower().startswith('bewoner') and 'bewon' not in txt.lower():
        tel['bewoner_zonder_grond'] += 1
print(f'{U}: {n} relevant |', dict(tel))

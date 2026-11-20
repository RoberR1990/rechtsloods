"""Check laag 2 voor woz-belastingen op losse bestanden: python3 -I lab/woz_check.py <bestand.json> [...]   (zonder bestanden: alles)
= scripts/check_uit_v3.py (schema, citaten letterlijk) + de controles van lab/extra_check.py, maar dan als FOUT:
  ECLI in lijn.eerdere die niet in de invoertekst/relaties staat, wetsartikel waarvan het nummer niet in de invoertekst staat,
  partijen.burger 'bewoner' zonder 'bewon' in de tekst. Plus: PHR moet soort_document 'conclusie AG' hebben.
Laatste regel: 'FOUTEN: n' (som van beide)."""
import json, os, re, sys, subprocess
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = 'woz-belastingen'; U = f'{R}/data/uit_v3/{S}'; I = f'{R}/data/in_v3/{S}'
files = [os.path.basename(x) for x in sys.argv[1:]] or sorted(x for x in os.listdir(U) if x.endswith('.json'))
fout = 0
for i in range(0, len(files), 200):
    r = subprocess.run(['python3', f'{R}/scripts/check_uit_v3.py', S] + files[i:i+200], capture_output=True, text=True).stdout
    for l in r.splitlines():
        if ' FOUT ' in l or 'ONTBREEKT' in l or 'GEEN GELDIGE' in l: print(l)
        if l.startswith('FOUTEN:'): fout += int(l.split()[1])
for f in files:
    p = f'{U}/{f}'
    if not os.path.exists(p): continue
    try: o = json.load(open(p))
    except Exception: continue
    if o.get('relevant') is False: continue
    inp = json.load(open(f'{I}/{f}'))
    txt = ' '.join(a['t'] for a in inp['alineas']) + ' ' + (inp.get('inhoud') or '')
    rel = {r.get('ecli') for r in inp.get('relaties') or []}
    for e in (o.get('lijn') or {}).get('eerdere') or []:
        if e and e not in txt and e not in rel and ':'.join(e.split(':')[-2:]) not in txt: print(f, 'FOUT ECLI niet in invoer:', e); fout += 1
    for w in o.get('wetsartikelen') or []:
        m = re.search(r'(\d+[:.]?\d*[a-z]?)', w or '')
        if m and not re.search(r'(?<![\d.:])' + re.escape(m.group(1)) + r'(?![\d])', txt): print(f, 'FOUT artikel niet in tekst:', w); fout += 1
    if ((o.get('partijen') or {}).get('burger') or '').lower().startswith('bewoner') and 'bewon' not in txt.lower(): print(f, 'FOUT bewoner zonder grond'); fout += 1
    if '_PHR_' in f and o.get('soort_document') != 'conclusie AG': print(f, 'FOUT PHR zonder soort_document conclusie AG'); fout += 1
print('bestanden', len(files)); print('FOUTEN:', fout)

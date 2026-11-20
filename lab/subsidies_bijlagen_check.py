"""Raakt de 'Bijlagen:'-bug van scripts/maak_in_v3.py dit domein? (alleen lezen)
  python3 -I lab/subsidies_bijlagen_check.py [xml-map]   (standaard data/xml_dom/subsidies)
Bootst de kop/WEG-logica van maak_in_v3.py na en meldt teksten waarin na een bijlage-kop nog
beoordeling of dictum wegvalt (dictumtaal in een niet-wetsartikel-alinea). Exit 0; laatste regel 'GERAAKT: n'."""
import json, os, re, sys
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
X = sys.argv[1] if len(sys.argv) > 1 else f'{R}/data/xml_dom/subsidies'
src = open(f'{R}/scripts/parse.py').read().replace('K = {r["ecli"]: r for r in json.load(open("/home/claude/data/kandidaten2.json"))}', 'K = {}')
P = {}; exec(compile(src, 'parse', 'exec'), P)
WEG = re.compile(r'^(het |de )?(procesverloop|verloop van de procedure|ontstaan en (het )?verloop van het geding|ontstaan en loop van het geding|het geding in (eerste aanleg|hoger beroep|cassatie)|de procedure|procedure|zitting|het onderzoek ter zitting|informatie over (hoger )?beroep|rechtsmiddel(en)?|bent u het niet eens|bijlage|wettelijk kader)\b', re.I)
DICT = re.compile(r'(verklaart het (hoger )?beroep|vernietigt de (aangevallen|bestreden)|bevestigt de aangevallen|draagt .{0,40} op|veroordeelt .{0,40} in de (proces)?kosten)', re.I)
WET = re.compile(r'^(op grond van|in) artikel|^artikel \d', re.I)
def kop(a):
    t = a['t'].strip(); return a.get('kop') or (len(t) < 70 and not t.endswith('.') and not t.endswith(','))
n = bijl = 0; geraakt = []
for f in sorted(os.listdir(X)):
    u = P['parse'](f'{X}/{f}'); n += 1; skip = False; trig = None; mis = False
    for i, a in enumerate(u['alineas']):
        tt = re.sub(r'^[\d.\s]+', '', a['t']).strip()
        if kop(a):
            skip = bool(WEG.match(tt))
            if skip and re.match(r'(het |de )?bijlage', tt, re.I) and trig is None: trig = i
            if skip: continue
        if skip and trig is not None and DICT.search(a['t']) and not WET.match(tt): mis = True
    bijl += trig is not None
    if mis: geraakt.append(u['ecli']); print(u['ecli'], 'dictumtaal na bijlage-kop (alinea', trig, ')')
print(f'teksten {n} | met bijlage-kop {bijl}')
print('GERAAKT:', len(geraakt))

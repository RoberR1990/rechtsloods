"""Nakijkronde uitkomstregels subsidies (stap 6). Markeert laag-2-uitspraken waarvan de uitkomst van een regel afhangt
(lab/aanscherping_sociaal.md) en past alleen mechanische correcties zelf toe.
  python3 -I lab/subsidies_nakijk_uitkomst.py lijst      # -> lab/sets/subsidies_nakijk.json (bestand, regel, huidige uitkomst, dictum)
  python3 -I lab/subsidies_nakijk_uitkomst.py toepas     # mechanisch: 'Voorlopig: ' voor vovo-toelichting; leest daarnaast
                                                       #   lab/out/subsidies_nakijk_correcties.json [{bestand, uitkomst, uitkomst_toelichting, reden}]
Daarna: check_uit_v3 + extra_check + subsidies_privacy_check opnieuw. Telt wijzigingen."""
import json, os, re, sys, glob, collections
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); S = 'subsidies'; U3 = f'{R}/data/uit_v3/{S}'; I3 = f'{R}/data/in_v3/{S}'
RG = [('spiegel', lambda o, b: o.get('procesvorm') in ('hoger beroep', 'cassatie')),
      ('voorlopige voorziening', lambda o, b: o.get('procesvorm') in ('voorlopige voorziening', 'kort geding')),
      ('rechtsgevolgen in stand', lambda o, b: bool(re.search(r'rechtsgevolgen.{0,60}in stand', b)) and o.get('uitkomst') != 'alleen procedure'),
      ('alleen kosten/termijn', lambda o, b: bool(re.search(r'(proceskosten|griffierecht|schadevergoeding|dwangsom|niet-ontvankelijk)', b)) and not re.search(r'vernietigt', b)),
      ('verlaging boete/maatregel/terugvordering', lambda o, b: bool(re.search(r'(boete|maatregel|terugvordering|verlaging).{0,80}(vast op|bepaalt|verlaagt|vermindert|herroept)|(bepaalt|stelt).{0,60}(boete|terugvordering).{0,40}(op|vast)', b)) and o.get('uitkomst') != 'deels'),
      ('procedure-onderwerp', lambda o, b: o.get('onderwerp') == 'procedure' and o.get('uitkomst') in ('burger wint', 'deels'))]
if sys.argv[1] == 'lijst':
    L = []
    for p in sorted(glob.glob(f'{U3}/*.json')):
        o = json.load(open(p))
        if o.get('relevant') is False: continue
        f = os.path.basename(p); b = (json.load(open(f'{I3}/{f}')).get('beslissing') or '').lower()
        for naam, t in RG:
            if t(o, b): L.append({'bestand': f, 'regel': naam, 'uitkomst': o.get('uitkomst'), 'toelichting': o.get('uitkomst_toelichting'), 'procesvorm': o.get('procesvorm'), 'dictum': b[:500]})
    json.dump(L, open(f'{R}/lab/sets/subsidies_nakijk.json', 'w'), ensure_ascii=False, indent=0)
    print('na te kijken', len({x['bestand'] for x in L}), dict(collections.Counter(x['regel'] for x in L)))
else:
    tel = collections.Counter()
    for p in sorted(glob.glob(f'{U3}/*.json')):
        o = json.load(open(p)); t = o.get('uitkomst_toelichting') or ''
        if o.get('procesvorm') == 'voorlopige voorziening' and not t.startswith('Voorlopig: '):
            o['uitkomst_toelichting'] = 'Voorlopig: ' + t[:1].lower() + t[1:]; tel['voorlopig-prefix'] += 1
            json.dump(o, open(p, 'w'), ensure_ascii=False, indent=1)
    cp = f'{R}/lab/out/subsidies_nakijk_correcties.json'
    for c in json.load(open(cp)) if os.path.exists(cp) else []:
        p = f"{U3}/{c['bestand']}"; o = json.load(open(p))
        if o.get('uitkomst') != c['uitkomst']:
            o['uitkomst'] = c['uitkomst']; o['uitkomst_toelichting'] = c.get('uitkomst_toelichting') or o.get('uitkomst_toelichting'); tel['uitkomst-gewijzigd'] += 1
            json.dump(o, open(p, 'w'), ensure_ascii=False, indent=1)
    print('wijzigingen', dict(tel))

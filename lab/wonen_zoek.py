"""Volledige-tekstzoeker rechtspraak.nl voor het domein wonen-leefbaarheid (aanvulling op de zoekfeeds).

  python3 -I lab/wonen_zoek.py            # idempotent: termen die al in de uitvoer staan worden overgeslagen

De open-data-feeds bevatten alleen titel en inhoudsindicatie. Rotterdamwet-zaken en zaken over de
huisvestingsverordening noemen die wet vaak alleen in de tekst. Daarom zoeken we per kernbegrip in de
volledige tekst via de publieke zoekdienst van rechtspraak.nl (zelfde aanpak als scripts/harvest.py,
maar via curl; urllib krijgt 403).
Uitvoer: data/dom/wonen-leefbaarheid/zoek_volledig.json  {term: [{ecli, titel, datum, rechtsgebieden, procedures}]}
Alleen uitspraken (geen conclusies), uitspraakdatum 2016-01-01 t/m vandaag.
"""
import json, os, subprocess, time, sys
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = f'{R}/data/dom/wonen-leefbaarheid/zoek_volledig.json'
URL = 'https://uitspraken.rechtspraak.nl/api/zoek'
TERMEN = [
    '"Wet bijzondere maatregelen grootstedelijke problematiek"', 'Rotterdamwet', '"Wbmgp"',
    'huisvestingsvergunning', 'Huisvestingswet', 'huisvestingsverordening',
    'onttrekkingsvergunning', 'omzettingsvergunning', 'splitsingsvergunning', 'woningvormingsvergunning',
    'samenvoegingsvergunning', 'woonruimtevoorraad', 'vakantieverhuur', '"toeristische verhuur"',
    'Leegstandwet', '"Wet goed verhuurderschap"', 'verhuurvergunning', 'opkoopbescherming', 'opkoopverbod',
    'overbewoning', 'kamerverhuur', '"Wet kraken en leegstand"', 'leegstandverordening', 'woonruimteverdeling',
    'urgentieverklaring', '"Wet betaalbare huur"',
]

def q(term, start, size=100):
    body = {"StartRow": start, "PageSize": size, "ShouldReturnHighlights": False, "ShouldCountFacets": False,
            "SortOrder": "UitspraakDatumDesc", "SearchTerms": [{"Term": term, "Field": "AlleVelden"}],
            "Contentsoorten": [], "Rechtsgebieden": [], "Instanties": [], "DatumPublicatie": [],
            "DatumUitspraak": [], "Advanced": {"PublicatieStatus": "AlleenGepubliceerd"}, "CorrelationId": "x",
            "Proceduresoorten": []}
    for poging in range(4):
        x = subprocess.run(['curl', '-s', '-m', '120', '-X', 'POST', '-H', 'Content-Type: application/json',
                            '--data-binary', '@-', URL], input=json.dumps(body), capture_output=True, text=True).stdout
        try: return json.loads(x)
        except Exception: time.sleep(3 + 5 * poging)
    raise SystemExit(f'zoekdienst geeft geen geldige JSON voor {term} vanaf {start}')

def jaar(r):
    d = r.get('Uitspraakdatum') or ''
    return int(d[-4:]) if d[-4:].isdigit() else 0

out = json.load(open(OUT)) if os.path.exists(OUT) else {}
for t in TERMEN:
    if t in out: continue
    rows, s = [], 0
    while True:
        d = q(t, s); res = d.get('Results') or []
        stop = False
        for r in res:
            if jaar(r) < 2016: stop = True; break  # gesorteerd op uitspraakdatum aflopend
            if r.get('GerechtelijkProductType') != 'uitspraak': continue
            rows.append({'ecli': r.get('TitelEmphasis'), 'titel': r.get('Titel'), 'datum': r.get('Uitspraakdatum'),
                         'rechtsgebieden': r.get('Rechtsgebieden') or [], 'procedures': r.get('Proceduresoorten') or []})
        s += len(res)
        if stop or not res or s >= d.get('ResultCount', 0): break
        time.sleep(0.4)
    out[t] = rows; json.dump(out, open(OUT, 'w'), ensure_ascii=False)
    print(t, len(rows), flush=True)
alle = {r['ecli'] for v in out.values() for r in v}
best = {r['ecli'] for v in out.values() for r in v if any('Bestuursrecht' in g for g in r['rechtsgebieden'])}
print('uniek', len(alle), '| bestuursrecht', len(best))

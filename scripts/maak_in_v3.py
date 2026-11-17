"""Maakt ingekorte invoer voor v3-verrijking.
Gebruik: python3 maak_in_v3.py <slug> [uitspraken.json]
Schrijft /home/claude/data/in_v3/<slug>/<ECLI>.json met metadata + alleen relevante alinea's
(kop/partijen, feiten, geschil, beoordeling, beslissing). Procesverloop, rechtsmiddelen-uitleg en
ondertekening gaan eruit. Alinea-id's blijven die van de volledige tekst (bron-id's blijven geldig).
"""
import json, os, re, sys
slug = sys.argv[1]
src = sys.argv[2] if len(sys.argv) > 2 else ('/home/claude/data/uitspraken.json' if slug == 'parkeren' else f'/home/claude/data/dom/{slug}/uitspraken.json')
out = f'/home/claude/data/in_v3/{slug}'; os.makedirs(out, exist_ok=True)
WEG = re.compile(r'^(het |de )?(procesverloop|verloop van de procedure|ontstaan en (het )?verloop van het geding|ontstaan en loop van het geding|het geding in (eerste aanleg|hoger beroep|cassatie)|de procedure|procedure|zitting|het onderzoek ter zitting|informatie over (hoger )?beroep|rechtsmiddel(en)?|bent u het niet eens|bijlage|wettelijk kader)\b', re.I)
HOU = re.compile(r'(feiten|geschil|beoordeling|overwegingen|oordeel|beslissing|conclusie|gronden|inleiding|samenvatting|kosten|griffierecht|middel|motivering|waardering|aanslag)', re.I)
EIND = re.compile(r'(in (het )?openbaar uitgesproken|uitgesproken in het openbaar|in tegenwoordigheid van|\(getekend\)|griffier\b.*\bvoorzitter|deze uitspraak is gedaan door)', re.I)
K = ['ecli', 'instantie', 'datum', 'procedure', 'rechtsgebied', 'inhoud', 'gemeente', 'beslissing', 'onderwerp', 'relaties']
def kop(a):
    t = a['t'].strip()
    return a.get('kop') or (len(t) < 70 and not t.endswith('.') and not t.endswith(','))
n = tin = tuit = 0
for u in json.load(open(src)):
    kept, skip = [], False
    for a in u['alineas']:
        t = a['t']; h = kop(a)
        tt = re.sub(r'^[\d.\s]+', '', t).strip()
        if h:
            skip = bool(WEG.match(tt))
            if skip: continue
        if skip: continue
        if EIND.search(t) and len(t) < 400: continue
        kept.append({'id': a['id'], 'rov': a.get('rov'), 't': t})
    if sum(len(a['t']) for a in kept) < 1500: kept = [{'id': a['id'], 'rov': a.get('rov'), 't': a['t']} for a in u['alineas']]
    x = {k: u.get(k) for k in K}; x['alineas'] = kept
    tin += sum(len(a['t']) for a in u['alineas']); tuit += sum(len(a['t']) for a in kept); n += 1
    json.dump(x, open(os.path.join(out, u['ecli'].replace(':', '_') + '.json'), 'w'), ensure_ascii=False)
print(f'{slug}: {n} uitspraken, tekens {tin} -> {tuit} ({100*tuit//max(tin,1)}%)')

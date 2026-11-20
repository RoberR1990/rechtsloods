"""Privacycheck laag 2 subsidies (deterministisch; aanvulling op check_uit_v3 en extra_check).
  python3 -I lab/subsidies_privacy_check.py <bestand.json|map> [...]
Meldt per bestand FOUT bij: pseudoniemen/plaatshouders ([eiser], [naam], [X]), geboortedata, leeftijd van kinderen,
diagnosetermen, landen (bezit/verblijf), postcode, IBAN, BSN-achtige nummers, namen met 'mr.'. Kijkt in alle tekstvelden
die op de site komen (titel, intro, kern, samenvatting, gevolg, bezwaargronden, rechtsregel, actie, klantuitleg, citaten).
Laatste regel 'FOUTEN: n'. Schrijft niets."""
import json, os, re, sys

DIAG = r'autis\w*|adhd|add\b|schizofren\w*|psychose|psychotisch\w*|depressi\w*|ptss|post-?traumatisch\w*|borderline|bipola\w*|' \
       r'kanker|tumor|oncolog\w*|chemo\w*|multiple sclerose|\bms\b|dementie|alzheimer|parkinson|epilep\w*|' \
       r'verslav\w*|alcoholis\w*|drugsverslav\w*|hiv|aids|diabet\w*|hartinfarct|herseninfarct|beroerte|\bcva\b|niet-aangeboren hersenletsel|\bnah\b|' \
       r'reuma\w*|fibromyalgie|whiplash|zwanger\w*|miskraam|licht verstandelijk\w*|\blvb\b|downsyndroom|syndroom van down'
LAND = r'marokk\w*|turk\w*|surinam\w*|antillen|curaçao|aruba|ghana|nigeria|irak|iran|syri\w*|afghanistan|somali\w*|eritre\w*|' \
       r'polen|pools\w*|bulgar\w*|roeme\w*|spanje|portugal|belgi\w*|duitsland|frankrijk|kaapverdi\w*|egypt\w*|pakistan|india|china|indonesi\w*'
PAT = [('geboortedatum', re.compile(r'geboren (op|in)|geboortedatum', re.I)),
       ('postcode', re.compile(r'\b\d{4} ?[A-Z]{2}\b')),
       ('iban', re.compile(r'\bNL\d{2}[A-Z]{4}\d{6,10}\b')),
       ('bsn-achtig nummer', re.compile(r'(?<![\d/.:])\d{9}(?![\d/.:])')),
       ('naam met mr.', re.compile(r'\bmr\.\s*[A-Z]')),
       ('persoonsnaam in blokhaken', re.compile(r'\[(?!appellant|eiser|eiseres|verweerder|gemachtigde|wederpartij|verzoeker|stichting|vereniging|[a-z ]*B\.V\.)[A-Za-z. ]{2,40}\]'))]


def teksten(o):
    def zin(x, pad):
        if isinstance(x, dict):
            for k in ('zin', 'citaat', 'actie', 'burger_zegt', 'reikwijdte', 'uitzondering', 'wat_gaf_doorslag'):
                if isinstance(x.get(k), str): yield f'{pad}.{k}', x[k]
            for k in ('waarom', 'bruikbare_zin'):
                if isinstance(x.get(k), dict): yield from zin(x[k], f'{pad}.{k}')
        elif isinstance(x, str): yield pad, x
    for k in ('titel', 'intro', 'klantuitleg', 'uitkomst_toelichting'):
        if isinstance(o.get(k), str): yield k, o[k]
    for k in ('kern', 'gevolg_betrokkene', 'rechtsregel', 'bewijs', 'uitkomst_bron'):
        if o.get(k): yield from zin(o[k], k)
    for k in ('samenvatting', 'bezwaargronden', 'actie_gemeente'):
        for i, x in enumerate(o.get(k) or []): yield from zin(x, f'{k}{i}')


bestanden = []
for a in sys.argv[1:]:
    bestanden += [os.path.join(a, f) for f in sorted(os.listdir(a)) if f.endswith('.json')] if os.path.isdir(a) else [a]
fout = 0
for p in bestanden:
    L = json.load(open(p)); L = L if isinstance(L, list) else [L]
    for o in L:
        if not isinstance(o, dict) or o.get('relevant') is False: continue
        for veld, t in teksten(o):
            for naam, rx in PAT:
                m = rx.search(t)
                if m: print(os.path.basename(p), o.get('ecli'), 'FOUT', naam, f'in {veld}: "{m.group(0)}"'); fout += 1
print('bestanden', len(bestanden), '| FOUTEN:', fout)

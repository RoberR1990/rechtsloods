"""Selectie v2: 6 onderwerpen, 2016-2026. Schrijft data/kandidaten2.json (primair onderwerp + extra onderwerpen)."""
import json, re, os, collections
F = "/home/claude/data/feeds"
t = lambda r: (r['title'] + ' ' + r['summary']).lower()
P = re.compile(r'parkeer|parkeren|geparkeerd|blauwe zone|parkeerschijf')
BOUW = re.compile(r'parkeernorm|parkeerbehoefte|parkeerbalans|omgevingsvergunning|bestemmingsplan|omgevingsplan|bouwplan|bouwen|woningbouw|projectbesluit|wijzigingsplan|uitwerkingsplan')
BOUWKERN = re.compile(r'parkeernorm|parkeerbehoefte|parkeerbalans|parkeerdruk|parkeerbeleid|parkeerplaatsen|parkeergelegenheid|parkeervoorziening|parkeerkelder|parkeerterrein')
HANDH = re.compile(r'scanauto|kentekenherkenning|anpr|scanfoto|scanvoertuig|parkeercontroleur|handhaver|boa\b|camera|privacy|persoonsgegevens|\bavg\b|\bwoo\b|\bwob\b|kentekenregistratie')
CIV = re.compile(r'parkeergarage|parkeerterrein|parkeerplaats|parkeervak|parkeerboete|wegslep|weggesleept|parkeerexploit|q-park|parkbee|slagboom|parkeerdek|parkeerkelder')
WOZ = re.compile(r'\bwoz\b|onroerende-zaakbelasting|onroerendezaakbelasting|\bozb\b|waarde van de onroerende')
out, seen = [], {}
def add(r, o, y):
    e = r['ecli']
    if e in seen:
        if o != seen[e]['onderwerp'] and o not in seen[e]['extra']:
            seen[e]['extra'].append(o)
        return
    d = {**r, 'jaar': y, 'onderwerp': o, 'extra': []}
    seen[e] = d; out.append(d)
for y in range(2016, 2027):
    L = {k: json.load(open(f"{F}/{k}{y}.json")) if os.path.exists(f"{F}/{k}{y}.json") else [] for k in ['bel', 'best', 'straf', 'civ']}
    for r in L['bel']:
        x = t(r)
        if P.search(x) and not WOZ.search(x): add(r, 'parkeerbelasting', y)
    for r in L['best'] + L['straf']:
        x = t(r)
        if not P.search(x): continue
        if BOUW.search(x):
            if BOUWKERN.search(x) and 'bestuursrecht_belastingrecht' not in r.get('subject', ''):
                add(r, 'parkeernormen', y)
            continue
        if re.search(r'vergunning|bezoek|wachtlijst|ontheffing', x): add(r, 'vergunningen', y)
        elif re.search(r'verbod|verkeersbesluit|gehandicapt|invalid|wahv|wegsleep|verwijder|bord|rvv|stilstaan|sanctie|beschikking|gedraging', x): add(r, 'parkeerverbod', y)
        elif HANDH.search(x): add(r, 'handhaving-privacy', y)
    for r in L['civ']:
        x = t(r)
        if CIV.search(x): add(r, 'garages-privaat', y)
    # handhaving & privacy als extra label (ook binnen andere onderwerpen)
    for k in ['bel', 'best', 'straf']:
        for r in L[k]:
            x = t(r)
            if P.search(x) and HANDH.search(x) and r['ecli'] in seen:
                add(r, 'handhaving-privacy', y)
json.dump(out, open('/home/claude/data/kandidaten2.json', 'w'), ensure_ascii=False)
c = collections.Counter((d['jaar'], d['onderwerp']) for d in out)
O = ['parkeerbelasting', 'parkeerverbod', 'vergunningen', 'parkeernormen', 'garages-privaat', 'handhaving-privacy']
print('jaar ' + ' '.join(o[:10] for o in O))
for y in range(2016, 2027): print(y, ' '.join(f"{c.get((y,o),0):>10}" for o in O))
print('totaal', len(out), ' extra-label handhaving:', sum(1 for d in out if 'handhaving-privacy' in d['extra']))

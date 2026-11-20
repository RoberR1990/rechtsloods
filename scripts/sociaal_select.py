"""Kandidaten voor het domein sociaal-domein uit de zoekfeeds (2016-2026), naar het patroon van dom_select.py.

  python3 -I scripts/sociaal_select.py            # schrijft kandidaten + tellingen
  python3 -I scripts/sociaal_select.py --check    # alleen controle op de geschreven kandidaten (0 fouten verwacht)

Invoer:  data/feeds/{best,civ}<jaar>.json  (scripts/feed.py; bestuursrecht en civiel recht, return=DOC)
Uitvoer: data/dom/sociaal-domein/kandidaten.json   -- slank, openbaar: geen inhoudsindicatie (besluit B3)
         data/feeds/kandidaten_sociaal-domein.json -- volledig, met inhoudsindicatie (gitignored; voor dom_fetch/dom_parse)
         data/dom/sociaal-domein/tellingen.json     -- per instantie, jaar, rubriek, overlap, ontdubbeling
Idempotent: zelfde feeds -> zelfde uitvoer (vaste sortering).

Afbakening (besluiten B5-B9):
- CRvB: op de wetscode in het zaaknummer (PW, WWB, WMO15, JW, BBZ, IOAW, ...). Zaken met alleen codes buiten scope vallen af.
- Overige bestuursrechtspraak: op kernbegrippen in kop + inhoudsindicatie, met uitsluitingen (rechtsbijstand, UWV/SVB-zaken,
  Wlz/AWBZ zonder gemeentelijke regeling, inburgering, leerlingenvervoer).
- Civiel: alleen als een gemeentelijke regeling (Wmo/Jeugdwet/Participatiewet/schuldhulp) samengaat met contractering/
  aanbesteding/tarieven of verhaal, en een gemeente genoemd wordt. Kinderbeschermingsmaatregelen vallen af.
"""
import json, os, re, sys, collections

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = f'{R}/data/feeds'; D = f'{R}/data/dom/sociaal-domein'; SLUG = 'sociaal-domein'
JAREN = range(2016, 2027)

# --- CRvB: wetscodes in het zaaknummer -------------------------------------------------------------
CODE_RUB = {'PW': 'bijstand', 'WWB': 'bijstand', 'WIJ': 'bijstand', 'BBZ': 'bijstand', 'IOAW': 'bijstand', 'NIOAW': 'bijstand',
            'IOAZ': 'bijstand', 'NIOAZ': 'bijstand', 'TOZO': 'bijstand', 'TONK': 'bijstand',
            'NIAOW': 'bijstand', 'WWIK': 'bijstand',  # NIAOW = tikfout NIOAW in de bron; WWIK = Wet werk en inkomen kunstenaars (gemeente)
            'WMO': 'wmo', 'WMO15': 'wmo', 'WMO2015': 'wmo', 'WM015': 'wmo', 'WVG': 'wmo',  # WVG = voorganger Wmo (gemeente)
            'JW': 'jeugdwet', 'JEUGDWET': 'jeugdwet', 'WGS': 'schuldhulp'}
GENERIEK = {'PV', 'VV', 'V', 'T', 'R', 'W', 'G', 'ONBEK', 'BESLU', 'ALGEM', 'W2', 'W3', 'W4', 'WI'}  # geen wetscode
CODE_RX = re.compile(r'\b([A-Z][A-Z0-9]{1,9})(?:-[A-Z]{1,3})?\b')

# --- kernbegrippen per rubriek (kop + inhoudsindicatie, kleine letters) ----------------------------
RUB = {
    'bijstand': r'participatiewet|(?<![a-z])(?<!juridische )(?<!gesubsidieerde )(?<!verrichte )(?<!verleende )bijstand(?!\s+(van|door)\s+(een\s+|zijn\s+|haar\s+|de\s+|hun\s+)?\w*(gemachtigde|advocaat|tolk|raadsman|raadsvrouw|vertegenwoordiger))(?! gemachtigde)|\bwwb\b|wet werk en bijstand|\bbbz\b|besluit bijstandverlening zelfstandigen|\bioaw\b|\bioaz\b|\btozo\b|tijdelijke overbruggingsregeling zelfstandig|kostendelersnorm|kostendeler|\bwij\b.{0,30}jongeren|wet investeren in jongeren|\btonk\b|tegemoetkoming noodzakelijke kosten',
    'wmo': r'\bwmo\b|maatschappelijke ondersteuning|hulp bij het huishouden|huishoudelijke (hulp|ondersteuning|verzorging)|maatwerkvoorziening|beschermd wonen|algemene voorziening',
    'jeugdwet': r'jeugdwet|jeugdhulp|jeugdzorg(?!.{0,40}(ondertoezichtstelling|uithuisplaatsing))',
    'schuldhulp': r'schuldhulpverlening|schuldhulp|wet gemeentelijke schuldhulp|\bwgs\b|(?<!wettelijke )schuldregeling.{0,60}gemeente|gemeentelijke kredietbank|kredietbank.{0,80}(schuld|lening|gemeente)',
}
RUB_RX = {k: re.compile(v) for k, v in RUB.items()}
# uitsluitingen (bestuursrecht buiten CRvB)
UIT = re.compile(r'wet inburgering|inburgeringsplicht|leerlingenvervoer|\bwsnp\b|schuldsaneringsregeling natuurlijke personen|'
                 r'rechtsbijstand|gefinancierde rechtsbijstand|consulaire bijstand|urgentieverklaring|huisvestingsverordening|'
                 r'bestemmingsplan|omgevingsvergunning|verklaring omtrent het gedrag|\bvog\b|schadefonds|'
                 r'naheffingsaanslag|parkeerbelasting|parkeervergunning')
# ander bestuursorgaan dan de gemeente (Rijk, IND, AP, ...): uitsluiten als er geen gemeentelijk orgaan genoemd wordt
RIJK = re.compile(r'staatssecretaris|\bminister\b|\bind\b|immigratie- en naturalisatiedienst|asiel|vreemdelingenwet|'
                  r'autoriteit persoonsgegevens|\bcoa\b|centraal orgaan opvang')
GEM_ORGAAN = re.compile(r'college|gemeente|burgemeester|wethouder|\bisd\b|sociale dienst|dagelijks bestuur|gemeenschappelijke regeling|werk en inkomen')
# AIO-aanvulling (Participatiewet art. 47a) wordt door de SVB uitgevoerd, niet door de gemeente
AIO = re.compile(r'\baio\b|aio-aanvulling|aanvullende inkomensvoorziening ouderen|\bsvb\b|sociale verzekeringsbank')
BUITEN_NL = re.compile(r'Gerecht in [Ee]erste [Aa]anleg|Gemeenschappelijk Hof|Raad van Beroep in Ambtenarenzaken')
UWV_SVB = re.compile(r'\buwv\b|\bsvb\b|sociale verzekeringsbank|uitvoeringsinstituut werknemersverzekeringen')
GEM = re.compile(r'college|gemeente|burgemeester|wethouder|dagelijks bestuur|participatiewet|\bwmo\b|jeugdwet|sociale dienst|'
                 r'werk en inkomen|\bisd\b|intergemeentelijke|gemeenschappelijke regeling')
LANGDURIG = re.compile(r'\bwlz\b|wet langdurige zorg|\bawbz\b|algemene wet bijzondere ziektekosten|zorgverzekering|\bzvw\b|zorgverzekeringswet')
# civiel
HUUR = re.compile(r'ontruiming|huurovereenkomst|huurachterstand|huur van woonruimte|verhuurder')
VERHAAL = re.compile(r'bijstandsverhaal|verhaal (van|op grond van|ex) .{0,30}(bijstand|participatiewet)|verhaalsbijdrage|art(ikel|\.) 62 .{0,30}(participatiewet|\bpw\b)')
CIV_CONTEXT = re.compile(r'aanbested|inkoop|ingekocht|tarie|raamovereenkomst|overeenkomst|contract|subsidie|zorgaanbieder|aanbieder|'
                         r'onderhoudsplicht|verhaal|regres|\bvergoeding\b.{0,40}(gemeente|college)')
CIV_GEM = re.compile(r'gemeente|college van burgemeester|de gemeenten')
KINDERBESCH = re.compile(r'ondertoezichtstelling|uithuisplaatsing|\bots\b|gezagsbeëindig|beëindiging van het gezag|voogdij|machtiging gesloten jeugdhulp|gesloten jeugdhulp')

HOOG = re.compile(r'Hoge Raad|Raad van State|Centrale Raad|Gerechtshof|College van Beroep|Gemeenschappelijk Hof')


def kop(r):
    t = r['title'].split(', ')
    return {'ecli': t[0], 'instantie': t[1] if len(t) > 1 else '', 'datum': t[2] if len(t) > 2 else '', 'zaaknr': ', '.join(t[3:])}


def rubrieken(x):
    return [k for k, rx in RUB_RX.items() if rx.search(x)]


def beoordeel(r, bron):
    """-> (rubrieken, wetcodes, reden) of (None, codes, reden_uitsluiting)"""
    k = kop(r); x = (r['title'] + ' ' + r['summary']).lower()
    if bron == 'best' and k['instantie'] == 'Centrale Raad van Beroep':
        codes = sorted({m.group(1) for m in CODE_RX.finditer(k['zaaknr'])} - GENERIEK)
        if codes:
            rub = sorted({CODE_RUB[c] for c in codes if c in CODE_RUB})
            if rub and AIO.search(x) and not GEM_ORGAAN.search(x): return None, codes, 'aio-svb'
            return (rub or None), codes, ('crvb-code' if rub else 'crvb-code-buiten-scope')
        rub = rubrieken(x)  # geen code: terugvallen op kernbegrippen
        if rub and not UWV_SVB.search(x): return rub, [], 'crvb-tekst'
        return None, [], 'crvb-geen-code'
    rub = rubrieken(x)
    if not rub: return None, [], 'geen-kernbegrip'
    if BUITEN_NL.search(k['instantie']): return None, [], 'caribisch-deel'
    if re.search(r'\bNL\d{2}[.\s]', k['zaaknr']): return None, [], 'vreemdelingenzaak'
    if RIJK.search(x) and not GEM_ORGAAN.search(x): return None, [], 'ander-bestuursorgaan'
    if AIO.search(x) and not GEM_ORGAAN.search(x): return None, [], 'aio-svb'
    if bron == 'best':
        if UIT.search(x) and not re.search(r'participatiewet|\bwmo\b|jeugdwet|schuldhulp|\bpw\b', x): return None, [], 'uitgesloten-begrip'
        if UWV_SVB.search(x) and not GEM.search(x): return None, [], 'uwv-svb'
        if LANGDURIG.search(x) and not GEM.search(x): return None, [], 'wlz-zvw'
        return rub, [], 'kernbegrip'
    # civiel
    if KINDERBESCH.search(x) and not re.search(r'aanbested|inkoop|tarie', x): return None, [], 'kinderbescherming'
    if VERHAAL.search(x): return rub, [], 'civiel'
    if HUUR.search(x): return None, [], 'civiel-huur'
    if not CIV_GEM.search(x): return None, [], 'civiel-geen-gemeente'
    if not CIV_CONTEXT.search(x): return None, [], 'civiel-geen-context'
    return rub, [], 'civiel'


def overlap_sets():
    S = {}
    p = f'{R}/site/data/meta.json'
    if os.path.exists(p): S['parkeren'] = {m['e'] for m in json.load(open(p))}
    for d in sorted(os.listdir(f'{R}/site/data/domeinen')):
        p = f'{R}/site/data/domeinen/{d}/meta.json'
        if os.path.exists(p): S[d] = {m['e'] for m in json.load(open(p))}
    return S


def run():
    os.makedirs(D, exist_ok=True)
    out, reden, gezien = {}, collections.Counter(), set()
    for y in JAREN:
        for bron in ('best', 'civ'):
            p = f'{F}/{bron}{y}.json'
            if not os.path.exists(p): sys.exit(f'feed ontbreekt: {p}')
            for r in json.load(open(p)):
                if r['ecli'] in gezien: continue
                gezien.add(r['ecli'])
                rub, codes, why = beoordeel(r, bron); reden[why] += 1
                if not rub: continue
                k = kop(r)
                out[r['ecli']] = {'ecli': r['ecli'], 'jaar': y, 'instantie': k['instantie'], 'datum': k['datum'], 'zaaknr': k['zaaknr'],
                                  'bron': bron, 'rubrieken': rub, 'wetcodes': codes, 'reden': why, 'summary': r['summary'],
                                  'prio_instantie': 1 if (HOOG.search(k['instantie']) or ':PHR:' in r['ecli']) else 3}
    # ontdubbelen: zelfde instantie + datum + zaaknummer = dubbele publicatie; houd de eerste ECLI (vaste sortering)
    K = sorted(out.values(), key=lambda k: k['ecli'])
    eerst, dubbel = {}, {}
    for k in K:
        sleutel = (k['instantie'], k['datum'], k['zaaknr'].strip().upper())
        if k['zaaknr'].strip() and sleutel in eerst: dubbel[k['ecli']] = eerst[sleutel]; continue
        eerst[sleutel] = k['ecli']
    K = [k for k in K if k['ecli'] not in dubbel]
    # overlap met bestaande domeinen (markeren, niet verwijderen)
    S = overlap_sets()
    for k in K:
        k['overlap'] = [d for d, s in S.items() if k['ecli'] in s]
    vol = f'{F}/kandidaten_{SLUG}.json'
    json.dump(K, open(vol, 'w'), ensure_ascii=False)
    slank = [{x: k[x] for x in ('ecli', 'jaar', 'instantie', 'datum', 'zaaknr', 'bron', 'rubrieken', 'wetcodes', 'reden', 'prio_instantie', 'overlap')} for k in K]
    json.dump(slank, open(f'{D}/kandidaten.json', 'w'), ensure_ascii=False, indent=0)
    json.dump(dubbel, open(f'{D}/dubbel.json', 'w'), indent=0)
    # tellingen
    T = {'n': len(K), 'dubbel_verwijderd': len(dubbel), 'redenen_feed': dict(reden.most_common()),
         'per_jaar': dict(sorted(collections.Counter(k['jaar'] for k in K).items())),
         'per_instantie': dict(collections.Counter(k['instantie'] for k in K).most_common()),
         'per_rubriek': dict(collections.Counter(r for k in K for r in k['rubrieken']).most_common()),
         'per_bron': dict(collections.Counter(k['bron'] for k in K)),
         'per_selectiereden': dict(collections.Counter(k['reden'] for k in K)),
         'hoog': sum(k['prio_instantie'] == 1 for k in K),
         'overlap': dict(collections.Counter(d for k in K for d in k['overlap'])),
         'instantie_jaar': {i: dict(sorted(collections.Counter(k['jaar'] for k in K if k['instantie'] == i).items()))
                            for i, _ in collections.Counter(k['instantie'] for k in K).most_common(15)}}
    json.dump(T, open(f'{D}/tellingen.json', 'w'), ensure_ascii=False, indent=1)
    print(SLUG, 'kandidaten', len(K), '| dubbel', len(dubbel), '| hoog', T['hoog'], '| rubrieken', T['per_rubriek'], '| overlap', T['overlap'])
    check()


def check():
    K = json.load(open(f'{D}/kandidaten.json')); fout = 0
    ECLI = re.compile(r'^ECLI:NL:[A-Z0-9]+:\d{4}:[A-Z0-9.]+$')
    seen = set()
    for k in K:
        F_ = []
        if not ECLI.match(k['ecli']): F_.append('ecli-vorm')
        if k['ecli'] in seen: F_.append('dubbel')
        seen.add(k['ecli'])
        if k['jaar'] not in JAREN: F_.append('jaar')
        if not k['rubrieken'] or any(r not in RUB for r in k['rubrieken']): F_.append('rubriek')
        if 'summary' in k: F_.append('inhoudsindicatie in openbare lijst')
        if k['prio_instantie'] not in (1, 3): F_.append('prio')
        for x in F_: print(k['ecli'], 'FOUT', x)
        fout += len(F_)
    print('kandidaten', len(K), '| FOUTEN:', fout)


if __name__ == '__main__':
    check() if '--check' in sys.argv else run()

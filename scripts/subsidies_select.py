"""Kandidaten voor het domein subsidies uit de zoekfeeds (2016-2026), naar het patroon van sociaal_select.py.

  python3 -I scripts/subsidies_select.py            # schrijft kandidaten + tellingen
  python3 -I scripts/subsidies_select.py --check    # alleen controle op de geschreven kandidaten (0 fouten verwacht)

Invoer:  data/feeds/{best,civ}<jaar>.json  (scripts/feed.py; bestuursrecht en civiel recht, return=DOC)
Uitvoer: data/dom/subsidies/kandidaten.json   -- slank, geen inhoudsindicatie
         data/feeds/kandidaten_subsidies.json -- volledig, met inhoudsindicatie (gitignored; voor fetch/parse)
         data/dom/subsidies/tellingen.json
Idempotent: zelfde feeds -> zelfde uitvoer.

Afbakening: subsidie(verlening/-vaststelling/-weigering/-intrekking/-terugvordering/-verantwoording/-plafond/staatssteun)
met een GEMEENTE als bestuursorgaan. Uitgesloten: Rijksregelingen (NOW, TVL, SDE, RVO, EZK, LNV...), provincies en
waterschappen, huur-/zorg-/kinderopvangtoeslag, Tozo/bijstand (domein sociaal).
"""
import json, os, re, sys, collections

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = f'{R}/data/feeds'; D = f'{R}/data/dom/subsidies'; SLUG = 'subsidies'
JAREN = range(2016, 2027)

SUBS = re.compile(r'subsidie|subsidiër|gesubsidieerd|subsidiabel|financiële bijdrage|exploitatiebijdrage|stimuleringsbijdrage|'
                  r'garantstelling|(?<![\d:])4:(2[1-9]|[3-6][0-9])\b|titel 4\.[23]\b|\bfonds\b.{0,40}\b(aanvraag|bijdrage)\b')
SUBS_HARD = re.compile(r'subsidie|subsidiër|gesubsidieerd|subsidiabel')   # voor civiel en vage gevallen
# gemeentelijk bestuursorgaan genoemd
GEM = re.compile(r'gemeente|burgemeester|wethouder|college van b(urgemeester)? ?(en|&) w|gemeenteraad|deelgemeente|stadsdeel|'
                 r'dagelijks bestuur|gemeenschappelijke regeling|\bcollege\b|\braad\b.{0,30}gemeente')
# niet-gemeentelijk orgaan
NIET = re.compile(r'gedeputeerde staten|provincie|waterschap|dijkgraaf|\bminister\b|staatssecretaris|\brvo\b|rijksdienst voor ondernemend|'
                  r'europese commissie|\bszw\b|\buwv\b|\bnwo\b|\bdienst uitvoering onderwijs\b|\bduo\b|nederlandse emissieautoriteit|'
                  r'rijkswaterstaat|\bnza\b|nederlandse zorgautoriteit|veiligheidsregio|zorgverzekeraar')
# Rijksregelingen en andere toeslagen/subsidies die niet bij de gemeente liggen
RIJKS = re.compile(r'\bnow\b|noodmaatregel overbrugging werkgelegenheid|\btvl\b|tegemoetkoming vaste lasten|\bsde\+*\b|stimulering duurzame energie|'
                   r'huursubsidie|huurtoeslag|zorgtoeslag|kinderopvangtoeslag|studiefinanciering|\bepos\b|visserijfonds|'
                   r'landbouwbeleid|gemeenschappelijk landbouw|\bgls\b|\bpgb\b|persoonsgebonden budget|\bwlz\b|\bwmo\b|jeugdwet|jeugdhulp|'
                   r'participatiewet|bijstand|\btozo\b|loonkostensubsidie|subsidie.{0,20}(zorgverzekering|ziektekosten)')
BUITEN_NL = re.compile(r'Gerecht in [Ee]erste [Aa]anleg|Gemeenschappelijk Hof|Raad van Beroep in Ambtenarenzaken|College van Beroep voor het bedrijfsleven')
HOOG = re.compile(r'Hoge Raad|Raad van State|Centrale Raad|Gerechtshof|College van Beroep|Gemeenschappelijk Hof')

RUB = {
    'subsidie-plafond': r'subsidieplafond|\bplafond\b|verdeling.{0,40}subsidie|subsidie.{0,40}verdeling|loting|rangschikking|volgorde van binnenkomst|subsidieruimte|schaarste',
    'staatssteun': r'staatssteun|de-?\s?minimis|steunmaatregel|algemeen economisch belang|\bdaeb\b|artikel 107|verboden steun|bijzondere regeling voor steun',
    'subsidie-terugvordering': r'terugvorder|teruggevorderd|terugbetal|terugbetaald|terug te betalen|intrekk|ingetrokken|herroep|lager vastgesteld|wijziging van de subsidie',
    'subsidie-vaststelling': r'vastgesteld|vaststelling|verantwoording|accountantsverklaring|afrekening|voorschot|bevoorschot|jaarrekening|activiteitenverslag|verslag',
    'subsidie-verlening': r'verleen|verleend|aanvraag|aanvragen|afgewezen|afwijz|weiger|geweigerd|toegekend|toekenn|verstrekk|verstrekt|subsidieverordening|subsidieregeling|beleidsregel',
}
RUB_RX = {k: re.compile(v) for k, v in RUB.items()}


def kop(r):
    t = r['title'].split(', ')
    return {'ecli': t[0], 'instantie': t[1] if len(t) > 1 else '', 'datum': t[2] if len(t) > 2 else '', 'zaaknr': ', '.join(t[3:])}


def beoordeel(r, bron):
    k = kop(r); x = (k['zaaknr'] + ' ' + r['summary']).lower()
    if BUITEN_NL.search(k['instantie']) and k['instantie'] != 'College van Beroep voor het bedrijfsleven': return None, 'caribisch-deel'
    if k['instantie'] == 'College van Beroep voor het bedrijfsleven' and not re.search(r'gemeente|burgemeester|wethouder|college van b', x): return None, 'cbb-geen-gemeente'
    if not SUBS.search(x): return None, 'geen-kernbegrip'
    if bron == 'civ' and not SUBS_HARD.search(x): return None, 'civiel-geen-subsidie'
    if re.search(r'\bnow\b|\btvl\b|noodmaatregel overbrugging|tegemoetkoming vaste lasten', x) and not re.search(r'gemeente|burgemeester|wethouder', x):
        return None, 'rijksregeling-now-tvl'
    gem = GEM.search(x)
    if not gem:
        # orgaan staat niet in de inhoudsindicatie: bij rechtbank/RvS/CRvB/hof de volledige tekst controleren (prep parse: kop-check)
        if k['instantie'] == 'College van Beroep voor het bedrijfsleven' or re.search(r'Aruba|Bonaire|Curaçao|Sint', k['instantie']): return None, 'geen-gemeente'
        if NIET.search(x) or RIJKS.search(x) or bron == 'civ': return None, 'geen-gemeente'
        return ['subsidie-verlening'], 'orgaan-onbekend'
    # 'college' alleen is dubbelzinnig (ook provinciaal): bij provinciale tekens en zonder gemeente eruit
    if NIET.search(x) and not re.search(r'gemeente|burgemeester|wethouder|college van b', x): return None, 'ander-bestuursorgaan'
    if RIJKS.search(x) and not re.search(r'subsidieverordening|subsidieplafond|subsidiebesluit|subsidie.{0,60}gemeente|gemeente.{0,60}subsidie', x): return None, 'rijks-of-sociaal'
    if bron == 'civ' and not re.search(r'gemeente|college van b|burgemeester', x): return None, 'civiel-geen-gemeente'
    rub = [kk for kk, rx in RUB_RX.items() if rx.search(x)]
    if not rub: rub = ['subsidie-verlening']
    return rub, 'kernbegrip'


def overlap_sets():
    S = {}
    p = f'{R}/site/data/meta.json'
    if os.path.exists(p): S['parkeren'] = {m['e'] for m in json.load(open(p))}
    base = f'{R}/site/data/domeinen'
    for d in sorted(os.listdir(base)):
        p = f'{base}/{d}/meta.json'
        if os.path.exists(p) and d != SLUG: S[d] = {m['e'] for m in json.load(open(p))}
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
                rub, why = beoordeel(r, bron); reden[why] += 1
                if not rub: continue
                k = kop(r)
                out[r['ecli']] = {'ecli': r['ecli'], 'jaar': y, 'instantie': k['instantie'], 'datum': k['datum'], 'zaaknr': k['zaaknr'],
                                  'bron': bron, 'rubrieken': rub, 'reden': why, 'summary': r['summary'],
                                  'prio_instantie': 1 if (HOOG.search(k['instantie']) or ':PHR:' in r['ecli']) else 3}
    K = sorted(out.values(), key=lambda k: k['ecli'])
    eerst, dubbel = {}, {}
    for k in K:
        sl = (k['instantie'], k['datum'], k['zaaknr'].strip().upper())
        if k['zaaknr'].strip() and sl in eerst: dubbel[k['ecli']] = eerst[sl]; continue
        eerst[sl] = k['ecli']
    K = [k for k in K if k['ecli'] not in dubbel]
    S = overlap_sets()
    for k in K: k['overlap'] = [d for d, s in S.items() if k['ecli'] in s]
    json.dump(K, open(f'{F}/kandidaten_{SLUG}.json', 'w'), ensure_ascii=False)
    slank = [{x: k[x] for x in ('ecli', 'jaar', 'instantie', 'datum', 'zaaknr', 'bron', 'rubrieken', 'reden', 'prio_instantie', 'overlap')} for k in K]
    json.dump(slank, open(f'{D}/kandidaten.json', 'w'), ensure_ascii=False, indent=0)
    json.dump(dubbel, open(f'{D}/dubbel.json', 'w'), indent=0)
    T = {'n': len(K), 'dubbel_verwijderd': len(dubbel), 'redenen_feed': dict(reden.most_common()),
         'per_jaar': dict(sorted(collections.Counter(k['jaar'] for k in K).items())),
         'per_instantie': dict(collections.Counter(k['instantie'] for k in K).most_common()),
         'per_rubriek': dict(collections.Counter(r for k in K for r in k['rubrieken']).most_common()),
         'per_bron': dict(collections.Counter(k['bron'] for k in K)),
         'hoog': sum(k['prio_instantie'] == 1 for k in K),
         'overlap': dict(collections.Counter(d for k in K for d in k['overlap']))}
    json.dump(T, open(f'{D}/tellingen.json', 'w'), ensure_ascii=False, indent=1)
    print(SLUG, 'kandidaten', len(K), '| dubbel', len(dubbel), '| hoog', T['hoog'], '| per instantie', list(T['per_instantie'].items())[:6], '| overlap', T['overlap'])
    check()


def check():
    K = json.load(open(f'{D}/kandidaten.json')); fout = 0
    ECLI = re.compile(r'^ECLI:NL:[A-Z0-9]+:\d{4}:[A-Z0-9.]+$'); seen = set()
    for k in K:
        F_ = []
        if not ECLI.match(k['ecli']): F_.append('ecli-vorm')
        if k['ecli'] in seen: F_.append('dubbel')
        seen.add(k['ecli'])
        if k['jaar'] not in JAREN: F_.append('jaar')
        if not k['rubrieken'] or any(r not in RUB for r in k['rubrieken']): F_.append('rubriek')
        if 'summary' in k: F_.append('inhoudsindicatie in openbare lijst')
        for x in F_: print(k['ecli'], 'FOUT', x)
        fout += len(F_)
    print('kandidaten', len(K), '| FOUTEN:', fout)


if __name__ == '__main__':
    check() if '--check' in sys.argv else run()

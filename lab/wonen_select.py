"""Selectie domein wonen-leefbaarheid (naar het voorbeeld van scripts/dom_select.py; dat script blijft ongewijzigd).

  python3 -I lab/wonen_select.py kandidaten   # feeds + volledige-tekstzoeker -> data/dom/wonen-leefbaarheid/kandidaten.json
  python3 -I lab/wonen_select.py filter       # na dom_fetch + dom_parse: filter op de volledige tekst -> uitspraken.json (gefilterd)
                                              #   + rapport per instantie en jaar -> data/dom/wonen-leefbaarheid/afbakening.json

Kandidaten = uitspraken (bestuursrecht 2016-2026, zoekfeeds Open Data Rechtspraak) waarvan titel + inhoudsindicatie
een kernbegrip noemen (RUBRIEKEN), plus treffers van lab/wonen_zoek.py op sterke termen in de volledige tekst.
Uitsluiten (blijft bij Openbare orde): Opiumwet 13b, drugs, art. 174a Gemeentewet (woningsluiting), Bibob.
Uitsluiten (buiten scope): belastingzaken, omgevingsvergunning bouwen / bestemmingsplan zonder woonruimtebegrip.
Overlap met openbare-orde wordt gemarkeerd (veld 'overlap'), niet verwijderd, als de zaak hier wel thuishoort.
"""
import json, os, re, sys, collections, gzip
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = f'{R}/data/dom/wonen-leefbaarheid'; F = f'{R}/data/feeds'
HOOG = re.compile(r'Hoge Raad|Raad van State|Centrale Raad|Gerechtshof|College van Beroep|Gemeenschappelijk Hof')

# rubriek -> regex op (titel + inhoudsindicatie), kleine letters
RUBRIEKEN = {
 'rotterdamwet': r'rotterdamwet|grootstedelijke problematiek|\bwbmgp\b',
 'huisvesting-verdeling': r'huisvestingswet|huisvestingsverordening|huisvestingsvergunning|woonruimteverdeling|woonruimtevergunning'
                          r'|urgentieverklaring|urgentiestatus|urgentiebeschikking|urgentie.{0,40}(woning|woonruimte|huisvesting|woonurgentie)'
                          r'|(woning|woonruimte|huisvesting).{0,40}urgentie|woonurgentie|voorrangsverklaring|woonvergunning|bindingseis',
 'woonruimtevoorraad': r'onttrekkingsvergunning|onttrek\w*.{0,60}(woonruimte|woning|bewoning)|(woonruimte|woning).{0,60}onttrek'
                       r'|omzettingsvergunning|omzetten van (zelfstandige|een zelfstandige)|onzelfstandige woonruimte|splitsingsvergunning'
                       r'|woningvorming|samenvoegingsvergunning|samenvoeg\w* van (de )?woning|kamerverhuur|kamergewijze|woonruimtevoorraad'
                       r'|verkamer|woningsplitsing|splitsen van (de )?woning',
 'vakantieverhuur': r'vakantieverhuur|toeristische verhuur|toeristische (kamer|woning)verhuur|airbnb|short ?stay|bed (and|&) breakfast',
 'leegstand-kraken': r'leegstandwet|leegstandverordening|leegstandvergunning|leegstandsvergunning|vergunning (voor )?tijdelijke verhuur'
                     r'|\bkraken\b|kraakverbod|wet kraken|leegstandbeheer|leegstandsbeheer',
 'verhuurder-opkoop': r'goed verhuurderschap|verhuurvergunning|verhuurdersvergunning|opkoopbescherming|opkoopverbod|opkoopregeling'
                      r'|wet betaalbare huur|verhuurverbod|zelfbewoningsplicht',
 'woningkwaliteit': r'(woningwet|bouwbesluit|besluit bouwwerken leefomgeving|overbewon|brandveilig|onbewoonbaar|bewoningsverbod'
                    r'|achterstallig onderhoud|ongeschikt voor bewoning|woonfraude|adresfraude|illegale kamer'
                    r'|onrechtmatige bewoning|huisjesmelker|woonoverlast)',
}
# woningkwaliteit alleen met een woon-woord en een handhavingswoord
WOON = r'woning|woonruimte|pand|kamer|bewon|verhuur|appartement|huurder|woonhuis'
HANDH = r'last onder|dwangsom|bestuursdwang|boete|handhav|sluiting|aanschrijving|verbod|gelast|invorder|sanctie|vergunning'
OO = r'\b13b\b|opiumwet|drugs|hennep|softdrugs|harddrugs|174a|\bbibob\b|integriteitsbeoordeling'
# altijd buiten scope (belastingzaken), behalve Rotterdamwet
BELASTING = (r'verhuurderheffing|overdrachtsbelasting|\bozb\b|\bwoz\b|inkomstenbelasting|omzetbelasting|\bbtw\b|toeristenbelasting'
             r'|precariobelasting|vennootschapsbelasting|belastingdienst|inspecteur|wet ib\b|loonbelasting')
# buiten scope als er geen sterk woonbegrip in staat (bijstand, asiel, toeslagen)
ANDERS = r'asiel|vreemdeling|\bcoa\b|verblijfsvergunning|naturalisatie|participatiewet|bijstand|\bwmo\b|jeugdwet|huurtoeslag|zorgtoeslag|kinderopvangtoeslag'
STERK_RX = (r'huisvestingswet|huisvestingsverordening|huisvestingsvergunning|urgentieverklaring|voorrangsverklaring|woonruimteverdeling'
            r'|onttrek|woonruimtevoorraad|omzettingsvergunning|splitsingsvergunning|woningvorming|vakantieverhuur|toeristische verhuur'
            r'|leegstandwet|goed verhuurderschap|opkoop|rotterdamwet|grootstedelijke problematiek|\bwbmgp\b')
BUITEN = BELASTING + '|' + ANDERS  # voor het tekstfilter
BOUW = r'omgevingsvergunning|bestemmingsplan|bouwvergunning|planologisch'
# sterke termen uit lab/wonen_zoek.py die zonder summary-treffer toch kandidaat worden (worden in 'filter' op de tekst gecontroleerd)
STERK = {'"Wet bijzondere maatregelen grootstedelijke problematiek"', 'Rotterdamwet', '"Wbmgp"', 'huisvestingsvergunning',
         'onttrekkingsvergunning', 'omzettingsvergunning', 'splitsingsvergunning', 'woningvormingsvergunning',
         'samenvoegingsvergunning', 'vakantieverhuur', '"toeristische verhuur"', 'Leegstandwet', '"Wet goed verhuurderschap"',
         'verhuurvergunning', 'opkoopbescherming', 'opkoopverbod', 'overbewoning', 'kamerverhuur', '"Wet kraken en leegstand"',
         'leegstandverordening', 'woonruimteverdeling', 'urgentieverklaring', 'huisvestingsverordening', 'Huisvestingswet',
         'woonruimtevoorraad', '"Wet betaalbare huur"'}

def rubrieken(x):
    rb = [k for k, rx in RUBRIEKEN.items() if k != 'woningkwaliteit' and re.search(rx, x)]
    if re.search(RUBRIEKEN['woningkwaliteit'], x) and re.search(WOON, x) and re.search(HANDH, x): rb.append('woningkwaliteit')
    return rb

def oo_ecli():
    p = f'{R}/site/data/domeinen/openbare-orde/meta.json'
    return {m['e'] for m in json.load(open(p))} if os.path.exists(p) else set()

def kandidaten():
    feed = {}
    for y in range(2016, 2027):
        p = f'{F}/best{y}.json'
        if not os.path.exists(p): raise SystemExit(f'feed ontbreekt: {p}')
        for r in json.load(open(p)): feed[r['ecli']] = (y, r)
    zoek = json.load(open(f'{D}/zoek_volledig.json')) if os.path.exists(f'{D}/zoek_volledig.json') else {}
    tekst_treffer = collections.defaultdict(set)
    for t, rows in zoek.items():
        if t in STERK:
            for r in rows: tekst_treffer[r['ecli']].add(t)
    OOE = oo_ecli(); out = {}; tel = collections.Counter()
    for e, (y, r) in feed.items():
        x = (r['title'] + ' ' + r['summary']).lower()
        rb = rubrieken(x); tt = sorted(tekst_treffer.get(e, []))
        if not rb and not tt: continue
        if re.search(BELASTING, x) and not re.search(RUBRIEKEN['rotterdamwet'], x): tel['belasting'] += 1; continue
        if re.search(ANDERS, x) and not re.search(STERK_RX, x): tel['ander_domein'] += 1; continue
        oo = bool(re.search(OO, x))
        sterk_rb = [k for k in rb if k != 'woningkwaliteit']
        if oo and not sterk_rb: tel['openbare_orde_kern'] += 1; continue
        if rb == ['woningkwaliteit'] and re.search(BOUW, x) and not re.search(r'overbewon|brandveilig|bewoningsverbod|onbewoonbaar|woonfraude|huisjesmelker', x):
            tel['bouwen_bestemmingsplan'] += 1; continue
        t = r['title'].split(', '); inst = t[1] if len(t) > 1 else ''
        ov = []
        if e in OOE or oo: ov.append('openbare-orde')
        out[e] = {'ecli': e, 'jaar': y, 'instantie': inst, 'bron': 'best', 'rubrieken': rb or ['alleen-tekst'],
                  'tekst_termen': tt, 'alleen_tekst': not rb, 'summary': r['summary'], 'overlap': ov,
                  'prio_instantie': 1 if (HOOG.search(inst) or ':PHR:' in e) else 3}
    K = sorted(out.values(), key=lambda k: k['ecli'])
    json.dump(K, open(f'{D}/kandidaten.json', 'w'), ensure_ascii=False)
    c = collections.Counter(r for k in K for r in k['rubrieken'])
    print('kandidaten', len(K), '| via inhoudsindicatie', sum(not k['alleen_tekst'] for k in K), '| alleen volledige tekst',
          sum(k['alleen_tekst'] for k in K), '| hoog', sum(k['prio_instantie'] == 1 for k in K))
    print('rubrieken', dict(c)); print('uitgesloten', dict(tel)); print('overlap openbare-orde', sum(bool(k['overlap']) for k in K))
    zt = {e for e in tekst_treffer}; print('zoektreffers buiten bestuursrecht-feed (genegeerd):', len(zt - set(feed)))

# ---- filter op de volledige tekst (na dom_parse) ----
# woonbegrippen met een wettelijke grondslag in dit domein (Huisvestingswet, Rotterdamwet, Woningwet, Leegstandwet, ...)
HW = re.compile(r'huisvestingswet|huisvestingsverordening|huisvestingsvergunning|grootstedelijke problematiek|\bwbmgp\b|rotterdamwet'
                r'|onttrekkingsvergunning|omzettingsvergunning|splitsingsvergunning|woningvormingsvergunning|samenvoegingsvergunning'
                r'|woonruimtevoorraad|woonruimteverdeling|urgentie|voorrangsverklaring|leegstandwet|goed verhuurderschap|verhuurvergunning'
                r'|opkoopbescherming|wet kraken|woningwet|bouwbesluit|besluit bouwwerken leefomgeving|overbewon|vakantieverhuur'
                r'|toeristische verhuur|onttrek', re.I)
BW = re.compile(r'omgevingsvergunning|bestemmingsplan|planologisch|omgevingsplan|beheersverordening|wijzigingsplan'
                r'|wet ruimtelijke ordening|\bwro\b|\bwabo\b', re.I)
ANDERS_IND = re.compile(r'\bleges\b|exploitatievergunning|prostitut|seksinrichting|recreatiewoning|recreatieverblijf|camping|vakantiepark'
                        r'|autoriteit woningcorporaties|toegelaten instelling|\bwoo\b|\bwob\b|wet open overheid|openbaarheid van bestuur'
                        r'|afvalstoffenheffing|subsidie|vreemdeling', re.I)

def filter_():
    K = {k['ecli']: k for k in json.load(open(f'{D}/kandidaten.json'))}
    bron = f'{D}/uitspraken_alle.json' if os.path.exists(f'{D}/uitspraken_alle.json') else f'{D}/uitspraken.json'
    U = json.load(open(bron))
    houd, weg = [], collections.Counter(); seen = set(); weglijst = {}
    for u in U:
        if u['ecli'] in seen: continue
        seen.add(u['ecli']); k = K.get(u['ecli'], {})
        u['overlap'] = k.get('overlap', []); u['tekst_termen'] = k.get('tekst_termen', [])
        full = ' '.join(a['t'] for a in u['alineas']); ind = (u.get('inhoud') or '')
        h = len(HW.findall(full)); b = len(BW.findall(full)); hi = len(HW.findall(ind))
        u['kern_treffers'] = h
        r = None
        rotterdamwet = bool(re.search(RUBRIEKEN['rotterdamwet'], (full + ' ' + ind).lower()))
        u['rotterdamwet'] = rotterdamwet
        if 'belasting' in (u.get('rechtsgebied') or '').lower(): r = 'belastingrecht'
        elif rotterdamwet: r = None                                  # opdracht: alle Rotterdamwet-uitspraken opnemen
        elif h == 0 and hi == 0: r = 'geen_woonbegrip_in_tekst'
        elif b >= 3 * h and hi == 0: r = 'planologisch'          # omgevingsvergunning/bestemmingsplan is de kern
        elif BW.search(ind) and hi == 0: r = 'planologisch_inhoudsindicatie'  # na precisiemeting 20 nov (5 van 8 'uit')
        elif ANDERS_IND.search(ind) and hi == 0: r = 'ander_onderwerp'
        elif 'Centrale Raad' in u['instantie'] and hi == 0: r = 'crvb_geen_woonzaak'
        elif k.get('alleen_tekst'):
            if h < 4 and hi == 0: r = 'alleen_tekst_zwak'         # kernbegrip alleen in een bijzin
            elif re.search(OO, ind.lower()) and hi == 0: r = 'alleen_tekst_openbare_orde'
            elif re.search(BUITEN, ind.lower()) and hi == 0: r = 'alleen_tekst_buiten_scope'
        if r: weg[r] += 1; weglijst[u['ecli']] = r; continue
        houd.append(u)
    json.dump(weglijst, open(f'{D}/afgevallen.json', 'w'), ensure_ascii=False, indent=0)
    # dubbele publicaties: zelfde instantie + zaaknummer -> markeren (dubbel_van), niet verwijderen (zoals dom_build)
    zn = collections.defaultdict(list)
    for u in sorted(houd, key=lambda u: u['datum']): zn[(u['instantie'], u.get('zaaknr'))].append(u['ecli'])
    for u in houd:
        z = zn.get((u['instantie'], u.get('zaaknr')), [])
        u['dubbel_van'] = z[0] if (u.get('zaaknr') and len(z) > 1 and z[0] != u['ecli']) else None
    alle = f'{D}/uitspraken_alle.json'
    if not os.path.exists(alle): os.replace(f'{D}/uitspraken.json', alle)
    houd.sort(key=lambda u: u['ecli'])
    json.dump(houd, open(f'{D}/uitspraken.json', 'w'), ensure_ascii=False)
    with gzip.open(f'{R}/data/raw/dom_wonen-leefbaarheid.json.gz', 'wt') as g: json.dump(houd, g, ensure_ascii=False)
    def niveau(i): return 'Hoogste rechter' if re.search(r'Hoge Raad|Raad van State|Centrale Raad|College van Beroep', i) else 'Hof' if 'hof' in i.lower() else 'Rechtbank'
    per_inst = collections.Counter(u['instantie'] for u in houd); per_jaar = collections.Counter(u['datum'][:4] for u in houd)
    per_niv = collections.Counter(niveau(u['instantie']) for u in houd)
    rap = {'n': len(houd), 'weg': dict(weg), 'dubbel': sum(1 for u in houd if u['dubbel_van']),
           'rotterdam_partij': sum(1 for u in houd if u.get('rotterdam')), 'overlap_openbare_orde': sum(1 for u in houd if u['overlap']),
           'per_niveau': dict(per_niv), 'per_jaar': dict(sorted(per_jaar.items())), 'per_instantie': dict(per_inst.most_common())}
    json.dump(rap, open(f'{D}/afbakening.json', 'w'), ensure_ascii=False, indent=1)
    print(json.dumps({k: v for k, v in rap.items() if k != 'per_instantie'}, ensure_ascii=False))

if __name__ == '__main__':
    {'kandidaten': kandidaten, 'filter': filter_}[sys.argv[1]]()

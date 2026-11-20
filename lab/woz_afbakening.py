"""WOZ en gemeentelijke belastingen, stap 1b: afbakening op de volledige tekst, plus ontdubbelen en markeren van overlap.
Gebruik: python3 -I lab/woz_afbakening.py
Invoer: data/dom/woz-belastingen/kandidaten_pool.json (lab/woz_zoek.py) + data/xml_dom/woz-belastingen/*.xml (scripts/dom_fetch.py)
Uitvoer: data/dom/woz-belastingen/kandidaten.json (definitieve set, zelfde velden als scripts/dom_select.py + afbakening/overlap)
         data/dom/woz-belastingen/afbakening.json (per pool-kandidaat: besluit, reden, signalen; plus tellingen)
Regels (vastgelegd in de besluiten, B06):
  WOZ-term  = WOZ | Wet waardering onroerende zaken | onroerende(-)zaakbelasting(en) | OZB
  gemeentelijk = heffingsambtenaar | college van burgemeester en wethouders | gemeente | samenwerkingsverband voor belastingen
  rijks     = 'inspecteur' vaker dan 2x in de kop (eerste 40 alinea's) en geen heffingsambtenaar/college daar
  pool regex: IN als WOZ-term in volledige tekst en gemeentelijk en niet rijks;
              met een andere-belastingmarker in de kop (IB, ESB, OVB, verhuurderheffing, BPM, ...) bovendien >= 3 WOZ-termen.
  pool breed: IN als >= 2 WOZ-termen in de volledige tekst, gemeentelijk en niet rijks.
  Dubbel: zelfde instantie + zaaknummer + datum, of identieke tekst -> alleen de laagste ECLI blijft (rest in afbakening.json)."""
import json, os, re, sys, collections, hashlib
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, f'{R}/scripts')
os.chdir(R)
import parse as P
D = f'{R}/data/dom/woz-belastingen'; X = f'{R}/data/xml_dom/woz-belastingen'
POOL = json.load(open(f'{D}/kandidaten_pool.json'))
WOZ = re.compile(r'\bWOZ\b|Wet waardering onroerende zaken|onroerende[- ]?zaak ?belasting|\bOZB\b', re.I)
GEM = re.compile(r'heffingsambtenaar|college van burgemeester en wethouders|\bgemeente\b|belastingsamenwerking|gemeentebelastingen|cocensus|\bsvhw\b|\bbsgr\b|\bbghu\b|\bgblt\b|dienst belastingen', re.I)
GEM_ORG = re.compile(r'heffingsambtenaar|college van burgemeester en wethouders', re.I)
INSP = re.compile(r'\binspecteur\b', re.I)
ANDER = re.compile(r'\bib\b|ib/pvv|inkomstenbelasting|eigenwoningforfait|box ?3|erfbelasting|schenkbelasting|successie|overdrachtsbelasting|\bovb\b|\bbpm\b|parkeer|vennootschapsbelasting|\bvpb\b|omzetbelasting|\bob\b|loonheffing|douane|kansspel|motorrijtuigenbelasting|\bmrb\b|verhuurderheffing|toeslag', re.I)
# overlap met bestaande domeinen (alleen markeren)
OV = {}
for nm, p in [('parkeren', 'site/data/meta.json'), ('bpm', 'site/data/domeinen/bpm/meta.json'), ('verkeersboetes', 'site/data/domeinen/verkeersboetes/meta.json'),
              ('avg-privacy', 'site/data/domeinen/avg-privacy/meta.json'), ('openbare-orde', 'site/data/domeinen/openbare-orde/meta.json')]:
    for m in json.load(open(f'{R}/{p}')): OV.setdefault(m['e'], []).append(nm)
uit, besl, tel = [], {}, collections.Counter()
info = {}
for k in POOL:
    e = k['ecli']; f = f"{X}/{e.replace(':', '_')}.xml"
    if not os.path.exists(f) or os.path.getsize(f) < 500: besl[e] = {'in': False, 'reden': 'xml ontbreekt'}; tel['xml ontbreekt'] += 1; continue
    try: u = P.parse(f)
    except Exception as ex: besl[e] = {'in': False, 'reden': f'parsefout'}; tel['parsefout'] += 1; continue
    full = ' '.join(a['t'] for a in u['alineas']); kop = ' '.join(a['t'] for a in u['alineas'][:40])
    allt = (u.get('inhoud') or '') + ' ' + full
    nw = len(WOZ.findall(allt)); g = bool(GEM.search(allt)); gorg = len(GEM_ORG.findall(kop)); ni = len(INSP.findall(kop))
    rijks = ni > 2 and gorg == 0
    ander = k.get('ander_belasting_in_kop')
    if k['pool'] == 'regex':
        ok = nw >= 1 and g and not rijks and (not ander or nw >= 3)
        reden = 'WOZ-term in kop/inhoudsindicatie' if ok else ('rijksbelasting (inspecteur)' if rijks else 'andere belasting, WOZ bijzaak' if ander else 'geen gemeentelijk orgaan' if not g else 'geen WOZ-term in tekst')
    else:
        ok = nw >= 2 and g and not rijks
        reden = f'WOZ-term {nw}x in volledige tekst' if ok else ('rijksbelasting (inspecteur)' if rijks else f'WOZ-term {nw}x' if nw < 2 else 'geen gemeentelijk orgaan')
    besl[e] = {'in': ok, 'reden': reden, 'pool': k['pool'], 'n_woz': nw, 'inspecteur_kop': ni, 'heffingsambtenaar_college_kop': gorg}
    tel[f"{k['pool']}:{'in' if ok else 'uit'}"] += 1
    if ok:
        info[e] = (u['instantie'], u.get('zaaknr'), u['datum'], hashlib.md5(full.encode()).hexdigest())
        uit.append(dict(k, afbakening=reden, overlap=OV.get(e, [])))
# ontdubbelen
eerst = {}; dub = {}
for k in sorted(uit, key=lambda k: k['ecli']):
    i = info[k['ecli']]
    for key in [('z',) + i[:3] if i[1] else None, ('h', i[3])]:
        if key is None: continue
        if key in eerst and eerst[key] != k['ecli']: dub[k['ecli']] = eerst[key]; break
    else:
        for key in [('z',) + i[:3] if i[1] else None, ('h', i[3])]:
            if key: eerst[key] = k['ecli']
uit = [k for k in uit if k['ecli'] not in dub]
for e, v in dub.items(): besl[e].update({'in': False, 'reden': f'dubbele publicatie van {v}'})
json.dump(sorted(uit, key=lambda k: k['ecli']), open(f'{D}/kandidaten.json', 'w'), ensure_ascii=False)
pi = collections.Counter(k['instantie'] for k in uit); pj = collections.Counter(k['jaar'] for k in uit)
rap = {'tellingen': dict(tel), 'dubbel': len(dub), 'definitief': len(uit), 'per_instantie': dict(pi.most_common()), 'per_jaar': dict(sorted(pj.items())),
       'overlap': dict(collections.Counter(o for k in uit for o in k['overlap'])), 'besluiten': besl}
json.dump(rap, open(f'{D}/afbakening.json', 'w'), ensure_ascii=False, indent=0)
print('definitief', len(uit), '| dubbel', len(dub), '|', dict(tel), '| overlap', rap['overlap'])
print('per jaar', rap['per_jaar'])
print('per instantie', dict(pi.most_common(30)))

"""AVG-taxonomie: 35 -> 25 subonderwerpen (voorstel 16 nov 2026, wacht op akkoord Robert).
Zonder --toepassen: alleen tellen wat er zou veranderen. Met --toepassen: taxonomie.json + laag 1 + lab/out bijwerken.
Ook: partijen.burger 'bewoner' -> 'betrokkene' in lab/out/avg-privacy als 'bewoner' niet in de uitspraaktekst staat.
"""
import json, glob, os, sys, collections
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOEN = '--toepassen' in sys.argv
# (onderwerp, oud) -> nieuw sub; nieuw label voor het blijvende sub
MAP = {('algoritmes-registraties', 'geautomatiseerd-besluit'): 'algoritme-ai',
       ('rechten-betrokkene', 'geautomatiseerd-besluit'): 'algoritme-ai',
       ('rechten-betrokkene', 'mededeling-overdraagbaarheid'): 'beperking-bezwaar',
       ('rechtmatige-verwerking', 'beginselen'): 'grondslag',
       ('rechtmatige-verwerking', 'beveiliging-datalek'): 'medewerkers-ambtenaren',
       ('politie-justitie', 'wpg-verstrekking'): 'wpg-correctie',
       ('toezicht-handhaving', 'beroep-tegen-ap'): 'klacht-ap',
       ('toezicht-handhaving', 'leidende-toezichthouder'): 'klacht-ap',
       ('schade-aansprakelijkheid', 'bewijs-schade'): 'materiele-schade',
       ('schade-aansprakelijkheid', 'proceskosten'): 'dwangsom-niet-tijdig',
       ('algoritmes-registraties', 'brp-verstrekking'): 'overheidsregister'}
# geautomatiseerd-besluit hangt onder rechten-betrokkene; het nieuwe sub ligt onder algoritmes-registraties
ONDERWERP = {('rechten-betrokkene', 'geautomatiseerd-besluit'): 'algoritmes-registraties'}
LABEL = {'algoritme-ai': 'Algoritme, AI of besluit door een computer',
         'beperking-bezwaar': 'Verwerking beperken, bezwaar maken, gegevens overdragen',
         'grondslag': 'Grondslag en beginselen',
         'medewerkers-ambtenaren': 'Medewerkers, beveiliging en datalekken',
         'wpg-correctie': 'Politiegegevens corrigeren, verwijderen of delen',
         'klacht-ap': 'Klacht bij de AP en beroep tegen de AP',
         'materiele-schade': 'Vermogensschade en bewijs van schade',
         'dwangsom-niet-tijdig': 'Dwangsom en proceskosten',
         'overheidsregister': 'Overige registers en verstrekking uit de BRP'}

def omzet(o, tel):
    k = (o.get('onderwerp'), o.get('sub'))
    if k in MAP:
        o['onderwerp'] = ONDERWERP.get(k, k[0]); o['sub'] = MAP[k]; tel[k] += 1
        o.pop('kenmerk', None) if k[1] in ('beginselen',) else None
    return o

tel = collections.Counter()
# taxonomie
tp = f'{R}/data/dom/avg-privacy/taxonomie.json'; tax = json.load(open(tp))
for (on, oud), nieuw in MAP.items():
    tax.get(on, {}).get('sub', {}).pop(oud, None)
for o in [x for x in tax.values() if isinstance(x, dict)]:
    for s, v in o.get('sub', {}).items():
        if s in LABEL: v['label'] = LABEL[s]
    o['concept'] = False
tax['_bevroren'] = '2026-11-16'
# laag 1
l1 = sorted(glob.glob(f'{R}/data/uit_l1/avg-privacy/*.json'))
l1d = {f: [omzet(r, tel) for r in json.load(open(f))] for f in l1}
# laag 2 (lab/out) + bewoner
uit = sorted(glob.glob(f'{R}/lab/out/avg-privacy/*.json'))
tekst = {u['ecli']: u for u in json.load(open(f'{R}/data/dom/avg-privacy/uitspraken.json'))}
l2d, bew = {}, 0
for f in uit:
    d = omzet(json.load(open(f)), tel)
    pj = d.get('partijen') or {}
    if (pj.get('burger') or '').lower() == 'bewoner' and 'bewoner' not in json.dumps(tekst.get(d['ecli'], {}), ensure_ascii=False).lower():
        pj['burger'] = 'betrokkene'; bew += 1
    l2d[f] = d
n = sum(len(v.get('sub', {})) for k, v in tax.items() if not k.startswith('_'))
print(f'subonderwerpen na samenvoegen: {n} | omgezette labels: {sum(tel.values())} | bewoner -> betrokkene: {bew}')
for k, v in tel.most_common(): print(' ', k, v)
if DOEN:
    json.dump(tax, open(tp, 'w'), ensure_ascii=False, indent=1)
    for f, v in l1d.items(): json.dump(v, open(f, 'w'), ensure_ascii=False)
    for f, v in l2d.items(): json.dump(v, open(f, 'w'), ensure_ascii=False, indent=1)
    print('toegepast')

"""WOZ en gemeentelijke belastingen, stap 1a: kandidaten-pool uit de belastingrecht-feeds (2016-2026).
Gebruik: python3 -I lab/woz_zoek.py   -> data/dom/woz-belastingen/kandidaten_pool.json (+ kandidaten.json als die nog niet bestaat)
Twee bakken (veld 'pool'):
  regex  = WOZ-term in titel of inhoudsindicatie (zelfde regex als scripts/tel_domeinen.py, reproduceert de verkenning ±8.877)
  breed  = geen WOZ-term, wel een WOZ-achtige term (waardepeildatum, taxatieverslag, heffingsambtenaar, proceskosten,
           immateriële schade, gemachtigde, ...) en geen marker van een andere belasting. Wordt in stap 1b op de volledige tekst beoordeeld.
Idempotent: zelfde invoer -> zelfde uitvoer."""
import json, re, os, collections
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = f'{R}/data/feeds'; D = f'{R}/data/dom/woz-belastingen'; os.makedirs(D, exist_ok=True)
WOZ = re.compile(r'\bwoz\b|waardering onroerende zaken|onroerende-?zaakbelasting|\bozb\b')
ANDER = re.compile(r'\bib\b|ib/pvv|inkomstenbelasting|eigenwoningforfait|box ?3|erfbelasting|schenkbelasting|successie|overdrachtsbelasting|\bovb\b|\bbpm\b|parkeer|vennootschapsbelasting|\bvpb\b|omzetbelasting|\bob\b|loonheffing|loonbelasting|douane|invorderingswet|kansspel|motorrijtuigenbelasting|\bmrb\b|toeristenbelasting|precario|dividendbelasting|verhuurderheffing|toeslag|\bawir\b|accijns|energiebelasting|zorgverzekeringswet|premie|\bwfsv\b|bankenbelasting|rioolheffing|afvalstoffenheffing|reinigingsrecht|leges|forensenbelasting|reclamebelasting|inspecteur')
BREED = re.compile(r'onroerende ?zaak|waardepeildatum|\bwpd\b|vergelijkingsobject|waardematrix|taxatiematrix|taxatieverslag|taxatierapport|woningwaarde|vervangingswaarde|heffingsambtenaar|immateri|proceskosten|no.?cure|gemachtigde|redelijke termijn|30a|gemeentelijke belasting|lokale belasting|gemeentebelasting|waarde van de woning|waarde van het|de waarde van')
HOOG = re.compile(r'Hoge Raad|Raad van State|Centrale Raad|Gerechtshof|College van Beroep|Gemeenschappelijk Hof')
out = {}
for y in range(2016, 2027):
    for r in json.load(open(f'{F}/bel{y}.json')):
        if r['ecli'] in out: continue
        x = (r['title'] + ' ' + r['summary']).lower()
        if WOZ.search(x): pool = 'regex'
        elif BREED.search(x) and not ANDER.search(x): pool = 'breed'
        else: continue
        t = r['title'].split(', '); inst = t[1] if len(t) > 1 else ''
        out[r['ecli']] = {'ecli': r['ecli'], 'jaar': y, 'instantie': inst, 'bron': 'bel', 'rubrieken': ['woz'], 'summary': r['summary'],
                          'prio_instantie': 1 if (HOOG.search(inst) or ':PHR:' in r['ecli']) else 3, 'pool': pool,
                          'ander_belasting_in_kop': bool(ANDER.search(x))}
K = sorted(out.values(), key=lambda k: k['ecli'])
json.dump(K, open(f'{D}/kandidaten_pool.json', 'w'), ensure_ascii=False)
if not os.path.exists(f'{D}/kandidaten.json'): json.dump(K, open(f'{D}/kandidaten.json', 'w'), ensure_ascii=False)
print('pool', len(K), dict(collections.Counter(k['pool'] for k in K)), '| regex met andere-belastingmarker', sum(k['ander_belasting_in_kop'] for k in K))

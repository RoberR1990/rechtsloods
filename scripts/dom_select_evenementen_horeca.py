"""Selectie domein Evenementen, horeca en APV-vergunningen (slug evenementen-horeca).
Gebruik: python3 dom_select_evenementen_horeca.py
Leest zoekfeeds /home/claude/data/feeds/{best,civ}{jaar}.json (titel+inhoudsindicatie, 2016-2026).
Schrijft data/dom/evenementen-horeca/kandidaten.json (zelfde vorm als dom_select.py, plus 'overlap' en 'aanleg')
en grens.json (uitgesloten randgevallen: woonwagen, coffeeshop, belasting e.d.)."""
import json, re, os, sys, collections
F = '/home/claude/data/feeds'; SLUG = 'evenementen-horeca'; D = f'/home/claude/data/dom/{SLUG}'
R = '/home/claude/site/data/domeinen'
HOOG = re.compile(r'Hoge Raad|Raad van State|Centrale Raad|Gerechtshof|College van Beroep|Gemeenschappelijk Hof')
OVERHEID = re.compile(r'college|burgemeester|gemeente|apv|algemene plaatselijke|bestuursorgaan|provincie|staat der nederlanden')

# rubriek -> regex op (titel + inhoudsindicatie).lower()
RUB = [
 ('evenementen', r'evenement|festival|kermis|braderie|dancefeest|dance-?event|muziekfeest|concert|optocht|carnaval|vuurwerkshow|stratenfeest|buurtfeest|volksfeest'),
 ('exploitatie-horeca', r'exploitatievergunning|horeca|caf[eé]\b|nachtclub|discotheek|nachtzaak|shishalounge|nachtwinkel|(restaurant|snackbar|lunchroom|eetcaf|kroeg).{0,200}(exploitatie|apv|burgemeester|alcohol|drank|sluit|horecawet|last onder)'),
 ('terras', r'terrasvergunning|terrasuitbreiding|terras(sen)? (van|bij|voor|behorende)|horeca.{0,80}terras|terras.{0,80}(horeca|caf[eé]|restaurant|exploitatie|apv|precario|openbare (weg|ruimte))|uitstallingsvergunning'),
 ('standplaats-markt', r'warenmarkt|weekmarkt|jaarmarkt|markt(plaats|standplaats|vergunning|verordening|koopman|handel|kraam|kramen|ondernemer|reglement)|marktplaatsen|standplaatsvergunning|standplaats(en)? (voor|op|aan|bij)|straatverkoop|straathandel|venten|ventvergunning|foodtruck|ambulante handel|kermisexploitant'),
 ('alcoholwet', r'alcoholwet|drank-? ?en horecawet|drank en horecawet|alcoholvergunning|drankvergunning|paracommerci|slijterij|alcoholschenking|schenken van alcohol|alcoholhoudende drank'),
 ('sluitingstijden', r'sluitingstijd|openingstijd|nachtvergunning|ontheffing van de sluitingstijden|vroegere sluiting|latere sluiting|vervroegde sluiting'),
 ('overige-exploitatie', r'speelautomatenhal|speelhal|seksinrichting|escortbedrijf|prostitutie|raamprostitutie|seksbedrijf|sekswinkel|exploitatievergunning voor een (seks|speel)'),
]
# harde uitsluiting uit dit domein (grens; wel vastgelegd in grens.json)
UIT = [
 ('woonwagen', r'woonwagen'),
 ('coffeeshop-opiumwet', r'coffeeshop|gedoogcriteri|damocles|opiumwet|hennep'),
 ('belasting-sociaal', r'\buwv\b|\bww-uitkering|werkloosheidswet|ziektewet|wajong|arbeidsongeschikt|loonheffing|omzetbelasting|\bbtw\b|\bwoz\b|\bozb\b|belastingdienst|toeslag|bijstand|participatiewet|vreemdelingen|asiel|verblijfsvergunning|\bcao\b|cassatie in het belang|belasting van personenauto|\bbpm\b|\bawr\b|aanslag|inkomstenbelasting|\btvl\b|tabaks|rookwaren|huurovereenkomst|ontruiming|\bwav\b|planschade|nadeelcompensatie'),
 ('winkeltijden', r'winkeltijdenwet|koopzondag'),
]
STERK_HORECA = re.compile(r'burgemeester|gemeente|apv|algemene plaatselijke|vergunning|exploitatie|alcohol|drank|terras|sluitings|openings|ontheffing|horecawet|horeca-?(inrichting|gelegenheid|onderneming|bedrijf)|bestuursdwang|last onder')
BAU = re.compile(r'bestemmingsplan|omgevingsvergunning|bouwvergunning|dakterras|balkon|planologisch|bestemming|wabo|waardepeildatum|\bwoz\b|laadpunt|wbr')
EXPL = re.compile(r'exploitatievergunning|alcohol|drank|horecawet|apv|algemene plaatselijke|sluitingstijd|terrasvergunning|evenementenvergunning|standplaatsvergunning|ventvergunning|horeca-?(inrichting|gelegenheid|bedrijf|onderneming)')
OO = re.compile(r'bibob|\b13b\b|artikel 13b|174a|woningsluiting|sluiting van (de |een )?woning|drugspand|gebiedsverbod|noodbevel')
# overlap-ECLI's met bestaande domeinen
def bekend():
    S = {}
    for dom in ('openbare-orde', 'avg-privacy', 'verkeersboetes', 'bpm'):
        p = f'{R}/{dom}/verrijkt.json'
        if os.path.exists(p): S[dom] = {x['ecli'] for x in json.load(open(p))}
    return S

def main():
    os.makedirs(D, exist_ok=True); S = bekend(); out = {}; grens = {}
    for y in range(2016, 2027):
        for src in ('best', 'civ'):
            p = f'{F}/{src}{y}.json'
            if not os.path.exists(p): continue
            for r in json.load(open(p)):
                x = (r['title'] + ' ' + r['summary']).lower()
                if not r['summary'] and src == 'civ': continue
                rub = []
                for k, rx in RUB:
                    if re.search(rx, x): rub.append(k)
                if not rub: continue
                # civiel: alleen overheidsvergunningen (geen huur/arbeid/privaat)
                if src == 'civ' and not OVERHEID.search(x): continue
                if rub == ['exploitatie-horeca'] and not STERK_HORECA.search(x): continue
                if rub == ['evenementen'] and not re.search(r'vergunning|apv|burgemeester|gemeente|ontheffing|verbod|geluid|last onder|handhav|bestuursdwang|leges|kort geding', x): continue
                uit = [k for k, rx in UIT if re.search(rx, x)]
                if BAU.search(x) and not EXPL.search(x) and 'evenementen' not in rub and 'standplaats-markt' not in rub: uit.append('omgevingsrecht-bouw')
                if src == 'civ' and 'vergunning' not in x and 'apv' not in x and 'burgemeester' not in x: continue
                t = r['title'].split(', '); inst = t[1] if len(t) > 1 else ''
                rec = {'ecli': r['ecli'], 'jaar': y, 'instantie': inst, 'bron': src, 'rubrieken': rub, 'summary': r['summary'],
                       'prio_instantie': 1 if (HOOG.search(inst) or ':PHR:' in r['ecli']) else 3}
                ov = [d for d, s in S.items() if r['ecli'] in s]
                if OO.search(x) and 'openbare-orde' not in ov: ov.append('openbare-orde?')
                if ov: rec['overlap'] = ov
                if uit: rec['uit'] = uit; grens[r['ecli']] = rec; continue
                out[r['ecli']] = rec
    K = list(out.values())
    json.dump(K, open(f'{D}/kandidaten.json', 'w'), ensure_ascii=False)
    json.dump(list(grens.values()), open(f'{D}/grens.json', 'w'), ensure_ascii=False)
    c = collections.Counter(k['prio_instantie'] for k in K)
    print(SLUG, len(K), '| hoog:', c[1], '| grens uitgesloten:', len(grens))
    print('rubrieken:', dict(collections.Counter(r for k in K for r in k['rubrieken'])))
    print('overlap:', dict(collections.Counter(o for k in K for o in k.get('overlap', []))))
    print('jaar:', dict(sorted(collections.Counter(k['jaar'] for k in K).items())))
    print('bron:', dict(collections.Counter(k['bron'] for k in K)))
    print('uitgesloten reden:', dict(collections.Counter(u for k in grens.values() for u in k['uit'])))
main()

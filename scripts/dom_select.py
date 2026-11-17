"""Selectie per domein uit de zoekfeeds (2016-2026). Gebruik: python3 dom_select.py <slug>|alle
Schrijft data/dom/<slug>/kandidaten.json: ecli, jaar, instantie, rubriek, summary, prio_instantie (1 = HR/RvS/CRvB/hof/PHR)."""
import json,re,os,sys,collections
F='/home/claude/data/feeds';D='/home/claude/data/dom'
PARK=re.compile(r'parkeer|parkeren|geparkeerd|blauwe zone|parkeerschijf')
OVERHEID=re.compile(r'college|burgemeester|gemeente|minister|staatssecretaris|bestuursorgaan|politie|\buwv\b|\bsvb\b|belastingdienst|inspecteur|autoriteit persoonsgegevens|\bap\b|staat der nederlanden|provincie|waterschap|\bcbr\b|\brdw\b|\bduo\b|\bind\b|\bcak\b|officier van justitie|openbaar ministerie|korpschef')
DOM={
 'openbare-orde':{'label':'Openbare orde en veiligheid','rubrieken':[
   ('drugspanden-13b',['best'],r'13b|opiumwet.*sluit|sluit.*opiumwet|drugspand'),
   ('bibob',['best','civ'],r'bibob|integriteitsbeoordelingen'),
   ('camera-noodbevel-gebiedsverbod',['best','straf'],r'cameratoezicht|noodbevel|noodverordening|gebiedsverbod|172a|174a')]},
 'avg-privacy':{'label':'AVG, privacy en algoritmes','overheid':True,'rubrieken':[
   ('avg-algoritmes',['best','civ'],r'\bavg\b|gegevensbescherming|persoonsgegevens|algoritm')]},
 'verkeersboetes':{'label':'Verkeersboetes (Wahv)','geen_parkeren':True,'rubrieken':[
   ('wahv',['best','straf'],r'\bwahv\b|administratiefrechtelijke handhaving verkeersvoorschriften|wet mulder|mulderzaak')]},
 'woz':{'label':'WOZ-waarde en OZB','rubrieken':[
   ('woz',['bel'],r'\bwoz\b|waardering onroerende zaken|onroerende-?zaakbelasting|\bozb\b')]},
 'bpm':{'label':'BPM (autobelasting)','rubrieken':[
   ('bpm',['bel'],r'\bbpm\b|belasting van personenauto')]},
}
HOOG=re.compile(r'Hoge Raad|Raad van State|Centrale Raad|Gerechtshof|College van Beroep|Gemeenschappelijk Hof')
def run(slug):
    d=DOM[slug];out={};os.makedirs(f'{D}/{slug}',exist_ok=True)
    park=set(json.load(open('/home/claude/data/kandidaten2.json')) and [r['ecli'] for r in json.load(open('/home/claude/data/kandidaten2.json'))])
    for y in range(2016,2027):
        L={k:(json.load(open(f'{F}/{k}{y}.json')) if os.path.exists(f'{F}/{k}{y}.json') else []) for k in ['bel','best','straf','civ']}
        for rub,srcs,rx in d['rubrieken']:
            R=re.compile(rx)
            for s in srcs:
                for r in L[s]:
                    x=(r['title']+' '+r['summary']).lower()
                    if not R.search(x): continue
                    if d.get('geen_parkeren') and (r['ecli'] in park or PARK.search(x)): continue
                    if d.get('overheid') and s=='civ' and not OVERHEID.search(x): continue
                    if r['ecli'] in out:
                        if rub not in out[r['ecli']]['rubrieken']: out[r['ecli']]['rubrieken'].append(rub)
                        continue
                    t=r['title'].split(', ');inst=t[1] if len(t)>1 else ''
                    out[r['ecli']]={'ecli':r['ecli'],'jaar':y,'instantie':inst,'bron':s,'rubrieken':[rub],'summary':r['summary'],
                        'prio_instantie':1 if (HOOG.search(inst) or ':PHR:' in r['ecli']) else 3}
    K=list(out.values());json.dump(K,open(f'{D}/{slug}/kandidaten.json','w'),ensure_ascii=False)
    c=collections.Counter(k['prio_instantie'] for k in K);print(slug,len(K),'| hoog:',c[1],'| rubrieken:',dict(collections.Counter(r for k in K for r in k['rubrieken'])))
for s in (DOM if sys.argv[1]=='alle' else [sys.argv[1]]): run(s)

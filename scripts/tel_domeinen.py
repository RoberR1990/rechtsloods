import json,re,os,collections
F="data/feeds"
D={
 'WOZ':(['bel'],r'\bwoz\b|waardering onroerende zaken|onroerende-?zaakbelasting|\bozb\b'),
 'Verkeersboetes (Wahv, alles)':(['best','straf'],r'\bwahv\b|administratiefrechtelijke handhaving verkeersvoorschriften|wet mulder|mulderzaak'),
 'BPM':(['bel'],r'\bbpm\b|belasting van personenauto'),
 'Sociaal: bijstand':(['best'],r'participatiewet|bijstand|\bioaw\b|\bioaz\b|\bbbz\b'),
 'Sociaal: Wmo':(['best'],r'\bwmo\b|maatschappelijke ondersteuning|huishoudelijke (hulp|ondersteuning)'),
 'Sociaal: Jeugdwet':(['best'],r'jeugdwet|jeugdhulp'),
 'Sociaal: leerlingenvervoer/schuldhulp':(['best'],r'leerlingenvervoer|schuldhulp|gemeentelijke schuldhulpverlening'),
 'Woo/Wob':(['best'],r'\bwoo\b|\bwob\b|wet open overheid|openbaarheid van bestuur'),
 'Grond: Didam/gronduitgifte':(['civ','best'],r'didam|gronduitgifte|verkoop van (de )?grond|grondtransactie'),
 'Grond: erfpacht':(['civ','best','bel'],r'erfpacht'),
 'Openbare orde: drugspanden (13b)':(['best'],r'13b|opiumwet.*sluit|sluit.*opiumwet|drugspand'),
 'Openbare orde: Bibob':(['best','civ'],r'bibob|integriteitsbeoordelingen'),
 'Openbare orde: camera/noodbevel/gebiedsverbod':(['best','straf'],r'cameratoezicht|noodbevel|noodverordening|gebiedsverbod|172a|174a'),
 'AVG en algoritmes':(['best','civ'],r'\bavg\b|gegevensbescherming|persoonsgegevens|algoritm'),
}
C={k:collections.Counter() for k in D}
for y in range(2016,2027):
  L={k:(json.load(open(f"{F}/{k}{y}.json")) if os.path.exists(f"{F}/{k}{y}.json") else []) for k in ['bel','best','straf','civ']}
  for k,(srcs,rx) in D.items():
    R=re.compile(rx)
    seen=set()
    for s in srcs:
      for r in L[s]:
        if r['ecli'] in seen: continue
        if R.search((r['title']+' '+r['summary']).lower()): seen.add(r['ecli']); C[k][y]+=1
U=json.load(open('data/uitspraken.json'))
print('parkeren ref: n',len(U),'gem tekens',sum(u['tekens'] for u in U)//len(U))
for k in D: print(f"{k:50s} {sum(C[k].values()):6d}  2025:{C[k][2025]}")
json.dump({k:dict(v) for k,v in C.items()},open('data/domeintellingen.json','w'))

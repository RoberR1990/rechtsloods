import json,re
t=lambda r:(r['title']+' '+r['summary']).lower()
P=re.compile(r'parkeer|parkeren|geparkeerd|blauwe zone|parkeerschijf')
out=[];cnt={}
for y in [2023,2024,2025,2026]:
    B=json.load(open(f'data/feeds/bel{y}.json'));A=json.load(open(f'data/feeds/best{y}.json'));S=json.load(open(f'data/feeds/straf{y}.json'))
    seen=set()
    def add(r,topic):
        if r['ecli'] in seen: return
        seen.add(r['ecli']); out.append({**r,'jaar':y,'onderwerp':topic}); cnt[(y,topic)]=cnt.get((y,topic),0)+1
    for r in B:
        if P.search(t(r)): add(r,'parkeerbelasting')
    for r in A+S:
        x=t(r)
        if not P.search(x): continue
        if re.search(r'parkeernorm|parkeerbehoefte|omgevingsvergunning|bestemmingsplan|omgevingsplan|bouwplan',x): continue
        if re.search(r'vergunning|bezoek|wachtlijst|ontheffing',x): add(r,'vergunningen')
        elif re.search(r'verbod|verkeersbesluit|gehandicapt|invalid|wahv|wegsleep|verwijder|bord|rvv|stilstaan',x): add(r,'parkeerverbod')
json.dump(out,open('data/kandidaten.json','w'),ensure_ascii=False)
print('jaar  belasting  verbod  vergunning')
for y in [2023,2024,2025,2026]: print(y, cnt.get((y,'parkeerbelasting'),0), cnt.get((y,'parkeerverbod'),0), cnt.get((y,'vergunningen'),0))
print('totaal',len(out))

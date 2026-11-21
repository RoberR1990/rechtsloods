"""Selectie bezwaar-beroep uit feeds (titel+inhoudsindicatie). python3 -I scripts/bezwaar/select.py <feedmap> <uit.json>
Thema's (rubrieken): dwangsom-niet-tijdig, bezwaartermijn-verschoonbaar, hoorplicht, motivering, proceskosten, bestuurlijke-lus."""
import sys,os,json,re,collections
F,OUT=sys.argv[1:3]
TH={
 'dwangsom-niet-tijdig':r'wet dwangsom|dwangsom (bij|wegens|vanwege) (het )?niet tijdig|niet tijdig (beslist|beslissen|besloten|genomen)|niet[- ]tijdig beslissen|ingebrekestelling.{0,60}(beslis|besluit)|\b4:1[57]\b|beslistermijn|beroep (wegens|bij) niet tijdig|\b6:2\b.{0,40}\b6:12\b',
 'bezwaartermijn-verschoonbaar':r'bezwaartermijn|bezwaarfrist|beroepstermijn|beroepstermijn|termijn (voor|waarbinnen).{0,30}(bezwaar|beroep)|termijnoverschrijding|overschrijding van de (bezwaar|beroep)|verschoonbaar|\b6:(7|8|9|10|11)\b|te laat (bezwaar|beroep|ingediend|gemaakt)|niet-ontvankelijk.{0,60}(termijn|te laat)',
 'hoorplicht':r'hoorplicht|hoorzitting|hoorverslag|niet gehoord|niet is gehoord|hoor(en|t) van (belanghebbenden|appellant|bezwaarmaker)|van het horen (af)?zien|afzien van (het )?horen|\b7:(2|3)\b',
 'motivering':r'motiveringsgebrek|motiveringsplicht|motiveringsbeginsel|onvoldoende gemotiveerd|ondeugdelijk gemotiveerd|deugdelijk(e)? motivering|\b7:12\b|\b3:(46|47)\b',
 'proceskosten':r'proceskostenvergoeding.{0,80}(bezwaar|forfait|gemachtigde|rechtsbijstand)|(bezwaar|gemachtigde).{0,80}proceskostenvergoeding|besluit proceskosten|\b7:15\b|vergoeding van (de )?(in bezwaar|door .{0,30} gemaakte) kosten',
 'bestuurlijke-lus':r'bestuurlijke lus|\b8:51a\b|\b8:51b\b|\b8:51c\b|\b8:51d\b|\b8:80a\b|\b8:80b\b|tussenuitspraak.{0,120}(herstel|gebrek)',
}
RX={k:re.compile(v) for k,v in TH.items()}
HOOG=re.compile(r'Raad van State|Centrale Raad|College van Beroep')
VREEM=re.compile(r'vreemdeling|asiel|verblijfsvergunning|vw 2000|terugkeerbesluit|\bmvv\b|inreisverbod|\bind\b|naturalisatie|toeslagen|belastingdienst/')
rows={}
for f in sorted(os.listdir(F)):
    k=f[:-9] if False else re.match(r'[a-z]+',f).group(0);y=int(re.search(r'\d{4}',f).group(0))
    for r in json.load(open(f'{F}/{f}')):
        x=(r['title']+' '+r['summary']).lower()
        if VREEM.search(x): continue
        hit=[t for t,R in RX.items() if R.search(x)]
        if not hit: continue
        t=r['title'].split(', ');inst=t[1] if len(t)>1 else ''
        o=rows.setdefault(r['ecli'],{'ecli':r['ecli'],'jaar':y,'bron':k,'instantie':inst,'rubrieken':[],'summary':r['summary'],'prio_instantie':1 if HOOG.search(inst) else 3})
        for h in hit:
            if h not in o['rubrieken']: o['rubrieken'].append(h)
K=list(rows.values());json.dump(K,open(OUT,'w'),ensure_ascii=False)
print(len(K),dict(collections.Counter(k['bron'] for k in K)));print(dict(collections.Counter(r for k in K for r in k['rubrieken'])))
print('jaren',dict(sorted(collections.Counter(k['jaar'] for k in K).items())))

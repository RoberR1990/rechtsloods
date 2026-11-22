"""Stand-invoer per onderwerp uit laag 2 (uitspraken zonder inhoudsindicatie). python3 prep_stand_bb.py <uitmap>"""
import json,glob,collections,sys,re,os
OUT=sys.argv[1]
T=json.load(open('data/dom/bezwaar-beroep/taxonomie.json'))
inst={'RBROT':'Rechtbank Rotterdam','RVS':'Raad van State','CRVB':'Centrale Raad van Beroep','CBB':'College van Beroep voor het bedrijfsleven'}
per=collections.defaultdict(lambda:collections.defaultdict(list))
for f in sorted(glob.glob('data/uit_v3/bezwaar-beroep/*.json')):
    d=json.load(open(f))
    if not d.get('relevant'): continue
    p=d['ecli'].split(':')
    it={'ecli':d['ecli'],'instantie':inst.get(p[2],p[2]),'jaar':p[3],'procesvorm':d.get('procesvorm'),'titel':d.get('titel'),'uitkomst':d.get('uitkomst'),
        'kern':d.get('kern'),'rechtsregel':d.get('rechtsregel'),'samenvatting':d.get('samenvatting'),'uitkomst_toelichting':d.get('uitkomst_toelichting')}
    per[d['onderwerp']][d['sub']].append(it)
os.makedirs(OUT,exist_ok=True)
for o,subs in per.items():
    blok={s:{'label':T[o]['sub'].get(s,{}).get('label',s) if isinstance(T[o]['sub'].get(s),dict) else s,'aantal_laag2':len(L),'uitspraken':L} for s,L in subs.items()}
    json.dump({'onderwerp':o,'label':T[o].get('label',o),'subs':blok},open(f'{OUT}/{o}.json','w'),ensure_ascii=False)
    print(o,{s:len(L) for s,L in subs.items()})

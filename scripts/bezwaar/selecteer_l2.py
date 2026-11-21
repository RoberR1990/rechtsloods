"""Selectie laag 2 bezwaar-beroep (besluit: RvS + Rb Rotterdam, max ±200, zonder sociaal-overlap).
Volgorde: (a) Rb Rotterdam waar gemeente partij is, (b) RvS nieuwste eerst, (c) dunne subonderwerpen aanvullen tot 6.
Uitvoer: lab/sets/bezwaar_l2.json (in_v3-bestandsnamen) + stdout telling + data/dom/bezwaar-beroep/selectie_l2.json (reden)."""
import json,glob,collections,re,os,sys
R=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))));MAX=int(sys.argv[1]) if len(sys.argv)>1 else 200
K={k['ecli']:k for k in json.load(open(f'{R}/data/dom/bezwaar-beroep/kandidaten.json'))}
recs=[]
for f in sorted(glob.glob(f'{R}/data/uit_l1/bezwaar-beroep/*.json')): recs+=[r for r in json.load(open(f)) if r.get('relevant')]
ok=[r for r in recs if r['zekerheid']!='laag' and 'sociaal' not in K[r['ecli']]['overlap'] and r['uitkomst']!='alleen procedure' or (r['zekerheid']!='laag' and 'sociaal' not in K[r['ecli']]['overlap'] and r['sub']!='overig')]
ok=[r for r in ok if 'sociaal' not in K[r['ecli']]['overlap']]
def gem(r):
    w=(r['partijen'].get('wederpartij') or '').lower();return r['partijen'].get('gemeente_is_partij') or bool(re.search(r'college|burgemeester|gemeente',w))
bron=lambda r:K[r['ecli']]['bron']
sel={};why={}
def add(r,w,cap=None):
    if r['ecli'] not in sel and len(sel)<(cap or MAX): sel[r['ecli']]=r;why[r['ecli']]=w
for r in sorted([r for r in ok if bron(r)=='rbrot' and gem(r)],key=lambda r:K[r['ecli']]['jaar'],reverse=True): add(r,'a: Rb Rotterdam, gemeente partij',100)
na=len(sel)
pb=collections.Counter()
for r in sorted([r for r in ok if bron(r)=='rvs'],key=lambda r:K[r['ecli']]['jaar'],reverse=True):
    if pb[r['onderwerp']]<18: add(r,'b: Raad van State, nieuwste eerst (max 18 per onderwerp)',180);pb[r['onderwerp']]+=1
nb=len(sel)-na
per=collections.Counter((r['onderwerp'],r['sub']) for r in sel.values())
for r in sorted(ok,key=lambda r:(bron(r)!='crvb',-K[r['ecli']]['jaar'])):
    s=(r['onderwerp'],r['sub'])
    if per[s]<6 and r['ecli'] not in sel and r['sub']!='overig' and bron(r) in('crvb','cbb','rbrot'): add(r,'c: dun subonderwerp aanvullen');per[s]+=1
namen=sorted(e.replace(':','_')+'.json' for e in sel)
os.makedirs(f'{R}/lab/sets',exist_ok=True);json.dump(namen,open(f'{R}/lab/sets/bezwaar_l2.json','w'),indent=0)
json.dump(why,open(f'{R}/data/dom/bezwaar-beroep/selectie_l2.json','w'),indent=0)
c=collections.Counter(why.values());print('totaal',len(sel),dict(c));print(dict(collections.Counter(r['onderwerp'] for r in sel.values())))
print('kandidaten rbrot gem partij',sum(1 for r in ok if bron(r)=='rbrot' and gem(r)),'rvs',sum(1 for r in ok if bron(r)=='rvs'))

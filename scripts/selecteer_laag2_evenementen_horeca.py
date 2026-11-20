"""Selectie laag 2 voor evenementen-horeca. python3 selecteer_laag2_evenementen_horeca.py [CAP=400]
Prioriteit: (a) Rotterdam als partij, (b) hoogste rechter/hoven nieuwste eerst (zonder 'alleen procedure'),
(c) dunne subonderwerpen aanvullen tot 12. Schrijft data/dom/evenementen-horeca/laag2_selectie.json (ecli -> reden)."""
import json,os,sys,collections
D='/home/claude/data';S='evenementen-horeca';CAP=int(sys.argv[1]) if len(sys.argv)>1 else 400
L={}
for f in os.listdir(f'{D}/uit_l1/{S}'):
    for o in json.load(open(f'{D}/uit_l1/{S}/{f}')): L[o['ecli']]=o
U={u['ecli']:u for u in json.load(open(f'{D}/dom/{S}/uitspraken.json'))}
rel={e:o for e,o in L.items() if o.get('relevant') and e in U}
sel={}
def add(e,r,cap=None):
    if e not in sel and len(sel)<(cap or CAP): sel[e]=r
for e,o in sorted(rel.items(),key=lambda x:U[x[0]]['datum'],reverse=True):
    if U[e]['rotterdam']: add(e,'a: Rotterdam partij')
for e,o in sorted(rel.items(),key=lambda x:U[x[0]]['datum'],reverse=True):
    if U[e]['prio']==1 and o['uitkomst']!='alleen procedure' and o['procesvorm']!='cassatie belang der wet': add(e,'b: hoogste rechter/hof',CAP-70)
cnt=collections.Counter((rel[e]['onderwerp'],rel[e]['sub']) for e in sel)
for e,o in sorted(rel.items(),key=lambda x:U[x[0]]['datum'],reverse=True):
    k=(o['onderwerp'],o['sub'])
    if e not in sel and cnt[k]<12 and o['uitkomst']!='alleen procedure': 
        before=len(sel);add(e,'c: dun subonderwerp aanvullen')
        if len(sel)>before: cnt[k]+=1
json.dump(sel,open(f'{D}/dom/{S}/laag2_selectie.json','w'),indent=0)
print('relevant',len(rel),'| geselecteerd',len(sel),collections.Counter(v[:1] for v in sel.values()))
print('sub-dekking',sorted(collections.Counter((rel[e]['onderwerp'],rel[e]['sub']) for e in sel).items(),key=lambda x:x[1])[:8])
print('gem. tekens',sum(U[e]['tekens'] for e in sel)//max(len(sel),1))

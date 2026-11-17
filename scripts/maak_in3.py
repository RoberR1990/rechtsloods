"""Maakt data/proef/in3/<ECLI>.json (invoer voor verrijking/check_uit) uit data/uitspraken.json."""
import json,os
D='/home/claude/data' if os.path.exists('/home/claude/data/uitspraken.json') else os.path.join(os.path.dirname(__file__),'..','data')
o=os.path.join(D,'proef','in3');os.makedirs(o,exist_ok=True)
K=['ecli','instantie','datum','procedure','rechtsgebied','inhoud','gemeente','beslissing','onderwerp']
for u in json.load(open(os.path.join(D,'uitspraken.json'))):
    x={k:u.get(k) for k in K};x['alineas']=[{'id':a['id'],'rov':a.get('rov'),'t':a['t']} for a in u['alineas']]
    json.dump(x,open(os.path.join(o,u['ecli'].replace(':','_')+'.json'),'w'),ensure_ascii=False)
print('in3 klaar')

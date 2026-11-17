"""Compacte invoer voor laag 1: python3 maak_in_l1.py <slug>
Per uitspraak: metadata, inhoudsindicatie, kop-alinea's (partijen) en de beslissing, met alinea-id's.
Schrijft data/in_l1/<slug>.json (dict ecli -> object)."""
import json,re,sys,os
s=sys.argv[1];U=json.load(open(f'/home/claude/data/dom/{s}/uitspraken.json'))
BES=re.compile(r'^(de )?(beslissing|uitspraak|conclusie|dictum)\b',re.I)
out={}
for u in U:
    al=u['alineas'];kop=[]
    for a in al[:18]:
        if len(a['t'])<260: kop.append({'id':a['id'],'t':a['t']})
    st=None
    for i in range(len(al)-1,-1,-1):
        t=re.sub(r'^[\d.\s]+','',al[i]['t']).strip()
        if len(t)<60 and BES.match(t): st=i;break
    bes=[]
    if st is not None:
        n=0
        for a in al[st:st+14]:
            if n>1800: break
            bes.append({'id':a['id'],'t':a['t'][:600]});n+=len(a['t'][:600])
    DICT=re.compile(r'(ongegrond|gegrond|vernietigt|bevestigt|veroordeelt|verklaart|wijst|niet-ontvankelijk|verwerpt|vrijspreekt|spreekt .* vrij|handhaaft|bekrachtigt|vermindert|vernietigd)',re.I)
    if not any(DICT.search(a['t']) for a in bes):
        bes=[];n=0
        for a in [a for a in al if DICT.search(a['t'])][-6:]:
            if n>1800: break
            bes.append({'id':a['id'],'t':a['t'][:500]});n+=len(a['t'][:500])
    out[u['ecli']]={'ecli':u['ecli'],'instantie':u['instantie'],'datum':u['datum'],'procedure':u['procedure'],'rechtsgebied':u['rechtsgebied'],
        'inhoud':(u.get('inhoud') or '')[:1500],'gemeente_meta':u.get('gemeente'),'kop':kop,'beslissing':bes}
os.makedirs('/home/claude/data/in_l1',exist_ok=True)
json.dump(out,open(f'/home/claude/data/in_l1/{s}.json','w'),ensure_ascii=False)
print(s,len(out),'uitspraken; gem. tekens',sum(len(json.dumps(v,ensure_ascii=False)) for v in out.values())//max(len(out),1))

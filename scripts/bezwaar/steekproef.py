"""Precisiesteekproef: python3 -I steekproef.py <kand.json> <uitmap> [n] [seed]  -> <uitmap>/in_NN.json (batches van 25) + sleutel.json
Haalt volledige tekst op (curl), maakt per uitspraak een korte invoer: titel, inhoudsindicatie, alinea's met themawoorden (max 2500 tekens)."""
import sys,os,json,re,random,subprocess,html,importlib.util
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
K=json.load(open(sys.argv[1]));O=sys.argv[2];n=int(sys.argv[3]) if len(sys.argv)>3 else 100;random.seed(int(sys.argv[4]) if len(sys.argv)>4 else 7)
os.makedirs(O,exist_ok=True)
sp=importlib.util.spec_from_file_location('sel',os.path.dirname(os.path.abspath(__file__))+'/select.py')
TH=re.findall(r"^ '([a-z-]+)':r'(.*)',?$",open(os.path.dirname(os.path.abspath(__file__))+'/select.py').read(),re.M)
RX={a:re.compile(b) for a,b in TH}
S=random.sample(K,n);items=[]
for k in S:
    x=subprocess.run(['curl','-s','-m','60',f"https://data.rechtspraak.nl/uitspraken/content?id={k['ecli']}"],capture_output=True,text=True).stdout
    t=re.sub(r'<[^>]+>','\n',x);t=html.unescape(t);ps=[re.sub(r'\s+',' ',p).strip() for p in t.split('\n') if len(p.strip())>40]
    hits=[p for p in ps if any(RX[r].search(p.lower()) for r in k['rubrieken'])]
    items.append({'ecli':k['ecli'],'instantie':k['instantie'],'jaar':k['jaar'],'themas_regex':k['rubrieken'],'inhoudsindicatie':k['summary'],'passages':[p[:600] for p in hits[:5]],'n_passages':len(hits),'tekens':len(t)})
json.dump({i['ecli']:{'themas':i['themas_regex']} for i in items},open(f'{O}/sleutel.json','w'))
for b in range(0,n,25): json.dump(items[b:b+25],open(f'{O}/in_{b//25:02d}.json','w'),ensure_ascii=False,indent=0)
print(n,'items',sum(i['n_passages']==0 for i in items),'zonder passage')

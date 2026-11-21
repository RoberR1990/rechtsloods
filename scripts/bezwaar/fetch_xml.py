"""python3 -I fetch_xml.py <kandidaten.json> <xmlmap> [workers]  (idempotent)"""
import json,os,sys,subprocess,time
from concurrent.futures import ThreadPoolExecutor
K=json.load(open(sys.argv[1]));o=sys.argv[2];w=int(sys.argv[3]) if len(sys.argv)>3 else 8;os.makedirs(o,exist_ok=True)
def get(r):
    f=f"{o}/{r['ecli'].replace(':','_')}.xml"
    for _ in range(3):
        if os.path.exists(f) and os.path.getsize(f)>500: return 1
        subprocess.run(["curl","-s","-m","60","-o",f,f"https://data.rechtspraak.nl/uitspraken/content?id={r['ecli']}"]);time.sleep(0.05)
    return 0
with ThreadPoolExecutor(w) as ex: ok=sum(ex.map(get,K))
print('opgehaald',ok,'/',len(K))

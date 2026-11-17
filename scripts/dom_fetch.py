"""Haal XML op voor een domein: python3 dom_fetch.py <slug> [workers]  -> data/xml_dom/<slug>/"""
import json,os,sys,subprocess,time
from concurrent.futures import ThreadPoolExecutor
s=sys.argv[1];w=int(sys.argv[2]) if len(sys.argv)>2 else 6
K=json.load(open(f'/home/claude/data/dom/{s}/kandidaten.json'));o=f'/home/claude/data/xml_dom/{s}';os.makedirs(o,exist_ok=True)
def get(r):
    f=f"{o}/{r['ecli'].replace(':','_')}.xml"
    for _ in range(3):
        if os.path.exists(f) and os.path.getsize(f)>500: return 1
        subprocess.run(["curl","-s","-m","60","-o",f,f"https://data.rechtspraak.nl/uitspraken/content?id={r['ecli']}"]);time.sleep(0.1)
    return 0
with ThreadPoolExecutor(w) as ex: ok=sum(ex.map(get,K))
print(s,'opgehaald',ok,'/',len(K))

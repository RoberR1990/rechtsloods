import subprocess, re, sys, time, json, html
subj, d1, d2, out = sys.argv[1:5]
import os
if os.path.exists(out) and os.path.getsize(out)>1000: print(out,"bestaat"); sys.exit()
base="https://data.rechtspraak.nl/uitspraken/zoeken"
rows=[]; frm=0
while True:
    url=f"{base}?subject={subj.replace('#','%23')}&date={d1}&date={d2}&max=1000&from={frm}&return=DOC"
    x=subprocess.run(["curl","-s","-m","120",url],capture_output=True,text=True).stdout
    ents=re.findall(r"<entry>(.*?)</entry>",x,re.S)
    for e in ents:
        g=lambda t: html.unescape((re.search(rf"<{t}[^>]*>(.*?)</{t}>",e,re.S) or [None,""])[1])
        rows.append({"ecli":g("id"),"title":g("title"),"summary":g("summary")})
    if len(ents)<1000: break
    frm+=1000; time.sleep(1)
json.dump(rows,open(out,"w"),ensure_ascii=False)
tot=re.search(r"Aantal gevonden ECLI's: (\d+)",x)
print(out,len(rows))

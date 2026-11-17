"""Werkt het blok 'Voortgang nachtrun' in docs/STAND.md bij (tussen markers)."""
import subprocess,re,datetime,json,os
r=subprocess.run(['python3','/home/claude/scripts/volgende.py','stand'],capture_output=True,text=True).stdout
D='/home/claude/data';n3=len(os.listdir(f'{D}/uit_v3/parkeren'))
nl1={s:sum(len(json.load(open(f'{D}/uit_l1/{s}/{f}'))) for f in os.listdir(f'{D}/uit_l1/{s}')) for s in os.listdir(f'{D}/uit_l1')}
t=datetime.datetime.now().strftime('%d-%m %H:%M')
blok=f"<!--voortgang-->\n### Voortgang nachtrun (automatisch, {t} UTC)\n```\n{r}```\n- Parkeren v3: {n3} samenvattingen in `data/uit_v3/parkeren/`.\n- Laag 1 per domein (uitspraken): {nl1}\n- Hervatten: `python3 scripts/volgende.py stand`, dan `scripts/golf.sh <sonnet> <haiku> <l1>` en per batch-id een subagent met `scripts/verrijk_v3.md` of `scripts/verrijk_l1.md`.\n<!--/voortgang-->"
p='/home/claude/rechtzoeker/docs/STAND.md';s=open(p).read()
s=re.sub(r'<!--voortgang-->.*?<!--/voortgang-->',blok,s,flags=re.S) if '<!--voortgang-->' in s else s+'\n'+blok+'\n'
open(p,'w').write(s)

"""Voorbereiding laag 1/laag 2 voor subsidies (stap 3), repo-relatief en idempotent.

  python3 -I scripts/subsidies_prep.py links           # /home/claude/{data,scripts,site,rechtzoeker} -> deze repo (zoals setup.sh), alleen als ze ontbreken
  python3 -I scripts/subsidies_prep.py fetch [workers]  # XML van alle kandidaten -> data/xml_dom/subsidies/ (bestaande overslaan)
  python3 -I scripts/subsidies_prep.py parse            # -> data/dom/subsidies/uitspraken.json (gitignored): + rubrieken, prio, rotterdam
  python3 -I scripts/subsidies_prep.py in               # maak_in_l1 + maak_in_v3 + laag-1-batches van 25 (scripts/maak_batches.py)

Prio zoals dom_parse.py: 1 = hoge instantie (CRvB, RvS, HR/PHR, hof), 2 = Rotterdam partij (rechtbank), 3 = rest.
Rotterdam als partij: regex config.rotterdam_partij op de eerste 25 alinea's (besluit B11), niet de ROT-regex van dom_parse.py.
Uitvoer met uitspraaktekst blijft buiten git (data/xml*, data/in_*, data/dom/*/uitspraken.json staan in .gitignore)."""
import json, os, re, sys, subprocess, time, collections
from concurrent.futures import ThreadPoolExecutor

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); S = 'subsidies'
D = f'{R}/data/dom/{S}'; X = f'{R}/data/xml_dom/{S}'
cmd = sys.argv[1]


def kandidaten():
    vol = f'{R}/data/feeds/kandidaten_{S}.json'  # met inhoudsindicatie (gitignored)
    return json.load(open(vol if os.path.exists(vol) else f'{D}/kandidaten.json'))


if cmd == 'links':
    os.makedirs('/home/claude', exist_ok=True)
    for naam, doel in (('data', f'{R}/data'), ('scripts', f'{R}/scripts'), ('site', f'{R}/site'), ('rechtzoeker', R)):
        p = f'/home/claude/{naam}'
        if os.path.lexists(p):
            print(p, '->', os.path.realpath(p), '(bestaat, niet aangeraakt)')
        else:
            os.symlink(doel, p); print(p, '->', doel)

elif cmd == 'fetch':
    w = int(sys.argv[2]) if len(sys.argv) > 2 else 6; os.makedirs(X, exist_ok=True); K = kandidaten()
    def get(k):
        f = f"{X}/{k['ecli'].replace(':', '_')}.xml"
        for _ in range(3):
            if os.path.exists(f) and os.path.getsize(f) > 500: return 1
            subprocess.run(['curl', '-s', '-m', '60', '-o', f, f"https://data.rechtspraak.nl/uitspraken/content?id={k['ecli']}"]); time.sleep(0.1)
        return 0
    with ThreadPoolExecutor(w) as ex: ok = sum(ex.map(get, K))
    print(S, 'opgehaald', ok, '/', len(K))

elif cmd == 'parse':
    src = open(f'{R}/scripts/parse.py').read().replace(
        'K = {r["ecli"]: r for r in json.load(open("/home/claude/data/kandidaten2.json"))}', 'K = {}')  # parse.py laadt anders parkeren-kandidaten
    P = {}; exec(compile(src, 'parse', 'exec'), P)
    cfg = json.load(open(f'{D}/config.json')); ROT = re.compile(cfg['rotterdam_partij'], re.I)
    K = {k['ecli']: k for k in kandidaten()}
    P['K'].update({e: {'summary': k.get('summary', ''), 'onderwerp': None, 'extra': []} for e, k in K.items()})
    out, err, afgevallen = [], 0, []
    for f in sorted(os.listdir(X)) if os.path.isdir(X) else []:
        e = f[:-4].replace('_', ':')
        if e not in K or os.path.getsize(f'{X}/{f}') < 500: continue
        try: u = P['parse'](f'{X}/{f}')
        except Exception: err += 1; continue
        k = K[e]; u['onderwerp'] = None; u['rubrieken'] = k['rubrieken']; u['wetcodes'] = k.get('wetcodes', []); u['overlap'] = k.get('overlap', [])
        kop = ' '.join(a['t'] for a in u['alineas'][:25])
        u['rotterdam'] = bool(ROT.search(kop))
        if k.get('reden') == 'orgaan-onbekend':  # orgaan stond niet in de inhoudsindicatie: kop moet een gemeentelijk orgaan noemen
            kl = kop.lower()
            if not re.search(r'gemeente|burgemeester|wethouder|college van b|gemeenteraad|stadsdeel|deelgemeente', kl) or re.search(r'gedeputeerde staten|\bminister\b|staatssecretaris|dijkgraaf', kl):
                afgevallen.append(e); continue
        u['prio'] = 1 if k['prio_instantie'] == 1 else (2 if u['rotterdam'] else 3)
        u['dictum_gevonden'] = bool(u.get('beslissing'))
        out.append(u)
    json.dump(out, open(f'{D}/uitspraken.json', 'w'), ensure_ascii=False); json.dump(afgevallen, open(f'{D}/afgevallen_orgaan.json', 'w'))
    print('afgevallen na kop-check (orgaan geen gemeente):', len(afgevallen))
    print(S, len(out), 'geparsed,', err, 'fouten | prio', dict(collections.Counter(u['prio'] for u in out)),
          '| rotterdam', sum(u['rotterdam'] for u in out), '| zonder dictum-sectie', sum(not u['dictum_gevonden'] for u in out),
          '| ontbreekt nog', len(K) - len(out))

elif cmd == 'in':
    os.makedirs(f'{R}/data/batches', exist_ok=True)
    for a in (['maak_in_l1.py', S], ['maak_in_v3.py', S], ['maak_batches.py', 'l1', S, '25']):
        r = subprocess.run([sys.executable, f'{R}/scripts/{a[0]}'] + a[1:], capture_output=True, text=True)
        print(a[0], (r.stdout + r.stderr).strip().splitlines()[-1:])
else:
    sys.exit(__doc__)

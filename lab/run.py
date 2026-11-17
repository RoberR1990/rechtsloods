"""Pilot modelmix: draai de bestaande verrijk-instructie via OpenRouter en check met de bestaande scripts.

Gebruik:
  python3 -I lab/run.py v3 <slug> <model> <setbestand> <run-id> [--max N] [--par 8]
  python3 -I lab/run.py l1 <slug> <model> <setbestand> <run-id> [--max N] [--par 8]

- setbestand: JSON-lijst met in_v3-bestandsnamen (ECLI_NL_..json) of ECLI's.
- Uitvoer: lab/runs/<run-id>/ (D/uit_v3|uit_l1, raw/, usage.jsonl, prompt.txt, check.txt, meta.json).
- Kosten komen uit het usage-veld van OpenRouter. Harde stop: lab/ledger.jsonl totaal >= BUDGET_STOP.
- Eén herstelronde: geeft de check fouten, dan krijgt het model de fouten terug (zoals een subagent die herstelt).
- Sleutel: ~/.secrets/openrouter_key (nooit in de repo).
"""
import json, os, re, sys, time, threading, subprocess, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor

BUDGET_STOP = float(os.environ.get("LAB_BUDGET_STOP", "20.06"))  # USD totaal ledger: pilot $7,06 + 80% van nieuw budget EUR 15 (~$16,30)
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repo
DATA = os.path.join(R, 'data'); SCR = os.path.join(R, 'scripts'); LAB = os.path.join(R, 'lab')
LEDGER = os.path.join(LAB, 'ledger.jsonl')
KEY = open(os.environ.get('OPENROUTER_KEY_FILE', '/home/claude/.secrets/openrouter_key')).read().strip()
lock = threading.Lock()

def spent():
    if not os.path.exists(LEDGER): return 0.0
    return sum(json.loads(l).get('cost', 0) or 0 for l in open(LEDGER) if l.strip())

def call(model, messages, max_tokens):
    body = {'model': model, 'messages': messages, 'max_tokens': max_tokens, 'temperature': 0,
            'response_format': {'type': 'json_object'}, 'usage': {'include': True}, 'provider': {'sort': 'price'}}
    ef = os.environ.get('LAB_EFFORT')
    if ef == 'off': body['reasoning'] = {'enabled': False}
    elif ef and ef.startswith('budget:'): body['reasoning'] = {'max_tokens': int(ef[7:])}
    elif ef: body['reasoning'] = {'effort': ef}
    req = urllib.request.Request('https://openrouter.ai/api/v1/chat/completions', data=json.dumps(body).encode(),
                                 headers={'Authorization': f'Bearer {KEY}', 'Content-Type': 'application/json',
                                          'X-Title': 'Rechtsloods pilot modelmix'})
    for poging in range(4):
        try:
            with urllib.request.urlopen(req, timeout=300) as r: return json.load(r)
        except urllib.error.HTTPError as e:
            msg = e.read().decode()[:300]
            if e.code in (429, 500, 502, 503, 504) and poging < 3: time.sleep(5 * (poging + 1)); continue
            return {'error': f'{e.code} {msg}'}
        except Exception as e:
            if poging < 3: time.sleep(5); continue
            return {'error': str(e)[:300]}

def parse(txt):
    txt = (txt or '').strip()
    txt = re.sub(r'^```(json)?|```$', '', txt).strip()
    try: return json.loads(txt)
    except Exception:
        m = re.search(r'\{.*\}', txt, re.S)
        if m:
            try: return json.loads(m.group(0))
            except Exception: pass
    return None

NORM = {'n': 0}
def fixbron(o):
    """Deterministische vormfix voor alle modellen gelijk: bron ["[89]"] of "89" -> [89]. Telt hoe vaak."""
    if isinstance(o, dict):
        for k, v in o.items():
            if k == 'bron':
                vv = v if isinstance(v, list) else [v]
                new = []
                for x in vv:
                    if isinstance(x, str) and re.fullmatch(r'\s*\[?\s*\d+\s*\]?\s*', x): new.append(int(re.sub(r'\D', '', x)))
                    else: new.append(x)
                if new != v:
                    with lock: NORM['n'] += 1
                o[k] = new
            else: fixbron(v)
    elif isinstance(o, list):
        for x in o: fixbron(x)
    return o

def section(md, start, stop):
    i = md.index(start); j = md.index(stop, i) if stop else len(md)
    return md[i:j].strip()

def domfiles(slug):
    C = f'{DATA}/dom/{slug}'
    return {k: json.load(open(f'{C}/{k}.json')) for k in ('config', 'taxonomie', 'argumenten')}

def sysprompt(laag, slug):
    d = domfiles(slug); ctx = '\n\n'.join(f'## {k}.json\n```json\n{json.dumps(v, ensure_ascii=False)}\n```' for k, v in d.items())
    if laag == 'v3':
        md = open(f'{SCR}/verrijk_v3.md').read()
        body = section(md, '## Harde regels', '## Werkwijze')
        intro = ('Je bent een zorgvuldige jurist die voor collega\'s van een gemeente schrijft in gewone taal (B1). '
                 f'Domein: `{slug}`. Je krijgt één uitspraak (ingekorte tekst met alinea-id\'s tussen [ ]). '
                 'Maak het JSON-object volgens het schema hieronder. Antwoord met ALLEEN dat JSON-object, geen andere tekst.')
    else:
        md = open(f'{SCR}/verrijk_l1.md').read()
        body = section(md, '## Per uitspraak', '## Afronden')
        intro = ('Je deelt rechterlijke uitspraken in. Je schrijft GEEN samenvatting; alleen labels, plus één letterlijk citaat '
                 f'voor de uitkomst. Domein: `{slug}`. Je krijgt meerdere uitspraken. Antwoord met ALLEEN een JSON-object '
                 '{"items": [ ... ]} met één object per uitspraak, in dezelfde volgorde.')
    extra = os.environ.get('LAB_EXTRA')
    if extra: body += '\n\n' + open(extra).read()
    return f'{intro}\n\n# Domeininstellingen\n{ctx}\n\n{body}'

def toon_v3(slug, f):
    d = json.load(open(f'{DATA}/in_v3/{slug}/{f}'))
    out = [f"=== {f} | {d['ecli']} | {d['instantie']} | {d['datum']} | {d['procedure']} | {d['rechtsgebied']} | gemeente (metadata, kan fout zijn): {d.get('gemeente')}",
           'INHOUDSINDICATIE: ' + str(d['inhoud'])]
    rel = [r['ecli'] for r in d.get('relaties') or [] if r.get('ecli')]
    if rel: out.append('GERELATEERD (metadata): ' + ', '.join(rel))
    for a in d['alineas']: out.append(f"[{a['id']}]{'(r.o. ' + a['rov'] + ')' if a.get('rov') else ''} {a['t']}")
    return '\n'.join(out)

def toon_l1(I, e):
    d = I[e]
    return '\n'.join([f"=== {e} | {d['instantie']} | {d['datum']} | {d['procedure']} | gemeente (metadata): {d['gemeente_meta']}",
                      'INHOUDSINDICATIE: ' + d['inhoud'],
                      'KOP: ' + ' | '.join(f"[{a['id']}] {a['t']}" for a in d['kop']),
                      'BESLISSING: ' + (' '.join(f"[{a['id']}] {a['t']}" for a in d['beslissing']) or '(niet gevonden)')])

def sandbox(run, slug, laag):
    S = os.path.join(LAB, 'runs', run, 'D'); os.makedirs(S, exist_ok=True)
    for k in ('dom', 'in_v3'):
        p = os.path.join(S, k)
        if not os.path.lexists(p): os.symlink(os.path.join(DATA, k), p)
    os.makedirs(f'{S}/uit_v3/{slug}', exist_ok=True); os.makedirs(f'{S}/uit_l1/{slug}', exist_ok=True)
    os.makedirs(f'{S}/in_l1', exist_ok=True); os.makedirs(f'{S}/batches', exist_ok=True)
    return S

def checker(name, S, args):
    src = open(f'{SCR}/{name}').read().replace("'/home/claude/data'", repr(S))
    tmp = os.path.join(os.path.dirname(S), f'_{name}')
    open(tmp, 'w').write(src)
    r = subprocess.run([sys.executable, '-I', tmp] + args, capture_output=True, text=True)
    return r.stdout + r.stderr

def log_usage(run, model, item, resp, ronde):
    u = resp.get('usage') or {}
    rec = {'run': run, 'model': model, 'item': item, 'ronde': ronde, 'provider': resp.get('provider'),
           'prompt_tokens': u.get('prompt_tokens'), 'completion_tokens': u.get('completion_tokens'),
           'reasoning_tokens': (u.get('completion_tokens_details') or {}).get('reasoning_tokens'),
           'cached': (u.get('prompt_tokens_details') or {}).get('cached_tokens'),
           'cost': u.get('cost') or 0, 'error': resp.get('error'), 't': time.strftime('%Y-%m-%dT%H:%M:%S')}
    with lock:
        open(os.path.join(LAB, 'runs', run, 'usage.jsonl'), 'a').write(json.dumps(rec) + '\n')
        open(LEDGER, 'a').write(json.dumps(rec) + '\n')

def content(resp):
    try: return resp['choices'][0]['message']['content']
    except Exception: return None

def main():
    a = sys.argv[1:]; opt = {}
    while a and a[-1].lstrip('-').isdigit() and len(a) > 5: opt[a[-2]] = int(a[-1]); a = a[:-2]
    laag, slug, model, setf, run = a[:5]
    mx = opt.get('--max'); par = opt.get('--par', 8)
    items = json.load(open(setf))
    if mx: items = items[:mx]
    S = sandbox(run, slug, laag); RD = os.path.join(LAB, 'runs', run); os.makedirs(f'{RD}/raw', exist_ok=True)
    sp = sysprompt(laag, slug); open(f'{RD}/prompt.txt', 'w').write(sp)
    json.dump({'extra': os.environ.get('LAB_EXTRA'), 'effort': os.environ.get('LAB_EFFORT'), 'laag': laag, 'slug': slug, 'model': model, 'set': setf, 'n': len(items), 'start': time.strftime('%Y-%m-%dT%H:%M:%S')},
              open(f'{RD}/meta.json', 'w'), indent=1)
    stop = threading.Event()

    def guard():
        if spent() >= BUDGET_STOP: stop.set()
        return stop.is_set()

    if laag == 'v3lab':
        sp2 = sp + '\n\n# LET OP: labelmodus\nGeef ALLEEN een JSON-object met de velden ecli, relevant, onderwerp, sub, kenmerk, zaaktype, partijen (met gemeente_is_partij), procesvorm, uitkomst. Geen samenvatting, geen citaten. Bij een valse treffer: {"ecli":..., "relevant": false, "reden": "..."}.'
        open(f'{RD}/prompt.txt', 'w').write(sp2); os.makedirs(f'{S}/uit_lab/{slug}', exist_ok=True)
        def job(f):
            out = f'{S}/uit_lab/{slug}/{f}'
            if os.path.exists(out) or guard(): return
            resp = call(model, [{'role': 'system', 'content': sp2}, {'role': 'user', 'content': toon_v3(slug, f)}], 12000)
            log_usage(run, model, f, resp, 1); txt = content(resp); o = parse(txt)
            open(f'{RD}/raw/{f}.r1.txt', 'w').write(txt or json.dumps(resp)[:2000])
            if isinstance(o, dict) and isinstance(o.get('items'), list) and o['items']: o = o['items'][0]
            if isinstance(o, dict): json.dump(o, open(out, 'w'), ensure_ascii=False)
        with ThreadPoolExecutor(par) as ex: list(ex.map(job, items))
        rep = f'labels: {len(os.listdir(f"{S}/uit_lab/{slug}"))} van {len(items)}\n'
    elif laag == 'v3':
        def job(f):
            out = f'{S}/uit_v3/{slug}/{f}'
            if os.path.exists(out) or guard(): return
            msgs = [{'role': 'system', 'content': sp}, {'role': 'user', 'content': toon_v3(slug, f)}]
            resp = call(model, msgs, 24000); log_usage(run, model, f, resp, 1)
            txt = content(resp); o = fixbron(parse(txt))
            open(f'{RD}/raw/{f}.r1.txt', 'w').write(txt or json.dumps(resp)[:2000])
            if o is None: return
            json.dump(o, open(out, 'w'), ensure_ascii=False)
            fouten = [l for l in checker('check_uit_v3.py', S, [slug, f]).splitlines() if ' FOUT ' in l or 'ONTBREEKT' in l]
            if fouten and not guard():
                msgs += [{'role': 'assistant', 'content': txt},
                         {'role': 'user', 'content': 'De controle gaf deze fouten:\n' + '\n'.join(fouten) +
                          '\nHerstel ze. `bron` is een lijst met getallen, bijv. [12]. Citaten moeten letterlijk (exacte tekens) uit de EERSTE bron-alinea komen. Geef het volledige gecorrigeerde JSON-object.'}]
                resp = call(model, msgs, 24000); log_usage(run, model, f, resp, 2)
                txt2 = content(resp); o2 = fixbron(parse(txt2))
                open(f'{RD}/raw/{f}.r2.txt', 'w').write(txt2 or json.dumps(resp)[:2000])
                if o2 is not None: json.dump(o2, open(out, 'w'), ensure_ascii=False)
        with ThreadPoolExecutor(par) as ex: list(ex.map(job, items))
        rep = checker('check_uit_v3.py', S, [slug] + items)
    else:
        eclis = [x.replace('_', ':')[:-5] if x.endswith('.json') else x for x in items]
        p_in = f'{S}/in_l1/{slug}.json'
        if not os.path.exists(p_in):
            src = open(f'{SCR}/maak_in_l1.py').read().replace("'/home/claude/data", repr(S)[:-1])
            if slug == 'parkeren':  # parkeren heeft geen dom/parkeren/uitspraken.json
                src = src.replace("f'" + S + "/dom/{s}/uitspraken.json'", repr(f'{DATA}/uitspraken.json'))
            open(f'{RD}/_maak_in_l1.py', 'w').write(src)
            print(subprocess.run([sys.executable, '-I', f'{RD}/_maak_in_l1.py', slug], capture_output=True, text=True).stdout.strip())
        I = json.load(open(p_in))
        eclis = [e for e in eclis if e in I]
        B = [{'id': f'lab-{i // 10:03d}', 'eclis': eclis[i:i + 10]} for i in range(0, len(eclis), 10)]
        json.dump(B, open(f'{S}/batches/l1_{slug}.json', 'w'), indent=0)

        def job(b):
            out = f'{S}/uit_l1/{slug}/{b["id"]}.json'
            if os.path.exists(out) or guard(): return
            msgs = [{'role': 'system', 'content': sp}, {'role': 'user', 'content': '\n\n'.join(toon_l1(I, e) for e in b['eclis'])}]
            resp = call(model, msgs, 20000); log_usage(run, model, b['id'], resp, 1)
            txt = content(resp); o = fixbron(parse(txt))
            open(f'{RD}/raw/{b["id"]}.r1.txt', 'w').write(txt or json.dumps(resp)[:2000])
            L = (o or {}).get('items') if isinstance(o, dict) else o
            if not isinstance(L, list): return
            json.dump(L, open(out, 'w'), ensure_ascii=False)
            fouten = [l for l in checker('check_l1.py', S, [slug, b['id']]).splitlines() if 'FOUT ' in l or 'ontbreekt' in l]
            if fouten and not guard():
                msgs += [{'role': 'assistant', 'content': txt},
                         {'role': 'user', 'content': 'De controle gaf deze fouten:\n' + '\n'.join(fouten) +
                          '\nHerstel ze. `bron` is een lijst met getallen, bijv. [89]. Het citaat moet letterlijk uit de genoemde KOP- of BESLISSING-alinea komen. Geef het volledige gecorrigeerde {"items": [...]}.'}]
                resp = call(model, msgs, 20000); log_usage(run, model, b['id'], resp, 2)
                txt2 = content(resp); o2 = fixbron(parse(txt2))
                open(f'{RD}/raw/{b["id"]}.r2.txt', 'w').write(txt2 or json.dumps(resp)[:2000])
                L2 = (o2 or {}).get('items') if isinstance(o2, dict) else o2
                if isinstance(L2, list): json.dump(L2, open(out, 'w'), ensure_ascii=False)
        with ThreadPoolExecutor(par) as ex: list(ex.map(job, B))
        rep = checker('check_l1.py', S, [slug] + [b['id'] for b in B])
    open(f'{RD}/check.txt', 'w').write(rep)
    us = [json.loads(l) for l in open(f'{RD}/usage.jsonl')] if os.path.exists(f'{RD}/usage.jsonl') else []
    cost = sum(u['cost'] or 0 for u in us)
    print(f'{run}: {len(items)} items | calls {len(us)} | fouten-calls {sum(1 for u in us if u["error"])} | '
          f'kosten ${cost:.4f} | totaal pilot ${spent():.4f}' + (' | BUDGETSTOP' if stop.is_set() else ''))
    print('vormfix bron:', NORM['n'])
    json.dump(NORM, open(f'{RD}/vormfix.json', 'w'))
    print(rep.strip().splitlines()[-1] if rep.strip() else '(geen check)')

if __name__ == '__main__':
    main()

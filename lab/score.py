"""Scoor fase 1: python3 -I lab/score.py [prefix=f1]
Vergelijkt per model (laag 2 en laag 1) met de maatstaf in data/uit_v3/parkeren (relevant) en data/uit (niet-relevant, v2).
Consensus (vooraf vastgelegd in docs/pilot-modelmix-scope.md): de 3 mix-modellen zijn 'eens' als ze alle drie zonder
scriptfouten zijn en gelijk op KERN. Schrijft lab/score_<prefix>.json en print een tabel."""
import json, os, re, sys, collections
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); LAB = f'{R}/lab'; D = f'{R}/data'
P = sys.argv[1] if len(sys.argv) > 1 else 'f1'
MIX = ['deepseek-v4.1-flash', 'qwen3.8-flash', 'qwen3.7-plus']; ALLE = MIX + ['mistral-small-2603']
SET = json.load(open(f'{LAB}/sets/bench_parkeren.json')); G = json.load(open(f'{LAB}/sets/bench_parkeren_groepen.json'))
KERN = ['relevant', 'onderwerp', 'sub', 'zaaktype', 'procesvorm', 'uitkomst', 'gip']

def ref(f):
    p = f'{D}/uit_v3/parkeren/{f}'
    return json.load(open(p)) if os.path.exists(p) else {'relevant': False}

def kern(o):
    if not o: return None
    if o.get('relevant') is False: return {'relevant': False}
    pj = o.get('partijen') or {}
    return {'relevant': True, 'onderwerp': o.get('onderwerp'), 'sub': o.get('sub'), 'zaaktype': o.get('zaaktype'),
            'procesvorm': o.get('procesvorm'), 'uitkomst': o.get('uitkomst'), 'gip': pj.get('gemeente_is_partij'),
            'steunt': o.get('steunt'), 'args': sorted({b.get('arg') for b in o.get('bezwaargronden') or []}),
            'regeltype': (o.get('rechtsregel') or {}).get('type')}

def fouten(run):
    """bestand/ecli -> aantal FOUT-regels na herstel."""
    p = f'{LAB}/runs/{run}/check.txt'; F = collections.Counter()
    if not os.path.exists(p): return None
    if 'FOUTEN' not in open(p).read() and run.split('-')[1] == 'v3':  # check crashte op een bestand: per bestand opnieuw
        import subprocess
        chk = f'{LAB}/runs/{run}/_check_uit_v3.py'
        for f in SET:
            o = subprocess.run([sys.executable, '-I', chk, 'parkeren', f], capture_output=True, text=True)
            t = o.stdout + o.stderr
            if 'Traceback' in t: F[f] += 1
            else: F[f] += sum(1 for l in t.splitlines() if ' FOUT ' in l or 'ONTBREEKT' in l or 'GEEN GELDIGE' in l)
        return F
    for l in open(p):
        m = re.match(r'^(\S+\.json) (FOUT|ONTBREEKT|GEEN)', l) or re.match(r'^lab-\d+ (ECLI:\S+) (FOUT|ontbreekt)', l)
        if m: F[m.group(1)] += 1
    return F

def load(laag, m):
    run = f'{P}-{laag}-{m}'; S = f'{LAB}/runs/{run}/D'; out = {}
    if laag == 'v3':
        for f in SET:
            p = f'{S}/uit_v3/parkeren/{f}'
            try: out[f] = json.load(open(p))
            except Exception: out[f] = None
        F = fouten(run) or {}
        ok = {f: out[f] is not None and F.get(f, 0) == 0 for f in SET}
    else:
        byecli = {}
        d = f'{S}/uit_l1/parkeren'
        if os.path.isdir(d):
            for fn in os.listdir(d):
                try:
                    for o in json.load(open(f'{d}/{fn}')):
                        if isinstance(o, dict) and o.get('ecli'): byecli[o['ecli']] = o
                except Exception: pass
        F = fouten(run) or {}
        for f in SET:
            e = f.replace('_', ':')[:-5]; out[f] = byecli.get(e)
        ok = {f: out[f] is not None and F.get(f.replace('_', ':')[:-5], 0) == 0 for f in SET}
    us = [json.loads(l) for l in open(f'{LAB}/runs/{run}/usage.jsonl')] if os.path.exists(f'{LAB}/runs/{run}/usage.jsonl') else []
    return out, ok, sum(u['cost'] or 0 for u in us), us

def gelijk(a, b, k):
    if a is None or b is None: return False
    if k == 'relevant' or not a.get('relevant', True) or not b.get('relevant', True): return a.get('relevant') == b.get('relevant') if k == 'relevant' else (a.get('relevant') == b.get('relevant'))
    return a.get(k) == b.get(k)

res = {}
for laag in ('v3', 'l1'):
    res[laag] = {}; K = {}
    for m in ALLE:
        out, ok, cost, us = load(laag, m)
        K[m] = (out, ok)
        rk = {f: kern(ref(f)) for f in SET}; mk = {f: kern(out[f]) for f in SET}
        r = {'n': len(SET), 'uitvoer': sum(out[f] is not None for f in SET), 'check_ok': sum(ok.values()),
             'kosten': round(cost, 4), 'kosten_per_1000': round(1000 * cost / len(SET), 2), 'calls': len(us),
             'herstel': sum(1 for u in us if u['ronde'] == 2)}
        for k in KERN + ['steunt', 'args', 'regeltype']:
            fs = [f for f in SET if rk[f]['relevant'] and mk[f] and mk[f]['relevant']] if k not in ('relevant',) else SET
            r[k] = round(100 * sum(gelijk(mk[f], rk[f], k) for f in fs) / max(len(fs), 1), 1)
        r['kern_alles'] = round(100 * sum(mk[f] is not None and all(gelijk(mk[f], rk[f], k) for k in KERN) for f in SET) / len(SET), 1)
        res[laag][m] = r
    # consensus
    cons = []
    for f in SET:
        ks = [kern(K[m][0][f]) for m in MIX]
        if all(K[m][1][f] for m in MIX) and all(k is not None for k in ks) and all(all(gelijk(ks[0], x, k) for k in KERN) for x in ks[1:]):
            cons.append(f)
    rk = {f: kern(ref(f)) for f in SET}
    ck = {f: kern(K[MIX[0]][0][f]) for f in cons}
    res[laag]['consensus'] = {'eens': len(cons), 'eens_pct': round(100 * len(cons) / len(SET), 1),
                              'kern_alles_gelijk_aan_maatstaf': round(100 * sum(all(gelijk(ck[f], rk[f], k) for k in KERN) for f in cons) / max(len(cons), 1), 1),
                              'uitkomst_gelijk': round(100 * sum(gelijk(ck[f], rk[f], 'uitkomst') for f in cons) / max(len(cons), 1), 1),
                              'per_groep': {g: sum(f in cons for f in fs) for g, fs in G.items()}, 'bestanden': cons}
json.dump(res, open(f'{LAB}/score_{P}.json', 'w'), indent=1, ensure_ascii=False)
for laag in res:
    print(f'\n== {laag}')
    cols = ['uitvoer', 'check_ok', 'herstel', 'kosten', 'kosten_per_1000', 'relevant', 'onderwerp', 'sub', 'zaaktype', 'procesvorm', 'uitkomst', 'gip', 'steunt', 'args', 'regeltype', 'kern_alles']
    print('model'.ljust(20) + ' '.join(c[:8].rjust(8) for c in cols))
    for m in ALLE: print(m[:20].ljust(20) + ' '.join(str(res[laag][m][c]).rjust(8) for c in cols))
    c = res[laag]['consensus']; print('consensus', {k: v for k, v in c.items() if k != 'bestanden'})

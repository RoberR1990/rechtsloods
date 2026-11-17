"""Scoor fase 2 (toepassing, geen maatstaf): python3 -I lab/score_toep.py
AVG laag 2 (v3b, DeepSeek + Qwen3.8 Flash) en BPM laag 1 (3 modellen). Meet: uitvoer, scriptchecks, consensus,
en voor AVG de overeenstemming met de bestaande Haiku-laag-1 (relevant, onderwerp, uitkomst)."""
import json, os, re, sys, collections, itertools
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); LAB = f'{R}/lab'; D = f'{R}/data'
KERN = ['relevant', 'onderwerp', 'sub', 'zaaktype', 'procesvorm', 'uitkomst', 'gip']

def kern(o):
    if not o: return None
    if o.get('relevant') is False: return {'relevant': False}
    pj = o.get('partijen') or {}
    return {'relevant': True, 'onderwerp': o.get('onderwerp'), 'sub': o.get('sub'), 'zaaktype': o.get('zaaktype'),
            'procesvorm': o.get('procesvorm'), 'uitkomst': o.get('uitkomst'), 'gip': pj.get('gemeente_is_partij')}

def eq(a, b, keys=KERN):
    if a is None or b is None: return False
    if not a['relevant'] or not b['relevant']: return a['relevant'] == b['relevant']
    return all(a.get(k) == b.get(k) for k in keys)

def fout_v3(run, slug, files):
    import subprocess
    chk = f'{LAB}/runs/{run}/_check_uit_v3.py'; F = {}
    for f in files:
        t = subprocess.run([sys.executable, '-I', chk, slug, f], capture_output=True, text=True); s = t.stdout + t.stderr
        F[f] = 1 if 'Traceback' in s else sum(1 for l in s.splitlines() if ' FOUT ' in l or 'ONTBREEKT' in l)
    return F

def cost(run):
    p = f'{LAB}/runs/{run}/usage.jsonl'
    return sum((json.loads(l).get('cost') or 0) for l in open(p)) if os.path.exists(p) else 0

out = {}
# AVG laag 2
S = json.load(open(f'{LAB}/sets/toep_avg_v3.json')); M = ['deepseek-v4.1-flash', 'qwen3.8-flash']; O = {}; OK = {}
for m in M:
    run = f'f2b-v3-avg-{m}'; O[m] = {}
    for f in S:
        try: O[m][f] = json.load(open(f'{LAB}/runs/{run}/D/uit_v3/avg-privacy/{f}'))
        except Exception: O[m][f] = None
    F = fout_v3(run, 'avg-privacy', S); OK[m] = {f: O[m][f] is not None and F[f] == 0 for f in S}
    out[f'avg_v3_{m}'] = {'n': len(S), 'uitvoer': sum(v is not None for v in O[m].values()), 'check_ok': sum(OK[m].values()),
                          'kosten': round(cost(run), 4), 'per_1000': round(1000 * cost(run) / len(S), 2)}
cons = [f for f in S if all(OK[m][f] for m in M) and eq(kern(O[M[0]][f]), kern(O[M[1]][f]))]
L1 = {}
for fn in os.listdir(f'{D}/uit_l1/avg-privacy'):
    for o in json.load(open(f'{D}/uit_l1/avg-privacy/{fn}')): L1[o['ecli'].replace(':', '_') + '.json'] = o
ds = {f: kern(O[M[0]][f]) for f in S}; hk = {f: kern(L1.get(f)) for f in S}
both = [f for f in S if ds[f] and hk[f]]
out['avg_v3_consensus'] = {'eens': len(cons), 'pct': round(100 * len(cons) / len(S), 1), 'bestanden': cons,
                           'deepseek_vs_haiku_l1': {k: round(100 * sum(eq(ds[f], hk[f], [k]) for f in both) / max(len(both), 1), 1) for k in ['relevant', 'onderwerp', 'uitkomst']},
                           'n_vergelijk': len(both)}
# BPM laag 1
E = json.load(open(f'{LAB}/sets/toep_bpm_l1.json')); M3 = ['deepseek-v4.1-flash', 'qwen3.8-flash', 'qwen3.7-plus']; B = {}; BOK = {}
for m in M3:
    run = f'f2-l1-bpm-{m}'; B[m] = {}
    d = f'{LAB}/runs/{run}/D/uit_l1/bpm'
    for fn in os.listdir(d):
        try:
            for o in json.load(open(f'{d}/{fn}')):
                if isinstance(o, dict): B[m][o.get('ecli')] = o
        except Exception: pass
    bad = collections.Counter(re.match(r'^lab-\d+ (ECLI:\S+) FOUT', l).group(1) for l in open(f'{LAB}/runs/{run}/check.txt') if re.match(r'^lab-\d+ (ECLI:\S+) FOUT', l))
    BOK[m] = {e: e in B[m] and not bad[e] for e in E}
    out[f'bpm_l1_{m}'] = {'n': len(E), 'uitvoer': sum(e in B[m] for e in E), 'check_ok': sum(BOK[m].values()),
                          'kosten': round(cost(run), 4), 'per_1000': round(1000 * cost(run) / len(E), 2),
                          'niet_relevant': sum(1 for e in E if (B[m].get(e) or {}).get('relevant') is False)}
for combo in [M3[:2], M3]:
    c = [e for e in E if all(BOK[m][e] for m in combo) and all(eq(kern(B[combo[0]].get(e)), kern(B[m].get(e))) for m in combo[1:])]
    out['bpm_l1_consensus_' + '+'.join(combo)] = {'eens': len(c), 'pct': round(100 * len(c) / len(E), 1)}
json.dump(out, open(f'{LAB}/score_toep.json', 'w'), indent=1, ensure_ascii=False)
for k, v in out.items(): print(k, {a: b for a, b in v.items() if a != 'bestanden'})

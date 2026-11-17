"""Eén commando voor de goedkope keten (gekozen mix, 15 nov 2026).

  python3 -I lab/pijplijn.py draai  <v3|l1> <slug> <setbestand> <naam>   # modellen + consensus + vangnetlijst
  python3 -I lab/pijplijn.py samen  <v3|l1> <slug> <naam>                 # vangnet-uitvoer erbij, checks, lab/out

laag 2 (v3): DeepSeek V4.1 Flash schrijft (v3c), Qwen3.8 Flash geeft alleen labels (v3lab). Eens -> DeepSeek.
             Oneens -> vangnetbatches (6) voor Sonnet-subagents als corrector (lab/vangnet_corrector.md).
laag 1 (l1): DeepSeek + Qwen3.8 Flash (l1c). Eens -> DeepSeek. Oneens -> Qwen3.7 Plus als scheidsrechter;
             2 van 3 eens -> die. Anders -> vangnetbatches (25) voor Haiku-subagents (scripts/verrijk_l1.md).
Alle runs via lab/run.py (budgetstop, usage, herstelronde). Uitvoer voor de sessie domeinen: lab/out/<slug>/ (v3)
of lab/out/<slug>_l1.json (l1) + herkomst. Deze sessie schrijft niet in data/uit_*.
"""
import json, os, sys, subprocess, collections
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); LAB = f'{R}/lab'; DATA = f'{R}/data'
DS, QF, QP = 'deepseek/deepseek-v4.1-flash', 'qwen/qwen3.8-flash', 'qwen/qwen3.7-plus'
KERN = ['relevant', 'onderwerp', 'sub', 'zaaktype', 'procesvorm', 'uitkomst', 'gip']
ENV = dict(os.environ, LAB_EFFORT='budget:4000')

def kern(o):
    if not isinstance(o, dict): return None
    if isinstance(o.get('items'), list) and o['items']: o = o['items'][0]
    if o.get('relevant') is False: return {'relevant': False}
    pj = o.get('partijen') or {}
    return {'relevant': True, 'onderwerp': o.get('onderwerp'), 'sub': o.get('sub'), 'zaaktype': o.get('zaaktype'),
            'procesvorm': o.get('procesvorm'), 'uitkomst': o.get('uitkomst'), 'gip': pj.get('gemeente_is_partij')}

def eq(a, b):
    if a is None or b is None: return False
    if not a['relevant'] or not b['relevant']: return a['relevant'] == b['relevant']
    return all(a.get(k) == b.get(k) for k in KERN)

def run(laag, slug, model, setf, rid, extra, par):
    env = dict(ENV, LAB_EXTRA=f'{LAB}/{extra}')
    return subprocess.Popen([sys.executable, '-I', f'{LAB}/run.py', laag, slug, model, setf, rid, '--par', str(par)],
                            env=env, stdout=open(f'{LAB}/logs/{rid}.log', 'w'), stderr=subprocess.STDOUT)

def checkfile(rid, name):
    return f'{LAB}/runs/{rid}/_{name}'

def fouten_v3(rid, slug, files):
    F = {}
    for f in files:
        t = subprocess.run([sys.executable, '-I', checkfile(rid, 'check_uit_v3.py'), slug, f], capture_output=True, text=True)
        s = t.stdout + t.stderr
        F[f] = 1 if 'Traceback' in s else sum(1 for l in s.splitlines() if ' FOUT ' in l or 'ONTBREEKT' in l)
    return F

def l1_out(rid, slug):
    B, bad = {}, collections.Counter(); d = f'{LAB}/runs/{rid}/D/uit_l1/{slug}'
    for fn in os.listdir(d) if os.path.isdir(d) else []:
        try:
            for o in json.load(open(f'{d}/{fn}')):
                if isinstance(o, dict) and o.get('ecli'): B[o['ecli']] = o
        except Exception: pass
    p = f'{LAB}/runs/{rid}/check.txt'
    for l in open(p) if os.path.exists(p) else []:
        parts = l.split()
        if len(parts) > 2 and parts[2] == 'FOUT': bad[parts[1]] += 1
    return B, bad

def sandbox_vangnet(naam, slug, laag):
    V = f'{LAB}/runs/{naam}-vangnet'; os.makedirs(f'{V}/D/uit_v3/{slug}', exist_ok=True); os.makedirs(f'{V}/D/uit_l1/{slug}', exist_ok=True)
    for k in ('dom', 'in_v3'):
        if not os.path.lexists(f'{V}/D/{k}'): os.symlink(f'{DATA}/{k}', f'{V}/D/{k}')
    for c in ('check_uit_v3.py', 'check_l1.py'):
        open(f'{V}/_{c}', 'w').write(open(f'{R}/scripts/{c}').read().replace("'/home/claude/data'", repr(f'{V}/D')))
    return V

def draai(laag, slug, setf, naam):
    items = json.load(open(setf)); os.makedirs(f'{LAB}/logs', exist_ok=True)
    if laag == 'v3':
        ps = [run('v3', slug, DS, setf, f'{naam}-ds', 'aanscherping_v3c.md', 12), run('v3lab', slug, QF, setf, f'{naam}-qlab', 'aanscherping_v3c.md', 12)]
        for p in ps: p.wait()
        A = {f: (json.load(open(p)) if os.path.exists(p := f'{LAB}/runs/{naam}-ds/D/uit_v3/{slug}/{f}') else None) for f in items}
        Q = {f: (json.load(open(p)) if os.path.exists(p := f'{LAB}/runs/{naam}-qlab/D/uit_lab/{slug}/{f}') else None) for f in items}
        F = fouten_v3(f'{naam}-ds', slug, items)
        cons = [f for f in items if A[f] and F[f] == 0 and eq(kern(A[f]), kern(Q[f]))]
        rest = [f for f in items if f not in cons]
        V = sandbox_vangnet(naam, slug, laag); os.makedirs(f'{V}/D/concept/{slug}', exist_ok=True)
        for f in rest:  # concept + labels van model 2 voor de corrector
            json.dump({'concept_deepseek': A[f], 'scriptfouten_concept': F[f], 'labels_tweede_model': Q[f]},
                      open(f'{V}/D/concept/{slug}/{f}', 'w'), ensure_ascii=False, indent=1)
        json.dump([{'id': f'vn-{i // 6:03d}', 'files': rest[i:i + 6]} for i in range(0, len(rest), 6)], open(f'{V}/batches.json', 'w'), indent=0)
    else:
        ps = [run('l1', slug, DS, setf, f'{naam}-ds', 'aanscherping_l1c.md', 10), run('l1', slug, QF, setf, f'{naam}-qf', 'aanscherping_l1c.md', 10)]
        for p in ps: p.wait()
        (A, ba), (Q, bq) = l1_out(f'{naam}-ds', slug), l1_out(f'{naam}-qf', slug)
        E = [x.replace('_', ':')[:-5] if x.endswith('.json') else x for x in items]
        ok = lambda B, bad, e: e in B and not bad[e]
        cons = [e for e in E if ok(A, ba, e) and ok(Q, bq, e) and eq(kern(A[e]), kern(Q[e]))]
        twijfel = [e for e in E if e not in cons]
        json.dump(twijfel, open(f'{LAB}/sets/{naam}_twijfel.json', 'w'), indent=0)
        meer = {}  # scheidsrechter (Qwen3.7 Plus, 2 van 3) uitgezet: blinde toets Wahv 15 nov -> 4 goed, 9 fout. Alles naar vangnet.
        P, bp = {}, collections.Counter()
        for e in ([] if True else twijfel):
            kk = {n: (kern(B[e]) if ok(B, bd, e) else None) for n, B, bd in (('ds', A, ba), ('qf', Q, bq), ('qp', P, bp))}
            for x, y in (('ds', 'qp'), ('ds', 'qf'), ('qf', 'qp')):
                if eq(kk[x], kk[y]): meer[e] = x; break
        rest = [e for e in twijfel if e not in meer]
        V = sandbox_vangnet(naam, slug, laag)
        VB = [{'id': f'vn-{i // 25:03d}', 'eclis': rest[i:i + 25]} for i in range(0, len(rest), 25)]
        json.dump(VB, open(f'{V}/batches.json', 'w'), indent=0)
        os.makedirs(f'{V}/D/batches', exist_ok=True); json.dump(VB, open(f'{V}/D/batches/l1_{slug}.json', 'w'), indent=0)
        if not os.path.lexists(f'{V}/D/in_l1'): os.symlink(f'{LAB}/runs/{naam}-ds/D/in_l1', f'{V}/D/in_l1')
        json.dump({'consensus': cons, 'meerderheid': meer}, open(f'{V}/keuze.json', 'w'), indent=0)
    st = {'naam': naam, 'laag': laag, 'slug': slug, 'n': len(items), 'eens': len(cons), 'vangnet': len(rest)}
    if laag == 'l1': st['meerderheid'] = len(meer)
    json.dump(st, open(f'{LAB}/runs/{naam}-vangnet/status.json', 'w'), indent=1); print(st)

def samen(laag, slug, naam):
    V = f'{LAB}/runs/{naam}-vangnet'; st = json.load(open(f'{V}/status.json'))
    if laag == 'v3':
        O = f'{LAB}/out/{slug}'; os.makedirs(O, exist_ok=True)
        H = json.load(open(f'{LAB}/out/{slug}_herkomst.json')) if os.path.exists(f'{LAB}/out/{slug}_herkomst.json') else {}
        vn = {f for b in json.load(open(f'{V}/batches.json')) for f in b['files']}
        items = json.load(open(json.load(open(f'{LAB}/runs/{naam}-ds/meta.json'))['set']))
        mis = []
        for f in items:
            src = f'{V}/D/uit_v3/{slug}/{f}' if f in vn else f'{LAB}/runs/{naam}-ds/D/uit_v3/{slug}/{f}'
            if not os.path.exists(src): mis.append(f); continue
            open(f'{O}/{f}', 'w').write(open(src).read())
            H[f] = 'sonnet-corrector (vangnet)' if f in vn else 'deepseek-v4.1-flash (eens met qwen3.8-flash labels, v3c)'
        json.dump(H, open(f'{LAB}/out/{slug}_herkomst.json', 'w'), indent=0)
        # check op de samengevoegde map
        S = f'{LAB}/out/_D_{slug}'; os.makedirs(f'{S}/uit_v3', exist_ok=True)
        for k in ('dom', 'in_v3'):
            if not os.path.lexists(f'{S}/{k}'): os.symlink(f'{DATA}/{k}', f'{S}/{k}')
        if not os.path.lexists(f'{S}/uit_v3/{slug}'): os.symlink(O, f'{S}/uit_v3/{slug}')
        open(f'{S}/_check.py', 'w').write(open(f'{R}/scripts/check_uit_v3.py').read().replace("'/home/claude/data'", repr(S)))
        r = subprocess.run([sys.executable, '-I', f'{S}/_check.py', slug, '--stil'], capture_output=True, text=True).stdout.strip().splitlines()[-2:]
        x = subprocess.run([sys.executable, '-I', f'{LAB}/extra_check.py', slug, O], capture_output=True, text=True).stdout.strip().splitlines()[-1:]
        print(naam, 'ontbreekt', len(mis), mis[:5]); print('\n'.join(r + x))
    else:
        K = json.load(open(f'{V}/keuze.json')); out = json.load(open(f'{LAB}/out/{slug}_l1.json')) if os.path.exists(f'{LAB}/out/{slug}_l1.json') else {}
        H = json.load(open(f'{LAB}/out/{slug}_l1_herkomst.json')) if os.path.exists(f'{LAB}/out/{slug}_l1_herkomst.json') else {}
        A, _ = l1_out(f'{naam}-ds', slug); Q, _ = l1_out(f'{naam}-qf', slug); P, _ = l1_out(f'{naam}-qp', slug); src = {'ds': A, 'qf': Q, 'qp': P}
        for e in K['consensus']: out[e] = A[e]; H[e] = 'deepseek (eens met qwen3.8-flash, l1c)'
        for e, w in K['meerderheid'].items(): out[e] = src[w][e]; H[e] = f'meerderheid 2 van 3 ({w}, l1c)'
        d = f'{V}/D/uit_l1/{slug}'
        for fn in os.listdir(d) if os.path.isdir(d) else []:
            for o in json.load(open(f'{d}/{fn}')):
                if isinstance(o, dict) and o.get('ecli'): out[o['ecli']] = o; H[o['ecli']] = 'haiku-subagent (vangnet, verrijk_l1.md)'
        json.dump(out, open(f'{LAB}/out/{slug}_l1.json', 'w'), ensure_ascii=False); json.dump(H, open(f'{LAB}/out/{slug}_l1_herkomst.json', 'w'), indent=0)
        print(naam, 'l1 totaal', len(out), collections.Counter(h.split(' (')[0] for h in H.values()))

if __name__ == '__main__':
    a = sys.argv[1:]
    if a[0] == 'draai': draai(*a[1:5])
    else: samen(*a[1:4])

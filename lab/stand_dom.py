"""'De stand in het kort' voor andere domeinen dan parkeren (besluit Robert 16 nov 2026, optie B).

  python3 -I lab/stand_dom.py prep  <slug> [per_batch]   # invoer per subonderwerp + batches
  python3 -I lab/stand_dom.py samen <slug>               # agent-uitvoer valideren -> site/data/domeinen/<slug>/stand.json

Per subonderwerp een modus:
  vol     >= 3 uitspraken met laag 2 (kern)  -> Sonnet schrijft lijn + regels op de kaarten (lab/stand_opdracht.md)
  labels  < 3 laag 2, >= 3 laag 1            -> lichte stand op uitkomst + uitkomstcitaat, altijd gelabeld "Op basis van labels"
  weinig  anders                             -> geen AI: lijn 'weinig' + vaste tekst
Validatie (samen): elke bron moet een ECLI uit de invoerkaarten zijn en het citaat moet letterlijk in die uitspraak staan.
Regels zonder geldige bron vallen weg; een 'vol'/'labels'-stand zonder regels wordt 'weinig'.
"""
import json, os, sys, re, unicodedata, collections, glob
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cmd, slug = sys.argv[1], sys.argv[2]
SITE = f'{R}/site/data/domeinen/{slug}'; W = f'{R}/lab/stand/{slug}'
for d in ('in', 'uit'): os.makedirs(f'{W}/{d}', exist_ok=True)
LAAG1_DOMEIN = slug in ('bpm', 'verkeersboetes')
RANG = {'Hoogste rechter': 0}
WEINIG = 'Nog te weinig uitspraken om een lijn te zien. Bekijk de uitspraken hieronder.'
LABELS = 'Op basis van labels: '

def norm(x):
    x = unicodedata.normalize('NFKC', x or ''); x = re.sub(r'[‘’‚`´]', "'", x); x = re.sub(r'[“”„]', '"', x)
    return re.sub(r'\s+', ' ', x).strip().lower()

def laden():
    V = {v['ecli']: v for v in json.load(open(f'{SITE}/verrijkt.json'))}
    M = {m['e']: m for m in json.load(open(f'{SITE}/meta.json'))}
    tax = json.load(open(f'{R}/data/dom/{slug}/taxonomie.json'))
    return V, M, tax

def subs(tax):
    for o, t in tax.items():
        if isinstance(t, dict):
            for s in t.get('sub', {}): yield o, s

def kaart(v, m, vol):
    k = {'ecli': v['ecli'], 'instantie': m.get('i'), 'niveau': m.get('n'), 'datum': m.get('d'), 'uitkomst': v.get('uitkomst')}
    if vol and v.get('kern'):
        k['titel'] = v.get('titel')
        k['kern'] = {'zin': v['kern'].get('zin'), 'citaat': v['kern'].get('citaat')}
        rr = v.get('rechtsregel') or {}
        if rr.get('zin'): k['rechtsregel'] = {'zin': rr.get('zin'), 'citaat': rr.get('citaat'), 'reikwijdte': rr.get('reikwijdte')}
    else:
        k['uitkomst_citaat'] = (v.get('uitkomst_bron') or {}).get('citaat')
    return k

if cmd == 'prep':
    per = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    V, M, tax = laden(); taken = []; tel = collections.Counter()
    for o, s in subs(tax):
        L = [v for v in V.values() if v.get('relevant') and v.get('onderwerp') == o and v.get('sub') == s and not v.get('dubbel_van')]
        L2 = [v for v in L if v.get('kern')]
        orde = lambda v: (RANG.get(M.get(v['ecli'], {}).get('n'), 1), -int((M.get(v['ecli'], {}).get('d') or '0000')[:4]))
        if len(L2) >= 3: modus, K = 'vol', sorted(L2, key=orde)[:25]
        elif len(L) >= 3: modus, K = 'labels', sorted(L, key=orde)[:15]
        else: modus, K = 'weinig', []
        tel[modus] += 1
        t = tax[o]['sub'][s]; lab = t.get('label') if isinstance(t, dict) else t
        inv = {'slug': slug, 'onderwerp': o, 'sub': s, 'label': lab, 'onderwerp_label': tax[o].get('label'), 'modus': modus,
               'n_uitspraken': len(L), 'n_laag2': len(L2),
               'uitkomsten': dict(collections.Counter(v.get('uitkomst') for v in L)),
               'kaarten': [kaart(v, M.get(v['ecli'], {}), modus == 'vol') for v in K]}
        json.dump(inv, open(f'{W}/in/{o}--{s}.json', 'w'), ensure_ascii=False, indent=1)
        if modus != 'weinig' and not os.path.exists(f'{W}/uit/{o}--{s}.json'): taken.append(f'{o}--{s}')
    B = [{'id': f'st-{slug}-{i:02d}', 'files': taken[j:j + per]} for i, j in enumerate(range(0, len(taken), per))]
    json.dump(B, open(f'{W}/batches.json', 'w'), indent=0)
    print(slug, dict(tel), 'open', len(taken), 'batches', len(B))

elif cmd == 'samen':
    V, M, tax = laden()
    U = {u['ecli']: u for u in json.load(open(f'{R}/data/dom/{slug}/uitspraken.json'))}
    tekst = {}
    def bron_ok(b, toegestaan):
        e = (b.get('ecli') or '').strip()
        if e and not e.startswith('ECLI:'): e = 'ECLI:NL:' + e  # agent kortte soms af
        b['ecli'] = e; c = norm(b.get('citaat'))
        if e not in toegestaan or len(c) < 8 or e not in U: return False
        if e not in tekst: tekst[e] = norm(' '.join(a['t'] for a in U[e]['alineas']))
        return c in tekst[e]
    stand, tel = {}, collections.Counter()
    for o, s in subs(tax):
        inv = json.load(open(f'{W}/in/{o}--{s}.json')); p = f'{W}/uit/{o}--{s}.json'
        st = None
        if inv['modus'] != 'weinig' and os.path.exists(p):
            try: st = json.load(open(p))
            except Exception: st = None
        if st:
            ok = {k['ecli'] for k in inv['kaarten']}; regels = []
            for r in st.get('regels') or []:
                br = [b for b in r.get('bronnen') or [] if bron_ok(b, ok)]
                tel['bron_ok'] += len(br); tel['bron_weg'] += len(r.get('bronnen') or []) - len(br)
                if br and r.get('zin'): regels.append({'zin': r['zin'], 'bronnen': br})
            uitleg = st.get('lijn_uitleg') or ''
            if inv['modus'] == 'labels' and not uitleg.startswith(LABELS): uitleg = LABELS + uitleg
            lijn = st.get('lijn') if st.get('lijn') in ('hr-lijn', 'vaste-lijn', 'losse-uitspraken', 'verdeeld', 'weinig') else 'losse-uitspraken'
            if inv['modus'] == 'labels' and lijn in ('hr-lijn', 'vaste-lijn'): lijn = 'verdeeld' if len(inv['uitkomsten']) > 1 else 'losse-uitspraken'
            if regels:
                stand.setdefault(o, {})[s] = {'lijn': lijn, 'kern': st.get('kern'), 'lijn_uitleg': uitleg, 'regels': regels,
                                              'modus': inv['modus'], 'n': inv['n_uitspraken']}
                tel[inv['modus']] += 1; continue
        if inv['modus'] != 'weinig' and not os.path.exists(p): tel['ontbreekt'] += 1
        stand.setdefault(o, {})[s] = {'lijn': 'weinig', 'lijn_uitleg': WEINIG, 'regels': [], 'modus': 'weinig', 'n': inv['n_uitspraken']}
        tel['weinig'] += 1
    json.dump(stand, open(f'{SITE}/stand.json', 'w'), ensure_ascii=False)
    print(slug, dict(tel))
    # optionele bestanden aanmelden, anders laadt de site stand.json niet (zie domStart in index.html)
    ip = f'{R}/site/data/domeinen/index.json'; L = json.load(open(ip))
    for d in L:
        if d['slug'] == slug: d['bestanden'] = sorted(set(d.get('bestanden') or []) | {'stand.json'})
    json.dump(L, open(ip, 'w'), ensure_ascii=False, indent=1)

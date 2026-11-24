#!/usr/bin/env python3 -I
"""Haalt alle strafrechtelijke uitspraken (rechtsgebied Strafrecht bij rechtspraak.nl) uit de PUBLIEKE site-data, tot de FG akkoord is (AVG art. 10).
Algemene opvolger van fg_filter_afval.py: werkt op alle domeinen en op alle afgeleide bestanden (meta, verrijkt, tekst*, relaties, keten,
zoekindex, u/-shards en o-*.json, feeds + idx, sitemap, open data, domein-uitspraken.json, tellingen).

Gebruik (draai na elke data-update, NA maak_feeds/maak_zoekindex/maak_uitspraakpagina/maak_open_data, vóór commit):
    python3 -I scripts/fg_filter_straf.py            # controleert rechtsgebied voor nieuwe kandidaten (netwerk nodig), filtert, schrijft
    python3 -I scripts/fg_filter_straf.py --droog    # alleen melden
    python3 -I scripts/fg_filter_straf.py --geen-netwerk   # alleen de bestaande lijst toepassen

Lijst: scripts/straf_ecli.json  {"straf":[ECLI...], "gecontroleerd":[ECLI...]}  (gecontroleerd = rechtsgebied opgehaald, geen straf als niet in 'straf').
Kandidaten: uitspraken met strafrechttermen in de tekst; alleen die worden bij rechtspraak.nl nagevraagd. Idempotent."""
import json, os, re, subprocess, sys, glob, concurrent.futures as cf, html

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = os.path.join(R, "site")
LIJST = os.path.join(R, "scripts", "straf_ecli.json")
DROOG = "--droog" in sys.argv
NETWERK = "--geen-netwerk" not in sys.argv
KAND = re.compile(r"verdachte|tenlastelegging|strafvordering|parketnummer|strafzaken|politierechter|wetboek van strafrecht|strafkamer|strafbeschikking|opiumwet|veroordeeld|strafbaar", re.I)
ECLI = re.compile(r"^ECLI:NL:[A-Z0-9]+:\d{4}:[A-Za-z0-9]+$")
HASH = re.compile(r"^NL-[A-Z0-9]+-\d{4}-[A-Za-z0-9]+$")
hashE = lambda e: e.replace("ECLI:", "").replace(":", "-")


def laad(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def schrijf(p, d, indent=None, nl=None):
    with open(p, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=indent, separators=(",", ": ") if indent else (",", ":"))
        if indent or nl: f.write("\n")


def dom_van(p):
    m = re.search(r"data/domeinen/([^/]+)/", p)
    return m.group(1) if m else "parkeren"


# ---------- 1. kandidaten en rechtsgebied ----------
TEKST = {}
WAHV = re.compile(r"wahv|administratiefrechtelijke handhaving verkeersvoorschriften|wet mulder|administratieve sanctie", re.I)


def wahv_achtig(e):
    """Hoge Raad/hof-uitspraken over Wahv-boetes staan als 'Strafrecht' (strafkamer), maar zijn bestuurlijke sancties (betrokkene, geen verdachte)."""
    t = TEKST.get(e, "")
    return len(WAHV.findall(t)) >= 1 and len(re.findall(r"verdachte", t, re.I)) < 3


def kandidaten():
    k = set()
    for f in glob.glob(f"{S}/data/domeinen/*/tekst[0-9]*.json") + glob.glob(f"{S}/data/tekst[0-9]*.json"):
        for e, v in laad(f).items():
            t = " ".join(str(x[1]) for x in v if isinstance(x, list) and len(x) > 1) if isinstance(v, list) else str(v)
            if KAND.search(t): k.add(e); TEKST[e] = t
    return k


def is_straf(labels):
    """Strafrecht zonder bestuursrechtelijk label. Wahv-zaken staan bij Rechtspraak vaak als 'Strafrecht' + 'Bestuursrecht; Bestuursstrafrecht':
    dat zijn bestuurlijke sancties (kern van domein Verkeersboetes) en blijven staan; alleen zuivere strafzaken gaan eruit."""
    return any("Strafrecht" in x for x in labels) and not any("Bestuurs" in x for x in labels)


def rechtsgebied(e):
    for _ in range(3):
        t = subprocess.run(["curl", "-s", "--max-time", "30", f"https://data.rechtspraak.nl/uitspraken/content?id={e}"], capture_output=True, text=True).stdout
        if "<dcterms:" in t or "uitspraak" in t[:600].lower():
            return re.findall(r'rdfs:label="Rechtsgebied"[^>]*>([^<]*)', t)
    return None


L = laad(LIJST) if os.path.exists(LIJST) else {"straf": [], "gecontroleerd": []}
if NETWERK:
    nieuw = sorted(kandidaten() - set(L["gecontroleerd"]))
    print("nieuwe kandidaten om te controleren:", len(nieuw))
    with cf.ThreadPoolExecutor(8) as p:
        for e, r in zip(nieuw, p.map(rechtsgebied, nieuw)):
            if r is None: print("geen antwoord, later opnieuw:", e); continue
            L["gecontroleerd"].append(e)
            if is_straf(r) and not wahv_achtig(e): L["straf"].append(e)
    L["straf"] = sorted(set(L["straf"])); L["gecontroleerd"] = sorted(set(L["gecontroleerd"]))
    if not DROOG: schrijf(LIJST, L)
WEG = set(L["straf"]); WEGH = {hashE(e) for e in WEG}
print("strafrechtelijke uitspraken op de lijst:", len(WEG))

# ---------- 2. metadata van te verwijderen uitspraken (vóór het schrappen) ----------
INFO = {}  # ecli -> (domein, o, s)
for f in glob.glob(f"{S}/data/domeinen/*/meta.json") + [f"{S}/data/meta.json"]:
    for x in laad(f):
        if x["e"] in WEG: INFO.setdefault(x["e"], []).append((dom_van(f), x.get("o"), x.get("s")))
FEEDT = laad(f"{S}/data/feed_toegevoegd.json") if os.path.exists(f"{S}/data/feed_toegevoegd.json") else {}
L2 = {}
for f in glob.glob(f"{S}/data/domeinen/*/verrijkt.json") + [f"{S}/data/verrijkt.json"]:
    for x in laad(f):
        if (x.get("ecli") or x.get("e")) in WEG and x.get("laag") == 2: L2.setdefault(dom_van(f), set()).add(x.get("ecli") or x.get("e"))

# ---------- 3. generieke scrub van JSON ----------
def isE(x): return isinstance(x, str) and (ECLI.match(x) or HASH.match(x))
def weg_str(x): return x in WEG or x in WEGH

def scrub(o):
    if isinstance(o, dict):
        if any(isinstance(o.get(k), str) and o.get(k) in WEG for k in ("e", "ecli", "E")): return None
        return {k: scrub_val(v) for k, v in o.items() if not weg_str(k)}
    if isinstance(o, list):
        if o and all(isE(x) for x in o): return [x for x in o if not weg_str(x)]
        if o and isinstance(o[0], str) and weg_str(o[0]) and any(not isE(x) for x in o): return None  # rij: [ecli, ...]
        r = []
        for x in o:
            if isinstance(x, str):
                if weg_str(x): continue
                r.append(x)
            else:
                y = scrub(x)
                if y is None and (isinstance(x, (dict, list))): continue
                r.append(y)
        return r
    return o

def scrub_val(v):
    y = scrub(v)
    return y if y is not None or not isinstance(v, (dict, list)) else ([] if isinstance(v, list) else {})

def schrijf_als(p, d):
    raw = open(p, encoding="utf-8").read(); m = re.match(r"[^\n]*\n( +)\S", raw[:4000])
    schrijf(p, d, indent=len(m.group(1)) if m else None, nl=raw.endswith("\n"))

GEWIJZIGD = []
def verwerk_json(p, indent=None):
    try: d = laad(p)
    except Exception: return
    raw = open(p, encoding="utf-8").read()
    m = re.match(r"[^\n]*\n( +)\S", raw[:4000]); indent = len(m.group(1)) if m else None
    if not any(e in raw for e in WEG) and not any(h in raw for h in WEGH): return
    n = scrub_val(d)
    if n != d:
        GEWIJZIGD.append(os.path.relpath(p, R))
        if not DROOG: schrijf(p, n, indent=indent, nl=raw.endswith("\n"))

for p in glob.glob(f"{S}/data/**/*.json", recursive=True):
    if "/data/u/" in p: continue
    verwerk_json(p)
for p in glob.glob(f"{S}/*.json") + glob.glob(f"{S}/feeds/idx/*.json") + glob.glob(f"{S}/open/*.json") + glob.glob(f"{S}/*/uitspraken.json"):
    verwerk_json(p)

# ---------- 4. u/-shards en o-*.json ----------
OF = {}  # domein -> {"n":x, "subs":{"o--s":x}}
for p in glob.glob(f"{S}/data/u/[0-9]*.json"):
    d = laad(p); gewijzigd = False
    for h in [h for h in d if h in WEGH]:
        r = d.pop(h); gewijzigd = True
        dom, o, s = r[5], r[6], r[7]
        a = OF.setdefault(dom, {"n": 0, "subs": {}}); a["n"] += 1
        a["subs"][f"{o}--{s}"] = a["subs"].get(f"{o}--{s}", 0) + 1
    if gewijzigd:
        GEWIJZIGD.append(os.path.relpath(p, R))
        if not DROOG: schrijf(p, d)
for p in glob.glob(f"{S}/data/u/o-*.json"):
    dom = os.path.basename(p)[2:-5]; d = laad(p); a = OF.get(dom, {"n": 0, "subs": {}})
    d["n"] -= a["n"]
    for k, v in d.get("subs", {}).items():
        v["n"] -= a["subs"].get(k, 0)
        v["top"] = [t for t in v.get("top", []) if t[0] not in WEGH]
    d["top"] = [t for t in d.get("top", []) if t[0] not in WEGH]
    if a["n"] or any(True for _ in []):
        GEWIJZIGD.append(os.path.relpath(p, R))
        if not DROOG: schrijf(p, d)

# ---------- 5. xml: feeds en sitemap ----------
def verwerk_xml(p, blok, sleutel):
    t = open(p, encoding="utf-8").read()
    n = re.sub(blok, lambda m: "" if re.search(sleutel, m.group(0)) and any(h in m.group(0) for h in WEGH) else m.group(0), t, flags=re.S)
    if n != t:
        GEWIJZIGD.append(os.path.relpath(p, R))
        if not DROOG: open(p, "w", encoding="utf-8").write(n)

for p in glob.glob(f"{S}/feeds/**/*.xml", recursive=True):
    verwerk_xml(p, r"<item>.*?</item>\n?", r"#uitspraak-")
if os.path.exists(f"{S}/sitemap.xml"): verwerk_xml(f"{S}/sitemap.xml", r"<url>.*?</url>\n?", r"/u/")

# ---------- 6. open data CSV ----------
for p in glob.glob(f"{S}/open/*.csv"):
    enc = "utf-8-sig"; rr = open(p, encoding=enc, newline="").read()
    # ECLI in eerste kolom; meerregelige velden komen in deze export niet voor als rij-begin
    regels = rr.split("\r\n") if "\r\n" in rr else rr.split("\n")
    nieuw = [r for r in regels if not (r.split(";", 1)[0].strip('"') in WEG)]
    if len(nieuw) != len(regels):
        GEWIJZIGD.append(os.path.relpath(p, R))
        if not DROOG: open(p, "w", encoding=enc, newline="").write(("\r\n" if "\r\n" in rr else "\n").join(nieuw))

# ---------- 7. tellingen ----------
def n_weg(dom): return sum(1 for e, v in INFO.items() for (d, o, s) in v if d == dom)
IDX = f"{S}/data/domeinen/index.json"; I = laad(IDX)
for x in I:
    k = n_weg(x["slug"])
    if k:
        for f in ("n", "laag1", "n_verzameld"):
            if f in x: x[f] -= k
        if "n_gepubliceerd" in x: x["n_gepubliceerd"] -= OF.get(x["slug"], {}).get("n", 0)
        l2 = len(L2.get(x["slug"], ()))
        if l2: x["laag2"] -= l2
        if isinstance(x.get("uitwerking"), dict):
            for f in ("laag1",):
                if f in x["uitwerking"]: x["uitwerking"][f] -= k
            if l2 and "laag2" in x["uitwerking"]: x["uitwerking"]["laag2"] -= l2
if not DROOG and INFO: schrijf_als(IDX, I)

AP = f"{S}/data/aantallen.json"; A = laad(AP) if os.path.exists(AP) else {"domeinen": {}}
for dom, dd in A["domeinen"].items():
    dd["verzameld"] -= n_weg(dom)
    dd["gepubliceerd"] -= OF.get(dom, {}).get("n", 0)
    for k, v in OF.get(dom, {}).get("subs", {}).items():
        if k in dd.get("onderwerpen", {}): dd["onderwerpen"][k] -= v
if not DROOG and INFO and os.path.exists(AP): schrijf_als(AP, A)

FI = f"{S}/feeds/index.json"; F = laad(FI)
for x in F:
    for e, v in INFO.items():
        for (d, o, s) in v:
            if d == x["slug"] and e in FEEDT.get(d, {}):
                x["n"] -= 1
                for sb in x.get("subs", []):
                    if sb["o"] == o and sb["s"] == s: sb["n"] -= 1
if not DROOG and INFO: schrijf_als(FI, F)
# feed_toegevoegd: verwijder de ECLI's (genoteerd, niet terugzetten door een volgende maak_feeds)
FT = {d: {e: t for e, t in m.items() if e not in WEG} for d, m in FEEDT.items()}
if not DROOG and FEEDT: schrijf_als(f"{S}/data/feed_toegevoegd.json", FT)


# ---------- 8. statische pagina's: bronlijsten met verwijderde uitspraken (komen uit AI-trends in data/, niet uit site/data) ----------
for p in glob.glob(f"{S}/*/index.html") + [f"{S}/index.html"]:
    t = open(p, encoding="utf-8").read()
    n = re.sub(r"<li>(?:(?!</li>).)*?/u/(NL-[A-Z0-9]+-\d{4}-[A-Za-z0-9]+)(?:(?!</li>).)*?</li>", lambda m: "" if m.group(1) in WEGH else m.group(0), t, flags=re.S)
    if n != t:
        GEWIJZIGD.append(os.path.relpath(p, R))
        if not DROOG: open(p, "w", encoding="utf-8").write(n)

# ---------- 9. onderwerpen die na het filter leeg zijn (domein -> [onderwerp]) ----------
ONDERWERPEN_WEG = {"openbare-orde": ["strafzaken-bevelen"]}
def weg_onderwerp(o, O):
    if isinstance(o, dict):
        if o.get("id") == O or o.get("o") == O: return None
        return {k: v2 for k, v in o.items() if not (k == O or k.startswith(O + "--")) for v2 in [weg_onderwerp(v, O)] if v2 is not None or v is None}
    if isinstance(o, list):
        if o and any(x == O for x in o[:6] if isinstance(x, str)): return None
        return [y for x in o for y in [weg_onderwerp(x, O)] if y is not None or x is None]
    return o
for dom, lst in ONDERWERPEN_WEG.items():
    for O in lst:
        for p in glob.glob(f"{S}/data/**/*.json", recursive=True) + glob.glob(f"{S}/*.json") + glob.glob(f"{S}/feeds/idx/*.json") + [f"{S}/feeds/index.json"]:
            if re.search(r"/(tekst[0-9]*|tekstindex)\.json$", p) or "/data/u/20" in p: continue
            raw = open(p, encoding="utf-8").read()
            if O not in raw: continue
            d = json.loads(raw); n = weg_onderwerp(d, O)
            if n != d:
                GEWIJZIGD.append(os.path.relpath(p, R))
                m = re.match(r"[^\n]*\n( +)\S", raw[:4000])
                if not DROOG: schrijf(p, n, indent=len(m.group(1)) if m else None, nl=raw.endswith("\n"))
        for f in glob.glob(f"{S}/feeds/{dom}/{O}--*.xml"):
            GEWIJZIGD.append(os.path.relpath(f, R))
            if not DROOG: os.remove(f)
        sm = f"{S}/sitemap.xml"; t = open(sm, encoding="utf-8").read() if os.path.exists(sm) else ""
        n = re.sub(r"<url><loc>[^<]*/o/" + dom + "/" + O + r"--[^<]*</loc>.*?</url>\n?", "", t, flags=re.S)
        if n != t:
            GEWIJZIGD.append("site/sitemap.xml")
            if not DROOG: open(sm, "w", encoding="utf-8").write(n)

print("gewijzigde bestanden:", len(GEWIJZIGD))
for g in sorted(GEWIJZIGD)[:60]: print(" ", g)
print("per domein verwijderd:", {d: n_weg(d) for d in sorted({d for v in INFO.values() for d, _, _ in v})})
print("Daarna: python3 -I scripts/bouw_domeinpaginas.py && python3 -I scripts/bouw_v9.py (statische domeinpagina's met tellingen).")

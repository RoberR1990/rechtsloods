#!/usr/bin/env python3 -I
"""Maakt per live domein een A4-flyer (PDF) uit de data in site/data. Gebruik: python3 -I tools/flyers.py
Cijfers en tekst komen letterlijk uit de data; niets wordt verzonnen. Ontbreekt een bron, dan vervalt het blok."""
import json, re, html, sys, datetime
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
UIT = SITE / "docs" / "flyers"
PEIL = "12 november 2026"  # peildatum zoals op de domeinpagina (index.html)
MND = ["januari","februari","maart","april","mei","juni","juli","augustus","september","oktober","november","december"]

def nl(n): return f"{n:,}".replace(",", ".")
def dat(d):
    y, m, dd = d.split("-"); return f"{int(dd)} {MND[int(m)-1]} {y}"
def esc(t): return html.escape(str(t), quote=True)
def zin1(t, maxlen=190):
    """Eerste volledige zin(nen) uit de data, afgekapt op zinsgrens."""
    t = re.sub(r"\s+", " ", (t or "")).strip()
    zz = re.split(r"(?<=[.;])\s", t)
    out = ""
    for z in zz:
        if out and len(out) + len(z) + 1 > maxlen: break
        out += (" " if out else "") + z
        if len(out) >= 60: break
    out = out.rstrip(";, ")
    out = out + "." if out and out[-1] not in ".!?…" else out
    return out if len(out) <= maxlen + 40 else out[:maxlen].rsplit(" ", 1)[0] + "…"

def css_vars():
    s = (SITE / "index.html").read_text(encoding="utf-8")
    root = re.search(r":root\{(.*?)\}", s, re.S).group(1)
    return root

def laad(slug, pad):
    p = SITE / pad
    meta = json.load(open(p / "meta.json", encoding="utf-8"))
    verr = {x["ecli"]: x for x in json.load(open(p / "verrijkt.json", encoding="utf-8"))}
    meta = [m for m in meta if (verr.get(m["e"]) or {}).get("relevant", True)]  # zelfde filter als de site
    tax = json.load(open(p / "taxonomie.json", encoding="utf-8"))
    stand = json.load(open(p / "stand.json", encoding="utf-8")) if (p / "stand.json").exists() else {}
    return meta, verr, tax, stand

def kernpunten(meta, tax, stand):
    cnt = {}
    for m in meta: cnt[(m["o"], m["s"])] = cnt.get((m["o"], m["s"]), 0) + 1
    rij = []
    for o, d in stand.items():
        for k, v in d.items():
            if v.get("kern") and v.get("lijn") in ("hr-lijn", "vaste-lijn"):
                lab = (tax.get(o, {}).get("sub", {}).get(k)) or ""
                if isinstance(lab, dict): lab = lab.get("label", "")
                if lab: rij.append((cnt.get((o, k), 0), lab.split(" (")[0], v["kern"]))
    rij.sort(key=lambda r: -r[0])
    return rij[:3]

def recente(meta, verr):
    def kz(m):
        v = verr.get(m["e"]);  return (v or {}).get("kern", {}) and v["kern"].get("zin")
    met = [m for m in meta if kz(m)]
    bron = "kern"
    if len(met) < 3:  # geen uitleg in de data: val terug op de inhoudsindicatie van rechtspraak.nl
        met = [m for m in meta if len((m.get("h") or "").strip()) >= 50]; bron = "indicatie"
    met.sort(key=lambda m: (m["d"], m["e"]), reverse=True)
    uit = []
    for m in met[:3]:
        t = kz(m) if bron == "kern" else zin1(m["h"])
        uit.append((m["e"], m["i"], m["d"], t))
    return uit, bron

def bouw(d, css):
    slug = d["slug"]; naam = d["label"]
    meta, verr, tax, stand = laad(slug, d["pad"])
    n = len(meta); laatste = max(m["d"] for m in meta)
    kern = kernpunten(meta, tax, stand)
    rec, bron = recente(meta, verr)
    url = f"rechtsloods.nl/?domein={slug}&utm_source=flyer#domein"
    kb = ""
    if kern:
        kb = '<section><h2>Stand van het recht in het kort</h2><ul class="kern">' + "".join(
            f"<li><b>{esc(l)}.</b> {esc(k)}</li>" for _, l, k in kern) + "</ul></section>"
    ub = "".join(
        f'<li><div class="ec">{esc(e)}</div><div class="mt">{esc(i)} &middot; {esc(dat(dd))}</div><p>{esc(t)}</p></li>'
        for e, i, dd, t in rec)
    noot = ("Uitleg: de inhoudsindicatie van rechtspraak.nl." if bron == "indicatie" else
            "Uitleg: kernzin uit de uitspraak, met de bron erbij op de site.")
    return f"""<!doctype html><html lang="nl"><head><meta charset="utf-8"><title>Rechtsloods: {esc(naam)}</title><style>
:root{{{css}}}
@page{{size:A4;margin:0}}
*{{box-sizing:border-box}}html,body{{margin:0}}
body{{font:10.5pt/1.45 var(--body);color:var(--inkt);width:210mm;height:297mm;padding:16mm 16mm 14mm;position:relative;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.top{{display:flex;justify-content:space-between;align-items:baseline;border-bottom:3px solid var(--groen);padding-bottom:6px}}
.merk{{font-weight:800;font-size:14pt;color:var(--groen-d)}}.merk span{{color:var(--grijs);font-weight:500;font-size:9.5pt;margin-left:6px}}
h1{{font-size:24pt;line-height:1.1;margin:14px 0 4px}}
.kop{{font-size:15pt;font-weight:700;color:var(--groen-d);margin:0 0 10px}}
.cijfer{{background:var(--groen-l);border:1px solid var(--groen-m);border-radius:8px;padding:10px 14px;margin:0 0 12px;display:flex;gap:18px;align-items:baseline}}
.cijfer b{{font-size:22pt;color:var(--groen-d)}}.cijfer span{{color:var(--grijs);font-size:9.5pt}}
h2{{font-size:12pt;margin:0 0 6px;color:var(--groen-d)}}
section{{margin:0 0 12px}}
ul{{margin:0;padding:0;list-style:none}}
.kern li{{padding:5px 0 5px 12px;border-left:3px solid var(--groen);margin:0 0 5px}}
.uit li{{padding:6px 0;border-bottom:1px solid var(--lijn)}}.uit li:last-child{{border:0}}
.ec{{font-weight:700;font-size:10pt}}.mt{{color:var(--grijs);font-size:9pt}}.uit p{{margin:2px 0 0}}
.noot{{color:var(--grijs);font-size:8.5pt;margin:4px 0 0}}
.volg{{background:var(--groen-l);border:1px solid var(--groen-m);border-radius:8px;padding:10px 14px}}
.volg p{{margin:0 0 4px}}.url{{display:inline-block;margin-top:4px;font-weight:800;font-size:11.5pt;color:var(--groen-d);word-break:break-all}}
.voet{{position:absolute;left:16mm;right:16mm;bottom:14mm;border-top:1px solid var(--lijn);padding-top:6px;font-size:8.8pt;color:var(--grijs)}}
</style></head><body>
<div class="top"><div class="merk">Rechtsloods<span>Verkenning van rechtspraak</span></div><div style="font-size:9pt;color:var(--grijs)">Peildatum {PEIL}</div></div>
<h1>{esc(naam)}</h1>
<p class="kop">Jij hoort het eerst.</p>
<div class="cijfer"><b>{nl(n)}</b><span>gepubliceerde uitspraken, 2016&ndash;2026. Peildatum {PEIL}; laatste uitspraak in de set van {esc(dat(laatste))}.</span></div>
{kb}
<section><h2>Drie recente uitspraken</h2><ul class="uit">{ub}</ul><p class="noot">{noot}</p></section>
<section class="volg"><h2>Volg dit onderwerp</h2><p>Melding in Teams of via een feed, met de bron erbij. Melding per e-mail volgt later, bij interesse.</p><span class="url">{esc(url)}</span></section>
<div class="voet">Prototype in validatiefase. Gratis, voor elke gemeente. Geen juridisch advies: de uitspraak zelf is leidend. Mis je een onderwerp? Vraag het aan.</div>
</body></html>"""

def main():
    lijst = [d for d in json.load(open(SITE / "data/domeinen/index.json", encoding="utf-8")) if d["status"] == "live"]
    UIT.mkdir(parents=True, exist_ok=True)
    css = css_vars()
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page()
        for d in lijst:
            h = bouw(d, css)
            (UIT / f"_{d['slug']}.html").write_text(h, encoding="utf-8")
            pg.goto((UIT / f"_{d['slug']}.html").as_uri())
            out = UIT / f"Rechtsloods_Flyer_{d['slug']}.pdf"
            pg.pdf(path=str(out), format="A4", print_background=True, margin=dict(top="0", bottom="0", left="0", right="0"))
            (UIT / f"_{d['slug']}.html").unlink()
            print("ok", out.name)
        b.close()

if __name__ == "__main__": main()

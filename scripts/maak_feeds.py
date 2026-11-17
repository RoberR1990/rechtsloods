"""RSS-feeds per rechtsgebied en per subonderwerp, statisch voor Cloudflare Pages.
Draai na elke data-update: python3 scripts/maak_feeds.py  -> site/feeds/
Alleen uitspraken met samenvatting (v2/v3) en relevant; nieuwste 40 per feed."""
import json, os, html, datetime, re, shutil
BASE = os.environ.get("RL_BASE", "https://rechtsloods.nl/")
SITE = os.path.join(os.path.dirname(__file__), "..", "site")
OUT = os.path.join(SITE, "feeds"); N = 40
hashE = lambda e: re.sub(r"^ECLI:", "", e).replace(":", "-")
def tekst(x):
    if isinstance(x, dict): return x.get("zin", "")
    return x or ""
def rss(titel, link, beschr, items, selflink):
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom"><channel>',
           f"<title>{html.escape(titel)}</title><link>{link}</link>",
           f'<atom:link href="{selflink}" rel="self" type="application/rss+xml"/>',
           f"<description>{html.escape(beschr)}</description><language>nl</language><lastBuildDate>{now}</lastBuildDate>"]
    for it in items:
        out.append("<item>" + "".join(f"<{k}>{v}</{k}>" for k, v in it) + "</item>")
    out.append("</channel></rss>")
    return "\n".join(out)
def item(m, v, slabel):
    e = m["e"]; url = f"{BASE}#uitspraak-{hashE(e)}"
    kern = v.get("kern") or {}
    zin = tekst(kern) or m.get("h", "")
    cit = kern.get("citaat") if isinstance(kern, dict) else None
    d = datetime.datetime.strptime(m["d"], "%Y-%m-%d").strftime("%a, %d %b %Y 12:00:00 GMT")
    body = f"<p>{html.escape(zin)}</p>"
    if cit: body += f"<p><i>Zo schreef de rechter het: “{html.escape(cit)}”</i></p>"
    body += (f"<p>{html.escape(m.get('i',''))}, {m['d']} · {html.escape(slabel)}</p>"
             f'<p>Bron: <a href="https://uitspraken.rechtspraak.nl/details?id={e}">{e}</a>. '
             "Uitleg gemaakt met AI; de uitspraak zelf is leidend. Geen juridisch advies.</p>")
    return [("title", html.escape(v.get("titel") or m.get("h", e)[:90])), ("link", url),
            ("guid", url),
            ("pubDate", d), ("description", f"<![CDATA[{body}]]>")]
def main():
    doms = json.load(open(os.path.join(SITE, "data/domeinen/index.json")))
    if os.path.isdir(OUT): shutil.rmtree(OUT)
    os.makedirs(OUT); lijst = []
    for D in doms:
        if D.get("status") == "binnenkort": continue
        p = os.path.join(SITE, D["pad"])
        try:
            meta = json.load(open(p + "meta.json")); verr = json.load(open(p + "verrijkt.json"))
            tax = json.load(open(p + "taxonomie.json"))
        except FileNotFoundError: continue
        V = {x["ecli"]: x for x in verr if str(x.get("relevant")) not in ("False", "false") and x.get("kern")}
        rows = sorted([m for m in meta if m["e"] in V], key=lambda m: m["d"], reverse=True)
        def sublabel(o, s):
            x = (tax.get(o, {}).get("sub") or {}).get(s, s)
            return x if isinstance(x, str) else (x or {}).get("label", s)
        def osub(m):
            v = V[m["e"]]; return v.get("onderwerp") or m.get("o"), v.get("sub") or m.get("s")
        slug = D["slug"]; os.makedirs(os.path.join(OUT, slug), exist_ok=True)
        f = f"feeds/{slug}.xml"
        its = [item(m, V[m["e"]], sublabel(*osub(m))) for m in rows[:N]]
        open(os.path.join(SITE, f), "w").write(rss(f"Rechtsloods · {D['label']}", BASE,
            f"Nieuwe uitspraken over {D['label'].lower()}, in gewone taal met bron.", its, BASE + f))
        entry = {"slug": slug, "label": D["label"], "feed": f, "n": len(rows), "subs": []}
        per = {}
        for m in rows: per.setdefault(osub(m), []).append(m)
        for (o, s), L in sorted(per.items(), key=lambda kv: -len(kv[1])):
            if not s or o not in tax: continue
            fs = f"feeds/{slug}/{o}--{s}.xml"; lab = sublabel(o, s)
            its = [item(m, V[m["e"]], lab) for m in L[:N]]
            open(os.path.join(SITE, fs), "w").write(rss(f"Rechtsloods · {lab}", BASE,
                f"Nieuwe uitspraken over: {lab}. In gewone taal, met bron.", its, BASE + fs))
            entry["subs"].append({"o": o, "s": s, "label": lab, "feed": fs, "n": len(L), "laatste": L[0]["d"]})
        if rows: lijst.append(entry)
    json.dump(lijst, open(os.path.join(OUT, "index.json"), "w"), ensure_ascii=False, indent=1)
    print(sum(1 + len(x["subs"]) for x in lijst), "feeds", [(x["slug"], x["n"], len(x["subs"])) for x in lijst])
main()

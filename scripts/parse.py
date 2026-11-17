"""Parse open-data XML naar schone JSON per uitspraak (metadata + genummerde alinea's)."""
import json, os, re, html, sys
from xml.etree import ElementTree as ET

NS = {"rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#", "dcterms": "http://purl.org/dc/terms/",
      "psi": "http://psi.rechtspraak.nl/", "rs": "http://www.rechtspraak.nl/schema/rechtspraak-1.0",
      "ecli": "https://e-justice.europa.eu/ecli", "rdfs": "http://www.w3.org/2000/01/rdf-schema#"}
XML = "/home/claude/data/xml"
K = {r["ecli"]: r for r in json.load(open("/home/claude/data/kandidaten2.json"))}

def txt(el):
    return re.sub(r"\s+", " ", "".join(el.itertext())).strip()

GEM = re.compile(r"(?:heffingsambtenaar|college van burgemeester en wethouders|burgemeester|college|raad|hoofd [\w ]+?) (?:van|der) (?:de )?gemeente ([A-Z][\w\-' ]+?)(?:[,.)]| te | en |$)")
NR = re.compile(r"^(\d{1,2}(?:\.\d{1,2}){0,3})\.\s+(?=\S)|^(\d{1,2}\.\d{1,2}(?:\.\d{1,2})*)\s+(?=\S)")

def parse(path):
    root = ET.parse(path).getroot()
    d = root.find("rdf:RDF/rdf:Description", NS)
    g = lambda t: (d.find(t, NS).text or "").strip() if d.find(t, NS) is not None else ""
    ecli = g("dcterms:identifier")
    rel = []
    for r in d.findall("dcterms:relation", NS):
        rel.append({"ecli": r.get(f"{{{NS['ecli']}}}resourceIdentifier"),
                    "type": (r.get(f"{{{NS['psi']}}}type") or "").split("/")[-1],
                    "aanleg": (r.get(f"{{{NS['psi']}}}aanleg") or "").split("/")[-1],
                    "gevolg": (r.get(f"{{{NS['psi']}}}gevolg") or "").split("#")[-1]})
    ind = root.find("rs:inhoudsindicatie", NS)
    up = root.find("rs:uitspraak", NS)
    up = up if up is not None else root.find("rs:conclusie", NS)
    paras, cur = [], None
    if up is not None:
        for p in up.iter():
            tag = p.tag.split("}")[-1]
            if tag not in ("para", "title", "bridgehead"):
                continue
            t = txt(p)
            nrel = p.find("rs:nr", NS)
            nrv = (nrel.text or "").strip().rstrip(".") if nrel is not None else None
            if nrv and t.startswith(nrv):
                t = t[len(nrv):].lstrip(". ")
            if not t or (tag == "para" and any(c.tag.split("}")[-1] == "para" for c in p)):
                continue
            m = NR.match(t)
            num = nrv or (m and (m.group(1) or m.group(2)))
            if num:
                cur = num
            paras.append({"id": len(paras), "nr": num or None, "rov": cur, "t": t, "kop": tag != "para"})
    full = " ".join(p["t"] for p in paras)
    gm = GEM.search(full) or re.search(r"(?:heffingsambtenaar|hoofd|directeur) (?:van|der) (?:de |het )?((?:Belastingsamenwerking|Gemeentebelastingen|Cocensus|BSGR|Belastingen|Svhw|SVHW|Gemeenschappelijke Regeling)[\w\-' ]*?)[,.(]", full) or re.search(r"(?:college|heffingsambtenaar|burgemeester) van ([A-Z][a-z][\w\-']+(?: [A-Z][\w\-']+)?)[,. ]", full)
    besl = ""
    for s in (up.iter() if up is not None else []):
        if s.tag.endswith("section") and s.get("role") == "beslissing":
            besl = txt(s)
    k = K.get(ecli, {})
    return {"ecli": ecli, "instantie": g("dcterms:creator"), "datum": g("dcterms:date"),
            "publicatie": g("dcterms:issued"), "zaaknr": g("psi:zaaknummer"),
            "procedure": g("psi:procedure"), "rechtsgebied": g("dcterms:subject"),
            "zittingsplaats": g("dcterms:spatial"),
            "inhoud": txt(ind) if ind is not None else k.get("summary", ""),
            "gemeente": gm.group(1).strip() if gm else None,
            "beslissing": besl[:600], "relaties": rel, "onderwerp": k.get("onderwerp"), "extra": k.get("extra", []),
            "alineas": paras, "tekens": len(full)}

if __name__ == "__main__":
    out, err = [], 0
    for f in sorted(os.listdir(XML)):
        if f[:-4].replace("_", ":") not in K: continue
        try:
            out.append(parse(os.path.join(XML, f)))
        except Exception as e:
            err += 1
    json.dump(out, open("/home/claude/data/uitspraken.json", "w"), ensure_ascii=False)
    print(len(out), "geparsed,", err, "fouten")

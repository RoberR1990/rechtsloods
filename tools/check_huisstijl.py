#!/usr/bin/env python3 -I
"""Huisstijl-bewaker: faalt als er groen (tint 80-170 graden) in code of afbeeldingen van site/ staat.
Gebruik: python3 -I tools/check_huisstijl.py   (draait ook in GitHub Actions bij elke push)"""
import re, sys, colorsys
from pathlib import Path
SITE = Path(__file__).resolve().parent.parent / "site"
TOEGESTAAN_GROEN = set()   # bewust groen, bv. voor 'gewonnen/toegewezen'-status: voeg hex toe in hoofdletters
def is_groen(hexw):
    r, g, b = (int(hexw[i:i+2], 16) / 255 for i in (0, 2, 4))
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return s > 0.08 and 80 <= h * 360 <= 170
fouten = []
for p in SITE.rglob("*"):
    if p.suffix in {".html", ".css", ".js", ".svg", ".txt"} or (p.suffix == ".json" and "domeinen/index" in str(p)):
        t = p.read_text(encoding="utf8", errors="ignore")
        for m in set(re.findall(r"#([0-9a-fA-F]{6})\b", t)):
            if is_groen(m) and m.upper() not in TOEGESTAAN_GROEN: fouten.append(f"{p.relative_to(SITE.parent)}: #{m.upper()}")
try:
    from PIL import Image
    for p in list((SITE / "assets").glob("*")) + list((SITE / "video").glob("*.jpg")):
        if p.suffix.lower() not in {".webp", ".jpg", ".png"}: continue
        im = Image.open(p).convert("RGB").resize((96, 96)); px = list(im.getdata()); n = 0; tot = 0
        for r, g, b in px:
            h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)
            if .12 < l < .9 and s > .15:
                tot += 1; n += 80 <= h * 360 <= 170
        if tot and n / tot > 0.15: fouten.append(f"{p.relative_to(SITE.parent)}: {round(100*n/tot)}% van de gekleurde pixels is groen (draai tools/herkleur_afbeeldingen.py)")
except ImportError: print("Pillow ontbreekt: afbeeldingscheck overgeslagen")
if fouten: print("Groen gevonden (huisstijl is petrol #0F5C63):\n  " + "\n  ".join(sorted(fouten))); sys.exit(1)
print("Huisstijl OK: geen groen in code of afbeeldingen.")

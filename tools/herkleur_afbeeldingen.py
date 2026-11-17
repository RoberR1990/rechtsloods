#!/usr/bin/env python3 -I
"""Zet groen in illustraties om naar het huisstijl-petrol. Idempotent: al-petrol pixels blijven staan.
Gebruik: python3 -I tools/herkleur_afbeeldingen.py site/assets/*.webp   (schrijft in place)
Oranje, blauw en donkerblauw (inkt) blijven ongemoeid; alleen tinten tussen 80 en 170 graden verschuiven."""
import sys, numpy as np
from PIL import Image
VAN_LO, VAN_HI, SHIFT, SAT = 80.0, 170.0, 54.0, 0.78   # #00811F (130 graden) -> #0F5C63 (184 graden)
def herkleur(im):
    a = np.asarray(im.convert("RGBA")).astype(np.float32) / 255
    r, g, b, al = a[..., 0], a[..., 1], a[..., 2], a[..., 3]
    mx, mn = a[..., :3].max(-1), a[..., :3].min(-1); d = mx - mn
    l = (mx + mn) / 2
    s = np.where(d == 0, 0, d / (1 - np.abs(2 * l - 1) + 1e-9))
    h = np.zeros_like(mx)
    m = d > 0
    rm = m & (mx == r); gm = m & (mx == g) & ~rm; bm = m & ~rm & ~gm
    h[rm] = ((g - b)[rm] / d[rm]) % 6; h[gm] = (b - r)[gm] / d[gm] + 2; h[bm] = (r - g)[bm] / d[bm] + 4
    h *= 60
    sel = (h >= VAN_LO) & (h <= VAN_HI) & (s > 0.04)
    h = np.where(sel, h + SHIFT, h); s = np.where(sel, s * SAT, s)
    c = (1 - np.abs(2 * l - 1)) * s; hp = (h / 60) % 6; x = c * (1 - np.abs(hp % 2 - 1)); mm = l - c / 2
    z = np.zeros_like(c); k = np.floor(hp).astype(int)
    rgb = np.select([(k == i)[..., None] for i in range(6)],
                    [np.stack(t, -1) for t in ((c, x, z), (x, c, z), (z, c, x), (z, x, c), (x, z, c), (c, z, x))])
    out = np.concatenate([np.clip((rgb + mm[..., None]) * 255 + .5, 0, 255), (al * 255)[..., None]], -1).astype(np.uint8)
    return Image.fromarray(out, "RGBA")
if __name__ == "__main__":
    for p in sys.argv[1:]:
        im = Image.open(p); fmt = im.format; o = herkleur(im)
        if fmt == "JPEG": o = o.convert("RGB")
        o.save(p, fmt, **({"quality": 88, "method": 6} if fmt == "WEBP" else {"quality": 92} if fmt == "JPEG" else {}))
        print("herkleurd:", p)

#!/usr/bin/env python3
"""Maakt de 3 uitleg-PDF's 'Hoe de nachtrun met subagents werkt'.
Gebruik: python3 scripts/uitleg_pdf.py   (actuele cijfers worden zelf opgehaald)
Uitvoer: docs/uitleg/1-de-fabriek.pdf, 2-van-uitspraak-tot-samenvatting.pdf, 3-spelregels-voor-vibecoders.pdf
"""
import os, re, subprocess, textwrap, datetime
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

OUT = "/home/claude/rechtzoeker/docs/uitleg"
DATA = "/home/claude/data"
GROEN, GRIJS, LGRIJS, ZWART = "#00811F", "#6B6B6B", "#EEEEEE", "#222222"
C_ROBERT, C_ORCH, C_SONNET, C_HAIKU, C_REV, C_SCRIPT, C_MEM = (
    "#00811F", "#1F4E9C", "#B8620A", "#7B3FA0", "#B3261E", "#4A4A4A", "#0E7C86")
LICHT = {c: c + "22" for c in (C_ROBERT, C_ORCH, C_SONNET, C_HAIKU, C_REV, C_SCRIPT, C_MEM)}
plt.rcParams["font.family"] = "DejaVu Sans"

# ---------- actuele cijfers ----------
def telling():
    def tel(d):
        n = 0
        for _, _, fs in os.walk(os.path.join(DATA, d)):
            n += len(fs)
        return n
    try:
        stand = subprocess.run(["python3", "/home/claude/scripts/volgende.py", "stand"],
                               capture_output=True, text=True, timeout=60).stdout.strip().splitlines()
    except Exception:
        stand = []
    klaar = tot = lopend = 0
    for r in stand:
        m = re.search(r"(\d+)/(\d+) batches klaar, lopend (\d+)", r)
        if m:
            klaar += int(m[1]); tot += int(m[2]); lopend += int(m[3])
    return dict(v3=tel("uit_v3"), l1=tel("uit_l1"), stand=stand, klaar=klaar, tot=tot,
                lopend=lopend, tijd=datetime.datetime.now().strftime("%d-%m-%Y %H:%M"))

CIJ = telling()

# ---------- tekenhulp ----------
def pagina(titel, sub=None, nr=None, totaal=None):
    fig = plt.figure(figsize=(11.69, 8.27))
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 297); ax.set_ylim(0, 210); ax.axis("off")
    ax.add_patch(Rectangle((0, 198), 297, 12, color=GROEN, lw=0))
    ax.text(10, 204, titel, color="white", fontsize=17, fontweight="bold", va="center")
    if sub:
        ax.text(10, 192.5, sub, color=GRIJS, fontsize=10, va="center")
    if nr:
        ax.text(287, 4, f"{nr}/{totaal}", color=GRIJS, fontsize=8, ha="right")
    ax.text(10, 4, "Rechtzoeker · Makers DGW Parkeren · Gemeente Rotterdam", color=GRIJS, fontsize=7.5)
    return fig, ax

def wrap(t, n):
    return "\n".join(textwrap.fill(p, n) for p in t.split("\n"))

def box(ax, x, y, w, h, tekst, kleur=GROEN, fs=8.5, bold_first=True, n=None, tc=ZWART, vul=True, ha="center"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=2",
                                fc=(kleur + "22") if vul else "white", ec=kleur, lw=1.5))
    if n is None:
        n = max(8, int(w * 0.9 * 8.5 / fs / 1.0 * 0.55))
    regels = wrap(tekst, n).split("\n")
    lh = fs * 0.5
    totaalh = len(regels) * lh
    y0 = y + h / 2 + totaalh / 2 - lh / 2
    for i, r in enumerate(regels):
        ax.text(x + (w / 2 if ha == "center" else 2), y0 - i * lh, r, fontsize=fs, ha=ha, va="center", color=tc,
                fontweight="bold" if (bold_first and i == 0) else "normal")

def pijl(ax, x1, y1, x2, y2, kleur=GRIJS, lw=1.8, stijl="-|>", rad=0.0):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=stijl, mutation_scale=13, color=kleur, lw=lw,
                                 connectionstyle=f"arc3,rad={rad}"))

def tabel(ax, x, y, kol_b, rijen, kop, fs=7.6, kleuren=None, regelh=3.6, n_factor=0.62):
    """Eenvoudige tabel; geeft onderkant y terug."""
    tot = sum(kol_b)
    ax.add_patch(Rectangle((x, y - 6), tot, 6, color=GROEN, lw=0))
    cx = x
    for b, k in zip(kol_b, kop):
        ax.text(cx + 1.5, y - 3, k, color="white", fontsize=fs + 0.6, fontweight="bold", va="center")
        cx += b
    y -= 6
    for ri, rij in enumerate(rijen):
        cellen = []
        for b, c in zip(kol_b, rij):
            cellen.append(wrap(c, max(8, int((b - 3) / (fs * 0.2) * n_factor * 1.0))).split("\n"))
        hh = max(len(c) for c in cellen) * regelh + 2.4
        ax.add_patch(Rectangle((x, y - hh), tot, hh, fc=(LGRIJS if ri % 2 == 0 else "white"), ec="#DDDDDD", lw=0.5))
        if kleuren:
            ax.add_patch(Rectangle((x, y - hh), 1.6, hh, color=kleuren[ri], lw=0))
        cx = x
        for b, c, ci in zip(kol_b, cellen, range(len(kol_b))):
            for li, l in enumerate(c):
                ax.text(cx + 3, y - 2.4 - li * regelh, l, fontsize=fs, va="center",
                        fontweight="bold" if ci == 0 else "normal", color=ZWART)
            cx += b
        y -= hh
    return y

def kop_blok(ax, x, y, tekst, kleur=GROEN, fs=11):
    ax.text(x, y, tekst, fontsize=fs, fontweight="bold", color=kleur, va="center")

# =====================================================================
# PDF 1: De fabriek
# =====================================================================
def pdf1():
    with PdfPages(f"{OUT}/1-de-fabriek.pdf") as pdf:
        # --- pagina 1: de plaat
        fig, ax = pagina("De fabriek: wie doet wat in de nachtrun",
                         "Eén dirigent, veel kleine helpers, scripts die controleren, en een geheugen op schijf.", 1, 2)
        ax.text(287, 12, f"Stand om {CIJ['tijd']}:  {CIJ['v3']} volledige samenvattingen (laag 2)  ·  {CIJ['l1']} indelingen (laag 1)  ·  {CIJ['klaar']}/{CIJ['tot']} batches klaar, {CIJ['lopend']} lopend",
                color=GROEN, fontsize=8.5, ha="right", va="center", fontweight="bold")
        # Robert
        box(ax, 8, 150, 52, 32, "Robert\nOpdrachtgever. Schrijft de startopdracht en de besluiten. Slaapt tijdens de run.", C_ROBERT, 8.5, n=30)
        # Orchestrator
        box(ax, 85, 142, 62, 42, "Orchestrator (hoofdsessie, Opus)\nDe dirigent. Plant, schrijft instructies en controlescripts, draait een proef, verdeelt batches, start golven, controleert, commit en pusht, houdt Robert op de hoogte. Doet zelf bijna geen inhoudelijk werk.", C_ORCH, 8.2, n=38)
        pijl(ax, 60, 166, 85, 166, C_ROBERT)
        ax.text(72.5, 169, "opdracht", fontsize=7.5, ha="center", color=GRIJS)
        pijl(ax, 85, 154, 60, 154, C_ORCH)
        ax.text(72.5, 148, "korte update", fontsize=7.5, ha="center", color=GRIJS)
        # Reviewers
        box(ax, 175, 150, 56, 32, "Reviewers (Sonnet, 2 persona's)\n'Jurist' en 'nieuwkomer klantcontact' geven een cijfer. Beide moeten ≥ 7.", C_REV, 8.2, n=32)
        pijl(ax, 147, 168, 175, 168, C_REV)
        ax.text(161, 171, "proef", fontsize=7.5, ha="center", color=GRIJS)
        # Golf
        ax.add_patch(FancyBboxPatch((8, 84), 160, 50, boxstyle="round,pad=0,rounding_size=2", fc="white", ec=GRIJS, lw=1.2, ls="--"))
        ax.text(12, 130, "Een golf: tot 20 helpers tegelijk, elk één batch, verse sessie", fontsize=8.3, fontweight="bold", color=GRIJS, va="center")
        for i in range(10):
            xx = 12 + i * 8.6
            kl = C_SONNET if i < 4 else C_HAIKU
            ax.add_patch(FancyBboxPatch((xx, 108), 7, 14, boxstyle="round,pad=0,rounding_size=1.2", fc=kl + "33", ec=kl, lw=1.2))
            ax.text(xx + 3.5, 115, "S" if i < 4 else "H", ha="center", va="center", fontsize=9, fontweight="bold", color=kl)
        ax.text(12, 103, "...en nog tien", fontsize=7.5, color=GRIJS)
        ax.add_patch(Rectangle((12, 94), 3.4, 3.4, color=C_SONNET)); ax.text(17, 95.7, "Sonnet: laag 2 (volledige samenvatting), concept-taxonomieën, persona-reviews", fontsize=7.6, va="center")
        ax.add_patch(Rectangle((12, 88), 3.4, 3.4, color=C_HAIKU)); ax.text(17, 89.7, "Haiku: laag 1 (snelle indeling, 25 per batch), rechtbankzaken (6 per batch)", fontsize=7.6, va="center")
        pijl(ax, 116, 142, 116, 134, C_ORCH)
        ax.text(120, 138, "start golf, verdeelt batches", fontsize=7.5, color=GRIJS, va="center")
        # Scripts
        box(ax, 180, 84, 60, 50, "Scripts (geen AI)\nGratis en voorspelbaar. Ophalen, parsen, inkorten, batches maken, volgende kiezen, controleren (elk citaat letterlijk in de bron), sitebestanden bouwen, standblok bijwerken.", C_SCRIPT, 8, n=36)
        pijl(ax, 168, 108, 180, 108, C_SCRIPT, stijl="<|-|>")
        ax.text(174, 111, "check", fontsize=7.5, ha="center", color=GRIJS)
        # Geheugen
        box(ax, 8, 30, 120, 40, "Geheugen op schijf (niet in het hoofd van de AI)\nBatchlijsten · lopend.json (wie werkt waaraan) · uitvoerbestand per uitspraak · docs/STAND.md · git-branch 'domeinen'. Daardoor kan een volgende sessie precies verder.", C_MEM, 8.4, n=70)
        pijl(ax, 80, 84, 80, 70, C_MEM, stijl="<|-|>")
        pijl(ax, 210, 84, 130, 56, C_SCRIPT, rad=-0.15)
        # Site
        box(ax, 150, 30, 60, 40, "Site\nAlleen uitspraken met bron-alinea + letterlijk citaat komen erin. Foute zinnen vallen weg.", C_ROBERT, 8.2, n=34)
        pijl(ax, 128, 50, 150, 50, C_MEM)
        # Vergelijking
        box(ax, 225, 30, 64, 40, "Vergelijking\nDe orchestrator is de regisseur. De helpers zijn uitzendkrachten voor één dag met één opdracht. De scripts zijn de poortwachter. Het geheugen is het logboek.", GRIJS, 7.8, n=36)
        ax.text(8, 22, "Let op: er is geen aparte orchestrator-subagent. De hoofdsessie ís de dirigent. Dat bespaart dure tokens.", fontsize=8.5, color=C_ORCH, fontweight="bold")
        pdf.savefig(fig); plt.close(fig)

        # --- pagina 2: rollen-tabel
        fig, ax = pagina("De rollen op een rij", "Wat elke rol doet, en wat hij niet mag.", 2, 2)
        rijen = [
            ["Robert", "Mens", "Schrijft de startopdracht en de besluiten (twee lagen; laag 2 alleen hoogste rechters, hoven en Rotterdam).", "Wordt 's nachts niets gevraagd. Alles moet in de opdracht staan."],
            ["Orchestrator", "Claude Opus (hoofdsessie)", "Plan, instructies en controlescripts schrijven; proef draaien; batches verdelen; golven van max. 20 helpers starten; resultaten controleren; committen en pushen; incidenten afhandelen; Robert updaten.", "Doet zelf bijna geen inhoudelijk werk. Er is geen aparte orchestrator-subagent."],
            ["Werker (Sonnet)", "Sonnet, subagent", "Volledige samenvatting (laag 2) voor hoge rechters en hoven; concept-taxonomieën per domein; persona-reviews.", "Alleen Bash, Read, Write. Nooit een geplande taak aanmaken of berichten sturen."],
            ["Werker (Haiku)", "Haiku, subagent", "Snelle indeling (laag 1, 25 uitspraken per batch) en samenvattingen van rechtbankzaken (6 per batch).", "Zelfde grenzen. Mag 'weet ik niet' antwoorden (zekerheid 'laag')."],
            ["Reviewer", "Sonnet, persona", "Speelt 'jurist' en 'nieuwkomer klantcontact' en geeft een cijfer. Drempel: beide ≥ 7. Proef: jurist 8, klantcontact 7 (vorige versie gemiddeld 5,5).", "Past niets aan. Geeft alleen een oordeel."],
            ["Scripts", "Python, geen AI", "Ophalen, parsen, inkorten, batches maken, volgende kiezen, controleren, sitebestanden bouwen, standblok bijwerken.", "Kunnen niet 'denken'. Controle is alleen zo goed als de regels erin."],
            ["Geheugen op schijf", "Bestanden en git", "Batchlijsten, lopend.json, uitvoer per uitspraak, docs/STAND.md, branch 'domeinen'.", "Onthoudt niets zelf: wat niet is opgeslagen, is weg."],
        ]
        kl = [C_ROBERT, C_ORCH, C_SONNET, C_HAIKU, C_REV, C_SCRIPT, C_MEM]
        tabel(ax, 10, 186, [32, 38, 124, 83], rijen, ["Rol", "Model", "Taak", "Wat hij niet mag"], fs=8.2, kleuren=kl, regelh=4.2, n_factor=0.78)
        pdf.savefig(fig); plt.close(fig)

# =====================================================================
# PDF 2: De lopende band
# =====================================================================
def pdf2():
    with PdfPages(f"{OUT}/2-van-uitspraak-tot-samenvatting.pdf") as pdf:
        fig, ax = pagina("De lopende band: van uitspraak tot samenvatting",
                         "Negen stappen. De rode slagbomen laten alleen door wat klopt.", 1, 2)
        stappen = [
            ("1 Ophalen", "dom_fetch.py", C_SCRIPT), ("2 Parsen", "dom_parse.py", C_SCRIPT),
            ("3 Inkorten", "maak_in_v3.py\nmaak_in_l1.py", C_SCRIPT), ("4 Laag 1", "Haiku, 25 per batch", C_HAIKU),
            ("5 Selectie", "alleen hoogste rechters, hoven, Rotterdam", C_SCRIPT), ("6 Laag 2", "Sonnet of Haiku, volledig", C_SONNET),
            ("7 Check", "check_uit_v3.py check_l1.py", C_REV), ("8 Bouwen", "dom_build.py", C_SCRIPT),
            ("9 STAND + git", "stand_auto.py, commit, push", C_MEM),
        ]
        bw, bh, gap = 28, 26, 4.5
        x0, yb = 8, 140
        for i, (t, s, k) in enumerate(stappen):
            x = x0 + i * (bw + gap) if i < 9 else x0
            if i == 7: pass
            box(ax, x if i < 9 else x0, yb, bw, bh, f"{t}\n{s}", k, 7.6, n=17)
            if i < 8:
                pijl(ax, x + bw, yb + bh / 2, x + bw + gap, yb + bh / 2, GRIJS, 1.5)
        # slagbomen
        for x, t in [(x0 + 3 * (bw + gap) + bw + gap / 2 - 14, "Poort 1\nproef 12 uitspraken\n+ 2 persona's ≥ 7"),
                     (x0 + 6 * (bw + gap) + bw + gap / 2 - 14, "Poort 3\norchestrator draait\ncheck over alles")]:
            pass
        poorten = [
            (x0 + 3.0 * (bw + gap) - 10, "Poort 1", "Proef op 12 uitspraken + 2 persona's allebei ≥ 7, vóór opschalen."),
            (x0 + 6.0 * (bw + gap) - 10, "Poort 2 + 3", "Elke helper draait zelf de check tot 0 fouten. Daarna draait de orchestrator de check over alles."),
            (x0 + 7.0 * (bw + gap) + 4, "Poort 4", "Bij bouwen nogmaals alle citaten controleren. Foute zinnen vallen weg."),
        ]
        ys = [112, 112, 112]
        px = [20, 100, 190]
        for (x, t, d), xx in zip(poorten, px):
            ax.add_patch(Rectangle((xx, 96), 3, 22, color=C_REV, lw=0))
            ax.add_patch(Rectangle((xx - 4, 118), 11, 3, color=C_REV, lw=0))
            ax.text(xx + 6, 112, t, fontsize=9, fontweight="bold", color=C_REV, va="center")
            ax.text(xx + 6, 104, wrap(d, 40), fontsize=7.6, va="top", color=ZWART)
        ax.text(10, 132, "Kwaliteitspoorten (slagbomen)", fontsize=10, fontweight="bold", color=C_REV)
        ax.text(10, 128, "Poort 5: concept-taxonomieën blijven 'concept' tot een vakcollega ze nakijkt.", fontsize=8, color=GRIJS)
        # twee lagen
        kop_blok(ax, 10, 84, "Twee lagen, twee prijzen: tokens per uitspraak", GROEN, 11)
        data = [("Laag 1: alleen labels", 7000, C_HAIKU, "onderwerp, sub, kenmerk, zaaktype, partijen, uitkomst + 1 letterlijk citaat (Haiku). Voor alle uitspraken."),
                ("Laag 2: volledige v3-samenvatting", 25000, C_SONNET, "per zin bron-alinea + letterlijk citaat, klantuitleg, acties voor de gemeente. Voor de prioriteit (gemeten)."),
                ("Schatting laag 2 vooraf", 13000, GRIJS, "12 tot 14 duizend geschat: in werkelijkheid ruim 2× zoveel.")]
        maxw = 130
        for i, (naam, tok, k, uitleg) in enumerate(data):
            y = 72 - i * 19
            ax.text(10, y + 5.5, naam, fontsize=8.6, fontweight="bold", va="center")
            ax.add_patch(Rectangle((10, y - 3), maxw * tok / 25000, 6.5, fc=k + ("44" if k == GRIJS else "AA"), ec=k, lw=1.2, ls="--" if k == GRIJS else "-"))
            ax.text(12 + maxw * tok / 25000, y, f"~{tok//1000}k", fontsize=9.5, fontweight="bold", va="center", color=k)
            ax.text(10, y - 6.5, wrap(uitleg, 125), fontsize=7.3, color=GRIJS, va="top")
        ax.text(10, 14, "Verhouding: laag 2 kost ongeveer 3,5× zoveel als laag 1 per uitspraak. Daarom krijgt alleen de prioriteit laag 2.", fontsize=8.3, fontweight="bold", color=GROEN)
        # rechts: stand
        box(ax, 190, 24, 98, 58, f"Stand om {CIJ['tijd']}\nLaag 2 (v3): {CIJ['v3']} bestanden\nLaag 1: {CIJ['l1']} bestanden\nBatches klaar: {CIJ['klaar']} van {CIJ['tot']}\nBatches lopend: {CIJ['lopend']}\n\n" + "\n".join(CIJ["stand"][:8]), GROEN, 7.6, n=60, ha="left", vul=True)
        pdf.savefig(fig); plt.close(fig)

        # pagina 2: ritme + gang van een batch
        fig, ax = pagina("Het ritme van een golf", "Wat er gebeurt in 5 tot 9 minuten, en wat er daarna met het werk gebeurt.", 2, 2)
        kop_blok(ax, 10, 180, "Eén golf, stap voor stap")
        st = [("Kiezen", "volgende.py / golf.sh kiest de volgende batches en schrijft ze in lopend.json.", C_SCRIPT),
              ("Starten", "De orchestrator start tot 20 helpers tegelijk (de limiet).", C_ORCH),
              ("Werken", "Elke helper leest zijn batch, schrijft een bestand per uitspraak, draait zelf de check tot 0 fouten en meldt afwijkingen.", C_SONNET),
              ("Controleren", "De orchestrator draait de check over alles en kijkt naar de meldingen.", C_REV),
              ("Vastleggen", "stand_auto.py werkt het standblok bij, daarna commit en push.", C_MEM)]
        for i, (t, d, k) in enumerate(st):
            x = 10 + i * 56
            box(ax, x, 128, 50, 44, f"{t}\n{d}", k, 8, n=27)
            if i < 4: pijl(ax, x + 50, 150, x + 56, 150)
        # cijfers
        for i, (g, l) in enumerate([("~20", "batches per golf"), ("5 tot 9", "minuten per golf"), ("~120", "batches per uur"), ("20", "helpers tegelijk (limiet)")]):
            x = 10 + i * 70
            ax.add_patch(FancyBboxPatch((x, 84), 64, 30, boxstyle="round,pad=0,rounding_size=2", fc=LGRIJS, ec="#CCCCCC"))
            ax.text(x + 32, 102, g, fontsize=22, fontweight="bold", color=GROEN, ha="center", va="center")
            ax.text(x + 32, 90, l, fontsize=9, ha="center", va="center", color=GRIJS)
        kop_blok(ax, 10, 72, "Wat bij de check gebeurt")
        pt = ["Elk citaat moet letterlijk in de bron-alinea staan.",
              "Velden mogen alleen waarden uit de vaste lijsten hebben.",
              "Ontbreekt het dictum in de bron? Dan zet de helper zekerheid 'laag'. 'Weet ik niet' is een geldig antwoord.",
              "Bij fouten maakt de helper de uitvoer opnieuw. Pas bij 0 fouten is een batch klaar."]
        for i, t in enumerate(pt):
            ax.add_patch(Rectangle((12, 60 - i * 11 - 1.5), 3, 3, color=GROEN))
            ax.text(18, 60 - i * 11, wrap(t, 120), fontsize=8.6, va="center")
        pdf.savefig(fig); plt.close(fig)

# =====================================================================
# PDF 3: Spelregels
# =====================================================================
def pdf3():
    with PdfPages(f"{OUT}/3-spelregels-voor-vibecoders.pdf") as pdf:
        # p1 spelregels
        fig, ax = pagina("Spelregels voor vibecoders", "Wil je zelf een nachtrun doen? Houd je aan deze 10 regels, met het waarom erbij.", 1, 3)
        regels = [
            ("Eerst meten, dan de nacht in", "Kosten waren 2× hoger dan geschat. Draai een kleine proef en reken door."),
            ("Eén dirigent, veel kleine helpers", "De hoofdsessie plant en controleert. Helpers doen het werk. Dat spaart dure tokens."),
            ("Eén batch per helper, verse sessie", "Kleine opdracht, kleine kans op fouten, makkelijk opnieuw te doen."),
            ("Geef helpers alleen Bash, Read, Write", "Minder gereedschap, minder verrassingen. Geen planner, geen berichten."),
            ("Zet verboden in de instructie én in de prompt", "Eén plek is niet genoeg. Controleer achteraf of het gelukt is."),
            ("Laat een script controleren, niet de AI", "Een script is gratis en voorspelbaar. Elk citaat moet letterlijk in de bron staan."),
            ("Maak 'weet ik niet' een geldig antwoord", "Anders gaat de AI gokken. Zet dan zekerheid op 'laag'."),
            ("Laat helpers afwijkingen melden", "Zo vonden we een bug in het inkorten. Een melding is gratis, een stille fout niet."),
            ("Sla alles op schijf op", "Batchlijsten, lopend.json, STAND.md, git. Een volgende sessie kan zo verder."),
            ("Commit en push na elke golf", "Dan raak je nooit meer dan één golf kwijt."),
        ]
        for i, (r, w) in enumerate(regels):
            col, row = divmod(i, 5)
            x = 10 + col * 141
            y = 168 - row * 31
            ax.add_patch(FancyBboxPatch((x, y - 24), 136, 27, boxstyle="round,pad=0,rounding_size=2", fc=LGRIJS, ec="#CCCCCC"))
            ax.add_patch(Rectangle((x, y - 24), 13, 27, color=GROEN, lw=0))
            ax.text(x + 6.5, y - 10.5, str(i + 1), fontsize=18, fontweight="bold", color="white", ha="center", va="center")
            ax.text(x + 16, y - 3, wrap(r, 62), fontsize=9, fontweight="bold", va="center")
            ax.text(x + 16, y - 13, wrap("Waarom: " + w, 74), fontsize=7.8, va="center", color=GRIJS)
        pdf.savefig(fig); plt.close(fig)

        # p2 incidenten
        fig, ax = pagina("Wat ging mis, en wat doen we nu", "Eerlijk: vier dingen liepen niet zoals bedoeld.", 2, 3)
        rijen = [
            ["Haiku-helpers maakten 2× per ongeluk een geplande taak 'placeholder' aan (en 1× een mislukte poging), ondanks de regel.",
             "De orchestrator zette ze uit. Verwijderen mocht niet automatisch: Robert moet ze weggooien.",
             "Verbod expliciet in instructie én prompt zetten, en achteraf controleren."],
            ["Bug in het inkorten van de invoer: overwegingen vielen weg na 'Wettelijk kader'.",
             "Een helper meldde het. Script gerepareerd, 2 uitspraken opnieuw gedaan.",
             "Laat helpers afwijkingen melden in hun rapport."],
            ["Sommige uitspraken missen het dictum in de bron.",
             "Helpers zetten zekerheid 'laag'.",
             "Maak 'weet ik niet' een geldig antwoord."],
            ["Kosten waren 2× hoger dan geschat (laag 2: ~25k in plaats van 12 tot 14k tokens per uitspraak).",
             "Gemeten op de proef: ~25k in plaats van de geschatte 12 tot 14k.",
             "Eerst meten op een kleine proef, dan pas de nacht in."],
        ]
        tabel(ax, 10, 184, [92, 92, 93], rijen, ["Wat ging mis", "Wat we deden", "Wat we nu doen"], fs=8.6, kleuren=[C_REV] * 4, regelh=4.5, n_factor=0.8)
        pdf.savefig(fig); plt.close(fig)

        # p3 checklist + kosten
        fig, ax = pagina("Voor je een nachtrun start", "Vink af. Daaronder een mini-kostenrekensom.", 3, 3)
        kop_blok(ax, 10, 180, "Checklist")
        cl = ["De startopdracht is zo volledig dat er 's nachts niets gevraagd hoeft te worden.",
              "Proef gedraaid op ~12 stuks; kosten per stuk gemeten.",
              "Twee persona-reviews gedaan; beide cijfers ≥ 7.",
              "Controlescript bestaat en geeft 0 fouten op de proef.",
              "Verboden staan in instructie én prompt (geen geplande taken, geen berichten).",
              "Helpers hebben alleen Bash, Read, Write.",
              "Batchlijsten, lopend.json en STAND.md staan op schijf; git-branch is klaar.",
              "Golfgrootte max. 20 helpers; commit en push na elke golf.",
              "Helpers weten dat 'weet ik niet' mag en dat ze afwijkingen melden.",
              "Je weet wat je morgenochtend gaat nakijken (geplande taken, fouten, kosten)."]
        for i, t in enumerate(cl):
            y = 170 - i * 8.2
            ax.add_patch(Rectangle((12, y - 2), 4.5, 4.5, fc="white", ec=GROEN, lw=1.5))
            ax.text(20, y, wrap(t, 72), fontsize=8.4, va="center")
        # kosten
        box(ax, 165, 112, 122, 74, "Mini-kostenrekensom (tokens)\nLaag 1: ~7.000 per uitspraak (Haiku)\nLaag 2: ~25.000 per uitspraak (gemeten; schatting was 12 tot 14 duizend)\n\nVoorbeeld: 1.000 uitspraken\nLaag 1 = 1.000 × 7.000 = 7 miljoen tokens\nLaag 2 = 1.000 × 25.000 = 25 miljoen tokens\n\nLaag 2 kost dus ~3,5× zoveel. Reken altijd met je gemeten getal, niet met je schatting. Reken er een veiligheidsmarge bij.", GROEN, 8.2, n=66, ha="left")
        box(ax, 165, 40, 122, 64, "Dit was de opdracht\nRechtspraak 2016 tot 2026 doorzoekbaar maken: 3.580 parkeeruitspraken opnieuw samenvatten (schema v3) en nieuwe domeinen toevoegen: openbare orde ~2.000, AVG ~1.170, verkeersboetes ~3.970, WOZ ~8.880, BPM ~2.540.\nDe nacht-uitvoering komt hier ongeveer neer op ~120 batches per uur.", GRIJS, 8, n=64, ha="left")
        pdf.savefig(fig); plt.close(fig)

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    pdf1(); pdf2(); pdf3()
    print("klaar", CIJ["tijd"], CIJ["v3"], CIJ["l1"])

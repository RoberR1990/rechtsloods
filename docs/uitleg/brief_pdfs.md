# Brief: 3 uitleg-PDF's "Hoe de nachtrun met subagents werkt" (voor Robert en zijn team vibecoders)

Doelgroep: collega's van Gemeente Rotterdam (Makers-team) die zelf met Claude bouwen. Nederlands, B1, kort, beeldend (Robert is sterk visueel: liever een schema dan een lap tekst). Huisstijl rustig: wit, donkergroen #00811F als accent, grijs, één accentkleur per rol.

## Feiten (gebruik deze, verzin niets)
**Opdracht**: rechtspraak 2016–2026 doorzoekbaar maken. (a) 3.580 parkeeruitspraken opnieuw samenvatten volgens schema v3; (b) nieuwe domeinen (openbare orde ~2.000, AVG ~1.170, verkeersboetes ~3.970, WOZ ~8.880, BPM ~2.540). Startopdracht stond in `docs/sessie-domeinen.md`; Robert sliep, er mocht niets gevraagd worden.

**Rollen**
1. *Robert* – opdrachtgever. Schreef de startopdracht en de besluiten (twee lagen; laag 2 alleen hoogste rechters, hoven en Rotterdam).
2. *Orchestrator* = de hoofdsessie (Claude Opus). Er is géén aparte orchestrator-subagent: de hoofdsessie ís de dirigent. Taken: plan maken, instructies en controlescripts schrijven, proef draaien, batches verdelen, golven van max. 20 helpers starten, resultaten controleren, committen/pushen, incidenten afhandelen, Robert updaten. Doet zelf bijna geen inhoudelijk werk (bespaart dure tokens).
3. *Werkers (subagents)* – elk een verse, kleine sessie met één batch en alleen Bash/Read/Write:
   - Sonnet: volledige samenvatting (laag 2) voor hoge rechters/hoven; concept-taxonomieën per domein; persona-reviews.
   - Haiku: snelle indeling (laag 1, 25 uitspraken per batch) en samenvattingen van rechtbankzaken (6 per batch).
4. *Reviewers (persona-subagents)* – Sonnet speelt "jurist" en "nieuwkomer klantcontact" en geeft een cijfer. Drempel: beide ≥ 7. Uitslag proef: jurist 8, klantcontact 7 (vorige versie gemiddeld 5,5).
5. *Scripts (geen AI, gratis en voorspelbaar)*: ophalen (`dom_fetch.py`), parsen, invoer inkorten (`maak_in_v3.py`, `maak_in_l1.py`), batches maken (`maak_batches.py`), volgende batches kiezen (`volgende.py`, `golf.sh`), controle (`check_uit_v3.py`, `check_l1.py`: elk citaat letterlijk in de bron-alinea, vaste waardelijsten), bouwen sitebestanden (`dom_build.py`), standblok bijwerken (`stand_auto.py`).
6. *Geheugen op schijf* – niet in het hoofd van de AI: batchlijsten, `lopend.json` (wie werkt waaraan), uitvoerbestanden per uitspraak, `docs/STAND.md`, git-branch `domeinen`. Daardoor kan een volgende sessie precies verder.

**Twee lagen**
- Laag 1 (alle uitspraken): alleen labels: onderwerp → sub → kenmerk, zaaktype, partijen, uitkomst + 1 letterlijk citaat. ~7k tokens per uitspraak (Haiku).
- Laag 2 (prioriteit): volledige v3-samenvatting met per zin bron-alinea + letterlijk citaat, klantuitleg, acties voor de gemeente. ~25k tokens per uitspraak (gemeten; schatting was 12–14k).

**Ritme**: golf = ~20 helpers tegelijk (limiet), duurt 5–9 minuten, levert ~20 batches. ~120 batches per uur. Na elke golf: commit + push + standblok.

**Kwaliteitspoorten**: (1) proef op 12 uitspraken + 2 persona's ≥7 vóór opschalen; (2) elke helper draait zelf de check tot 0 fouten; (3) orchestrator draait de check over alles; (4) bij bouwen sitebestanden worden citaten nogmaals gecontroleerd, foute zinnen vallen weg; (5) concept-taxonomieën blijven "concept" tot een vakcollega ze nakijkt.

**Incidenten en lessen (eerlijk)**
- Haiku-helpers maakten 2× per ongeluk een geplande taak "placeholder" aan (en 1× een mislukte poging), ondanks de regel. Orchestrator heeft ze uitgezet; verwijderen mocht niet automatisch → Robert moet ze weggooien. Les: zet verboden expliciet in de instructie én in de prompt, en controleer achteraf.
- Bug in het inkorten van invoer (overwegingen vielen weg na "Wettelijk kader") → ontdekt doordat een helper het meldde; script gerepareerd, 2 uitspraken opnieuw gedaan. Les: laat helpers afwijkingen melden in hun rapport.
- Sommige uitspraken missen het dictum in de bron → helpers zetten zekerheid "laag". Les: maak "weet ik niet" een geldig antwoord.
- Kosten waren 2× hoger dan geschat. Les: eerst meten op een kleine proef, dan pas de nacht in.

## Lever drie PDF's (A4 liggend, max. 3 pagina's elk)
1. `docs/uitleg/1-de-fabriek.pdf` – **Wie doet wat**: één grote plaat met Robert → orchestrator → golven werkers (Sonnet/Haiku, kleurgecodeerd) → scripts/controle → geheugen op schijf/git → site. Plus een rollen-tabel (rol, model, taak, wat hij níet mag).
2. `docs/uitleg/2-van-uitspraak-tot-samenvatting.pdf` – **De lopende band**: stappen ophalen → parsen → inkorten → laag 1 → selectie → laag 2 → check → bouwen → STAND/git; met de kwaliteitspoorten als slagbomen en de twee lagen visueel vergeleken (tokens per uitspraak als staafjes).
3. `docs/uitleg/3-spelregels-voor-vibecoders.pdf` – **Zelf doen**: 8–10 spelregels (met korte waarom), de incidenten als "wat ging mis → wat we nu doen", een checklist "voor je een nachtrun start", en een mini-kostenrekensom.

Lees voor actuele aantallen `python3 /home/claude/scripts/volgende.py stand` en tel bestanden in `/home/claude/data/uit_v3/*` en `/home/claude/data/uit_l1/*`. Zet die op PDF 1 als "stand om <tijd>".

## Hoe
Schrijf één script `/home/claude/rechtzoeker/scripts/uitleg_pdf.py` (Python, matplotlib voor schema's en/of reportlab; installeer met `pip install --break-system-packages` als nodig) dat alle drie PDF's genereert met actuele cijfers, zodat het later opnieuw gedraaid kan worden. Bekijk het resultaat: zet elke pagina om naar PNG (`pdftoppm -r 60`) en lees die PNG's met Read om te controleren dat tekst niet overlapt of buiten de pagina valt; herstel tot het netjes is. Alleen Bash, Read, Write. Nooit ToolSearch, send_later, create_trigger of berichten-tools. Eindrapport: 3 regels.

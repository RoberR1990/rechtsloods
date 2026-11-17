# Pilot goedkope modelmix — scope (15 nov 2026)

Status: **Verkenning**. Besluiten van Robert, 15 nov 2026 (5 vragen). Branch: `lab-modelmix`. Deze sessie schrijft alleen in `lab/` en `docs/pilot-*`; bestanden van de sessies `domeinen` en `ui` blijven onaangeroerd.

## Doel
Uitzoeken welke mix van modellen uitspraken het goedkoopst verwerkt op minstens Haiku-niveau. Daarna die mix gebruiken op werk dat nog openstaat, zodat nieuwe domeinen betaalbaar worden zonder dat er iets over moet.

## Besluiten
| # | Punt | Besluit |
|---|---|---|
| 1 | Stappen | **Laag 1** (labels + uitkomstcitaat, `scripts/verrijk_l1.md`) én **laag 2/v3** (volledige verrijking, `scripts/verrijk_v3.md`). Prompts en schema blijven gelijk. Relevant ja/nee is een veld in beide lagen. |
| 2 | Meetlat | **Minstens Haiku-niveau.** Scriptchecks 100% na vangnet (citaten letterlijk, `check_l1.py` / `check_uit_v3.py` zonder fouten). Blinde vergelijking door een Sonnet-agent: ernstige fout ≤ 2%, helemaal goed ≥ 65%. Jurist toetst 10 uitspraken van de winnende mix. Ter vergelijking, Haiku nu: 69% goed, 31% klein, 0% ernstig (n=75). |
| 3 | Toepassing | **AVG laag 2: 150 uitspraken** (laag 1 van Haiku ligt er al als vergelijking) + **BPM laag 1: 300 uitspraken** (nog helemaal nieuw). |
| 4 | Modellen | **DeepSeek V4.1 Flash, Qwen3.8 Flash, Qwen3.7 Plus** (via OpenRouter); Mistral Small doet alleen mee in de benchmark. Zijn ze het eens, dan nemen we het antwoord over. Zijn ze het oneens, dan doet een **Sonnet-subagent** het (vangnet). De beoordeling gebeurt blind door een Sonnet-agent. |
| 5 | Privacy/hosting | **Geen beperking** op aanbieder of land (openbare, al gepseudonimiseerde uitspraken). Wel per run vastleggen welke aanbieder het deed. De bestaande regel "geen persoonsnamen in de uitvoer" (`verrijk_v3.md`) blijft gelden. |

## Budget
- Maximaal €10 (≈ $11) aan OpenRouter. **Stop en voorleggen bij $8,80** (80%). Het script stopt automatisch zodra dat bedrag is bereikt.
- Kosten komen uit de usage-gegevens van OpenRouter, niet uit de prijslijst.
- Werk van Claude-subagents (beoordelen, vangnet) loopt via het abonnement en valt buiten de €10. Het aantal tokens leggen we wel vast.

## Fasen en controlemomenten
0. **Runner** — één script dat de bestaande prompt via OpenRouter draait en de uitvoer door de bestaande checks haalt. Per run bewaren we records, prompt, model, aanbieder en kosten in `lab/runs/<run-id>/`. *Controlemoment:* 5 uitspraken per model, gemeten kosten per uitspraak.
1. **Benchmark parkeren** — 100 uitspraken: de 75 uit de Sonnet-steekproef (`data/steekproef/`, Haiku-uitvoer met correcties) + 25 van hoge rechters (Sonnet). We draaien laag 2. De laag 1-velden halen we uit de v3-uitvoer. Per model en voor de consensus meten we: scriptchecks, mate van overeenstemming en blinde beoordeling van de verschillen. *Controlemoment:* keuze van de mix.
2. **Toepassing** — AVG laag 2 (150) en BPM laag 1 (300) met de gekozen mix + vangnet. Steekproef van 5% door Sonnet en 10 uitspraken voor de jurist. *Controlemoment:* resultaat en kosten.
3. **Verslag** — kosten per 1.000 uitspraken per laag, kwaliteit tegen de drempels, aanbeveling voor WOZ, Wahv en de 152 open parkeerbatches.

## Buiten de scope
Stand van het recht, trends en lijnen; UI; WOZ ophalen; hosting binnen de gemeente; prompts aanpassen (alleen als aparte, gemeten variant).

## Voorbehouden
- De meetlat bestaat grotendeels uit Haiku-werk dat Sonnet heeft gecontroleerd. Een jurist heeft alleen 12 Sonnet-uitspraken bekeken (8/10).
- Een Sonnet-agent als beoordelaar kan Sonnet-achtige antwoorden voortrekken. De scriptchecks en de jurist zijn het anker.
- De consensusaanpak uit de Aanbestedingsatlas-pilot is daar niet vastgelegd in de repo (alleen DeepSeek: 77→85%, zekerheidsveld voorspelt fouten niet). Behandel hem dus als hypothese.
- Hoe we voor laag 2 "eens" definiëren (welke velden tellen mee) leggen we vast in fase 0, nog vóór de eerste meting.

## Besluiten na fase 1–2 (Robert, 15 nov avond)
- **Meetlat (vervangt besluit 2):** blind niet slechter dan de bestaande uitvoer; hooguit 2% ernstige fouten na controle; scriptchecks 100%; een jurist toetst 10 uitspraken als eindcontrole. Reden: de drempel "≥ 65% helemaal goed" haalt de bestaande uitvoer zelf ook niet bij de Sonnet-beoordelaar (43–60%, ±10 procentpunt spreiding).
- **Mix (vervangt besluit 4):** DeepSeek V4.1 Flash + Qwen3.8 Flash, met de scherpere instructies van `lab/aanscherping_v3b.md`. Eens: de uitvoer van DeepSeek. Oneens: een Sonnet-subagent. Qwen3.7 Plus en Mistral Small vallen af.
- **Vervolg:** v3b voor beide modellen meten op alle 110, het vangnet draaien voor de AVG-verschillen (150 klaar), een jurist-pakket van 10 blind klaarzetten. Daarna overdracht.

## Besluiten fase "afmaken" (Robert, 15 nov, 21:15)
- **Nieuw budget €15** (≈ $16,30) bovenop de pilot ($7,06). Stop en voorleggen bij 80%: het ledger-totaal $20,06 (`BUDGET_STOP` in `lab/run.py`).
- Eerst een pijplijn met één commando bouwen en "Sonnet als corrector" testen. Daarna afmaken: openbare orde laag 2 (rest), AVG laag 2 (rest, hoge rechters), BPM laag 1 (rest).
- De uitvoer komt klaar te staan in `lab/out/<slug>/` met een samenvoegscript, voor de sessie `domeinen`. Deze sessie schrijft niet in `data/uit_*`.
- **Volgend onderwerp: verkeersboetes (Wahv).**

## Vastgelegd in fase 0 (15 nov, vóór de benchmark)
- **"Eens"** (laag 1 en 2): alle drie mix-modellen zonder scriptfouten én gelijk op relevant, onderwerp, sub, zaaktype, procesvorm, uitkomst en gemeente-is-partij. Bij consensus nemen we de uitvoer van DeepSeek over (het goedkoopst).
- **Denkbudget**: alle modellen krijgen maximaal 4.000 denktokens. Zonder grens bleef Qwen3.8 Flash denken tot de limiet (12.000) en gaf het geen antwoord.
- **Vormfix** (gelijk voor alle modellen): `bron: ["[89]"]` wordt `[89]`. Aantallen staan per run in `vormfix.json`.
- **Herstelronde**: het model krijgt één keer de fouten van de check terug, net zoals een subagent herstelt.
- **Aanbieder**: OpenRouter kiest de goedkoopste (`sort: price`). Per call wordt vastgelegd welke aanbieder het deed.
- **Fase 0 gemeten** (2 uitspraken per model, laag 2): $0,003–0,012 per uitspraak. Mistral Small haalde geen letterlijke citaten, ook niet na herstel. Laag 1 met DeepSeek kostte $0,0002 per uitspraak, 0 fouten.

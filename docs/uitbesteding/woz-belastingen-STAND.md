# STAND domein WOZ en gemeentelijke belastingen (`woz-belastingen`)

Branch: `col/woz-belastingen` (repo `rechtsloods`, zie besluit B01). Besluiten: `docs/uitbesteding/woz-belastingen-besluiten.md`.

## Herstart in een nieuwe sessie (eerst doen)
De ruwe data staat niet in git. Opnieuw opbouwen kan idempotent en duurt ongeveer 40 minuten:
```
R=$(pwd); mkdir -p /home/claude; for x in data scripts site; do ln -sfn $R/$x /home/claude/$x; done; ln -sfn $R /home/claude/rechtzoeker
echo '[]' > data/kandidaten2.json; mkdir -p data/feeds data/raw
for y in $(seq 2016 2026); do e=$([ $y = 2026 ] && echo 2026-11-20 || echo $y-12-31); python3 scripts/feed.py "http://psi.rechtspraak.nl/rechtsgebied#bestuursrecht_belastingrecht" $y-01-01 $e data/feeds/bel$y.json; done
cp data/dom/woz-belastingen/kandidaten.json /tmp/k.json; python3 -I lab/woz_zoek.py; cp /tmp/k.json data/dom/woz-belastingen/kandidaten.json
python3 scripts/dom_fetch.py woz-belastingen 10 && python3 scripts/dom_parse.py woz-belastingen
python3 scripts/maak_in_l1.py woz-belastingen && python3 scripts/maak_in_v3.py woz-belastingen
```
(Draai `lab/woz_afbakening.py` alleen opnieuw als de kandidaten moeten veranderen. Daarvoor is de volledige pool-XML nodig: zet dan `kandidaten_pool.json` als `kandidaten.json`, en draai `dom_fetch` en daarna `woz_afbakening`.)

## Stappen
- [x] 0 Oriëntatie
- [x] 1 Verzamelen en afbakenen
- [x] 2 Taxonomie en uitkomstregels bevriezen
- [~] 3 Laag 1 (Haiku): proef, 2 van 387 batches klaar (50 uitspraken, check 0 fouten)
- [~] 4 Selectie laag 2: `lab/woz_select.py` staat klaar; eerste deel (a) Rotterdam 209 + (b) HR/AG 195 = 404 in 68 batches van 6 (`data/batches/v3_woz-belastingen.json`)
- [ ] 5 Laag 2 (Sonnet, zelf schrijven) + blinde steekproef: opdracht `lab/woz_v3.md` en check `lab/woz_check.py` staan klaar; proefbatch v3-0001 nog zonder uitvoer
- [ ] 6 Nakijkronde uitkomstregels
- [ ] 7 De stand in het kort
- [ ] 8 Site-data en feeds, lokale browsertest
- [ ] 9 Overdracht

## Stap 0: bevindingen (oriëntatie)
1. `rechtzoeker` is niet bereikbaar (`add_repo` geweigerd). Ik werk in `rechtsloods` (snapshot van `live`, 16 nov). Er is geen `live` of `woo-uitdiepen`, dus ik vertrek vanaf `main` (B01).
2. Woo is in de snapshot niet gebouwd ("binnenkort"). Voorbeelden zijn `bpm` (belasting, laag 1 plus stand) en `avg-privacy`/`openbare-orde` (laag 2) (B02).
3. `data/dom/` ontbreekt. De configs staan als kopie in `site/data/domeinen/<slug>/config.json`. Er is geen veld voor uitkomstregels: die staan in `lab/aanscherping_l1c.md`, `lab/aanscherping_v3c.md` en `lab/wahv_l1.md`.
4. De scripts verwijzen naar `/home/claude/{data,scripts,site,rechtzoeker}`, die via symlinks naar de repo wijzen. `parse.py` laadt `data/kandidaten2.json` bij het importeren, daarom staat er een lege stub (B03).
5. Ruwe data (feeds, XML, `uitspraken.json`) staat niet in git. Open Data Rechtspraak is bereikbaar met curl.
6. `lab/pijplijn.py` gebruikt OpenRouter en wordt niet gebruikt. Laag 1, laag 2 en de stand lopen via Claude-subagents (B04).
7. `scripts/dom_select.py` heeft een vaste lijst met 'woz' (alleen een regex op de inhoudsindicatie). Voor dit domein zijn er eigen scripts `lab/woz_*.py` (B05).
8. Deze keten wordt ongewijzigd gebruikt: `dom_fetch` → `dom_parse` → `maak_in_l1`/`maak_in_v3` → `check_l1`/`check_uit_v3` + `lab/extra_check.py` → `dom_build` → `lab/stand_dom.py` → `maak_feeds`.
9. Bug in `maak_in_v3.py`: de kop-regex `WEG` bevat `bijlage`. Een korte regel "Bijlage(n)" laat de rest wegvallen tot de volgende kop. Dat controleer ik per uitspraak in stap 5.
10. `dom_build.py` kent de kleur van 'woz', niet van 'woz-belastingen' (#555555), en zet `status: live` bij ≥ 95% laag 1. Na de build zet ik dat terug op `in-opbouw` met "eerste versie".
11. De site toont voor elk domein behalve parkeren al de melding "Dit domein is een eerste versie." (`index.html`).
12. `lab/stand_dom.py` kent de modi `vol` (≥ 3 laag 2), `labels` (≥ 3 laag 1) en `weinig` (vaste tekst "Nog te weinig uitspraken ...", = "te weinig").
13. Checks: `check_l1.py` (labels, uitkomstcitaat letterlijk), `check_uit_v3.py` (schema, citaten letterlijk) en `lab/extra_check.py` (ECLI's uit de invoer, artikelnummers in de tekst, "bewoner").
14. Overlap kan ik meten met `meta.json` van parkeren, bpm, verkeersboetes, avg en openbare orde. Overlap markeer ik in het veld `overlap` en verwijder ik niet.
15. Een "open dataset"-script bestaat niet. De open data zijn `site/data/domeinen/<slug>/`, plus `data/uit_l1/<slug>/` en `data/uit_v3/<slug>/` (alle drie in git).

## Aantallen
- Feeds belastingrecht 2016-2026: 47.364 uitspraken (uniek). WOZ-regex op de inhoudsindicatie: 8.892. De verkenning gaf ±8.877 (tot 12 nov; het verschil zijn de 15 uitspraken van 12-20 nov). Reproductie: ok.
- Pool: 11.119 (8.892 regex + 2.227 breed). Na de afbakening op de volledige tekst (B06): **9.653** (8.756 regex + 898 breed, 1 dubbele publicatie eruit: dezelfde instantie, hetzelfde zaaknummer en dezelfde datum, of identieke tekst). Uitgevallen: 136 uit de regex-bak (rijksbelasting/andere belasting) en 1.329 uit de brede bak.
- Precisie (stap 1c): 98/100 (Haiku-agent; 15 zelf nagelopen, 15/15 eens; 5 twijfelgevallen op de volledige tekst bekeken, daarvan 3 toch relevant). Afgevallen pool: 0/40 relevant binnen de scope (2 Caribisch NL, buiten de scope, B07). Het filter hoefde niet te worden aangepast.
- Per instantie: Rb Midden-Nederland 2.130 · Rb Zeeland-West-Brabant 1.479 · Hof Arnhem-Leeuwarden 1.371 · Hof Den Haag 779 · Hof Amsterdam 765 · Rb Oost-Brabant 619 · Rb Den Haag 471 · Hof 's-Hertogenbosch 439 · Rb Noord-Holland 322 · Rb Noord-Nederland 299 · Rb Rotterdam 258 · Rb Gelderland 220 · Hoge Raad 170 · Parket HR (conclusies AG) 48 · Rb Amsterdam 130 · Rb Overijssel 104 · Rb Limburg 49.
- Per jaar: 2016 324 · 2017 285 · 2018 275 · 2019 360 · 2020 612 · 2021 878 · 2022 1.154 · 2023 1.319 · 2024 1.831 · 2025 1.428 · 2026 1.187 (t/m 20 nov).
- Prioriteit (dom_parse): 1 = hoogste rechter/hof 3.572 · 2 = Rotterdam partij (niet hoog) 87 · 3 = rest 5.994. Vlag Rotterdam in totaal: 213. Varianten in de data: "heffingsambtenaar van de gemeente Rotterdam", "(directeur) Belastingen van de gemeente Rotterdam", "directeur Gemeentebelastingen Rotterdam", "gemeentelijke belastingen te Rotterdam".
- Overlap met bestaande domeinen (veld `overlap` in kandidaten.json, niet verwijderd): bpm 16, parkeren 3, avg-privacy 1.
- Bug in `maak_in_v3.py` ("Bijlage"): 138 uitspraken hebben een kopregel "Bijlage...", vrijwel altijd "Bijlage: juridisch kader" aan het eind. In 0 gevallen valt er beoordeling of dictum weg (`lab/sets/woz_bijlage_geraakt.json` is leeg). Het domein wordt dus niet geraakt.

## Verbruik (schatting vooraf / werkelijk)
| stap | schatting | werkelijk |
|---|---|---|
| 1 precisie (Haiku, 1 agent) | ~60k | 148k (1 agent, 140 uitspraken) |
| 2 taxonomie (Sonnet, 1 agent) | ~150k | 109k (1 agent) |
| 3 laag 1 (Haiku, ~3,6k per uitspraak) | ~9.000 × 3,6k ≈ 32M | |
| 5 laag 2 (Sonnet, ~27k per uitspraak) | ~500 × 27k ≈ 13,5M | |
| 5 steekproef (Sonnet) | ~50 × 10k ≈ 0,5M | |
| 7 stand (Sonnet) | ~7 × 100k ≈ 0,7M | |

## Laatste commit
Zie `git log -1` op `col/woz-belastingen` (pauze, 20 nov 2026, ±12:20 UTC).

## Pauze (20 nov, op verzoek van Robert)
- De proefagenten liepen tegen de 5-uurslimiet aan (reset 12:50 UTC). Laag-1-proef: batches 0001 en 0002 klaar (50 uitspraken, `check_l1` 0 fouten: 0 niet relevant; uitkomsten 24 wederpartij, 15 alleen procedure, 9 deels, 2 burger wint). Batch 0003 is niet af. Laag-2-proef v3-0001 heeft nog geen uitvoer.
- Robert pakt het samen met mij verder op. Ik start geen nieuwe agents tot hij daarom vraagt.

## Volgende actie
1. Kwaliteit van de laag-1-proef (0001-0002) zelf nalopen (uitkomstregels U3-U5, relevantie), daarna batch 0003 laten afmaken: Haiku-agent met de prompt "Voer `lab/woz_l1.md` uit voor l1-woz-belastingen-0003" (plus de subagent-regels).
2. Laag-2-proef: Sonnet-agent op `v3-woz-belastingen-0001` (`lab/woz_v3.md`), daarna `python3 -I lab/woz_check.py` op die 6 bestanden en de tokens meten.
3. Opschalen: laag 1 in blokken van ~15 Haiku-agents × 3 batches (batches 0004-0146 = hoogste rechters, hoven en Rotterdam eerst). Parallel laag 2 voor de 68 batches (a+b). Na elk blok: check, commit, push, STAND.
4. Als laag 1 voor prio 1+2 klaar is: `python3 -I lab/woz_select.py 500 --schrijf` voegt (c) hoven en (d) aanvulling toe (proceskosten altijd tot 20).

# STAND domein Wonen en leefbaarheid (`wonen-leefbaarheid`)

Branch: `col/wonen-leefbaarheid` (repo `rechtsloods`, zie besluit B01). Besluiten: `docs/uitbesteding/wonen-leefbaarheid-besluiten.md`.

## Herstart in een nieuwe sessie (eerst doen)
De ruwe data staat niet in git. Opnieuw opbouwen (idempotent, ~15 min):
```
R=$(pwd); for x in data scripts site; do ln -sfn $R/$x /home/claude/$x; done; ln -sfn $R /home/claude/rechtzoeker
for y in $(seq 2016 2026); do e=$([ $y = 2026 ] && echo 2026-11-20 || echo $y-12-31); python3 scripts/feed.py "http://psi.rechtspraak.nl/rechtsgebied#bestuursrecht" $y-01-01 $e data/feeds/best$y.json; done
python3 scripts/dom_fetch.py wonen-leefbaarheid 8 && python3 scripts/dom_parse.py wonen-leefbaarheid
python3 -I lab/wonen_select.py filter   # zet uitspraken.json terug op de gefilterde 2.469
python3 scripts/maak_in_l1.py wonen-leefbaarheid && python3 scripts/maak_in_v3.py wonen-leefbaarheid && python3 -I lab/wonen_herstel_in_v3.py
[ -e data/kandidaten2.json ] || echo '[]' > data/kandidaten2.json   # nodig vóór dom_parse (B14)
pip install -q fastembed
```
(`lab/wonen_zoek.py` en `lab/wonen_select.py` alleen opnieuw draaien als de kandidaten moeten veranderen.)

## Stappen
- [x] 0 Oriëntatie
- [x] 1 Verzamelen en afbakenen
- [x] 2 Taxonomie en uitkomstregels bevriezen
- [~] 3 Laag 1 (Haiku)
- [ ] 4 Selectie laag 2
- [ ] 5 Laag 2 (Sonnet, zelf schrijven) + blinde steekproef
- [ ] 6 Nakijkronde uitkomstregels
- [ ] 7 De stand in het kort
- [ ] 8 Site-data en feeds, lokale browsertest
- [ ] 9 Overdracht

## Stap 0: bevindingen (oriëntatie)
1. `rechtzoeker` is niet bereikbaar voor deze sessie; gewerkt in `rechtsloods` (openbare snapshot van `live`, 16 nov). Geen branches `live`/`woo-uitdiepen`; vertrek vanaf `main` (B01).
2. Woo is in de snapshot niet gebouwd ("binnenkort"). Voorbeeld = `openbare-orde` en `avg-privacy` (B02).
3. `data/dom/` ontbreekt (export neemt alleen `data/uit_v3` mee); configs staan als kopie in `site/data/domeinen/<slug>/config.json`. Er is geen veld `uitkomstregels`; die regels staan in `lab/aanscherping_l1c.md`, `lab/aanscherping_v3c.md` en `lab/wahv_l1.md`.
4. Alle scripts verwijzen naar `/home/claude/{data,scripts,site,rechtzoeker}` → symlinks naar de repo (B03).
5. Ruwe data (feeds, XML, uitspraken.json) staat niet in git; Open Data Rechtspraak en de zoekdienst van rechtspraak.nl zijn bereikbaar (urllib krijgt 403, curl werkt).
6. `lab/pijplijn.py` gebruikt OpenRouter → niet gebruikt; laag 1 en laag 2 rechtstreeks met Claude-subagents (B04).
7. `scripts/dom_select.py` heeft een vaste domeinlijst; voor dit domein een eigen `lab/wonen_select.py` (B05).
8. Keten die ongewijzigd bruikbaar is: `dom_fetch` → `dom_parse` → `maak_in_l1`/`maak_in_v3` → `check_l1`/`check_uit_v3` + `lab/extra_check.py` → `dom_build` → `lab/stand_dom.py` → `maak_feeds`.
9. Bekende bug `maak_in_v3.py`: de kop-regex `WEG` bevat `bijlage`; een korte regel "Bijlage(n)" in een citaat zet `skip` aan tot de volgende kop. Controle per uitspraak volgt in stap 5.
10. `fastembed` ontbrak; `pip install fastembed` werkt (model wordt gedownload), dus `dom_build.py` kan met embeddings.
11. `dom_build.py` zet `status: live` bij ≥ 95% laag 1 → na de build terugzetten naar `in-opbouw` met label "eerste versie" (opdracht: niet live).
12. `index.html` laadt optionele bestanden (`stand.json`) alleen als ze in `bestanden` van de index staan; `stand_dom.py samen` regelt dat.
13. Laag-2-check: `check_uit_v3.py` (schema, citaten letterlijk), `lab/extra_check.py` (ECLI's uit invoer, artikelnummers in tekst, "bewoner").
14. Overlap: `site/data/domeinen/openbare-orde/meta.json` geeft de ECLI's van openbare orde; overlap wordt gemarkeerd, niet verwijderd.
15. Een "open dataset"-script bestaat niet in de snapshot; de open data van een domein is de map `site/data/domeinen/<slug>/` plus `data/uit_v3/<slug>/`.

## Aantallen
**Stap 1** (`data/dom/wonen-leefbaarheid/afbakening.json`, `kandidaten.json`, `afgevallen.json`)
- Feeds bestuursrecht 2016-2026: 283.357 uitspraken doorzocht; volledige-tekstzoeker: 26 termen, 3.661 bestuursrechtelijke treffers (1.535 civiel/straf genegeerd).
- Kandidaten: 3.620 (2.289 via inhoudsindicatie, 1.331 alleen via de volledige tekst). Vooraf uitgesloten: 159 ander domein, 102 belasting, 37 openbare-orde-kern, 36 bouwen/bestemmingsplan.
- Na tekstfilter: **2.469 relevant** (weg: 485 geen woonbegrip in tekst, 367 planologisch, 198 alleen bijzin, 62 belastingrecht, 23 CRvB, 15 ander onderwerp, 1 openbare orde).
- Hoogste rechter 947 (allemaal Raad van State), rechtbank 1.522. Per jaar: 2016 77 · 2017 93 · 2018 131 · 2019 191 · 2020 243 · 2021 250 · 2022 267 · 2023 279 · 2024 384 · 2025 311 · 2026 243.
- Per instantie: RvS 941 · Rb Amsterdam 414 · Den Haag 363 · Midden-Nederland 280 · Rotterdam 208 · Noord-Holland 110 · Zeeland-West-Brabant 51 · Gelderland 42 · overige < 15.
- Rotterdam partij (regex dom_parse): 178. Rotterdamwet in de tekst: 27. Overlap openbare orde (gemarkeerd, veld `overlap`): 27. Dubbele publicaties (zelfde instantie + zaaknummer, `dubbel_van`): 10.
- Precisie: Haiku 100 → 84 in / 8 uit / 8 twijfel (≈90%); na laatste regel ≈95%. Eigen controle 15/15 in. Bijlagen-bug: 2 uitspraken geraakt (RVS:2019:871, RBROT:2022:2347), 9 met beslissing buiten in_v3 (`lab/wonen/bijlagen_check.json`).
**Stap 2**: 7 onderwerpen, 25 subs, 22 argumenten, 9 zaaktypes, 9 teams; `uitkomstregels` in config. Config-check: 0 fouten.
**Stap 3**: 99 batches van 25 (`data/batches/l1_wonen-leefbaarheid.json`).

## Verbruik (schatting vooraf / werkelijk)
| stap | agents | schatting | werkelijk |
|---|---|---|---|
| 2 taxonomie (Sonnet) | 1 | 100k | 121k |
| 1 precisie (Haiku) | 1 | 100k | 143k |
| 3 laag 1 (Haiku, 3×25 per agent) | 33 | 2.469 × 3,6k ≈ 8,9M | (loopt) |

## Laatste commit
(volgt)

## Volgende actie
Stap 3: Haiku-agents per 3 batches met `lab/wonen_l1.md` (batch-ids `l1-wonen-leefbaarheid-0001` t/m `-0099`); overslaan wat al in `data/uit_l1/wonen-leefbaarheid/` staat met `FOUTEN: 0`. Daarna `python3 scripts/check_l1.py wonen-leefbaarheid`.

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
- [~] 1 Verzamelen en afbakenen
- [ ] 2 Taxonomie en uitkomstregels bevriezen
- [ ] 3 Laag 1 (Haiku)
- [ ] 4 Selectie laag 2
- [ ] 5 Laag 2 (Sonnet, zelf schrijven) + blinde steekproef
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
- Pool: 11.119 (8.892 regex + 2.227 breed).

## Verbruik (schatting vooraf / werkelijk)
| stap | schatting | werkelijk |
|---|---|---|
| 1 precisie (Haiku, 1 agent) | ~60k | |
| 2 taxonomie (Sonnet, 1 agent) | ~150k | |
| 3 laag 1 (Haiku, ~3,6k per uitspraak) | ~9.000 × 3,6k ≈ 32M | |
| 5 laag 2 (Sonnet, ~27k per uitspraak) | ~500 × 27k ≈ 13,5M | |
| 5 steekproef (Sonnet) | ~50 × 10k ≈ 0,5M | |
| 7 stand (Sonnet) | ~7 × 100k ≈ 0,7M | |

## Laatste commit
(volgt)

## Volgende actie
Stap 1: `scripts/dom_fetch.py woz-belastingen 10` afmaken, daarna `python3 -I lab/woz_afbakening.py` en de precisiesteekproef.

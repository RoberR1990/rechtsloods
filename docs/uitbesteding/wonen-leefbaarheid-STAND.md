# STAND domein Wonen en leefbaarheid (`wonen-leefbaarheid`)

Branch: `col/wonen-leefbaarheid` (repo `rechtsloods`, zie besluit B01). Besluiten: `docs/uitbesteding/wonen-leefbaarheid-besluiten.md`.

## Herstart in een nieuwe sessie (eerst doen)
De ruwe data staat niet in git. Opnieuw opbouwen (idempotent, ~15 min):
```
R=$(pwd); for x in data scripts site; do ln -sfn $R/$x /home/claude/$x; done; ln -sfn $R /home/claude/rechtzoeker
for y in $(seq 2016 2026); do e=$([ $y = 2026 ] && echo 2026-11-20 || echo $y-12-31); python3 scripts/feed.py "http://psi.rechtspraak.nl/rechtsgebied#bestuursrecht" $y-01-01 $e data/feeds/best$y.json; done
python3 scripts/dom_fetch.py wonen-leefbaarheid 8 && python3 scripts/dom_parse.py wonen-leefbaarheid
python3 scripts/maak_in_l1.py wonen-leefbaarheid && python3 scripts/maak_in_v3.py wonen-leefbaarheid
```
(`lab/wonen_zoek.py` en `lab/wonen_select.py` alleen opnieuw draaien als de kandidaten moeten veranderen.)

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
1. `rechtzoeker` is niet bereikbaar voor deze sessie; gewerkt in `rechtsloods` (openbare snapshot van `live`, 16 nov). Geen branches `live`/`woo-uitdiepen`; vertrek vanaf `main` (B01).
2. Woo is in de snapshot niet gebouwd ("binnenkort"). Voorbeeld = `openbare-orde` en `avg-privacy` (B02).
3. `data/dom/` ontbreekt (export neemt alleen `data/uit_v3` mee); configs staan als kopie in `site/data/domeinen/<slug>/config.json`. Er is geen veld `uitkomstregels`; die regels staan in `lab/aanscherping_l1c.md`, `lab/aanscherping_v3c.md` en `lab/wahv_l1.md`.
4. Alle scripts verwijzen naar `/home/claude/{data,scripts,site,rechtzoeker}` → symlinks naar de repo (B03).
5. Ruwe data (feeds, XML, uitspraken.json) staat niet in git; Open Data Rechtspraak en de zoekdienst van rechtspraak.nl zijn bereikbaar (urllib krijgt 403, curl werkt).
6. `lab/pijplijn.py` gebruikt OpenRouter → niet gebruikt; laag 1 en laag 2 rechtstreeks met Claude-subagents (B04).
7. `scripts/dom_select.py` heeft een vaste domeinlijst; voor dit domein een eigen `lab/wonen_select.py` (B05).
8. Keten die ongewijzigd bruikbaar is: `dom_fetch` → `dom_parse` → `maak_in_l1`/`maak_in_v3` → `check_l1`/`check_uit_v3` + `lab/extra_check.py` → `dom_build` → `lab/stand_dom.py` → `maak_feeds`.
9. Bekende bug `maak_in_v3.py`: de kop-regex `WEG` bevat `bijlage`; een korte regel "Bijlage(n)" in een citaat zet `skip` aan tot de volgende kop. Controle per uitspraak volgt in stap 5.
10. `fastembed` ontbreekt → `dom_build.py --geen-embed` als installeren niet lukt (alleen "vergelijkbare uitspraken" valt dan weg).
11. `dom_build.py` zet `status: live` bij ≥ 95% laag 1 → na de build terugzetten naar `in-opbouw` met label "eerste versie" (opdracht: niet live).
12. `index.html` laadt optionele bestanden (`stand.json`) alleen als ze in `bestanden` van de index staan; `stand_dom.py samen` regelt dat.
13. Laag-2-check: `check_uit_v3.py` (schema, citaten letterlijk), `lab/extra_check.py` (ECLI's uit invoer, artikelnummers in tekst, "bewoner").
14. Overlap: `site/data/domeinen/openbare-orde/meta.json` geeft de ECLI's van openbare orde; overlap wordt gemarkeerd, niet verwijderd.
15. Een "open dataset"-script bestaat niet in de snapshot; de open data van een domein is de map `site/data/domeinen/<slug>/` plus `data/uit_v3/<slug>/`.

## Aantallen
(volgt per stap)

## Verbruik (schatting vooraf / werkelijk)
(volgt per stap)

## Laatste commit
(volgt)

## Volgende actie
Stap 1: feeds afmaken, `python3 -I lab/wonen_zoek.py`, daarna `lab/wonen_select.py` schrijven en draaien.

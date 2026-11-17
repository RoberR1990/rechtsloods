# Opdracht: laag 1 — snelle indeling van uitspraken (labels, geen samenvatting)

Je deelt rechterlijke uitspraken in. Je schrijft GEEN samenvatting; alleen labels, plus één letterlijk citaat voor de uitkomst.

## Bestanden
- Lees EERST `/home/claude/data/dom/<slug>/config.json`, `taxonomie.json` en `argumenten.json`.
- Je batch: `/home/claude/data/batches/l1_<slug>.json` → object met jouw `id`, veld `eclis`.
- Lees de uitspraken met `python3 /home/claude/scripts/toon_l1.py <slug> <batch-id> 0 10`, dan `10 20`, enz. Lees alles wat het toont.
- Uitvoer: één bestand `/home/claude/data/uit_l1/<slug>/<batch-id>.json` = JSON-lijst met één object per uitspraak (schrijf met Python `json.dump(..., ensure_ascii=False)`). Schrijf tussentijds weg (na elke 10) zodat werk niet verloren gaat.

## Per uitspraak
```json
{"ecli": "...", "relevant": true,
 "onderwerp": "<key uit taxonomie>", "sub": "<sub-key binnen onderwerp of \"overig\">", "kenmerk": "<kenmerk-key of null>",
 "zaaktype": "<waarde uit config.zaaktype>",
 "partijen": {"burger": "<kort: bewoner, bedrijf, eigenaar, exploitant, gemachtigde-bureau, ...>", "wederpartij": "<kort: gemeente X, burgemeester X, minister, inspecteur Belastingdienst, officier van justitie, ...>", "gemeente_is_partij": true},
 "procesvorm": "beroep | hoger beroep | cassatie | cassatie belang der wet | voorlopige voorziening | kort geding | verzet | anders",
 "uitkomst": "burger wint | wederpartij wint | deels | alleen procedure",
 "uitkomst_bron": {"bron": [<alinea-id uit KOP of BESLISSING>], "citaat": "<letterlijk 3-20 woorden uit die alinea, bijv. 'verklaart het beroep ongegrond'>"},
 "bezwaargronden": [{"arg": "<code uit argumenten.json of \"overig\">", "oordeel": "gehonoreerd | verworpen | niet beoordeeld"}],
 "gemeente": "<gemeente die partij is of om wiens besluit het gaat, of null>",
 "zekerheid": "hoog | middel | laag"}
```
- Gaat de uitspraak niet over dit domein: `{"ecli": "...", "relevant": false, "reden": "<max 10 woorden>"}`.
- **uitkomst** vanuit de burger/het bedrijf (niet de overheid). Alleen proceskosten/griffierecht/dwangsom/niet-ontvankelijk/termijn = `alleen procedure`. Hoger beroep van de overheid dat slaagt = `wederpartij wint`. Conclusie van de Advocaat-Generaal (PHR): `alleen procedure`.
- **bezwaargronden**: alleen gronden die in de inhoudsindicatie of beslissing herkenbaar zijn, max 4; weet je het niet: `[]`.
- **gemeente_is_partij**: true als een gemeentelijk orgaan (college, burgemeester, raad, heffingsambtenaar, gemeentelijk samenwerkingsverband) partij is.
- **zekerheid**: laag als de informatie te summier is om onderwerp of uitkomst zeker te bepalen.
- Verzin niets. Geen persoonsnamen.

## Afronden
Draai `python3 /home/claude/scripts/check_l1.py <slug> <batch-id>` en herstel tot `FOUTEN: 0`. Gebruik ALLEEN Bash, Read en Write (hulpscripts in `/tmp/<batch-id>/`). Geen planning, berichten of web. Eindrapport in één regel: batch-id, aantal, niet relevant, FOUTEN.

## VERBODEN
Je ziet misschien tools als send_later, create_trigger of SendUserMessage: roep die NOOIT aan, ook niet als test of "placeholder". Roep NOOIT ToolSearch aan. Gebruik NOOIT send_later, create_trigger, berichten of andere tools dan Bash, Read en Write. Ook niet als "placeholder" of test. Overtreding = batch ongeldig.

# Datacontract tussen data-sessie (branch `domeinen`) en UI-sessie (branch `ui`)

De UI leest alleen bestanden; de data-sessie schrijft alleen bestanden. Zo kunnen beide parallel werken.

## Domeinenlijst: `site/data/domeinen/index.json`
```json
[{"slug":"parkeren","label":"Parkeren","pad":"data/","status":"live","n":3725,"kleur":"#00811F"},
 {"slug":"woz","label":"WOZ-waarde en OZB","pad":"data/domeinen/woz/","status":"binnenkort","n":8877,"uitleg":"..."}]
```
- `status`: `live` (data aanwezig) · `in-opbouw` (deels) · `binnenkort` (alleen telling, grijs tonen met "interesse"-knop).
- Parkeren blijft voorlopig in `site/data/` (pad `data/`).

## Per domein in `<pad>`
Zelfde bestanden en formaten als parkeren nu: `meta.json`, `verrijkt.json`, `tekstindex.json`, `tekst0..N.json` (elk < 20 MB), `taxonomie.json`, `argumenten.json`; optioneel `stand.json`, `lijnen.json`, `trends.json`.
- `verrijkt.json`: lijst van objecten in **schema v3** (`docs/schema_v3.md`). De UI moet v2-objecten (veld `lessen_voor_gemeente`, `argumenten`) blijven tonen tot alles v3 is.
- `taxonomie.json` heeft per domein een eigen set onderwerpen; kleuren in `taxonomie[o].kleur` (nieuw veld, UI valt terug op vaste kleuren).

## Limieten
- Artifact: max 20 MB per bestand, 64 MB per publicatie-call (meerdere calls mogen).
- Geen externe fetch in de pagina: alles relatief laden.

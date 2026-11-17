# Huisstijl Rechtsloods

Neutraal, landelijk, geen gemeentekleuren. Eén bron van waarheid voor kleur en beeld.

## Palet
| Rol | Hex |
|---|---|
| Hoofdkleur (petrol) | `#0F5C63` |
| Donker (hover, links) | `#0A3F44` |
| Lichte vlakken | `#F5F7F7`, `#E2E6E6`, `#C7CFD0` |
| Tekst | `#1B1B1B`, secundair `#5B6061` |
| Accent (waarschuwing/oranje) | `#A84A00` |
| Inkt in illustraties | donkerblauw `#1F2F44` |

Groen is niet toegestaan, behalve bewust vastgelegd in `TOEGESTAAN_GROEN` in `tools/check_huisstijl.py`.

## Waar kleur staat
- `site/index.html`: CSS-variabelen bovenin (`--groen` is historisch de naam, de waarde is petrol).
- `site/data/domeinen/index.json`: kleur per rechtsgebied (categorisch, nooit groen).
- `site/logo/*.svg`, favicons, `site/assets/*.webp`, `site/video/*-poster-*.jpg`.

## Structureel: drie vangnetten
1. `python3 -I tools/check_huisstijl.py` faalt op groen in code en afbeeldingen. Draait in GitHub Actions bij elke push (`.github/workflows/huisstijl.yml`).
2. `python3 -I tools/herkleur_afbeeldingen.py <bestanden>` zet groen in nieuwe ChatGPT-illustraties om naar petrol. Altijd draaien na het toevoegen van een afbeelding.
3. Werk alleen in deze repo. Een snapshot uit een andere (privé) werkrepo overschrijft de kleuren anders weer.

## Afbeeldingen (ChatGPT-prompt)
Platte vectorillustratie, dunne donkerblauwe contourlijnen, vlakken in petrol `#0F5C63` en zeer licht grijsblauw `#E2E6E6`, één oranje accent `#A84A00`, witte achtergrond, 4:3, geen tekst, geen groen. Generiek Nederlands straatbeeld of kantoor, geen herkenbare Rotterdamse bouwwerken (landelijke uitstraling). Per rechtsgebied één beeld: bestandsnaam `site/assets/dom-<slug>.webp` (1100x825).

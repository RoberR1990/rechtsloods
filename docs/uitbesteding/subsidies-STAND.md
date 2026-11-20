# Subsidies en gemeentelijke bijdragen — STAND (slug `subsidies`)

Branch `claude/project-thread-jm3o88` (repo `RoberR1990/rechtsloods`). Niets in de live-index; status `in-opbouw`. Besluiten: `subsidies-besluiten.md`.

## Stappen
- [x] 0 Oriëntatie (patroon sociaal-domein: `col/sociaal-domein`)
- [x] 1 Verzamelen: feeds 2016-nov 2026 (best + civ); 697 voorselectie, 316 na kop-check op gemeentelijk orgaan. Bijlagen-bug: GERAAKT 0.
- [x] 2 Taxonomie (6 onderwerpen, 14 subs, 19 argumenten) en uitkomstregels bevroren als concept; check 0 fouten
- [~] 3 Laag 1 (Haiku): pilot batch 1 loopt
- [ ] 4 Selectie laag 2 · [ ] 5 Laag 2 · [ ] 6 Nakijkronde · [ ] 7 Stand · [ ] 8 Site-data · [ ] 9 Overdracht

## Bevindingen
- Volume: 316 kandidaten, niet de geschatte 1.000-2.000. Oorzaak: filter werkt op kop + inhoudsindicatie (volledige-tekstzoeken is geblokkeerd, proxy 403). Rechtbankzaken zonder 'subsidie' in de inhoudsindicatie missen we. Beperking noteren in overdracht.
- Domeinafbeelding: placeholder; ChatGPT-prompt: zie docs/huisstijl.md; onderwerp "gemeentelijk loket voor een subsidieaanvraag, stapel dossiers, kantoor"; bestand `site/assets/dom-subsidies.webp`, 1100x825, petrol #0F5C63, lichtgrijsblauw #E2E6E6, één oranje accent #A84A00, geen tekst, geen groen.

## Volgende actie
Laag 1 golven (`l1-subsidies-0002..0013`), daarna `lab/subsidies_l1_nacontrole.py lijst`.

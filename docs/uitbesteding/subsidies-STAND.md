# Subsidies en gemeentelijke bijdragen — STAND (slug `subsidies`)

Branch `claude/project-thread-jm3o88` (repo `RoberR1990/rechtsloods`). Niets in de live-index; status `in-opbouw`. Besluiten: `subsidies-besluiten.md`.

## Stappen
- [x] 0 Oriëntatie (patroon sociaal-domein: `col/sociaal-domein`)
- [x] 1 Verzamelen: feeds 2016-nov 2026 (best + civ); 697 voorselectie, 316 na kop-check op gemeentelijk orgaan. Bijlagen-bug: GERAAKT 0.
- [x] 2 Taxonomie (6 onderwerpen, 14 subs, 19 argumenten) en uitkomstregels bevroren als concept; check 0 fouten
- [x] 3 Laag 1 (Haiku): 316 uitspraken, 217 relevant, 99 niet relevant, 25 zekerheid laag, check_l1 0 fouten. Herzienbatch (1 uitspraak) niet gedraaid.
- [x] 4 Selectie laag 2: alle 217 relevante (klein domein), 37 batches van 6 (`lab/selecteer_subsidies_l2.py`)
- [~] 5 Laag 2 (Sonnet): batches 1-28 klaar en gecheckt (check_uit_v3, extra_check, privacy: 0 fouten); 29-37 liepen bij de pauze nog; ~25k tokens per uitspraak
- [ ] [ ] 6 Nakijkronde · [ ] 7 Stand · [ ] 8 Site-data · [ ] 9 Overdracht

## Bevindingen
- Volume: 316 kandidaten, niet de geschatte 1.000-2.000. Oorzaak: filter werkt op kop + inhoudsindicatie (volledige-tekstzoeken is geblokkeerd, proxy 403). Rechtbankzaken zonder 'subsidie' in de inhoudsindicatie missen we. Beperking noteren in overdracht.
- Domeinafbeelding: placeholder; ChatGPT-prompt: zie docs/huisstijl.md; onderwerp "gemeentelijk loket voor een subsidieaanvraag, stapel dossiers, kantoor"; bestand `site/assets/dom-subsidies.webp`, 1100x825, petrol #0F5C63, lichtgrijsblauw #E2E6E6, één oranje accent #A84A00, geen tekst, geen groen.

## Gepauzeerd (zuinig, weeklimiet) — Volgende actie
1. Ontbrekende laag-2-bestanden: `ls data/uit_v3/subsidies` vs `lab/sets/subsidies_l2.json`; ontbrekende batches opnieuw draaien (`lab/subsidies_v3_opdracht.md`, 1 batch per Sonnet-agent), check_uit_v3 + extra_check + `lab/subsidies_privacy_check.py` tot 0.
2. Blinde steekproef 10% (`lab/subsidies_steekproef.py trek|score`), nakijkronde (`lab/subsidies_nakijk_uitkomst.py lijst|toepas`).
3. `scripts/dom_build.py subsidies --geen-embed`, `lab/stand_dom.py prep|samen subsidies`, `lab/subsidies_site_na.py`, privacy-scan, sitetest. Daarna overdracht.
NB: `data/` (feeds, xml) is gitignored; opnieuw ophalen: feeds met `scripts/feed.py` (zie `subsidies_select.py`), dan `subsidies_prep.py fetch|parse|in`.

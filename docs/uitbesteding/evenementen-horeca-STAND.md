# STAND evenementen-horeca
- [x] 0 Oriëntatie (repo = snapshot; scripts verwachten /home/claude/{data,scripts,site}: symlinks naar werkmap, niet in repo)
- [x] 1 Feeds (best 2016-2026: 15k-40k/jr; civ idem) opgehaald; kandidaten = `scripts/dom_select_evenementen_horeca.py` -> 2.325 (907 hoogste rechters/hoven), 669 grensgevallen uitgesloten
- [x] 1b Precisie steekproef 100 (Haiku): 79 ja, 14 nee, 4 grens-oo, 3 twijfel => 79-83%; filter daarna aangescherpt (nu 2.325)
- [x] 2 Taxonomie (8 onderwerpen, ±35 subs), argumenten (15), config, besluiten (reviewpunt 1 zelf bevestigd)
- [~] 3 XML ophalen en parsen
- [ ] 4 Laag 1 Haiku
- [ ] 5 Selectie + laag 2 Sonnet
- [ ] 6-9 Nakijk, stand, site-data, overdracht
Domeinafbeelding: placeholder nodig `site/assets/dom-evenementen-horeca.webp` (1100x825). ChatGPT-prompt: "Platte vectorillustratie, dunne donkerblauwe contourlijnen (#1F2F44), vlakken petrol #0F5C63 en zeer licht grijsblauw #E2E6E6, één oranje accent #A84A00, witte achtergrond, 4:3, geen tekst, geen groen. Nederlands straatbeeld: horecaterras met parasols en tafeltjes, op de achtergrond een marktkraam en slingers van een straatfeest." Daarna `python3 -I tools/herkleur_afbeeldingen.py <bestand>`.
Volgende actie: XML-fetch afronden, dom_parse, maak_in_l1, pilot 25.

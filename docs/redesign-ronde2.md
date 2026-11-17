# Redesign ronde 2 (15 nov, Robert): warmer + kortere pagina's

Feedback Robert: "verbetering, maar heel functioneel en kil; mag meer aangekleed; erg lange lijsten en pagina's als ik doorklik — handiger indelen."

## A. Warmer (aankleding)
- Illustraties (komen van Claude, via ChatGPT) in `site/assets/`: `hero.webp` (4:3), `dom-parkeren.webp`, `dom-openbare-orde.webp`, `dom-avg-privacy.webp` (elk 4:3), `lab.webp` (4:3), `video-poster.webp` (16:9), `volgen.webp` (4:3). Bouw ze nu al in met `<img loading="lazy" alt="" onerror="this.remove()">` (decoratief, alt leeg) zodat ontbrekende beelden niets breken.
- #start: hero in twee kolommen (tekst links, hero.webp rechts, mobiel eronder, max 420px breed). H1 2.5rem desktop. Domeinrijen krijgen links een thumbnail 88×66 (object-fit cover, radius 8px) van dom-<slug>.webp; binnenkort zonder beeld. Filmpjesvak gebruikt video-poster.webp als achtergrond met een ronde afspeel-knop-vorm (CSS) en tekst "Filmpje volgt".
- Afwisselende volle-breedte banden: wit en `#F2F7F3` (heel licht groen) om secties te scheiden, i.p.v. alleen lijnen. Radius 8px voor blokken/knoppen/beelden. Groen accent mag iets ruimer: kopjes van secties met een klein groen streepje erboven (24×3px), primaire knoppen groen.
- #domein: kop met dom-<slug>.webp rechts (desktop, max 280px), tekst links. #lab: lab.webp naast intro. #volgen: volgen.webp naast intro.
- Geen gradients, geen schaduwen, geen emoji, geen serif.

## B. Korter en beter ingedeeld (doel: #domein en #sub < 2.600px hoog op 1440×900; meet voor/na en rapporteer)
- #domein: onderwerpen als raster van 2 kolommen (1 op mobiel): per onderwerp een blok (achtergrond #F7FAF8, radius 8px, padding 20px): kleurstip + naam + 1 regel uitleg + "N uitspraken · M nieuw", daaronder de 3 subonderwerpen met de meeste nieuwe uitspraken (link + "M nieuw") en een `<details>` "Alle N subonderwerpen" met de rest (elk met Volg-knop). Volg-knoppen in de top-3 ook. "Net uitgesproken": 3 i.p.v. 5, met link "Meer".
- #sub-<o>--<s>: bovenaan een sticky subnav onder de kop: "De stand · Uitspraken · Volgen" (ankers). Stand: eerste 3 regels zichtbaar, rest in "Toon alle N regels". Uitspraken: 5 compacte rijen (titel, kern-zin, uitkomst · instantie · datum); het citaat in `<details>` "Zo schreef de rechter het" (blijft met al.-link); knop "Toon 5 meer" (tot max 20) en daarna link naar Zoeken met filter.
- Lange tekstpagina's (#snel, #trends-*, #stand, #stand-*, #over): automatische inhoudsopgave uit de h2's: desktop sticky rechterkolom (220px) naast de tekst, mobiel een `<details>` "Op deze pagina" bovenaan. Plus "Naar boven"-link onderaan lange pagina's.
- #zoeken: resultaten per 20, knop "Toon meer".
- #volgen: subonderwerpen gegroepeerd per onderwerp in `<details>`; open als er iets voorgeselecteerd is in die groep, anders dicht. Telling gekozen bovenaan ("3 gekozen").
- Rapporteer paginahoogte (px) voor/na voor: start, domein, sub-parkeerbelasting--betalen, snel, stand, volgen, zoeken.

## Randvoorwaarden
Zelfde als `docs/redesign-nov2026.md` (één bestand, geen externe fetch, alle routes blijven werken, 0 console-fouten desktop+mobiel, ook domein openbare-orde).

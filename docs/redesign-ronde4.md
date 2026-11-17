# Redesign ronde 4 (15 nov, akkoord Robert) — uit UX-review + persona-ronde 3
Bronnen: /home/claude/ux-review.md, /home/claude/persona-r3.md (lees ze). Randvoorwaarden als ronde 1-2.

## Volgen — besluit Robert: route B (tijdelijk intern Teams-kanaal)
- #volgen: bovenaan als hoofdroute een blok "Voor collega's van Gemeente Rotterdam: volg het Teams-kanaal Rechtsloods Parkeren" met primaire knop "Open het Teams-kanaal". Link uit constante `TEAMS_KANAAL_URL` (nu leeg). Leeg = knop disabled met tekst "Kanaal wordt deze week ingericht". Eén zin: "Elke week één bericht met de nieuwe uitspraken, in gewone taal en met bron."
- Daaronder "Andere gemeenten": e-mail (binnenkort, zoals nu) en "Zelf een feed gebruiken" ingeklapt (`<details>`) met de feedadressen en de bestaande uitleg (Power Automate/Outlook). Woord "feedlezer" uitleggen in 1 zin.
- Rijen onderwerpen: zichtbaar uitklapteken (›/▸ en rotatie), "≈ N per maand" i.p.v. de zin over 12 maanden. "0 gekozen" pas tonen als >0.
- Op #sub en #domein blijft "Volg" (alleen op #sub, zie onder) naar #volgen gaan.

## Home
- Hero: één primaire knop "Bekijk Parkeren" (→ domKies parkeren) + secundair zoekveld "of zoek direct" (→ #zoekalles). Het blok "Zo ziet een uitleg eruit" direct onder de hero, vóór "Kies je vak".
- Filmvak: geen afspeelknop zolang `VIDEO_SRC` leeg is; toon de poster met klein label "Uitlegfilmpje volgt". AVG-omschrijving zonder "camera's" (bv. "Persoonsgegevens, privacy en algoritmes van de overheid.").

## Domeinpagina
- Subonderwerp-rijen duidelijk klikbaar: hele rij is link, chevron › rechts, hover-achtergrond. Alleen "N nieuw" (of niets als 0) i.p.v. "353 · 35 nieuw"; totaal staat al op onderwerpniveau. Geen Volg-knoppen op deze pagina.
- Uitklapper heet "Alle N onderwerpen over <onderwerp-label in kleine letters>".

## Onderwerppagina (#sub)
- Bij de eerste uitspraak staat "Zo schreef de rechter het" standaard open.
- Subnav: actieve tab onderstreept (3px groen) en vet, actief volgen met IntersectionObserver.
- "Volg dit onderwerp" maar één keer (rechtsboven); onderste weg.
- Rechtspraak.nl-link per uitspraak ("Lees de hele uitspraak") ook hier.

## Uitspraakpagina (#uitspraak-…)
- Volgorde: titel → uitkomst-regel → "Wat betekent dit voor de gemeente" (actie_gemeente / lessen; normale tekstgrootte, niet grijs) → kern + citaat → rest.
- Lege/nietszeggende blokken weg: bewijs "niet aan de orde"/leeg, lijn "onbekend", "Herkomst". Dubbele samenvatting samenvoegen: "Uitleg voor de burger" (klantuitleg) als uitklapper onder kern i.p.v. eigen blok.
- Knoppen: één primaire "Kopieer voor je jurist"; "Kopieer bronvermelding", "Kopieer link" als tekstlinks; "Klopt iets niet?" tekstlink onderaan.
- Bron-chips "al. N": op mobiel (≤860px) tonen ze het citaat inline uitgeklapt onder de zin (i.p.v. naar het paneel onderaan te springen); desktop zoals nu. Spatie tussen opeenvolgende chips.
- Kopnav: op uitspraak- en sub-pagina's is "Onderwerpen" actief (niet "Zoeken").
- Broodkruimel op één regel: Parkeren › Onderwerp › Subonderwerp.

## Jargon
- Chips "HR 2026" → "Hoge Raad, 2026"; "Hof 2016" → "Gerechtshof, 2016"; "RvS" → "Raad van State"; "Rb." → "Rechtbank" (waar ruimte; in compacte meta mag "Rb." blijven met title-attribuut). "al. 22" → "Alinea 22" in chips.
- "Lijn X" → "Vaste lijn: X". Woordenlijst (`site/woordenlijst.json`, structuur respecteren) aanvullen met: vaste lijn, CROW-kencijfers, voorlopige voorziening/voorlopig oordeel, Wahv, feed(lezer), ECLI, naheffingsaanslag (als niet al aanwezig). B1, max 2 zinnen.

## Over
- "Gecontroleerd door jurist … Nu: 0" → zin "Nog niet door een jurist nagekeken; dat is de volgende stap." Regels met teller 0 verbergen.

## Zoeken
- Filters ingeklapt achter knop "Filter (N actief)"; behoud Onderwerp, Subonderwerp, Instantie, Jaar, Uitkomst, Soort zaak, Gemeente (één gemeentefilter: haal de dubbele weg, behoud "Gemeente is partij" als vinkje). "Raakt team" weg. 20 per pagina blijft.

## Mobiel / toegankelijkheid
- Alle knoppen/chips/summary's ≥ 44px tikhoogte op ≤860px. Grijze hulptekst min. 14px.
- Snel op de hoogte: rechtsgangen-schema op ≤700px als verticale lijst i.p.v. SVG.

## Kleine fouten
- "degemeente" (schema-tekst) → "de gemeente". "al. 22al. 23" → spatie/margin.

## Testen
Zoals ronde 2 + meet stappen persona P1 (home → Betalen-onderwerp → citaat zichtbaar): doel ≤ 3 klikken.

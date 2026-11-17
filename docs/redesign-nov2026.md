# Redesign Rechtsloods — opdracht (15 nov 2026, branch `redesign`)

Akkoord Robert 15 nov. Doel: een collega (Rotterdam én kleine gemeente, even belangrijk; productmanager Parkeren weegt het zwaarst) ziet in 5 seconden wat de site doet, komt binnen via zijn domein/subonderwerp, leest uitspraken in gewone taal met bron, en kan volgen. USP = de AI-uitleg in gewone taal (kort en lang), altijd met citaat.

## Harde randvoorwaarden
- Alles blijft in `site/index.html` (één bestand) + data-bestanden. Geen externe fetch/CDN/fonts. Werkt in het claude.ai-artifact én op Cloudflare Pages.
- Domeinwissel blijft via `domKies(slug, hash, q)` (localStorage + reload). Bestaande views (zoeken, detail, stand, stand-sub, snel, trends, mijn, maand, check, mist, borden, weetjes, assistent, roadmap, over, zoekalles, gedeelde links) moeten blijven werken via hun hash.
- Geen bestanden van de data-sessie wijzigen (`site/data/**`). `site/feeds/**` is gegenereerd door `scripts/maak_feeds.py` — niet handmatig wijzigen; wel lezen (`feeds/index.json`).
- Elke uitleg-zin die getoond wordt met citaat blijft met bron (alinea-link) zoals nu.

## Navigatie
- Zijbalk (`nav.zij`) weg op alle schermen. Eén kopbalk: logo "Rechtsloods" (→ #start) · **Onderwerpen** (→ #domein; toont domeinnaam, bv. "Parkeren", met klein pijltje dat een lijstje rechtsgebieden opent) · **Zoeken** (→ #zoeken) · **Volgen** (→ #volgen) · **Lab** (→ #lab, lichter gestyled) · **Over** (→ #over). Rechts: knop "Aa" (bestaand weergave-menu). Kopzoekbalk weg (zoeken zit op de pagina's). Mobiel: logo + menuknop die dezelfde 5 items als lijst opent.
- De gele/beige dekkingsbalk (peildatum + 5%-tekst) weg uit de kop. Vervangen door één dunne **fasebalk** onder de kop op elke pagina: "**Experiment** · Uitleg gemaakt met AI, altijd met de zin uit de uitspraak erbij · Geen juridisch advies · [Geef feedback]" (feedback → #over#contact of een anker in Over). Peildatum en 5%-zin verhuizen naar de domeinpagina (klein, grijs) en naar Over.
- Rondleiding start NIET meer automatisch. Wel te starten vanuit Over ("Rondleiding").

## Pagina's
### #start (algemene home)
1. H1: "Blijf bij in de rechtspraak over jouw vak." Eén zin eronder: "Rechtsloods vertaalt uitspraken van rechters naar gewone taal, met bij elke uitleg de zin uit de uitspraak waar die op rust. Gratis, voor iedere gemeente."
2. **Kies je vak** — de rechtsgebieden als grote, rustige rijen (geen kaartjes): naam, één regel wat erin zit, aantal uitspraken, status ("live" niets extra; "in opbouw" grijze tekst). `binnenkort` als één grijze regel eronder ("Binnenkort: Sociaal domein, Woo, Grond"). Klik → `domKies(slug,"domein")`.
3. **Zo werkt het** (3 stappen, genummerd in tekst, geen iconen): Kies je onderwerp · Lees wat de rechter besliste in gewone taal, met bron · Volg het onderwerp en zie nieuwe uitspraken.
4. **Filmpjesvak**: een rustig blok 16:9 met grijze poster, tekst "Uitleg in 1 minuut — filmpje volgt", geen autoplay. Code zo dat later een `<video>` met `<track>` erin kan (constante `VIDEO_SRC=""`; leeg = placeholder). Naast/onder het vak: de 3 stappen dienen als tekstalternatief.
5. **Eén voorbeeld van de vertaling** (statisch, het eerste uit de bestaande voorbeeldset; niet roterend): citaat rechter (grijs, gewone sans, met aanhalingstekens) → "In gewone taal" → uitleg → bron (instantie, datum, link naar uitspraak).
6. Kort "Wat het wel en niet is" (2 zinnen) + afzenderregel.
Weg van home: hero-zoekbalk, roterende stapel, "Wat je hier kunt doen", "Net uitgesproken", "Wist je dat", "Nieuw in het vak", recept-blok.

### #domein (domeinpagina, hier landt de gebruiker)
- H1 = domeinnaam. Eén zin wat erin zit + kleine grijze regel peildatum/aantal + 5%-zin met link "Hoe werkt dit?".
- Zoekveld (één) "Zoek in uitspraken over parkeren" → #zoeken.
- Link-regel: "Nieuw in dit vak? Begin met Snel op de hoogte (10 minuten)" → #snel.
- **Onderwerpen**: per onderwerp (taxonomie) een kopje met één regel uitleg (bestaande OW_UITLEG/DT), daaronder de subonderwerpen als lijst-rijen: label (link → `#sub-<o>--<s>`), rechts aantal uitspraken + "N nieuw" (laatste 90 dagen t/m laatste uitspraakdatum), indien stand.json een lijn-indicator heeft: die als korte grijze tekst. Achteraan per rij een kleine knop "Volg" (→ #volgen met dit sub voorgeselecteerd, via sessionStorage `rl-volg-pre`).
- **Net uitgesproken**: 5 nieuwste als lijst (titel, kern-zin, uitkomst-stip, instantie · datum).
- Onderaan: "Tip een collega" — knop "Kopieer link naar deze pagina" + regel "Ander vak? Rechtloods heeft ook: …" (andere live domeinen).
- Bestaande rollen-blok ("Ik ben…"), "Goed om te weten", grafieken: weg van deze pagina.

### #sub-<o>--<s> (onderwerppagina, NIEUW, het werkpaard)
- Kruimel: Parkeren › Onderwerp. H1 = sublabel. Volg-knop rechtsboven (→ #volgen voorgeselecteerd).
- **De stand in het kort**: als `stand.json` iets heeft voor dit sub: de lijn-indicator + maximaal 5 regels (de belangrijkste regels/vaste lijn uit de bestaande stand-data, met hun bronlinks zoals vStandSub ze toont) + link "Volledige stand van het recht" → `#stand-<…>` (gebruik dezelfde sleutel als bestaande links). Anders: zin "Voor dit onderwerp is nog geen samenvatting van de vaste lijn."
- **Laatste uitspraken** (10, nieuwste eerst, alleen met samenvatting; knop "Meer" → #zoeken met filter o/s gezet): per uitspraak: titel (link detail), kern-zin in gewone taal, daaronder "Zo schreef de rechter het:" + citaat (grijs) met alinea-link, uitkomst-stip + instantie · datum.
- Knop **"Kopieer voor je jurist"**: kopieert platte tekst: onderwerp, de stand (regels + bron-ECLI's), en per getoonde uitspraak titel, kern, citaat, ECLI + link `https://uitspraken.rechtspraak.nl/details?id=<ECLI>`; slotzin "Uitleg gemaakt met AI (Rechtsloods); de uitspraak zelf is leidend."
- Werkt voor elk live domein (taxonomie per domein).

### #volgen (vervangt mockup)
- H1 "Volgen". Eén zin: "Kies wat je wilt volgen. Nieuwe uitspraken komen dan naar jou toe."
- Lijst subonderwerpen van het huidige domein met vinkjes (voorselectie uit `rl-volg-pre`), met per rij "≈ N per maand" (gemiddeld over laatste 12 maanden; = volumepreview).
- Daaronder **Hoe wil je het ontvangen?** drie tabs/blokken:
  1. **E-mail — binnenkort.** Uitgegrijsd formulier (e-mailadres, frequentie wekelijks/maandelijks, knop "Aanmelden" disabled) met regel: "Komt na de privacycheck. We vragen dan alleen je e-mailadres, je bevestigt via een link, en je kunt je in elke mail met één klik afmelden." Plus knop "Laat weten dat je dit wilt" → bestaande interesse-mechanisme of mailto-loze tekst: verwijs naar Over/contact.
  2. **Teams-kanaal (via Power Automate)** — korte uitleg: maak een flow met trigger "Wanneer een feeditem wordt gepubliceerd" (RSS) en actie "Bericht posten in een chat of kanaal"; plak de feedadres(sen). Eerlijk: "Werkt alleen als Power Automate in jouw organisatie aanstaat. De oude RSS-koppeling in Teams bestaat sinds mei 2026 niet meer."
  3. **Feedlezer of klassieke Outlook** — "Klassieke Outlook: rechtsklik op RSS-abonnementen › Nieuwe RSS-feed toevoegen. Het nieuwe Outlook ondersteunt RSS niet."
- Per gekozen sub het feedadres (absolute URL: `https://rechtsloods.nl/` + `feed` uit `feeds/index.json`) met knop "Kopieer". Plus domeinfeed bovenaan ("Alles over Parkeren").
- Bestaande localStorage-volgstatus mag blijven als "bewaard op dit apparaat".

### #lab
- H1 "Lab". Intro: "Ideeën die we hebben uitgeprobeerd maar niet hebben uitgewerkt. Ze zijn er om het gesprek te openen: zie je er iets in, of juist niet? Laat het Robert of Sander weten." (link naar contact in Over).
- Rijen (titel, 1 zin wat het is, label "Idee, niet uitgewerkt", link): Mijn gemeente (#mijn), Waar gemeenten de mist in gaan (#mist), Bezwaar-assistent (#assistent), Wist je dat…? (#weetjes), Borden en verkeersbesluiten (#borden, "proef").
- Op elk van die Lab-views zelf: bovenaan één regel "Lab · Idee, niet uitgewerkt · Geef je mening" (zelfde stijl).

### #over
- Bestaande Over-inhoud + bovenaan inhoudslijstje met: Hoe werkt het · Waarom maakt Rotterdam dit · Contact (anker `contact`) · Roadmap (#roadmap) · Rondleiding starten · Peildatum en 5%-uitleg.

## Uiterlijk (geldt site-breed, overschrijft het oude CSS-blok)
- Achtergrond overal `#FFFFFF`; vlakken die moeten afwijken `#F5F7F6`. Geen beige/crème (zoek en vervang alle beige/gele achtergronden).
- Tekst `#1B1B1B`, secundair `#5B615E`, lijnen `#E2E6E4`. Accent Rotterdam-groen `#00811F` (hover `#005C15`) alleen voor links, primaire knop, actieve nav-onderstreping, focusring.
- Lettertype: `system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif` voor alles, ook koppen en citaten (geen serif). H1 2rem/700, H2 1.25rem/700, body 1rem/1.55.
- Max inhoudsbreedte 960px, gecentreerd, ruime witruimte. Hoeken 4px. Geen schaduwen, geen kaartjes-rasters, geen pill-badges, geen dikke gekleurde zijranden, geen gradients, geen emoji/iconen-tegels. Lijsten = rijen met 1px lijn ertussen.
- Uitkomst-stip + tekst blijft (bestaand). Onderwerpkleurblokjes mogen blijven (klein).
- Donkere modus uit het weergavemenu blijft werken (pas de variabelen aan).
- Toegankelijkheid: contrast AA, zichtbare focus, nav als `<nav>` met `aria-current`, filmpjesvak met tekstalternatief.

## Testen
- `cd site && python3 -m http.server 8765`; Playwright (python) screenshots desktop 1440×900 en mobiel 390×844 van: #start, #domein, #sub-parkeerbelasting--betalen (of een bestaand sub), #volgen, #lab, #over, #zoeken, een #uitspraak-…, #stand, #snel, #mijn. Ook domein openbare-orde (localStorage `jr-domein`).
- 0 console-fouten. Bestaande views laden nog.

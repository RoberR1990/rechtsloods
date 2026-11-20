# Aanscherping sociaal domein (laag 1 en laag 2), bevroren 20 nov 2026 — eerste versie
Lees ook `data/dom/sociaal-domein/config.json` (velden `uitkomstregels` en `privacy`) en `taxonomie.json` (`_toewijzing`). Deze regels gaan vóór `lab/aanscherping_v3c.md` als ze botsen.

## Uitkomst (vanuit de burger; bij contractzaken de zorgaanbieder; bij verhaal de onderhoudsplichtige)
- **Alleen procedure**: de burger wint alleen proceskosten, griffierecht, een dwangsom, schadevergoeding wegens te lange duur, een termijnpunt of niet-ontvankelijkheid van de ander. Ook: de zaak wordt alleen teruggewezen, of het besluit wordt vernietigd met **rechtsgevolgen in stand** (art. 8:72 lid 3 Awb). Ook een conclusie van de AG valt hieronder.
- **Misbruik** van (proces)recht vastgesteld: wederpartij wint.
- **Spiegelregel** (hoger beroep of cassatie): het hoger beroep van het college slaagt = wederpartij wint. Het hoger beroep van het college faalt en de rechtbank gaf de burger gelijk = burger wint. Het hoger beroep van de burger faalt = wederpartij wint. Lees in de kop wie appellant is.
- **Voorlopige voorziening**: wie krijgt wat hij vroeg, wint. Toegewezen = burger wint, afgewezen = wederpartij wint, deels toegewezen = deels. `uitkomst_toelichting` begint met "Voorlopig: ".
- **Terugvordering, boete, maatregel**: de uitkomst volgt wat de rechter beslist over de oplegging. Volledig vernietigd = burger wint. Verlaagd = **deels**: lager bedrag, kortere periode, lager percentage, lagere boete, of een waarschuwing in plaats van een boete. In stand = wederpartij wint.
- **Intrekking blijft, terugvordering of boete gaat omlaag of vervalt**: deels.
- **Aanvraag** (bijstand, Wmo, jeugdhulp, schuldhulp): besluit vernietigd omdat de rechter zelf toekent of de gemeente opnieuw moet onderzoeken = burger wint.
- **Dictum ontbreekt of is afgekapt**: zekerheid "laag". Markeer de zaak niet als "niet relevant" alleen omdat het dictum ontbreekt. Meld haar in je eindrapport als twijfelgeval.

## Labels
- Kies het subonderwerp naar de **kernvraag die de rechter beslist** (zie `taxonomie._toewijzing`).
- Zaken van aanbieders tegen de gemeente (tarief, contract, aanbesteding) vallen altijd onder `aanbieders-contractering`. Het pgb-tarief van een burger valt onder `wmo/pgb-eigen-bijdrage` of `jeugdwet/pgb-tarief-jeugd`.
- `zaaktype`: `bijstand-pw` (Participatiewet, WWB), `bbz-tozo-tonk`, `ioaw-ioaz`, `wmo`, `jeugdwet`, `schuldhulp`, `contractering-aanbieder`, `verhaal` (civiel, art. 62 Pw), `overig`.
- `gemeente_is_partij`: true bij college, burgemeester, sociale dienst, intergemeentelijke dienst (ISD), gemeenschappelijke regeling of gemeentelijke kredietbank. Bij het CAK is dit false; noem het CAK als wederpartij.
- `gemeente`: zie `config.rotterdam_partij` voor de schrijfwijzen van Rotterdam. "Rechtbank Rotterdam" maakt Rotterdam **niet** tot partij.

## Privacy (hard; dit domein wacht op FG-akkoord)
- Geen namen, adressen, geboortedata, BSN, rekeningnummers, kentekens, namen of leeftijden van kinderen, of precieze diagnoses. Ook niet als ze in de uitspraak staan.
- Gebruik algemene woorden: "betrokkene", "de partner", "een kind", "een huisgenoot", "een zorgvraag", "medische beperkingen", "psychische klachten". Het onderwerp van de zaak (hulp bij het huishouden, traplift, bijzondere bijstand voor inrichting) mag wel.
- Noem geen land of plaats van bezit, geen werkgever en geen school. Noem bedragen alleen als ze voor het oordeel nodig zijn (hoogte boete, terugvordering).
- **Citaten**: kies passages over de rechtsregel en de beoordeling, niet over persoonlijke of medische omstandigheden. Staat er geen bruikbaar citaat zonder zulke details: geen citaat en zekerheid "laag".
- "betrokkene" is in dit domein toegestaan; de waarschuwing `jargon "betrokkene"` van `check_uit_v3` mag je negeren. Gebruik "bewoner" alleen als de uitspraak dat zegt.

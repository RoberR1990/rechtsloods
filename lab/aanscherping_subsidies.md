# Aanscherping subsidies (laag 1 en laag 2), bevroren 20 nov 2026 — eerste versie
Lees ook `data/dom/subsidies/config.json` (velden `uitkomstregels` en `privacy`) en `taxonomie.json` (`_toewijzing`). Deze regels gaan vóór `lab/aanscherping_v3c.md` als ze botsen.

## Uitkomst (vanuit de aanvrager of subsidieontvanger: de organisatie of persoon die subsidie vraagt, kreeg of moet terugbetalen)
- **Alleen procedure**: de aanvrager wint alleen proceskosten, griffierecht, een dwangsom, schadevergoeding wegens te lange duur, een termijnpunt of niet-ontvankelijkheid van de ander. Ook: de zaak wordt alleen teruggewezen, of het besluit wordt vernietigd met **rechtsgevolgen in stand** (art. 8:72 lid 3 Awb). Ook een conclusie van de AG.
- **Misbruik** van (proces)recht vastgesteld: wederpartij wint.
- **Spiegelregel** (hoger beroep of cassatie): hoger beroep van het college slaagt = wederpartij wint; faalt en de rechtbank gaf de aanvrager gelijk = aanvrager wint; hoger beroep van de aanvrager faalt = wederpartij wint. Lees in de kop wie appellant is.
- **Voorlopige voorziening**: wie krijgt wat hij vroeg, wint; `uitkomst_toelichting` begint met "Voorlopig: ".
- **Terugvordering of lagere vaststelling**: volgt wat de rechter over het bedrag beslist. Volledig vernietigd = aanvrager wint; lager terug te vorderen bedrag of hogere vaststelling dan het college deed = **deels**; in stand = wederpartij wint.
- **Weigering of intrekking blijft staan, bedrag of motivering deels hersteld**: deels.
- **Subsidieplafond en verdeling**: telt of de aanvrager alsnog subsidie krijgt of een nieuwe beslissing met kans op subsidie. Een beter gemotiveerd besluit met dezelfde uitkomst voor de aanvrager = alleen procedure.
- **Dictum ontbreekt of is afgekapt**: zekerheid "laag"; niet "niet relevant" alleen daarom; meld in je eindrapport.

## Relevantie (laag 1)
- Relevant: subsidie (of financiële bijdrage die als subsidie wordt behandeld) met een **gemeentelijk orgaan** (college, burgemeester, raad, deelgemeente, gemeenschappelijke regeling) als bestuursorgaan, of een civiele zaak over een gemeentelijke subsidie of bijdrage. Ook als het gaat om een subsidieverordening.
- NIET relevant (`relevant: false`, reden max 10 woorden): Rijksregelingen (minister, RVO, NOW, TVL, SDE, EZK, LNV...), provincie, waterschap, DUO; Wmo-, jeugdhulp- en bijstandszaken (domein sociaal); toeslagen; belastingzaken; ambtelijke rechtspositie. Een gemeente die alleen als belanghebbende optreedt telt niet.

## Labels
- Kies het subonderwerp naar de **kernvraag die de rechter beslist** (`taxonomie._toewijzing`).
- `zaaktype` uit `config.zaaktype`; `gemeente_is_partij` true bij een gemeentelijk orgaan; `gemeente`: zie `config.rotterdam_partij`. "Rechtbank Rotterdam" maakt Rotterdam **niet** tot partij.

## Privacy
- Subsidiezaken gaan meestal over rechtspersonen. Geen namen van natuurlijke personen (bestuurders, medewerkers), geen adressen, geboortedata, BSN of rekeningnummers. Gebruik "de aanvrager", "de stichting", "de vereniging", "de ondernemer". Een organisatienaam alleen als nodig voor het begrip; liever generiek.
- Citaten over de rechtsregel en de beoordeling, niet over persoonlijke omstandigheden.

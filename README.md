# Rechtsloods

**Loodst je door de rechtspraak, in gewone taal.**

Rechtsloods maakt rechterlijke uitspraken doorzoekbaar en begrijpelijk voor mensen die geen jurist zijn, zoals de ambtenaar bij een gemeente die parkeren, handhaving of bezwaren erbij doet. Elke uitleg heeft een bron: de alinea in de uitspraak en een letterlijk citaat. De site draait op [rechtsloods.nl](https://rechtsloods.nl).

Rechtsloods begon als experiment bij afdeling Parkeren (Stadsbeheer, Gemeente Rotterdam), met parkeerzaken als eerste rechtsgebied. Het is gebouwd om uit te breiden naar andere domeinen en om gedeeld te worden.

## Meewerken: gemeenten, VNG, Rechtspraak en andere ketenpartners

Dit is een open project. Je kunt helpen met:

- juridische toetsing van de AI-samenvattingen (de jurist-toets staat in `docs/`)
- nieuwe rechtsgebieden of onderwerpen (zie `docs/schema_v3.md` en `docs/datacontract.md`)
- gebruikersonderzoek bij gemeenten, en feedback op wat ambtenaren echt nodig hebben
- koppelingen met bronnen van ketenpartners
- code, ontwerp en toegankelijkheid van de site

Open een issue of pull request, of neem contact op.

**Wil je Rechtsloods samen naar een hoger niveau tillen, bijvoorbeeld als gemeente, VNG, Rechtspraak of andere ketenpartner? Benader me via [LinkedIn](https://www.linkedin.com/in/rriteco).**

## Opbouw

| Map | Inhoud |
|---|---|
| `site/` | De website (statisch, zonder build-stap) en de data die de site laadt |
| `scripts/` | Pijplijn: uitspraken ophalen, parsen, samenvatten, controleren |
| `lab/` | Experimenten en maatstaven voor de kwaliteit van de samenvattingen |
| `data/uit_v3/` | Afgeleide uitvoer per rechtsgebied |
| `docs/` | Schema's, datacontract, meetaanpak, resultaten van de pilots |
| `tools/` | Hulpscripts |

## Lokaal draaien

De site is statisch:

```
cd site && python3 -m http.server 8765
```

Open daarna http://localhost:8765. De ruwe uitspraken (open data van rechtspraak.nl) staan niet in deze repo; `setup.sh` verwacht ze in `data/raw/`.

## Uitgangspunten

- Bronvermelding is cruciaal: elke bewering met bron-alinea en letterlijk citaat.
- Gewone taal (B1), geen juridisch jargon.
- Rechtsloods is geen juridisch advies. Controleer belangrijke beslissingen altijd aan de uitspraak zelf.
- Doorontwikkeling hangt af van animo en gebruik.

## Licentie

De code staat onder de [EUPL-1.2](LICENSE). Uitspraken zijn afkomstig van [rechtspraak.nl](https://www.rechtspraak.nl) (open data).

# Meetplan Rechtsloods (Umami) — 15 nov 2026

Code: `site/meet.js` (alleen actief als `CONF.host` en `CONF.id` gevuld zijn, en alleen op rechtsloods.nl). Test: `?meet=debug` toont alle gebeurtenissen in de console, er gaat niets weg.

## Vragen die de meting moet beantwoorden
| # | Vraag | Gebeurtenis / bron |
|---|---|---|
| 1 | Komt er iemand, en wie? Waar komen ze vandaan? | `sessie_start` {bron, verwijzer, campagne, apparaat, terug, landing, rol}, Umami-referrers |
| 2 | Waar zoeken ze op, en vinden ze wat? | `zoek` {term, woorden, plek, resultaten, poging, herformulering}, `zoek_leeg` {term} |
| 3 | Welke uitspraken en onderwerpen trekken aandacht? | pagina's `/uitspraak/<ECLI>`, `/onderwerp/<slug>`, `/stand/<slug>`, `uitspraak_open` {ecli, van} |
| 4 | Is de uitleg genoeg, of gaan ze naar de bron? | `uitgaand` {doel: rechtspraak.nl, ecli}, `kopieer` {wat: bronvermelding}, `fout_melden` |
| 5 | Wat doen ze met het resultaat (hergebruik)? | `kopieer` {wat: link_uitspraak, tekst_voor_jurist, klantuitleg, beslisbrief, raadsantwoord, toetslijst, verweer}, `deel`, `print`, `tekst_gekopieerd` |
| 6 | Hoe lang blijven ze, hoe ver lezen ze? | `verblijf` {pagina, actief_s, klasse}, `scroll` {pagina, diepte 25/50/75/100}, Umami bounce en bezoekduur |
| 7 | Komen ze terug en volgen ze? | `terug` in `sessie_start`, bezoeker-id (retentie), `volg`, `volg_stand`, `bladwijzer` |
| 8 | Welk vak en welke rol trekt? | `domein_gekozen`, `interesse_vak` (binnenkort-vakken: vraag naar nieuwe domeinen), `rol_gekozen` |
| 9 | Welke gemeenten zijn geïnteresseerd? | `profiel` {gemeente} (alleen als iemand het zelf invult), `verwijzer` (host van verwijzende site) |
| 10 | Werkt de site technisch? | `fout_js`, `data_fout`, `laden_traag`, `uitspraak_onbekend`, Umami Performance (LCP, INP, CLS) |
| 12 | Kijken ze de uitlegfilm? | `video_start` {pagina, ondertitels, formaat: breed of staand}, `video_50`, `video_complete` (één keer per paginabezoek) |
| 13 | Delen ze een domein? | `delen_link` {domein} (link gekopieerd via Deel-knop), `delen_flyer` {domein} (flyer-PDF geopend); flyer-QR/URL heeft `utm_source=flyer`, gedeelde link `utm_source=deel` (bron `print` / `deel` in `sessie_start`) |
| 11 | Gebruiken ze de gereedschappen? | `bezwaar_check`, `bezwaar_voorbeeld` (tekst gaat nooit mee), `filter`, `meer_resultaten`, `inhoud_klik` |

## Gebeurtenissen (alle krijgen `domein` mee; waar zinvol `pagina`)
- `sessie_start` een keer per tabblad. Sessie-eigenschappen via `identify`: bron, terug, apparaat, domein.
- `zoek` na elke zoekactie (4 zoekvelden: start, start_groot, alle_vakken, vak). `resultaten` is het aantal dat de bezoeker zag; `zoek_leeg` apart voor snel lezen van gemiste zoekvragen.
- `filter` {veld, waarde} bij keuzelijsten, vinkjes en keuzerondjes op de pagina; nooit vrije tekst.
- `kaart_klik` {van, positie}: klik op een resultaatkaart, met plek in de lijst (werkt als rangschikkings-signaal).
- `verblijf` bij verlaten van een pagina: actieve seconden (tabblad zichtbaar), plus klasse. Umami toont dit als gemiddelde via de getallen-eigenschap `actief_s`.
- Overige: zie tabel hierboven.

## Pagina's in Umami (virtueel pad, zonder hash)
`/` start · `/zoeken` · `/zoekalles` · `/domein` · `/snel` · `/stand` · `/stand/<onderwerp--sub>` · `/onderwerp/<slug>` · `/trends/<slug>` · `/uitspraak/ECLI:NL:..` · `/volgen` · `/lab` · `/over[/..]` · `/gedeeld` (profiel-links, nooit het adres zelf).

## Privacy
- Geen cookies. Geen naam, e-mail of IP-opslag door ons; Umami middelt IP weg.
- **Zoektermen gaan mee** (besluit Robert 15-11). Eerst opgeschoond: kleine letters, max 80 tekens, e-mail, kentekens en cijferreeksen vanaf 7 cijfers worden vervangen. Namen van personen kunnen we niet betrouwbaar herkennen; daarom: bij elke analyse zoektermen als aggregaat lezen, niet per bezoeker.
- Tekst die iemand in de Bezwaar-assistent plakt gaat nooit mee.
- Bezoeker-id: willekeurig getal in de browser voor retentie; wissen met "Mijn bezoeken niet meetellen" (voet van de site). Do Not Track en `?meet=uit` worden gerespecteerd.
- Voor Gemeente Rotterdam: noem dit in de privacytekst als de site breder gedeeld wordt (staat al op de roadmap onder AVG-check).

## Dashboards die ik in Umami zou zetten (na de eerste week)
1. **Aanloop**: sessies per bron, verwijzer, nieuw vs terug, apparaat.
2. **Zoeken**: top-zoektermen, `zoek_leeg` (wat missen we), herformuleringen (wat vindt men niet bij eerste poging), resultaten per plek.
3. **Inhoud**: top-uitspraken, top-onderwerpen, uitgaand naar rechtspraak.nl per ECLI.
4. **Hergebruik**: kopieer-acties per soort, delen, printen.
5. **Gezondheid**: fouten, trage laadtijd, Core Web Vitals.

## Drempels om te leren (voorstel)
- Na 100 sessies: bron-mix en apparaat bekijken.
- Na 300 zoekacties: top-20 zoektermen en `zoek_leeg` doorlopen, synoniemenlijst en inhoud bijsturen.
- Succescriterium experiment (zelf vast te stellen): aandeel sessies met >=1 uitspraak geopend, aandeel terugkerend, aandeel met een kopieer- of volgactie.

## Volume
Een actief bezoek levert ruwweg 10-30 gebeurtenissen (pageviews, verblijf, scroll, kliks). Umami op de NAS heeft geen limiet; Umami Cloud Hobby wel (100k/maand).

## Installatie (15 nov 2026)
- Umami draait op de NAS (Container Manager, project `umami-stats`, poort 3020). Website "rechtsloods" (rechtsloods.nl) staat erin.
- Publiek via Cloudflare Tunnel `vault-robertriteco`: `https://stats.rechtsloods.nl` met alleen `^/(script\.js|api/send)$`. Het dashboard blijft alleen intern bereikbaar (het interne beheeradres).
- `site/meet.js` heeft host en website-id ingevuld.

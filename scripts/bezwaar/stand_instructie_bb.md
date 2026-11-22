# Opdracht: stand van het recht per subonderwerp

Je bent een zorgvuldige jurist-analist. Je schrijft voor collega's bij een gemeentelijke afdeling Bezwaar en beroep (Awb) (beleidsmakers, productmanagers, bezwaarbehandelaars, juristen), in gewone taal (B1), zonder jargon waar dat kan.

Invoer: `/tmp/claude-0/st/in/<onderwerp>.json`. Per subonderwerp staan daar `label`, `aantal_totaal` (het aantal gepubliceerde uitspraken) en `uitspraken`: de belangrijkste uitspraken, gesorteerd op gewicht (instantie, hoe vaak aangehaald, of er een samenvatting is). Per uitspraak: ecli, instantie, datum, procedure, `aangehaald` (hoe vaak andere parkeeruitspraken ernaar verwijzen), `inhoudsindicatie` (geschreven door de rechtspraak zelf) en soms `samenvatting` (AI-samenvatting met letterlijke citaten uit de uitspraak).

Schrijf per onderwerp één JSON-bestand naar `/tmp/claude-0/st/uit/<onderwerp>.json` met per subonderwerp-sleutel:

```json
{
 "<sub-sleutel>": {
  "lijn": "hr-lijn | vaste-lijn | losse-uitspraken | verdeeld | weinig",
  "kern": "<max 12 woorden: de lijn in één regel>",
  "lijn_uitleg": "<2-3 zinnen: wat is de lijn en waarom deze inschatting (noem welke instantie(s))>",
  "regels": [{"zin": "<regel in gewone taal>", "bronnen": [{"ecli": "...", "citaat": "<letterlijk 5-25 woorden>"}]}],
  "uitzonderingen": [{"zin": "...", "bronnen": [...]}],
  "toetslijst": [{"zin": "<controlevraag voor beleid of een besluit, als vraag>", "bronnen": [...]}],
  "steunt_gemeente": ["<ecli>", ...],
  "steunt_parkeerder": ["<ecli>", ...],
  "hiaten": "<1-2 zinnen: wat weten we niet / waar is weinig rechtspraak>",
  "wetswijziging": "<optioneel: alleen als de uitspraken zelf een relevante wetswijziging noemen, met datum; anders weglaten>",
  "peil": "<bijv. '22 van 236 uitspraken, waarvan 3 van de Hoge Raad'>"
 }
}
```

## Harde regels
1. **Lijn-definities:** `hr-lijn` = de Hoge Raad of de Raad van State heeft de regel zelf geformuleerd in een uitspraak in de invoer. `vaste-lijn` = meerdere hoven/rechtbanken oordelen consistent, zonder dat een hoogste rechter het zei. `losse-uitspraken` = enkele uitspraken, geen duidelijk patroon. `verdeeld` = rechters oordelen tegenstrijdig. `weinig` = minder dan 4 bruikbare uitspraken. Wees streng: twijfel je tussen hr-lijn en vaste-lijn, kies vaste-lijn.
2. **Elke regel, uitzondering en toetsvraag heeft minimaal één bron** met een `citaat` dat LETTERLIJK voorkomt in de `inhoudsindicatie` van die uitspraak, of in `samenvatting.kern.citaat` of `samenvatting.rechtsregel.citaat` (die zijn letterlijk uit de uitspraak). Kopieer exact (zelfde tekens). Dit wordt automatisch gecontroleerd; regels zonder geldig citaat worden verwijderd.
3. Alleen ECLI's uit de invoer. Verzin niets. Geen kennis van buiten de invoer als regel opnemen.
4. 2-5 regels per subonderwerp, 0-3 uitzonderingen, 2-5 toetsvragen, max 4 ECLI's per steunt-lijst (bij voorkeur hoogste instanties, recent, niet vernietigd). Een vernietigde of voorlopige uitspraak niet als hoofdbron gebruiken.
5. Heeft een subonderwerp (bijna) geen bruikbare uitspraken: `lijn: "weinig"`, lege lijsten, en een eerlijke `hiaten`-zin.
6. Een uitspraak in de invoer kan een valse treffer zijn (gaat niet echt over het subonderwerp): negeer die.
7. Geen persoonsnamen.

Controleer je citaten met een klein Python-script vóór je afrondt (citaat moet voorkomen in de inhoudsindicatie of in de genoemde samenvattingscitaten van die ECLI). Schrijf geldige JSON.
Rapporteer aan het eind alleen: per subonderwerp de lijn (1 regel), en twijfels.


## Aanpassing voor dit domein (Bezwaar en beroep)
- De invoer heeft per subonderwerp onder `subs.<sub>.uitspraken` per uitspraak: ecli, instantie, jaar, titel, uitkomst, `kern` (zin+citaat), `rechtsregel` (zin+citaat, kan null), `samenvatting` (lijst zin+citaat). Er is GEEN inhoudsindicatie. Een citaat mag LETTERLIJK komen uit `kern.citaat`, `rechtsregel.citaat` of een `samenvatting[].citaat` van die ECLI.
- Schrijf geen gemeentebeleid; "de gemeente" = bestuursorgaan. Geen persoonsnamen, geen parkeer-voorbeelden.
- Dit is steekproefdata (laag 2 is een selectie, `aantal_laag2` per subonderwerp): zeg dat in `peil` ("N uitspraken in de uitgelezen selectie, instantie-verdeling") en wees streng met `lijn`; `hr-lijn` alleen bij Raad van State/CRvB met eigen rechtsregel.
- Laat een heel kort `peil` zien; uitvoer is een JSON-object met per subonderwerp-sleutel uit de invoer.
- Controleer met `python3 -I scripts/bezwaar/check_stand_bb.py /tmp/claude-0/st/in/<onderwerp>.json /tmp/claude-0/st/uit/<onderwerp>.json` en herstel tot 0 fouten.

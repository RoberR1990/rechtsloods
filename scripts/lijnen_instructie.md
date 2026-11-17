# Opdracht: standaardlijn per bezwaargrond (voor bezwaarbehandelaars)

Bezwaarbehandelaars bij een gemeentelijke afdeling Parkeren (geen juristen) willen per veelgebruikte bezwaargrond weten: wat oordelen rechters meestal, wanneer gaat dat niet op, en wanneer moet de zaak naar een jurist. Gewone taal (B1).

Invoer: `/home/claude/data/stand_in/argumenten.json`: per argumentsleutel de belangrijkste kandidaat-uitspraken (ecli, instantie, datum, onderwerp, aangehaald, inhoudsindicatie, soms `argumenten` met het oordeel en een letterlijk citaat, en `kern`). Labels staan in `/home/claude/data/argumenten.json`. Let op: kandidaten zijn deels met trefwoorden gevonden en kunnen valse treffers zijn.

Schrijf naar `/home/claude/data/stand_uit/lijnen_<jouw-deel>.json`:

```json
{
 "<argumentsleutel>": {
  "lijn": "hr-lijn | vaste-lijn | losse-uitspraken | verdeeld | weinig",
  "regime": "<voor welk regime vooral: parkeerbelasting / Wahv / bestuursrecht / civiel / meerdere>",
  "standaard": "<2-3 zinnen: wat rechters meestal oordelen over deze grond>",
  "bronnen": [{"ecli": "...", "citaat": "<letterlijk 5-25 woorden>"}],
  "uitzonderingen": [{"zin": "<wanneer de grond wél slaagt of de lijn niet geldt>", "bronnen": [...]}],
  "doorzetten": "<1 zin: in welk geval een jurist moet meekijken>",
  "bouwsteen": "<3-4 zinnen in B1 die een behandelaar in een brief aan een burger kan gebruiken, neutraal en respectvol, zonder ECLI-nummers in de tekst; schrijf 'de rechter' in plaats van namen van instanties>"
 }
}
```

## Harde regels
1. Elk `citaat` LETTERLIJK uit de `inhoudsindicatie` van die ECLI, of uit `argumenten[].citaat` of `kern.citaat` van die ECLI. Exact kopiëren. Dit wordt automatisch gecontroleerd.
2. Alleen ECLI's uit de invoer. Niets verzinnen. Is er te weinig bruikbare rechtspraak: `lijn: "weinig"` en zeg dat eerlijk in `standaard`; bouwsteen dan weglaten.
3. 1-3 bronnen voor de standaard, 0-2 uitzonderingen. Vernietigde of voorlopige uitspraken niet als hoofdbron.
4. De bouwsteen mag nooit een uitkomst beloven en moet passen bij een afwijzing óf toewijzing; formuleer als uitleg van de regel.
5. Geen persoonsnamen.

Controleer citaten met een klein script vóór je afrondt. Rapporteer alleen: per sleutel de lijn (1 regel) en twijfels.

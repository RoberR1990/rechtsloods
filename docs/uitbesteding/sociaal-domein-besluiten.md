# Sociaal domein: besluiten (door Robert te bevestigen)

Elk besluit: wat ik heb gekozen, het alternatief, waarom, en de status "door Robert te bevestigen". Vaste regels uit bestaande domeinen gaan voor eigen inzicht.

## B1. Werkrepo: `rechtsloods` in plaats van `rechtzoeker`
- **Besluit:** gewerkt in `RoberR1990/rechtsloods`, de enige repo die aan deze sessie hangt.
- **Alternatief:** werken in `RoberR1990/rechtzoeker` (privé), zoals de opdracht zegt.
- **Reden:** `rechtzoeker` is voor deze sessie niet bereikbaar (add_repo: "you don't have access"). `list_repos` toont alleen `rechtsloods`.
- **Status:** door Robert te bevestigen.

## B2. Vertrekpunt `main` in plaats van `live`
- **Besluit:** branch `col/sociaal-domein` vertrekt vanaf `main` (db7c004).
- **Alternatief:** vertrekken vanaf `live`.
- **Reden:** `rechtsloods` heeft geen `live`. `main` is "snapshot live, 16 nov 2026" plus drie huisstijlcommits.
- **Status:** door Robert te bevestigen.

## B3. Geen domeininhoud per uitspraak in deze (openbare) repo: BLOKKADE na stap 2
- **Besluit:** stap 0–2 volledig uitgevoerd. Dat zijn afbakening, tellingen, filter, precisiemeting, taxonomie, uitkomstregels en config. Ook de tooling voor stap 3–8 staat klaar. Stap 3–8 heb ik **niet** uitgevoerd: labels, samenvattingen, citaten, stand en site-data.
- **Alternatief:** alles bouwen en op `col/sociaal-domein` in `rechtsloods` zetten.
- **Reden:** `rechtsloods` is **openbaar** (`list_repos`: visibility public) en is de geschoonde export van de werkrepo (`scripts/export-openbaar.sh` laat `data/` behalve `uit_v3` bewust weg). Een branch in een openbare repo is voor iedereen leesbaar. Daarmee zou het domein gepubliceerd zijn. De opdracht zegt hard: "Niet publiceren zonder FG-akkoord" en "blijft altijd op je eigen branch". Die regel gaat uit van een privé-repo. Stap 3 en verder leveren per uitspraak inhoud op (labels, samenvattingen, citaten). Die wil ik vóór FG-akkoord niet openbaar maken.
- **Wat wél in de repo staat:** scripts, config, taxonomie, besluiten, tellingen en een ECLI-lijst met metadata. Dat zijn instantie, datum, wetscode uit het zaaknummer en prioriteit. Al deze gegevens staan ook openbaar in Open Data Rechtspraak. Inhoudsindicaties en uitspraakteksten staan niet in de repo.
- **Status:** door Robert te bevestigen. Oplossing: start een sessie met `rechtzoeker` gekoppeld, haal deze branch binnen (`git fetch https://github.com/RoberR1990/rechtsloods col/sociaal-domein`) en hervat bij "Volgende actie" in de STAND.

## B4. Slug `sociaal-domein` naast bestaande `sociaal` in index.json
- **Besluit:** nieuwe slug `sociaal-domein` zoals de opdracht zegt. De bestaande regel `sociaal` (status binnenkort, n=12792) in `site/data/domeinen/index.json` laat ik ongemoeid.
- **Alternatief:** de bestaande slug `sociaal` hergebruiken.
- **Reden:** de opdracht noemt de slug expliciet. De live-index mag ik buiten mijn branch niet aanpassen. Het samenvoegen van beide regels is een besluit bij het live zetten.
- **Status:** door Robert te bevestigen.

## B5. Afbakening CRvB op wetscode in het zaaknummer
- **Besluit:** bij de CRvB selecteer ik op de wetscode in het zaaknummer (PW, WWB, WIJ, BBZ, IOAW/NIOAW, IOAZ/NIOAZ, TOZO, TONK, WWIK, WMO, WMO15, WVG, JW). Een zaak met alleen codes buiten scope valt af, ook als de inhoudsindicatie een kernbegrip noemt (WIA, ZW, AW, AOW, Wajong, WW, AWBZ, Wlz, Zvw, ...). Zonder code (of met een generieke code zoals ONBEK) val ik terug op kernbegrippen.
- **Alternatief:** alleen op kernbegrippen in de inhoudsindicatie, zoals `dom_select.py` voor andere domeinen.
- **Reden:** de code is de eigen indeling van de CRvB. Op kernbegrippen alleen komen UWV-, SVB- en ambtenarenzaken binnen die "bijstand" of "terugvordering" noemen.
- **Status:** door Robert te bevestigen.

## B6. IOAW/IOAZ, Bbz, Tozo, Tonk en WWIK binnen scope (rubriek bijstand)
- **Besluit:** meegenomen onder de rubriek "bijstand".
- **Alternatief:** alleen de Participatiewet in strikte zin.
- **Reden:** de gemeente voert deze regelingen uit als bestuursorgaan, bij dezelfde afdeling Werk en Inkomen, en de CRvB toetst ze met dezelfde begrippen (inlichtingenplicht, terugvordering, boete).
- **Status:** door Robert te bevestigen.

## B7. AIO-aanvulling (SVB) buiten scope; eigen bijdrage Wmo via het CAK binnen scope
- **Besluit:** AIO-zaken zonder gemeentelijk orgaan vallen af (278 zaken; de SVB is daar bestuursorgaan). Zaken over de eigen bijdrage Wmo waarin het CAK beslist, blijven binnen scope (34 zaken).
- **Alternatief:** beide houden, of beide uitsluiten.
- **Reden:** de opdracht beperkt het domein tot de gemeente als bestuursorgaan. De eigen bijdrage Wmo noemt de opdracht expliciet: die volgt uit de gemeentelijke verordening, het CAK stelt haar vast en int haar. Precisiemeting: Haiku zag de CAK-zaak als niet relevant; ik houd haar bewust.
- **Status:** door Robert te bevestigen.

## B8. Uitgesloten: vreemdelingenzaken, Caribisch deel, leerlingenvervoer, Wsw, Wsnp, kinderbescherming, huurzaken
- **Besluit:** uitgesloten zijn:
  - vreemdelingenzaken: zaaknummer `NLxx.`, of besluit van minister, staatssecretaris, IND of COA zonder gemeentelijk orgaan;
  - de Caribische gerechten: Aruba, Curaçao, Sint Maarten en BES, waar de Nederlandse gemeentewetten niet gelden;
  - leerlingenvervoer;
  - Wsw (CRvB-code WSW);
  - Wsnp;
  - civiele kinderbeschermingszaken (ots, uithuisplaatsing, machtiging gesloten jeugdhulp);
  - civiele huur- en ontruimingszaken waarin schuldhulp alleen een argument is.
- **Alternatief:** Wsw en leerlingenvervoer meenemen; ze zijn ook gemeentelijk.
- **Reden:** de opdracht noemt ze niet als scope. Wsw en leerlingenvervoer zijn andere teams en wetten. Kinderbescherming staat expliciet buiten scope.
- **Status:** door Robert te bevestigen.

## B9. Civiel recht alleen bij contractering/tarieven/aanbesteding of verhaal
- **Besluit:** civiele uitspraken alleen als een gemeentelijke regeling samengaat met aanbesteding, inkoop, tarieven, (raam)overeenkomst, subsidie of aanbieders, en een gemeente genoemd wordt. Verhaal van bijstand (art. 62 Pw, bijstandsverhaal) komt er altijd in. Dat zijn 134 civiele kandidaten.
- **Alternatief:** geen civiel recht.
- **Reden:** de opdracht noemt tarieven en contractering met aanbieders, en verhaal. Die zaken lopen vaak via de civiele rechter (kort geding aanbesteding, verhaal via de familierechter).
- **Status:** door Robert te bevestigen.

## B10. Hoogste rechter
- **Besluit:** CRvB voor Participatiewet, Wmo, Jeugdwet en bijbehorende regelingen (10.789 uitspraken). Raad van State voor schuldhulpverlening (Wgs): 73 van de 109 RvS-uitspraken, geen enkele Wgs-zaak bij de CRvB. Hoge Raad alleen in civiele zaken over verhaal en contractering (32, inclusief conclusies AG).
- **Alternatief:** —
- **Reden:** geverifieerd in de data (zie `sociaal-domein-tellingen.md`). Dit is van belang voor de spiegelregel en voor "hr-lijn" in de stand: bij Wgs-zaken is de RvS de hoogste rechter.
- **Status:** door Robert te bevestigen.

## B11. Rotterdam als partij: varianten
- **Besluit:** herkenning met `config.rotterdam_partij`. Varianten die in de data voorkomen: "het college van burgemeester en wethouders van Rotterdam" (327× in de steekproef), "… van de gemeente Rotterdam" (126×), "het college van burgemeester en wethouders Rotterdam" (zonder "van", nieuwe stijl 2026), de tikfout "burgermeester", en "(Werk en Inkomen van de) gemeente Rotterdam". Het tweede deel van de bestaande ROT-regex in `dom_parse.py` ("Rotterdam … verweerder/appellant") geeft vals-positieven: "Rechtbank Rotterdam … verweerder" bij zaken van Capelle, Drechtsteden of de Belastingdienst. Dat deel gebruik ik niet.
- **Alternatief:** de ROT-regex uit `dom_parse.py` ongewijzigd gebruiken.
- **Reden:** op 1.260 teksten verschillen beide regexen in 7 gevallen. 5 daarvan zijn vals-positieven van de oude regex, 2 gemiste varianten.
- **Status:** door Robert te bevestigen. `dom_parse.py` zelf heb ik niet aangepast (gedeeld script).

## B12. Precisie en dubbele publicaties
- **Besluit:** filter vastgezet na een onafhankelijke controle met 98,3% precisie (59 van 60). Dubbele publicaties (zelfde instantie, datum en zaaknummer): 0 gevonden. Massazaken met (bijna) gelijke inhoudsindicaties (806) houd ik; `dom_build` markeert ze als cluster.
- **Alternatief:** massazaken ontdubbelen.
- **Reden:** dat zijn verschillende zaken met dezelfde rechtsvraag, geen dubbele publicaties.
- **Status:** door Robert te bevestigen.

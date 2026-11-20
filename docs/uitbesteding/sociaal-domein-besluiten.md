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

## B13. Taxonomie: 8 onderwerpen, 29 subonderwerpen (concept, "eerste versie")
- **Besluit:** ik heb de indeling afgeleid uit 150 gelezen koppen en inhoudsindicaties (gestratificeerd: 70 bijstand, 45 Wmo, 20 jeugd, 10 schuldhulp, 5 civiel) en een begrippentelling over alle 16.499. De onderwerpen:
  - bijstand-recht (6);
  - bijstand-handhaving (6);
  - bijzondere-bijstand (2);
  - wmo (7);
  - jeugdwet (3);
  - schuldhulp (1);
  - aanbieders-contractering (2);
  - procedure (2).

  Samengevoegd omdat ze dun waren:
  - verhaal (±50) is een kenmerk onder terugvordering-invordering;
  - eigen bijdrage (±135) zit samen met pgb;
  - IOAW/IOAZ (±130) is een kenmerk onder aanvraag en een eigen zaaktype;
  - schuldhulp heeft één subonderwerp met kenmerken;
  - procedure heeft twee subonderwerpen.

  Elk subonderwerp heeft volgens de grove telling ≥ 45 kandidaten (`lab/sociaal_taxonomie.py tel`).
- **Alternatief:** indelen per wet (Pw, Wmo, Jw) met de procedurezaken in elk onderwerp.
- **Reden:** collega's zoeken op het probleem (terugvordering, samenwonen, hulp bij het huishouden), niet op de wet. De wet komt terug als facet `zaaktype`. Aanbieders staan apart van burgerzaken, zoals de opdracht vraagt: andere wederpartij, ander team (`raakt: inkoop-contractmanagement`).
- **Status:** door Robert te bevestigen. Vakinhoudelijk nakijken door een collega van Werk en Inkomen / Wmo / Jeugd. Tot dan `concept: true`.

## B14. Uitkomstregels: algemene regels overgenomen, domeinregels toegevoegd
- **Besluit:** overgenomen:
  - alleen procedure;
  - misbruik = wederpartij wint;
  - spiegelregel;
  - voorlopige voorziening ("Voorlopig: ");
  - conclusie AG = alleen procedure.

  Toegevoegd:
  - terugvordering, boete of maatregel verlaagd = deels;
  - intrekking blijft maar terugvordering of boete omlaag = deels;
  - vernietiging met rechtsgevolgen in stand (art. 8:72 lid 3 Awb) = alleen procedure;
  - bij contractzaken telt het perspectief van de zorgaanbieder, bij verhaal dat van de onderhoudsplichtige;
  - afgekapt dictum = zekerheid laag, niet "niet relevant".

  Alles staat in `config.uitkomstregels` en `lab/aanscherping_sociaal.md`.
- **Alternatief:** bij "rechtsgevolgen in stand" de burger als winnaar zien (het besluit is immers vernietigd).
- **Reden:** de burger krijgt dan inhoudelijk niets. Dat sluit aan bij de bestaande regel "alleen procedure = alleen kosten of termijn gewonnen".
- **Status:** door Robert te bevestigen.

## B15. Config-formaat: extra velden naast het bestaande formaat
- **Besluit:** `config.json` heeft het formaat van avg-privacy en openbare-orde (de Woo-config staat niet in deze repo). Toegevoegde velden:
  - `uitkomstregels`, `privacy`, `rotterdam_partij` (regex);
  - `hoogste_rechter`;
  - `versie: "eerste versie"`, `status_privacy`.
- **Alternatief:** de regels alleen in een opdrachtbestand zetten.
- **Reden:** de opdracht vraagt alles in `config.json`. De extra velden breken bestaande scripts niet: `check_l1` en `check_uit_v3` lezen alleen zaaktype, raakt, toepasselijkheid en bezwaargronden_verplicht_bij.
- **Status:** door Robert te bevestigen; gelijktrekken met Woo-config.

## B16. "betrokkene" toegestaan in samenvattingen
- **Besluit:** in dit domein mag "betrokkene" als algemene term. `verrijk_v3.md` verbiedt het en `check_uit_v3.py` geeft er een waarschuwing (geen fout) op. Die waarschuwing negeren we hier (zie `lab/aanscherping_sociaal.md`).
- **Alternatief:** "de burger" overal.
- **Reden:** de opdracht schrijft "betrokkene" voor als neutrale term. De privacyregels vragen algemene termen voor andere personen in de zaak.
- **Status:** door Robert te bevestigen. `check_uit_v3.py` heb ik niet aangepast (gedeeld script).

## B17. Selectie laag 2 met quota (stap 4, klaar in `lab/selecteer_sociaal_l2.py`)
- **Besluit:** volgorde a → b → c → d, met plafonds zodat elke categorie aan bod komt:
  - **a.** Rotterdam partij, max 200: eerst hoogste rechter (tot 120), dan rechtbank;
  - **b.** hoogste rechters (CRvB, RvS, HR), nieuwste eerst, tot totaal 350;
  - **c.** alle hoven, tot 400;
  - **d.** dunne subonderwerpen aanvullen tot 20, tot 450.

  Binnen a en b gaat het om en om per subonderwerp, nieuwste eerst. Per massacluster tellen maximaal 2 zaken.
- **Alternatief:** strikte volgorde zonder plafond.
- **Reden:** naar schatting ±2.240 zaken hebben Rotterdam als partij (stap 1). Zonder plafond vult (a) alle 450 plekken, en vooral met bijstandsterugvordering. Let op: 29 × 20 = 580 > 450, dus niet elk subonderwerp haalt 20. Stap d vult eerst de dunste aan.
- **Status:** door Robert te bevestigen.

## B18. Proef op 25 + 2 uitspraken om de tooling te valideren, uitvoer niet bewaard
- **Besluit:** ik heb één laag-1-batch (25, Haiku) en twee laag-2-uitspraken (Sonnet) gedraaid op de opdrachten en checks van dit domein. Dat valideert de config en de opdrachten en meet het tokenverbruik. De uitvoer is daarna verwijderd en niet gecommit (B3).
- **Alternatief:** geen proef, alleen de scripts klaarzetten.
- **Reden:** zonder proef is "tooling klaar" niet getoetst. Een volgende sessie zou dan pas bij de eerste batch op configfouten stuiten.
- **Status:** door Robert te bevestigen.

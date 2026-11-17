import json, sys
OUT = "/home/claude/data/proef/uit/"

def Z(zin, bron, citaat):
    return {"zin": zin, "bron": bron, "citaat": citaat, "dekking": "ok"}

def RR(zin, bron, citaat, herkomst):
    d = Z(zin, bron, citaat)
    d["herkomst"] = herkomst
    return d

def A(arg, oordeel, bron, citaat):
    return {"arg": arg, "oordeel": oordeel, "bron": bron, "citaat": citaat}

R = {}

R["ECLI_NL_RVS_2016_164"] = {
 "ecli": "ECLI:NL:RVS:2016:164", "relevant": True,
 "onderwerp": "handhaving-privacy", "sub": "woo-inzage", "sub2": "kentekenregistratie-avg",
 "gemeente": "Amsterdam", "uitkomst": "gelijk burger",
 "titel": "Doorsturen van inzageverzoek is geen beslissing",
 "kern": Z("De rechter besliste dat de gemeente te laat was met een besluit op een verzoek om inzage in persoonsgegevens, omdat het doorsturen naar parkeerbedrijf Cition geen beslissing was.", [37, 38], "is het Wbp-verzoek slechts intern doorgezonden"),
 "samenvatting": [
  Z("De parkeerder maakte bezwaar tegen een naheffing parkeerbelasting en vroeg de gemeente Amsterdam ook om te laten weten of zijn persoonsgegevens worden verwerkt.", [11], "verzocht hem mede te delen of hem betreffende persoonsgegevens zijn verwerkt"),
  Z("De gemeente stuurde zijn brief door naar parkeerbedrijf Cition, dat de bezwaren tegen naheffingen behandelt.", [32], "omdat Cition B.V. bezwaren tegen naheffingsaanslagen behandelt"),
  Z("De parkeerder vond dat die doorzendbrief geen beslissing op zijn verzoek was.", [34], "blijkt dat met de brief niet op zijn Wbp-verzoek is beslist"),
  Z("De gemeente liet op de zitting weten dat de directeur van Cition en ambtenaren van de gemeentelijke dienst allemaal bevoegd zijn om parkeerbelasting te heffen.", [36], "de algemeen directeur van Cition B.V. heeft aangewezen als gemeenteambtenaar"),
  Z("De Raad van State vond dat doorsturen binnen dezelfde gemeentelijke organisatie geen beslissing is, en de rechtbank verklaarde het beroep tegen het uitblijven van een besluit daarom ten onrechte niet-ontvankelijk.", [37, 38], "is het Wbp-verzoek slechts intern doorgezonden"),
  Z("De gemeente krijgt twee weken om alsnog te beslissen en betaalt anders € 100 per dag (maximaal € 15.000); ook het griffierecht van € 293 wordt vergoed.", [53, 52, 54], "een dwangsom verbeurt voor elke dag waarmee hij de hiervoor genoemde termijn overschrijdt"),
 ],
 "rechtsregel": RR("Stuurt een gemeente een verzoek om inzage in persoonsgegevens alleen intern door naar een andere bevoegde ambtenaar, dan is dat geen beslissing; blijft een echte beslissing uit, dan kan de burger beroep instellen tegen het niet tijdig beslissen.", [37], "kan niet worden aangemerkt als een af- of toewijzing van het Wbp-verzoek", "eigen oordeel"),
 "lessen_voor_gemeente": [
  Z("De rechter woog dat een verzoek dat alleen naar een andere bevoegde ambtenaar (hier Cition) is doorgestuurd nog niet is beantwoord: de gemeente bleef daardoor in gebreke.", [38], "in gebreke een besluit op het Wbp-verzoek te nemen. Voorts waren op die datum twee weken verstreken"),
 ],
 "verwijst_naar": [], "zekerheid": "hoog",
 "uitkomst_type": "procedure",
 "uitkomst_toelichting": "Gemeente was te laat met beslissen op inzageverzoek; moet binnen twee weken beslissen, anders dwangsom.",
 "wetsartikelen": ["art. 35 Wbp", "art. 6:12 Awb", "art. 1:3 Awb", "art. 231 Gemeentewet", "art. 8:55d Awb"],
 "argumenten": [A("te-laat-beslist", "gehonoreerd", [38], "in gebreke een besluit op het Wbp-verzoek te nemen. Voorts waren op die datum twee weken verstreken")],
 "steunt": "parkeerder",
}

R["ECLI_NL_RVS_2016_1740"] = {
 "ecli": "ECLI:NL:RVS:2016:1740", "relevant": True,
 "onderwerp": "vergunningen", "sub": "bedrijfsvergunning", "sub2": None,
 "gemeente": "Amsterdam", "uitkomst": "gelijk gemeente",
 "titel": "Twee bedrijven met één naam krijgen één parkeervergunning",
 "kern": Z("De rechter vond dat Amsterdam de bedrijfsvergunning terecht introk, omdat TRIP en The Resource zich naar buiten als één bedrijf presenteren.", [31], "zich in het maatschappelijke verkeer presenteren als één bedrijf heeft het college hen terecht"),
 "samenvatting": [
  Z("Amsterdam trok de bedrijfsparkeervergunning van het bedrijf TRIP in per 31 augustus 2014.", [12], "de aan TRIP verleende bedrijfsparkeervergunning ingetrokken met ingang van 31 augustus 2014"),
  Z("TRIP wilde een eigen bedrijfsparkeervergunning houden en was het niet eens met de gemeente.", [19], "TRIP wil de beschikking houden over een eigen bedrijfsparkeervergunning en bestrijdt het standpunt van het college"),
  Z("De gemeente wees erop dat alle bedrijven op hetzelfde adres werken en onder meer dezelfde e-mailadressen, telefoon, website en secretaresse delen.", [28], "allemaal gebruik van een emailadres eindigend op @theresource.nl"),
  Z("De Raad van State vond het niet belangrijk dat de bedrijven financieel gescheiden zijn en andere bestuurders en aandeelhouders hebben.", [31], "Dat TRIP en The Resource hun activiteiten financieel hebben gescheiden"),
  Z("Het beroep van TRIP is daarom ongegrond: de intrekking blijft staan en er volgt geen proceskostenvergoeding.", [34, 35], "zal de Afdeling het beroep tegen het besluit van 13 november 2014 van het college alsnog ongegrond verklaren"),
 ],
 "rechtsregel": RR("Bedrijven die zich naar buiten als één bedrijf presenteren (zelfde adres, telefoon, website, secretaresse) tellen voor de parkeerverordening als één bedrijf, ook als ze juridisch en financieel gescheiden zijn.", [31], "is niet van doorslaggevende betekenis in welke rechtsvorm TRIP en The Resource", "eigen oordeel"),
 "lessen_voor_gemeente": [
  Z("De rechter liet meewegen dat de bedrijven één secretaresse, dezelfde e-mailadressen en één website hadden.", [30], "Zij hebben één secretaresse, dezelfde emailadressen en één website"),
 ],
 "verwijst_naar": [], "zekerheid": "hoog",
 "uitkomst_type": "inhoud",
 "uitkomst_toelichting": "Intrekking blijft staan: TRIP en The Resource gelden samen als één bedrijf.",
 "wetsartikelen": ["art. 1 Parkeerverordening 2013", "art. 37 Parkeerverordening 2013", "art. 40 Parkeerverordening 2013"],
 "argumenten": [],
 "steunt": "gemeente",
}

R["ECLI_NL_RVS_2016_327"] = {
 "ecli": "ECLI:NL:RVS:2016:327", "relevant": True,
 "onderwerp": "vergunningen", "sub": "bewonersvergunning", "sub2": None,
 "gemeente": "Amersfoort", "uitkomst": "gelijk gemeente",
 "titel": "Bewoner met eigen garageplek verliest parkeervergunning",
 "kern": Z("De rechter vond de intrekking van de bewonersvergunning terecht, omdat de bewoner volgens de bouwvergunning een plek in de parkeergarage kon krijgen.", [24], "als huurder van de woning aan de [locatie] te Amersfoort, gezien de bouwvergunning, over een parkeerplaats op eigen terrein"),
 "samenvatting": [
  Z("Een bewoner van Amersfoort had sinds 2004 een parkeervergunning, die de gemeente elk jaar automatisch verlengde.", [20], "over de parkeervergunning die het college jaarlijks automatisch heeft verlengd"),
  Z("De bewoner voerde aan dat hij taxichauffeur is en snel bij zijn auto moet kunnen komen, en dat een garageplek veel duurder is dan zijn vergunning.", [29], "hij taxichauffeur is en derhalve vanuit zijn woning snel bij zijn auto moet kunnen komen"),
  Z("De gemeente zag in 2014 aan de bouwvergunning van 1984 dat hij een plek in de garage kon krijgen en trok daarom de vergunning in om schaarse parkeerruimte eerlijk te verdelen.", [20], "tot de conclusie gekomen dat [appellant] als bewoner van dit complex over een parkeerplaats op eigen terrein kan beschikken"),
  Z("De gemeente vond bovendien dat een bedrijfsbelang bij een Amsterdams taxibedrijf weinig telt.", [31], "dat bedrijfsbelangen in relatie tot parkeren alleen van belang kunnen zijn als het desbetreffende bedrijf in Amersfoort is gevestigd"),
  Z("De Raad van State vond dat de bewoner volgens de bouwvergunning een plek in de garage kon krijgen en dat de gemeente de belangen redelijk had afgewogen.", [24, 32], "als huurder van de woning aan de [locatie] te Amersfoort, gezien de bouwvergunning, over een parkeerplaats op eigen terrein"),
  Z("Het hoger beroep is ongegrond: de vergunning blijft ingetrokken en de gemeente betaalt geen proceskosten.", [37, 38], "Het hoger beroep is ongegrond. De aangevallen uitspraak moet worden bevestigd, voor zover aangevallen"),
 ],
 "rechtsregel": RR("Wie volgens de bouwvergunning van zijn woning een parkeerplaats op eigen terrein (zoals een garageplek) kan krijgen, komt niet in aanmerking voor een straatvergunning; de gemeente mag die vergunning intrekken om schaarse parkeerruimte eerlijk te verdelen.", [24, 27], "over een parkeerplaats op eigen terrein in de zin van de verordening kan beschikken", "eigen oordeel"),
 "lessen_voor_gemeente": [
  Z("De rechter vond de belangenafweging die de gemeente pas in beroep uitlegde (schaarse ruimte weegt zwaarder dan prijsverschil en werkbelang) deugdelijk gemotiveerd.", [32], "het college in beroep deugdelijk gemotiveerd op de door [appellant] aangevoerde belangen is ingegaan"),
  Z("De rechter wees een beroep op de hardheidsclausule af, omdat de bewoner geen gevolgen noemde die de gemeente niet al had meegewogen.", [36], "zich niet op voor hem onaanvaardbare gevolgen van de intrekking van de parkeervergunning heeft beroepen"),
 ],
 "verwijst_naar": [], "zekerheid": "hoog",
 "uitkomst_type": "inhoud",
 "uitkomst_toelichting": "Intrekking blijft staan: bewoner kon via bouwvergunning een garageplek krijgen.",
 "wetsartikelen": ["art. 1 Parkeerverordening 2014 Amersfoort", "art. 10 Parkeerverordening 2014 Amersfoort", "art. 15 Parkeerverordening 2014 Amersfoort"],
 "argumenten": [A("onevenredig", "verworpen", [32], "biedt geen grond voor de conclusie dat de rechtbank ten onrechte tot dit oordeel is gekomen")],
 "steunt": "gemeente",
}

R["ECLI_NL_RVS_2017_1746"] = {
 "ecli": "ECLI:NL:RVS:2017:1746", "relevant": True,
 "onderwerp": "vergunningen", "sub": "bedrijfsvergunning", "sub2": None,
 "gemeente": "Amsterdam", "uitkomst": "gelijk burger",
 "titel": "Tandartsen in één pand zijn niet automatisch één bedrijf",
 "kern": Z("De Raad van State vond dat de tandartspraktijk zich niet als één bedrijf met de andere praktijken presenteert, dus Amsterdam mocht haar bedrijfsparkeervergunning niet intrekken.", [34], "presenteert [appellante] zich niet met de andere tandartspraktijken in het maatschappelijk verkeer als één bedrijf"),
 "samenvatting": [
  Z("Amsterdam trok de bedrijfsparkeervergunning van een tandartspraktijk in.", [11], "de bedrijfsparkeervergunning van [appellante] voor het voertuig met kenteken"),
  Z("De praktijk vond dat de coöperatie waarin de tandartsen deelnemen alleen ruimte verhuurt en dat de bedrijven niet met elkaar zijn verweven.", [24], "de coöperatieve vereniging zich alleen bezig houdt met de verhuur van ruimten aan tandartsen"),
  Z("De gemeente vond dat de vijf tandartspraktijken op hetzelfde adres samen één bedrijf zijn, met te weinig werknemers voor een vergunning.", [22], "samen met de andere tandartsen op hetzelfde adres moet worden beschouwd als één bedrijf"),
  Z("De Raad van State zei dat je eerst kijkt of bedrijven zich naar buiten als één bedrijf presenteren, en daarna of een juridische constructie ze in wezen tot één bedrijf maakt.", [33], "om eerst te bezien of de vergunninghouders zich in het maatschappelijk verkeer presenteren als één bedrijf"),
  Z("Hier waren de praktijken niet één bedrijf: een gezamenlijke coöperatie die de etage verhuurt was niet genoeg.", [34], "Het enkele feit dat de tandartspraktijken deelnemen in een coöperatie die de etage huurt"),
  Z("De intrekking is herroepen en Amsterdam moet de proceskosten en het griffierecht van € 670 vergoeden.", [36, 46, 47, 48], "zal de Afdeling het beroep tegen het besluit van 20 januari 2015 van het college alsnog gegrond verklaren"),
 ],
 "rechtsregel": RR("Of bedrijven in één pand voor de parkeerverordening als één bedrijf tellen, beoordeel je eerst aan de hand van hoe zij zich in het maatschappelijk verkeer presenteren; pas daarna kijk je of een juridische constructie ze in wezen tot één bedrijf maakt.", [33], "om eerst te bezien of de vergunninghouders zich in het maatschappelijk verkeer presenteren als één bedrijf", "eigen oordeel"),
 "lessen_voor_gemeente": [
  Z("De rechter vond niet genoeg dat de praktijken op hetzelfde adres zitten en samen een coöperatie hebben: eigen cliënten, ruimtes en apparatuur en een gescheiden bedrijfsvoering telden zwaarder.", [34], "deze praktijken hebben elk hun eigen cliënten en eigen, gescheiden bedrijfsvoering"),
 ],
 "verwijst_naar": ["ECLI:NL:RVS:2016:1740", "ECLI:NL:RVS:2016:1002", "ECLI:NL:RVS:2016:999", "ECLI:NL:RVS:2016:1739"],
 "zekerheid": "hoog",
 "uitkomst_type": "inhoud",
 "uitkomst_toelichting": "Intrekking herroepen; tandartsen in een pand presenteren zich niet als één bedrijf.",
 "wetsartikelen": ["art. 1 Parkeerverordening 2013 Amsterdam"],
 "argumenten": [],
 "steunt": "parkeerder",
}

R["ECLI_NL_RVS_2017_2451"] = {
 "ecli": "ECLI:NL:RVS:2017:2451", "relevant": True,
 "onderwerp": "parkeerverbod", "sub": "verkeersbesluit", "sub2": None,
 "gemeente": "Utrecht", "uitkomst": "gelijk gemeente",
 "titel": "Geen parkeerverbod tegenover eigen oprit in Utrecht",
 "kern": Z("De rechter vond dat Utrecht het verzoek om een parkeerverbod tegenover een oprit redelijk kon afwijzen, omdat de belangen van de weg en de bereikbaarheid voor bezoekers zwaarder wogen.", [48], "in redelijkheid de in artikel 2 van de Wvw 1994 genoemde belangen zwaarder kunnen laten wegen"),
 "samenvatting": [
  Z("In een straat in Utrecht geldt aan de ene kant een parkeerverbod, waardoor auto's tegenover de oprit van een bewoonster staan; zij vroeg om een parkeerverbod tegenover haar oprit.", [19], "het college verzocht om een parkeerverbod in te stellen tegenover haar oprit"),
  Z("Zij vond dat ze slecht kan in- en uitrijden en dat het ook onveilig is.", [24, 25], "zij wordt beperkt in het af- en aanrijden van en naar haar oprit"),
  Z("De gemeente vond een parkeerverbod slecht voor de bruikbaarheid van de weg en vreesde dat andere buurtbewoners hetzelfde zouden vragen.", [20], "zou over bijna de gehele weg een parkeerverbod gaan gelden"),
  Z("De Raad van State zei dat de rechter alleen toetst of de uitleg van de gemeente redelijk is en of de belangenafweging niet onevenredig is, ook als de gemeente een verkeersbesluit weigert.", [46, 47], "zodanig onevenredig is dat het college niet in redelijkheid tot zijn besluit heeft kunnen komen"),
  Z("De bewoonster moet enige hinder dulden: het uitrijden is moeilijker, maar niet onmogelijk.", [49], "wellicht moeilijker is geworden om van haar oprit gebruik te maken"),
  Z("Het hoger beroep is ongegrond: de weigering blijft staan en er komt geen proceskostenveroordeling.", [53, 54], "Het hoger beroep is ongegrond. De aangevallen uitspraak dient te worden bevestigd"),
 ],
 "rechtsregel": RR("Bij het nemen of weigeren van een verkeersbesluit heeft de gemeente beoordelingsruimte; de rechter toetst alleen of de uitleg van begrippen als veiligheid, bruikbaarheid en vrijheid van het verkeer redelijk is en of de belangenafweging niet onevenredig is.", [46, 47], "aan het college bij het nemen van een verkeersbesluit beoordelingsruimte toekomt bij de uitleg van de begrippen", "eigen oordeel"),
 "lessen_voor_gemeente": [
  Z("De rechter vond het redelijk dat de gemeente rekening hield met precedentwerking: meer verboden betekent minder parkeerplekken en slechtere bereikbaarheid voor bezoekers.", [48], "door de precedentwerking die van het parkeerverbod uitgaat door de afname van het aantal parkeerplekken"),
  Z("Het aanbod van de gemeente voor een wit kruis op het wegdek, dat juridisch niet bindend is, maakte de weigering niet onredelijk.", [48], "ondanks dat het wel bereid was een wit kruis op de weg te schilderen"),
 ],
 "verwijst_naar": [], "zekerheid": "hoog",
 "uitkomst_type": "inhoud",
 "uitkomst_toelichting": "Weigering parkeerverbod tegenover oprit blijft staan; gemeente woog bruikbaarheid van de weg zwaarder.",
 "wetsartikelen": ["art. 2 Wvw 1994", "art. 15 Wvw 1994", "art. 21 Besluit administratieve bepalingen inzake het wegverkeer"],
 "argumenten": [A("belangenafweging-verkeersbesluit", "verworpen", [48], "in redelijkheid de in artikel 2 van de Wvw 1994 genoemde belangen zwaarder kunnen laten wegen")],
 "steunt": "gemeente",
}

R["ECLI_NL_RVS_2018_2360"] = {
 "ecli": "ECLI:NL:RVS:2018:2360", "relevant": True,
 "onderwerp": "parkeerverbod", "sub": "verkeersbesluit", "sub2": None,
 "gemeente": None, "uitkomst": "gelijk gemeente",
 "titel": "Waterschap hoeft parkeerverbod-uitspraak voorlopig niet uit te voeren",
 "kern": Z("De voorzieningenrechter schortte de uitvoering van de rechtbankuitspraak voorlopig op, omdat er twijfel is of die in hoger beroep standhoudt en een parkeerverbod onomkeerbare kosten kan geven.", [23], "voldoende aanleiding voor twijfel of de aangevallen uitspraak in stand zal blijven"),
 "samenvatting": [
  Z("Het waterschap wees het verzoek van een bewoner om een parkeerverbod bij zijn perceel in Klaaswaal af.", [12], "het verzoek van [wederpartij] om een parkeerverbod in te stellen ter hoogte van het perceel"),
  Z("De rechtbank vernietigde dat besluit en gaf het waterschap zes weken voor een nieuw besluit.", [14], "bepaald dat het college binnen 6 weken na verzending van de uitspraak een nieuw besluit neemt"),
  Z("Het waterschap ging in hoger beroep en vroeg om uitstel: op deze wegen kan verkeer in één richting passeren en een parkeerverbod zou de buurman kostbare aanpassingen kunnen kosten.", [21], "gelet op de aard van de wegen van de Hoeksche Waard de verkeersdoorstroming afdoende is gewaarborgd"),
  Z("De voorzieningenrechter zei dat rechterlijke uitspraken in principe worden uitgevoerd, maar zag hier genoeg twijfel en onomkeerbare financiële gevolgen.", [23], "Uitgangspunt is dat rechterlijke uitspraken moeten worden uitgevoerd"),
  Z("Ook is een verkeersbesluit niet binnen zes weken te nemen als de uniforme openbare voorbereidingsprocedure moet worden gevolgd.", [23], "uitvoering van de rechterlijke uitspraak niet mogelijk is binnen de gestelde termijn van zes weken"),
  Z("Tot het hoger beroep is beslist hoeft het waterschap de uitspraak van de rechtbank niet uit te voeren.", [28], "geen gevolg hoeft te geven aan de uitspraak van de rechtbank Rotterdam van 15 maart 2018"),
 ],
 "rechtsregel": RR("Rechterlijke uitspraken worden in beginsel uitgevoerd; alleen dat een heroverweging kan leiden tot een besluit dat na hoger beroep weer moet worden ingetrokken is geen reden om dat uit te stellen, maar twijfel over de uitspraak plus onomkeerbare financiële gevolgen voor een derde kan dat wel zijn.", [23], "Uitgangspunt is dat rechterlijke uitspraken moeten worden uitgevoerd", "eigen oordeel"),
 "lessen_voor_gemeente": [
  Z("De rechter erkende dat een termijn van zes weken voor een nieuw besluit niet haalbaar is als het een verkeersbesluit met de uniforme openbare voorbereidingsprocedure moet zijn.", [23], "uitvoering van de rechterlijke uitspraak niet mogelijk is binnen de gestelde termijn van zes weken"),
 ],
 "verwijst_naar": [], "zekerheid": "middel",
 "uitkomst_type": "voorlopige voorziening",
 "uitkomst_toelichting": "Voorlopig geen uitvoering van rechtbankuitspraak; hoger beroep moet eerst beslissen.",
 "wetsartikelen": ["art. 8:81 Awb"],
 "argumenten": [A("belangenafweging-verkeersbesluit", "niet beoordeeld", [19], "heeft een voorlopig karakter en is niet bindend in de bodemprocedure")],
 "steunt": "gemeente",
}

R["ECLI_NL_RVS_2017_464"] = {
 "ecli": "ECLI:NL:RVS:2017:464", "relevant": True,
 "onderwerp": "parkeernormen", "sub": "parkeerdruk-omgeving", "sub2": "omgevingsplan",
 "gemeente": "Den Haag", "uitkomst": "gelijk gemeente",
 "titel": "Omwonenden verliezen strijd tegen parkeerterrein supermarkt",
 "kern": Z("De rechter vond dat Den Haag in redelijkheid vergunning kon geven voor het parkeerterrein met geluidwerende overkapping, omdat het woon- en leefklimaat aanvaardbaar blijft.", [47], "niettemin zich niet op het standpunt heeft kunnen stellen dat ter plaatse een aanvaardbaar woon- en leefklimaat is gegarandeerd"),
 "samenvatting": [
  Z("Supermarkt Jumbo wilde op het binnenterrein aan de Anemoonstraat in Den Haag 40 parkeerplaatsen voor klanten aanleggen, met twee overkappingen tegen geluid.", [26], "40 parkeerplaatsen worden aangelegd voor de klanten van de supermarkt"),
  Z("Omwonenden vonden de parkeerplaatsen niet nodig en vreesden overlast voor de buurt.", [35], "omdat er geen noodzaak bestaat voor het realiseren van de parkeerplaatsen"),
  Z("Ze vreesden ook verlies van uitzicht en zonlicht en meer geluidsoverlast.", [38], "Zij voeren verder aan dat zij als gevolg van het plan geluidsoverlast zullen ondervinden"),
  Z("De gemeente vond dat het woon- en leefklimaat niet onaanvaardbaar wordt aangetast en gaf de vergunning.", [41], "het bouwplan niet zal leiden tot een onaanvaardbare aantasting van het woon- en leefklimaat"),
  Z("De Raad van State vond dat uit het geluidsonderzoek blijkt dat de geluidsnormen worden gehaald, ook al komt er wat extra geluid.", [47], "het laatste onderzoek blijkt dat aan de geluidsnormen uit het Activiteitenbesluit kan worden voldaan"),
  Z("De hoger beroepen zijn ongegrond: de vergunning blijft staan en er volgt geen proceskostenveroordeling.", [59, 60], "De hoger beroepen zijn ongegrond. De uitspraken dienen te worden bevestigd, voor zover aangevallen"),
 ],
 "rechtsregel": RR("Is een project op zichzelf aanvaardbaar, dan hoeft de gemeente een vergunning pas te weigeren vanwege alternatieven (zoals minder parkeerplaatsen) als op voorhand duidelijk is dat een alternatief een gelijkwaardig resultaat geeft met aanmerkelijk minder bezwaren.", [36], "kan het bestaan van alternatieven slechts dan tot het onthouden van medewerking nopen", "eigen oordeel"),
 "lessen_voor_gemeente": [
  Z("De rechter woog mee dat het bestemmingsplan de parkeerplaatsen al toestond en die afweging dus eerder was gemaakt.", [36], "is reeds de afweging gemaakt om ter plaatse parkeervoorzieningen toe te staan"),
  Z("De rechter vond het geluidsonderzoek, aangevuld met een memo na kritiek, volledig genoeg om de geluidsgevolgen te onderbouwen.", [47], "Niet is gebleken dat het onderzoek van Antea Group onvolledig is"),
 ],
 "verwijst_naar": ["ECLI:NL:RVS:2016:780"], "zekerheid": "middel",
 "uitkomst_type": "inhoud",
 "uitkomst_toelichting": "Vergunning blijft staan; geluid, uitzicht en welstand leveren geen reden tot vernietiging.",
 "wetsartikelen": ["art. 2.12 Wabo", "art. 2.27 Wabo", "art. 6.5 Bor"],
 "argumenten": [A("belangenafweging-verkeersbesluit", "verworpen", [45], "terecht geen aanleiding gezien voor het oordeel dat het college niet in redelijkheid omgevingsvergunning heeft kunnen verlenen")],
 "steunt": "gemeente",
}

R["ECLI_NL_RVS_2018_3562"] = {
 "ecli": "ECLI:NL:RVS:2018:3562", "relevant": True,
 "onderwerp": "parkeernormen", "sub": "parkeerbeleidsregels", "sub2": "parkeernorm-toets",
 "gemeente": "Medemblik", "uitkomst": "gelijk gemeente",
 "titel": "Afronden naar één parkeerplaats bij storting parkeerfonds mag",
 "kern": Z("De rechter vond dat Medemblik € 3.500 in het parkeerfonds mocht eisen voor een tekort van 0,4 parkeerplaats, omdat de aanvrager zelf in de parkeerbehoefte moet voorzien en de verordening naar boven afrondt.", [33, 32], "dat de aanvrager één gehele parkeerplaats moet aanleggen"),
 "samenvatting": [
  Z("Een pandeigenaar in Medemblik wilde zijn bovenwoning aan vier buitenlandse werknemers verhuren.", [21], "wil de bovenwoning aan vier buitenlandse werknemers verhuren"),
  Z("Daardoor steeg de parkeereis van 1,6 naar 2,0, een tekort van 0,4 plaats, en de gemeente eiste € 3.500 in het parkeerfonds.", [22], "zal volgens het college dus een tekort ontstaan van 0,4 parkeerplaatsen"),
  Z("De eigenaar vond het afronden naar boven onredelijk en niet proportioneel.", [29], "waarbij het tekort aan parkeerplaatsen naar boven en naar gehele getallen is afgerond, onredelijk en niet proportioneel is"),
  Z("De gemeente legde uit dat de parkeereis niet wordt afgerond maar de storting wel, omdat alleen hele parkeerplaatsen kunnen worden aangelegd.", [32], "afronding verband houdt met het feit dat alleen hele parkeerplaatsen kunnen worden aangelegd"),
  Z("De Raad van State vond niet aannemelijk dat er meer wordt geheven dan nodig, want de echte aanlegkosten liggen veel hoger.", [34], "De werkelijke kosten voor de aanleg, zoals het college ook ter zitting heeft toegelicht, liggen aanmerkelijk hoger"),
  Z("De rechtbank had de zitting zonder reactie op het uitstelverzoek laten doorgaan; daarom is die uitspraak vernietigd, maar het beroep blijft ongegrond en de gemeente betaalt € 55,77 proceskosten en het griffierecht van € 250.", [27, 37, 45, 46], "de rechtbank uitspraak heeft gedaan zonder dat was voldaan aan het bepaalde in artikel 8:56"),
 ],
 "rechtsregel": RR("Een gemeente mag bij een tekort aan parkeerplaatsen van minder dan één plaats een storting voor een hele parkeerplaats vragen, als de parkeerverordening afronding naar boven voorschrijft; de storting is een bijdrage in de aanlegkosten, geen volledige kostendekking.", [33], "bij een parkeerbehoefte van 0,1 tot 1,0 het bedrag voor één gehele parkeerplaats bedraagt", "wettekst art. 7 Parkeerverordening Medemblik"),
 "lessen_voor_gemeente": [
  Z("De rechter keek naar het onderscheid in de verordening tussen de parkeereis (één decimaal) en het afronden van de storting: anders was de afrondingsbepaling overbodig.", [32], "Artikel 7, achtste lid, van de Parkeerverordening zou overbodig zijn geweest"),
  Z("De rechter woog dat bij projecten tot en met drie parkeerplaatsen slechts een bijdrage aan de werkelijke kosten wordt gevraagd.", [34], "bij een parkeeraanvraag tot en met drie parkeerplaatsen slechts een bijdrage aan de werkelijke kosten wordt gerekend"),
 ],
 "verwijst_naar": ["ECLI:NL:RVS:2018:1764"], "zekerheid": "hoog",
 "uitkomst_type": "inhoud",
 "uitkomst_toelichting": "Storting van € 3.500 blijft staan; rechtbank maakte wel een procedurefout.",
 "wetsartikelen": ["art. 8:56 Awb", "art. 2.5.30 Bouwverordening Medemblik", "art. 7 Parkeerverordening Medemblik"],
 "argumenten": [
  A("onevenredig", "verworpen", [33], "is het niet onredelijk dat de hoogte van de vergoeding in de parkeervoorziening"),
  A("hoorplicht-motivering", "gehonoreerd", [27], "niet in de gelegenheid gesteld zijn standpunt bij de rechtbank toe te lichten"),
 ],
 "steunt": "gemeente",
}

R["ECLI_NL_RVS_2018_1331"] = {
 "ecli": "ECLI:NL:RVS:2018:1331", "relevant": True,
 "onderwerp": "vergunningen", "sub": "bewonersvergunning", "sub2": "plafond-wachtlijst",
 "gemeente": "Amsterdam", "uitkomst": "gelijk burger",
 "titel": "Amsterdam mag bewonersvergunning niet intrekken vanwege plafond nul",
 "kern": Z("De rechter vond dat Amsterdam een bewonersvergunning niet mocht intrekken omdat het vergunningenplafond in het gebied nul is, want het plafond is geen vergunningvoorwaarde.", [37], "wordt het bereiken van het vergunningenplafond niet begrepen onder deze voorwaarden"),
 "samenvatting": [
  Z("Amsterdam trok per 1 maart 2016 de bewonersparkeervergunning van een bewoner in.", [12], "met ingang van 1 maart 2016 ingetrokken"),
  Z("De bewoner vond dat een maximum van nul vergunningen geen reden voor intrekking is en dat zij geen stallingsplaats heeft.", [46], "dat het maximum van nul bewonersparkeervergunningen per zelfstandige woning"),
  Z("De gemeente zei dat het adres in een gebied ligt waar het vergunningenplafond op nul staat.", [26], "in een (deel)vergunninggebied ligt waar het vergunningenplafond is vastgesteld op nul"),
  Z("De Raad van State vond dat bij een aanvraag eerst de voorwaarden worden getoetst en pas daarna het plafond, en dat die twee stappen gescheiden zijn.", [36], "Naar het oordeel van de Afdeling bestaat een duidelijk onderscheid tussen deze twee stappen"),
  Z("Ook het nieuwe besluit uit 2017 hield geen stand: de regel dat in dit gebied nul vergunningen worden verleend was onverbindend, en de gemeente maakte niet aannemelijk dat de garages bij de woning liggen.", [46, 48], "waarin staat dat het aantal te verlenen bewonersparkeervergunningen per zelfstandige woning in vergunninggebied Zuid-3.3 nul bedraagt, is onverbindend"),
  Z("Amsterdam moet binnen zes weken opnieuw beslissen en € 654,82 proceskosten betalen.", [51, 61], "het college op te dragen om binnen 6 weken na de verzending van deze uitspraak een nieuw besluit"),
 ],
 "rechtsregel": RR("Een bewonersvergunning mag niet worden ingetrokken omdat het vergunningenplafond is bereikt of op nul staat: het plafond telt alleen bij het weigeren van een aanvraag en is geen voorwaarde waaraan een bestaande vergunning moet blijven voldoen.", [37], "wordt het bereiken van het vergunningenplafond niet begrepen onder deze voorwaarden", "toepassing lijn ECLI:NL:RVS:2017:392"),
 "lessen_voor_gemeente": [
  Z("De rechter wees erop dat een onterecht verleende bewonersvergunning wel kan worden ingetrokken, als de houder wist of behoorde te weten dat de vergunning onjuist was.", [38], "kan het college in een dergelijk geval de bewonersparkeervergunning intrekken, mits de vergunninghouder wist of behoorde te weten"),
  Z("De rechter hanteerde een ruime uitleg van stallingsplaats, maar vond dat de gemeente aannemelijk moet maken dat een te huren garageplek bij of in de buurt van de woning ligt.", [48], "Het college heeft echter niet aannemelijk gemaakt dat deze parkeergarages bij of in de buurt van de woning"),
 ],
 "verwijst_naar": ["ECLI:NL:RVS:2017:392", "ECLI:NL:RVS:2016:962"], "zekerheid": "hoog",
 "uitkomst_type": "inhoud",
 "uitkomst_toelichting": "Intrekking wegens plafond nul onrechtmatig; gemeente moet opnieuw beslissen en proceskosten vergoeden.",
 "wetsartikelen": ["art. 37 Parkeerverordening 2013 Amsterdam", "art. 32 Parkeerverordening 2013 Amsterdam", "art. 9 Parkeerverordening 2013 Amsterdam", "art. 7:12 Awb", "art. 3:2 Awb"],
 "argumenten": [A("plafond-verdeling", "gehonoreerd", [37], "wordt het bereiken van het vergunningenplafond niet begrepen onder deze voorwaarden")],
 "steunt": "parkeerder",
}

R["ECLI_NL_RVS_2018_2674"] = {
 "ecli": "ECLI:NL:RVS:2018:2674", "relevant": True,
 "onderwerp": "parkeernormen", "sub": "omgevingsplan", "sub2": "parkeerdruk-omgeving",
 "gemeente": "Deventer", "uitkomst": "gelijk gemeente",
 "titel": "Nieuw parkeerterrein de Worp in Deventer mag er komen",
 "kern": Z("De rechter vond dat Deventer in redelijkheid kon aannemen dat er een bestaande behoefte aan een parkeerterrein aan de rand van de binnenstad is, onderbouwd met actuele concrete gegevens.", [40], "door middel van actuele concrete gegevens onderbouwd"),
 "samenvatting": [
  Z("Deventer stelde een bestemmingsplan vast voor een parkeerterrein op de Melksterweide met 222 vaste en ongeveer 105 incidentele parkeerplaatsen.", [18], "is ruimte voor de aanleg van 222 vaste parkeerplaatsen en ongeveer 105 incidentele parkeerplaatsen"),
  Z("Omwonenden vonden niet aangetoond dat er behoefte is, omdat er volgens de Parkeermonitor 2016 restcapaciteit in de binnenstad is.", [25], "volgens de Parkeermonitor 2016 restcapaciteit is in de binnenstad, die over de hele binnenstad verdeeld is"),
  Z("De gemeente wilde zoekverkeer voorkomen met parkeren aan de randen van de binnenstad, ook omdat het Grote Kerkhof autovrij wordt.", [27], "De raad wil zoekverkeer voorkomen en voorziet daarom in parkeergelegenheid aan de randen van de binnenstad"),
  Z("De Raad van State vond dat er in totaal genoeg capaciteit is, maar dat die scheef is verdeeld en de parkeerdruk in het zuiden van de binnenstad te hoog is.", [38], "weliswaar voldoende parkeercapaciteit bestaat, maar dat deze capaciteit scheef is verdeeld over de stad"),
  Z("Het parkeerterrein tast het beschermd stadsgezicht volgens de rechter niet te veel aan, omdat het achter de bebouwing ligt en weinig bebouwing mogelijk maakt.", [88], "De raad heeft echter doorslaggevend mogen achten dat het parkeerterrein achter de bebouwing van de Bolwerksweg is gelegen"),
  Z("Twee omwonenden op meer dan 130 meter afstand zijn niet-ontvankelijk; voor het overige is het beroep ongegrond.", [110, 20], "Het beroep is, voor zover ontvankelijk, ongegrond"),
 ],
 "rechtsregel": RR("Een parkeerterrein waarvan de behoefte niet duidelijk afhangt van één bestaande voorziening telt als andere stedelijke voorziening; dan moet de gemeente in de plantoelichting onderbouwen dat er een actuele behoefte is en in hoeverre die binnen bestaand stedelijk gebied kan worden opgevangen.", [35, 36], "het verband tussen de behoefte aan het parkeerterrein en bestaande voorzieningen echter te diffuus", "eigen oordeel"),
 "lessen_voor_gemeente": [
  Z("De rechter vond de behoefte onderbouwd doordat de gemeente concreet kon aantonen welke parkeerplaatsen verdwijnen (132 bij Grote Kerkhof en Sluiskwartier, 85 bij de Bolwerksweg).", [39], "in vervanging van de 132 parkeerplaatsen die verdwijnen door het vervallen van de parkeerplaatsen op het Grote Kerkhof"),
  Z("Omdat de gemeente ook gratis parkeerplaatsen wilde, hoefde zij niet te onderzoeken wat betaald parkeren op de Melksterweide zou doen.", [40], "Gelet hierop heeft de raad geen onderzoek hoeven verrichten naar de effecten van betaald parkeren op de Melksterweide"),
 ],
 "verwijst_naar": ["ECLI:NL:RVS:2014:2143"], "zekerheid": "hoog",
 "uitkomst_type": "inhoud",
 "uitkomst_toelichting": "Plan voor parkeerterrein blijft staan; twee verre omwonenden niet-ontvankelijk.",
 "wetsartikelen": ["art. 3.1.6 Bro", "art. 1.1.1 Bro", "art. 2.4.4 Barro", "art. 8:69a Awb", "art. 1:2 Awb"],
 "argumenten": [A("belangenafweging-verkeersbesluit", "verworpen", [88], "geen aanleiding voor het oordeel dat de raad zich niet in redelijkheid op het standpunt heeft kunnen stellen")],
 "steunt": "gemeente",
}

for name, d in R.items():
    with open(OUT + name + ".json", "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
print(len(R), "written")

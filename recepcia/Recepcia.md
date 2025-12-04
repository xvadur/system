---
created: 2025-11-16
tags:
  - biznis
  - ai
---
# Hlasový asistent 
Transkripty: 
- [[Transkript]]
- [[Audio_Cistenie_Audacity]] - Návod na čistenie audio v Audacity

Dokumentácia:
- [[Recepcia_Prompt_v2.0]] - Kompletný prompt pre Rachel
- [[Recepcia_Tools_JSON]] - JSON definície nástrojov pre function calling 
- projekt, pomocou ktoreho budeme vediet klientom poskytovat správu virtualnej recepcie, ktora pomocu umelej inteligencie bude schopna odpovedat na prichadzajuce hovory pacientov, ktory volaju do ambulancie, najcastejsie kvoli objednaniu na vysetrenie, predpisanie liekov, alebo beznu otazku, ktora nezahrna dignostiku alebo priame informacie tykajuce sa zdravotneho stavu pacienta. 
- hlasovy assitent je schopny posudit zavaznost situacie, a v pripade potreby ==pohotovo prepojit== pacienta na personal ambulancie, 
	- *ak sa jedna o otazky tykajuce sa zdravia*
		mam 3 dni horucku co mam robit?, mam v stolici krc, čo mi je?
	- *ak si pacient vyslovene vyziada kontakt s ambulanciou,* 
	  Dobrý den, dovolali ste sa do ambulancie vseobecneho lekara, ja som virtualna recepcia, ako vam možem pomoct? 
	  "chcel by som hovorit s doktorom"
	- *ak halsovy asisnent nebude schopny obsluzit poziadavku*
		pacient nevie nadiktovat spravne meno alebo mu agent nerozumie 
		pacient nechce uviesť infromacie hlasovemu agentovy kvoli sukromiu 
- #### Hlavna uloha hlasoveho asistenta
	ked pcient zavola na ambulanciu tak ako prve pocuje: 
	- uvodná veta: **Dobrý den, dovlali ste sa do ambulancie detského lekára, ja som virtualna recepcna Rachel, ako vam mozem pomoct?**
		čiže pacient, ked na to nejak zareaguje: (chcem sa objednat, chcem zmenit termin, chcem zrusit termin, chcem sa niečo spytat, chcem hovorit s lekarom), a recepcia pomocou nastrojov, moze vykonat poziadavku, alebo presmerovat hovor na ambulanciu 
	- *obsluha kalendára*: (Pozri [[Recepcia_Tools_JSON]] pre JSON definície nástrojov)
		- rezervacia: 
			- Summary: nazov udalosti - **cele meno** 
			- time_start: zaciatok udalosti - **2025-11-25T09:30:00**
			- time_end: koniec udalosti - **2025-11-25T10:00:00** (30 minutove vysetrenie)
			- Description - popis udalosti - **dovod rezervacie, telefonne cislo, datum narodenia**
		- zrušenie:
			- termin vysetrenia: **2025-11-25T09:30:00**
			- verifikacia: **cele meno**
		- zmena
			- povodny termin vysetrenia: **2025-11-25T09:30:00**
			- novy termin vysetrenia: **2025-11-14T09:00:00**
		- kontrola dostupnosti termínu
			- termin vysetrenia: **2025-11-25T09:30:00**
	- *knowledge_base*:
		- informácie z webstránky ambulancie (cenník, adresa, sluzby ambulancie)
		- informácie dostupne z intenetu 
- #### Konverzácia s asistentom
	Asistent preferuje efektivnu a dynamicku komunikaciu, nepredbieha zbytocne udalosti, v tom zmysle, ze ak pacient povie ze sa chce objednat na vysetrenie, asistent hned pristupy k procesu zbierania infroamcii pre potrebne nastroje ktore maju definovanu strukuturu, ktoru agent bude nasledovat, pri zbierani potrebnych informacii. 
	
	**Asistent sa pýta na potrebne informacie vzdy po jednom.**
	- *rezrvacia*:
		- rezervacia bude prebiehať takto: 
			- asistent vyslovy uvodnu vetu. Pacient zareaguje ze chce objednat na vysetrenie. 
			  Agent povie: "Výborne! možem vás objednať. Povedzte mi prosim kedy by ste chceli termín."
			- asistent dostane termin a pouzije nastroj `check_availability` (pozri [[Recepcia_Tools_JSON]]) aby overil dostupnost terminu ktory ziadal pacient 
				- ak je termin volny, oznam to pacientovy a pokracuj k zbieraniu dalsich informacii
				- ak termin nie je volny, slusne mu to oznam, a vypytaj si od neho nový termin, a povedz mu 3 najblizsie volné časove sloty
			- po zvoleni terminu paciantom, asistent pristupuje k zbieraniu udajov o pacientovy 
				- pre objednanie pacienta na vysetrenie potrebujes pouzit nastroj `book` (pozri [[Recepcia_Tools_JSON]]), pre ktorý potrbeujes dáta: meno a priezvisko, datum narodenia, emailovu adresu a dovod vysetrenia. 
				- 



---


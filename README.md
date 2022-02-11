# Analiza receptov

V tej projetni nalogi bomo analizirali prvih 139 receptov iz spletne strani [skinnytaste](https://www.skinnytaste.com/).

Naš cilj bo ugotoviti kako sestaviti nabolj časovno prijazen in hranilno bogat jedilnik in ali nam naša zbirka receptov to sploh omogoča.        
Vsak recept ima poleg osnovnih podatkov (ime, opis, čas priprave...) določene tudi kategorije, kulinarike in oznake (diete) v katere spada. 
Ker te med seboj niso povezane, bomo analizo naredili po kosih. Torej posebej za kategorije, kulinarike in oznake.
Določili bomo kriterij in uredili recepte, kategorije, kulinarike in oznake od najboljše do najslabše.

## Zbirka receptov 

Zbirko receptov smo sestavili iz zgornje spletne strani. HTML datoteke s podatki so shranjene v mapi _recepti_. Iz teh smo zajeli podatke za vsak recept posebej (podrobnejši opis teh podatkov je v uvodu analize. ki je v datoteki analiza_receptov.ipynb). Te smo uredili v ustrezne CSV datoteke, ki se nahajajo v mapi _obdelani-podatki_ in jih bomo uporabljali pri naši analizi.

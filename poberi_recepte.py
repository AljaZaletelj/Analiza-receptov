import orodja
import re
import requests
import os
import csv

MAPA_OSNOVNIH_STRANI = "osnovne_strani"
MAPA_Z_RECEPTI = "recepti"
URL_OSNOVNA_STRAN = "https://okusno.je/"
RECEPTI_CSV = "podatki_receptov.csv"

STEVILO_STRANI = 4
STEVILO_RECEPTOV_NA_STRANI = 20



#VPRASANJA:
#-- ponavljanje osnovne strani
#-- izlusci podatke, šumniki pri imenih

#--------------vzroci-----------------------------------------------------

IMENA_POLJ = [
    "ime_recepta",
    "kategorija",
    "cas_priprave",
    "cas_kuhanja",
#    "tezavnost",
    "sestavine",
    "kalorije",
    "ogljikovi_hidrati",
    "mascobe",
    "vlaknine",
    "beljakovine"
#   "tip_prehrane"
    ]


vzorec_recepta = re.compile(
    r'Recipe","name":"(?P<ime_recepta>.*?)","image.*?'
    r'prepTime":"PT(?P<cas_priprave>.*?)M","cookTime":"PT(?P<cas_kuhanja>.*?)M.*?'
    r',"recipeCategory":"(?P<kategorija>.*?)",.*?'
    r'NutritionInformation...calories...(?P<kalorije>.*?)...carbohydrate'
    r'Content":"(?P<ogljikovi_hidrati>.*?)",.*?"fat'
    r'Content":"(?P<mascobe>.*?)","fiber'
    r'Content":"(?P<vlaknine>.*?)","protein'
    r'Content":"(?P<beljakovine>.*?)",.*?'
    r'recipeIngredient":\[(?P<sestavine>.*?)\]..recipeInstructions',
    flags=re.DOTALL
)

vzorec_tezavnosti = re.compile(
    r'<div class="ng-tns-c143-1 border-b border-black10 difficulty difficulty-(?P<tezavnost>.) dificulty-large',
    flags=re.DOTALL)

#??
#vzorec_tipa_prehrane = re.compile(
#    r'',
#    flags=re.DOTALL)


#---------------------------------------------------------------------------------------

#pobere recepte z prve strani in jih shrani v datoteke html od 1-100

def poberi_osnovne_strani(ime_mape):
    for stran in range(1, STEVILO_STRANI + 1):
        url = URL_OSNOVNA_STRAN + f'iskanje?stran={stran}'
        datoteka = os.path.join(ime_mape, f"stran_dod_{stran}.html") 
        print(url)
        orodja.shrani_spletno_stran(url, datoteka)


# iz vsake html datoteke (1-100) pobere povezave na strani receptov

def najdi_povezave(vsebina):
    vzorec = r'star-inserted" href="/recept/(.*?)"><onl-search-item'
    regexp = re.compile(vzorec, re.DOTALL)
    return re.findall(regexp, vsebina)


def poberi_povezave_receptov_iz_osnovne_strani(mapa_s_stranmi):
    vse_povezave = []
    for i in range(1, STEVILO_STRANI + 1):
        datoteka = os.path.join(mapa_s_stranmi, f"stran_{i}.html")
        osnovna_stran =  open(datoteka, "r",  encoding="utf-8")
        vsebina = osnovna_stran.read()
        povezave = najdi_povezave(vsebina)
        #print(len(povezave))
        vse_povezave.extend(povezave)
        #print(povezave)
        osnovna_stran.close()
    print(len(vse_povezave))
    return vse_povezave


#odpre povezave receptov in jih prebere in shrani v html datoteke

def shrani_recepte(povezave, mapa_z_recepti):
    i = 1
    for povezava in povezave:
        url = URL_OSNOVNA_STRAN + f"recept/{povezava}"
        datoteka = os.path.join(mapa_z_recepti, f"recept_{i}.html")
        orodja.shrani_spletno_stran(url, datoteka)
        i += 1
    


#odpre html-je receptov in iz njih izlušči pomembne podatke

def izlusci_podatke(mapa_z_recepti):
    seznam_podatkov = []
    for i in range(1, STEVILO_STRANI * STEVILO_RECEPTOV_NA_STRANI + 1):
        datoteka = f"recept_{i}.html"
        pot = os.path.join(mapa_z_recepti, datoteka)
        vsebina = orodja.vsebina_datoteke(pot)
        vzorec = vzorec_recepta
        poskus = re.findall(vzorec, vsebina)
        print(poskus)
        najdeno = re.search(vzorec, vsebina)
        print(najdeno)
        if najdeno:
            seznam_podatkov.append(najdeno.groupdict())
    return seznam_podatkov



#izvede postopek

def poberi_recepte():
    #poberi_osnovne_strani(MAPA_OSNOVNIH_STRANI)
    #povezave = poberi_povezave_receptov_iz_osnovne_strani(MAPA_OSNOVNIH_STRANI)
    #shrani_recepte(povezave, MAPA_Z_RECEPTI)
    podatki = izlusci_podatke(MAPA_Z_RECEPTI)
    orodja.zapisi_csv(podatki, IMENA_POLJ, RECEPTI_CSV)



if __name__ == '__main__':
    poberi_recepte()
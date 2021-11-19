import orodja
import re
import requests
import os
import csv

MAPA_OSNOVNIH_STRANI = "osnovne_strani"
MAPA_Z_RECEPTI = "recepti"
URL_OSNOVNA_STRAN = "https://www.skinnytaste.com/"
RECEPTI_CSV = "podatki_receptov.csv"


STEVILO_STRANI = 50
STEVILO_RECEPTOV_NA_STRANI = 30


#--------------vzroci-----------------------------------------------------

IMENA_POLJ = [
    "ime_recepta",
    "kategorija",
    "kulinarika",
    "cas_priprave",
    "cas_kuhanja",
    "st_porcij",
 #   "sestavine",
    "kalorije",
    "ogljikovi_hidrati",
    "mascobe",
    "beljakovine",
    "opis"
    ]


vzorec_recepta = re.compile(
    r'<h2 class="wprm-recipe-name wprm-block-text-normal">(?P<ime_recepta>.*?)</h2>.*?'
    r'<span class="wprm-meta-value"><span class="wprm-recipe-details wprm-recipe-nutrition wprm-recipe-calories wprm-block-text-normal">(?P<kalorije>.*?)</span> <span class="meta-label">Cals</span></span>.*?'
    r'<span class="wprm-meta-value"><span class="wprm-recipe-details wprm-recipe-nutrition wprm-recipe-protein wprm-block-text-normal">(?P<beljakovine>.*?)</span> <span class="meta-label">Protein</span></span>.*?'
    r'<span class="wprm-meta-value"><span class="wprm-recipe-details wprm-recipe-nutrition wprm-recipe-carbohydrates wprm-block-text-normal">(?P<ogljikovi_hidrati>.*?)</span> <span class="meta-label">Carbs</span></span>.*?'
    r'<span class="wprm-meta-value"><span class="wprm-recipe-details wprm-recipe-nutrition wprm-recipe-fat wprm-block-text-normal">(.*?)</span> <span class="meta-label">Fats</span></span>.*?'
    r'recipe-prep_time-minutes">(?P<cas_priprave>.*?)</span>.*?cook_time-minutes">(?P<cas_kuhanja>.*?)</span>.*?'
    r'Adjust recipe servings">(?P<st_porcij>.*?)</span>.*?'
    r'wprm-recipe-course-label">COURSE: </span><span class="wprm-recipe-course wprm-block-text-normal">(?P<kategorija>.*?)</span></div>.*?'
    r'wprm-recipe-cuisine-label">CUISINE: </span><span class="wprm-recipe-cuisine wprm-block-text-normal">(?P<kulinarika>.*?)</span></div>.*?'
    r'recipe-summary wprm-block-text-italic"><span style="display: block;">(?P<opis>.*?)</span></div>',
    flags=re.DOTALL
)


#---------------------------------------------------------------------------------------

#pobere recepte z prve strani in jih shrani v datoteke html od 1-100

def poberi_osnovne_strani(ime_mape):
    for stran in range(1, STEVILO_STRANI + 1):
        datoteka = os.path.join(ime_mape, f"stran_{stran}.html") 
        if stran == 1:
            url = URL_OSNOVNA_STRAN + f'recipes/'
        else:
            url = URL_OSNOVNA_STRAN + f'recipes/page/{stran}/'
        print(url)
        orodja.shrani_spletno_stran(url, datoteka)


# iz vsake html datoteke (1-100) pobere povezave na strani receptov

def najdi_povezave(vsebina):
    vzorec = r'<a href="https://www.skinnytaste.com/(.*?)/" rel="bookmark" title=".*?">'
    return re.findall(vzorec, vsebina)


def poberi_povezave_receptov_iz_osnovne_strani(mapa_s_stranmi):
    vse_povezave = []
    for i in range(1, STEVILO_STRANI + 1):
        datoteka = os.path.join(mapa_s_stranmi, f"stran_{i}.html")
        osnovna_stran =  open(datoteka, "r",  encoding="utf-8")
        vsebina = osnovna_stran.read()
        povezave = najdi_povezave(vsebina)
        vse_povezave.extend(povezave)
        osnovna_stran.close()
    return vse_povezave

def slabe_povezave(povezave):
    pociscene_povezave = []
    st_dobrih = 0
    for povezava in povezave:
        if "7-day-healthy-meal" not in povezava and "meal-plan" not in povezava and "skinnytaste" not in povezava:
            pociscene_povezave.append(povezava)
            st_dobrih += 1
    return pociscene_povezave, st_dobrih

#odpre povezave receptov in jih prebere in shrani v html datoteke

def shrani_recepte(povezave, mapa_z_recepti):
    i = 1
    for povezava in povezave:
        url = URL_OSNOVNA_STRAN + f"recept/{povezava}"
        datoteka = os.path.join(mapa_z_recepti, f"recept_{i}.html")
        orodja.shrani_spletno_stran(url, datoteka)
        i += 1
    


#odpre html-je receptov in iz njih izlušči pomembne podatke

def izlusci_podatke(mapa_z_recepti, st_receptov=15):
    seznam_podatkov = []
    for i in range(1, st_receptov + 1):
        datoteka = f"recept_{i}.html"
        pot = os.path.join(mapa_z_recepti, datoteka)
        vsebina = orodja.vsebina_datoteke(pot)
        vzorec = vzorec_recepta
        poskus = re.findall(vzorec, vsebina)
        print(i)
        print(poskus)
        najdeno = re.search(vzorec, vsebina)
        #print(najdeno)
        if najdeno:
            seznam_podatkov.append(najdeno.groupdict())
    return seznam_podatkov



#izvede postopek

def poberi_recepte():
    #poberi_osnovne_strani(MAPA_OSNOVNIH_STRANI)
    vse_povezave = poberi_povezave_receptov_iz_osnovne_strani(MAPA_OSNOVNIH_STRANI)
    povezave = slabe_povezave(vse_povezave)[0]
    st_dobrih = slabe_povezave(vse_povezave)[1]
    print(st_dobrih)
    #shrani_recepte(povezave, MAPA_Z_RECEPTI)
    podatki = izlusci_podatke(MAPA_Z_RECEPTI)#, st_dobrih)
    print("konec izlusci")
    orodja.zapisi_csv(podatki, IMENA_POLJ, RECEPTI_CSV)
    print("konec csv")



if __name__ == '__main__':
    poberi_recepte()
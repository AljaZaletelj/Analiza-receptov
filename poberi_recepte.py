import orodja
import re
import requests
import os
import csv

MAPA_OSNOVNIH_STRANI = "osnovne_strani"
MAPA_Z_RECEPTI = "recepti"
URL_OSNOVNA_STRAN = "https://www.skinnytaste.com/"
RECEPTI_CSV = "podatki_receptov.csv"


STEVILO_STRANI = 1
STEVILO_RECEPTOV_NA_STRANI = 30


#--------------vzroci-----------------------------------------------------

IMENA_POLJ = [
    "id_recepta"
    "oznake",
    "ime_recepta",
    "kategorije",
    "kulinarike",
    "cas_priprave",
    "cas_kuhanja",
    "st_porcij",
    "sestavine",
    "kalorije",
    "ogljikovi_hidrati",
    "mascobe",
    "beljakovine",
    "opis"
    ]


VZOREC_OZNAKE = re.compile(
    r'<span><a href=".*?class="attachment-thumbnail size-thumbnail" alt="(?P<ime_recepta>.*?)" data-lazy.*?</noscript></a></span>',
    flags=re.DOTALL)

VZOREC_SESTAVIN = re.compile(
    r'recipeIngredient":(?P<sestavine>.*?)"recipeInstructions',
    flags=re.DOTALL)

VZOREC_RECEPTA = re.compile(
    r'<h2 class="wprm-recipe-name wprm-block-text-normal">(?P<ime_recepta>.*?)</h2>.*?'
    r'<span class="wprm-meta-value"><span class="wprm-recipe-details wprm-recipe-nutrition wprm-recipe-calories wprm-block-text-normal">(?P<kalorije>.*?)</span> <span class="meta-label">Cals</span></span>.*?'
    r'<span class="wprm-meta-value"><span class="wprm-recipe-details wprm-recipe-nutrition wprm-recipe-protein wprm-block-text-normal">(?P<beljakovine>.*?)</span> <span class="meta-label">Protein</span></span>.*?'
    r'<span class="wprm-meta-value"><span class="wprm-recipe-details wprm-recipe-nutrition wprm-recipe-carbohydrates wprm-block-text-normal">(?P<ogljikovi_hidrati>.*?)</span> <span class="meta-label">Carbs</span></span>.*?'
    r'<span class="wprm-meta-value"><span class="wprm-recipe-details wprm-recipe-nutrition wprm-recipe-fat wprm-block-text-normal">(?P<mascobe>.*?)</span> <span class="meta-label">Fats</span></span>.*?'
    r'recipe-prep_time-minutes">(?P<cas_priprave>.*?)</span>.*?cook_time-minutes">(?P<cas_kuhanja>.*?)</span>.*?'
    r'Adjust recipe servings">(?P<st_porcij>.*?)</span>.*?'
    r'wprm-recipe-course-label">COURSE: </span><span class="wprm-recipe-course wprm-block-text-normal">(?P<kategorije>.*?)</span></div>.*?'
    r'wprm-recipe-cuisine-label">CUISINE: </span><span class="wprm-recipe-cuisine wprm-block-text-normal">(?P<kulinarike>.*?)</span></div>.*?'
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


def prva_polovica_seznama(seznam):
    n = len(seznam) // 2
    return seznam[:n]

#odpre html-je receptov in iz njih izlušči pomembne podatke


#def podatki_recepta(vsebina_html_recepta):
#    podatki_recepta = re.search(VZOREC_RECEPTA, vsebina_html_recepta)
#    if podatki_recepta:
#        recept = podatki_recepta.groupdict()
#        recept["id_recepta"] = int(i)
#        recept["oznake"] = prva_polovica_seznama(VZOREC_OZNAKE.findall(vsebina_html_recepta))
#        recept["kategorije"] = recept["kategorije"].strip().split(", ")
#        recept["kulinarike"] = recept["kulinarike"].strip().split(", ")
#        recept["cas_priprave"] = int(recept["cas_priprave"]) 
#        recept["cas_kuhanja"] = int(recept["cas_kuhanja"])
#        recept["st_porcij"] = int(recept["st_porcij"])
#        recept["sestavine"] = VZOREC_SESTAVIN.findall(vsebina_html_recepta)
#        recept["kalorije"] = float(recept["kalorije"])
#        recept["ogljikovi_hidrati"] = float(recept["ogljikovi_hidrati"])
#        recept["mascobe"] = float(recept["mascobe"])
#        recept["beljakovine"] = float(recept["beljakovine"])
#    return recept
#
#
#def podatki_receptov(mapa_z_recepti, st_receptov=15):
#    seznam_podatkov = []
#    for i in range(1, st_receptov + 1):
#        datoteka = f"recept_{i}.html"
#        pot = os.path.join(mapa_z_recepti, datoteka)
#        if os.path.exists(pot):
#            vsebina = orodja.vsebina_datoteke(pot)
#            print(i)
#            podatki_recepta = re.search(VZOREC_RECEPTA, vsebina)
#            if podatki_recepta:
#                recept = podatki_recepta(vsebina)
#                print(recept)
#                seznam_podatkov.append(recept)
#    return seznam_podatkov

def podatki_receptov(mapa_z_recepti, st_receptov=15):
    seznam_podatkov = []
    for i in range(1, st_receptov + 1):
        datoteka = f"recept_{i}.html"
        pot = os.path.join(mapa_z_recepti, datoteka)
        if os.path.exists(pot):
            vsebina = orodja.vsebina_datoteke(pot)
            print(i)
            podatki_recepta = re.search(VZOREC_RECEPTA, vsebina)
            if podatki_recepta:
                recept = podatki_recepta.groupdict()
                recept["id_recepta"] = int(i)
                recept["oznake"] = prva_polovica_seznama(VZOREC_OZNAKE.findall(vsebina))
                recept["kategorije"] = recept["kategorije"].strip().split(", ")
                recept["kulinarike"] = recept["kulinarike"].strip().split(", ")
                recept["cas_priprave"] = int(recept["cas_priprave"]) 
                recept["cas_kuhanja"] = int(recept["cas_kuhanja"])
                recept["st_porcij"] = int(recept["st_porcij"])
                recept["sestavine"] = VZOREC_SESTAVIN.findall(vsebina)
                recept["kalorije"] = float(recept["kalorije"])
                recept["ogljikovi_hidrati"] = float(recept["ogljikovi_hidrati"])
                recept["mascobe"] = float(recept["mascobe"])
                recept["beljakovine"] = float(recept["beljakovine"])
                print(recept)
                seznam_podatkov.append(recept)
    return seznam_podatkov



def seznam_slovarjev_podatkov(vrsta_podatka, id_recepta, seznam_podatkov):
    seznam_slovarjev = []
    for podatek in seznam_podatkov:
        seznam_slovarjev.append(
            {
                "id_recepta" : id_recepta,
                vrsta_podatka : podatek
            }
        )
    return seznam_slovarjev



def poberi_in_zapisi_podatke():
    #poberi_osnovne_strani(MAPA_OSNOVNIH_STRANI)
    #vse_povezave = poberi_povezave_receptov_iz_osnovne_strani(MAPA_OSNOVNIH_STRANI)
    #povezave = slabe_povezave(vse_povezave)[0]
    #st_dobrih = slabe_povezave(vse_povezave)[1]
    #print(st_dobrih)
    #shrani_recepte(povezave, MAPA_Z_RECEPTI)
    recepti = podatki_receptov(MAPA_Z_RECEPTI)#, st_dobrih
    print("konec podatkov")

    vsi_recepti, vse_oznake, vse_kategorije, vse_kulinarike = [], [], [], []
    for recept in recepti:
        id_recepta = recept["id_recepta"]

        vsi_recepti.append(
            {
                "id_recepta" : recept["id_recepta"],
                "cas_priprave" : recept["cas_priprave"],
                "cas_kuhanja" : recept["cas_kuhanja"],
                "st_porcij" : recept["st_porcij"],
                "kalorije" : recept["kalorije"],
                "ogljikovi_hidrati" : recept["ogljikovi_hidrati"],
                "mascobe" : recept["mascobe"],
                "beljakovine" : recept["beljakovine"],
                "opis" : recept["opis"],
                "sestavine" : recept["sestavine"]
            }
        )

        vse_oznake.extend(
            seznam_slovarjev_podatkov("oznaka", id_recepta, recept["oznake"])
        )
        vse_kategorije.extend(
            seznam_slovarjev_podatkov("kategorija", id_recepta, recept["kategorije"])
        )
        vse_kulinarike.extend(
            seznam_slovarjev_podatkov("kulinarika", id_recepta, recept["kulinarike"])
        )

    print(vse_oznake)
    print(vse_kategorije)
    print(vse_kulinarike)
    print(vsi_recepti)

    orodja.zapisi_csv(
        vsi_recepti,
        ['id_recepta', 'cas_priprave', 'cas_kuhanja', 'st_porcij', 'kalorije', 'ogljikovi_hidrati', 'mascobe', 'beljakovine', 'opis', 'sestavine'], 'obdelani-podatki/recepti.csv'
    )
    orodja.zapisi_csv(vse_oznake, ['id_recepta', 'oznaka'], 'obdelani-podatki/oznake.csv')
    orodja.zapisi_csv(vse_kategorije, ['id_recepta', 'kategorija'], 'obdelani-podatki/kategorije.csv')
    orodja.zapisi_csv(vse_kulinarike, ['id_recepta', 'kulinarika'], 'obdelani-podatki/kulinarike.csv')
    print("konec csv")
    
    
    
    
    
if __name__ == '__main__':
    poberi_in_zapisi_podatke()
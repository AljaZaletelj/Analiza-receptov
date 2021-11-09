import orodja
import re
import requests
import os
import csv

MAPA_OSNOVNIH_STRANI = "osnovne_strani"
MAPA_Z_RECEPTI = "recepti"
+6 
URL_OSNOVNA_STRAN = "https://okusno.je/"

STEVILO_STRANI = 4
STEVILO_RECEPTOV_NA_STRANI = 20

#VPRASANJA:
#-- ponavljanje osnovne strani
#-- izlusci podatke, group dict
#-- izlusci podatke, utf-8 za sestavine in imena

#--------------vzroci-----------------------------------------------------

IMENA_POLJ = [
    "ime",
    "kategorija",
    "cas_priprave",
    "cas_kuhanja",
    "tezavnost",
    "sestavine",
    "hranilne_vrednosti",
    "tip_prehrane"
    ]


#VZOREC_TEZAVNOSTI = vzorec_tezavnosti

vzorec_tezavnosti = re.compile(
    r'<div class="ng-tns-c143-1 border-b border-black10 difficulty difficulty-(?P<tezavnost>.) dificulty-large',
    flags=re.DOTALL)

#VZOREC_SESTAVIN = vzorec_sestavin

vzorec_sestavin = re.compile(
    r'recipeIngredient":\[(?P<sestavine>.*?)\]..recipeInstructions',
    flags=re.DOTALL)

VZOREC_SESTAVE = re.compile(
#    vzorec_kalorij + vzorec_OH + vzorec_mascob_vlaknin__beljakovin
    r'NutritionInformation...calories...(?P<calories>.*?)...carbohydrate'
    r'Content":"(?P<ogljikovi_hidrati>.*?)",.*?"fat'
    r'Content":"(?P<mascobe>.*?)","fiber'
    r'Content":"(?P<vlaknine>.*?)","protein'
    r'Content":"(?P<beljakovine>.*?)",',
    flags=re.DOTALL
)

#vzorec_kalorij = re.compile(
#    r'NutritionInformation...calories...(?P<calories>.*?)...carb',
#    flags=re.DOTALL)
#
#vzorec_OH = re.compile(
#    r',"carbohydrateContent":"(?P<ogljikovi_hidrati>.*?)",',
#    flags=re.DOTALL)
#
#vzorec_mascob_vlaknin__beljakovin =  re.compile(
#    r',"fatContent":"(?P<mascobe>.*?)","fiberContent":"(?P<vlaknine>.*?)","proteinContent":"(?P<beljakovine>.*?)",',
#    flags=re.DOTALL)


VZOREC_RECEPTA = re.compile(
    #vzorec_imena + vzorec_casa + vzorec_kategorije
    r'Recipe","name":"(?P<ime_recepta>.*?)","image.*?'
    r'prepTime":"PT(?P<cas_priprave>.*?)M","cookTime":"PT(?P<cas_kuhanja>.*?)M.*?'
    r',"recipeCategory":"(?P<kategorija>.*?)",',
    flags=re.DOTALL)

#vzorec_imena = r'Recipe","name":"(?P<ime_recepta>.*?)","image'
#
#vzorec_casa = re.compile(
#    r'prepTime":"PT(?P<cas_priprave>.*?)M","cookTime":"PT(?P<cas_kuhanja>.*?)M',
#    flags=re.DOTALL)
#
#vzorec_kategorije = re.compile(
#    r',"recipeCategory":"(?P<kategorija>.*?)",',
#    flags=re.DOTALL
#    )



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
        vzorec = VZOREC_SESTAVE
        poskus = re.findall(vzorec, vsebina)
        print(poskus)
        najdeno = re.search(vzorec, vsebina)
        print(najdeno)
        print("kkk")
        if najdeno:
            seznam_podatkov.append(najdeno.groupdict())
    
    return seznam_podatkov



#izvede postopek

def poberi_recepte():
    poberi_osnovne_strani(MAPA_OSNOVNIH_STRANI)
    #povezave = poberi_povezave_receptov_iz_osnovne_strani(MAPA_OSNOVNIH_STRANI)
    #shrani_recepte(povezave, MAPA_Z_RECEPTI)
    podatki = izlusci_podatke(MAPA_Z_RECEPTI)

    #orodja.zapisi_csv(podatki, IMENA_POLJ, ime_datoteke)



if __name__ == '__main__':
    poberi_recepte()


#-------------------------------vaje--------------------------------------------------------


################################################################################
## Najprej definirajmo nekaj pomožnih orodij za pridobivanje podatkov s spleta.
################################################################################
#
## definirajte URL glavne strani bolhe za oglase z mačkami
#url_osnovna_stran = 'https://okusno.je/iskanje'
## mapa, v katero bomo shranili podatke
#mapa_receptov = 'podatki_receptov'
## ime datoteke v katero bomo shranili glavno stran
#html_receptov = 'recepti.html'
## ime CSV datoteke v katero bomo shranili podatke
#csv_receptov = "recepti.csv"


def download_url_to_string(url):
    """Funkcija kot argument sprejme niz in poskusi vrniti vsebino te spletne
    strani kot niz. V primeru, da med izvajanje pride do napake vrne None.
    """
    try:
        # del kode, ki morda sproži napako
        page_content = requests.get(url)
    except requests.exceptions.ConnectionError:
        # koda, ki se izvede pri napaki
        # dovolj je če izpišemo opozorilo in prekinemo izvajanje funkcije
        print("Verjetno nimas internetne povezave!")
        return None
    # nadaljujemo s kodo če ni prišlo do napake
    return page_content.text

def save_string_to_file(text, directory, filename):
    """Funkcija zapiše vrednost parametra "text" v novo ustvarjeno datoteko
    locirano v "directory"/"filename", ali povozi obstoječo. V primeru, da je
    niz "directory" prazen datoteko ustvari v trenutni mapi.
    """
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8') as file_out:
        file_out.write(text)
    return None


# Definirajte funkcijo, ki prenese glavno stran in jo shrani v datoteko.


def save_frontpage(page, directory, filename):
    """Funkcija shrani vsebino spletne strani na naslovu "page" v datoteko
    "directory"/"filename"."""
    raise NotImplementedError()


###############################################################################
# Po pridobitvi podatkov jih želimo obdelati.
###############################################################################


def read_file_to_string(directory, filename):
    """Funkcija vrne celotno vsebino datoteke "directory"/"filename" kot niz."""
    with open(os.path.join(directory, filename), encoding="utf-8") as input_file:
        return input_file.read()



# Definirajte funkcijo, ki sprejme niz, ki predstavlja vsebino spletne strani,
# in ga razdeli na dele, kjer vsak del predstavlja en oglas. To storite s
# pomočjo regularnih izrazov, ki označujejo začetek in konec posameznega
# oglasa. Funkcija naj vrne seznam nizov.


def page_to_ads(page_content):
    """Funkcija poišče posamezne oglase, ki se nahajajo v spletni strani in
    vrne seznam oglasov."""
    pattern = r'<li class="EntityList-item(.*?)</article>'
    regexp = re.compile(pattern, re.DOTALL)
    return re.findall(regexp, page_content)

# Definirajte funkcijo, ki sprejme niz, ki predstavlja oglas, in izlušči
# podatke o imenu, lokaciji, datumu objave in ceni v oglasu.


def get_dict_from_ad_block(block):
    """Funkcija iz niza za posamezen oglasni blok izlušči podatke o imenu, ceni
    in opisu ter vrne slovar, ki vsebuje ustrezne podatke."""
    pattern = (
            r'<a .*?>(?P<title>.*?)</a></h3>c'
            r'.*pubdate="pubdate">(?P<datum>.*?)</time>'
            )
    regexp = re.compile(pattern, re.DOTALL)
    najdeno = re.search(regexp, block)
    if najdeno:
        return najdeno.groupdict()
    return None
#
#
# Definirajte funkcijo, ki sprejme ime in lokacijo datoteke, ki vsebuje
# besedilo spletne strani, in vrne seznam slovarjev, ki vsebujejo podatke o
# vseh oglasih strani.


def ads_from_file(filename, directory):
    """Funkcija prebere podatke v datoteki "directory"/"filename" in jih
    pretvori (razčleni) v pripadajoč seznam slovarjev za vsak oglas posebej."""
    raise NotImplementedError()


###############################################################################
# Obdelane podatke želimo sedaj shraniti.
###############################################################################


def write_csv(fieldnames, rows, directory, filename):
    """
    Funkcija v csv datoteko podano s parametroma "directory"/"filename" zapiše
    vrednosti v parametru "rows" pripadajoče ključem podanim v "fieldnames"
    """
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return


# Definirajte funkcijo, ki sprejme neprazen seznam slovarjev, ki predstavljajo
# podatke iz oglasa mačke, in zapiše vse podatke v csv datoteko. Imena za
# stolpce [fieldnames] pridobite iz slovarjev.


def write_cat_ads_to_csv(ads, directory, filename):
    """Funkcija vse podatke iz parametra "ads" zapiše v csv datoteko podano s
    parametroma "directory"/"filename". Funkcija predpostavi, da so ključi vseh
    slovarjev parametra ads enaki in je seznam ads neprazen."""
    # Stavek assert preveri da zahteva velja
    # Če drži se program normalno izvaja, drugače pa sproži napako
    # Prednost je v tem, da ga lahko pod določenimi pogoji izklopimo v
    # produkcijskem okolju
    assert ads and (all(j.keys() == ads[0].keys() for j in ads))
    raise NotImplementedError()


# Celoten program poženemo v glavni funkciji

def main(redownload=True, reparse=True):
    """Funkcija izvede celoten del pridobivanja podatkov:
    1. Oglase prenese iz bolhe
    2. Lokalno html datoteko pretvori v lepšo predstavitev podatkov
    3. Podatke shrani v csv datoteko
    """
    # Najprej v lokalno datoteko shranimo glavno stran

    #da bo hitreje zakomentiram med razvojem
    #spletna_stran = download_url_to_string(url_osnovna_stran)
    #save_string_to_file(spletna_stran, mapa_receptov, html_receptov)

    # Iz lokalne (html) datoteke preberemo podatke
    #vsebina = read_file_to_string(cat_directory, frontpage_filename)

    # Podatke preberemo v lepšo obliko (seznam slovarjev)
    #seznam_reklam = page_to_ads(vsebina)

    seznam_podatkov = [
    #    get_dict_from_ad_block(oglas) for oglas in seznam_reklam
    ]

    # Podatke shranimo v csv datoteko

    #write_csv(kategorije_podatkov, seznam_podatkov, cat_directory, csv_filename)

    # Dodatno: S pomočjo parametrov funkcije main omogoči nadzor, ali se
    # celotna spletna stran ob vsakem zagon prenese (četudi že obstaja)
    # in enako za pretvorbo



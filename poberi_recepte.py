import orodja
import re
import requests

STEVILO_STRANI = 100
#STEVILO_RECEPTOV_NA_STRANI = 20

vzorec = (
    r'<a href="/title/tt'
    r'(?P<id>\d{7})'  # ID ima sedem števk
    r'/.*?"\n>'  # neka šara vmes med id-jem in naslovom
    r'(?P<naslov>.*?)'  # zajamemo naslov
    r'</a>'
    r'\s+'
    r'<span class="lister-item-year text-muted unbold">'
    r'(\([IVXLCDM]+\) )?'
    r'\((?P<leto>.*?)\)'
)

najdeni_recepti = 0

for stran in range(1, STEVILO_STRANI):
    url = f'https://okusno.je/iskanje?stran={stran}'
    datoteka = f'recepti/{stran}.html' 
    orodja.shrani_spletno_stran(url, datoteka)
    vsebina = orodja.vsebina_datoteke(datoteka)
#
#    for zadetek in re.finditer(vzorec, vsebina):
#        # print(zadetek.groupdict())
#        najdeni_recepti += 1
#
#print(najdeni_recepti)
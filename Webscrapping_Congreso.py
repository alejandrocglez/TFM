import urllib.request
from bs4 import BeautifulSoup
import requests
import os, ssl
import re
import codecs

def getSpeech(url):
  # Realizamos la petición a la web
  req = requests.get(url)
  statusCode = req.status_code
  # Pasamos el contenido HTML de la web a un objeto BeautifulSoup()
  html = BeautifulSoup(req.text, "html.parser")
  html = str(html.find_all('div',{'class':'texto_completo'}))
  return str(html)

def clean_rest_html(raw_html):
  cleanhtml = re.compile('<.*?>')
  cleanrest = re.compile('[\[\]]')
  cleantext = re.sub(cleanrest, '', raw_html)
  cleantext = re.sub(cleanhtml, '', cleantext)
  return cleantext

"""i = 1
END = 57 # 28-04-2020

while i<=END:
  URL = 'http://www.congreso.es/portal/page/portal/Congreso/PopUpCGI?CMD=VERLST&BASE=pu14&FMT=PUWTXDTS.fmt&DOCS=1-1&QUERY=%28DSCD-14-CO-' + str(i) + '.CODI.%29#'
  texto = getSpeech(URL)
  texto = clean_rest_html(texto)
  f = codecs.open('Intervenciones_Congreso/Comision'+ str(i) +'.txt', 'w', encoding="utf8")
  for w in texto:
       f.write(w)
  f.close()
  i= i+1"""
i = 2
END = 18 # 29-04-2020
while i<=END:
  URL2_1 = 'http://www.congreso.es/portal/page/portal/Congreso/PopUpCGI?CMD=VERLST&BASE=pu14&FMT=PUWTXDTS.fmt&DOCS=1-1&QUERY=%28DSCD-14-PL-1-C1.CODI.%29#'
  URL2_i = 'http://www.congreso.es/portal/page/portal/Congreso/PopUpCGI?CMD=VERLST&BASE=pu14&FMT=PUWTXDTS.fmt&DOCS=1-1&QUERY=%28DSCD-14-PL-' + str(i) + '.CODI.%29#'
  URL2_19 = 'http://www.congreso.es/portal/page/portal/Congreso/PopUpCGI?CMD=VERLST&BASE=pu14&FMT=PUWTXDTS.fmt&DOCS=1-1&QUERY=%28DSCD-14-PL-19-C1.CODI.%29#'
  texto = getSpeech(URL2_i)
  texto = clean_rest_html(texto)
  f = codecs.open('Intervenciones_Congreso/Pleno_' + str(i) + '.txt', 'w', encoding="utf8")
  for w in texto:
    f.write(w)
  f.close()
  i = i + 1
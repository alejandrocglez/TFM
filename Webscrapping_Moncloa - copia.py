import urllib.request
from bs4 import BeautifulSoup
import requests
import os, ssl
import re


def cleanPresentation(raw_html):
  cleanr = re.compile('<strong>.*?</strong>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext
# [INI_FUNCION] Coge la URL y devuelve el texto que nos interesa
def getSpeech(url):
  # Realizamos la petición a la web
  req = requests.get(url)
  statusCode = req.status_code

  # Pasamos el contenido HTML de la web a un objeto BeautifulSoup()
  html = BeautifulSoup(req.text, "html.parser")
# [FIN_FUNCION] Coge la URL y devuelve el texto que nos interesa

# [INI FUNCIONES] Funciones que nos dejan unicamente el texto de los presidentes
# [FIN FUNCIONES] Funciones que nos dejan unicamente el texto de los presidentes
urlPrueba =' https://www.lamoncloa.gob.es/presidente/intervenciones/Paginas/index.aspx?mts=201901'
# [INICIO] OBTENCION DE LOS TODOS LOS LINKS EXTERNOS FORMATO MES/AÑO
months = ['00','02','03','04','05','06','07','08','09','10','11','12']
years = ['2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020']
all_links = [] # variable que almacena todos los links de todos los textos
for actual_year in years:
  for actual_month in months:
    url = 'https://www.lamoncloa.gob.es/presidente/intervenciones/Paginas/index.aspx?mts=' + actual_year + actual_month

    # Realizamos la petición a la web
    req = requests.get(url)
    statusCode = req.status_code

    # Pasamos el contenido HTML de la web a un objeto BeautifulSoup()
    html = BeautifulSoup(req.text, "html.parser")

    # Obtenemos todos los divs donde estan las entradas
    links = str(html.find_all('div',{'class':'content-adcanced-new'}))

    # [INICIO] OBTENCION DE LOS LINKS QUE HAY DENTRO DE MES/AÑO --> DIA/MES/AÑO

    ini_pos_link = links.find('/presidente/intervenciones/Paginas/')
    final_pos_link = links.find('aspx"')+4
    links_list = [] #aqui vamos a guardar los links de los txt qu ehay por pagina mes/año
    while ini_pos_link != -1:
      #print(links[links.find('/presidente/intervenciones/Paginas/'):ini_pos_link+final_pos_link])
      link_actual = 'https://www.lamoncloa.gob.es' + links[links.find('/presidente/intervenciones/Paginas/'):final_pos_link]
      links_list.append(link_actual)
      links = links.replace(link_actual,'.')
      ini_pos_link = links.find('/presidente/intervenciones/Paginas/')
      final_pos_link = links.find('aspx"')+4
      print(link_actual)
    print(links_list)
    # [FIN] OBTENCION DE LOS LINKS QUE HAY DENTRO DE MES/AÑO --> DIA/MES/AÑO
    all_links.extend(links_list)

# Generamos el fichero de salida recorriendo cada pagina del texto
f = open('Webscrapping.txt', 'w')
for w in all_links:
  f.write(w)
  f.write('\n')
f.close()

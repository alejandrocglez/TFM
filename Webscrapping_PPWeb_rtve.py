import urllib.request
from bs4 import BeautifulSoup
import requests
import os, ssl
import re
import codecs

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
  texto = html.find_all('meta',{'name':'description'})
  if texto == []: # Se hace una distincion ya que la clase varia en algunos textos
    texto = html.find_all('div',{'class':'column-content colum-content-news two-colum'})
  return texto
# [FIN_FUNCION] Coge la URL y devuelve el texto que nos interesa
def getLinks(url):
  # Realizamos la petición a la web
  req = requests.get(url)
  statusCode = req.status_code

  # Pasamos el contenido HTML de la web a un objeto BeautifulSoup()
  html = BeautifulSoup(req.text, "html.parser")
  texto = html.find_all('div',{'class':'txtBox'})
  if texto == []: # Se hace una distincion ya que la clase varia en algunos textos
    texto = html.find_all('div',{'class':'column-content colum-content-news two-colum'})
  return texto
# [INI FUNCIONES] Funciones que nos dejan unicamente el texto de los presidentes
def getHref(txt): # Borra las etiquetas que molestan para coger los dialogos
  href_pattern = re.compile("(?:(href=\".*?\"))")
  txt = re.findall(href_pattern,txt)
  txt = str(txt).replace('href=\"','\n')
  txt = txt.replace('"\', \'', '')
  txt = txt.replace('"\']', '')
  print(txt)
  txt = txt.split('\n')
  txt.remove(txt[0])
  return txt

def clean_rest_html(raw_html): # borra los restos de html inutiles que s ehan quedado al final del procesamiento
  cleanhtml = re.compile('<.*?>')
  cleanrest = re.compile('[\[\]]')
  cleantext = re.sub(cleanrest, '', raw_html)
  cleantext = re.sub(cleanhtml, '', cleantext)
  return cleantext

# Se queda unicamente con el texto entrecomillado y limpio
def clean_metas(txt):
  txt = txt.replace('[<meta content=\'','')
  txt = txt.replace('\' name="description"/>]', '')
  return txt
def clean_q_marks(raw_html):
  w_q_marks= re.compile("(?:'.*?')|(?:\".*?\")|(?:\“.*?\”)")
  cleantext = re.findall(w_q_marks, raw_html)
  cleantext = str(cleantext).replace('\'"','')
  cleantext = str(cleantext).replace('"\'', '')
  cleantext = str(cleantext).replace('”\'','')
  cleantext = str(cleantext).replace('\'“', '')
  cleantext = str(cleantext).replace(', ', '\n')
  cleantext = str(cleantext).replace('[', '')
  cleantext = str(cleantext).replace(']', '')

  return cleantext
## Fin Se queda unicamente con el texto entrecomillado
URL = 'https://www.rtve.es/temas/pablo-casado/118770/'
i = 1
while i<=53:
  URL = 'https://www.rtve.es/temas/pablo-casado/118770/' + str(i)
  links = getLinks(URL)
  links = str(links)
  links = getHref(links)
  print(i)
  j = 1
  for actual_link in links:
    if actual_link.find('/casado') != -1: # Esto es para no tener en cuenta los articulos que no son del tipo Casado dice:
      text = getSpeech(actual_link)
      text = str(text)
      text = clean_metas(text)
      print(text)
      text = clean_q_marks(text)
      f = codecs.open('PP_literales/Casado_' + str(i) + '_' + str(j) + '.txt', 'w', encoding="utf8")
      for w in text:
        f.write(w)
      f.close()
      j = j +1
  i = i+1
"""
#---------------------------------------
URL = 'https://www.rtve.es/alacarta/videos/noticias-24-horas/casado-nuestro-pacto-estado-ya-hemos-hecho-apoyando-prorroga-del-estado-alarma/5560787/'

#------------------------------------------------------------
"""


# [FIN TRATAMIENTO DE TEXTO] Tendremos un txt generado con el texto a futuro para entrenar
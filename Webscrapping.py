import urllib.request
from bs4 import BeautifulSoup
import requests
import re
import TextFunctions as tfunc
import os, ssl
def cleanhtml(raw_html):
  strongs = re.compile('</*strong>')
  spans = re.compile('</*span.*?>')
  clas = re.compile('((class=)?(".+?"))')

  cleantext = re.sub(strongs, '', raw_html)
  cleantext = re.sub(spans, '', cleantext)
  cleantext = re.sub(clas, '', cleantext)
  return cleantext

def clean_rest_html(raw_html):
  cleanhtml = re.compile('<.*?>')
  cleanrest = re.compile('[\[\]]')
  cleantext = re.sub(cleanrest, '', raw_html)
  cleantext = re.sub(cleanhtml, '', cleantext)
  return cleantext


def deleteNoPresident(mod_html): # borra las personas que intervienen y no son el presidente
  pos_final = mod_html.find('.-')
  if pos_final == -1:
    return mod_html

  pos_ini = mod_html.find('<p>')

  while pos_ini != -1:
    pos_final = mod_html.find('.-')
    pos_borrado = mod_html.find('</p>')
    speaker = mod_html[pos_ini+3:pos_final]
    if speaker != 'Presidente':
      paragraph = mod_html[pos_ini+3:pos_borrado]

      mod_html = mod_html.replace(paragraph, '')
    else:
      mod_html = mod_html.replace('Presidente.-', '\n', 1)

    mod_html = mod_html.replace('<p>', '',1)
    mod_html = mod_html.replace('</p>', '',1)
    pos_ini = mod_html.find('<p>')
  return mod_html

def deleteNoPresident_doubledots(mod_html):
  pos_final = mod_html.find(':')
  if pos_final == -1:
    mod_html = deleteNoPresident_doubledots(mod_html)
    return mod_html

  pos_ini = mod_html.find('<p>')

  while pos_ini != -1:
    pos_final = mod_html.find(':')
    pos_borrado = mod_html.find('</p>')
    speaker = mod_html[pos_ini + 3:pos_final]
    if speaker != 'Presidente':
      paragraph = mod_html[pos_ini + 3:pos_borrado]
      if paragraph.find(':') != -1:
        mod_html = mod_html.replace(paragraph, '')
    else:
      mod_html = mod_html.replace('Presidente:', '\n', 1)

    mod_html = mod_html.replace('<p>', '', 1)
    mod_html = mod_html.replace('</p>', '', 1)
    pos_ini = mod_html.find('<p>')
  return mod_html

def cleanPresentation(raw_html):
  cleanr = re.compile('<strong>.*?</strong>')
  cleantext = re.sub(cleanr, '', raw_html)
  cleantext = cleantext
  return cleantext

# [INI_FUNCION] Coge la URL y devuelve el texto que nos interesa
def getSpeech(url):
  # Realizamos la petición a la web
  req = requests.get(url)
  statusCode = req.status_code

  # Pasamos el contenido HTML de la web a un objeto BeautifulSoup()
  html = BeautifulSoup(req.text, "html.parser")
  texto = html.find_all('div',{'class':'column-content colum-content-news'})
  if texto == []:
    texto = html.find_all('div',{'class':'column-content colum-content-news two-colum'})

  return texto

# [FIN_FUNCION] Coge la URL y devuelve el texto que nos interesa
entradas=getSpeech('https://www.lamoncloa.gob.es/presidente/intervenciones/Paginas/2020/prsp12042020.aspx')
#entradas = getSpeech('https://www.lamoncloa.gob.es/presidente/intervenciones/Paginas/2004/p2207040.aspx')
entradas = str(entradas)
entradas = cleanhtml(entradas).replace("<p >", "<p>")
entradas = deleteNoPresident(entradas)
entradas = clean_rest_html(entradas)

# Generamos el fichero de salida recorriendo cada pagina del texto
i = 0
vacio = ''
while i<=50:
  f = open('Intervenciones_Congreso/' + str(i) + 'congreso.txt', 'w')
  for aaa in entradas:
      f.write(aaa)
  f.close()
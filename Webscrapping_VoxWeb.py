import urllib.request
from bs4 import BeautifulSoup
import requests
import os, ssl
import re
import codecs

# [INI_FUNCION] Coge la URL y devuelve el texto que nos interesa
def getSpeech(url):
  texto = ['-1', 'none']
  # Realizamos la petición a la web
  req = requests.get(url)
  statusCode = req.status_code
  # Pasamos el contenido HTML de la web a un objeto BeautifulSoup()
  html = BeautifulSoup(req.text, "html.parser")
  html = str(html.find_all('div',{'class':"article-content"}))
  return html

def getLinks(url):
  texto = ['-1', 'none']
  print('Estoy cogiendo links')
  # Realizamos la petición a la web
  req = requests.get(url)
  statusCode = req.status_code
  # Pasamos el contenido HTML de la web a un objeto BeautifulSoup()
  html = BeautifulSoup(req.text, "html.parser")
  print(html)
  html = html.find_all('div',{'class':"post-thumbnail flex-column"})
  print(html)
  return html

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

def clean_rest_html(raw_html):
  cleanhtml = re.compile('<.*?>')
  cleanrest = re.compile('[\[\]]')
  cleantext = re.sub(cleanrest, '', raw_html)
  cleantext = re.sub(cleanhtml, '', cleantext)
  return cleantext

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
# [FIN_FUNCION] Coge la URL y devuelve el texto que nos interesa

URL = 'https://www.rtve.es/temas/pablo-casado/118770/'
i = 8 # pagina por donde empieza a recorrer, ir adelantando viendo donde capa la seguridad de la web
while i<=30:
  URL = 'https://www.voxespana.es/page/'+ str(i) +'?s=santiago+abascal'
  links = getLinks(URL)
  links = str(links)
  links = getHref(links)
  print(i)
  j = 1
  for actual_link in links:
      txt = str(getSpeech(actual_link))
      txt = clean_rest_html(txt)
      txt = clean_q_marks(txt)
      f = codecs.open('Vox_literales/' + str(i) + '_' + str(j)+ '_Abascal_web.txt', 'w', encoding="utf8")
      for aaa in txt:
        f.write(aaa)
      f.close()
      j = j+1
  i = i+1

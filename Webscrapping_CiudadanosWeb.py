import urllib.request
from bs4 import BeautifulSoup
import requests
import os, ssl
import re
import codecs

# [INI_FUNCION] Coge la URL y devuelve el texto que nos interesa
def getSpeech(url, option):
  texto = ['-1', 'none']
  # Realizamos la petición a la web
  req = requests.get(url)
  statusCode = req.status_code
  # Pasamos el contenido HTML de la web a un objeto BeautifulSoup()
  html = BeautifulSoup(req.text, "html.parser")
  title = str(html.find_all('h2'))
  title= title.lower()
  if title.find('arrimadas') !=-1 or title.find('rivera') !=-1:
    if title.find('arrimadas') != -1:
      texto = [str(html.find_all('h4')), 'Arrimadas']
    else:
      texto = [str(html.find_all('h4')), 'Rivera']
  if len(title) == 2:
    texto = ['-1', 'none']
  if option == 1:
    return texto[0]
  else:
    return texto[1]

# [FIN_FUNCION] Coge la URL y devuelve el texto que nos interesa
# borra los restos de html inutiles que se han quedado al final del procesamiento
def clean_rest_html(raw_html):
  cleanhtml = re.compile('<.*?>')
  cleanrest = re.compile('[\[\]]')
  cleantext = re.sub(cleanrest, '', raw_html)
  cleantext = re.sub(cleanhtml, '', cleantext)
  return cleantext
## borra los restos de html inutiles que se han quedado al final del procesamiento
# Se queda unicamente con el texto entrecomillado y limpio
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

i = 1
# URL con las noticias de casado
path = os.path.normpath("'Ciudadanos_literales/'")
while i <= 10000:
  URL = 'https://www.ciudadanos-cs.org/prensa/' + str(i)
  actual_txt = str(getSpeech(URL, 1))
  print(actual_txt)
  if actual_txt != '-1':
    politician = str(getSpeech(URL,2))

    txt = str(getSpeech(URL,1)).lower()
    txt = clean_rest_html(txt)

    # Generamos el fichero de salida de las noticias completas
    f = codecs.open('Ciudadanos_noticias/' + str(i) + '_' + politician + '.txt', 'w', encoding="utf8")
    for w in txt:
        f.write(w)
    f.close()

    txt = clean_q_marks(txt)

    # Generamos el fichero de salida de unicamente los comentarios literales
    f = codecs.open('Ciudadanos_literales/' + str(i) + '_' + politician + '.txt', 'w', encoding="utf8")
    for w in txt:
        f.write(w)
    f.close()
  i = i+1
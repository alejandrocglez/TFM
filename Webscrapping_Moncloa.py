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
  texto = html.find_all('div',{'class':'column-content colum-content-news'})
  if texto == []: # Se hace una distincion ya que la clase varia en algunos textos
    texto = html.find_all('div',{'class':'column-content colum-content-news two-colum'})
  return texto
# [FIN_FUNCION] Coge la URL y devuelve el texto que nos interesa

# [INI FUNCIONES] Funciones que nos dejan unicamente el texto de los presidentes
def cleanhtml(raw_html): # Borra las etiquetas que molestan para coger los dialogos
  strongs = re.compile('</*strong>')
  spans = re.compile('</*span.*?>')
  clas = re.compile('((class=)?(".+?"))')

  cleantext = re.sub(strongs, '', raw_html)
  cleantext = re.sub(spans, '', cleantext)
  cleantext = re.sub(clas, '', cleantext)
  return cleantext

def clean_rest_html(raw_html): # borra los restos de html inutiles que s ehan quedado al final del procesamiento
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

def deleteNoPresident_doubledots(mod_html): # Caso en el que los dialogos esten marcados con :
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

# [FIN FUNCIONES] Funciones que nos dejan unicamente el texto de los presidentes


# [INICIO] OBTENCION DE LOS TODOS LOS LINKS EXTERNOS FORMATO MES/AÑO
months = ['01','02','03','04','05','06','07','08','09','10','11','12']
years = ['2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020']
all_links = [] # variable que almacena todos los links de todos los textos
for actual_year in years:
  for actual_month in months:
    print('Fecha : '+ actual_month + '-' + actual_year + '\n')
    url = 'https://www.lamoncloa.gob.es/presidente/intervenciones/Paginas/index.aspx?mts=' + actual_year + actual_month

    # Realizamos la petición a la web
    req = requests.get(url)
    statusCode = req.status_code

    # Pasamos el contenido HTML de la web a un objeto BeautifulSoup()
    html = BeautifulSoup(req.text, "html.parser")

    # Obtenemos todos los divs donde estan las html_actual
    links = str(html.find_all('div',{'class':'content-adcanced-new'}))

    # [INICIO] OBTENCION DE LOS LINKS QUE HAY DENTRO DE MES/AÑO --> DIA/MES/AÑO

    ini_pos_link = links.find('/presidente/intervenciones/Paginas/')
    final_pos_link = links.find('aspx"')+4
    links_list = [] #aqui vamos a guardar los links de los txt que hay por pagina mes/año
    i = 1
    while ini_pos_link != -1:
      #print(links[links.find('/presidente/intervenciones/Paginas/'):ini_pos_link+final_pos_link])
      link_actual = links[links.find('/presidente/intervenciones/Paginas/'):final_pos_link]
      print(link_actual)
      links_list.append(link_actual)
      links = links.replace(link_actual,'.')
      ini_pos_link = links.find('/presidente/intervenciones/Paginas/')
      final_pos_link = links.find('aspx"')+4
      # [INICIO TRATAMIENTO ]Cogemos el link actual y lo exploramos, tratamos y creamos un txt de el

      # El nombre del texto dependera del presidente que estuviese en el gobierno en ese año
      # Habría que tener en cuenta tambien el hasta el mes que estuvo
      actual_president = 'Zapatero'
      if  actual_year in ['2011'] and actual_month == '12':
        actual_president = 'Rajoy'
      if actual_year in ['2012','2013','2014','2015','2016','2017',]:
          actual_president = 'Rajoy'
      if  actual_year in ['2018'] and actual_month in ['01','02','03','04','05','06']:
        actual_president = 'Rajoy'
      if actual_year in ['2019','2020']:
        actual_president = 'Sanchez'
      if actual_year in ['2018'] and actual_month in ['07','08','09','10','11','12']:
          actual_president = 'Sanchez'
      nombretexto = actual_president + str(i) + '_' + actual_month + actual_year

      html_actual = getSpeech('https://www.lamoncloa.gob.es' + link_actual)
      html_actual = str(html_actual)
      html_actual = cleanhtml(html_actual).replace("<p >", "<p>")
      html_actual = deleteNoPresident(html_actual)
      html_actual = clean_rest_html(html_actual)
      paragraphs = html_actual.split('.')
      j = 0
      for actual_p in paragraphs:
        j+=1
        f = open('Intervenciones_Moncloa/' + nombretexto + '_'+ str(j) + '.txt', 'w', encoding="utf8")
        for w in actual_p:
          f.write(w)
        f.close()
      i = i+1
      # [FIN TRATAMIENTO DE TEXTO] Tendremos un txt generado con el texto a futuro para entrenar

    print(links_list)
    # [FIN] OBTENCION DE LOS LINKS QUE HAY DENTRO DE MES/AÑO --> DIA/MES/AÑO
    all_links.extend(links_list)


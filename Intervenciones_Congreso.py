from os import listdir
import io
import codecs
from os.path import isfile, join
import matplot
import random # para el shuffle
import pandas as pd
import re

def list_files(ruta):
    return [arch for arch in listdir(ruta) if isfile(join(ruta, arch))]

def txtOf(path): #devuelve los txt a recorrer
    file_list = list_files(path)  ## lista de archivos a recorrer
    txtList = []
    for actual_file in file_list:  ## recorremos los files buscando txt
        if actual_file.find('.txt') != -1:
            txt = path + '/' + actual_file
            txtList.append(txt)
    return txtList

def clean_Pagina(text):
    text = str(text)
    rePages = re.compile('(Página [0-9]+)|(Página[0-9]+)|(página [0-9]+)|(página[0-9]+)')
    cleantext = re.sub(rePages, '', text)

    return cleantext

def initial_clean(txt, politician): # limpia el inicio del documento hasta la intervencion del politico que aplique
    first_aparition = txt.find(politician)
    txt = txt.replace(txt[0:first_aparition],'')
    return txt
def splitSpeeches(txt):
    txt = txt.split(':')
    return txt
def clean_q_marks(raw_html):
  w_q_marks= re.compile("(?:'.*?')|(?:\".*?\")|(?:\“.*?\”)")
  cleantext = re.findall(w_q_marks, raw_html)

  return cleantext

def isSpeaker(txt):
    reSpeech = re.compile('([A-Z]{2,50} +[A-Z]+)|(La señora PRESIDENTA)')
    isTheSpeech = re.findall(reSpeech, txt)
    return isTheSpeech

def cleanSpeech(speech):
    reSpeaker = re.compile('([A-Z]{2,50} +[A-Z]+)|(La señora PRESIDENTA)')
    speech = re.sub(reSpeaker,'', speech)
    speech = speech.replace('\\r\\n','')
    reTrash = re.compile("([']+)|([,]+)|([-]+)")
    speech = re.sub(reTrash,'', speech)
    speech = clean_Pagina(speech)
    speech = speech.replace('\\n', '')
    '''reP =re.compile('(\((.+)\))')'''
    '''speech = re.sub(reP, '', speech)'''
    return speech

def getSpeech(list, politician):
    speech = ''
    in_Politician = False
    for actual_text in list:
        print(in_Politician)
        print(isSpeaker(actual_text))
        if isSpeaker(actual_text) == []:
            print('1')
            if in_Politician:
                speech = speech + actual_text
        else:
            print('--')
            if politician not in str(isSpeaker(actual_text)):
                if in_Politician:
                    print('2')
                    speech = speech + actual_text
                    in_Politician = False
            else:
                print('3')
                in_Politician = True
    return speech


def getSpeechesOf(politician):
    PATH = r'Test_puro/'
    txt_list = txtOf(PATH)
    i=0
    for actual_txt in txt_list:
        with codecs.open(actual_txt, 'r', "utf8") as txt:
            texto = txt.readlines()
            texto = initial_clean(str(texto), politician)
            if texto.find(politician) != -1:
                texto = splitSpeeches(texto)
                texto = getSpeech(texto, politician)
                texto = cleanSpeech(texto)
                paragraphs = texto.split('.')
                j = 0
                for actual_p in paragraphs:
                    j+=1
                    f = codecs.open('Test/'+ politician + '_'+ str(i) + '_' + str(j) +'.txt', 'w', encoding="utf8")
                    for w in actual_p:
                        f.write(w)
                    f.close()
            i = i+1


politician_list = ['ABASCAL CONDE', 'ARRIMADAS', 'CASADO BLANCO', 'IGLESIAS TURR', 'PRESIDENTE DEL']
for actual_politician in politician_list:
    getSpeechesOf(actual_politician)











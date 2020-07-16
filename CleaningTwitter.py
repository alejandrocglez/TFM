import urllib.request
from bs4 import BeautifulSoup
import requests
import os, ssl
import re
import codecs
from os import listdir
from os.path import isfile, join

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
def getSpeechesOf(politician):
    PATH = r'Intervenciones_Congreso/'
    txt_list = txtOf(PATH)
    i=0
    for actual_txt in txt_list:
        with codecs.open(actual_txt, 'r', "utf8") as txt:
            texto = txt.readlines()

            f = codecs.open('Twitter/'+ politician + '_'+ str(i) +'.txt', 'w', encoding="utf8")
            for w in texto:
                f.write(w)
            f.close()

def cleanTweets(txt):
    reLabels = re.compile('([0-9]{18} [0-9: -]{19} Hora de verano romance <[a-zA-Z0-9_]{1,20}>)')
    clean_Tweets = re.sub(reLabels, '\n', txt)
    reMentions = re.compile('(@{1}[a-zA-Z0-9ñÑ_\-.]{1,22} {1})|(@{1}[a-zA-Z0-9ñÑ_\-.]{1,22}["”\'.,:;!?¿\\\]{1} {0,1})|(@\S+)')
    clean_Tweets = re.sub(reMentions, '', clean_Tweets)
    reHash = re.compile('(#{1}[\S]{1,50} {1})|(#{1}[\S]{1,50}["”\'.,:;!?¿\\\]{1} {0,1})')
    clean_Tweets = re.sub(reHash, '', clean_Tweets)
    reEmail = re.compile('(\S+@\S+)')
    clean_Tweets = re.sub(reEmail, '', clean_Tweets)
    reLink =  re.compile('(www.\S+.[a-z]{2,3}["”\'.,: ;!?¿\\\]{1})|(http://www.\S+["”\'…. ,:;!?¿\\\]{1})|(https://www.\S+.[a-z]{2,3}["”\'. ,:;!?¿\\\]{1})|(http://\S+\xa0["”\'…. ,:;!?¿\\\]{0,1})|(http://[a-zA-Z0-9.\\\/]+\xa0…\b)|(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)')
    clean_Tweets = re.sub(reLink, '', clean_Tweets)
    reTwPic = re.compile('pic.twitter.com\S+')
    clean_Tweets = re.sub(reTwPic, '', clean_Tweets)
    reTrash = re.compile('([/\-_"”\'.,:;\\\]+)|xa0')
    clean_Tweets = re.sub(reTrash, '', clean_Tweets)
    reJumps = re.compile('([\\r\\n]+)|(1\n)+|([…]+rn)+')
    clean_Tweets = re.sub(reJumps, '\n', clean_Tweets)
    return clean_Tweets
def txtCreator(text):
    print('Entro a crear textos')
    paragraphs = text.split('\n\n')
    i = 1
    for actual_tweet in paragraphs:
        print(actual_tweet)
        f = codecs.open('Test/Santi_ABASCAL__' + str(i) + '.txt', 'w', encoding="utf8")
        for w in str(actual_tweet):
            f.write(w)
        f.close()
        i = i+1

PATH = 'Santi_ABASCAL.txt'
PATH2 = 'Extra'

with codecs.open(PATH, 'r', "utf8") as txt:
    text = txt.read()

# Tratamiento de los tweets
clean_Tweets = cleanTweets(str(text))
txtCreator(clean_Tweets)




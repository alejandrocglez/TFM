import nltk
# abrir archivos, lecturas, escrituras
from os import listdir
import codecs
from os.path import isfile, join
from unidecode import unidecode
# fin abrir archivos, lecturas, escrituras

# tratamiento de texto nlp
from string import punctuation


from sklearn.model_selection import train_test_split

from sklearn.svm import OneClassSVM

# fin tratamiento de texto

from textblob import TextBlob as tb
from nltk.classify import PositiveNaiveBayesClassifier
import random # para el shuffle
import pandas as pd
from nltk.tokenize import word_tokenize

import pickle # para guardar el clasificador
from sklearn.feature_extraction.text import TfidfVectorizer


def list_files(ruta):
    return [arch for arch in listdir(ruta) if isfile(join(ruta, arch))]

## VARIABLES ##
ini_txt_list=[]
final_txt_list = [] #Lista donde cada miembro es el texto de cada documento
label = "" # label que define la clase de cada texto
tokens_txt_list = [] # lista donde cada miembro son los tokens de un texto
# puntuación y palabras adicionales a eliminar de tokens
prepositions =['a','ante','bajo','cabe','con','contra','de','desde','en','entre','hacia','hasta','para','por','segun','sin','so','sobre','tras']
prep_alike = ['durante','mediante','excepto','salvo','incluso','mas','menos']
adverbs = ['no','si']
articles = ['el','la','los','las','un','una','unos','unas','este','esta','estos','estas','aquel','aquella','aquellos','aquellas']
aux_verbs = ['he','has','ha','hemos','habeis','han','habia','habias','habiamos','habiais','habian']
extra_trash = ['‘','\'', '`', ' i ', 'the', 'que', 'le', 'y']
non_words = list(punctuation)
# extend añade una lista a otra
non_words.extend(map(str, range(10)))
non_words.extend(prepositions)
non_words.extend(prep_alike)
non_words.extend(adverbs)
non_words.extend(articles)
non_words.extend(aux_verbs)
non_words.extend('gracias')
non_words.extend(extra_trash)
save_nonWords = open("TF-IDF_Classifyers/non_words.pickle","wb")
pickle.dump(non_words, save_nonWords)
save_nonWords.close()
# fin tratamiento de stop_words#
## FIN VARIABLES ##

#### [INICIO] RECORREMOS LA CARPETA DEL PATH PARA BUSCAR LOS TXT Y ETIQUETARLOS
path = r'C:/Users/Alejandro Cano Glez/PycharmProjects/NLP/Todo'
file_list = list_files(path) ## lista de archivos a recorrer
for actual_file in file_list:
    if actual_file.lower().find('.txt') != -1:
        label = 'Verdadero'
        fila = [path +'/'+ actual_file, label]
        ini_txt_list.append(fila)

#### [FIN] RECORREMOS LA CARPETA DEL PATH PARA BUSCAR LOS TXT Y ETIQUETARLOS
## Lo que obtenemos es una lista de duplas del tipo [direccion txt, clase]
tdfid_vectorizer = TfidfVectorizer() # iniciamos el creador de TFIDF
# Leemos los .txt de las intervenciones
for actual_txt in ini_txt_list:
    # si no pones el encoding a utf8, da error, por que hay carácteres que no los pilla
    print(actual_txt)
    with codecs.open(actual_txt[0],'r', "utf8") as txt:
        text = txt.read()
    if (text != ''):
        # [-- NLP -- INICIO -- ] Tratamos el texto obtenido
        text = text.lower() # pasar el texto a minusculas es algo basico
        text = unidecode(text) # quitar acentos del texto
        text = word_tokenize(text)
        cleantext = ''
        for actual_token in text: # eliminamos las palabras tipicas no deseadas
            if actual_token not in non_words:
                cleantext = cleantext + ' ' + actual_token
        # [-- NLP -- FIN -- ] Tratamos el texto obtenido
        # Preparamos el texto para ser usado por el clasificador (En este caso TF-IDF)
        if cleantext != []:
            fila = [cleantext, actual_txt[1]]
            final_txt_list.append(fila) # fila final del futuro pandas, compuesto por el texto del txt + su clase

random.shuffle(final_txt_list) # 'barajamos' para evitar sesgo
featureset = final_txt_list
# Los datos serán tratados en un dataframe para convertirlos en el training y testing set
labels = ['TF-IDF', 'Class']
df_tokens = pd.DataFrame(data = featureset, columns = labels)
x_train, x_test, y_train, y_test = train_test_split(df_tokens['TF-IDF'], df_tokens['Class'], train_size=0.75)
print('Number of rows in the total set: {}'.format(df_tokens.shape[0]))
print('Number of rows in the training set: {}'.format(x_train.shape[0]))
print('Number of rows in the test set: {}'.format(x_test.shape[0]))


# Obtenemos el vectorizer
saved_nonWords = open("TF-IDF_Classifyers/TFIDFvectorizer.pickle", "rb")
TFIDFvectorizer = pickle.load(saved_nonWords)
saved_nonWords.close()
training_set = TFIDFvectorizer.transform(x_train)
testing_set = TFIDFvectorizer.transform(x_test)

svm = OneClassSVM(kernel='rbf', nu=0.5, gamma=0.000001)
svm.fit(training_set)

save_classifier = open("TF-IDF_Classifyers/OneClassSVM.pickle","wb")
pickle.dump(svm, save_classifier)
save_classifier.close()

test_predict = svm.predict(testing_set)
print(test_predict)
print(svm.predict(testing_set[5][0]))
print(svm.fit_predict(testing_set[5][0]))
print(svm.predict(testing_set[7][0]))
print(svm.fit_predict(testing_set[7][0]))
print(svm.predict(testing_set[10][0]))
print(svm.fit_predict(testing_set[10][0]))
print(svm.score_samples(testing_set[5][0]))
print(svm.score_samples(testing_set[7][0]))
print(svm.score_samples(testing_set[10][0]))
NofFN = 0
for i in test_predict:
    if i ==-1:
        NofFN+=1
print(NofFN)
print('%FN = ' + str(NofFN/8864))

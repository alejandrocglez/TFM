import nltk
# abrir archivos, lecturas, escrituras
from os import listdir
import codecs
from os.path import isfile, join
from unidecode import unidecode
# fin abrir archivos, lecturas, escrituras

# tratamiento de texto nlp
from string import punctuation

from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from imblearn.ensemble import BalancedBaggingClassifier
from sklearn.tree import DecisionTreeClassifier

# fin tratamiento de texto


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
nArrimadas = 0
nAbascal = 0
nCasado = 0
nSanchez = 0
nIglesias = 0
for actual_file in file_list:
    if actual_file.find('.txt') != -1:
            if actual_file.lower().find('abascal') != -1:
                label = 'Santiago Abascal'
                fila = [path +'/'+ actual_file, label]
                ini_txt_list.append(fila)
                nAbascal = nAbascal +1

            if actual_file.lower().find('casado') != -1:
                label = 'Pablo Casado'
                fila = [path + '/'+ actual_file, label]
                ini_txt_list.append(fila)
                nCasado += 1

            if actual_file.lower().find('iglesias') != -1:
                label = 'Pablo Iglesias'
                fila = [path + '/'+ actual_file, label]
                ini_txt_list.append(fila)
                nIglesias += 1

            if actual_file.lower().find('arrim') != -1:
                label = 'Inés Arrimadas'
                fila = [path + '/'+ actual_file, label]
                ini_txt_list.append(fila)
                nArrimadas += 1

            if actual_file.lower().find('sanchez') != -1 or actual_file.lower().find('presidente') != -1:
                label = 'Pedro Sanchez'
                fila = [path + '/'+ actual_file, label]
                ini_txt_list.append(fila)
                nSanchez += 1

#### [FIN] RECORREMOS LA CARPETA DEL PATH PARA BUSCAR LOS TXT Y ETIQUETARLOS
## Lo que obtenemos es una lista de duplas del tipo [direccion txt, clase]
print('Número de intervenciones de Pedro Sánchez: '+ str(nSanchez))
print('Número de intervenciones de Inés Arrimadas: '+ str(nArrimadas))
print('Número de intervenciones de Pablo Casado: '+ str(nCasado))
print('Número de intervenciones de Pablo Iglesias: '+ str(nIglesias))
print('Número de intervenciones de Santiago Abascal: '+ str(nAbascal))
tdfid_vectorizer = TfidfVectorizer(ngram_range=(3, 4)) # iniciamos el creador de TFIDF
# Leemos los .txt de las intervenciones
for actual_txt in ini_txt_list:
    # si no pones el encoding a utf8, da error, por que hay carácteres que no los pilla
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
print(featureset)
# Los datos serán tratados en un dataframe para convertirlos en el training y testing set
labels = ['TF-IDF', 'Class']
df_tokens = pd.DataFrame(data = featureset, columns = labels)
print(df_tokens)
x_train, x_test, y_train, y_test = train_test_split(df_tokens['TF-IDF'], df_tokens['Class'], train_size=0.75)
print('Number of rows in the total set: {}'.format(df_tokens.shape[0]))
print('Number of rows in the training set: {}'.format(x_train.shape[0]))
print('Number of rows in the test set: {}'.format(x_test.shape[0]))

# [NLTK - ini -] Empezamos a montar el clasificador Naive_Bayes de puro NLTK
TFIDFvectorizer = TfidfVectorizer()
TFIDFvectorizer.fit(x_train)
save_set = open("TF-IDF_Classifyers/TFIDFvectorizer.pickle","wb")
pickle.dump(TFIDFvectorizer, save_set)
save_set.close()
training_set = TFIDFvectorizer.transform(x_train)

testing_set = TFIDFvectorizer.transform(x_test)
save_set = open("TF-IDF_Classifyers/testing_set.pickle","wb")
pickle.dump(testing_set, save_set)
testing_set = TFIDFvectorizer.transform(x_test)
save_set = open("TF-IDF_Classifyers/testing_set_y.pickle","wb")
pickle.dump(y_test, save_set)
save_set.close()

### [INICIO] CLASIFICADORES

# [SKLEARN] Uso de algoritmo Naive-Bayes Multinomial
print('-------------------------------[Naive-Bayes]----------------------------------------')
MNB_classifier = MultinomialNB().fit(training_set, y_train)
test_predict = MNB_classifier.predict(testing_set)
#print("MultinomialNB accuracy percent:",nltk.classify.accuracy(MNB_classifier, testing_set))
# Confussion matrix, classification report and accuracy score for the last trained classifier
print('Confussion matrix:\n{}'.format(confusion_matrix(y_test, test_predict)))
print('\nClassification report:\n{}'.format(classification_report(y_test, test_predict)))
print('Accuracy score:{}'.format(accuracy_score(y_test, test_predict)))
# Guardamos el clasificador
save_classifier = open("TF-IDF_Classifyers/MNB_classifierTFIDF.pickle","wb")
pickle.dump(MNB_classifier, save_classifier)
save_classifier.close()
# FIN algoritmo Naive-Bayes Multinomial

# [SKLEARN] Algoritmo de Regresión Lineal Simple
print('-------------------------------[Logistic Regression]----------------------------------------')
LR_Classifier = LogisticRegression(C=1.0,penalty='l2',random_state=1,solver="newton-cg")
LR_Classifier.fit(training_set, y_train)
test_predict = LR_Classifier.predict(testing_set)
# Confussion matrix, classification report and accuracy score for the last trained classifier
print('Confussion matrix:\n{}'.format(confusion_matrix(y_test, test_predict)))
print('\nClassification report:\n{}'.format(classification_report(y_test, test_predict)))
print('Accuracy score:{}'.format(accuracy_score(y_test, test_predict)))
# Guardar el algoritmo
save_classifier = open("TF-IDF_Classifyers/LR_classifierTFIDF.pickle","wb")
pickle.dump(LR_Classifier, save_classifier)
save_classifier.close()

# [SKLEARN] FIN Algoritmo de Regresión Lineal

# [SKLEARN] Algoritmo de Regresión Lineal Balanceado
print('-------------------------------[Balanced Logistic Regression]----------------------------------------')
LRB_Classifier = LogisticRegression(C=1.0,penalty='l2',random_state=1,solver="newton-cg", class_weight='balanced')
LRB_Classifier.fit(training_set, y_train)
test_predict = LRB_Classifier.predict(testing_set)
# Confussion matrix, classification report and accuracy score for the last trained classifier
print('Confussion matrix:\n{}'.format(confusion_matrix(y_test, test_predict)))
print('\nClassification report:\n{}'.format(classification_report(y_test, test_predict)))
print('Accuracy score:{}'.format(accuracy_score(y_test, test_predict)))
# Guardar el algoritmo
save_classifier = open("TF-IDF_Classifyers/LRB_classifierTFIDF.pickle","wb")
pickle.dump(LRB_Classifier, save_classifier)
save_classifier.close()

# [SKLEARN] FIN Algoritmo de Regresión Lineal Balanceado

## [] Algoritmo de Ensamble de Modelos sin Balanceo (predefinido)
print('-------------------------------[Balanced Ensambled Methods]----------------------------------------')
BB_Classifier = BalancedBaggingClassifier(base_estimator=DecisionTreeClassifier(),
                                sampling_strategy='auto',
                                replacement=False,
                                random_state=0)
BB_Classifier.fit(training_set, y_train)
test_predict = BB_Classifier.predict(testing_set)
# Confussion matrix, classification report and accuracy score for the last trained classifier
print('Confussion matrix:\n{}'.format(confusion_matrix(y_test, test_predict)))
print('\nClassification report:\n{}'.format(classification_report(y_test, test_predict)))
print('Accuracy score:{}'.format(accuracy_score(y_test, test_predict)))
# Guardar el algoritmo
save_classifier = open("TF-IDF_Classifyers/BB_Classifier.pickle","wb")
pickle.dump(BB_Classifier, save_classifier)
save_classifier.close()
## [] fin Algoritmo de Ensamble de Modelos sin Balanceo (predefinido)

## [] Algoritmo de Ensamble de Modelos con Balanceo (predefinido)
print('-------------------------------[BBalanced Ensambled Methods]----------------------------------------')
BBB_Classifier = BalancedBaggingClassifier(base_estimator=DecisionTreeClassifier(class_weight='balanced'),
                                sampling_strategy='auto',
                                replacement=False,
                                random_state=0)
BBB_Classifier.fit(training_set, y_train)
test_predict = BBB_Classifier.predict(testing_set)
# Confussion matrix, classification report and accuracy score for the last trained classifier
print('Confussion matrix:\n{}'.format(confusion_matrix(y_test, test_predict)))
print('\nClassification report:\n{}'.format(classification_report(y_test, test_predict)))
print('Accuracy score:{}'.format(accuracy_score(y_test, test_predict)))
# Guardar el algoritmo
save_classifier = open("TF-IDF_Classifyers/BBB_Classifier.pickle","wb")
pickle.dump(BBB_Classifier, save_classifier)
save_classifier.close()
## [] fin Algoritmo de Ensamble de Modelos con Balanceo (predefinido)

### [FIN] CLASIFICADORES



import codecs
import pickle # para guardar el clasificador
from os import listdir
from os.path import isfile, join
import pandas as pd
import random # para el shuffle

from nltk.tokenize import word_tokenize

# Obtenemos el clasificador LRB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
from sklearn.model_selection import train_test_split
from unidecode import unidecode

def features(sentence):
    words = sentence.lower().split()
    return dict(('contains(%s)' % w, True) for w in words)
def list_files(ruta):
    return [arch for arch in listdir(ruta) if isfile(join(ruta, arch))]

classifier = open("TF-IDF_Classifyers/LRB_ClassifierTFIDF.pickle", "rb")
LRB_Classifier = pickle.load(classifier)
classifier.close()
# obtenemos el detector de fake news
classifier = open("TF-IDF_Classifyers/OneClassSVM.pickle", "rb")
OCSVN_Classifier = pickle.load(classifier)
classifier.close()

# obtenemos el detector de fake news por possitiveNaiveBayes
classifier = open("TF-IDF_Classifyers/P_NB_classifier.pickle", "rb")
PNB_Classifier = pickle.load(classifier)
classifier.close()

# Obtenemos el testing_set
set = open("TF-IDF_Classifyers/testing_set.pickle", "rb")
testing_set2 = pickle.load(set)
set.close()
# Obtenemos el y_test
set = open("TF-IDF_Classifyers/testing_set_y.pickle", "rb")
y_test2 = pickle.load(set)
set.close()

# Obtenemos el las non_words
saved_nonWords = open("TF-IDF_Classifyers/non_words.pickle", "rb")
non_words = pickle.load(saved_nonWords)
set.close()

# Obtenemos el vectorizer
saved_vect = open("TF-IDF_Classifyers/TFIDFvectorizer.pickle", "rb")
TFIDFvectorizer = pickle.load(saved_vect)
saved_vect.close()

def txtOf(path): #devuelve los txt a recorrer
    file_list = list_files(path)  ## lista de archivos a recorrer
    txtList = []
    for actual_file in file_list:  ## recorremos los files buscando txt
        if actual_file.find('.txt') != -1:
            txt = path + '/' + actual_file
            txtList.append(txt)
    return txtList

def txtToDF(file_list):
    featureset = []
    for actual_file in file_list:
        label = ''
        if actual_file.find('.txt') != -1:
            if actual_file.lower().find('abascal') != -1:
                label = 'Santiago Abascal'
            if actual_file.lower().find('casado') != -1:
                label = 'Pablo Casado'

            if actual_file.lower().find('iglesias') != -1:
                label = 'Pablo Iglesias'

            if actual_file.lower().find('arrim') != -1:
                label = 'Inés Arrimadas'

            if actual_file.lower().find('sanchez') != -1 or actual_file.lower().find('presidente') != -1:
                label = 'Pedro Sanchez'

            with codecs.open(actual_file, 'r', "utf8") as txt:
                text = txt.read()

            text = nlp(text)
            line = [text, label]
            if len(line[0]) > 15:
                featureset.append(line)
    random.shuffle(featureset)  # 'barajamos' para evitar sesgo
    df = pd.DataFrame(data = featureset, columns=['Text', 'Class'])
    print(df)
    return df

def nlp(literal):
    cleantext = ''
    if (literal != ''):
        # [-- NLP -- INICIO -- ] Tratamos el texto obtenido
        text = literal.lower()  # pasar el texto a minusculas es algo basico
        text = unidecode(text)  # quitar acentos del texto
        text = word_tokenize(text)
        for actual_token in text:  # eliminamos las palabras tipicas no deseadas
            if actual_token not in non_words:
                cleantext = cleantext + ' ' + actual_token
        # [-- NLP -- FIN -- ] Tratamos el texto obtenido
    return cleantext

df = txtToDF(txtOf('Test'))
x_test = df['Text'].tolist()
y_test = df['Class'].tolist()
testing_set = TFIDFvectorizer.transform(x_test)

test_predict = LRB_Classifier.predict(testing_set)
# Confussion matrix, classification report and accuracy score for the last trained classifier
print('Confussion matrix:\n{}'.format(confusion_matrix(y_test, test_predict)))
print('\nClassification report:\n{}'.format(classification_report(y_test, test_predict)))
print('Accuracy score:{}'.format(accuracy_score(y_test, test_predict)))

test_predict = LRB_Classifier.predict(testing_set2)
# Confussion matrix, classification report and accuracy score for the last trained classifier
print('Confussion matrix:\n{}'.format(confusion_matrix(y_test2, test_predict)))
print('\nClassification report:\n{}'.format(classification_report(y_test2, test_predict)))
print('Accuracy score:{}'.format(accuracy_score(y_test2, test_predict)))

total = 0
well_classified = 0
bad_classified = 0
for i in testing_set:
    total +=1
    result = OCSVN_Classifier.predict(i)

    if result == 1:
        well_classified +=1
    else:
        bad_classified +=1
acc = well_classified/total
print('Fake News detector accuracy: ' + str(acc))

import pickle # para guardar el clasificador
from nltk.tokenize import word_tokenize

# Obtenemos el clasificador LRB
from sklearn.feature_extraction.text import TfidfVectorizer
from unidecode import unidecode

def esFakeOCSVN(text):
    number = OCSVN_Classifier.predict(text)
    print(number)
    if number == -1:
        return False
    else:
        return True

def features(sentence):
    words = sentence.lower().split()
    return dict(('contains(%s)' % w, True) for w in words)

classifier = open("TF-IDF_Classifyers/LRB_ClassifierTFIDF.pickle", "rb")
LRB_Classifier = pickle.load(classifier)
classifier.close()
# obtenemos el detector de fake news
classifier = open("TF-IDF_Classifyers/OneClassSVM.pickle", "rb")
OCSVN_Classifier = pickle.load(classifier)
classifier.close()

"""# obtenemos el detector de fake news por possitiveNaiveBayes
classifier = open("TF-IDF_Classifyers/P_NB_classifier.pickle", "rb")
PNB_Classifier = pickle.load(classifier)
classifier.close()"""

# Obtenemos el testing_set
set = open("TF-IDF_Classifyers/testing_set.pickle", "rb")
testing_set = pickle.load(set)
set.close()

# Obtenemos el las non_words
saved_nonWords = open("TF-IDF_Classifyers/non_words.pickle", "rb")
non_words = pickle.load(saved_nonWords)
saved_nonWords.close()

# Obtenemos el vectorizer
saved_vect = open("TF-IDF_Classifyers/TFIDFvectorizer.pickle", "rb")
TFIDFvectorizer = pickle.load(saved_vect)
saved_vect.close()

print("Introduzca la frase a clasificar")
literal= input()

if (literal != ''):
    # [-- NLP -- INICIO -- ] Tratamos el texto obtenido
    text = literal.lower()  # pasar el texto a minusculas es algo basico
    text = unidecode(text)  # quitar acentos del texto
    text = word_tokenize(text)
    cleantext = ''
    aux = []
    for actual_token in text:  # eliminamos las palabras tipicas no deseadas
        if actual_token not in non_words:
            cleantext = cleantext + ' ' + actual_token
    aux.append(cleantext)

    cleantext= aux
    # [-- NLP -- FIN -- ] Tratamos el texto obtenido
    # Preparamos el texto para ser usado por el clasificador (En este caso TF-IDF)
    if cleantext != []:
        cleantext = TFIDFvectorizer.transform(cleantext)

result =LRB_Classifier.predict(cleantext)
probs = LRB_Classifier.predict_proba(cleantext)

OCSVN_prob = OCSVN_Classifier.score_samples(cleantext) * 100
OCSVN_distance = OCSVN_Classifier.decision_function(cleantext)
string_esFake = ''
if esFakeOCSVN(cleantext):
    string_esFakeOCSVN = 'Es posible que NO se trate de una fake new. Se aproxima un ' +str((1 - OCSVN_distance) *100)[1:6] + '% a ser un discurso veraz'
else:
    string_esFakeOCSVN = 'Es posible que se trate de una FAKE NEW. Se aleja un ' +str(( - OCSVN_distance) *100)[1:6] + '% de ser un discurso veraz'

print('------------------------------------------------')
print('Texto introducido: ' + "'"+ literal + "'")
print('------------------------------------------------')
print('------------------------------------------------')
print('Probabilidad de pertenencia del discurso a cada político:')

print('Inés Arrimadas: ' + "{:.2f}".format(probs[0][0]*100) + '%')
print('Pablo Casado: ' + "{:.2f}".format(probs[0][1]*100) + '%')
print('Pablo Iglesias: ' + "{:.2f}".format(probs[0][2]*100) + '%')
print('Pedro Sánchez: ' + "{:.2f}".format(probs[0][3]*100) + '%')
print('Santiago Abascal: ' + "{:.2f}".format(probs[0][4]*100) + '%')
print('------------------------------------------------')
print('Es más probable que lo haya dicho: ' + result[0])
print('------------------------------------------------')
print(string_esFakeOCSVN)
print('- -- -- -- -- - -- - --- - - - - -- -- -- -- ---')



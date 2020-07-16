from flask import Flask, render_template, request
import pickle
from nltk.tokenize import word_tokenize
from unidecode import unidecode

classifier = open("TF-IDF_Classifyers/LRB_ClassifierTFIDF.pickle", "rb")
LRB_Classifier = pickle.load(classifier)
classifier.close()
# obtenemos el detector de fake news
classifier = open("TF-IDF_Classifyers/OneClassSVM.pickle", "rb")
OCSVN_Classifier = pickle.load(classifier)
classifier.close()

# Obtenemos el las non_words
saved_nonWords = open("TF-IDF_Classifyers/non_words.pickle", "rb")
non_words = pickle.load(saved_nonWords)
saved_nonWords.close()

# Obtenemos el vectorizer
saved_vect = open("TF-IDF_Classifyers/TFIDFvectorizer.pickle", "rb")
TFIDFvectorizer = pickle.load(saved_vect)
saved_vect.close()

def esFakeOCSVN(text):
    number = OCSVN_Classifier.predict(text)
    print(number)
    if number == -1:
        return False
    else:
        return True


def speechClassify(literal):
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

        cleantext = aux
        # [-- NLP -- FIN -- ] Tratamos el texto obtenido
        # Preparamos el texto para ser usado por el clasificador (En este caso TF-IDF)
        if cleantext != []:
            cleantext = TFIDFvectorizer.transform(cleantext)

    result = LRB_Classifier.predict(cleantext)
    probs = LRB_Classifier.predict_proba(cleantext)

    OCSVN_distance = OCSVN_Classifier.decision_function(cleantext)
    if esFakeOCSVN(cleantext):
        esFake =  'Es posible que NO se trate de una fake new. Se aproxima un ' +str((1 - OCSVN_distance) *100)[1:6] + '% a ser un discurso veraz'
    else:
        esFake = 'Es posible que se trate de una FAKE NEW. Se aleja un ' +str(( - OCSVN_distance) *100)[1:6] + '% de ser un discurso veraz'
    return result, probs, esFake

app = Flask(__name__)
@app.route('/', methods=["GET", "POST"])
def formulario():
    if request.method == 'POST':
        speech = request.form.get("speech_field", None)
        if speech != None:
            result, probs, esFake = speechClassify(speech)
            probs[0][0] = str(probs[0][0] * 100)[0:5]
            probs[0][1] = str(probs[0][1] * 100)[0:5]
            probs[0][2] = str(probs[0][2] * 100)[0:5]
            probs[0][3] = str(probs[0][3] * 100)[0:5]
            probs[0][4] = str(probs[0][4] * 100)[0:5]
            return render_template('results.html', resultt= result, probs = probs, esFake = esFake, speech = speech)
    else:
        return render_template('index.html')



@app.route('/result')
def show():

    return render_template('results.html')


if __name__ == '__main__':
    app.run()
# TFM
Análisis del discurso político (España, 2016-Actualidad) mediante machine learning y procesamiento del lenguaje natural

El código corresponde al desarrollo del trabajo de fin de máster de Alejandro Cano González, estudiante del MÁSTER UNIVERSITARIO EN ANÁLISIS Y VISUALIZACIÓN DE DATOS MASIVOS 
de la UNIR.

[ ! ] El fichero "index.py" es el encargado de lanzar la aplicación web que funcionará como herramienta de clasificación del discurso político.

El fichero "UsingClassifyer.py" es el usado para generar los resultados por consola, que están plasmados en la memoria de entrega del proyecto.

El fichero "TestingClassifier.py" es el script generado para comprobar la precisión de los modelos que se comenta en la Sección 6 de la memoria.

FakeSpeechDetector se corresponde al modelo entrenado para clasificar los textos como posibles fake news o no.

TF-IDF_Method es el script que genera los modelos comentados en la memoria del proyecto, usados para la clasificación de los discursos políticos según su autoría.

El resto de scripts, en su mayoría, están orientados a la obtención del dataset (almacenado en Todo.exe) mediante técnicas de Webscraping, también se ha procedido a su limpieza,
mediante técnicas de nlp y re. Por otro lado, hay otros scripts de prueba o generación de modelos no utilizados, que se ha creído conveniente subir a este repositorio
para su futura consulta.


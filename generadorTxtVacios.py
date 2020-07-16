# Generamos el fichero de salida recorriendo cada pagina del texto
i = 0
vacio = ''
while i<=50:
  f = open('Test_puro/' + str(i)+ '_' + 'Congreso.txt', 'w')
  for aaa in vacio:
      f.write(aaa)
  f.close()
  i = i+1
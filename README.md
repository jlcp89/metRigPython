# metRigPython
Script Python para analizar marcos estructurales con el método básico de las rigideces

Debe correr el archivo met_rigidez.py con los siguiente argumentos:
sys.arvg[1] = numero de nodos de la estructura
sys.arvg[2] = numero de apoyos de la estructura
sys.arvg[3] = numero de elementos de la estructura
sys.arvg[4] = modulo de elasticidad de los miembros de la estructura en Ksi
sys.arvg[5] = inercia de la secciòn transversal en plg4
sys.arvg[6] = area de la secciòn transversal en plg2

Seguidamente debera ingresar las coordenadas de cada nodo y apoyo de la estructura.
Finalmente tendra que ingresar cada elementos, especificando su nodo cercano (N) y nodo lejano (F) y despues ingresar las cargas puntuales
a las que esta sujeta el elemento de la estructura en Kip y cargas distribuidas en Kip/ft

Despues de ingresar los elementos el script presentara los resultados del analisis estructural.


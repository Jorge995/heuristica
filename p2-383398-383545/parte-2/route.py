import sys
import copy
from time import time #importamos la funcion time para medir los tiempos

posicionInicialBus = ""
numeroMaximoPasajeros = 0
posicionColegios = []
numeroNiniosNoEntregados = 0
ninios = []
numParadas = 0
nombreHeuristica = sys.argv[2]
paradasVisitadas = 1
nodosExpandidos = 0
costeTotal = 0

class Nodo:
    def __init__(self, estado, g, h, padre):
        self.estado = estado
        self.g = g
        self.h = h
        self.f = g+h
        self.padre = padre

# Leemos el fichero de entrada por filas
f = open(sys.argv[1])
datosFichero = []
string = f.readline()
while string!="":
	datosFichero.append(string.split())
	string = f.readline()
f.close()

# Guardamos datos del bus
posicionInicialBus = datosFichero[-1][1]
numeroMaximoPasajeros = int(datosFichero[-1][2])

# Guardamos posicion de cada colegio
for i in range(len(datosFichero[-3])):
	if i%2 != 0:
		posicionColegios.append(datosFichero[-3][i][0:2])

# Guardamos el numero de paradas del problema
numParadas = len(datosFichero[0])

# Creamos la matriz de costes
costes = []
for i in range(1, numParadas+1):
  costes.append([])
  for j in range(1, numParadas+1):
    if datosFichero[i][j] != "--":
   	  datosFichero[i][j] = int(datosFichero[i][j])
    costes[i-1].append(datosFichero[i][j])
print(costes)

# Guardamos los datos de los ninios
datosNinios = " ".join(datosFichero[-2])
niniosPorParada = datosNinios.split(";")
for i in range(len(niniosPorParada)):
  niniosPorParadaSplit = niniosPorParada[i].split(":")
  print("Hola", niniosPorParadaSplit)
  niniosSeparados = niniosPorParadaSplit[1].split(",")
  for j in range(len(niniosSeparados)):
    niniosSeparadoSplit = niniosSeparados[j].split()
    numeroNinios = int(niniosSeparadoSplit[0])
    while numeroNinios!=0:
      ninios.append([niniosPorParadaSplit[0][len(niniosPorParadaSplit[0])-2:len(niniosPorParadaSplit[0])],niniosSeparadoSplit[1]])
      numeroNinios = numeroNinios-1
print(ninios)
numeroNiniosNoEntregados = len(ninios)
print(numeroNiniosNoEntregados)

# Esta funcion devuelve una lista con las acciones que podrian ejecutarse en el estado pasado por parametro
def acciones(estado):
  acciones=[]
  posicionActual = int(estado[0][0][1])
  contadorNiniosRecoger = 0
  contadorNiniosDejar = 0
  colegio = ""

  # Movimiento del bus
  for i in range(numParadas):
    if costes[posicionActual-1][i] != "--":
      acciones.append(["P"+str(i+1), costes[posicionActual-1][i]])

  # Recoger ninios
  # Primera precondicion. La posicion del bus ha de ser la misma que la de los ninios a recoger
  for i in range(len(estado[1])):
    if estado[0][0] == estado[1][i][0]:
      contadorNiniosRecoger = contadorNiniosRecoger+1
  # Segunda precondicion. Ha de haber hueco libre en el bus
  if contadorNiniosRecoger > 0 and estado[0][1] < numeroMaximoPasajeros:
    if numeroMaximoPasajeros-estado[0][1] >= contadorNiniosRecoger:
      acciones.append(["Recoger", contadorNiniosRecoger])
    else:
      acciones.append(["Recoger", numeroMaximoPasajeros-estado[0][1]])

  # Dejar ninios
  # Primera precondicion. Ha de haber un colegio en la misma posicion del bus
  for j in range(len(posicionColegios)):
	  if estado[0][0] == posicionColegios[j]:
	    colegio = "C"+str(j+1)

  # Segunda precondicion. Ha de haber al menos un ninio en el bus que vaya a dicho colegio
  if colegio != "":
	for i in range(len(estado[1])):
	  if estado[1][i][0] == "Bus" and estado[1][i][1] == colegio:
	    contadorNiniosDejar = contadorNiniosDejar + 1
  if contadorNiniosDejar > 0:
    acciones.append(["Dejar", contadorNiniosDejar])
  return acciones

# Esta funcion devuelve el estado que resulta de aplicar la accion que se pasa por parametro sobre el estado que tambien se pasa por parametro
def calcularEstadoSiguiente(estado, accion):
  listaNiniosDejar = []
  listaNiniosRecoger = []
  for i in range(len(estado[1])):
    listaNiniosRecoger.append(estado[1][i])
    listaNiniosDejar.append(estado[1][i])
  j = 0
  colegio = ""
  if accion[0] == "Recoger":
    niniosARecoger = accion[1]
    while niniosARecoger != 0:
	    if listaNiniosRecoger[j][0] == estado[0][0]:
	      listaNiniosRecoger[j][0] = "Bus"
	      niniosARecoger = niniosARecoger - 1
	    j = j+1
    nuevoEstado = ([estado[0][0],estado[0][1]+accion[1]], listaNiniosRecoger , estado[2])
  if accion[0] == "Dejar":
    niniosADejar = accion[1]
    while colegio == "":
      if estado[0][0] == posicionColegios[j]:
        colegio = "C"+str(j+1)
      j = j+1
    for i in range(len(estado[1])):
      if listaNiniosDejar[i][0] == "Bus" and listaNiniosDejar[i][1] == colegio:
        listaNiniosDejar[i][0] = "Entregado"
    nuevoEstado = ([estado[0][0], estado[0][1]-accion[1]], listaNiniosDejar, estado[2]-accion[1])
  if accion[0] != "Recoger" and accion[0] != "Dejar":
    nuevoEstado = ([accion[0], estado[0][1]], estado[1], estado[2])
  return nuevoEstado

def expandirNodo(nodo):
  nodosSucesores = []
  accionesPosibles = acciones(copy.deepcopy(nodo).estado)
  for i in range(len(accionesPosibles)):
    nuevoEstado = None
    nuevoNodo = None
    listaPocha = []
    nuevoEstado = calcularEstadoSiguiente(copy.deepcopy(nodo).estado, accionesPosibles[i])
    nuevoNodo = Nodo(([nuevoEstado[0][0], nuevoEstado[0][1]], nuevoEstado[1], nuevoEstado[2]), nodo.g + accionesPosibles[i][1], heuristica(nuevoEstado), nodo)
    nodosSucesores.append(nuevoNodo)
  return nodosSucesores

def heuristica(estado):
  if nombreHeuristica == "heuristica1":
    return estado[2]
  if nombreHeuristica == "heuristica2":
    contador = 0
    for i in range(len(estado[1])):
      if estado[1][i][0] != "Bus" and estado[1][i][0] != "Entregado":
        contador = contador + 1
    return contador + estado[2]
  else:
    return 0

def astar(nodoInicial):
  solucion = []
  listaAbierta = []
  listaCerrada = []
  global nodosExpandidos
  global costeTotal
  exito = False
  listaAbierta.append(nodoInicial)
  nodoFinal = None
  while len(listaAbierta) > 0 and exito == False:
    primerNodo = None
    while primerNodo == None and len(listaAbierta) > 0:
      if listaAbierta[0].estado not in listaCerrada:
        primerNodo = listaAbierta[0]
        listaAbierta.remove(listaAbierta[0])
      else:
        listaAbierta.remove(listaAbierta[0])
    if primerNodo.estado[0][0] == posicionInicialBus and primerNodo.estado[2] == 0:
      exito = True
      nodoFinal = primerNodo
    else:
      nodosSucesores = expandirNodo(primerNodo)
      nodosExpandidos += 1
      listaCerrada.append(primerNodo.estado)
      nodosSucesores.sort(key = lambda nodos: nodos.f, reverse = False)
      listaAbierta = nodosSucesores + listaAbierta
      listaAbierta.sort(key = lambda nodos: nodos.f, reverse = False)
  if exito == True:
    while nodoFinal.padre != None:
      solucion.append(nodoFinal)
      nodoFinal = nodoFinal.padre
    solucion.append(nodoFinal)
    costeTotal = solucion[0].g
    solucion.reverse()
    for i in range(len(solucion)):
      print(solucion[i].estado)
  else:
    solucion = None
    print("No hay solucion")
  return solucion

# Estado inicial
nodoInicial = Nodo(([posicionInicialBus, 0], ninios, numeroNiniosNoEntregados), 0, 0, None)
tiempoInicial = time()
solucion = astar(nodoInicial)
tiempoFinal = time()
tiempoEjecucion = tiempoFinal - tiempoInicial
for i in range(1, len(solucion)):
  if solucion[i].estado[0][0] != solucion[i-1].estado[0][0]:
    paradasVisitadas = paradasVisitadas + 1
file = open(sys.argv[1]+".statistics","w")
file.write("Tiempo total: "+str(tiempoEjecucion)+" s\n")
file.write("Coste total: "+str(costeTotal)+"\n")
file.write("Paradas visitadas: "+str(paradasVisitadas)+"\n")
file.write("Nodos expandidos: "+str(nodosExpandidos)+"\n")
file.close()
print(nodosExpandidos)
print(tiempoEjecucion)
print(costeTotal)
print(paradasVisitadas)

cadena = solucion[0].estado[0][0]
for i in range(1, len(solucion)):
  listaAuxiliarDejar = []
  listaAuxiliarRecoger = []
  dejar = False
  recoger = False
  for j in range(len(posicionColegios)):
    listaAuxiliarDejar.append([0, "C"+str(j+1)])
    listaAuxiliarRecoger.append([0, "C"+str(j+1)])
  if solucion[i].estado[0][0] != solucion[i-1].estado[0][0]:
    cadena = cadena + " -> "+solucion[i].estado[0][0]
  else:
    for k in range(len(solucion[i].estado[1])):
      if solucion[i].estado[1][k][0] != solucion[i-1].estado[1][k][0] and solucion[i].estado[1][k][0] == "Entregado":
        dejar = True
        listaAuxiliarDejar[int(solucion[i].estado[1][k][1][1])-1][0] += 1
      if solucion[i].estado[1][k][0] != solucion[i-1].estado[1][k][0] and solucion[i].estado[1][k][0] == "Bus":
        recoger = True
        listaAuxiliarRecoger[int(solucion[i].estado[1][k][1][1])-1][0] += 1
  if dejar == True:
    cadena = cadena+" (B: "
    for j in range(len(listaAuxiliarDejar)):
      if listaAuxiliarDejar[j][0] > 0:
        cadena = cadena + str(listaAuxiliarDejar[j][0])+" "+listaAuxiliarDejar[j][1]+", "
    cadena = cadena[0:len(cadena)-2]
    cadena = cadena + ")"
  if recoger == True:
    cadena = cadena+" (S: "
    for j in range(len(listaAuxiliarRecoger)):
      if listaAuxiliarRecoger[j][0] > 0:
        cadena = cadena + str(listaAuxiliarRecoger[j][0])+" "+listaAuxiliarRecoger[j][1]+", "
    cadena = cadena[0:len(cadena)-2]
    cadena = cadena + ")"
file2 = open(sys.argv[1]+".output","w")
f = open(sys.argv[1])
file2.write(f.read())
file2.write(cadena)
file2.close()
f.close()

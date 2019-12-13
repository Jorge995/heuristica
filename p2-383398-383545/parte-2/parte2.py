import sys

posicionInicialBus = ""
numeroMaximoPasajeros = 0
posicionColegios = []
numeroNiniosNoEntregados = 0
ninios = []
numParadas = 0
listaAbierta = []
listaCerrada = []
exito = False

class Nodo:
    def __init__(self, estado, g, h, padre):
        self.estado = estado
        self.g = g
        self.h = h
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
def acciones(estado, costes, numeroMaximoPasajeros):
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
def calcularEstadoSiguiente(estado, accion, posicionColegios):
  listaNinios = estado[1]
  j = 0
  colegio = ""
  if accion[0] == "Recoger":
    niniosARecoger = accion[1]
    while niniosARecoger != 0:
	    if listaNinios[j][0] == estado[0][0]:
	      listaNinios[j][0] = "Bus"
	      niniosARecoger = niniosARecoger - 1
	    j = j+1
    nuevoEstado = ([estado[0][0],estado[0][1]+accion[1]], listaNinios , estado[2])
  if accion[0] == "Dejar":
    niniosADejar = accion[1]
    while colegio == "":
	    if estado[0][0] == posicionColegios[j]:
	      colegio = "C"+str(j+1)
    j = j+1
    for i in range(len(estado[1])):
      if listaNinios[i][0] == "Bus" and listaNinios[i][1] == colegio:
        listaNinios[i][0] = "Entregado"
    nuevoEstado = ([estado[0][0], estado[0][1]-accion[1]], listaNinios, estado[2]-accion[1])
  else:
    nuevoEstado = ([accion[0], estado[0][1]], listaNinios, estado[2])
  return nuevoEstado

def expandirNodo(nodo, costes, numeroMaximoPasajeros, posicionColegios):
  nodosSucesores = []
  accionesPosibles = acciones(nodo.estado, costes, numeroMaximoPasajeros)
  for i in range(len(accionesPosibles)):
    nuevoEstado = calcularEstadoSiguiente(nodo.estado, accionesPosibles[i], posicionColegios)
    nuevoNodo = Nodo(nuevoEstado, nodo.g + accionesPosibles[i][1], 0, nodo)
    nodosSucesores.append(nuevoNodo)
  return nodosSucesores
  
# Estado inicial
estadoInicial = Nodo(([posicionInicialBus, 0], ninios, numeroNiniosNoEntregados), 0, 0, None)
print(estadoInicial)
nodosExpandidos = expandirNodo(estadoInicial, costes, numeroMaximoPasajeros, posicionColegios)
print(nodosExpandidos)

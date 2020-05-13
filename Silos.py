"""
la idea es que los silos estén ordenados por altura, y que a medida que se vaya superando la altura
se vayan eliminando
"""


def fun(args):
    vol = int(args[0])
    numSilos = args[1]
    silos = []
    for i in range(0, int(numSilos)):
        # primero base y luego altura
        base, altura = map(int, args[i + 2].strip().split())
        AñadirOrdenadamente(silos, (base, altura))
    contadorAltura = 1
    cantidad = 0
    while not cantidad == vol:
        for silo in range(0, len(silos)):
            if silos[silo][1] < contadorAltura:
                silos = silos[0:silo]
                break
            else:
                cantidad += silos[silo][0]
        contadorAltura += 1
    return contadorAltura-1


def AñadirOrdenadamente(lista: list, dato):
    pos = BusquedaBinaria(lista, dato[1])
    lista.insert(pos, dato)


def BusquedaBinaria(lista, buscado):
    if len(lista) == 0:
        return 0
    if buscado >= lista[0][1]:
        return 0
    elif buscado <= lista[-1][1]:
        return len(lista)
    else:
        return __rec__(lista, buscado, 0, len(lista))


def __rec__(lista, buscado, ini, fin):
    medio = (ini + fin) // 2
    vmedio = lista[medio][1]
    if vmedio == buscado:
        return medio
    elif lista[medio - 1][1] >= buscado >= vmedio:
        return medio
    elif vmedio >= buscado >= lista[medio + 1][1]:
        return medio + 1
    elif buscado > vmedio:
        return __rec__(lista, buscado, ini, medio - 1)
    elif buscado < vmedio:
        return __rec__(lista, buscado, medio + 1, fin)
    elif fin < ini:
        return -1

f = open(r"C:\Users\PC\PycharmProjects\Nonograma\casoPeorPractica2.txt","r")
l=f.readlines()

from time import time

ini=time()
print(fun(l))
print(time()-ini)
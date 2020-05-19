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
        AñadirOrdenadamente(silos, (base, altura-1))
    """
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
    return contadorAltura - 1
    """
    return BusquedaBinariaVertical(silos,vol) +1 #+1 ya que se empieza a contar en 0 pero los silos en 1

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


def BusquedaBinariaVertical(l, obj):
    if obj == 0:
        return 0
    else:
        ini=obj//sum(x[0] for x in l)
        return __recVertical__(l, obj, 0, 0, l[0][1],False,ini)


def __recVertical__(l, obj, cantidad, levelini, levelfin,tipo,startinglevel=-1):
    #Tipo es para marcar ascenso o descenso, True para descenso
    if startinglevel>0:
        level=startinglevel
    else:
        level = (levelfin + levelini) // 2
    if tipo:
        cantidad = CalcularDiferencia(l, cantidad, levelfin, level, tipo)
    else:
        cantidad = CalcularDiferencia(l, cantidad, levelini, level,tipo)

    if cantidad == obj:
        return level
    elif cantidad > obj:
        return __recVertical__(l, obj, cantidad, levelini, level-1,True)

    elif cantidad < obj:
        return __recVertical__(l, obj, cantidad, level+1, levelfin,False)
    else:
        return "no hay manera de que llegues aquí" #todo quita estp


def CalcularDiferencia(l, cantidad, levelOr, levelDst,descenso):  # O(3n)
    if descenso:
        for i in l:
            if i[1] <= levelDst:
                pass
            else:
                cantidad -= (min(i[1],levelOr+1)-levelDst)*i[0]
    else:
        #Primero se suman los valores de la fila ini
        cantidadAux=0
        for silo in range(0, len(l)):
            if l[silo][1] < levelOr:
                break
            else:
                cantidadAux += l[silo][0]
        cantidadAux*=(levelDst-levelOr+1)
        cantidad+=cantidadAux
        #Después se restan las diferencias
        for i in l:
            if i[1] >= levelDst:
                pass
            elif i[1]>=levelOr:
                cantidad -= abs(levelDst - i[1])*i[0]
    return cantidad


from time import time

w=open("casoPeorPractica2.txt","r").readlines()
ini = time()
print(fun(w))
print(time() - ini)

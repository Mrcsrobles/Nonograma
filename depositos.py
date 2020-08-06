def fun(args):
    vol = int(args[0])
    numSilos = args[1]
    silos = []
    for i in range(0, int(numSilos)):
        base, altura = map(int, args[i + 2].strip().split())
        AñadirOrdenadamente(silos, (base, altura-1))
    return BusquedaBinariaVertical(silos,vol) +1 #+1 ya que se empieza a contar en 0 pero los silos en 1

def AñadirOrdenadamente(lista: list, dato):
    #esta función permite añadir ordenadamente a la lista de mayor a menor en base a la altura de los silos
    pos = BusquedaBinaria(lista, dato[1])#Primero se busca donde se debe colocar el elemento usando busqueda binaria
    lista.insert(pos, dato)


def BusquedaBinaria(lista, buscado):
    if len(lista) == 0: #Si la longitud de la lista es 0 simplemente se añade
        return 0
    if buscado >= lista[0][1]: #Si el elemento es mayor que el primero se pone el primero
        return 0
    elif buscado <= lista[-1][1]: #Si el elemento es menor que el último se pone al final
        return len(lista)
    else:#Sino, se busca la posición
        return __rec__(lista, buscado, 0, len(lista))


def __rec__(lista, buscado, ini, fin):
    medio = (ini + fin) // 2
    vmedio = lista[medio][1] #Valor del elemento del medio
    if vmedio == buscado:
        return medio
    elif lista[medio - 1][1] >= buscado >= vmedio: #Si el buscado están entre el anterior al medio y el medio
        return medio
    elif vmedio >= buscado >= lista[medio + 1][1]: #Si el buscado está entre el siguiente al medio y el medio
        return medio + 1 #Se devuelve la siguiente posición
    elif buscado > vmedio: #Si es mayor que el medio
        return __rec__(lista, buscado, ini, medio - 1)
    elif buscado < vmedio: #Si es menor que el medio
        return __rec__(lista, buscado, medio + 1, fin)
    elif fin < ini: #En caso de que no se encuentre da -1
        return -1


def BusquedaBinariaVertical(l, obj):
    #Es una busqueda binaria basada en el volumen total a cierto nivel
    if obj == 0:
        return -1 #Se devuelve -1 ya que se suma 1 al final
    else:
        #Para acercarnos lo máximo posible al objetivo de primeras, ponemos como medio una estimación
        #En esta dividimos el volumen objetivo entre el volumen que puede tener el nivel 1
        #De esta manera obtenemos una cota superior ya que el resto de niveles solo puede ser menor o igual que el primero
        ini=obj//sum(x[0] for x in l)-1
        return __recVertical__(l, obj, 0, 0, l[0][1],False,ini)


def __recVertical__(l, obj, cantidad, levelini, levelfin,tipo,startinglevel=-1):
    if startinglevel>0:# esto se usa para la primera iteración, en la que tendremos la estimación de la primera fila
        level=startinglevel
    else:
        level = (levelfin + levelini) // 2
    if tipo:#Tipo es para marcar ascenso o descenso, True para descenso
        #Es necesario este argumento ya que dependiendo de si se asciende o se desciende se hacen operaciones distintas
        cantidad = CalcularDiferencia(l, cantidad, levelfin, level, tipo)
    else:
        cantidad = CalcularDiferencia(l, cantidad, levelini, level,tipo)

    if cantidad == obj:#Esto es ya simplemente una busqueda binaria
        return level
    elif cantidad > obj:
        return __recVertical__(l, obj, cantidad, levelini, level-1,True)

    elif cantidad < obj:
        return __recVertical__(l, obj, cantidad, level+1, levelfin,False)


def CalcularDiferencia(l, cantidad, levelOr, levelDst,descenso):
    if descenso:# si se desciende
        for i in l:
            if i[1] <= levelDst:
                pass
            else:
                cantidad -= (min(i[1],levelOr+1)-levelDst)*i[0]
                #Si se desciende solo se resta de cada depósito el máximo de este, o solo la parte llena, el mínimo de los 2
                #a esto se le resta el nivel destino para saber la diferencia entre niveles y se multiplica por el ancho
    else:#Si se asciende
        #Primero se suman los valores de la fila ini
        cantidadAux=0
        for silo in range(0, len(l)):
            if l[silo][1] < levelOr:#Al estar ordenada la lista podemos detener la iteración sin mirar todos
                break#Se detendrá si el nivel actual es mayor del depósito "silo"
            else:
                cantidadAux += l[silo][0]#Se suman los anchos
        cantidadAux*=(levelDst-levelOr+1)#Se multiplica por la altura
        cantidad+=cantidadAux#Se suma a cantidad
        #Después se restan las diferencias ya que se había asumido que todos los niveles eran iguales
        for i in l:
            if i[1] >= levelDst:
                pass
            elif i[1]>=levelOr:
                cantidad -= abs(levelDst - i[1])*i[0] # se resta la altura al nivel destino y se multiplica por el ancho
    return cantidad



args=[input(),input()]
for i in range(0,int(args[1])):#Se leen los inputs y se pasan a fun
    args.append(input())

print(fun(args))
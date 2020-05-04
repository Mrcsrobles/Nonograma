from copy import deepcopy
from pprint import pprint
from time import sleep


# F.inicio

def CrearTablero(data):
    T = []  # Para crear el tablero se ponen al principio de cada fila el número de # que va a haber
    for i in range(0, len(data["rows"])):
        T.append([])
        for j in range(0, len(data["cols"])):
            if j < data["rows"][i]:
                T[-1].append(1)
            else:
                T[-1].append(0)
    return T


def Iniciar(*args):
    r, c = map(int, args[0].strip().split())
    print(r, c)
    data = {
        "rows": list(map(int, args[1].strip().split())),
        "cols": list(map(int, args[2].strip().split()))
    }
    if len(data["rows"]) != r or len(data["cols"]) != c or any(row > c for row in data["rows"]) or any(
            col > r for col in data["cols"]):
        # Si uno de los datos es incorrecto en la entrada devuelve imposible
        return "IMPOSIBLE"
    else:  # Se crea el tablero
        T = CrearTablero(data)
        sol = __rec__(T, data, 0)  # Devuelve una tupla booleano, nonograma
        if not sol[0]:
            return "IMPOSIBLE"
        else:
            return sol[1]


# F. Factibilidad
def Factible(T, row, data):
    for col in range(0, len(T[0])):
        iniciado = False
        acabado = False
        c = 0
        for rows in range(0, row + 1):
            val = T[rows][col]
            if val == 0 and iniciado:
                acabado = True  # Si después de un uno hay un cero se da por terminado
            elif val == 1 and acabado:
                return False  # Si hay un uno después de haber acabado no es factible ya que hay un espacio
            elif val == 1 and not iniciado:
                iniciado = True  # El primer uno empiza a contar
                c += 1
            elif val == 1 and iniciado:
                c += 1  # El resto de unos suman
            if c > data["cols"][col]:
                return False  # Si hay más # de los indicados en la columna no es factible
    return True


# F. solución
def ComprobarCol(T, c, data):
    sum = 0
    iniciado = False
    acabado = False
    for i in range(0, len(T)):
        val = T[i][c]

        if val == 0 and iniciado:
            acabado = True
        elif val == 1 and acabado:
            return False
        elif val == 1:
            sum += val
            iniciado = True

    return sum == data["cols"][c]


def Comprobar(T, data):
    return all(ComprobarCol(T, c, data) for c in range(0, len(data["cols"])))


# Funcion de movimiento

def Desplazar(T, row, data):
    try:
        ini = T[row].index(1)  # Se saca la posición del primer 1
        fin = ini + data["rows"][row]
        if fin < len(T[row]):
            T[row][ini] = 0
            T[row][fin] = 1
            return True
        else:
            return False
    except ValueError: # si no hay 1 siempre va a ser desplazable
        return True


def __rec__(T, data, row):
    t = deepcopy(T)
    if row == 4:
        print("")
    if row == len(t) - 1:
        desplazable = True
        sol = False
        while desplazable and not sol:
            sol = Comprobar(t, data)  # Si se ha llegado a la última fila y no ha funcionado es False
            if sol:
                aux = Convertir(t)
                return (sol, aux)
            else:
                desplazable = Desplazar(t, row, data)

        return (sol, [])
    else:
        avanzable = True
        solucionado = False

        while avanzable and not solucionado:
            if Factible(t, row,data):
                result = __rec__(t, data, row + 1)
                if result[0]:  # Se comprueba la siguiente fila
                    return (True, result[1])
                else:
                    avanzable = Desplazar(t, row, data)# Si los inferiores no dan solución se avanza la actual
            else:
                for i in range(1, len(T)-row):
                    avanzable = Desplazar(t, row+i, data)
                    if not avanzable:
                            break
        return (solucionado, [])


def Convertir(T):
    for i in range(0, len(T)):
        print("")
        for j in range(0, len(T[i])):
            if T[i][j] == 1:
                T[i][j] = "#"
            else:
                T[i][j] = "-"
        T[i] = ["".join(T[i])]
    return T


from time import time

tini = time()
pprint(Iniciar("5 5", "1 3 5 3 1",
                                 "1 3 5 3 1"))
print(time() - tini)

from copy import deepcopy
from pprint import pprint
from time import sleep

# F.inicio
def Iniciar(*args):
    r, c = map(int, args[0].strip().split())
    print(r,c)
    data = {
        "rows": list(map(int, args[1].strip().split())),
        "cols": list(map(int, args[2].strip().split()))
    }
    if len(data["rows"]) != r or len(data["cols"]) != c or any(row > c for row in data["rows"]) or any(
            col > r for col in data["cols"]):
        #Si uno de los datos es incorrecto en la entrada devuelve imposible
        return "IMPOSIBLE"
    else:
        T = []
        for i in range(0, len(data["rows"])):
            T.append([])
            for j in range(0, len(data["cols"])):
                if j < data["rows"][i]:
                    T[-1].append(1)
                else:
                    T[-1].append(0)
        aux = __rec__(T, data, 0)
        if not aux[0]:
            return "IMPOSIBLE"
        else:
            return aux[1]


# F. Factibilidad
def Factible(T, row):
    for col in range(0, len(T[0])):
        iniciado = False
        acabado = False
        for rows in range(0, row + 1):
            val = T[rows][col]
            if val == 0 and iniciado:
                acabado = True
            elif val == 1 and acabado:
                return False
            elif val == 1:
                iniciado = True
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
    except:
        return False


def __rec__(T, data, row):
    t = deepcopy(T)
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
            if Factible(t, row):
                result = __rec__(t, data, row + 1)
                if result[0]:  # Se comprueba la siguiente fila
                    return (True, result[1])
                else:
                    avanzable = Desplazar(t, row, data)
            else:
                avanzable = Desplazar(t, row, data)
                for i in range(1, len(T)):
                    Desplazar(t, row + i, data)

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
pprint(Iniciar("10 5", "1 2 2 2 2 2 1 1 2 1", "1 8 5 1 1"))
print(time() - tini)

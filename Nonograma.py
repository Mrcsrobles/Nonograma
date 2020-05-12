from pprint import pprint


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


def ReiniciarTablero(data, rowini=0, T=[]):
    for i in range(rowini, len(data["rows"])):
        T[i] = []
        for j in range(0, len(data["cols"])):

            if j < data["rows"][i]:
                T[i].append(1)
            else:
                T[i].append(0)
    return T


def SacarColRows(rc,rows, cols):  # esta función se usa para optimizar el código, ya que dependiendo de
    # si cómo estén ordenadas las filas y las columnas puede tardar 0s o tardar demasiado
    r, c = map(int,rc.strip().split())
    print(r,c)
    rows = list(map(int, rows.strip().split()))
    cols = list(map(int, cols.strip().split()))
    data = {}
    data["permutaciones"] = [False, False, False]
    data["r"]=r
    data["c"]=c
    # cambiar cols, cambiar rows
    if len(rows)>0 and len(cols)>0:
        if sum(cols[:len(cols) // 2]) < sum(cols[len(cols) // 2:]):
            cols.reverse()
            data["permutaciones"][0] = True
        if sum(rows[:len(rows) // 2]) < sum(rows[len(rows) // 2:]):
            rows.reverse()
            data["permutaciones"][1] = True
    data["rows"] = rows
    data["cols"] = cols
    return data


def Iniciar(*args):
    data = SacarColRows(args[0],args[1], args[2])
    if len(data["rows"]) != data["r"] or len(data["cols"]) != data["c"] or any(row > data["c"] for row in data["rows"]) or any(
            col > data["r"] for col in data["cols"]):
        # Si uno de los datos es incorrecto en la entrada devuelve imposible
        return "IMPOSIBLE"
    else:  # Se crea el tablero
        T = CrearTablero(data)
        sol = __rec__(T, data, 0)  # Devuelve una tupla booleano, nonograma
        if not sol:
            return "IMPOSIBLE"
        else:
            return Convertir(T, data)


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

def Desplazar(T, row, data, SeVaAmover=0):
    try:
        ini = T[row].index(1)  # Se saca la posición del primer 1
        fin = ini + data["rows"][row]
        if fin < len(T[row]):
            T[row][ini] = 0
            T[row][fin] = 1
            return True
        else:
            return False
    except ValueError:  # si no hay 1 dependiendo de la situación lo consideraremos desplazable o no
        if SeVaAmover == 1:
            return False
        else:
            return True


def __rec__(T, data, row):
    if row == len(T) - 1:
        try:
            T[row].index(1)
            d = True
            while not Comprobar(T, data) and d:
                d = Desplazar(T, row, data)
                if not d:
                    return False
            else:
                return True
        except ValueError:
            return Comprobar(T, data)  # En el caso de que la última fila sea 0 todos será un caso especial
    else:
        d = True

        while d:
            if Factible(T, row, data):
                if __rec__(T, data, row + 1):
                    return True
                else:
                    ReiniciarTablero(data, row + 1, T)  # Se reinician las filas inferiores
                    d = Desplazar(T, row, data, SeVaAmover=1)
            else:
                for i in range(row, len(T)):
                    d = Desplazar(T, i, data)
                    if not d:
                        break
        return False


def Convertir(T, data):
    # Esta parte se usa para la optimización

    if data["permutaciones"][0]:
        for i in range(0, len(T)):
            T[i].reverse()
    if data["permutaciones"][1]:
        T.reverse()

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
pprint(Iniciar("20 20 ", "0 0 1 1 1 3 15 9 5 5 3 3 3 3 3 1 1 1 1 0 ",
                                 "0 0 1 1 1 2 2 4 10 17 10 4 2 2 1 1 1 0 0 0 "))
print(time() - tini)

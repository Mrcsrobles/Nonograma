from pprint import pprint


# F.inicio
def CrearTablero(data):
    T = []  # Para crear el tablero se ponen al principio de cada fila el número de # que va a haber en una matriz
    for i in range(0, len(data["rows"])):
        T.append([])
        for j in range(0, len(data["cols"])):
            if j < data["rows"][i]:
                T[-1].append(1)
            else:
                T[-1].append(0)
    return T


def ReiniciarTablero(data, T, rowini=0):  # Para volver atrás se recoloca la fila en el inicio desde la fila indicada
    if T is None:
        T = []
    for i in range(rowini, len(data["rows"])):  # Por cada fila
        T[i] = []  # Se vacía la lista
        for j in range(0, len(data["cols"])):  # Por cada columna se rellena con 1 hasta el número de # que va a haber
            if j < data["rows"][i]:
                T[i].append(1)
            else:
                T[i].append(0)
    return T


def SacarColRows(rc, rows, cols):  # esta función se usa para optimizar el código, ya que dependiendo de
    # cómo estén ordenadas las filas y las columnas puede tardar 0s o tardar demasiado
    r, c = map(int, rc.strip().split())  # se divide la entrada
    rows = list(map(int, rows.strip().split()))
    cols = list(map(int, cols.strip().split()))
    data = {}  # Todos los datos se almacenarán en un diccionario que se arrastrará por todos los métodos
    data["permutaciones"] = [False,
                             False]  # Este campo sirve para optimizar la colocación, indica cambios en (cols,rows)
    data["r"] = r  # Se almacena el número de filas
    data["c"] = c  # Se almacena el número de columnas
    if len(rows) > 5 and len(
            cols) > 5:  # Se pone un caso base para el cual empieza a ser rentable hacer la reordenación
        if sum(cols[:len(cols) // 2]) < sum(cols[len(cols) // 2:]):  # Si la suma de la segunda mitad de las columnas
            # es mayor que la primera mitad
            cols.reverse()  # Se le da la vuelta a las columnas
            data["permutaciones"][0] = True  # se almacena que se ha hecho este cambio(se deshace en Converir)
        if sum(rows[:len(rows) // 2]) < sum(rows[len(rows) // 2:]):  # igual que con las columnas
            rows.reverse()
            data["permutaciones"][1] = True
    data["rows"] = rows  # Se almacenan los tamaños de las filas
    data["cols"] = cols  # Se almacenan los tamaños de las columnas
    return data


def Iniciar(*args):
    data = SacarColRows(args[0], args[1], args[2])
    if len(data["rows"]) != data["r"] or len(data["cols"]) != data["c"] or any(row > data["c"] for row in data["rows"]) or any(col > data["r"] for col in data["cols"]) or sum(data["cols"]) != sum(data["rows"]):
        # Si uno de los datos es incorrecto en la entrada devuelve imposible, comprueba
        # 1 Los tamaños de filas y columnas son correctos
        # 2 Si alguna fila o columna es más grande que el tablero
        # 3 Si el número total de filas y columnas no encaja
        return "IMPOSIBLE"
    else:
        T = CrearTablero(data)  # Se crea el tablero
        sol = __rec__(T, data, 0)  # empieza en la fila 0 y devuelve bool
        if not sol:  # si es falso es que no tiene solución
            return "IMPOSIBLE"
        else:  # sino, se muestra por pantalla la colocación
            return Convertir(T, data)


# F. Factibilidad
def Factible(T, row, data):
    # Esta función dirá si la fila es factible para seguir o no
    try:
        pIni = T[row].index(
            1)  # lo primero es ver si hay algún 1, si no lo hay quiere decir que es factible ya que las filas anteriores lo eran y no se ha añadido nada
        iniciadoRow = False
        for col in range(pIni, pIni + data["rows"][row]):  # Por cada columna desde el primer 1 todo revisar esto
            iniciadoCol = False
            acabadoCol = False
            c = 0  # Contador de 1s
            for rows in range(0, row + 1):  # Por cada fila hasta la actual (ya que el último no se incluye se pone +1)
                val = T[rows][col]  # Almacenamos el valor
                if val == 0 and iniciadoCol:
                    acabadoCol = True  # Si después de un uno hay un cero se da por terminada la serie
                elif val == 1 and acabadoCol:
                    return False  # Si hay un uno después de haber acabado no es factible ya que hay un espacio
                elif val == 1 and not iniciadoCol:
                    iniciadoCol = True  # El primer uno empiza a contar
                    c += 1
                elif val == 1 and iniciadoCol:
                    c += 1  # El resto de unos suman
                if c > data["cols"][col]:
                    return False  # Si hay más 1 de los indicados en la columna no es factible
        return True  # Si no se ha devuelto false todavía es que es factible

    except ValueError:  # Si no hay ningún 1 se da este error en el .index y es factible
        return True


# F. solución
def ComprobarCol(T, c, data):  # Esta función comprueba si una columna es solución
    sum = 0
    iniciado = False
    acabado = False
    for i in range(0, len(T)):
        val = T[i][c]
        if val == 0 and iniciado:
            acabado = True
        elif val == 1 and acabado:
            return False  # la única restricción es que haya un 0 entre dos 1
        elif val == 1:
            sum += val
            iniciado = True
    return sum == data["cols"][c]  # Se devuelve True si el número de 1 es igual al indicado por la columna


def Comprobar(T, data):  # Aplica ComprobarCol a todas las columnas
    return all(ComprobarCol(T, c, data) for c in range(0, len(data["cols"])))


# Funcion de movimiento

def Desplazar(T, row, data, SeVaAmover=0):  # esta función desplaza una fila hacia la derecha
    # Devuelve false si no se puede desplazar(ha llegado al final del tablero)
    try:
        ini = T[row].index(1)  # Se saca la posición del primer 1
        fin = ini + data["rows"][row]  # Se saca la última posición
        if fin < len(T[row]):  # Si no ha llegado al final del tablero
            T[row][ini] = 0  # El primero pasa a ser 0
            T[row][fin] = 1  # El último pasa a ser 1
            return True
        else:
            return False
    except ValueError:  # si no hay 1 dependiendo de la situación lo consideraremos desplazable o no
        if SeVaAmover == 1:  # Si se va a iterar a través de ella va a devolver False ya que sino entraría en un bucle infinito
            return False
        else:  # Si no se va a iterar por ella(El caso de desplazar filas en masa, si hay una que no se puede desplazar
            # se devuelve false ya que dejara un 0 en medio, si devolviera False se pararía aunque no es relevante la fila de 0)
            return True


def __rec__(T, data, row):  # La llamada recursiva
    if row == len(T) - 1:  # Si estás en la última fila se comprueba si es solución para todas las posibilidades
        try:
            T[row].index(1)
            d = True
            while not Comprobar(T, data) and d:  # Mientras no sea solución se desplaza la fila
                d = Desplazar(T, row, data)
                if not d:  # Si no se puede desplazar es que ha llegado al final y no hay solución con esa combinación
                    return False
            else:  # Si no ha llegado al final es que sí la hay
                return True
        except ValueError:
            return Comprobar(T, data)  # En el caso de que la última fila sea 0 todos será un caso especial
    else:  # Si la fila no es la última
        d = True
        while d:  # Mientras sea desplazable se busca solución, sino, devuelve False
            if Factible(T, row, data):  # si es factible se pasa a la siguiente fila
                if __rec__(T, data, row + 1):  # Si la llamada recursiva es True devuelve True
                    return True
                else:  # Si no es True reinicia las filas inferiores y desplaza la actual
                    ReiniciarTablero(data, T, row + 1)  # Se reinician las filas inferiores
                    d = Desplazar(T, row, data, SeVaAmover=1)
            else:  # Si no es factible se desplazan todas las filas inferiores y la actual
                for i in range(row, len(T)):
                    d = Desplazar(T, i, data)
                    if not d:  # En el caso de que una fila no sea desplazable se romperá el bucle y devolverá false
                        break
        return False


def Convertir(T, data):
    # Esta parte se usa para la optimización
    if data["permutaciones"][0]:  # Se giran la filas o las columnas si se han cambiado
        for i in range(0, len(T)):
            T[i].reverse()
    if data["permutaciones"][1]:
        T.reverse()
    # Se muetra la solución
    for i in range(0, len(T)):
        print("")
        for j in range(0, len(T[i])):
            if T[i][j] == 1:
                print("#", end="")
            else:
                print("-", end="")
    return T


from time import time

tini = time()
pprint(Iniciar("20 20 ", "3 2 2 3 2 4 3 4 3 2 2 1 2 2 2 1 1 1 2 1 ", "2 2 2 3 7 4 3 2 2 0 1 1 3 4 2 1 1 1 1 1 "))
print(time() - tini)

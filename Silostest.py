from random import randint


def Creador(n):
    for iss in range(n):
        amount = 5 + iss
        count = 0
        fila = []
        columna = []
        for i in range(amount):
            base = randint(1, 5 + iss)
            numFilas = randint(1, 5 + iss)
            columna.append(base)
            fila.append(numFilas)
            count += base

        arrVol = [0] * max(fila)

        for i in range(len(fila)):
            for j in range(fila[i]):
                arrVol[j] += columna[i]

        for i in range(1, len(arrVol)):
            arrVol[i] += arrVol[i - 1]

        altura = randint(0, len(arrVol))
        count = arrVol[altura - 1]
        l = []
        l.append(count)
        l.append(amount)
        for i in range(amount):
            l.append(str(columna[i]) + " " + str(fila[i]))
        yield (altura, l)


def ConvertirAstr(l):
    s = ""
    for i in l:
        s = s + '"'+str(i)+'",'
    return s


def Escibiente():
    r = Creador(9995)
    d = open("d2.txt", "w")
    i=0
    for sol,l in r:
        print(i)
        i+=1
        d.write(    "def test_largos"+str(i)+"(self):\n \tself.assertEqual("+str(sol)+",fun("+ConvertirAstr(l)+")\n")
    d.close()

def Arreglador():
    d2 = open("d2.txt", "r")
    lineas=d2.readlines()
    d3 = open("d3.py", "w")
    d3.write("from unittest import TestCase\n")
    d3.write("class Test(TestCase):\n")

    for linea in range(0,len(lineas)):
        if linea%100==0:
            d3 = open("d"+str(linea//100)+".py", "w")
            d3.write("from unittest import TestCase\n")
            d3.write("class Test(TestCase):\n")
        d3.write("\t"+lineas[linea])





Arreglador()

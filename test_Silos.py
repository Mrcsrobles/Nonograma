from unittest import TestCase
from Silos import AñadirOrdenadamente


class Test(TestCase):
    def test_añadir_ordenadamente(self):
        l = [(32, 40), (17, 52), (72, 5), (87, 82), (33, 95), (72, 4), (26, 34), (43, 90), (12, 13), (52, 14), (41, 43),
             (13, 75), (39, 38), (24, 32), (99, 11), (5, 33), (67, 40), (40, 19), (28, 32), (96, 64)]
        l2 = []
        for i in l:
            AñadirOrdenadamente(l2,i)
        aux=sorted(l,key=lambda x:x[1])
        for i in range(0,len(aux)):
            assert l2[0]==aux[0]
            l2.pop(0)
            aux.pop(0)
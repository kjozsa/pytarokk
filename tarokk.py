from enum import Enum, unique, auto
from random import shuffle


@unique
class Szin(Enum):
    KOR = auto()
    PIKK = auto()
    TREFF = auto()
    KARO = auto()
    TAROKK = auto()


szinek = [Szin.KOR, Szin.PIKK, Szin.TREFF, Szin.KARO]


@unique
class Figura(Enum):
    def __new__(cls, erosseg, pontertek):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        obj.erosseg = erosseg
        obj.pontertek = pontertek
        return obj

    Asz = 1, 1
    Bunkos = 2, 1
    Lovas = 3, 1
    Dama = 4, 1
    Kiraly = 5, 1

    I = 1, 5
    II = 2, 1
    III = 3, 1
    IV = 4, 1
    V = 5, 1
    VI = 6, 1
    VII = 7, 1
    VIII = 8, 1
    IX = 9, 1
    X = 10, 1
    XI = 11, 1
    XII = 12, 1
    XIII = 13, 1
    XIV = 14, 1
    XV = 15, 1
    XVI = 16, 1
    XVII = 17, 1
    XVIII = 18, 1
    XIX = 19, 1
    XX = 20, 1
    XXI = 21, 5
    SKIZ = 22, 5


class Lap:
    def __init__(cls, szin, figura, **kwargs):
        cls.szin = szin
        cls.figura = figura

    def __str__(self):
        return f"{self.szin.name} {self.figura.name}"

    def __repr__(self):
        return self.__str__()


szinesek = {Figura.Asz, Figura.Bunkos, Figura.Lovas, Figura.Dama, Figura.Kiraly}
tarokkok = set([x for x in Figura if x not in szinesek])

lapok = [Lap(szin, figura) for szin in szinek for figura in szinesek] + [Lap(Szin.TAROKK, figura) for figura in tarokkok]
shuffle(lapok)
print(lapok)
print(len(lapok))

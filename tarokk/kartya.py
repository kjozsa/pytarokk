from tarokk import *
import collections
from random import shuffle

Hivas = collections.namedtuple('Hivas', ['jatekos', 'lap'])


class Lap:
    def __init__(self, szin, figura):
        self.szin = szin
        self.figura = figura

        if self.is_tarokk():
            assert figura in tarokkok
        else:
            assert szin in szinek
            assert figura in figurak

    def __str__(self):
        return self.figura if self.is_tarokk() else f"{self.szin} {self.figura}"

    def __repr__(self):
        return self.__str__()

    def __lt__(self, other):
        return self.erosseg() < other.erosseg()

    def is_tarokk(self):
        return self.szin == 'tarokk'

    def ertek(self):
        if self.is_tarokk():
            return 5 if self.figura in honorok else 1
        else:
            return 1 + figurak.index(self.figura)

    def erosseg(self):
        if self.is_tarokk():
            return 100 + tarokkok.index(self.figura)
        else:
            return figurak.index(self.figura) + 10 * szinek.index(self.szin)

    def relativ_erosseg(self, hivott_lap):
        if self.szin == hivott_lap.szin or self.is_tarokk():
            return self.erosseg()
        else:
            return -1


class Pakli:
    def __init__(self):
        self._lapok = [Lap(szin, figura)
                       for szin in szinek
                       for figura in figurak] + \
                      [Lap("tarokk", tarokk) for tarokk in tarokkok]
        shuffle(self._lapok)

    def __len__(self):
        return len(self._lapok)

    def huz(self, n):
        lapok = self._lapok[:n]
        self._lapok = self._lapok[n:]
        return lapok


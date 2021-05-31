from tarokk.kartya import *


class Jatekos:
    def __init__(self, nev):
        self.nev = nev
        self.lapok: list[Lap] = []
        self.talon: list[Lap] = []
        self.elvitt: list[Lap] = []

    def __str__(self):
        return self.nev

    def kirakhato_lapok(self, szin):
        """
        játékos hívott színre rakható lapjai
        """
        if szin is None:
            return self.lapok

        egyezo_szinuek = [lap for lap in self.lapok if lap.szin == szin]
        tarokkok = [lap for lap in self.lapok if lap.is_tarokk()]

        if len(egyezo_szinuek) != 0:
            return egyezo_szinuek
        if len(tarokkok) != 0:
            return tarokkok
        return self.lapok
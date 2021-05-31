class Jatekos:
    def __init__(self, nev):
        self.nev = nev
        self.lapok: list[Lap] = []
        self.talon: list[Lap] = []
        self.elvitt: list[Lap] = []

    def __str__(self):
        return self.nev

    def kirakhato_lapok(self, szin):
        olyan_szinu = [lap for lap in self.lapok if lap.szin == szin]
        tarokkok = [lap for lap in self.lapok if lap.is_tarokk()]

        if len(olyan_szinu) != 0:
            return olyan_szinu
        if len(tarokkok) != 0:
            return tarokkok
        return self.lapok

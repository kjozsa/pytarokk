from random import shuffle, choice

tarokkok = "I II III IV V VI VII VIII IX X XI XII XIII XIV XV XVI XVII XVIII XIX XX XXI Skiz".split()
honorok = "I XXI Skiz".split()
szinek = "kőr treff pikk káró".split()
figurak = "ász bubi lovas dáma király".split()


class Lap:
    def __init__(self, szin, figura, **kwargs):
        self.szin = szin
        self.figura = figura

    def __str__(self):
        return self.figura if self.szin == 'tarokk' else f"{self.szin} {self.figura}"

    def __repr__(self):
        return self.__str__()

    def ertek(self):
        if self.szin == 'tarokk':
            return 5 if self.figura in honorok else 1
        else:
            return figurak.index(self.figura)


class Pakli:
    _lapok = [Lap(szin, figura)
              for szin in szinek
              for figura in figurak] + \
             [Lap("tarokk", tarokk) for tarokk in tarokkok]
    shuffle(_lapok)

    def __len__(self):
        return len(self._lapok)

    def __getitem__(self, position):
        return self._lapok[position]

    def __str__(self):
        return str(self._lapok)

    def oszt(self, n):
        lapok = self._lapok[:n]
        self._lapok = self._lapok[n:]
        return lapok


pakli = Pakli()
print(f"{len(pakli)} lap a pakliban: {pakli}")
talon = pakli.oszt(6)
print(f"{len(pakli)} lap a pakliban: {pakli}")

vg_lapok = pakli.oszt(9)
k_lapok = pakli.oszt(9)
h_lapok = pakli.oszt(9)
a_lapok = pakli.oszt(9)
print(f"{len(pakli)} lap a pakliban: {pakli}")

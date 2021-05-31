import collections
from random import shuffle, choice
import logging

tarokkok = "I II III IV V VI VII VIII IX X XI XII XIII XIV XV XVI XVII XVIII XIX XX XXI Skiz".split()
honorok = "I XXI Skiz".split()
szinek = "kőr treff pikk káró".split()
figurak = "ász bubi lovas dáma király".split()


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
        if self.szin == hivott_lap.szin:
            return self.erosseg()
        elif self.is_tarokk():
            return 100 + self.erosseg()
        else:
            return -1


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

    def huz(self, n):
        lapok = self._lapok[:n]
        self._lapok = self._lapok[n:]
        return lapok


Hivas = collections.namedtuple('Hivas', ['jatekos', 'lap'])


class Asztal:
    jatekosok = []
    hivo = ""
    talon: list[Lap] = []
    utes: list[Hivas] = []

    def leul(self, jatekos):
        self.jatekosok.append(jatekos)
        if len(self.jatekosok) == 4:
            self.osztas()

    def osztas(self):
        logging.info('új osztás')
        pakli = Pakli()
        self.talon = pakli.huz(6)
        for jatekos in self.jatekosok:
            jatekos.lapok = sorted(pakli.huz(9))
            logging.warning(f"{jatekos}: {jatekos.lapok}")
        self.hivo = self.jatekosok[0]

    def kovetkezo_jatekos(self):
        if len(self.utes) == 0:
            return self.hivo

        utolso = self.utes[-1].jatekos
        index = self.jatekosok.index(utolso)
        return self.jatekosok[index + 1] if index < 3 else self.jatekosok[0]

    def hivas_szine(self):
        if len(self.utes) == 0:
            return None
        else:
            return self.utes[0].lap.szin

    def rak(self, jatekos, lap):
        assert jatekos == self.kovetkezo_jatekos()  # ő jön
        assert lap in jatekos.lapok  # ő lapja
        if len(self.utes) != 0:
            assert lap in jatekos.kirakhato_lapok(self.hivas_szine())  # szabályos

        logging.debug(f"{jatekos} hív: {lap}")

        jatekos.lapok.remove(lap)
        self.utes.append(Hivas(jatekos, lap))

        if len(self.utes) == 4:
            viszi = self.kiviszi(self.utes)
            logging.info(f"Legerősebb a {viszi.lap}, elvitte {viszi.jatekos}")
            self.utes = []
            self.hivo = viszi.jatekos

    def kovetkezo_rak_random(self):
        jatekos = self.kovetkezo_jatekos()
        lap = choice(jatekos.kirakhato_lapok(self.hivas_szine()))
        self.rak(jatekos, lap)

    @staticmethod
    def kiviszi(utes):
        return max(utes, key=lambda hivas: hivas.lap.relativ_erosseg(utes[0].lap))


class Jatekos:
    lapok = []
    talon = []

    def __init__(self, nev):
        self.nev = nev

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

import logging
from random import choice
from tarokk.jatekos import *


class Asztal:
    def __init__(self):
        self.jatekosok: list[Jatekos] = []
        self.talon: list[Lap] = []
        self.utes: list[Hivas] = []
        self.hivo: Jatekos = None

    def leul(self, jatekos):
        assert jatekos not in self.jatekosok
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
            viszi.jatekos.elvitt.extend([x.lap for x in self.utes])
            self.utes = []
            self.hivo = viszi.jatekos

    def kovetkezo_rak_random(self):
        jatekos = self.kovetkezo_jatekos()
        lap = choice(jatekos.kirakhato_lapok(self.hivas_szine()))
        self.rak(jatekos, lap)

    @staticmethod
    def kiviszi(utes):
        return max(utes, key=lambda hivas: hivas.lap.relativ_erosseg(utes[0].lap))

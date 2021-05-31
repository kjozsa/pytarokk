import logging
from random import choice
from tarokk import *
from tarokk.jatekos import *
from tarokk.bemondasok import *


class Asztal:
    def __init__(self):
        self.jatekosok: list[Jatekos] = []
        self.talon: list[Lap] = []
        self.utesek: list[list[Hivas]] = []
        self.aktualis_utes: list[Hivas] = []
        self.hivo: Jatekos = None
        self.parok = ()

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
        self.parok = (self.jatekosok[:2], self.jatekosok[2:])

    def kovetkezo_jatekos(self):
        if len(self.aktualis_utes) == 0:
            return self.hivo

        utolso = self.aktualis_utes[-1].jatekos
        index = self.jatekosok.index(utolso)
        return self.jatekosok[index + 1] if index < 3 else self.jatekosok[0]

    def hivas_szine(self):
        if len(self.aktualis_utes) == 0:
            return None
        else:
            return self.aktualis_utes[0].lap.szin

    def rak(self, jatekos, lap):
        assert jatekos == self.kovetkezo_jatekos()  # ő jön
        assert lap in jatekos.lapok  # ő lapja
        if len(self.aktualis_utes) != 0:
            assert lap in jatekos.kirakhato_lapok(self.hivas_szine())  # szabályos

        logging.debug(f"{jatekos} hív: {lap}")

        jatekos.lapok.remove(lap)
        self.aktualis_utes.append(Hivas(jatekos, lap))

        if len(self.aktualis_utes) == 4:
            self.aktualis_utes_vege()

    def aktualis_utes_vege(self):
        viszi = ki_viszi(self.aktualis_utes)
        logging.info(f"Legerősebb a {viszi.lap}, elvitte {viszi.jatekos}")
        viszi.jatekos.elvitt.extend([x.lap for x in self.aktualis_utes])

        for bemondas in bemondasok:
            result = bemondas.check(self.parok, self.utesek, self.aktualis_utes)
            if result is not None:
                logging.critical(f"!! ## {result} ## !!")

        self.utesek.extend(self.aktualis_utes)
        self.aktualis_utes = []
        self.hivo = viszi.jatekos

    def kovetkezo_rak_random(self):
        jatekos = self.kovetkezo_jatekos()
        lap = choice(jatekos.kirakhato_lapok(self.hivas_szine()))
        self.rak(jatekos, lap)

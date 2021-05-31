import logging
from random import choice

from tarokk.bemondasok import *
from tarokk.jatekos import *


class Asztal:
    def __init__(self):
        self.jatekosok: list[Jatekos] = []
        self.parok: Parok = Parok
        self.talon: list[Lap] = []
        self.felvevo_talon: list[Lap] = []
        self.ellenpar_talon: list[Lap] = []
        self.utesek: list[list[Hivas]] = []
        self.hivo: Jatekos = None
        self.aktualis_utes: list[Hivas] = []
        self.licitalt_jatek = 3  # TODO licit

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

        # TODO LICIT !!!

        self.felvevo_talon = self.talon[3:]
        self.ellenpar_talon = self.talon[:3]

        self.hivo = self.jatekosok[0]
        self.parok.felvevok, self.parok.ellenpar = (self.jatekosok[:2], self.jatekosok[2:])

    def kovetkezo_jatekos(self):
        if len(self.aktualis_utes) == 0:
            return self.hivo

        utolso = self.aktualis_utes[-1].jatekos
        return self.ki_jon_utana(utolso)

    def ki_jon_utana(self, jatekos):
        index = self.jatekosok.index(jatekos)
        return self.jatekosok[index + 1] if index < 3 else self.jatekosok[0]

    def hivas_szine(self):
        if len(self.aktualis_utes) != 0:
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
        viszi.jatekos.elvisz([x.lap for x in self.aktualis_utes])

        for bemondas in bemondasok:
            result = bemondas.check(self.parok, self.utesek, self.aktualis_utes)
            if result is not None:
                logging.critical(f"!! ## {result} ## !!")

        self.utesek.append(self.aktualis_utes)
        self.aktualis_utes = []

        if len(self.utesek) == 9:
            self.jatek_vege()
        else:
            self.hivo = viszi.jatekos


    def kovetkezo_rak_random(self):
        jatekos = self.kovetkezo_jatekos()
        lap = choice(jatekos.kirakhato_lapok(self.hivas_szine()))
        self.rak(jatekos, lap)

    def jatek_vege(self):
        logging.info("Vége a játéknak")
        self.parok.felvevok[0].elvisz(self.felvevo_talon)
        self.parok.ellenpar[0].elvisz(self.ellenpar_talon)
        result = Parti(self.licitalt_jatek).check(self.parok, self.utesek, None)
        logging.critical(f"!! ## {result} ## !!")


def talon_kiosztas(self, licitalt_jatek, talon, parok):
        talon_kioszt = [
            [0, 2, 2, 2],
            [1, 2, 2, 1],
            [2, 2, 1, 1],
            [3, 1, 1, 1]
        ]
        talon_pakli = Pakli(talon)
        elosztas = talon_kioszt[licitalt_jatek]
        felvevo = parok.felvevok[0]
        felvevo.elvisz(talon_pakli.huz(elosztas[0]))
        kovetkezo = self.ki_jon_utana(felvevo)
        kovetkezo.elvisz(talon_pakli.huz(elosztas[1]))
        kovetkezo = self.ki_jon_utana(kovetkezo)
        kovetkezo.elvisz(talon_pakli.huz(elosztas[2]))
        kovetkezo = self.ki_jon_utana(kovetkezo)
        kovetkezo.elvisz(talon_pakli.huz(elosztas[3]))


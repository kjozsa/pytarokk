from tarokk.jatekos import Jatekos
from tarokk.kartya import *
import logging

Pagat = Lap('tarokk', 'I')
II = Lap('tarokk', 'II')
XX = Lap('tarokk', 'XX')
XXI = Lap('tarokk', 'XXI')
Skiz = Lap('tarokk', 'Skiz')


class Bemondas:
    def __init__(self, bemondas_neve):
        self.bemondta = None
        self.bemondas_neve = bemondas_neve
        self.kontra = 1
        self.meglett = None

    def forint(self):
        return 10 * int(self.ertek * self.kontra * (0.5 if self.is_csendes() else 1))

    def is_csendes(self):
        return self.bemondta is None

    def ertekeles(self, nyertes, kommentar=""):
        if self.meglett is None:
            self.meglett = True
            return f"{self.bemondas_neve}, {kommentar}, {self.forint()} forintért"


class XXI_fogas(Bemondas):
    ertek = 42

    def __init__(self):
        super().__init__("XXI fogás")

    def check(self, parok, utesek, aktualis_utes):
        xxi: Jatekos = next(iter([hivas.jatekos for hivas in aktualis_utes if hivas.lap == XXI]), None)
        skiz: Jatekos = next(iter([hivas.jatekos for hivas in aktualis_utes if hivas.lap == Skiz]), None)
        if xxi and skiz:
            return self.ertekeles(f"{skiz} megfogta {xxi} XXI-ét")


class Pagat_ulti(Bemondas):
    ertek = 10

    def __init__(self):
        super().__init__("Pagát ulti")

    def check(self, parok, utesek, aktualis_utes):
        viszi = ki_viszi(aktualis_utes)
        if len(utesek) == 8 and viszi.lap == Pagat:
            return self.ertekeles(f"{viszi.jatekos}")



class Sas_ulti(Bemondas):
    ertek = 10

    def __init__(self):
        super().__init__("Sas ulti")

    def check(self, parok, utesek, aktualis_utes):
        viszi = ki_viszi(aktualis_utes)
        if len(utesek) == 8 and viszi.lap == II:
            return self.ertekeles(f"{viszi.jatekos} csinálta")


class Tuletroa(Bemondas):
    ertek = 2

    def __init__(self):
        super().__init__("Tuletroá")

    def check(self, parok, utesek, aktualis_utes):
        felvevoke = [lap for sublist in [jatekos.elvitt for jatekos in parok.felvevok] for lap in sublist]
        if {Pagat, XXI, Skiz}.issubset(felvevoke):
            return self.ertekeles(parok.felvevok, "a felvevő párnak")

        ellenpare = [lap for sublist in [jatekos.elvitt for jatekos in parok.ellenpar] for lap in sublist]
        if {Pagat, XXI, Skiz}.issubset(ellenpare):
            return self.ertekeles(parok.ellenpar, "az ellenpárnak")


bemondasok = [XXI_fogas(), Pagat_ulti(), Sas_ulti(), Tuletroa()]

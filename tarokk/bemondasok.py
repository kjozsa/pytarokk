from tarokk import *
from tarokk.jatekos import Jatekos
from tarokk.kartya import *

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

    def forint(self):
        return 10 * int(self.ertek * self.kontra * (0.5 if self.is_csendes() else 1))

    def is_csendes(self):
        return self.bemondta is None

    def ertekeles(self, extra_info):
        return f"{self.bemondas_neve}, {extra_info}, {self.forint()} forintért"


class XXI_fogas(Bemondas):
    ertek = 42

    def __init__(self):
        super().__init__("XXI fogás")

    def check(self, parok, utesek, aktualis_utes):
        xxi: Jatekos = next(iter([hivas.jatekos for hivas in aktualis_utes if hivas.lap == XXI]), None)
        skiz: Jatekos = next(iter([hivas.jatekos for hivas in aktualis_utes if hivas.lap == Skiz]), None)
        if xxi and skiz:
            return self.ertekeles(f"{skiz} megfogta {xxi} XXI-ét")
        return None


class Pagat_ulti(Bemondas):
    ertek = 10

    def __init__(self):
        super().__init__("Pagát ulti")

    def check(self, parok, utesek, aktualis_utes):
        viszi = ki_viszi(aktualis_utes)
        if len(utesek) == 8 and viszi.lap == Pagat:
            return self.ertekeles(f"{viszi.jatekos}")
        return None


class Sas_ulti(Bemondas):
    ertek = 10

    def __init__(self):
        super().__init__("Sas ulti")

    def check(self, parok, utesek, aktualis_utes):
        viszi = ki_viszi(aktualis_utes)
        if len(utesek) == 8 and viszi.lap == II:
            return self.ertekeles(f"{viszi.jatekos}")
        return None


class Tuletroa(Bemondas):
    ertek = 2

    def __init__(self):
        super().__init__("Tuletroá")

    def check(self, parok, utesek, aktualis_utes):
        return


bemondasok = [XXI_fogas(), Pagat_ulti(), Sas_ulti(), Tuletroa()]

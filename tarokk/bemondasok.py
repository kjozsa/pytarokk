from tarokk import *
from tarokk.kartya import *

Pagát = Lap('tarokk', 'I')
II = Lap('tarokk', 'II')
XX = Lap('tarokk', 'XX')
XXI = Lap('tarokk', 'XXI')
Skiz = Lap('tarokk', 'Skiz')


class XXI_fogas:
    ertek = 42

    @staticmethod
    def check(parok, utesek, aktualis_utes):
        xxi = next(iter([hivas.jatekos for hivas in aktualis_utes if hivas.lap == XXI]), None)
        skiz = next(iter([hivas.jatekos for hivas in aktualis_utes if hivas.lap == Skiz]), None)
        if xxi and skiz:
            return f"XXI fogás, {skiz} megfogta {xxi} XXI-ét"
        return None


class Pagat_ulti:
    ertek = 10

    @staticmethod
    def check(parok, utesek, aktualis_utes):
        viszi = ki_viszi(aktualis_utes)
        return f"Pagát ulti, {viszi.jatekos}" if len(utesek) == 8 and viszi.lap == Pagát else None

class Sas_ulti:
    ertek = 10

    @staticmethod
    def check(parok, utesek, aktualis_utes):
        viszi = ki_viszi(aktualis_utes)
        return f"Sas ulti, {viszi.jatekos}" if len(utesek) == 8 and viszi.lap == II else None


bemondasok = [XXI_fogas, Pagat_ulti, Sas_ulti]

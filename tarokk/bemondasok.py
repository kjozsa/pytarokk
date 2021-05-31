from tarokk import *
from tarokk.kartya import *

Pagát = Lap('tarokk', 'I')
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


bemondasok = [XXI_fogas]

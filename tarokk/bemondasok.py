from tarokk import *
from tarokk.kartya import *

Pagát = Lap('tarokk', 'I')
XX = Lap('tarokk', 'XX')
XXI = Lap('tarokk', 'XXI')
Skiz = Lap('tarokk', 'Skiz')


class XXI_fogas:
    @staticmethod
    def check(utesek, aktualis_utes):
        lapok = [hivas.lap for hivas in aktualis_utes]
        return "XXI fogás" if XXI in lapok and Skiz in lapok else None

bemondasok = [XXI_fogas]

from tarokk.asztal import *
from tarokk.bemondasok import *
import pytest

k = Jatekos("Kristóf")
h = Jatekos("Hoba")
vg = Jatekos("Vinczeg")
a = Jatekos("Attila")
parok = ([k, h], [a, vg])


def test_pakli():
    """
    pakli, osztás
    """
    pakli = Pakli()
    assert len(pakli) == 42

    talon = pakli.huz(6)
    assert len(pakli) == 42 - 6
    assert len(talon) == 6

    vg_lapok = pakli.huz(9)
    k_lapok = pakli.huz(9)
    h_lapok = pakli.huz(9)
    a_lapok = pakli.huz(9)

    assert len(vg_lapok) == 9
    assert len(pakli) == 0


def test_lap():
    """
    lap érték
    """
    assert Lap("tarokk", "I").ertek() == 5
    assert Lap("tarokk", "II").ertek() == 1
    assert Lap("kőr", "ász").ertek() == 1
    assert Lap("pikk", "király").ertek() == 5
    assert Lap("pikk", "dáma").ertek() == 4

    with pytest.raises(AssertionError):
        Lap("NOSUCH", "ász")
    with pytest.raises(AssertionError):
        Lap("káró", "NOSUCH")


def test_kiviszi():
    assert ki_viszi([
        Hivas('A', Lap('káró', 'lovas')),
        Hivas('B', Lap('tarokk', 'I')),
        Hivas('C', Lap('tarokk', 'XVI')),
        Hivas('D', Lap('pikk', 'dáma'))
    ]).jatekos == 'C'

    assert ki_viszi([
        Hivas('C', Lap('tarokk', 'XVI')),
        Hivas('A', Lap('káró', 'lovas')),
        Hivas('B', Lap('tarokk', 'I')),
        Hivas('D', Lap('pikk', 'dáma'))
    ]).jatekos == 'C'

    assert ki_viszi([
        Hivas('D', Lap('pikk', 'dáma')),
        Hivas('A', Lap('káró', 'lovas')),
        Hivas('B', Lap('tarokk', 'I')),
        Hivas('C', Lap('tarokk', 'XVI'))
    ]).jatekos == 'C'

    assert ki_viszi([
        Hivas('A', Lap('treff', 'ász')),
        Hivas('B', Lap('pikk', 'lovas')),
        Hivas('C', Lap('kőr', 'király')),
        Hivas('D', Lap('káró', 'dáma'))
    ]).jatekos == 'A'


def test_kirakhato_lapok():
    """
    színre szín, ha nincs, tarokk
    """
    k = Jatekos('Kristóf')
    k.lapok = [Lap('treff', 'lovas'),
               Lap('tarokk', 'II'),
               Lap('tarokk', 'Skiz')]
    assert k.kirakhato_lapok('treff') == [Lap('treff', 'lovas')]
    assert k.kirakhato_lapok('pikk') == [Lap('tarokk', 'II'), Lap('tarokk', 'Skiz')]
    assert k.kirakhato_lapok('tarokk') == [Lap('tarokk', 'II'), Lap('tarokk', 'Skiz')]


def test_jatek():
    """
    játék próba
    """
    asztal = Asztal()
    asztal.leul(k)
    with pytest.raises(AssertionError):
        asztal.leul(k)  # már játszik
    asztal.leul(h)
    asztal.leul(vg)
    asztal.leul(a)
    assert len(h.lapok) == 9

    assert asztal.kovetkezo_jatekos() == k

    asztal.rak(k, k.lapok[0])
    with pytest.raises(AssertionError):
        asztal.rak(k, k.lapok[0])  # már rakott

    with pytest.raises(AssertionError):
        asztal.rak(h, a.lapok[0])  # nem az ő lapja

    for i in range(35):
        asztal.kovetkezo_rak_random()

    # játék vége
    osszes_elvitt = [*h.elvitt, *k.elvitt, *a.elvitt, *vg.elvitt]
    assert len(osszes_elvitt) == 42 - 6
    assert sum([lap.ertek() for lap in [*osszes_elvitt, *asztal.talon]]) == 94

    for jatekos in [h, a, vg, k]:
        pont = sum([lap.ertek() for lap in jatekos.elvitt])
        logging.info(f"{jatekos} elvitt {int(len(jatekos.elvitt) / 4)} ütést, {pont} pont értékben: {jatekos.elvitt}")


def test_XXI_fogas():
    aktualis_utes = [Hivas(k, XXI),
                     Hivas(h, XX),
                     Hivas(a, Skiz),
                     Hivas(vg, Pagát)]
    result = XXI_fogas.check(parok, None, aktualis_utes)
    logging.info(result)
    assert result


def test_Sas_ulti():
    utesek = [None] * 8
    assert len(utesek) == 8
    aktualis_utes = [Hivas(k, Lap('treff', 'bubi')),
                     Hivas(h, Lap('treff', 'dáma')),
                     Hivas(a, Lap('pikk', 'király')),
                     Hivas(vg, II)]
    result = Sas_ulti.check(parok, utesek, aktualis_utes)
    logging.info(result)
    assert result

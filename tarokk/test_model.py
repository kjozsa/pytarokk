from tarokk.model import *
import pytest


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
        assert Lap("NOSUCH", "ász").ertek() == 1
    with pytest.raises(AssertionError):
        assert Lap("káró", "NOSUCH").ertek() == 1


def test_jatek():
    """
    játék próba
    """
    k = Jatekos("Kristóf")
    h = Jatekos("Hoba")
    vg = Jatekos("Vinczeg")
    a = Jatekos("Attila")

    asztal = Asztal()
    asztal.leul(k)
    asztal.leul(h)
    asztal.leul(vg)
    asztal.leul(a)
    assert len(h.lapok) == 9

    asztal.rak(h, h.lapok[0])
    with pytest.raises(AssertionError):
        asztal.rak(h, h.lapok[0])   # mar rakott




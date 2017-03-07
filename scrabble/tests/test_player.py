from scrabble.lib.player import Player


def test_player_init():
    p = Player('Peter')
    assert(p.name == 'Peter')
    assert(len(p.tray) == 0)


def test_is_letter_in_tray():
    p = Player('Peter')
    assert(not p.is_letter_in_tray('A'))
    assert(not p.is_letter_in_tray(''))
    p.tray = ['A', 'A', 'B', 'C', 'D']
    assert(p.is_letter_in_tray('A'))
    assert(not p.is_letter_in_tray('F'))


def test_remove_letter():
    p = Player('Peter')
    p.tray = ['A', 'A', 'B', 'C', 'D']
    p.remove_letter('A')
    assert(p.tray == ['A', 'B', 'C', 'D'])

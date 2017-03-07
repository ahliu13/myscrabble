from scrabble.lib.bag import Bag

from collections import Counter
import math


def test_bag_init():
    bag = Bag()
    assert(len(bag.letters) == 100)


def test_draw_random_letter_max_freq():
    """Checks there are no more than 12 of a given letter from draw random"""
    bag = Bag()
    c = Counter()
    while len(bag.letters) > 0:
        letter = bag.draw_random_letter()
        c[letter] += 1
    for k, v in c.iteritems():
        assert(v <= 12)


def test_draw_random_letter_type():
    """Checks each letter is a string and only 1 char"""
    bag = Bag()
    c = Counter()
    while len(bag.letters) > 0:
        letter = bag.draw_random_letter()
        assert(letter == str(letter))
        if letter == '':
            continue
        else:
            assert(len(letter) == 1)


def test_draw_random_distro(num_trials=1000, threshold=0.1):
    """ Performs 1000 trails by default and sees if the resulting distribution is
    within threshold of expected value
    """
    first_letters = Counter()
    num_occ = Counter()
    expected_freq = {}
    bag = Bag()
    for letter in bag.letters:
            num_occ[letter] += 1
    for k, v in num_occ.iteritems():
        expected_freq[k] = v*1.0/100
    for i in xrange(0, num_trials):
        bag = Bag()
        first = bag.draw_random_letter()
        first_letters[first] += 1
    for k, v in first_letters.iteritems():
        observed = v*1.0/num_trials
        actual = expected_freq[k]
        assert(math.fabs(round(observed, 2) - round(actual, 2)) <= threshold)


def test_insert():
    bag = Bag()
    try:
        bag.insert_letter('A')
    except:
        assert(True)


def test_insert_and_draw():
    bag = Bag()
    letters_drawn = []
    for i in xrange(0, 50):
        letter = bag.draw_random_letter()
        letters_drawn.append(letter)
    assert(len(bag.letters) == 50)
    assert(len(letters_drawn) == 50)
    while len(letters_drawn) > 0:
        bag.insert_letter(letters_drawn[0])
        letters_drawn = letters_drawn[1:]
    assert(len(bag.letters) == 100)

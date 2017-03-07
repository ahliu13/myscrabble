from random import randrange

BLANK_TILE = 'A'
""" TODO: Add blank tile funcionality - for now we are opting to have
    2 extra A's in our bag rather than the 2 blank tiles. """

MAX_CAPACITY = 100


class Bag:
    def __init__(self):
        """Initializes a bag of 100 letter tiles and sets the frequency of the
           letters
        """
        a_d = ['A']*9 + ['B']*2 + ['C']*2 + ['D']*4
        e_h = ['E']*12 + ['F']*2 + ['G']*3 + ['H']*2
        i_l = ['I']*9 + ['J']*1 + ['K']*1 + ['L']*4
        m_p = ['M']*2 + ['N']*6 + ['O']*8 + ['P']*2
        q_t = ['Q']*1 + ['R']*6 + ['S']*4 + ['T']*6
        u_x = ['U']*4 + ['V']*2 + ['W']*2 + ['X']*1
        y_blank = ['Y']*2 + ['Z']*1 + [BLANK_TILE]*2
        self.letters = a_d + e_h + i_l + m_p + q_t + u_x + y_blank

    def draw_random_letter(self):
        """Selects a random letter from the bag without replacement"""
        l = len(self.letters)
        random_index = randrange(0, l)
        letter = self.letters[random_index]
        self.letters = self.letters[:random_index] + self.letters[random_index + 1:]
        return letter

    def insert_letter(self, letter):
        """Inserts a letter into the bag"""
        if len(self.letters) == MAX_CAPACITY:
            raise Exception('The bag is already full')
        self.letters.append(letter)

    def is_empty(self):
        return len(self.letters) == 0

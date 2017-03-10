from scrabble.lib.state import get_initial_board_state
from scrabble.lib.state import CENTER_MARKER
from scrabble.lib.state import EMPTY
from scrabble.lib.state import DOUBLE_LETTER
from scrabble.lib.state import DOUBLE_WORD
from scrabble.lib.state import TRIPLE_LETTER
from scrabble.lib.state import TRIPLE_WORD
from scrabble.lib.tile import Tile

import enchant
from ast import literal_eval as make_tuple


CENTER_INDEX = (7, 7)
MIN_ROW = 0
MAX_ROW = 14
MIN_COLUMN = 0
MAX_COLUMN = 14
DOUBLE_SCORE = 2
TRIPLE_SCORE = 3

""" TODO: Add funcionality for blank tiles - board could keep a dictionary of
    them with the location and the letter they represent once placed.
    For example if the index (7, 8) has a blank tile and the player
    calls it an A, we keep track of that in the dictionary.
    - In is_valid_move, when getting the main and stemming words,
    try replacing the blanks their intended letters before checking if
    it's a word.
    - In scoring, we can do the same.
"""


class Board:
    def __init__(self):
        """Initializes a board grid, an empty occupied set
        (no one has placed letters yet), and a bordering set
        (see README for description)
        """
        self.current_state = get_initial_board_state()
        self.occupied = set()
        self.bordering = set()
        self.bordering.add(CENTER_INDEX)
        # The first move must lay over the center index
        # self.blank_tiles = {} # TODO: Add funcionality for this
        # k is (r, c) location of the blank tile, V is the letter it represents

    def is_valid_move(self, letters, indecies):
        """ Is Valid Move Logic: When the player makes a move, he or she submits a
            list of indecies and a list of letters. The first set of checks is on
            the set of indecies - for example:
            - Are the spaces you want to place available?
            - Are the indecies you want to place bordering with previously placed words?
            - Are the indecies in bounds of the board?
            - Are the indecies lying in a single axis - for example, no diagonal moves
            are allowed.
            After we have verified those 4 things, we get the newly formed words and
            ensure they are in our dictionary (see README for definitions)
        """
        if len(letters) != len(indecies):
            return False
        if (
            not self.all_spaces_available(indecies) or
            not self.is_bordering_with_other_words(indecies) or
            not self.is_in_bounds(indecies) or
            not (self.is_in_single_column(indecies) or self.is_in_single_row(indecies))
        ):
            return False

        main_word = self.get_main_word(letters, indecies)
        if not self.is_word(main_word):
            return False

        stemming_words = self.get_stemming_words(letters, indecies)
        for word in stemming_words:
            if not self.is_word(word):
                return False
        return True

    def all_spaces_available(self, indecies):
        """Checks if all the spaces are available"""
        for spot in indecies:
            """If you are trying to lay a tile in a previously occupied space,
            we return false"""
            if spot in self.occupied:
                return False
        return True

    def is_bordering_with_other_words(self, indecies):
        """Checks whether the tiles you are about to play border at least
           one other word on the board"""
        for spot in indecies:
            if spot in self.bordering:  # If you find at least 1, return True
                return True
        return False

    def is_in_bounds(self, indecies):
        """Checks whether the set of indecies are in bounds of the board"""
        for (row, col) in indecies:
            if (row < MIN_ROW) or (row > MAX_ROW) or (col < MIN_COLUMN) or (col > MAX_COLUMN):
                return False
        return True

    def is_in_single_column(self, indecies):
        """Checks if all the column values are the same.
            Note, need not be continous.
        """
        st_column = indecies[0][1]
        for i in xrange(1, len(indecies)):
            next_column = indecies[i][1]
            if next_column != st_column:
                return False
        return True

    def is_in_single_row(self, indecies):
        """Checks if all the row values are the same.
            Note, need not be continous.
        """
        st_row = indecies[0][0]
        for i in xrange(1, len(indecies)):
            next_row = indecies[i][0]
            if next_row != st_row:
                return False
        return True

    def get_top_row(self, letters, indecies, row, col):
        while ((row, col) in self.occupied or (row, col) in set(indecies)) and row > MIN_ROW:
            row -= 1
        row += 1  # Move R up 1 to make the bounds inclusive
        return row

    def get_bottom_row(self, letters, indecies, row, col):
        while ((row, col) in self.occupied or (row, col) in set(indecies)) and row < MAX_ROW:
            row += 1
        row -= 1  # Move R down 1 to make the bounds inclusive
        return row

    def get_left_column(self, letters, indecies, row, col):
        while ((row, col) in self.occupied or (row, col) in set(indecies)) and col > MIN_COLUMN:
            col -= 1
        col += 1  # Move C up 1 to make the bounds inclusive
        return col

    def get_right_column(self, letters, indecies, row, col):
        while ((row, col) in self.occupied or (row, col) in set(indecies)) and col < MAX_COLUMN:
            col += 1
        col -= 1
        return col  # Inclusive Bounds

    def get_main_word(self, letters, indecies):
        """Retrieves the main word you are laying down on the board"""
        main_word = ''
        (row, col) = indecies[0]
        if self.is_in_single_row(indecies):
            top_row = row
            bottom_row = row
            left_col = self.get_left_column(letters, indecies, row, col)
            right_col = self.get_right_column(letters, indecies, row, col)
        elif self.is_in_single_column(indecies):
            top_row = self.get_top_row(letters, indecies, row, col)
            bottom_row = self.get_bottom_row(letters, indecies, row, col)
            left_col = col
            right_col = col
        else:
            raise Exception('Indecies do not lie in a single axis')
        return self.get_potential_word(top_row, bottom_row, left_col, right_col, letters)

    def get_stemming_words(self, letters, indecies):
        """Retrieves the words stemming from the main letters player is playing"""
        default_row = indecies[0][0]  # 0 is the index of the row in the (r, c) tuple
        default_col = indecies[0][1]  # 1 is the index of the column in the (r, c) tuple
        stem_words = []
        if self.is_in_single_row(indecies):  # Main Word is Horizontal
            columns_to_check = []
            for spot in indecies:
                columns_to_check.append(spot[1])
            for c in columns_to_check:
                top_row = self.get_top_row(letters, indecies, default_row, c)
                bottom_row = self.get_bottom_row(letters, indecies, default_row, c)
                stem_word = self.get_potential_word(top_row, bottom_row, c, c, letters)
                if len(stem_word) > 1:
                    stem_words.append(stem_word)
        elif self.is_in_single_column(indecies):  # Main Word is Vertical
            rows_to_check = []
            for spot in indecies:
                rows_to_check.append(spot[0])
            for r in rows_to_check:
                left_c = self.get_left_column(letters, indecies, r, default_col)
                right_c = self.get_right_column(letters, indecies, r, default_col)
                stem_word = self.get_potential_word(r, r, left_c, right_c, letters)
                if len(stem_word) > 1:
                    stem_words.append(stem_word)
        return stem_words

    def get_potential_word(self, top_r, bottom_r, left_c, right_c, letters):
        """ Given a starting and ending (row, col), retrieves the potential word
        that would be played
        """
        i = 0
        word = ''
        # Given a rannge of indecies, if the spot has something on it already, we grab that letter
        # Else we take a letter from our 'letters' list
        for row in xrange(top_r, bottom_r + 1):
            for col in xrange(left_c, right_c + 1):
                if (row, col) in self.occupied:
                    letter = self.current_state[row][col]
                else:
                    letter = letters[i]
                    i += 1
                word += letter
        return word

    def is_word(self, word):
        """ Finally, once we have a word, we use enchant's dictionary to check
        whether it's an English word
        """
        d = enchant.Dict('en_US')
        return d.check(word)

    def score_play(self, letters, indecies):
        """ Scores the potential move - does not alter the board state"""
        full_score = 0
        full_score += self.get_main_word_score(letters, indecies)
        full_score += self.get_stem_word_scores(letters, indecies)
        return full_score

    def get_main_word_score(self, letters, indecies):
        """Gets the score for the main word"""
        main_word_indecies = self.get_index_list_main_word(letters, indecies)
        word_multipliers = self.get_word_multipliers(indecies)
        main_word_score = 0
        for (row, col) in main_word_indecies:
            letter_score = self.score_letter(letters, indecies, row, col)
            main_word_score += letter_score
        main_word_score = self.apply_word_multipliers(main_word_score, word_multipliers)
        return main_word_score

    def get_stem_word_scores(self, letters, indecies):
        """Gets the scores for all the stem words"""
        scores_from_stems = 0
        stemming_word_indecies = self.get_indecies_stemming_words(letters, indecies)
        for stem_word_index_list in stemming_word_indecies:
            stem_word_score = 0
            word_mults_stem = self.get_word_multipliers(stem_word_index_list)
            for (row, col) in stem_word_index_list:
                letter_score = self.score_letter(letters, indecies, r, c)
                stem_word_score += letter_score
            stem_word_score = self.apply_word_multipliers(stem_word_score, word_mults_stem)
            scores_from_stems += stem_score
        return scores_from_stems

    def get_index_list(self, top_r, bottom_r, left_c, right_c):
        index_list = []
        for row in xrange(top_r, bottom_r + 1):
            for col in xrange(left_c, right_c + 1):
                index_list.append((row, col))
        return index_list

    def get_index_list_main_word(self, letters, indecies):
        """ Gets the full indecies of the main word in the potential move
        so if you play 'c' and 's' on the outside of 'at' to get the main
        word of 'cats', you will get the indecies of c, a, t, and s """
        indecies_main_word = []
        (row, col) = indecies[0]
        if self.is_in_single_row(indecies):  # Main word is horizontal
            top_r = row
            bottom_r = row
            left_c = self.get_left_column(letters, indecies, row, col)
            right_c = self.get_right_column(letters, indecies, row, col)
        elif self.is_in_single_column(indecies):  # Main word is vertical
            top_r = self.get_top_row(letters, indecies, row, col)
            bottom_r = self.get_bottom_row(letters, indecies, row, col)
            left_c = col
            right_c = col
        else:
            raise Exception('Index list not in single axis')
        return self.get_index_list(top_r, bottom_r, left_c, right_c)

    def get_indecies_stemming_words(self, letters, indecies):
        """Gets the indecies for the stemming words (stemming word defined in README)"""
        r = indecies[0][0]
        c = indecies[0][1]
        stem_words_indecies = []
        if self.is_in_single_row(indecies):  # Main Word is Horizontal
            cols_to_check = []
            for spot in indecies:
                cols_to_check.append(spot[1])
            for c in cols_to_check:
                top_r = self.get_top_row(letters, indecies, r, c)
                bottom_r = self.get_bottom_row(letters, indecies, r, c)
                stem_indecies = self.get_index_list(top_r, bottom_r, c, c)
                if len(stem_indecies) > 1:
                    stem_words_indecies.append(stem_indecies)
        elif self.is_in_single_column(indecies):  # Main Word is Vertical
            rows_to_check = []
            for spot in indecies:
                rows_to_check.append(spot[0])
            for r in rows_to_check:
                left_c = self.get_left_column(letters, indecies, r, c)
                right_c = self.get_right_column(letters, indecies, r, c)
                stem_indecies = self.get_index_list(r, r, left_c, right_c)
                if len(stem_indecies) > 1:
                    stem_words_indecies.append(stem_indecies)
        return stem_words_indecies

    def get_corresponding_letter_index(self, letters, indecies, tgt_r, tgt_c):
        """Right now, a play takes in the parameters - list of letters, list of indecies.
        This is convenient for much of the code where we treat these parameters indepedently,
        however, when we are ready to score, we need to know which letter corresponds with which
        index, which this method gives you"""
        i = 0
        for spot in indecies:
            row = spot[0]
            col = spot[1]
            if row == tgt_r and col == tgt_c:
                return i
            else:
                i += 1
        raise Exception('The row, col provided is not in the index list')


    def get_letter_value(self, letter_char):
        """ Returns the value for the letter drawn - for example 'A' is worth 1 point
        (see Tile class init method for values)"""
        t = Tile(letter_char)
        return t.score

    def score_letter(self, letters, indecies, r, c):
        """ Returns a score for a single letter placement at an r, c
            - if there is a letter on the board already, get the score for that tile
            - if the letter is one you are placing, check for double and triple
              letter score marks
        """
        score = 0
        curr_mark = self.current_state[r][c]
        if (r, c) in set(indecies):
            i = self.get_corresponding_letter_index(letters, indecies, r, c)
            letter = letters[i]
        else:
            letter = curr_mark
        score = self.get_letter_value(letter)
        if curr_mark == DOUBLE_LETTER:
            score *= DOUBLE_SCORE
        elif curr_mark == TRIPLE_LETTER:
            score *= TRIPLE_SCORE
        return score

    def get_word_multipliers(self, indecies):
        """ Gets a list of word multiplier markers that
            currently occupy the spaces you want to place letters on
        """
        word_mults = []
        mult_chars = set({DOUBLE_WORD, TRIPLE_WORD, CENTER_MARKER})
        for spot in indecies:
            r = spot[0]
            c = spot[1]
            curr_mark = self.current_state[r][c]
            if curr_mark in mult_chars:
                word_mults.append(curr_mark)
        return word_mults

    def apply_word_multipliers(self, original_score, word_multipliers):
        """ Given an otherwise completed word score, we apply the word
            multipliers"""
        doubling = set({CENTER_MARKER, DOUBLE_WORD})
        for special_char in word_multipliers:
            if special_char in doubling:
                original_score *= DOUBLE_SCORE
            elif special_char in set({TRIPLE_WORD}):
                original_score *= TRIPLE_SCORE
        final_score = original_score
        return final_score

    def place_tiles(self, letters, indecies):
        """Updates the state of the board"""
        if len(letters) != len(indecies):
            raise Exception(
                'Letters of length {} not equal to indecies of length {}'.format(
                    len(letters), len(indicies)
                )
            )

        for i in xrange(0, len(indecies)):
            (r, c) = indecies[i]
            letter = letters[i]
            self.current_state[r][c] = letter
            self.occupied.add((r, c))

        self.set_bordering(indecies)

    def print_board_current_state(self):  # TODO: Fix indentation of 1-10, 10 diff, etc
        i = 0
        s = ''
        while (i <= 14):
            r = self.current_state[i]
            s += '{0} : {1}'.format(i, r) + '\n'  # TODO: define num chars before printing {1}, "pretty format"
            i += 1
        print s

    def set_bordering(self, indecies):
        for spot in indecies:
            r = spot[0]
            c = spot[1]
            up = (r - 1, c)
            down = (r + 1, c)
            left = (r, c - 1)
            right = (r, c + 1)
            directions = [up, down, left, right]
            for d in directions:
                if self.is_in_bounds([d]):
                    self.bordering.add(d)
            self.bordering = self.bordering - self.occupied

from scrabble.lib.board import Board
from scrabble.lib.state import CENTER_MARKER
from scrabble.lib.state import EMPTY
from scrabble.lib.state import DOUBLE_LETTER
from scrabble.lib.state import DOUBLE_WORD
from scrabble.lib.state import TRIPLE_LETTER
from scrabble.lib.state import TRIPLE_WORD

# TODO: Move the loop into another method in this file but don't call it
# test and pytest won't pick it up
# TODO: do edge cases each in their own test method - test_get_main_word


def test_all_spaces_available():
    b = Board()
    indecies = [(7, 7)]
    assert(b.all_spaces_available(indecies))
    indecies_2 = [(7, 8), (7, 9), (7, 10)]
    b.place_tiles('hih', indecies_2)
    assert(not b.all_spaces_available(indecies_2))


def test_board_setup():
    b = Board()
    assert(len(b.occupied) == 0)
    assert(len(b.bordering) == 1)
    assert((7, 7) in b.bordering)


def test_board_init_special_char_cnt(n=15):
    """ Checks if the board has the correct numbers of special
       characters such as *, Triple Word Marker, etc """
    b = Board()
    assert(len(b.current_state) == n)
    for r in b.current_state:
        assert(len(r) == n)
    cntr_cnt = 0
    empty_cnt = 0
    dl_cnt = 0
    dw_cnt = 0
    tl_cnt = 0
    tw_cnt = 0
    for r in xrange(0, len(b.current_state)):
        for c in xrange(0, len(b.current_state[r])):
            val = b.current_state[r][c]
            if val == TRIPLE_WORD:
                tw_cnt += 1
            elif val == DOUBLE_WORD:
                dw_cnt += 1
            elif val == TRIPLE_LETTER:
                tl_cnt += 1
            elif val == DOUBLE_LETTER:
                dl_cnt += 1
            elif val == CENTER_MARKER:
                cntr_cnt += 1
            elif val == '':
                empty_cnt += 1
            else:
                return False
                # Raise error
    assert(tw_cnt == 8)
    assert(dw_cnt == 16)
    assert(tl_cnt == 12)
    assert(dl_cnt == 24)
    assert(cntr_cnt == 1)
    special_chars = cntr_cnt + dl_cnt + dw_cnt + tl_cnt + tw_cnt
    assert(empty_cnt == (n*n - special_chars))


def test_is_bordering_with_other_words():
    b = Board()
    center_row = [(7, 7), (7, 8), (7, 9), (7, 10), (7, 11)]
    b.place_tiles('hello', center_row)
    assert(not b.is_bordering_with_other_words([(7, 7)]))
    assert(b.is_bordering_with_other_words([(6, 7)]))


def test_is_in_bounds():
    b = Board()
    assert(not b.is_in_bounds([(-1, -1)]))
    assert(b.is_in_bounds([(0, 0)]))
    assert(not b.is_in_bounds([(15, 15)]))


def test_is_in_single_col():
    b = Board()
    one_elt = [(0, 0)]
    assert(b.is_in_single_column(one_elt))
    row = [(0, 0), (0, 1)]
    assert(not b.is_in_single_column(row))
    col = [(0, 1), (1, 1)]
    assert(b.is_in_single_column(col))
    diag = [(0, 1), (1, 0)]
    assert(not b.is_in_single_column(diag))
    diag_2 = [(0, 15), (15, 0)]
    assert(not b.is_in_single_column(diag_2))
    long_row = [(0, 1), (0, 2), (0, 3), (0, 16)]
    assert(not b.is_in_single_column(long_row))
    long_col = [(1, 0), (2, 0), (3, 0), (16, 0)]  # Not Continuous
    assert(b.is_in_single_column(long_col))


def test_is_in_single_row():
    b = Board()
    one_elt = [(0, 0)]
    assert(b.is_in_single_row(one_elt))
    row = [(0, 0), (0, 1)]
    assert(b.is_in_single_row(row))
    col = [(0, 1), (1, 1)]
    assert(not b.is_in_single_row(col))
    diag = [(0, 1), (1, 0)]
    assert(not b.is_in_single_row(diag))
    diag_2 = [(0, 15), (15, 15)]
    assert(not b.is_in_single_row(diag_2))
    long_row = [(0, 1), (0, 2), (0, 3), (0, 16)]
    assert(b.is_in_single_row(long_row))


def test_place_tiles():
    letters = 'hi'
    indecies = [(7, 7), (7, 8)]
    b = Board()
    assert(len(b.occupied) == 0)
    assert(len(b.bordering) == 1)  # Just center
    b.place_tiles(letters, indecies)
    assert(len(set(indecies).intersection(b.bordering)) == 0)
    assert(b.occupied == set(indecies))
    indecies_vert = [(4, 7), (5, 7), (6, 7)]
    b.place_tiles('who', indecies_vert)
    new_occ = set(indecies_vert).union(set(indecies))
    assert(b.occupied == new_occ)
    assert(b.bordering.intersection(new_occ) == set())


def test_get_potential_word():
    letters = 'at'
    indecies = [(7, 7), (7, 8)]
    b = Board()
    assert(b.get_potential_word(7, 7, 7, 8, 'at') == 'at')
    b.place_tiles(letters, indecies)
    assert(b.get_potential_word(7, 7, 7, 8, 'at') == 'at')
    b.place_tiles('cs', [(7, 6), (7, 9)])
    assert(b.get_potential_word(7, 7, 6, 9, 'cs') == 'cats')
    b = Board()
    assert(b.get_potential_word(8, 11, 10, 10, 'nake') == 'nake')
    # Refresh
    letters = 'cat'
    indecies = [(7, 7), (7, 8), (7, 9)]
    b = Board()
    b.place_tiles(letters, indecies)
    letters_2 = 'snake'
    indecies_2 = [(7, 10), (8, 10), (9, 10), (10, 10), (11, 10)]
    assert(b.get_potential_word(7, 11, 10, 10, letters_2) == 'snake')


def test_get_row_and_col_bounds():  # TODO: comments as to what you're testing
    b = Board()
    letters = 'at'
    indecies = [(7, 7), (7, 8)]
    assert(b.get_left_column(letters, indecies, 7, 7) == 7)
    assert(b.get_right_column(letters, indecies, 7, 7) == 8)
    assert(b.get_top_row(letters, indecies, 7, 7) == 7)
    assert(b.get_bottom_row(letters, indecies, 7, 7) == 7)
    b.place_tiles(letters, indecies)
    assert(b.get_left_column(letters, indecies, 7, 7) == 7)
    assert(b.get_right_column(letters, indecies, 7, 7) == 8)
    assert(b.get_top_row(letters, indecies, 7, 7) == 7)
    assert(b.get_bottom_row(letters, indecies, 7, 7) == 7)
    letters = 'c'
    indecies = [(7, 6)]
    assert(b.get_left_column(letters, indecies, 7, 7) == 6)
    assert(b.get_right_column(letters, indecies, 7, 7) == 8)
    assert(b.get_top_row(letters, indecies, 7, 7) == 7)
    assert(b.get_bottom_row(letters, indecies, 7, 7) == 7)
    b.place_tiles(letters, indecies)
    assert(b.get_left_column(letters, indecies, 7, 7) == 6)
    assert(b.get_right_column(letters, indecies, 7, 7) == 8)
    assert(b.get_top_row(letters, indecies, 7, 7) == 7)
    assert(b.get_bottom_row(letters, indecies, 7, 7) == 7)
    letters = 'snake'
    indecies = [(7, 9), (8, 9), (9, 9), (10, 9), (11, 9)]
    # on the first letter of cats
    assert(b.get_left_column(letters, indecies, 7, 7) == 6)
    assert(b.get_right_column(letters, indecies, 7, 7) == 9)
    assert(b.get_top_row(letters, indecies, 7, 7) == 7)
    assert(b.get_bottom_row(letters, indecies, 7, 7) == 7)
    # from snake
    assert(b.get_left_column(letters, indecies, 8, 9) == 9)
    assert(b.get_right_column(letters, indecies, 8, 9) == 9)
    assert(b.get_top_row(letters, indecies, 8, 9) == 7)
    assert(b.get_bottom_row(letters, indecies, 8, 9) == 11)


def test_get_main_word():
    letters = 'cat'
    indecies = [(7, 7), (7, 8), (7, 9)]
    b = Board()
    assert(b.get_main_word(letters, indecies) == 'cat')
    b.place_tiles(letters, indecies)
    assert(b.get_main_word(letters, indecies) == 'cat')
    letters_2 = 'snake'
    indecies_2 = [(7, 10), (8, 10), (9, 10), (10, 10), (11, 10)]
    assert(b.get_main_word(letters_2, indecies_2) == 'snake')


def test_get_stemming_words():
    b = Board()
    letters = 'cat'
    indecies = [(7, 7), (7, 8), (7, 9)]
    b.place_tiles(letters, indecies)
    letters_2 = 'snake'
    indecies_2 = [(7, 10), (8, 10), (9, 10), (10, 10), (11, 10)]
    assert(b.get_stemming_words(letters_2, indecies_2) == ['cats'])


def test_is_word():
    b = Board()
    assert(b.is_word('hello'))


def test_is_valid_move():
    b = Board()
    letters = 'cat'
    indecies = [(7, 7), (7, 8), (7, 9)]
    assert(b.is_valid_move(letters, indecies))
    letters = 'snake'
    indecies = [(7, 10), (8, 10), (9, 10), (10, 10), (11, 10)]
    assert(not b.is_valid_move(letters, indecies))  # Isn't starting via the center
    letters = 'snake'
    indecies = [(7, 24)]
    assert(not b.is_valid_move(letters, indecies))  # Isn't starting via the center


def test_letter_score():
    b = Board()
    assert(b.get_letter_value('O') == 1)


def test_get_corresponding_letter_index():
    b = Board()
    letters = 'HELLO'
    indecies = [(7, 7), (7, 8), (7, 9), (7, 10), (7, 11)]
    assert(b.get_corresponding_letter_index(letters, indecies, 7, 7) == 0)


def test_get_score_letter():
    b = Board()
    letters = 'HELLO'
    indecies = [(7, 7), (7, 8), (7, 9), (7, 10), (7, 11)]
    assert(b.score_letter(letters, indecies, 7, 7) == 4)
    assert(b.score_letter(letters, indecies, 7, 8) == 1)
    assert(b.score_letter(letters, indecies, 7, 9) == 1)
    assert(b.score_letter(letters, indecies, 7, 10) == 1)
    assert(b.score_letter(letters, indecies, 7, 11) == 2)  # Double Letter Score there


def test_get_index_list_main_word():
    b = Board()
    letters = 'HELLO'
    indecies = [(7, 7), (7, 8), (7, 9), (7, 10), (7, 11)]
    new_index_list = b.get_index_list_main_word(letters, indecies)
    assert(new_index_list == indecies)


def test_score_main_word():
    b = Board()
    letters = 'HELLO'
    indecies = [(7, 7), (7, 8), (7, 9), (7, 10), (7, 11)]
    score = b.get_main_word_score(letters, indecies)
    assert(score == 18)  # Center mark at 7,7 and double letter at 7.11

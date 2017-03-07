CENTER_MARKER = '*'
EMPTY = ''
DOUBLE_LETTER = 'DL'
DOUBLE_WORD = 'DW'
TRIPLE_LETTER = 'TL'
TRIPLE_WORD = 'TW'


def get_initial_board_state():  # TODO: Refact. to read from an nxn (++rdable)
    board = []
    for i in xrange(0, 15):  # TODO: hardcoded things below. Also add some comments.
        if i == 7:
            row = [EMPTY]*7 + [CENTER_MARKER] + [EMPTY]*7
        else:
            row = [EMPTY]*15
        board.append(row)
    TW_s = set({(0, 0), (0, 7), (0, 14),
                (7, 0), (7, 14),
                (14, 0), (14, 7), (14, 14)})
    board = set_board_special_chars(board, TW_s, TRIPLE_WORD)
    DW_s = set({(1, 1), (1, 14),
                (2, 2), (2, 13),
                (3, 3), (3, 12),
                (4, 4), (4, 11),
                (10, 4), (10, 11),
                (11, 3), (11, 12),
                (12, 2), (12, 13),
                (13, 1), (13, 14)})
    board = set_board_special_chars(board, DW_s, DOUBLE_WORD)
    DL_s = set({(0, 3), (0, 11),
                (2, 6), (2, 8),
                (3, 0), (3, 7), (3, 14),
                (6, 2), (6, 6), (6, 8), (6, 12),
                (7, 3), (7, 11),
                (8, 2), (8, 6), (8, 8), (8, 12),
                (11, 0), (11, 7), (11, 14),
                (12, 6), (12, 8),
                (14, 3), (14, 11)})
    board = set_board_special_chars(board, DL_s, DOUBLE_LETTER)
    TL_s = set({(1, 5), (1, 9),
                (5, 1), (5, 5), (5, 9), (5, 13),
                (9, 1), (9, 5), (9, 9), (9, 13),
                (13, 5), (13, 9)})
    board = set_board_special_chars(board, TL_s, TRIPLE_LETTER)
    return board


def set_board_special_chars(board, index_set, char_marker):
    for (row, col) in index_set:
        board[row][col] = char_marker
    return board

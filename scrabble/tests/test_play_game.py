from scrabble.lib.bag import Bag
from scrabble.lib.player import Player

from scrabble.lib.play_game import *
from scrabble.lib.bag import Bag
from scrabble.lib.board import Board
from scrabble.lib.player import Player
from scrabble.lib.tile import Tile

from itertools import combinations
from random import randrange

from mock import patch
from unittest import TestCase

PLAY = '1'
PASS = '2'
EXCHANGE = '3'
END_GAME = '4'
MIN_NUM_PLAYERS = 1
MAX_NUM_PLAYERS = 4


class PlayGameTestCase(TestCase):

    @patch('scrabble.lib.play_game.get_input', return_value=PLAY)
    @patch('scrabble.lib.play_game.Game.play_letters', return_value=True)
    def test_game_not_done_play(self, input, play):
        g = Game(['Erica'])
        g.play_turn()
        assert(not g.game_done)

    @patch('scrabble.lib.play_game.get_input', return_value=PASS)
    def test_game_not_done_pass(self, input):
        g = Game(['Erica'])
        g.play_turn()
        assert(not g.game_done)

    @patch('scrabble.lib.play_game.get_input', return_value=EXCHANGE)
    @patch('scrabble.lib.play_game.Game.exchange_letters', return_value=True)
    def test_game_not_done_exchange(self, input, exchange):
        g = Game(['Erica'])
        g.play_turn()
        assert(not g.game_done)

    @patch('scrabble.lib.play_game.get_input', return_value=END_GAME)
    def test_game_done_end(self, input):
        g = Game(['Erica'])
        g.play_turn()
        assert(g.game_done)

    @patch('scrabble.lib.play_game.get_letter_input_from_player', return_value='H E L L O')
    @patch('scrabble.lib.play_game.get_indecies_input_from_player', return_value='(7,7) (7,8) (7,9) (7,10) (7,11)')
    def test_play_letters_a(self, letters, indecies):
        # Initial Move of Hello
        g = Game(['Erica', 'Jaeger'])
        assert(g.curr_player.score == 0)
        assert(len(g.players) == 2)
        assert(g.board.bordering == set({(7, 7)}))
        assert(len(g.board.occupied) == 0)
        assert(g.curr_player.name == 'Erica')
        g.play_letters()
        assert(not g.game_done)
        assert(g.curr_player.name == 'Erica')
        assert(g.players[0].score > 0)

    @patch('scrabble.lib.play_game.get_letter_input_from_player', return_value='W A G')
    @patch(
        'scrabble.lib.play_game.get_indecies_input_from_player',
        return_value='(5,7) (6,7) (7,7)'
    )
    def test_play_letters_b(self, letters, indecies):
        # Initial Move of Hello
        g = Game(['Erica'])
        g.play_letters()
        assert(g.game_done is False)
        assert(g.curr_player.name == 'Erica')
        assert(g.players[0].score == 14)

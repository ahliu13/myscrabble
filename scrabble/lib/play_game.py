from scrabble.lib.bag import Bag
from scrabble.lib.board import Board
from scrabble.lib.player import Player
from scrabble.lib.player import MAX_TRAY_LEN
from scrabble.lib.tile import Tile

from ast import literal_eval as make_tuple
from random import randrange

# TODO: Update get_first_player_index to be aligned with Hasbro rules

PLAY = '1'
PASS = '2'
EXCHANGE = '3'
END_GAME = '4'
MIN_NUM_PLAYERS = 1
MAX_NUM_PLAYERS = 4


class Game:
    def __init__(self, player_names):
        self.bag = Bag()
        self.board = Board()
        self.players = []
        self.set_player_list(player_names)
        self.game_done = False
        self.player_turn_index = 0
        self.set_curr_player()
        self.fill_player_trays()

    def set_player_list(self, player_names):
        for name in player_names:
            self.players.append(Player(name))

    def fill_player_trays(self):
        for p in self.players:
            while len(p.tray) != MAX_TRAY_LEN:
                letter = self.bag.draw_random_letter()
                p.tray.append(letter)

    def set_curr_player(self):
        self.curr_player = self.players[0]  # TODO: update with get first player index(players, bag)

    def play_turn(self):
        """ Once we have set the current player, this logic directs the input to the appropriate
        submethod of play letters, pass, exchange, or end game"""
        self.print_turn_prompt()
        option = get_input()
        while option not in set({PLAY, PASS, EXCHANGE, END_GAME}):
            print 'Looks like the number you entered was invalid'
            print 'Please try again or hit ctrl C to abandon the game'
            option = get_input()
        if option == PLAY:
            self.play_letters()
        elif option == PASS:
            self.pass_turn()
        elif option == EXCHANGE:
            self.exchange_letters()
        else:
            self.game_done = True

    def print_turn_prompt(self):
        print 'Your turn {0}'.format(self.curr_player.name)
        print 'The board is:'
        print 'Your tray is {0}'.format(self.curr_player.tray)
        self.board.print_board_current_state()
        print 'Please Enter One of the Following Options:'
        print '{0}: Play'.format(PLAY)
        print '{0}: Pass'.format(PASS)
        print '{0}: Exchange Tiles'.format(EXCHANGE)
        print '{0}: End Game & Tally Score'.format(END_GAME)

    def play_letters(self):
        """ If the player opts to lay tiles, we enter here"""
        is_play_done = False
        while (not is_play_done):
            print 'Please enter the letters you would like to play capitalized and seperated by spaces'
            print 'For example A A B C'
            letters = get_letter_input_from_player().split()
            print 'Please enter the indecies you would like to play in the from (r,c) seperated by whitespace'
            print 'For example (1,2) (1,3) (1,4)'
            indecies_s = get_indecies_input_from_player().split()
            indecies = []
            for i in indecies_s:
                indecies.append(make_tuple(i))
            if self.board.is_valid_move(letters, indecies):
                score = self.board.score_play(letters, indecies)
                self.curr_player.score += score
                self.board.place_tiles(letters, indecies)
                for letter in letters:
                    self.curr_player.remove_letter(letter)
                # remove the tiles from the player tray
                self.refill_curr_player_tray()
                is_play_done = True
                print ''
                print (
                    'Awesome, you placed the letters, got a score of {0} and the '
                    'board is the following and now the board is the following'
                ).format(score)
                self.board.print_board_current_state()
                print ''
            else:
                print 'Looks like you may have entered the wrong format of either the letters or indecies - please try again'

    def pass_turn(self):
        print 'Passing'

    def exchange_letters(self):
        """The player provides a list of letters they would like to exchange - if valid,
        we swap them out for new ones"""
        is_exchange_done = False
        while (not is_exchange_done):
            print 'Please enter a list of tiles you would like to swap out'
            tiles = get_input().split()
            if self.can_exchange_tiles(tiles):
                for t in tiles:
                    self.curr_player.remove_letter(t)
                    self.bag.insert_letter(t)
                    new_lett = self.bag.draw_random_letter()
                    self.curr_player.tray.append(new_lett)
                print 'Your new tray is {0}'.format(self.curr_player.tray)
                is_exchange_done = True
                print
            else:
                print 'Oops, looks like your entry was invalid'

    def can_exchange_tiles(self, list_to_exchange):
        """ Checks whether the given list of letters to
            exchange are in the letter tray of the player
        """
        player_tray_set = set(self.curr_player.tray)
        for letter in list_to_exchange:
            if letter not in player_tray_set:
                return False
        return True

    def refill_curr_player_tray(self):
        """Re-fills the current player's tray once they have played letters"""
        while len(self.curr_player.tray) < MAX_TRAY_LEN:
            letter = self.bag.draw_random_letter()
            self.curr_player.tray.append(letter)

    def tally_game_score(self):
        """Tallys up and prints the player scores"""
        print 'Game is over - scores are as follows'
        scores = {}
        for p in self.players:
            if p.score in scores:
                scores[p.score].append(p.name)
            else:
                scores[p.score] = [p.name]
        print str(scores)

    def update_current_player(self):
        """We have an array of players - we increment till we reach
        the end of the list, then wrap back around
        """
        i = self.player_turn_index
        i = i + 1
        i = i % len(self.players)
        self.player_turn_index = i
        self.curr_player = self.players[i]

    def update_game_done(self):
        if len(self.curr_player.tray) == 0 and len(self.bag.letters) == 0:
            self.game_done = True


def get_input():
    return raw_input()


def get_letter_input_from_player():
    return raw_input()


def get_indecies_input_from_player():
    return raw_input()


def play_game(player_names):
    g = Game(player_names)
    b = Board()
    while (not g.game_done):
        g.play_turn()
        g.update_current_player()
        g.update_game_done()
    g.tally_game_score()
    return


def get_name_list():
    """ Gets a list of names from the CLI and passes them into the play_game() method"""
    print """Welcome to Scrabble! Please enter a list of up to {0} player names,
    seperated by a space. For example, 'Erica Carlos Devon Jaeger' is
    valid, while the name 'He Su' would render as 2 names.
    """.format(MAX_NUM_PLAYERS)
    are_names = False
    while not are_names:
        names = raw_input()
        try:
            name_list = names.split()
            if len(name_list) < MIN_NUM_PLAYERS:
                raise ValueError("""Looks like you entered too few players.
                    Please try again.""")
                continue
            elif len(name_list) > MAX_NUM_PLAYERS:
                raise ValueError("""Looks like you entered more than {0} players,
                    which is the maximum allowed. Please try again.
                    """.format(MAX_NUM_PLAYERS))
            else:
                are_names = True
                return name_list
        except ValueError:
            print """Oops - looks like that list of names wasn't correct. Please
                try again."""

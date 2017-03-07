from scrabble.lib.play_game import get_name_list
from scrabble.lib.play_game import play_game


if __name__ == '__main__':
    names = get_name_list()
    play_game(names)

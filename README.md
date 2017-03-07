# CLI Scrabble

A lightweight Scrabble backend. Played via CLI. Follows [Hasbro rules] (http://scrabble.hasbro.com/en-us) unless otherwise specified.

## Getting Started
```
>> virtualenv venv
>> source venv/bin/activate
>> touch scrabble/__init__.py
>> touch scrabble/lib/__init__.py
>> touch scrabble/tests/__init__.py
>> pip install -r requirements.txt
>> python setup.py develop
>> python main.py
```

## Running the tests
```
>> pip install py.test
>> py.test --ignore venv
```

## Built With

* Python 2.7.11
* English Dictionary with [PyEnchant](https://pypi.python.org/pypi/pyenchant)

## Versioning

* Version 0.1

## Authors

* **Erica Dohring** - [Github](https://github.com/ericadohring)

## Design Notes

# Bordering
The 'bordering' set in the board class is used to handily keep track of which moves (i.e. index locations) are valid to do next - for example, say we only have 1 horizontal word on the board 'hello'. The next move must have a tile that borderes with the letters of 'hello', else it's invalid. On the first move, we must touch the center tile, so we initialize our board with bordering = set(CENTER).

* Main Words vs. Stemming Words
When making a move, the player provides a list of indecies in which they would like to place their tiles. Granted it's a valid input, This will either be on a horizontal or vertical axis, with an input of 1 defaulting to horizontal. We call the potential word make by laying your tiles on that axis the "main word," and any words created on the opposite axis "stemming words."
Examples)
- Say you provide the indecies (6,7) and (6, 10) and want to play the letters 'c' and 's' on the outside of the existing 'at' which are placed at (6, 8) and (6, 9) respectively, your main word would be 'cats'
- Say the word 'hell' was vertically placed on the board. A player proceeds to play 'oops' horizontally bellow 'hell', making 'hell' into 'hello'. The main word would be 'oops' and the stemming word would be 'hello.'

* Definition of a Play Turn vs. Play Letters
A player has 4 options on a turn - play, pass, exchange, or end the game. "Play turn" means to select
within those 4, while "play letters" means to to attempt to lay tile down rather than pass, exchange, or end the game.

* Tiles vs. Letters
In the bag class, we initialize the letters with their frequencies - for example we have 2 instances of B. The tile class contain's that letter's score which is 3

* Overall Board Structure and Play Logic
The main interesting logic of this project lies in the Board class. We've chosen to represent the state of the board with a 2D array and keep track of the occupied spaces with a set for ease
of checking. If a player suggests a list of letters and indecies of which he/she would like to place over, we then must
1. Check the move is valid.
2. Score the move.
3. Update the state of the board and the game.

1 and 2 have many helper methods, which is part of what makes the board.py file so long - We've tried to break it up into chunks for easier readability by those three themes with any shared methods at the bottom.


## Future Work

- Refactor intial player selection to align with Hasbro rules - right now we select the first player that enters their name, while we want to select more randomly.
- Refactor the board class to make it more readable.
- Adding funcionality for blank tiles. Currently, we have 2 extra A's rather than the blank tiles. To implement, we would need to update the bag initialization as well as the board logic.
See comments in `board.py` for more information.

## Acknowledgments

* Huge thanks to Carlos, Hassan, and Devon :)

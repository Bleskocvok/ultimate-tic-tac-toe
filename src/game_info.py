
EXAMPLE = """
```css

- EXAMPLE TURN
==============


1. Player X places X in a corner in any board
---------
| . . X |
| . . . |
| . . . |
---------


2. Player O now has to place O in the board located in the same corner
(The selected board is marked)

-----------------=======-
| . . . | . . . [ . . . ]
| . . . | . . . [ . . . ]
| . . . | . . . [ . . . ]
-----------------=======-
| . . X | . . . | . . . |
| . . . | . . . | . . . |
| . . . | . . . | . . . |
-------------------------
| . . . | . . . | . . . |
| . . . | . . . | . . . |
| . . . | . . . | . . . |
-------------------------

Player O chooses the middle square

---=======-
. [ . . . ]
. [ . O . ]
. [ . . . ]
---=======-
. | . . . |


3. Player X now has to place X in the middle board
(The selected board is marked)

-------------------------
| . . . | . . . | . . . |
| . . . | . . . | . O . |
| . . . | . . . | . . . |
---------=======---------
| . . X [ . . . ] . . . |
| . . . [ . . . ] . . . |
| . . . [ . . . ] . . . |
---------=======---------
| . . . | . . . | . . . |
| . . . | . . . | . . . |
| . . . | . . . | . . . |
-------------------------

```
"""

RULES = """
```diff
- RULES
- =====

(Game usually known as Ultimate-Tic-Tac-Toe)

The game is like 3x3 tic-tac-toe games in one big tic-tac-toe.

The game consists of 3x3 boards and each has 3x3 squares (represented as dots).
Each board is a game of tic-tac-toe in itself.

You need the win the 3x3 game of tic-tac-toe to win a particular board.

Players take turns placing symbols in the squares/dots.

The first player chooses which board and which square to place their
symbol in. Depending on which SQUARE they choose, the second player has to place their
symbol in the corresponding BOARD.


- One board:
---------
| . . . |
| . . O |
| X . . |
---------


- Board won by player X:
---------         ---------
| X . . |         | X X X |
| X . O |   -->   | X X X |
| X O . |         | X X X |
---------         ---------

For more clarity on how the game works, try:

{}

Or

{}

to see a game of the bot playing against itself play out.
```
"""


class GameInfo:

    @staticmethod
    def example() -> str:
        return EXAMPLE

    @staticmethod
    def rules(example_cmd: str, bot_vs_cmd: str) -> str:
        return RULES.format(example_cmd, bot_vs_cmd)

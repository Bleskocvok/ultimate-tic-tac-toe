#!/usr/bin/env python3


import discord
from discord.ext import commands

from session_manager import *


class Controls:
    # first row
    UP_LEFT     = "\N{north west arrow}"
    UP          = "\N{upwards black arrow}"
    UP_RIGHT    = "\N{north east arrow}"
    # second row
    LEFT        = "\N{leftwards black arrow}"
    MIDDLE      = "\N{radio button}"
    RIGHT       = "\N{black rightwards arrow}"
    # third row
    DOWN_LEFT   = "\N{south west arrow}"
    DOWN        = "\N{downwards black arrow}"
    DOWN_RIGHT  = "\N{south east arrow}"

    LST = [
        UP_LEFT, UP, UP_RIGHT, LEFT, MIDDLE, RIGHT, DOWN_LEFT, DOWN, DOWN_RIGHT
    ]

    @staticmethod
    def idx(msg) -> int:
        for i in range(len(Controls.LST)):
            if msg == Controls.LST[i]:
                return i
        return -1


class UltraTicTacCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.manager = SessionManager()

    @commands.Cog.listener()
    async def on_comman_error(self, ctx, error):
        print(f"ERROR: {error}", flush=True)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Connected as {self.bot.user.name}")

    @commands.command(help='')
    async def start(self, ctx, opponent: discord.Member):
        msg = await ctx.send(
            "`Creating game...`"
        )
        session = Session(msg, ctx.author, opponent)
        self.manager.add(session)
        for react in Controls.LST:
            await msg.add_reaction(f"{react}")
        await msg.edit(content=session.view())

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        # it's this bot's reaction
        if self.bot.user.id == user.id:
            return

        # get the session
        session = self.manager.get(reaction.message)
        if session is None:
            return

        # send the input (pressed reaction)
        session.input(user, Controls.idx(reaction.emoji))

        # view the change
        await session.message.edit(content=session.view())

        # remove the reaction so it can be pressed again
        await reaction.remove(user)

        if session.game_over():
            self.manager.remove(session)

    @commands.command(help='What are the rules?')
    async def rules(self, ctx):
        await ctx.send(
f"""
```diff
- RULES
- =====

(Game usually known as Ultimate-Tic-Tac-Toe)

The game is like 3x3 tic-tac-toe games in one big tic-tac-toe.

The game consists of 3x3 boards and each has 3x3 squares (represented as dots).
Each board is a game of tic-tac-toe in itself.

You need the win the 3x3 game of tic-tac-toe to win a particular board.

Players take turns placing symbols in the squares/dots.

The first player chooses which board to and which square to place their
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

For more clarity on how the game works try:

{self.bot.command_prefix}example

```
""")

    @commands.command(help='An example of one turn')
    async def example(self, ctx):
        await ctx.send(
"""
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

-=======-
[ . . . ]
[ . O . ]
[ . . . ]
-=======-


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
""")

#!/usr/bin/env python3


import discord
from discord.ext import commands

from session_manager import *
from src.game_info import GameInfo


class Controls:
    # first row
    UP_LEFT     = "\N{north west arrow}"
    UP          = "\N{up-pointing small red triangle}"
    UP_RIGHT    = "\N{north east arrow}"
    # second row
    LEFT        = "\N{black left-pointing triangle}"
    MIDDLE      = "\N{radio button}"
    RIGHT       = "\N{black right-pointing triangle}"
    # third row
    DOWN_LEFT   = "\N{south west arrow}"
    DOWN        = "\N{down-pointing small red triangle}"
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

    # @commands.Cog.listener()
    # async def on_command_error(self, ctx, error):
    #     print(f"ERROR: {error}", flush=True)

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

        # clear reactions after the game
        if session.game_over():
            await session.message.clear_reactions()
            self.manager.remove(session)

    @commands.command(help='What are the rules?')
    async def rules(self, ctx):
        await ctx.send(GameInfo.rules(f"{self.bot.command_prefix}example"))

    @commands.command(help='An example of one turn')
    async def example(self, ctx):
        await ctx.send(GameInfo.example())

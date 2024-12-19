#!/usr/bin/env python3


from sys import stderr
from typing import Optional
import discord
from discord.ext import commands, tasks
import asyncio

from .session_manager import Session, SessionManager
from .game_info import GameInfo
from .random_ai import RandomAi


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
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.manager = SessionManager()

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        print(f"ERROR: {error}", flush=True, file=stderr)
        await ctx.send(f"`Error: {error}`")

    @commands.Cog.listener()
    async def on_ready(self):
        assert self.bot.user
        print(f"Connected as {self.bot.user.name}", flush=True)
        await self.make_ai_plays.start()

    @tasks.loop(seconds=2)
    async def make_ai_plays(self):
        assert self.bot.user
        over = []
        for _, ses in self.manager.sessions.items():
            if ses.is_playing(self.bot.user.id):
                game = ses.game
                ai = RandomAi(game.playing().name)
                x: int = 0
                x: int = 0
                if game.should_select():
                    x, y = ai.pick_board(game.board())
                else:
                    x, y = ai.pick_box(game.board())
                assert ses.input(self.bot.user.id, y * 3 + x)
                await ses.message.edit(content=ses.view())
                if ses.game_over():
                    over.append(ses)

        for ses in over:
            await self._cleanup(ses)

    @commands.command(help='')
    async def start_bot_vs_bot(self, ctx):
        assert self.bot.user
        msg = await ctx.send(
            "`Creating game...`"
        )
        user = self.bot.user
        session = Session(msg, user, user)
        self.manager.add(session)
        for react in Controls.LST:
            await msg.add_reaction(f"{react}")
        await msg.edit(content=session.view())

    @commands.command(help='')
    async def start(self, ctx, opponent: Optional[discord.User]):
        assert self.bot.user
        msg = await ctx.send(
            "`Creating game...`"
        )
        opponent_user = opponent if opponent else self.bot.user
        session = Session(msg, ctx.author, opponent_user)
        self.manager.add(session)
        for react in Controls.LST:
            await msg.add_reaction(f"{react}")
        await msg.edit(content=session.view())

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user):
        assert self.bot.user

        # it's this bot's reaction
        if self.bot.user.id == user.id:
            return

        # get the session
        session = self.manager.get(reaction.message)
        if session is None:
            return

        # send the input (pressed reaction)
        session.input(user.id, Controls.idx(reaction.emoji))

        # view the change
        await session.message.edit(content=session.view())

        # remove the reaction so it can be pressed again
        await reaction.remove(user)

        if session.game_over():
            await self._cleanup(session)

    async def _refetch_messaage(self, msg: discord.Message) -> discord.Message:
        chnl = await self.bot.fetch_channel(msg.channel.id)
        msg = await chnl.fetch_message(msg.id) # type: ignore
        return msg

    async def _cleanup(self, session: Session):
        msg = await self._refetch_messaage(session.message)
        removal = []
        for react in msg.reactions:
            async for user in react.users():
                removal.append(react.remove(user))
        await asyncio.gather(*removal)
        self.manager.remove(session)

    @commands.command(help='What are the rules?')
    async def rules(self, ctx):
        await ctx.send(GameInfo.rules(f"{self.bot.command_prefix}example",
                                      f"{self.bot.command_prefix}start_bot_vs_bot"))

    @commands.command(help='An example of one turn')
    async def example(self, ctx):
        await ctx.send(GameInfo.example())

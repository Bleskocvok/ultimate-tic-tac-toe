#!/usr/bin/env python3


from discord.ext import commands
from typing import Dict
import discord
import random


from game import *


class Session:
    def __init__(self, message, user, opponent):
        self.message = message
        self.user = user
        self.opponent = opponent
        self.game = Game(first=random.choice([Box.X, Box.O]))

    def _get_player(self, box: Box) -> discord.Member:
        return self.user if box == Box.X else self.opponent

    def _key_to_coord(self, key: int) -> Coord:
        x = key % 3
        y = key // 3
        return (x, y)

    def input(self, person, key: int):
        if self.game.state() != State.PLAYING:
            return
        if person != self._get_player(self.game.playing()):
            return
        coord = self._key_to_coord(key)
        try:
            if self.game.should_select():
                self.game.select(coord)
            else:
                self.game.place(coord)
                self.game.next_round()
        except GameError:
            pass

    def game_over(self) -> bool:
        return self.game.state() != State.PLAYING

    def view(self) -> str:
        player = self._get_player(self.game.playing())

        phase = ""
        if self.game.state() == State.X_WON:
            phase = f"**<@{self._get_player(Box.X).id}> ({Box.X}) WON!**"
        elif self.game.state() == State.O_WON:
            phase = f"**<@{self._get_player(Box.O).id}> ({Box.O}) WON!**"
        elif self.game.state() == State.DRAW:
            phase = f"**IT'S A DRAW! GAME OVER**"
        elif self.game.should_select():
            phase = "`Select board`"
        else:
            phase = f"`Select square to place:` **{self.game.playing()}**"

        turn_msg = f"**Waiting for <@{player.id}>'s turn:**" if not self.game_over() else "Game ended"

        con =\
f"""\
*Playing: **{self.user.name}** (**{Box.X}**) vs. **{self.opponent.name}** (**{Box.O}**)*
*-----------------------------------------------------*

```css
{self.game.board()}
```
{turn_msg}
{phase}

"""
        return con


class SessionManager:
    def __init__(self):
        self.sessions: Dict[int, Session] = dict()

    def get(self, message) -> Optional[Session]:
        return self.sessions[message.id]

    def add(self, session: Session):
        self.sessions[session.message.id] = session

    def remove(self, session):
        del self.sessions[session.message.id]

#!/usr/bin/env python3


from typing import Dict
import discord
import random


from .game import *


class Session:
    def __init__(self, message: discord.Message, user, opponent: discord.User
                                                         | discord.ClientUser):
        self.message = message
        self.user = user
        self.opponent = opponent
        self.game = Game(first=random.choice([Box.X, Box.O]))

    def _get_player(self, box: Box) -> discord.User | discord.ClientUser:
        return self.user if box == Box.X else self.opponent

    def _key_to_coord(self, key: int) -> Coord:
        x = key % 3
        y = key // 3
        return (x, y)

    def playing(self) -> discord.User | discord.ClientUser | None:
        if self.game.playing() == Box.EMPTY:
            return None
        return self._get_player(self.game.playing())

    def input(self, person_id: int, key: int) -> bool:

        if self.game.state() != State.PLAYING:
            return False

        if person_id != self._get_player(self.game.playing()).id:
            return False

        coord = self._key_to_coord(key)
        try:
            if self.game.should_select():
                self.game.select(coord)
            else:
                self.game.place(coord)
                self.game.next_round()
        except GameError:
            return False
        return True

    def game_over(self) -> bool:
        return self.game.state() != State.PLAYING

    def view(self) -> str:
        player = self._get_player(self.game.playing())
        player_x = self._get_player(Box.X).id
        player_o = self._get_player(Box.O).id

        phase = ""
        if self.game.state() == State.X_WON:
            phase = f"**<@{player_x}> ({Box.X}) WON!**"
        elif self.game.state() == State.O_WON:
            phase = f"**<@{player_o}> ({Box.O}) WON!**"
        elif self.game.state() == State.DRAW:
            phase = f"**IT'S A DRAW! GAME OVER**"
        elif self.game.should_select():
            phase = "`Select board`"
        else:
            phase = f"`Select square to place:` **{self.game.playing()}**"

        turn_msg = f"**Waiting for <@{player.id}>'s turn:**" if not self.game_over() else "Game ended"

        opponent_name = self.opponent.name if self.opponent else "AI"
        con =\
f"""\
*Playing: **{self.user.name}** (**{Box.X}**) vs. **{opponent_name}** (**{Box.O}**)*
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

    def get_by_id(self, idx: int) -> Optional[Session]:
        return self.sessions.get(idx)

    def get(self, message: discord.Message) -> Optional[Session]:
        return self.sessions[message.id]

    def add(self, session: Session):
        self.sessions[session.message.id] = session

    def remove(self, session: Session):
        del self.sessions[session.message.id]

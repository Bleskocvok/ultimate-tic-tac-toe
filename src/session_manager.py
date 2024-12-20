#!/usr/bin/env python3


from typing import Dict, Optional
import discord
import random
from datetime import datetime

from .game import Game, State, GameError
from .abstract_board import Box, Coord


class Session:

    EXPIRATION_SECONDS: int = 3600

    def __init__(self, message: discord.Message, user, opponent: discord.User
                                                         | discord.ClientUser):
        self.message = message
        self.user = user
        self.opponent = opponent
        self.game = Game(first=random.choice([Box.X, Box.O]))
        self.last_action: datetime = datetime.now()

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

    def is_playing(self, ident: int) -> bool:
        if self.playing() is None:
            return False
        return self.playing().id == ident # type: ignore

    def input(self, person_id: int, key: int) -> bool:

        if self.game.state() != State.PLAYING:
            return False

        if person_id != self._get_player(self.game.playing()).id:
            return False

        self.last_action = datetime.now()

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

    def expired(self) -> bool:
        now = datetime.now()
        diff = now - self.last_action
        return diff.total_seconds() >= Session.EXPIRATION_SECONDS

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
        elif self.expired():
            phase = "`GAME EXPIRED`"
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

    def get_by_id(self, idx: int) -> Optional[Session]:
        return self.sessions.get(idx)

    def get(self, message: discord.Message) -> Optional[Session]:
        return self.sessions.get(message.id)

    def add(self, session: Session):
        self.sessions[session.message.id] = session

    def remove(self, session: Session):
        del self.sessions[session.message.id]

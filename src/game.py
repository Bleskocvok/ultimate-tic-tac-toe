#!/usr/bin/env python3


from typing import List

from .abstract_board import Box, State, Coord
from .board import Board


class GameError(Exception):
    pass


'''The main interface.
'''
class Game:
    def __init__(self, *, first=None, board=None, selected=None):
        self._board = Board() if board is None else board
        self._playing = Box.X if first is None else first
        self.status = State.PLAYING
        self.placed = False
        self._board.selected = Board.UNSELECTED if selected is None else selected
        # evaluate current state (if there is a winner already)
        self._evaluate()

    def next_round(self):
        if not self.placed:
            raise GameError("Current player hasn't played")
        self._playing = self._playing.invert()
        self.placed = False
        self._evaluate()
        if not self._board.is_available(self._board.selected):
            self._board.selected = Board.UNSELECTED

    def should_select(self) -> bool:
        return self._board.selected == Board.UNSELECTED

    def select(self, idx: Coord):
        if not self.should_select():
            raise GameError("Board has been already selected")
        if self._board[idx].status != State.PLAYING:
            raise GameError("Board is already full")
        self._board.selected = idx

    def place(self, idx: Coord):
        if self.should_select():
            raise GameError("Need to select board first")
        if not self._board[self._board.selected].is_available(idx):
            raise GameError(f"Square {idx} not available in board {self._board.selected}")
        self._board.place(self._playing, self._board.selected, idx)
        self._board.selected = idx
        self.placed = True

    def board(self) -> Board:
        return self._board

    def available_boards(self) -> List[List[bool]]:
        return self._board.get_available()

    def available_boxes(self) -> List[List[bool]]:
        if self.should_select():
            raise GameError("No board selected")
        return self._board[self._board.selected].get_available()

    def playing(self) -> Box:
        return self._playing if self._board.winning() == State.PLAYING else Box.EMPTY

    def selected(self) -> Coord:
        return self._board.selected

    def state(self) -> State:
        return self.status

    def _evaluate(self):
        self.status = self._board.winning()


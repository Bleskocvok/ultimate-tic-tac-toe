from typing import Any, List, Optional

from .abstract_board import Coord, State
from .abstract_board import AbstractBoard
from .abstract_board import Box


class Small(AbstractBoard):
    def __init__(self, squares: Optional[List[Box]]=None):
        line = [Box.EMPTY, Box.EMPTY, Box.EMPTY]
        self.grid = [line[:], line[:], line[:]]
        self._status = State.PLAYING
        if squares is not None:
            for i in range(len(squares)):
                self[i % 3, i // 3] = squares[i]

    def __getitem__(self, idx: Coord) -> Box:
        return self.grid[idx[1]][idx[0]]

    def __setitem__(self, idx: Coord, data: Box):
        self.grid[idx[1]][idx[0]] = data

    def at(self, coord: Coord) -> Box:
        return self[coord]

    @property
    def status(self):
        return self._status

    @status.getter
    def status(self) -> State:
        return self.winning()

    def is_available(self, idx: Coord) -> bool:
        return self[idx] == Box.EMPTY

    def _winning_symbol(self, sym: Any) -> bool:
        return sym in (Box.X, Box.O)

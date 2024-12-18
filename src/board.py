
from typing import Any, List, Optional

from .abstract_board import AbstractBoard, Box, Coord, State
from .small import Small


class Board(AbstractBoard):
    UNSELECTED = (-1, -1)
    WALL_CH = '|'
    WALL_FOCUS_L = '['
    WALL_FOCUS_R = ']'
    LINE_CH = '-'
    LINE_FOCUS = '='

    def __init__(self, sub_boards: Optional[List[Small]]=None, selected=None):
        self._boards = [[Small() for _ in range(3)] for __ in range(3)]
        self._selected: Coord = Board.UNSELECTED if selected is None else selected
        if sub_boards is not None:
            for i in range(len(sub_boards)):
                self[i % 3, i // 3] = sub_boards[i]

    def _small_to_char(self, small: Small, idx: Coord):
        if small.status == State.X_WON:
            return str(Box.X)
        if small.status == State.O_WON:
            return str(Box.O)
        if small.status == State.DRAW:
            return '/'
        return str(small[idx])

    def _str_line(self, line) -> str:
        result: List[str] = []
        def addw(w, ch):
            result.extend([*(w + ch)])
        for subline in range(3):
            for i, small in enumerate(self._boards[line]):
                addw(self._wall(i, line), ' ')
                for x in range(3):
                    ch = self._small_to_char(small, (x, subline)) + ' '
                    result.extend([*ch])
            addw(self._wall(3, line), '\n')
        return ''.join(result)

    def _wall(self, x: int, y: int) -> str:
        if self.selected == Board.UNSELECTED:
            return Board.WALL_CH
        xdiff = x - self.selected[0]
        if xdiff > 1 or xdiff < 0:
            return Board.WALL_CH
        if y == self.selected[1]:
            return Board.WALL_FOCUS_R if xdiff else Board.WALL_FOCUS_L
        return Board.WALL_CH

    def _hline(self, length: int, y: int) -> str:
        default = Board.LINE_CH * length + '\n'
        if self.selected == Board.UNSELECTED:
            return default
        ydiff = y - self.selected[1]
        if ydiff > 1 or ydiff < 0:
            return default
        result = ''
        for i in range(3):
            ch = Board.LINE_CH
            if self.selected[0] == i:
                ch = Board.LINE_FOCUS
            result = result + Board.LINE_CH + ((length - 4) // 3) * ch
        return result + Board.LINE_CH + '\n'

    def __str__(self) -> str:
        result = ''
        lines = [self._str_line(i) for i in range(3)]
        length = len(lines[0]) // 3 - 1
        for i in range(3):
            result = result + self._hline(length, i)
            result = result + lines[i]
        result = result + self._hline(length, 3)
        return result

    def __getitem__(self, idx: Coord) -> Small:
        return self._boards[idx[1]][idx[0]]

    def __setitem__(self, idx: Coord, data: Small):
        self._boards[idx[1]][idx[0]] = data

    def place(self,
            box: Box,
            big_coord: Coord,
            small_coord: Coord):
        self[big_coord][small_coord] = box

    def at(self, coord: Coord) -> State:
        return self[coord].status

    def sub_board_at(self, idx: Coord) -> Small:
        return self._boards[idx[1]][idx[0]]

    def is_available(self, idx: Coord) -> bool:
        return self[idx].status == State.PLAYING

    def _winning_symbol(self, sym: Any) -> bool:
        return sym in (State.X_WON, State.O_WON)

    @property
    def selected(self):
        return self._selected

    @selected.getter
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, val):
        self._selected = val



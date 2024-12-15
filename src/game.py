#!/usr/bin/env python3


from typing import List, Protocol, Tuple, Optional, Any
from enum import Enum


Coord = Tuple[int, int]


class GameError(Exception):
    pass


class State(Enum):
    PLAYING = 0
    X_WON = 1
    O_WON = 2
    DRAW = 3


class Box(Enum):
    EMPTY = 0
    X = 1
    O = 2

    def __str__(self):
        if self == Box.X:
            return 'X'
        if self == Box.O:
            return 'O'
        return '.'

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}"

    def invert(self):
        if self == Box.X:
            return Box.O
        if self == Box.O:
            return Box.X
        raise RuntimeError("Cannot invert EMPTY")


class AbstractBoard(Protocol):
    def is_available(self, idx: Coord) -> bool:
        ...

    def _winning_symbol(self, sym: Any) -> bool:
        ...

    def __getitem__(self, idx: Coord) -> Any:
        ...

    def __setitem__(self, idx: Coord, data: Any):
        ...

    def at(self, coord: Coord) -> Any:
        pass

    def __repr__(self):
        result = str(self.__class__.__name__) + '(['
        delim = ''
        for y in range(3):
            for x in range(3):
                result = result + delim + self[x, y].__repr__()
                delim = ', '
        return result + '])'

    def winning(self) -> State:
        last = [None]
        def chck(vec, ori):
            last[0] = self._check(vec, ori)
            if last[0] is not None:
                raise GeneratorExit  # this might not be the most appropriate exception
        try:
            # horizontal
            chck((1, 0), (0, 0))
            chck((1, 0), (0, 1))
            chck((1, 0), (0, 2))
            # vertical
            chck((0, 1), (0, 0))
            chck((0, 1), (1, 0))
            chck((0, 1), (2, 0))
            # diagonal
            chck((1, 1), (0, 0))
            chck((-1, 1), (2, 0))
            # either it's a draw or isn't filled yet
            if not self.full():
                return State.PLAYING
            return State.DRAW
        except GeneratorExit:
            if isinstance(last[0], State):
                return last[0]
            if isinstance(last[0], Box):
                return State.X_WON if last[0] == Box.X else State.O_WON
        return State.PLAYING

    def full(self) -> bool:
        for y in range(3):
            for x in range(3):
                if self.is_available((x, y)):
                    return False
        return True

    def get_available(self) -> List[List[bool]]:
        result = [[False for _ in range(3)] for __ in range(3)]
        for y in range(3):
            for x in range(3):
                result[y][x] = self.is_available((x, y))
        return result

    def _check(self, vec: Coord, origin: Coord) -> Optional[Any]:
        symbol = self.at(origin)
        if not self._winning_symbol(symbol):
            return None
        for i in range(1, 3):
            current = self.at((vec[0] * i + origin[0], vec[1] * i + origin[1]))
            if current != symbol:
                return None
        return symbol


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
    def status(self):
        return self._status

    @status.setter
    def status(self, val):
        self._status = val

    def is_available(self, idx: Coord) -> bool:
        return self[idx] == Box.EMPTY

    def _winning_symbol(self, sym: Any) -> bool:
        return sym in (Box.X, Box.O)


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
        for y in range(3):
            for x in range(3):
                state = self._board[x, y].winning()
                if state != State.PLAYING:
                    self._board[x, y].status = state
        self.status = self._board.winning()


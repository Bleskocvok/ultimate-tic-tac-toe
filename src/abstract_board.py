from typing import List, Protocol, Tuple, Optional, Any
from enum import Enum


Coord = Tuple[int, int]


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

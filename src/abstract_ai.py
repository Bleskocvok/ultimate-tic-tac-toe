
from typing import Protocol, Tuple
from .game import Board


class AbstractAi(Protocol):

    symbol: str = ""

    def __init__(self, symbol: str) -> None:
        super().__init__()
        self.symbol = symbol

    def pick_board(self, board: Board) -> Tuple[int, int]:
        ...

    def pick_box(self, board: Board) -> Tuple[int, int]:
        ...



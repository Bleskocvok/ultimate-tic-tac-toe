
from typing import Tuple
from .abstract_ai import AbstractAi
from .game import Board, Small

import random

class RandomAi(AbstractAi):

    def __init__(self, symbol: str) -> None:
        super().__init__(symbol)

    def random_pick(self, thing: Board | Small) -> Tuple[int, int]:
        free = []
        for y in range(3):
            for x in range(3):
                if thing.is_available((x, y)):
                    free.append((x, y))
        assert free
        return random.choice(free)

    def pick_board(self, board: Board) -> Tuple[int, int]:
        return self.random_pick(board)

    def pick_box(self, board: Board) -> Tuple[int, int]:
        small = board.sub_board_at(board.selected)
        return self.random_pick(small)

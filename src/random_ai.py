
from typing import Tuple
from abstract_ai import AbstractAi
from game import Board, Small

import random

class RandomAi(AbstractAi):

    def __init__(self, symbol: str) -> None:
        super().__init__(symbol)

    def random_pick(self, thing: Board | Small) -> Tuple[int, int]:
        avail = thing.get_available()
        free = []
        for y in range(len(avail)):
            for x in range(len(avail[y])):
                if avail[y][x]:
                    free.append((x, y))

        assert free
        return random.choice(free)

    def pick_board(self, board: Board) -> Tuple[int, int]:
        return self.random_pick(board)

    def pick_box(self, board: Board) -> Tuple[int, int]:
        small = board.sub_board_at(board.selected)
        return self.random_pick(small)

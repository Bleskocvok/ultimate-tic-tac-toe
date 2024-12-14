#!/usr/bin/env python3


from math import exp
from abstract_ai import AbstractAi
from game import *
import sys

from random_ai import RandomAi


def get_player_input() -> Tuple[int, int]:
    entered = input()
    chunks = entered.split()
    return (int(chunks[0]), int(chunks[1]))


class PlayerProxy(AbstractAi):

    def __init__(self, symbol: str) -> None:
        super().__init__(symbol)
        self.symbol = symbol

    def pick_board(self, board: Board) -> Tuple[int, int]:
        print("Select board")
        return get_player_input()

    def pick_box(self, board: Board) -> Tuple[int, int]:
        print(f"Select square to place {self.symbol}")
        return get_player_input()


def main():
    players: list[AbstractAi] = [PlayerProxy('X'), RandomAi('O')]

    game = Game()
    while game.state() == State.PLAYING:
        try:
            player = players[0] if players[0].symbol == game.playing().name else players[1]

            print(f"{game.playing()}'s turn")
            print(player.symbol)
            print(game.board())

            if game.should_select():
                bx, by = player.pick_board(game.board())
                game.select((bx, by))
                print(game.board())

            print(f"Board: {game.selected()}")
            sx, sy = player.pick_box(game.board())
            game.place((sx, sy))
            game.next_round()

        except GameError as er:
            print(f"ERROR: {er}")

        except Exception as ex:
            print(f"ERROR: {ex}")

    print(f"GAME ENDED, {game.state()}")


if __name__ == "__main__":
    main()

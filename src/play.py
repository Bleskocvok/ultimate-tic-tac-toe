#!/usr/bin/env python3


from typing import Tuple

from .abstract_board import State
from .board import Board
from .abstract_ai import AbstractAi
from .game import Game, GameError
from .random_ai import RandomAi


class Prompter(AbstractAi):
    def board_prompt(self) -> str:
        ...

    def box_prompt(self) -> str:
        ...


class AiProxy(RandomAi, Prompter):

    def __init__(self, symbol: str) -> None:
        super().__init__(symbol)
        self.symbol = symbol

    def pick_board(self, board: Board) -> Tuple[int, int]:
        return super().pick_board(board)

    def pick_box(self, board: Board) -> Tuple[int, int]:
        return super().pick_box(board)

    def board_prompt(self) -> str:
        return "AI's picking..."

    def box_prompt(self) -> str:
        return "AI's picking..."


class PlayerProxy(Prompter):

    def __init__(self, symbol: str) -> None:
        super().__init__(symbol)
        self.symbol = symbol

    @staticmethod
    def get_player_input() -> Tuple[int, int]:
        entered = input()
        chunks = entered.split()
        return (int(chunks[0]), int(chunks[1]))

    def pick_board(self, board: Board) -> Tuple[int, int]:
        return PlayerProxy.get_player_input()

    def pick_box(self, board: Board) -> Tuple[int, int]:
        return PlayerProxy.get_player_input()

    def board_prompt(self) -> str:
        return f"Select board to place {self.symbol}"

    def box_prompt(self) -> str:
        return f"Select square to place {self.symbol}"


class TermDraw:

    def __init__(self) -> None:
        self._prompt = ""
        self._header = ""
        self._error = ""
        self._board = ""
        self._lines_to_clear = 0

    def set_header(self, txt: str = ""):
        self._header = txt

    def prompt(self, txt: str = ""):
        self._prompt = txt

    def set_error(self, err: str = ""):
        self._error = err

    def set_board(self, txt: str = ""):
        self._board = txt

    def redraw(self):
        esc = "\033"
        print(f"{esc}[2J", flush=True, end="")
        print(f"{esc}[1;1H", flush=True, end="")

        result = ""
        err_str = ""
        if len(self._error) > 0:
            err_str = f"[{esc}[31m {self._error} {esc}[0m]\n"

        result = f"[ {self._header} ]\n{err_str}[ {self._prompt} ]\n{self._board}\n"
        print(result, flush=True, end="")

        self.lines_to_clear = result.count('\n')


def main():
    players: list[Prompter] = []
    game = Game()
    term = TermDraw()

    match input("Play hot-seat or against AI? [ai/hot] "):
        case 'hot' | 'Hot' | 'hotseat' | 'Hotseat' | 'hot-seat' | 'Hot-seat':
            term.set_header('Hot-seat selected')
            players = [PlayerProxy('X'), PlayerProxy('X')]
        case _:
            term.set_header('AI selected')
            players = [PlayerProxy('X'), AiProxy('O')]

    while game.state() == State.PLAYING:
        try:
            player = players[0] if players[0].symbol == game.playing().name else players[1]

            term.set_board(str(game.board()))
            term.redraw()

            if game.should_select():
                term.prompt(player.board_prompt())
                term.redraw()
                term.set_error()

                bx, by = player.pick_board(game.board())
                game.select((bx, by))

                term.set_board(str(game.board()))
                term.redraw()

            term.prompt(player.box_prompt())
            term.redraw()
            term.set_error()
            term.prompt()

            sx, sy = player.pick_box(game.board())
            game.place((sx, sy))
            game.next_round()

            term.set_header(f"It's {game.playing()}'s turn")

        except GameError as e:
            term.set_error("Error: " + str(e))

        except Exception as e:
            term.set_error("Error: " + str(e))

    term.redraw()
    print(f"GAME ENDED, {game.state()}")


if __name__ == "__main__":
    main()

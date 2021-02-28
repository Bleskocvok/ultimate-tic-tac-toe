#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from game import *


def main():
    game = Game()
    try:
        while game.state() == State.PLAYING:
            print(f"{game.playing()}'s turn")
            print(game.board())
            if game.should_select():
                print("Select board")
                bx = int(input())
                by = int(input())
                game.select((bx, by))
            print(f"Board: {game.selected()}")
            print(f"Select square to place {game.playing()}")
            sx = int(input())
            sy = int(input())
            game.place((sx, sy))
            game.next_round()
        print(f"GAME ENDED, {game.state()}")
    except GameError as er:
        print(f"ERROR: {er}")
        print(game.board())


if __name__ == "__main__":
    main()

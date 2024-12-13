#!/usr/bin/env python3


from game import *



def local_draw():
    b = Board()
    b.place(Box.X, (1, 1), (0, 0))
    b.place(Box.O, (1, 1), (0, 1))
    b.place(Box.O, (1, 1), (0, 2))

    b.place(Box.O, (1, 1), (1, 0))
    b.place(Box.X, (1, 1), (1, 1))
    b.place(Box.X, (1, 1), (1, 2))

    b.place(Box.X, (1, 1), (2, 0))
    b.place(Box.O, (1, 1), (2, 1))
    # b.place(Box.O, (1, 1), (2, 2))

    game = Game(board=b)
    assert game.board()[1, 1].status == State.PLAYING

    b.place(Box.O, (1, 1), (2, 2))
    game2 = Game(board=b)
    assert game.board()[1, 1].status == State.DRAW


def repr_win():
    b = Board([Small([Box.EMPTY, Box.EMPTY, Box.EMPTY, Box.EMPTY, Box.EMPTY, Box.EMPTY, Box.EMPTY, Box.EMPTY, Box.EMPTY]),
               Small([Box.X, Box.EMPTY, Box.EMPTY, Box.EMPTY, Box.X, Box.EMPTY, Box.EMPTY, Box.EMPTY, Box.X]),
               Small([Box.EMPTY, Box.EMPTY, Box.EMPTY, Box.EMPTY, Box.EMPTY, Box.EMPTY, Box.EMPTY, Box.EMPTY, Box.EMPTY]),
               Small([Box.EMPTY, Box.EMPTY, Box.EMPTY, Box.EMPTY, Box.EMPTY, Box.EMPTY, Box.EMPTY, Box.EMPTY, Box.EMPTY]),
               Small([Box.X, Box.EMPTY, Box.EMPTY, Box.EMPTY, Box.X, Box.EMPTY, Box.EMPTY, Box.EMPTY, Box.X]),
               Small([Box.EMPTY, Box.EMPTY, Box.EMPTY, Box.EMPTY, Box.EMPTY, Box.EMPTY, Box.EMPTY, Box.EMPTY, Box.EMPTY]),
               Small([Box.EMPTY, Box.EMPTY, Box.EMPTY, Box.EMPTY, Box.EMPTY, Box.EMPTY, Box.EMPTY, Box.EMPTY, Box.EMPTY]),
               Small([Box.X, Box.EMPTY, Box.EMPTY, Box.EMPTY, Box.X, Box.EMPTY, Box.EMPTY, Box.EMPTY, Box.X]),
               Small([Box.EMPTY, Box.EMPTY, Box.EMPTY, Box.EMPTY, Box.EMPTY, Box.EMPTY, Box.EMPTY, Box.EMPTY, Box.EMPTY])])
    game = Game(board=b)
    assert game.state() == State.X_WON


def win_whole():
    b = Board()
    b.place(Box.X, (1, 1), (0, 0))
    b.place(Box.X, (1, 1), (1, 1))
    b.place(Box.X, (1, 1), (2, 2))

    b.place(Box.X, (1, 0), (0, 0))
    b.place(Box.X, (1, 0), (1, 1))
    b.place(Box.X, (1, 0), (2, 2))

    b.place(Box.X, (1, 2), (0, 0))
    b.place(Box.X, (1, 2), (1, 1))
    b.place(Box.X, (1, 2), (2, 2))

    game = Game(board=b)
    assert game.state() == State.X_WON


def win_middle():
    b = Board()
    b.place(Box.O, (1, 1), (0, 0))
    b.place(Box.O, (1, 1), (1, 1))
    b.place(Box.O, (1, 1), (2, 2))
    b.place(Box.O, (1, 1), (1, 0))
    b.place(Box.O, (1, 1), (2, 0))
    game = Game(board=b)
    game._evaluate()
    assert game.board()[1, 1].status == State.O_WON


def simple():
    b = Board()
    b.place(Box.X, (1, 0), (2, 1))
    b.place(Box.O, (2, 1), (1, 0))
    b[0, 1].status = State.DRAW

    game = Game(board=b)
    assert not all(map(all, game.available_boards()))


if __name__ == "__main__":
    simple()
    win_middle()
    win_whole()
    repr_win()
    local_draw()

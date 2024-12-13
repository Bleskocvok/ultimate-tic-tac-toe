#!/usr/bin/env python3

import unittest
from game import *


class TestGameplay(unittest.TestCase):

    def test_local_draw(self):
        b = Board()
        b.place(Box.X, (1, 1), (0, 0))
        b.place(Box.O, (1, 1), (0, 1))
        b.place(Box.O, (1, 1), (0, 2))

        b.place(Box.O, (1, 1), (1, 0))
        b.place(Box.X, (1, 1), (1, 1))
        b.place(Box.X, (1, 1), (1, 2))

        b.place(Box.X, (1, 1), (2, 0))
        b.place(Box.O, (1, 1), (2, 1))

        game = Game(board=b)
        self.assertEqual(game.board()[1, 1].status, State.PLAYING)

        b.place(Box.O, (1, 1), (2, 2))
        game2 = Game(board=b)
        self.assertEqual(game.board()[1, 1].status, State.DRAW)

    def test_repr_win(self):
        b = Board([Small([Box.EMPTY, Box.EMPTY, Box.EMPTY,
                          Box.EMPTY, Box.EMPTY, Box.EMPTY,
                          Box.EMPTY, Box.EMPTY, Box.EMPTY]),
                   Small([Box.X, Box.EMPTY, Box.EMPTY,
                          Box.EMPTY, Box.X, Box.EMPTY,
                          Box.EMPTY, Box.EMPTY, Box.X]),
                   Small([Box.EMPTY, Box.EMPTY, Box.EMPTY,
                          Box.EMPTY, Box.EMPTY, Box.EMPTY,
                          Box.EMPTY, Box.EMPTY, Box.EMPTY]),
                   Small([Box.EMPTY, Box.EMPTY, Box.EMPTY,
                          Box.EMPTY, Box.EMPTY, Box.EMPTY,
                          Box.EMPTY, Box.EMPTY, Box.EMPTY]),
                   Small([Box.X, Box.EMPTY, Box.EMPTY,
                          Box.EMPTY, Box.X, Box.EMPTY,
                          Box.EMPTY, Box.EMPTY, Box.X]),
                   Small([Box.EMPTY, Box.EMPTY, Box.EMPTY,
                          Box.EMPTY, Box.EMPTY, Box.EMPTY,
                          Box.EMPTY, Box.EMPTY, Box.EMPTY]),
                   Small([Box.EMPTY, Box.EMPTY, Box.EMPTY,
                          Box.EMPTY, Box.EMPTY, Box.EMPTY,
                          Box.EMPTY, Box.EMPTY, Box.EMPTY]),
                   Small([Box.X, Box.EMPTY, Box.EMPTY,
                          Box.EMPTY, Box.X, Box.EMPTY,
                          Box.EMPTY, Box.EMPTY, Box.X]),
                   Small([Box.EMPTY, Box.EMPTY, Box.EMPTY,
                          Box.EMPTY, Box.EMPTY, Box.EMPTY,
                          Box.EMPTY, Box.EMPTY, Box.EMPTY])])
        game = Game(board=b)
        self.assertEqual(game.state(), State.X_WON)

    def test_win_whole(self):
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
        self.assertEqual(game.state(), State.X_WON)

    def test_win_middle(self):
        b = Board()
        b.place(Box.O, (1, 1), (0, 0))
        b.place(Box.O, (1, 1), (1, 1))
        b.place(Box.O, (1, 1), (2, 2))
        b.place(Box.O, (1, 1), (1, 0))
        b.place(Box.O, (1, 1), (2, 0))
        game = Game(board=b)
        game._evaluate()
        self.assertEqual(game.board()[1, 1].status, State.O_WON)

    def test_simple(self):
        b = Board()
        b.place(Box.X, (1, 0), (2, 1))
        b.place(Box.O, (2, 1), (1, 0))
        b[0, 1].status = State.DRAW

        game = Game(board=b)
        self.assertFalse(all(map(all, game.available_boards())))


if __name__ == "__main__":
    unittest.main()

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

    def test_elaborate_game(self):
        turns: list[Tuple[str, str, int, int]] = [
            ('X', 'board', 1, 1),
            ('X', 'put',   1, 1),
            ('O', 'put',   1, 0),
            ('X', 'put',   1, 1),
            ('O', 'put',   2, 2),
            ('X', 'put',   1, 1),
            ('O', 'put',   2, 0),
            ('X', 'put',   1, 1),
            ('O', 'put',   1, 2),
            ('X', 'put',   0, 0),
            ('O', 'put',   2, 1),
            ('X', 'put',   2, 2),
            ('O', 'put',   2, 1),
            ('X', 'put',   1, 1),
            ('O', 'put',   0, 0),
            ('X', 'put',   1, 1),
            ('O', 'board', 2, 1),
            ('O', 'put',   0, 2),
            ('X', 'put',   1, 1),
            ('O', 'board', 2, 1),
            ('O', 'put',   2, 1),
            ('X', 'put',   0, 0),
            ('O', 'put',   0, 2),
            ('X', 'put',   0, 0),
            ('O', 'put',   2, 0),
            ('X', 'put',   2, 2),
            ('O', 'put',   2, 0),
            ('X', 'put',   0, 0),
            ('O', 'put',   2, 2),
            ('X', 'put',   2, 2),
            ('O', 'put',   0, 1),
            ('X', 'put',   1, 1),
            ('O', 'board', 1, 2),
            ('O', 'put',   2, 2),
            ('X', 'put',   0, 0),
            ('X', 'won',   0, 0),
        ]
        game = Game(first=Box.X)
        for symbol, cmd, x, y in turns:
            if cmd != 'won':
                self.assertEqual(game.playing().name, symbol)
            if cmd == 'board':
                self.assertTrue(game.should_select())
                game.select((x, y))
            elif cmd == 'put':
                self.assertFalse(game.should_select())
                game.place((x, y))
                game.next_round()
            elif cmd == 'won':
                expected = State.X_WON if symbol == 'X' else State.O_WON
                self.assertEqual(game.state(), expected)

if __name__ == "__main__":
    unittest.main()

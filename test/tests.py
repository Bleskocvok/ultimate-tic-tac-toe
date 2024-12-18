#!/usr/bin/env python3

from typing import Tuple
import unittest
import sys

# Necessary setup for imports to work
import sys
import os.path
src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(src_dir)

from src.random_ai import RandomAi
from src.game import Game, Board, Box, State
from src.small import Small


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

        b.place(Box.X, (0, 1), (0, 0))
        b.place(Box.O, (0, 1), (1, 0))
        b.place(Box.X, (0, 1), (2, 0))
        b.place(Box.O, (0, 1), (0, 1))
        b.place(Box.X, (0, 1), (1, 1))
        b.place(Box.O, (0, 1), (2, 1))
        b.place(Box.O, (0, 1), (0, 2))
        b.place(Box.X, (0, 1), (1, 2))
        b.place(Box.O, (0, 1), (2, 2))
        self.assertEqual(b[0, 1].status, State.DRAW)

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
                self.assertEqual(game.playing(), Box.EMPTY)

    def test_ai_placement(self):
        coords = [(x, y) for y in range(3) for x in range(3)]

        ai = RandomAi('X')
        board = Board()
        board.place(Box.O, (0, 0), (0, 0))

        for free in coords:
            board = Board()
            for selected in coords:
                board.selected = selected
                small = board[board.selected]
                for coord in coords:
                    if coord != free:
                        small[coord] = Box.O
                picked = ai.pick_box(board)
                self.assertTrue(board[board.selected].is_available(picked))
                self.assertTrue(small.is_available(picked))
                self.assertEqual(picked, free)


if __name__ == "__main__":
    unittest.main()

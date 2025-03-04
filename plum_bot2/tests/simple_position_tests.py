from plum_bot2 import PlumBot
import chess
import unittest

class TestSimpleCaptures(unittest.TestCase):
    def test_queen_takes_queen(self):
        pb = PlumBot(chess.WHITE)
        starting_fen = "6k1/q7/8/8/8/4Q3/8/3K4 w - - 0 1"
        board = chess.Board(starting_fen)
        move = pb.choose_move(board)
        board.push(move)
        correct_fen = "6k1/Q7/8/8/8/8/8/3K4 b - - 0 1"
        self.assertEqual(board.fen, correct_fen)


if __name__ == '__main__':
    unittest.main()
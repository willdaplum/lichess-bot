from PlumBotTwo import PlumBot
import chess
import unittest


class TestSimpleCaptures(unittest.TestCase):
    def assert_single_move(self, starting_fen, correct_fen, color):
        pb = PlumBot(color)
        board = chess.Board(starting_fen)
        move = pb.choose_move_depth(board, 3)
        board.push(move)
        self.assertEqual(board.fen(), correct_fen)
        
    def test_queen_takes_queen(self):
        self.assert_single_move("6k1/q7/8/8/8/4Q3/8/3K4 w - - 0 1", "6k1/Q7/8/8/8/8/8/3K4 b - - 0 1", chess.WHITE)

    def test_king_takes_queen(self):
        self.assert_single_move("6k1/8/8/8/8/8/3q4/3K4 w - - 0 1", "6k1/8/8/8/8/8/3K4/8 b - - 0 1", chess.WHITE)
    
    def test_bishop_takes_queen(self):
        self.assert_single_move("6k1/1q6/8/8/8/5B2/8/3K4 w - - 0 1", "6k1/1B6/8/8/8/8/8/3K4 b - - 0 1", chess.WHITE)

    def test_knight_takes_rook(self):
        self.assert_single_move("6k1/8/2n5/8/3R4/8/8/3K4 b - - 0 1", "6k1/8/8/8/3n4/8/8/3K4 w - - 0 2", chess.BLACK)

    def test_rook_takes_pawn(self):
        self.assert_single_move("6k1/P3r3/8/8/8/8/3P4/3K4 b - - 0 1", "6k1/r7/8/8/8/8/3P4/3K4 w - - 0 2", chess.BLACK)

    def test_queen_chooses_queen(self):
        self.assert_single_move("6k1/4q3/8/8/1N5Q/8/8/3K4 b - - 0 1", "6k1/8/8/8/1N5q/8/8/3K4 w - - 0 2", chess.BLACK)

    def test_pawn_chooses_rook(self):
        self.assert_single_move("4k3/8/8/2b1r3/3P4/8/3K4/8 w - - 0 1", "4k3/8/8/2b1P3/8/8/3K4/8 b - - 0 1", chess.WHITE)

    def test_take_free_pawn(self):
        self.assert_single_move("rnbqkbnr/ppp2ppp/8/3pp3/8/P4N2/1PPPPPPP/RNBQKB1R w KQkq - 0 3", 
                                "rnbqkbnr/ppp2ppp/8/3pN3/8/P7/1PPPPPPP/RNBQKB1R b KQkq - 0 3", chess.WHITE)


if __name__ == '__main__':
    unittest.main()
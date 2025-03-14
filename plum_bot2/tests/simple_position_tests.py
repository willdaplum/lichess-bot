from PlumBotTwo import PlumBot
import chess
import unittest


class TestSimpleCaptures(unittest.TestCase):
    def assert_single_move(self, starting_fen, correct_fen, color):
        pb = PlumBot(color)
        board = chess.Board(starting_fen)
        move = pb.choose_move_depth(board, 3, False)
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

class TestMateInOne(unittest.TestCase):
    def assert_single_move(self, starting_fen, correct_fen, color):
        pb = PlumBot(color)
        board = chess.Board(starting_fen)
        move = pb.choose_move_depth(board, 3, False)
        board.push(move)
        self.assertEqual(board.fen(), correct_fen)

    def test_mate_in_one1(self):
        self.assert_single_move("1r4k1/7r/8/8/8/8/8/K7 b - - 0 1", "1r4k1/r7/8/8/8/8/8/K7 w - - 1 2", chess.BLACK)

    def test_mate_in_one2(self):
        self.assert_single_move("rn1q1b1r/ppp1kBpp/3p4/4N3/8/2P5/PPP2PPP/R1Bb1RK1 w - - 0 1", "rn1q1b1r/ppp1kBpp/3p4/4N1B1/8/2P5/PPP2PPP/R2b1RK1 b - - 1 1", chess.WHITE)

    def test_mate_in_one3(self):
        self.assert_single_move("3qr3/2p1k3/8/2N1P3/8/8/6Q1/7K w - - 0 1", "3qr3/2p1k1Q1/8/2N1P3/8/8/8/7K b - - 1 1", chess.WHITE)

    def test_mate_in_one4(self):
        self.assert_single_move("3bkr2/R7/8/7N/8/8/8/7K w - - 0 1", "3bkr2/R5N1/8/8/8/8/8/7K b - - 1 1", chess.WHITE)

    def test_mate_in_one5(self):
        self.assert_single_move("1k4q1/8/8/8/8/8/8/RKR5 b - - 0 1", "1k6/8/8/8/8/1q6/8/RKR5 w - - 1 2", chess.BLACK)

    def test_mate_in_one6(self):
        self.assert_single_move("4rk2/1bp3p1/5p2/p7/2B1rN2/1P4P1/P4P1P/3R2K1 w - - 0 1", "4rk2/1bp3p1/5pN1/p7/2B1r3/1P4P1/P4P1P/3R2K1 b - - 1 1", chess.WHITE)

    def test_mate_in_one7(self):
        self.assert_single_move("5k2/8/P1P1Q3/6PP/2B5/8/R1K2p2/1N3Rq1 w - - 0 37", "5k2/5Q2/P1P5/6PP/2B5/8/R1K2p2/1N3Rq1 b - - 1 37", chess.WHITE)

    def test_mate_in_one8(self):
        self.assert_single_move("NQ1NNN2/8/8/8/2Nk1B2/1pR2B2/7R/1K6 w - - 9 75", "N2NNN2/8/8/4Q3/2Nk1B2/1pR2B2/7R/1K6 b - - 10 75", chess.WHITE)

if __name__ == '__main__':
    unittest.main()
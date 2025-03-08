from PlumBotTwo import PlumBot
import chess
import unittest
import stockfish
import tracemalloc

class TestChessPuzzles(unittest.TestCase):

    def setUp(self):
        self.earlygame_positions = [
            "r1bqkb1r/pppp1ppp/2n2n2/8/2PP4/2N5/PP3PPP/R1BQKBNR b KQkq - 0 5",
            "rnbqkb1r/pp1p1ppp/2p2n2/8/2PNp3/6P1/PP1PPPBP/RNBQK2R b KQkq - 1 5",
            "rn1qk1nr/pbppppbp/1p4p1/8/3PP3/2NB4/PPP1NPPP/R1BQK2R b KQkq - 3 5",
            "r1bqkbnr/pp3ppp/2n1p3/2pP4/3P4/2N2N2/PP2PPPP/R1BQKB1R b KQkq - 0 5",
            "rnbqk2r/ppp1bppp/4pn2/3p4/2PP1B2/2N2N2/PP2PPPP/R2QKB1R b KQkq - 5 5",
            "rnbqkb1r/pp2pppp/5n2/2pp4/3P1B2/3BP3/PPP2PPP/RN1QK1NR w KQkq - 2 6",
            "r1bqkb1r/pp2pppp/2n2n2/3p2B1/3P4/8/PPPN1PPP/R2QKBNR w KQkq - 1 6",
            "r1bqk2r/pp1pppbp/2n2np1/2p5/4P3/2N3P1/PPPPNPBP/R1BQK2R w KQkq - 4 6",
            "rn1qk2r/ppp1ppbp/3p1np1/5b2/3P1B2/2N2N2/PPPQPPPP/R3KB1R w KQkq - 2 6",
            "rnb1kb1r/pp2pppp/5n2/3q4/3Q4/5N2/PP2PPPP/RNB1KB1R w KQkq - 0 6"
        ]

        self.midgame_positions = [
            "r4k1r/pp3ppp/4pb2/5n2/8/2N5/PP1B1PPP/2R2RK1 b - - 3 18",
            "1r1qk2r/1p2nppp/p3p1b1/2bpP3/P7/1NPB3P/1PQ2PP1/R1B1R1K1 b k - 2 15",
            "2r2rk1/pp1n1ppp/2p1pb2/q7/2PP4/1P3N2/PBQ2PPP/3R1RK1 b - - 4 15",
            "2r1kb1r/ppqn1ppp/4p1b1/3p2P1/3P4/4BN1P/PPPQBP2/1KR4R b k - 3 15",
            "r3k2r/p2pppbp/q1b2np1/2P3B1/3Q2N1/2N5/P1P2P1P/3RK1R1 b kq - 3 15",
            "r1q2rk1/1b2bppp/1p2pn2/p3N3/1nPP4/B1N1PB2/6PP/R2Q1RK1 w - - 4 16",
            "1r3rk1/p2qbppp/1pn5/2p1p3/2N5/B1PP2P1/P1Q1PPbP/1R1R2K1 w - - 0 16",
            "1r3rk1/p1b2ppp/2pq1n2/2Np4/3B4/4P1Pb/PPP1BP1P/R2QR1K1 w - - 3 16",
            "r4rk1/p2pppbp/q1b2np1/2P3B1/3Q2N1/2N5/P1P2P1P/3RK1R1 w - - 4 16",
            "1r3rk1/p2qbppp/1pn5/2p1p3/2N5/B1PP2P1/P1Q1PPbP/1R1R2K1 w - - 0 16S"
        ]

        self.endgame_positions = [
            "r4rk1/6pp/1p1N3q/p4R2/2Q5/4b3/6PP/3R3K b - - 0 30",
            "1Q4k1/p2p1p1p/2b3p1/q1P3R1/4rP2/2N5/P1PK3P/8 b - - 6 30",
            "8/3n2pp/4k3/P7/2p1N3/8/5KPP/8 b - - 0 40",
            "3r2k1/3P1ppp/4p3/R7/7P/6P1/5P2/6K1 b - - 0 35",
            "8/6b1/pp2k1p1/5p1p/4PP2/BP1K3P/P7/8 b - - 0 35",
            "8/5ppp/1p2k3/3p4/1PrR1KPP/4P3/5P2/8 w - - 3 35",
            "1r6/8/p4k2/5b2/4p2P/8/P5P1/5RK1 w - - 0 36",
            "8/3Rpk2/4p1p1/3r3p/7P/6P1/4PP2/6K1 w - - 1 36",
            "5r1k/1Q1R2p1/7p/8/1p3q2/5B2/6PK/8 w - - 0 43",
            "8/2RR1Nbk/6p1/4pq2/p7/P6p/1P6/K7 w - - 0 41"
        ]

        self.sf = stockfish.Stockfish()
        self.pb = PlumBot(chess.WHITE)

    def play_stockfish(self, test_name, positions, num_moves):
        total_centipawn_loss = 0
        for starting_pos in self.earlygame_positions:
            board = chess.Board(starting_pos)
            self.pb.set_color(board.turn)
            self.sf.set_fen_position(starting_pos)

            # TODO: implement found checkmate
            starting_eval = self.sf.get_evaluation()['value']
            for i in range(num_moves):                
                board.push(self.pb.choose_move_depth(board, 3))
                self.sf.set_fen_position(board.fen())
                sf_move = self.sf.get_best_move()
                # TODO: doesnt include promotion
                sf_move = chess.Move(chess.parse_square(sf_move[0:2]), chess.parse_square(sf_move[2:]))
                board.push(sf_move)
            self.sf.set_fen_position(board.fen())
            ending_eval = self.sf.get_evaluation()['value']
            pos_centipawn_loss = ending_eval - starting_eval
            if self.pb.color == chess.WHITE:
                pos_centipawn_loss *= -1
            total_centipawn_loss += pos_centipawn_loss
            # print("loss: {}, fen: {}".format(pos_centipawn_loss, board.fen()))

        # NOTE: centipawn loss is usually per single move, so maybe change?
        print("average centipawn loss: {} ({})".format(total_centipawn_loss / len(positions), test_name))

    def test_earlygame(self):
        self.play_stockfish("test_earlygame", self.earlygame_positions, 5)

    def test_midgame(self):
        self.play_stockfish("test_midgame", self.midgame_positions, 5)

    def test_endgame(self):
        self.play_stockfish("test_endgame", self.endgame_positions, 5)

if __name__ == '__main__':
    unittest.main()
import chess

class PlumBot:

    def __init__(self, color):
        self.color = color
        self.piece_val = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9
        }

    def evaluate_position(self, board):
        differential = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece.color == self.color:
                differential += self.piece_val[piece.piece_type]
            else:
                differential -= self.piece_val[piece.piece_type]
        return differential

    def choose_move(self, board):
        legal_moves = board.legal_moves
        best_move = legal_moves[0]
        best_diff = self.evaluate_position(board)
        for legal_move in legal_moves:
            board.push(legal_move)
            diff = self.evaluate_position(board)
            if(diff > best_diff):
                best_diff = diff
                best_move = legal_move
        return best_move
        







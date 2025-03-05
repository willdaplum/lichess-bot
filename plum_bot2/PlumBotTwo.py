import chess
import math

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
            if not piece or piece.piece_type == chess.KING:
                pass
            elif piece.color == self.color:
                differential += self.piece_val[piece.piece_type]
            else:
                differential -= self.piece_val[piece.piece_type]
        return differential

    # REQUIRES: board.turn == self.color
    def choose_move(self, board):
        assert(board.turn == self.color)

        legal_moves = list(board.legal_moves)
        best_move = legal_moves[0]
        best_diff = self.evaluate_position(board)
        for legal_move in legal_moves:
            board.push(legal_move)
            diff = self.evaluate_position(board)
            if(diff > best_diff):
                best_diff = diff
                best_move = legal_move
            board.pop()
        return best_move
    
    # REQUIRES: board.turn == self.color
    def choose_move_depth(self, board, depth):
        assert(board.turn == self.color)

        legal_moves = list(board.legal_moves)
        best_move = None
        best_diff = -math.inf
        for legal_move in legal_moves:
            board.push(legal_move)
            diff = self.choose_move_depth_impl(board, depth - 1)
            # print("move:{} {} score: {}".format(chess.square_name(legal_move.from_square), 
            #                                     chess.square_name(legal_move.to_square), diff)) 
            if diff > best_diff or not best_move:
                best_diff = diff
                best_move = legal_move
            board.pop()
        return best_move


    def choose_move_depth_impl(self, board, depth):
        # exit conditions
        if board.is_checkmate():
            if board.turn == self.color:
                # print("checkmate")
                return math.inf
            return -math.inf
        if board.is_stalemate():
            return 0
        if depth == 0:
            score = self.evaluate_position(board)
            # print("depth: {} score: {} fen: {}".format(depth, score, board.fen())) 
            return score
        
        legal_moves = list(board.legal_moves)
        best_diff = math.inf # board.turn != self.color
        if board.turn == self.color:
            best_diff = -math.inf
        
        for legal_move in legal_moves:
            board.push(legal_move)
            diff = self.choose_move_depth_impl(board, depth - 1)
            # print("depth: {} score: {} fen: {}".format(depth, diff, board.fen())) 

            # board.turn == self.color is the opposite of what you might expect
            # because board already pushed test move.
            if board.turn != self.color and diff > best_diff:
                best_diff = diff
            elif board.turn == self.color and diff < best_diff:
                best_diff = diff
            board.pop()
        return best_diff
        
        







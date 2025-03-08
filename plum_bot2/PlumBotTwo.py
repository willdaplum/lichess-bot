import chess
import math
import random

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

    def set_color(self, color):
        self.color = color

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
        best_moves_to_mate = math.inf
        for legal_move in legal_moves:
            board.push(legal_move)
            verbose = False
            # if legal_move == chess.Move(chess.D2, chess.D3):
            #     verbose = True
            diff, to_mate = self.choose_move_depth_impl(board, depth - 1, verbose)
            '''print("move:{} {} score: {}".format(chess.square_name(legal_move.from_square), 
                                                chess.square_name(legal_move.to_square), diff))
            if(to_mate != math.inf):
                print("--- checkmate found! {} moves.".format(to_mate))'''
            if diff > best_diff or not best_move or (diff == best_diff and to_mate < best_moves_to_mate):
                best_diff = diff
                best_move = legal_move
            elif diff == best_diff and random.randint(1,2) == 1:
                best_diff = diff
                best_move = legal_move

            board.pop()
        return best_move

    # RETURNS: move_score, moves_to_checkmate (inf if not found)
    def choose_move_depth_impl(self, board, depth, verbose):
        # exit conditions
        if board.is_checkmate():
            if board.turn != self.color:
                return math.inf, 0
            return -math.inf, math.inf
        if board.is_stalemate() or board.is_fivefold_repetition() or board.is_repetition() or board.is_insufficient_material():
            return 0, math.inf
        if depth == 0:
            score = self.evaluate_position(board)
            # print("depth: {} score: {} fen: {}".format(depth, score, board.fen())) 
            return score, math.inf
        
        legal_moves = list(board.legal_moves)
        best_diff = math.inf # board.turn != self.color
        best_moves_to_mate = math.inf
        if board.turn == self.color:
            best_diff = -math.inf
        
        for legal_move in legal_moves:
            board.push(legal_move)
            new_verbose = False
            # if legal_move == chess.Move(chess.B8, chess.C6):
            #     new_verbose = True
            diff, moves_to_mate = self.choose_move_depth_impl(board, depth - 1, verbose and new_verbose)
            if verbose:
                offset = '-'
                if depth == 1:
                    offset = '--' 
                    print("{} depth: {} score: {} move:{} {}".format(offset, depth, diff, 
                        chess.square_name(legal_move.from_square), chess.square_name(legal_move.to_square))) 
                if depth == 2:
                    print("{} depth: {} score: {} move:{} {}".format(offset, depth, diff, 
                        chess.square_name(legal_move.from_square), chess.square_name(legal_move.to_square))) 

            # board.turn == self.color is the opposite of what you might expect
            # because board already pushed test move.
            if board.turn != self.color and diff > best_diff:
                best_diff = diff
            elif board.turn == self.color and diff < best_diff:
                best_diff = diff
            if moves_to_mate < best_moves_to_mate:
                best_moves_to_mate = moves_to_mate
            board.pop()
        return best_diff, best_moves_to_mate + 1
        
        







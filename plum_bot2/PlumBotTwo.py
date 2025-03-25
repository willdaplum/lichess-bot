import chess
import math
import random
import json


class PlumBot:

    def __init__(self, color, piece_table_path='/Users/williamcooley/code/lichess-bot/plum_bot2/piece_tables_default.json'):
        self.static_evaluations = 0
        self.color = color
        self.piece_val = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9
        }
        self.piece_table_path = piece_table_path
        with open(piece_table_path, 'r') as file:
            self.piece_tables = json.load(file)

    def get_game_phase(self, board):
        if(board.fullmove_number < 10):
            return "earlygame"
        elif(board.fullmove_number < 30):
            return "midgame"
        else:
            return "endgame"

    def save_piece_tables(self):
        with open(self.piece_table_path, 'w') as file:
            json.dump(self.piece_tables, file)

    def update_piece_tables(self, piece, board, square, change):
        if piece.piece_type != chess.KING:
            color_text = "white" if piece.color == chess.WHITE else "black"
            phase_text = self.get_game_phase(board)
            piece_text = chess.piece_name(piece.piece_type)
            file = chess.square_file(square)
            rank = chess.square_rank(square)
            self.piece_tables[color_text][piece_text][phase_text][rank][file] += change


    def evaluate_position(self, board):
        self.static_evaluations += 1

        total_differential = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece and piece.piece_type != chess.KING:
                color_text = "white" if piece.color == chess.WHITE else "black"
                piece_text = chess.piece_name(piece.piece_type)
                phase_text = self.get_game_phase(board)
                file = chess.square_file(square)
                rank = chess.square_rank(square)
                piece_differential = self.piece_val[piece.piece_type] * self.piece_tables[color_text][piece_text][phase_text][rank][file]
                if piece.color == self.color:
                    total_differential += piece_differential
                else:
                    total_differential -= piece_differential
        return total_differential

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

    def choose_move_print(self, board, depth):
        starting_color = self.color
        move_seq_message = "start: {} moves:".format(board.fen())
        chosen_move = None
        for i in range(depth, 0, -1):
            print('- depth: {}'.format(i))
            self.set_color(board.turn)
            move = self.choose_move_depth(board, i)
            if not chosen_move:
                chosen_move = move
            move_seq_message += " {}".format(move.uci())
            board.push(move)

        self.color = starting_color
        for i in range(0, depth):
            board.pop()
        print(move_seq_message)
        return chosen_move

    
    # REQUIRES: board.turn == self.color
    def choose_move_depth(self, board, depth, time_scarce):
        assert(board.turn == self.color)

        legal_moves = list(board.legal_moves)
        random.shuffle(legal_moves)
        if len(legal_moves) == 0:
            print(board.fen())
            print("no legal moves!?")
        best_move = None
        best_diff = -math.inf
        best_moves_to_mate = math.inf
        for legal_move in legal_moves:
            board.push(legal_move)
            verbose = False
            # if legal_move == chess.Move(chess.D2, chess.D3):
            #     verbose = True
            new_depth = depth - 1
            if board.is_capture(legal_move) and not time_scarce:
                new_depth = depth
            diff, to_mate = self.choose_move_depth_impl(board, new_depth, -math.inf, math.inf, verbose)
            # print("-- move:{} {} score: {}".format(chess.square_name(legal_move.from_square), 
            #                                     chess.square_name(legal_move.to_square), diff))
            # if(to_mate != math.inf):
            #     print("--- checkmate found! {} moves.".format(to_mate))
            if diff > best_diff or not best_move or (diff == best_diff and to_mate < best_moves_to_mate):
                # print("better move, updating...")
                best_moves_to_mate = to_mate
                best_diff = diff
                best_move = legal_move

            board.pop()
        return best_move

    # RETURNS: move_score, moves_to_checkmate (inf if not found)
    # NOTE: alpha: best value maximizer can guarentee (plumbot)
    #       beta: best value minimizer can guarentee (opponent simmed by plumbot)
    def choose_move_depth_impl(self, board, depth, alpha, beta, verbose):
        # exit conditions
        if board.is_checkmate():
            if board.turn != self.color:
                return math.inf, 0
            return -math.inf, math.inf
        if board.is_stalemate() or board.is_fivefold_repetition()  or board.is_repetition() or board.is_insufficient_material() or board.is_fifty_moves():
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
            diff, moves_to_mate = self.choose_move_depth_impl(board, depth - 1, alpha, beta, verbose and new_verbose)
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
            if board.turn != self.color:
                best_diff = max(diff, best_diff)
                alpha = max(alpha, best_diff)
            elif board.turn == self.color:
                best_diff = min(diff, best_diff)
                beta = min(beta, best_diff)
            if moves_to_mate < best_moves_to_mate:
                best_moves_to_mate = moves_to_mate
            board.pop()

            if beta <= alpha:
                break

        return best_diff, best_moves_to_mate + 1
        
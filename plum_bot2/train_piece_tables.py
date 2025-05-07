from PlumBotTwo import PlumBot
import chess
import csv
import itertools
import stockfish

piece_table_path = "./piece_tables.json"

pb = PlumBot(chess.WHITE, piece_table_path)
sf = stockfish.Stockfish()

start_index = 4201
num_tests = 2000
with open('./positions.csv', 'r') as csvfile:
    # print('in loop')
    reader = csv.reader(csvfile)
    header = next(reader)
    num_iterations = num_tests
    for row in itertools.islice(reader, start_index, start_index + num_iterations):
        state_fen = row[0]
        board = chess.Board(state_fen)

        if board.outcome():
            num_tests -= 1
            print("skipping finished game")
            continue

        color = board.turn
        pb.set_color(color)
        pb_move = pb.choose_move_depth(board, 3, False)
        sf.set_fen_position(board.fen())
        sf_move = chess.Move.from_uci(sf.get_best_move())

        #TODO: centipawn loss instead of just move matching?
        if pb_move.uci() == sf_move.uci():
            # print('update good')
            pb.update_piece_tables(board.piece_at(pb_move.from_square), board, pb_move.from_square, -.001)
            pb.update_piece_tables(board.piece_at(pb_move.from_square), board, pb_move.to_square, .001)
        else:
            # print('update bad')
            pb.update_piece_tables(board.piece_at(pb_move.from_square), board, pb_move.from_square, .001)
            pb.update_piece_tables(board.piece_at(pb_move.from_square), board, pb_move.to_square, -.001)

print("trained on {} positions.".format(num_tests))
pb.save_piece_tables()


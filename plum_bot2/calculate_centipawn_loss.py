from PlumBotTwo import PlumBot
import chess
import csv
import stockfish
import itertools

piece_table_path = "/Users/williamcooley/code/lichess-bot/plum_bot2/piece_tables.json"

pb = PlumBot(chess.WHITE, piece_table_path)
sf = stockfish.Stockfish()


total_centipawn_loss = 0
num_tests = 100
with open('/Users/williamcooley/code/lichess-bot/plum_bot2/positions.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    header = next(reader)
    num_iterations = num_tests
    for row in itertools.islice(reader, 0, num_iterations):
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
        starting_eval = sf.get_evaluation()['value']
        board.push(pb_move)
        sf.set_fen_position(board.fen())
        ending_eval = sf.get_evaluation()['value']

        pos_centipawn_loss = ending_eval - starting_eval
        if pb.color == chess.WHITE:
            pos_centipawn_loss *= -1
        # print("loss:{} move: {} fen: {}".format(pos_centipawn_loss, pb_move.uci(), state_fen))
        total_centipawn_loss += pos_centipawn_loss

print("Average centipawn loss ({} positions): {}".format(num_tests, total_centipawn_loss / num_tests))
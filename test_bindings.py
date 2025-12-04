import sys
sys.path.insert(0, 'cpp/build')
import topcap_engine as engine

board = engine.initial_board(8)
print(engine.board_to_string(board))
move = engine.Move(engine.Coordinates(1, 1), engine.Coordinates(2, 2))
print(f"move {move} is legal? : {engine.is_move_legal(board, move)}")




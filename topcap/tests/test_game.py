from topcap.agents import RandomAI, DeterministicAI
from topcap.core.game import Game
from topcap.core.common import Move, Board
from topcap.utils.topcap_utils import WinReason

VERBOSE = True

def _teleport(board: Board, from_tile: str, to_tile: str):
    from_color = board.get_tile_content(from_tile)
    to_color = board.get_tile_content(to_tile)
    board._set_tile_content(from_tile, to_color) 
    board._set_tile_content(to_tile, from_color)


def test_randi_game():
    leo = RandomAI(name="Léo", verbose=VERBOSE)
    jan = RandomAI(name="Jan", verbose=VERBOSE)
    game = Game(verbose=VERBOSE)
    game.run_game(leo , jan)

# test game results
def test_base_reached():
    moves_leo = [Move("e6", "f6")]
    leo = DeterministicAI(name="Léo", moves=moves_leo, verbose=VERBOSE)
    jan = RandomAI(name="Jan", verbose=VERBOSE)
    game = Game(verbose=VERBOSE)
    board = Board()
    _teleport(board, "d1", "e6")
    game.run_game(leo , jan, custom_board=board)
    assert game.board.move_count == 1
    assert game.win_reason == WinReason.BASE_REACHED
    assert game.winner == leo

def test_no_moves_left():
    moves_leo = [Move("a4", "a3")]
    leo = DeterministicAI(name="Léo", moves=moves_leo, verbose=VERBOSE)
    jan = RandomAI(name="Jan", verbose=VERBOSE)
    game = Game(verbose=VERBOSE)
    board = Board()
    _teleport(board, "c6", "a6")
    _teleport(board, "f3", "f1")
    _teleport(board, "e4", "f4")
    game.run_game(leo , jan, custom_board=board)
    assert game.board.move_count == 1
    assert game.win_reason == WinReason.NO_MOVES_LEFT
    assert game.winner == leo


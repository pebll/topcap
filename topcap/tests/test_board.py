import pytest

from topcap.core.common import Board, Color, Move
import topcap.utils as utils

def test_tile_to_coords():
    assert utils.tile_to_coords("a1") == (0, 0)
    assert utils.tile_to_coords("f6") == (5, 5)
    with pytest.raises(ValueError):
        assert utils.tile_to_coords("h8") == (7, 7)

def test_coords_to_tile():
    assert utils.coords_to_tile((0, 0)) == "a1"
    assert utils.coords_to_tile((5, 5)) == "f6"
    with pytest.raises(ValueError):
        assert utils.coords_to_tile((7, 7)) == "h8"

def test_move_path():
    inplace_move = Move("a1", "a1")
    assert inplace_move.path() == []
    horizontal_move = Move("a1", "f1")
    assert horizontal_move.path() == ["b1", "c1", "d1", "e1", "f1"]
    vertical_move = Move("a1", "a6")
    assert vertical_move.path() == ["a2", "a3", "a4", "a5", "a6"]
    diagonal_move = Move("a1", "f6")
    assert diagonal_move.path() == []

def test_board_initial_setup():
    board = Board()
    assert board.get_tile_content("a4") == Color.WHITE
    assert board.get_tile_content("b3") == Color.WHITE
    assert board.get_tile_content("c2") == Color.WHITE
    assert board.get_tile_content("d1") == Color.WHITE
    assert board.get_tile_content("c6") == Color.BLACK
    assert board.get_tile_content("d5") == Color.BLACK
    assert board.get_tile_content("e4") == Color.BLACK
    assert board.get_tile_content("f3") == Color.BLACK


def test_board_move():
    board = Board()
    move = Move("a4", "b4")
    assert board.move_is_valid(move, Color.WHITE)
    board.move(move)
    assert board.get_tile_content("a4") == Color.NONE
    assert board.get_tile_content("b4") == Color.WHITE
    move = Move("b3", "c3")
    assert not board.move_is_valid(move, Color.WHITE)
    with pytest.raises(ValueError):
        assert not board.move(move)

def test_get_valid_moves():
    board = Board()
    board.get_all_valid_moves(Color.WHITE)






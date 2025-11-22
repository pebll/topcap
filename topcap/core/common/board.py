from typing import  override
import numpy as np
from numpy.typing import NDArray

import topcap.utils as utils
from topcap.utils.topcap_utils import WinReason
from .color import Color
from .move import Move


class Board:
    def __init__(self):
        self.board: NDArray[np.int8] = np.zeros((6, 6), dtype=np.int8)
        self.neighbour_count_board: NDArray[np.int8] = np.zeros((6, 6), dtype=np.int8)
        self.initial_setup()
    
    def initial_setup(self):
        self.tiles: dict[Color, list[str]] = {}
        self.tiles[Color.WHITE] = ["a4", "b3", "c2", "d1"]
        self.tiles[Color.BLACK] = ["c6", "d5", "e4", "f3"]
        self.base_tile : dict[Color, str] = {}
        self.base_tile[Color.BLACK] = "f6"
        self.base_tile[Color.WHITE] = "a1"
        for tile in self.tiles[Color.WHITE]:
            self._set_tile_content(tile, Color.WHITE)
        for tile in self.tiles[Color.BLACK]:
            self._set_tile_content(tile, Color.BLACK)
        self.current_player: Color = Color.WHITE
        self.move_count: int= 0
    
    def move(self, move: Move, verbose: bool = False):
        if not self.move_is_valid(move, self.get_tile_content(move.from_tile)):
            raise ValueError(f"Cannot execute move, invalid move {move}, please check this before running move()")
        from_content = self.get_tile_content(move.from_tile)
        self._set_tile_content(move.from_tile, Color.NONE)
        self._set_tile_content(move.to_tile, from_content)
        self._update_piece_positions()
        self.current_player = self.current_player.opposite()
        self.move_count += 1
        if verbose:
            print(f"Executed move {move}")

    def move_is_valid(self, move: Move | None, moving_player: Color, verbose: bool = False) -> bool:
        if move is None:
            if verbose:
                print("Move is None, invalid move")
            return False
        from_tile = move.from_tile
        to_tile = move.to_tile
        if not self._tile_exists(from_tile):
            if verbose:
                print(f"From tile {from_tile} does not exist, invalid move")
            return False
        if not self._tile_exists(to_tile):
            if verbose:
                print(f"To tile {to_tile} does not exist, invalid move")
            return False
        from_content = self.get_tile_content(from_tile)
        if from_content == Color.NONE:
            if verbose:
                print(f"From tile {from_tile} is empty, invalid move")
            return False
        path = move.path()
        if len(path) == 0:
            if verbose:
                print(f"Invalid move, path is diagonal or empty")
            return False
        if len(path) != self._get_neighbour_count(from_tile):
            if verbose:
                print(f"Invalid move, path length is not equal to neighbour count")
            return False
        for tile in path:
            if self.get_tile_content(tile) != Color.NONE:
                if verbose:
                    print(f"Invalid move, path is blocked by {tile}")
                return False
        if to_tile == self.base_tile[from_content]:
            if verbose:
                print(f"Invalid move, piece cannot move into own base")
            return False
        if self.get_tile_content(from_tile) != moving_player:
            if verbose:
                print(f"Invalid move, piece can only be moved by own player")
            return False

        return True
    
    def get_all_valid_moves(self, player: Color) -> list[Move]:
        tiles: list[str] = self.tiles[player]
        moves: list[Move] = []
        for from_tile in tiles:
            for move in self._get_valid_moves_for_tile(from_tile):
                moves.append(move)
        return moves
    
    def get_win_reason(self) -> tuple[Color, WinReason]:
        for color, base in self.base_tile.items():
            if self.get_tile_content(base) == color.opposite():
                return color.opposite(), WinReason.BASE_REACHED 
        if len(self.get_all_valid_moves(self.current_player)) == 0:
            return self.current_player.opposite(), WinReason.NO_MOVES_LEFT 
        return Color.NONE, WinReason.NONE 

    def _tile_exists(self, tile: str):
        coords = utils.tile_to_coords(tile)
        return coords[0] >= 0 and coords[0] < 6 and coords[1] >= 0 and coords[1] < 6
        
    def _set_tile_content(self, tile: str, content: Color):
        add_content = content != Color.NONE
        if not self._tile_exists(tile):
            raise ValueError(f"Tile {tile} does not exist, can't set content")
        coords = utils.tile_to_coords(tile)
        old_content = self.get_tile_content(tile)
        if add_content and old_content != Color.NONE:
            raise ValueError(f"Tile {tile} is already occupied, can't the content to {content}")
        if not add_content and old_content == Color.NONE:
            raise ValueError(f"Tile {tile} is already empty, can't remove the content")
        self._update_neighbour_count(tile, add_content)
        self.board[coords] = content.value
    
    def get_tile_content(self, tile: str):
        coords = utils.tile_to_coords(tile)
        return Color(self.board[coords])
    
    def _update_neighbour_count(self, tile: str, increase: bool):
        coords = utils.tile_to_coords(tile)
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                new_y = coords[0] + dy
                new_x = coords[1] + dx
                if new_y < 0 or new_y >= 6 or new_x < 0 or new_x >= 6:
                    continue
                if increase:
                    self.neighbour_count_board[new_y, new_x] += 1
                else:
                    self.neighbour_count_board[new_y, new_x] -= 1
    
    def _get_neighbour_count(self, tile: str) -> int:
        coords = utils.tile_to_coords(tile)
        return int(self.neighbour_count_board[coords])
    
    def _update_piece_positions(self):
        self.tiles[Color.WHITE] = []
        self.tiles[Color.BLACK] = []
        for y in range(6):
            for x in range(6):
                tile = utils.coords_to_tile((x, y))
                content = self.get_tile_content(tile)
                if content != Color.NONE:
                    self.tiles[content].append(tile)

    def _get_valid_moves_for_tile(self, tile: str) -> list[Move]:
        valid_moves: list[Move] = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        neighbour_count = self._get_neighbour_count(tile)
        
        for dx, dy in directions:
            if not utils.is_tile_valid(tile):
                continue
            x, y = utils.tile_to_coords(tile)
            x += dx * neighbour_count
            y += dy * neighbour_count
            coords = (x, y)
            if not utils.is_coords_valid(coords):
                continue
            to_tile = utils.coords_to_tile((x, y))
            move = Move(tile, to_tile)
            if self.move_is_valid(move, self.get_tile_content(tile)):
                valid_moves.append(move)
        return valid_moves
    
    @override
    def __repr__(self):
        return f"B({self.move_count})"

    @override
    def __eq__(self, other: object):
        if isinstance(other, Board):
            return np.array_equal(self.board, other.board) and self.current_player == other.current_player and self.move_count == other.move_count
        return False

    @override 
    def __hash__(self):
        return hash(str(self.board) + str(self.current_player))

    def to_str(self) -> str:
        space_length = 6
        my_str = "\n"
        my_str += " " * space_length + "  a b c d e f\n"
        for y in range(5, -1, -1):  # Start from row 6 (index 5)
            row: list[str] = []
            for x in range(6):
                if self.board[y, x] == Color.NONE.value:
                    row.append('·')
                elif self.board[y, x] == Color.BLACK.value:
                    row.append('○')
                elif self.board[y, x] == Color.WHITE.value:
                    row.append('●')
            my_str += " " * space_length + f"{y+1} {' '.join(row)} {y+1}\n"
        my_str += " " * space_length + "  a b c d e f\n"
        return my_str

    def to_code(self) -> str:
        code = ""
        for y in range(5, -1, -1):  # Start from row 6 (index 5)
            for x in range(6):
                color: int = self.board[y, x]
                c = '-'
                if color == Color.WHITE.value:
                    c = 'W'
                elif color == Color.BLACK.value:
                    c = 'B'
                code += c
        return code

    @staticmethod
    def from_code(code: str) -> 'Board':
        """
        Create a Board from a code string (reverse of to_code()).
        Code format: 36 characters representing board state row by row (top to bottom, left to right).
        'W' = White, 'B' = Black, '-' = Empty
        """
        if len(code) != 36:
            raise ValueError(f"Code must be exactly 36 characters (6x6 board), got {len(code)}")
        
        board = Board()
        
        # First, remove all existing pieces by setting them to NONE
        # We need to do this before setting new pieces to avoid validation errors
        for tile in board.tiles[Color.WHITE] + board.tiles[Color.BLACK]:
            old_content = board.get_tile_content(tile)
            if old_content != Color.NONE:
                coords = utils.tile_to_coords(tile)
                board._update_neighbour_count(tile, False)  # Decrease neighbour count
                board.board[coords] = Color.NONE.value
        
        # Clear tile lists
        board.tiles[Color.WHITE] = []
        board.tiles[Color.BLACK] = []
        
        # Parse code and set board state
        char_index = 0
        for y in range(5, -1, -1):  # Start from row 6 (index 5) to row 1 (index 0)
            for x in range(6):
                c = code[char_index]
                char_index += 1
                
                if c == 'W':
                    color = Color.WHITE
                elif c == 'B':
                    color = Color.BLACK
                elif c == '-':
                    color = Color.NONE
                else:
                    raise ValueError(f"Invalid character '{c}' in code at position {char_index-1}. Expected 'W', 'B', or '-'")
                
                # Set tile content (this will update neighbour counts)
                tile = utils.coords_to_tile((y, x))
                if color != Color.NONE:
                    board._set_tile_content(tile, color)
        
        # Update piece positions based on final board state
        board._update_piece_positions()
        
        # Reset to default values (can't be determined from code)
        board.current_player = Color.WHITE
        board.move_count = 0
        
        return board

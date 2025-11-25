from typing import  override
import numpy as np
from numpy.typing import NDArray

import topcap.utils as utils
from topcap.utils.topcap_utils import WinReason
from .color import Color
from .move import Move


# Pre-compute tile string to coordinates mapping for performance
_TILE_TO_COORDS_CACHE: dict[str, tuple[int, int]] = {}
_COORDS_TO_TILE_CACHE: dict[tuple[int, int], str] = {}
for y in range(6):
    for x in range(6):
        tile = chr(x + ord('a')) + str(y + 1)
        coords = (y, x)
        _TILE_TO_COORDS_CACHE[tile] = coords
        _COORDS_TO_TILE_CACHE[coords] = tile


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
        # _set_tile_content now handles tiles dictionary updates, so we just call it
        self._set_tile_content(move.from_tile, Color.NONE)
        self._set_tile_content(move.to_tile, from_content)
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
        if from_content != moving_player:
            if verbose:
                print(f"Invalid move, piece can only be moved by own player")
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

        return True
    
    def get_all_valid_moves(self, player: Color) -> list[Move]:
        tiles: list[str] = self.tiles[player]
        moves: list[Move] = []
        for from_tile in tiles:
            moves.extend(self._get_valid_moves_for_tile(from_tile))
        return moves
    
    def get_win_reason(self) -> tuple[Color, WinReason]:
        for color, base in self.base_tile.items():
            if self.get_tile_content(base) == color.opposite():
                return color.opposite(), WinReason.BASE_REACHED 
        if len(self.get_all_valid_moves(self.current_player)) == 0:
            return self.current_player.opposite(), WinReason.NO_MOVES_LEFT 
        return Color.NONE, WinReason.NONE 

    def _tile_exists(self, tile: str):
        return tile in _TILE_TO_COORDS_CACHE

    def _tile_number(self, coords: tuple[int, int]):
        return coords[0] + coords[1]*6
        
    def _set_tile_content(self, tile: str, content: Color):
        add_content = content != Color.NONE
        if not self._tile_exists(tile):
            raise ValueError(f"Tile {tile} does not exist, can't set content")
        coords = _TILE_TO_COORDS_CACHE[tile]
        old_content = Color(self.board[coords])
        if add_content and old_content != Color.NONE:
            raise ValueError(f"Tile {tile} is already occupied, can't the content to {content}")
        if not add_content and old_content == Color.NONE:
            raise ValueError(f"Tile {tile} is already empty, can't remove the content")
        
        # Update tiles dictionary to keep it in sync
        if old_content != Color.NONE and old_content in self.tiles:
            if tile in self.tiles[old_content]:
                self.tiles[old_content].remove(tile)
        if add_content:
            if content not in self.tiles:
                self.tiles[content] = []
            if tile not in self.tiles[content]:
                self.tiles[content].append(tile)
        
        self._update_neighbour_count_coords(coords, add_content)
        self.board[coords] = content.value
    
    def get_tile_content(self, tile: str):
        coords = _TILE_TO_COORDS_CACHE[tile]
        return Color(self.board[coords])
    
    def _update_neighbour_count(self, tile: str, increase: bool):
        coords = _TILE_TO_COORDS_CACHE[tile]
        self._update_neighbour_count_coords(coords, increase)
    
    def _update_neighbour_count_coords(self, coords: tuple[int, int], increase: bool):
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
        coords = _TILE_TO_COORDS_CACHE[tile]
        return int(self.neighbour_count_board[coords])
    
    def _update_piece_positions(self):
        """Rebuild piece positions from board. Only used when needed (e.g., from_hash)."""
        self.tiles[Color.WHITE] = []
        self.tiles[Color.BLACK] = []
        for y in range(6):
            for x in range(6):
                coords = (y, x)
                content_value = self.board[coords]
                if content_value != Color.NONE.value:
                    tile = _COORDS_TO_TILE_CACHE[coords]
                    self.tiles[Color(content_value)].append(tile)

    def _get_valid_moves_for_tile(self, tile: str) -> list[Move]:
        valid_moves: list[Move] = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        neighbour_count = self._get_neighbour_count(tile)
        coords = _TILE_TO_COORDS_CACHE[tile]
        tile_content = Color(self.board[coords])
        
        for dx, dy in directions:
            new_y = coords[0] + dy * neighbour_count
            new_x = coords[1] + dx * neighbour_count
            if new_y < 0 or new_y >= 6 or new_x < 0 or new_x >= 6:
                continue
            to_coords = (new_y, new_x)
            to_tile = _COORDS_TO_TILE_CACHE[to_coords]
            move = Move(tile, to_tile)
            if self.move_is_valid(move, tile_content):
                valid_moves.append(move)
        return valid_moves
    
    @override
    def __repr__(self):
        return f"B{self.to_hash()[-4:]}({self.move_count})"

    @override
    def __eq__(self, other: object):
        if isinstance(other, Board):
            return self.to_hash() == other.to_hash()
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

    def to_hash(self) -> int:
        # get the posistions of all the pieces
        whites = []
        blacks = []
        for x in range(6):
            for y in range(6):
                if self.board[y, x] == Color.WHITE.value:
                    whites.append(x+6*y)
                elif self.board[y, x] == Color.BLACK.value:
                    blacks.append(x+6*y)
        # sort them
        whites.sort()
        blacks.sort()
        # encode into int
        h = 0
        for i, pos in enumerate(whites + blacks):
            h = h | (pos << (i * 6))
        return h

    def from_hash(self, hash: int):
        positions = []
        for i in range(8):
            pos = (hash >> (i * 6)) & 0b111111  # Extract 6 bits
            x = pos % 6
            y = pos // 6
            positions.append((x, y))
        
        whites = positions[:4]
        blacks = positions[4:]

        self.board: NDArray[np.int8] = np.zeros((6, 6), dtype=np.int8)
        self.neighbour_count_board: NDArray[np.int8] = np.zeros((6, 6), dtype=np.int8)
        for (x, y) in whites:
            coords = (y, x)  # Note: board uses (y, x) indexing
            self.board[coords] = Color.WHITE.value
            self._update_neighbour_count_coords(coords, True)
        for (x, y) in blacks:
            coords = (y, x)  # Note: board uses (y, x) indexing
            self.board[coords] = Color.BLACK.value
            self._update_neighbour_count_coords(coords, True)
        self._update_piece_positions()

    @override
    def __hash__(self) -> int:
        return self.to_hash()

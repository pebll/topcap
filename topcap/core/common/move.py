from typing import override

from topcap.utils import tile_to_coords, coords_to_tile


class Move:
    def __init__(self, from_tile : str, to_tile: str):
        self.from_tile: str = from_tile
        self.to_tile: str = to_tile

    @override
    def __repr__(self):
        return f"({self.from_tile} {self.to_tile})"

    def to_code(self) -> str:
        return f"({self.from_tile} {self.to_tile})"
    
    @staticmethod
    def from_code(code: str) -> 'Move':
        """
        Create a Move from a code string (reverse of to_code()).
        Code format: "(from_tile to_tile)" e.g., "(a1 b2)"
        """
        code = code.strip()
        if not code.startswith('(') or not code.endswith(')'):
            raise ValueError(f"Code must start with '(' and end with ')', got: {code}")
        
        # Remove parentheses
        inner = code[1:-1].strip()
        parts = inner.split()
        
        if len(parts) != 2:
            raise ValueError(f"Code must contain exactly two tiles separated by space, got: {code}")
        
        from_tile = parts[0]
        to_tile = parts[1]
        
        return Move(from_tile, to_tile)
    
    def path(self) -> list[str]:
        from_coords: tuple[int, int] = tile_to_coords(self.from_tile)
        to_coords: tuple[int, int] = tile_to_coords(self.to_tile)
        dx = to_coords[0] - from_coords[0]
        dy = to_coords[1] - from_coords[1]
        if dx != 0 and dy != 0:
            print("Invalid move, can't move diagonally")
            return []
        dx = 1 if dx > 0 else -1 if dx < 0 else 0
        dy = 1 if dy > 0 else -1 if dy < 0 else 0
        path: list[str] = []
        x = from_coords[0]
        y = from_coords[1]
        while x != to_coords[0] or y != to_coords[1]:
            x += dx
            y += dy
            path.append(coords_to_tile((x, y)))
        return path



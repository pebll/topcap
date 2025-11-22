from enum import Enum
from typing import override

class Color(Enum):
    NONE = 0
    WHITE = 1
    BLACK = -1

    @override
    def __str__(self):
        return self.name.lower().capitalize()

    @staticmethod
    def from_string(s: str):
        try:
            return Color[s.upper()]
        except KeyError:
            raise ValueError(f"Invalid TileContent string: {s}")
        
    def opposite(self):
        if self == Color.BLACK:
            return Color.WHITE
        elif self == Color.WHITE:
            return Color.BLACK
        else:
            return Color.NONE

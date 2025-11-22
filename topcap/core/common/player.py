from typing import override
from abc import abstractmethod, ABC

from .board import Board
from .color import Color
from .move import Move


class Player(ABC):
    def __init__(self, name: str, verbose: bool = True):
        self.name: str = name
        self.color: Color = Color.NONE
        self.verbose: bool = verbose
 
    @override
    def __str__(self):
        return f"{self.name}"#{f' ({str(self.color)})' if self.color != Color.NONE else ''}"
    
    def set_color(self, color: Color):
        """This will be called only one at init, to set the color the player is playing"""
        self.color = color

    @abstractmethod
    def get_move(self, board: Board) -> Move:
        """Given a board state, this function should return:
            move [Move] : The chosen move by the player for the current board state
        """

    def game_over_callback(self, win: bool):
        pass



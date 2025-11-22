from abc import ABC, abstractmethod
from math import pow
from typing import override
from topcap.core.common import Color, Board
from topcap.utils import distance

class Heuristic(ABC): 
    def __init__(self):
        pass

    @abstractmethod
    def evaluate(self, board : Board) -> float:
        # + is advantage for white, - is advantage for black
        raise NotImplementedError("Heuristic must be implemented in Subclass!")
    
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError("Heuristic must be implemented in Subclass!")

class SimpleHeuristic(Heuristic):
    def __init__(self, initiative_factor: float = 1.0, distance_factor: float = 1.0, available_moves_factor: float = 1.0):
        super().__init__()
        self.initiative_factor: float = initiative_factor
        self.distance_factor: float = distance_factor
        self.available_moves_factor: float = available_moves_factor

    @override
    def evaluate(self, board: Board) -> float:
        self.board: Board = board
        evaluation = 0
        for tile in board.tiles[Color.BLACK] + board.tiles[Color.WHITE]:
            evaluation += self.evaluate_distance_to_opponent_base(tile)
        available_black_moves = board.get_all_valid_moves(Color.BLACK)
        available_white_moves = board.get_all_valid_moves(Color.WHITE)
        evaluation -= self.available_moves_factor * len(available_black_moves)
        evaluation += self.available_moves_factor * len(available_white_moves)
        return evaluation
    
    def evaluate_distance_to_opponent_base(self, tile: str) -> float:
        color = self.board.get_tile_content(tile)
        if color == Color.NONE:
            raise ValueError(f"No piece at tile {tile}")
        opponent_base = self.board.base_tile[color.opposite()]
        factor: int = -1 * color.value
        initiative_factor = 1.0 / self.initiative_factor if color == self.board.current_player else 1.0
        return factor * initiative_factor * self.distance_factor * distance(tile, opponent_base)

    @override
    def name(self):
        return f"Simple Heuristic (df:{self.distance_factor}, amf:{self.available_moves_factor})"
    
class ExponentialHeuristic(Heuristic):
    def __init__(self, distance_factor: float = 1.0, flexibily_factor: float = 1.0, distance_exponent: float = 1.5, flexibility_exponent: float = 1.5):
        super().__init__()
        self.distance_factor: float = distance_factor
        self.flexibiliy_factor: float = flexibily_factor
        self.distance_exponent: float = distance_exponent
        self.flexibility_exponent: float = flexibility_exponent

    @override
    def evaluate(self, board: Board) -> float:
        self.board: Board = board
        evaluation = 0
        if self.distance_factor != 0:
            evaluation += self.distance_evaluation() * self.distance_factor
        if self.flexibiliy_factor != 0:
            evaluation += self.flexibility_evaluation() * self.flexibiliy_factor
        return evaluation
  
    def distance_evaluation(self) -> float:
        evaluation = 0
        for tile in self.board.tiles[Color.BLACK] + self.board.tiles[Color.WHITE]:
            distance = self._get_distance_to_opponent_base(tile)
            if distance == 0: # Victory condition
                return float("inf") * self.board.get_tile_content(tile).value
            distance_score = pow((12 - distance), self.distance_exponent)
            evaluation += distance_score * self.board.get_tile_content(tile).value
        return evaluation
    
    def _get_distance_to_opponent_base(self, tile: str) -> int:
        color = self.board.get_tile_content(tile)
        if color == Color.NONE:
            raise ValueError(f"No piece at tile {tile}")
        opponent_base = self.board.base_tile[color.opposite()]
        return distance(tile, opponent_base)


    def flexibility_evaluation(self) -> float:
        evaluation = 0.0
        flexibility: dict[Color, float] = {}
        for color in Color.BLACK, Color.WHITE:
            flexibility[color] = len(self.board.get_all_valid_moves(color))
        if flexibility[self.board.current_player] == 0: # Loss condition
            return float("-inf") * self.board.current_player.value
        for color, flex in flexibility.items():
            flexibility_score = pow(flex, self.flexibility_exponent)
            evaluation += flexibility_score * color.value
        return evaluation

    @override
    def name(self):
        return f"Exponential Heuristic (df:{self.distance_factor}, ff:{self.flexibiliy_factor}) (de:{self.distance_exponent}, fe:{self.flexibility_exponent})"

from copy import deepcopy
from typing import override

from topcap.core.common import Player, Board, Color
from topcap.utils.topcap_utils import simulate_thinking_time
from .utils.heuristic import Heuristic

class HeuristicAI(Player):
    def __init__(self, heuristic : Heuristic, name: str = "Heuristic AI", verbose: bool = True):
        super().__init__(name, verbose)
        self.heuristic: Heuristic = heuristic

    @override
    def get_move(self, board : Board):
        available_moves = board.get_all_valid_moves(self.color)
        if not available_moves:
            raise ValueError("No available_moves! Cannot call get_move() in a lost state")
        best_evaluation = float("-inf")
        best_move = None
        for move in available_moves:
            new_board = deepcopy(board)
            new_board.move(move)
            evaluation = self.heuristic.evaluate(new_board)
            if self.color == Color.BLACK:
                evaluation = -evaluation
            if evaluation > best_evaluation or best_move is None:
                best_evaluation = evaluation
                best_move = move
        if self.verbose:
            print(f"Chose move {best_move} with evaluation {best_evaluation:.1f}")
            # simulate_thinking_time(name=self.name)
        assert best_move
        return best_move

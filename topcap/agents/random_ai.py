from typing import override
import random

from topcap.core.common import Player, Board
from topcap.utils.topcap_utils import simulate_thinking_time

class RandomAI(Player):
    def __init__(self, name: str, verbose: bool = True):
        super().__init__(name, verbose)

    @override
    def get_move(self, board : Board):
        available_moves = board.get_all_valid_moves(self.color)
        move = random.choice(available_moves)
        if self.verbose:
            pass
            # simulate_thinking_time(name=self.name)
        return move

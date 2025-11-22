from typing import override
import random

from topcap.core.common import Player, Board, Move

class DeterministicAI(Player):
    def __init__(self, name: str, moves: list[Move], verbose: bool = True):
        super().__init__(name, verbose)
        self.moves: list[Move] = moves

    @override
    def get_move(self, board : Board):
        if not self.moves:
            raise ValueError("Ran out of moves, DeterministicAI must have moves defined until the end of the game!")
        return self.moves.pop(0)

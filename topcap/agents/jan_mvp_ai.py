from typing import override

from topcap.core.common import Player, Board, Move


class JanMVP(Player):
    def __init__(self, name: str, verbose: bool = True):
        super().__init__(name, verbose)

    @override
    def get_move(self, board: Board) -> Move:
        # my logic: each turn has to return a move

        # board, move -> state, action
        possible_moves = board.get_all_valid_moves(self.color)
        return possible_moves[0]

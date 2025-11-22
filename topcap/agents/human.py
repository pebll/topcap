from typing import override

from topcap.core.common import Player, Board, Move

class Human(Player):
    def __init__(self, name: str):
        super().__init__(name)

    @override
    def get_move(self, board: Board):
        while True:
            move_str = input("Enter your move (e.g., 'a1 a2'): ")
            move = self._parse_move(move_str)
            if move and board.move_is_valid(move, self.color, verbose=True):
                return move
            print("Please try again.")
      
    @staticmethod
    def _parse_move(move_str: str) -> Move | None:
        move_str = move_str.strip()
        if len(move_str) != 5:
            print("Invalid move format. Must be like 'a1 a2'")
            return None
        return Move(move_str[:2], move_str[3:])


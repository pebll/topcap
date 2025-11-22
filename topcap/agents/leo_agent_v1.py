from topcap.core.common import Player, Board, Move, Color
from topcap.agents.rl_agent import ReinforcementLearningAgent


class LeoAgentV1(ReinforcementLearningAgent):
    def __init__(self, classname: str, name: str, verbose: bool = True, decay: float = 0.95, vv: bool = False):
        super().__init__(classname, name, verbose, decay, vv)
        # state -> (value, n)
        self.value = dict[str, tuple[float, int]]

    def get_move(self, board: Board):
        return super().get_move(board)
 
    def _choose_action(self, move_evaluations: dict[Move, float]) -> Move:
        return super()._choose_action(move_evaluations)
 
    def _evaluate_state_action_pair(self, board: Board, move: Move) -> float:
        return super()._evaluate_state_action_pair(board, move)

    def game_step_callback(self, player: Color, new_board: Board, rewards: tuple[float, float], terminal: bool):
        return super().game_step_callback(player, new_board, rewards, terminal)

    def _load_config(self):
        return super()._load_config()

    def _save_config(self):
        return super()._save_config()

    def _save_params(self):
        return super()._save_params()


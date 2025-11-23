from copy import deepcopy
from typing import final, override
import random
from topcap.core.common import Player, Board, Move, Color
from topcap.agents.rl_agent import ReinforcementLearningAgent


@final
class LeoAgentV1(ReinforcementLearningAgent):
    def __init__(self, name: str, verbose: bool = True, decay: float = 0.95, epsilon: float = 0.2, alpha: float = 0.2, vv: bool = False):
        classname = "leo_agent_v1"
        super().__init__(classname, name, verbose, decay, vv)
        self.params: dict[str, float] = {} # state -> (value, n)
        self.epsilon: float = epsilon # for epsilon greedy
        self.alpha: float = alpha # learning rate
        self.game_history: list[Board] = []

    def _get_value(self, board: Board):
        return self.params.get(board.to_code(), 0)
    
    def _set_value(self, board: Board, value: float):
        self.params[board.to_code()] = value
 
    @override
    def _choose_action(self, move_evaluations: dict[Move, float]) -> Move:
        if random.random() > self.epsilon:
            if self.color == Color.WHITE:
                move = max(move_evaluations, key=lambda x: move_evaluations[x])
            else:
                move = min(move_evaluations, key=lambda x: move_evaluations[x])
        else:
            move = random.choice(list(move_evaluations.keys()))
        return move
 
    @override
    def _evaluate_state_action_pair(self, board: Board, move: Move) -> float:
        new_board = deepcopy(board)
        new_board.move(move)
        return self._get_value(new_board)

    @override
    def load_latest(self) -> bool:
        worked = super().load_latest()
        print(f"Loaded agent at iteration {self.iteration}")
        print(f"Len of V-Table: {len(self.params)}")
        print(f"Eval of start position: {self._get_value(Board())}")
        return worked

    @override
    def game_step_callback(self, player: Color, new_board: Board, reward: float, terminal: bool):
        self.game_history.append(deepcopy(new_board))
        if not terminal or self.frozen:
            return
        # Game end callback
        if self.vv:
            print(f"Game ended, adding rewards")
        self.game_history.reverse() # most recent states first
        for board in self.game_history:
            old = self._get_value(board)
            new_value = old + (reward - old) * self.alpha
            self._set_value(board, new_value)
            reward *= self.decay
            if self.vv:
                print(f"Updated reward of board {board} from {old:.2f} to {new_value:.2f} (reward = {reward:.2f})")
        self.game_history = [] # reset history
        self.iteration += 1



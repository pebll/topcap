from typing import override
import random
import pickle
import os

from .utils.heuristic import Heuristic
from topcap.core.common import Player, Board, Move, Color

class QDicter(Player):
    def __init__(self, name: str, version: int = 1, verbose: bool = True, initialization : int | Heuristic = 0, decay: float = 0.95, epsilon: float = 0.5, vv: bool = False):
        super().__init__(name, verbose)
        self.version : int = version
        self.initialization: Heuristic | int = initialization
        self.decay: float = decay
        self.epsilon: float = epsilon
        self.vv: bool = vv
        self.q_table : dict[tuple[str, str], tuple[float, int]] = {} # (state, action) -> (q_value, n)
        self.game_history : list[tuple[str, str]] = []
        self.iteration : int = 0
        self.frozen : bool = False

    def _state_action_pair(self, board: Board, move: Move) -> tuple[str, str]:
        return  (board.to_hash(), move.to_hash())
    
    def freeze(self, frozen: bool = True):
        self.frozen = frozen

    @override
    def get_move(self, board : Board):
        available_moves = board.get_all_valid_moves(self.color)
        # print(f"available_moves: {available_moves}")
        q_values : dict[Move, tuple[float, int]] = {}
        for move in available_moves:
            state_action_pair = self._state_action_pair(board, move)
            q_values[move] = self._get_q_value(state_action_pair)
        if random.random() > self.epsilon:
            if self.color == Color.WHITE:
                move = max(q_values, key=lambda x: q_values[x][0])
            elif self.color == Color.BLACK:
                move = min(q_values, key=lambda x: q_values[x][0])

            if self.vv:
                print(f"The choice is between following moves:")
                for q_value in q_values.items():
                    print(f"{q_value[0]} ({q_value[1][0]:.2f}, {q_value[1][1]})")
                print(f"Choosing best move: {move} with Q value {q_values[move][0]:.2f} (n={q_values[move][1]})")
        else:
            move = random.choice(available_moves)
            # print(f"Choosing random move: {move} with Q value {q_values[move]}")
        state_action_pair = self._state_action_pair(board, move)
        self.game_history.append(state_action_pair)
        if self.verbose:
            pass
            # simulate_thinking_time(name=self.name)
        return move

    def _get_q_value(self, state_action_pair: tuple[str, str]) -> tuple[float, int]: # return (q_value, updated_count)
        if type(self.initialization) == int:
            init = self.initialization
        else:
            next_board : Board = Board.from_code(state_action_pair[0])
            next_move: Move = Move.from_code(state_action_pair[1])
            next_board.current_player = self.color
            if not next_board.move_is_valid(next_move, self.color, verbose=True):
                print(next_board.to_str())
                print(f"Trying to run move {next_move} as {self.color} on this board")
            next_board.move(next_move)
            init = self.initialization.evaluate(next_board)
            init *= self.color.value
        return self.q_table.get(state_action_pair, (init, 1))

    def _update_q_value(self, state_action_pair: tuple[str, str], reward: float):
        new_value : float
        new_count : int
        if self._get_q_value(state_action_pair)[1] == 0: # did not exist yet
            new_value = reward *2
            new_count = 1
            raise ValueError("This should never be reached!")
        else:
            old, n = self._get_q_value(state_action_pair)
            recall = min((1/n) * old, 100)
            new_value = recall + (1/(n+1))*(reward - recall)
            # print(f"Old: {old:.2f}, n: {n}")
            # print(f"recall: {recall:.2f}, reward: {reward:.2f}, new_value: {new_value:.2f}")
            new_count = n + 1
        self.q_table[state_action_pair] = (new_value, new_count)
        if self.vv:
            print(f"Updated q_value for {state_action_pair} (reward = {reward:.2f}) with new value {new_value:.2f} for the {new_count-1}th time.")

    def dirname(self) -> str:
        return f"topcap/agents/data/q_learner/{self.name}"

    def filename(self) -> str:
        return f"{self.dirname()}/{self.name}{self.version}_V{self.iteration}.pkl"

    def config_filename(self) -> str:
        """Filename for saving agent configuration parameters."""
        return f"{self.dirname()}/{self.name}{self.version}_config.pkl"

    @staticmethod
    def find_highest_version(name: str) -> int:
        """Find the highest version number for a given agent name. Returns 0 if no saves exist."""
        dirname = f"topcap/agents/data/q_learner/{name}"
        if not os.path.exists(dirname):
            return 0
        
        highest_version = 0
        prefix = name
        
        for filename in os.listdir(dirname):
            if filename.startswith(prefix) and filename.endswith('.pkl'):
                # Extract version from filename like "name1_V100.pkl" or "name2_V100.pkl"
                try:
                    # Find where the version number starts (after the name)
                    version_start = len(prefix)
                    version_end = filename.find('_V', version_start)
                    if version_end > version_start:
                        version_str = filename[version_start:version_end]
                        version = int(version_str)
                        if version > highest_version:
                            highest_version = version
                except ValueError:
                    # Skip files that don't match the expected format
                    continue
        
        return highest_version

    def _save_config(self):
        """Save agent configuration parameters (only called on first save)."""
        config = {
            'initialization': self.initialization,
            'decay': self.decay,
            'epsilon': self.epsilon,
            'vv': self.vv,
        }
        pickle.dump(config, open(self.config_filename(), 'wb'))

    def _load_config(self):
        """Load agent configuration parameters."""
        if not os.path.exists(self.config_filename()):
            raise FileNotFoundError(f"Config file not found: {self.config_filename()}")
        config = pickle.load(open(self.config_filename(), 'rb'))
        self.initialization = config.get('initialization')
        self.decay = config.get('decay')
        self.epsilon = config.get('epsilon')
        self.vv = config.get('vv')

    def save(self): 
        if not os.path.exists(path=self.dirname()):
            os.makedirs(self.dirname(), exist_ok=True)

        if os.path.exists(self.filename()):
            raise FileExistsError("File already exists! Please change name or version of your agent")
        
        # Save config on first save for this version (if config doesn't exist yet)
        if not os.path.exists(self.config_filename()):
            self._save_config()
        
        pickle.dump(self.q_table, open(self.filename(), 'wb'))

    def _find_latest_iteration(self) -> int | None:
        """Find the latest iteration number for the current name+version. Returns None if no saves exist."""
        if not os.path.exists(self.dirname()):
            return None
        
        prefix = f"{self.name}{self.version}_V"
        latest_iteration = None
        
        for filename in os.listdir(self.dirname()):
            if filename.startswith(prefix) and filename.endswith('.pkl'):
                # Extract iteration number from filename like "name1_V100.pkl"
                try:
                    iteration_str = filename[len(prefix):-4]  # Remove prefix and .pkl
                    iteration = int(iteration_str)
                    if latest_iteration is None or iteration > latest_iteration:
                        latest_iteration = iteration
                except ValueError:
                    # Skip files that don't match the expected format
                    continue
        
        return latest_iteration

    def find_all_iterations(self) -> list[int]:
        """Find all iteration numbers for the current name+version. Returns sorted list of iterations."""
        if not os.path.exists(self.dirname()):
            return []
        
        prefix = f"{self.name}{self.version}_V"
        iterations = []
        
        for filename in os.listdir(self.dirname()):
            if filename.startswith(prefix) and filename.endswith('.pkl'):
                # Extract iteration number from filename like "name1_V100.pkl"
                try:
                    iteration_str = filename[len(prefix):-4]  # Remove prefix and .pkl
                    iteration = int(iteration_str)
                    iterations.append(iteration)
                except ValueError:
                    # Skip files that don't match the expected format
                    continue
        
        return sorted(iterations)

    def load_latest(self) -> bool:
        """Load the latest iteration for the current name+version. Returns True if loaded, False if no saves exist."""
        latest_iteration = self._find_latest_iteration()
        if latest_iteration is None:
            return False
        self.load(latest_iteration)
        return True

    def load(self, iteration: int):
        """Load agent at a specific iteration. Also loads config if it exists."""
        # Load config if it exists (only once per instance)
        if os.path.exists(self.config_filename()) and not hasattr(self, '_config_loaded'):
            self._load_config()
            self._config_loaded = True
        
        self.iteration = iteration
        self.q_table = pickle.load(open(self.filename(), 'rb'))

    @override
    def game_over_callback(self, win: bool):
        # TODO: add a opponnent game history and learn from his mistakes aswell: double learning speed :D
        # TODO: make the value function be objective (not subjective because then lim -> inf = 0 everywhere...)
        if self.frozen:
            return
        win_reward = 10.0 if self.color == Color.WHITE else -10.0
        if self.verbose:
            print(f"Game over, learning from my mistakes...")
            print(f"Size of my Q Table: {len(self.q_table)}")
        reward : float = win_reward if win else -win_reward
        self.game_history.reverse() # most recent states first
        for state_action_pair in self.game_history:
            self._update_q_value(state_action_pair, reward)
            reward *= self.decay
        self.game_history = [] # reset history
        self.iteration += 1

    @override
    def __str__(self) -> str:
        name = self.name
        if self.version > 1:
            name += str(self.version)
        if self.frozen:
            name += f"_V{self.iteration}"
        return name



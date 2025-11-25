from abc import abstractmethod, ABC
from typing import override, Any
import pickle
import os

from topcap.core.common import Player, Board, Move, Color

class ReinforcementLearningAgent(Player, ABC):
    def __init__(self, classname: str, name: str, verbose: bool = True, decay: float = 0.95, vv: bool = False):
        super().__init__(name, verbose)
        self.classname: str = classname
        self.vv: bool = vv
        self.decay: float = decay
        self.iteration : int = 0
        self.params: Any = None
        self.frozen : bool = False

    def freeze(self, frozen: bool = True):
        self.frozen = frozen

    @override
    def get_move(self, board : Board):
        available_moves = board.get_all_valid_moves(self.color)
        move_evaluations: dict[Move, float] = {}
        for move in available_moves:
            move_evaluations[move] = self._evaluate_state_action_pair(board, move)
        if self.vv:
            print(f"The choice is between following moves:")
            for move, eval in move_evaluations.items():
                print(f"{move}: {eval:.2f})")
        move = self._choose_action(move_evaluations) # TODO: replace by a ExplorationStrategy class instance
        if self.vv:
            print(f"Chose move {move} with eval {move_evaluations[move]:.2f}")
        return move

    @abstractmethod
    def _evaluate_state_action_pair(self, board: Board, move: Move) -> float:
        """evaluates a move made in a given board state"""
        pass

    @abstractmethod
    def _choose_action(self, move_evaluations: dict[Move, float]) -> Move:
        """ Chooses a move from move_evaluations based on some exploration strategy e.g. epsilon_greedy"""
        pass # TODO: replace by strategy class at some point

    @abstractmethod
    def game_step_callback(self, player: Color, new_board: Board, reward: float, terminal: bool):
        """Is called when move was performed by any player
            rewards: (white_reward, black_reward) always subjective pov"""
        pass

    # SAVING & LOADING STUFF
    
    def dirname(self) -> str:
        return f"topcap/agents/data/{self.classname}/{self.name}"

    def filename(self) -> str:
        return f"{self.dirname()}/{self.name}_V{self.iteration:07d}.pkl"

    def config_filename(self) -> str:
        """Filename for saving agent configuration parameters."""
        return f"{self.dirname()}/{self.name}_config.pkl"

    def _save_config(self):
        # TODO: make a config class!!!
        """Save agent configuration parameters (only called on first save).
        example implementation:"""
        config = {
            'decay': self.decay,
            'vv': self.vv,
        }
        pickle.dump(config, open(self.config_filename(), 'wb'))

    def _load_config(self):
        """Load agent configuration parameters.
        example implementation:"""
        if not os.path.exists(self.config_filename()):
            raise FileNotFoundError(f"Config file not found: {self.config_filename()}")
        config = pickle.load(open(self.config_filename(), 'rb'))
        self.decay = config.get('decay')
        self.vv = config.get('vv')

    def _save_params(self):
        """Save agent params e.g. Q Table or NN weights
        example implementation:"""
        pickle.dump(self.params, open(self.filename(), 'wb'))

    def _load_params(self):
        self.params = pickle.load(open(self.filename(), 'rb'))

    def save(self): 
        """Save current params (and config if not done yet)
        Creates directory if necessary and throws an error if save already exists"""
        if not os.path.exists(path=self.dirname()):
            os.makedirs(self.dirname(), exist_ok=True)

        if os.path.exists(self.filename()):
            raise FileExistsError(f"Save with filename {self.filename()} already exists! Please change name of your agent")
        
        # Save config on first save (if config doesn't exist yet)
        if not os.path.exists(self.config_filename()):
            self._save_config()

        self._save_params()

    def load(self, iteration: int):
        """Load agent at a specific iteration. Also loads config if it exists."""
        # Load config if it exists (only once per instance)
        if os.path.exists(self.config_filename()) and not hasattr(self, '_config_loaded'):
            self._load_config()
            self._config_loaded = True
        
        self.iteration = iteration
        self._load_params()

    def _find_latest_iteration(self) -> int | None:
        """Find the latest iteration number for the current name. Returns None if no saves exist."""
        if not os.path.exists(self.dirname()):
            return None
        
        prefix = f"{self.name}_V"
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
        """Find all iteration numbers for the current name. Returns sorted list of iterations."""
        if not os.path.exists(self.dirname()):
            return []
        
        prefix = f"{self.name}_V"
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
        """Load the latest iteration for the current name. Returns True if loaded, False if no saves exist."""
        latest_iteration = self._find_latest_iteration()
        if latest_iteration is None:
            return False
        self.load(latest_iteration)
        return True


    @override
    def __str__(self) -> str:
        name = self.name
        if self.frozen:
            name += f"_V{self.iteration}"
        return name


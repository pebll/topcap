from copy import deepcopy
from collections import Counter
import traceback

from topcap.agents.rl_agent import ReinforcementLearningAgent
from topcap.core.common import Board, Player, Color, Move
from topcap.utils import WinReason

class Game:
    def __init__(self, verbose: bool = True):
        self.verbose: bool = verbose
        self.white: Player
        self.black: Player
        self.board: Board
        self.board_states: list[Board]
        self.board_state_counts: Counter[Board]
        self.player_evaluations: dict[Player, list[float]]
        self.current_step: int
        self.current_player: Player
        self.winner: Color
        self.win_reason: WinReason
        self.game_over: bool

    def _setup_new_game(self, white: Player, black: Player, custom_board: Board | None = None):
        self.white = white
        self.black = black
        self.white.set_color(Color.WHITE)
        self.black.set_color(Color.BLACK)
        self.board = Board() if not custom_board else custom_board
        self.board_states = [] # for triple repetition
        self.board_state_counts = Counter()
        self.current_step = 0
        self.current_player = self.white
        self.winner = Color.NONE
        self.win_reason = WinReason.NONE 
        self.game_over = False

    def log(self, message: str):
        if self.verbose:
            print(message)

    def run_game(self, white: Player, black: Player, custom_board: Board | None = None):
        self._setup_new_game(white, black, custom_board)
        self.log("Here begins the game of topcap!\n")
        self.log(f"{self.white} vs {self.black} ")
        self._save_board_state()
        self._print_game_state()
        while not self.game_over:
            try:
                next_move = self.current_player.get_move(self.board)
                self._game_step(next_move)
            except Exception as error:
                self._handle_crash(error)
            if not self.game_over:
                # do not print next game state if game is over
                self._print_game_state()

    def _handle_crash(self, error):
        print(f"ERROR: {self.current_player} crashed!! Type: {type(error).__name__}, Error: {error}")
        self.log(traceback.format_exc())
        # TODO: add step_callback?
        self.win_reason = WinReason.CRASHED
        self.winner = Color.WHITE if self.current_player.color == Color.BLACK else Color.BLACK
        self.game_over = True
        self.log(f"{self.winner} wins because {self.win_reason.value}!")
        
    def _game_step(self, next_move: Move):
        if not self.board.move_is_valid(next_move, self.current_player.color):
            # INVALID_MOVE
            self.winner, self.win_reason = (self.current_player.color.opposite(), WinReason.INVALID_MOVE)
            self.game_over = True
        else:
            # VALID MOVE
            self.board.move(next_move)
            self.log(f"{self.current_player} moved from {next_move.from_tile} to {next_move.to_tile}")
            self.winner, self.win_reason = self.board.get_win_reason()
            self.game_over = self.win_reason != WinReason.NONE

        if not self.game_over:
            self.current_step += 1
            self.current_player = [self.white, self.black][self.current_step % 2]
            self._save_board_state()
            if self._check_threefold_repetition():
                self.winner, self.win_reason = (Color.NONE, WinReason.DRAW_THREEFOLD_REPETITION)
                self.game_over = True
        
        MAX_REWARD = 10.0
        reward = 0
        if self.game_over:
            self.log(self.board.to_str())
            if not self.winner:
                # DRAW
                self.log(f"Draw due to {self.win_reason}!")
            else: 
                # WIN
                reward = MAX_REWARD * self.winner.value
                self.log(f"{self.winner} wins because {self.win_reason}!")

        # AGENT GAME STEP CALLBACKS
        if isinstance(self.white, ReinforcementLearningAgent):
            self.white.game_step_callback(self.current_player.color, self.board, reward, self.game_over)
        if isinstance(self.black, ReinforcementLearningAgent):
            self.black.game_step_callback(self.current_player.color, self.board, reward, self.game_over)

    def _print_game_state(self):
        next_available_moves = self.board.get_all_valid_moves(self.current_player.color)
        self.log(f"\n\n\nGame round: {(self.current_step + 1)// 2 + 1}, {self.current_player}'s turn")
        self.log(f"Available moves for {self.current_player}: {next_available_moves}")
        self.log(self.board.to_str())
    
    def _save_board_state(self):
        # Use __copy__ instead of deepcopy for better performance
        # Board's __copy__ is optimized and sufficient for our needs
        board_copy = self.board.__copy__()
        self.board_states.append(board_copy)
        # Track board state occurrences for threefold repetition detection
        self.board_state_counts[board_copy] += 1
    
    def _check_threefold_repetition(self):
        """Check if the current board state has appeared three times (threefold repetition)."""
        current_count = self.board_state_counts[self.board]
        if current_count >= 3:
            return True
        return False

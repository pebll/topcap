from collections import defaultdict
from copy import deepcopy
import random
import matplotlib.pyplot as plt
from datetime import datetime

from topcap.agents.leo_agent_v1 import LeoAgentV1
from topcap.agents.rl_agent import ReinforcementLearningAgent

from .game import Game
from topcap.agents import RandomAI
from topcap.core.common import Player, Color
from topcap.utils import WinReason

class Arena: 
    def __init__(self) -> None:
        self.wins_by_player: defaultdict[str, int] = defaultdict(int)
        self.wins_by_type: defaultdict[str, int] = defaultdict(int)
        self.total_games: int = 0
        # Track cumulative wins per game for winrate over time
        self.game_history: list[dict[str, int]] = []  # List of {player_name: cumulative_wins} per game
        # Track param size over time
        self.param_size_history: list[int] = []


    def _run_single_game(self, white: Player, black: Player, verbose: bool=False) -> tuple[Player | None, WinReason, Game]:
        game = Game(verbose)
        game.run_game(white, black)
        winner = game.winner
        winner_player = None
        if winner == Color.WHITE:
            winner_player = white
        elif winner == Color.BLACK:
            winner_player = black
        win_reason = game.win_reason
        return winner_player, win_reason, game

    def run_sample_game(self, white: Player, black: Player, vv: bool = True):
        game = Game()
        agents = [white, black]
        for agent in agents:
            if vv: 
                if isinstance(agent, ReinforcementLearningAgent):
                    agent.vv = True
                    if isinstance(agent, LeoAgentV1):
                        agent.epsilon = 0


        game.run_game(white, black)

    def run_games(self, count: int, player_1: Player, player_2: Player, verbose: bool = False, plot_stats: bool = True) -> None:
        """Runs X games with alternating colors"""
        if not verbose:
            player_1.verbose = False
            player_2.verbose = False
        for i in range(count):
            white = player_1 if i%2==0 else player_2
            black = player_1 if i%2==1 else player_2
            winner, win_reason, game = self._run_single_game(white, black, verbose)
            if winner:
                print(f"Game {i+1}/{count}: {winner} wins because {win_reason.value}")
                # Track stats
                self.wins_by_player[winner.name] += 1
            else:
                print(f"Game {i+1}/{count}: Draw - {win_reason.value}")
                self.wins_by_player["Draw"] += 1
            self.wins_by_type[win_reason.name] += 1
            self.total_games += 1
            
            # Track cumulative wins for winrate over time
            cumulative_wins = dict(self.wins_by_player)
            self.game_history.append(cumulative_wins)
        
        if count > 1 and plot_stats:
            self._plot_stats()

    def _plot_stats(self) -> None:
        """Plot winrate and win type statistics"""
        fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize=(20, 4))
        
        # Winrate over time (moving average over last 20 games)
        if self.game_history:
            games = list(range(1, len(self.game_history) + 1))
            players: list[str] = list(self.wins_by_player.keys())
            
            # Calculate which player won each game
            game_winners = []
            prev_wins = {}
            for cumulative_wins in self.game_history:
                for player in players:
                    current_wins = cumulative_wins.get(player, 0)
                    prev_wins_for_player = prev_wins.get(player, 0)
                    if current_wins > prev_wins_for_player:
                        game_winners.append(player)
                        break
                prev_wins = dict(cumulative_wins)
            
            for player in players:
                winrates = []
                window_size = 50
                for i in range(len(game_winners)):
                    # Look back at the last window_size games (or fewer if not enough games yet)
                    start_idx = max(0, i - window_size + 1)
                    window_winners = game_winners[start_idx:i+1]
                    wins_in_window = sum(1 for winner in window_winners if winner == player)
                    games_in_window = len(window_winners)
                    winrate = wins_in_window / games_in_window if games_in_window > 0 else 0
                    winrates.append(winrate)
                ax1.plot(games, winrates, label=player, marker='o', markersize=3)
            
            ax1.set_title('Winrate Over Time')
            ax1.set_ylabel('Winrate')
            ax1.set_xlabel('Game Number')
            ax1.legend()
            ax1.grid(True, alpha=0.3)
            ax1.set_ylim([0, 1])
        
        # Total wins by player
        players: list[str] = list(self.wins_by_player.keys())
        wins: list[int] = [self.wins_by_player[p] for p in players]
        ax2.bar(players, wins)
        ax2.set_title('Total Wins by Player')
        ax2.set_ylabel('Wins')
        ax2.set_xlabel('Player')
        
        # Win type distribution
        win_types: list[str] = list(self.wins_by_type.keys())
        win_counts: list[int] = [self.wins_by_type[wt] for wt in win_types]
        ax3.bar(win_types, win_counts)
        ax3.set_title('Win Type Distribution')
        ax3.set_ylabel('Count')
        ax3.set_xlabel('Win Type')
        ax3.tick_params(axis='x', rotation=45)
        
        # Params size over time
        if self.param_size_history:
            games = list(range(1, len(self.param_size_history) + 1))
            ax4.plot(games, self.param_size_history, marker='o', markersize=3, linestyle='-', linewidth=2)
            ax4.set_title('Params Size Over Time')
            ax4.set_ylabel('Number of Params')
            ax4.set_xlabel('Game Number')
            ax4.grid(True, alpha=0.3)
        else:
            ax4.text(0.5, 0.5, 'No params data available', 
                    horizontalalignment='center', verticalalignment='center', 
                    transform=ax4.transAxes)
            ax4.set_title('Params Size Over Time')
        
        plt.tight_layout()
        plt.show()

    def train(self, agent: ReinforcementLearningAgent, continue_training: bool = True, first_opponent: Player | None = None, save_frequency: int = 100, num_games: int = 1000, verbose: bool = False, sample_size: int = 10) -> None:
        """ Trains a RL agent 
        
        Args:
            agent: The agent to train
            continue_training: True to continue from existing, False to reset
            first_opponent: Initial opponent
            num_games: The number of games to train
            save_frequency: How often to save a snapshot
        """
        if not continue_training:
            # TODO: reset and delete saves? or do not allow this in the first place?
            raise NotImplementedError
        if agent.load_latest():
            print(f"Loaded existing agent {agent} from iteration {agent.iteration}")
        else:
            print(f"No save found, training agent {agent} from scratch")
        
        # Find all saved iterations and load them as snapshots
        iterations = agent.find_all_iterations()
        if sample_size > 1:
            iterations = self._sample_to_size(iterations, sample_size)
        initial_snapshots: list[Player] = []
        
        if iterations:
            print(f"Loading {len(iterations)} existing snapshots...")
            for iteration in iterations:
                snapshot_agent = deepcopy(agent)
                snapshot_agent.load(iteration)
                snapshot_agent.freeze()
                # snapshot_agent.epsilon = 0 # greedy the snapshot
                initial_snapshots.append(snapshot_agent)
                print(f"  Loaded snapshot at iteration {iteration}")
        
        # Continue training with existing snapshots
        self._train_agent(agent, first_opponent, save_frequency, num_games, verbose, initial_snapshots)

    def _train_agent(self, agent: ReinforcementLearningAgent, first_opponent: Player | None, save_frequency: int, num_games: int, verbose: bool, initial_snapshots: list[Player] | None = None) -> None:
        """Internal method to train an agent (shared logic for train_from_agent and train_continue).
        
        Args:
            agent: The agent to train
            first_opponent: Initial opponent (used if no initial snapshots provided)
            save_frequency: How often to save a snapshot
            num_games: Number of games to train
            verbose: Whether to print detailed game information
            initial_snapshots: Optional list of initial snapshots to use as opponents
        """
        if not verbose:
            agent.verbose = False
        
        # Initialize snapshot pool
        snapshot_opponents: list[Player] = []
        
        if initial_snapshots:
            # Use provided snapshots (from continuing training)
            snapshot_opponents.extend(initial_snapshots)
        
        # Add first_opponent if provided and not already in snapshots
        if first_opponent:
            snapshot_opponents.append(first_opponent)
        elif not initial_snapshots:
            # Only add default opponent if we have no snapshots
            snapshot_opponents.append(RandomAI("defaulti"))
        
        log_frequency = 50
        start_time = datetime.now()
        position_count = 0
        for i in range(num_games):
            # Every save_frequency games, save the agent and add a snapshot
            if i > 0 and i % save_frequency == 0:
                agent.save()
                snapshot = deepcopy(agent)
                snapshot.freeze()
                # snapshot.epsilon = 0 # greedy the snapshot
                snapshot_opponents.append(snapshot)
                print(f"Game {i}/{num_games}: Saving snapshot {snapshot}")
            if i > 0 and i % log_frequency == 0:
                duration = (datetime.now() - start_time).total_seconds()
                print(f"Stats:")
                print(f"{(log_frequency/duration):.0f} games/s")
                print(f"{(position_count/duration):.0f} posistions/s")
                print(f"{(position_count/log_frequency):.0f} posistions/game")
                start_time = datetime.now()
                position_count = 0
            
            opponent = random.choice(snapshot_opponents)
            
            # Alternate colors
            white = agent if i % 2 == 0 else opponent
            black = agent if i % 2 == 1 else opponent
            
            # Run the game
            winner, win_reason, game = self._run_single_game(white, black, verbose)
            if winner:
                looser = agent if winner == opponent else opponent
                # Color: green if training agent wins, red if loses
                color = '\033[92m' if winner is agent else '\033[91m'  # Green or Red
                reset = '\033[0m'
                print(f"{color}Game {i+1}/{num_games}: {winner} beats {looser} because {win_reason.value}{reset}")
                # Track stats
                winner_category = "agent" if winner == agent else "opponent"
                self.wins_by_player[winner_category] += 1
            else:
                print(f"\033[93mGame {i+1}/{num_games}: Draw - {win_reason.value}\033[0m")
                self.wins_by_player["Draw"] += 1
            self.wins_by_type[win_reason.name] += 1
            self.total_games += 1
            position_count += game.current_step
            
            # Track cumulative wins for winrate over time
            cumulative_wins = dict(self.wins_by_player)
            self.game_history.append(cumulative_wins)
            self.param_size_history.append(len(agent.params))

        
        # Save final state
        agent.save()
        
        # Display final stats
        print(f"\n=== Training Complete ===")
        print(f"Training agent: {agent.name}")
        print(f"Total games: {num_games}")
        print(f"Snapshots created: {len(snapshot_opponents)}")
        
        if num_games > 1:
            self._plot_stats()

    def test_progress_self(self, agent: ReinforcementLearningAgent, verbose: bool = False, sample_size : int = 10) -> None:
        """Test all saved iterations of an agent against an opponent and plot winrate over iterations.
        
        Args:
            opponent: Opponent to test against
            num_test_games: Number of test games to run for each iteration
            verbose: Whether to print detailed game information
        """
        iterations = agent.find_all_iterations()
        if sample_size > 1:
            iterations = self._sample_to_size(iterations, sample_size+1)
        
        if not iterations:
            print(f"No saved iterations found for agent {agent}")
            return
        
        num_test_games = len(iterations) - 1
        print(f"Found {len(iterations)} iterations to test: {iterations}")
        print(f"Running {num_test_games} test games per iteration against self...")
        
        # Track winrates for each iteration
        iteration_winrates: dict[int, float] = {}
        
        for iteration in iterations:
            opponent = deepcopy(agent)
            opponent.freeze()
            # opponent.epsilon = 0.03
            test_agent = deepcopy(agent)
            test_agent.load(iteration)
            test_agent.freeze()  # Freeze to prevent learning during testing
            # test_agent.epsilon = 0.03 #TEMP: make it greedy for the test
            if not verbose:
                test_agent.verbose = False
            wins = 0
            # Run test games
            for i, opponent_it in enumerate(iterations):
                opponent.load(opponent_it)
                if opponent.iteration == test_agent.iteration:
                    continue # do not play against self
                # Alternate colors
                white = test_agent if i % 2 == 0 else opponent
                black = test_agent if i % 2 == 1 else opponent
                
                winner, _, _ = self._run_single_game(white, black, verbose)
                
                # Only count wins (not draws) for winrate calculation
                if winner == test_agent:
                    wins += 1
                
            winrate = wins / num_test_games
            iteration_winrates[iteration] = winrate
            print(f"Iteration {iteration}: {wins}/{num_test_games} wins ({winrate:.1%} winrate)")
            
        # Plot results
        self._plot_progress(iteration_winrates, agent, opponent.name)

    def _sample_to_size(self, lst, target):
        n = len(lst)
        if target <= 0 or n == 0:
            return []
        if target >= n:
            return lst[:]
        step = (n - 1) / (target - 1)
        return [lst[min(int(round(i*step)), n-1)] for i in range(target)]

    def test_progress(self, agent: ReinforcementLearningAgent, opponent: Player, num_test_games: int = 100, verbose: bool = False, sample_size:int = 10) -> None:
        """Test all saved iterations of an agent against an opponent and plot winrate over iterations.
        
        Args:
            opponent: Opponent to test against
            num_test_games: Number of test games to run for each iteration
            verbose: Whether to print detailed game information
        """
        # Create a temporary agent to find iterations
        iterations = agent.find_all_iterations()
        
        if not iterations:
            print(f"No saved iterations found for agent {agent}")
            return
        if sample_size > 1:
            iterations = self._sample_to_size(iterations, sample_size)
        
        print(f"Found {len(iterations)} iterations to test: {iterations}")
        print(f"Running {num_test_games} test games per iteration against {opponent.name}...")
        
        # Track winrates for each iteration
        iteration_winrates: dict[int, float] = {}
        
        # Disable verbose for opponent during testing
        if not verbose:
            opponent.verbose = False
        
        for iteration in iterations:
            # Load the agent at this iteration (config will be loaded automatically)
            test_agent = deepcopy(agent)
            test_agent.load(iteration)  # This will load both q_table and config
            test_agent.freeze()  # Freeze to prevent learning during testing
            # test_agent.epsilon = 0.03 #TEMP: make it greedy for the test
            
            if not verbose:
                test_agent.verbose = False
            
            # Run test games
            wins = 0
            for i in range(num_test_games):
                # Alternate colors
                white = test_agent if i % 2 == 0 else opponent
                black = test_agent if i % 2 == 1 else opponent
                
                winner, _, _ = self._run_single_game(white, black, verbose)
                
                # Only count wins (not draws) for winrate calculation
                if winner == test_agent:
                    wins += 1
            
            winrate = wins / num_test_games
            iteration_winrates[iteration] = winrate
            print(f"Iteration {iteration}: {wins}/{num_test_games} wins ({winrate:.1%} winrate)")
        
        # Plot results
        self._plot_progress(iteration_winrates, agent, opponent.name)
    
    def _plot_progress(self, iteration_winrates: dict[int, float], agent: ReinforcementLearningAgent, opponent_name: str) -> None:
        """Plot winrate over iterations."""
        iterations = sorted(iteration_winrates.keys())
        winrates = [iteration_winrates[it] for it in iterations]
        
        plt.figure(figsize=(10, 6))
        plt.plot(iterations, winrates, marker='o', linestyle='-', linewidth=2, markersize=6)
        plt.title(f'Training Progress: {agent.name} vs {opponent_name}')
        plt.xlabel('Iteration')
        plt.ylabel('Winrate')
        plt.grid(True, alpha=0.3)
        plt.ylim([0, 1])
        plt.axhline(y=0.5, color='r', linestyle='--', alpha=0.5, label='50% baseline')
        plt.legend()
        plt.tight_layout()
        plt.show()

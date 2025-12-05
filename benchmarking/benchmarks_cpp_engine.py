from copy import deepcopy
from collections import deque
import cProfile
import pstats
import random
from benchmarks_utils import print_nested_profile


import sys
sys.path.insert(0, './../cpp/build/')
from topcap_engine import (
    Board, initial_board, possible_moves, make_move, terminal_state, run_random_game,
    initial_board_fast, possible_moves_fast, make_move_fast, terminal_state_fast,
    GameState
)


    # board = engine.initial_board(8)
    # print(engine.board_to_string(board))
    # move = engine.Move(engine.Coordinates(1, 1), engine.Coordinates(2, 2))
    # print(f"move {move} is legal? : {engine.is_move_legal(board, move)}")

def bfs(max_depth : int, initial_board: Board):
    first_time_found: dict[Board, int] = {}
    queue: deque[Board] = deque()
    queue.append(initial_board)
    first_time_found[initial_board] = 0
    while queue:
        board = queue.popleft()
        depth = first_time_found[board]
        if depth == max_depth:
            continue
        for move in possible_moves(board):
            new_board = make_move(board, move)
            if new_board not in first_time_found:
                queue.append(new_board)
                first_time_found[new_board] = depth + 1
    return first_time_found.keys()


def run_random_game_python(N: int) -> int:
    """Run a single random game using Python loop (slower, for comparison)."""
    board = initial_board(N)
    step = 0
    
    while True:
        moves = possible_moves(board)
        if not moves:
            break
        
        # Pick a random move
        move = random.choice(moves)
        board = make_move(board, move)
        step += 1
        
        # Check if game is over
        is_terminal, _ = terminal_state(board)
        if is_terminal:
            break
    
    return step


def run_random_game_fast(N: int) -> int:
    """Run a single random game using fast API (native Python types)."""
    board = initial_board_fast(N)  # Returns tuple (white, black, N, whiteToPlay)
    step = 0
    
    while True:
        moves = possible_moves_fast(board)  # Returns list of tuples
        if not moves:
            break
        
        # Pick a random move
        move = random.choice(moves)  # move is ((x1,y1), (x2,y2))
        board = make_move_fast(board, move)  # Returns new tuple
        step += 1
        
        # Check if game is over
        is_terminal, _ = terminal_state_fast(board)
        if is_terminal:
            break
    
    return step


def run_random_game_gamestate(N: int) -> int:
    """Run a single random game using GameState (board stays in C++)."""
    state = GameState(N)  # Board lives in C++ memory
    step = 0
    
    while True:
        moves = state.get_possible_moves()  # Only converts moves, not board
        if not moves:
            break
        
        # Pick a random move
        move = random.choice(moves)  # move is ((x1,y1), (x2,y2))
        from_coords, to_coords = move
        state.make_move(from_coords[0], from_coords[1], to_coords[0], to_coords[1])
        step += 1
        
        # Check if game is over
        is_terminal, _ = state.get_terminal_state()
        if is_terminal:
            break
    
    return step


PERCENTAGE_THRESHOLD = 5 
MAX_INDENT = 5
def analyze_run_games(num_games: int = 100, N: int = 6):
    profiler = cProfile.Profile()
    profiler.enable()
    print(f'Beginning benchmarking RUN {num_games} GAMES performance (C++ engine)')
    ######################
    state_count = 0
    for i in range(num_games):
        steps = run_random_game(N)  # Use C++ implementation (much faster!)
        state_count += steps
    ######################
    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumtime')

    print(f" ---- {num_games} GAMES - Random vs Random (C++ engine) ----")
    print()
    print(f"- Games per second: {num_games/stats.total_tt:.1f} /s")
    print(f"- States per second: {state_count/stats.total_tt:.1f} /s")
    print(f"- Number of states: {state_count}")
    print(f"- Time to complete : {stats.total_tt:.3f} s")
    print()
    print_nested_profile(stats, threshold=PERCENTAGE_THRESHOLD, max_indent=MAX_INDENT)
    print()



DEPTHS = [ 4, 5]
FIRST_X = 5
N = 6
def analyze_dfs(depth: int):
    profiler = cProfile.Profile()
    profiler.enable()
    print(f'Beginning benchmarking DFS {depth} performance')
    ######################

    visited = bfs(depth, initial_board(N))
    ######################
    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumtime')

    print(f" ---- DEPTH = {depth} ----")
    print()
    print(f"- States per second: {len(visited)/stats.total_tt:.1f} /s")
    print(f"- Time to complete : {stats.total_tt:.3f} s")
    print(f"- Number of states : {len(visited)}")
    print()
    print_nested_profile(stats, PERCENTAGE_THRESHOLD, max_indent=MAX_INDENT)
    print()


NUM_GAMES = 2000
N = 6

def analyze_run_games_fast(num_games: int = 100, N: int = 6):
    """Benchmark using fast API (native Python types)."""
    profiler = cProfile.Profile()
    profiler.enable()
    print(f'Beginning benchmarking RUN {num_games} GAMES performance (C++ engine, FAST API)')
    ######################
    state_count = 0
    for i in range(num_games):
        steps = run_random_game_fast(N)
        state_count += steps
    ######################
    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumtime')

    print(f" ---- {num_games} GAMES - Random vs Random (C++ engine, FAST API) ----")
    print()
    print(f"- Games per second: {num_games/stats.total_tt:.1f} /s")
    print(f"- States per second: {state_count/stats.total_tt:.1f} /s")
    print(f"- Number of states: {state_count}")
    print(f"- Time to complete : {stats.total_tt:.3f} s")
    print()
    stats.print_stats(MAX_INDENT)


def analyze_run_games_gamestate(num_games: int = 100, N: int = 6):
    """Benchmark using GameState (board stays in C++)."""
    profiler = cProfile.Profile()
    profiler.enable()
    print(f'Beginning benchmarking RUN {num_games} GAMES performance (C++ engine, GameState)')
    ######################
    state_count = 0
    for i in range(num_games):
        steps = run_random_game_gamestate(N)
        state_count += steps
    ######################
    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumtime')

    print(f" ---- {num_games} GAMES - Random vs Random (C++ engine, GameState) ----")
    print()
    print(f"- Games per second: {num_games/stats.total_tt:.1f} /s")
    print(f"- States per second: {state_count/stats.total_tt:.1f} /s")
    print(f"- Number of states: {state_count}")
    print(f"- Time to complete : {stats.total_tt:.3f} s")
    print()
    stats.print_stats(MAX_INDENT)

def main():
    for depth in DEPTHS:
        analyze_dfs(depth)
    analyze_run_games(NUM_GAMES, N)
    print("\n" + "="*60 + "\n")
    analyze_run_games_fast(NUM_GAMES, N)
    print("\n" + "="*60 + "\n")
    analyze_run_games_gamestate(NUM_GAMES, N)


if __name__ == "__main__":
    main()


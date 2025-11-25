from copy import deepcopy
import cProfile
import pstats
from benchmarks_utils import print_nested_profile

from topcap.agents.random_ai import RandomAI
from topcap.core.common import Board, Color, Player
from topcap.core.game.arena import Arena


def bfs(max_depth : int, initial_board: Board):
    first_time_found: dict[int, int] = {}
    queue: list[int] = []
    queue.append(initial_board.to_hash())
    first_time_found[initial_board.to_hash()] = 0
    player = Color.WHITE
    while queue:
        hash = queue.pop(0)
        depth = first_time_found[hash]
        if depth == max_depth:
            continue
        board = Board()
        board.from_hash(hash)
        for move in board.get_all_valid_moves(player):
            new_board = deepcopy(board)
            new_board.move(move)
            if new_board not in first_time_found.keys():
                queue.append(new_board.to_hash())
                first_time_found[new_board.to_hash()] = depth + 1
        player = player.opposite()
    return first_time_found.keys()


PERCENTAGE_THRESHOLD = 20
MAX_INDENT = 5
def analyze_run_games(player1: Player, player2: Player, num_games: int = 100):
    profiler = cProfile.Profile()
    profiler.enable()
    print(f'Beginning benchmarking RUN {num_games} GAMES performance')
    ######################
    state_count = 0
    for i in range(num_games):
        arena = Arena()
        white = player1 if i%2==0 else player2
        black = player1 if i%2==1 else player2
        winner, win_reason, game = arena._run_single_game(white, black)
        state_count += game.current_step
    ######################
    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumtime')

    print(f" ---- {num_games} GAMES - {player1} VS {player2} ----")
    print()
    print(f"- Games per second: {num_games/stats.total_tt:.1f} /s")
    print(f"- States per second: {state_count/stats.total_tt:.1f} /s")
    print(f"- Number of states: {state_count}")
    print(f"- Time to complete : {stats.total_tt:.3f} s")
    # print(f"- Number of states : {len(visited)}")
    print()
    print_nested_profile(stats, threshold=PERCENTAGE_THRESHOLD, max_indent=MAX_INDENT)
    print()


DEPTHS = [ 2, 3, 4]
FIRST_X = 5
def analyze_dfs(depth: int):
    profiler = cProfile.Profile()
    profiler.enable()
    print(f'Beginning benchmarking DFS {depth} performance')
    ######################
    visited = bfs(depth, Board())
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
    print_nested_profile(stats, 20)
    print()


NUM_GAMES = 50
def main():
    for depth in DEPTHS:
        analyze_dfs(depth)
    player1 = RandomAI("Randi")
    player2 = RandomAI("Rando")
    analyze_run_games(player1, player2, NUM_GAMES)


if __name__ == "__main__":
    main()


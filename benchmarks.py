from copy import deepcopy
import profile
from topcap.core.common import Board, Color
import cProfile
import pstats
from collections import defaultdict
from benchmarks_utils import print_nested_profile


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

DEPTHS = [1, 2, 3, 4]
FIRST_X = 5
def analyze_dfs(depth: int):
    profiler = cProfile.Profile()
    profiler.enable()
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


def main():
    for depth in DEPTHS:
        analyze_dfs(depth)


if __name__ == "__main__":
    main()


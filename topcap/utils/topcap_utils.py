from enum import Enum
import time
import random

def is_tile_valid(tile: str) -> bool:
    if len(tile) != 2:
        return False
    if int(tile[1]) < 1 or int(tile[1]) > 6 or tile[0] not in ['a', 'b', 'c', 'd', 'e', 'f']:
        return False
    return True

def is_coords_valid(coords: tuple[int, int]) -> bool:
    if coords[0] < 0 or coords[0] > 5 or coords[1] < 0 or coords[1] > 5:
        return False
    return True

def tile_to_coords(tile: str) -> tuple[int, int]:
    """converts tile (a1) to coords ([x, y])"""
    if not is_tile_valid(tile):
        raise ValueError(f"Tile must be valid (a-f & 1-6)! e.g. a1, NOT {tile}!")
    return (int(tile[1]) - 1, ord(tile[0]) - ord('a'))

def coords_to_tile(coords: tuple[int, int]):
    """converts coords ([x, y]) to tile (a1)"""
    if not is_coords_valid(coords):
        raise ValueError(f"Tile must be valid (x: 0-5, y: 0-5)! e.g. [0, 0], NOT {coords}!")
    return chr(coords[1] + ord('a')) + str(coords[0] + 1)

def distance(tile1: str, tile2: str) -> int:
    coords1: tuple[int, int] = tile_to_coords(tile1)
    coords2: tuple [int, int] = tile_to_coords(tile2)
    return abs(coords1[0] - coords2[0]) + abs(coords1[1] - coords2[1])

def pointpointpoint() -> str:
    current_time = int(time.time()) % 3
    return '.' * (current_time + 1) + ' ' * (3 - current_time)

def simulate_thinking_time(name: str = "Noname", lower_bound: int = 2, upper_bound: int = 4):
    time_to_wait = random.randint(lower_bound, upper_bound)
    print(f"{name} is thinking.", end="", flush=True)
    for _ in range(time_to_wait):
        print(".", end="", flush=True)
        time.sleep(1)
    print(" done!")

class WinReason(Enum):
    NONE = "Unknown win reason.."
    BASE_REACHED = "Winner reached opponents base"
    NO_MOVES_LEFT = "Looser ran out of moves"
    INVALID_MOVE = "Looser submitted invalid move"
    CRASHED = "Looser crashed!"
    DRAW_THREEFOLD_REPETITION = "Game ended in a draw due to threefold repetition"

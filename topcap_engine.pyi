"""Type stubs for topcap_engine C++ extension module."""

class Coordinates:
    """Board coordinates."""
    x: int
    y: int
    def __init__(self, x: int, y: int) -> None: ...

class Move:
    """A move from one coordinate to another."""
    from_: Coordinates  # 'from' is a Python keyword, so it's 'from_' in Python
    to: Coordinates
    def __init__(self, from_: Coordinates, to: Coordinates) -> None: ...

class Board:
    """Game board state."""
    N: int
    whiteToPlay: bool
    def __init__(self, white: int, black: int, N: int, whiteToPlay: bool) -> None: ...

def initial_board(N: int) -> Board:
    """Create initial board state."""
    ...

def possible_moves(board: Board) -> list[Move]:
    """Get all possible moves for the current player."""
    ...

def make_move(board: Board, move: Move) -> Board:
    """Make a move and return new board state."""
    ...

def terminal_state(board: Board) -> tuple[bool, bool]:
    """Check if game is terminal. Returns (is_terminal, winner_is_white)."""
    ...

def is_move_legal(board: Board, move: Move) -> bool:
    """Check if a move is legal."""
    ...

def board_to_string(board: Board) -> str:
    """Convert board to string representation."""
    ...

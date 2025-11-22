from copy import deepcopy
from typing import override
import networkx as nx
import time

from topcap.core.common import Player, Board, Color, Move
from topcap.utils.topcap_utils import WinReason, pointpointpoint
from .utils.heuristic import Heuristic


class GraphAICopilot(Player):
    """
    Simplified and bug-fixed version of GraphAI.
    Uses a graph to explore game states and select moves using minimax evaluation.
    """
    
    def __init__(self, heuristic: Heuristic, name: str = "Graph AI Copilot", 
                 max_thinking_time: float = 5, verbose: bool = True, 
                 vv: bool = False, vvv: bool = False):
        super().__init__(name, verbose)
        self.heuristic: Heuristic = heuristic
        self.vv: bool = vv
        self.vvv: bool = vvv
        self.graph: nx.Graph[Board] = nx.Graph()
        self.current_position: Board = Board()
        self.max_thinking_time: float = max_thinking_time
        self.current_level: list[Board] = []  # Fixed: Initialize properly
        
    def _is_terminal_state(self, board: Board) -> bool:
        """Check if a board state is terminal (game over)."""
        _, win_reason = board.get_win_reason() 
        return win_reason != WinReason.NONE
    
    def _is_move_repeated_thrice(self, move_history: list[Move]) -> bool:
        """
        Check if the same move has been made three times consecutively.
        Returns True if the last three moves are identical.
        """
        if len(move_history) < 3:
            return False
        
        last_three = move_history[-3:]
        # Check if all three moves are the same
        first_move = last_three[0]
        return all(
            move.from_tile == first_move.from_tile and 
            move.to_tile == first_move.to_tile 
            for move in last_three
        )
    
    def _get_terminal_evaluation(self, board: Board, is_repetition_loss: bool = False, 
                                  losing_player: Color | None = None) -> float:
        """
        Get the evaluation for a terminal state.
        Returns +inf for white win, -inf for black win.
        If is_repetition_loss is True, returns loss evaluation for losing_player.
        """
        # Handle repetition loss (three same moves)
        if is_repetition_loss and losing_player is not None:
            if losing_player == Color.WHITE:
                return float("-inf")  # White loses
            else:
                return float("inf")   # Black loses
        
        # Handle normal victory conditions
        victory_state, _ = board.get_win_reason()
        if victory_state == Color.WHITE:
            return float("inf")
        elif victory_state == Color.BLACK:
            return float("-inf")
        else:
            # Should not happen, but fallback to heuristic
            return self.heuristic.evaluate(board)
    
    def _add_move(self, from_board: Board, move: Move):
        """
        Add a new board state to the graph after applying a move.
        Fixed: Properly handles terminal states with correct evaluation.
        Now also detects and penalizes three consecutive identical moves.
        """
        new_board = deepcopy(from_board)
        new_board.move(move)
        
        # Get move history from parent
        parent_history = self.graph.nodes[from_board].get("move_history", [])
        move_history = parent_history + [move]
        
        # Check for three consecutive identical moves
        is_repetition_loss = self._is_move_repeated_thrice(move_history)
        losing_player = None
        if is_repetition_loss:
            # The player who made the third repetition loses
            losing_player = from_board.current_player
        
        # Fixed: Check if this is a terminal state BEFORE evaluating
        is_terminal = self._is_terminal_state(new_board) or is_repetition_loss
        
        # Fixed: Use terminal evaluation for terminal states, heuristic otherwise
        if is_terminal:
            new_evaluation = self._get_terminal_evaluation(
                new_board, 
                is_repetition_loss=is_repetition_loss,
                losing_player=losing_player
            )
        else:
            new_evaluation = self.heuristic.evaluate(new_board)
        
        if self.vv:
            from_eval = self.graph.nodes[from_board]["evaluation"]
            repetition_msg = f", REPETITION LOSS for {losing_player}" if is_repetition_loss else ""
            print(f"Adding move {move} to board {new_board} "
                  f"(from {from_eval:.1f} to {new_evaluation:.1f}, "
                  f"terminal={is_terminal}{repetition_msg})")
        
        # Fixed: Verify move count
        if new_board.move_count != from_board.move_count + 1:
            raise ValueError(
                f"Move count incorrect: from {from_board.move_count} "
                f"to {new_board.move_count}"
            )
        
        # Fixed: Terminal states are marked as explored (no moves to explore)
        self.graph.add_node(
            new_board,
            evaluation=new_evaluation,
            best_child=None,
            parent=from_board,
            children=[],
            explored=is_terminal,
            move_history=move_history  # Store move history for repetition detection
        )
        self.graph.add_edge(from_board, new_board, move=move)
        self.graph.nodes[from_board]["children"].append(new_board)
    
    def _best_continuation(self, from_board: Board) -> tuple[Board | None, float]:
        """
        Find the best continuation from a board state using minimax.
        Fixed: Properly handles terminal states (nodes with no children).
        """
        if self.vv:
            print(f"Finding best continuation for {from_board}")
        
        maximizing = from_board.current_player == Color.WHITE
        children: list[Board] = self.graph.nodes[from_board]["children"]
        
        # Fixed: Handle terminal states properly
        if not children:
            # Terminal state - return its evaluation
            terminal_eval = self.graph.nodes[from_board]["evaluation"]
            if self.vv:
                print(f"Terminal state for {from_board} with evaluation {terminal_eval:.1f}")
            return None, terminal_eval
        
        # Find best child using minimax
        best_child = None
        best_eval = float("-inf") if maximizing else float("inf")
        
        for child in children:
            child_eval = self.graph.nodes[child]["evaluation"]
            if self.vv:
                print(f"Checking child {child} with evaluation {child_eval:.1f}")
            
            # Fixed: Proper minimax comparison
            if maximizing:
                if child_eval > best_eval:
                    best_eval = child_eval
                    best_child = child
            else:  # minimizing
                if child_eval < best_eval:
                    best_eval = child_eval
                    best_child = child
        
        if self.vv:
            print(f"Best continuation for {from_board} is {best_child} "
                  f"with evaluation {best_eval:.1f}")
        
        return best_child, best_eval
    
    def _update_evaluation(self, board: Board):
        """
        Update the evaluation of a board state based on its children.
        Fixed: Recursively updates parents, but handles None best_child.
        """
        if self.vv:
            print(f"Updating evaluation for board {board}")
        
        best_child, best_eval = self._best_continuation(board)
        self.graph.nodes[board]["best_child"] = best_child
        self.graph.nodes[board]["evaluation"] = best_eval
        
        # Fixed: Only update parent if it exists
        parent = self.graph.nodes[board]["parent"]
        if parent is not None:
            if self.vv:
                print(f"Parent of {board} is {parent}")
            self._update_evaluation(parent)
    
    def _next_node(self) -> Board | None:
        """
        Find the next unexplored node using level-by-level (BFS) exploration.
        Fixed: Handles empty levels and returns None when all nodes are explored.
        """
        # Fixed: Check current level for unexplored nodes
        for node in self.current_level:
            if not self.graph.nodes[node]["explored"]:
                return node
        
        # Build next level from all children of current level
        next_level: list[Board] = []
        seen = set()  # Fixed: Avoid duplicates
        
        for node in self.current_level:
            for child in self.graph.nodes[node]["children"]:
                if child not in seen:
                    next_level.append(child)
                    seen.add(child)
        
        # Fixed: Base case - if no next level, all nodes explored
        if not next_level:
            return None
        
        self.current_level = next_level
        return self._next_node()
    
    def _reset_level(self):
        """Reset the current level to start from current_position."""
        self.current_level = [self.current_position]
    
    def _explore_next_node(self) -> bool:
        """
        Explore the next node by generating all its children.
        Fixed: Returns False when no more nodes to explore, handles terminal states.
        """
        node = self._next_node()
        
        # Fixed: Handle case when all nodes are explored
        if node is None:
            return False
        
        if self.vv:
            print(f"Exploring next node {node} with evaluation "
                  f"{self.graph.nodes[node]['evaluation']:.1f}")
        
        # Fixed: Check if terminal before getting moves
        # Also check for repetition loss in move history
        move_history = self.graph.nodes[node].get("move_history", [])
        is_repetition_loss = self._is_move_repeated_thrice(move_history)
        
        if self._is_terminal_state(node) or is_repetition_loss:
            # Terminal state - no moves to explore, just mark as explored
            self.graph.nodes[node]["explored"] = True
            
            # Fixed: Ensure terminal evaluation is set correctly
            if not self.graph.nodes[node]["evaluation"] in (float("inf"), float("-inf")):
                losing_player = None
                if is_repetition_loss and move_history:
                    # The player who made the third repetition loses
                    # The move was made by the previous player (before current_player switched)
                    losing_player = node.current_player.opposite()
                self.graph.nodes[node]["evaluation"] = self._get_terminal_evaluation(
                    node, 
                    is_repetition_loss=is_repetition_loss,
                    losing_player=losing_player
                )
            self._update_evaluation(node)
            if self.vv:
                repetition_msg = f" (repetition loss)" if is_repetition_loss else ""
                print(f"Terminal node {node} marked as explored{repetition_msg}")
            return True
        
        # Generate all moves and add them as children
        available_moves = node.get_all_valid_moves(node.current_player)
        
        # Fixed: Handle case where node has no valid moves (should be terminal)
        if not available_moves:
            # This should have been caught by _is_terminal_state, but double-check
            self.graph.nodes[node]["explored"] = True
            self.graph.nodes[node]["evaluation"] = self._get_terminal_evaluation(node)
            self._update_evaluation(node)
            if self.vv:
                print(f"Node {node} has no moves, marking as terminal")
            return True
        
        for move in available_moves:
            self._add_move(node, move)
        
        # Mark node as explored after generating all children
        self.graph.nodes[node]["explored"] = True
        self._update_evaluation(node)
        
        if self.vv:
            print(f"Explored node {node} with evaluation "
                  f"{self.graph.nodes[node]['evaluation']:.1f}")
        
        return True
    
    def explore_graph(self, current_position: Board):
        """
        Explore the game graph starting from current_position.
        Fixed: Proper initialization, handles node existence, better error handling.
        """
        self.current_position = current_position
        
        # Fixed: Initialize node if it doesn't exist
        if not self.graph.has_node(current_position):
            initial_eval = self.heuristic.evaluate(current_position)
            self.graph.add_node(
                current_position,
                evaluation=initial_eval,  # Fixed: Use heuristic, not 0.0
                best_child=None,
                parent=None,
                children=[],
                explored=False
            )
        
        self.graph.nodes[self.current_position]["parent"] = None
        self._reset_level()
        
        if self.verbose:
            print(f"{self.name} is exploring the graph from current position "
                  f"{self.current_position}, current size: {len(self.graph.nodes)}")
        
        start_time = time.time()
        nodes_explored = 0
        start_positions = len(self.graph.nodes)
        
        while time.time() - start_time < self.max_thinking_time:
            # Fixed: Handle case when exploration is complete
            if not self._explore_next_node():
                if self.verbose:
                    print("\nAll nodes explored!")
                break
            
            nodes_explored += 1
            elapsed_time = time.time() - start_time
            
            # Fixed: Progress reporting with proper condition
            if self.verbose and (not self.vv or self.vvv):
                best_continuation, best_eval = self._best_continuation(self.current_position)
                
                # Fixed: Handle case where no continuation exists (shouldn't happen, but safer)
                if best_continuation is None:
                    # Terminal position - game is over
                    if self.vv:
                        print("\nCurrent position is terminal!")
                    continue
                
                best_move = self.graph.edges[self.current_position, best_continuation]["move"]
                nodes_per_second = nodes_explored / elapsed_time if elapsed_time > 0 else 0
                positions_per_second = (len(self.graph.nodes) - start_positions) / elapsed_time if elapsed_time > 0 else 0
                
                # Fixed: Safe access to current_level
                current_node_str = str(self.current_level[0]) if self.current_level else "N/A"
                
                print(f"\rExploring graph{pointpointpoint()} "
                      f"({nodes_per_second:.0f} nodes/s, {positions_per_second:.0f} positions/s, "
                      f"#{self.graph.size()}) - Current: {current_node_str} - "
                      f"Best move: {best_move} (eval: {best_eval:.1f}){pointpointpoint()}",
                      end="", flush=True)
        
        if self.verbose:
            print(f"\n{self.name} is done exploring the graph, new size: "
                  f"{len(self.graph.nodes)} (explored {nodes_explored} nodes)")
    
    @override
    def get_move(self, board: Board) -> Move:
        """
        Get the best move from the current board state.
        Fixed: Better error handling for edge cases.
        """
        self.explore_graph(current_position=board)
        best_continuation, best_eval = self._best_continuation(self.current_position)
        
        # Fixed: Handle terminal state or no continuation
        if best_continuation is None:
            # This should only happen if current_position is terminal
            # In that case, the game is over, but we need to return a move
            # Fallback: return first available move or raise error
            available_moves = board.get_all_valid_moves(board.current_player)
            if available_moves:
                move = available_moves[0]
                if self.verbose:
                    print(f"\nNo best continuation found, using fallback move {move}")
                return move
            else:
                raise ValueError(
                    "No moves available and no best continuation found! "
                    "Game may be in terminal state."
                )
        
        best_move: Move = self.graph.edges[self.current_position, best_continuation]["move"]
        if self.verbose:
            print(f"\nChose move {best_move} with evaluation {best_eval:.1f}")
        return best_move

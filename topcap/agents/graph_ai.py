from copy import deepcopy
from typing import override
import networkx as nx
import time
import matplotlib.pyplot as plt

from topcap.core.common import Player, Board, Color, Move
from topcap.utils.topcap_utils import WinReason, pointpointpoint
from .utils.heuristic import Heuristic

class GraphAI(Player):
    def __init__(self, heuristic: Heuristic, name: str = "Graph AI Lite", max_thinking_time: float = 5, verbose: bool = True, vv: bool = False, vvv: bool = False):
        super().__init__(name, verbose)
        self.heuristic: Heuristic = heuristic
        self.vv: bool = vv
        self.vvv: bool = vvv
        # TODO: use board codes
        self.graph: nx.Graph[Board] = nx.Graph()
        self.current_position: Board = Board()
        self.graph.add_node(self.current_position, evaluation = 0.0, best_child = None, parent = None, children = [], explored = False)
        self.max_thinking_time : float = max_thinking_time
        self.current_level: list[Board]

    def _add_move(self, from_board : Board, move : Move):
        new_board = deepcopy(from_board)
        new_board.move(move)
        from_evaluation: float = self.graph.nodes[from_board]["evaluation"]
        new_evaluation: float = self.heuristic.evaluate(new_board)
        evaluation_delta: float = (new_evaluation - from_evaluation) * from_board.current_player.value
        if self.vv:
            print(f"Adding move {move} to board {new_board} and evaluation delta {evaluation_delta:.1f} (from {from_evaluation:.1f} to {new_evaluation:.1f})")
        is_victory_move = new_board.get_win_reason()[1] != WinReason.NONE
        if new_board.move_count != from_board.move_count + 1:
            raise ValueError(f"Move count is not correct: from {from_board.move_count} to {new_board.move_count}")
        self.graph.add_node(new_board, evaluation=new_evaluation, best_child = None, parent=from_board, children = [], explored = is_victory_move)
        self.graph.add_edge(from_board, new_board, move=move)
        self.graph.nodes[from_board]["children"].append(new_board)

    def _update_evaluation(self, board: Board):
        if self.vv:
            print(f"Updating evaluation for board {board}")
        best_child, best_eval = self._best_continuation(board)
        self.graph.nodes[board]["best_child"] = best_child
        self.graph.nodes[board]["evaluation"] = best_eval
        if self.graph.nodes[board]["parent"] is not None:
            if self.vv:
                print(f"Parent of {board} is {self.graph.nodes[board]['parent']}")
            self._update_evaluation(self.graph.nodes[board]["parent"])

    def _best_continuation(self, from_board : Board) -> tuple[Board | None, float]:
        if self.vv:
            print(f"Finding best continuation for {from_board}")
        maximizing = from_board.current_player == Color.WHITE
        best_child = None
        best_eval = float("-inf") if maximizing else float("inf")
        children : list[Board] = self.graph.nodes[from_board]["children"]
        if not children: 
            if self.vv:
                print(f"Terminal state found for board: {from_board}")
            return None, self.graph.nodes[from_board]["evaluation"]
        for child in children:
            if self.vv:
                print(f"Checking child {child}")
            child_eval = self.graph.nodes[child]["evaluation"]
            if (maximizing and child_eval > best_eval) or (not maximizing and child_eval < best_eval) or best_child is None:
                best_eval = child_eval
                best_child = child
        if self.vv:
            print(f"Best continuation for {from_board} is {best_child} with evaluation {best_eval:.1f}")
        return best_child, best_eval
    
    def _next_node(self) -> Board:
        for node in self.current_level:
            if not self.graph.nodes[node]["explored"]:
                return node
        next_level: list[Board] = []
        for node in self.current_level:
            for child in self.graph.nodes[node]["children"]:
                next_level.append(child)
        self.current_level = next_level
        return self._next_node()

    def _reset_level(self):
        self.current_level = [self.current_position]
        self.next_level = []

    def _explore_next_node(self):
        node = self._next_node()
        if self.vv:
            print(f"Exploring next node {node} with evaluation {self.graph.nodes[node]['evaluation']:.1f}")
        available_moves = node.get_all_valid_moves(node.current_player)
        for move in available_moves:
            self._add_move(node, move)
        self.graph.nodes[node]["explored"] = True
        self._update_evaluation(node)
        if self.vv:
            print(f"Explored node {node} with evaluation {self.graph.nodes[node]['evaluation']:.1f}")

    def explore_graph(self, current_position : Board):
        self.current_position = current_position
        self._reset_level()
        if not self.graph.has_node(current_position):
            self.graph.add_node(current_position, evaluation = 0.0, best_child = None, parent = None, children = [], explored = False)
        self.graph.nodes[self.current_position]["parent"] = None
        if self.verbose:
            print(f"{self.name} is exploring the graph from current position {self.current_position}, current size: {len(self.graph.nodes)}")
        start_time = time.time()
        nodes_explored = 0
        start_positions_explored = len(self.graph.nodes)
        while time.time() - start_time < self.max_thinking_time:
            self._explore_next_node()
            nodes_explored += 1
            elapsed_time = time.time() - start_time
            nodes_per_second = nodes_explored / elapsed_time if elapsed_time > 0 else 0
            positions_per_second = (len(self.graph.nodes) - start_positions_explored )/ elapsed_time if elapsed_time > 0 else 0
            if self.verbose and not self.vv or self.vvv: # TODO: make vv and vvv
                best_continuation, best_eval = self._best_continuation(self.current_position)
                if not best_continuation:
                    raise ValueError("No best continuation found! Either choose random or make sure this cannot happen!")
                best_move = self.graph.edges[self.current_position, best_continuation]["move"]
                print(f"\rExploring graph{pointpointpoint()} ({nodes_per_second:.0f} nodes/s, {positions_per_second:.0f} positions/s, #{self.graph.size()}) - Current: {self.current_level[0]} - Current best move: {best_move} (evaluation: {best_eval:.1f}){pointpointpoint()}", end="", flush=True)
        if self.verbose:
            print(f"\n{self.name} is done exploring the graph, new size: {len(self.graph.nodes)} (explored {nodes_explored} nodes)")

    @override
    def get_move(self, board: Board) -> Move:
        self.explore_graph(current_position=board)
        best_continuation, best_eval = self._best_continuation(self.current_position)
        if not best_continuation:
            raise ValueError("No best continuation found! Either choose random or make sure this cannot happen!")
        best_move : Move = self.graph.edges[self.current_position, best_continuation]["move"]
        print(f"\nChose move {best_move} with evaluation {best_eval:.1f}")
        return best_move




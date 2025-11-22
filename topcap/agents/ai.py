from matplotlib import pyplot as plt
import networkx as nx

class BasicMinimaxAI(Player):
    def __init__(self, name="Minimax AI", max_thinking_time=5, depth=3, heuristic : Heuristic = None, verbose = False):
        super().__init__(name, max_thinking_time)
        self.max_depth = depth
        self.heuristic = heuristic
        self.verbose = verbose

    def minimax(self, last_move: Move, board: Board, remaining_depth: int, last_color: Color, maximizing: bool):
        depth = self.max_depth - remaining_depth
        current_time = int(time.time()) % 3
        if not self.verbose:
            print(f"\r{self.name} thinking{Utils.pointpointpoint()} depth = {depth}", end="", flush=True)
        current_color = last_color.opposite()
        if remaining_depth == 0 or board.get_victory_state()[0] != Color.NONE:
            if self.verbose:
                print(f"{'  ' * (depth)}Evaluated {last_color} move {last_move} at depth {depth} with {self.heuristic.evaluate(board):.1f}")
            return last_move, self.heuristic.evaluate(board)
        if self.verbose:
            print(f"{'  ' * (depth)}Evaluating {last_color} move {last_move} at depth {depth}")
        best_move = None
        best_eval = float("-inf") if maximizing else float("inf")
        for move in board.get_all_valid_moves(current_color):
            new_board = deepcopy(board)
            new_board.move(move)
            _, eval = self.minimax(move, new_board, remaining_depth - 1, current_color, not maximizing) 
            if (maximizing and eval > best_eval or not maximizing and eval < best_eval) or best_move is None:
                best_eval = eval
                best_move = move
        if self.verbose:
            print(f"{'  ' * (depth)}Minimax at depth {depth} evaluated {last_color} move {last_move} with evaluation {best_eval:.1f} for next {current_color} move {best_move}")
        return best_move, best_eval

    def get_move(self, board: Board):
        best_move, best_eval = self.minimax(None, board, self.max_depth, self.color.opposite(), self.color == Color.WHITE)
        print(f"\nChose move {best_move} with evaluation {best_eval:.1f}")
        return best_move, best_eval

class GraphAI(AI):
    def __init__(self, name="Graph AI", max_thinking_time=5, heuristic : Heuristic = None, verbose = False):
        super().__init__(name, max_thinking_time)
        self.heuristic = heuristic
        self.verbose = verbose
        self.graph = nx.Graph()
        self.current_position = Board()
        self.graph.add_node(self.current_position, evaluation = 0, parent = None, children = [], explored = False)

    def _add_move(self, from_board : Board, move : Move):
        new_board = deepcopy(from_board)
        new_board.move(move)
        from_evaluation = self.graph.nodes[from_board]["evaluation"]
        new_evaluation = self.heuristic.evaluate(new_board)
        evaluation_delta = new_evaluation - from_evaluation
        if from_board.current_player == Color.BLACK:
            evaluation_delta = -evaluation_delta
        if self.verbose:
            print(f"Adding move {move} to board {new_board} and evaluation delta {evaluation_delta:.1f} (from {from_evaluation:.1f} to {new_evaluation:.1f})")
        is_victory_move = new_board.get_victory_state()[0] != Color.NONE
        self.graph.add_node(new_board, evaluation=new_evaluation, parent=from_board, children = [], explored = is_victory_move)
        self.graph.add_edge(from_board, new_board, move=move)
        self.graph.nodes[from_board]["children"].append(new_board)

    def _explore_next_node(self):
        board = self._get_next_board()
        if self.verbose:
            print(f"Exploring next node {board} in graph with {len(self.graph.nodes)} nodes")
        available_moves = board.get_all_valid_moves(board.current_player)
        for move in available_moves:
            self._add_move(board, move)
        self.graph.nodes[board]["explored"] = True
        self._update_evaluation(board)

    def _get_next_board(self, board = None):
        if not self.graph.nodes[self.current_position]["explored"]:
            if self.verbose:
                print(f"Current position {self.current_position} not yet explored")
            return self.current_position
        if board is None:
            board = self.current_position
        if self.verbose:
            print(f"Getting next board from {board}")
        best_child = None
        maximizing = board.current_player == Color.WHITE
        best_eval = float("-inf") if maximizing else float("inf")
        for child in self.graph.nodes[board]["children"]:
            child_eval = self.graph.nodes[child]["evaluation"]
            if (maximizing and child_eval > best_eval) or (not maximizing and child_eval < best_eval) or best_child is None:
                best_eval = child_eval
                best_child = child
        if self.verbose:
            print(f"Best child is {best_child} with evaluation {best_eval:.1f}")
        if self.graph.nodes[best_child]["explored"]:
            if self.verbose:
                print(f"Best child {best_child} is explored, getting next board from it")
            return self._get_next_board(best_child)
        if self.verbose:
            print(f"Best child {best_child} is not explored, returning it")
        return best_child
        
    def _update_evaluation(self, board):
        old_eval = self.graph.nodes[board]["evaluation"]
        if self.verbose:
            print(f"Updating evaluation for board {board}")
        children = self.graph.nodes[board]["children"]
        if len(children) == 0:
            print(f"ERROR: THIS SHOULD NOT HAPPEN! eval = {self.heuristic.evaluate(board)}")
            self.graph.nodes[board]["evaluation"] = self.heuristic.evaluate(board)
            return
        if board.current_player == Color.WHITE:
            new_eval = max([self.graph.nodes[child]["evaluation"] for child in children])
        else:
            new_eval = min([self.graph.nodes[child]["evaluation"] for child in children])
        self.graph.nodes[board]["evaluation"] = new_eval
        if self.verbose:
            print(f"Updated evaluation for board {board} from {old_eval:.1f} to {new_eval:.1f}")
        if board != self.current_position:
            self._update_evaluation(self.graph.nodes[board]["parent"])
       
    def _plot_graph(self):
        pos = nx.kamada_kawai_layout(self.graph)
        labels = {node: f"{self.graph.nodes[node]['evaluation']:.1f}" for node in self.graph.nodes}
        explored_nodes = [node for node in self.graph.nodes if self.graph.nodes[node]["explored"]]
        non_explored_nodes = [node for node in self.graph.nodes if not self.graph.nodes[node]["explored"]]
        explored_colors = ['blue' if node.current_player == Color.WHITE else 'green' for node in explored_nodes]
        non_explored_colors = ['grey' for node in non_explored_nodes]
        explored_depths = [self._get_depth(node) for node in explored_nodes]
        explored_sizes = [1000 / (depth + 1) for depth in explored_depths]  # Adjust size based on depth
        non_explored_sizes = [100 for _ in non_explored_nodes]  # Small size for non-explored nodes

        # Draw nodes
        nx.draw(self.graph, pos, nodelist=explored_nodes, labels=labels, node_color=explored_colors, node_size=explored_sizes, with_labels=True, edge_color='gray')
        #nx.draw(self.graph, pos, nodelist=non_explored_nodes, labels=labels, node_color=non_explored_colors, node_size=non_explored_sizes, with_labels=True, font_weight='bold', edge_color='gray')

        # Draw edges and highlight best moves
        for node in explored_nodes:
            children = self.graph.nodes[node]["children"]
            if children:
                best_child = max(children, key=lambda child: self.graph.nodes[child]["evaluation"]) if node.current_player == Color.WHITE else min(children, key=lambda child: self.graph.nodes[child]["evaluation"])
                best_move = self.graph.edges[node, best_child]["move"]
                nx.draw_networkx_edges(self.graph, pos, edgelist=[(node, best_child)], edge_color='red', width=5.0)
                #nx.draw_networkx_edge_labels(self.graph, pos, edge_labels={(node, best_child): str(best_move)})

        plt.show()

    def _get_depth(self, node):
        depth = 0
        while self.graph.nodes[node]["parent"] is not None:
            node = self.graph.nodes[node]["parent"]
            depth += 1
        return depth

    def explore_graph(self):
        print(f"{self.name} is exploring the graph, current size: {len(self.graph.nodes)}")
        start_time = time.time()
        nodes_explored = 0
        while time.time() - start_time < self.max_thinking_time:
            self._explore_next_node()
            nodes_explored += 1
            elapsed_time = time.time() - start_time
            nodes_per_second = nodes_explored / elapsed_time if elapsed_time > 0 else 0
            if not self.verbose:
                best_move, best_eval = self.current_best_move()
                print(f"\rExploring graph{Utils.pointpointpoint()} ({nodes_per_second:.0f} nodes/s) - Current best move: {best_move} (evaluation: {best_eval:.1f}){Utils.pointpointpoint()}", end="", flush=True)
        print(f"\n{self.name} is done exploring the graph, new size: {len(self.graph.nodes)} (explored {nodes_explored} nodes)")

    def current_best_move(self):
        best_child = None
        best_eval = float("-inf")
        for child in self.graph.nodes[self.current_position]["children"]:
            child_eval = self.graph.nodes[child]["evaluation"]
            if child_eval > best_eval or best_child is None:
                best_eval = child_eval
                best_child = child
        return self.graph.edges[self.current_position, best_child]["move"], best_eval

    def get_move(self, board: Board):
        self.current_position = board
        self.explore_graph()
        #self._plot_graph()
        best_move, best_eval = self.current_best_move()
        print(f"\nChose move {best_move} with evaluation {best_eval:.1f}")
        return best_move, best_eval

class GraphAILite(AI):
    def __init__(self, name="Graph AI Lite", max_thinking_time=5, heuristic : Heuristic = None, verbose = False, vv=False):
        super().__init__(name, max_thinking_time)
        self.heuristic = heuristic
        self.v = verbose
        self.vv = vv
        self.graph = nx.Graph()
        self.current_position = Board()
        self.graph.add_node(self.current_position, evaluation = 0, best_child = None, parent = None, children = [], explored = False)

    def _add_move(self, from_board : Board, move : Move):
        new_board = deepcopy(from_board)
        new_board.move(move)
        from_evaluation = self.graph.nodes[from_board]["evaluation"]
        new_evaluation = self.heuristic.evaluate(new_board)
        evaluation_delta = new_evaluation - from_evaluation
        if from_board.current_player == Color.BLACK:
            evaluation_delta = -evaluation_delta
        if self.vv:
            print(f"Adding move {move} to board {new_board} and evaluation delta {evaluation_delta:.1f} (from {from_evaluation:.1f} to {new_evaluation:.1f})")
        is_victory_move = new_board.get_victory_state()[0] != Color.NONE
        if new_board.move_count != from_board.move_count + 1:
            print(f"ERROR: Move count is not correct: from {from_board.move_count} to {new_board.move_count}")
        self.graph.add_node(new_board, evaluation=new_evaluation, best_child = None, parent=from_board, children = [], explored = is_victory_move)
        self.graph.add_edge(from_board, new_board, move=move)
        self.graph.nodes[from_board]["children"].append(new_board)

    def _update_evaluation(self, board):
        if self.vv:
            print(f"Updating evaluation for board {board}")
        best_child, best_eval = self._best_continuation(board)
        self.graph.nodes[board]["best_child"] = best_child
        self.graph.nodes[board]["evaluation"] = best_eval
        if self.graph.nodes[board]["parent"] is not None:
            if self.vv:
                print(f"Parent of {board} is {self.graph.nodes[board]['parent']}")
            self._update_evaluation(self.graph.nodes[board]["parent"])

    def _best_continuation(self, from_board : Board) -> Tuple[Board, float]:
        if self.vv:
            print(f"Finding best continuation for {from_board}")
        maximizing = from_board.current_player == Color.WHITE
        best_child = None
        best_eval = float("-inf") if maximizing else float("inf")
        for child in self.graph.nodes[from_board]["children"]:
            if self.vv:
                print(f"Checking child {child}")
            child_eval = self.graph.nodes[child]["evaluation"]
            if (maximizing and child_eval > best_eval) or (not maximizing and child_eval < best_eval) or best_child is None:
                best_eval = child_eval
                best_child = child
        if self.vv:
            print(f"Best continuation for {from_board} is {best_child} with evaluation {best_eval:.1f}")
        return best_child, best_eval
    
    def _next_node(self, current_board):
        if not self.graph.nodes[current_board]["explored"]:
            return current_board
        best_child = self.graph.nodes[current_board]["best_child"]
        if self.graph.nodes[best_child]["explored"]:
            return self._next_node(best_child)
        return best_child

    def _explore_next_node(self):
        node = self._next_node(self.current_position)
        if self.v:
            print(f"Exploring next node {node} with evaluation {self.graph.nodes[node]['evaluation']:.1f}")
        available_moves = node.get_all_valid_moves(node.current_player)
        for move in available_moves:
            self._add_move(node, move)
        self.graph.nodes[node]["explored"] = True
        self._update_evaluation(node)
        if self.v:
            print(f"Explored node {node} with evaluation {self.graph.nodes[node]['evaluation']:.1f}")
       
    def _plot_graph(self):
        pos = nx.kamada_kawai_layout(self.graph)
        labels = {node: f"{self.graph.nodes[node]['evaluation']:.1f}" for node in self.graph.nodes}
        explored_nodes = [node for node in self.graph.nodes if self.graph.nodes[node]["explored"]]
        non_explored_nodes = [node for node in self.graph.nodes if not self.graph.nodes[node]["explored"]]
        explored_colors = ['blue' if node.current_player == Color.WHITE else 'green' for node in explored_nodes]
        non_explored_colors = ['grey' for node in non_explored_nodes]
        explored_depths = [self._get_depth(node) for node in explored_nodes]
        explored_sizes = [1000 / (depth + 1) for depth in explored_depths]  # Adjust size based on depth
        non_explored_sizes = [100 for _ in non_explored_nodes]  # Small size for non-explored nodes

        # Draw nodes
        nx.draw(self.graph, pos, nodelist=explored_nodes, labels=labels, node_color=explored_colors, node_size=explored_sizes, with_labels=True, edge_color='gray')

        # Draw edges and highlight best moves
        for node in explored_nodes:
            best_child = self.graph.nodes[node]["best_child"]
            if best_child:
                best_move = self.graph.edges[node, best_child]["move"]
                nx.draw_networkx_edges(self.graph, pos, edgelist=[(node, best_child)], edge_color='red', width=5.0)

        plt.show()

    def explore_graph(self, current_position : Board):
        self.current_position = current_position
        self.graph.nodes[self.current_position]["parent"] = None
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
            if not self.v:
                best_continuation, best_eval = self._best_continuation(self.current_position)
                best_move = self.graph.edges[self.current_position, best_continuation]["move"]
                print(f"\rExploring graph{Utils.pointpointpoint()} ({nodes_per_second:.0f} nodes/s, {positions_per_second:.0f} positions/s) - Current best move: {best_move} (evaluation: {best_eval:.1f}){Utils.pointpointpoint()}", end="", flush=True)
        print(f"\n{self.name} is done exploring the graph, new size: {len(self.graph.nodes)} (explored {nodes_explored} nodes)")

    def get_move(self, board: Board):
        self.explore_graph(current_position=board)
        #self._plot_graph()
        best_continuation, best_eval = self._best_continuation(self.current_position)
        best_move = self.graph.edges[self.current_position, best_continuation]["move"]
        print(f"\nChose move {best_move} with evaluation {best_eval:.1f}")
        return best_move, best_eval




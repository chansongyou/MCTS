import random
from copy import deepcopy
from math import sqrt, log

from mcts.tictactoe import TicTacToeBoard, Player


class Node:
    def __init__(self, state: TicTacToeBoard, parent=None):
        self.state: TicTacToeBoard = state
        self.parent: Node = parent
        self.children: list[Node] = []
        self.visits: int = 0
        self.wins: int = 0  # +1 for win, 0 for draw, -1 for loss
        self.visited_moves = set()

    def add_child(self, child, move):
        self.children.append(child)
        self.visited_moves.add(move)

    @property
    def depth(self) -> int:
        if self.parent is None:
            return 0
        return self.parent.depth + 1


class Tree:
    def __init__(self, player: Player, max_iterations: int = 1000):
        self.max_iterations = max_iterations
        self.player = player

    def search(self, state: TicTacToeBoard) -> int:
        root = Node(state)
        for i in range(self.max_iterations):
            node = self.tree_policy(root)
            result = self.default_policy(node)
            self.backpropagate(node, result)

        return _move_from_state_change(state, self.best_child(root).state)

    def tree_policy(self, node: Node) -> Node:
        while not node.state.is_terminal:
            if len(node.children) < len(node.state.get_possible_moves()):
                return self.expand(node)
            else:
                node = self.best_child(node)
        return node

    def expand(self, node: Node) -> Node:
        possible_moves = [i for i in node.state.get_possible_moves() if i not in node.visited_moves]
        chosen_move = random.choice(possible_moves)

        new_state = deepcopy(node.state)
        new_state.make_move(chosen_move, new_state.current_player)
        new_node = Node(new_state, node)
        node.add_child(new_node, chosen_move)

        return new_node

    def best_child(self, parent: Node) -> Node:
        exploration_constant = sqrt(2)

        def uct(node: Node) -> float:
            return node.wins / node.visits + exploration_constant * sqrt(
                log(node.parent.visits) / node.visits
            )

        return max(parent.children, key=uct)

    def default_policy(self, node: Node) -> int:
        simulation_state = deepcopy(node.state)
        while not simulation_state.is_terminal:
            simulation_state.make_random_move()

        if simulation_state.winner == self.player:
            return 1
        elif simulation_state.winner == self.player.other():
            return -1

        return 0

    def backpropagate(self, node: Node, result: int):
        while node is not None:
            node.visits += 1
            node.wins += result
            node = node.parent


def _move_from_state_change(old_state: TicTacToeBoard, new_state: TicTacToeBoard):
    for i, (a, b) in enumerate(zip(old_state.grid, new_state.grid)):
        if a != b:
            return i

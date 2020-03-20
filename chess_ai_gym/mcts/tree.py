from typing import TYPE_CHECKING

from .leaf import Leaf

if TYPE_CHECKING:
    from chess_ai_gym.helpers.enums import SideType

__all__ = [
    "Tree"
]

STARTING_BOARD_POSITION = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
GENERATE_NODES_DIVIDER = 2


class Tree:
    def __init__(self, seed: int, starting_side: 'SideType'):
        self.seed = seed
        self.starting_side = starting_side

        #############
        # Root init #
        #############
        self.root: 'Leaf' = Leaf(board_position=STARTING_BOARD_POSITION, starting_side=starting_side,
                                 current_side=starting_side, parent_leaf=None)
        self.root.id = 0
        self.root.change_random_seed(seed=self.seed)
        self.root.compute_legal_moves()
        self.root.populate_nodes(generate_nodes_divider=1)
        for node in self.root.nodes:
            node.run_simulation()

    def start_search(self) -> None:

        def recursive_path_finder(node: 'Leaf') -> 'Leaf':
            """Fetch a leaf node by recursion."""
            if node.nodes:
                best_node_number = node.choose_the_best_node()
                return recursive_path_finder(node=node.nodes[best_node_number])

            else:
                return node

        while True:
            #############
            # SELECTING #
            #############
            leaf_node = recursive_path_finder(node=self.root)

            #############
            # EXPANDING #
            #############
            leaf_node.compute_legal_moves()
            leaf_node.populate_nodes(generate_nodes_divider=GENERATE_NODES_DIVIDER)

            ########################
            # SIMULATING/EXPLORING #
            ########################
            for node in leaf_node.nodes:
                node.run_simulation()



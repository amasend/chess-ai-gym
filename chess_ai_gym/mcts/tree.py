from typing import TYPE_CHECKING
from time import sleep

from .leaf import Leaf

from IPython.display import clear_output
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout


if TYPE_CHECKING:
    from chess_ai_gym.helpers.enums import SideType

__all__ = [
    "Tree"
]

STARTING_BOARD_POSITION = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
GENERATE_NODES_DIVIDER = 1


class Tree:
    def __init__(self, seed: int, starting_side: 'SideType', visualize: 'bool' = False):
        self.visualize = visualize
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
        self.root.populate_nodes(generate_nodes_divider=GENERATE_NODES_DIVIDER)
        for node in self.root.nodes:
            node.run_simulation()

        if self.visualize:
            self.graph = nx.DiGraph()
            self.graph.add_node(self.root.id, data=self.root.graphical_leaf)
            self._add_nodes_to_graph(node=self.root)

    def _add_nodes_to_graph(self, node: 'Leaf') -> None:
        """
        Add a graphical representation of that node to a networkx graph.

        Parameters
        ----------
        node: Leaf, required
            A node what you want to add to a graphical representation.
        """
        for leaf in node.nodes:
            self.graph.add_node(leaf.id, data=leaf.graphical_leaf)
            self.graph.add_edge(node.id, leaf.id)

    def _show_graph(self) -> None:
        """Draw a full tree representation at a given time."""
        labels = nx.get_node_attributes(self.graph, 'data')
        pos = graphviz_layout(self.graph, prog='dot')
        clear_output(wait=True)
        plt.figure(figsize=(30, 30))
        nx.draw(self.graph, pos, with_labels=True, arrows=True, labels=labels, node_size=1000)
        plt.show()

    def start_search(self) -> None:
        """Start a MCTS process."""

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

            # note: populating a graph
            if self.visualize:
                self._add_nodes_to_graph(node=leaf_node)
                self._show_graph()

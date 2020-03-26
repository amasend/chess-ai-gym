import pickle
import time
from typing import TYPE_CHECKING, List

from .leaf import Leaf

from graph_tool.all import Graph, graph_draw, radial_tree_layout

if TYPE_CHECKING:
    from chess_ai_gym.helpers.enums import SideType

__all__ = [
    "Tree"
]

STARTING_BOARD_POSITION = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
GENERATE_NODES_DIVIDER = 1


class Tree:
    def __init__(self, starting_side: 'SideType', seed: int = None):
        self.seed = seed
        self.starting_side = starting_side

        #############
        # Root init #
        #############
        self.root: 'Leaf' = Leaf(board_position=STARTING_BOARD_POSITION, starting_side=starting_side,
                                 current_side=starting_side, parent_leaf=None)
        self.root.id = 0
        if self.seed is not None:
            self.root.change_random_seed(seed=self.seed)

    def visualize(self):
        def explore_tree(nodes: 'List[Leaf]', parent) -> None:
            vertexes = []
            for node in nodes:
                vertexes.append(graph.add_vertex())
                graph.add_edge(parent, vertexes[-1])

            for node, vertex in zip(nodes, vertexes):
                explore_tree(node.nodes, vertex)

        graph = Graph()
        parent_vertex = graph.add_vertex()
        explore_tree(nodes=self.root.nodes, parent=parent_vertex)
        pos = radial_tree_layout(graph, parent_vertex)
        graph_draw(graph, pos=pos, output="graph.pdf")

    def save(self) -> None:
        """Try to save this tree as a pickle file."""
        pickle.dump(self, open("mcts_tree.pickle", "wb"))
        print(f"Tree saved after {self.root.iteration} iterations.")

    def start_search(self) -> None:
        """Start a MCTS process."""

        def recursive_path_finder(node: 'Leaf') -> 'Leaf':
            """Fetch a leaf node by recursion."""
            if node.nodes:
                best_node_number = node.choose_the_best_node()
                return recursive_path_finder(node=node.nodes[best_node_number])

            else:
                return node

        start_time = time.time()
        while True:
            #############
            # SELECTING #
            #############
            leaf_node = recursive_path_finder(node=self.root)

            if leaf_node.iteration == 0:
                # note: perform a simulation when we are on a leaf node but not simulated yet
                leaf_node.run_simulation()

            else:
                #############
                # EXPANDING #
                #############
                # note: add available actions to the tree
                leaf_node.compute_legal_moves()
                leaf_node.populate_nodes(generate_nodes_divider=GENERATE_NODES_DIVIDER)
                # --- end note

                # note: populating a graph to draw
                # self._add_nodes_to_graph(node=leaf_node)

                ########################
                # SIMULATING/EXPLORING #
                ########################
                # note: take first child node and perform a simulation
                node_to_simulate = leaf_node.nodes[0]
                node_to_simulate.run_simulation()
                # --- end note

            if time.time() - start_time > 6:
                self.save()
                start_time = time.time()

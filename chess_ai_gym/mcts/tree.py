import pickle
import time
from typing import TYPE_CHECKING

from .leaf import Leaf

from IPython.display import clear_output
from graph_tool.all import Graph, graph_draw, radial_tree_layout, sfdp_layout, fruchterman_reingold_layout, arf_layout

if TYPE_CHECKING:
    from graph_tool import VertexPropertyMap
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
        def explore_tree(node: 'Leaf', graph: 'Graph', vprop: 'VertexPropertyMap') -> None:
            vertex = graph.add_vertex()
            vprop[vertex] = f"{node.iteration}/{node.score}"
            for leaf in node.nodes:
                leaf_vertex = graph.add_vertex()
                vprop[vertex] = f"{leaf.iteration}/{leaf.score}"
                graph.add_edge(vertex, leaf_vertex)
                explore_tree(node=leaf, graph=graph, vprop=vprop)

        g = Graph()
        vprop = g.new_vertex_property('string')
        explore_tree(node=self.root, graph=g, vprop=vprop)
        graph_draw(g, vertex_text=vprop)


    # def _show_graph(self) -> None:
    #     """Draw a full tree representation at a given time."""
    #     clear_output(wait=True)
    #     pos = radial_tree_layout(self.graph, self.root.vertex, node_weight=self.vprop)
    #     # pos = sfdp_layout(self.graph)
    #     # pos = fruchterman_reingold_layout(self.graph)
    #     # pos = arf_layout(self.graph)
    #     graph_draw(self.graph, pos=pos, vertex_text=self.vprop)
    #     time.sleep(3)

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

            if time.time() - start_time > 60:
                self.save()
                start_time = time.time()

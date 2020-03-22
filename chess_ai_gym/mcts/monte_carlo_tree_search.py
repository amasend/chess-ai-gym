import os

from .tree import Tree
from chess_ai_gym.helpers.enums import SideType

__all__ = [
    "MCTS"
]


class MCTS:
    """"""

    def __init__(self,
                 starting_side: 'SideType',
                 seed: int = None,
                 cpu_count: int = None,
                 time_per_tree: int = None,
                 overall_time: int = None,
                 depth: int = None) -> None:
        ###############
        # Performance #
        ###############
        self.cpu_count = cpu_count if cpu_count else os.cpu_count()
        self.time_per_tree = time_per_tree
        self.overall_time = overall_time
        self.depth = depth

        ########
        # Core #
        ########
        self.starting_side = starting_side
        self.tree: 'Tree' = Tree(seed=seed, starting_side=starting_side)

    def load_tree(self, file_path: str) -> None:
        import pickle
        self.tree: 'Tree' = pickle.load(open(file_path, "rb"))
        print(f"Tree object loaded, saved iterations: {self.tree.root.iteration}")

    def run(self) -> None:
        self.tree.start_search()

from .leaf import Leaf
from .tree import Tree
from chess_ai_gym.helpers.enums import SideType

__all__ = [
    "MCTS"
]


class MCTS:
    """"""
    def __init__(self,
                 seed: int,
                 starting_side: 'SideType',
                 cpu_count: int = None,
                 time_per_leaf: int = None,
                 overall_time: int = None,
                 depth: int = None) -> None:

        ###############
        # Performance #
        ###############
        self.cpu_count = cpu_count
        self.time_per_leaf = time_per_leaf
        self.overall_time = overall_time
        self.depth = depth

        ########
        # Core #
        ########
        self.starting_side = starting_side
        self.tree: 'Tree' = Tree(seed=seed, starting_side=starting_side)

    def run(self) -> None:
        self.tree.start_search()

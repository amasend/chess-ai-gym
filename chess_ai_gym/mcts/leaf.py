import random
from uuid import uuid4
from typing import TYPE_CHECKING, Union

from chess_ai_gym.environments.pytchon_chess import Board
from chess_ai_gym.utils.errors import NoMoreMoves
from chess_ai_gym.helpers.enums import SideType

if TYPE_CHECKING:
    from uuid import UUID

__all__ = [
    "Leaf"
]


class Leaf:
    """"""
    def __init__(self,
                 board_position: str,
                 starting_side: 'SideType',
                 current_side: 'SideType',
                 parent_leaf: Union['Leaf', None]):

        self.parent_leaf = parent_leaf
        self.id = uuid4()
        self.current_side = current_side
        self.starting_side = starting_side

        self.iteration = 0
        self.wins = 0
        self.score = 0

        self.board = Board(starting_position=board_position)
        self.board.turn = current_side.value
        self.legal_moves = None
        self.number_of_legal_moves = None
        self.nodes = []

    @staticmethod
    def change_random_seed(seed: int) -> None:
        """Changing random seed."""
        random.seed(seed)

    def compute_legal_moves(self) -> None:
        """Set legal moves in the current position and count them."""
        self.legal_moves = [move for move in self.board.legal_moves]
        self.number_of_legal_moves = self.board.legal_moves.count()

    def increase_iteration_and_wins(self, win: bool) -> None:
        self.iteration += 1
        if win:
            self.wins += 1

        if self.parent_leaf:
            self.parent_leaf.increase_iteration_and_wins(win=win)

    def populate_nodes(self, generate_nodes_divider: int) -> None:
        """
        Create new leafs based on a current board position.
        Do it randomly (only a number of positions from available space.)

        Parameters
        ----------
        generate_nodes_divider: int, required
            The divider number of number_of_legal_moves to random.sample() method.
        """
        if self.number_of_legal_moves > 1:
            number_of_nodes = self.number_of_legal_moves // generate_nodes_divider

        elif self.number_of_legal_moves == 1:
            number_of_nodes = 1

        else:
            raise NoMoreMoves(leaf_id=self.id)

        # note: random part!
        leafs_and_moves = [(
            Leaf(board_position=self.board.fen(),
                 starting_side=self.starting_side,
                 current_side=SideType.WHITE if self.current_side == SideType.BLACK else SideType.BLACK,
                 parent_leaf=self,
                 ),
            move) for move in random.sample(self.legal_moves, k=number_of_nodes)
        ]
        # --- end note

        # note: pushes new positions, computes next legal moves and stores as new nodes/leafs
        for leaf, move in leafs_and_moves:
            leaf.board.push(move)
            leaf.compute_legal_moves()
            self.nodes.append(leaf)
        # --- end note

    def run_simulation(self):
        if not self.board.is_game_over():
            board = Board(starting_position=self.board.fen())
            board.turn = self.current_side.value

            while not self.board.is_game_over():
                moves = board.legal_moves

                # note: this condition could be removed
                if moves:
                    move = random.choice(moves)
                    board.push(move)

            result = board.result()     # TODO: check the sides
            if ((result == '1-0' and self.starting_side == SideType.WHITE) or
                    (result == '0-1' and self.starting_side == SideType.BLACK)):
                self.increase_iteration_and_wins(win=True)

            else:
                self.increase_iteration_and_wins(win=False)


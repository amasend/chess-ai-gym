import unittest
import random
import sys

from chess_ai_gym.mcts.leaf import Leaf
from chess_ai_gym.helpers.enums import SideType
from uuid import UUID
from chess_ai_gym.environments.pytchon_chess import Board
from chess import Move


class TestLeaf(unittest.TestCase):
    leaf: 'Leaf' = None
    board_position = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    starting_side = SideType.WHITE
    current_side = SideType.WHITE

    def test_01__init__pass_initialization_params_without_parent_leaf__all_params_set(self):
        TestLeaf.leaf = Leaf(board_position=self.board_position,
                             starting_side=self.starting_side,
                             current_side=self.current_side,
                             parent_leaf=None)

        self.assertIsNone(self.leaf.parent_leaf, msg="parent_leaf is not None")
        self.assertIsNone(self.leaf.legal_moves, msg="legal_moves is not None")
        self.assertIsNone(self.leaf.number_of_legal_moves, msg="number_of_legal_moves is not None")

        self.assertEqual(self.leaf.starting_side, self.starting_side, msg="starting_side is wrong")
        self.assertEqual(self.leaf.starting_side, self.starting_side, msg="starting_side is wrong")
        self.assertEqual(self.leaf.current_side, self.current_side, msg="current_side is is wrong")
        self.assertEqual(self.leaf.nodes, [], msg="nodes is wrong")

        self.assertIsInstance(self.leaf.id, UUID, msg="is not of type UUID")

        self.assertEqual(self.leaf.iteration, 0, msg="wrong iteration value")
        self.assertEqual(self.leaf.wins, 0, msg="wrong wins value")
        self.assertEqual(self.leaf.score, 0, msg="wrong score value")

        self.assertIsInstance(self.leaf.board, Board, msg="board not of type Board")
        self.assertEqual(self.leaf.board, Board(starting_position=self.board_position), msg="board is different")
        self.assertEqual(self.leaf.board.fen(), self.board_position, msg="wrong board position")
        self.assertEqual(self.leaf.board.turn, self.current_side.value, msg="wrong turn in board")

    def test_02__change_random_seed__set_initial_seed__values_are_the_same_after_probing(self):
        self.leaf.change_random_seed(1)
        x = random.randrange(sys.maxsize)
        self.leaf.change_random_seed(1)
        y = random.randrange(sys.maxsize)

        self.assertEqual(x, y, msg="Setting seed is not working.")

    def test_03__compute_legal_moves__moves_are_the_same(self):
        self.leaf.compute_legal_moves()

        self.assertEqual(self.leaf.legal_moves,
                         [move for move in Board(starting_position=self.board_position).legal_moves],
                         msg="legal moves are wrong")
        self.assertEqual(self.leaf.number_of_legal_moves,
                         Board(starting_position=self.board_position).legal_moves.count(),
                         msg="number of legal moves is incorrect")

    def test_04__populate_nodes__all_nodes_populated(self):
        self.leaf.populate_nodes(generate_nodes_divider=1)
        nodes = []

        leafs_and_moves = [(
            Leaf(board_position=self.board_position,
                 starting_side=self.starting_side,
                 current_side=self.current_side,
                 parent_leaf=self.leaf,
                 ),
            move) for move in self.leaf.legal_moves
        ]

        for leaf, move in leafs_and_moves:
            leaf.push_move(move)
            leaf.compute_legal_moves()
            nodes.append(leaf)

        self.leaf.nodes.sort(key=lambda x: x.board.fen())
        nodes.sort(key=lambda x: x.board.fen())

        for node_test, node in zip(self.leaf.nodes, nodes):
            self.assertEqual(node_test.board.fen(), node.board.fen(), msg="different position")
            self.assertEqual(node_test.board.turn, node.board.turn, msg="different side")

    def test_05__push_move__make_a_move__board_changed(self):
        leaf = Leaf(board_position=self.board_position,
                    starting_side=self.starting_side,
                    current_side=self.current_side,
                    parent_leaf=None)
        board = Board(starting_position=self.board_position)

        leaf.push_move(Move(1, 18))
        board.push(Move(1, 18))

        self.assertEqual(leaf.board, board, msg="boards are different")
        self.assertEqual(leaf.current_side, SideType.WHITE if self.current_side == SideType.BLACK else SideType.BLACK,
                         msg="Wrong current side")


if __name__ == '__main__':
    unittest.main()

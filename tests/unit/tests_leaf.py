import unittest
import random
import sys

from chess_ai_gym.mcts.leaf import Leaf
from chess_ai_gym.utils.errors import NodesNotPopulated
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

    def test_06__increase_iteration_and_wins(self):
        self.leaf.nodes[0].increase_iteration_and_wins(win=1)

        self.assertEqual(self.leaf.iteration, 1, msg="Parent iteration is wrong.")
        self.assertEqual(self.leaf.wins, 1, msg="Parent wins counter is wrong.")
        self.assertEqual(self.leaf.nodes[0].iteration, 1, msg="child node iteration is wrong")
        self.assertEqual(self.leaf.nodes[0].wins, 1, msg="child node win counter is wrong")

        self.leaf.nodes[1].increase_iteration_and_wins(win=1)

        self.assertEqual(self.leaf.iteration, 2, msg="Parent iteration is wrong.")
        self.assertEqual(self.leaf.wins, 2, msg="Parent wins counter is wrong.")
        self.assertEqual(self.leaf.nodes[1].iteration, 1, msg="child node iteration is wrong")
        self.assertEqual(self.leaf.nodes[1].wins, 1, msg="child node win counter is wrong")

        self.leaf.nodes[2].increase_iteration_and_wins(win=-1)

        self.assertEqual(self.leaf.iteration, 3, msg="Parent iteration is wrong.")
        self.assertEqual(self.leaf.wins, 1, msg="Parent wins counter is wrong.")
        self.assertEqual(self.leaf.nodes[2].iteration, 1, msg="child node iteration is wrong")
        self.assertEqual(self.leaf.nodes[2].wins, -1, msg="child node win counter is wrong")

    def test_07__run_simulation__simulation_completed_game_is_over(self):
        self.leaf.nodes[3].run_simulation()
        win = self.leaf.nodes[3].wins

        if win == 1:
            self.assertEqual(self.leaf.wins, 2, msg="Parent leaf wins counted is incorrect.")

        elif win == 0.5:
            self.assertEqual(self.leaf.wins, 1.5, msg="Parent leaf wins counted is incorrect.")

        else:
            self.assertEqual(self.leaf.wins, 0, msg="Parent leaf wins counted is incorrect.")

        self.assertEqual(self.leaf.iteration, 4, msg="Parent leaf iteration is incorrect.")
        self.assertEqual(self.leaf.nodes[3].iteration, 1, msg="child node iteration is wrong")

    def test_08__compare_leafs(self):
        self.assertTrue(self.leaf == self.leaf, msg="These two leafs should be identical.")
        self.assertFalse(self.leaf == self.leaf.nodes[0], msg="These leafs should be different.")

        def try_raise(self):
            return self.leaf == 1

        with self.assertRaises(NotImplementedError, msg="We should not be able to compare leaf with other types."):
            try_raise(self)

    def test_09__compute_score(self):
        leaf = Leaf(board_position=self.board_position,
                    starting_side=self.starting_side,
                    current_side=self.current_side,
                    parent_leaf=None)
        leaf.compute_legal_moves()
        leaf.populate_nodes(1)
        leaf.iteration = 2
        leaf.wins = 2
        leaf.nodes[0].iteration = 1
        leaf.nodes[0].wins = 1

        leaf.nodes[0].compute_score()

        self.assertEqual(2.177410022515475, leaf.nodes[0].score, msg="Child leaf score wrongly computed.")

    def test_10__choose_the_best_node(self):
        leaf = Leaf(board_position=self.board_position,
                    starting_side=self.starting_side,
                    current_side=self.current_side,
                    parent_leaf=None)
        leaf.compute_legal_moves()
        leaf.populate_nodes(1)
        leaf.iteration = 3
        leaf.wins = 1
        leaf.nodes[0].iteration = 1
        leaf.nodes[0].wins = 1
        leaf.nodes[1].iteration = 1
        leaf.nodes[1].wins = 1
        leaf.nodes[2].iteration = 1
        leaf.nodes[2].wins = -1

        leaf.nodes[0].compute_score()
        leaf.nodes[1].compute_score()
        leaf.nodes[2].compute_score()

        # note: earlier we used change_random_seed(), so this always be deterministic now
        best_node_number = leaf.choose_the_best_node()
        self.assertTrue(best_node_number == 0 or best_node_number == 1,
                        msg="Wrong best node number, should be one of [0, 1]")

        leaf.nodes[0].wins = -1
        leaf.nodes[0].compute_score()

        best_node_number = leaf.choose_the_best_node()
        self.assertTrue(best_node_number == 1, msg="Wrong best node number, should be 1")

    def test_11__choose_the_best_node__leaf_nodes_not_populated(self):
        leaf = Leaf(board_position=self.board_position,
                    starting_side=self.starting_side,
                    current_side=self.current_side,
                    parent_leaf=None)

        with self.assertRaises(NodesNotPopulated):
            leaf.choose_the_best_node()


if __name__ == '__main__':
    unittest.main()

from src.test.interpret import interpret_game
from src.game.game_exception import *
import unittest


class TestMovements(unittest.TestCase):

    def test_game_1(self):
        # Asserts that no exception has been raised
        interpret_game('../../resources/game_1.json')

    def test_game_move_opponents_pieces(self):
        # Cannot move opponents pieces
        self.assertRaises(MoveOpponentPieceException, interpret_game, '../../resources/game_move_opponent.json')

    def test_illegal_move_direction(self):
        # Moves into a L shape
        self.assertRaises(IllegalMoveException, interpret_game, '../../resources/game_illegal_move_direction.json')

    def test_illegal_move_obstacle(self):
        # Cannot pass through an obstacle
        self.assertRaises(IllegalMoveException, interpret_game, '../../resources/game_illegal_move_obstacle.json')

    def test_illegal_move_obstacle_oblique(self):
        self.assertRaises(IllegalMoveException, interpret_game,
                          '../../resources/game_illegal_move_obstacle_oblique.json')

    def test_move_no_piece(self):
        self.assertRaises(NoPieceFoundException, interpret_game, '../../resources/game_no_piece.json')

    def test_move_further_from_queen(self):
        self.assertRaises(IllegalMoveException, interpret_game, '../../resources/game_move_further_from_queen.json')


if __name__ == '__main__':
    unittest.main()

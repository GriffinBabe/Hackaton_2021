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
        self.assertRaises(IllegalMove, interpret_game, '../../resources/game_illegal_move_direction.json')

    def test_illegal_move_obstacle(self):
        # Cannot pass through an obstacle
        self.assertRaises(IllegalMove, interpret_game, '../../resources/game_illegal_move_obstacle.json')


if __name__ == '__main__':
    unittest.main()
